---
name: bloat-cleanup
description: Automated Windows system bloatware cleanup, disk decluttering, and DeepChat thin-client compliance enforcement. Use when the user wants to clean up disk space, remove bloatware, kill vampire processes, disable unnecessary services, run system audits across all drives, enforce DeepChat KIF-32 thin-client mandate by detecting and cleaning local project files, purge caches/temp files/browser junk/npm caches, or optimize a Windows laptop for DeepChat performance by freeing RAM and CPU.
version: 2.3
triggers:
- cleanup
- bloatware
- vampire processes
- free space
- declutter
- thin client
- system audit
- disk cleanup
- free RAM
- optimize Windows
---

# Bloat Cleanup

Automated system cleanup for Windows machines running DeepChat. Covers disk decluttering, process/service bloatware removal, and thin-client mandate enforcement.

## Trigger Keywords

"cleanup", "bloatware", "vampire processes", "free space", "declutter", "thin client", "system audit", "optimize Windows", "speed up laptop", "kill bloat", "clean my system", "disk cleanup", "free RAM", "audit services", "dynamic services", "service audit", "disable services"

## Architecture

All logic lives in bundled Python scripts under `scripts/`. The SKILL.md provides workflow guidance. The agent should run scripts via `skill_run` or `exec`.

```
bloat-cleanup/
â”œâ”€â”€ SKILL.md
â””â”€â”€ scripts/
    â”œâ”€â”€ audit_system.py       # Full system audit (disk, processes, services, thin-client)
    â”œâ”€â”€ audit_services.py     # â˜… NEW (KIF-40): Dynamic runtime service classification
    â”œâ”€â”€ kill_bloat.py         # Kill bloatware processes with anti-restart logic
    â”œâ”€â”€ disable_services.py   # Legacy: stop + disable from fixed list (v2.0, sc.exe, reset=86400)
    â”œâ”€â”€ dynamic_disable.py    # â˜… NEW (KIF-40): Runtime target generation + apply (dry-run default)
    â”œâ”€â”€ clean_disk.py         # Delete caches, temps, logs, dumps, package caches
    â”œâ”€â”€     ├── thin_client.py        # Enforce KIF-32 (detect project violations, clean sessions)
    ├── agent_db_prune.py     # v2.3: Delete old sessions + VACUUM agent.db
    ├── kill_clean_restart.bat # v2.3: Autonomous kill->clean->restart
    ├── kill_clean_restart_14d.bat # v2.3: Aggressive 14-day prune
    ├── admin_watcher.ps1     # v2.3: SYSTEM admin signal watcher
    ├── trigger_admin.ps1     # v2.3: No-admin operation queuing
    ├── manage_watcher.ps1    # v2.3: Watcher install/check/repair/stop
    ├── quick_optimize.ps1    # v2.3: Bundled non-admin optimizations
    ├── system_tune.ps1       # v2.3: Power plan, startup, config cleanup
    └── full_clean.py         # Orchestrator: runs all phases (8 phases)
`

**Two-tier service management:**
1. **Static (legacy):** `disable_services.py` â€” fixed hardcoded list. Used as a safety baseline.
2. **Dynamic (â˜… preferred):** `audit_services.py` â†’ `dynamic_disable.py` â€” runtime heuristic classification with no fixed list. Discovers all 284+ services, classifies by vendor/pattern/state, generates targets dynamically.

## Workflow

### Quick: Run everything at once
```
skill_run bloat-cleanup scripts/full_clean.py
```
This runs 7 phases: audit â†’ dynamic service analysis â†’ kill processes â†’ disable services (legacy) â†’ clean disk â†’ thin-client â†’ verify.

### Targeted: Run individual phases

**System audit only** (no changes):
```
skill_run bloat-cleanup scripts/audit_system.py
```

**â˜… Dynamic service audit** (read-only, no admin required):
```
skill_run bloat-cleanup scripts/audit_services.py
```
Discovers all services and classifies them as `essential`, `bloat`, `suspicious`, `user_installed`, or `unknown`. Shows actionable targets with rationale. **Always run this first** before making service changes.

**â˜… Dynamic service disable** (admin required for `--apply`):
```
# Dry-run (default â€” see what would be disabled):
skill_run bloat-cleanup scripts/dynamic_disable.py

# Dry-run with suspicious 3rd-party services:
skill_run bloat-cleanup scripts/dynamic_disable.py --include-suspicious

# Apply (requires admin + --confirm):
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\dynamic_disable.py" --apply --confirm

# Apply with suspicious services:
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\dynamic_disable.py" --apply --confirm --include-suspicious
```

**Kill bloatware processes only:**
```
skill_run bloat-cleanup scripts/kill_bloat.py
```

