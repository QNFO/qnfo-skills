#!/usr/bin/env python3
"""Kill bloatware processes with anti-restart retry logic."""
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
            subprocess.run(["sc", "stop", svc], capture_output=True, timeout=10)
            subprocess.run(["sc", "config", svc, "start=disabled"], capture_output=True, timeout=10)
            # Disable auto-recovery
            subprocess.run(["sc", "failure", svc, "reset=0", "actions="], capture_output=True, timeout=5)
            # Try kill again
            ok, msg = kill_process(proc, retries=1)
            print(f"    {msg}")

    return killed, missed

if __name__ == "__main__":
    main()
