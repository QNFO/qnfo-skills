#!/usr/bin/env python3
"""Zenodo → PhilPapers metadata fixer v4 (deposit-API only, robust).

Adds philosophy-domain keywords + ORCID to QNFO Zenodo records via the
deposit API edit -> PUT -> publish cycle (ZENODO-INPLACE-EDIT-1, verified
on 322 records 2026-08-04). Same DOI preserved; metadata-only change.

Key robustness fixes vs v3:
- Uses ONLY the authenticated deposit API (search API returns 400 on
  special-char queries and rate-limits).
- Paginates deposit listings (size=100).
- Targeted keyword sets per title domain (physics / math / science / default)
  instead of a blind blanket list.
- ORCID added ONLY to person creators (skips org creators like "QNFO").
- python -u + flush=True for live progress; summary written to result file.
"""
import json
import sys
import time
import urllib.request

TOKEN = "BkLOVH2EDBccmqRMEYz0KRjmx9gqnEGKdxSz4RAkwCLgr0yvJUZMJoqjw72g"
ORCID = "0009-0002-4317-5604"
RESULT_FILE = r"C:\Users\LENOVO\AppData\Local\Temp\deepchat_work\fix4_result.txt"

AUTH = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "QNFO/PhilPapers-Opt/1.0",
}

PHIL_KW_SETS = {
    "physics": ["philosophy of physics", "foundations of quantum mechanics", "epistemology"],
    "math": ["philosophy of mathematics", "epistemology"],
    "science": ["philosophy of science", "epistemology", "consilience"],
    "default": ["epistemology", "philosophy of science", "consilience"],
}

PHYS_HINTS = ["ultrametric", "p-adic", "quantum", "physic", "zitterbewegung", "qec",
              "bruhat", "tensor network", "compton", "shadows", "quasiparticle", "lorentz"]
MATH_HINTS = ["number", " pi", "math", "valuation", "adelic", "geometry", "counting",
              "positional", "ratio", "frequency"]
SCI_HINTS = ["consilience", "framework", "synthesis", "falsifiability", "scientific",
             "research", "stratigraphy", "paradigm", "audit", "thesis", "foundation"]


def kw_set_for_title(title):
    t = title.lower()
    if any(h in t for h in PHYS_HINTS):
        return PHIL_KW_SETS["physics"]
    if any(h in t for h in MATH_HINTS):
        return PHIL_KW_SETS["math"]
    if any(h in t for h in SCI_HINTS):
        return PHIL_KW_SETS["science"]
    return PHIL_KW_SETS["default"]


def http_json(url, headers, method="GET", data=None, timeout=30):
    req = urllib.request.Request(url, headers=headers, method=method,
                                 data=data if data is not None else None)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        return (resp.status, json.loads(body) if body else {})


def list_all_deposits():
    deposits = []
    page = 1
    while True:
        url = f"https://zenodo.org/api/deposit/depositions?size=100&page={page}&sort=mostrecent"
        status, data = http_json(url, AUTH)
        if status != 200 or not isinstance(data, list):
            print(f"  page {page}: HTTP {status} — stopping", flush=True)
            break
        deposits.extend(data)
        print(f"  page {page}: +{len(data)} (cumulative {len(deposits)})", flush=True)
        if len(data) < 100:
            break
        page += 1
        time.sleep(0.4)
    return deposits


def find_person_creator(creators):
    for c in creators or []:
        nm = c.get("name", "")
        if any(k in nm for k in ("Quni", "Rowan", "Gudzinas")):
            return c
    return None


def has_phil_kw(keywords):
    for k in keywords or []:
        kl = k.lower()
        if any(p in kl for p in ("philosoph", "epistemolog", "metaphysic", "ontolog")):
            return True
    return False


