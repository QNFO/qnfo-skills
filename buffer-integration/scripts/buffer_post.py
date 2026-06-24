#!/usr/bin/env python3
# buffer_post.py v2.0 — Create and schedule Buffer social media posts
# Uses Buffer GraphQL API (api.buffer.com). Part of the buffer-integration skill.

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

API_URL = "https://api.buffer.com/1/graphql.json"


# ── Token ────────────────────────────────────────────────────────────────────

def load_token() -> str:
    """Load Buffer access token from env var or token file."""
    token = os.environ.get("BUFFER_ACCESS_TOKEN", "")
    if token:
        return token.lstrip("\ufeff").strip()
    token_path = os.path.expandvars(r"%USERPROFILE%\.buffer_token")
    if os.path.exists(token_path):
        with open(token_path, "r", encoding="utf-8-sig") as f:
            return f.read().strip()
    raise FileNotFoundError(
        "[BLOCKED] Buffer token not found.\n"
        "Store at %USERPROFILE%\\.buffer_token or set BUFFER_ACCESS_TOKEN env var.\n"
        "Get token from: https://buffer.com/developers"
    )


# ── GraphQL Helpers ──────────────────────────────────────────────────────────

def _gql_request(query: str, variables: dict = None) -> dict:
    """Send a GraphQL request to the Buffer API."""
    body = {"query": query}
    if variables:
        body["variables"] = variables

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {_gql_request._token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "QNFO-BufferIntegration/2.0")

    try:
        resp = urllib.request.urlopen(req, timeout=20)
        return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        return {"_http_error": e.code, "_body": body_text}


# ── Profile / Channel Queries ────────────────────────────────────────────────

def _get_organization_id(token: str) -> str:
    """Get the first organization ID for the authenticated account."""
    _gql_request._token = token
    result = _gql_request("{ account { organizations { id name channelCount } } }")

    if "_http_error" in result:
        raise ConnectionError(f"Buffer API error ({result['_http_error']}): {result['_body']}")

    orgs = result.get("data", {}).get("account", {}).get("organizations", [])
    if not orgs:
        raise RuntimeError("[BLOCKED] No Buffer organization found. Create one at https://buffer.com.")
    return orgs[0]["id"]


def list_channels(token: str) -> list[dict]:
    """List all social media channels/profiles."""
    _gql_request._token = token
    org_id = _get_organization_id(token)

    query = """
    query($orgId: OrganizationId!) {
      channels(input: { organizationId: $orgId }) {
        id
        service
        name
        displayName
        type
        isDisconnected
        isLocked
      }
    }
    """
    result = _gql_request(query, {"orgId": org_id})

    if "_http_error" in result:
        raise ConnectionError(f"Buffer API error ({result['_http_error']}): {result['_body']}")

    channels = result.get("data", {}).get("channels", [])
    return [
        {
            "id": ch["id"],
            "service": ch["service"],
            "name": ch.get("displayName", ch.get("name", ch["service"])),
            "isDisconnected": ch.get("isDisconnected", False),
            "isLocked": ch.get("isLocked", False),
        }
        for ch in channels
    ]


# ── Post Creation ────────────────────────────────────────────────────────────

