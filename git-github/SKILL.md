---
name: git-github
description: Git workflow operations and GitHub project management -- conventional commits, branch recovery, merge conflicts, detached HEAD, stash recovery, GitHub Issues, PRs, Wikis, Releases, Milestones, project boards, and GitHub-D1 sync. GitHub is CANONICAL for skills repository and project files/archives.
version: "2.11"
triggers: ["git", "commit", "merge", "rebase", "branch", "push", "pull", "detached HEAD", "conflict", "stash", "reflog", "GitHub", "Issues", "PRs", "pull request", "wiki", "releases", "Milestones", "project board", "GitHub sync", "D1 sync", "repo", "repository", "fork", "clone", "remote", "origin", "main", "master", "feature branch"]
related: []
priority: 2
platform: all
autonomous: false
self_sufficient: true
---

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
> Cross-reference: cloudflare v3.18.

> **v2.6 UPDATE (2026-08-04, kaizen — Red-team skills audit closeout):**
> Red-team: 5-skill Watchtower scan; git-github flagged for missing N-2 version footer.
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] N-2 version footer added — was the only QNFO core skill without one.
> Cross-reference: kaizen v1.14, cloudflare v3.25 (cross-ref table updated).


> **v2.11 UPDATE (2026-08-04, kaizen — PowerShell remediation + repo consolidation audit):**
> Red-team: 5-subagent parallel + direct parent-agent audit (session vy97NnZcIGFjkhebn1DPU).
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] PowerShell references replaced with Python equivalents:
>     `Remove-Item -Recurse -Force $env:TEMP\<project>` → `python -c "import shutil; shutil.rmtree(...)"`;
>     `$env:TEMP` → `%TEMP%` in clone instructions.
> Cross-reference: qnfo-core §0.6 Python-First Execution Mandate, windows-command-patterns v3.9.

> (2) [HARD] **WBS-TAXONOMY-GAP closed (iteration-2 red-team)** — execute_plan now
>     carries CONCRETE [QNFO.UMP.002.P4]-style WBS-coded steps (was no prefix at all);
>     WBS-NO-CODE HARD GATE example in-file. Cross-ref qnfo-core v1.11 §N-4.
# GIT-GITHUB — v2.11
> **API-FAILURE PROTOCOL (HARD, cross-ref):** When any API call returns 403/401/404,
> run the API-Failure Self-Diagnosis Protocol (windows-command-patterns S-1.0.6):
> STOP -> VERIFY your HTTP method/headers -> COMPARE with curl -> THEN consider
> infrastructure. The bug is ALWAYS your code until proven otherwise (kaizen BLAME-EXTERNAL-1).
> Canonical case: Zenodo 403 was urllib.Request(method="DELETE") silently sending GET.

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
git commit -m "ACTION:TYPE FILE: path RATIONALE: reason"

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
- **Archive:** `gh repo archive {owner/repo} --yes` — **WARNING**: `gh repo archive` follows GitHub HTTP 301 redirects. Always verify the repo's actual owner via `gh api repos/<owner>/<name> --jq .owner.login` AND confirm it's in the `user/repos?affiliation=owner` list before archiving. Archiving the wrong copy (org repo via redirect) can be undone with `gh repo unarchive`. See ARCHIVE-REDIRECT-1 anti-pattern.

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
git add <files> ; git commit -m "ACTION:..."

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

## Anti-Patterns
| Anti-Pattern | Fix |
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
| **ARCHIVE-REDIRECT-1: `gh repo archive owner/name` archives the CANONICAL org repo via GitHub 301 redirect — v2.9, 2026-08-04** | When a repo is owned by an org but queried under a different owner path, GitHub returns HTTP 301 → gh follows silently and operates on the canonical org repo. Relying on the owner prefix in `gh repo archive` to target the right copy is UNSAFE. **Fix:** Before archiving, verify the repo's actual owner via `gh api repos/owner/name --jq .owner.login` AND check `user/repos?affiliation=owner` to confirm it's owned by the target account. Canonical case: session PMH0kzte — `gh repo archive rwnq8/ultrametric-physics` archived QNFO/ultrametric-physics (same repo id) because the repo was created directly in the QNFO org, not rwnq8. |
| **CLONE-LEFTOVER-1: Previous session's temp clone blocks a new clone — v2.9, 2026-08-04** | A background Python script that exits before cleanup (`shutil.rmtree`) leaves a clone directory in `%TEMP%`. A subsequent clone in the same session hits "destination path already exists and is not an empty directory." **Fix:** ALWAYS `shutil.rmtree(workdir, ignore_errors=True)` BEFORE cloning, in the same script. Never assume the workdir is clean from a prior run. Canonical case: session PMH0kzte — the killed consolidate.py v1 left `%TEMP%\ultrametric-physics` with bootstrap files, blocking v2's clone. |
| **CHECK-FALSE-SWALLOW-1: `check=False` in subprocess.run swallows git failures with no diagnostic output — v2.9, 2026-08-04** | `subprocess.run(cmd, check=False)` returns a CompletedProcess but the caller never inspects `returncode` or prints `stderr`. The failure is invisible. This is especially dangerous with `git subtree add` which can fail for multiple reasons (no HEAD, remote unreachable, branch mismatch). **Fix:** NEVER use `check=False` on git operations without capturing AND printing both stdout and stderr on non-zero returncode. Use `check=True` (fail-fast, visible) as the default; reserve `check=False` ONLY for operations where failure is expected (e.g., `git rev-parse --verify` to check existence). Canonical case: session PMH0kzte — consolidate.py v1 used `check=False` on all 12 subtree adds, all failed, none were diagnosed until post-hoc verification. |
| **DELETE-BRANCH-DEFAULT-1: `gh pr merge --delete-branch` cannot delete a branch if it was the repo's default at creation — v2.9, 2026-08-04** | When a new repo has only one branch (the feature branch, because main was empty/unborn), GitHub sets that branch as the default. `gh pr merge --delete-branch` refuses to delete the default branch — the branch survives the merge. **Fix:** After PR merge, explicitly set the default branch to `main` via `gh repo edit --default-branch main`, then DELETE the leftover feature branch via API (`gh api -X DELETE repos/owner/repo/git/refs/heads/<branch>`). Verify with `gh api repos/owner/repo/branches`. Canonical case: session PMH0kzte — ultrametric-physics, laws-of-form, cfpe all had leftover `feature/consolidate-projects` branches after merge because they were the repo's default at creation time. |

## Version

**API-FAILURE PROTOCOL (HARD):** When any API call returns 403/401/404, run the API-Failure Self-Diagnosis Protocol (windows-command-patterns S-1.0.6): STOP -> VERIFY your HTTP method/headers -> COMPARE with curl -> THEN consider infrastructure. The bug is ALWAYS your code until proven otherwise (kaizen BLAME-EXTERNAL-1).

Current: **v2.11** (git-github — PowerShell remediation: Remove-Item/Test-Path/$env:TEMP replaced with Python/shutil/%%TEMP%% equivalents per qnfo-core §0.6 Python-First mandate; cross-ref qnfo-core v1.11, windows-command-patterns v3.9; 2026-08-04) (git-github — v2.10: WBS taxonomy; v2.11: PowerShell; 2026-08-04)
