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
    - License default 1 = CC BY 4.0 (Figshare v2 offers only 7 license IDs; CC BY-NC-SA
      is NOT available — closest compatible public license). Accepts integer ID or known name.
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

# Figshare v2 license IDs (verified live 2026-08-16 via GET /v2/licenses):
# 1=CC BY 4.0, 2=CC0, 3=MIT, 4=GPL, 5=GPL 2.0+, 6=GPL 3.0+, 7=Apache 2.0.
# NOTE: CC BY-NC-SA is NOT offered by Figshare v2 (QNFO Zenodo norm cc-by-nc-sa-4.0
# cannot be mirrored here; CC BY 4.0 is the closest compatible public license).
LICENSES = {
    "1": 1, "cc-by": 1, "cc-by-4.0": 1,
    "2": 2, "cc0": 2,
    "3": 3, "mit": 3,
    "4": 4, "gpl": 4,
    "5": 5, "gpl-2.0": 5, "gpl-2.0+": 5,
    "6": 6, "gpl-3.0": 6, "gpl-3.0+": 6,
    "7": 7, "apache-2.0": 7,
}


def coerce_license(raw):
    """Accept integer ID or known name; error with the available list otherwise."""
    key = str(raw).strip().lower()
    if key in LICENSES:
        return LICENSES[key]
    sys.exit(f"ERROR: unknown license '{raw}'. Figshare v2 offers: "
             "1=CC BY 4.0, 2=CC0, 3=MIT, 4=GPL, 5=GPL 2.0+, 6=GPL 3.0+, 7=Apache 2.0. "
             "(CC BY-NC-SA is not available on Figshare v2.)")


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


def create_article(token, title, description, keywords, license_id, defined_type, categories=""):
    """POST /account/articles -> draft article. Returns article id.
    Categories (comma-separated Figshare category IDs) are required before publish."""
    data = {
        "title": title,
        "description": description,
        "license": coerce_license(license_id),
        "defined_type": defined_type,
    }
    if keywords:
        data["tags"] = [k.strip() for k in keywords.split(",") if k.strip()]
    if categories:
        data["categories"] = [int(c.strip()) for c in categories.split(",") if c.strip()]
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
    """Attach one file to an article — Figshare v2 CHUNKED upload (VERIFIED LIVE 2026-08-16):
    initiate -> GET file resource (upload_url) -> GET upload_url (parts) ->
    PUT each part to {upload_url}/{partNo} -> complete (202 async) -> poll computed_md5."""
    name, size, md5 = file_meta(path)
    st, body = request(
        f"{API_BASE}/account/articles/{article_id}/files",
        token=token, method="POST",
        data={"name": name, "size": size, "md5": md5},
    )
    if st != 201:
        sys.exit(f"ERROR: file init failed HTTP {st}: {json.dumps(body, ensure_ascii=False)[:300]}")
    if isinstance(body, dict) and body.get("location"):
        loc = body["location"]
        if not loc.startswith("http"):
            loc = f"{API_BASE}{loc}"
    else:
        sys.exit(f"ERROR: unexpected file init response: {json.dumps(body, ensure_ascii=False)[:300]}")

    st2, fbody = request(loc, token=token)
    if st2 != 200:
        sys.exit(f"ERROR: file resource read failed HTTP {st2}")
    upload_url = (fbody or {}).get("upload_url") or (fbody or {}).get("uploadUrl")
    file_id = loc.rsplit("/", 1)[-1]
    if not upload_url or not file_id or not file_id.isdigit():
        sys.exit(f"ERROR: bad file resource: {json.dumps(fbody, ensure_ascii=False)[:300]}")

    # Chunked upload: GET {upload_url} -> parts[{partNo,startOffset,endOffset}]
    st3, pbody = request(upload_url)
    if st3 != 200:
        sys.exit(f"ERROR: parts read failed HTTP {st3}: {json.dumps(pbody, ensure_ascii=False)[:200]}")
    parts = (pbody or {}).get("parts") or []
    if not parts:
        sys.exit(f"ERROR: no parts in upload_url response: {json.dumps(pbody, ensure_ascii=False)[:300]}")
    with open(path, "rb") as fh:
        raw = fh.read()
    for part in parts:
        pno = part.get("partNo")
        start = int(part.get("startOffset", 0))
        end = int(part.get("endOffset", -1))
        chunk = raw[start:end + 1]
        stp, _ = request(f"{upload_url}/{pno}", method="PUT", raw_body=chunk,
                         content_type="application/octet-stream")
        if stp not in (200, 201, 204):
            sys.exit(f"ERROR: part {pno} upload failed HTTP {stp}")

    # Complete (202 = accepted for async processing)
    st4, cbody = request(
        f"{API_BASE}/account/articles/{article_id}/files/{file_id}",
        token=token, method="POST",
        data={"status": "completed"},
    )
    if st4 not in (200, 201, 202, 204):
        sys.exit(f"ERROR: complete upload failed HTTP {st4}: {json.dumps(cbody, ensure_ascii=False)[:300]}")

    # Poll until computed_md5 == supplied md5 (processing is async)
    import time as _time
    for _ in range(10):
        _time.sleep(3)
        _, fv = request(f"{API_BASE}/account/articles/{article_id}/files/{file_id}", token=token)
        if isinstance(fv, dict) and fv.get("computed_md5") == md5:
            break
    print(f"File attached: {name} ({size} bytes, md5 {md5}, {len(parts)} part(s) chunked)")
    return file_id


def publish(token, article_id):
    st, body = request(f"{API_BASE}/account/articles/{article_id}/publish", token=token, method="POST", data={})
    if st not in (200, 201, 202, 204):
        msg = json.dumps(body, ensure_ascii=False)[:300]
        if "categories" in msg.lower():
            sys.exit(f"ERROR: publish failed HTTP {st}: {msg}. Hint: set --categories on create/submit (selectable Figshare category IDs; e.g. --categories 30229,29785,29827,30022). Publish requires at least one category.")
        sys.exit(f"ERROR: publish failed HTTP {st}: {msg}")
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
    ap.add_argument("--license", default="1", help="Figshare license ID integer (default 1 = CC BY 4.0; see LICENSES)")
    ap.add_argument("--defined-type", default="thesis",
                    choices=["figure", "media", "dataset", "poster", "journal contribution",
                             "presentation", "thesis", "software", "online resource",
                             "preprint", "book", "conference contribution"])
    ap.add_argument("--categories", default="",
                    help="comma-separated Figshare category IDs (REQUIRED before publish; "
                         "selectable leaves only, e.g. 30229=Foundations of QM, 29785=Algebraic "
                         "structures in math phys, 29827=Algebra & number theory, 30022=Philosophy "
                         "of science)")
    ap.add_argument("--article", help="article id for upload/publish/verify")
    ap.add_argument("--no-publish", action="store_true", help="leave as private draft")
    args = ap.parse_args()

    token = None
    if args.mode in ("submit", "create", "upload", "publish", "verify"):
        token = get_token()

    if args.mode == "create":
        if not args.title or not args.description:
            sys.exit("ERROR: --title and --description required for create")
        create_article(token, args.title, args.description, args.keywords, args.license, args.defined_type, args.categories)
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
        aid = create_article(token, args.title, args.description, args.keywords, args.license, args.defined_type, args.categories)
        upload_file(token, aid, args.file)
        if not args.no_publish:
            publish(token, aid)
        verify(token, aid)


if __name__ == "__main__":
    main()
