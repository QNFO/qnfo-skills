---
name: bloat-cleanup
description: Automated Windows system bloatware cleanup, disk decluttering, and DeepChat thin-client compliance enforcement. Use when the user wants to clean up disk space, remove bloatware, kill vampire processes, disable unnecessary services, run system audits across all drives, enforce DeepChat KIF-32 thin-client mandate by detecting and cleaning local project files, purge caches/temp files/browser junk/npm caches, or optimize a Windows laptop for DeepChat performance by freeing RAM and CPU.
version: 3.5
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


> **v3.5 UPDATE (2026-08-12, kaizen — CMD SKILLS UPDATE: FRONTMATTER-HARD-1 duplicate version keys):**
> Red-team: direct parent-agent 5-adversary audit (CMD SKILLS UPDATE — session this). HARD: 1. SOFT: 0. DESIGN: 0.
> Changes:
> (1) [HARD] **Duplicate `version:` YAML keys removed** — the frontmatter had `version: 3.4` three times
>     (lines 3, 15, 17), a YAML parse-breaking defect that would fail any strict frontmatter parser.
>     Kept the first occurrence, removed the two strays after the triggers list. Header bumped to v3.5
>     for N-2 consistency (header/frontmatter/file-title triple).
> Cross-reference: kaizen v2.31, system v2.14.

# BLOAT CLEANUP — v3.5

> **v3.4 UPDATE (2026-08-06, kaizen — CUA tools integration for GUI cleanup + stale cross-ref fix):**
> Red-team: direct parent-agent 5-adversary audit (session QPBAVeVkU0Y5qkMNG6CC9 — CONTINUE
> deferred SOFT item from kaizen v1.66 closeout). HARD: 0. SOFT: 2. DESIGN: 1. Changes:
> (1) [SOFT] **CUA tools reference added** — Widgets Settings GUI fallback now references
>     DeepChat Computer Use (CUA) tools (`list_apps` → `launch_app` → `get_window_state` →
>     `click`/`type_text`) as a programmatic GUI automation path for Settings dialogs,
>     app uninstall, and other GUI-only operations. Load `computer-use` skill for full CUA
>     protocol.
> (2) [SOFT] **Stale cross-references fixed** — windows-command-patterns v3.13→v3.16,
>     kaizen v1.31→v1.66 in Runtime Context and Self-Elevation references.
> (3) [DESIGN] **GUI automation pattern documented** — same pattern as WCP v3.16:
>     CUA tools provide a programmatic alternative to "or use the Settings GUI" fallback
>     text found throughout the skill.
> Cross-reference: windows-command-patterns v3.16, kaizen v1.66, computer-use skill,
> session QPBAVeVkU0Y5qkMNG6CC9.

>> **v3.3 UPDATE (2026-08-05, kaizen — TEMP stale-clone scan + STALE-CLONE-ACCUM-1):**
> Red-team: kaizen red-team skills audit (session -WyivBiyZ6xFy4uXS_RNy).
> HARD: 0. SOFT: 1. DESIGN: 1. Changes:
> (1) [DESIGN] **thin_client.py v2.7 — %TEMP% stale-clone scan** — new STALE_CLONE
>     category scans %TEMP% for qnfo-*/repo-pattern dirs and any dir containing .git.
>     Prior sessions left 52 stale clones (156.7 MB) invisible to the old scan.
>     Verified: scan found 52, all deleted, audit fully clean.
> (2) [SOFT] **Cross-reference** — STALE-CLONE-ACCUM-1 documented in git-github v2.20;
>     every temp clone MUST use the force_rmtree pattern (chmod-sweep + \\?\ prefix).
> Cross-reference: git-github v2.20, kaizen v1.45, session -WyivBiyZ6xFy4uXS_RNy.

> **v3.2 UPDATE (2026-08-05, kaizen — Edge background/startup policies + Widgets MDM + TrustedInstaller lesson):**
> Red-team: session VBvCOsXhzlQJUubBqtdFz — bloat extermination live-fire test:
> Edge background mode + startup boost disabled via HKLM/HKCU Group Policy;
> Edge auto-launch `MicrosoftEdgeAutoLaunch_*` deleted from HKCU\Run;
> Widgets permanently disabled via PolicyManager MDM path (`AllowNewsAndInterests=0`);
> Office ClickToRun set to DEMAND_START via `sc`.
> HARD: 0. SOFT: 4. DESIGN: 1.
> Changes:
> (1) [SOFT] **Edge policies documented** — `BackgroundModeEnabled` + `StartupBoostEnabled`
>     registry keys (HKLM+HKCU, `REG_DWORD 0`); auto-launch deletion from HKCU\Run.
> (2) [SOFT] **Widgets MDM policy path** — `HKLM\SOFTWARE\Microsoft\PolicyManager\default\NewsAndInterests\AllowNewsAndInterests`
>     = 0 is the only working registry path; TrustedInstaller blocks Dsh and ACL blocks Feeds.
> (3) [SOFT] **TrustedInstaller/key-owner gap** — documented that TrustedInstaller-protected
>     registry keys (HKLM\Dsh, HKCU\Feeds) CANNOT be written even with admin elevation.
>     PolicyManager MDM path is the fallback. Don't waste tool calls on icacls/takeown.
> (4) [SOFT] **Self-elevation via ShellExecute runas** — documented `ctypes.windll.shell32.ShellExecuteW`
>     as the canonical UAC elevation pattern (cross-ref: windows-command-patterns v3.13 §S-1.0.8).
> (5) [DESIGN] **kill_bloat.py targets expanded** — now includes Edge auto-launch deletion.
> Cross-reference: windows-command-patterns v3.13 §S-1.0.8, kaizen v1.31, session VBvCOsXhzlQJUubBqtdFz.

