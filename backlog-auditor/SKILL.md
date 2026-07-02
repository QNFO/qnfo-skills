---
name: backlog-auditor
version: 1.0
priority: 1
pinned: false
related: qnfo-agent, closeout-manager, knowledge-graph, cloudflare-deployer
---

# BACKLOG AUDITOR SKILL — v1.0

> **AUTONOMOUS.** Detects projects with only placeholder P0 tasks ("Audit project state and create comprehensive backlog") and generates real, verifiable task registers from D1, KG, and DI state.
> **GAP-CLOSING.** This skill directly addresses the 24 P0 systemic backlog tasks across 23 QNFO projects.

---

## Purpose

Automate the "Audit project state and create comprehensive backlog" pattern. When a project has only auto-generated P0 tasks with no real task register, this skill:
1. Queries D1, KG, and DI for the project's current state
2. Identifies gaps: missing KG edges, missing DI metadata, missing documentation, stale deployment
3. Generates a concrete, verifiable task register
4. Inserts tasks into D1 with proper priority assignments
5. Reports the complete audit trail

## When to Use

| Trigger | Action |
|:--------|:-------|
| Project has P0 task "Audit project state and create comprehensive backlog" | Full audit + task generation |
| New project discovered in DI/KG with no tasks | Initial backlog creation |
| "Audit backlog for [project]" | Targeted audit |
| Session startup discovers uninitialized project | Auto-trigger via qnfo-agent §3.2.1 |

## Workflow — 5 Stages

### Stage 1: State Collection

Query all sources for the project's current state:
- **D1 (qnfo-audit):** Existing tasks, handoffs, decisions
- **Knowledge Graph:** Node properties, BELONGS_TO, DEPENDS_ON, REFERENCES, neighbors
- **Discovery Index:** Metadata (title, summary, url, tags, last_active)

### Stage 2: Gap Analysis

| Gap Rule | Check | Priority |
|:---------|:------|:---------|
| **KG-ORPHAN** | 0 KG edges | P0 |
| **NO-BACKLOG** | Only "Audit project state" tasks exist | P0 |
| **MISSING-TAXONOMY** | No BELONGS_TO to domain | P1 |
| **MISSING-DEPS** | No DEPENDS_ON edges | P1 |
| **STALE-LIFECYCLE** | last_active > 30 days | P1 |
| **MISSING-URL** | No url in DI | P2 |
| **MISSING-SUMMARY** | No summary in DI | P2 |
| **NO-KG-NODE** | In DI but not KG | P2 |
| **NO-DI-ENTRY** | In KG but not DI | P2 |

### Stage 3: Task Generation

For each gap found, generate a concrete task with title, description, priority, and verification criteria.

### Stage 4: D1 Insertion

Insert generated tasks into D1 `qnfo-audit.tasks` via API Worker.

### Stage 5: Reporting

Output complete audit trail: task register, gap matrix, remaining gaps.

---

## Embedded Script: `_backlog_auditor.py`

Usage:
```bash
python _backlog_auditor.py --project qwav --report-only
python _backlog_auditor.py --top 5 --insert  # Audit top-5 + write to D1
python _backlog_auditor.py --all --top 10     # Audit all pending projects
```

Full script available on R2: `qnfo/tools/backlog_auditor.py`

---

## Failure Handling

| Scenario | Response |
|:---------|:---------|
| D1 API unavailable | Flag `[D1-UNAVAILABLE]`, continue with KG + DI only |
| KG API unavailable | Flag `[KG-UNAVAILABLE]`, continue with D1 + DI only |
| No _discovery_index.json | Pull from R2 first, retry |
| Task insert fails (conflict) | Skip duplicate, continue with remaining |

---

*backlog-auditor v1.0 — Closes 24 P0 systemic backlog gaps.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:
1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)
