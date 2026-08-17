---
name: git-github
description: Git workflow operations and GitHub project management -- conventional commits, branch recovery, merge conflicts, detached HEAD, stash recovery, GitHub Issues, PRs, Wikis, Releases, Milestones, project boards, and GitHub-D1 sync. GitHub is CANONICAL for skills repository and project files/archives.
version: 2.22
triggers: ["git", "commit", "merge", "rebase", "branch", "push", "pull", "detached HEAD", "conflict", "stash", "reflog", "GitHub", "Issues", "PRs", "pull request", "wiki", "releases", "Milestones", "project board", "GitHub sync", "D1 sync", "repo", "repository", "fork", "clone", "remote", "origin", "main", "master", "feature branch"]
related: []
priority: 2
platform: all
autonomous: false
self_sufficient: true
---
> **v2.22 UPDATE (2026-08-06, kaizen — VERSION-OVERWRITE-1 merge + GH-API-STDIN-NOOP-1):**
> Concurrent session's .kaizen_history claimed v2.21 with GITHUB-TOPICS-PATCH-NOOP-1 + GH-API-STDIN-NOOP-1,
> but the file was still v2.20 at scan time (phantom/aspirational history claim, PHANTOM-CLAIM-2 class).
> This session's v2.21 (TOPICS-API-1, the canonical PATCH-topics silent-noop finding) landed first; merged
> past the collision per VERSION-OVERWRITE-1 to v2.22, preserving ALL content. GH-API-STDIN-NOOP-1 folded
> in as a verified anti-pattern (stdin body PATCH returned 0 without persisting).
> Changes: (1) [SOFT] Topics API documented (PUT /repos/{x}/topics replace-all; PATCH-topics no-op).
> (2) [SOFT] GH-API-STDIN-NOOP-1 anti-pattern added. (3) [DESIGN] TOPICS-API-1 anti-pattern added.
> Cross-reference: TOPICS-API-1, GH-API-STDIN-NOOP-1, MEMORY-TO-SKILL-DRIFT (mem-blydRPUvzC0Z),
> kaizen API-DOC-GAP-1, VERSION-OVERWRITE-1, session repo-tagging (2026-08-06).
> Red-team: direct parent-agent 5-adversary audit (SKILLS UPDATE directive; session repo-tagging run).
> HARD: 0. SOFT: 1. DESIGN: 1. Changes:
> (1) [SOFT] **Topics API documented** in Repository Operations — `PUT /repos/{owner}/{repo}/topics`
>     with `{"names":[...]}` (replace-all) is the working endpoint; `PATCH /repos/{owner}/{repo}` with
>     `{"topics":[...]}` is SILENTLY IGNORED (HTTP 200, topics unchanged). Canonical case: 150-repo
>     taxonomy tagging run 2026-08-06 — 2 false-positive rounds burned before the dedicated Topics
>     endpoint was confirmed. Memory mem-blydRPUvzC0Z migrated here per MEMORY-TO-SKILL-DRIFT.
> (2) [DESIGN] **TOPICS-API-1 anti-pattern added** to the anti-patterns table.
> Cross-reference: kaizen API-DOC-GAP-1, BLAME-EXTERNAL-1, session repo-tagging (2026-08-06).
> **API-FAILURE PROTOCOL (HARD, cross-ref):** When any API call returns 403/401/404,
> run the API-Failure Self-Diagnosis Protocol (windows-command-patterns S-1.0.6):
> STOP -> VERIFY your HTTP method/headers -> COMPARE with curl -> THEN consider
> infrastructure. The bug is ALWAYS your code until proven otherwise (kaizen BLAME-EXTERNAL-1).
> Canonical case: Zenodo 403 was urllib.Request(method="DELETE") silently sending GET.



> **v2.12 UPDATE (2026-08-04, kaizen — staleness sweep + N-2 nomenclature):**
> Red-team: direct parent-agent audit (session C8CxG7CWs3AOR9w37Q5c8).
> HARD: 0. SOFT: 2. DESIGN: 0.
> Changes:
> (1) [SOFT] **Staleness sweep**: 19 days since last kaizen (2026-07-18).
>     Verified WBS routing table (v2.10) still matches canonical codes in
>     QNFO/qnfo-ops:WBS/WBS.TAXONOMY.md. No drift.
> (2) [SOFT] **N-2 nomenclature check**: version-header delimiter standardized
>     to em-dash per qnfo-core N-2. Any remaining `--` formats deprecated.
> Cross-reference: qnfo-core N-2, kaizen v1.18, WBS-AGENT-PROTOCOL.md.

> **v2.4 UPDATE (2026-08-02, kaizen — Cloudflare tool discoverability):**
> Ephemeral-memory mandate: memories are NOT permanent — skill instructions must name
> the actual agent tools. GitHub-D1 Sync (this skill) touches Cloudflare D1 via
> `query_graph` and `workers_list` for verification. For any D1/Worker/R2 state
> verification, use the agent tools `query_graph(endpoint, params)` and
> `workers_list` (see cloudflare skill §Skill Cross-Reference v3.18). Never rely
> on durable memory for Cloudflare operational state.
> Cross-reference: cloudflare v3.33

> **v2.6 UPDATE (2026-08-04, kaizen — Red-team skills audit closeout):**
> Red-team: 5-skill Watchtower scan; git-github flagged for missing N-2 version footer.
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] N-2 version footer added — was the only QNFO core skill without one.
> Cross-reference: kaizen v1.14, cloudflare v3.33 (cross-ref table updated).

> **v2.11 UPDATE (2026-08-04, kaizen — PowerShell remediation + repo consolidation audit):**
> Red-team: 5-subagent parallel + direct parent-agent audit (session vy97NnZcIGFjkhebn1DPU).
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] PowerShell references replaced with Python equivalents:
>     `Remove-Item -Recurse -Force $env:TEMP\<project>` → `python -c "import shutil; shutil.rmtree(...)"`;
>     `$env:TEMP` → `%TEMP%` in clone instructions.
> Cross-reference: qnfo-core §0.6 Python-First Execution Mandate, windows-command-patterns v3.12.

> (2) [HARD] **WBS-TAXONOMY-GAP closed (iteration-2 red-team)** — execute_plan now
>     carries CONCRETE [QNFO.UMP.002.P4]-style WBS-coded steps (was no prefix at all);
>     WBS-NO-CODE HARD GATE example in-file. Cross-ref qnfo-core v1.13 §N-4.
# GIT-GITHUB — v2.22
 (Ultra-Consolidated VC + PM)

> **v2.3 UPDATE (2026-07-29, KIF-32 thin-client temp-volatility incident):**
> Added **TEMP Volatility & Same-Turn Commit Mandate (HARD GATE)** below.
> A session editing Continuum Trilogy files cloned to `$env:TEMP` lost work
> across 3 re-clones because Windows temp directories are volatile — the
> system cleaned the temp directory between turns before `git commit` ran.
> **Edits applied to a temp checkout MUST be committed AND pushed in the
> SAME turn as the edit.** Deferring commit to a later turn = guaranteed
> data loss. The old "Work, commit, push" three-step phrasing wrongly implied
> multi-turn work with a deferred commit was acceptable — it is not.
> Incident produced ~25 wasted tool calls and demonstrated exactly the
> failure mode KIF-32 was designed to prevent.

