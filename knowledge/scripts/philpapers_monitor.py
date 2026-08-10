#!/usr/bin/env python3
"""
PhilPapers Index Monitor — Autonomous Watchtower
=================================================
Periodically checks PhilPapers for new QNFO-indexed records,
compares against Zenodo corpus, and alerts on gaps.

SCHEDULING (knowledge v2.9, 2026-08-10):
  Runs MONTHLY (1st of month, 06:00 UTC). NOT daily.
  Rationale: PhilPapers indexing pipeline (Zenodo -> DataCite ->
  CrossRef -> PhilPapers crawler) runs on a days-to-weeks crawl
  cycle; daily polling yields no signal. The prior "daily cron
  ffc8f08f" claim was a phantom — that cron never existed in the
  scheduler (red-team audit 2026-08-10).

DOMAIN-SCOPE POLICY (knowledge v2.9, 2026-08-10):
  Only papers that ARE philosophy-domain papers are PhilPapers
  candidates. Non-philosophy QNFO records (physics, engineering,
  licensing, patent filings, finance briefs) must NOT carry
  philosophy-class keywords. Coverage is computed against the
  philosophy-eligible subset, not the whole 680-record corpus.

USAGE:
  python philpapers_monitor.py [--alert] [--reset]
"""

import json
import re
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

AUTHOR_CODE = "QUN"  # PhilPapers author prefix for Quni-Gudzinas
PHILPAPERS_SEARCH_URL = "https://philpapers.org/s/{author}"
ORCID_IDENTIFIER = "0009-0002-4317-5604"
KNOWN_INDEXED = {
    "QUNTUF": {
        "title": "The Ultrametric Foundation: A Unified Thesis on Number, Time, Knowledge, and Computation",
        "doi": "10.5281/zenodo.21208346",
        "first_seen": "2026-08-06",
    },
    "QUNSAI": {
        "title": "Scaffolds and Invariants: An Epistemic Hygiene Audit of pi, Number Bases, and Geometric Centers",
        "doi": "10.5281/zenodo.21255344",
        "first_seen": "2026-08-06",
    },
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; QNFO-PhilPapers-Monitor/2.0; +https://qnfo.org)",
    "Accept": "text/html,application/json",
}

import os as _os
STATE_FILE = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                          "philpapers_monitor_state.json")

# Philosophy-class keyword labels. Present on a record => that record is
# claiming to be a philosophy paper. (Domain terms like "consilience",
# "measurement theory", "foundations of quantum mechanics" are NOT in this
# list — they are cross-domain methodology terms, not philosophy labels.)
PHIL_LABELS = [
    "philosophy of physics", "philosophy of mathematics",
    "philosophy of science", "philosophy of information",
    "epistemology", "metaphysics", "ontology",
    "structural realism", "paradigm theory",
]


def load_state():
    """Load persisted monitoring state."""
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "known_indexed": KNOWN_INDEXED.copy(),
            "last_check": None,
            "total_checks": 0,
            "new_discoveries": [],
        }


def save_state(state):
    """Persist monitoring state."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


def search_philpapers_author(author_code):
    """Search PhilPapers for an author's records."""
    url = PHILPAPERS_SEARCH_URL.format(author=urllib.parse.quote(author_code))

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "html": ""}
    except Exception as e:
        return {"error": str(e), "html": ""}

    # Parse record IDs from the page
    rec_pattern = re.compile(r'/rec/(QUN\w+)')
    title_pattern = re.compile(r'<meta name="citation_title" content="([^"]*)"')
    doi_pattern = re.compile(r'<meta name="citation_doi" content="([^"]*)"')

    records = []
    seen_ids = set()

    for match in rec_pattern.finditer(html):
        rec_id = match.group(1)
        if rec_id not in seen_ids:
            seen_ids.add(rec_id)
            records.append({"id": rec_id})

    titles = title_pattern.findall(html)
    dois = doi_pattern.findall(html)

    for i, rec in enumerate(records):
        if i < len(titles):
            rec["title"] = titles[i]
        if i < len(dois):
            rec["doi"] = dois[i]

    return {"records": records, "count": len(records)}


def get_zenodo_corpus():
    """Get all Zenodo records by ORCID identifier.

    v2 (2026-08-10): canonical query is the ORCID identifier query —
    fuzzy name queries ("Rowan Quni", "Quni-Gudzinas") return 0 hits or
    unrelated records (names stored as "Quni-Gudzinas, Rowan Brad").
    Unauthenticated API caps size at 25 (observed 2026-08-10), so this
    paginates with size=25 instead of the old size=250 (HTTP 400).
    """
    query = urllib.parse.quote(
        f'metadata.creators.person_or_org.identifiers.identifier:"{ORCID_IDENTIFIER}"'
    )
    records = []
    page = 1
    size = 25
    while True:
        url = f"https://zenodo.org/api/records?q={query}&size={size}&page={page}&sort=mostrecent"
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "QNFO/1.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e), "records": records, "count": len(records)}

        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            break
        for hit in hits:
            meta = hit.get("metadata", {})
            creators = meta.get("creators", [])
            orcid_ok = False
            for c in creators:
                ids = c.get("person_or_org", {}).get("identifiers", [])
                for iid in ids:
                    if ORCID_IDENTIFIER in str(iid.get("identifier", "")):
                        orcid_ok = True
                        break
                if c.get("orcid") == ORCID_IDENTIFIER:
                    orcid_ok = True
                if orcid_ok:
                    break
            if orcid_ok:
                records.append({
                    "title": meta.get("title", ""),
                    "doi": meta.get("doi", ""),
                    "keywords": meta.get("keywords", []),
                    "description": meta.get("description", ""),
                    "pubdate": meta.get("publication_date", ""),
                })

        total = data.get("hits", {}).get("total", 0)
        if len(records) >= total or len(hits) < size:
            break
        page += 1
        time.sleep(0.3)

    return {"records": records, "count": len(records)}


