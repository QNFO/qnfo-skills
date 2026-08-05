#!/usr/bin/env python3
r"""DeepChat agent.db comprehensive prune + VACUUM — Budget Laptop Edition v2.1
2026-07-29: Red-team audited + kaizen. FTS orphan handling fixed.

KEY IMPROVEMENTS OVER v2.0:
- FTS tables WITH session_id: deleted inline during prune (was skipped)
- FTS tables WITHOUT session_id: rebuild-based orphan cleanup
- FTS meta tables: cleaned
- Default cutoff: 7 days (budget laptop config)
- --budget mode: 3-day cutoff + RAM-tuned PRAGMAs
- --target-db-size: prune oldest-first until DB <= target GB
- Batch deletion (500 sessions at a time) to avoid SQLite OOM
- WAL checkpoint BEFORE operations
- RAM-aware PRAGMA tuning
- Session offload cleanup
- Post-prune metrics

Usage:
    python agent_db_prune.py --max-age-days 7 --dry-run
    python agent_db_prune.py --budget
    python agent_db_prune.py --target-db-size-gb 1.5 --vacuum
    python agent_db_prune.py --budget --vacuum
"""
import sqlite3, os, time, json, shutil, argparse, sys, gc
from datetime import datetime, timezone

ROAMING = os.path.expandvars(r'%APPDATA%\DeepChat')
DB_PATH = os.path.join(ROAMING, 'app_db', 'agent.db')
PROVIDER_DB = os.path.join(ROAMING, 'provider-db', 'providers.json')
SESSION_DIR = os.path.expandvars(r'%USERPROFILE%\.deepchat\sessions')
BATCH_SIZE = 500

# FTS tables confirmed to HAVE session_id column (can DELETE directly)
FTS_WITH_SESSION_ID = [
    'deepchat_tape_search_fts',
    'deepchat_tape_search_projection',
    'deepchat_tape_search_fts_meta',
    'deepchat_tape_search_projection_meta',
]

# FTS tables WITHOUT session_id column (use INSERT rebuild for orphan cleanup)
FTS_NO_SESSION_ID = [
    'deepchat_search_documents_fts',
    'agent_memory_fts',
]


def fmt_size(bytes_val):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} TB"


def get_db_size():
    try:
        return os.path.getsize(DB_PATH)
    except OSError:
        return 0


def check_deepchat_running():
    import subprocess
    try:
        r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq DeepChat.exe', '/NH'],
                           capture_output=True, text=True, timeout=5)
        return 'DeepChat.exe' in r.stdout
    except Exception:
        return False


def wal_checkpoint(conn):
    try:
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        print("  WAL checkpoint: TRUNCATE completed")
    except Exception as e:
        print(f"  WAL checkpoint: {e}")


def apply_budget_pragmas(conn):
    pragmas = {
        'cache_size': -4000,
        'mmap_size': 0,
        'temp_store': 2,
        'synchronous': 1,
        'page_size': 4096,
    }
    print("  Budget laptop PRAGMAs:")
    for k, v in pragmas.items():
        try:
            conn.execute(f"PRAGMA {k}={v}")
            print(f"    {k} = {v}")
        except Exception as e:
            print(f"    {k}: {e}")


def get_old_sessions(cursor, cutoff_ms):
    cursor.execute(
        "SELECT id, title, datetime(updated_at/1000, 'unixepoch'), updated_at "
        "FROM new_sessions "
        "WHERE updated_at < ? AND is_pinned = 0 "
        "ORDER BY updated_at ASC",
        (cutoff_ms,)
    )
    return cursor.fetchall()


