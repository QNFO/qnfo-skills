#!/usr/bin/env python3
"""
calendar-sync.py — Outlook calendar + tasks sync for the GTD register
(CALENDAR-SYNC-1 + CALENDAR-TASKS-1, USER MANDATE 2026-08-20: anything with a
date lives on the Outlook calendar and/or as an Outlook to-do, maintained
automatically, WITHOUT user intervention, forever).

Tool (the ONLY supported mechanism for calendar/task creation):
  list                                 read calendar state (next 30 days)
  tasks                                read to-do state (open tasks)
  add      --title T --start "YYYY-MM-DD HH:MM" [--end E] [--loc L]
           [--reminder MIN] [--body B] create calendar event (idempotent)
  add-task --title T --due YYYY-MM-DD [--note N]  create to-do (idempotent)
  sync-register                        GTD register dated lines -> calendar events
  sync-tasks                           GTD register action lines -> to-dos;
                                       complete to-dos whose register line
                                       became [x] or was removed (date-prefixed
                                       register-derived titles ONLY — never
                                       agent-maintained tasks)
  complete --title T                   complete a to-do by title (substring)

GTD register source of truth: D:\\Obsidian\\notes\\v1\\_personal-gtd.md, NEXT STEPS
section, dated line format:  - [ ] YYYY-MM-DD[ HH:MM][ to DD|YYYY-MM-DD] — subject
(also accepts a leading "By "). [x] lines are skipped; sync-tasks completes the
matching to-do. Reminder defaults: single-day events fire 09:00 the DAY
BEFORE (planning — user checks the calendar primarily in the morning,
mandate 2026-08-25); multi-day ranges keep 10080 min week-before. One native
reminder per event; prep-heavy meetings add cronjob prep layers on top.

HARD CONSTRAINTS (mirrors outlook-gtd-triage.py):
  - COM ONLY, INVISIBLE: never opens the Outlook UI.
  - Outlook is quit ONLY if this script started it (GetObject fallback).
  - Idempotent: same title+start event / same title task = skipped; title
    similarity is token-based (parenthetical variants do not duplicate).
  - Never fabricates dates/titles/reminders; report only on changes.
  - Per-account fault isolation (CAL_ACCOUNT env override; defaults to
    rowan.quni@outlook.com; falls back to any store containing the address
    or any calendar store). Personal events use CAL_ACCOUNT=rwnquni@outlook.com.
  - Completion safety: auto-complete ONLY tasks whose Subject starts with a
    date prefix (YYYY-MM-DD) and whose register line is [x] or absent; tasks
    without a date prefix are agent-maintained and NEVER auto-completed.
"""
import argparse
import datetime as dt
import os
import re
import sys

import win32com.client

REGISTER = r"D:\Obsidian\notes\v1\_personal-gtd.md"
# Default account is the QNFO-facing calendar; PERSONAL events must go to
# the personal account via: CAL_ACCOUNT=rwnquni@outlook.com (user mandate 2026-08-25).
CAL_ACCOUNT = os.environ.get("CAL_ACCOUNT", "rowan.quni@outlook.com")

OL_FOLDER_CALENDAR = 9    # olFolderCalendar
OL_FOLDER_TASKS = 13      # olFolderTasks
OL_FOLDER_INBOX = 6       # olFolderInbox (reference)

ACTION_KEYWORDS = (
    "decision", "registration", "abstract", "pitch", "venue", "rebalance",
    "apply", "submit", "register", "print", "deadline", "approve", "confirm",
    "notification",
)

RX_DATE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
RX_TIME = re.compile(r"^(\d{1,2}:\d{2})")
RX_RANGE = re.compile(r"^to\s+(\d{4}-\d{2}-\d{2}|\d{1,2})", re.I)
RX_LIST = re.compile(r"^-\s*\[([ xX])\]\s*(.*)$")
RX_TASK_DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}")


