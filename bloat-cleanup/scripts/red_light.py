#!/usr/bin/env python3
"""Ultra-light red-team checks."""
import sqlite3, os, time

DB = os.path.expandvars(r'%APPDATA%\DeepChat\app_db\agent.db')
c = sqlite3.connect(DB).cursor()
now_ms = int(time.time() * 1000)
cut7 = now_ms - 7 * 86400000

checks = {
    "integrity": "PRAGMA integrity_check",
    "quick_check": "PRAGMA quick_check",
    "FK violations": "PRAGMA foreign_key_check",
    "sessions": "SELECT COUNT(*) FROM new_sessions",
    "pinned": "SELECT COUNT(*) FROM new_sessions WHERE is_pinned=1",
    f"stale (>7d)": f"SELECT COUNT(*) FROM new_sessions WHERE is_pinned=0 AND updated_at<={cut7}",
    "tape_entries": "SELECT COUNT(*) FROM deepchat_tape_entries",
    "messages": "SELECT COUNT(*) FROM deepchat_messages",
    "asst_blocks": "SELECT COUNT(*) FROM deepchat_assistant_blocks",
    "user_msgs": "SELECT COUNT(*) FROM deepchat_user_messages",
}

for label, sql in checks.items():
    if sql.startswith("PRAGMA"):
        rows = c.execute(sql).fetchall()
        if label == "FK violations":
            print(f"{label}: {len(rows)}")
        else:
            print(f"{label}: {rows[0][0]}")
    else:
        print(f"{label}: {c.execute(sql).fetchone()[0]:,}")

# Sample 5 tape entries
print("\n--- SPOT CHECK: 5 tape entries ---")
for row in c.execute("SELECT session_id FROM deepchat_tape_entries LIMIT 5"):
    sid = row[0]
    c2 = sqlite3.connect(DB).cursor()
    ok = c2.execute("SELECT COUNT(*) FROM new_sessions WHERE id=?", (sid,)).fetchone()[0]
    print(f"  {sid[:20]} -> {'OK' if ok else 'NO SESSION [FAIL]'}")

print(f"\nDB size: {os.path.getsize(DB)/1024**3:.2f} GB")

import shutil
_, _, f = shutil.disk_usage('C:\\')
print(f"C: free: {f/1024**3:.1f} GB")
