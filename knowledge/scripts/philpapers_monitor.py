#!/usr/bin/env python3
"""
PhilPapers Index Monitor — Autonomous Watchtower
=================================================
Periodically checks PhilPapers for new QNFO-indexed records,
compares against Zenodo corpus, and alerts on gaps.

Scheduled Task: runs daily (cron ffc8f08f, 06:00 UTC),
reports new PhilPapers entries.

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
    "User-Agent": "Mozilla/5.0 (compatible; QNFO-PhilPapers-Monitor/1.0; +https://qnfo.org)",
    "Accept": "text/html,application/json",
}

STATE_FILE = "philpapers_monitor_state.json"


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
    # PhilPapers record IDs look like: /rec/QUNXXX
    rec_pattern = re.compile(r'/rec/(QUN\w+)')
    title_pattern = re.compile(r'<meta name="citation_title" content="([^"]*)"')
    doi_pattern = re.compile(r'<meta name="citation_doi" content="([^"]*)"')

    records = []
    seen_ids = set()

    # Find all record links
    for match in rec_pattern.finditer(html):
        rec_id = match.group(1)
        if rec_id not in seen_ids:
            seen_ids.add(rec_id)
            records.append({"id": rec_id})

    # Try to extract titles and DOIs
    titles = title_pattern.findall(html)
    dois = doi_pattern.findall(html)

    for i, rec in enumerate(records):
        if i < len(titles):
            rec["title"] = titles[i]
        if i < len(dois):
            rec["doi"] = dois[i]

    return {"records": records, "count": len(records)}


def get_zenodo_corpus():
    """Get all Zenodo records by the author for comparison."""
    query = urllib.parse.quote("Rowan Quni")
    url = f"https://zenodo.org/api/records?q={query}&size=250"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "QNFO/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e), "records": []}

    records = []
    for hit in data.get("hits", {}).get("hits", []):
        creators = hit.get("metadata", {}).get("creators", [])
        if any("Quni" in c.get("name", "") or "Rowan" in c.get("name", "") for c in creators):
            records.append({
                "title": hit.get("metadata", {}).get("title", ""),
                "doi": hit.get("metadata", {}).get("doi", ""),
                "keywords": hit.get("metadata", {}).get("keywords", []),
                "pubdate": hit.get("metadata", {}).get("publication_date", ""),
            })

    return {"records": records, "count": len(records)}


def compare_corpora(philpapers_recs, zenodo_recs, known):
    """Compare PhilPapers index vs Zenodo corpus, find gaps."""
    phil_ids = {r.get("id") for r in philpapers_recs}
    known_ids = set(known.keys())

    new_ids = phil_ids - known_ids
    total_zenodo = zenodo_recs.get("count", 0)
    total_phil = len(philpapers_recs)

    # Estimate coverage
    coverage_pct = (total_phil / total_zenodo * 100) if total_zenodo > 0 else 0

    return {
        "total_zenodo": total_zenodo,
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
        print("  (PhilPapers may be rate-limiting or blocking; will retry next cycle)")
        state["last_check"] = now
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
            print(f"    🆕 {r.get('id')}: {r.get('title', 'N/A')[:80]}")
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
    print(f"  Zenodo: {zenodo.get('count', '?')} Quni records")

    # 4. Coverage report
    coverage = round(len(state["known_indexed"]) / zenodo.get("count", 1) * 100, 1)
    print(f"  Coverage: {len(state['known_indexed'])}/{zenodo.get('count', '?')} = {coverage}%")

    state["last_check"] = now
    state["total_checks"] = state.get("total_checks", 0) + 1
    state["last_coverage"] = coverage
    save_state(state)

    return state


def main():
    import argparse
    parser = argparse.ArgumentParser(description="PhilPapers Index Monitor")
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

    # Alert if new records
    recent = [
        d for d in state.get("new_discoveries", [])
        if d.get("discovered_at", "").startswith(datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    ]
    if recent and args.alert:
        print(f"\n⚠️  ALERT: {len(recent)} new PhilPapers records today!")
        for d in recent:
            print(f"  {d['id']}: {d['title']}")


if __name__ == "__main__":
    main()
