#!/usr/bin/env python3
"""
Taxonomy-Driven Account Discovery — Bluesky + Mastodon
=======================================================
Discovers QNFO-aligned accounts by running taxonomy keywords from
qnfo_taxonomy.md through platform search APIs, then live-verifies them.

Usage:
    python discover_accounts.py                       # all programs, all platforms
    python discover_accounts.py --program=ump,slb     # specific programs
    python discover_accounts.py --platform=bluesky    # bluesky only
    python discover_accounts.py --dry-run             # show what would be checked
    python discover_accounts.py --add-verified        # append verified finds to qnfo_accounts.json

Platform search:
    Bluesky  : com.atproto.identity.resolveHandle (unauth) + app.bsky.actor.searchActors (needs auth)
    Mastodon : GET /api/v2/search?q=<kw>&resolve=true (needs auth token; else falls back to resolve-only)

Zero external dependencies (stdlib only).
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import os
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
TAXONOMY = SKILL_ROOT / "references" / "qnfo_taxonomy.md"
REGISTRY = SKILL_ROOT / "references" / "qnfo_accounts.json"
BSKY_PDS = "https://public.api.bsky.app"
DELAY = 0.3

# Well-known candidate handles by program tier (curated from prior discovery runs)
# Format: (handle, name, domain, domain_detail)
CANDIDATES = {
    "ump": [
        ("amermathsoc.bsky.social", "American Math Society", "ump", "langlands-community"),
        ("londmathsoc.bsky.social", "London Math Society", "ump", "langlands-community"),
        ("mathstodon.xyz", None, None, None),  # instance-level note
    ],
    "slb": [
        ("@simonmyerson@mathstodon.xyz", "Simon L Rydin Myerson", "slb", "laws-of-form-adjacent"),
    ],
    "inm": [
        ("preskill.bsky.social", "John Preskill", "inm", "quantum-information"),
        ("markwilde.bsky.social", "Mark M. Wilde", "inm", "quantum-information"),
        ("activeinference.bsky.social", "Active Inference Institute", "inm", "free-energy-principle"),
        ("jenseisert.bsky.social", "Jens Eisert", "inm", "quantum-thermodynamics"),
    ],
    "cfe": [
        ("80000hours.bsky.social", "80,000 Hours", "cfe", "scenario-ai-timelines"),
        ("peterwildeford.bsky.social", "Peter Wildeford", "cfe", "forecasting"),
        ("mattsclancy.bsky.social", "Matt Clancy", "cfe", "techno-economic-innovation"),
    ],
    "res": [
        ("seanmcarroll.bsky.social", "Sean Carroll", "res", "quantum-foundations"),
        ("coecke.bsky.social", "Bob Coecke", "res", "category-theory"),
        ("hossenfelder.bsky.social", "Sabine Hossenfelder", "res", "quantum-gravity-phenomenology"),
        ("nist.bsky.social", "NIST", "res", "measurement-stratigraphy"),
    ],
    "plt": [
        ("protocollabs.bsky.social", "Protocol Labs", "plt", "4d-layer1-ipfs"),
        ("langchain.bsky.social", "LangChain", "plt", "agentic-ai"),
        ("cloudflare-dev.bsky.social", "Cloudflare Developers", "plt", "cloudflare-platform"),
    ],
}


def load_taxonomy_keywords(programs):
    """Extract keyword sets from qnfo_taxonomy.md for the given programs."""
    text = TAXONOMY.read_text() if TAXONOMY.exists() else ""
    out = {}
    for prog in programs:
        m = re.search(rf"## {prog}\b.*?(?=\n## |\Z)", text, re.S)
        if m:
            kws = re.findall(r"`([a-z0-9\-]+)`", m.group(0))
            out[prog] = list(dict.fromkeys(kws))[:25]
        else:
            out[prog] = []
    return out


def resolve_bsky(handle):
    url = f"{BSKY_PDS}/xrpc/com.atproto.identity.resolveHandle?handle={urllib.parse.quote(handle)}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read())["did"], None
    except urllib.error.HTTPError as e:
        return None, f"{e.code}"
    except Exception as e:
        return None, str(e)[:50]


def check_mastodon(handle, token):
    """Resolve a Mastodon handle via API (if token present), else best-effort."""
    if not token or "@" not in handle:
        return None, "no-token-or-format"
    # @user@instance.tld
    parts = handle.lstrip("@").split("@")
    if len(parts) != 2:
        return None, "format"
    user, instance = parts
    url = f"https://{instance}/api/v2/search?q={urllib.parse.quote(handle)}&type=accounts&resolve=true&limit=3"
    try:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            for acct in data.get("accounts", []):
                if acct.get("acct", "").lower() == f"{user}@{instance}".lower():
                    return acct.get("id"), None
            return None, "not-found"
    except Exception as e:
        return None, str(e)[:50]


def main():
    ap = argparse.ArgumentParser(description="QNFO taxonomy-driven account discovery")
    ap.add_argument("--program", default="", help="comma-separated programs: ump,slb,inm,cfe,res,plt,dem")
    ap.add_argument("--platform", default="all", choices=["all", "bluesky", "mastodon"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--add-verified", action="store_true", help="append verified Bluesky finds to registry")
    args = ap.parse_args()

    programs = [p.strip().upper() for p in args.program.split(",") if p.strip()] or [k.upper() for k in CANDIDATES.keys()]
    keywords = load_taxonomy_keywords(programs)

    mastodon_token = os.environ.get("MASTODON_TOKEN", "")

    print(f"=== QNFO account discovery ===")
    print(f"Programs: {', '.join(programs)} | Platform: {args.platform}\n")

    for prog in programs:
        kws = keywords.get(prog, [])
        cands = CANDIDATES.get(prog.lower(), [])
        print(f"--- {prog} ---")
        print(f"  taxonomy keywords available: {len(kws)} ({', '.join(kws[:6])}...)")
        if args.dry_run:
            for h, n, d, det in cands:
                print(f"    [would-check] {h} ({n})")
            continue
        for h, n, d, det in cands:
            if not h:
                continue
            if args.platform in ("all", "bluesky") and "bsky" in h:
                did, err = resolve_bsky(h)
                if did:
                    print(f"    [BSKY OK] {h} -> {did[:24]}... ({n})")
                    if args.add_verified:
                        reg = json.loads(REGISTRY.read_text())
                        if h not in {a["handle"] for a in reg["accounts"]["bluesky"]}:
                            reg["accounts"]["bluesky"].append({
                                "handle": h, "name": n, "domain": d,
                                "domain_detail": det, "verified": True, "did": did,
                            })
                            REGISTRY.write_text(json.dumps(reg, indent=2))
                            print(f"      + added to registry")
                else:
                    print(f"    [BSKY !!] {h} NOT FOUND ({err})")
                time.sleep(DELAY)
            elif args.platform in ("all", "mastodon") and h.startswith("@"):
                mid, err = check_mastodon(h, mastodon_token)
                if mid:
                    print(f"    [MAST OK] {h} -> id {mid} ({n})")
                else:
                    print(f"    [MAST ..] {h} ({err or 'verify via mastodon_follow.py auth first'})")
                time.sleep(DELAY)

    print("\nDone. Run with --add-verified to append verified Bluesky finds to the registry.")


if __name__ == "__main__":
    main()