> **v3.1 UPDATE (2026-08-02, kaizen — Thin-Client Enforcement Protocol):**
> Red-team: KIF-32 thin-client mandate audit found local-only files (stale git clones,
> unarchived research deliverables, ephemeral build scripts) surviving session closeout
> in violation of "local files are never canonical." This version adds enforcement gates:
> (1) [HARD] **Thin-Client Enforcement Protocol** — post-closeout scan that flags every
>   file present ONLY locally (not in canonical git, not in R2). Files must be synced
>   to canonical + deleted locally, or user-approved as permanent ephemeral workspace.
> (2) [HARD] **Pre-Closeout Scan** — list all local-only files by category (stale clones,
>   unarchived deliverables, orphaned git repos, temp scripts). Any category > 0 = BLOCK.
> (3) [HARD] **Mandatory Cleanup Gate** — after R2 archive confirmation (SHA-256 verified
>   round-trip), delete ALL local copies of archived project files per KIF-32. No
>   lingering local copies of published papers, art configurations, or research deliverables.
> (4) [SOFT] **Stale Clone Detection** — any git clone whose HEAD differs from origin
>   master → flag as thin-client violation. Delete after confirming origin has the work.
> (5) [DESIGN] Canonical case: D:\qnfo-skills — a 5.1MB git clone of QNFO/qnfo-skills
>   with diverged HEAD (160f9da vs canonical e7b7f9c, 5 commits behind), stale prompts/
>   skills/ layout, missing kaizen/ directory. Survived multiple session closeouts as
>   a local-only artifact until force-deleted via bloat-cleanup v3.1 enforcement.

## Thin-Client Enforcement Protocol (NEW — HARD, KIF-32)

**Per mandate: LOCAL FILES ARE NEVER CANONICAL.** The canonical source of truth is the
GitHub repository (git) + Cloudflare R2 (durable backup). Any file that exists ONLY
locally — not in git, not in R2 — is a thin-client violation.

### Pre-Closeout Scan (HARD — blocks closeout)

Before ANY session closeout or research phase completion, enumerate ALL local-only files:

1. **Git repositories** — `git status`, `git log`, `git ls-remote` on every local git dir.
   Flag any clone whose HEAD differs from origin/master (stale clone violation).
2. **Project directories** — scan all known project roots (D:\ODR, C:\Users\...\Documents\GitHub,
   C:\Users\...\.deepchat\artifacts) for files NOT tracked in git or synced to R2.
3. **Research deliverables** — papers, PDFs, notebooks, datasets that are published on
   Zenodo but still exist locally.
4. **Ephemeral scripts** — build helpers, audit scripts, merge scripts that served their
   purpose in a completed session.
5. **Orphaned git repos** — clones in temp directories, stale checkouts.

| Category | Action |
|:---------|:-------|
| Stale clone (diverged HEAD) | Confirm origin has the work → delete local clone |
| Unarchived deliverable | R2 archive + SHA verify → delete local copy |
| Orphaned git repo | Push to remote or confirm already-pushed → delete |
| Ephemeral script | Served its purpose → delete (already in git history if committed) |
| Permanent ephemeral workspace | User must explicitly approve — flag as [THIN-CLIENT-EXEMPT] |

### Mandatory Cleanup Gate (HARD)

After the pre-closeout scan completes:
1. **Sync all deliverable artifacts to R2** — papers (.md, .pdf, .html), notebooks,
   datasets — to `qnfo-releases/releases/<YYYY>/<MM>/<slug>/`.
2. **Verify R2 round-trip** — SHA-256 must match between local and R2 object.
3. **Delete local copies** of ALL R2-verified files. R2 IS the canonical storage.
4. **Verify post-cleanup** — re-run scan, confirm zero local-only files in the
   archive target paths.

**GATE:** If any paper/deliverable/repo remains local-only after closeout → HARD BLOCK.
Session must not be declared complete until the scan passes.

### Anti-Patterns (NEW rows for thin-client enforcement)

| Anti-Pattern | Fix |
|:-------------|:----|
| **Stale git clone surviving multiple session closeouts** | Pre-closeout scan → `git fetch` + `git log --oneline -1` → compare to `git ls-remote origin master`. If diverged: delete clone. Canonical case: D:\qnfo-skills (5.1MB, HEAD 160f9da vs canonical e7b7f9c, 5 commits behind, survived 3+ sessions). |
| **Published research paper still on local disk** | Zenodo DOI published → R2 archive qnfo-releases/ → SHA verify → `os.remove()` local copy. Paper is published; local copy is a thin-client violation. |
| **Ephemeral build/audit scripts left in artifacts directory** | After session complete: delete `_*.py` build helpers, audit runners, merge scripts. Deliverables (papers, skill updates) are archived separately. |
| **Closing a session with local-only files not synced to canonical layer** | Run Pre-Closeout Scan. Zero local-only files before declaring complete. |
| **Trusting file existence as proof of canonical status** | File existence ≠ canonical. Check git (`git ls-files`, `git log`) and R2 (`GET /objects/{key}`). File must exist in at least one canonical layer OR be ephemeral. |


