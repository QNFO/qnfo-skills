#!/usr/bin/env python3
"""
zenodo_broadcast.py — Zenodo Dissemination Playbook lever D7 (2026-08-14).

Composes <280-char "impact copy" for a published Zenodo record and (only with
an explicit --post flag) dispatches it to Mastodon + Bluesky.

PLAYBOOK RULES (from the note + live lessons):
  - Lead with the primary contribution.
  - End with the DOI link: https://doi.org/<doi>
  - Exactly three hashtags.
  - NO exclamation points, no marketing jargon; objective scientific tone.
  - <=280 characters for Mastodon; <=300 graphemes for Bluesky
    (BSKY-300-GRAPHEME-1 hard limit — script trims to 290 to be safe).
  - COMPOSE-ONLY by default. --post requires credentials and is an
    explicit, user-visible action (TEST-SEND-EXTERNAL-1: never test-post
    to external accounts; this only posts to QNFO's own handles).

CREDENTIAL DISCOVERY (TOKEN-DISCOVERY-1 order):
  env -> C:\\Users\\LENOVO\\.deepchat\\keys.json -> .env in script dir
  -> ~/.mastodon_creds.json (mastodon_follow.py auth)
  -> ~/.bsky_credentials / .bsky_follow_state.json
  For Bluesky: BSKY_HANDLE + BSKY_APP_PASS.
  For Mastodon: MASTODON_INSTANCE + MASTODON_TOKEN.

USAGE:
  python zenodo_broadcast.py --doi 10.5281/zenodo.21208346          # compose only
  python zenodo_broadcast.py --doi 10.5281/zenodo.21208346 --title "The Ultrametric Foundation: A Unified Thesis on Number, Time, Knowledge, and Computation"
  python zenodo_broadcast.py --doi 10.5281/zenodo.21208346 --title "..." --post

Zero external dependencies (urllib stdlib). Python 3.8+.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

MAX_MASTODON = 280
MAX_BSKY = 290  # under the 300-grapheme hard limit (BSKY-300-GRAPHEME-1)

UA = {"User-Agent": "QNFO-ZenodoBroadcast/1.0 (rowan.quni@outlook.com)"}


def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def discover_creds():
    """Return dict with bluesky handle/pass + mastodon instance/token or None."""
    creds = {"bsky_handle": os.environ.get("BSKY_HANDLE"),
             "bsky_pass": os.environ.get("BSKY_APP_PASS") or os.environ.get("BSKY_APP_PASSWORD"),
             "mastodon_instance": os.environ.get("MASTODON_INSTANCE"),
             "mastodon_token": os.environ.get("MASTODON_TOKEN")}
    keys = load_json(r"C:\Users\LENOVO\.deepchat\keys.json")
    if keys:
        for k, v in keys.items():
            kl = k.lower()
            if "bsky" in kl and "handle" in kl and not creds["bsky_handle"]:
                creds["bsky_handle"] = str(v)
            elif "bsky" in kl and ("pass" in kl or "apppass" in kl.replace("_", "")) and not creds["bsky_pass"]:
                creds["bsky_pass"] = str(v)
            elif "mastodon" in kl and "instance" in kl and not creds["mastodon_instance"]:
                creds["mastodon_instance"] = str(v)
            elif "mastodon" in kl and "token" in kl and not creds["mastodon_token"]:
                creds["mastodon_token"] = str(v)
    mast = load_json(os.path.expanduser("~/.mastodon_creds.json"))
    if mast:
        creds["mastodon_instance"] = creds["mastodon_instance"] or mast.get("instance")
        creds["mastodon_token"] = creds["mastodon_token"] or mast.get("access_token") or mast.get("token")
    return creds


def compose(title, doi, contribution_hint=None):
    """Compose <280-char impact copy: contribution -> DOI -> 3 hashtags."""
    hashtags = ["#OpenScience", "#QuantumFoundations", "#UltrametricPhysics"]
    core = (contribution_hint or title).strip().rstrip(".")
    core = re.sub(r"[!]+", "", core)  # no exclamation points
    if len(core) > 180:
        core = core[:177].rstrip() + "..."
    text = f"{core}. {hashtags[0]} {hashtags[1]} {hashtags[2]}\nhttps://doi.org/{doi}"
    if len(text) > MAX_MASTODON:
        overflow = len(text) - MAX_MASTODON
        core = core[:max(0, len(core) - overflow - 3)].rstrip() + "..."
        text = f"{core}. {hashtags[0]} {hashtags[1]} {hashtags[2]}\nhttps://doi.org/{doi}"
    return text


def bsky_post(handle, app_pass, text):
    """Post to Bluesky via AT Protocol (mirrors bluesky_post.py auth flow)."""
    session_req = urllib.request.Request(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        data=json.dumps({"identifier": handle, "password": app_pass}).encode(),
        headers={**UA, "Content-Type": "application/json"})
    with urllib.request.urlopen(session_req, timeout=30) as r:
        session = json.loads(r.read().decode())
    now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    record = {"text": text, "createdAt": now,
              "langs": ["en"], "$type": "app.bsky.feed.post"}
    post_req = urllib.request.Request(
        "https://bsky.social/xrpc/com.atproto.repo.createRecord",
        data=json.dumps({"repo": session["did"], "collection": "app.bsky.feed.post",
                         "record": record}).encode(),
        headers={**UA, "Content-Type": "application/json",
                 "Authorization": f"Bearer {session['accessJwt']}"})
    with urllib.request.urlopen(post_req, timeout=30) as r:
        return json.loads(r.read().decode())


def mastodon_post(instance, token, text):
    """Post to Mastodon /api/v1/statuses."""
    url = f"https://{instance}/api/v1/statuses"
    req = urllib.request.Request(
        url, data=urllib.parse.urlencode({"status": text, "visibility": "public"}).encode(),
        headers={**UA, "Content-Type": "application/x-www-form-urlencoded",
                 "Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def main():
    args = sys.argv[1:]
    if "--doi" not in args:
        sys.exit(__doc__)
    doi = args[args.index("--doi") + 1]
    title = args[args.index("--title") + 1] if "--title" in args else None
    do_post = "--post" in args

    text = compose(title or "New QNFO open-access publication", doi)
    print("=== COMPOSED BROADCAST ===")
    print(text)
    print(f"--- chars: {len(text)} (Mastodon max 280, Bluesky max 290) ---")

    if not do_post:
        print("\nCOMPOSE-ONLY. Re-run with --post to dispatch (QNFO-owned handles only).")
        return

    creds = discover_creds()
    results = []
    if creds.get("bsky_handle") and creds.get("bsky_pass"):
        try:
            r = bsky_post(creds["bsky_handle"], creds["bsky_pass"], text[:MAX_BSKY])
            results.append(f"Bluesky: posted uri={r.get('uri')}")
        except Exception as e:
            results.append(f"Bluesky: FAILED {e}")
    else:
        results.append("Bluesky: SKIPPED (no credentials)")
    if creds.get("mastodon_instance") and creds.get("mastodon_token"):
        try:
            r = mastodon_post(creds["mastodon_instance"], creds["mastodon_token"], text)
            results.append(f"Mastodon: posted id={r.get('id')}")
        except Exception as e:
            results.append(f"Mastodon: FAILED {e}")
    else:
        results.append("Mastodon: SKIPPED (no credentials)")
    print("\n".join(f"- {r}" for r in results))


if __name__ == "__main__":
    main()
