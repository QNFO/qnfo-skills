#!/usr/bin/env python3
"""zenodo_stats.py — fetch per-record view/download stats from the Zenodo
records API and write a snapshot + top-directions report.

Reliable surface: GET /api/records/{id} -> "stats" {downloads, unique_downloads,
views, unique_views, version_*}. (The /stats endpoints 404; DataCite events
time out.) Reads the corpus DOI list from D1 living-paper (published+distributed),
dedupes by DOI, fetches stats sequentially (polite delay, browser UA), writes:
  artifacts/zenodo_stats_snapshot_<ts>.json
  artifacts/zenodo_stats_top20_<ts>.md
Stdlib only. Thin-client: evidence written under the CWD's artifacts/ dir.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
DELAY = 0.25
CORPUS = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("corpus_dois.json")
OUT_DIR = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("artifacts")


def fetch_record(doi: str) -> dict | None:
    rid = doi.rsplit(".", 1)[-1]  # zenodo record id
    url = f"https://zenodo.org/api/records/{rid}"
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            d = json.loads(resp.read())
        stats = d.get("stats", {})
        return {
            "doi": d.get("doi", doi),
            "conceptrecid": d.get("conceptrecid"),
            "conceptdoi": d.get("conceptdoi"),
            "title": (d.get("metadata", {}) or {}).get("title", ""),
            "downloads": stats.get("downloads", 0),
            "unique_downloads": stats.get("unique_downloads", 0),
            "views": stats.get("views", 0),
            "unique_views": stats.get("unique_views", 0),
            "version_downloads": stats.get("version_downloads", 0),
        }
    except Exception as e:  # noqa: BLE001
        return {"doi": doi, "error": str(e)[:100]}


def main() -> int:
    rows = json.loads(CORPUS.read_text(encoding="utf-8"))
    # filter to published + distributed
    keep = [r for r in rows if r.get("status") in ("published", "distributed")]
    # dedupe by zenodo_doi (chapter fragments share DOIs); keep first slug
    by_doi = {}
    for r in keep:
        by_doi.setdefault(r["zenodo_doi"], r)
    print(f"records with zenodo_doi: {len(rows)} | published/distributed: {len(keep)} | unique DOIs: {len(by_doi)}")

    results = []
    errors = 0
    for i, (doi, r) in enumerate(sorted(by_doi.items()), 1):
        rec = fetch_record(doi)
        if rec.get("error"):
            errors += 1
            if errors <= 5:
                print(f"  ERR {doi}: {rec['error']}")
        else:
            rec["slug"] = r.get("slug")
        results.append(rec)
        if i % 50 == 0:
            print(f"  fetched {i}/{len(by_doi)} (errors {errors})", flush=True)
        time.sleep(DELAY)

    ok = [r for r in results if "error" not in r]
    ts = time.strftime("%Y%m%d-%H%M%S")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    snap = {"fetched_at": ts, "total_unique_dois": len(by_doi),
            "records": results}
    (OUT_DIR / f"zenodo_stats_snapshot_{ts}.json").write_text(
        json.dumps(snap, indent=1), encoding="utf-8")

    # top-20 report
    def top(key):
        return sorted(ok, key=lambda r: -r.get(key, 0))[:20]

    lines = [f"# Zenodo analytics snapshot — {ts}",
             f"Unique records: {len(ok)} (errors {errors})",
             "", "## Top 20 by downloads", ""]
    lines.append("| # | downloads (unique) | views | title | doi |")
    lines.append("|--|--|--|--|--|")
    for i, r in enumerate(top("downloads"), 1):
        lines.append(f"| {i} | {r['downloads']} ({r['unique_downloads']}) | {r['views']} | {(r['title'] or '')[:60]} | {r['doi']} |")
    lines += ["", "## Top 20 by views", ""]
    lines.append("| # | views (unique) | downloads | title | doi |")
    lines.append("|--|--|--|--|--|")
    for i, r in enumerate(top("views"), 1):
        lines.append(f"| {i} | {r['views']} ({r['unique_views']}) | {r['downloads']} | {(r['title'] or '')[:60]} | {r['doi']} |")
    (OUT_DIR / f"zenodo_stats_top20_{ts}.md").write_text(
        "\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
