#!/usr/bin/env python3
"""Analyze agent.db: table sizes, session age distribution, tape entry sizes.
Read-only, no changes."""
import sqlite3, os, sys
from datetime import datetime, timezone

DB = os.path.expandvars(r'%APPDATA%\DeepChat\app_db\agent.db')

def fmt_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} TB"

conn = sqlite3.connect(DB)
c = conn.cursor()

print("=" * 70)
print("AGENT.DB ANALYSIS")
print("=" * 70)
print(f"File: {DB}")
print(f"Size: {fmt_size(os.path.getsize(DB))}")
print()

# 1. All tables with row counts
print("--- TABLE ROW COUNTS ---")
c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in c.fetchall()]
for tbl in tables:
    try:
        c.execute(f"SELECT COUNT(*) FROM [{tbl}]")
        count = c.fetchone()[0]
        print(f"  {tbl:50s} {count:>10,} rows")
    except Exception as e:
        print(f"  {tbl:50s} (error: {e})")

print()

# 2. Session age distribution
print("--- SESSION AGE DISTRIBUTION ---")
now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
cutoffs = [
    (3, "0-3 days"),
    (7, "4-7 days"),
    (14, "8-14 days"),
    (30, "15-30 days"),
    (60, "31-60 days"),
    (90, "61-90 days"),
    (180, "91-180 days"),
    (365, "181-365 days"),
]

prev_cutoff_ms = now_ms
for days, label in cutoffs:
    cutoff_ms = now_ms - (days * 86400 * 1000)
    c.execute(
        "SELECT COUNT(*), COUNT(CASE WHEN is_pinned=1 THEN 1 END) "
        "FROM new_sessions WHERE updated_at < ? AND updated_at >= ?",
        (prev_cutoff_ms, cutoff_ms)
    )
    count, pinned = c.fetchone()
    prev_cutoff_ms = cutoff_ms
    if count > 0:
        print(f"  {label:20s} {count:>5,} sessions  ({pinned} pinned)")

# Older than 365 days
c.execute(
    "SELECT COUNT(*), COUNT(CASE WHEN is_pinned=1 THEN 1 END) "
    "FROM new_sessions WHERE updated_at < ?", (prev_cutoff_ms,)
)
count, pinned = c.fetchone()
if count > 0:
    print(f"  {'365+ days':20s} {count:>5,} sessions  ({pinned} pinned)")

# Total
c.execute("SELECT COUNT(*), COUNT(CASE WHEN is_pinned=1 THEN 1 END) FROM new_sessions")
total, total_pinned = c.fetchone()
print(f"  {'TOTAL':20s} {total:>5,} sessions  ({total_pinned} pinned)")
print()

# 3. Tape entries by session age
print("--- TAPE ENTRIES BREAKDOWN ---")
c.execute("SELECT COUNT(*) FROM deepchat_tape_entries")
total_tape = c.fetchone()[0]
print(f"  Total tape entries: {total_tape:,}")

# Tape entries by session age bracket
prev_cutoff_ms = now_ms
for days, label in [(3, "0-3d"), (7, "4-7d"), (14, "8-14d"), (30, "15-30d"), (60, "31-60d"), (90, "61-90d"), (365, "91-365d")]:
    cutoff_ms = now_ms - (days * 86400 * 1000)
    c.execute(
        "SELECT COUNT(*) FROM deepchat_tape_entries "
        "WHERE session_id IN (SELECT id FROM new_sessions WHERE updated_at < ? AND updated_at >= ?)",
        (prev_cutoff_ms, cutoff_ms)
    )
    count = c.fetchone()[0]
    if count > 0:
        print(f"  {label:10s} {count:>10,} entries")
    prev_cutoff_ms = cutoff_ms

# Older than 365
c.execute(
    "SELECT COUNT(*) FROM deepchat_tape_entries "
    "WHERE session_id IN (SELECT id FROM new_sessions WHERE updated_at < ?)", (prev_cutoff_ms,)
)
count = c.fetchone()[0]
if count > 0:
    print(f"  {'365+d':10s} {count:>10,} entries")

print()

# 4. Largest sessions by tape count
print("--- TOP 10 SESSIONS BY TAPE ENTRIES ---")
c.execute("""
    SELECT ns.id, ns.title, 
           datetime(ns.updated_at/1000, 'unixepoch') as last_updated,
           ns.is_pinned,
           COUNT(te.id) as tape_count
    FROM new_sessions ns
    LEFT JOIN deepchat_tape_entries te ON te.session_id = ns.id
    GROUP BY ns.id
    ORDER BY tape_count DESC
    LIMIT 10
""")
for row in c.fetchall():
    sid, title, updated, pinned, count = row
    title_short = (title or '(no title)')[:50]
    pin = ' [PINNED]' if pinned else ''
    print(f"  {tape_count:>7,} entries | {updated} | {title_short}{pin}")

print()

# 5. Recent sessions (last 7 days)
print("--- SESSIONS IN LAST 7 DAYS ---")
cutoff_7d = now_ms - (7 * 86400 * 1000)
c.execute(
    "SELECT id, title, datetime(updated_at/1000, 'unixepoch'), is_pinned "
    "FROM new_sessions WHERE updated_at >= ? ORDER BY updated_at DESC",
    (cutoff_7d,)
)
for row in c.fetchall():
    sid, title, updated, pinned = row
    title_short = (title or '(no title)')[:60]
    pin = ' [PINNED]' if pinned else ''
    print(f"  {updated} | {title_short}{pin}")

conn.close()