> **v3.0 UPDATE (2026-08-02, kaizen — lossy-vs-acceptable criteria + unified scope):**
> Red-team: user audit of the research v2.46 de-bloat (2,022→531 lines, 75% reduction)
> challenged: "how is it possible to lose 1,500 lines and retain all functionality?"
> Answer: a skill is TWO content classes — executable protocol (must never shrink) and
> accumulated metadata (safe to reduce). This version codifies the distinction as a
> mandatory pre-de-bloat classifier:
> (1) [HARD] **Bloat Reduction Techniques taxonomy** — 7 techniques (Collapse, Remove,
>   Relocate, Archive, Merge, Compress, Supersede) with per-technique loss profile.
> (2) [HARD] **Lossy vs Acceptable criteria** — two-class, five-criterion classifier.
>   ACCEPTABLE (zero-information-loss): Redundancy, Supersession, Historical narrative,
>   Encoded lessons, Relocatable reference. LOSSY (positive information, MUST retain):
>   Live constants, Live gates/checklists, Current tool wiring, Recent anti-patterns,
>   Canonical cases.
> (3) [HARD] **Unified scope** — the criteria apply identically to filesystem bloat
>   (OS/disk/caches/services) AND skill bloat (SKILL.md directories, contents,
>   instructions). Same techniques, same loss classifier, same gates.
> (4) [SOFT] **Behavior-preservation audit gate** — before declaring ANY de-bloat
>   complete, verify every live constant/endpoint/gate/wiring survives verbatim.
>   Missing item = lossy, restore it. Canonical pattern: _behavior_audit.py
>   (research v2.46 audit: 48/49 active, 1 correctly-superseded, 0 lost).
> (5) [DESIGN] Conditional-entropy framing — bloat = content whose conditional entropy
>   is ZERO given the rest of the document (reconstructible or superseded); entropy =
>   unique information nothing else carries. Removing entropy = data loss.

## Bloat Reduction Techniques (NEW — HARD)

| # | Technique | Operation | Loss Profile | Example |
|:--|:----------|:----------|:-------------|:--------|
| T1 | **Collapse** | N→1 consolidation | Zero IF consolidated content preserved | 22 version banners → 1 |
| T2 | **Remove** | Delete dead content | Zero IF supersession confirmed | Deleted-script references |
| T3 | **Relocate** | Move to references/ | Zero IF pointer resolves | 37-field Zenodo dictionary |
| T4 | **Archive** | Move to deploy/history/ | Zero at storage; execution-time loss possible if referenced content was needed live | Full v2.45 research |
| T5 | **Merge** | Deduplicate | Zero IF merged text retains full content | 4× Anti-Phantom → 1 umbrella |
| T6 | **Compress** | Shorten prose | POTENTIALLY LOSSY — narrative only, never constants/instructions | Copyediting |
| T7 | **Supersede** | Replace with newer | Zero + improvement IF new content complete | XeLaTeX → build-pdf-pro.py |

## Lossy vs Acceptable Criteria (NEW — HARD)

### ACCEPTABLE — zero-information-loss, safe to reduce

| Criterion | Definition | Test |
|:----------|:-----------|:-----|
| **Redundancy** | Content duplicated ≥2× in same document | Remove N-1 copies; information preserved elsewhere |
| **Supersession** | Explicitly replaced by newer content | Old content is wrong guidance if followed |
| **Historical narrative** | Changelog/version banners, not instructions | No agent behavior depends on it |
| **Encoded lessons** | Anti-patterns whose corrective behavior is now a live gate | The gate is the living instruction |
| **Relocatable reference** | Data better as a file than inline | Pointer resolves to preserved content |

### LOSSY — positive information, MUST retain

| Criterion | Definition | Violation Example |
|:----------|:-----------|:-----------------|
| **Live constants** | Endpoints, scopes, error strings, paths (verbatim) | Removing an API endpoint from active guidance |
| **Live gates/checklists** | Anything that BLOCKS an action | Deleting a HARD gate |
| **Current tool wiring** | Script paths, canonical pipeline | Removing build-pdf-pro.py reference |
| **Recent anti-patterns** | Failure modes last 12 months, still active | Archiving a live warning |
| **Canonical cases** | "Why this gate exists" narratives for ambiguity | Dropping the Compton-BT silo case |

**OPERATIONAL TEST:** line count is the wrong metric. Behavior preservation is the test:
1. Constant audit — every live constant survives verbatim?
2. Gate audit — every HARD gate present?
3. Phase/instruction audit — every executable step runnable from the active file?
4. Recovery path — full prior version archived for reconstruction?

