---
name: cost-optimized-routing
description: Fleet-wide cost-optimized model routing stack (L0-L7, COST-ROUTING-STACK-1). Use
  whenever modifying any AI-calling worker's model routing, caching, budgets, or cost telemetry
  (qnfo-ops, qnfo-ai, AI Gateway, Workers-AI calls) to preserve the cost ladder, capability gate,
  and measurement contract.
---

# Cost-Optimized Routing Stack (COST-ROUTING-STACK-1)

Permanent reference: `qnfo-workers/docs/COST-OPTIMIZED-MODEL-CALLS.md` (v2, IMPLEMENTED 2026-09-26).
Live: qnfo-ops v2.37.x (L0/L1/L2/L3/L7 + metrics), qnfo-ai v5.29.0 (semantic cache + metrics),
AI Gateway `default` + `ops` (cache_ttl 86400, invalidate_on_update, monthly-200).
D1 qnfo-audit: `routing_capability`, `routing_policy`, `model_ladder_*`, `cost_router_metrics`.

## The stack (cheapest lever first)

- **L0 deterministic-first** — SQL/regex/probe handlers, cached facts, templates. Biggest lever.
- **L1 cache** — exact KV + semantic Vectorize (serve above cosine threshold) + AI Gateway cache
  (ttl + invalidate_on_update). Context economics: prefix reuse, compaction, bounded tool outputs,
  never re-send full history.
- **L2 capability gate before price gate** — only route to models that pass the canary for the task
  class; a cheap model that fails tool_calls costs MORE via retries. `routing_capability` is the
  matrix; the gate lives in qnfo-ops `agentLoopIncapable()` + the chat-class-only free-first branch.
- **L3 cascade** — free @cf → cheap paid (deepseek-v4-flash) → frontier; escalate ONLY on measured
  failure signals (empty content, tool-call parse failure, validation failure, 429). The
  deterministic verifier is what makes cascades cheap — you don't need a model to verify code, tests do.
- **L4 ensemble/MoA** — only when free or cached. Paid ensembles are N× cost; cheap models share
  training data so ensembles cannot fix shared blind spots — verification still required.
- **L5 distillation** — frontier trajectories offline → small specialist / exemplar bank. (Deferred.)
- **L6 draft-verify** — cheap draft, frontier verify/repair only when checks fail. (Partial.)
- **L7 budget scheduler** — per-tier daily caps (`model_ladder_daily`), graceful degradation order,
  free fallback on cap hit (BUDGET-CAP-FREE-FALLBACK-1), gateway monthly cap, per-job cap.

## Measurement

`GET https://ops.qnfo.org/cost-router/stats` — cost per SUCCESSFUL task by task class, cache hit
rate, escalation count, tool-call validity rate. Every completion path in qnfo-ops and qnfo-ai
writes `cost_router_metrics`. Cost-per-outcome, not cost-per-token.

## Canary protocol (run before ANY upstream/model change)

Prompt the candidate model with a realistic ops tool schema (fleet_status / ops_d1_query / r2_list /
web_fetch / email_check) asking it to call one tool and return its value. PASS = valid tool_calls
block for the right tool. Update `routing_capability` with the result BEFORE deploy
(AGENTIC-CANARY-1); deploying a non-tool-calling upstream for agent loops is a REGRESSION
(`fleet_loop_meta.model_pin` v2). Note: gpt-5.x requires `max_completion_tokens`, never `max_tokens`.

## Maintenance checklist (every AI-calling worker update)

1. L2 gate intact (free-first only for chat class; agent loops consult the capability matrix).
2. Ladder cheapest-capable-first (no T3 default; escalations logged, never silent).
3. Metrics written in every completion path; `/cost-router/stats` green.
4. Caches invalidate (gateway invalidate_on_update, KV TTL, semantic thresholds ≥0.93 ops / ≥0.95 ai).
5. Registry drift zero; R2 `qnfo-canonical/<worker>.js` refreshed after deploy.
6. `routing_policy` D1 rows stay truthful.

## Anti-patterns

Price-only routing · paid ensembles · re-sending full history · unbounded tool outputs ·
capability-agnostic cheap routing · caching without invalidation · trusting a catalog row over a canary.
