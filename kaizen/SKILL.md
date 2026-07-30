---
name: kaizen
description: Proactive skill improvement protocol — audit, upgrade, and harden any skill or configuration artifact. Mandatory red-team review with parallel subagent orchestration. Uses structured forecasting to predict skill needs BEFORE users report problems. Use when the user asks to audit, improve, update, or kaizen a skill; when a skill shows staleness signals (stale refs, contradictions, outdated banners); when a skill's dependencies have changed; or when proactively scanning for skill rot across the ecosystem. Incorporates the research skill's forecast protocol as a design pattern for anticipating future skill requirements.
---

> **v1.1 UPDATE (2026-07-30, kaizen — self-kaizen):**
> Red-team review: 5 parallel subagents attempted, all truncated; fell back to direct
> parent-agent audit (Self-Kaizen Protocol invoked). HARD findings: 2 (both negated —
> `skill_run` confirmed as valid tool, research v2.31 confirmed via `skill_view`).
> Changes:
> (1) Added Self-Kaizen Protocol section — mandatory steps when kaizen audits itself
> (S-01, parent-agent).
> (2) Added Subagent Failure Handling section — truncated outputs must trigger direct
> fallback (S-02, parent-agent).
> (3) Added pre-flight checks to Phase 0 — `memory_recall`, `tape_info`, `tape_anchors`,
> double-kaizen detection (S-03/S-05, parent-agent).
> (4) Added Phase 4 disambiguation note — distinguishes research skill's Phase 4 from
> kaizen's Phase 4 (S-04, parent-agent).
> (5) Added `update_plan` and `cronjob` to Cross-Skill Integration table (D-01/D-02,
> parent-agent).
> (6) Added Kaizen History Log section — per-skill `.kaizen_history` tracking (D-03,
> parent-agent).
> (7) Added Calibration Register section — dated fragility predictions (D-04,
> parent-agent).
> (8) Added 7 new anti-patterns: history log, update_plan, truncation, memory_recall,
> cronjob, calibration register, double-kaizen.
> Cross-reference: research v2.31 (confirmed live), self-kaizen protocol now documented.

# KAIZEN v1.1 (Proactive Skill Improvement Protocol)

## Overview

Kaizen is a continuous-improvement protocol for skills and configuration
artifacts. It has two modes:

1. **Reactive kaizen** — triggered by user request ("audit X skill", "update Y
   for Z change"). This is the minimum baseline.
2. **Proactive kaizen** — triggered by detecting drift signals BEFORE the user
   notices. This is the target state. The research skill's forecast integration
   (v2.31) is the canonical case study: the improvement (Forecast Integration
   Map) was NOT a user-requested fix — it was an architectural insight that
   made the "seamless weaving" of forecasting into research explicit and
   auditable.

## Self-Kaizen Protocol (MANDATORY when kaizen audits itself)

When the kaizen skill is kaizening itself (self-kaizen), the agent MUST:

1. **Read the skill independently** — do not rely solely on subagent outputs; subagent_orchestrator truncation can lose audit findings. The parent agent must also read the full SKILL.md directly.
2. **Cross-verify every version reference** — the canonical case study (research skill v2.31) must be live-verified via `skill_view("research")` to confirm the version header matches. Never trust a `skill_list` description field for version numbers; those are separate metadata that may drift independently of the actual SKILL.md heading.
3. **Test every tool name claim** — the Runtime Context block may reference tools that were available at creation time but could have been renamed/deprecated. Verify each tool name against the current available tools list.
4. **Use `update_plan` from Phase 0** — track progress through Phases 0-5 with the progress checklist tool so the self-kaizen execution is auditable.

## Subagent Failure Handling (MANDATORY)

When subagent_orchestrator outputs are truncated, the parent agent MUST:

1. **Assume findings were lost** — truncated output is equivalent to "subagent did not complete." Do not treat partial output as a findings report.
2. **Fall back to direct audit** — the parent agent reads the target skill directly and performs the audit dimensions itself. The explorer/reviewer roles are assigned as perspectives the parent agent adopts sequentially, not as subagent delegations that can silently fail.
3. **Report the failure** — in the kaizen closeout banner, note: "N subagents attempted, M completed with full output; (N-M) fell back to direct parent-agent audit due to truncation."

## Kaizen Pipeline (Standard Execution)

### Phase 0: Trigger Detection

**Pre-flight checks (run BEFORE Phase 1):**
- `memory_recall({query: "<skill-name> kaizen"})` — check for prior kaizen sessions on this skill. Log the most recent session date and version.
- `tape_info()` — inspect current session tape for related kaizen activity.
- `tape_anchors()` — check for recent kaizen handoff anchors.
- If a prior kaizen session completed within the last 24 hours on the same skill, flag `[RECENT-KAIZEN: <date>, v<version>]` and confirm the user wants to kaizen again. Double-kaizen (two consecutive kaizen sessions with no user changes between them) is an anti-pattern.

Kaizen initiates from one of these signals:

| Signal | Example | Reactive or Proactive |
|:-------|:--------|:----------------------|
| **User directive** | "Audit X skill" | Reactive |
| **Cross-skill version drift** | Skill A references Skill B v2.3, but B is now v3.0 | Proactive |
| **Tool capability change** | New MCP server available, skill doesn't use it | Proactive |
| **Dependency retirement** | Script deleted in a parent skill, child skill still references it | Proactive |
| **Self-audit interval** | Any skill not kaizen'd in >30 days | Proactive |
| **Forecast signal** | Structured forecast predicts a skill will need update within N weeks | Proactive |
| **Incident-triggered** | A session failed because a skill was wrong (e.g., stale token, deleted script) | Reactive |

> **Disambiguation:** Where this skill says "Phase 4 (Structured Forecast)," it refers to the **research skill's** Phase 4 (Deep Research & Structured Forecast Protocol). The kaizen skill's own Phase 4 is "Verification Gate." Context determines which is meant: the case study and forecast protocol sections reference the research skill; the pipeline phases reference kaizen itself.

### Phase 1: Skill Audit (Explorer Subagent)

Delegate to an **explorer** subagent: read the target skill end-to-end, produce
a structured audit report.

**Audit dimensions:**

1. **Staleness Audit** — Does the skill reference deleted scripts, deprecated
   tool names, retired endpoints, or stale version numbers?
2. **Contradiction Audit** — Does any section contradict another? Does the
   `execute_plan` match what phase sections actually describe?
3. **Completeness Audit** — Are all gates covered? Missing verification steps?
   Missing anti-patterns?
4. **Cross-Skill Dependency Audit** — Does this skill reference other skills
   that have version-drifted? Do those skills still have the sections/versions
   referenced?
5. **Structural Audit** — Duplicate sections? Copy-paste artifacts?
   Anti-patterns appearing multiple times? Banners that restate the same thing?
6. **Capability Gap Audit** — Are there new tools, MCP servers, or patterns
   this skill should leverage but doesn't?

**Output:** A structured audit report with line numbers, severity ratings
(HARD/SOFT/DESIGN), and proposed fixes for each finding.

### Phase 2: Red-Team Review (Reviewer Subagents — PARALLEL)

**MANDATORY for every kaizen.** Run 3-5 reviewer subagents in parallel, each
assigned one adversarial perspective:

| Reviewer Role | Core Question | Assignment |
|:--------------|:--------------|:-----------|
| **Accuracy Auditor** | Are the skill's factual claims still true? (endpoints, tool names, file paths, script existence, version numbers) | Verify every external reference |
| **Completeness Auditor** | What's missing? (gates, anti-patterns, edge cases, new capability integration) | Gap analysis against ecosystem |
| **Dependency Auditor** | Do cross-skill references resolve correctly? Have referenced skills drifted? | Cross-reference all `See X skill vN.M` claims |
| **Novelty Auditor** | What new capabilities should this skill leverage? (new MCP servers, new tools, new patterns from other skills) | Capability-matrix gap scan |
| **Status Auditor** | Are all version banners accurate? Is the closing banner current? Are KIF tags consistent? | Banners + metadata reconciliation |

**Orchestration pattern:**
```
subagent_orchestrator(operation="run", mode="parallel", tasks=[
  {slotId: "reviewer", title: "Accuracy", ...},
  {slotId: "reviewer", title: "Completeness", ...},
  {slotId: "reviewer", title: "Dependency", ...},
  {slotId: "reviewer", title: "Novelty", ...},
  {slotId: "reviewer", title: "Status", ...},
])
```

**Gate:** Phase 3 (apply fixes) MUST NOT begin until ALL reviewer subagents
have returned findings. This is a HARD GATE — partial review is no review.

**Minimum bar:** At least 3 of the 5 roles must complete. If only 2 can run
(insufficient subagent slots), run the remaining roles sequentially in the
parent session. Never skip a role.

### Phase 3: Apply Fixes (Implementer — SEQUENTIAL after Phase 2)

Collate all audit findings (Phase 1 + Phase 2) into a prioritized fix list:

| Priority | Definition | Action |
|:---------|:-----------|:-------|
| **HARD** | Would cause a session failure if not fixed (stale endpoint, deleted script, wrong tool name) | Fix immediately, before any other change |
| **SOFT** | Degrades quality but doesn't break execution (duplicate text, formatting, missing anti-pattern) | Fix in this kaizen session |
| **DESIGN** | Architectural improvement (new section, restructured workflow, forecast integration) | Fix in this kaizen session; document rationale |

Apply fixes using the `edit` tool (surgical) or `write` (full rewrite). After
each fix, verify with `read` that the change landed correctly.

**Implementation principle:** Batch related fixes when safe, but NEVER fix
multiple HARD issues in one edit — each HARD fix gets its own tool call so
a partial failure doesn't leave the skill in an unknown state.

### Phase 4: Verification Gate

After all fixes applied:

1. **Self-verification:** Re-run the audit checks from Phase 1 against the
   updated skill. Confirm every finding is resolved.
2. **Red-team re-review:** Run at least ONE reviewer subagent against the
   updated skill with a fresh prompt: "Verify all fixes from [kaizen session]
   were applied correctly. Find any remaining gaps."
3. **Cross-skill sync check:** If this kaizen involved cross-skill changes,
   verify the OTHER skill's version/references are updated too.
4. **Critical gate:** If any HARD finding is not verifiably fixed, BLOCK
   the closeout. Do not declare kaizen complete with unresolved HARD issues.

### Phase 5: Closeout

```
1. VERSION BUMP: Increment the skill's version in the SKILL.md header
   (e.g., "# SKILLNAME -- v1.0" → "# SKILLNAME -- v1.1")
2. KAIZEN BANNER: Insert a dated banner summarizing ALL changes, including
   which red-team roles found what. Format:
   > **vN.M UPDATE (YYYY-MM-DD, kaizen):**
   > Red-team review: N parallel subagents + direct forensic audit.
   > Changes: (1)... (2)... (3)...
   > Cross-reference: [any related skill updates].
3. MEMORY: `memory_remember(category="task_outcome")` with a summary of
   changes and the new version.
4. TAPE: `tape_handoff(name="kaizen/<skill-name>-vN.M", summary="...")`
5. SYNC: If this is a live-installed skill, ensure the on-disk file is
   current. No git commit required for skill files outside a repo.
```

## Proactive Kaizen: The Forecast-Driven Model

### Why Reactive-Only Kaizen Fails

Reactive kaizen (waiting for the user to say "audit X") has a systematic blind
spot: it only finds problems the user already suspects. Problems the user
doesn't know about — stale references in skills they haven't loaded recently,
cross-skill version drift, new capabilities not yet integrated — accumulate
silently until they cause a session failure.

### The Forecast-Driven Alternative

For skills that are part of an active ecosystem (multiple interdependent skills
evolving in parallel), run a **proactive kaizen forecast** at regular intervals
or after any significant ecosystem change (major skill version bump, new MCP
server deployment, tool retirement).

**Protocol (adapted from the research skill's Structured Forecast Protocol):**

1. **Domain Assessment:** Map the skill ecosystem. Which skills depend on which
   others? What external dependencies (MCP servers, APIs, tools) does each
   skill have?

2. **Drift Candidate Identification:** For each skill, identify:
   - Cross-references to other skills with specific version numbers
   - References to scripts in other skills
   - References to tools/APIs that might change
   - Anti-patterns that reference deprecated workflows

3. **Assumption Audit:** For each cross-reference, ask: "What would have to
   change in the referenced skill to make THIS skill's reference stale?"
   Flag every assumption.

4. **Red-Team Challenge:** "What is the MOST LIKELY thing to break in this
   skill within the next 30 days?" Run the answer through the 5-adversary
   framework from Phase 2.

5. **Calibration Register:** For each identified risk, register a dated
   prediction: "[CHECK: YYYY-MM-DD] Skill X will need update because
   dependency Y will change by [date]."

6. **Effort Allocation:** Rank skills by predicted fragility. Most-fragile
   skills get kaizen'd first.

**Case Study: Research Skill v2.31 Forecast Integration**

The Forecast Integration Map added in v2.31 was a proactive kaizen finding.
It was NOT triggered by a user complaint or a broken reference — it was
triggered by the observation that:

- Phase 4 (Structured Forecast) was mandatory for ALL research projects
- But there was no explicit map showing HOW forecast outputs fed into
  Phases 1-8
- An agent could treat forecasting as a standalone deliverable to "check off"
  rather than the analytical engine generating the paper's claims

This finding was discovered by applying the **Novelty Auditor** perspective:
"What structural improvement would make the integration so explicit that no
agent could misunderstand it?" The answer was a cross-reference table mapping
every forecast stage to its publication-phase integration point.

The user's feedback ("I like how forecasting is seamlessly woven in") confirmed
the value of this proactive approach. Reactive kaizen would never have
suggested this — only proactive gap-scanning did.

### When to Run Proactive Kaizen

| Trigger | Action |
|:--------|:-------|
| Any skill reaches a major version bump (v2.0 → v3.0) | Kaizen all skills that reference it |
| New MCP server deployed | Scan all skills for capability gaps |
| Tool deprecation announced | Kaizen all skills that use the deprecated tool |
| >30 days since last kaizen on any skill | Run the proactive forecast protocol |
| Session failure traced to a stale skill reference | Kaizen the failing skill + all skills that reference it |
| **Scheduled audit (monthly)** | Use `cronjob` to run a `kaizen --batch --dry-run` scan of all installed skills; review findings before applying |

## Red-Team Integration (MANDATORY)

### The 5-Adversary Framework

Every kaizen MUST include ALL five adversary perspectives. No skipping "because
this is a simple update." A simple update can hide a complex oversight.

| # | Adversary | Question | Assignment to Subagent |
|:--|:----------|:---------|:----------------------|
| 1 | Accuracy Auditor | "These claims are wrong — here's why" | `slotId: "reviewer"` |
| 2 | Completeness Auditor | "This is missing critical gates — here's what's absent" | `slotId: "reviewer"` |
| 3 | Dependency Auditor | "Cross-references are broken — skill X moved to v3, this still says v2" | `slotId: "reviewer"` |
| 4 | Novelty Auditor | "This skill is outdated — it should use [new capability] but doesn't" | `slotId: "reviewer"` |
| 5 | Status Auditor | "Version banners are contradictory — v2.3 claims a fix that v2.4 says was reverted" | `slotId: "reviewer"` |

### Subagent Configuration

```
Subagent slots:
- reviewer × 5 (for parallel red-team audit)
- explorer × 1 (for initial skill audit in Phase 1)
- implementer × 1 (for applying fixes in Phase 3, if needed — 
  usually the parent agent does this directly)

Parallel mode: Phase 2 (all 5 reviewers run concurrently)
Sequential dependency: Phase 2 MUST complete before Phase 3 begins
```

### Minimum Viable Red-Team (when subagent slots are limited)

If only 2 reviewer slots exist:
1. **First wave (parallel):** Accuracy + Completeness
2. **Second wave (parallel):** Dependency + Novelty
3. **Third wave (direct):** Status audit (parent agent)

If only 1 reviewer slot exists:
1. Run all 5 sequentially
2. Each gets a FRESH subagent session (no context contamination)
3. This is slower but still complete — speed is sacrificed, not thoroughness

## Anti-Patterns

| Anti-Pattern | Correct |
|:-------------|:--------|
| Skipping red-team review because "it's a simple update" | ALL kaizen includes red-team. A "simple" update that introduces a wrong version number in a cross-reference can silently break another skill. |
| Running only 1-2 adversary roles because "the skill is small" | All 5 roles. A small skill can have all the same failure modes as a large one. |
| Applying fixes without re-verifying with a fresh reviewer subagent | Phase 4 re-review is mandatory. The implementer's own verification is insufficient — the same agent that made the error is the worst auditor of its fix. |
| Deferring DESIGN findings because "they're not critical" | DESIGN findings are architecture improvements — they prevent future HARD findings. Defer them once, but never twice. |
| Not updating cross-referenced skills when a dependency changes | If Skill A's kaizen changes a shared reference (e.g., a script path), immediately audit Skill B (which also references it). Cross-skill drift is the #1 source of stale references. |
| Writing a kaizen banner that says only "various fixes" | Every kaizen banner MUST itemize changes with numbered entries and red-team provenance. A future agent reading the banner should know exactly what changed and why. |
| Reactive-only kaizen — never scanning for drift | Run the proactive forecast protocol at least monthly, or after any major ecosystem change. Skills rot silently. |
| Treating the forecast as an optional "nice to have" | Forecast-driven gap detection (like the research skill v2.31 Forecast Integration Map) finds improvements that reactive kaizen never would. It's not optional — it's how you avoid accumulating technical debt. |
| Not storing kaizen outcomes in durable memory | Every kaizen closeout writes to `memory_remember(task_outcome)`. Future sessions need to know what was changed and why. |
| **Kaizening a skill without first checking its history log** | Read `.kaizen_history` or `kaizen-history.json` first — duplicate kaizen on unchanged code is wasted effort. |
| **Running kaizen without `update_plan` tracking** | Use `update_plan` from Phase 0 through Phase 5 — untracked kaizen is unauditable kaizen. |
| **Treating subagent truncation as successful audit completion** | Truncated subagent output = subagent did not complete. Fall back to direct parent-agent audit per Subagent Failure Handling section. |
| **Skipping `memory_recall` before starting kaizen** | Check for prior kaizen sessions in durable memory — a skill kaizened 2 hours ago with no intervening changes does not need a re-kaizen. |
| **Never scheduling proactive kaizen** | Use `cronjob` to run monthly `kaizen --batch` scans — skills rot silently without scheduled vigilance. |
| **No calibration register after kaizen closeout** | Register dated fragility predictions per the Calibration Register section — so future agents know what to watch for.

## Cross-Skill Integration

| Skill | Load at Phase | Purpose |
|:------|:-------------|:--------|
| `skill-creator` | Phase 0 (if creating a new skill) | Skill structure, progressive disclosure patterns |
| `git-github` | Phase 5 (closeout, if skill lives in a repo) | Conventional commits for kaizen changes |
| `knowledge` | Phase 5 (closeout) | KG/D1 logging of skill state changes |
| `memory-management` | Phase 5 (closeout) | Durable memory for kaizen outcomes |
| `update_plan` | Phase 0 (and all phases) | Progress tracking and auditability of kaizen execution |
| `cronjob` | Phase 5 (closeout, optional) | Schedule recurring proactive kaizen audits |

## Version

Current: **v1.1** (kaizen — self-kaizen, 2026-07-30)

This is the first version of the kaizen skill. It was created in direct
response to the research skill v2.31 kaizen session, which demonstrated
the value of:

1. **Proactive gap detection** (the Forecast Integration Map was not a
   user-requested fix — it emerged from architectural analysis)
2. **Parallel red-team review** (3 subagents found different classes of
   issues; no single reviewer would have caught all of them)
3. **Forecast-driven kaizen** (the user explicitly praised the "seamless
   weaving" of forecasting into research and wanted it as a model for
   future improvements)

The research skill v2.31 kaizen is the canonical case study embedded in the
Proactive Kaizen section above.

## Kaizen History Log (MANDATORY per-skill tracking)

Every kaizen session writes an entry to a per-skill history log. For skills
inside a git repo, the log is `kaizen-history.json` at the repo root. For
standalone skills (like this one), the log is a `.kaizen_history` file in
the skill directory. Format:

```json
{
  "skill": "kaizen",
  "entries": [
    {
      "version": "v1.0",
      "date": "2026-07-30",
      "type": "creation",
      "red_team_roles": 5,
      "hard_findings": 0,
      "soft_findings": 5,
      "design_findings": 4,
      "summary": "Initial creation. Red-team: 5 parallel subagents + direct parent-agent audit."
    }
  ]
}
```

**Purpose:** Future kaizen sessions read this log to understand what was
already fixed, what remains open, and whether the skill is on a predictable
improvement trajectory. A skill with no history log is indistinguishable
from one that has never been audited.

## Calibration Register (DESIGN — forward-looking fragility predictions)

For skills in an active ecosystem, the kaizen closeout produces fragility
predictions. These function like the research skill's Calibration Register:
dated, falsifiable claims about skill drift risk.

```
[CHECK: 2026-08-30] Kaizen skill will need update because:
- Cross-Skill Integration references research v2.31 — if research reaches
  v3.0, the canonical case study claim may become misleading.
- Subagent slot availability may change — the 5-adversary framework assumes
  5 reviewer slots exist.
Likelihood: [MODERATE] — research skill is actively evolving.
```
