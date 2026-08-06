> **v2.5 UPDATE (2026-08-06, kaizen — EMAIL-ROUTE-STRIP-1 + duplicate-H1 structural fix):**
> Red-team: direct parent-agent audit (session SFkcXsRZjmvs4TMr9Fo_m — kaizen cycle #3).
> HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **EMAIL-ROUTE-STRIP-1 anti-pattern added** — the qnfo-email Worker route-strip
>     `if (p.startsWith('/email')) { p = p.replace('/email','') }` mangles `/emails/*` paths on the
>     workers.dev host: plain `/emails/recent`, `/emails/body?id=N`, `/emails/search` return the
>     catch-all ENDPOINT INDEX (HTTP 200, wrong payload — SILENT failure). Working form on the
>     workers.dev host: `/email/emails/recent` (the strip normalizes it). Fix in worker: scope the
>     strip to `p === '/email' || p.startsWith('/email/')`. Canonical case: 2026-08-06 email
>     follow-up session — ~15 probe calls burned before the working form was found.
> (2) [SOFT] **Duplicate H1 fixed** — version header `# Email Composer — 2.4` normalized to
>     `# Email Composer — v2.5`; descriptive title H1 demoted to H2 per N-2 (one H1 per file).
> Cross-reference: kaizen v1.80, qnfo-core N-2, N-2-SCAN-FALSE-POSITIVE-1, API-DOC-GAP-1.

> **v2.3 UPDATE (2026-08-04, kaizen — orphan artifact removal + cmd.exe curl syntax):**


> Red-team: direct parent-agent audit (session C8CxG7CWs3AOR9w37Q5c8).


> HARD: 3. SOFT: 2. DESIGN: 0.


> Changes:


> (1) [HARD] **Orphan artifact removed**: scripts/physical-number-theory-*.pdf


>     (an unrelated physics PDF) deleted from this skill — violated file hygiene


>     and skill-bloat metrics (kaizen v1.5).


> (2) [HARD] **CMD.EXE curl syntax documented**: all curl examples use bash `$KEY`


>     which does NOT expand under the exec tool's cmd.exe. Added cmd.exe note


>     with `set KEY=`/`%KEY%` alternative.


> (3) [HARD] **Missing v2.2 banner repaired**: the Current line said v2.2 but the


>     banner block at top only showed v2.1 (auth gate). Banner chain now complete.


> (4) [SOFT] **WRANGLER-PATH-REGRESSION-1 note**: `wrangler email routing rules`


>     may fail if wrangler is off PATH (2026-08-04 regression). Fallback: use


>     Cloudflare MCP tools or the zone-level REST API.


> (5) [SOFT] Worker source path canonicalized to `C:\Users\LENOVO\.deepchat\workers\qnfo-email\qnfo-email.js`.


> Cross-reference: cloudflare v3.27, kaizen v1.18, qnfo-core N-2.





---


name: email-composer


description: Email triage, drafting, reading, and sending for qnfo.org via the qnfo-email Cloudflare Worker. Use when the user asks to check email, read messages, reply, compose, or manage filters for @qnfo.org addresses.


version: 2.4


triggers: ["check email", "read email", "send email", "reply to", "compose email", "draft email", "my inbox", "manage filters", "block sender", "auto-reply", "email history", "search email", "qnfo email", "inter-personal communication"]


related: ["qnfo-core", "cloudflare", "knowledge"]


priority: 2


platform: cloudflare


autonomous: true


self_sufficient: true


---





# Email Composer — v2.5





> **v2.4 UPDATE (2026-08-05, kaizen — WORKER-SOURCE-EVICTED-1 + CF API key retrieval):**


> Red-team: direct parent-agent audit of session 8APhB8pdpgihrWgDLpXIP


> (research briefing email archive wiring). HARD: 1. SOFT: 1. DESIGN: 0.


> Changes:


> (1) [HARD] **WORKER-SOURCE-EVICTED-1** — the local Worker source at


>     `C:\Users\LENOVO\.deepchat\workers\qnfo-email\` (wrangler.toml +


>     qnfo-email.js) NO LONGER EXISTS (thin-client eviction 2026-08-05). The


>     Worker itself is LIVE in Cloudflare (v1.6, qnfo-email.q08.workers.dev).


>     API key retrieval fallback documented: GET


>     `https://api.cloudflare.com/client/v4/accounts/{acct}/workers/scripts/qnfo-email/settings`


>     with `Authorization: Bearer $CLOUDFLARE_API_TOKEN` → `result.bindings[]`


>     find `name == "API_KEY"` → `text`. Account:


>     edb167b78c9fb901ea5bca3ce58ccc4b. (verified 2026-08-05)


> (2) [SOFT] Orphan PDF: v2.3 banner claimed scripts/physical-number-theory-*.pdf


>     was deleted, but the file was STILL PRESENT until removed again 2026-08-05


>     (verified gone now). Banner claims of deletion must be verified with a


>     dir listing in the same pass.


> Cross-reference: kaizen v1.43, cloudflare v3.33, research v2.77,


> session 8APhB8pdpgihrWgDLpXIP.








> **v2.1 (2026-08-03, red-team — send pipeline fix):**


> Red-team audit found `POST /send` failing with 500. Root cause: the qnfo-email Worker


> used the deprecated positional `new EmailMessage(from, to, ...)` constructor. Cloudflare


> Email Service now requires the object-builder API: `send({to, from, subject, text, html})`.


> Worker bumped v1.3 → v1.5 with the fix; all 9 endpoints verified 200. The `send_email`


> binding must be UNRESTRICTED (no `destination_address`) for general sending.


> Cross-reference: cloudflare v3.22 (EMAILMSG-1, SEND-BIND-RESTRICT anti-patterns),


> qnfo-email Worker v1.5.





## Email Composer — Inter-Personal Communication via Cloudflare Worker





> **v2.0 (2026-08-03, kaizen — Cloudflare-native migration):**


> Complete rewrite. Email infrastructure migrated from Outlook/win32com to the


> `qnfo-email` Cloudflare Worker. All qnfo.org email now lives in Cloudflare:


> inbound routed via Email Routing rules → Worker processes/stores in D1 →


> DeepChat queries the Worker HTTP API to read, search, send, and manage filters.


> Zero Outlook dependency. Zero win32com. Zero desktop automation for email.


>


> Changes:


> (1) [HARD] Phase 0: Outlook win32com account discovery → Worker /health probe.


> (2) [HARD] Phase 1: Computer Use Outlook navigation → Worker GET /emails/recent + /search.


> (3) [HARD] Phase 2: win32com item.Body → Worker GET /emails/body?id=N.


> (4) [HARD] Phase 5: Outlook Reply button click → Worker POST /send.


> (5) [SOFT] Added phase 6 (filter management) and phase 7 (memory logging).


> (6) [SOFT] All win32com/Outlook code blocks removed. Computer Use references removed.


> (7) [DESIGN] Integration table updated: cloudflare replaces windows-command-patterns + CUA.


> Cross-reference: cloudflare v3.22, qnfo-email Worker v1.5, qnfo-core.





## Quick Start





> **CMD.EXE NOTE (v2.3):** All curl examples below use bash `$KEY` syntax.


> The exec tool runs `cmd.exe`, which does NOT expand `$KEY`. On Windows use:


> - Either `set KEY=<API_KEY>` then `%KEY%` in commands (cmd.exe variable syntax), OR


> - Inline the key directly: `curl -s -H "Authorization: Bearer <API_KEY>" ...`


> The Worker returns HTTP 401 without a valid Bearer key on ALL endpoints (except OPTIONS).








> **ALL Worker requests require auth (v1.6+).** Send `Authorization: Bearer <API_KEY>` on every call.


> API key: `~/.deepchat/workers/qnfo-email/wrangler.toml` → `[vars] API_KEY`


> **NOTE (v2.4): local wrangler.toml may be thin-client EVICTED. Fallback:


> GET `https://api.cloudflare.com/client/v4/accounts/edb167b78c9fb901ea5bca3ce58ccc4b/workers/scripts/qnfo-email/settings`


> (Bearer CLOUDFLARE_API_TOKEN) → bindings[].name=="API_KEY" → text.


> (WORKER-SOURCE-EVICTED-1, verified 2026-08-05)


> No key → HTTP 401. Key wrong → HTTP 401.





**Read recent email:**


```bash


KEY="<API_KEY from wrangler.toml>"


curl -s -H "Authorization: Bearer $KEY" https://qnfo-email.q08.workers.dev/emails/recent?limit=10


```





**Read a specific email:**


```bash


curl -s -H "Authorization: Bearer $KEY" "https://qnfo-email.q08.workers.dev/emails/body?id=1"


```





**Search email:**


```bash


curl -s -H "Authorization: Bearer $KEY" "https://qnfo-email.q08.workers.dev/emails/search?q=research"


```





**Send email / reply:**


```bash


curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $KEY" \


  https://qnfo-email.q08.workers.dev/send \


  -d '{"to":"person@example.com","subject":"Re: Hello","body":"Thanks for reaching out.","reply_to_id":1}'


```





**Get stats:**


```bash


curl -s -H "Authorization: Bearer $KEY" https://qnfo-email.q08.workers.dev/stats


```





**The Worker routes ALL @qnfo.org email.** No desktop app needed. All endpoints except `OPTIONS` preflight require the Bearer key.





---





## Core Workflow





### Phase 0: Connectivity Check (MANDATORY — run before Phase 1)





Verify the Worker is healthy and email is flowing:





```


1. curl -s -H "Authorization: Bearer $KEY" https://qnfo-email.q08.workers.dev/health


   → Expect: {"status":"ok","version":"1.6","bindings":{"d1":true,"send_email":true,...}}


   → If status != "ok": Worker may be down. Check wrangler deploy logs.


   → If d1 == false: D1 binding missing — redeploy Worker.


   → If HTTP 401: API_KEY mismatch — read key from wrangler.toml [vars].





2. curl -s -H "Authorization: Bearer $KEY" https://qnfo-email.q08.workers.dev/stats


   → Expect: {"total":<N>,"last24h":<M>,...}


   → If total == 0: no email has been received yet, OR D1 is not connected.





3. Verify Email Routing rules are routing to the Worker:


   wrangler email routing rules list qnfo.org


   → (if wrangler is off PATH, use Cloudflare MCP / REST API per WRANGLER-PATH-REGRESSION-1)


   → ALL rules should show "Actions: worker:qnfo-email" (not "forward:*@outlook.com")





4. memory_recall({query: "email sent OR replied OR qnfo-email"})


   → Check for recent email interactions in durable memory.


```





### Phase 1: Discovery & Triage





**List recent emails:**


```bash


curl -s -H "Authorization: Bearer $KEY" "https://qnfo-email.q08.workers.dev/emails/recent?limit=20"


```


Returns metadata for each email: id, sender, recipient, subject, classification, status, received_at.





**Search for specific emails:**


```bash


curl -s -H "Authorization: Bearer $KEY" "https://qnfo-email.q08.workers.dev/emails/search?q=<keyword>"


```


Searches across sender, subject, and body_text fields.





**Triage checklist:**


- Parse the JSON response. Extract: id, sender, subject, classification.


- Categorize by urgency:


  - `classification: "personal"` — from known contacts (e.g., rowan.quni@qnfo.org) → highest priority


  - `classification: "research"` or `"publications"` — bizdev/research opportunities


  - `classification: "alerts"` — infrastructure notifications


  - `status: "rejected"` or `"spam"` — filtered, skip unless user asks


- **Critical search tip:** Sender addresses may differ from display names. Always search by domain (e.g., `@example.com`) or partial name first, before assuming identity.





### Phase 2: Analysis





**Read full email body:**


```bash


curl -s -H "Authorization: Bearer $KEY" "https://qnfo-email.q08.workers.dev/emails/body?id=<id>"


```


Returns: sender, recipient, subject, body_text, body_html, headers_json, classification, status, received_at, processing_ms.





**Analysis steps:**


1. Extract sender identity from `sender` field and cross-reference with `search_memories` and `recall_facts` for prior interactions.


2. Read `body_text` for the full message content.


3. Check `headers_json` for additional context (reply-to, in-reply-to, references).


4. Search for prior conversation threads:


   - `curl -s -H "Authorization: Bearer $KEY" "https://qnfo-email.q08.workers.dev/emails/search?q=<sender_email>"`


   - Or: `curl -s -H "Authorization: Bearer $KEY" "https://qnfo-email.q08.workers.dev/emails/search?q=<subject_keyword>"`


5. Check durable memory for decisions related to this sender/topic:


   - `search_memories({query: "<sender name> OR <topic>"})`


   - `recall_facts({keyword: "<sender email>"})`





### Phase 3: Strategic Context





- **ALWAYS** verify QNFO agent is loaded via `skill_view("qnfo-core")` before drafting — it contains the Research Integrity Mandate and governance framework.


- If QNFO/QWAV commercial positioning is relevant, read `references/qnfo-qwav-strategy.md`.


- If the response requires specific communication patterns, read `references/email-patterns.md`.


- Cross-reference against qnfo-core §0.0 (Research Integrity) — no marketing language, no promissory statements, certainty labels required.





### Phase 4: Drafting





1. Determine the strategic goal: accept, decline, defer, pitch, gather information, maintain relationship.


2. Apply the QNFO/QWAV positioning from `references/qnfo-qwav-strategy.md`.


3. Apply tone guidelines from `references/email-patterns.md`.


4. Run through qnfo-core §0.0: banned words check, certainty calibration, falsifiability check.


5. Present the draft to the user with explicit strategic rationale before sending.





### Phase 5: Delivery





**Send the reply via the Worker:**


```bash


curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $KEY" \


  https://qnfo-email.q08.workers.dev/send \


  -d '{


    "to": "recipient@example.com",


    "subject": "Re: Original Subject",


    "body": "Plain text reply body...",


    "reply_to_id": <original_email_id>


  }'


```





**Parameters:**


| Field | Required | Description |


|:------|:--------|:------------|


| `to` | Yes | Recipient email address |


| `subject` | No | Subject line (defaults to "(no subject)") |


| `body` | No | Plain text body |


| `html` | No | HTML body (falls back to body text wrapped in `<p>`) |


| `reply_to_id` | No | D1 email ID this is replying to — marks original as "replied" |





**The Worker automatically:**


- Sends via the `SEND_EMAIL` binding (DKIM-signed, SPF-aligned)


- Records the sent email in D1 with `status: "sent"`


- Marks the original email as `status: "replied"` if `reply_to_id` is provided





**On success:** `{"success":true,"message_id":"<uuid>","to":"...","subject":"...","sent_at":"..."}`





### Phase 6: Mark as Processed





After reading or replying to an email, update its status:


```bash


curl -s -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer $KEY" \


  https://qnfo-email.q08.workers.dev/emails/status \


  -d '{"id": 1, "status": "read"}'


```





**Valid statuses:** `received`, `processed`, `sent`, `replied`, `archived`, `spam`, `read`, `rejected`





### Phase 7: Log to Memory





After any email interaction, remember it for future sessions:


```


memory_remember(category="task_outcome", content="Email interaction: <sender> — <subject> — <action taken>. Email ID: <id>.")


```





---





## Filter Management





### List filters:


```bash


curl -s -H "Authorization: Bearer $KEY" https://qnfo-email.q08.workers.dev/filters


```





### Create a filter:


```bash


curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $KEY" \


  https://qnfo-email.q08.workers.dev/filters \


  -d '{


    "field": "from",


    "pattern": "spammer@example.com",


    "action": "reject",


    "priority": 10


  }'


```





**Filter fields:** `from`, `to`, `subject`, `body` (or empty for all fields)


**Filter actions:** `accept` (default), `reject` (bounce), `auto_reply` (send template), `notify` (webhook), `tag` (classify)





### Delete a filter:


```bash


curl -s -X DELETE -H "Authorization: Bearer $KEY" https://qnfo-email.q08.workers.dev/filters/<id>


```





---





## qnfo-email Worker API Reference





| Endpoint | Method | Purpose | Example |


|:---------|:-------|:--------|:--------|


| `/health` | GET | Binding status, version | `curl -s -H "Authorization: Bearer $KEY" .../health` |


| `/stats` | GET | Total, last24h, by classification, by status | `curl -s -H "Authorization: Bearer $KEY" .../stats` |


| `/emails/recent` | GET | List emails (limit, offset, status filter) | `curl -s -H "Authorization: Bearer $KEY" ".../emails/recent?limit=20&status=received"` |


| `/emails/body` | GET | Full email body by ID | `curl -s -H "Authorization: Bearer $KEY" ".../emails/body?id=5"` |


| `/emails/search` | GET | Search sender/subject/body | `curl -s -H "Authorization: Bearer $KEY" ".../emails/search?q=meeting"` |


| `/emails/status` | PATCH | Update status | `curl -s -X PATCH -H "Authorization: Bearer $KEY" ... -d '{"id":1,"status":"read"}'` |


| `/send` | POST | Send email | `curl -s -X POST -H "Authorization: Bearer $KEY" ... -d '{"to":"...","subject":"...","body":"..."}'` |


| `/filters` | GET/POST | List/create filters | `curl -s -H "Authorization: Bearer $KEY" .../filters` |


| `/filters/:id` | DELETE | Remove filter | `curl -s -X DELETE -H "Authorization: Bearer $KEY" .../filters/5` |





**Worker source:** `C:\Users\LENOVO\.deepchat\workers\qnfo-email\qnfo-email.js`


**Worker URL:** `https://qnfo-email.q08.workers.dev`


**D1 database:** `qnfo-audit` (tables: `emails`, `email_filters`)


**Bindings:** `SEND_EMAIL`, `AUDIT_DB`, `NOTIFY_WEBHOOK`





---





## Integration Points





| Skill / Tool | When to Load | What It Provides |


|:-------------|:-------------|:-----------------|


| `qnfo-core` | Before drafting any response | Research Integrity Mandate, governance, banned words, certainty labels |


| `cloudflare` | For Worker management, D1 queries, infrastructure context | Workers fleet status, D1 query tools, Email Routing rules |


| `knowledge` | Before checking contact history | KG querying, memory search (`search_memories`, `recall_facts`) |


| `research` | When citing QNFO publications in replies | Paper lookup, DOI retrieval, publication context |


| `exec` (curl) | Throughout — ALL email operations | Worker HTTP API queries |


| `wrangler` | Email Routing rule management | `wrangler email routing rules list qnfo.org` |





---





## Key Constraints





- **Description must stay ≤176 chars** (same scanner bug that broke qnfo-core and system).


- All email operations go through `curl` → `qnfo-email.q08.workers.dev`. No desktop apps.


- Drafts must pass qnfo-core §0.0 before delivery — no exceptions.


- Never fabricate citations or DOI references. Verify via `search_papers_enriched` or `get_paper_context`.


- The Worker records ALL sent emails in D1 — replies are traceable.


- The `send_email` binding sends FROM the address configured in wrangler.toml (currently `qnfo@qnfo.org`).


- If `qnfo@qnfo.org` is not yet verified, catch-all won't forward to it — unknown addresses are dropped.





---





## Anti-Patterns





| Anti-Pattern | Correct |


|:-------------|:--------|


| Launching Outlook to check qnfo.org email | Query the Worker API: `curl -s -H "Authorization: Bearer $KEY" https://qnfo-email.q08.workers.dev/emails/recent` |


| Using win32com / Python COM for email | Use `curl` HTTP calls to the Worker. All email is in D1, not in Outlook. |


| Using Computer Use to navigate Outlook UI | No desktop email client needed. The Worker IS the email client. |


| Reading email body via UIA tree / screenshot | `curl -s -H "Authorization: Bearer $KEY" ".../emails/body?id=N"` — full text, no truncation. |


| Sending email via Outlook Reply button | `POST /send` — DKIM-signed, SPF-aligned, recorded in D1. |


| Assuming email is only in Inbox | All qnfo.org mail goes to the Worker. D1 is the canonical store. |


| Forgetting to mark emails as read | `PATCH /emails/status {"id":N, "status":"read"}` after reading. |


| Not logging email interactions to memory | `memory_remember(category="task_outcome", ...)` after every interaction. |


| Treating all qnfo.org addresses equally | Classifications (research/alerts/publications/personal/general) drive priority and response strategy. |


| Searching D1 directly instead of using Worker API | The Worker API is the canonical interface. D1 queries bypass classification and logging. |


| Skipping Phase 0 connectivity check | Always run `/health` + `/stats` + verify Email Routing rules before email operations. |


| Omitting `reply_to_id` when replying | Include `reply_to_id` so the Worker can mark the original email as "replied". |


| **Calling Worker endpoints without `Authorization: Bearer <API_KEY>`** | ALL endpoints (except `OPTIONS`) return HTTP 401 without the key. Read the key from `wrangler.toml [vars] API_KEY`. v1.6+ enforces this — a red-team audit proved full inbox read + send-as was possible with zero auth (2026-08-03). |





---





| **EMAIL-ROUTE-STRIP-1: qnfo-email Worker route-strip mangles `/emails/*` on the workers.dev host — plain `/emails/*` returns the catch-all endpoint index (HTTP 200, silent wrong payload) (2026-08-06)** | On the workers.dev host use the `/email`-prefixed form (`/email/emails/recent`, `/email/emails/body?id=N`) — the strip normalizes it to `/emails/*`. Fix in worker source: scope strip to `p === '/email' || p.startsWith('/email/')`. Canonical case: session SFkcXsRZjmvs4TMr9Fo_m — ~15 probes burned. Cross-ref: API-DOC-GAP-1. |
## References





- `references/qnfo-qwav-strategy.md` — QWAV commercial thesis, Qubit Delusion series, Manifesto, Problem-Substrate Mapping, JPCUB positioning


- `references/email-patterns.md` — Communication patterns: declining opportunities, pitching QWAV, follow-ups, relationship maintenance





**Worker source:** `C:\Users\LENOVO\.deepchat\workers\qnfo-email\qnfo-email.js` (v1.6)


**Worker deploy:** `wrangler deploy` from `C:\Users\LENOVO\.deepchat\workers\qnfo-email\`





---





## Version





**API-FAILURE PROTOCOL (HARD):** When any API call returns 403/401/404, run the API-Failure Self-Diagnosis Protocol (windows-command-patterns S-1.0.6): STOP -> VERIFY your HTTP method/headers -> COMPARE with curl -> THEN consider infrastructure. The bug is ALWAYS your code until proven otherwise (kaizen BLAME-EXTERNAL-1).





Current: **v2.5** (email-composer — WORKER-SOURCE-EVICTED-1 + CF API key fallback; 2026-08-05)