> **v2.2 UPDATE (2026-07-21, phantom-claim audit):** Added the
> **Tool-Call Execution Mandate** section below, extending the existing
> "tool success messages are NOT verification" rule with an explicit
> requirement to independently re-query GitHub's API (not just local git)
> before claiming a push, tag, release, or PR is live remotely.

> **Merges 2:** git-operations + github-manager
> **Cloudflare Full-Stack:** Git is version control for the import surface ONLY. R2 + D1 are canonical for project artifacts. GitHub is secondary to D1 for project state. Skills repo (`qnfo-skills`) is for skills exclusively -- NEVER place project data there (ADR-026).
> **v2.1 UPDATE (2026-07-18):** Added mandatory REPO-TARGET GATE (`git remote -v` before ANY tag/release/commit) after ADR-026 Incident 3 -- a prior session created research-project tags (`v0.1-phase0`, `v1.0.0`) and a Zenodo-DOI GitHub Release inside `qnfo-skills` by mistake. The old "Protected Repositories" section only warned about committing *files*; it did not cover tags/releases, which are independent git refs and slip through file-level checks.

> **v2.14 UPDATE (2026-08-04, kaizen — GIT-COMMIT-M-QUOTE-1 + fresh-clone identity + N-2 frontmatter fix):**
> Red-team: direct parent-agent audit of session 1tz85-vMiqh2TyFySznBA (IPR publication pipeline;
> 6 commits, 4 failed `git commit -m` calls, 2 "Author identity unknown" errors).
> HARD: 1. SOFT: 2. DESIGN: 0. Changes:
> (1) [HARD] **GIT-COMMIT-M-QUOTE-1 enforced in this skill** — Standard Workflow + TEMP Volatility
>     sections now mandate `git commit -F <msgfile>` (write tool message file). The old
>     `git commit -m "ACTION:..."` instructions were the EXACT pattern that failed 4x this
>     session through cmd.exe (pathspec errors). Cross-ref windows-command-patterns v3.12.
> (2) [SOFT] **Fresh-clone identity gate added** — new clone fails "Author identity unknown"
>     (2x this session); git config user.email/user.name required before first commit.
> (3) [SOFT] **N-2 frontmatter fixed** — frontmatter said 2.12 while header/footer said 2.13
>     (drift from v2.13 kaizen which bumped header/footer only).
> Cross-reference: windows-command-patterns v3.12 (GIT-COMMIT-M-QUOTE-1), kaizen v1.20,
> qnfo-core N-2, session 1tz85-vMiqh2TyFySznBA.

> **v2.13 UPDATE (2026-08-04, kaizen — Watchtower session retrospective):**
> Red-team: direct parent-agent audit (session hdd6PloLtF_ybqD_CK7EH).
> HARD: 0. SOFT: 1. DESIGN: 0.
> Changes:
> (1) [SOFT] ARCHIVED-REPO-BLOCK-1 anti-pattern added — push/pull to archived repos
>     fails 403; unarchive via gh API PATCH. Living documents = keep unarchived.
> Cross-reference: kaizen v1.19, session hdd6PloLtF_ybqD_CK7EH.

## execute_plan

**WBS INTEGRATION (v2.11, iteration-2 kaizen):** every `update_plan` step in a git
operation carries a canonical WBS prefix per qnfo-core §N-4 + `QNFO/qnfo-ops:WBS/WBS-AGENT-PROTOCOL.md`.
CONCRETE EXAMPLE — branching in the Ultrametric Physics program repo:
`[QNFO.UMP.002.P4] Branch ump/paper/adelic-shannon-theory + PR`.

```python
update_plan([
  {"step": "[QNFO.UMP.002.P4] REPO-TARGET GATE: git remote -v -- confirm program repo, NEVER qnfo-skills", "status": "in_progress"},
  {"step": "[QNFO.UMP.002.P4] Create branch: git checkout -b ump/paper/adelic-shannon-theory (WBS {prog}/{type}/{slug})", "status": "pending"},
  {"step": "[QNFO.UMP.002.P4] Execute git operation, conventional commit", "status": "pending"},
  {"step": "[QNFO.UMP.002.P4] Verify: git log -1 --oneline, git status --short, git ls-remote origin", "status": "pending"},
])
```

Fallback (no program repo context): use `[{WBS}.P{N}]` template form, never omit
the prefix — a plan step without a WBS code is WBS-NO-CODE (HARD GATE).

update_plan([
  {"step": "REPO-TARGET GATE: git remote -v -- confirm this is the intended repo, NEVER qnfo-skills for project/research content", "status": "pending"},
  {"step": "Verify current branch: git branch --show-current (IRON RULE: NEVER main/master)", "status": "pending"},
  {"step": "Execute git or GitHub operation", "status": "pending"},
  {"step": "Verify: git log -1 --oneline, git status --short (must be clean)", "status": "pending"},
])

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — MANDATORY)

Claiming a commit is "pushed", a tag/release is "created", or a PR/Issue
is "opened" without an invoked tool call showing evidence in this turn is a
PHANTOM CLAIM (`qnfo-core` §9.11 Rule 14) — BLOCKED.

1. **Local commit** — `git log -1 --oneline` must show the hash; `git status --short` must be empty.
2. **Push** — a local `git push` returning exit 0 is NOT sufficient. Independently re-query the GitHub API (`GET /repos/{owner}/{repo}/commits/{sha}` or `git ls-remote origin <branch>`) to confirm the commit is actually visible on the remote before claiming "pushed".
3. **Tags/Releases** — after `git tag`/`gh release create`, re-query `GET /repos/{owner}/{repo}/releases` or `git ls-remote --tags origin` to confirm the ref exists remotely, not just locally.
4. **Issues/PRs** — after creation, `GET` the issue/PR number back from the API and show its real state (open/number/URL) rather than trusting the creation response body alone.
5. If remote verification cannot be run in this turn, say `[NOT-VERIFIED: reason]` instead of "pushed"/"released"/"opened".

---

## Git Operations

### Conventional Commits (MANDATORY)
Format: `ACTION:[CREATE|EDIT|DELETE] FILE: <path> RATIONALE: <reason>`

Valid ACTION values:
- `CREATE` -- new file
- `EDIT` -- modified existing file
- `DELETE` -- removed file

Examples:
```
ACTION:CREATE FILE: prompts/DEFAULT.md RATIONALE: Added execution gate
ACTION:EDIT FILE: skills/cloudflare/SKILL.md RATIONALE: Added Email section
ACTION:DELETE FILE: deprecated/old-script.py RATIONALE: Replaced by new version
```