**Disable bloatware services (legacy fixed list):**
> âš ï¸ **ADMIN REQUIRED.** This script manages Windows services (stop, startup=disabled, recovery clear).
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

### audit_services.py â˜… NEW (KIF-40)
**Dynamic runtime service analysis** â€” replaces the hardcoded `BLOAT_SERVICES` list with heuristic classification. Queries all ~284 services via `Get-CimInstance Win32_Service` and classifies each as:

| Classification | Description | Action |
|---|---|---|
| `essential` | Critical OS services (RpcSs, DcomLaunch, WinDefend, etc.) | Never touch |
| `bloat` | High-confidence bloatware (Lenovo, Dolby, search indexing, telemetry) | Safe to disable |
| `bloat_stopped` | Bloat that's currently stopped (low priority) | Flag for cleanup |
| `suspicious` | Third-party auto-start, no clear purpose | Review before disabling |
| `user_installed` | Known apps (MySQL, Docker, Steam, Discord, etc.) | User decides |
| `inactive` | Stopped + Manual/Disabled â€” dormant | Ignore |
| `unknown` | No heuristic match | Investigate |

**Classification rules (in priority order):**
1. **Critical OS safelist** â€” 60+ essential services never flagged
2. **Vendor patterns** â€” Lenovo, Dolby, Elevoc, Adobe, Google updaters
3. **Windows bloat patterns** â€” WSearch, DiagTrack, DusmSvc, WpnService, CDPSvc, PcaSvc, StiSvc, FontCache
4. **Feature bloat** â€” Xbox, OneDrive, Office ClickToRun
5. **Third-party auto-start** â€” services with Auto start, Running, but no Microsoft/Windows in display name â†’ `suspicious`
6. **User software detection** â€” MySQL, PostgreSQL, Docker, Steam, Discord, etc.

**Read-only, no admin required.** Always run this first.

### dynamic_disable.py â˜… NEW (KIF-40)
**Dynamic target generation + disable** â€” consumes the same classification rules as `audit_services.py` to generate a target list at runtime, then disables services.

**Modes:**
- **Dry-run (default):** Shows what WOULD be disabled. No changes. No admin needed.
- **`--apply --confirm`:** Actually stops + disables + clears recovery. Requires admin.
- **`--include-suspicious`:** Also targets third-party auto-start services (more aggressive).
- **`--json`:** Output targets as JSON for programmatic consumption.

**Safety features:**
- `NEVER_DISABLE` safelist of 60+ critical OS services
- `--confirm` flag required for `--apply`
- Admin privilege check before applying
- Post-disable verification via `sc.exe qfailure`
- Uses `sc.exe` with `reset=86400` (KIF-30 compliant)

### kill_bloat.py
Kills these processes with 3-retry logic:
- **Search/Shell**: SearchHost, SearchApp, SearchIndexer, StartMenuExperienceHost, TextInputHost, LockApp
- **Office**: OfficeClickToRun, SDXHelper
- **Lenovo**: MSPCManagerService
- **Startup bloat**: GoogleDriveFS, uTorrent, Claude, Widgets, CrossDeviceService, OneNote, SecurityHealthSystray

For stubborn processes that restart, falls back to service-level kill (stop + disable + clear auto-recovery) using `sc.exe` with `reset=86400` (KIF-30 fix applied v1.1).

### disable_services.py (Legacy)
Stops, disables startup, and clears auto-recovery for a **fixed list**:
- **Windows bloat**: WSearch, SysMain, DiagTrack, WpnService, DusmSvc, CDPSvc, PcaSvc, StiSvc, FontCache
- **Lenovo bloat**: LITSSVC, LenovoFnAndFunctionKeys, PC Manager Service Store
- **Audio bloat**: DolbyDAXAPI, ElevocService
- **Office**: ClickToRunSvc
- **Optional**: Spooler (disable only if no printer)

Critical: clears `sc.exe failure` auto-recovery actions to prevent Windows auto-restart. The red-team audit from 2026-07-27 confirmed 4 services restarted when only taskkill was used â€” this script fixes that root cause.

> **WARNING â€” PowerShell `sc` alias trap (KIF-05 class):** In PowerShell, `sc` is an ALIAS for `Set-Content`, NOT `sc.exe`. Running `sc failure WSearch reset=0 actions=` in PowerShell silently fails with "A positional parameter cannot be found." The correct invocation is `cmd /c 'sc.exe failure "WSearch" reset= 86400 actions= ""'` (note: `reset=` requires AT LEAST one blank-space-delimited argument; `86400` = 1 day reset window). This requires Administrator privileges.

> **Note:** `disable_services.py` is the legacy fixed-list approach. Prefer `audit_services.py` + `dynamic_disable.py` for runtime discovery on unfamiliar machines.

