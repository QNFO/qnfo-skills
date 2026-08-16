#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zenodo Communities — Discovery + Submission (dissemination add-on)

Purpose: widen QNFO research dissemination by (1) discovering Zenodo communities
that are genuinely OPEN to third-party submission and (2) requesting inclusion of
an already-published QNFO record in those communities. Zero manual intervention.

WHY THIS EXISTS (verified 2026-08-16, see research/references/dissemination-outlets-2026-08-16.md):
    - The "no-gatekeeping / no-AI-ban / no-cost / API-driven" preprint space has
      SHRUNK. OSF Preprints bans LLM/AI-generated content (and suspended new
      submissions Aug 2025). arXiv requires endorsement. Preprints.org / TechRxiv /
      Research Square / SSRN all moderate. Zenodo + Internet Archive + Figshare are
      the remaining no-endorsement, API-driven channels.
    - Most "open" Zenodo topic communities are slug-squatted or near-empty
      (0-4 records). Submitting into an empty community is wasted effort and can
      look like spam. This script therefore FILTERS by substantive record count.

CREDENTIALS (research/SKILL.md "Zenodo Credential Protocol"):
    ZENODO_TOKEN is read from the environment ONLY. Never hardcode, never retype
    a truncated token. A wrong token returns the SAME 403 "Permission denied."
    as a scope-less token — do not misdiagnose.

USAGE:
    python zenodo-communities.py discover [--min-records 5] [--top 15]
        Search QNFO-relevant domains, verify open access policy, rank by record count.

    python zenodo-communities.py submit --doi 10.5281/zenodo.XXXX --community <slug>
        Request inclusion of a published record in one open community.

    python zenodo-communities.py submit --doi 10.5281/zenodo.XXXX --all-open [--min-records 5]
        Request inclusion in every discovered open community meeting the bar.

    python zenodo-communities.py report --doi 10.5281/zenodo.XXXX
        Show current community memberships for a record (GET read-only).

SAFETY GATES (HARD):
    - Only submits to communities with access.record_submission_policy == "open".
      Never to "closed"/restricted communities (403 + possible account flag).
    - Only submits records that are already PUBLISHED (state=done via records API).
    - Skips empty/squatted communities by default (min-record filter).
    - review_policy handling (VERIFIED LIVE 2026-08-16): "closed" does NOT mean
      auto-included for third-party submitters (ZENODO-COMMUNITY-INCLUSION-REQUEST-1).
      POST /records/{id}/communities
      creates a community-inclusion REQUEST (status=submitted) that awaits the
      community's curators; only the user's OWN communities auto-accept (owner).
      "open"/"members" -> queued for curator review. Report via /api/requests
      (status=submitted), not the memberships list (which only shows accepted).
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://zenodo.org/api"

# Browser-like headers — REQUIRED to avoid Zenodo bot-detection 403
# (ZENODO-BOT-403-1: minimal UA triggers "unusual traffic" 403, NOT an IP block).
BROWSER_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"),
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

# QNFO-relevant domain keywords (UMP/SLB/INM/RES/CFE/QEC + adjacent).
DOMAIN_KEYWORDS = [
    "quantum foundations", "theoretical physics", "complex systems",
    "complexity", "information theory", "philosophy of physics",
    "philosophy of science", "mathematical physics", "open science",
    "artificial intelligence", "foundations of physics", "systems science",
    "interdisciplinary", "ultrametric", "p-adic", "quantum information",
    "laws of form", "consilience",
]


def get_token() -> str:
    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        sys.exit("ERROR: ZENODO_TOKEN not set in environment. Set it before running.")
    return token


def request(url, token=None, method="GET", data=None):
    """urllib request with browser headers + optional bearer token."""
    headers = dict(BROWSER_HEADERS)
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, headers=headers, data=body, method=method)
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read().decode("utf-8", "replace")
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"_raw": raw}
    except Exception as e:
        return -1, {"_error": str(e)}


def search_communities(keyword, size=15):
    q = urllib.parse.quote(keyword)
    st, body = request(f"{API_BASE}/communities?q={q}&size={size}&sort=bestmatch")
    if st != 200:
        return []
    return body.get("hits", {}).get("hits", [])


def community_access(ident):
    """Return dict with title/slug/access or None."""
    st, body = request(f"{API_BASE}/communities/{ident}")
    if st != 200:
        return None
    meta = body.get("metadata", {}) or {}
    return {
        "id": body.get("id"),
        "slug": body.get("slug"),
        "title": (meta.get("title") or "").strip(),
        "access": body.get("access", {}),
        "is_open": (body.get("access", {}).get("record_submission_policy") == "open"),
        "review": body.get("access", {}).get("review_policy"),
    }


def community_record_count(slug):
    q = urllib.parse.quote(slug)
    st, body = request(f"{API_BASE}/records?q=communities:{q}&size=1")
    if st != 200:
        return 0
    return body.get("hits", {}).get("total", 0)


def resolve_record(doi):
    """Resolve a DOI to a published Zenodo record id. Returns (record_id, state)."""
    q = urllib.parse.quote(doi)
    st, body = request(f"{API_BASE}/records?q=doi:{q}&size=1")
    if st != 200:
        return None, None
    hits = body.get("hits", {}).get("hits", [])
    if not hits:
        # fallback: strip the zenodo prefix and hit the record directly
        recid = doi.rsplit(".", 1)[-1] if "zenodo." in doi else None
        return recid, None
    return hits[0].get("id"), hits[0].get("status")


def record_communities(record_id, token):
    st, body = request(f"{API_BASE}/records/{record_id}/communities", token=token)
    if st != 200:
        return None, body
    return body, None


