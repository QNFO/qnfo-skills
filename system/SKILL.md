---
name: system
description: SESSION STARTUP: load after qnfo-agent. DeepChat config, skill ecosystem, desktop automation. Settings, MCP, skills lifecycle, CUA GUI automation.
---
> **v2.5 UPDATE (2026-08-02, kaizen — skill-sync v4 REST fast path + autonomy):**
> Red-team: direct parent-agent audit. HARD: 2. SOFT: 1. DESIGN: 2.
> Changes:
> (1) [HARD] **skill-sync.js v3.0.0's `npx --yes --package wrangler@latest` per-file
>     path was pathological** — npx cold-start + wrangler re-resolution per file,
>     90s timeout each, WinError 2 in daemon subprocess env. Measured: ZERO state
>     updates in 20+ min (state file stale at 33h). **v4.0.0 replaces it with the
>     Cloudflare R2 REST API** (`PUT /accounts/{id}/r2/buckets/qnfo-skills/objects/{key}`
>     + Bearer token) with 8-way parallel pool + per-file GET verify. Measured:
>     **278 files in 27.2s, 0 failures** (~600x faster). No npx, no wrangler, no
>     node_modules. Token discovery: env → ~/.cloudflare_token → ~/keys.json.
> (2) [HARD] **`git add -A` in skill-sync swept unrelated files** — commit cbc5f7f
>     accidentally included research/scripts/build-paper.py.bak-20260802 (506 lines,
>     reverted d109323). Fix: repo `.gitignore` now excludes `*.bak`, `*.bak-*`,
>     `*.tmp`, `*.log`, `.deepchat/`, `node_modules/`; walkFiles also skips *.bak-*.
> (3) [SOFT] New flags: `--skip-git` (R2 only), `--no-verify`, `--force`, `--targets=`.
>     Exit codes: 0 clean, 1 R2 failures after retry, 2 no token.
> (4) [DESIGN] **Autonomous sync (no prompting):** new cronjob `skills-autonomous-sync`
>     runs `node system/scripts/skill-sync.js` every 6h (agentId deepchat, UTC).
>     Also hookable at session start / Watchtower. Sync is idempotent via
>     content-hash state (~/.deepchat/.skill-sync-state.json).
> (5) [DESIGN] §Autonomous Skill Sync section below documents the cronjob + manual
>     invocation + failure handling.
> Cross-reference: cloudflare v3.18, kaizen v1.4.1, research v2.45.

## Autonomous Skill Sync (v2.5)

Skill changes are synced to GitHub (origin QNFO/qnfo-skills + rwnq8 mirror) and R2
(qnfo-skills bucket) WITHOUT user prompting:

1. **Cronjob:** `skills-autonomous-sync` — `node C:\Users\LENOVO\.deepchat\skills\system\scripts\skill-sync.js` every 6h (cron `0 */6 * * *`, UTC, agentId deepchat).
2. **Manual invocation:** `node system/scripts/skill-sync.js` (full) or `--skip-git` (R2 only).
3. **Idempotency:** content-hash state file skips unchanged files; re-runs are fast.
4. **Failure handling:** script exits 1 on R2 failures (after 1 retry each); cronjob
   logs failures to durable memory; exit 2 = token missing.
5. **Verification:** after sync, GET a sample object from R2
   (`GET /accounts/{id}/r2/buckets/qnfo-skills/objects/prompts/skills/<name>/SKILL.md`)
   and compare Content-Length.



# SYSTEM -- v2.5 (Ultra-Consolidated Config + Skills + Desktop + Hygiene + Session Init)

