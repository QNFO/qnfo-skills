# qnfo-idea-factory

Public read-only window into the QNFO research conversations — an "idea factory"
LLM-like chat UI, live at **https://ideas.qnfo.org** (linked from the QNFO hub
and Papers nav).

## What it does

- Serves a read-only chat UI over the QNFO chat data already saved in Cloudflare:
  - `qnfo-audit.chat_sessions` — full conversation threads (JSON message arrays)
  - `qnfo-audit.chat_logs` — session metadata rows (title/summary/model) fed live
    by the local `log_chat.py` → `qnfo-skill-sync /log/chat` pipeline
- Real-time: the UI polls `/api/feed?after=` every 30 s and prepends new sessions.
- Public, read-only, no auth, no write endpoints.

## Routes

| Route | Purpose |
|---|---|
| `GET /` | Chat UI (LLM-like: session list + chat bubbles) |
| `GET /api/sessions?limit=&offset=&kind=&q=` | List sessions (kind=all\|threads\|logs, q=search) |
| `GET /api/session/:id` | One session's full messages (threads) or record (logs) |
| `GET /api/feed?after=` | Real-time feed of sessions newer than `after` |
| `GET /health` | Health + D1 binding check |
| `GET /robots.txt` | Allow all |

## Redaction layer (mandatory)

Every string is passed through `redact()` before leaving the worker:

- Emails → `[redacted]`
- Bearer tokens and `token=`/`key=`/`secret=`/`password=` values → `[redacted]`
- Known token prefixes (`wWbJ…`, `ghp_`, `xox…`, wrangler OAuth) → `[redacted]`
- Long hex (32+) and generic 24+ alnum runs → `[redacted]`
- Windows paths (`C:\…`), MSYS paths (`/c/Users/…`), env vars (`%TEMP%`) → `[redacted]`
- IP addresses and phone numbers → `[redacted]`
- Internal session/thread/run/delegation IDs → shortened to `name:[redacted]`
- DOIs and URLs are **protected** (never mangled)

## Deploy

```bash
wrangler deploy   # wrangler.jsonc binds qnfo-audit D1 as QNFO_AUDIT
```

DNS: `ideas.qnfo.org` AAAA `100::` proxied (created 2026-08-28).
Route: `ideas.qnfo.org/*` → `qnfo-idea-factory` (created 2026-08-28).

## QNFO website links

`qnfo-gateway` v3.4.2-identity-fix-v2 was patched (2026-08-28) to add
"Ideas" to the hub nav, the hub cards ("Idea Factory" card), the Papers index
nav, and the paper-detail nav — all pointing at `https://ideas.qnfo.org`.