**GATE:** if any live constant/gate/wiring is missing from the active file → LOSSY, restore before declaring de-bloat complete.

## Unified Scope (NEW — HARD)

The criteria apply to BOTH:

**A. Filesystem bloat** (v1.0-v2.8 scope): OS bloatware, disk clutter, caches, vampire processes, services, npm caches. Techniques: Remove (T2), Archive (T4), Merge (T5).

**B. Skill bloat** (v2.0+ scope): SKILL.md directories, contents, and instructions.
- Directories: orphaned skill dirs, stale scripts, duplicate references
- Contents: version banners, duplicate mandates, historical pipelines, anti-pattern graveyards, oversized spec tables
- Instructions: superseded tooling, deleted-script references, deprecated endpoints
- Techniques: all 7 apply (Collapse T1, Remove T2, Relocate T3, Archive T4, Merge T5, Compress T6, Supersede T7)

**Same classifier, same gates, both scopes.**

## Behavior-Preservation Audit Gate (NEW — SOFT)

Before declaring ANY de-bloat complete:
1. Enumerate every live constant, gate, endpoint, script path, and error string in the PRE-de-bloat version.
2. Check each survives verbatim in the POST-de-bloat version.
3. Any missing item → classify: Acceptable (superseded/relocated/encoded) or Lossy (restore).
4. Only when 100% of live items are present or provably-superseded → de-bloat complete.
5. Evidence: audit script output saved to artifacts/ (canonical pattern: _behavior_audit.py → 48/49 active, 1 correctly-superseded, 0 lost).

## execute_plan (v3.0 update)

update_plan([
  {"step": "Scan bloat (filesystem + skills): measure bloat_ratio, enumerate live constants/gates", "status": "pending"},
  {"step": "Classify each reduction target: Acceptable (5 criteria) vs Lossy (5 criteria)", "status": "pending"},
  {"step": "Apply techniques: Collapse/Remove/Relocate/Archive/Merge/Compress/Supersede", "status": "pending"},
  {"step": "Run behavior-preservation audit — 100% live items present or provably-superseded", "status": "pending"},
  {"step": "Archive full prior version, sync to R2, verify round-trip", "status": "pending"},
])


> **v2.9 UPDATE (2026-08-02, kaizen — Skill-Space De-Bloat extension):**
> Adds the Skill-Space De-Bloat protocol for SKILL.md files themselves (distinct from
> OS/disk bloat). Canonical case: research skill v2.45→v2.46 (2,022→531 lines, 75%
> reduction, core pipeline preserved, bloat_ratio ~0.60→~0.05). Bloat categories:
> version banners (>3 → collapse), deleted-script refs (>0 → remove), duplicate mandates
> (>1 copy → umbrella), historical pipelines (>1 gen → HISTORY.md), anti-pattern rows
> (>50 → trim to 12 months), specification tables (>1 page → references/ file).
> bloat_ratio formula: (banner_lines + deleted_ref_lines + duplicate_mandate_lines +
> historical_pipeline_lines + archived_antipattern_rows×3) / total_lines. Threshold >0.30
> → de-bloat required. De-bloat removes ONLY non-executable metadata; executable pipeline
> (phases, gates, protocols) preserved byte-for-byte. Archive full prior version to
> deploy/history/ before replacing SKILL.md. Sync de-bloated skill to R2 + verify round-trip.

## Skill-Space De-Bloat (NEW — HARD)

### Bloat Categories & Thresholds

| Category | Threshold | Research v2.45 case | Remediation |
|:---------|:----------|:--------------------|:------------|
| Version banners | >3 | 22 (~400 lines) | Collapse to latest + 1-line prior link → HISTORY.md |
| Deleted-script refs | >0 | 5 scripts | Remove; cross-ref living scripts only |
| Duplicate mandates | >1 copy | 4× Anti-Phantom Gate | 1 umbrella section + per-phase cross-refs |
| Historical pipelines | >1 gen | 3 PDF pipelines | Retire to HISTORY.md; keep canonical only |
| Anti-pattern rows | >50 | ~80 | Trim to last 12 months; archive rest |
| Specification tables | >1 page | 37-field Zenodo dict | Move to references/ file |
| Executable protocol | — | ~800 lines core | KEEP — never remove executable pipeline |

### De-Bloat Protocol

1. Measure: compute bloat_ratio per formula below.
2. Categorize: map every non-executable line to a bloat category.
3. Remediate: collapse/remove/archive per table above.
4. Verify: re-measure; target bloat_ratio < 0.30; executable core intact.
5. Archive: write deploy/history/ with full prior content.
6. Sync: version-bump + R2 upload (`qnfo/prompts/skills/<name>/SKILL.md`).
7. Verify round-trip: download from R2, compare hash.

### bloat_ratio Formula (DESIGN)

```
bloat_ratio = (version_banner_lines + deleted_ref_lines + duplicate_mandate_lines
               + historical_pipeline_lines + archived_antipattern_rows×3) / total_lines
```
Threshold: >0.30 → de-bloat required. Research v2.45: ~0.60 (bloated) → v2.46: ~0.05 (clean).

### Canonical Case — Research Skill v2.45→v2.46 (2026-08-02)