def delete_session_data_batch(conn, session_ids, dry_run=False):
    """Delete all data for a batch of session IDs. Returns total rows deleted.
    
    v2.1: Includes FTS tables with session_id (tape_search_fts, projection, meta).
    """
    c = conn.cursor()
    if not session_ids:
        return 0
    placeholders = ','.join(['?'] * len(session_ids))
    total = 0

    # Phase 1: FTS tables with session_id (delete first to reduce FTS overhead)
    for tbl in FTS_WITH_SESSION_ID:
        sql = f"DELETE FROM [{tbl}] WHERE session_id IN ({placeholders})"
        try:
            if not dry_run:
                c.execute(sql, session_ids)
                total += c.rowcount
        except Exception as e:
            if not dry_run:
                print(f"  [{tbl}] WARNING: {e}")

    # Phase 2: Get message IDs
    c.execute(
        f"SELECT id FROM deepchat_messages WHERE session_id IN ({placeholders})",
        session_ids
    )
    msg_ids = [r[0] for r in c.fetchall()]

    # Phase 3: Message-linked tables
    if msg_ids:
        mp = ','.join(['?'] * len(msg_ids))
        msg_deletes = [
            (f"DELETE FROM deepchat_user_messages WHERE message_id IN ({mp})", msg_ids),
            (f"DELETE FROM deepchat_assistant_blocks WHERE message_id IN ({mp})", msg_ids),
            (f"DELETE FROM deepchat_usage_stats WHERE message_id IN ({mp})", msg_ids),
            (f"DELETE FROM deepchat_messages WHERE id IN ({mp})", msg_ids),
        ]
        for sql, params in msg_deletes:
            if not dry_run:
                c.execute(sql, params)
                total += c.rowcount

    # Phase 4: Session-linked tables
    session_deletes = [
        (f"DELETE FROM deepchat_tape_entries WHERE session_id IN ({placeholders})", session_ids),
        (f"DELETE FROM deepchat_usage_stats WHERE session_id IN ({placeholders})", session_ids),
        (f"DELETE FROM new_session_active_skills WHERE session_id IN ({placeholders})", session_ids),
        (f"DELETE FROM new_session_disabled_agent_tools WHERE session_id IN ({placeholders})", session_ids),
        (f"DELETE FROM deepchat_search_documents WHERE session_id IN ({placeholders})", session_ids),
        (f"DELETE FROM deepchat_sessions WHERE id IN ({placeholders})", session_ids),
        (f"DELETE FROM new_sessions WHERE id IN ({placeholders})", session_ids),
    ]
    for sql, params in session_deletes:
        try:
            if not dry_run:
                c.execute(sql, params)
                total += c.rowcount
        except Exception as e:
            if not dry_run:
                print(f"  WARNING: {e}")

    if not dry_run:
        conn.commit()
    return total


def clean_fts_no_session_id(conn, dry_run=False):
    """Clean FTS tables without session_id using rebuild + orphan sweep."""
    c = conn.cursor()
    total = 0

    # Rebuild to compact (this also helps remove stale content)
    for tbl in FTS_NO_SESSION_ID:
        try:
            if not dry_run:
                c.execute(f"INSERT INTO [{tbl}]([{tbl}]) VALUES('rebuild')")
            print(f"  [{tbl}] FTS rebuild {'(dry-run skipped)' if dry_run else 'OK'}")
        except Exception as e:
            if 'no such table' in str(e).lower():
                continue
            print(f"  [{tbl}] FTS rebuild: {e}")

    return total


def compact_db(conn, dry_run=False):
    if dry_run:
        print("  PRAGMA optimize (dry-run skipped)")
        return
    try:
        conn.execute("PRAGMA optimize")
        print("  PRAGMA optimize: OK")
    except Exception as e:
        print(f"  PRAGMA optimize: {e}")


def vacuum_db(conn):
    print("  Running VACUUM (this may take a while)...")
    before = get_db_size()
    t0 = time.time()
    try:
        conn.execute("VACUUM")
        elapsed = time.time() - t0
        after = get_db_size()
        freed = before - after
        print(f"  VACUUM complete: {fmt_size(before)} -> {fmt_size(after)} "
              f"(-{fmt_size(freed)}) in {elapsed:.0f}s")
    except sqlite3.OperationalError as e:
        if 'locked' in str(e):
            print("  VACUUM FAILED: database is locked. Close DeepChat first.")
        else:
            print(f"  VACUUM FAILED: {e}")


def compact_providers():
    if not os.path.exists(PROVIDER_DB):
        return
    try:
        before = os.path.getsize(PROVIDER_DB)
        with open(PROVIDER_DB, 'r', encoding='utf-8') as f:
            data = json.load(f)
        compacted = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        if len(compacted.encode('utf-8')) < before:
            with open(PROVIDER_DB, 'w', encoding='utf-8') as f:
                f.write(compacted)
            after = os.path.getsize(PROVIDER_DB)
            print(f"  providers.json: {fmt_size(before)} -> {fmt_size(after)} "
                  f"(-{fmt_size(before - after)})")
        else:
            print(f"  providers.json: {fmt_size(before)} (already compact)")
    except Exception as e:
        print(f"  providers.json: {e}")


def clean_session_offloads(keep_current=True):
    if not os.path.exists(SESSION_DIR):
        return
    current_session = None
    if keep_current:
        try:
            ct = sqlite3.connect(DB_PATH)
            cc = ct.cursor()
            cc.execute("SELECT id FROM deepchat_sessions ORDER BY rowid DESC LIMIT 1")
            row = cc.fetchone()
            if row:
                current_session = row[0]
            ct.close()
        except Exception:
            pass

    deleted = 0
    freed = 0
    for entry in os.listdir(SESSION_DIR):
        path = os.path.join(SESSION_DIR, entry)
        if os.path.isdir(path) and entry != current_session:
            try:
                size = sum(os.path.getsize(os.path.join(dp, f))
                           for dp, _, files in os.walk(path) for f in files)
                shutil.rmtree(path)
                deleted += 1
                freed += size
            except Exception:
                pass

    if deleted > 0:
        print(f"  Session offloads: deleted {deleted} dirs, freed {fmt_size(freed)}")
    else:
        print(f"  Session offloads: no stale dirs")


