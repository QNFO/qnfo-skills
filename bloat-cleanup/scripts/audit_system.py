#!/usr/bin/env python3
"""Full system audit: disk space, processes, services, startup items, thin-client compliance."""
import os, shutil, subprocess, sys, time
from collections import defaultdict

def dir_size(path):
    if not os.path.exists(path): return 0, 0
    total, fc = 0, 0
    if os.path.isfile(path):
        try: return os.path.getsize(path), 1
        except: return 0, 0
    try:
        for r, ds, fs in os.walk(path):
            for f in fs:
                try: total += os.path.getsize(os.path.join(r, f)); fc += 1
                except: pass
    except: pass
    return total, fc

def check(path, label, report):
    sz, fc = dir_size(path)
    if sz > 0:
        report.append({"label": label, "path": path, "size_mb": round(sz/1048576, 1), "files": fc})
    return sz

def main():
    report = {"disk": [], "processes": [], "services": [], "startup": [], "thin_client": [], "other": []}
    user = os.environ["USERPROFILE"]
    local = os.environ.get("LOCALAPPDATA", os.path.join(user, "AppData", "Local"))
    now = time.time()

    # === DISK AUDIT ===
    print("=== DISK AUDIT ===")
    for drive in ["C:", "D:", "G:"]:
        try:
            t, u, f = shutil.disk_usage(drive)
            report["disk"].append({"drive": drive, "free_gb": round(f/1073741824, 1),
                                    "total_gb": round(t/1073741824, 1), "pct_free": round(f/t*100, 1)})
            print(f"  {drive} Free={f/1073741824:.1f} GB ({f/t*100:.1f}%)")
        except: pass

    # Cleanable paths
    cleanable = [
        (r"C:\hiberfil.sys", "Hibernation file"),
        (r"C:\Windows\Temp", "Windows Temp"),
        (r"C:\Windows\Prefetch", "Prefetch"),
        (r"C:\Windows\SoftwareDistribution\Download", "Windows Update cache"),
        (r"C:\Windows\Logs\CBS", "CBS Logs"),
        (r"C:\$Recycle.Bin", "Recycle Bin"),
        (os.path.join(local, "Temp"), "User Temp"),
        (os.path.join(local, "npm-cache"), "npm cache"),
        (os.path.join(user, ".npm"), ".npm cache"),
        (os.path.join(user, "AppData", "Roaming", "Code", "CachedData"), "VS Code CachedData"),
        (os.path.join(user, "AppData", "Roaming", "Code", "CachedExtensionVSIXs"), "VS Code Ext VSIXs"),
        (os.path.join(user, "AppData", "Roaming", "Code", "Cache"), "VS Code Cache"),
        (os.path.join(local, "Google", "Chrome", "User Data", "Default", "Code Cache"), "Chrome Code Cache"),
        (os.path.join(local, "Google", "Chrome", "User Data", "Default", "Service Worker"), "Chrome SW Cache"),
        (os.path.join(local, "Google", "Chrome", "User Data", "GrShaderCache"), "Chrome GPU Shader"),
        (os.path.join(local, "Google", "Chrome", "User Data", "ShaderCache"), "Chrome Shader"),
        (os.path.join(local, "Microsoft", "Edge", "User Data", "Default", "Code Cache"), "Edge Code Cache"),
        (os.path.join(local, "Microsoft", "Edge", "User Data", "ShaderCache"), "Edge Shader"),
        (os.path.join(user, "AppData", "Local", "Microsoft", "Windows", "Explorer"), "Explorer Thumbnails"),
        (os.path.join(user, "AppData", "Local", "Microsoft", "Office", "OTele"), "Office Telemetry"),
        (os.path.join(local, "PC Manager Store"), "PC Manager Store"),
        (os.path.join(local, "pip"), "pip cache"),
        (os.path.join(user, "AppData", "Local", "D3DSCache"), "D3D Shader Cache"),
        (os.path.join(user, "AppData", "Roaming", "discord", "Cache"), "Discord Cache"),
    ]

    # TexLive docs/source
    for d in ["doc", "source"]:
        cleanable.append((os.path.join(r"c:\texlive\2025\texmf-dist", d), f"TexLive {d}/"))

    # Crash dumps
    for p in [r"C:\Windows\Minidump", r"C:\Windows\MEMORY.DMP",
              os.path.join(local, "CrashDumps")]:
        if os.path.exists(p):
            cleanable.append((p, "Crash Dump/" + os.path.basename(p)))

    grand = 0
    for path, label in cleanable:
        grand += check(path, label, report["disk"])

    # === DEEPCHAT SESSIONS ===
    print("=== DEEPCHAT SESSIONS ===")
    sessions_dir = os.path.join(user, ".deepchat", "sessions")
    if os.path.exists(sessions_dir):
        total_sessions = 0
        total_size = 0
        for d in os.listdir(sessions_dir):
            dp = os.path.join(sessions_dir, d)
            if os.path.isdir(dp):
                sz = sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(dp) for f in fs)
                total_sessions += 1
                total_size += sz
        report["other"].append({"type": "deepchat_sessions", "count": total_sessions,
                                "total_mb": round(total_size/1048576, 1)})
        print(f"  Sessions: {total_sessions}, {total_size/1048576:.1f} MB")

    # === PROCESSES ===
    print("=== BLOATWARE PROCESSES ===")
    bloat_processes = [
        "SearchHost", "SearchIndexer", "SearchApp",
        "OfficeClickToRun", "SDXHelper",
        "MSPCManagerService",
        "GoogleDriveFS", "utweb", "uTorrent",
        "Claude", "Widgets", "WidgetService",
        "CrossDeviceService", "OneNote", "ONENOTEM",
        "SecurityHealthSystray", "LockApp",
    ]
    for proc in bloat_processes:
        r = subprocess.run(["tasklist", "/fi", f"imagename eq {proc}.exe", "/fo", "csv", "/nh"],
                          capture_output=True, text=True, timeout=5)
        if proc in r.stdout:
            report["processes"].append({"name": proc, "running": True})
            print(f"  RUNNING: {proc}")
        else:
            report["processes"].append({"name": proc, "running": False})

    # === SERVICES ===
    print("=== BLOATWARE SERVICES ===")
    bloat_services = [
        "WSearch", "SysMain", "DiagTrack", "WpnService", "DusmSvc", "CDPSvc",
        "Spooler", "ClickToRunSvc", "PcaSvc", "StiSvc", "FontCache",
        "LITSSVC", "LenovoFnAndFunctionKeys", "DolbyDAXAPI", "ElevocService",
        "PC Manager Service Store",
    ]
    for svc in bloat_services:
        try:
            r = subprocess.run(["sc", "query", svc], capture_output=True, text=True, timeout=5)
            running = "RUNNING" in r.stdout
            report["services"].append({"name": svc, "running": running})
            if running:
                print(f"  RUNNING: {svc}")
        except:
            pass

    # === STARTUP ITEMS ===
    print("=== STARTUP ITEMS ===")
    import winreg
    for hive_name, hive in [("HKCU", winreg.HKEY_CURRENT_USER), ("HKLM", winreg.HKEY_LOCAL_MACHINE)]:
        try:
            key = winreg.OpenKey(hive, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    report["startup"].append({"hive": hive_name, "name": name, "command": value[:100]})
                    print(f"  {hive_name}: {name}")
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except: pass

    # === THIN-CLIENT COMPLIANCE ===
    print("=== THIN-CLIENT COMPLIANCE ===")
    projects_dir = os.path.join(user, ".deepchat", "projects")
    violations = []
    if os.path.exists(projects_dir):
        for d in os.listdir(projects_dir):
            dp = os.path.join(projects_dir, d)
            if os.path.isdir(dp):
                sz = sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(dp) for f in fs)
                has_git = os.path.exists(os.path.join(dp, ".git"))
                violations.append({"path": d, "size_mb": round(sz/1048576, 1), "has_git": has_git})
                print(f"  VIOLATION: projects/{d} ({sz/1048576:.1f} MB) git={has_git}")

    report["thin_client"] = violations

    # === APPX BLOATWARE CHECK ===
    print("\n=== APPX BLOATWARE ===")
    appx_bloat = [
        "Microsoft.XboxGameOverlay", "Microsoft.XboxGamingOverlay",
        "Microsoft.XboxIdentityProvider", "Microsoft.BingSearch",
        "Microsoft.WidgetsPlatformRuntime", "Microsoft.YourPhone",
        "Microsoft.GetHelp", "Microsoft.StartExperiencesApp",
        "Microsoft.Windows.DevHome", "MicrosoftWindows.CrossDevice",
        "Microsoft.MicrosoftPCManager", "Microsoft.ApplicationCompatibilityEnhancements",
    ]
    appx_found = 0
    for pkg in appx_bloat:
        r = subprocess.run(
            ['powershell', '-NoProfile', '-Command',
             f'(Get-AppxPackage -Name "{pkg}" -ErrorAction SilentlyContinue).Count'],
            capture_output=True, text=True, timeout=10
        )
        try:
            count = int(r.stdout.strip() or '0')
        except:
            count = 0
        if count > 0:
            appx_found += 1
            print(f"  BLOAT: {pkg} ({count} installed)")
    report["other"].append({"type": "appx_bloat", "count": appx_found})
    print(f"  AppX bloat packages: {appx_found} installed")

    # === AGENT.DB SIZE ===
    agent_db = os.path.join(user, "AppData", "Roaming", "DeepChat", "app_db", "agent.db")
    if os.path.exists(agent_db):
        sz = os.path.getsize(agent_db)
        report["other"].append({"type": "agent_db", "size_mb": round(sz/1048576, 1)})
        print(f"\n  agent.db: {sz/1048576:.1f} MB")

    # === SUMMARY ===
    print(f"\n=== AUDIT SUMMARY ===")
    total_cleanable = sum(item.get("size_mb", 0) for item in report["disk"])
    running_procs = sum(1 for p in report["processes"] if p["running"])
    running_svcs = sum(1 for s in report["services"] if s["running"])
    startup_count = len(report["startup"])
    violations_count = len(report["thin_client"])
    appx_count = next((item["count"] for item in report["other"] if item.get("type") == "appx_bloat"), 0)

    print(f"  Cleanable disk: {total_cleanable:.0f} MB")
    print(f"  Bloat processes: {running_procs} running")
    print(f"  Bloat services: {running_svcs} running")
    print(f"  Startup items: {startup_count}")
    print(f"  AppX bloat: {appx_count} packages")
    print(f"  Thin-client violations: {violations_count}")

    return report

if __name__ == "__main__":
    main()
