#!/usr/bin/env python3
"""zenodo_stats_delta.py — weekly Zenodo analytics delta job.

Fetches per-record view/download stats from the public Zenodo records API for
the QNFO corpus (D1 living-paper, status published|distributed, deduped by
zenodo_doi), upserts into qnfo-audit.zenodo_stats carrying prev_* growth deltas,
and prints a delta report (totals old -> new + top movers).

Companion to zenodo_stats.py (local artifacts); THIS job persists to D1
(qnfo-audit.zenodo_stats) so weekly growth is comparable without artifact hunts.

Stdlib only. Credential discovery (in order):
  token:     CLOUDFLARE_API_TOKEN env, ~/.cloudflare_token, ~/keys.json
             (cloudflare_api_token), ~/tokens/cloudflare
  account:   ~/.deepchat/d1-cache.json -> account_id (fallback documented ID)
  db UUIDs:  ~/.deepchat/d1-cache.json -> databases[name] (fallback documented IDs)

Usage: python zenodo_stats_delta.py [--dry-run]
Exit 0 on success (report printed); exit 1 on fatal errors (cron notifies).
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
DELAY = 0.1
LOG = Path(os.environ.get("USERPROFILE", ".")) / ".deepchat" / "skills" / "research" / "logs" / "zenodo-stats-delta.log"

ACCOUNT_FALLBACK = "edb167b78c9fb901ea5bca3ce58ccc4b"
DB_FALLBACK = {
    "living-paper": "70a58cb3-b2cd-498d-877f-ecca86859a22",
    "qnfo-audit": "35e2e573-92f3-46ac-83c6-22f6429fc5e5",
}


def discover_token():
    cand = os.environ.get("CLOUDFLARE_API_TOKEN")
    if cand and cand.startswith("cfat_") and len(cand) > 20:
        return cand.strip()
    for p in (Path(os.environ.get("USERPROFILE", ".")) / ".cloudflare_token",
              Path(os.environ.get("USERPROFILE", ".")) / "tokens" / "cloudflare"):
        if p.exists():
            cand = p.read_text(encoding="utf-8").strip()
            if cand.startswith("cfat_") and len(cand) > 20:
                return cand
    keys = Path(os.environ.get("USERPROFILE", ".")) / "keys.json"
    if keys.exists():
        try:
            cand = json.loads(keys.read_text(encoding="utf-8")).get("cloudflare_api_token")
            if cand and cand.startswith("cfat_") and len(cand) > 20:
                return cand.strip()
        except (json.JSONDecodeError, KeyError):
            pass
    print("FATAL: cannot discover CLOUDFLARE_API_TOKEN", file=sys.stderr)
    sys.exit(1)


def discover_ids():
    cache = Path(os.environ.get("USERPROFILE", ".")) / ".deepchat" / "d1-cache.json"
    account = ACCOUNT_FALLBACK
    dbs = dict(DB_FALLBACK)
    if cache.exists():
        try:
            c = json.loads(cache.read_text(encoding="utf-8"))
            if c.get("account_id"):
                account = c["account_id"]
            dbs.update(c.get("databases", {}))
        except (json.JSONDecodeError, KeyError):
            pass
    return account, dbs


def d1(token, account, db_uuid, sql, params=()):
    url = (f"https://api.cloudflare.com/client/v4/accounts/{account}"
           f"/d1/database/{db_uuid}/query")
    body = json.dumps({"sql": sql, "params": list(params)}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        out = json.loads(resp.read().decode("utf-8"))
    if not out.get("success"):
        raise RuntimeError(f"D1 error: {out.get('errors')}")
    res = out.get("result")
    # D1 REST returns an array of statement results (one element per statement),
    # each carrying {"results": [...rows...], ...}. Unwrap to flat rows.
    if isinstance(res, list) and res and isinstance(res[0], dict) and "results" in res[0]:
        rows = []
        for stmt in res:
            rows.extend(stmt.get("results") or [])
        return rows
    return res or []


def fetch_record(doi):
    rid = doi.rsplit(".", 1)[-1]
    req = urllib.request.Request(f"https://zenodo.org/api/records/{rid}", headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            d = json.loads(resp.read())
        stats = d.get("stats", {}) or {}
        return {
            "doi": d.get("doi", doi),
            "conceptrecid": d.get("conceptrecid"),
            "conceptdoi": d.get("conceptdoi"),
            "title": ((d.get("metadata") or {}).get("title") or "")[:200],
            "downloads": int(stats.get("downloads", 0) or 0),
            "unique_downloads": int(stats.get("unique_downloads", 0) or 0),
            "views": int(stats.get("views", 0) or 0),
            "unique_views": int(stats.get("unique_views", 0) or 0),
            "version_downloads": int(stats.get("version_downloads", 0) or 0),
        }
    except Exception as e:  # noqa: BLE001
        return {"doi": doi, "error": str(e)[:100]}


UPSERT = """
INSERT INTO zenodo_stats
  (doi, conceptdoi, title, slug, downloads, unique_downloads, views,
   unique_views, version_downloads, prev_downloads, prev_views,
   fetched_at, updated_at)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?, datetime('now'))