> **v2.4 UPDATE (2026-07-31, kaizen — R2 sync tooling hardening):**
> Red-team: direct parent-agent 5-adversary audit (Accuracy, Completeness,
> Dependency, Novelty, Status). HARD findings: 1. SOFT findings: 2.
> Changes:
> (1) [HARD] `scripts/skill-sync.js` v2.0.0 -> v3.0.0. Bare `npx wrangler`
>     per-file resolved to a corrupted npx cache (missing
>     `@cloudflare/workerd-windows-64`) making EVERY upload fail with a workerd
>     module error misdiagnosed as auth. Fix: pin `npx --yes --package
>     wrangler@latest` for all invocations; add failure-cause classification
>     (auth / cache-corruption / timeout) with actionable remediation hints.
>     (Accuracy Auditor, parent-agent).
> (2) [SOFT] skill-sync.js v3.0.0 adds content-hash state file
>     (`~/.deepchat/.skill-sync-state.json`): files unchanged since last
>     successful upload are SKIPPED, making re-runs idempotent and fast.
>     Previous full syncs were reaped at 19/29 skills by the harness timeout
>     and re-uploaded everything from scratch. Also adds `--targets=a,b,c`
>     filter, `--force` bypass, and 1x retry on transient failures.
>     (Completeness + Novelty Auditors, parent-agent).
> (3) [SOFT] `scripts/skill-sync-remaining.js` v1.0 -> v1.1: same wrangler
>     pinning + shared hash state file. (Dependency Auditor, parent-agent).
> Cross-reference: kaizen v1.2.5, windows-command-patterns v2.1 (KIF-12
> exec-session reaping), mem-Hbi-G-pFovi8 (npx cache corruption anti-pattern).

> **v2.3 UPDATE (2026-07-26, session initialization + startup integration):**
> Added **Session Initialization Protocol** to fix the skill auto-loading
> weak link (KIF-25). New components: (1) `/init` custom prompt that loads
> qnfo-agent + system + runs skill-hygiene.js at session start, (2)
> `deepchat-skill-hygiene.vbs` in Windows Startup folder for automatic
> hygiene checks at logon, (3) `skill-loader.js` for generating skill
> discovery summaries. The 24-Skill Trigger Table inside qnfo-agent is
> now reliably accessible via the `/init` command.

> **v2.2 UPDATE (2026-07-26, skill location hygiene):** Added the
> **Canonical Skill Locations** and **Skill Hygiene Enforcement** sections.
> Skills exist in ONE canonical location only. Duplicate/stale locations
> are detected and must be cleaned. New scripts: `skill-hygiene.js`,
> `skill-locations-audit.md` template. GitHub dual-remote (QNFO + rwnq8)
> is intentional mirroring, not duplication.

> **v2.1 UPDATE (2026-07-21, phantom-claim audit):** Added the
> **Tool-Call Execution Mandate** section below. Skill sync is not "done"
> until all 3 layers (disk/GitHub/R2) are independently re-read back in
> the same turn — a script's exit code alone does not prove GitHub or R2
> actually received the content.

> **Merges 3:** deepchat-config + skill-management + computer-use
> **Related:** Load `cloudflare` for skill deployment to R2 bucket `qnfo-skills/prompts/skills/`. Desktop automation is platform-local only.
> **Cloudflare Full-Stack:** Skills deploy to R2. App settings reference Cloudflare MCP Workers. All config is Cloudflare-backed.

## execute_plan

update_plan([
  {"step": "Identify target: configuration, skill lifecycle, or desktop automation", "status": "pending"},
  {"step": "Run skill-hygiene.js if skill-related", "status": "pending"},
  {"step": "Execute with proper tooling", "status": "pending"},
  {"step": "Verify: settings persisted, skills deployed, or action confirmed", "status": "pending"},
])

---

## Canonical Skill Locations (MANDATORY — v2.2)

### Single Source of Truth