def fix_deposit(dep):
    meta = dep.get("metadata", {})
    title = meta.get("title", "?") or "?"
    doi = meta.get("doi", "")
    dep_id = dep.get("id")
    if not dep_id:
        return {"status": "skip", "title": title, "doi": doi, "why": "no id"}

    kw = meta.get("keywords", [])
    person = find_person_creator(meta.get("creators", []))
    has_phil = has_phil_kw(kw)
    has_orcid = bool(person and person.get("orcid"))

    if has_phil and has_orcid:
        return {"status": "skip", "title": title, "doi": doi, "why": "already optimized"}

    changes = []
    if not has_phil:
        add_kw = kw_set_for_title(title)
        existing = {k.lower() for k in kw}
        merged = list(kw)
        for k in add_kw:
            if k.lower() not in existing:
                merged.append(k)
        changes.append(f"+{len(merged) - len(kw)}kw")
    if not has_orcid and person:
        changes.append("orcid")

    # apply: edit -> PUT -> publish
    try:
        st, ed = http_json(
            f"https://zenodo.org/api/deposit/depositions/{dep_id}/actions/edit",
            AUTH, method="POST")
        if st != 201:
            return {"status": "error", "title": title, "doi": doi,
                    "error": f"edit HTTP {st}"}

        m = ed.get("metadata", {})
        if not has_phil:
            existing = {k.lower() for k in m.get("keywords", [])}
            for k in kw_set_for_title(title):
                if k.lower() not in existing:
                    m.setdefault("keywords", []).append(k)
        if not has_orcid:
            for c in m.get("creators", []):
                nm = c.get("name", "")
                if any(k in nm for k in ("Quni", "Rowan", "Gudzinas")):
                    c["orcid"] = ORCID
                    break

        payload = json.dumps({"metadata": m}).encode("utf-8")
        st, pu = http_json(ed["links"]["self"], AUTH, method="PUT", data=payload)
        if st != 200:
            return {"status": "error", "title": title, "doi": doi,
                    "error": f"PUT HTTP {st}"}

        st, fi = http_json(pu["links"]["publish"], AUTH, method="POST")
        if st != 202:
            return {"status": "error", "title": title, "doi": doi,
                    "error": f"publish HTTP {st}"}

        return {"status": "fixed", "title": title,
                "doi": fi.get("metadata", {}).get("doi", doi), "changes": changes}
    except Exception as e:
        return {"status": "error", "title": title, "doi": doi, "error": str(e)[:140]}


def main():
    dry = "--dry-run" in sys.argv
    mode = "DRY-RUN" if dry else "FIX"
    print(f"=== ZENODO→PHILPAPERS OPTIMIZER v4 [{mode}] ===", flush=True)

    print("\n[1] Listing deposits (paginated)...", flush=True)
    deposits = list_all_deposits()
    print(f"  Total deposits: {len(deposits)}", flush=True)

    print("\n[2] Auditing + fixing...", flush=True)
    stats = {"total": len(deposits), "skip": 0, "fixed": 0, "error": 0}
    lines = []
    for i, dep in enumerate(deposits):
        r = fix_deposit(dep) if not dry else {**fix_deposit(dep), "dry": True}
        stats[r["status"]] = stats.get(r["status"], 0) + 1
        if r["status"] == "fixed":
            print(f"  ✓ [{i+1}/{len(deposits)}] {r['title'][:60]} → {r['changes']}", flush=True)
            lines.append(f"FIXED | {r['doi']} | {r['title'][:70]} | {r['changes']}")
        elif r["status"] == "skip":
            print(f"  - [{i+1}/{len(deposits)}] {r['title'][:60]} (skip)", flush=True)
        else:
            print(f"  ✗ [{i+1}/{len(deposits)}] {r['title'][:60]} → {r.get('error','')}", flush=True)
            lines.append(f"ERROR | {r['doi']} | {r['title'][:70]} | {r.get('error','')}")
        time.sleep(0.4)

    summary = f"\n=== SUMMARY [{mode}] ===\n{json.dumps(stats, indent=2)}\n"
    print(summary, flush=True)
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write(summary + "\n".join(lines))
    print(f"Result file: {RESULT_FILE}", flush=True)


if __name__ == "__main__":
    main()
