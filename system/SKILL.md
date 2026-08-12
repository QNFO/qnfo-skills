---
name: system
description: SESSION STARTUP: load after qnfo-core. DeepChat config, skill ecosystem, desktop automation. Settings, MCP, skills lifecycle, CUA GUI automation. Exec uses cmd.exe (PSModulePath deleted + Python shim v3). See EXEC-SHELL-FIX.md.
version: 2.14
kif_tags: [KIF-32]
---

> **API-FAILURE PROTOCOL (HARD, cross-ref):** When any API call returns 403/401/404,
> run the API-Failure Self-Diagnosis Protocol (windows-command-patterns S-1.0.6):
> STOP -> VERIFY your HTTP method/headers -> COMPARE with curl -> THEN consider
> infrastructure. The bug is ALWAYS your code until proven otherwise (kaizen BLAME-EXTERNAL-1).

> **v2.14 UPDATE (2026-08-12, kaizen — skill-sync v4.0.11 H1/H2/S2 remediation + 4-store prompt parity):**
> Red-team: direct parent-agent 5-adversary audit (this session — skill-sync remediation + prompt-store parity audit).
> HARD: 3. SOFT: 1. Changes:
> (1) [HARD] **skill-sync.js v4.0.11** — `gitOk = pushedOk.has('origin') && pushedOk.has('rwnq8')` replaces the
>     unconditional `gitOk = true` (the "✓ Skill sync complete" message printed + exit 0 even when BOTH pushes
>     were rejected — the "⚠ Skill sync partial" branch was unreachable). walkFiles now skips `logs` dirs.
> (2) [HARD] **SYNC-DIVERGENCE-MERGE-1:** do NOT blindly apply the memory-documented "--theirs local tip" rebase
>     policy on divergence — FETCH + INSPECT remote first; if remote has substantive content (e.g. 2026-08-12:
>     1,300+ lines of cloudflare v3.46-3.49 work, deepchat-hooks v1.1 skill, system-prompt edits) MERGE and
>     resolve per-superset; the blind policy would have DESTROYED remote work. Cross-ref: §Autonomous Skill Sync.
> (3) [HARD] **PROMPT-STORE-4STORE-1:** system-prompt dual-writes MUST hit ALL 4 stores (agent.db systemPrompts /
>     app-settings.json default_system_prompt / .deepchat/system-prompt-v2.7.md / qnfo-skills repo copy) —
>     v1.13 wrote only 3, the repo copy stayed stale at v3.3 until this cycle.
> (4) [SOFT] CMD DEPLOY template stale $10/30d → $90/30d (both stores); CMD SKILLS UPDATE template gained the
>     4-store parity mandate. Cross-ref: skill-sync.js v4.0.11, kaizen v2.25, deepchat-settings v1.14.

> **v2.12 UPDATE (2026-08-04, kaizen — RCLONE-FIRST-1 default for bulk transfers):**
> [HARD] **rclone is the system default for ANY large or multi-file transfer**
> (R2/S3/cloud). Not wrangler, not per-object API loops. Verified live: 54k-file
> D:\Archive sync + R2 bucket-to-bucket server-side copy (0.5s, zero local traffic).
> Canonical binary `C:\rclone\rclone.exe` (cmount build, v1.74.4). Config:
> `%APPDATA%\rclone\rclone.conf` (remotes `primary-r2`, `releases`, `archive`).
> Detached pattern: `subprocess.Popen(..., creationflags=CREATE_NO_WINDOW|DETACHED_PROCESS)`
> so transfers survive exec teardown. Full protocol: cloudflare skill §R2 Transfer Protocol.