| Layer | Canonical Location | Purpose |
|:------|:-------------------|:--------|
| **Local Disk** | `%USERPROFILE%\.deepchat\skills\` | Primary working directory, git-tracked |
| **GitHub Primary** | `QNFO/qnfo-skills` | Organization repo, `origin` remote |
| **GitHub Mirror** | `rwnq8/qnfo-skills` | Personal backup, `rwnq8` remote |
| **R2 Backup** | `qnfo-skills` bucket, `prompts/skills/<name>/` | Cloudflare R2 disaster recovery |

### PROHIBITED Locations (Must Not Exist)

| Path | Why Prohibited |
|:-----|:---------------|
| `%APPDATA%\.deepchat\skills\` | Legacy bootstrap location, causes version conflicts |
| `%APPDATA%\DeepChat\skills\` | Unused app data location, confuses discovery |
| `%LOCALAPPDATA%\DeepChat\skills\` | Electron cache, not for skills |

### What Constitutes a "Skill"

A skill is **NOT just SKILL.md** — it includes all supplemental files:

```
<skill-name>/
├── SKILL.md          (required — the skill definition)
├── scripts/          (optional — utility scripts the skill invokes)
├── references/       (optional — supporting reference docs)
├── templates/        (optional — file templates the skill instantiates)
└── assets/           (optional — static assets)
```

**Sync operations MUST include ALL files**, not just SKILL.md. Use `skill-sync.js` which walks the entire directory tree.

### GitHub Dual-Remote (Intentional Mirroring)

The local repo has TWO remotes configured:
- `origin` → `https://github.com/QNFO/qnfo-skills.git` (primary)
- `rwnq8` → `https://github.com/rwnq8/qnfo-skills.git` (mirror)

This is **intentional redundancy**, not duplication. Both repos should have identical HEAD commits. After every push:
```powershell
git push origin master
git push rwnq8 master
```

---

## Skill Hygiene Enforcement (MANDATORY — v2.2)

### Pre-Session Gate

Before any skill-related work, run the hygiene audit:
```powershell
node "$env:USERPROFILE\.deepchat\skills\system\scripts\skill-hygiene.js"
```

**Exit codes:**
- `0` = All clean, proceed
- `1` = Stale locations found, cleanup required before proceeding
- `2` = Version conflicts, manual resolution required
- `3` = Script error

**If exit code ≠ 0, DO NOT proceed with skill modifications until resolved.**

### Stale Location Cleanup Protocol

If stale locations are detected:

1. **Check for version conflicts:**
   ```powershell
   Get-Content "<stale>\<skill>\SKILL.md" | Select-String "version:"
   Get-Content "$env:USERPROFILE\.deepchat\skills\<skill>\SKILL.md" | Select-String "version:"
   ```

2. **If stale has newer/valuable changes:**
   - Merge to canonical location first
   - Commit to git
   - Then delete stale

3. **Delete stale location:**
   ```powershell
   Remove-Item -Recurse -Force "<stale-path>"
   ```

4. **Re-run hygiene audit to confirm clean:**
   ```powershell
   node "$env:USERPROFILE\.deepchat\skills\system\scripts\skill-hygiene.js"
   # Must exit with code 0
   ```

### DeepChat Startup Integration

**Option A: Windows Task Scheduler (Recommended)**
```powershell
$action = New-ScheduledTaskAction -Execute "node" -Argument "$env:USERPROFILE\.deepchat\skills\system\scripts\skill-hygiene.js"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
Register-ScheduledTask -TaskName "DeepChat-SkillHygiene" -Action $action -Trigger $trigger -Principal $principal -Description "Audit skill locations on startup"
```

**Option B: Manual Pre-Session Check**
At the start of any session involving skill modifications, the agent should run `skill-hygiene.js` and report results.

**Option C: Audit Log Review**
Check the latest audit report:
```powershell
Get-Content "$env:USERPROFILE\.deepchat\audit\skill-hygiene-latest.json" | ConvertFrom-Json
```

### Anti-Patterns (Skill Hygiene)

