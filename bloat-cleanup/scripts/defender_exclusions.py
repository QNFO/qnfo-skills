#!/usr/bin/env python3
"""Add Windows Defender exclusions for DeepChat paths and process.
v1.0 — 2026-07-29: extracted from proven defender_appx_cleanup.ps1 pattern.

Adds path exclusions for .deepchat, AppData\Local\Programs\DeepChat,
AppData\Roaming\DeepChat, and process exclusion for DeepChat.exe.
Skips paths already excluded. Requires Administrator privileges.

Usage:
    python defender_exclusions.py
    python defender_exclusions.py --verify-only
"""
import os, sys, subprocess, re

DEEPCHAT_PATHS = [
    os.path.expandvars(r'%USERPROFILE%\.deepchat'),
    os.path.expandvars(r'%LOCALAPPDATA%\Programs\DeepChat'),
    os.path.expandvars(r'%APPDATA%\DeepChat'),
]

DEEPCHAT_PROCESSES = [
    os.path.expandvars(r'%LOCALAPPDATA%\Programs\DeepChat\DeepChat.exe'),
]

def is_admin():
    try:
        return subprocess.run(
            ['powershell', '-NoProfile', '-Command',
             '([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)'],
            capture_output=True, text=True, timeout=10
        ).stdout.strip() == 'True'
    except:
        return False

def get_existing_exclusions():
    """Return (paths, processes) already excluded."""
    r = subprocess.run(
        ['powershell', '-NoProfile', '-Command',
         '(Get-MpPreference).ExclusionPath -join "|||"; (Get-MpPreference).ExclusionProcess -join "|||"'],
        capture_output=True, text=True, timeout=15
    )
    parts = r.stdout.strip().split('|||')
    existing_paths = [p for p in parts[0].split('\n') if p.strip()] if parts else []
    existing_procs = [p for p in parts[1].split('\n') if p.strip()] if len(parts) > 1 else []
    return existing_paths, existing_procs

def add_exclusion_path(path):
    r = subprocess.run(
        ['powershell', '-NoProfile', '-Command',
         f'Add-MpPreference -ExclusionPath "{path}"'],
        capture_output=True, text=True, timeout=10
    )
    return r.returncode == 0

def add_exclusion_process(proc):
    r = subprocess.run(
        ['powershell', '-NoProfile', '-Command',
         f'Add-MpPreference -ExclusionProcess "{proc}"'],
        capture_output=True, text=True, timeout=10
    )
    return r.returncode == 0

def main():
    verify_only = '--verify-only' in sys.argv or '-v' in sys.argv

    print("=== Defender Exclusions for DeepChat ===")
    print()

    if not is_admin():
        print("[ERROR] Administrator privileges required.")
        print("Run from an elevated PowerShell or Command Prompt.")
        sys.exit(1)

    existing_paths, existing_procs = get_existing_exclusions()
    print(f"Existing path exclusions: {len(existing_paths)}")
    print(f"Existing process exclusions: {len(existing_procs)}")
    print()

    paths_added = 0
    paths_skipped = 0

    for path in DEEPCHAT_PATHS:
        if not os.path.exists(path):
            print(f"  [SKIP] Not found: {path}")
            continue
        if path in existing_paths:
            print(f"  [SKIP] Already excluded: {path}")
            paths_skipped += 1
            continue
        if verify_only:
            print(f"  [WOULD ADD] {path}")
            paths_added += 1
            continue
        ok = add_exclusion_path(path)
        status = "ADDED" if ok else "FAILED"
        print(f"  [{status}] {path}")
        if ok:
            paths_added += 1

    procs_added = 0
    procs_skipped = 0

    for proc in DEEPCHAT_PROCESSES:
        if proc in existing_procs:
            print(f"  [SKIP] Already excluded process: {proc}")
            procs_skipped += 1
            continue
        if verify_only:
            print(f"  [WOULD ADD] Process: {proc}")
            procs_added += 1
            continue
        ok = add_exclusion_process(proc)
        status = "ADDED" if ok else "FAILED"
        print(f"  [{status}] Process: {proc}")
        if ok:
            procs_added += 1

    print()
    mode = "[DRY RUN] " if verify_only else ""
    print(f"{mode}Paths: {paths_added} added, {paths_skipped} already excluded")
    print(f"{mode}Processes: {procs_added} added, {procs_skipped} already excluded")

    if verify_only:
        print()
        print("Use without --verify-only to apply changes.")

if __name__ == "__main__":
    main()
