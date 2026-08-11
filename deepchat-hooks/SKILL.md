---
name: deepchat-hooks
description: DeepChat lifecycle hooks integration — Cloudflare infrastructure audit on session lifecycle events. Manages the cf_audit_hook.py script, the hooksNotifications config schema, and the qnfo-audit integration (qnfo-lifecycle worker endpoints + D1 audit_sessions). Load when the user asks about DeepChat Hooks, lifecycle events, SessionStart/SessionEnd commands, or the Cloudflare infra audit hook.
---

# DeepChat Hooks — Cloudflare Infrastructure Audit

> **v1.1 (2026-08-12):** Red-team fix cycle (CMD RED TEAM 5-adversary direct audit, session
> UgsJmhHMt0OElfaPhKMSk). HARD-1 fixed: timeout budget brought under the app's 30s
> SIGKILL (`COMMAND_TIMEOUT_MS = 30000`) — `HTTP_TIMEOUT` 8→4s, stdin probe 3→0.8s,
> health pings parallelized (worst case ~13s < 25s target; observed 0.3–2.3s). SOFT-2:
> production stdin is never written by the app — script now reads `DEEPCHAT_*` env vars
> as fallback (event/conversationId via argv+env; agentId/workdir from env). SOFT-3:
> module-level `os.makedirs` guarded. SOFT-4: registered command now uses absolute
> `python.exe` path (removes PATH-order dependency + cmd delayed-expansion `!` risk).
> DESIGN-6 fixed: rotated qnfo-lifecycle `CF_API_TOKEN` secret to the working local
> token (drift audit had been silently returning `warnings: ["Cloudflare API returned
> HTTP 400"]` — the live comparison was broken; after rotation the audit surfaced
> REAL drift: 26 stale portfolio workers + 13 missing live workers, verdict
> DRIFT_DETECTED). Skill now git-tracked in qnfo-skills repo (origin + rwnq8) and
> synced to R2 via skill-sync.

## Hook Script

**Path:** `scripts/cf_audit_hook.py` — stdlib-only Python, never raises, exits 0.

**Registered command** (in DeepChat Hooks settings):
```
"C:\Users\LENOVO\AppData\Local\Programs\Python\Python312\python.exe" "C:\Users\LENOVO\.deepchat\skills\deepchat-hooks\scripts\cf_audit_hook.py" --event {{event}} --conversationId {{conversationId}}
```

**What it does:**
1. Reads the full payload from stdin (JSON). **NOTE: in production the app passes NO
   stdin** — the script falls back to argv placeholders and `DEEPCHAT_*` env vars.
2. On **every** event: health-pings `qnfo-lifecycle` /health, `qnfo-gateway` /health,
   `qnfo-archive` /health in PARALLEL (HTTP 200 checks, 4s per-request timeout).
3. On **SessionEnd**: additionally calls `/status` (projects + auditSessions counts)
   and `/run/drift` (full drift audit, which persists to D1 `audit_sessions`).
4. Appends one JSONL record to `logs/audit-YYYY-MM.jsonl` (pruned after 90 days).
5. Prints a compact summary to stdout.

**Record shape (JSONL):**
```json
{
  "ts": "2026-08-12T00:40:01.048Z",
  "event": "SessionEnd",
  "isTest": false,
  "conversationId": "session-123",
  "agentId": "deepchat",
  "workdir": null,
  "source": "deepchat-hook",
  "checks": {"lifecycle": {"ok": true, "http": 200}, "gateway": {...}, "archive": {...}},
  "status": {"ok": true, "http": 200, "projects": 24, "auditSessions": 127},
  "drift": {"ok": true, "http": 200, "verdict": "DRIFT_DETECTED", "driftCount": 39, "drift": [...], "warnings": []},
  "elapsedMs": 1796
}
```

## Timeout Discipline (HARD — 2026-08-12)

