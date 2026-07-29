import sqlite3, os, time

DB = os.path.expandvars(r'%APPDATA%\DeepChat\app_db\agent.db')
conn = sqlite3.connect(DB)
c = conn.cursor()

print("=== POST-PRUNE VERIFICATION ===")
print(f"DB size: {os.path.getsize(DB)/1024**3:.2f} GB")
print()

for table in ['deepchat_sessions','new_sessions','deepchat_tape_entries',
              'deepchat_messages','deepchat_assistant_blocks','deepchat_user_messages']:
    c.execute(f"SELECT COUNT(*) FROM [{table}]")
    print(f"  {table:30s} {c.fetchone()[0]:>12,} rows")

now_ms = int(time.time() * 1000)
print("\n=== SESSION AGE DISTRIBUTION ===")
brackets = [(3,"0-3d"),(7,"4-7d"),(14,"8-14d"),(30,"15-30d"),(9999,"30d+")]
prev = now_ms
for d,label in brackets:
    cutoff = now_ms - (d * 86400 * 1000)
    c.execute("SELECT COUNT(*) FROM new_sessions WHERE updated_at < ? AND updated_at >= ?", (prev, cutoff))
    cnt = c.fetchone()[0]
    print(f"  {label:10s} {cnt:>5} sessions")
    prev = cutoff

c.execute("SELECT COUNT(*) FROM new_sessions")
total = c.fetchone()[0]
print(f"  {'TOTAL':10s} {total:>5} sessions")
conn.close()