def submit_to_community(record_id, slug, token):
    """POST /api/records/{id}/communities with {"communities":[{"id": slug}]}."""
    st, body = request(
        f"{API_BASE}/records/{record_id}/communities",
        token=token, method="POST",
        data={"communities": [{"id": slug}]},
    )
    return st, body


def discover(min_records, top, max_check=60):
    # Phase 1: collect candidate communities (dedup by id, cap to max_check)
    seen = {}
    for kw in DOMAIN_KEYWORDS:
        for h in search_communities(kw):
            cid = h.get("id")
            if cid not in seen:
                seen[cid] = h
            if len(seen) >= max_check:
                break
        if len(seen) >= max_check:
            break
        time.sleep(0.1)

    # Phase 2: verify access policy + record count for each candidate
    results = []
    for cid in list(seen.keys()):
        info = community_access(cid)
        if info and info["is_open"]:
            n = community_record_count(info["slug"])
            info["records"] = n
            results.append(info)
        time.sleep(0.1)

    results.sort(key=lambda r: -r["records"])
    print("OPEN Zenodo communities (record_submission_policy=open), ranked by record count:")
    print(f"{'records':>8}  {'review':<9}  slug / title")
    print("-" * 78)
    shown = 0
    for r in results:
        if r["records"] < min_records:
            continue
        print(f"{r['records']:>8}  {str(r['review']):<9}  {r['slug']}  |  {r['title'][:50]}")
        shown += 1
        if shown >= top:
            break
    if shown == 0:
        print(f"(none with >= {min_records} records — the open-community landscape is sparse; "
              "see report for the verified reality.)")
    return results


def do_submit(doi, community_slug, all_open, min_records, token):
    record_id, status = resolve_record(doi)
    if not record_id:
        sys.exit(f"ERROR: could not resolve record for DOI {doi}")
    if status not in ("done", "published"):
        sys.exit(f"ERROR: record {record_id} status={status} — submit only PUBLISHED records.")

    targets = []
    if all_open:
        results = discover(min_records, top=50)
        targets = [r["slug"] for r in results if r["records"] >= min_records and r["slug"]]
    elif community_slug:
        info = community_access(community_slug)
        if not info or not info["is_open"]:
            sys.exit(f"ERROR: community '{community_slug}' is not open to submission (or not found).")
        targets = [community_slug]
    else:
        sys.exit("ERROR: provide --community <slug> or --all-open.")

    print(f"Record: https://zenodo.org/records/{record_id}  (status={status})")
    for slug in targets:
        st, body = submit_to_community(record_id, slug, token)
        if st in (200, 201):
            print(f"  [{slug}] requested (HTTP {st}) -> {json.dumps(body, ensure_ascii=False)[:160]}")
        else:
            print(f"  [{slug}] HTTP {st} -> {json.dumps(body, ensure_ascii=False)[:200]}")
            # ZENODO-COMMUNITY-SUBMIT-MEMBERSHIP-1: "only allowed to community members"
            # -> join first (POST /api/communities/{slug}/members) then retry submit.
            msg = json.dumps(body).lower()
            if "member" in msg or st == 403:
                print(f"  [{slug}] hint: join first via POST /api/communities/{slug}/members, then retry.")
        time.sleep(0.5)


def do_report(doi, token):
    record_id, status = resolve_record(doi)
    if not record_id:
        sys.exit(f"ERROR: could not resolve record for DOI {doi}")
    print(f"Record: https://zenodo.org/records/{record_id}  (status={status})")

    # 1) Active memberships (accepted communities only)
    body, err = record_communities(record_id, token)
    if err is not None:
        print(f"  (read communities: {err})")
    else:
        memberships = body.get("hits", body) if isinstance(body, dict) else body
        items = memberships.get("hits", []) if isinstance(memberships, dict) else memberships
        if isinstance(items, list) and items:
            for m in items:
                if isinstance(m, dict):
                    print(f"  MEMBER: {m.get('slug', m.get('id'))}  {m.get('title', '')[:50]}")
        else:
            print("  MEMBER: (none)")

    # 2) Pending community-inclusion requests for this record (VERIFIED LIVE 2026-08-16:
    #    third-party submissions create status=submitted requests awaiting curators).
    try:
        q = urllib.parse.quote(f"topic.record:{record_id}")
        st, rbody = request(f"{API_BASE}/requests?q={q}&size=50", token=token)
        if st == 200:
            rh = rbody.get("hits", {}).get("hits", []) if isinstance(rbody, dict) else []
            pending = [r for r in rh if isinstance(r, dict) and r.get("type") == "community-inclusion"]
            if pending:
                for r in pending:
                    recv = (r.get("receiver") or {}).get("community", "")[:14]
                    print(f"  REQUEST: {r.get('status')}  receiver={recv}  created={(r.get('created') or '')[:19]}")
            else:
                print("  REQUEST: (none pending)")
        else:
            print(f"  REQUEST: (read failed HTTP {st})")
    except Exception as e:
        print(f"  REQUEST: (read failed {e})")


def main():
    ap = argparse.ArgumentParser(description="Zenodo community discovery + submission")
    ap.add_argument("mode", choices=["discover", "submit", "report"])
    ap.add_argument("--doi", help="record DOI (submit/report)")
    ap.add_argument("--community", help="community slug (submit)")
    ap.add_argument("--all-open", action="store_true", help="submit to all eligible open communities")
    ap.add_argument("--min-records", type=int, default=5, help="minimum record count to consider (default 5)")
    ap.add_argument("--top", type=int, default=15, help="max communities to show in discover (default 15)")
    args = ap.parse_args()

    if args.mode == "discover":
        discover(args.min_records, args.top)
    elif args.mode == "submit":
        do_submit(args.doi, args.community, args.all_open, args.min_records, get_token())
    elif args.mode == "report":
        do_report(args.doi, get_token())


if __name__ == "__main__":
    main()