The app SIGKILLs any hook command at **30s** (`COMMAND_TIMEOUT_MS = 30000` in
app.asar). The script worst-case budget is ~13s: 0.8s stdin probe + 4s parallel
health (max of 3) + 4s status + 4s drift. **Never raise timeouts above this
budget** — under network degradation a SessionEnd audit would be killed before
`log_record`, silently losing both the JSONL record and the D1 drift audit.

## Hooks Config Schema (from app.asar)

Stored under settings key **`hooksNotifications`** → `{"hooks": [...]}`.

```json
{
  "hooks": [
    {
      "id": "cf-infra-audit-v1",
      "name": "CF Infra Audit",
      "enabled": true,
      "command": "\"C:\\Users\\LENOVO\\AppData\\Local\\Programs\\Python\\Python312\\python.exe\" \"C:\\Users\\LENOVO\\.deepchat\\skills\\deepchat-hooks\\scripts\\cf_audit_hook.py\" --event {{event}} --conversationId {{conversationId}}",
      "events": ["SessionStart", "SessionEnd"]
    }
  ]
}
```

Schema rules (validated by `normalizeHooksNotificationsConfig`):
- `id` (string, optional) — defaults to a random UUID if missing/blank.
- `name` (string, optional) — defaults to `Hook N`.
- `enabled` (boolean) — must be exactly `true` to run.
- `command` (string) — required; command placeholders expanded before exec.
- `events` (array of strings) — only valid event names kept (`sanitizeEvents`).

**CRITICAL placeholder escaping:** the stored command must contain literal
`{{event}}` / `{{conversationId}}` (DOUBLE braces). The app's
`expandHookCommandPlaceholders` regex is `{{\s*([a-zA-Z][a-zA-Z0-9]*)\s*}}` —
single braces `{event}` are left as literal text and the hook receives a broken
arg. When writing the command programmatically, build it with string
concatenation, NOT an f-string (f-strings collapse `{{x}}` → `{x}`).

**Dual-write requirement (HARD):** update BOTH stores or the hook silently
vanishes at restart (same class as MCP-REGISTRATION-ONE-STORE-1):
1. `agent.db` → `app_settings` → `key='hooksNotifications'` (startup persistence)
2. `app-settings.json` → `hooksNotifications` (settingsWatcher live reload)

## Event Semantics

| Event | Payload extras | Hook behavior |
|:------|:---------------|:--------------|
| `SessionStart` | `session` | Health ping only |
| `UserPromptSubmit` | `user.promptPreview` | Health ping |
| `PreToolUse` / `PostToolUse` / `PostToolUseFailure` | `tool` | Health ping |
| `PermissionRequest` | `tool`, `permission` | Health ping |
| `Stop` | `stop.reason` | Health ping |
| `SessionEnd` | `usage` | Health ping + status + drift audit |

Placeholders: `{{event}}` → `%DEEPCHAT_HOOK_EVENT%` (win32), plus `{{time}}`,
`{{isTest}}`, `{{conversationId}}`, `{{workdir}}`, `{{agentId}}`, `{{providerId}}`,
`{{modelId}}`, `{{messageId}}`, `{{toolName}}`, `{{toolCallId}}`. Environment
variables: `DEEPCHAT_HOOK_EVENT`, `DEEPCHAT_HOOK_TIME`, `DEEPCHAT_HOOK_IS_TEST`,
`DEEPCHAT_CONVERSATION_ID`, `DEEPCHAT_WORKDIR`, `DEEPCHAT_AGENT_ID`,
`DEEPCHAT_PROVIDER_ID`, `DEEPCHAT_MODEL_ID`, `DEEPCHAT_MESSAGE_ID`,
`DEEPCHAT_TOOL_NAME`, `DEEPCHAT_TOOL_CALL_ID`.

## Verification

1. Run the script manually with a simulated payload:
   `python scripts/cf_audit_hook.py --event SessionEnd --conversationId test-1` (stdin optional)
2. Check `logs/audit-YYYY-MM.jsonl` for the new record.
3. Verify both stores: agent.db `hooksNotifications` + app-settings.json `hooksNotifications`
   contain the hook entry with `enabled: true` and command with `{{event}}` double braces.
