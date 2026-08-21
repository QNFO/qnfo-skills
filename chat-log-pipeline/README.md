# chat-log-pipeline

DeepChat session-log → kaizen-issue pipeline. The local collector pushes DeepChat
session metadata + error telemetry to the `qnfo-skill-sync` Worker; the Worker's
kaizen cycle extracts actionable issues via Workers AI into D1 `qnfo-audit`.

## Files
- `log_chat.py` — local collector v2 (QNFO.INF.LOGCAP.W1-5, 2026-08-21)
- `kaizen_surface.py` — ≤5-line open-issue surfacing for Daily Ops §4b (W10)
- `deploy_worker.py` — multipart PUT deploy helper (canonical deploy path)
- `meta-prod.json` — non-secret bindings for the PUT (secrets re-attach by name)
- `worker.js` — qnfo-skill-sync v1.1.2 source (deployed 2026-08-21)

## v1.1.x changes (2026-08-21)
- W1 real error signal: `deepchat_messages.status='error'` (replaces keyword heuristic, ~60% false positives)
- W1 payload adds `error_count` + `error_sample` (actual failure text feeds the extractor)
- W2 cap 100→1000 (`--limit`); W3 per-row retry; W4 console title; W5 `/kaizen/run` trigger after push
- W6 extractor v2 + `normalizeTitle` dedup; W7 stale auto-close >30d; W8 skill-source issues
- v1.1.1 lock TTL reclaim; v1.1.2 TTL 20min + async cap 30 rows (waitUntil ~300s wall-clock kill found in prod)

## Local install
Copy `log_chat.py` + `kaizen_surface.py` + `.sync_token` into `%USERPROFILE%\.deepchat\scripts\`.
Daily Ops §4b restore path: this repo, `chat-log-pipeline/`.

## Deploy
```
python deploy_worker.py qnfo-skill-sync worker.js <worker.js> meta-prod.json
```
Rollback: Workers Versions API v23 (wrangler) or local `backups/qnfo-skill-sync.worker.js.v23-bundle`.
