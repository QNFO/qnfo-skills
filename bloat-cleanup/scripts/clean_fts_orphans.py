#!/usr/bin/env python3
"""Clean orphan FTS entries from agent.db."""
import sqlite3, os

DB = os.path.expandvars(r'%APPDATA%\DeepChat\app_db\agent.db')
conn = sqlite3.connect(DB)
c = conn.cursor()

# Delete orphan FTS entries where session no longer exists
c.execute("DELETE FROM deepchat_tape_search_fts WHERE session_id NOT IN (SELECT id FROM new_sessions)")
n1 = c.rowcount
print(f"Deleted tape_search_fts orphans: {n1:,}")

c.execute("DELETE FROM deepchat_tape_search_projection WHERE session_id NOT IN (SELECT id FROM new_sessions)")
n2 = c.rowcount
print(f"Deleted projection orphans: {n2:,}")

# Also check search_documents_fts
try:
    c.execute("DELETE FROM deepchat_search_documents_fts WHERE session_id NOT IN (SELECT id FROM new_sessions)")
    n3 = c.rowcount
    print(f"Deleted search_docs_fts orphans: {n3:,}")
except Exception as e:
    print(f"search_docs_fts: {e}")

# Rebuild FTS indexes to compact freed space
for tbl in ['deepchat_tape_search_fts', 'deepchat_tape_search_projection']:
    try:
        c.execute(f"INSERT INTO [{tbl}]([{tbl}]) VALUES('rebuild')")
        print(f"Rebuilt: {tbl}")
    except Exception as e:
        print(f"{tbl}: {e}")

conn.commit()

# Final counts
c.execute("SELECT COUNT(*) FROM deepchat_tape_search_fts")
print(f"\ntape_search_fts entries: {c.fetchone()[0]:,}")
c.execute("SELECT COUNT(*) FROM deepchat_tape_search_projection")
print(f"projection entries: {c.fetchone()[0]:,}")

# Verify no more orphans
c.execute("SELECT COUNT(*) FROM deepchat_tape_search_fts WHERE session_id NOT IN (SELECT id FROM new_sessions)")
print(f"remaining orphans: {c.fetchone()[0]}")

conn.close()
print("Done.")
