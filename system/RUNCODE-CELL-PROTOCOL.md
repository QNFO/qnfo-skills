# RUN_CODE Cell Protocol — stop the sudden terminations (2026-09-02)
# Load this BEFORE Code Mode work: skill_view("system") -> RUNCODE-CELL-PROTOCOL.md
# Companion guard: python C:/Users/LENOVO/.deepchat/scripts/runcode-guard.py (canonical QNFO/qnfo-ops/scripts/)

## Why cells die — app.asar primary evidence (RUNCODE-HALT-LIMITS-2026-09-02)
DeepChat run_code executes each cell in its OWN Electron utilityProcess fork
(codeModeUtilityHost.js, execArgv ["--max-old-space-size=64"]). The parent enforces:

| # | Mechanism | Value | Kills when | Surface text |
|---|-----------|-------|------------|--------------|
| 1 | HEARTBEAT_TIMEOUT_MS (liveness watchdog, ~1s tick) | 3500 ms | event-loop stall >3.5s: sync exec/grep, huge-result serialization, busy-wait | "Code cell heartbeat timed out." |
| 2 | READY_TIMEOUT_MS (spawn gate, NO retry) | 5000 ms | utility process not READY within 5s of fork (parallel dispatch, machine under load) | "Code mode utility did not become ready within 5 seconds" |
| 3 | script.runInContext sync prefix | 2000 ms | long synchronous prefix at cell start | runInContext timeout |
| 4 | RSS monitor (1s) on 64MB-heap child | soft Δ128MB / hard 512MB | growing large objects / giant strings in-cell | kill (often no clean error) |
| 5 | RUN_CODE_OUTPUT_MAX_BYTES | 1 MiB | prints + nested tool results exceed cap | "Code mode output exceeded the 1 MiB limit" |
| 6 | one active cell per session | — | a second concurrent run_code call in the same session | spawn/READY failure |

Effective budget is min(3.5s heartbeat-silence, timeout_ms) — the documented 5-min
timeout_ms does NOT buy long synchronous work.

## Verified 2026-09-02 termination trend (agent.db deepchat_messages, 1335 rows)
last 24h / last 7d mentions: heartbeat_timeout 21/98, ready_timeout 20/29,
output_cap+alt 6/27, sync_prefix 5/13. This is the pain the user reports; every
cell we author must be shaped to not add to it.

## Cell-authoring rules (HARD for every run_code cell)
1. ONE logical op per cell; never chain 6+ subtool calls "just in case".
2. Never print/return raw blobs (worker code, big JSON, asar slices) — extract 1-2
   small fields, curate to <2KB of console output. Output cap = 1 MiB TOTAL incl.
   nested tool results.
3. No synchronous heavy work: no giant in-cell regex over MBs, no busy-wait, no
   multi-thousand-row array builds. Keep cells short enough that event-loop gaps
   stay <3.5s.
4. Subtool results arrive as STRINGS (RUNCODE-SUBTOOL-STRING-1): exec returns
   "…\nExit Code: N"; JSON results need JSON.parse before property access. Accessing
   .stdout on a string yields "" — looks like "empty", is a parse bug.
5. Prefer bounded async subtools over exec where possible. For exec: prefer
   background:true + process poll for anything non-trivial (RUNCODE-EXEC-BG-1);
   foreground exec may return empty; retry once on "Session … is not running".
6. Do NOT dispatch run_code calls in parallel within one turn (READY_TIMEOUT /
   one-active-per-session). Sequential only.
7. Heavy-read subtools (tape_search, get_conversation_history, big search_* ) risk
   heartbeat kill on result serialization — bound limit/low, one per cell.
8. Catch ToolCallError around every subtool; never let an unhandled rejection kill
   the cell silently.
9. Sandbox has NO setTimeout/setInterval/fetch/process/Buffer — use poll loops,
   web_fetch/curl subtools, and background exec sessions.
10. update_plan first and after each phase; keep plan items ≤10 words; no
    micro-cell churn (the user's #1 time complaint).

## If a cell still dies
1. Treat the death as DATA: match the surface text to the table above.
2. Do NOT retry the same shape. Split into smaller cells / smaller outputs /
   background exec / sequential dispatch.
3. Verify the replacement with a same-turn read-back (small cell).
4. Same-turn evidence gate: never claim "cell done" without its printed result.

## Guard
- runcode-guard.py exit 0 verifies (A) asar constants match baseline (drift = a
  DeepChat update changed the limits — re-baseline + re-document BEFORE diagnosing),
  (B) DB termination-signature trend, (C) this doc exists in live + repo.
- Re-run after every DeepChat app update and in every ops cycle that touches Code Mode.

## Claim sheet (FRAMEWORK-DOGFOOD-1)
| Claim | Evidence | Confidence | Status |
|-------|----------|------------|--------|
| 5 kill mechanisms + 1-active-cell exist | app.asar 2026-08-31 build, constants grepped/streamed | high | verified 2026-09-02 |
| HEARTBEAT 3500 / READY 5e3 / output 1MiB in current build | runcode-guard.py ASAR check PASS | high | verified 2026-09-02 |
| Terminations recur across sessions | DB scan d1 counts (heartbeat 21, ready 20) | medium (content mentions over-count) | verified 2026-09-02 |