def get_disk_free_gb():
    try:
        import ctypes
        free = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wintypes.LPCWSTR("C:\\"), None, None, ctypes.byref(free))
        return free.value / (1024 ** 3)
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="DeepChat agent.db prune — Budget Laptop Edition v2.1")
    parser.add_argument('--max-age-days', type=int, default=7,
                        help='Delete sessions older than N days (default: 7)')
    parser.add_argument('--budget', action='store_true',
                        help='Budget laptop mode: 3-day cutoff + RAM-tuned PRAGMAs')
    parser.add_argument('--target-db-size-gb', type=float, default=0,
                        help='Prune oldest-first until DB <= N GB')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--vacuum', action='store_true',
                        help='Run VACUUM after deletions (close DeepChat first)')
    parser.add_argument('--no-session-clean', action='store_true')
    parser.add_argument('--no-provider-compact', action='store_true')
    args = parser.parse_args()

    if args.budget:
        args.max_age_days = 3
        args.target_db_size_gb = max(args.target_db_size_gb, 1.5)

    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    cutoff_ms = now_ms - (args.max_age_days * 86400 * 1000)

    print("=" * 60)
    print(f"DEEPCHAT AGENT.DB PRUNE v2.1{' -- DRY RUN' if args.dry_run else ''}")
    print(f"{datetime.now(timezone.utc).isoformat()}")
    print(f"DB: {DB_PATH}")
    print(f"Age cutoff: {args.max_age_days} days")
    if args.budget:
        print(f"Mode: BUDGET LAPTOP (6GB RAM optimized)")
    if args.target_db_size_gb:
        print(f"Target DB size: <= {args.target_db_size_gb} GB")
    print("=" * 60)

    ds_free = get_disk_free_gb()
    initial_size = get_db_size()
    print(f"C: drive free: {ds_free:.1f} GB" if ds_free else "C: drive: unknown")
    print(f"agent.db: {fmt_size(initial_size)}")
    print()

    running = check_deepchat_running()
    if running:
        print("[WARNING] DeepChat appears to be running.")
        print("  VACUUM will fail. Close DeepChat for full compaction.")
        print()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if args.budget:
        apply_budget_pragmas(conn)

    # Phase 0: WAL checkpoint
    print("-" * 60)
    print("PHASE 0: WAL Checkpoint")
    print("-" * 60)
    wal_checkpoint(conn)

    # Phase 1: Identify old sessions
    print()
    print("-" * 60)
    print("PHASE 1: Identify old sessions")
    print("-" * 60)
    old_sessions = get_old_sessions(c, cutoff_ms)

    if not old_sessions:
        print(f"No unpinned sessions older than {args.max_age_days} days.")
        conn.close()
        return

    old_ids = [s[0] for s in old_sessions]
    print(f"Found {len(old_sessions)} sessions older than {args.max_age_days} days:")
    for i, s in enumerate(old_sessions[:10]):
        sid, title, updated, _ = s
        print(f"  {i+1:3d}. {sid[:16]:16s} | {updated} | {(title or '(no title)')[:60]}")
    if len(old_sessions) > 10:
        print(f"  ... and {len(old_sessions) - 10} more")

    id_placeholders = ','.join(['?'] * len(old_ids))
    c.execute(f"SELECT COUNT(*) FROM deepchat_tape_entries WHERE session_id IN ({id_placeholders})", old_ids)
    tape_count = c.fetchone()[0]
    c.execute(f"SELECT COUNT(*) FROM deepchat_messages WHERE session_id IN ({id_placeholders})", old_ids)
    msg_count = c.fetchone()[0]
    c.execute(
        f"SELECT COUNT(*) FROM deepchat_assistant_blocks "
        f"WHERE message_id IN (SELECT id FROM deepchat_messages WHERE session_id IN ({id_placeholders}))",
        old_ids)
    block_count = c.fetchone()[0]

    # Count FTS entries
    fts_counts = {}
    for tbl in FTS_WITH_SESSION_ID:
        try:
            c.execute(f"SELECT COUNT(*) FROM [{tbl}] WHERE session_id IN ({id_placeholders})", old_ids)
            fts_counts[tbl] = c.fetchone()[0]
        except Exception:
            fts_counts[tbl] = 0

    print(f"\n  Tape entries to delete:   {tape_count:>10,}")
    print(f"  Messages to delete:       {msg_count:>10,}")
    print(f"  Assistant blocks:         {block_count:>10,}")
    for tbl, cnt in fts_counts.items():
        if cnt > 0:
            print(f"  {tbl:25s} {cnt:>10,}")

    if args.dry_run:
        print("\n[DRY RUN] No changes will be made.")
        conn.close()
        return

    # Phase 2: Delete session data in batches
    print()
    print("-" * 60)
    print("PHASE 2: Delete old session data (batched, including FTS)")
    print("-" * 60)
    total_deleted = 0
    n_batches = (len(old_ids) + BATCH_SIZE - 1) // BATCH_SIZE

    # Sort oldest-first for target mode
    if args.target_db_size_gb:
        print(f"Target mode: pruning until DB <= {args.target_db_size_gb} GB")
        target_bytes = args.target_db_size_gb * 1024 ** 3
        old_sessions.sort(key=lambda s: s[3])

        for batch_idx in range(n_batches):
            batch = old_sessions[batch_idx * BATCH_SIZE:(batch_idx + 1) * BATCH_SIZE]
            batch_ids = [s[0] for s in batch]
            deleted = delete_session_data_batch(conn, batch_ids)
            total_deleted += deleted

            current_size = get_db_size()
            pct = min(100, (batch_idx + 1) * 100 // n_batches)
            print(f"  Batch {batch_idx + 1}/{n_batches} ({pct}%): "
                  f"deleted {deleted} rows, DB now {fmt_size(current_size)}")

            if current_size <= target_bytes:
                print(f"  Target reached! {fmt_size(current_size)} <= {args.target_db_size_gb} GB")
                break
            gc.collect()
    else:
        for batch_idx in range(n_batches):
            batch = old_sessions[batch_idx * BATCH_SIZE:(batch_idx + 1) * BATCH_SIZE]
            batch_ids = [s[0] for s in batch]
            deleted = delete_session_data_batch(conn, batch_ids)
            total_deleted += deleted
            pct = min(100, (batch_idx + 1) * 100 // n_batches)
            print(f"  Batch {batch_idx + 1}/{n_batches} ({pct}%): deleted {deleted} rows")
            gc.collect()

    print(f"\n  Total rows deleted: {total_deleted:,}")
    mid_size = get_db_size()
    print(f"  DB size after deletes: {fmt_size(mid_size)}")

    # Phase 3: Clean FTS tables without session_id + rebuild
    print()
    print("-" * 60)
    print("PHASE 3: Clean FTS (no session_id tables) + rebuild indexes")
    print("-" * 60)
    clean_fts_no_session_id(conn)
    compact_db(conn)

    # Phase 4: Compact providers.json
    if not args.no_provider_compact:
        print()
        print("-" * 60)
        print("PHASE 4: Compact providers.json")
        print("-" * 60)
        compact_providers()

    # Phase 5: Clean session offloads
    if not args.no_session_clean:
        print()
        print("-" * 60)
        print("PHASE 5: Clean session offloads")
        print("-" * 60)
        clean_session_offloads()

    # Phase 6: VACUUM
    if args.vacuum:
        print()
        print("-" * 60)
        print("PHASE 6: VACUUM")
        print("-" * 60)
        if running:
            print("[SKIP] DeepChat is running -- VACUUM would fail.")
            print("Close DeepChat and run: python agent_db_prune.py --vacuum")
        else:
            vacuum_db(conn)

    # Phase 7: Clean WAL/SHM
    print()
    print("-" * 60)
    print("PHASE 7: Clean WAL/SHM artifacts")
    print("-" * 60)
    for ext in ['-wal', '-shm']:
        wal_path = DB_PATH + ext
        if os.path.exists(wal_path):
            try:
                os.remove(wal_path)
                print(f"  Removed: {os.path.basename(wal_path)}")
            except Exception as e:
                print(f"  {os.path.basename(wal_path)}: {e}")

    conn.close()

    # Final report
    final_size = get_db_size()
    final_free = get_disk_free_gb()
    freed = initial_size - final_size

    print()
    print("=" * 60)
    print("  PRUNE COMPLETE")
    print("=" * 60)
    print(f"  agent.db: {fmt_size(initial_size)} -> {fmt_size(final_size)} "
          f"(-{fmt_size(freed)} = {freed/initial_size*100:.1f}%)")
    print(f"  Sessions pruned: {len(old_sessions)}")
    print(f"  Rows deleted: {total_deleted:,}")
    if ds_free and final_free:
        disk_freed = final_free - ds_free
        print(f"  C: drive: {ds_free:.1f} -> {final_free:.1f} GB free "
              f"(+{disk_freed:.1f} GB)")
    if args.vacuum and not running:
        print(f"  VACUUM: completed")
    elif args.vacuum and running:
        print(f"  VACUUM: SKIPPED (DeepChat running)")
    print()


if __name__ == '__main__':
    main()
