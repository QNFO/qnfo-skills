---
name: git-github
description: Git workflow operations and GitHub project management -- conventional commits, branch recovery, merge conflicts, detached HEAD, stash recovery, GitHub Issues, PRs, Wikis, Releases, Milestones, project boards, and GitHub-D1 sync. GitHub is CANONICAL for skills repository and project files/archives.
version: "2.2"
triggers: ["git", "commit", "merge", "rebase", "branch", "push", "pull", "detached HEAD", "conflict", "stash", "reflog", "GitHub", "Issues", "PRs", "pull request", "wiki", "releases", "Milestones", "project board", "GitHub sync", "D1 sync", "repo", "repository", "fork", "clone", "remote", "origin", "main", "master", "feature branch"]
related: []
priority: 2
platform: all
autonomous: false
self_sufficient: true
---
> **v2.4 UPDATE (2026-08-02, kaizen — Cloudflare tool discoverability):**
> Ephemeral-memory mandate: memories are NOT permanent — skill instructions must name
> the actual agent tools. GitHub-D1 Sync (this skill) touches Cloudflare D1 via
> `query_graph` and `workers_list` for verification. For any D1/Worker/R2 state
> verification, use the agent tools `query_graph(endpoint, params)` and
> `workers_list` (see cloudflare skill §Skill Cross-Reference v3.18). Never rely
> on durable memory for Cloudflare operational state.
> Cross-reference: cloudflare v3.18.


# GIT-GITHUB -- v2.4 (Ultra-Consolidated VC + PM)

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
PHANTOM CLAIM (`qnfo-agent` §9.11 Rule 14) — BLOCKED.

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
- Always use feature branches: `feature/<kebab-case-description>`
- Branch naming: lowercase, hyphens, descriptive (no underscores, no CamelCase)
- Verify before commit: `git branch --show-current`
- Examples: `feature/kaizen-update-2026-07-17`, `feature/cfpe-stage-4-red-team`

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
- **Create repo:** Via GitHub API or web UI
- **Clone:** `git clone <url>`
- **Push:** `git push origin <branch>`
- **Pull:** `git pull origin <branch>`

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
git clone <url> $env:TEMP\<project>

# Step 2: Apply ALL edits (this turn only)

# Step 3: Commit (MANDATORY SAME TURN — never defer)
git add <files> ; git commit -m "ACTION:..."

# Step 4: Push (MANDATORY SAME TURN — never defer)
git push origin <branch>

# Step 5: Verify push reached remote (Anti-Phantom Gate)
git ls-remote origin <branch>

# Step 6: Delete local clone immediately
Remove-Item -Recurse -Force $env:TEMP\<project>
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
