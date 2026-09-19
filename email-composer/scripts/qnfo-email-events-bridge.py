#!/usr/bin/env python3
"""qnfo-email-events-bridge.py

Bridge QNFO email-sourced calendar events into the LOCAL Outlook calendar by
calling calendar-sync.py (Outlook COM). Closes the cloud -> Outlook gap for the
EMAIL-EVENT-CALENDAR-LIVE-1 pipeline (qnfo-calendar-intake).

Reads qnfo-audit `calendar` rows WHERE plane='personal' AND source='email'
AND status!='cancelled' AND dtstart in the future, via the Cloudflare D1 query
API, then calls `calendar-sync.py add` per event (idempotent: same title+start
is skipped by calendar-sync.py).

Runs LOCALLY (Outlook COM). Recommended: run alongside the existing GTD sync.
Env: CLOUDFLARE_API_TOKEN (D1 read), QNFO_ACCOUNT_ID (optional), CAL_ACCOUNT.
"""
import os, sys, json, subprocess, urllib.request
from datetime import datetime, timezone

ACCT = os.environ.get("QNFO_ACCOUNT_ID", "edb167b78c9fb901ea5bca3ce58ccc4b")
D1 = "35e2e573-92f3-46ac-83c6-22f6429fc5e5"
SYNC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calendar-sync.py")

def d1(sql):
    tok = os.environ["CLOUDFLARE_API_TOKEN"]
    url = "https://api.cloudflare.com/client/v4/accounts/%s/d1/database/%s/query" % (ACCT, D1)
    req = urllib.request.Request(url, data=json.dumps({"sql": sql}).encode(),
        headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"}, method="POST")
    j = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
    return (j.get("result") or [{}])[0].get("results") or []

def local_dt(iso):
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone()
    return dt.strftime("%Y-%m-%d %H:%M")

def main():
    sql = ("SELECT title,dtstart,dtend,location FROM calendar WHERE plane='personal' "
           "AND source='email' AND status!='cancelled' "
           "AND dtstart > strftime('%Y-%m-%dT%H:%M:%SZ','now') ORDER BY dtstart LIMIT 50")
    rows = d1(sql)
    print("email-sourced future events: %d" % len(rows))
    ok = 0
    for r in rows:
        title = (r.get("title") or "").strip()
        if not title or not r.get("dtstart"):
            continue
        args = [sys.executable, SYNC, "add", "--title", title, "--start", local_dt(r["dtstart"])]
        if r.get("dtend"):
            args += ["--end", local_dt(r["dtend"])]
        if r.get("location"):
            args += ["--loc", r["location"]]
        p = subprocess.run(args, capture_output=True, text=True)
        tail = ((p.stdout or "") + (p.stderr or "")).strip().splitlines()
        print("  %-42s -> %s" % (title[:42], tail[-1] if tail else "(no output)"))
        if p.returncode == 0:
            ok += 1
    print("done: %d/%d" % (ok, len(rows)))

if __name__ == "__main__":
    main()
