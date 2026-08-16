#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figshare Submit — cross-post a published QNFO artifact to Figshare (dissemination add-on)

WHY THIS EXISTS (verified 2026-08-16, see research/references/dissemination-outlets-2026-08-16.md):
    - Figshare is one of the FEW remaining no-endorsement, API-driven, free-tier
      outlets (20 GB private + unlimited public for individual researchers).
    - OSF Preprints is DISQUALIFIED (bans LLM/AI-generated text; suspended new
      submissions Aug 2025). Zenodo remains primary. Figshare is the secondary leg
      for data/articles/preprints with a DOI.
    - No peer review, no endorsement requirement, light moderation, no formatting
      template, and no explicit AI-text ban found in Figshare's published policies.

CREDENTIALS:
    FIGSHARE_TOKEN is read from the environment OR from the canonical key store
    C:/Users/LENOVO/keys.json (key "figshare_token" — same store as zenodo_token /
    buffer_token / cloudflare_api_token). One-time setup: log in to figshare.com ->
    Settings -> Applications -> Personal Token, then store it in keys.json (or export
    FIGSHARE_TOKEN). Never hardcode, never retype a truncated token.

USAGE:
    python figshare-submit.py submit --file <path> --title "<T>" --description "<D>"
        [--keywords "a,b,c"] [--license cc-by-nc-sa] [--defined-type paper]
        [--no-publish]
        Create a draft article, upload the file, optionally publish (default publish).

    python figshare-submit.py create --title "<T>" --description "<D>" ...
        Create a draft article only (returns article id).

    python figshare-submit.py upload --article <id> --file <path>
        Attach a file to an existing article (computes md5+size, initiates S3
        upload, completes it).

    python figshare-submit.py publish --article <id>
        Publish an article (makes it public).

    python figshare-submit.py verify --article <id>
        Read back article status (public/private) — the verification gate.

SAFETY GATES (HARD):
    - No live submission without FIGSHARE_TOKEN (exit with clear message).
    - Default is PUBLIC publish (that is the dissemination point); --no-publish
      keeps a private draft for review.
    - License default cc-by-nc-sa (matches QNFO Zenodo corpus norm); override
      with --license if a record uses a different license.
    - Every publish is followed by verify (read-back) before reporting success.
