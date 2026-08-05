#!/usr/bin/env python3
"""
Social Follow — Unified CLI for Bluesky & Mastodon Follow Management
=====================================================================
Single entry point for managing social media follows across platforms.

Usage:
    python social_follow.py bluesky follow @handle.bsky.social
    python social_follow.py bluesky bulk qnfo_accounts.json
    python social_follow.py bluesky unfollow @handle.bsky.social
    python social_follow.py bluesky list-following

    python social_follow.py mastodon auth
    python social_follow.py mastodon follow @user@instance.social
    python social_follow.py mastodon bulk qnfo_accounts.json
    python social_follow.py mastodon list-following

    python social_follow.py all              # Follow ALL QNFO accounts on configured platforms
    python social_follow.py dry-run          # Show what would be followed

Environment:
    BSKY_HANDLE / BSKY_APP_PASS          — Bluesky credentials
    MASTODON_INSTANCE / MASTODON_TOKEN    — Mastodon credentials
    (Or create a .env file in the working directory)
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SKILL_ROOT / "references" / "qnfo_accounts.json"


def load_registry():
    """Load the QNFO account registry."""
    if not REGISTRY_PATH.exists():
        print(f"ERROR: Registry not found at {REGISTRY_PATH}")
        sys.exit(1)
    return json.loads(REGISTRY_PATH.read_text())


def run_script(script_name: str, args: list):
    """Run a platform-specific follow script."""
    script_path = SKILL_ROOT / "scripts" / script_name
    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}")
        sys.exit(1)

    cmd = [sys.executable, str(script_path)] + args
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode


def cmd_all(args: list):
    """Follow all QNFO accounts on all configured platforms."""
    registry = load_registry()
    platforms = args if args else ["bluesky", "mastodon"]

    for platform in platforms:
        if platform not in registry["accounts"]:
            print(f"⚠ Unknown platform: {platform}")
            continue

        accounts = registry["accounts"][platform]
        if not accounts:
            print(f"  No accounts registered for {platform}")
            continue

        print(f"\n{'='*60}")
        print(f"  {platform.upper()} — {len(accounts)} accounts")
        print(f"{'='*60}")

        # Check if credentials are configured
        if platform == "bluesky":
            if not os.environ.get("BSKY_HANDLE") and not os.environ.get("BSKY_APP_PASS"):
                env = {}
                env_file = Path(".env")
                if env_file.exists():
                    for line in env_file.read_text().splitlines():
                        if "=" in line:
                            k, v = line.split("=", 1)
                            env[k.strip()] = v.strip().strip('"').strip("'")
                if not env.get("BSKY_HANDLE"):
                    print("  ⚠ Skipping Bluesky: BSKY_HANDLE not configured")
                    continue
        elif platform == "mastodon":
            creds = Path.home() / ".mastodon_creds.json"
            if not os.environ.get("MASTODON_TOKEN") and not creds.exists():
                print("  ⚠ Skipping Mastodon: not authenticated (run 'mastodon auth' first)")
                continue

        # Build handles list
        handles = [a["handle"] for a in accounts]

        if platform == "bluesky":
            run_script("bluesky_follow.py", ["bulk", str(REGISTRY_PATH)])
        elif platform == "mastodon":
            run_script("mastodon_follow.py", ["bulk", str(REGISTRY_PATH)])


def cmd_dry_run(args: list):
    """Preview what accounts would be followed."""
    registry = load_registry()
    platforms = args if args else ["bluesky", "mastodon", "x-twitter", "linkedin"]

    for platform in platforms:
        if platform not in registry["accounts"]:
            print(f"  ⚠ Unknown: {platform}")
            continue

        accounts = registry["accounts"][platform]
        api_support = {
            "bluesky": "✅ YES",
            "mastodon": "✅ YES",
            "x-twitter": "❌ NO (Enterprise only)",
            "linkedin": "⚠️ PARTIAL (connections only, 5/day)",
        }

        print(f"\n{'─'*50}")
        print(f"  {platform.upper()} ({len(accounts)} accounts) — API: {api_support.get(platform, '?')}")
        print(f"{'─'*50}")
        for a in accounts:
            name = a.get("name", "?")
            handle = a.get("handle", a.get("search", "?"))
            domain = a.get("domain", "?")
            print(f"  {name:<25} {handle:<45} [{domain}]")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable commands:")
        print("  all [platforms...]     Follow all QNFO accounts on all (or specified) platforms")
        print("  dry-run [platforms...] Preview what would be followed")
        print("  bluesky <cmd> [...]    Run a Bluesky command")
        print("  mastodon <cmd> [...]   Run a Mastodon command")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "all":
        cmd_all(args)
    elif command == "dry-run":
        cmd_dry_run(args)
    elif command == "bluesky":
        run_script("bluesky_follow.py", args)
    elif command == "mastodon":
        run_script("mastodon_follow.py", args)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
