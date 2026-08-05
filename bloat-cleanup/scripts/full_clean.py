#!/usr/bin/env python3
"""Full system bloat cleanup orchestrator. Runs all cleanup phases in sequence.
v2.4 — 2026-07-29 KAIZEN: added Defender exclusions, AppX removal, agent DB prune,
quick optimize, system tune phases. 10-phase full cleanup superset."""
import sys, os, time

def phase(script_name, args=None, timeout=300):
    """Run a script and check exit code."""
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(skill_root, "scripts", script_name)
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)

    print(f"\n{'='*60}")
    print(f"PHASE: {script_name}")
    print(f"{'='*60}")

    import subprocess
    r = subprocess.run(cmd, capture_output=False, text=True, timeout=timeout)
    return r.returncode == 0

def run_ps(script_name, timeout=300):
    """Run a PowerShell script from the scripts directory."""
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(skill_root, "scripts", script_name)

    print(f"\n{'='*60}")
    print(f"PHASE: {script_name}")
    print(f"{'='*60}")

    import subprocess
    r = subprocess.run(
        ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', script_path],
        capture_output=False, text=True, timeout=timeout
    )
    return r.returncode == 0

def main():
    started = time.time()

    print("=" * 60)
    print("  DEEPCHAT SYSTEM CLEANUP — FULL ORCHESTRATOR v2.4")
    print(f"  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Phase 1: System Audit (read-only, always first)
    print("\n>>> PHASE 1: System Audit")
    phase("audit_system.py")

    # Phase 2: Dynamic service audit (KIF-40)
    print("\n>>> PHASE 2: Dynamic Service Analysis")
    phase("audit_services.py")

    # Phase 3: Kill bloat processes
    print("\n>>> PHASE 3: Kill Bloatware Processes")
    phase("kill_bloat.py")

    # Phase 4: Stop + disable services (legacy fixed list)
    print("\n>>> PHASE 4: Disable Bloatware Services (legacy fixed list)")
    phase("disable_services.py")

    # Phase 5: Defender exclusions (v2.4 — new)
    print("\n>>> PHASE 5: Defender Exclusions for DeepChat")
    phase("defender_exclusions.py")

    # Phase 6: Remove AppX bloatware (v2.4 — new)
    print("\n>>> PHASE 6: Remove AppX Bloatware Packages")
    phase("remove_appx.py")

    # Phase 7: Clean disk caches
    print("\n>>> PHASE 7: Clean Disk Caches & Temp Files")
    phase("clean_disk.py")

    # Phase 8: Agent DB prune (v2.4 — new, needs DeepChat closed for VACUUM)
    print("\n>>> PHASE 8: Prune Old DeepChat Sessions")
    phase("agent_db_prune.py")

    # Phase 9: Thin-client enforcement
    print("\n>>> PHASE 9: DeepChat Thin-Client Compliance")
    phase("thin_client.py", ["--clean"])

    # Phase 10: Final audit
    print("\n>>> PHASE 10: Post-Cleanup Verification")
    phase("audit_system.py")

    # Final disk report
    import shutil
    elapsed = time.time() - started
    print(f"\n{'='*60}")
    print(f"  CLEANUP COMPLETE — {elapsed:.1f}s elapsed")
    print(f"{'='*60}")

    for drive in ["C:", "D:"]:
        try:
            t, u, f = shutil.disk_usage(drive)
            print(f"  {drive} Free: {f/1073741824:.1f} GB / {t/1073741824:.1f} GB ({f/t*100:.1f}%)")
        except:
            pass

if __name__ == "__main__":
    main()
