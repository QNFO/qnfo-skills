#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schedule-restart.py — Deferred auto-restart of DeepChat (2026-08-02)

AGENT-SAFE restart: an agent MUST NOT kill its own host process mid-turn.
This script registers a ONE-SHOT Windows Scheduled Task that fires after a
delay, runs restart-deepchat.py (graceful quit + relaunch), and auto-deletes
itself. This lets the agent update skills on disk and request a restart that
happens safely AFTER the current session ends (or at the user's next
interaction window), without terminating the agent mid-conversation.

WHEN TO USE (per skill memories):
  - A NEW skill was created  -> invisible until restart (skill-creator)
  - A skill was DELETED      -> phantom persists in agent.db until restart
  - Skills were bulk-edited  -> stale index entries (kaizen)
  - Platform-default skill restored -> re-delete + restart (bloat-cleanup)
  - agent.db cache is stale  -> skill fails to load after disk edit
    (memory: "suspect a stale agent.db cache rather than frontmatter errors")

USAGE:
  python schedule-restart.py                     # restart in 60s
  python schedule-restart.py --delay 120         # restart in 120s
  python schedule-restart.py --delay 0           # as fast as Task Scheduler allows
  python schedule-restart.py --task DEEPCHAT-RESTART-NOW

Cancellation: python cancel-restart.py
"""
import subprocess, sys, os, argparse, datetime, time

TASK_NAME = 'DeepChat-AutoRestart'
TASK_XML = '''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <TimeTrigger>
      <StartBoundary>{start}</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>{user}</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <Hidden>false</Hidden>
    <ExecutionTimeLimit>PT10M</ExecutionTimeLimit>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{python}</Command>
      <Arguments>{script} --grace 20 --force</Arguments>
    </Exec>
  </Actions>
</Task>
'''


def get_python():
    import sys as _sys
    return _sys.executable


def schedule(delay_seconds):
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'restart-deepchat.py')
    start = (datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds))
    # Task Scheduler StartBoundary format: YYYY-MM-DDTHH:MM:SS
    start_str = start.strftime('%Y-%m-%dT%H:%M:%S')
    user = os.environ.get('USERNAME', os.path.expanduser('~').split('\\')[-1])
    # Try schtasks /create first (simplest)
    cmd = [
        'schtasks', '/create', '/tn', TASK_NAME,
        '/tr', f'"{get_python()}" "{script}" --grace 20 --force',
        '/sc', 'once', '/st', start.strftime('%H:%M:%S'),
        '/f'
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            print(f'Scheduled: DeepChat restart at {start.strftime("%H:%M:%S")} '
                  f'(task {TASK_NAME})')
            return True
        print(f'schtasks failed: {r.stderr.strip()[:200]}')
    except Exception as e:
        print(f'schtasks ERR: {e}')

    # Fallback: XML import
    xml = TASK_XML.format(start=start_str, user=user,
                          python=get_python(), script=script)
    xml_path = os.path.join(os.environ.get('TEMP', '.'), 'dc-restart-task.xml')
    with open(xml_path, 'w', encoding='utf-16') as f:
        f.write(xml)
    r = subprocess.run(['schtasks', '/create', '/tn', TASK_NAME,
                        '/xml', xml_path, '/f'],
                       capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        print(f'Scheduled (XML): DeepChat restart at {start.strftime("%H:%M:%S")}')
        return True
    print(f'XML import failed: {r.stderr.strip()[:200]}')
    print('FALLBACK: tell the user to restart DeepChat manually at their convenience.')
    return False


def main():
    ap = argparse.ArgumentParser(description='Schedule deferred DeepChat restart')
    ap.add_argument('--delay', type=int, default=60,
                    help='delay in seconds before restart (default 60)')
    args = ap.parse_args()
    ok = schedule(max(0, args.delay))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
