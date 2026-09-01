# CLOUD-SYNC — 100% Cloud Delivery & Settings Sync

Directive (2026-09-01, user): all local/deepchat/GitHub skills + settings must SYNC with Cloudflare "100% cloud" infrastructure (workers/execution). Local state = ephemeral mirror; Cloudflare = canonical (Worker Secrets canonical for all tokens/keys). Execution must NOT assume local Windows DeepChat is open.

## Sync map
| Local/deepchat/GitHub | Cloud target | Status (2026-09-01) |
|---|---|---|
| Skills repo (C:/Users/LENOVO/.deepchat/skills, git master) | GitHub QNFO/qnfo-skills (canonical verified: master branch HTTP 200; write-to-obsidian.py tracked, commit 044e0c8) | DONE (verified 2026-09-01) |
| Settings parity stores (customPrompts, system-prompt v2.7/v3.95 dual-write, prompt-stores 10-vs-12) | Cloud canonical + prompt parity store | OPEN - prompt-store 10-vs-12 parity pending (handoff 28823) |
| write-to-obsidian.py (local python, APPEND defect documented) | obsidian-writer Worker (classic, R2 VAULT binding, delete-then-create via atomic put) | DONE (deployed 2026-09-01, verified code+binding) |
| Obsidian vault (D:/Obsidian, NOT a git repo) | R2 bucket obsidian-vault (WEUR) as cloud vault mirror | PARTIAL - bucket created; worker writes notes/v1/...; local Obsidian Git sync = follow-up |
| Cloud crons | qnfo-twin-maintain 04:00Z, research-daily-brief 06:00Z, personal-life-maintain 02:00Z, Citation Watch, Conference Radar | Registered; first runs 2026-09-02 (verify logs) |

## obsidian-writer Worker (deployed 2026-09-01)
- Name: obsidian-writer - Classic format - Deployment abd78c6d - Tag 5c5d2282
- Binding: VAULT -> r2_bucket obsidian-vault (verified via bindings API, 200)
- Semantics: POST {slug, section, content, date} -> atomic R2 put to notes/v1/YYYY/MM/DD/_slug-YYYY-MM-DD.md (delete-then-create; replaces the local python append bug)
- Responses: 405 non-POST - 400 missing slug/content - JSON {ok,key,bytes}
- Pending: workers.dev subdomain enable (token scope 10405 - needs dashboard toggle or broader token) -> live route obsidian-writer.q08.workers.dev

## Follow-ups
1. Enable workers.dev route for obsidian-writer (dashboard) + live smoke POST.
2. Local Obsidian vault -> cloud mirror sync (Obsidian Git plugin pointing at R2-backed repo, or vault mirror repo).
3. Settings parity stores -> cloud canonical (prompt-store 10-vs-12, handoff 28823).
4. First cloud cron runs 2026-09-02 04:00/06:00Z: verify memory_maintain_runs + brief output in cloud vault.
5. Skills/settings drift check: git status clean each cycle; push-only own files (GIT-OWNERSHIP-1).


## CLAIM SHEET (FRAMEWORK-DOGFOOD-1 — this record's locked claims)
| Claim | Source | Verified | Confidence |
|---|---|---|---|
| CSYNC-01 GitHub canonical write-to-obsidian.py on master (HTTP 200) | raw.githubusercontent.com/QNFO/qnfo-skills/master/... (fetch 2026-09-01) | YES | HIGH |
| CSYNC-02 obsidian-writer Worker deployed (classic, abd78c6d) | Cloudflare Workers API + code readback | YES | HIGH |
| CSYNC-03 R2 bucket obsidian-vault exists (WEUR) | r2_buckets_list 2026-09-01 | YES | HIGH |
| CSYNC-04 CLOUD-SYNC.md claim sheet committed dcde072 + c60679a, merged/pushed as d136e4f | git ls-remote origin/master == HEAD d136e4f (2026-09-01) | YES | HIGH |
| CSYNC-05 D1 handoffs 28841 + wbs_state cloud-sync 6/6 | D1 SELECT | YES | HIGH |
| CSYNC-06 job-market-watch Workflow deployed + instance ran (6 steps, success; instance bd1524ba, workflow debe5193) | Workflows API instance status + D1 self-record 28845 | YES | HIGH |