| Anti-Pattern | Detection | Fix |
|:-------------|:----------|:----|
| Editing skills in stale location | `skill-hygiene.js` exit 1 | Move edits to canonical, delete stale |
| SKILL.md-only sync | R2 missing scripts/templates | Use `skill-sync.js` for full sync |
| Forgetting rwnq8 push | `git log rwnq8/master` behind | `git push rwnq8 master` |
| Creating skills in AppData | `skill-hygiene.js` exit 1 | Only create in `%USERPROFILE%\.deepchat\skills\` |
| Manual token copy | Truncated tokens cause auth | Use `$env:TOKEN_NAME` directly |

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — MANDATORY)

Claiming a setting is "changed", a skill is "deployed"/"synced", or a
desktop action is "done" without an invoked tool call showing evidence in
this turn is a PHANTOM CLAIM (`qnfo-agent` §9.11 Rule 14) — BLOCKED.

1. **Settings changes** — call the actual `deepchat_settings_*` tool and confirm the returned value matches the requested change; do not assert a setting changed without the tool's confirmed return value.
2. **Skill deploy/sync** — a `git push`/R2 `object put` script's exit code 0 is NOT sufficient. Independently re-read back all 3 layers in this turn: `Test-Path` (disk), `git log -1 --oneline` on the skill's own commit (GitHub), AND `npx wrangler r2 object get qnfo-skills/prompts/skills/<name>/SKILL.md --remote` (R2) — compare content, not just presence.
3. **Desktop automation** — after any click/type/launch action, call `get_window_state` again and show the resulting UI state; do not claim an action succeeded from the dispatch call's return alone.
4. If any of the 3 sync layers cannot be re-verified in this turn, say `[NOT-VERIFIED: layer X unconfirmed]` instead of "synced"/"deployed"/"done".

---

## DeepChat Configuration

### App Settings
**Path:** `%APPDATA%\DeepChat\app-settings.json`

Key settings:
- `skillsPath`: `%USERPROFILE%\.deepchat\skills` (MUST point to canonical location)
- `enableSkills`: `true`

```json
{
  "theme": "light",
  "language": "en",
  "fontSize": 14,
  "fontFamily": "Inter",
  "skillsPath": "C:\\Users\\LENOVO\\.deepchat\\skills",
  "enableSkills": true,
  "modelConfig": {
    "temperature": 0.3,
    "maxTokens": 64000,
    "contextLength": 128000,
    "reasoning": true
  }
}
```

### MCP Server Configuration
**RAG Bridge (primary):** `qnfo-memory-mcp` at `https://qnfo-memory-mcp.q08.workers.dev/mcp`
- Tools: `search_papers`, `search_memories`, `remember_fact`, `recall_facts`, `get_paper_context`
- Bindings: MEMORY_DB, MEMORY_VZ, PAPER_VZ, AI
- Version: v1.2 (2026-07-14, red-team audited)

**AI Search (managed):** `qnfo-ai-search` -- Cloudflare AI Search
- Source: R2 bucket `qnfo/papers/`
- Embedding model: `bge-base-en-v1.5`

### Disaster Recovery
1. Settings lost -> restore from `deepchat-config` skill backup
2. GitHub backup -> `qnfo-skills` repo (QNFO/qnfo-skills or rwnq8/qnfo-skills)
3. R2 backup -> `prompts/skills/` on R2 bucket `qnfo-skills`
4. DeepChat restart: `taskkill /F /IM DeepChat.exe` -> auto-restart

---

## Skill Management

### SKILL.md Structure (MANDATORY)
```yaml
---
name: skill-name
description: Rich description with comprehensive trigger keywords for autonomous discovery
version: "2.5"
triggers: ["keyword1", "keyword2", ...]
related: ["other-skill"]
priority: 0-3
platform: all | cloudflare | local
autonomous: true | false
self_sufficient: true
---

# SKILL TITLE -- v1.0

> **Merges:** list of merged skills (if consolidated)

## execute_plan
update_plan([...])

## Core Content
[Complete unabridged instructions]

## Verification
[Post-execution gates]

## Anti-Patterns
[What NOT to do]
```

