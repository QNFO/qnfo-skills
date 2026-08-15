#!/usr/bin/env python3
r"""Bluesky posting — AT Protocol minimal client, zero dependencies.

CREDENTIAL DISCOVERY (auto, never prompts):
1. Environment variables: BSKY_HANDLE, BSKY_APP_PASS
2. keys.json: C:\Users\LENOVO\keys.json
3. .env file: C:\Users\LENOVO\.env
4. .bsky_credentials: C:\Users\LENOVO\.bsky_credentials

Usage:
  python bluesky_post.py post "Your message here"
  python bluesky_post.py thread < thread-content.txt
"""
import json, os, sys, time, urllib.request, urllib.error

BSKY_API = "https://bsky.social/xrpc"

def _req(method, endpoint, body=None, headers=None):
    url = f"{BSKY_API}/{endpoint}"
    data = json.dumps(body).encode() if body else None
    hdrs = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    if headers: hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        raise RuntimeError(f"AT Protocol error: {err.get('message', str(err))}")

def create_session(handle, app_pass):
    return _req("POST", "com.atproto.server.createSession",
                {"identifier": handle, "password": app_pass})

def post_text(session, text, reply_to=None):
    record = {"$type": "app.bsky.feed.post", "text": text,
              "createdAt": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())}
    if reply_to: record["reply"] = reply_to
    headers = {"Authorization": f"Bearer {session['accessJwt']}"}
    return _req("POST", "com.atproto.repo.createRecord",
                {"repo": session["did"], "collection": "app.bsky.feed.post",
                 "record": record}, headers=headers)

def discover_credentials():
    """Auto-discover Bluesky credentials from multiple redundant sources."""
    handle = os.environ.get("BSKY_HANDLE")
    app_pass = os.environ.get("BSKY_APP_PASS")

    # Fallback 1: keys.json
    if not handle or not app_pass:
        try:
            with open(r'C:\Users\LENOVO\keys.json') as f:
                keys = json.load(f)
            handle = handle or keys.get('bluesky_handle')
            app_pass = app_pass or keys.get('bluesky_app_password')
        except Exception: pass

    # Fallback 2: .env file
    if not handle or not app_pass:
        try:
            with open(r'C:\Users\LENOVO\.env') as f:
                for line in f:
                    if line.startswith('BSKY_HANDLE='):
                        handle = handle or line.split('=',1)[1].strip()
                    elif line.startswith('BSKY_APP_PASS='):
                        app_pass = app_pass or line.split('=',1)[1].strip()
        except Exception: pass

    # Fallback 3: .bsky_credentials
    if not handle or not app_pass:
        try:
            with open(r'C:\Users\LENOVO\.bsky_credentials') as f:
                h = f.readline().strip()
                p = f.readline().strip()
                handle = handle or h
                app_pass = app_pass or p
        except Exception: pass

    if not handle or not app_pass:
        print("ERROR: Cannot find Bluesky credentials.", file=sys.stderr)
        print("Create an app password at https://bsky.app/settings/app-passwords", file=sys.stderr)
        sys.exit(1)
    return handle, app_pass

def main():
    handle, app_pass = discover_credentials()
    session = create_session(handle, app_pass)
    print(f"Authenticated as: {session['handle']} (DID: {session['did']})")

    if len(sys.argv) < 2:
        print("Usage: bluesky_post.py post <text>  OR  bluesky_post.py thread < file.txt")
        sys.exit(1)

    subcmd = sys.argv[1]
    if subcmd == "post":
        text = sys.argv[2] if len(sys.argv) > 2 else sys.stdin.read().strip()
        result = post_text(session, text)
        print(f"Posted: {result['uri']}")
    elif subcmd == "thread":
        raw = sys.argv[2:] if len(sys.argv) > 2 else [sys.stdin.read().strip()]
        if not raw[0]: raw = sys.stdin.read().strip().split("---THREAD---")
        else: raw = [r for r in raw if r.strip()]
        posts = [p.strip() for p in raw if p.strip()]
        root_uri = root_cid = parent_uri = parent_cid = None
        for i, pt in enumerate(posts):
            reply = {"root": {"uri": root_uri, "cid": root_cid},
                     "parent": {"uri": parent_uri, "cid": parent_cid}} if i > 0 else None
            result = post_text(session, pt, reply_to=reply)
            uri, cid = result["uri"], result["cid"]
            print(f"Post {i+1}/{len(posts)}: {pt[:60]}... -> {uri}")
            if i == 0: root_uri, root_cid = uri, cid
            parent_uri, parent_cid = uri, cid
            time.sleep(1.5)
    else:
        result = post_text(session, subcmd)
        print(f"Posted: {result['uri']}")

if __name__ == "__main__":
    main()
