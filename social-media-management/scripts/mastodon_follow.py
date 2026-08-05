#!/usr/bin/env python3
"""
Mastodon Follow Automation — REST API
======================================
Manages follows on Mastodon using the standard REST API with OAuth 2.0.

Usage:
    python mastodon_follow.py follow @user@instance.social
    python mastodon_follow.py bulk accounts.json
    python mastodon_follow.py unfollow @user@instance.social
    python mastodon_follow.py list-following
    python mastodon_follow.py auth          # Interactive OAuth setup

Environment variables (or .env file):
    MASTODON_INSTANCE    — your Mastodon instance (e.g. "mastodon.social")
    MASTODON_TOKEN       — OAuth access token (set by `auth` command)
    MASTODON_CLIENT_ID   — OAuth client ID (set by `auth` command)
    MASTODON_CLIENT_SECRET — OAuth client secret (set by `auth` command)
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import webbrowser
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────
MASTODON_INSTANCE = os.environ.get("MASTODON_INSTANCE", "")
MASTODON_TOKEN = os.environ.get("MASTODON_TOKEN", "")
MASTODON_CLIENT_ID = os.environ.get("MASTODON_CLIENT_ID", "")
MASTODON_CLIENT_SECRET = os.environ.get("MASTODON_CLIENT_SECRET", "")
CREDS_FILE = Path(os.environ.get("MASTODON_CREDS_FILE", Path.home() / ".mastodon_creds.json"))
STATE_FILE = Path(os.environ.get("MASTODON_STATE_FILE", Path.home() / ".mastodon_follow_state.json"))
RATE_LIMIT_DELAY = float(os.environ.get("MASTODON_RATE_LIMIT_DELAY", "1.5"))


def load_env():
    """Load credentials from .env file."""
    global MASTODON_INSTANCE, MASTODON_TOKEN, MASTODON_CLIENT_ID, MASTODON_CLIENT_SECRET
    env_file = Path(".env")
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                for var in ["MASTODON_INSTANCE", "MASTODON_TOKEN",
                           "MASTODON_CLIENT_ID", "MASTODON_CLIENT_SECRET"]:
                    if k == var:
                        globals()[var] = globals()[var] or v


def load_creds():
    """Load credentials from JSON creds file."""
    global MASTODON_TOKEN, MASTODON_CLIENT_ID, MASTODON_CLIENT_SECRET, MASTODON_INSTANCE
    if CREDS_FILE.exists():
        c = json.loads(CREDS_FILE.read_text())
        MASTODON_INSTANCE = MASTODON_INSTANCE or c.get("instance", "")
        MASTODON_TOKEN = MASTODON_TOKEN or c.get("token", "")
        MASTODON_CLIENT_ID = MASTODON_CLIENT_ID or c.get("client_id", "")
        MASTODON_CLIENT_SECRET = MASTODON_CLIENT_SECRET or c.get("client_secret", "")


def save_creds():
    """Save credentials to JSON creds file."""
    CREDS_FILE.write_text(json.dumps({
        "instance": MASTODON_INSTANCE,
        "token": MASTODON_TOKEN,
        "client_id": MASTODON_CLIENT_ID,
        "client_secret": MASTODON_CLIENT_SECRET,
    }, indent=2))


# ── Mastodon API Client ──────────────────────────────────────────────

class MastodonClient:
    """Minimal Mastodon REST API client for follow management."""

    def __init__(self, instance: str, token: str):
        self.instance = instance.rstrip("/")
        self.token = token
        self.base = f"https://{self.instance}"
        # Verify credentials
        me = self._req("GET", "/api/v1/accounts/verify_credentials")
        self.user_id = me["id"]
        self.username = me["username"]
        print(f"✓ Authenticated as @{self.username}@{self.instance} (ID: {self.user_id})")

    def _req(self, method: str, path: str, body: dict = None) -> dict:
        """Send a request to the Mastodon API."""
        url = f"{self.base}{path}"
        data = json.dumps(body).encode() if body else None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            raise RuntimeError(f"Mastodon API error ({e.code}): {error_body}")

    def resolve_account(self, handle: str) -> dict:
        """Resolve a handle like @user@instance.social to an account object."""
        # Handle format: @user@instance.social or user@instance.social
        handle = handle.lstrip("@")
        if "@" in handle:
            # Full handle — search by acct
            resp = self._req("GET", f"/api/v2/search?q={urllib.parse.quote(handle)}&type=accounts&limit=5&resolve=true")
            for acct in resp.get("accounts", []):
                if acct["acct"].lower() == handle.lower():
                    return acct
            raise RuntimeError(f"Account not found: {handle}")
        else:
            # Local handle (same instance)
            resp = self._req("GET", f"/api/v1/accounts/lookup?acct={urllib.parse.quote(handle)}")
            return resp

    def follow(self, target: str) -> dict:
        """Follow an account by handle.

        Args:
            target: Mastodon handle (e.g. "@user@instance.social" or "user@instance.social")
        Returns:
            Relationship object from the API
        """
        account = self.resolve_account(target)
        print(f"  Resolved {target} → @{account['acct']} (ID: {account['id']})")
        resp = self._req("POST", f"/api/v1/accounts/{account['id']}/follow", {
            "reblogs": True,
            "notify": False,
        })
        return resp

    def unfollow(self, target: str) -> dict:
        """Unfollow an account by handle."""
        account = self.resolve_account(target)
        resp = self._req("POST", f"/api/v1/accounts/{account['id']}/unfollow")
        return resp

    def list_following(self, limit: int = 80) -> list:
        """List accounts you follow."""
        resp = self._req("GET", f"/api/v1/accounts/{self.user_id}/following?limit={limit}")
        return resp


# ── OAuth Authentication Flow ─────────────────────────────────────────

def cmd_auth(args: list):
    """Interactive OAuth setup for Mastodon."""
    global MASTODON_INSTANCE, MASTODON_CLIENT_ID, MASTODON_CLIENT_SECRET, MASTODON_TOKEN

    instance = args[0] if args else input("Mastodon instance (e.g. mastodon.social): ").strip()
    if not instance:
        print("Instance is required.")
        sys.exit(1)

    MASTODON_INSTANCE = instance
    base = f"https://{instance}"

    # Step 1: Register OAuth app
    app_data = {
        "client_name": "DeepChat Social Manager",
        "redirect_uris": "urn:ietf:wg:oauth:2.0:oob",
        "scopes": "read write follow",
        "website": "https://deepchat.ai",
    }

    req = urllib.request.Request(
        f"{base}/api/v1/apps",
        data=json.dumps(app_data).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        app = json.loads(resp.read())

    MASTODON_CLIENT_ID = app["client_id"]
    MASTODON_CLIENT_SECRET = app["client_secret"]
    print(f"✓ App registered (client_id: {MASTODON_CLIENT_ID[:20]}...)")

    # Step 2: Get authorization code
    auth_url = (f"{base}/oauth/authorize"
                f"?client_id={MASTODON_CLIENT_ID}"
                f"&redirect_uri=urn:ietf:wg:oauth:2.0:oob"
                f"&response_type=code"
                f"&scope=read+write+follow")

    print(f"\nOpening browser to authorize...")
    print(f"If browser doesn't open, visit:\n  {auth_url}")
    webbrowser.open(auth_url)

    code = input("\nPaste the authorization code here: ").strip()
    if not code:
        print("Authorization code is required.")
        sys.exit(1)

    # Step 3: Exchange code for access token
    token_data = urllib.parse.urlencode({
        "client_id": MASTODON_CLIENT_ID,
        "client_secret": MASTODON_CLIENT_SECRET,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "authorization_code",
        "code": code,
        "scope": "read write follow",
    }).encode()

    req = urllib.request.Request(
        f"{base}/oauth/token",
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req) as resp:
        token_resp = json.loads(resp.read())

    MASTODON_TOKEN = token_resp["access_token"]
    save_creds()
    print(f"✓ Token obtained and saved to {CREDS_FILE}")

    # Verify
    client = MastodonClient(instance, MASTODON_TOKEN)
    print(f"✓ Authenticated as @{client.username}@{instance}")


# ── State Management ──────────────────────────────────────────────────

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"followed": {}, "failed": {}}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ── CLI ───────────────────────────────────────────────────────────────

def cmd_follow(client: MastodonClient, args: list):
    if not args:
        print("Usage: mastodon_follow.py follow @user@instance.social")
        sys.exit(1)
    target = args[0]
    try:
        resp = client.follow(target)
        print(f"✓ Now following: @{resp.get('acct', target)}")
    except RuntimeError as e:
        print(f"✗ Failed: {e}")
        sys.exit(1)


def cmd_bulk(client: MastodonClient, args: list):
    if not args:
        print("Usage: mastodon_follow.py bulk accounts.json")
        sys.exit(1)

    path = Path(args[0])
    if path.suffix == ".json":
        data = json.loads(path.read_text())
        if isinstance(data, list):
            handles = data
        elif "mastodon" in data:
            handles = [a["handle"] for a in data.get("mastodon", [])]
        else:
            handles = data.get("accounts", data.get("handles", []))
    else:
        handles = path.read_text().strip().splitlines()

    if not handles:
        print("No handles found.")
        sys.exit(1)

    state = load_state()
    success, failed, skipped = 0, 0, 0

    for i, handle in enumerate(handles):
        handle = handle.strip()
        if not handle or handle.startswith("#"):
            continue

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

        if i < len(handles) - 1:
            time.sleep(RATE_LIMIT_DELAY)

    save_state(state)
    print(f"\nDone: {success} followed, {failed} failed, {skipped} skipped (of {len(handles)})")


def cmd_unfollow(client: MastodonClient, args: list):
    if not args:
        print("Usage: mastodon_follow.py unfollow @user@instance.social")
        sys.exit(1)
    target = args[0]
    try:
        client.unfollow(target)
        print(f"✓ Unfollowed: {target}")
        state = load_state()
        state["followed"].pop(target, None)
        save_state(state)
    except RuntimeError as e:
        print(f"✗ Failed: {e}")
        sys.exit(1)


def cmd_list_following(client: MastodonClient, args: list):
    following = client.list_following(limit=80)
    print(f"Following {len(following)} accounts:\n")
    for acct in sorted(following, key=lambda a: a.get("acct", "")):
        print(f"  @{acct['acct']:<40} {acct.get('display_name', '')}")


def main():
    load_env()
    load_creds()

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "auth":
        cmd_auth(args)
        return

    if not MASTODON_TOKEN or not MASTODON_INSTANCE:
        print("ERROR: Run 'mastodon_follow.py auth' first to set up OAuth.")
        sys.exit(1)

    client = MastodonClient(MASTODON_INSTANCE, MASTODON_TOKEN)

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
