---
name: bloat-cleanup
description: >-
  Automated Windows system bloatware cleanup, disk decluttering, and DeepChat thin-client compliance enforcement.
  Use when the user wants to clean up disk space, remove bloatware, kill vampire processes, disable unnecessary services,
  run system audits across all drives, enforce DeepChat KIF-32 thin-client mandate by detecting and cleaning local project files,
  purge caches/temp files/browser junk/npm caches, or optimize a Windows laptop for DeepChat performance by freeing RAM and CPU.
---

# Bloat Cleanup

Automated system cleanup for Windows machines running DeepChat. Covers disk decluttering, process/service bloatware removal, and thin-client mandate enforcement.

## Trigger Keywords

"cleanup", "bloatware", "vampire processes", "free space", "declutter", "thin client", "system audit", "optimize Windows", "speed up laptop", "kill bloat", "clean my system", "disk cleanup", "free RAM"

## Architecture

All logic lives in bundled Python scripts under `scripts/`. The SKILL.md provides workflow guidance. The agent should run scripts via `skill_run` or `exec`.

```
bloat-cleanup/
├── SKILL.md
└── scripts/
    ├── audit_system.py     # Full system audit (disk, processes, services, thin-client)
    ├── kill_bloat.py       # Kill bloatware processes with anti-restart logic
    ├── disable_services.py # Stop + disable + remove auto-recovery for services
    ├── clean_disk.py       # Delete caches, temps, logs, dumps, package caches
    ├── thin_client.py      # Enforce KIF-32 (detect project violations, clean sessions)
    └── full_clean.py       # Orchestrator: runs all phases in sequence
```

## Workflow

### Quick: Run everything at once
```
skill_run bloat-cleanup scripts/full_clean.py
```
This runs audit → kill → disable services → clean disk → thin-client → verify (6 phases).

### Targeted: Run individual phases

**Audit only** (no changes):
```
skill_run bloat-cleanup scripts/audit_system.py
```

**Kill bloatware processes only:**
```
skill_run bloat-cleanup scripts/kill_bloat.py
```

**Disable bloatware services:**
> ⚠️ **ADMIN REQUIRED.** This script manages Windows services (stop, startup=disabled, recovery clear).
> Running without admin will show "SKIP (may need admin)" for all services and make no changes.
> To run as admin, open an elevated PowerShell/CMD and execute:
> `python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\disable_services.py"`
>
> Via skill_run (without admin, shows which services need attention):
```
skill_run bloat-cleanup scripts/disable_services.py
```

**Clean disk caches:**
```
skill_run bloat-cleanup scripts/clean_disk.py
```

**Thin-client enforcement** (audit only):
```
skill_run bloat-cleanup scripts/thin_client.py
```
Add `--clean` to also delete old session offload files:
```
skill_run bloat-cleanup scripts/thin_client.py --clean
```

## What Each Script Does

### audit_system.py
Scans all drives, lists cleanable files with sizes, checks running bloatware processes, checks service status, lists startup registry items, audits thin-client compliance (`.deepchat/projects/`, archive, session offload files), reports `agent.db` size. **Read-only, makes no changes.**

### kill_bloat.py
Kills these processes with 3-retry logic:
- **Search/Shell**: SearchHost, SearchApp, SearchIndexer, StartMenuExperienceHost, TextInputHost, LockApp
- **Office**: OfficeClickToRun, SDXHelper
- **Lenovo**: MSPCManagerService
- **Startup bloat**: GoogleDriveFS, uTorrent, Claude, Widgets, CrossDeviceService, OneNote, SecurityHealthSystray

For stubborn processes that restart, falls back to service-level kill (stop + disable + clear auto-recovery).

### disable_services.py
Stops, disables startup, and clears auto-recovery for:
- **Windows bloat**: WSearch, SysMain, DiagTrack, WpnService, DusmSvc, CDPSvc, PcaSvc, StiSvc, FontCache
- **Lenovo bloat**: LITSSVC, LenovoFnAndFunctionKeys, PC Manager Service Store
- **Audio bloat**: DolbyDAXAPI, ElevocService
- **Office**: ClickToRunSvc
- **Optional**: Spooler (disable only if no printer)

