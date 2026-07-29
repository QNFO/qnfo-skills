---
name: bloat-cleanup
description: Automated Windows system bloatware cleanup, disk decluttering, and DeepChat thin-client compliance enforcement. Use when the user wants to clean up disk space, remove bloatware, kill vampire processes, disable unnecessary services, run system audits across all drives, enforce DeepChat KIF-32 thin-client mandate by detecting and cleaning local project files, purge caches/temp files/browser junk/npm caches, or optimize a Windows laptop for DeepChat performance by freeing RAM and CPU.
version: 2.6
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

All logic lives in bundled Python scripts under  + "scripts/" + @". The SKILL.md provides workflow guidance. The agent should run scripts via  + "skill_run" + @ or  + "exec" + @.

 + "`" + @"
bloat-cleanup/
+-- SKILL.md
+-- scripts/
    +-- audit_system.py       # Full system audit (disk, processes, services, thin-client, AppX)
    +-- audit_services.py     # Dynamic runtime service classification (KIF-40)
    +-- kill_bloat.py         # Kill bloatware processes with anti-restart logic
    +-- disable_services.py   # Legacy: stop + disable from fixed list (v2.0, sc.exe, reset=86400)
    +-- dynamic_disable.py    # Runtime target generation + apply (KIF-40, dry-run default)
    +-- clean_disk.py         # Delete caches, temps, logs, dumps, package caches
    +-- defender_exclusions.py # v2.4: Add DeepChat paths to Defender exclusions
    +-- remove_appx.py        # v2.4: Remove known AppX bloatware packages
    +-- thin_client.py        # Enforce KIF-32 + KIF-48 (project violations, root hygiene, orphan archives, clean sessions)
    +-- agent_db_prune.py     # v2.1: Budget-laptop prune (7d default, 3d budget, target-size, FTS-aware)
    +-- analyze_agent_db.py   # Read-only: table sizes, session age distribution, tape breakdown
    +-- red_team_audit_db.py  # v2.1: Post-prune integrity audit (orphans, FK, FTS, integrity_check)
    +-- red_light.py          # Ultra-light version: fast spot-checks
    +-- clean_fts_orphans.py  # v2.1: Clean orphaned FTS entries + rebuild indexes
    +-- vacuum_only.py        # Standalone VACUUM runner (run with DeepChat closed)
    +-- budget_laptop_tune.py # v2.0 (KIF-50): Comprehensive system audit + auto-apply + admin queue
    +-- apply_budget_opts.py  # v2.0 (KIF-50): Fast-path non-admin apply + queue variant
    +-- kill_clean_restart.bat # v2.5: 7-day maintenance prune + restart
    +-- kill_clean_restart_14d.bat # v2.5: Aggressive 14-day prune
    +-- kill_clean_restart_budget.bat # v2.5: Budget laptop 3-day prune
    +-- admin_watcher.ps1     # v2.3: SYSTEM admin signal watcher
    +-- trigger_admin.ps1     # v2.3: No-admin operation queuing
    +-- manage_watcher.ps1    # v2.3: Watcher install/check/repair/stop
    +-- quick_optimize.ps1    # v2.3: Bundled non-admin optimizations
    +-- system_tune.ps1       # v2.3: Power plan, startup, config cleanup
    +-- full_clean.py         # Orchestrator: runs all 10 phases
 + "`" + @"
**Two-tier service management:**
1. **Static (legacy):** `disable_services.py` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â fixed hardcoded list. Used as a safety baseline.
2. **Dynamic (ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã¢â‚¬Â¹Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ preferred):** `audit_services.py` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ `dynamic_disable.py` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â runtime heuristic classification with no fixed list. Discovers all 284+ services, classifies by vendor/pattern/state, generates targets dynamically.

## Workflow

### Quick: Run everything at once
```
skill_run bloat-cleanup scripts/full_clean.py
```
This runs 10 phases: audit, dynamic service analysis, kill processes, disable services, Defender exclusions, AppX removal, clean disk, agent DB prune, thin-client, verify.

### Targeted: Run individual phases

**System audit only** (no changes):
```
skill_run bloat-cleanup scripts/audit_system.py
```

**ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã¢â‚¬Â¹Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ Dynamic service audit** (read-only, no admin required):
```
skill_run bloat-cleanup scripts/audit_services.py
```
Discovers all services and classifies them as `essential`, `bloat`, `suspicious`, `user_installed`, or `unknown`. Shows actionable targets with rationale. **Always run this first** before making service changes.

**ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã¢â‚¬Â¹Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ Dynamic service disable** (admin required for `--apply`):
```
# Dry-run (default ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â see what would be disabled):
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
> ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¯ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¸ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â **ADMIN REQUIRED.** This script manages Windows services (stop, startup=disabled, recovery clear).
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

### audit_services.py ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã¢â‚¬Â¹Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ NEW (KIF-40)
**Dynamic runtime service analysis** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â replaces the hardcoded `BLOAT_SERVICES` list with heuristic classification. Queries all ~284 services via `Get-CimInstance Win32_Service` and classifies each as:

| Classification | Description | Action |
|---|---|---|
| `essential` | Critical OS services (RpcSs, DcomLaunch, WinDefend, etc.) | Never touch |
| `bloat` | High-confidence bloatware (Lenovo, Dolby, search indexing, telemetry) | Safe to disable |
| `bloat_stopped` | Bloat that's currently stopped (low priority) | Flag for cleanup |
| `suspicious` | Third-party auto-start, no clear purpose | Review before disabling |
| `user_installed` | Known apps (MySQL, Docker, Steam, Discord, etc.) | User decides |
| `inactive` | Stopped + Manual/Disabled ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â dormant | Ignore |
| `unknown` | No heuristic match | Investigate |

**Classification rules (in priority order):**
1. **Critical OS safelist** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â 60+ essential services never flagged
2. **Vendor patterns** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Lenovo, Dolby, Elevoc, Adobe, Google updaters
3. **Windows bloat patterns** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â WSearch, DiagTrack, DusmSvc, WpnService, CDPSvc, PcaSvc, StiSvc, FontCache
4. **Feature bloat** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Xbox, OneDrive, Office ClickToRun
5. **Third-party auto-start** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â services with Auto start, Running, but no Microsoft/Windows in display name ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ `suspicious`
6. **User software detection** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â MySQL, PostgreSQL, Docker, Steam, Discord, etc.

**Read-only, no admin required.** Always run this first.

### dynamic_disable.py ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã¢â‚¬Â¹Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ NEW (KIF-40)
**Dynamic target generation + disable** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â consumes the same classification rules as `audit_services.py` to generate a target list at runtime, then disables services.

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

Critical: clears `sc.exe failure` auto-recovery actions to prevent Windows auto-restart. The red-team audit from 2026-07-27 confirmed 4 services restarted when only taskkill was used ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â this script fixes that root cause.

> **WARNING ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â PowerShell `sc` alias trap (KIF-05 class):** In PowerShell, `sc` is an ALIAS for `Set-Content`, NOT `sc.exe`. Running `sc failure WSearch reset=0 actions=` in PowerShell silently fails with "A positional parameter cannot be found." The correct invocation is `cmd /c 'sc.exe failure "WSearch" reset= 86400 actions= ""'` (note: `reset=` requires AT LEAST one blank-space-delimited argument; `86400` = 1 day reset window). This requires Administrator privileges.

> **Note:** `disable_services.py` is the legacy fixed-list approach. Prefer `audit_services.py` + `dynamic_disable.py` for runtime discovery on unfamiliar machines.

### clean_disk.py
Deletes (with error handling and size reporting):
- System: hiberfil.sys, Windows Temp, Prefetch, Update cache, CBS logs
- Packages: npm cache (both locations), pip cache
- Browsers: Chrome code/sw/shader caches, Edge code/shader caches
- VS Code: CachedData, CachedExtensionVSIXs, Cache
- Apps: Discord cache, Explorer thumbnails, Office telemetry, PC Manager store, D3DShader
- TexLive: `doc/` and `source/` directories (safe ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â all available online)
- Crash dumps: minidumps, MEMORY.DMP, CrashDumps
- User Temp

### thin_client.py
Enforces KIF-32: "No local project files or archives in .deepchat, AppData, or anywhere in the local file system."

Enforces KIF-48: ".deepchat root directory and file hygiene. Only operational directories and files permitted in .deepchat root. No orphan zip/archive files in AppData\Roaming. No project artifacts masquerading as operational files."

Checks:
1. `.deepchat/projects/` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â flags each project directory, checks git push status
2. `.deepchat/archive/` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â violation if exists
3. Desktop/Documents ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â looks for git repos or project-like directories
4. Session offload files ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â lists old sessions (keeps current)

With `--clean`: deletes all old session directories (keeps current session).


### defender_exclusions.py (v2.4)
Adds DeepChat paths and process to Windows Defender exclusions. Reduces MsMpEng CPU/RAM overhead. Requires Administrator. Run --verify-only for dry-run.

`ash
# Add exclusions (requires admin):
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\defender_exclusions.py"

# Verify only (no changes):
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\defender_exclusions.py" --verify-only
`

### remove_appx.py (v2.4)
Removes known bloatware AppX packages (Xbox, Bing, Widgets, YourPhone, etc.) from both user and provisioned stores. Requires Administrator for provisioned removal.

`ash
# Dry-run (see what would be removed):
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\remove_appx.py" --dry-run

# Live removal:
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\remove_appx.py"

