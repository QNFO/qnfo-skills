#!/usr/bin/env python3
"""Remove known bloatware AppX packages from Windows.
v1.0 — 2026-07-29.

Removes both user-installed and provisioned AppX packages for known
bloatware (Xbox, Bing, Widgets, YourPhone, GetHelp, etc.).
Requires Administrator privileges for provisioned package removal.

Usage:
    python remove_appx.py
    python remove_appx.py --dry-run
    python remove_appx.py --aggressive  (includes more packages)
"""
import subprocess, sys, os

# High-confidence bloatware — safe to remove
BLOAT_PACKAGES = [
    "Microsoft.XboxGameOverlay",
    "Microsoft.XboxGamingOverlay",
    "Microsoft.XboxIdentityProvider",
    "Microsoft.BingSearch",
    "Microsoft.WidgetsPlatformRuntime",
    "Microsoft.YourPhone",
    "Microsoft.GetHelp",
    "Microsoft.StartExperiencesApp",
    "Microsoft.Windows.DevHome",
    "MicrosoftWindows.CrossDevice",
    "Microsoft.MicrosoftPCManager",
    "Microsoft.ApplicationCompatibilityEnhancements",
]

# Additional packages removed only with --aggressive
AGGRESSIVE_PACKAGES = [
    "Microsoft.BingWeather",
    "Microsoft.BingNews",
    "Microsoft.MicrosoftOfficeHub",
    "Microsoft.MicrosoftSolitaireCollection",
    "Microsoft.MixedReality.Portal",
    "Microsoft.Office.OneNote",
    "Microsoft.People",
    "Microsoft.SkypeApp",
    "Microsoft.Wallet",
    "Microsoft.ZuneMusic",
    "Microsoft.ZuneVideo",
    "Microsoft.WindowsCamera",
]

# NEVER remove these — critical system components
SAFELIST = [
    "Microsoft.SecHealthUI",
    "Microsoft.WindowsStore",
    "Microsoft.DesktopAppInstaller",
    "Microsoft.WindowsTerminal",
    "Microsoft.PowerShell",
    "Microsoft.WindowsNotepad",
    "Microsoft.ScreenSketch",
    "Microsoft.WindowsCalculator",
    "Microsoft.StorePurchaseApp",
    "Microsoft.Winget.Source",
]


def run_ps(command):
    r = subprocess.run(
        ['powershell', '-NoProfile', '-Command', command],
        capture_output=True, text=True, timeout=30
    )
    return r.returncode == 0, r.stdout.strip(), r.stderr.strip()

def remove_user_package(name):
    ok, out, err = run_ps(
        f'$p = Get-AppxPackage -Name "{name}" -ErrorAction SilentlyContinue; '
        f'if ($p) {{ Remove-AppxPackage -Package $p.PackageFullName; Write-Host $p.PackageFullName }} '
        f'else {{ Write-Host "NOT_FOUND" }}'
    )
    return ok, out

def remove_provisioned_package(name):
    ok, out, err = run_ps(
        f'$p = Get-AppxProvisionedPackage -Online | Where-Object {{ $_.DisplayName -like "*{name}*" }}; '
        f'if ($p) {{ Remove-AppxProvisionedPackage -Online -PackageName $p.PackageName; Write-Host $p.PackageName }} '
        f'else {{ Write-Host "NOT_FOUND" }}'
    )
    return ok, out

def is_admin():
    try:
        return subprocess.run(
            ['powershell', '-NoProfile', '-Command',
             '([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)'],
            capture_output=True, text=True, timeout=10
        ).stdout.strip() == 'True'
    except:
        return False

def main():
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    aggressive = '--aggressive' in sys.argv or '-a' in sys.argv

    packages = BLOAT_PACKAGES.copy()
    if aggressive:
        packages.extend(AGGRESSIVE_PACKAGES)

    print("=== AppX Bloatware Removal ===")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}{' (AGGRESSIVE)' if aggressive else ''}")
    print(f"Targets: {len(packages)} packages")
    print()

    admin = is_admin()
    if not admin:
        print("[WARN] Not running as Administrator.")
        print("  User packages: can remove")
        print("  Provisioned packages: SKIP (requires admin)")
        print()

    removed_user = 0
    removed_prov = 0
    not_found = 0
    failed = 0
    skipped_prov = 0

    for pkg in packages:
        if pkg in SAFELIST:
            print(f"  [SAFELIST] {pkg} — skipped")
            continue

        if dry_run:
            print(f"  [DRY RUN] Would remove: {pkg}")
            continue

        # Step 1: Remove user package
        ok, out = remove_user_package(pkg)
        if not ok:
            print(f"  [FAILED] {pkg} (user)")
            failed += 1
            continue
        if 'NOT_FOUND' in out:
            print(f"  [NOT FOUND] {pkg} (user)")
            not_found += 1
        else:
            print(f"  [REMOVED] {pkg} (user: {out})")
            removed_user += 1

        # Step 2: Remove provisioned package (prevents reinstall)
        if not admin:
            print(f"  [SKIP] {pkg} (provisioned — needs admin)")
            skipped_prov += 1
            continue
        ok, out = remove_provisioned_package(pkg)
        if ok and 'NOT_FOUND' not in out:
            print(f"  [REMOVED] {pkg} (provisioned: {out})")
            removed_prov += 1

    print()
    print(f"User packages removed: {removed_user}")
    print(f"Provisioned packages removed: {removed_prov}")
    print(f"Not found: {not_found}")
    print(f"Skipped (provisioned, no admin): {skipped_prov}")
    print(f"Failed: {failed}")

    if skipped_prov > 0:
        print()
        print("[TIP] Run as Administrator to also remove provisioned packages.")
        print("      Provisioned packages can reinstall for new user accounts.")

if __name__ == "__main__":
    main()
