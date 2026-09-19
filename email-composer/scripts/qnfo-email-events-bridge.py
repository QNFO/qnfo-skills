#!/usr/bin/env python3
"""qnfo-email-events-bridge.py

Bridge QNFO email-sourced calendar events into the LOCAL Outlook calendar AND
To-Do list (via calendar-sync.py / Outlook COM), and PRUNE Outlook events whose
QNFO calendar row was CANCELLED. Closes the cloud -> Outlook gap for
EMAIL-EVENT-CALENDAR-LIVE-1 (qnfo-calendar-intake).

- calendar-sync.py add       (idempotent)      for future, non-cancelled events
- calendar-sync.py add-task  (action titles)   deadline/submit/apply/register/...
- prune: delete the matching Outlook appointment for rows with status='cancelled'
  (exact subject + exact start time; resolved via calendar-sync's own
   get_outlook/get_store_root/get_folder so only CAL_ACCOUNT is touched).

Runs LOCALLY (Outlook COM); scheduled by Windows task QNFO_Email_Events_Bridge.
Env: CLOUDFLARE_API_TOKEN (D1 read), CAL_ACCOUNT, QNFO_ACCOUNT_ID (optional).
"""
import os, sys, json, re, subprocess, urllib.request, importlib.util
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

def _cal_sync():
    spec = importlib.util.spec_from_file_location("cal_sync", SYNC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def prune_cancelled():
    rows = d1("SELECT title,dtstart FROM calendar WHERE plane='personal' "
              "AND source='email' AND status='cancelled'")
    if not rows:
        return 0
    cs = _cal_sync()
    try:
        app, _started = cs.get_outlook()
        ns = app.GetNamespace("MAPI")
        folder = cs.get_folder(ns, cs.CAL_ACCOUNT, cs.OL_FOLDER_CALENDAR)
    except Exception as e:
        print("  [prune] Outlook unavailable: %s" % str(e)[:120])
        return 0
    n = 0
    for r in rows:
        title = (r.get("title") or "").strip()
        if not title or not r.get("dtstart"):
            continue
        want_day = local(r["dtstart"])[1]
        try:
            for it in list(folder.Items.Restrict("[Subject]='" + title.replace("'", "''") + "'")):
                try:
                    if it.Start.strftime("%Y-%m-%d") == want_day:
                        it.Delete()
                        n += 1
                        print("  [prune] deleted cancelled: %s @ %s" % (title[:40], want))
                except Exception:
                    pass
        except Exception:
            pass
    return n

def main():
    pruned = prune_cancelled()
    print("cancelled pruned: %d" % pruned)
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
    print("done: pruned %d, events %d/%d, tasks %d" % (pruned, ev_ok, len(rows), task_ok))

if __name__ == "__main__":
    main()