# Aggressive (includes more packages):
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\remove_appx.py" --aggressive
`
### full_clean.py
Orchestrator running all 7 phases in sequence: audit ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ dynamic service analysis ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ kill processes ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ disable services (legacy) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ clean disk ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ thin-client (with `--clean`) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ re-audit to verify. Reports elapsed time and final disk state.

## Known Limitations (from Red-Team Audit 2026-07-29, v2.5 kaizen)

1. **SearchHost/StartMenuExperienceHost** restart endlessly ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â even with service disable. The only permanent fix requires registry policy or `Remove-AppxPackage Microsoft.Windows.Search` (admin PowerShell).
2. **MsMpEng (Defender)** consumes 200-300 MB ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â not targeted by this skill. Instead, recommend adding DeepChat directories to Defender exclusions via `Add-MpPreference -ExclusionPath`.
3. **Office ClickToRun** may restart even after service disable ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â requires `cmd /c 'sc.exe failure "ClickToRunSvc" reset= 86400 actions= ""'` (Admin) which is handled by both `disable_services.py` v2.0 and `dynamic_disable.py` v1.0. Note: `sc` alone fails in PowerShell ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â see WARNING above.
4. **Lenovo MSPCManagerService** may restart ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â recommend uninstalling "Lenovo PC Manager" via `winget uninstall`.
5. Some paths require administrator privileges (Windows Temp, CBS logs, service config). The scripts handle permission errors gracefully and report which items need admin.
6. **KIF-30 (2026-07-27 kaizen): `reset=0` drift bug.** `disable_services.py` v1.0 used `reset=0` (immediate failure-counter reset) instead of the documented `reset= 86400` (1-day window). Fixed in v2.0. **`kill_bloat.py`** had the same bug ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â fixed in v1.1 (2026-07-27 KIF-40 kaizen).
7. **KIF-40 (2026-07-27 kaizen): Dynamic service audit.** The original `disable_services.py` used a hardcoded list of 16 services, missing vendor-specific bloat (Dolby, Elevoc, Adobe updaters, Google updaters, Xbox services, OneDrive) and failing to classify unknown services. Resolved by `audit_services.py` (runtime heuristic classification of 284+ services) and `dynamic_disable.py` (dynamic target generation). The legacy fixed-list script remains as a safety baseline.
8. **KIF-48 (2026-07-29 red-team): .deepchat root hygiene gap.** `thin_client.py` only scanned `.deepchat/projects/` and `archive/`, missing arbitrary project directories in `.deepchat` root (e.g., `qnfo-unified/`, `biophoton-ultrametric-consilience/`), loose project files (`*.js`, `*.jsonc`, `*.reg`), and orphan zip archives in `AppData\Roaming` (e.g., 1.6 GB `DeepChat.zip`). Resolved by KIF-48 scanning: directory allowlist check, file extension check, orphan archive scan. Updated v2.4 (2026-07-29).
9. **KIF-49 (2026-07-29 red-team): FTS orphan leak after session prune.** `agent_db_prune.py` v2.0 skipped `deepchat_tape_search_fts` and `deepchat_tape_search_projection` during deletion (44,853 orphan entries found post-prune red-team audit). Root cause: FTS tables WITH `session_id` column (`tape_search_fts`, `projection`, `_meta` variants) were incorrectly grouped with FTS tables WITHOUT `session_id` (`search_documents_fts`). Fixed in v2.1: FTS_WITH_SESSION_ID list deleted inline; FTS_NO_SESSION_ID uses rebuild-based orphan cleanup. Additionally, orphan FTS meta tables cleaned. Two orphan `usage_stats` rows also fixed. Run `clean_fts_orphans.py` to clean any remaining FTS orphans.
10. **KIF-50 (2026-07-29 red-team): Budget laptop comprehensive tuner.** No single script covered all budget-laptop optimizations end-to-end. Created `budget_laptop_tune.py`: read-only system audit (RAM, disk, services, VBS, visual effects, agent.db, startup, top processes) with severity-rated recommendations; non-admin auto-apply (power plan, transparency, config cleanup); admin queue (hibernation, VBS/HVCI, defender exclusions, dynamic service disable, AppX removal). Run `python budget_laptop_tune.py` for audit; `--apply` to execute non-admin + queue admin. `apply_budget_opts.py` is the fast-path variant. VACUUM confirmed working with DeepChat live (WAL/SHM locks harmless).

## Post-Cleanup Verification

After running cleanup, always verify:
1. Disk space changed as expected
2. Bloat processes didn't restart (check with `audit_system.py`)
3. Services stayed disabled (verify with `audit_services.py`)
4. Thin-client violations resolved

If processes restart, the permanent fix is usually:
```powershell
# Admin PowerShell ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â MANDATORY: use sc.exe (NOT the 'sc' alias which is Set-Content)
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
  - scripts\audit_services.py (python) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã¢â‚¬Â¹Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ NEW
  - scripts\clean_disk.py (python)
  - scripts\disable_services.py (python)
  - scripts\dynamic_disable.py (python) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã¢â‚¬Â¹Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ NEW
  - scripts\full_clean.py (python)
  - scripts\kill_bloat.py (python)
  - scripts\thin_client.py (python)
- Do not guess script paths or change directories to locate skill files.