> **v2.13 UPDATE (2026-08-04, kaizen — SKILL-SYNC-GITPATH-1 + desktop boundary + R2 key paths):**
> Red-team: direct parent-agent audit of session 5ptZtvKLdqr3GzAykql8G (D-drive migration + personal-life build).
> HARD: 3. SOFT: 2. Changes:
> (1) [HARD] **SKILL-SYNC-GITPATH-1:** skill-sync.js runs git with `cwd = C:\Users\LENOVO\.deepchat\skills`
>     which is NOT a git repo → GitHub sync **silently fails** while R2 sync reports OK. The real repo is
>     `C:\Users\LENOVO\Documents\GitHub\qnfo-skills` (canonical remote `QNFO/qnfo-skills.git`; the rwnq8
>     mirror is ARCHIVED — 403 on push). Fix: run git ops in the Documents\GitHub\qnfo-skills clone, or
>     pass a repo-aware cwd; verify with `git log origin/master` after every sync. Cross-ref: system §Autonomous Skill Sync.
> (2) [HARD] **DESKTOP-BOUNDARY-1:** NEVER place files on the user's Desktop (or Documents root) without
>     explicit consent — user mandate 2026-08-04. Deliverables go to `C:\rclone\` (technical working dir)
>     or user-designated locations. Violation case: D-Drive-Migration-Plan.md was written to Desktop; corrected.
> (3) [HARD] **R2-SKILL-KEYPATH-1:** skills live in the `qnfo-skills` R2 bucket at
>     `prompts/skills/<name>/SKILL.md` — NOT bucket root (`cloudflare/SKILL.md` is a stale legacy copy).
>     Verify with `rclone cat primary-r2:qnfo-skills/prompts/skills/<name>/SKILL.md`.
> (4) [SOFT] **DESKTOP-BOUNDARY-1** also applies to Desktop subfolders and Documents — user reads everything there.
> (5) [SOFT] Cross-ref: cloudflare v3.32 (Vectorize gotchas), kaizen v1.26, git-github v2.14.



> **v2.9 UPDATE (2026-08-03, kaizen — RED-TEAM RECOVERY + EXEC SHELL MANDATE):**
> Recovered from write-tool corruption (was 9,902 bytes with broken YAML). Restored
> from git working copy (27,935 bytes) + re-applied session deltas. Added:
> (1) [HARD] **EXEC SHELL MANDATE — cmd.exe via PSModulePath deletion + Python shim v3**
>     at `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`. DeepChat's
>     `getUserShell()` (shellEnvHelper.ts) picks PowerShell when `process.env.PSModulePath`
>     is truthy, cmd.exe when unset. PSModulePath deleted from HKCU. Shim strips the
>     3 UTF8Encoding preambles, forwards to cmd.exe. Full guide: EXEC-SHELL-FIX.md.
> (2) [HARD] **EXEC-SHELL-FIX.md reference** — reproducible step-by-step recovery guide.
> (3) [SOFT] Cross-reference: windows-command-patterns v3.17, deepchat-internals.md,
>     SESSION_LOG_POWERSHELL_EXTERMINATION.md.
> Red-team: direct parent-agent audit (subagent truncated — systemic). HARD: 2, SOFT: 1.

> **v2.6 UPDATE (2026-08-02, kaizen — DeepChat restart automation):**
> [HARD] Added **§DeepChat Restart Protocol** — mandatory automatic restart
> after any skill/settings/agent.db change (DeepChat scans skills at startup
> only; changes are invisible until restart). Canonical helper:
> `scripts/restart-deepchat.py` (detaches, waits, graceful-close, relaunch,
> marker + log). Wired into: deepchat-settings (settings), skill-creator
> (new skills), memory-management (agent.db prune), bloat-cleanup (VACUUM).
> Post-boot session-init checks pending-restart.json + clears stale agent.db
> skill-index cache if skills still missing.
> Cross-reference: deepchat-settings, skill-creator, memory-management,
> bloat-cleanup v2.8, memory "stale agent.db cache".

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
> Cross-reference: cloudflare v3.29, kaizen v1.4.1, research v2.45.

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



# SYSTEM — 2.13 (Ultra-Consolidated Config + Skills + Desktop + Hygiene + Session Init + Exec Shell Mandate)

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
> Cross-reference: kaizen v1.22, windows-command-patterns v2.1 (KIF-12
> exec-session reaping), mem-Hbi-G-pFovi8 (npx cache corruption anti-pattern).

> **v2.3 UPDATE (2026-07-26, session initialization + startup integration):**
> Added **Session Initialization Protocol** to fix the skill auto-loading
> weak link (KIF-25). New components: (1) `/init` custom prompt that loads
> qnfo-core + system + runs skill-hygiene.js at session start, (2)
> `deepchat-skill-hygiene.vbs` in Windows Startup folder for automatic
> hygiene checks at logon, (3) `skill-loader.js` for generating skill
> discovery summaries. The 24-Skill Trigger Table inside qnfo-core is
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
```python
import subprocess
subprocess.run(["git", "push", "origin", "master"], check=True)
subprocess.run(["git", "push", "rwnq8", "master"], check=True)
```

---

## Skill Hygiene Enforcement (MANDATORY — v2.2)

### Pre-Session Gate

Before any skill-related work, run the hygiene audit:
```python
import subprocess, os
subprocess.run(
    ["node", os.path.join(os.environ["USERPROFILE"], ".deepchat", "skills", "system", "scripts", "skill-hygiene.js")],
    check=True
)
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
   ```python
   import os
   from pathlib import Path

   userprofile = os.environ["USERPROFILE"]
   for f in [Path("<stale>", "<skill>", "SKILL.md"), Path(userprofile, ".deepchat", "skills", "<skill>", "SKILL.md")]:
       if f.exists():
           for line in f.read_text(encoding="utf-8").splitlines():
               if "version:" in line:
                   print(f"{f}: {line}")
   ```