### Design Principles
1. **Self-sufficient:** No external file references. Embed ALL scripts, templates, and protocols inline.
2. **Verifiable:** Every workflow step produces tool evidence (Test-Path, git log, exec output).
3. **Chainable:** `related:` field lists subsidiary skills for auto-loading.
4. **Discoverable:** `triggers:` contains comprehensive keyword arrays for autonomous pattern matching.
5. **Concrete:** No vague instructions ("handle errors properly"). Specific, executable steps.

### Skill Lifecycle
```
CREATE -> WRITE (SKILL.md with complete content) -> DEPLOY -> VERIFY -> MAINTAIN
```

### Deployment (3-Layer Sync)
1. **Local disk:** Write to `%USERPROFILE%\.deepchat\skills\<name>\SKILL.md`
2. **GitHub:** Commit and push to BOTH remotes:
   ```powershell
   git add -A
   git commit -m "skill: <name> v<version>"
   git push origin master
   git push rwnq8 master
   ```
3. **R2:** Upload ALL files (not just SKILL.md):
   ```powershell
   node "$env:USERPROFILE\.deepchat\skills\system\scripts\skill-sync.js"
   ```
4. **Verify:** All layers have identical content

### Verification
```powershell
# Check local
Test-Path "$env:USERPROFILE\.deepchat\skills\<name>\SKILL.md"

# Check GitHub (both remotes)
git log -1 --oneline origin/master
git log -1 --oneline rwnq8/master

# Check R2
npx wrangler r2 object get qnfo-skills prompts/skills/<name>/SKILL.md --remote
```

---

## Desktop Automation (Computer Use)

### Available Tools
`list_apps` | `list_windows` | `get_window_state` | `click` | `double_click` | `right_click` | `type_text` | `press_key` | `hotkey` | `scroll` | `drag` | `launch_app` | `kill_app` | `bring_to_front` | `get_screen_size` | `get_desktop_state` | `get_cursor_position` | `move_cursor` | `set_value` | `debug_window_info`

### Standard Usage Pattern
```python
# 1. Find the app
list_apps()  # Returns: {name, pid, running, kind, launch_path}

# 2. Launch if not running, or get window handle
launch_app({name: "Notepad", start_minimized: True})
# Returns: {pid, name, windows: [{window_id, title, bounds}]}

# 3. Inspect the window
get_window_state({pid: 1234, window_id: 5678})
# Returns: {tree_markdown, structuredContent, screenshot}

# 4. Interact via element_index (background-safe)
click({pid: 1234, window_id: 5678, element_index: 5})
type_text({pid: 1234, text: "Hello", element_index: 3, window_id: 5678})

# 5. Verify result
get_window_state({pid: 1234, window_id: 5678})
```

### Windows Platform Notes
- **Element index preferred** for background-safe clicks (no focus steal, no window activation)
- **XAML/WinUI3/UWP apps** (modern Notepad, Calculator, Photos) -- require `element_index` for `type_text`
- **Legacy Win32 apps** -- `type_text` via PostMessage(WM_CHAR) works without element_index
- **`delivery_mode: "background"` FIRST** -- only escalate to `"foreground"` on `background_unavailable` error
- **Element index is per-snapshot** -- re-snapshot with `get_window_state` before each interact cycle
- **minimized windows** -- UIA works on minimized windows; `screenshot` and foreground delivery need restoration
- **Check permissions:** `check_permissions()`
- **Health:** `health_report()`

### Anti-Patterns (CUA)
| Anti-Pattern | Fix |
|:-------------|:----|
| Pixel click without element_index | Prefer element_index for background-safety |
| Foreground delivery without trying background first | Always try `background` first |
| Using stale element_index | Re-snapshot with `get_window_state` before each cycle |
| Click on XAML app without element_index | XAML requires element_index for type_text |
| Launching app without `start_minimized: true` | Launch hidden to not disrupt user |

---

