#!/usr/bin/env python3
"""
Verify Bluesky handles in the QNFO registry against the live AT Protocol
public API (com.atproto.identity.resolveHandle) — NO authentication needed.

Usage:
    python verify_bsky_handles.py [registry.json]

Updates the "verified" field in-place; prints a summary table.
"""
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

REGISTRY = Path(sys.argv[1] if len(sys.argv) > 1 else
                r"C:\Users\LENOVO\.deepchat\skills\social-media-management\references\qnfo_accounts.json")
PDS = "https://public.api.bsky.app"
DELAY = 0.35  # be polite

def resolve(handle):
    url = f"{PDS}/xrpc/com.atproto.identity.resolveHandle?handle={handle}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read())["did"], None
    except urllib.error.HTTPError as e:
        if e.code == 400:
            return None, "400: invalid handle"
        return None, f"{e.code}"
    except Exception as e:
        return None, str(e)[:60]

def main():
    data = json.loads(REGISTRY.read_text())
    accounts = data["accounts"].get("bluesky", [])
    print(f"Verifying {len(accounts)} Bluesky handles against {PDS}\n")

    ok, bad = 0, 0
    for i, acct in enumerate(accounts):
        handle = acct["handle"]
        did, err = resolve(handle)
        if did:
            acct["verified"] = True
            acct["did"] = did
            ok += 1
            print(f"  [{'OK':>2}] {handle:<42} {did[:28]}...")
        else:
            acct["verified"] = False
            acct.pop("did", None)
            bad += 1
            print(f"  [!!] {handle:<42} NOT FOUND ({err})")
        time.sleep(DELAY)

    REGISTRY.write_text(json.dumps(data, indent=2))
    print(f"\n{ok} verified / {bad} not found / {len(accounts)} total")
    return 0 if bad == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