2. **If stale has newer/valuable changes:**
   - Merge to canonical location first
   - Commit to git
   - Then delete stale

3. **Delete stale location:**
   ```python
   import shutil
   shutil.rmtree("<stale-path>", ignore_errors=True)
   ```

4. **Re-run hygiene audit to confirm clean:**
   ```python
   import subprocess, os
   result = subprocess.run(
       ["node", os.path.join(os.environ["USERPROFILE"], ".deepchat", "skills", "system", "scripts", "skill-hygiene.js")],
       check=False
   )
   # Must exit with code 0
   print(f"Exit code: {result.returncode}")
   ```

### DeepChat Startup Integration

**Option A: Windows Task Scheduler (Recommended)**
```python
import subprocess, os
skill_hygiene_path = os.path.join(os.environ["USERPROFILE"], ".deepchat", "skills", "system", "scripts", "skill-hygiene.js")
subprocess.run([
    "schtasks", "/create", "/tn", "DeepChat-SkillHygiene",
    "/tr", f"node {skill_hygiene_path}",
    "/sc", "onlogon",
    "/it",
    "/f"
], check=True)
```

**Option B: Manual Pre-Session Check**
At the start of any session involving skill modifications, the agent should run `skill-hygiene.js` and report results.

**Option C: Audit Log Review**
Check the latest audit report:
```python
import json, os
from pathlib import Path

report_path = Path(os.environ["USERPROFILE"], ".deepchat", "audit", "skill-hygiene-latest.json")
if report_path.exists():
    print(json.dumps(json.loads(report_path.read_text(encoding="utf-8")), indent=2))
```

### Anti-Patterns (Skill Hygiene)