| Metric | v2.45 (before) | v2.46 (after) | Δ |
|:-------|:---------------|:--------------|:--|
| Total lines | 2,022 | 531 | **-75%** |
| Version banners | 22 | 1 | -21 |
| Anti-pattern rows | ~80 | 21 | -59 |
| Deleted-script refs | 5 | 0 | -5 |
| Duplicate mandates | 4× | 1× | -3 |
| bloat_ratio | ~0.60 | ~0.05 | -0.55 |
| Core pipeline | ~800 lines | ~800 lines | **0 (intact)** |
| KIF-29 HARD upgrade | absent | present | +1 gate |

**Lesson:** De-bloat removes ONLY non-executable metadata. The executable pipeline
(Phases 0-8, gates, protocols) is preserved byte-for-byte. Version history moves to
deploy/history/, never deleted.



> **v2.8 UPDATE (2026-08-02, kaizen — restart automation):**
> [HARD] agent_db_prune --vacuum requires DeepChat CLOSED. Use the restart
> helper to close + relaunch: `python "<system>\scripts\restart-deepchat.py" --delay 5 --reason "agent.db VACUUM"`.
> Also after pruning the agent DB, schedule a restart so the skill index is
> rebuilt. Cross-reference: system v2.6, memory-management v1.1.



> **v2.7 UPDATE (2026-08-02, kaizen — script retirement + deep-bloat audit):**
> [HARD] **DEPRECATED SCRIPTS REMOVED (user mandate).** All 5 legacy Windows
> admin scripts (admin_watcher, trigger_admin, manage_watcher, quick_optimize,
> system_tune) have been DELETED — the retired runtime and its version 7 are
> fully removed from QNFO operations (Python-first only, cloudflare KIF-59).
> Admin-required ops (service disable, AppX, Defender exclusions, DNS) route
> through Python scripts with admin-queue messaging. No legacy runtime
> cmdlets, script files, or interpreter invocations are permitted anywhere.
> [SOFT] **AGENT DB PRUNE — LIVE MEMORY SAFEGUARD.** Dry-run on a production
> 1.8 GB agent.db returned "No unpinned sessions older than 7 days" — the DB
> is LIVE AGENT MEMORY (12,353 agent_memory rows), NOT pruneable history.
> DO NOT force --max-age-days/--target-db-size-gb on an active agent.db.
> Only session/turn history is pruneable. VACUUM requires DeepChat closed.
> [SOFT] **HIDDEN DATA STORES.** .wrangler/ in skills tree is gitignored
> (0.0 MB, Cloudflare cache) — harmless. skills .git benefits from `git gc`
> (35.5 -> 9.9 MB). Stale AppData/Roaming/.deepchat/skills (8 outdated)
> confirmed GONE. system/SKILL.md lives ONLY at .deepchat/skills/system/.
> [SOFT] **MCP CLEANUP.** Buffer MCP token in mcp-settings.json was STALE
> (HTTP 401, ...6JGD vs documented ...14Ky) — fixed + backup. LinkedIn MCP
> stores LINKEDIN_PASSWORD + LINKEDIN_COOKIE plaintext (documented linkedin-mcp
> pattern) — rotate if config exposure is a concern.
> Cross-reference: windows-command-patterns v2.4, cloudflare v3.19, research v2.45.


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
    +-- full_clean.py         # Orchestrator: runs all 10 phases
 + "`" + @"
**Two-tier service management:**
1. **Static (legacy):** `disable_services.py` — fixed hardcoded list. Used as a safety baseline.
2. **Dynamic (★ preferred):** `audit_services.py` → `dynamic_disable.py` — runtime heuristic classification with no fixed list. Discovers all 284+ services, classifies by vendor/pattern/state, generates targets dynamically.

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

**★ Dynamic service audit** (read-only, no admin required):
```
skill_run bloat-cleanup scripts/audit_services.py
```
Discovers all services and classifies them as `essential`, `bloat`, `suspicious`, `user_installed`, or `unknown`. Shows actionable targets with rationale. **Always run this first** before making service changes.

