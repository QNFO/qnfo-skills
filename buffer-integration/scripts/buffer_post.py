#!/usr/bin/env python3
# buffer_post.py v1.0 -- Create and schedule Buffer social media posts
# Part of the buffer-integration skill. Usage: python buffer_post.py --title "TITLE" --doi "DOI"

import argparse, json, os, sys, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

def load_token() -> str:
    token = os.environ.get("BUFFER_ACCESS_TOKEN", "")
    if token: return token
    token_path = os.path.expandvars(r"%USERPROFILE%\.buffer_token")
    if os.path.exists(token_path):
        with open(token_path, "r") as f: return f.read().strip()
    raise FileNotFoundError("[BLOCKED] Buffer token not found. Store at %USERPROFILE%\\.buffer_token or set BUFFER_ACCESS_TOKEN env var.")

def list_profiles(token: str) -> list[dict]:
    req = urllib.request.Request("https://api.bufferapp.com/1/profiles.json")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("User-Agent", "QNFO-BufferIntegration/1.0")
    profiles = json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))
    return [{"id": p["id"], "service": p["service"], "name": p.get("formatted_username", p["service"]), "timezone": p.get("timezone", "UTC")} for p in profiles]

def create_update(token: str, profile_id: str, text: str, link_url: str = None, schedule_at: str = None, now: bool = False) -> dict:
    params = {"profile_ids[]": profile_id, "text": text}
    if link_url: params["media[link]"] = link_url
    if now: params["now"] = "true"
    elif schedule_at: params["scheduled_at"] = schedule_at
    else: params["schedulingType"] = "notification"
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request("https://api.bufferapp.com/1/updates/create.json", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", "QNFO-BufferIntegration/1.0")
    result = json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))
    success = result.get("success", False)
    return {"success": success, "post_id": result.get("buffer_count") or result.get("id", ""), "error": result.get("message", "") if not success else ""}

def format_for_channel(service: str, title: str, doi: str = "", finding: str = "", url: str = "", custom: str = "") -> str:
    if custom: return custom
    templates = {"twitter": "New research: {title}\nKey finding: {finding}\nFull paper: {link}", "linkedin": "New Research Publication: {title}\n\n{finding}\n\nRead: {link}", "bluesky": "New QNFO/QWAV research: {title}\n\n{finding}\n\nRead: {link}"}
    tmpl = templates.get(service, templates["twitter"])
    short = title[:100] + "..." if len(title) > 100 else title
    link = url or (f"https://doi.org/{doi}" if doi else "[link pending]")
    return tmpl.format(title=short, finding=finding or "Published on QNFO/QWAV via Zenodo.", link=link)

def stagger(base: datetime, idx: int) -> str: return (base + timedelta(hours=2+idx*2)).isoformat()

def main():
    p = argparse.ArgumentParser(description="Create and schedule Buffer posts")
    p.add_argument("--title", "-t", required=True); p.add_argument("--doi", "-d", default="")
    p.add_argument("--url", "-u", default=""); p.add_argument("--finding", "-f", default="")
    p.add_argument("--text", default=""); p.add_argument("--channels", default="twitter,linkedin,bluesky")
    p.add_argument("--now", action="store_true"); p.add_argument("--schedule-for", default="")
    p.add_argument("--list", action="store_true"); p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    token = load_token()
    profiles = list_profiles(token)
    if args.list:
        print(f"Buffer Profiles ({len(profiles)}):")
        for pr in profiles: print(f"  [{pr['service']}] {pr['name']} (ID: {pr['id']})")
        return
    channels = [c.strip().lower() for c in args.channels.split(",")]
    targets = [pr for pr in profiles if pr["service"] in channels]
    if not targets:
        print(f"[BLOCKED] No profiles for: {channels}. Available: {[pr['service'] for pr in profiles]}")
        return
    results = []
    for i, pr in enumerate(targets):
        text = format_for_channel(pr["service"], args.title, args.doi, args.finding, args.url, args.text)
        sched = stagger(datetime.now(timezone.utc), i) if not args.now and not args.schedule_for else (args.schedule_for or None)
        if args.dry_run:
            print(f"\n[Dry Run] {pr['service']} ({pr['name']}):\n  {text[:100]}...\n  Schedule: {sched or 'now'}")
            continue
        result = create_update(token, pr["id"], text, args.url or f"https://doi.org/{args.doi}" if args.doi else None, sched, args.now)
        status = "Created" if result["success"] else f"Failed: {result['error']}"
        results.append({"channel": pr["service"], "profile": pr["name"], "status": status, "post_id": result.get("post_id", ""), "scheduled_at": sched})
        print(f"  [{pr['service']}] {status} (ID: {result.get('post_id', 'N/A')})")
    successes = sum(1 for r in results if "Created" in r["status"])
    print(f"\n[SUMMARY] {successes}/{len(results)} posts created")
    if not args.now and not args.dry_run and results: print(f"[SCHEDULED] First at: {results[0]['scheduled_at']}")

if __name__ == "__main__": main()