| Anti-Pattern | Detection | Fix |
|:-------------|:----------|:----|
| Editing skills in stale location | `skill-hygiene.js` exit 1 | Move edits to canonical, delete stale |
| SKILL.md-only sync | R2 missing scripts/templates | Use `skill-sync.js` for full sync |
| Forgetting rwnq8 push | `git log rwnq8/master` behind | `git push rwnq8 master` |
| Creating skills in AppData | `skill-hygiene.js` exit 1 | Only create in `%USERPROFILE%\.deepchat\skills\` |
| Manual token copy | Truncated tokens cause auth | Use `os.environ["TOKEN_NAME"]` directly |

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — MANDATORY)

Claiming a setting is "changed", a skill is "deployed"/"synced", or a
desktop action is "done" without an invoked tool call showing evidence in
this turn is a PHANTOM CLAIM (`qnfo-core` §9.11 Rule 14) — BLOCKED.

1. **Settings changes** — call the actual `deepchat_settings_*` tool and confirm the returned value matches the requested change; do not assert a setting changed without the tool's confirmed return value.
2. **Skill deploy/sync** — a `git push`/R2 `object put` script's exit code 0 is NOT sufficient. Independently re-read back all 3 layers in this turn: `os.path.exists` (disk), `git log -1 --oneline` on the skill's own commit (GitHub), AND `npx wrangler r2 object get qnfo-skills/prompts/skills/<name>/SKILL.md --remote` (R2) — compare content, not just presence.
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
version: "2.6"
triggers: ["keyword1", "keyword2", ...]
related: ["other-skill"]
priority: 0-3
platform: all | cloudflare | local
autonomous: true | false
self_sufficient: true
---

# SKILL TITLE — v1.0

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
2. **Verifiable:** Every workflow step produces tool evidence (os.path.exists, git log, exec output).
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
   ```python
   import subprocess
   subprocess.run(["git", "add", "-A"], check=True)
   subprocess.run(["git", "commit", "-m", "skill: <name> v<version>"], check=True)
   subprocess.run(["git", "push", "origin", "master"], check=True)
   subprocess.run(["git", "push", "rwnq8", "master"], check=True)
   ```
3. **R2:** Upload ALL files (not just SKILL.md):
   ```python
   import subprocess, os
   subprocess.run(
       ["node", os.path.join(os.environ["USERPROFILE"], ".deepchat", "skills", "system", "scripts", "skill-sync.js")],
       check=True
   )
   ```
4. **Verify:** All layers have identical content

### Verification
```python
import subprocess, os
from pathlib import Path

# Check local
skill_path = Path(os.environ["USERPROFILE"], ".deepchat", "skills", "<name>", "SKILL.md")
print(f"Local exists: {skill_path.exists()}")

# Check GitHub (both remotes)
subprocess.run(["git", "log", "-1", "--oneline", "origin/master"], check=True)
subprocess.run(["git", "log", "-1", "--oneline", "rwnq8/master"], check=True)

# Check R2
subprocess.run([
    "npx", "wrangler", "r2", "object", "get", "qnfo-skills",
    "prompts/skills/<name>/SKILL.md", "--remote"
], check=True)
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
(which enables autonomous skill discovery) is inside qnfo-core's body — but
qnfo-core must be explicitly loaded via `skill_view` for the table to be active.
Without loading qnfo-core first, the LLM cannot discover which skill to use.

### The Solution

Three-layer automatic initialization:

**Layer 1: Windows Startup (Automatic)**
- `deepchat-skill-hygiene.vbs` in Windows Startup folder
- Runs `skill-hygiene.js` silently at every Windows logon
- Logs results to `%USERPROFILE%\.deepchat\audit\startup-hygiene.log`
- Location: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`

**Layer 2: /init Custom Prompt (User-Triggered)**
- Type `/init` in DeepChat to initialize session
- Executes: `skill_view("qnfo-core")` + `skill_view("system")` + `skill-hygiene.js`
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
This loads qnfo-core + system and runs hygiene check.

**Option B: Direct Skill Loading**
```
skill_view("qnfo-core")  # Load safety-net core with trigger table
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
```python
import os, json
from pathlib import Path

# Check startup script exists
startup_path = Path(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "deepchat-skill-hygiene.vbs")
print(f"Startup script exists: {startup_path.exists()}")

# Check /init prompt exists
prompts_path = Path(os.environ["APPDATA"], "DeepChat", "custom_prompts.json")
if prompts_path.exists():
    prompts = json.loads(prompts_path.read_text(encoding="utf-8"))
    init_found = any(v.get("id") == "init-session" for v in prompts.values())
    print(f"/init prompt exists: {init_found}")

# Check startup log
log_path = Path(os.environ["USERPROFILE"], ".deepchat", "audit", "startup-hygiene.log")
if log_path.exists():
    lines = log_path.read_text(encoding="utf-8").splitlines()
    for line in lines[-5:]:
        print(line)
```