**★ Dynamic service disable** (admin required for `--apply`):
```
# Dry-run (default — see what would be disabled):
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
> ⚠️ **ADMIN REQUIRED.** This script manages Windows services (stop, startup=disabled, recovery clear).
> Running without admin will show "SKIP (may need admin)" for all services and make no changes.
> To run as admin, open an elevated Command Prompt and execute:
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

### audit_services.py ★ NEW (KIF-40)
**Dynamic runtime service analysis** — replaces the hardcoded `BLOAT_SERVICES` list with heuristic classification. Queries all ~284 services via `Get-CimInstance Win32_Service` and classifies each as:

| Classification | Description | Action |
|---|---|---|
| `essential` | Critical OS services (RpcSs, DcomLaunch, WinDefend, etc.) | Never touch |
| `bloat` | High-confidence bloatware (Lenovo, Dolby, search indexing, telemetry) | Safe to disable |
| `bloat_stopped` | Bloat that's currently stopped (low priority) | Flag for cleanup |
| `suspicious` | Third-party auto-start, no clear purpose | Review before disabling |
| `user_installed` | Known apps (MySQL, Docker, Steam, Discord, etc.) | User decides |
| `inactive` | Stopped + Manual/Disabled — dormant | Ignore |
| `unknown` | No heuristic match | Investigate |

**Classification rules (in priority order):**
1. **Critical OS safelist** — 60+ essential services never flagged
2. **Vendor patterns** — Lenovo, Dolby, Elevoc, Adobe, Google updaters
3. **Windows bloat patterns** — WSearch, DiagTrack, DusmSvc, WpnService, CDPSvc, PcaSvc, StiSvc, FontCache
4. **Feature bloat** — Xbox, OneDrive, Office ClickToRun
5. **Third-party auto-start** — services with Auto start, Running, but no Microsoft/Windows in display name → `suspicious`
6. **User software detection** — MySQL, PostgreSQL, Docker, Steam, Discord, etc.

**Read-only, no admin required.** Always run this first.

### dynamic_disable.py ★ NEW (KIF-40)
**Dynamic target generation + disable** — consumes the same classification rules as `audit_services.py` to generate a target list at runtime, then disables services.

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

Critical: clears `sc.exe failure` auto-recovery actions to prevent Windows auto-restart. The red-team audit from 2026-07-27 confirmed 4 services restarted when only taskkill was used — this script fixes that root cause.

> **WARNING — `sc.exe` invocation (KIF-05 class):** The correct invocation is
> `cmd /c 'sc.exe failure "WSearch" reset= 86400 actions= ""'` (note: `reset=`
> requires at least one blank-space-delimited argument; `86400` = 1 day reset
> window). Always use the full `sc.exe` executable via `cmd /c` or Python
> `subprocess`. This requires Administrator privileges.

> **Note:** `disable_services.py` is the legacy fixed-list approach. Prefer `audit_services.py` + `dynamic_disable.py` for runtime discovery on unfamiliar machines.

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

Enforces KIF-48: ".deepchat root directory and file hygiene. Only operational directories and files permitted in .deepchat root. No orphan zip/archive files in AppData\Roaming. No project artifacts masquerading as operational files."

Checks:
1. `.deepchat/projects/` — flags each project directory, checks git push status
2. `.deepchat/archive/` — violation if exists
3. Desktop/Documents — looks for git repos or project-like directories
4. Session offload files — lists old sessions (keeps current)

With `--clean`: deletes all old session directories (keeps current session).


### defender_exclusions.py (v2.4)
Adds DeepChat paths and process to Windows Defender exclusions. Reduces MsMpEng CPU/RAM overhead. Requires Administrator. Run --verify-only for dry-run.

`ash
# Add exclusions (requires admin):
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\defender_exclusions.py"

# Verify only (no changes):
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\defender_exclusions.py" --verify-only
`

### remove_appx.py (v2.4)
Removes known bloatware AppX packages (Xbox, Bing, Widgets, YourPhone, etc.) from both user and provisioned stores. Requires Administrator for provisioned removal.

`ash
# Dry-run (see what would be removed):
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\remove_appx.py" --dry-run

# Live removal:
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\remove_appx.py"

