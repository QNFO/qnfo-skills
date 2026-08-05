#!/usr/bin/env python3
"""Final red-team audit: comprehensive post-kaizen DB verification."""
import sqlite3, os, time

DB = os.path.expandvars(r'%APPDATA%\DeepChat\app_db\agent.db')
c = sqlite3.connect('file:' + DB + '?mode=ro', uri=True).cursor()
now_ms = int(time.time() * 1000)
cut7 = now_ms - 7 * 86400000

print('=' * 60)
print('FINAL RED-TEAM AUDIT — POST KAIZEN v2.5')
print('=' * 60)

results = []

# 1. Counts
checks = [
    ('sessions', f"SELECT COUNT(*) FROM new_sessions"),
    ('pinned', "SELECT COUNT(*) FROM new_sessions WHERE is_pinned=1"),
    ('stale >7d', f"SELECT COUNT(*) FROM new_sessions WHERE is_pinned=0 AND updated_at<={cut7}"),
    ('tape_entries', "SELECT COUNT(*) FROM deepchat_tape_entries"),
    ('messages', "SELECT COUNT(*) FROM deepchat_messages"),
    ('assistant_blocks', "SELECT COUNT(*) FROM deepchat_assistant_blocks"),
    ('user_messages', "SELECT COUNT(*) FROM deepchat_user_messages"),
    ('fts_tape_search', "SELECT COUNT(*) FROM deepchat_tape_search_fts"),
    ('fts_projection', "SELECT COUNT(*) FROM deepchat_tape_search_projection"),
]
print('\n--- COUNTS ---')
for label, sql in checks:
    val = c.execute(sql).fetchone()[0]
    print(f'  {label:25s} {val:>10,}')
print()

# 2. Orphan checks
print('--- ORPHAN CHECKS ---')
orphans = [
    ('tape_entries', "SELECT COUNT(*) FROM deepchat_tape_entries WHERE session_id NOT IN (SELECT id FROM new_sessions)"),
    ('messages', "SELECT COUNT(*) FROM deepchat_messages WHERE session_id NOT IN (SELECT id FROM new_sessions)"),
    ('assistant_blocks', "SELECT COUNT(*) FROM deepchat_assistant_blocks WHERE message_id NOT IN (SELECT id FROM deepchat_messages)"),
    ('user_messages', "SELECT COUNT(*) FROM deepchat_user_messages WHERE message_id NOT IN (SELECT id FROM deepchat_messages)"),
    ('usage_stats', "SELECT COUNT(*) FROM deepchat_usage_stats WHERE session_id IS NOT NULL AND session_id NOT IN (SELECT id FROM new_sessions)"),
    ('search_docs', "SELECT COUNT(*) FROM deepchat_search_documents WHERE session_id NOT IN (SELECT id FROM new_sessions)"),
    ('session_skills', "SELECT COUNT(*) FROM new_session_active_skills WHERE session_id NOT IN (SELECT id FROM new_sessions)"),
    ('fts_tape_search', "SELECT COUNT(*) FROM deepchat_tape_search_fts WHERE session_id NOT IN (SELECT id FROM new_sessions)"),
    ('fts_projection', "SELECT COUNT(*) FROM deepchat_tape_search_projection WHERE session_id NOT IN (SELECT id FROM new_sessions)"),
]

all_clean = True
for label, sql in orphans:
    val = c.execute(sql).fetchone()[0]
    status = 'PASS' if val == 0 else 'FAIL'
    if val > 0:
        all_clean = False
    print(f'  {label:25s} {val:>6}  {status}')

# 3. Integrity
c.execute("PRAGMA quick_check")
qc = c.fetchone()[0]
print(f'\n  quick_check: {qc}')

c.execute("PRAGMA foreign_key_check")
fks = c.fetchall()
print(f'  FK violations: {len(fks)}')
if fks:
    all_clean = False

# 4. File
size = os.path.getsize(DB) / 1024**3
print(f'\nDB: {size:.2f} GB')

import shutil
_, _, free = shutil.disk_usage('C:\\')
print(f'C: free: {free/1024**3:.1f} GB ({free/1024**4*100:.1f}%)')

# VERDICT
print()
print('=' * 60)
if all_clean:
    print('VERDICT: ALL CLEAN — No data integrity issues')
else:
    print('VERDICT: ISSUES FOUND — See above')
print('=' * 60)