### clean_disk.py
Deletes (with error handling and size reporting):
- System: hiberfil.sys, Windows Temp, Prefetch, Update cache, CBS logs
- Packages: npm cache (both locations), pip cache
- Browsers: Chrome code/sw/shader caches, Edge code/shader caches
- VS Code: CachedData, CachedExtensionVSIXs, Cache
- Apps: Discord cache, Explorer thumbnails, Office telemetry, PC Manager store, D3DShader
- TexLive: `doc/` and `source/` directories (safe â€” all available online)
- Crash dumps: minidumps, MEMORY.DMP, CrashDumps
- User Temp

### thin_client.py
Enforces KIF-32: "No local project files or archives in .deepchat, AppData, or anywhere in the local file system."

Checks:
1. `.deepchat/projects/` â€” flags each project directory, checks git push status
2. `.deepchat/archive/` â€” violation if exists
3. Desktop/Documents â€” looks for git repos or project-like directories
4. Session offload files â€” lists old sessions (keeps current)

With `--clean`: deletes all old session directories (keeps current session).

### full_clean.py
Orchestrator running all 7 phases in sequence: audit â†’ dynamic service analysis â†’ kill processes â†’ disable services (legacy) â†’ clean disk â†’ thin-client (with `--clean`) â†’ re-audit to verify. Reports elapsed time and final disk state.

## Known Limitations (from Red-Team Audit 2026-07-27, updated KIF-40 kaizen 2026-07-27)

1. **SearchHost/StartMenuExperienceHost** restart endlessly â€” even with service disable. The only permanent fix requires registry policy or `Remove-AppxPackage Microsoft.Windows.Search` (admin PowerShell).
2. **MsMpEng (Defender)** consumes 200-300 MB â€” not targeted by this skill. Instead, recommend adding DeepChat directories to Defender exclusions via `Add-MpPreference -ExclusionPath`.
3. **Office ClickToRun** may restart even after service disable â€” requires `cmd /c 'sc.exe failure "ClickToRunSvc" reset= 86400 actions= ""'` (Admin) which is handled by both `disable_services.py` v2.0 and `dynamic_disable.py` v1.0. Note: `sc` alone fails in PowerShell â€” see WARNING above.
4. **Lenovo MSPCManagerService** may restart â€” recommend uninstalling "Lenovo PC Manager" via `winget uninstall`.
5. Some paths require administrator privileges (Windows Temp, CBS logs, service config). The scripts handle permission errors gracefully and report which items need admin.
6. **KIF-30 (2026-07-27 kaizen): `reset=0` drift bug.** `disable_services.py` v1.0 used `reset=0` (immediate failure-counter reset) instead of the documented `reset= 86400` (1-day window). Fixed in v2.0. **`kill_bloat.py`** had the same bug â€” fixed in v1.1 (2026-07-27 KIF-40 kaizen).
7. **KIF-40 (2026-07-27 kaizen): Dynamic service audit.** The original `disable_services.py` used a hardcoded list of 16 services, missing vendor-specific bloat (Dolby, Elevoc, Adobe updaters, Google updaters, Xbox services, OneDrive) and failing to classify unknown services. Resolved by `audit_services.py` (runtime heuristic classification of 284+ services) and `dynamic_disable.py` (dynamic target generation). The legacy fixed-list script remains as a safety baseline.

## Post-Cleanup Verification

After running cleanup, always verify:
1. Disk space changed as expected
2. Bloat processes didn't restart (check with `audit_system.py`)
3. Services stayed disabled (verify with `audit_services.py`)
4. Thin-client violations resolved

If processes restart, the permanent fix is usually:
```powershell
# Admin PowerShell â€” MANDATORY: use sc.exe (NOT the 'sc' alias which is Set-Content)
Get-AppxPackage Microsoft.Windows.Search | Remove-AppxPackage
cmd /c 'sc.exe config WSearch start= disabled'
cmd /c 'sc.exe failure "WSearch" reset= 86400 actions= ""'
```

## DeepChat Runtime Context
- Skill root: `C:\Users\LENOVO\.deepchat\skills\bloat-cleanup`.
- Relative paths mentioned by this skill are relative to the skill root unless stated otherwise.
- When this skill needs script execution, prefer `skill_run` over `exec`.
- Bundled runnable scripts:
  - scripts\audit_system.py (python)
  - scripts\audit_services.py (python) â˜… NEW
  - scripts\clean_disk.py (python)
  - scripts\disable_services.py (python)
  - scripts\dynamic_disable.py (python) â˜… NEW
  - scripts\full_clean.py (python)
  - scripts\kill_bloat.py (python)
  - scripts\thin_client.py (python)
- Do not guess script paths or change directories to locate skill files.
