# qnfo-idea-factory

Public read-only window into the QNFO research conversations — an "idea factory"
LLM-like chat UI, live at **https://ideas.qnfo.org** (linked from the QNFO hub
and Papers nav).

## What it does

- Serves a read-only chat UI over the QNFO research conversations saved in
  Cloudflare (`qnfo-audit.chat_sessions`).
- **RESEARCH THREADS ONLY** (v1.1): the public feed serves `category='research'`
  sessions — the user's `deepchat` agent regular sessions. Infrastructure,
  automation, personal, and subagent-audit sessions are stored
  (`category='infra'`) but NEVER served publicly.
- **FULL THREADS** (v1.1): complete user/assistant conversations are
  reconstructed from the local DeepChat `agent.db`
  (`deepchat_messages` + `deepchat_user_messages` + `deepchat_assistant_blocks`)
  by `scripts/log_threads.py` and pushed to the private `qnfo-thread-ingest`
  worker (`POST /threads`, X-Sync-Token auth).
- Real-time: the UI polls `/api/feed?after=` every 30 s and prepends new
  research sessions.

## Pipeline

```
agent.db (local DeepChat)
   │  log_threads.py (daily 05:25 via QNFO_Chat_Log_Push, after log_chat.py)
   ▼
qnfo-thread-ingest.q08.workers.dev/threads  (PRIVATE write, X-Sync-Token)
   ▼
qnfo-audit.chat_sessions  (category=research|infra, full messages JSON)
   ▼
ideas.qnfo.org/api/*  (PUBLIC read, research only, redacted)
```

## Routes (qnfo-idea-factory)

| Route | Purpose |
|---|---|
| `GET /` | Chat UI (LLM-like: session list + chat bubbles) |
| `GET /api/sessions?limit=&offset=&q=` | Research sessions list (q=search title/content) |
| `GET /api/session/:id` | One research session's full messages |
| `GET /api/feed?after=` | Real-time feed of new research sessions |
| `GET /health` | Health + D1 binding check |
| `GET /robots.txt` | Allow all |

## Routes (qnfo-thread-ingest — private)

| Route | Purpose |
|---|---|
| `POST /threads` | Upsert a full thread (X-Sync-Token required) |
| `GET /health` | Health |
| `GET /stats` | Category counts |

## Classification (research vs infra)

`scripts/log_threads.py` classifies each session at push time:
- **research** = agent_id `deepchat` + session_kind `regular` (the user's
  research agent conversations)
- **infra** = everything else (automation agent, personal agent, subagent
  audits, delegation prompts)

The public worker hard-filters `category='research'` server-side — an infra
session id returns `404 Session not found or not public`.

## Redaction layer (mandatory)

Every string is passed through `redact()` before leaving the public worker:
emails, bearer tokens, `token=`/`key=`/`secret=` values, known token prefixes
(`wWbJ…`, `ghp_`, `xox…`), long hex, Windows/MSYS paths, env vars, IPs, phone
numbers, and internal session/run IDs → `[redacted]`. DOIs and URLs are
protected. Verified byte-exact against raw D1 rows (2026-08-28).

## Deploy

```bash
wrangler deploy -c wrangler.jsonc              # qnfo-idea-factory
wrangler deploy -c wrangler-ingest.jsonc       # qnfo-thread-ingest
wrangler secret put SYNC_TOKEN                  # qnfo-thread-ingest only
```

DNS: `ideas.qnfo.org` AAAA `100::` proxied (created 2026-08-28).
Route: `ideas.qnfo.org/*` → `qnfo-idea-factory` (created 2026-08-28).

## QNFO website links

`qnfo-gateway` v3.4.2-identity-fix-v2 was patched (2026-08-28) to add
"Ideas" to the hub nav, the hub cards ("Idea Factory" card), the Papers index
nav, and the paper-detail nav — all pointing at `https://ideas.qnfo.org`.

## v1.1 changelog (2026-08-28)

- Research-only public feed (category filter server-side; infra never served).
- Full multi-message threads (extractor + ingest worker + schema columns
  `category/agent_id/title/model_id/source` on `chat_sessions`).
- Backfilled 136 research + 118 infra sessions from local agent.db.
- Scheduled task `QNFO_Chat_Log_Push` now runs log_threads.py after log_chat.py.