"""

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

API_BASE = "https://api.figshare.com/v2"

BROWSER_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"),
    "Accept": "application/json",
}


def get_token() -> str:
    token = os.environ.get("FIGSHARE_TOKEN")
    if not token:
        # Fallback: canonical key store (same convention as buffer-post.py / keys.json).
        try:
            with open(r"C:\Users\LENOVO\keys.json", encoding="utf-8") as _f:
                token = json.load(_f).get("figshare_token")
        except Exception:
            token = None
    if not token:
        sys.exit(
            "ERROR: FIGSHARE_TOKEN not found (env or C:\\Users\\LENOVO\\keys.json). One-time "
            "setup: figshare.com -> Settings -> Applications -> Personal Token, then store it "
            "as figshare_token in keys.json (or export FIGSHARE_TOKEN). Never hardcode it."
        )
    return token


def request(url, token=None, method="GET", data=None, raw_body=None, content_type=None):
    headers = dict(BROWSER_HEADERS)
    if token:
        headers["Authorization"] = f"token {token}"
    body = None
    if raw_body is not None:
        body = raw_body
        headers["Content-Type"] = content_type or "application/octet-stream"
    elif data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, headers=headers, data=body, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8", "replace")
            try:
                return r.status, json.loads(raw) if raw.strip() else {}
            except Exception:
                return r.status, {"_raw": raw[:500]}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw) if raw.strip() else {"_raw": ""}
        except Exception:
            return e.code, {"_raw": raw[:500]}
    except Exception as e:
        return -1, {"_error": str(e)}


def file_meta(path):
    size = os.path.getsize(path)
    md5 = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            md5.update(chunk)
    return os.path.basename(path), size, md5.hexdigest()


def create_article(token, title, description, keywords, license_id, defined_type):
    """POST /account/articles -> draft article. Returns article id."""
    data = {
        "title": title,
        "description": description,
        "license": license_id,
        "defined_type": defined_type,
    }
    if keywords:
        data["tags"] = [k.strip() for k in keywords.split(",") if k.strip()]
    st, body = request(f"{API_BASE}/account/articles", token=token, method="POST", data=data)
    if st != 201:
        sys.exit(f"ERROR: create article failed HTTP {st}: {json.dumps(body, ensure_ascii=False)[:300]}")
    article_id = None
    if isinstance(body, dict):
        article_id = body.get("entity_id")
    if not article_id:
        sys.exit(f"ERROR: no entity_id in create response: {json.dumps(body, ensure_ascii=False)[:300]}")
    print(f"Article draft created: https://figshare.com/articles/{article_id}")
    return article_id


def upload_file(token, article_id, path):
    """Attach one file to an article: initiate -> S3 PUT -> complete."""
    name, size, md5 = file_meta(path)
    st, body = request(
        f"{API_BASE}/account/articles/{article_id}/files",
        token=token, method="POST",
        data={"name": name, "size": size, "md5": md5},
    )
    if st != 201:
        sys.exit(f"ERROR: file init failed HTTP {st}: {json.dumps(body, ensure_ascii=False)[:300]}")
    if isinstance(body, dict) and body.get("location"):
        # body.location points to /account/articles/{id}/files/{file_id}
        loc = body["location"]
        if not loc.startswith("http"):
            loc = f"{API_BASE}{loc}"
        st2, fbody = request(loc, token=token)
        if st2 != 200:
            sys.exit(f"ERROR: file resource read failed HTTP {st2}")
        upload_url = (fbody or {}).get("upload_url") or (fbody or {}).get("uploadUrl")
        if not upload_url:
            sys.exit(f"ERROR: no upload_url in {json.dumps(fbody, ensure_ascii=False)[:300]}")
        file_id = None
        loc_tail = loc.rsplit("/", 1)[-1]
        if loc_tail.isdigit():
            file_id = loc_tail
        if not file_id:
            sys.exit(f"ERROR: could not parse file_id from {loc}")
    else:
        sys.exit(f"ERROR: unexpected file init response: {json.dumps(body, ensure_ascii=False)[:300]}")

    # S3 presigned PUT
    with open(path, "rb") as fh:
        raw = fh.read()
    st3, _ = request(upload_url, method="PUT", raw_body=raw, content_type="application/octet-stream")
    if st3 not in (200, 201, 204):
        sys.exit(f"ERROR: S3 upload failed HTTP {st3}")

    # Complete upload
    st4, cbody = request(
        f"{API_BASE}/account/articles/{article_id}/files/{file_id}",
        token=token, method="POST",
        data={"status": "completed"},
    )
    if st4 not in (200, 201, 204):
        sys.exit(f"ERROR: complete upload failed HTTP {st4}: {json.dumps(cbody, ensure_ascii=False)[:300]}")
    print(f"File attached: {name} ({size} bytes, md5 {md5})")
    return file_id


def publish(token, article_id):
    st, body = request(f"{API_BASE}/account/articles/{article_id}/publish", token=token, method="POST", data={})
    if st not in (200, 201, 202, 204):
        sys.exit(f"ERROR: publish failed HTTP {st}: {json.dumps(body, ensure_ascii=False)[:300]}")
    print(f"Publish request accepted for article {article_id} (HTTP {st})")


def verify(token, article_id):
    st, body = request(f"{API_BASE}/account/articles/{article_id}", token=token)
    if st != 200:
        sys.exit(f"ERROR: verify read-back failed HTTP {st}")
    status = body.get("status") if isinstance(body, dict) else None
    title = (body.get("title") if isinstance(body, dict) else None) or ""
    print(f"VERIFY article {article_id}: status={status} title={title}")
    if status != "public":
        print("WARNING: article is not public yet — check https://figshare.com/articles/{id}")
        return False
    return True


def main():
    ap = argparse.ArgumentParser(description="Figshare cross-post (dissemination add-on)")
    ap.add_argument("mode", choices=["submit", "create", "upload", "publish", "verify"])
    ap.add_argument("--file", help="local file to attach")
    ap.add_argument("--title", help="article title")
    ap.add_argument("--description", help="article description")
    ap.add_argument("--keywords", default="", help="comma-separated keywords")
    ap.add_argument("--license", default="cc-by-nc-sa", help="Figshare license id (default cc-by-nc-sa)")
    ap.add_argument("--defined-type", default="paper",
                    choices=["paper", "preprint", "dataset", "poster", "presentation",
                             "figure", "media", "fileset"])
    ap.add_argument("--article", help="article id for upload/publish/verify")
    ap.add_argument("--no-publish", action="store_true", help="leave as private draft")
    args = ap.parse_args()

    token = None
    if args.mode in ("submit", "create", "upload", "publish", "verify"):
        token = get_token()

    if args.mode == "create":
        if not args.title or not args.description:
            sys.exit("ERROR: --title and --description required for create")
        create_article(token, args.title, args.description, args.keywords, args.license, args.defined_type)
    elif args.mode == "upload":
        if not args.article or not args.file:
            sys.exit("ERROR: --article and --file required for upload")
        upload_file(token, args.article, args.file)
    elif args.mode == "publish":
        if not args.article:
            sys.exit("ERROR: --article required for publish")
        publish(token, args.article)
    elif args.mode == "verify":
        if not args.article:
            sys.exit("ERROR: --article required for verify")
        verify(token, args.article)
    elif args.mode == "submit":
        if not args.file or not args.title or not args.description:
            sys.exit("ERROR: --file, --title, --description required for submit")
        aid = create_article(token, args.title, args.description, args.keywords, args.license, args.defined_type)
        upload_file(token, aid, args.file)
        if not args.no_publish:
            publish(token, aid)
        verify(token, aid)


if __name__ == "__main__":
    main()
