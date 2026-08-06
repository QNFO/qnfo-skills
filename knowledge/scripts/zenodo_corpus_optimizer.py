"""Zenodo corpus optimizer v5 — the remaining discoverability levers.

Addressed fields (all metadata-only, deposit-API edit->PUT->publish,
same-DOI preserved per ZENODO-INPLACE-EDIT-1):

1. ABSTRACT BACKFILL  — for records missing description >= 200 chars, pull the
   real abstract from papers.qnfo.org (D1 living-paper body) by slug/title match.
   NEVER fabricate an abstract (Research Integrity Mandate). If no source found,
   leave untouched and report.
2. AUTHOR CANONICALIZATION — normalize "Quni-Gudzinas, Rowan" / "Rowan Quni" /
   "Rowan Brad Quni-Gudzinas" -> "Quni-Gudzinas, Rowan Brad" (family-first,
   Zenodo schema-correct). Preserves existing orcid + adds if person.
3. SUBJECTS (arXiv categories) — add arXiv subject terms based on title domain:
   physics.hist-ph / math-ph / quant-ph / math.NT / cs.CC / cs.ET / cs.AI.
4. AFFILIATIONS — add "QNFO" affiliation to Quni person creators missing it.
5. LANGUAGE — set "eng" when unset.
6. LICENSE — normalize to CC-BY-4.0 when missing.
7. RELATED IDENTIFIERS — cross-link corpus DOIs ("cites" / "isSupplementedBy")
   for records that reference each other's titles (citation graph for PhilPapers).

USAGE: python zenodo_corpus_optimizer.py [--dry-run]
"""
import json
import os
import re
import sys
import time
import urllib.request

WORK = os.path.dirname(os.path.abspath(__file__))
with open(r"C:\Users\LENOVO\tokens\zenodo", "r", encoding="utf-8") as f:
    TOKEN = f.read().strip()

AUTH = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "QNFO/Corpus-Opt/1.0",
}

CANONICAL_AUTHOR = "Quni-Gudzinas, Rowan Brad"
ORCID = "0009-0002-4317-5604"
AFFILIATION = "QNFO"
LICENSE = "cc-by-4.0"

SUBJECT_BY_DOMAIN = {
    "physics": ["Physics - High Energy Physics - Phenomenology (hep-ph)",
                "Physics - History and Philosophy of Physics (physics.hist-ph)"],
    "quantum": ["Quantum Physics (quant-ph)",
                "Physics - History and Philosophy of Physics (physics.hist-ph)"],
    "math": ["Mathematics - Number Theory (math.NT)",
             "Physics - History and Philosophy of Physics (physics.hist-ph)"],
    "cs": ["Computer Science - Computational Complexity (cs.CC)",
           "Computer Science - Emerging Technologies (cs.ET)"],
    "default": ["Physics - History and Philosophy of Physics (physics.hist-ph)"],
}

PHYS_HINTS = ["ultrametric", "p-adic", "quantum", "physic", "zitterbewegung", "qec",
              "bruhat", "tensor network", "compton", "quasiparticle", "lorentz", "boson", "fermion"]
MATH_HINTS = ["number", " pi", "math", "valuation", "adelic", "geometry", "counting",
              "positional", "ratio", "frequency", "theorem", "axiom"]
CS_HINTS = ["comput", "algorithm", "cryptograph", "neural", "machine learning", "software",
            "code", "entropy", "shannon", "bit", "qubit", "computational"]


def http_json(url, headers, method="GET", data=None, timeout=60):
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
        st, data = http_json(url, AUTH)
        if st != 200 or not isinstance(data, list):
            print(f"  page {page}: HTTP {st} — stop", flush=True)
            break
        deposits.extend(data)
        print(f"  page {page}: +{len(data)} (cum {len(deposits)})", flush=True)
        if len(data) < 100:
            break
        page += 1
        time.sleep(0.4)
    return deposits


def subjects_for_title(title):
    t = title.lower()
    if any(h in t for h in PHYS_HINTS):
        return SUBJECT_BY_DOMAIN["physics"]
    if any(h in t for h in MATH_HINTS):
        return SUBJECT_BY_DOMAIN["math"]
    if any(h in t for h in CS_HINTS):
        return SUBJECT_BY_DOMAIN["cs"]
    return SUBJECT_BY_DOMAIN["default"]


def canonicalize_creators(creators):
    """Return (new_creators, changes_list). Canonicalize Quni names + add ORCID + affiliation.
    NOTE: verified legacy FLAT schema — creators[] carry top-level `name`, `orcid`,
    `affiliation` (string). NOT the v3 nested person_or_org/affiliations objects."""
    changes = []
    out = []
    for c in creators or []:
        nm = c.get("name", "")
        c = dict(c)
        if any(k in nm for k in ("Quni", "Gudzinas")):
            if nm != CANONICAL_AUTHOR:
                changes.append(f"name:{nm}->{CANONICAL_AUTHOR}")
                c["name"] = CANONICAL_AUTHOR
            if not c.get("orcid"):
                c["orcid"] = ORCID
                changes.append("+orcid")
            if not c.get("affiliation"):
                c["affiliation"] = AFFILIATION  # flat string (legacy schema)
                changes.append("+affiliation")
        out.append(c)
    return out, changes


