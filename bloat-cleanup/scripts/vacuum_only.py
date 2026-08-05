#!/usr/bin/env python3
"""Standalone VACUUM runner for agent.db.
Must be run while DeepChat is CLOSED for maximum compaction.
"""
import sqlite3, os, time

ROAMING = os.path.expandvars(r'%APPDATA%\DeepChat')
DB_PATH = os.path.join(ROAMING, 'app_db', 'agent.db')

print("=" * 60)
print("AGENT.DB VACUUM")
print("=" * 60)

before = os.path.getsize(DB_PATH)
print(f"Before: {before/1024**3:.2f} GB")

# Remove WAL/SHM first
for ext in ['-wal', '-shm']:
    path = DB_PATH + ext
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"Removed {os.path.basename(path)}")
        except Exception as e:
            print(f"WARNING: could not remove {os.path.basename(path)}: {e}")

conn = sqlite3.connect(DB_PATH)
t0 = time.time()

try:
    conn.execute("VACUUM")
    elapsed = time.time() - t0
    after = os.path.getsize(DB_PATH)
    freed = before - after
    print(f"\nVACUUM complete in {elapsed:.0f}s")
    print(f"After:  {after/1024**3:.2f} GB")
    print(f"Freed:  {freed/1024**3:.2f} GB ({freed/before*100:.1f}%)")
except sqlite3.OperationalError as e:
    if 'locked' in str(e):
        print("\nFAILED: Database is locked. Close DeepChat completely and retry.")
    else:
        print(f"\nFAILED: {e}")
finally:
    conn.close()
