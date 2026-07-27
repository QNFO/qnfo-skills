#!/usr/bin/env python3
"""Stop and disable bloatware services. Handles auto-recovery disable.
v2.0 — 2026-07-27 KAIZEN: reset=0 → reset=86400 (KIF-30 drift fix),
sc.exe explicit (KIF-05 armoring), UTF-8 I/O, post-disable verification.
REQUIRES ADMINISTRATOR PRIVILEGES (elevated terminal)."""
import subprocess, sys, time

# Services to disable (stop + startup=disabled + remove recovery)
BLOAT_SERVICES = [
    # Windows Search
    "WSearch",
    # Performance (useless on SSD)
    "SysMain",
    # Telemetry
    "DiagTrack",
    # Push notifications
    "WpnService",
    # Data usage collection
    "DusmSvc",
    # Connected devices platform (Phone Link)
    "CDPSvc",
    # Print spooler (if no printer)
    "Spooler",
    # Office click-to-run
    "ClickToRunSvc",
    # Program compatibility assistant
    "PcaSvc",
    # Windows image acquisition (scanners)
    "StiSvc",
    # Font cache
    "FontCache",
    # Lenovo bloat
    "LITSSVC",
    "LenovoFnAndFunctionKeys",
    "PC Manager Service Store",
    # Dolby audio bloat
    "DolbyDAXAPI",
    "ElevocService",
]

def run_sc(args):
    """Run sc.exe with utf-8 encoding (KIF-27)."""
    return subprocess.run(
        ["sc.exe"] + args,
        capture_output=True, encoding="utf-8", errors="replace", timeout=15
    )

def verify_recovery(name):
    """Post-disable check: verify sc.exe failure actions are cleared."""
    r = run_sc(["qfailure", name])
    if "FAILURE_ACTIONS" in (r.stdout or "") and "NONE" not in (r.stdout or "").upper():
        return False
    return True

def disable_service(name):
    """Stop service, set startup=disabled, remove failure recovery actions.
    Uses sc.exe (NOT bare sc) to avoid PowerShell alias trap (KIF-05).
    reset=86400 (1 day) per v2.0 kaizen (KIF-30 — was incorrectly reset=0)."""
    results = []
    found = True

    # Step 0: Check if service exists
    r = run_sc(["query", name])
    if "FAILED" in (r.stdout or "") and "1060" in (r.stdout or ""):
        results.append(f"stop: SKIP (not found)")
        results.append(f"disabled: SKIP (not found)")
        results.append(f"recovery: SKIP (not found)")
        return "; ".join(results), False

    # Step 1: Stop
    r = run_sc(["stop", name])
    if "FAILED" in (r.stdout or "") and "not started" not in (r.stdout or "").lower():
        results.append(f"stop: FAILED")
    else:
        results.append("stop: OK")
    time.sleep(0.5)

    # Step 2: Disable startup (note: space after "start=" is MANDATORY for sc.exe)
    r = run_sc(["config", name, "start=", "disabled"])
    if "SUCCESS" in (r.stdout or ""):
        results.append("disabled: OK")
    else:
        results.append("disabled: SKIP (may need admin)")
    time.sleep(0.3)

    # Step 3: Remove auto-recovery actions (critical for stubborn services)
    # KIF-30 FIX (2026-07-27): reset=86400 (1 day), was reset=0 (immediate)
    # KIF-05 ARMORING: use sc.exe, separate args with space after "="
    r = run_sc(["failure", name, "reset=", "86400", "actions=", ""])
    if "SUCCESS" in (r.stdout or ""):
        # Verify it actually cleared
        if verify_recovery(name):
            results.append("recovery: CLEARED")
        else:
            results.append("recovery: WARN (clear cmd succeeded but verify shows recovery still present)")
    else:
        results.append("recovery: SKIP")

    return "; ".join(results), True

def main():
    success = []
    failed = []
    skipped = []

    for svc in BLOAT_SERVICES:
        print(f"  {svc:<35}", end=" ", flush=True)
        result, found = disable_service(svc)
        print(result)
        if not found:
            skipped.append(svc)
        elif "disabled: OK" in result:
            success.append(svc)
        else:
            failed.append(svc)

    print(f"\nSuccessfully disabled: {len(success)}/{len(BLOAT_SERVICES)}")
    if skipped:
        print(f"Not found (already removed): {', '.join(skipped)}")
    if failed:
        print(f"Need admin for: {', '.join(failed)}")

    return success, failed

if __name__ == "__main__":
    main()