## Session Initialization Protocol (v2.3)

### The Problem (KIF-25: Skill Auto-Loading Weak Link)

DeepChat shows only 8 skills in the system prompt. The **24-Skill Trigger Table**
(which enables autonomous skill discovery) is inside qnfo-agent's body — but
qnfo-agent must be explicitly loaded via `skill_view` for the table to be active.
Without loading qnfo-agent first, the LLM cannot discover which skill to use.

### The Solution

Three-layer automatic initialization:

**Layer 1: Windows Startup (Automatic)**
- `deepchat-skill-hygiene.vbs` in Windows Startup folder
- Runs `skill-hygiene.js` silently at every Windows logon
- Logs results to `%USERPROFILE%\.deepchat\audit\startup-hygiene.log`
- Location: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`

**Layer 2: /init Custom Prompt (User-Triggered)**
- Type `/init` in DeepChat to initialize session
- Executes: `skill_view("qnfo-agent")` + `skill_view("system")` + `skill-hygiene.js`
- Ensures 24-Skill Trigger Table is available for autonomous discovery
- Added via `system/scripts/add-init-prompt.js`

**Layer 3: skill-loader.js (Programmatic)**
- Generates compact skill discovery summary
- Can be called by scripts/tools that need skill information
- Usage: `node skill-loader.js [--json|--triggers]`

### Usage

**Option A: Manual Session Init (Recommended)**
```
/init
```
This loads qnfo-agent + system and runs hygiene check.

**Option B: Direct Skill Loading**
```
skill_view("qnfo-agent")  # Load safety-net core with trigger table
skill_view("system")       # Load skill management
```

**Option C: Task-Specific Loading**
When you know which skill you need:
```
skill_view("research")     # For papers/Zenodo/literature
skill_view("cloudflare")   # For Workers/R2/D1/infra
skill_view("code-review")  # For code quality/security
```

### Verification
```powershell
# Check startup script exists
Test-Path "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\deepchat-skill-hygiene.vbs"

# Check /init prompt exists
(Get-Content "$env:APPDATA\DeepChat\custom_prompts.json" | ConvertFrom-Json).PSObject.Properties | Where-Object { $_.Value.id -eq 'init-session' }

# Check startup log
Get-Content "$env:USERPROFILE\.deepchat\audit\startup-hygiene.log" -Tail 5
```

---

## Reusable Scripts

### Skill Hygiene Audit
```powershell
# Run before any skill work
node "$env:USERPROFILE\.deepchat\skills\system\scripts\skill-hygiene.js"
# Exit 0 = clean, Exit 1 = stale locations, Exit 2 = version conflicts
```

### Full Skill Sync (All Files)
```powershell
# Syncs ALL skill files (not just SKILL.md) to R2
node "$env:USERPROFILE\.deepchat\skills\system\scripts\skill-sync.js"
```

### Worker Fleet Audit
```js
// See cloudflare/scripts/worker-audit.js
```

### Infrastructure Audit
```js
// See cloudflare/scripts/infra-audit.js
```

---

## Verification Checklist
- [ ] Config changes persist across DeepChat restarts
- [ ] Skills synced to all 3 layers: disk -> GitHub (both remotes) -> R2
- [ ] `skill-hygiene.js` exits with code 0 (no stale locations)
- [ ] Desktop automation result confirmed via window state
- [ ] `health_report()` returns all checks passing
- [ ] No skill has external file references (self-sufficiency)
- [ ] No skill has fewer than 15 trigger keywords
- [ ] **4-D Gate:** Critical assets verified across ≥4 distribution stores
- [ ] **Worker fleet:** ≤7 Workers (consolidation pattern enforced), 0 orphaned Workers
- [ ] **R2 hygiene:** No `qnfo/qnfo/` double-prefix paths in qnfo bucket

---

*system v2.3 — DeepChat configuration, skill ecosystem management, skill location hygiene, session initialization, and desktop automation.*