# Aggressive (includes more packages):
python "%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts\remove_appx.py" --aggressive
`
### full_clean.py
Orchestrator running all 7 phases in sequence: audit → dynamic service analysis → kill processes → disable services (legacy) → clean disk → thin-client (with `--clean`) → re-audit to verify. Reports elapsed time and final disk state.

## Known Limitations (from Red-Team Audit 2026-07-29, v2.5 kaizen)

1. **SearchHost/StartMenuExperienceHost** restart endlessly — even with service disable. The only permanent fix requires registry policy or running `winget uninstall` / `dism /online /Remove-ProvisionedAppxPackage` via Python `subprocess` (admin required).
2. **MsMpEng (Defender)** consumes 200-300 MB — not targeted by this skill. Instead, run `defender_exclusions.py` to add DeepChat directories to Defender exclusions.
3. **Office ClickToRun** may restart even after service disable — requires `cmd /c 'sc.exe failure "ClickToRunSvc" reset= 86400 actions= ""'` (Admin) which is handled by both `disable_services.py` v2.0 and `dynamic_disable.py` v1.0.
4. **Lenovo MSPCManagerService** may restart — recommend uninstalling "Lenovo PC Manager" via `winget uninstall`.
5. Some paths require administrator privileges (Windows Temp, CBS logs, service config). The scripts handle permission errors gracefully and report which items need admin.
6. **KIF-30 (2026-07-27 kaizen): `reset=0` drift bug.** `disable_services.py` v1.0 used `reset=0` (immediate failure-counter reset) instead of the documented `reset= 86400` (1-day window). Fixed in v2.0. **`kill_bloat.py`** had the same bug — fixed in v1.1 (2026-07-27 KIF-40 kaizen).
7. **KIF-40 (2026-07-27 kaizen): Dynamic service audit.** The original `disable_services.py` used a hardcoded list of 16 services, missing vendor-specific bloat (Dolby, Elevoc, Adobe updaters, Google updaters, Xbox services, OneDrive) and failing to classify unknown services. Resolved by `audit_services.py` (runtime heuristic classification of 284+ services) and `dynamic_disable.py` (dynamic target generation). The legacy fixed-list script remains as a safety baseline.
8. **KIF-48 (2026-07-29 red-team): .deepchat root hygiene gap.** `thin_client.py` only scanned `.deepchat/projects/` and `archive/`, missing arbitrary project directories in `.deepchat` root (e.g., `qnfo-unified/`, `biophoton-ultrametric-consilience/`), loose project files (`*.js`, `*.jsonc`, `*.reg`), and orphan zip archives in `AppData\Roaming` (e.g., 1.6 GB `DeepChat.zip`). Resolved by KIF-48 scanning: directory allowlist check, file extension check, orphan archive scan. Updated v2.4 (2026-07-29).
9. **KIF-49 (2026-07-29 red-team): FTS orphan leak after session prune.** `agent_db_prune.py` v2.0 skipped `deepchat_tape_search_fts` and `deepchat_tape_search_projection` during deletion (44,853 orphan entries found post-prune red-team audit). Root cause: FTS tables WITH `session_id` column (`tape_search_fts`, `projection`, `_meta` variants) were incorrectly grouped with FTS tables WITHOUT `session_id` (`search_documents_fts`). Fixed in v2.1: FTS_WITH_SESSION_ID list deleted inline; FTS_NO_SESSION_ID uses rebuild-based orphan cleanup. Additionally, orphan FTS meta tables cleaned. Two orphan `usage_stats` rows also fixed. Run `clean_fts_orphans.py` to clean any remaining FTS orphans.
10. **KIF-50 (2026-07-29 red-team): Budget laptop comprehensive tuner.** No single script covered all budget-laptop optimizations end-to-end. Created `budget_laptop_tune.py`: read-only system audit (RAM, disk, services, VBS, visual effects, agent.db, startup, top processes) with severity-rated recommendations; non-admin auto-apply (power plan, transparency, config cleanup); admin queue (hibernation, VBS/HVCI, defender exclusions, dynamic service disable, AppX removal). Run `python budget_laptop_tune.py` for audit; `--apply` to execute non-admin + queue admin. `apply_budget_opts.py` is the fast-path variant. VACUUM confirmed working with DeepChat live (WAL/SHM locks harmless).
11. **KIF-51 (2026-07-29 red-team): analyze_agent_db.py column bug + thin_client allowlist gap.** Red-team audit discovered: (a) `analyze_agent_db.py` used `COUNT(te.id)` but `deepchat_tape_entries` has no `id` column (composite key), causing OperationalError; plus undefined variable `tape_count` instead of `count`. Fixed: `COUNT(*)` + correct variable. (b) `thin_client.py` flagged `.gitattributes` and `d1-cache.json` as UNKNOWN FILE in `.deepchat` root. Fixed: added both to `OPERATIONAL_FILES`. Post-kaizen: all scripts exit 0, red-team audit ALL CLEAN.
12. **KIF-52 (2026-08-05, session VBvCOsXhzlQJUubBqtdFz): TrustedInstaller-protected registry keys.** Windows 11 locks certain keys under `HKLM\SOFTWARE\Policies\Microsoft\Dsh` and `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Feeds` — they're owned by TrustedInstaller, NOT Administrators. Even ShellExecute "runas" UAC elevation cannot write to them. Do NOT waste tool calls on `icacls`/`takeown`. Use the PolicyManager MDM alternative path: `HKLM\SOFTWARE\Microsoft\PolicyManager\default\NewsAndInterests\AllowNewsAndInterests` = 0 (REG_DWORD). This IS writable with admin elevation. See §Widgets MDM Policy below. Cross-ref: windows-command-patterns v3.13 WIN-TRUSTEDINSTALLER-REG-1, kaizen v1.31 WIN-ELEVATION-PARTIAL-1.

## Edge Background Policies (v3.2)

Edge runs background processes even after all windows are closed, and preloads at Windows
login via "Startup Boost." Both are bloat — RAM consumption for no user benefit.

**Permanent disable via Group Policy registry (admin required):**

```
HKLM\SOFTWARE\Policies\Microsoft\Edge\BackgroundModeEnabled  REG_DWORD 0
HKLM\SOFTWARE\Policies\Microsoft\Edge\StartupBoostEnabled    REG_DWORD 0
HKCU\SOFTWARE\Policies\Microsoft\Edge\BackgroundModeEnabled  REG_DWORD 0
HKCU\SOFTWARE\Policies\Microsoft\Edge\StartupBoostEnabled    REG_DWORD 0
```

These are Group Policy-level settings — Edge cannot override them, even after updates.

**Edge auto-launch deletion (no admin required):**
```
HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    DELETE: MicrosoftEdgeAutoLaunch_*
```
This removes the `--win-session-start` flag that preloads Edge at every login.

**Dispatch pattern (write payload → ShellExecute runas → poll):**
```python
import ctypes, sys, tempfile, os, time
# Write admin payload
payload = r'''
import subprocess, os
for hive in [r"HKLM\SOFTWARE\Policies\Microsoft\Edge",
             r"HKCU\SOFTWARE\Policies\Microsoft\Edge"]:
    for val in ["BackgroundModeEnabled", "StartupBoostEnabled"]:
        subprocess.run(f"reg add {hive} /v {val} /t REG_DWORD /d 0 /f", shell=True)
with open(os.path.join(os.environ["TEMP"], "_edge_result.txt"), "w") as f:
    f.write("done")
'''
p = os.path.join(tempfile.gettempdir(), "_edge_admin.py")
with open(p, "w") as f: f.write(payload)
ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{p}"', None, 1)
# Poll for completion
for _ in range(20):
    time.sleep(0.5)
    if os.path.exists(os.path.join(tempfile.gettempdir(), "_edge_result.txt")):
        break
