#!/usr/bin/env python3
"""Dynamic service disabling — runtime target generation + apply.
Consumes heuristic classification from audit_services.py (or runs inline)
to generate a dynamic target list, then stops + disables + clears recovery.

MODES:
  --dry-run  (default): Show what WOULD be disabled, make no changes.
  --apply --confirm:   Actually stop + disable + clear recovery.
                        REQUIRES ADMINISTRATOR PRIVILEGES.

v1.0 — 2026-07-27 KAIZEN: replaces hardcoded BLOAT_SERVICES list from
disable_services.py with dynamic runtime target generation. KIF-40.
sc.exe with reset=86400 (KIF-30), UTF-8 I/O (KIF-27)."""

import json, os, subprocess, sys, time, argparse

# ── DYNAMIC TARGET GENERATION ───────────────────────────────────────────

# These patterns-in-name trigger auto-targeting (high confidence bloat).
# Same as audit_services.py BLOAT_PATTERNS but as simple name matchers.
BLOAT_NAME_PATTERNS = [
    # Vendor
    "lenovo", "dolby", "elevoc",
    # Windows Search / Indexing
    "wsearch", "searchindexer", "searchhost",
    # Telemetry & data
    "diagtrack", "dusmsvc", "wpnservice", "wpnuser",
    # Connected devices
    "cdpsvc", "cdpuser",
    # Compatibility
    "pcasvc",
    # Image acquisition
    "stisvc",
    # Font cache (legacy — FontCache3.0.0.0 is separate)
    "fontcache",
    # Office
    "clicktorunsvc", "clicktorun", "sdxhelper",
    # Xbox
    "xbox", "xbl",
    # OneDrive
    "onedrive",
    # Adobe auto-updaters
    "adobeupdate", "adobearmservice", "adobe_acrobat_update", "agsservice",
    # Google updaters
    "googleupdate", "googleupdater", "gupdate", "gupdatem",
    # Lenovo PC Manager
    "pc manager", "mspcmanagerservice",
]

# These services are NEVER disabled, even if they match a pattern above.
# (Extra safety net beyond what audit_services.py classifies as essential.)
NEVER_DISABLE = {
    "RpcSs", "DcomLaunch", "RpcEptMapper", "SamSs", "EventLog",
    "PlugPlay", "Power", "BFE", "MpsSvc", "WinDefend", "WdNisSvc",
    "wuauserv", "CryptSvc", "KeyIso", "VaultSvc", "Schedule",
    "LanmanWorkstation", "LanmanServer", "DHCP", "DNScache", "Dnscache",
    "netprofm", "NlaSvc", "W32Time", "TrustedInstaller",
    "Winmgmt", "gpsvc", "iphlpsvc", "spoolsv", "ShellHWDetection",
    "AudioSrv", "AudioEndpointBuilder", "BrokerInfrastructure",
    "CoreMessagingRegistrar", "StateRepository", "UserManager",
    "ProfSvc", "SENS", "Themes", "StorSvc", "DPS",
    "DisplayEnhancementService", "WdiServiceHost", "WdiSystemHost",
}


def query_all_services():
    """Query all services via Get-CimInstance Win32_Service."""
    ps_cmd = (
        "Get-CimInstance Win32_Service | "
        "Select-Object Name, DisplayName, State, StartMode, ProcessId | "
        "ConvertTo-Json -Compress"
    )
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_cmd],
        capture_output=True, encoding="utf-8", errors="replace", timeout=30
    )
    if r.returncode != 0 or not r.stdout.strip():
        return []
    data = json.loads(r.stdout.strip())
    return [data] if isinstance(data, dict) else data


def generate_targets(services, include_suspicious=False):
    """Dynamically generate a target list from all services.
    Matches BLOAT_NAME_PATTERNS against service name + display name,
    excludes NEVER_DISABLE, and optionally includes suspicious patterns."""
    targets = []
    reasons = []

    for svc in services:
        name = (svc.get("Name") or "").strip()
        display = (svc.get("DisplayName") or "").strip()

        # Safety: never touch critical OS services
        if name in NEVER_DISABLE:
            continue

        combined = f"{name.lower()} {display.lower()}"

        # Match bloat patterns
        for pattern in BLOAT_NAME_PATTERNS:
            if pattern in combined:
                targets.append(svc)
                reasons.append(f"pattern:{pattern}")
                break

        # Optionally include suspicious (auto-start 3rd-party, not in NEVER_DISABLE)
        if include_suspicious and svc not in targets:
            start_mode = (svc.get("StartMode") or "").strip()
            state = (svc.get("State") or "").strip()
            if start_mode == "Auto" and state == "Running":
                if "microsoft" not in display.lower() and "windows" not in display.lower():
                    targets.append(svc)
                    reasons.append("suspicious:third-party-auto-start")

    return targets, reasons


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
    """Stop, disable startup, clear auto-recovery for a single service.
    Uses sc.exe with reset=86400 (KIF-30). Returns (success: bool, detail: str)."""
    results = []

    # Check if service exists
    r = run_sc(["query", name])
    if "FAILED" in (r.stdout or "") and "1060" in (r.stdout or ""):
        return False, "not found"

    # Stop
    r = run_sc(["stop", name])
    if "FAILED" in (r.stdout or "") and "not started" not in (r.stdout or "").lower():
        results.append("stop:FAIL")
    else:
        results.append("stop:OK")
    time.sleep(0.5)

    # Disable startup
    r = run_sc(["config", name, "start=", "disabled"])
    if "SUCCESS" in (r.stdout or ""):
        results.append("disabled:OK")
    else:
        results.append("disabled:FAIL (need admin?)")

    # Clear auto-recovery (KIF-30: reset=86400, KIF-05: sc.exe)
    r = run_sc(["failure", name, "reset=", "86400", "actions=", ""])
    if "SUCCESS" in (r.stdout or ""):
        if verify_recovery(name):
            results.append("recovery:CLEARED")
        else:
            results.append("recovery:WARN")
    else:
        results.append("recovery:SKIP")

    return True, "; ".join(results)