### Branch Discipline (IRON RULE)
- **NEVER commit to main/master.** This is a HARD GATE.
- Branch naming uses the `{type}/{slug}` convention (replaces legacy `feature/<description>`).
- **Type** is the work category: `paper`, `project`, `audit`, `artifact`, `fix`, `kaizen`, `infra`.
- **Slug** is the paper or project identifier in kebab-case — it MUST be descriptive (the paper's canonical short name, not a generic phase label like "phase0-scaffold" or "project-init-phase0").
- **No underscores or CamelCase.** lowercase-kebab-case only.
- Verify before commit: `git branch --show-current`
- **Good:** `paper/measurable-vs-imaginable`, `audit/acrp04-five-smooth`, `fix/zenodo-403-urllib`, `kaizen/e2e-nomenclature-audit`, `infra/r2-sync-worker`
- **Bad (forbidden):** `feature/phase0-scaffold`, `feature/project-init-phase0` — generic phase names are not descriptive and cannot be disambiguated across projects sharing a repo.

### Project Branch Policy (HARD GATE — no new repos for individual papers/projects)

**NEVER create a new repository for a single paper, project, or audit.** QNFO and QWAV content lives in a small set of consolidated **program repos** in the QNFO org. Every new piece of work is a **branch** inside the appropriate program repo, not a new repository.

| Work Type | QNFO Program Repo | Branch Prefix | Example |
|:----------|:------------------|:--------------|:--------|
| Ultrametric / p-adic / adelic physics papers | `QNFO/ultrametric-physics` | `paper/` | `paper/adelic-shannon-theory` |
| Laws of Form / Spencer-Brown research | `QNFO/laws-of-form` | `paper/` | `paper/cancellation-rule` |
| Infomatics / information-as-fundamental | `QNFO/infomatics` | `paper/` | `paper/informational-universe` |
| CFPE / paradigm forecasting | `QNFO/cfpe` | `paper/` | `paper/computing-after-silicon` |
| General QNFO research papers / audits | `QNFO/qnfo-research` | `paper/`, `audit/` | `paper/rosetta-fractal`, `audit/pqs-ai-evaluation` |
| QWAV platform / worker infra | `QNFO/qwav-platform` | `infra/`, `project/` | `infra/d1-backfill`, `project/papers-server-v2` |
| QWAV interactive demos | `QNFO/qwav-demos` | `artifact/` | `artifact/hardware-visualizer` |
| QNFO skills / prompts | `QNFO/qnfo-skills` | `kaizen/`, `feature/` | `kaizen/watchtower-scan` |

**Routing protocol:** Before starting ANY new project, paper, or audit:
1. Classify the work against the table above to select the correct program repo.
2. If the work doesn't match any existing program area, consult the user — do NOT invent a new repo.
3. Clone the program repo → `git checkout -b {type}/{slug}` → work → PR into main.
4. The branch slug MUST be the paper's canonical short name (the same slug used for Zenodo, D1, R2, and the paper filename).

### Standard Workflow
```bash
# 0a. FRESH-CLONE IDENTITY GATE (v2.14): first commit on a new machine/clone fails with
#    "Author identity unknown" unless git config user.email/user.name is set. Before the
#    first commit in ANY fresh clone:
#      git config user.email "rowan@qnfo.org"
#      git config user.name "Rowan Brad Quni-Gudzinas"
#    (or one-shot: git -c user.email=... -c user.name=... commit -F <msgfile>)
#    Configure via a Python subprocess script (windows-command-patterns S0.0) — never
#    `git config` with quoted values through the exec tool (same GIT-COMMIT-M-QUOTE-1 class).

# 0. REPO-TARGET GATE (HARD, run FIRST -- especially before ANY `git tag` or
#    `gh release create`, not just commits)
git remote -v
# Confirm this is the repo you actually intend to operate on. If the task
# involves research, publications, WBS, project phases, or any content that
# is not a skill definition -- this MUST NOT be QNFO/qnfo-skills. See
# "Protected Repositories" below and ADR-026 Incident 3.

# 1. Check state
git status

# 2. Verify on feature branch
git branch --show-current
# MUST show: feature/<name>, NOT main/master

# 3. Stage changes
git add <files>

# 4. Commit with conventional format
git commit -F C:\Users\LENOVO\AppData\Local\Temp\commit-msg.txt
#   ^ GIT-COMMIT-M-QUOTE-1 RESOLVED under Git Bash (2026-08-15, windows-command-patterns
#   v3.23): `git commit -m "multi word message"` now works natively (bash passes quotes
#   correctly). The -F write-file pattern remains canonical for long/complex messages
#   (em-dashes, multiline, signed-off-by), but -m with spaces/special chars is safe again.

# 5. Verify commit
git log -1 --oneline

# 6. Verify branch
git branch --show-current

# 7. Push if needed
git push origin <branch>
```

### Verification Protocol (POST-WRITE MANDATORY)
After EVERY git operation:
1. `git log -1 --oneline` -- commit exists in log
2. `git branch --show-current` -- on correct feature branch
3. `git status --short` -- clean working tree (empty output)

**Tool success messages are NOT verification.** Show the actual git output.

---

## Git Recovery Procedures

### Detached HEAD
```bash
# Scenario: you see "HEAD detached at <hash>"
git checkout -b feature/recovery-branch
# Verify: git branch --show-current
```

### Merge Conflicts
```bash
# 1. Identify conflicted files
git status

# 2. Open each conflicted file
# Conflict markers: <<<<<<< HEAD, =======, >>>>>>> other-branch

# 3. Resolve conflicts in each file
# Remove conflict markers, keep desired changes

# 4. Stage resolved files
git add <resolved-file>

# 5. Complete merge
git commit

# 6. Verify
git log --oneline -3
```

### Lost Commits (Reflog Recovery)
```bash
# 1. Find lost commit in reflog
git reflog
# Example: abc1234 HEAD@{2}: commit: ACTION:CREATE FILE: ...

# 2. Checkout the lost commit
git checkout abc1234

# 3. Create branch from it
git checkout -b feature/recovered

# 4. Verify
git log --oneline -3
```

### Stash Recovery
```bash
# 1. List saved stashes
git stash list
# stash@{0}: WIP on feature/branch: abc1234 Commit message
# stash@{1}: WIP on main: def5678 Older work

# 2. Apply most recent stash
git stash pop

# Or apply specific stash
git stash apply stash@{1}

# 3. Clear if needed
git stash clear
```

### Fixing Wrong Branch Commits
```bash
# Committed to main by mistake
git log -1 --oneline  # Note the hash
git checkout -b feature/correct-branch
git checkout main
git reset --hard origin/main  # Undo wrong commit on main
```

### Undoing Last Commit (not pushed)
```bash
# Undo commit, keep changes staged
git reset --soft HEAD~1

# Undo commit, keep changes unstaged
git reset HEAD~1

# Undo commit, discard changes (DANGEROUS)
git reset --hard HEAD~1
```

---

## GitHub Management

### Repository Operations
- **Create repo:** `gh repo create {owner/repo} --public --add-readme` (recommended: `--add-readme` ensures a bootstrap commit on main, making the repo immediately subtree-add-safe). NEVER create without a bootstrap commit if `git subtree add` will follow.
- **Clone:** `git clone <url>`
- **Push:** `git push origin <branch>`
- **Pull:** `git pull origin <branch>`
- **Archive:** `gh repo archive {owner/repo} --yes`
- **Topics (repo tags):** `PUT /repos/{owner}/{repo}/topics` with body `{"names": ["topic1", "topic2"]}` (replace-all semantics — always send existing + new). **WARNING — TOPICS-API-1:** `PATCH /repos/{owner}/{repo}` with `{"topics": [...]}` is SILENTLY IGNORED (HTTP 200, topics unchanged) — do not use it. Verify with `GET /repos/{owner}/{repo}/topics`. Discovered 2026-08-06 during the 150-repo taxonomy tagging run. — **WARNING**: `gh repo archive` follows GitHub HTTP 301 redirects. Always verify the repo's actual owner via `gh api repos/<owner>/<name> --jq .owner.login` AND confirm it's in the `user/repos?affiliation=owner` list before archiving. Archiving the wrong copy (org repo via redirect) can be undone with `gh repo unarchive`. See ARCHIVE-REDIRECT-1 anti-pattern.

### Issues
Create, update, close Issues. Template: title (actionable, specific), body (description, steps, expected behavior, environment).

### Pull Requests
Create PRs with: title, description, linked issues, reviewers. Merge strategies: squash (clean history), merge (preserve commits), rebase (linear history).

### Wikis
Create/edit documentation pages. Structure: Home (overview), Getting Started (setup), Architecture (design), Operations (deploy/maintain).

### Releases
Create semantic versioned releases with release notes. Attach build artifacts (binaries, PDFs, archives).

### Milestones & Projects
Group issues into milestones with due dates. Track via project boards (To Do -> In Progress -> Done).

### GitHub-D1 Sync
GitHub is SECONDARY to D1 for project state. Sync direction: D1 -> GitHub (D1 is canonical). Sync on: project state changes, publication events, session closeouts.

---

## File/Project Hygiene (KIF-32 Enforcement)

### NO git repos in .deepchat/projects/

KIF-32 prohibits local project files. A git repository checked out under
`.deepchat/projects/` is a KIF-32 VIOLATION -- it puts project files on
local disk outside the thin-client protocol. Before any `git clone` or
`git init`, verify the target path is NOT under `.deepchat/projects/`.

**Enforcement:**
- NEVER `git clone` or `git init` under `.deepchat/projects/`, Desktop,
  Documents, or any system directory (C:\, C:\Windows, C:\Program Files).
- **Canonical project paths:** Projects live on R2 (Cloudflare) with git
  mirrors on GitHub. Local clones are temporary scratchpads only.
### TEMP Volatility & Same-Turn Commit Mandate (HARD GATE, v2.3)

**Windows `$env:TEMP` is VOLATILE. It can be cleaned by the system, session
cleanup, or between tool-call turns without warning.** Any clone to a temp
location is a MAXIMUM ONE-TURN checkout. The sequence:

**HARD GATE — this is the ONLY permitted workflow for temp-location edits:**

```
# Step 1: Clone (this turn only)
git clone <url> %TEMP%\<project>

# Step 2: Apply ALL edits (this turn only)

# Step 3: Commit (MANDATORY SAME TURN — never defer)
git add <files> ; git commit -F C:\Users\LENOVO\AppData\Local\Temp\commit-msg.txt
#   (GIT-COMMIT-M-QUOTE-1 RESOLVED under Git Bash 2026-08-15; -F still canonical for long messages)

# Step 4: Push (MANDATORY SAME TURN — never defer)
git push origin <branch>

# Step 5: Verify push reached remote (Anti-Phantom Gate)
git ls-remote origin <branch>

# Step 6: Delete local clone immediately
python -c "import shutil; shutil.rmtree(r'%TEMP%\<project>', ignore_errors=True)"
```

**What is FORBIDDEN (v2.3 HARD GATE):**
- ❌ Edit a file in turn N, plan to commit in turn N+1 — the temp may be gone
- ❌ Clone, edit file 1, think "I'll edit file 2 next turn then commit" — lost
- ❌ Apply fixes iteratively across turns without committing each batch
- ❌ Assume `Test-Path $env:TEMP\<project>` returns true across turn boundaries

**If a task requires multi-turn editing of a temp clone:**
1. Clone, edit batch 1, commit, push, delete clone — all in turn 1
2. Next turn: re-clone (gets latest from remote), edit batch 2, commit, push, delete
3. Never assume a clone from turn N still exists in turn N+1

**R2 is the canonical durable store.** Git is the mirror. Temp is a one-turn
scratchpad. Never treat temp as persistent storage.
- After `git push`, delete local project files (per JIT thin-client protocol).

### Script Canonical Layers (v2.19, verified 2026-08-05)

Per KIF-32, the local filesystem is NEVER canonical for scripts. Reusable
scripts live in exactly TWO git layers; throwaways live in %TEMP% and die;
R2 holds deliverables, not executables.

| Layer | Location | Run Protocol |
|:------|:---------|:-------------|
| Skill-bound scripts | git: `QNFO/qnfo-skills` → `<name>/scripts/` (FLAT root, no /skills/ subtree — stale legacy removed 9591280); live: `skills/<name>/scripts/` | `skill_run <skill> scripts/<name>.py` or exec python against live path |
| Ops toolbox | `QNFO/qnfo-ops/scripts/` (bootstrapped 2026-08-05, commit b54a983) | Clone to %TEMP% → run → delete clone, ONE turn |
| One-shot | `%TEMP%\_task.py` | write → exec python → del (never committed) |
| R2 (artifacts only) | `qnfo-releases/`, `qnfo-projects/`, `qnfo-backups/` | Archive + SHA-256 verify → delete local |

**Classification rules:**
1. Domain-tied to one skill → qnfo-skills skill dir (git is superset, live dir is subset).
   **GIT PATH IS FLAT ROOT:** qnfo-skills repo stores skills at repo ROOT (`/<name>/`), NOT under
   `skills/`. A legacy `/skills/` subtree existed (stale duplicate paths) and was REMOVED in commit
   9591280 (2026-08-05). Commits to `skills/<name>/...` land in a non-canonical path — always use
   `/<name>/...` when targeting git. The LIVE hydrated dir uses `skills/<name>/` — the two paths
   differ by design (git flat root vs live skills/ namespace).
2. Cross-cutting reusable → qnfo-ops/scripts/. If it doesn't exist there, WRITE it,
   commit to qnfo-ops (same-turn), then clone-to-TEMP to run.
3. One-shot never reused → %TEMP% only. NEVER commit throwaways to any repo.
4. Deliverables (corpora, PDFs, archives) → R2 buckets, SHA-256 round-trip verified,
   THEN delete local. R2 does NOT hold executable scripts.

**Ops-script clone cleanup (NEW — 2026-08-05):** git pack files are read-only
(0o444). `shutil.rmtree(path, ignore_errors=True)` SILENTLY FAILS on them,
leaving a thin-client-violating leftover clone. Mandatory pattern:
```python
def force_rmtree(path):
    for root, dirs, files in os.walk(path):
        for n in dirs + files:
            try: os.chmod(os.path.join(root, n), 0o777)
            except Exception: pass
    shutil.rmtree("\\\\?\\" + os.path.abspath(path), ignore_errors=False)
```
Canonical case: session -WyivBiyZ6xFy4uXS_RNy — leftover qnfo-ops-verify clone
survived 2 rmtree attempts until the `\\?\` + chmod-sweep pattern.

**REPO-DEFAULT-BRANCH-1 (NEW — 2026-08-05):** QNFO/qnfo-ops default branch is
`main`, NOT `master` (same for qwav-platform). Verify `git branch --show-current`
after clone before pushing; a `git push origin master` on a main-default repo
fails with "src refspec master does not match any". Canonical case: session
-WyivBiyZ6xFy4uXS_RNy — bootstrap commit pushed to a temp branch, remote branch
deleted before the main push, causing a transient data-loss incident recovered
by re-committing both files directly to main.

### Skills Repository (qnfo-skills) is PROTECTED

The skills repo survives thin-client cleanups (ADR-021/ADR-025). NEVER place
project data, publications, research artifacts, or governance documents there.
See ADR-026 below.

---

## Protected Repositories

### qnfo-skills (ADR-026)
- **Git repo is for SKILLS ONLY.** See also KIF-32 above. NEVER place project data, publications, research artifacts, or governance documents.
- Git-tracked files in the skills repo are PROTECTED. They survive thin-client cleanups (ADR-021/ADR-025).
- Violating this rule is a fabrication-level offense (Rule 14).
- **This restriction applies to git metadata too, not just files** (ADR-026
  Incident 3): tags (`git tag`), GitHub Releases (`gh release create`), and
  branches are independent of the file tree. A commit with zero non-skill
  files can still be wrapped in a project-phase tag (`v0.1-phase0`) or a
  publication Release (Zenodo DOI announcement) -- both are equally
  prohibited in `qnfo-skills`.
- **Before `git tag`, `gh release create`, or `git commit` for ANYTHING other
  than a skill definition change: run `git remote -v` and confirm the target
  is NOT `QNFO/qnfo-skills`.** This is the single check that would have
  prevented Incident 3 (6 stale research/project tags + 1 Zenodo-DOI
  GitHub Release found embedded in `qnfo-skills`, requiring backup+delete
  remediation on 2026-07-18).
- **Routine sync/cleanup audits of `qnfo-skills` MUST check `git tag -l` and
  `gh release list` in addition to the file tree.** A clean `master` branch
  does NOT imply a clean repo -- stale tags/releases from before a
  remediation survive branch force-pushes.

### Import Surface
- `qnfo/prompts/` -- system prompts, templates, skills, configs
- This is the ONLY content that should be in the Local disk import surface
- Everything else: R2 + D1 (Cloudflare-native)

---

## Owner Routing Rule (HARD, added 2026-08-05)

**User mandate:** GitHub accounts rwnq8 and QNFO are STRICTLY SEPARATE for distinct
work streams, programs, and focus areas.

| Repo type | Canonical owner | Always |
|:----------|:---------------|:-------|
| **QNFO repos** (programs, skills, research) | **QNFO org** (`QNFO/<name>`) | ALWAYS |
| **PERSONAL repos** (resume, portfolio, personal projects) | **rwnq8** (`rwnq8/<name>`) | ALWAYS |

Rules:
1. **Never route a QNFO repo to rwnq8, never route a personal repo to QNFO.**
2. Use EXPLICIT owner prefixes on every `gh repo create`: `QNFO/<name>` or
   `rwnq8/<name>` — never rely on default owner resolution
   (CONSOLIDATION-OWNER-RESOLVE-1: bare `gh repo create <name>` can resolve to
   the wrong owner via redirect).
3. The rwnq8 account is ALIVE and canonical for personal repos — only the
   `rwnq8/qnfo-skills-1.git` skill-repo MIRROR was archived (2026-08-05).
4. Personal profile/resume repos live under rwnq8 (rwnq8/rwnq8 profile README,
   rwnq8/resume). CLI-created profile repos need "Share to Profile" on the repo
   page to render on the profile (GITHUB-CDN-PROPAGATION-1 is NOT a CDN issue).

## Thin-Client Canonical Asset Protocol (HARD, added 2026-08-05)

**User mandate:** Any reusable script MUST NOT be saved canonically to the local
filesystem — all local files are ephemeral and may disappear at any time. If a
script is needed again, it must be recoverable from a canonical store.

### The 4 Tiers

| Tier | Location | Status | What Lives Here |
|:-----|:---------|:-------|:----------------|
| **1. Git origin** | `QNFO/qnfo-skills` → local clone `Documents\GitHub\qnfo-skills\<skill>\scripts\` | ⭐ **PRIMARY canonical** | ALL reusable skill scripts (97 today: bloat-cleanup 26, cloudflare 16, research 14, system 10, ...) |
| **2. R2 (durable mirror)** | `deepchat` bucket (app-settings `cloudSyncConfig`) + `qnfo-releases` bucket | ⭐ **SECONDARY canonical** | skill-sync.js mirror of skills tree; large binaries (PDFs, release artifacts) via rclone |
| **3. Live skill dirs** | `C:\Users\LENOVO\.deepchat\skills\<name>\scripts\` | ⚠️ **Ephemeral runtime view** | Hydrated copy for the app to run — re-created from git/R2 if lost. NEVER canonical. |
| **4. One-off `_*.py`** | `%TEMP%` or `.deepchat\_*.py` | 🗑️ **Ephemeral by design** | Analysis/diagnostic scripts — delete after use. Never commit, never persist. |

### The Dual-Store Rule (rwnq8 account alive — only the qnfo-skills-1 mirror archived)

The thin-client mandate requires durable state in at least two independent stores.
**CORRECTED (2026-08-05):** The rwnq8 ACCOUNT is ALIVE and canonical for personal
repos. Only the `rwnq8/qnfo-skills-1.git` MIRROR remote of the qnfo-skills repo was
archived (403) and removed as a remote. For the qnfo-skills skill repo, the durable
pair is:

```
ORIGIN (QNFO/qnfo-skills)  +  R2 (deepchat bucket via skill-sync.js)
```

Personal repos (resume, portfolio, personal projects) follow OWNER-ROUTING-1:
canonical home is rwnq8, dual-stored with R2 as the second copy.

Every reusable script MUST reach BOTH: commit+push to its canonical owner, and
skill-sync.js mirror to R2. One store alone is not durable.

### The Sync Flow (HOW)

```
Edit in live dir (.deepchat\skills\<name>\scripts\)
   → copy to git clone (Documents\GitHub\qnfo-skills\<name>\scripts\)
   → git add + commit + push origin            (SKILL-COMMIT-SAME-SESSION-1)
   → skill-sync.js → R2 deepchat bucket        (durable mirror)
   → large binaries (>1MB) → rclone → qnfo-releases bucket
```

### Classification Rules (WHAT goes where)

| Asset type | Canonical home |
|:-----------|:---------------|
| Reusable skill script (function, automation, tool) | Tier 1 git origin → Tier 2 R2 |
| Large binary (PDF, template pack, data artifact) | Tier 2 R2 (`qnfo-releases`), referenced by skill |
| One-off analysis / diagnostic script | Tier 4 ephemeral — delete after use |
| Config/secrets (API keys, tokens) | NEVER in git — `.env` / R2-secured / env vars (TOKEN-DISCOVERY-1) |
| Script inside an official Cloudflare/3rd-party skill | Tier 2 fork repos (cloudflare-skill-forks etc.), PR back to upstream |

**Test:** if a script would be needed again after a full local wipe, it is NOT
ephemeral — commit it. If it's a one-off diagnostic, delete it after use.


## GitHub Hygiene Mandate (HARD, added 2026-08-05)

**User mandate:** GitHub IS the canonical skills repo/store/location. Master must
be pristine, up-to-date, and canonical. It must NEVER drift. Features must be
pushed to master to merge them.

### Canonical Repository Discipline

1. **The qnfo-skills repo (`QNFO/qnfo-skills`) is the SINGLE canonical store for
   all skills.** `C:\Users\LENOVO\.deepchat\skills\` (live dir) is a PARTIAL
   runtime view — it may lack scripts/templates that exist only in git. **Git is
   the superset. The live dir is a subset. NEVER let the subset overwrite the
   superset.**

2. **Sync direction is ONE-WAY: git -> live (hydrate runtime), NEVER live -> git
   (destroys canonical content).** Canonical case (2026-08-05): a "master sync"
   did rmtree+copy live->git and DELETED 61 canonical files from git
   (bloat-cleanup/scripts/*, research/scripts/*, research/templates/*) — they
   existed in git but not on live. Restored via `git checkout <parent> -- <path>`.
   This is SYNC-OVERWRITE-DESTRUCTION-1.

3. **To update a skill:** edit the file in the LIVE dir (the app loads from it),
   then commit to git by copying that skill's files INTO the git repo —
   ADD/UPDATE only, never rmtree the git dir first. If the git skill dir has
   files the live dir lacks (scripts, templates, references), KEEP them in git
   (do not delete) and hydrate them to live.

4. **Every session MUST end with:** `git status --short` == clean AND
   `git rev-parse master` == `git rev-parse origin/master` (in sync). A session
   that leaves master drifted or dirty is a FAILED session (SKILL-COMMIT-SAME-SESSION-1).

### Push-to-Master Rule

1. **Features/branches MUST be merged to master.** Never leave work sitting in a
   branch. A branch with unmerged commits is a FAILED closeout.
   Canonical case (2026-08-05): 5 stale `kaizen/*` branches held 6,008 insertions
   unmerged; all were superseded by the live-sync (master had newer versions of
   every file) and deleted after verification.
2. **Branch lifecycle:** create feature branch -> work -> verify -> merge to
   master -> push master -> delete branch (local + remote) -> prune. Same session.
3. **Before deleting a branch, verify it is superseded or merged:**
   `git log --oneline master..origin/<branch>` (0 unique commits = safe) and
   version headers on master >= branch. Only unique content requires merge.
4. **Never delete a branch with unique commits without merging it first.**

### Remote Hygiene

1. **Remove dead remotes.** A remote that returns 403/archived (e.g., rwnq8 mirror
   archived 2026-08-05) MUST be removed: `git remote remove <name>`. Only origin
   remains canonical.
2. **Verify remotes each session:** `git remote -v` — origin = QNFO/qnfo-skills
   ONLY.

### Post-Push Verification (MANDATORY)

```
After ANY push:
1. git status --short          -> must be CLEAN (0 output)
2. git rev-parse master        -> local hash
3. git rev-parse origin/master -> remote hash
4. MUST MATCH. If not: git push origin master again, then re-verify.
```


| **PLATFORM-DEFAULT-EXPUNGE-1: Version-tracking or customizing DeepChat platform default skills in any git repo (2026-08-05)** | **HARD GATE.** DeepChat platform default skills (src=builtin in the registry: algorithmic-art, code-review, doc-coauthoring, docx, frontend-design, git-commit, infographic-syntax-creator, mcp-builder, memory-management, pdf, pptx, skill-creator, web-artifacts-builder, xlsx) MUST be expunged from any/all git repos and NEVER version-tracked or customized/updated. They remain available in the app (DeepChat ships them) but are not ours to version. Canonical case (2026-08-05): 14 platform defaults removed from qnfo-skills (commit 4ff764d); deepchat-settings KEPT because substantially refactored into custom QNFO knowledge (Backend Storage Layout, Skill Registry Truth-Source). Exception: a platform default that has been SUBSTANTIALLY refactored into genuinely custom content may be kept — document the decision. |
| **CLOUDFLARE-FORK-1: Storing official Cloudflare skill content in qnfo-skills instead of a separate fork repo (2026-08-05)** | Official Cloudflare skills (durable-objects, workers-best-practices, web-perf, turnstile-spin, cloudflare-one, email-service, sandbox-sdk, agents-sdk, wrangler, deployer, github-manager) MUST be forked into the SEPARATE repo `QNFO/cloudflare-skill-forks` — NEVER backed up in qnfo-skills. The custom cloudflare skill documents coverage matrices and links to the fork; it does NOT copy official content. Modifications to forks are PR'd back to Cloudflare for update consideration. Canonical case (2026-08-05): fork repo created at github.com/QNFO/cloudflare-skill-forks; cloudflare skill v3.34 documents the policy. |

| **OWNER-ROUTING-1: Routing a repo to the wrong GitHub owner — QNFO work to rwnq8 or personal work to QNFO (2026-08-05)** | **HARD GATE.** QNFO repos → QNFO org ALWAYS; PERSONAL repos → rwnq8 ALWAYS. Never route across. Use explicit owner prefixes on every gh repo create (`QNFO/<name>` / `rwnq8/<name>`) — bare names resolve unpredictably (CONSOLIDATION-OWNER-RESOLVE-1). The rwnq8 account is ALIVE and canonical for personal repos; only the rwnq8/qnfo-skills-1.git skill mirror was archived. Canonical case (2026-08-05): v2.17 wrongly implied rwnq8 was dead — corrected; personal repos (resume, portfolio) are rwnq8-canonical, dual-stored with R2. |

| **SYNC-OVERWRITE-DESTRUCTION-1: Copying a partial source (live dir) over the canonical git repo with rmtree+copy, deleting git-only files (2026-08-05)** | **HARD GATE.** Git is the canonical superset; the live skills dir is a partial runtime subset. Sync direction is ONE-WAY: git -> live (hydrate), NEVER live -> git with directory replacement. To commit a skill change: ADD/UPDATE that skill's files in git — never rmtree the git skill dir first (that deletes scripts/templates/references that exist only in git). Canonical case: d4b432c deleted 61 canonical files (bloat-cleanup/scripts/*, research/scripts/*, research/templates/springer-nature-latex/*, research/references/*.json, email-composer/scripts/*.pdf, xlsx/scripts/recalc.py); restored from parent commit. Verify after every sync: `git show --name-status <commit>` shows NO unexpected deletions. |
| **PUSH-TO-MASTER-1: Leaving feature branches unmerged — work sitting in branches instead of master (2026-08-05)** | Features MUST be merged to master in the same session. Branch lifecycle: create -> work -> verify -> merge -> push master -> delete branch (local+remote) -> prune. Canonical case: 5 stale kaizen/* branches with 6,008 insertions left unmerged; all superseded by live-sync and deleted. Before deleting a branch, verify `git log master..origin/<branch>` is empty (0 unique commits) OR merge the unique content first. |
| **BRANCH-HYGIENE-1: Accumulating stale branches (local or remote) across sessions (2026-08-05)** | Every session ends with ONLY master (plus any active feature branch). Delete merged/superseded branches and prune remote-tracking refs. A branch list with 5+ stale entries is a hygiene failure. |
| **DEAD-REMOTE-1: Keeping archived/dead remotes configured (2026-08-05)** | Remove remotes that return 403/archived. `git remote remove <name>`. Only origin (QNFO/qnfo-skills) is canonical. rwnq8 mirror was archived (403) and removed 2026-08-05. |
| **POST-PUSH-VERIFY-1: Pushing without verifying master == origin/master (2026-08-05)** | After ANY push, verify: `git status --short` clean AND `git rev-parse master` == `git rev-parse origin/master`. A push that leaves drift unverified is invisible drift. |

## Anti-Patterns

| Anti-Pattern | Correct |
|:-------------|:--------|
| **AUTOCRLF-VERIFY-1: Raw byte comparison flags 'modified' for every file on Windows (2026-08-05)** | `core.autocrlf=true` makes git check out working files as CRLF while the live/hydrated dir stores LF. `git status` after copying live→git shows 20+ 'M' flags that are pure line-ending artifacts — the content is blob-identical. VERIFY with `git hash-object <live-file>` vs `git rev-parse HEAD:<path>` (blob comparison) — if equal, the file IS in sync. Never trust raw byte diff or `git status` alone on Windows. Canonical case: session -WyivBiyZ6xFy4uXS_RNy cycle 2 — 24 copied files flagged M, all proven blob-identical; only 3 genuine diffs existed. |
| **STALE-CLONE-ACCUM-1: Temp clones from prior sessions accumulate in %TEMP% — thin-client violations (2026-08-05)** | 18 stale `%TEMP%\qnfo-*` clones (197.4 MB: qnfo-pdf-v2/v3, qnfo-research-ph1-6, qnfo-skills, qnfo-ops-*, qnfo-github-repo…) survived multiple session closeouts — the pre-closeout scan has NO %TEMP% clone category. Fix: (a) thin_client.py now scans %TEMP% for `qnfo-*` / repo-pattern dirs (STALE_CLONE category, bloat-cleanup v3.3); (b) every temp clone MUST use the force_rmtree pattern (chmod-sweep + `\\?\` prefix, handles read-only git pack files) same-turn. Canonical case: session -WyivBiyZ6xFy4uXS_RNy — 18 clones deleted at closeout, 197.4 MB freed. |

## Anti-Patterns
| Anti-Pattern | Fix |
| **TOPICS-API-1: PATCH /repos/{x} with `{"topics":[...]}` returns 200 but never changes topics (2026-08-06)** |
| **GH-API-STDIN-NOOP-1: `gh api --input -` (stdin body) can return exit 0 without persisting — do not trust it for verification (2026-08-06)** | When a gh API PATCH with `--input -` (body via stdin) returns 0, independently re-query with `GET /repos/{x}/topics` before claiming success. In the 2026-08-06 tagging run, the stdin PATCH path reported OK for .deepchat/QWAV yet re-fetch showed topics unchanged. (Primary root cause was TOPICS-API-1 — PATCH-topics silent no-op — but stdin bodies are not a reliable write path either.) Prefer `--input <file>` or urllib with explicit JSON, and ALWAYS verify by re-query. Cross-ref: TOPICS-API-1, API-FAILURE PROTOCOL, BLAME-EXTERNAL-1. | GitHub silently ignores the `topics` field on the repo PATCH endpoint. The working endpoint is `PUT /repos/{owner}/{repo}/topics` with `{"names": [...]}` (replace-all — union existing + new). Canonical case: 2026-08-06 repo-tagging run — 2 false-positive rounds (PATCH returned 200, topics stayed []) before the dedicated Topics endpoint was confirmed; 150 repos tagged via PUT. Verify with GET /repos/{x}/topics. Cross-ref: API-DOC-GAP-1 (kaizen), BLAME-EXTERNAL-1 (bug is your code until proven otherwise). |
|:-------------|:----|
| Creating a new repo for a single paper/project | **HARD GATE (Project Branch Policy):** Branch from the appropriate program repo (see routing table). NEVER create a new repo for an individual paper, audit, or project. All QNFO/QWAV content lives in the consolidated program repos. |
| Using generic branch names (`feature/phase0-scaffold`) | Use `{type}/{canonical-slug}` — e.g. `paper/measurable-vs-imaginable`, `audit/acrp04-five-smooth`. The slug must match the paper's canonical short name used everywhere (Zenodo, D1, R2, filename). |
| **WBS-NO-CODE: Branch or plan item lacks a WBS program code prefix — v2.10, 2026-08-04** | Every branch MUST use `{prog}/{type}/{slug}` format where `{prog}` is the lowercase WBS program code (`ump`, `slb`, `inm`, `cfe`, `res`, `plt`, `dem`). Every `update_plan` step MUST carry `[{PORTFOLIO}.{PROG}.{NNN}.P{N}]` prefix. Branches and plan items without WBS codes cannot be audited, traced, or linked across sessions. Canonical codes: qnfo-core §N-1 table. |
| **WBS-INVENT-CODE: Inventing a non-canonical WBS code instead of looking it up — v2.10, 2026-08-04** | WBS program codes are DEFINED in qnfo-core §N-1 (canonical registry) and the Project Branch Policy routing table. Never invent a code. Resolve from: (1) qnfo-core SKILL.md §N-1 table, (2) the routing table in this skill, (3) `QNFO/qnfo-ops:WBS/WBS.TAXONOMY.md` (live canonical; archived copy: `QNFO/wbs-6-synthesis:docs/`). The codes are: `UMP`, `SLB`, `INM`, `CFE`, `RES`, `PLT`, `DEM` plus the existing `ADL`, `CON`, `SR`. Any other code is a fabrication. |
| Committing to main/master | HARD GATE: `git branch --show-current` before commit |
| `git push --force` on shared branches | NEVER force-push to branches others use |
| Amending pushed commits | Only amend unpushed commits |
| Claiming commit without git log evidence | ALWAYS verify: `git log -1 --oneline` |
| Using skills repo as project workspace | ADR-026: skills repo = skills ONLY |
| `git add .` (adds everything blindly) | Stage specific files: `git add <file>` |
| Losing work by `git reset --hard` | Check `git stash` or `git reflog` first |
| Tagging/releasing research content inside `qnfo-skills` | `git remote -v` REPO-TARGET GATE before EVERY tag/release (ADR-026 Incident 3) |
| Assuming a clean file tree means a clean repo | Also audit `git tag -l` and `gh release list` -- tags/releases survive branch force-pushes |
| Trusting a prior remediation without re-verifying | Backfilled/legacy tags predating a policy fix can still exist -- explicitly check `git tag -l` against current policy, don't assume a past cleanup got everything |
| Editing files in a temp clone without committing same-turn (KIF-32, v2.3) | **HARD GATE:** clone → edit → commit → push → delete, ALL in one turn. Never defer commit across turn boundaries. If a file was edited in turn N and `git status` showed changes at the start of turn N+1, re-clone the repo and re-apply the edits — the local files may have been silently lost or corrupted. |
| Assuming `$env:TEMP` persists across turns on Windows (v2.3) | Temp directories are volatile. System cleanup, session teardown, or storage-sense can evict files between turns. `Test-Path $env:TEMP\<project>` returning true in turn N does NOT guarantee it returns true in turn N+1. |
| Multi-turn iterative editing on a single temp clone (v2.3) | Re-clone each turn (fetching latest from remote). Batch edits must be atomic per turn: if you can't finish all edits in one turn, commit what you have, push it, and pick up the rest next turn from a fresh clone. |
| **SUBTREE-NO-HEAD: `git subtree add` fails silently on a new/empty repository (no HEAD commit) — v2.9, 2026-08-04** | `git subtree add` requires an existing HEAD commit to merge into. A brand-new repo cloned without `--add-readme` has no commits → all subtree adds fail silently (especially with `check=False`). **Fix:** Always bootstrap main with a commit BEFORE subtree adds. Use `gh repo create --add-readme` (or create/bootstrap a README commit on main). Never run subtree add on an unborn HEAD. Canonical case: session PMH0kzte — 12 subtree adds failed silently, then README+PROVENANCE committed alone, producing a program repo with ONLY bootstrap files and zero member content. |
| **PR-CREATE-CWD: `gh pr create` without `--repo` flag fails outside a git repo — v2.9, 2026-08-04** | `gh pr create` (and `gh pr merge`) require being run INSIDE a local git checkout or given `--repo owner/name`. When the working directory is not a git repo, gh fails with "not a git repository." **Fix:** Always use `--repo owner/name` on pr create/merge from scripts running in temp directories. Never rely on cwd being a git clone. Canonical case: session PMH0kzte — consolidate_v2.py succeeded through subtree merges and push, then failed at `gh pr create` because the script's cwd was the temp root, not the clone. |
| **REPO-ARCHIVED-403: Writing to an archived GitHub repo returns 403 "Repository was archived so is read-only" — v2.13, 2026-08-04** | Writing to an ARCHIVED repo (Contents API PUT, push, PR) fails with HTTP 403. Unarchive first: `PATCH /repos/{owner}/{repo}` `{"archived": false}` (requires admin rights on the repo). Verify with `GET /repos/{owner}/{repo}` → `archived: false`. Canonical case: session C8CxG7CWs3AOR9w37Q5c8 — QNFO/QWAV strategy/3.0.md rows frozen until unarchived (PATCH archived:false → writes succeeded, commits 2aab2ef7bd/34839f636b). Cross-ref: web-artifacts-builder v0.3 REPO-ARCHIVED-403, ARCHIVE-REDIRECT-1. |
| **ARCHIVE-REDIRECT-1: `gh repo archive owner/name` archives the CANONICAL org repo via GitHub 301 redirect — v2.9, 2026-08-04** | When a repo is owned by an org but queried under a different owner path, GitHub returns HTTP 301 → gh follows silently and operates on the canonical org repo. Relying on the owner prefix in `gh repo archive` to target the right copy is UNSAFE. **Fix:** Before archiving, verify the repo's actual owner via `gh api repos/owner/name --jq .owner.login` AND check `user/repos?affiliation=owner` to confirm it's owned by the target account. Canonical case: session PMH0kzte — `gh repo archive rwnq8/ultrametric-physics` archived QNFO/ultrametric-physics (same repo id) because the repo was created directly in the QNFO org, not rwnq8. |
| **CLONE-LEFTOVER-1: Previous session's temp clone blocks a new clone — v2.9, 2026-08-04** | A background Python script that exits before cleanup (`shutil.rmtree`) leaves a clone directory in `%TEMP%`. A subsequent clone in the same session hits "destination path already exists and is not an empty directory." **Fix:** ALWAYS `shutil.rmtree(workdir, ignore_errors=True)` BEFORE cloning, in the same script. Never assume the workdir is clean from a prior run. Canonical case: session PMH0kzte — the killed consolidate.py v1 left `%TEMP%\ultrametric-physics` with bootstrap files, blocking v2's clone. |
| **CHECK-FALSE-SWALLOW-1: `check=False` in subprocess.run swallows git failures with no diagnostic output — v2.9, 2026-08-04** | `subprocess.run(cmd, check=False)` returns a CompletedProcess but the caller never inspects `returncode` or prints `stderr`. The failure is invisible. This is especially dangerous with `git subtree add` which can fail for multiple reasons (no HEAD, remote unreachable, branch mismatch). **Fix:** NEVER use `check=False` on git operations without capturing AND printing both stdout and stderr on non-zero returncode. Use `check=True` (fail-fast, visible) as the default; reserve `check=False` ONLY for operations where failure is expected (e.g., `git rev-parse --verify` to check existence). Canonical case: session PMH0kzte — consolidate.py v1 used `check=False` on all 12 subtree adds, all failed, none were diagnosed until post-hoc verification. |
| **DELETE-BRANCH-DEFAULT-1: `gh pr merge --delete-branch` cannot delete a branch if it was the repo's default at creation — v2.9, 2026-08-04** | When a new repo has only one branch (the feature branch, because main was empty/unborn), GitHub sets that branch as the default. `gh pr merge --delete-branch` refuses to delete the default branch — the branch survives the merge. **Fix:** After PR merge, explicitly set the default branch to `main` via `gh repo edit --default-branch main`, then DELETE the leftover feature branch via API (`gh api -X DELETE repos/owner/repo/git/refs/heads/<branch>`). Verify with `gh api repos/owner/repo/branches`. Canonical case: session PMH0kzte — ultrametric-physics, laws-of-form, cfpe all had leftover `feature/consolidate-projects` branches after merge because they were the repo's default at creation time. |

| **ARCHIVED-REPO-BLOCK-1: Push/pull to archived GitHub repo fails 403 (2026-08-04)** | If `git push` returns `remote: This repository was archived so it is read-only.` and `fatal: unable to access`, the repo must be UNARCHIVED before pushing. Use `gh api repos/QNFO/<repo> -X PATCH -f archived=false` OR `gh repo edit QNFO/<repo>` (if gh CLI supports it). After push, decide whether to re-archive: if the repo contains LIVING documents (e.g., research continuity registry), keep it UNARCHIVED. If it's a static publication archive, re-archive. Do NOT leave local commits unpushed — verify remote with `git ls-remote`. Canonical case: session hdd6PloLtF_ybqD_CK7EH — consilient-gap-synthesis archived, RESEARCH-CONTINUITY-REGISTRY.md cross-ref committed locally (a72546e) but blocked from push. odr-thesis was successfully unarchived via GitHub API PATCH. |

## Version

**API-FAILURE PROTOCOL (HARD):** When any API call returns 403/401/404, run the API-Failure Self-Diagnosis Protocol (windows-command-patterns S-1.0.6): STOP -> VERIFY your HTTP method/headers -> COMPARE with curl -> THEN consider infrastructure. The bug is ALWAYS your code until proven otherwise (kaizen BLAME-EXTERNAL-1).

Current: **v2.22** (git-github — Script Canonical Layers: qnfo-ops/scripts/ bootstrapped, ops-clone force_rmtree pattern, REPO-DEFAULT-BRANCH-1; verified 2026-08-05)
