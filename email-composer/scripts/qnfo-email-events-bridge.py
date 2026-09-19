#!/usr/bin/env python3
"""qnfo-email-events-bridge.py

Bridge QNFO email-sourced calendar events into the LOCAL Outlook calendar AND
To-Do list by calling calendar-sync.py (Outlook COM). Closes the cloud -> Outlook
gap for EMAIL-EVENT-CALENDAR-LIVE-1 (qnfo-calendar-intake).

Reads qnfo-audit `calendar` rows WHERE plane='personal' AND source='email'
AND status!='cancelled' AND dtstart in the future via the Cloudflare D1 query
API, then, per event:
  - calendar-sync.py add       (idempotent: same title+start skipped)
  - calendar-sync.py add-task  (only for action-titled events: deadline/submit/
                                apply/register/renew/confirm/book/pay/reply/...)

Runs LOCALLY (Outlook COM). Scheduled by the Windows task QNFO_Email_Events_Bridge
(via .deepchat/secrets/run-email-events-bridge.cmd). Env: CLOUDFLARE_API_TOKEN
(D1 read), CAL_ACCOUNT (personal account), QNFO_ACCOUNT_ID (optional).
"""
import os, sys, json, re, subprocess, urllib.request
from datetime import datetime

ACCT = os.environ.get("QNFO_ACCOUNT_ID", "edb167b78c9fb901ea5bca3ce58ccc4b")
D1 = "35e2e573-92f3-46ac-83c6-22f6429fc5e5"
SYNC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calendar-sync.py")

ACTION = re.compile(
    r"deadline|submit|apply|register|renew|confirm|book|pay|reply|prepare|sign|"
    r"rebalance|approve|publish|print|notification", re.I)

def d1(sql):
    tok = os.environ["CLOUDFLARE_API_TOKEN"]
    url = "https://api.cloudflare.com/client/v4/accounts/%s/d1/database/%s/query" % (ACCT, D1)
    req = urllib.request.Request(url, data=json.dumps({"sql": sql}).encode(),
        headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"}, method="POST")
    j = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
    return (j.get("result") or [{}])[0].get("results") or []

def local(iso):
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone()
    return dt.strftime("%Y-%m-%d %H:%M"), dt.strftime("%Y-%m-%d")

def sync(args):
    p = subprocess.run([sys.executable, SYNC] + args, capture_output=True, text=True)
    tail = ((p.stdout or "") + (p.stderr or "")).strip().splitlines()
    return p.returncode, (tail[-1] if tail else "")

def main():
    sql = ("SELECT title,dtstart,dtend,location FROM calendar WHERE plane='personal' "
           "AND source='email' AND status!='cancelled' "
           "AND dtstart > strftime('%Y-%m-%dT%H:%M:%SZ','now') ORDER BY dtstart LIMIT 50")
    rows = d1(sql)
    print("email-sourced future events: %d" % len(rows))
    ev_ok = task_ok = 0
    for r in rows:
        title = (r.get("title") or "").strip()
        if not title or not r.get("dtstart"):
            continue
        start, day = local(r["dtstart"])
        a = ["add", "--title", title, "--start", start]
        if r.get("dtend"):
            a += ["--end", local(r["dtend"])[0]]
        if r.get("location"):
            a += ["--loc", r["location"]]
        rc, msg = sync(a)
        print("  [cal]  %-40s -> %s" % (title[:40], msg))
        if rc == 0:
            ev_ok += 1
        if ACTION.search(title):
            rc2, msg2 = sync(["add-task", "--title", title, "--due", day,
                              "--note", "email event (qnfo-calendar-intake)"])
            print("  [task] %-40s -> %s" % (title[:40], msg2))
            if rc2 == 0:
                task_ok += 1
    print("done: events %d/%d, tasks %d" % (ev_ok, len(rows), task_ok))

if __name__ == "__main__":
    main()
