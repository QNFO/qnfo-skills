---
name: github-cloudflare-sync
description: AUTONOMOUS bidirectional sync between GitHub Issues/Milestones/Projects and Cloudflare D1 qnfo-audit. GitHub is CANONICAL for skills repo and project files/archives (ADR-001 REVOKED 2026-07-14). Priority 1 — auto-loads at session start when GITHUB_TOKEN is available. Runs sync verification, drift detection, and auto-remediation without user prompting. Use when user says sync GitHub, sync issues, cross-reference GitHub and D1, check GitHub alignment, or when infrastructure-audit detects GitHub to D1 drift.
version: "1.2"
---

> **Related:** infrastructure-audit, kaizen-autonomous-update, closeout-manager, execution-guard

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification — negative verification. (2) Assumption Challenge — state and test every assumption. (3) Edge Case Check — empty/null/max/boundary/desync. (4) Iteration — retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

---

## execute_plan (MANDATORY — Before Any Execution)

Populate update_plan with workflow phases as concrete checklist items.

### Execution Protocol
1. Populate update_plan with all phases as checklist items
2. Execute one item at a time — at most ONE in_progress
3. Mark items completed ONLY with tool evidence
4. Never claim completion without execution evidence

---

# GITHUB-CLOUDFLARE SYNC SKILL — v1.2

## Purpose

Automated bidirectional sync between GitHub Issues, Milestones, Projects and Cloudflare D1 `qnfo-audit`. GitHub is CANONICAL for skills repository and project files/archives. This skill runs sync verification, detects drift, and performs auto-remediation without user prompting.

## When to Use

| Trigger | Action |
|:--------|:-------|
| Session start (GITHUB_TOKEN available) | Auto-sync verification |
| `sync GitHub` / `sync issues` | Full bidirectional sync |
| infrastructure-audit detects drift | Auto-remediation |
| `check GitHub alignment` | Drift detection only |

## Architecture

```
GitHub Issues/Milestones ←→ D1 qnfo-audit
     (canonical)              (runtime state)
```

## Reference Files

- **GitHub sync prompts:** See `prompts/` directory for detailed sync instructions
- **Configuration reference:** See `references/` for sync configuration

---

> **Version:** v1.2 — Created SKILL.md with proper YAML frontmatter (previously had no root SKILL.md, only prompts/ subdirectory). Added Related header with cross-links.