ON CONFLICT(doi) DO UPDATE SET
  prev_downloads = zenodo_stats.downloads,
  prev_views     = zenodo_stats.views,
  downloads      = excluded.downloads,
  unique_downloads = excluded.unique_downloads,
  views          = excluded.views,
  unique_views   = excluded.unique_views,
  version_downloads = excluded.version_downloads,
  title          = excluded.title,
  slug           = excluded.slug,
  conceptdoi     = excluded.conceptdoi,
  fetched_at     = excluded.fetched_at,
  updated_at     = datetime('now')
"""


def main():
    dry = "--dry-run" in sys.argv
    token = discover_token()
    account, dbs = discover_ids()
    lp_uuid, au_uuid = dbs["living-paper"], dbs["qnfo-audit"]

    corpus = d1(token, account, lp_uuid, (
        "SELECT zenodo_doi, slug, status FROM papers "
        "WHERE zenodo_doi IS NOT NULL AND zenodo_doi != '' "
        "AND status IN ('published','distributed')"))
    by_doi = {}
    for row in corpus:
        doi = (row.get("zenodo_doi") or "").strip()
        if doi and doi != "pending" and doi not in by_doi:
            by_doi[doi] = row
    print(f"corpus: {len(corpus)} rows -> {len(by_doi)} unique DOIs", flush=True)

    prev_rows = d1(token, account, au_uuid,
                   "SELECT doi, downloads, views FROM zenodo_stats")
    prev_map = {r["doi"]: r for r in prev_rows}
    prev_tot = {
        "dl": sum(int(r["downloads"] or 0) for r in prev_rows),
        "vw": sum(int(r["views"] or 0) for r in prev_rows),
    }
    # Resume support: skip DOIs already refreshed today (host may kill
    # long-running trees ~10 min; the next run continues where it stopped).
    today = time.strftime("%Y%m%d")
    fresh = {r["doi"] for r in d1(token, account, au_uuid,
        "SELECT doi FROM zenodo_stats WHERE fetched_at LIKE ? || '%'",
        (today,))}
    todo = sorted(set(by_doi) - fresh)
    skipped = len(by_doi) - len(todo)
    print(f"fresh today: {skipped} | to fetch: {len(todo)}", flush=True)

    results, errors = [], 0
    for i, doi in enumerate(todo, 1):
        rec = fetch_record(doi)
        if rec.get("error"):
            errors += 1
            if errors <= 5:
                print(f"  ERR {doi}: {rec['error']}", flush=True)
        else:
            rec["slug"] = by_doi[doi].get("slug")
            if not dry:
                # Incremental upsert: a mid-run kill leaves today's rows written,
                # so the next run resumes from where it stopped.
                d1(token, account, au_uuid, UPSERT, (
                    rec["doi"], rec.get("conceptdoi"), rec.get("title"), rec.get("slug"),
                    str(rec["downloads"]), str(rec["unique_downloads"]), str(rec["views"]),
                    str(rec["unique_views"]), str(rec["version_downloads"]),
                    str(prev_map.get(rec["doi"], {}).get("downloads") or 0),
                    str(prev_map.get(rec["doi"], {}).get("views") or 0),
                    time.strftime("%Y%m%d-%H%M%S")))
        results.append(rec)
        if i % 50 == 0:
            print(f"  fetched {i}/{len(todo)} (errors {errors})", flush=True)
        time.sleep(DELAY)

    ok = [r for r in results if "error" not in r]

    # Totals from the table AFTER upsert so partial/resumed runs still report
    # the true snapshot sums.
    tot_rows = d1(token, account, au_uuid,
                  "SELECT SUM(downloads) dl, SUM(views) vw, COUNT(*) n FROM zenodo_stats")
    new_tot = {"dl": int(tot_rows[0]["dl"] or 0), "vw": int(tot_rows[0]["vw"] or 0)}
    movers = sorted(ok, key=lambda r: -(
        r["downloads"] - int(prev_map.get(r["doi"], {}).get("downloads") or 0)))[:10]

    lines = [
        f"zenodo_stats delta {time.strftime('%Y-%m-%d %H:%M')} "
        f"({'DRY-RUN ' if dry else ''}{len(ok)} fetched, {len(by_doi)} DOIs, errors {errors})",
        f"downloads: {prev_tot['dl']} -> {new_tot['dl']} "
        f"(+{new_tot['dl'] - prev_tot['dl']})",
        f"views:     {prev_tot['vw']} -> {new_tot['vw']} "
        f"(+{new_tot['vw'] - prev_tot['vw']})",
        "top movers (downloads):",
    ]
    for k, r in enumerate(movers, 1):
        g = r["downloads"] - int(prev_map.get(r["doi"], {}).get("downloads") or 0)
        lines.append(f"  {k}. +{g}  {r['title'][:50]}  {r['doi']}")
    report = "\n".join(lines)
    print(report)
    if not dry:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(report.replace("\n", " | ") + "\n")
    return 0 if (errors == 0 and ok) or (len(todo) == 0) else (
        1 if errors > max(len(ok), 1) // 2 else 0)


if __name__ == "__main__":
    sys.exit(main())
