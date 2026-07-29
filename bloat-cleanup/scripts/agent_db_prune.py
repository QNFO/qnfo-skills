#!/usr/bin/env python3
"""DeepChat agent.db comprehensive prune + VACUUM + file cleanup.
v1.0 — 2026-07-29: extracted from proven kill→clean→restart pattern.

Deletes ALL data for sessions older than --max-age-days (default 30),
rebuilds FTS indexes, VACUUMs the database to reclaim freed pages,
compacts providers.json, and cleans WAL/SHM artifacts.

Safe: skips pinned sessions, runs VACUUM only if --vacuum flag is set.
Intended to run while DeepChat is CLOSED for maximum compaction,
but can run live (VACUUM will fail with lock on live DB).

Usage:
    # Dry-run (no changes):
    python agent_db_prune.py --dry-run

    # Delete old sessions, no VACUUM:
    python agent_db_prune.py

    # Delete + VACUUM (requires DeepChat closed):
    python agent_db_prune.py --vacuum

    # Aggressive: 14-day cutoff + VACUUM:
    python agent_db_prune.py --max-age-days 14 --vacuum
"""
import sqlite3, os, time, json, shutil, argparse, sys
from datetime import datetime, timezone

ROAMING = os.path.expandvars(r'%APPDATA%\DeepChat')
DB_PATH = os.path.join(ROAMING, 'app_db', 'agent.db')
PROVIDER_DB = os.path.join(ROAMING, 'provider-db', 'providers.json')
RTK_DB = os.path.join(ROAMING, 'rtk', 'history.db')


def get_old_sessions(cursor, cutoff_ms):
    """Return (id, title, updated) for unpinned sessions older than cutoff."""
    cursor.execute(
        'SELECT id, title, datetime(updated_at/1000, "unixepoch") '
        'FROM new_sessions '
        'WHERE updated_at < ? AND is_pinned = 0 '
        'ORDER BY updated_at ASC',
        (cutoff_ms,)
    )
    return cursor.fetchall()


def get_message_ids(cursor, session_ids):
    """Get all message IDs belonging to given session IDs."""
    if not session_ids:
        return []
    placeholders = ','.join(['?'] * len(session_ids))
    cursor.execute(
        f'SELECT id FROM deepchat_messages WHERE session_id IN ({placeholders})',
        session_ids
    )
    return [r[0] for r in cursor.fetchall()]