4. Confirm lifecycle `/status` auditSessions count increments after a SessionEnd run
   (drift audit persists to D1).
5. E2E: emulate `expandHookCommandPlaceholders` + `spawn(shell:true)` — run the
   expanded command with `subprocess.run(expanded, shell=True)` (NO manual `cmd /c`
   prefix — Node spawn already wraps it) with `DEEPCHAT_HOOK_EVENT=SessionEnd`.

## Known Findings (2026-08-12)

- **Drift audit now functional** after `CF_API_TOKEN` rotation on qnfo-lifecycle.
  The 2026-08-11 audit surfaced `DRIFT_DETECTED count=39`: 26 stale portfolio
  workers (in D1 portfolio-state, not live) + 13 missing live workers. The
  portfolio-state `resources` table needs reconciliation (defer to a data
  cleanup pass — verify against the 14 live workers listed by the CF API).
- The worker hardcodes `agent="qnfo-lifecycle-cron"` on the D1 drift INSERT, so
  hook-triggered audits are indistinguishable from cron-triggered in D1. The
  local JSONL (`source: deepchat-hook`) is the discriminator.
- On app timeout, Node kills the cmd.exe pid; python.exe (grandchild) may finish
  writing JSONL after the app reports failure. Acceptable for an audit hook.

## Anti-Patterns

| Anti-Pattern | Correct |
|:-------------|:--------|
| **HOOK-SINGLE-STORE-1: Registering hooks in only ONE store** | Dual-write `agent.db` app_settings `hooksNotifications` AND `app-settings.json` `hooksNotifications`. One-store writes vanish at restart or are invisible to live reload. |
| **HOOK-INVALID-EVENT-1: Using an event name outside the 8 valid events** | `sanitizeEvents` silently drops unknown names → hook never fires. Only use: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, Stop, SessionEnd. |
| **HOOK-BLOCKING-1: Hook command that can hang or raise** | Script must be stdlib-only, timeout every network call, never raise, exit 0. Keep worst-case budget < 25s (app kills at 30s). |
| **HOOK-SECRETS-1: Embedding secrets in the hook command/config** | Hook config is stored in plaintext settings. Use environment variables or worker-side secrets (the lifecycle worker already holds CF_API_TOKEN server-side). |
| **HOOK-BRACE-COLLAPSE-1: Writing the command with an f-string collapses `{{event}}` to `{event}`** | Build the command with string concatenation so the stored JSON contains literal `{{event}}` / `{{conversationId}}`. Single braces break placeholder expansion (the app's regex requires double braces). Canonical case: 2026-08-12 `_update_cmd.py` f-string bug — fixed in `_update_cmd2.py`. |
| **HOOK-STALE-TOKEN-1: A rotated/expired worker secret silently degrades the audit (drift returns HTTP 400 warnings with a misleading CLEAN verdict)** | Verify the drift audit's live comparison works: run `/run/drift` and check `warnings` is empty and `liveState.workers` is populated. A 400 with empty liveState means the worker's CF_API_TOKEN is stale — rotate it to a working token (same class as PROVIDER-KEY-SYNC-1). Canonical case: 2026-08-11→12 — 30+ hours of false CLEAN verdicts from a stale token. |

## Related

- qnfo-lifecycle worker: `/health`, `/status`, `/run/drift`, `/run/backup`,
  `/run/secrets-audit`, `/run/ula-check` (D1: qnfo-audit `audit_sessions`).
- deepchat-settings skill: dual-store app_settings patterns.
- qnfo-audit infra: Workers (Lifecycle, Archive, Gateway), R2 `qnfo-audit`,
  D1 qnfo-audit, managed DNS — all tracked for configuration drift.
- qnfo-skill-sync worker + `skill_pull.py`: skills git-tracked in qnfo-skills
  repo (origin QNFO/qnfo-skills + rwnq8 mirror), synced to R2.