---

## Reusable Scripts

### Skill Hygiene Audit
```python
import subprocess, os
result = subprocess.run(
    ["node", os.path.join(os.environ["USERPROFILE"], ".deepchat", "skills", "system", "scripts", "skill-hygiene.js")],
    check=False
)
# Exit 0 = clean, Exit 1 = stale locations, Exit 2 = version conflicts
print(f"Exit code: {result.returncode}")
```

### Full Skill Sync (All Files)
```python
import subprocess, os
subprocess.run(
    ["node", os.path.join(os.environ["USERPROFILE"], ".deepchat", "skills", "system", "scripts", "skill-sync.js")],
    check=True
)
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

*system v2.9 — DeepChat configuration, skill ecosystem management, skill location hygiene, session initialization, desktop automation, and exec shell mandate.*


## Auto-Restart Protocol (2026-08-02) — DeepChat quit + restart when needed

DeepChat builds its skill index from `agent.db` at **startup only**. Skills
created, deleted, or bulk-modified on disk stay invisible / phantom / stale
until a restart. (memory: new skill invisible until restart; deleted platform
skills auto-restore; stale agent.db cache masquerades as frontmatter errors.)

**AGENT SAFETY (MANDATORY):** Never kill DeepChat mid-turn — it terminates the
agent and loses session state. Use the DEFERRED restart path below.

### Scripts (system skill)

| Script | Purpose |
|:-------|:--------|
| `scripts/schedule-restart.py` | **AGENT-SAFE**: register a one-shot delayed task that restarts DeepChat after the session ends. `python schedule-restart.py --delay 60` (default 60s). |
| `scripts/restart-deepchat.py` | Graceful quit (WM_CLOSE) + wait + relaunch. For **user/manual** restarts, or when DeepChat is closed. `python restart-deepchat.py --grace 20 --force`. |
| `scripts/cancel-restart.py` | Cancel a pending deferred restart. `python cancel-restart.py`. |

### When to trigger a restart

| Condition | Action |
|:----------|:-------|
| NEW skill created | `schedule-restart.py --delay 60`, tell user "restarting in 60s to load new skill" |
| Skill DELETED | `schedule-restart.py`, then re-delete any auto-restored platform skill after relaunch |
| Bulk skill edits (kaizen) | `schedule-restart.py --delay 60` |
| Skills fail to load despite valid YAML | suspect stale agent.db cache → `schedule-restart.py` (memory: restart clears indexer cache) |
| agent.db / DIPS locked | cannot checkpoint live; restart clears WAL — schedule it, do NOT force |

### Manual restart (user)

```
python "%USERPROFILE%\.deepchat\skills\system\scripts\restart-deepchat.py"
```

### Verify after restart

1. `skill_list` — confirm the new/modified skill appears, deleted skill gone.
2. `skill_view <name>` — confirm SKILL.md loads with current version.
3. If a platform-default skill was auto-restored, re-delete it (memory: platform
   auto-restores deleted defaults; must be re-deleted after purge).


## DeepChat Restart Protocol (v2.6, 2026-08-02) — MANDATORY

**DeepChat scans skillsPath + settings at startup only.** Skills added, deleted,
consolidated, or edited on disk are INVISIBLE until a restart. agent.db also
caches the skill index — stale entries persist until restart (and in rare cases
need a cache clear, see memory "stale agent.db cache"). Some operations require
DeepChat CLOSED (e.g. `agent_db_prune.py --vacuum`).

**Canonical helper:** `python "{{SKILL_ROOT}}\scripts\restart-deepchat.py" --delay 20 --reason "<why>"`
The script detaches itself, waits 20s (lets the current turn finish), gracefully
closes DeepChat, waits for exit (force-kills if needed), relaunches DeepChat.exe,
and logs to `~/.deepchat/restarts.log`. A `pending-restart.json` marker is written
so the next boot's session-init can verify + clear the reason.

**WHEN to auto-restart (call the helper):**
1. **After creating/editing/deleting any skill** (skill-creator, consolidation,
   kaizen edits, deprecation banners) — otherwise the change is invisible until
   a manual restart.
2. **After changing DeepChat settings** (theme, MCP config, etc.) that require
   a reload (deepchat-settings skill).
3. **After agent.db pruning** (memory-management / bloat-cleanup) — especially
   `--vacuum`, which requires DeepChat CLOSED.
4. **When skills fail to load after a restart** — clear the stale agent.db
   skill-index cache (process restart alone may not clear it), then restart again.

**POST-RESTART VERIFICATION (session-init, this skill):**
- On boot, check `~/.deepchat/pending-restart.json`. If present: log the reason,
  clear the marker, confirm the restart completed.
- If skills are still missing after restart: the agent.db skill-index cache is
  stale — clear it (see memory heuristic) and restart once more.

**SAFETY:** the helper verifies the target is DeepChat.exe, detaches itself so it
survives the kill, and defaults to a 20s delay so the current turn completes.
Do NOT force-kill DeepChat from within an agent turn — always use the helper.


## EXEC SHELL MANDATE — CMD.EXE ONLY (v2.9, 2026-08-03)

**The DeepChat `exec` tool uses `cmd.exe`. It does NOT use PowerShell.**

### Root Cause (Source-Level Fix)

DeepChat's source (`ThinkInAIXYZ/deepchat`, package `@nicepkg/deepchat` v1.1.0-beta.11)
in `src/main/agent/shared/process/shellEnvHelper.ts`:

```typescript
export function getUserShell(): { shell: string; args: string[] } {
  if (platform === 'win32') {
    const powershell = process.env.PSModulePath ? 'powershell.exe' : null
    if (powershell) {
      return { shell: powershell, args: ['-NoProfile', '-Command'] }
    }
    return { shell: 'cmd.exe', args: ['/c'] }  // ← WE WANT THIS
  }
}
```

**PSModulePath SET → PowerShell. PSModulePath UNSET → cmd.exe.**
DeepChat bundles its own PS modules into `process.env.PSModulePath` at launch,
so registry deletion alone is insufficient. **The fix is a Python shim v3 at
`C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`** that strips the 3
UTF8Encoding preambles and forwards the real command to `cmd.exe /c`.

**REPRODUCIBILITY:** Complete step-by-step guide (shim source, PyInstaller compile,
winreg PATH fix — NEVER setx, verification, troubleshooting) at `EXEC-SHELL-FIX.md`
in this skill's root directory. Recompile if lost:
`pyinstaller --onefile --name powershell _ps_shim.py` (source in EXEC-SHELL-FIX.md).

**Verification (session start):**
1. `git --version` → shows `git version 2.49.0` (NOT empty exit-0 — empty means shim v2 bug)
2. `echo test` → prints `test`
3. `npm --version` → works directly (no .ps1 wrapper blocking)

**CRITICAL:** If commands return exit 0 with NO output, the shim is v2 (eats commands).
Recompile v3. Never use `setx` for PATH — it truncates at 1024 chars; use winreg REG_EXPAND_SZ.

**Docs:** `deepchat-internals.md` (14 sections), `SESSION_LOG_POWERSHELL_EXTERMINATION.md`,
`EXEC-SHELL-FIX.md`. Cross-ref: windows-command-patterns v3.20 §S-1.0.2.
Current: **2.14** (system — skill-sync v4.0.11 remediation: gitOk false-success fix + SYNC-DIVERGENCE-MERGE-1 (merge-not-rebase) + PROMPT-STORE-4STORE-1 parity; 2026-08-12) (system — nomenclature — N-2 nomenclature: H1 version-header delimiter standardized from -- to — (em-dash); version line added; 2026-08-04)