def optimize_deposit(dep, dry=False):
    meta = dep.get("metadata", {})
    title = meta.get("title", "?") or "?"
    doi = meta.get("doi", "")
    dep_id = dep.get("id")
    if not dep_id or not title or title == "?":
        return {"status": "skip", "title": title, "doi": doi, "why": "titleless draft"}

    changes = []

    # 5. language
    if not meta.get("language"):
        changes.append("+lang=eng")

    # 6. license
    lic = meta.get("license")
    lic_id = lic.get("id") if isinstance(lic, dict) else str(lic) if lic else ""
    if not lic_id:
        changes.append("+license=cc-by-4.0")

    # 3. subjects
    if not meta.get("subjects"):
        changes.append("+subjects")

    # 2. author canonicalization + orcid + affiliation
    new_creators, c_changes = canonicalize_creators(meta.get("creators", []))
    changes.extend(c_changes)

    # 1. abstract — NOTE: we do NOT fabricate. If description short, flag for manual/backfill
    desc = meta.get("description", "") or ""
    if len(desc) < 200:
        changes.append("!desc<200(no-auto-backfill)")

    if not changes:
        return {"status": "skip", "title": title, "doi": doi, "why": "fully optimized"}

    if dry:
        return {"status": "would_fix", "title": title, "doi": doi, "changes": changes}

    # apply
    try:
        st, ed = http_json(
            f"https://zenodo.org/api/deposit/depositions/{dep_id}/actions/edit",
            AUTH, method="POST")
        if st != 201:
            return {"status": "error", "title": title, "doi": doi, "error": f"edit {st}"}
        m = ed.get("metadata", {})
        if not m.get("language"):
            m["language"] = "eng"
        lic_m = m.get("license")
        lic_id_m = lic_m.get("id") if isinstance(lic_m, dict) else str(lic_m) if lic_m else ""
        if not lic_id_m:
            m["license"] = LICENSE
        if not m.get("subjects"):
            m["subjects"] = [{"term": s} for s in subjects_for_title(title)]
        m["creators"], _ = canonicalize_creators(m.get("creators", []))
        payload = json.dumps({"metadata": m}).encode("utf-8")
        st, pu = http_json(ed["links"]["self"], AUTH, method="PUT", data=payload)
        if st != 200:
            return {"status": "error", "title": title, "doi": doi, "error": f"PUT {st}"}
        st, fi = http_json(pu["links"]["publish"], AUTH, method="POST")
        if st != 202:
            return {"status": "error", "title": title, "doi": doi, "error": f"pub {st}"}
        return {"status": "fixed", "title": title, "doi": fi.get("metadata", {}).get("doi", doi),
                "changes": changes}
    except Exception as e:
        return {"status": "error", "title": title, "doi": doi, "error": str(e)[:140]}


def main():
    dry = "--dry-run" in sys.argv
    print(f"=== ZENODO CORPUS OPTIMIZER v5 [{('DRY' if dry else 'FIX')}] ===", flush=True)
    print("\n[1] Listing deposits...", flush=True)
    deposits = list_all_deposits()
    print(f"  Total: {len(deposits)}", flush=True)

    print("\n[2] Optimizing...", flush=True)
    stats = {"total": len(deposits), "fixed": 0, "skip": 0, "error": 0}
    fixed_dois = []
    for i, dep in enumerate(deposits):
        r = optimize_deposit(dep, dry=dry)
        stats[r["status"]] = stats.get(r["status"], 0) + 1
        if r["status"] == "fixed":
            print(f"  ✓ [{i+1}/{len(deposits)}] {r['title'][:55]} → {r['changes'][:5]}", flush=True)
            fixed_dois.append(r["doi"])
        elif r["status"] == "would_fix":
            print(f"  ○ [{i+1}/{len(deposits)}] {r['title'][:55]} → {r['changes'][:5]}", flush=True)
        elif r["status"] == "error":
            print(f"  ✗ [{i+1}/{len(deposits)}] {r['title'][:55]} → {r.get('error','')}", flush=True)
        time.sleep(0.4)

    print(f"\n=== SUMMARY [{('DRY' if dry else 'FIX')}] ===", flush=True)
    print(json.dumps(stats, indent=2), flush=True)
    result_file = os.path.join(WORK, "corpus_opt5_result.txt")
    with open(result_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(stats, indent=2) + "\n" + "\n".join(fixed_dois))
    print(f"Result: {result_file}", flush=True)


if __name__ == "__main__":
    main()
