#!/usr/bin/env python3
"""
Bluesky Follow Automation — AT Protocol API
=============================================
Manages follows on Bluesky using the AT Protocol API with app-password auth.

Usage:
    python bluesky_follow.py follow @handle.bsky.social
    python bluesky_follow.py bulk accounts.json
    python bluesky_follow.py unfollow @handle.bsky.social
    python bluesky_follow.py list-following

Environment variables (or .env file):
    BSKY_HANDLE     — your Bluesky handle (e.g. "you.bsky.social")
    BSKY_APP_PASS   — app-specific password (NOT your account password)
                       Create at: https://bsky.app/settings/app-passwords
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────
BSKY_PDS = os.environ.get("BSKY_PDS", "https://bsky.social")
BSKY_HANDLE = os.environ.get("BSKY_HANDLE")
BSKY_APP_PASS = os.environ.get("BSKY_APP_PASS")
STATE_FILE = Path(os.environ.get("BSKY_STATE_FILE", Path.home() / ".bsky_follow_state.json"))
RATE_LIMIT_DELAY = float(os.environ.get("BSKY_RATE_LIMIT_DELAY", "1.0"))  # seconds between follows


def load_env():
    """Load credentials from .env file if not in environment."""
    global BSKY_HANDLE, BSKY_APP_PASS
    env_file = Path(".env")
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k == "BSKY_HANDLE":
                    BSKY_HANDLE = BSKY_HANDLE or v
                elif k == "BSKY_APP_PASS":
                    BSKY_APP_PASS = BSKY_APP_PASS or v


# ── AT Protocol Client ────────────────────────────────────────────────

class BlueskyClient:
    """Minimal AT Protocol client for Bluesky follow management."""

    def __init__(self, handle: str, app_password: str, pds: str = BSKY_PDS):
        self.pds = pds.rstrip("/")
        self.handle = handle
        self.session = None
        self._auth(handle, app_password)

    def _req(self, method: str, path: str, body: dict = None) -> dict:
        """Send an XRPC request to the PDS."""
        url = f"{self.pds}/xrpc/{path}"
        data = json.dumps(body).encode() if body else None
        headers = {"Content-Type": "application/json"}
        if self.session:
            headers["Authorization"] = f"Bearer {self.session['accessJwt']}"

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            raise RuntimeError(f"AT Protocol error ({e.code}): {error_body}")

    def _auth(self, handle: str, app_password: str):
        """Create a session with handle + app password."""
        resp = self._req("POST", "com.atproto.server.createSession", {
            "identifier": handle,
            "password": app_password,
        })
        self.session = resp
        self.did = resp["did"]
        print(f"✓ Authenticated as @{handle} (DID: {self.did})")

    def resolve_handle(self, handle: str) -> str:
        """Resolve a handle to a DID."""
        resp = self._req("GET", f"com.atproto.identity.resolveHandle?handle={handle}")
        return resp["did"]

    def follow(self, target: str) -> dict:
        """Follow an account by handle or DID.

        Args:
            target: Bluesky handle (e.g. "user.bsky.social") or DID
        Returns:
            AT Protocol response with uri and cid of the follow record
        """
        # Resolve handle to DID if needed
        if target.startswith("did:"):
            target_did = target
        else:
            target_did = self.resolve_handle(target)
            print(f"  Resolved {target} → {target_did}")

        record = {
            "$type": "app.bsky.graph.follow",
            "subject": target_did,
            "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        }

        resp = self._req("POST", "com.atproto.repo.createRecord", {
            "repo": self.did,
            "collection": "app.bsky.graph.follow",
            "record": record,
        })
        return resp

    def unfollow(self, target: str) -> dict:
        """Unfollow an account by handle or DID.

        First looks up the follow record URI, then deletes it.
        """
        if target.startswith("did:"):
            target_did = target
        else:
            target_did = self.resolve_handle(target)

        # Find the follow record
        follows = self._req("GET", f"com.atproto.repo.listRecords"
                            f"?repo={self.did}"
                            f"&collection=app.bsky.graph.follow"
                            f"&limit=100")

        rkey = None
        for rec in follows.get("records", []):
            if rec["value"].get("subject") == target_did:
                rkey = rec["uri"].split("/")[-1]
                break

        if not rkey:
            raise RuntimeError(f"Not following {target} — no follow record found")

        resp = self._req("POST", "com.atproto.repo.deleteRecord", {
            "repo": self.did,
            "collection": "app.bsky.graph.follow",
            "rkey": rkey,
        })
        return resp

    def list_following(self, limit: int = 100, cursor: str = None) -> list:
        """List accounts you follow."""
        params = f"?repo={self.did}&collection=app.bsky.graph.follow&limit={limit}"
        if cursor:
            params += f"&cursor={cursor}"
        resp = self._req("GET", f"com.atproto.repo.listRecords{params}")
        return resp.get("records", [])

    def get_profile(self, actor: str) -> dict:
        """Get a profile by handle or DID."""
        if actor.startswith("did:"):
            did = actor
        else:
            did = self.resolve_handle(actor)
        return self._req("GET", f"app.bsky.actor.getProfile?actor={did}")


# ── State Management ──────────────────────────────────────────────────

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"followed": {}, "failed": {}}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ── CLI ───────────────────────────────────────────────────────────────

def cmd_follow(client: BlueskyClient, args: list):
    """Follow a single account."""
    if not args:
        print("Usage: bluesky_follow.py follow @handle.bsky.social")
        sys.exit(1)
    target = args[0]
    try:
        resp = client.follow(target)
        print(f"✓ Now following: {target}")
        print(f"  Record: {resp['uri']}")
    except RuntimeError as e:
        print(f"✗ Failed: {e}")
        sys.exit(1)


def cmd_bulk(client: BlueskyClient, args: list):
    """Bulk follow from a JSON file or list of handles."""
    if not args:
        print("Usage: bluesky_follow.py bulk accounts.json")
        sys.exit(1)

    # Load accounts
    path = Path(args[0])
    if path.suffix == ".json":
        data = json.loads(path.read_text())
        # Support multiple formats
        if isinstance(data, list):
            handles = data
        elif "bluesky" in data:
            handles = [a["handle"] for a in data.get("bluesky", [])]
        else:
            handles = data.get("accounts", data.get("handles", []))
    else:
        handles = path.read_text().strip().splitlines()

    if not handles:
        print("No handles found in input file.")
        sys.exit(1)

    # Load previous state
    state = load_state()
    success, failed, skipped = 0, 0, 0

    for i, handle in enumerate(handles):
        handle = handle.strip()
        if not handle or handle.startswith("#"):
            continue

        # Skip already followed
        if handle in state["followed"]:
            print(f"  [{i+1}/{len(handles)}] ⏭ {handle} (already followed)")
            skipped += 1
            continue

        print(f"  [{i+1}/{len(handles)}] → {handle} ...", end=" ", flush=True)
        try:
            client.follow(handle)
            state["followed"][handle] = datetime.now(timezone.utc).isoformat()
            print("✓")
            success += 1
        except RuntimeError as e:
            state["failed"][handle] = str(e)
            print(f"✗ {e}")
            failed += 1

        # Rate limit delay
        if i < len(handles) - 1:
            time.sleep(RATE_LIMIT_DELAY)

    save_state(state)
    print(f"\nDone: {success} followed, {failed} failed, {skipped} skipped (of {len(handles)})")


def cmd_unfollow(client: BlueskyClient, args: list):
    """Unfollow an account."""
    if not args:
        print("Usage: bluesky_follow.py unfollow @handle.bsky.social")
        sys.exit(1)
    target = args[0]
    try:
        client.unfollow(target)
        print(f"✓ Unfollowed: {target}")
        # Update state
        state = load_state()
        state["followed"].pop(target, None)
        save_state(state)
    except RuntimeError as e:
        print(f"✗ Failed: {e}")
        sys.exit(1)


def cmd_list_following(client: BlueskyClient, args: list):
    """List followed accounts."""
    records = client.list_following(limit=100)
    print(f"Following {len(records)} accounts:\n")
    for rec in records:
        subj = rec["value"].get("subject", "unknown")
        print(f"  {subj}")


def main():
    load_env()

    if not BSKY_HANDLE or not BSKY_APP_PASS:
        print("ERROR: Set BSKY_HANDLE and BSKY_APP_PASS environment variables.")
        print("  Create an app password at: https://bsky.app/settings/app-passwords")
        sys.exit(1)

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    client = BlueskyClient(BSKY_HANDLE, BSKY_APP_PASS)

    commands = {
        "follow": cmd_follow,
        "bulk": cmd_bulk,
        "unfollow": cmd_unfollow,
        "list-following": cmd_list_following,
    }

    if command in commands:
        commands[command](client, args)
    else:
        print(f"Unknown command: {command}")
        print(f"Available: {', '.join(commands.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
