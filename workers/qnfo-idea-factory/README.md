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
| `POST /api/ask` | Ask the corpus (proxies qnfo-qwav) + related research threads |
| `POST /api/proposals` | Public idea proposal (honeypot + rate limit) |
| `GET /api/proposals` | Private review queue (X-Sync-Token required) |
| `GET /health` | Health + D1 binding check |
| `GET /robots.txt` | Allow all |

## Routes (qnfo-thread-ingest — private)

| Route | Purpose |
|---|---|
| `POST /threads` | Upsert a full thread (X-Sync-Token required) |
| `GET /health` | Health |
| `GET /stats` | Category counts |

## Classification (research vs infra) — v3 content-based

`scripts/log_threads.py` classifies each session at push time with a
**content-based scoring classifier** (calibrated 2026-08-28 on the full
deepchat-regular corpus: 5 research / 138 infra of 143 sessions):

- **research** requires BOTH:
  1. agent_id `deepchat` + session_kind `regular` (automation/personal/
     subagent sessions are NEVER public), AND
  2. content test: the title or ANY user-message intent scores >= 2 research
     terms and more research terms than infra terms (vocabulary in
     `log_threads.py`: p-adic/ultrametric/quantum/anyon/critique/paper/
     numeracy/laws-of-form ... vs ui/api/cloudflare/email/git/audit/...).
- User-message intent = text BEFORE the first `CMD <WORD>:` marker (CMD
  RESEARCH / CMD PUBLISH / CMD CONTINUE / CMD RED TEAM ...) with file paths
  stripped — CMD boilerplate (git/commit/branch/worker words) never pollutes
  the score.
- Display titles fall back to the first meaningful user intent for sessions
  whose title is only a file path.

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

## Changelog

### v1.5 (2026-08-28) — RSS + embed + hash deep-links + chat-UI gate
- /rss.xml (40-item research-thread feed), /embed (iframe widget, 60s refresh)
- #/s/<id> hash deep-links (RSS/embed/topics link straight into a thread)
- scripts/chat-ui-click-test.py added to qwav-demo-kit: real-background light
  theme scan (fixes the MathJax 'black' false positive), canvas optional,
  mobile 375px overflow check. ALL CHECKS PASSED on both surfaces.
- log_threads.py v4: dedicated research agent (id 'research') sessions are
  research by definition — hard separation; deepchat regular keeps the content
  test as safety net.
- qnfo-cloud-ops v1.2.1: briefing + weekly include idea_proposals review.
- Fixed: template-literal regex corruption (hash handler broke the UI script),
  mobile grid blowout (min-width:0 + overflow-wrap:anywhere).

### v1.4 (2026-08-28) — math rendering + dedupe
- MathJax (tex-svg) + markdown-inline renderer (`renderRich` + `typeset`) on BOTH
  surfaces: ideas.qnfo.org Ask box, conversation message bubbles, and the
  ask.qwav.tech answer panel. `\(...\)`/`$$...$$`/`$...$` now render as math,
  `**bold**`/`*italic*`/code as HTML. renderRich is backslash/backtick-free
  (String.fromCharCode + split/join) because it lives inside a template literal.
- Thread dedupe + junk filter: `collapseThreads()` merges duplicate titles
  (the June scrape's ~40 "What is ultrametric geometry?" duplicates collapse to
  one; junk "test"/"hi"/"hello" dropped). 118 -> 62 research threads.

### v1.3 (2026-08-28) — Ask + participation layer
- Fixed ask.qwav.tech: qnfo-qwav `/ai/ask` now uses the AVAILABLE AI + Vectorize
  + D1 bindings (embed → search qwav-research-v2 → enrich from living-paper →
  compose via Workers AI chat). The old AI-Search (QNFO_SEARCH) path was never
  bound; this is the working path. CORS now `*` for the public read-only API.
- Ask box on ideas.qnfo.org: `/api/ask` proxies to qnfo-qwav and surfaces
  related research threads (tokenized ANY-match; short queries need 1 match).
- Propose an idea: public form → `idea_proposals` D1 table (honeypot + 3/hr/IP
  rate limit); private review at `GET /api/proposals` (X-Sync-Token).
- ask.qwav.tech page: nav link to ideas.qnfo.org, canonical/og → ask.qwav.tech
  (deployed via wrangler pages).

### v1.2 (2026-08-28)
- v3 content-based research classifier (agent rule + research-dominant content
  scoring of title/user intents; CMD boilerplate + paths stripped). Calibrated:
  5 research / 138 infra. Empty closeout stubs skipped. Display titles derived
  from first meaningful user intent.

### v1.1 (2026-08-28)
- Research-only public feed (category filter server-side; infra never served).
- Full multi-message threads (extractor + ingest worker + schema columns
  `category/agent_id/title/model_id/source` on `chat_sessions`).
- Backfilled 136 research + 118 infra sessions from local agent.db.
- Scheduled task `QNFO_Chat_Log_Push` now runs log_threads.py after log_chat.py.
