#!/usr/bin/env python3
"""Kill bloatware processes with anti-restart retry logic.
v1.1 — 2026-07-27 KAIZEN: sc → sc.exe (KIF-05), reset=0 → reset=86400 (KIF-30 drift fix),
UTF-8 I/O (KIF-27). Still uses a fixed process list (audit_services.py provides
dynamic service discovery)."""
import subprocess, sys, time

BLOAT_PROCESSES = [
    "SearchHost", "SearchApp", "SearchIndexer",
    "OfficeClickToRun", "SDXHelper",
    "MSPCManagerService",
    "GoogleDriveFS", "utweb", "uTorrent",
    "Claude", "Widgets", "WidgetService",
    "CrossDeviceService", "OneNote", "ONENOTEM",
    "SecurityHealthSystray", "LockApp", "TextInputHost",
    "StartMenuExperienceHost",
]

def kill_process(name, retries=3):
    """Force-kill a process with retry."""
    for attempt in range(retries):
        r = subprocess.run(["taskkill", "/f", "/im", f"{name}.exe"],
                          capture_output=True, text=True, timeout=5)
        if "SUCCESS" in r.stdout:
            return True, f"KILLED (attempt {attempt+1})"
        time.sleep(1)
    return False, "FAILED after retries"

def main():
    killed = []
    missed = []

    for proc in BLOAT_PROCESSES:
        # First check if running
        r = subprocess.run(["tasklist", "/fi", f"imagename eq {proc}.exe", "/fo", "csv", "/nh"],
                          capture_output=True, text=True, timeout=3)
        if proc not in r.stdout:
            print(f"  SKIP: {proc} (not running)")
            continue

        print(f"  KILLING: {proc}...", end=" ")
        ok, msg = kill_process(proc)
        if ok:
            killed.append(proc)
            print(msg)
        else:
            missed.append(proc)
            print(msg)

    print(f"\nKilled {len(killed)} processes, {len(missed)} resisted")

    # For stubborn ones that restarted, disable service
    stubborn_map = {
        "SearchHost": "WSearch",
        "SearchIndexer": "WSearch",
        "OfficeClickToRun": "ClickToRunSvc",
        "MSPCManagerService": "PC Manager Service Store",
    }

    for proc in missed:
        svc = stubborn_map.get(proc)
        if svc:
            print(f"  Attempting service-level kill for {proc} via {svc}...")
            # KIF-05: use sc.exe (NOT bare sc — PowerShell alias trap)
            subprocess.run(["sc.exe", "stop", svc],
                          capture_output=True, encoding="utf-8", errors="replace", timeout=10)
            # Note: space after "start=" is MANDATORY for sc.exe
            subprocess.run(["sc.exe", "config", svc, "start=", "disabled"],
                          capture_output=True, encoding="utf-8", errors="replace", timeout=10)
            # KIF-30: reset=86400 (1 day), not reset=0 (immediate)
            subprocess.run(["sc.exe", "failure", svc, "reset=", "86400", "actions=", ""],
                          capture_output=True, encoding="utf-8", errors="replace", timeout=5)
            # Try kill again
            ok, msg = kill_process(proc, retries=1)
            print(f"    {msg}")

    return killed, missed

if __name__ == "__main__":
    main()