def _morning_reminder(start):
    """Reminder fires 09:00 the day BEFORE the event (user mandate 2026-08-25:
    user checks the calendar primarily in the morning; reminders must be
    sufficiently in advance to allow planning)."""
    base = (start - dt.timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    return int((start - base).total_seconds() // 60)


def get_outlook():
    """Attach to running Outlook or start hidden; return (app, was_started)."""
    try:
        app = win32com.client.GetObject(Class="Outlook.Application")
        return app, False
    except Exception:
        app = win32com.client.Dispatch("Outlook.Application")
        return app, True


def get_store_root(ns, email):
    """ns.Folders yields store-ROOT MAPIFolders (OUTLOOK-COM-STORE-PATTERN-1);
    match root.Name or root.Store.SmtpAddress; fall back to the first store
    whose SmtpAddress contains '@' (single-account hosts)."""
    fallback = None
    for root in ns.Folders:
        name = (root.Name or "").lower()
        try:
            smtp = (root.Store.SmtpAddress or "").lower()
        except Exception:
            smtp = ""
        if email.lower() in name or email.lower() in smtp:
            return root
        if fallback is None and smtp and "@" in smtp:
            fallback = root
    return fallback


def get_folder(ns, email, folder_const):
    """Resolve a default folder (calendar/tasks) for the target account."""
    root = get_store_root(ns, email)
    if root is None:
        return None
    try:
        return root.Store.GetDefaultFolder(folder_const)
    except Exception:
        try:
            return ns.GetDefaultFolder(folder_const)
        except Exception:
            return None


def _norm_dt(v):
    try:
        if hasattr(v, "tzinfo") and v.tzinfo is not None:
            return v.astimezone().replace(tzinfo=None)
    except Exception:
        pass
    return v


def _subj(item):
    try:
        return (item.Subject or "").strip()
    except Exception:
        return ""


def _tokens(title):
    """Significant title tokens (alnum runs >= 3 chars, lowercased)."""
    return {t.lower() for t in re.findall(r"[A-Za-z0-9]{3,}", title or "")}


def _similar(a, b):
    """Token-overlap similarity: >=2 shared significant tokens = same item."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return False
    inter = ta & tb
    if len(inter) >= 2:
        return True
    # fallback: one title contains the other (normalized, parentheticals stripped)
    na = re.sub(r"\s*\(.*?\)\s*", " ", (a or "").lower())
    nb = re.sub(r"\s*\(.*?\)\s*", " ", (b or "").lower())
    return (na and nb and (na in nb or nb in na)) and min(len(na), len(nb)) >= 8


def _norm_title(t):
    """Normalized title: parentheticals stripped, lowercased, whitespace-collapsed."""
    return re.sub(r"\s+", " ", re.sub(r"\s*\(.*?\)\s*", " ", (t or "").lower())).strip()


def _title_exists(folder, title, start=None, strict=False):
    """Idempotency check: similar Subject (and same Start when given).

    strict=True (tasks): normalized-title equality/containment only — no token
    overlap, which false-matches distinct titles sharing date/location tokens.
    """
    try:
        for it in list(folder.Items):
            s = _subj(it)
            if not s:
                continue
            if strict:
                na, nb = _norm_title(s), _norm_title(title)
                if na and nb and min(len(na), len(nb)) >= 8 and (na == nb or na in nb or nb in na):
                    return True
                continue
            if _similar(s, title):
                if start is None:
                    return True
                try:
                    st = _norm_dt(it.Start)
                    if st and abs((st - start).total_seconds()) < 3600:
                        return True
                except Exception:
                    return True
    except Exception:
        pass
    return False


def cmd_add(app, ns, args):
    folder = get_folder(ns, CAL_ACCOUNT, OL_FOLDER_CALENDAR)
    if folder is None:
        print("ERROR: calendar folder not found")
        return 2
    try:
        start = dt.datetime.strptime(args.start, "%Y-%m-%d %H:%M")
    except ValueError:
        print("ERROR: --start must be 'YYYY-MM-DD HH:MM'")
        return 2
    end = dt.datetime.strptime(args.end, "%Y-%m-%d %H:%M") if args.end else start + dt.timedelta(hours=1)
    reminder = int(args.reminder) if args.reminder else 1440
    if _title_exists(folder, args.title, start):
        print(f"skip (exists): {args.title} @ {start:%Y-%m-%d %H:%M}")
        return 0
    ev = folder.Items.Add(1)  # olAppointmentItem
    ev.Subject = args.title
    ev.Start = start
    ev.End = end
    if args.loc:
        ev.Location = args.loc
    if args.body:
        ev.Body = args.body
    try:
        ev.ReminderSet = True
        ev.ReminderMinutesBeforeStart = reminder
    except Exception:
        pass
    ev.Save()
    print(f"created: {args.title} @ {start:%Y-%m-%d %H:%M} (reminder {reminder} min)")
    return 0


def cmd_add_task(app, ns, args):
    folder = get_folder(ns, CAL_ACCOUNT, OL_FOLDER_TASKS)
    if folder is None:
        print("ERROR: tasks folder not found")
        return 2
    try:
        due = dt.datetime.strptime(args.due, "%Y-%m-%d")
    except ValueError:
        print("ERROR: --due must be YYYY-MM-DD")
        return 2
    if _title_exists(folder, args.title, strict=True):
        print(f"skip (exists): {args.title}")
        return 0
    t = folder.Items.Add(3)  # olTaskItem
    t.Subject = args.title
    t.DueDate = due
    t.StartDate = due - dt.timedelta(days=1)
    if args.note:
        t.Body = args.note
    t.ReminderSet = True
    t.ReminderTime = due.replace(hour=9, minute=0)
    t.Save()
    print(f"created task: {args.title} (due {args.due})")
    return 0


def parse_register():
    """Return (open_events, open_tasks, done_subjects) from NEXT STEPS.

    open_events:  dated OPEN lines -> calendar events (title/start/end/reminder/body)
    open_tasks:   dated OPEN lines with an ACTION keyword -> to-dos
    done_subjects: normalized subjects of [x] lines (for completion matching)
    """
    if not os.path.exists(REGISTER):
        print(f"ERROR: register not found: {REGISTER}")
        return None, None, None
    in_next = False
    open_events = []
    open_tasks = []
    done_subjects = []
    now = dt.datetime.now()
    with open(REGISTER, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            ls = line.strip()
            if ls.startswith("## NEXT STEPS"):
                in_next = True
                continue
            if in_next and ls.startswith("## "):
                break
            if not in_next:
                continue
            m = RX_LIST.match(ls)
            if not m:
                continue
            done, rest = m.group(1), m.group(2).strip()
            if done.lower() == "x":
                # normalize the subject for completion matching
                dm = RX_DATE.match(rest)
                if dm:
                    subj = rest[dm.end():]
                    subj = re.sub(r"^[—–\-:]\s*", "", subj).strip()
                    if subj:
                        done_subjects.append(subj.lower())
                continue
            rest = re.sub(r"^By\s+", "", rest, flags=re.I).strip()
            dm = RX_DATE.match(rest)
            if not dm:
                continue  # undated / month-only lines are skipped
            d1 = dm.group(1)
            rest = rest[dm.end():].strip()
            try:
                day = dt.datetime.strptime(d1, "%Y-%m-%d")
            except ValueError:
                continue
            hm = None
            tm = RX_TIME.match(rest)
            if tm:
                hm = tm.group(1)
                rest = rest[tm.end():].strip()
            d2 = None
            rm = RX_RANGE.match(rest)
            if rm:
                end_s = rm.group(1)
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", end_s):
                    d2 = end_s
                else:
                    d2 = f"{d1[:8]}{int(end_s):02d}"
                rest = rest[rm.end():].strip()
            rest = re.sub(r"^[—–\-:]\s*", "", rest).strip()
            subject = rest[:120]
            if not subject:
                continue
            if hm:
                try:
                    start = dt.datetime.strptime(f"{d1} {hm}", "%Y-%m-%d %H:%M")
                except ValueError:
                    start = day
            else:
                start = day.replace(hour=9, minute=0)
            if d2:
                try:
                    end = dt.datetime.strptime(d2, "%Y-%m-%d").replace(hour=18, minute=0)
                except ValueError:
                    end = start + dt.timedelta(hours=1)
                reminder = 10080 if (end - start).days >= 4 else _morning_reminder(start)
            else:
                end = start + dt.timedelta(hours=1)
                reminder = _morning_reminder(start)
            # past lines (yesterday or older) are stale
            if start < now - dt.timedelta(days=1):
                continue
            open_events.append({"title": subject, "start": start, "end": end,
                                "reminder": reminder, "body": ls[:400]})
            if any(k in subject.lower() for k in ACTION_KEYWORDS):
                open_tasks.append({"title": subject, "due": d1, "note": ls[:400]})
    return open_events, open_tasks, done_subjects


def cmd_sync_register(app, ns, args):
    folder = get_folder(ns, CAL_ACCOUNT, OL_FOLDER_CALENDAR)
    if folder is None:
        print("ERROR: calendar folder not found")
        return 2
    open_events, _, _ = parse_register()
    if open_events is None:
        return 2
    created = 0
    skipped = 0
    for ev in open_events:
        if ev["start"] < dt.datetime.now():
            skipped += 1
            continue
        if _title_exists(folder, ev["title"]):
            skipped += 1
            continue
        item = folder.Items.Add(1)
        item.Subject = ev["title"]
        item.Start = ev["start"]
        item.End = ev["end"]
        item.Body = ev["body"]
        try:
            item.ReminderSet = True
            item.ReminderMinutesBeforeStart = ev["reminder"]
        except Exception:
            pass
        item.Save()
        created += 1
        print(f"created: {ev['title']} @ {ev['start']:%Y-%m-%d %H:%M} (reminder {ev['reminder']} min)")
    print(f"sync-register: created={created} skipped={skipped}")
    return 0


def cmd_sync_tasks(app, ns, args):
    folder = get_folder(ns, CAL_ACCOUNT, OL_FOLDER_TASKS)
    if folder is None:
        print("ERROR: tasks folder not found")
        return 2
    _, open_tasks, done_subjects = parse_register()
    if open_tasks is None:
        return 2
    created = 0
    completed = 0
    # 1. Create tasks for OPEN action lines not yet present.
    #    Subject is DATE-PREFIXED ("YYYY-MM-DD — <title>") so the completion
    #    gate below can distinguish register-derived tasks from
    #    agent-maintained ones (H-CAL-1 fix 2026-08-21).
    for t in open_tasks:
        if _title_exists(folder, t["title"]):
            continue
        due = dt.datetime.strptime(t["due"], "%Y-%m-%d")
        if due < dt.datetime.now() - dt.timedelta(days=30):
            continue
        item = folder.Items.Add(3)
        item.Subject = f"{t['due']} — {t['title']}"
        item.DueDate = due
        item.StartDate = due - dt.timedelta(days=1)
        item.Body = t["note"]
        item.ReminderSet = True
        item.ReminderTime = due.replace(hour=9, minute=0)
        item.Save()
        created += 1
        print(f"created task: {t['title']} (due {t['due']})")
    # 2. Complete register-derived tasks whose line became [x] or vanished.
    #    SAFETY (H-CAL-1 fix 2026-08-21, remediation reviewer): auto-complete
    #    ONLY tasks whose Subject starts with a DATE PREFIX (YYYY-MM-DD — the
    #    register-derived signature) AND token-overlaps (>=3) a DONE register
    #    subject AND does NOT overlap (>=2) any OPEN line. Tasks without a
    #    date prefix are agent-maintained and are NEVER auto-completed —
    #    complete them explicitly via `complete --title`.
    try:
        for it in list(folder.Items):
            s = _subj(it)
            if not s or not RX_TASK_DATE_PREFIX.match(s):
                continue
            try:
                if it.Complete:
                    continue
            except Exception:
                continue
            tokens = _tokens(s)
            is_open = any(len(tokens & _tokens(ev["title"])) >= 2 for ev in open_events)
            done_match = any(len(tokens & _tokens(ds)) >= 3 for ds in done_subjects)
            if done_match and not is_open:
                it.Complete = True
                it.Save()
                completed += 1
                print(f"completed task: {s}")
    except Exception:
        pass
    print(f"sync-tasks: created={created} completed={completed}")
    return 0


def cmd_list(app, ns, args):
    folder = get_folder(ns, CAL_ACCOUNT, OL_FOLDER_CALENDAR)
    if folder is None:
        print("ERROR: calendar folder not found")
        return 2
    now = dt.datetime.now()
    end = now + dt.timedelta(days=30)
    n = 0
    try:
        for it in list(folder.Items):
            try:
                st = _norm_dt(it.Start)
                if st and now <= st <= end:
                    n += 1
                    print(f"{st:%Y-%m-%d %H:%M}  {_subj(it)[:80]}")
            except Exception:
                continue
    except Exception:
        pass
    print(f"calendar: {n} upcoming event(s) in 30 days")
    return 0


def cmd_tasks(app, ns, args):
    folder = get_folder(ns, CAL_ACCOUNT, OL_FOLDER_TASKS)
    if folder is None:
        print("ERROR: tasks folder not found")
        return 2
    n = 0
    try:
        for it in list(folder.Items):
            try:
                if not it.Complete:
                    n += 1
                    due = _norm_dt(it.DueDate)
                    d = due.strftime("%Y-%m-%d") if due else "?"
                    print(f"{d}  {_subj(it)[:80]}")
            except Exception:
                continue
    except Exception:
        pass
    print(f"tasks: {n} open")
    return 0


def cmd_complete(app, ns, args):
    folder = get_folder(ns, CAL_ACCOUNT, OL_FOLDER_TASKS)
    if folder is None:
        print("ERROR: tasks folder not found")
        return 2
    done = 0
    try:
        for it in list(folder.Items):
            try:
                if not it.Complete and args.title.lower() in _subj(it).lower():
                    it.Complete = True
                    it.Save()
                    done += 1
                    print(f"completed task: {_subj(it)}")
            except Exception:
                continue
    except Exception:
        pass
    print(f"complete: {done} task(s)")
    return 0


def main():
    p = argparse.ArgumentParser(prog="calendar-sync.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("tasks")
    pa = sub.add_parser("add")
    pa.add_argument("--title", required=True)
    pa.add_argument("--start", required=True)
    pa.add_argument("--end", default=None)
    pa.add_argument("--loc", default=None)
    pa.add_argument("--reminder", default=None)
    pa.add_argument("--body", default=None)
    pt = sub.add_parser("add-task")
    pt.add_argument("--title", required=True)
    pt.add_argument("--due", required=True)
    pt.add_argument("--note", default=None)
    sub.add_parser("sync-register")
    sub.add_parser("sync-tasks")
    pc = sub.add_parser("complete")
    pc.add_argument("--title", required=True)
    args = p.parse_args()

    app, was_started = get_outlook()
    try:
        ns = app.GetNamespace("MAPI")
        if args.cmd == "add":
            return cmd_add(app, ns, args)
        if args.cmd == "add-task":
            return cmd_add_task(app, ns, args)
        if args.cmd == "sync-register":
            return cmd_sync_register(app, ns, args)
        if args.cmd == "sync-tasks":
            return cmd_sync_tasks(app, ns, args)
        if args.cmd == "list":
            return cmd_list(app, ns, args)
        if args.cmd == "tasks":
            return cmd_tasks(app, ns, args)
        if args.cmd == "complete":
            return cmd_complete(app, ns, args)
        return 0
    finally:
        if was_started:
            try:
                app.Quit()
            except Exception:
                pass


if __name__ == "__main__":
    sys.exit(main())