def is_philosophy_paper(rec):
    """Domain-scope check: does this record carry a philosophy-class label?"""
    kws = " ".join(k.lower() for k in rec.get("keywords", []))
    return any(label in kws for label in PHIL_LABELS)


def compare_corpora(philpapers_recs, zenodo_recs, known):
    """Compare PhilPapers index vs Zenodo corpus, find gaps.

    Coverage denominator (v2.9 policy): philosophy-eligible records only —
    non-philosophy QNFO records are not PhilPapers candidates.
    """
    phil_ids = {r.get("id") for r in philpapers_recs}
    known_ids = set(known.keys())

    new_ids = phil_ids - known_ids
    total_zenodo = zenodo_recs.get("count", 0)

    phil_eligible = [r for r in zenodo_recs.get("records", [])
                     if is_philosophy_paper(r)]
    total_phil = len(philpapers_recs)
    denominator = max(len(phil_eligible), 1)
    coverage_pct = (total_phil / denominator * 100) if denominator else 0

    return {
        "total_zenodo": total_zenodo,
        "philosophy_eligible": len(phil_eligible),
        "total_philpapers": total_phil,
        "coverage_pct": round(coverage_pct, 1),
        "new_ids": list(new_ids),
        "known_ids": list(known_ids),
    }


def run_check():
    """Run a single monitoring check cycle."""
    state = load_state()
    now = datetime.now(timezone.utc).isoformat()

    print(f"=== PhilPapers Monitor Check @ {now} ===")

    # 1. Search PhilPapers
    print("Searching PhilPapers for QUN records...")
    pp_result = search_philpapers_author(AUTHOR_CODE)

    if pp_result.get("error"):
        print(f"  WARNING: PhilPapers search failed: {pp_result['error']}")
        print("  (PhilPapers is Cloudflare-blocked; will retry next cycle)")
        # v2: every cycle counts, even failed ones (was: only successes)
        state["last_check"] = now
        state["total_checks"] = state.get("total_checks", 0) + 1
        save_state(state)
        return state

    pp_records = pp_result.get("records", [])
    print(f"  Found {len(pp_records)} PhilPapers records")
    for r in pp_records:
        print(f"    - {r.get('id')}: {r.get('title', 'N/A')[:80]}")

    # 2. Compare with known
    new = [r for r in pp_records if r.get("id") not in state["known_indexed"]]

    if new:
        print(f"\n  *** {len(new)} NEW RECORDS DETECTED ***")
        for r in new:
            print(f"    NEW: {r.get('id')}: {r.get('title', 'N/A')[:80]}")
            state["known_indexed"][r["id"]] = {
                "title": r.get("title", "unknown"),
                "doi": r.get("doi", "unknown"),
                "first_seen": now,
            }
            state["new_discoveries"].append({
                "id": r["id"],
                "title": r.get("title", "unknown"),
                "discovered_at": now,
            })
    else:
        print(f"\n  No new records. Currently tracking {len(state['known_indexed'])} records.")

    # 3. Get Zenodo corpus for coverage estimate
    print("\nFetching Zenodo corpus for coverage estimate...")
    zenodo = get_zenodo_corpus()
    if zenodo.get("error"):
        print(f"  Zenodo fetch failed: {zenodo['error']} (using {zenodo.get('count', 0)} cached records)")
    else:
        print(f"  Zenodo: {zenodo.get('count')} ORCID records")

    # 4. Coverage report (domain-scoped denominator)
    coverage = compare_corpora(pp_records, zenodo, state["known_indexed"])
    print(f"  Coverage (philosophy-eligible): {coverage['total_philpapers']}/{coverage['philosophy_eligible']} = {coverage['coverage_pct']}%")
    print(f"  Total Zenodo records: {coverage['total_zenodo']}")

    state["last_check"] = now
    state["total_checks"] = state.get("total_checks", 0) + 1
    state["last_coverage"] = coverage
    save_state(state)

    return state


def main():
    import argparse
    parser = argparse.ArgumentParser(description="PhilPapers Index Monitor (v2, monthly)")
    parser.add_argument("--alert", action="store_true", help="Print alert if new records found")
    parser.add_argument("--reset", action="store_true", help="Reset monitoring state")
    args = parser.parse_args()

    if args.reset:
        state = {
            "known_indexed": KNOWN_INDEXED.copy(),
            "last_check": None,
            "total_checks": 0,
            "new_discoveries": [],
        }
        save_state(state)
        print("State reset. Now tracking 2 known records.")
        return

    state = run_check()

    recent = [
        d for d in state.get("new_discoveries", [])
        if d.get("discovered_at", "").startswith(datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    ]
    if recent and args.alert:
        print(f"\nALERT: {len(recent)} new PhilPapers records today!")
        for d in recent:
            print(f"  {d['id']}: {d['title']}")


if __name__ == "__main__":
    main()