Critical: clears `sc.exe failure` auto-recovery actions to prevent Windows auto-restart. The red-team audit from 2026-07-27 confirmed 4 services restarted when only taskkill was used — this script fixes that root cause.

> **WARNING — PowerShell `sc` alias trap (KIF-05 class):** In PowerShell, `sc` is an ALIAS for `Set-Content`, NOT `sc.exe`. Running `sc failure WSearch reset=0 actions=` in PowerShell silently fails with "A positional parameter cannot be found." The correct invocation is `cmd /c 'sc.exe failure "WSearch" reset= 86400 actions= ""'` (note: `reset=` requires AT LEAST one blank-space-delimited argument; `86400` = 1 day reset window). This requires Administrator privileges.

### clean_disk.py
Deletes (with error handling and size reporting):
- System: hiberfil.sys, Windows Temp, Prefetch, Update cache, CBS logs
- Packages: npm cache (both locations), pip cache
- Browsers: Chrome code/sw/shader caches, Edge code/shader caches
- VS Code: CachedData, CachedExtensionVSIXs, Cache
- Apps: Discord cache, Explorer thumbnails, Office telemetry, PC Manager store, D3DShader
- TexLive: `doc/` and `source/` directories (safe — all available online)
- Crash dumps: minidumps, MEMORY.DMP, CrashDumps
- User Temp

### thin_client.py
Enforces KIF-32: "No local project files or archives in .deepchat, AppData, or anywhere in the local file system."

Checks:
1. `.deepchat/projects/` — flags each project directory, checks git push status
2. `.deepchat/archive/` — violation if exists
3. Desktop/Documents — looks for git repos or project-like directories
4. Session offload files — lists old sessions (keeps current)

With `--clean`: deletes all old session directories (keeps current session).

### full_clean.py
Orchestrator running all 5 scripts in order: audit → kill → disable services → clean disk → thin-client (with `--clean`) → re-audit to verify. Reports elapsed time and final disk state.

## Known Limitations (from Red-Team Audit 2026-07-27, updated kaizen 2026-07-27)

1. **SearchHost/StartMenuExperienceHost** restart endlessly — even with service disable. The only permanent fix requires registry policy or `Remove-AppxPackage Microsoft.Windows.Search` (admin PowerShell).
2. **MsMpEng (Defender)** consumes 200-300 MB — not targeted by this skill. Instead, recommend adding DeepChat directories to Defender exclusions via `Add-MpPreference -ExclusionPath`.
3. **Office ClickToRun** may restart even after service disable — requires `cmd /c 'sc.exe failure "ClickToRunSvc" reset= 86400 actions= ""'` (Admin) which is handled by `disable_services.py` v2.0. Note: `sc` alone fails in PowerShell — see WARNING above.
4. **Lenovo MSPCManagerService** may restart — recommend uninstalling "Lenovo PC Manager" via `winget uninstall`.
5. Some paths require administrator privileges (Windows Temp, CBS logs, service config). The scripts handle permission errors gracefully and report which items need admin.
6. **KIF-30 (2026-07-27 kaizen): eset=0 drift bug.** disable_services.py v1.0 used eset=0 (immediate failure-counter reset) instead of the documented eset= 86400 (1-day window). The SKILL.md was updated during the KIF-28 red-team pass but the Python script was NOT — a registry-extension drift bug (cf. KIF-22 class). Fixed in v2.0: eset= 86400 with explicit sc.exe, post-disable verification via sc.exe qfailure, and UTF-8 I/O.

## Post-Cleanup Verification

After running cleanup, always verify:
1. Disk space changed as expected
2. Bloat processes didn't restart (check with `audit_system.py`)
3. Services stayed disabled
4. Thin-client violations resolved

If processes restart, the permanent fix is usually:
```powershell
# Admin PowerShell — MANDATORY: use sc.exe (NOT the 'sc' alias which is Set-Content)
Get-AppxPackage Microsoft.Windows.Search | Remove-AppxPackage
cmd /c 'sc.exe config WSearch start= disabled'
cmd /c 'sc.exe failure "WSearch" reset= 86400 actions= ""'
```