def is_admin():
    """Check if running with administrator privileges."""
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "(New-Object Security.Principal.WindowsPrincipal "
             "[Security.Principal.WindowsIdentity]::GetCurrent()"
             ").IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)"],
            capture_output=True, encoding="utf-8", timeout=5
        )
        return "True" in r.stdout
    except:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Dynamic service disabling — runtime target generation"
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Actually disable services (requires --confirm)"
    )
    parser.add_argument(
        "--confirm", action="store_true",
        help="Confirm that you want to apply changes"
    )
    parser.add_argument(
        "--include-suspicious", action="store_true",
        help="Also target suspicious third-party auto-start services"
    )
    parser.add_argument(
        "--dry-run", action="store_true", default=True,
        help="Show what would be disabled without making changes (default)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output targets as JSON (for programmatic consumption)"
    )
    args = parser.parse_args()

    # ── Discover services ──
    print("=" * 72)
    print("  DYNAMIC SERVICE DISABLER")
    print("=" * 72)
    print()

    print("Discovering services... ", end="", flush=True)
    services = query_all_services()
    if not services:
        print("FAILED")
        return 1
    print(f"{len(services)} found")

    # ── Generate targets ──
    targets, reasons = generate_targets(services, args.include_suspicious)

    if not targets:
        print("\nNo bloat services detected. System is already clean!")
        return 0

    print(f"\nDynamic target list: {len(targets)} services")
    print()

    # ── Show targets ──
    for i, (svc, reason) in enumerate(zip(targets, reasons), 1):
        name = svc.get("Name", "?")
        display = svc.get("DisplayName", "")
        state = svc.get("State", "?")
        start = svc.get("StartMode", "?")
        running = "RUNNING" if state == "Running" else "STOPPED"
        print(f"  [{i:>2}] {name:<45} [{running:>7}] [{start:<8}] {reason}")
        if display and display != name:
            print(f"       {display}")

    # ── Summary ──
    running_targets = [s for s in targets if s.get("State") == "Running"]
    stopped_targets = [s for s in targets if s.get("State") != "Running"]
    print(f"\n  Running targets:  {len(running_targets)}")
    print(f"  Stopped targets:  {len(stopped_targets)}")
    print()

    # ── JSON output mode ──
    if args.json:
        output = [{
            "name": svc.get("Name"),
            "display": svc.get("DisplayName"),
            "state": svc.get("State"),
            "start_mode": svc.get("StartMode"),
            "reason": reason,
        } for svc, reason in zip(targets, reasons)]
        print(json.dumps(output, indent=2))
        return 0

    # ── Dry-run: just show, don't act ──
    if not args.apply:
        print("── DRY RUN — no changes made ──")
        print("To apply these changes (requires administrator privileges):")
        print("  skill_run bloat-cleanup scripts/dynamic_disable.py --apply --confirm")
        if args.include_suspicious:
            print("    (with --include-suspicious to also target third-party auto-start)")
        return 0

    # ── Apply mode ──
    if not args.confirm:
        print("ERROR: --apply requires --confirm for safety.", file=sys.stderr)
        print("  skill_run bloat-cleanup scripts/dynamic_disable.py --apply --confirm")
        return 1

    if not is_admin():
        print("\n⚠️  ADMINISTRATOR PRIVILEGES REQUIRED", file=sys.stderr)
        print("This script must be run from an elevated terminal.", file=sys.stderr)
        print("To run as admin:", file=sys.stderr)
        print(f'  python "{__file__}" --apply --confirm', file=sys.stderr)
        return 1

    print("── APPLYING CHANGES ──")
    print()

    success = []
    failed = []

    for svc, reason in zip(targets, reasons):
        name = svc.get("Name")
        print(f"  {name:<45} ", end="", flush=True)
        ok, detail = disable_service(name)
        print(detail)
        if ok:
            success.append(name)
        else:
            failed.append(name)

    print(f"\n── RESULTS ──")
    print(f"  Disabled: {len(success)}/{len(targets)}")
    if failed:
        print(f"  Failed:   {len(failed)}")
        for f in failed:
            print(f"    - {f}")
    print()

    # Per-service verification
    if success:
        print("── POST-DISABLE VERIFICATION ──")
        for name in success:
            v = verify_recovery(name)
            status = "✓ CLEAN" if v else "✗ RECOVERY STILL PRESENT"
            print(f"  {name:<45} {status}")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
