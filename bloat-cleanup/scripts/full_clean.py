#!/usr/bin/env python3
"""Full system bloat cleanup orchestrator. Runs all cleanup phases in sequence."""
import sys, os, time

def phase(script_name, args=None):
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
    r = subprocess.run(cmd, capture_output=False, text=True, timeout=120)
    return r.returncode == 0

def main():
    started = time.time()

    print("=" * 60)
    print("  DEEPCHAT SYSTEM CLEANUP — FULL ORCHESTRATOR")
    print(f"  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Phase 1: Audit
    print("\n>>> PHASE 1: System Audit")
    phase("audit_system.py")

    # Phase 2: Kill bloat processes
    print("\n>>> PHASE 2: Kill Bloatware Processes")
    phase("kill_bloat.py")

    # Phase 3: Stop + disable services
    print("\n>>> PHASE 3: Disable Bloatware Services")
    phase("disable_services.py")

    # Phase 4: Clean disk caches
    print("\n>>> PHASE 4: Clean Disk Caches & Temp Files")
    phase("clean_disk.py")

    # Phase 5: Thin-client enforcement
    print("\n>>> PHASE 5: DeepChat Thin-Client Compliance")
    phase("thin_client.py", ["--clean"])

    # Phase 6: Final audit
    print("\n>>> PHASE 6: Post-Cleanup Verification")
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