def create_post(
    token: str,
    channel_id: str,
    text: str,
    link_url: str = None,
    schedule_at: str = None,
    now: bool = False,
    service: str = "",
) -> dict:
    """Create a social media post via Buffer GraphQL API.

    Returns dict with keys: success, post_id, status, error, due_at
    """
    _gql_request._token = token

    # Determine scheduling mode
    if now:
        mode = "shareNow"
        scheduling_type = "automatic"
        due_at = None
    elif schedule_at:
        mode = "customScheduled"
        scheduling_type = "automatic"
        due_at = schedule_at
    else:
        mode = "addToQueue"
        scheduling_type = "automatic"
        due_at = None

    # Build input
    post_input = {
        "channelId": channel_id,
        "text": text,
        "schedulingType": scheduling_type,
        "mode": mode,
        "assets": [],
    }

    if due_at:
        post_input["dueAt"] = due_at

    # Add link attachment via metadata if link_url provided
    if link_url and service:
        meta_key = service  # "twitter", "linkedin", "bluesky"
        post_input["metadata"] = {
            meta_key: {"linkAttachment": {"url": link_url}}
        }

    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post { id status text dueAt channelId }
        }
        ... on InvalidInputError { message }
        ... on LimitReachedError { message }
        ... on UnauthorizedError { message }
        ... on NotFoundError { message }
      }
    }
    """
    result = _gql_request(mutation, {"input": post_input})

    if "_http_error" in result:
        return {
            "success": False,
            "post_id": "",
            "status": "error",
            "error": f"HTTP {result['_http_error']}: {result['_body'][:200]}",
            "due_at": None,
        }

    post_result = result.get("data", {}).get("createPost", {})

    if "post" in post_result:
        post = post_result["post"]
        return {
            "success": True,
            "post_id": post["id"],
            "status": post.get("status", "unknown"),
            "error": "",
            "due_at": post.get("dueAt"),
        }
    else:
        return {
            "success": False,
            "post_id": "",
            "status": "failed",
            "error": post_result.get("message", "Unknown error"),
            "due_at": None,
        }


# ── Text Formatting ──────────────────────────────────────────────────────────

def format_for_channel(
    service: str,
    title: str,
    doi: str = "",
    finding: str = "",
    url: str = "",
    custom: str = "",
) -> str:
    """Generate channel-optimized post text."""
    if custom:
        return custom

    link = url or (f"https://doi.org/{doi}" if doi else "[link pending]")
    short_title = title[:100] + "..." if len(title) > 100 else title
    finding_text = finding or "Published on QNFO/QWAV via Zenodo."

    if service == "twitter":
        text = f"New research: {short_title}\nKey finding: {finding_text}\nFull paper: {link}"
        return text[:280]
    elif service == "linkedin":
        return f"New Research Publication: {title}\n\n{finding_text}\n\nRead: {link}"
    elif service == "bluesky":
        return f"New QNFO/QWAV research: {title}\n\n{finding_text}\n\nRead: {link}"
    else:
        return f"{title}\n\n{finding_text}\n\n{link}"


def stagger_schedule(base: datetime, idx: int) -> str:
    """Stagger posts by 2-4 hours between channels."""
    hours = 2 + idx * 2
    scheduled = base + timedelta(hours=hours)
    return scheduled.strftime("%Y-%m-%dT%H:%M:%SZ")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Create and schedule Buffer social media posts (GraphQL API v2)"
    )
    parser.add_argument("--title", "-t", required=False, default="Test Post",
                        help="Publication title")
    parser.add_argument("--doi", "-d", default="", help="Zenodo DOI")
    parser.add_argument("--url", "-u", default="", help="Publication page URL")
    parser.add_argument("--finding", "-f", default="", help="Key finding (one sentence)")
    parser.add_argument("--text", default="", help="Custom text (overrides auto-format)")
    parser.add_argument(
        "--channels", default="twitter,linkedin,bluesky",
        help="Comma-separated channels (twitter, linkedin, bluesky)"
    )
    parser.add_argument("--now", action="store_true", help="Post immediately")
    parser.add_argument("--schedule-for", default="",
                        help="Schedule for specific ISO datetime (e.g. 2026-06-25T09:00:00Z)")
    parser.add_argument("--list", action="store_true", help="List channels only, don't post")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview posts without creating them")
    args = parser.parse_args()

    # ── Load token ──
    try:
        token = load_token()
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1

    # ── List channels ──
    try:
        channels = list_channels(token)
    except Exception as e:
        print(f"[ERROR] Failed to list channels: {e}", file=sys.stderr)
        return 1

    if args.list:
        print(f"Buffer Channels ({len(channels)}):")
        for ch in channels:
            status = ""
            if ch["isDisconnected"]:
                status = " [DISCONNECTED]"
            if ch["isLocked"]:
                status = " [LOCKED]"
            print(f"  [{ch['service']:>10}] {ch['name']:<30} (ID: {ch['id']}){status}")
        return 0

    # ── Filter by requested services ──
    requested = [c.strip().lower() for c in args.channels.split(",")]
    targets = [ch for ch in channels if ch["service"] in requested and not ch["isDisconnected"]]

    if not targets:
        available = [ch["service"] for ch in channels if not ch["isDisconnected"]]
        print(f"[BLOCKED] No active channels for: {requested}")
        print(f"Available: {available}")
        return 1

    # Warn about disconnected channels
    disconnected = [ch for ch in channels if ch["service"] in requested and ch["isDisconnected"]]
    for dc in disconnected:
        print(f"[WARN] Channel {dc['service']} ({dc['name']}) is disconnected — skipping.")

    # ── Post to each channel ──
    results = []
    for i, ch in enumerate(targets):
        text = format_for_channel(
            service=ch["service"],
            title=args.title,
            doi=args.doi,
            finding=args.finding,
            url=args.url,
            custom=args.text,
        )

        # Determine schedule time
        if args.now:
            sched = None
        elif args.schedule_for:
            sched = args.schedule_for
        else:
            sched = stagger_schedule(datetime.now(timezone.utc), i)

        link_url = args.url or (f"https://doi.org/{args.doi}" if args.doi else None)

        if args.dry_run:
            print(f"\n[Dry Run] {ch['service']} ({ch['name']}):")
            print(f"  Text: {text[:120]}...")
            print(f"  Link: {link_url or 'none'}")
            print(f"  Schedule: {sched or 'now'}")
            continue

        result = create_post(
            token=token,
            channel_id=ch["id"],
            text=text,
            link_url=link_url,
            schedule_at=sched,
            now=args.now,
            service=ch["service"],
        )

        if result["success"]:
            status_str = f"[OK] Created (status: {result['status']})"
        else:
            status_str = f"[FAIL] {result['error']}"

        results.append({
            "channel": ch["service"],
            "profile": ch["name"],
            "success": result["success"],
            "post_id": result["post_id"],
            "status": result["status"],
            "error": result["error"],
            "scheduled_at": sched or result.get("due_at", "now"),
        })

        print(f"  [{ch['service']:>10}] {status_str} (ID: {result['post_id'] or 'N/A'})")

    # ── Summary ──
    successes = sum(1 for r in results if r["success"])
    print(f"\n[SUMMARY] {successes}/{len(results)} posts created")
    if not args.now and not args.dry_run and results:
        first_sched = results[0].get("scheduled_at", "N/A")
        print(f"[SCHEDULED] First post at: {first_sched}")

    return 0 if successes == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
