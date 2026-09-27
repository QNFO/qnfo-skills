---
name: kaizen-cycle-2026-09-25
description: Kaizen draft from the 2026-09-25 holistic cycle. Five evidence-backed lessons - version-parity audits must read the LAST Current line (first-match produces false positives), the skill-registry gap has a measured cost, reparse-point checks are mandatory before deleting a suspected duplicate, backup snapshot cleanup does not survive a hard kill, and an MCP file edit does not change runtime until app restart.
version: "1.0"
---

# KAIZEN DRAFT — 2026-09-25 HOLISTIC CYCLE

Drafted from the CMD UPDATE (HOLISTIC) cycle of 2026-09-25, executed at root
(child subagent slots frozen; `run_code` unavailable, so `write` + `exec`).

## Gate status at time of drafting (same-turn evidence)

- `prompt-store-verify.py` -> **PASS**, exit **0**
- `scheduler-guard.py` -> **PASS**, exit **0** (0 enabled local cron rows)
- `model_guard.py` -> **state=clean**, exit **0** (8/8 stores clean; 243 sessions pinned `QNFO-OPS/ops-frontier`)
- `service_registry` = **57 rows / 0 unversioned / 0 non-semver**; live CF scripts = **57** -> drift **0**

## K1. VERSION-PARITY-AUDIT-LAST-OCCURRENCE-1 (recurrence, self-inflicted)

**Rule.** A three-way version-parity audit (frontmatter / H1 / footer) MUST read the
**LAST** `Current:` occurrence in the file.

**Why.** Skill files accumulate one `Current:` stanza per version. A first-occurrence
scan returns a historical line, not the footer.

**Evidence (this cycle).** A first-match regex reported three false TITLE-LINE-PARITY-1
breaches:

| skill | reported footer | actual last `Current:` | truth |
|---|---|---|---|
| `kaizen` | 2.70 (false) | L15819 -> v2.155 | consistent |
| `knowledge` | 2.15 (false) | L647 -> v2.16 | consistent |
| `system` | 2.14 (false) | L801 -> v2.15 | consistent |

All three retracted. The guard (`SKILL-ANCHOR-PARITY: PASS`) was correct; the audit was
wrong. The rule was already documented (TITLE-LINE-PARITY-1, MANDATORY 2026-08-19) and
was nonetheless violated — the codification belongs at the point of use.

**Anti-pattern.** Auditing a version with `Select-String | Select-Object -First 1`.

## K2. SKILL-REGISTRY-GAP-COST-1 (measured cost, not just a gap)

**Rule.** Before relying on a skill, verify it is **registered**, not merely on disk.

**Evidence.** `skill_list` exposes **15** skills (generic defaults only). On disk there are
**46** skill dirs / **40** `SKILL.md`. None of `kaizen`, `research`, `cloudflare`,
`qnfo-core`, `execution-mandate`, `system`, `deepchat-settings` appear in the registry; a
targeted query for "kaizen / skills audit / assistant-config / custom templates" matched
**0 of 15**.

**Consequence (the real cost).** A **`bloat-cleanup` v3.5 skill (46,408 chars)** exists on
disk and was **never loaded** during an entire bloat-cleanup cycle. A dedicated skill for
the exact work being performed was invisible.

**Disposition.** Read operational skills from disk until the registry gap is closed.
Closing it is an app-side registry write, owner: user.

## K3. JUNCTION-CHECK-BEFORE-DEDUPE-1 (near-miss, destructive)

**Rule.** Never delete a suspected "duplicate" directory until a reparse-point / hardlink
check proves it is not a link to the live path.

**Evidence.** Planned "dedupe app_db (~25 GB duplicated)". Checks proved:

- `AppData\Roaming\DeepChat` = **Junction -> `DeepChatData\app`**
- `.deepchat` = **Junction -> `DeepChatData\dotdeepchat`**
- `fsutil hardlink list` on `agent.db` -> a **single** path

There was **no duplication**. Executing the plan would have deleted the live config, skills
and secrets. The 24.84 GB actually reclaimed came from *inside* those dirs (orphaned
`%TEMP%` snapshots ~7.2 GB, stale `agent.db.bak-*` ~11.1 GB, dated backup dirs ~7.2 GB).

**Probe.** `Get-Item <path> | Select Attributes,LinkType,Target` + `fsutil hardlink list`.

## K4. BACKUP-SNAPSHOT-HARDKILL-LEAK-1 (active defect, recurrence)

**Rule.** A `finally:` cleanup does not run when a process is hard-killed. Snapshot temp
files must be purged by an independent sweep that tolerates same-day orphans.

**Evidence.** `backup_deepchat.py` writes `%TEMP%\agent-snapshot-<stamp>.db` (~3,581 MB).
`BACKUP-DISK-LEAK-1`'s `finally: os.remove(db_tmp)` is present in both copies, yet two
orphans dated `20260925-121652` and `20260925-121804-settings` survived with lock holder
`pid=1048` already dead. `QNFO-Snapshot-Purge` (daily 03:00, `AGE_HOURS=24`) cannot clean
**same-day** orphans, so up to ~7 GB/day can accumulate until the next 03:00 run.

**Recommended gate.** Purge `agent-snapshot-*` at the **start** of each backup run and/or
give the purge task an hourly trigger with a short age. Note the scheduled task actually
executes `DeepChatData\repo\scripts\backup_deepchat.py` — a **third** copy; any fix must
target that one.

## K5. MCP-TRIM-FILE-VS-RUNTIME-1

**Rule.** Editing `mcp-settings.json` changes the **file**, not the **running** app.

**Evidence.** File shows 9 servers, 6 enabled; `PSV` reports 9 servers with `autoApprove`;
runtime process count for the dropped servers was **13** (respawned), not 0. `PSV` states it
explicitly: the running app rewrites them from its runtime; the file is the source of truth
and re-syncs after app restarts. A restart is required to apply.

**Anti-pattern.** Claiming "MCP trimmed" as a runtime fact from a file read.

## Failure modes of this draft

1. K1 is derived from a **local** regex re-check, not from the canonical parity tool.
2. K2's registry census is from `skill_list` at one instant; a concurrent session could register skills.
3. K4's "up to ~7 GB/day" is extrapolated from a single-day two-orphan sample.
4. K3 rests on three paths only; other QNFO paths could still be linked.