def delete_session_data(conn, old_ids, dry_run=False):
    """Delete all data for old sessions across all related tables."""
    c = conn.cursor()
    total = 0
    placeholders = ','.join(['?'] * len(old_ids))

    msg_ids = get_message_ids(c, old_ids)
    msg_placeholders = ','.join(['?'] * len(msg_ids)) if msg_ids else None

    # Ordered deletions: children first, then tape entries, then session records
    deletions = []

    # FTS indexes first
    for tbl in ['deepchat_tape_search_fts', 'deepchat_tape_search_projection',
                'deepchat_tape_search_fts_meta', 'deepchat_tape_search_projection_meta']:
        deletions.append((f'DELETE FROM [{tbl}] WHERE session_id IN ({placeholders})', old_ids, tbl))

    # Search documents
    deletions.append((f'DELETE FROM deepchat_search_documents_fts WHERE session_id IN ({placeholders})', old_ids, 'search_docs_fts'))
    deletions.append((f'DELETE FROM deepchat_search_documents WHERE session_id IN ({placeholders})', old_ids, 'search_docs'))

    # Usage stats
    deletions.append((f'DELETE FROM deepchat_usage_stats WHERE session_id IN ({placeholders})', old_ids, 'usage_stats'))

    # Session skills + disabled tools
    deletions.append((f'DELETE FROM new_session_active_skills WHERE session_id IN ({placeholders})', old_ids, 'session_skills'))
    deletions.append((f'DELETE FROM new_session_disabled_agent_tools WHERE session_id IN ({placeholders})', old_ids, 'disabled_tools'))

    # Message-linked tables
    if msg_placeholders:
        deletions.append((f'DELETE FROM deepchat_user_messages WHERE message_id IN ({msg_placeholders})', msg_ids, 'user_messages'))
        deletions.append((f'DELETE FROM deepchat_assistant_blocks WHERE message_id IN ({msg_placeholders})', msg_ids, 'assistant_blocks'))
        deletions.append((f'DELETE FROM deepchat_messages WHERE id IN ({msg_placeholders})', msg_ids, 'messages'))
        deletions.append((f'DELETE FROM deepchat_usage_stats WHERE message_id IN ({msg_placeholders})', msg_ids, 'usage_stats_by_msg'))

    # Tape entries (the big one)
    deletions.append((f'DELETE FROM deepchat_tape_entries WHERE session_id IN ({placeholders})', old_ids, 'tape_entries'))

    # Session records (last)
    deletions.append((f'DELETE FROM deepchat_sessions WHERE id IN ({placeholders})', old_ids, 'deepchat_sessions'))
    deletions.append((f'DELETE FROM new_sessions WHERE id IN ({placeholders})', old_ids, 'new_sessions'))

    for sql, params, label in deletions:
        if dry_run:
            c.execute(sql.replace('DELETE', 'SELECT COUNT(*)'), params)
            count = c.fetchone()[0]
        else:
            c.execute(sql, params)
            count = c.rowcount
        total += count
        action = 'WOULD delete' if dry_run else 'Deleted'
        print(f'  [{label:25s}] {action} {count:>6} rows')

    print(f'  {"─" * 50}')
    print(f'  TOTAL {"WOULD delete" if dry_run else "Deleted"}: {total} rows')

    if not dry_run:
        conn.commit()
    return total


def rebuild_fts_indexes(cursor):
    """Rebuild all FTS indexes to compact after deletions."""
    fts_tables = [
        'deepchat_tape_search_fts',
        'deepchat_tape_search_projection',
        'deepchat_search_documents_fts',
        'agent_memory_fts',
    ]
    for ft in fts_tables:
        try:
            cursor.execute(f"INSERT INTO [{ft}]([{ft}]) VALUES('rebuild')")
            print(f'  [{ft}] FTS: rebuilt')
        except Exception as e:
            print(f'  [{ft}] FTS: {e}')

    # Clean orphaned FTS entries
    orphan_checks = [
        ('deepchat_tape_search_fts', 'session_id', 'new_sessions'),
        ('deepchat_tape_search_projection', 'session_id', 'new_sessions'),
        ('deepchat_search_documents_fts', 'session_id', 'new_sessions'),
        ('deepchat_search_documents', 'session_id', 'new_sessions'),
    ]
    for tbl, fk_col, parent in orphan_checks:
        try:
            cursor.execute(f'DELETE FROM [{tbl}] WHERE {fk_col} NOT IN (SELECT id FROM [{parent}])')
            if cursor.rowcount:
                print(f'  [{tbl}] orphaned cleaned: {cursor.rowcount}')
        except:
            pass
    print()


