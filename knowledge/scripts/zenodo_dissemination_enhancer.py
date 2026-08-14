#!/usr/bin/env python3
"""
zenodo_dissemination_enhancer.py — Zenodo Dissemination Playbook levers D1-D3
(2026-08-14, QNFO.OUTREACH.2026-08-14-CONTINUE).

Implements:
  D1: EuroSciVoc `scheme`/`identifier` enrichment on `subjects`
      (playbook §2 — aggregators parse Term IDs/URIs, not plain strings)
  D2: `alternate_identifiers` (e.g., Software Heritage `swh`) — merges
      duplicates across engines
  D3: community membership extension (playbook recommends 3+ per record)

SAFETY:
  - DRY-RUN BY DEFAULT. --apply is required to write anything.
  - ADDITIVE ONLY. Never removes existing metadata.
  - Community slugs are verified to EXIST against the live Zenodo API
    before being proposed; non-existent slugs are reported and skipped.
  - Identifiers are only written from an explicit JSON mapping (no
    fabricated URIs — the playbook's example identifier "http://europa.eu"
    is a generic domain, NOT a valid EuroSciVoc term URI; pass real URIs).

USAGE:
  python zenodo_dissemination_enhancer.py --record 21208346
  python zenodo_dissemination_enhancer.py --record 10.5281/zenodo.21208346 \
      --subjects-json subjects.json --community open-science --apply
  python zenodo_dissemination_enhancer.py --record 21208346 \
      --alternate-json alternates.json --apply

subject JSON shape:  [{"term": "Ultrametric analysis", "identifier": "http://publications.europa.eu/resource/authority/euroscivoc/...", "scheme": "EuroSciVoc"}]
alternate JSON shape: [{"identifier": "https://archive.softwareheritage.org/...", "scheme": "swh"}]

Requires: Zenodo token at C:\\Users\\LENOVO\\tokens\\zenodo (for --apply only;
record reads are public).
"""
import json
import os
import sys
import urllib.parse
import urllib.request

TOKEN_PATH = r"C:\Users\LENOVO\tokens\zenodo"
BASE = "https://zenodo.org"
UA = {"User-Agent": "QNFO-Dissemination-Enhancer/1.0 (rowan.quni@outlook.com)"}


def api_get(path):
    req = urllib.request.Request(BASE + path, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def api_put(path, payload):
    with open(TOKEN_PATH, "r", encoding="utf-8") as f:
        tok = f.read().strip()
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE + path, data=data, method="PUT",
                                 headers={**UA, "Content-Type": "application/json",
                                          "Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def load_json_flag(fname, flag):
    if not fname:
        return []
    with open(fname, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        sys.exit(f"ERROR: {flag} must be a JSON array")
    return data


def community_exists(slug):
    try:
        api_get(f"/api/communities/{urllib.parse.quote(slug)}")
        return True
    except Exception:
        return False


def main():
    args = sys.argv[1:]
    if "--record" not in args:
        sys.exit(__doc__)
    record = args[args.index("--record") + 1]
    apply_flag = "--apply" in args
    subjects = load_json_flag(
        args[args.index("--subjects-json") + 1] if "--subjects-json" in args else None,
        "--subjects-json")
    alternates = load_json_flag(
        args[args.index("--alternate-json") + 1] if "--alternate-json" in args else None,
        "--alternate-json")
    communities = []
    i = 0
    while i < len(args):
        if args[i] == "--community":
            communities.append(args[i + 1])
            i += 2
        else:
            i += 1

    # Resolve record id
    rid = record.split("/")[-1] if "/" in record else record
    rec = api_get(f"/api/records/{rid}")
    md = rec.get("metadata", {})

    print(f"Record: {md.get('title', '?')} (id={rid})")
    print(f"  DOI: {md.get('doi')}")
    print(f"  Mode: {'APPLY' if apply_flag else 'DRY-RUN'} (--apply required to write)")
    print()

    changes = {}

    # ---- D1: subjects ----
    if subjects:
        existing_terms = {s.get("term") for s in md.get("subjects", [])}
        new_subjects = [s for s in subjects if s.get("term") not in existing_terms]
        if new_subjects:
            changes["subjects"] = md.get("subjects", []) + new_subjects
            print(f"[D1] subjects: +{len(new_subjects)} EuroSciVoc entries "
                  f"(existing {len(existing_terms)})")
            for s in new_subjects:
                print(f"     + {s.get('term')} [{s.get('scheme')}] {s.get('identifier')}")
        else:
            print(f"[D1] subjects: no new terms (all {len(existing_terms)} already present)")

    # ---- D2: alternate_identifiers ----
    if alternates:
        existing_alt = {a.get("identifier") for a in md.get("alternate_identifiers", [])}
        new_alt = [a for a in alternates if a.get("identifier") not in existing_alt]
        if new_alt:
            changes["alternate_identifiers"] = md.get("alternate_identifiers", []) + new_alt
            print(f"[D2] alternate_identifiers: +{len(new_alt)} "
                  f"(existing {len(existing_alt)})")
            for a in new_alt:
                print(f"     + {a.get('scheme')}: {a.get('identifier')}")
        else:
            print(f"[D2] alternate_identifiers: no new entries "
                  f"(existing {len(existing_alt)})")

    # ---- D3: communities ----
    if communities:
        existing_com = {c.get("id") for c in md.get("communities", [])}
        ok, missing = [], []
        for slug in communities:
            if slug in existing_com:
                continue
            (ok if community_exists(slug) else missing).append(slug)
        for slug in missing:
            print(f"[D3] WARN: community '{slug}' NOT FOUND on Zenodo — skipped")
        if ok:
            changes["communities"] = md.get("communities", []) + [{"id": s} for s in ok]
            print(f"[D3] communities: +{len(ok)} (existing {len(existing_com)}) -> {ok}")
        else:
            print(f"[D3] communities: no new valid slugs (existing {len(existing_com)})")

    # ---- Apply / report ----
    print()
    if not changes:
        print("No changes proposed. Done.")
        return
    if not apply_flag:
        print("DRY-RUN: proposed changes above. Re-run with --apply to write.")
        return

    # Edit the record (draft edit endpoint), then re-publish not required
    # for metadata-only edits on published records? Zenodo v2: metadata edits
    # on published records go through /api/records/{id}/draft + publish.
    rec_id = rec.get("id")
    draft = api_get(f"/api/records/{rec_id}/draft")
    new_md = draft.get("metadata", {})
    new_md.update(changes)
    api_put(f"/api/records/{rec_id}/draft", {"metadata": new_md})
    print(f"Applied metadata changes to draft of record {rec_id}.")
    print("NOTE: run POST /api/records/{id}/actions/publish to publish the draft "
          "(or the UI) — publishing creates a new version with a new DOI.")
    print("VERIFY: fetch https://zenodo.org/api/records/{id} and check the fields.")


if __name__ == "__main__":
    main()
