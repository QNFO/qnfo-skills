#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
restart-deepchat.py — Gracefully quit + relaunch DeepChat (2026-08-02)

Canonical restart mechanism for DeepChat skill updates. DeepChat builds its
skill index from agent.db at STARTUP — new skills are invisible, deleted
skills persist as phantom entries, and modified skills may be stale until
restart. This script provides a clean, safe restart.

AGENT SAFETY (IMPORTANT):
  An agent MUST NOT invoke this directly mid-turn — killing the host process
  terminates the agent mid-session and loses state. Use schedule-restart.py
  to defer the restart, OR instruct the user to run this manually.

Graceful sequence:
  1. Send WM_CLOSE to all DeepChat.exe processes (graceful quit).
  2. Wait up to --grace seconds for them to exit.
  3. Force-kill any survivors (--force) if they did not exit in time.
  4. Relaunch DeepChat.exe from the canonical install path.

USAGE:
  python restart-deepchat.py              # graceful close + relaunch
  python restart-deepchat.py --grace 15   # wait up to 15s for close
  python restart-deepchat.py --force      # taskkill /F after grace
  python restart-deepchat.py --no-relaunch# quit only (user relaunches)

Python-only (no PowerShell) per the windows-command-patterns mandate.
"""
import subprocess, sys, time, os, argparse

CHROME_INSTALLS = [
    r'C:\Program Files\DeepChat\DeepChat.exe',
    r'C:\Users\LENOVO\AppData\Local\Programs\DeepChat\DeepChat.exe',
]

PROC_NAME = 'DeepChat.exe'


def find_deepchat_pids():
    """Return PIDs of running DeepChat.exe processes."""
    try:
        r = subprocess.run(['tasklist', '/fi', f'imagename eq {PROC_NAME}',
                            '/fo', 'csv', '/nh'],
                           capture_output=True, text=True, timeout=20)
    except Exception as e:
        print(f'  [tasklist ERR] {e}')
        return []
    pids = []
    for line in r.stdout.splitlines():
        parts = [p.strip().strip('"') for p in line.split(',')]
        if len(parts) >= 2 and parts[0] == PROC_NAME:
            try:
                pids.append(parts[1])
            except ValueError:
                pass
    return pids


def graceful_close(pids):
    """Send WM_CLOSE (graceful) to each DeepChat process."""
    for pid in pids:
        try:
            subprocess.run(['taskkill', '/pid', pid], capture_output=True,
                           text=True, timeout=20)
            print(f'  [graceful close] pid {pid}')
        except Exception as e:
            print(f'  [ERR pid {pid}] {e}')


def wait_for_exit(pids, grace):
    """Wait up to grace seconds for processes to exit."""
    deadline = time.time() + grace
    while time.time() < deadline:
        remaining = find_deepchat_pids()
        if not remaining:
            return True
        time.sleep(1)
    return False


def force_kill(pids):
    for pid in pids:
        try:
            subprocess.run(['taskkill', '/f', '/pid', pid], capture_output=True,
                           text=True, timeout=20)
            print(f'  [force kill] pid {pid}')
        except Exception as e:
            print(f'  [ERR] {e}')


def relaunch():
    for exe in CHROME_INSTALLS:
        if os.path.exists(exe):
            try:
                subprocess.Popen([exe], cwd=os.path.dirname(exe))
                print(f'  [relaunch] {exe}')
                return True
            except Exception as e:
                print(f'  [relaunch ERR] {e}')
    print('  [WARN] DeepChat.exe not found at known paths — relaunch manually')
    return False


def main():
    ap = argparse.ArgumentParser(description='Restart DeepChat gracefully')
    ap.add_argument('--grace', type=int, default=20,
                    help='seconds to wait for graceful exit (default 20)')
    ap.add_argument('--force', action='store_true',
                    help='force-kill survivors after grace period')
    ap.add_argument('--no-relaunch', action='store_true',
                    help='quit only, do not relaunch')
    args = ap.parse_args()

    pids = find_deepchat_pids()
    if not pids:
        print('DeepChat not running — skipping quit, relaunching')
        if not args.no_relaunch:
            relaunch()
        sys.exit(0)

    print(f'DeepChat running: {len(pids)} process(es): {pids}')
    graceful_close(pids)
    if wait_for_exit(pids, args.grace):
        print(f'  All processes exited cleanly')
    else:
        print(f'  {args.grace}s elapsed — processes still running')
        if args.force:
            force_kill(find_deepchat_pids())
            time.sleep(2)
        else:
            print('  (use --force to kill remaining processes)')

    if not args.no_relaunch:
        relaunch()

    print('Restart complete.')


if __name__ == '__main__':
    main()