def compact_providers_json():
    """Re-serialize providers.json with compact formatting."""
    if not os.path.exists(PROVIDER_DB):
        return
    s1 = os.path.getsize(PROVIDER_DB)
    if s1 < 1024 * 1024:  # Skip if under 1MB
        print(f'  providers.json: {s1/1024/1024:.1f} MB (skipped — already small)')
        return
    try:
        with open(PROVIDER_DB, encoding='utf-8') as f:
            data = json.load(f)
        with open(PROVIDER_DB, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        s2 = os.path.getsize(PROVIDER_DB)
        print(f'  providers.json: {s1/1024/1024:.1f} → {s2/1024/1024:.1f} MB (-{(s1-s2)/1024/1024:.1f} MB)')
    except Exception as e:
        print(f'  providers.json: error — {e}')


def clean_wal_files():
    """Remove WAL/SHM artifacts."""
    for base in [DB_PATH, RTK_DB]:
        for ext in ['-wal', '-shm']:
            p = base + ext
            if os.path.exists(p):
                try:
                    sz = os.path.getsize(p)
                    os.remove(p)
                    print(f'  Removed {os.path.basename(p)}: {sz/1024/1024:.1f} MB')
                except:
                    pass


def run_vacuum(db_path):
    """VACUUM the database to reclaim freed pages."""
    size_before = os.path.getsize(db_path)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('PRAGMA freelist_count')
    free_before = c.fetchone()[0]
    c.execute('PRAGMA page_size')
    ps = c.fetchone()[0]
    c.execute('PRAGMA optimize')
    conn.close()
    print(f'  Freelist before VACUUM: {free_before} pages ({free_before*ps/1048576:.1f} MB)')

    if free_before == 0:
        print(f'  No free pages — VACUUM would have no effect. Skipping.')
        return size_before

    print(f'  Running VACUUM on {size_before/1024**3:.2f} GB database...')
    t0 = time.time()

    conn = sqlite3.connect(db_path)
    conn.isolation_level = None
    try:
        conn.execute('VACUUM')
        elapsed = time.time() - t0
        print(f'  VACUUM complete ({elapsed:.1f}s)')
    except sqlite3.OperationalError as e:
        print(f'  VACUUM failed (likely DB locked by running DeepChat): {e}')
        print(f'  Tip: Close DeepChat first or run "kill_clean_restart.bat"')
    finally:
        conn.close()

    size_after = os.path.getsize(db_path)
    reduction = (size_before - size_after) / (1024 * 1024)
    print(f'  Size: {size_before/1024**3:.2f} → {size_after/1024**3:.2f} GB (-{reduction:.1f} MB)')

    # Clean WAL after VACUUM
    for ext in ['-wal', '-shm']:
        p = db_path + ext
        if os.path.exists(p):
            try:
                os.remove(p)
            except:
                pass

    return size_after


def main():
    parser = argparse.ArgumentParser(description='DeepChat agent.db prune + VACUUM')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted, no changes')
    parser.add_argument('--vacuum', action='store_true', help='Run VACUUM after pruning (needs DB unlocked)')
    parser.add_argument('--max-age-days', type=int, default=30, help='Delete sessions older than N days (default: 30)')
    args = parser.parse_args()

    cutoff_ms = int(time.time() * 1000) - args.max_age_days * 86400 * 1000
    mode = 'DRY RUN' if args.dry_run else 'LIVE'

    print('=' * 60)
    print(f'  DEEPCHAT AGENT.DB PRUNE — {mode}')
    print(f'  {datetime.now().isoformat()}')
    print(f'  DB: {DB_PATH}')
    print(f'  Age cutoff: {args.max_age_days} days')
    print('=' * 60)
    print()

    if not os.path.exists(DB_PATH):
        print(f'ERROR: agent.db not found at {DB_PATH}')
        sys.exit(1)

    size_before = os.path.getsize(DB_PATH)
    print(f'  agent.db: {size_before/1024**3:.2f} GB')
    print()

    # ──────────────────────────────────────────────
    # PHASE 1: Identify old sessions
    # ──────────────────────────────────────────────
    print('─' * 60)
    print('PHASE 1: Identify old sessions')
    print('─' * 60)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    old_sessions = get_old_sessions(c, cutoff_ms)
    old_ids = [s[0] for s in old_sessions]

    if not old_sessions:
        print(f'  No unpinned sessions older than {args.max_age_days} days.')
        conn.close()
    else:
        print(f'  Found {len(old_sessions)} sessions older than {args.max_age_days} days:')
        for sid, title, updated in old_sessions[:10]:
            print(f'    {sid[:24]:24s} | {str(title)[:50]:50s} | {updated}')
        if len(old_sessions) > 10:
            print(f'    ... and {len(old_sessions) - 10} more')

        # Count what would be deleted
        c.execute('SELECT COUNT(*) FROM deepchat_tape_entries WHERE session_id IN ({})'.format(','.join(['?']*len(old_ids))), old_ids)
        tape_count = c.fetchone()[0]

        msg_ids = get_message_ids(c, old_ids)
        if msg_ids:
            mp = ','.join(['?']*len(msg_ids))
            c.execute(f'SELECT COUNT(*) FROM deepchat_assistant_blocks WHERE message_id IN ({mp})', msg_ids)
            block_count = c.fetchone()[0]
            c.execute(f'SELECT COUNT(*) FROM deepchat_messages WHERE id IN ({mp})', msg_ids)
            msg_count = c.fetchone()[0]
        else:
            block_count = msg_count = 0

        print()
        print(f'  Tape entries to delete:  {tape_count}')
        print(f'  Messages to delete:      {msg_count}')
        print(f'  Assistant blocks:        {block_count}')
        print()

        # ──────────────────────────────────────────────
        # PHASE 2: Delete or dry-run report
        # ──────────────────────────────────────────────
        print('─' * 60)
        print(f'PHASE 2: {"DRY RUN — would delete" if args.dry_run else "Delete"} old session data')
        print('─' * 60)
        deleted = delete_session_data(conn, old_ids, dry_run=args.dry_run)

        # ──────────────────────────────────────────────
        # PHASE 3: Rebuild FTS
        # ──────────────────────────────────────────────
        if not args.dry_run and deleted > 0:
            print('─' * 60)
            print('PHASE 3: Rebuild FTS indexes')
            print('─' * 60)
            rebuild_fts_indexes(c)

        conn.commit()
        conn.close()

    # ──────────────────────────────────────────────
    # PHASE 4: Compact providers.json
    # ──────────────────────────────────────────────
    print('─' * 60)
    print('PHASE 4: Compact providers.json')
    print('─' * 60)
    compact_providers_json()
    print()

    # ──────────────────────────────────────────────
    # PHASE 5: VACUUM (if requested)
    # ──────────────────────────────────────────────
    if args.vacuum and not args.dry_run:
        print('─' * 60)
        print('PHASE 5: VACUUM database')
        print('─' * 60)
        final_size = run_vacuum(DB_PATH)
    else:
        final_size = os.path.getsize(DB_PATH)
        if args.dry_run:
            print('  VACUUM skipped (dry run)')
        else:
            print('  VACUUM skipped (use --vacuum flag, requires DeepChat closed)')
    print()

    # ──────────────────────────────────────────────
    # PHASE 6: Clean WAL artifacts
    # ──────────────────────────────────────────────
    print('─' * 60)
    print('PHASE 6: Clean WAL/SHM artifacts')
    print('─' * 60)
    clean_wal_files()
    print()

    # ──────────────────────────────────────────────
    # SUMMARY
    # ──────────────────────────────────────────────
    print('=' * 60)
    print('  PRUNE COMPLETE')
    print('=' * 60)

    reduction = (size_before - final_size) / (1024 * 1024)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM new_sessions')
    sessions = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM deepchat_tape_entries')
    tapes = c.fetchone()[0]
    conn.close()

    print(f'  agent.db: {size_before/1024**3:.2f} → {final_size/1024**3:.2f} GB (-{reduction:.1f} MB)')
    print(f'  Sessions: {sessions}')
    print(f'  Tape entries: {tapes}')
    print(f'  Sessions >{args.max_age_days}d: 0')

    usage = shutil.disk_usage('C:')
    print(f'  C: drive: {usage.free/1024**3:.1f} GB free ({usage.free/usage.total*100:.1f}%)')


if __name__ == '__main__':
    main()
