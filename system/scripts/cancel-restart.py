#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cancel-restart.py — Cancel a pending DeepChat auto-restart (2026-08-02)

Cancels the one-shot restart task created by schedule-restart.py.
Safe to run anytime; no-op if no task is pending.

USAGE:
  python cancel-restart.py
"""
import subprocess, sys

TASK_NAME = 'DeepChat-AutoRestart'


def main():
    r = subprocess.run(['schtasks', '/delete', '/tn', TASK_NAME, '/f'],
                       capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        print(f'Cancelled pending restart task: {TASK_NAME}')
    else:
        print(f'No pending restart task (or already fired): {TASK_NAME}')
    sys.exit(0)


if __name__ == '__main__':
    main()
