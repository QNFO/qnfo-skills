#!/usr/bin/env python3
"""
Buffer GraphQL Post Publisher (v1.0 — 2026-07-22)
==================================================
Canonical script for publishing social media posts via Buffer's GraphQL API.

Usage:
    python buffer-post.py <text-file|inline-text> --platforms twitter,linkedin,bluesky [--dry-run]

Environment:
    BUFFER_TOKEN — Buffer Personal Access Token (43 chars, suffix 14Ky)
                   Stored at %USERPROFILE%\buffer\token

Endpoint: https://api.buffer.com/graphql
Mutation: createPost (NOT deprecated createDraft)

Verified live 2026-07-22 with 3-channel posting for IQM/DB critique.
"""
import urllib.request, json, os, sys, argparse
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────
URL = "https://api.buffer.com/graphql"
TOKEN = os.environ.get("BUFFER_TOKEN") or open(Path.home() / "buffer" / "token", "rb").read().strip().decode()
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# ── Channel Discovery (always live, never hardcoded) ─────────────────
def discover_channels():
    """Discover live channel IDs via GraphQL API. Returns {service: id}."""
    # Step 1: Get organization ID
    query = json.dumps({"query": "query { account { organizations { id } } }"}).encode()
    req = urllib.request.Request(URL, data=query, headers=HEADERS, method="POST")
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    orgs = data["data"]["account"]["organizations"]
    if not orgs:
        raise RuntimeError("No organizations found — token may lack permissions")
    org_id = orgs[0]["id"]
    
    # Step 2: Get channels
    query = json.dumps({
        "query": f'query {{ channels(input: {{ organizationId: "{org_id}" }}) {{ id name service }} }}'
    }).encode()
    req = urllib.request.Request(URL, data=query, headers=HEADERS, method="POST")
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    channels = {c["service"].lower(): c["id"] for c in data["data"]["channels"]}
    return channels


# ── Post Creation ───────────────────────────────────────────────────
def create_post(channel_id: str, text: str, dry_run: bool = False) -> dict:
    """Publish a single post via Buffer createPost mutation.
    
    Args:
        channel_id: Live channel ID from discover_channels()
        text: Post body text (Buffer auto-shortens URLs)
        dry_run: If True, only validate and print — don't actually post
    
    Returns:
        dict with keys: ok, typename, error (if any)
    """
    # Escape text for GraphQL inline string
    text_escaped = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    
    mutation = f"""
    mutation {{
      createPost(input: {{
        channelId: "{channel_id}",
        text: "{text_escaped}",
        schedulingType: automatic,
        mode: addToQueue,
        assets: [],
        saveToDraft: false
      }}) {{
        __typename
      }}
    }}
    """
    
    if dry_run:
        return {"ok": True, "typename": "DRY_RUN", "text_len": len(text)}
    
    body = json.dumps({"query": mutation}).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers=HEADERS, method="POST")
    resp = urllib.request.urlopen(req, timeout=20)
    data = json.loads(resp.read().decode("utf-8"))
    
    result = data.get("data", {}).get("createPost", {})
    typename = result.get("__typename", "NO_TYPENAME")
    
    if typename and "Error" not in typename:
        return {"ok": True, "typename": typename, "text_len": len(text)}
    elif "errors" in data:
        err_msg = data["errors"][0].get("message", "Unknown GraphQL error")
        return {"ok": False, "typename": typename, "error": err_msg}
    else:
        return {"ok": False, "typename": typename, "error": json.dumps(data)}


# ── Main ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Publish social media posts via Buffer GraphQL API")
    parser.add_argument("text", help="Post text (inline) or path to text file")
    parser.add_argument("--platforms", default="twitter,linkedin,bluesky",
                        help="Comma-separated platform names (twitter, linkedin, bluesky)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate without posting")
    parser.add_argument("--list-channels", action="store_true",
                        help="Only list available channels and exit")
    args = parser.parse_args()
    
    # Discover channels
    try:
        channels = discover_channels()
    except Exception as e:
        print(f"FATAL: Failed to discover channels: {e}")
        print("Check: BUFFER_TOKEN env var or %USERPROFILE%\\buffer\\token")
        sys.exit(1)
    
    if args.list_channels:
        print("=== Available Channels ===")
        for svc, cid in channels.items():
            print(f"  {svc}: {cid}")
        return
    
    # Read text
    text_path = Path(args.text)
    if text_path.exists():
        with open(text_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
    else:
        text = args.text
    
    # Determine target platforms
    targets = [p.strip().lower() for p in args.platforms.split(",")]
    unknown = [t for t in targets if t not in channels]
    if unknown:
        print(f"WARNING: Unknown platforms: {', '.join(unknown)}. Available: {list(channels.keys())}")
        targets = [t for t in targets if t in channels]
    
    if not targets:
        print("ERROR: No valid platforms to post to")
        sys.exit(1)
    
    # Post to each platform
    results = {}
    for platform in targets:
        ch_id = channels[platform]
        print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Posting to {platform} (channel: {ch_id[:8]}...)...")
        try:
            result = create_post(ch_id, text, dry_run=args.dry_run)
            results[platform] = result
            if result["ok"]:
                print(f"  ✅ {result['typename']} ({result['text_len']} chars)")
            else:
                print(f"  ❌ {result.get('typename', '?')}: {result.get('error', '?')[:150]}")
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            results[platform] = {"ok": False, "error": f"HTTP {e.code}: {body}"}
            print(f"  ❌ HTTP {e.code}: {body[:150]}")
        except Exception as e:
            results[platform] = {"ok": False, "error": str(e)}
            print(f"  ❌ {e}")
    
    # Summary
    print(f"\n{'=' * 50}")
    success = all(r["ok"] for r in results.values())
    for p, r in results.items():
        s = "✅" if r["ok"] else "❌"
        detail = r.get("typename", r.get("error", "?"))[:80]
        print(f"  {s} {p}: {detail}")
    
    if success:
        print(f"\n🎉 All {len(results)} posts {'validated' if args.dry_run else 'published'} successfully!")
    else:
        failed = [p for p, r in results.items() if not r["ok"]]
        print(f"\n⚠️  Failed: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
