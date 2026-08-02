#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
restart-deepchat.py — Graceful DeepChat restart helper (2026-08-02)

WHY THIS EXISTS:
  DeepChat scans the skills directory ONCE at startup and builds an
  in-memory index. Skills added, deleted, or consolidated on disk are
  INVISIBLE until a restart. agent.db also caches the skill index, so
  stale entries persist until restart (and in rare cases need a cache
  clear — see memory "stale agent.db cache"). agent_db_prune.py
  --vacuum additionally requires DeepChat CLOSED. This helper makes
  restarts AUTOMATIC and GRACEFUL from any skill.

USAGE (from any skill when a restart is needed):
    python restart-deepchat.py --delay 20 --reason "added skill X"
    python restart-deepchat.py --check            # verify marker (post-boot)
    python restart-deepchat.py --clear            # clear pending marker

FLOW (detached child):
  1. Write pending-restart marker + restarts.log entry
  2. Sleep `delay` seconds (lets the current agent turn finish output)
  3. Send graceful WM_CLOSE to DeepChat (taskkill without /F)
  4. Wait up to 30s for exit; force-kill if still alive
  5. Relaunch DeepChat.exe (same user profile — config in AppData)
  6. Log outcome

SAFETY:
  - Detaches itself (DETACHED_PROCESS) so it survives the agent kill
  - Verifies target is DeepChat.exe before killing
  - Marker file (~/.deepchat/pending-restart.json) lets the next
    session-init step in the `system` skill verify + clear the reason
  - Non-destructive by default: --delay default 20s, no forced kill
    unless graceful close fails

POST-RESTART (system skill session-init):
  If pending-restart.json exists on boot: log the reason, clear the
  marker, and note the restart completed. If skills are STILL missing
  after restart, clear the agent.db skill-index cache (stale-cache
  heuristic — a process restart alone may not clear the indexer cache).
"""
import argparse, json, os, subprocess, sys, time, datetime

USER = os.path.expanduser('~')
DEEPCHAT_DIR = os.path.join(USER, '.deepchat')
MARKER = os.path.join(DEEPCHAT_DIR, 'pending-restart.json')
LOG = os.path.join(DEEPCHAT_DIR, 'restarts.log')
DEEPCHAT_EXE_CANDIDATES = [
    r'C:\Program Files\DeepChat\DeepChat.exe',
    os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'DeepChat', 'DeepChat.exe'),
]
PROC_NAME = 'DeepChat.exe'


def log(msg):
    ts = datetime.datetime.now().isoformat()
    line = f'{ts}  {msg}'
    os.makedirs(DEEPCHAT_DIR, exist_ok=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
    print(line)


def is_running(name):
    r = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {name}'],
                       capture_output=True, text=True, timeout=15)
    return name.lower() in r.stdout.lower()


def find_deepchat_exe():
    for p in DEEPCHAT_EXE_CANDIDATES:
        if os.path.exists(p):
            return p
    # PATH fallback
    import shutil
    return shutil.which('DeepChat.exe')


def write_marker(reason):
    os.makedirs(DEEPCHAT_DIR, exist_ok=True)
    data = {
        'reason': reason,
        'scheduled_at': datetime.datetime.now().isoformat(),
        'status': 'pending',
    }
    with open(MARKER, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def read_marker():
    if os.path.exists(MARKER):
        try:
            return json.load(open(MARKER, encoding='utf-8'))
        except (OSError, json.JSONDecodeError):
            return {'reason': '(unreadable marker)', 'status': 'unknown'}
    return None


def do_restart(delay, reason):
    write_marker(reason)
    log(f'SCHEDULED: DeepChat restart in {delay}s — reason: {reason}')
    time.sleep(delay)

    if not is_running(PROC_NAME):
        log('DeepChat already stopped — skipping kill, relaunching')
    else:
        # 1. graceful close (WM_CLOSE)
        subprocess.run(['taskkill', '/IM', PROC_NAME], capture_output=True, text=True)
        # 2. wait up to 30s
        for _ in range(60):
            if not is_running(PROC_NAME):
                break
            time.sleep(0.5)
        # 3. force if still alive
        if is_running(PROC_NAME):
            log('Graceful close timed out — forcing kill')
            subprocess.run(['taskkill', '/IM', PROC_NAME, '/F'], capture_output=True, text=True)
            time.sleep(2)

    # 4. relaunch
    exe = find_deepchat_exe()
    if exe and os.path.exists(exe):
        subprocess.Popen([exe],
                         creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                         close_fds=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
        log(f'RELAUNCHED: {exe}')
    else:
        log('ERROR: DeepChat.exe not found — could not relaunch. Restart manually.')

    # 5. mark done (the next boot will confirm it actually came back)
    m = read_marker()
    if m:
        m['status'] = 'restart-issued'
        with open(MARKER, 'w', encoding='utf-8') as f:
            json.dump(m, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Graceful DeepChat restart helper')
    parser.add_argument('--delay', type=int, default=20, help='seconds to wait before restart (default 20)')
    parser.add_argument('--reason', default='unspecified', help='reason for the restart')
    parser.add_argument('--check', action='store_true', help='report pending-restart marker and exit')
    parser.add_argument('--clear', action='store_true', help='clear the pending-restart marker and exit')
    args = parser.parse_args()

    # Child-mode guard: if DEEPCHAT_RESTART_CHILD is set, we ARE the detached child.
    # Otherwise, detach a child and exit (so the agent turn can finish).
    if not os.environ.get('DEEPCHAT_RESTART_CHILD'):
        env = os.environ.copy()
        env['DEEPCHAT_RESTART_CHILD'] = '1'
        subprocess.Popen(
            [sys.executable, os.path.abspath(__file__), '--delay', str(args.delay), '--reason', args.reason],
            env=env, close_fds=True,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        log(f'Detached restart child launched (restart in {args.delay}s, reason: {args.reason})')
        print(f'[RESTART SCHEDULED] DeepChat will restart in {args.delay}s. Reason: {args.reason}')
        return

    # We are the detached child
    do_restart(args.delay, args.reason)
    log('Restart sequence complete.')


if __name__ == '__main__':
    main()