```

## Widgets MDM Policy (v3.2)

Windows 11 Widgets (`widgets.exe` + `widgetservice.exe`) can be killed without admin,
but they restart on reboot. The registry keys to permanently disable them are
TrustedInstaller-protected.

**The WORKING path (admin required):**
```
HKLM\SOFTWARE\Microsoft\PolicyManager\default\NewsAndInterests
    AllowNewsAndInterests  REG_DWORD 0
```
This is the MDM/Intune-compatible path. Unlike Dsh and Feeds, it IS writable with
ShellExecute "runas" admin elevation.

**Paths that DO NOT work (TrustedInstaller / ACL-locked):**
```
HKLM\SOFTWARE\Policies\Microsoft\Dsh\AllowNewsAndInterests               ← TRUSTEDINSTALLER
HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Feeds\ShellFeedsTaskbarViewMode  ← ACL-LOCKED
```

**Fallback:** If the MDM path is also blocked, instruct the user:
Settings → Personalization → Taskbar → Widgets = Off. When
the Settings GUI path is needed, DeepChat's Computer Use (CUA) tools
(`list_apps` → `launch_app` → `get_window_state` → `click`/`type_text`) can drive
the Settings app programmatically — load the `computer-use` skill for the full CUA
protocol.

## Self-Elevation Pattern (v3.2)

Many bloat operations require admin: writing to HKLM, service control, AppX removal.
Use `ctypes.windll.shell32.ShellExecuteW` with `"runas"` verb for UAC self-elevation.
The user clicks "Yes" on the UAC prompt — no typing required.

**Cross-ref:** `windows-command-patterns` v3.16 §S-1.0.8 for the full pattern
(what works, what doesn't, TrustedInstaller caveat).

```python
import ctypes, sys, tempfile, os, time

# Write ALL admin operations into ONE payload
payload = r'''<admin operations as Python script>'''
p = os.path.join(tempfile.gettempdir(), "_admin.py")
with open(p, "w") as f: f.write(payload)

# Launch as admin (ONE UAC prompt for ALL operations)
ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{p}"', None, 1)

# Poll result file
for _ in range(20):
    time.sleep(0.5)
    if os.path.exists(os.path.join(tempfile.gettempdir(), "_result.txt")):
        break
```


> **RESTART AFTER SKILL PURGE (2026-08-02):** DeepChat auto-restores deleted
> platform-default skills — they must be re-deleted AFTER a restart, and the
> restart is required for the purge to register in agent.db. Schedule deferred:
> `python "%USERPROFILE%\.deepchat\skills\system\scripts\schedule-restart.py" --delay 60`,
> then re-delete auto-restored platform skills post-relaunch.
> See system skill §Auto-Restart Protocol.

## Post-Cleanup Verification

After running cleanup, always verify:
1. Disk space changed as expected
2. Bloat processes didn't restart (check with `audit_system.py`)
3. Services stayed disabled (verify with `audit_services.py`)
4. Thin-client violations resolved

If processes restart, the permanent fix is usually:
```python
# Run with admin privileges
import subprocess
subprocess.run(['winget', 'uninstall', 'Microsoft.Windows.Search'], check=False)
subprocess.run(['cmd', '/c', 'sc.exe', 'config', 'WSearch', 'start=', 'disabled'], check=False)
subprocess.run(['cmd', '/c', 'sc.exe', 'failure', 'WSearch', 'reset=', '86400', 'actions=', ''], check=False)
```

## DeepChat Runtime Context
- Skill root: `C:\Users\LENOVO\.deepchat\skills\bloat-cleanup`.
- Relative paths mentioned by this skill are relative to the skill root unless stated otherwise.
- When this skill needs script execution, prefer `skill_run` over `exec`.
- Bundled runnable scripts:
  - scripts\audit_system.py (python)
  - scripts\audit_services.py (python) ★ NEW
  - scripts\clean_disk.py (python)
  - scripts\disable_services.py (python)
  - scripts\dynamic_disable.py (python) ★ NEW
  - scripts\full_clean.py (python)
  - scripts\kill_bloat.py (python)
  - scripts\thin_client.py (python)
- Cross-references: windows-command-patterns v3.16 §S-1.0.8 (ShellExecute runas, sc, taskkill, TrustedInstaller caveat, CUA tools), kaizen v1.66 (WIN-ELEVATION-PARTIAL-1)
- Do not guess script paths or change directories to locate skill files.

## Version

Current: **v3.4** (bloat-cleanup — CUA tools integration for GUI cleanup + stale cross-ref fix; 2026-08-06)
