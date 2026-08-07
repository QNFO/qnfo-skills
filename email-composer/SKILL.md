> **> **v2.12 UPDATE (2026-08-07, kaizen — AUTONOMOUS OUTREACH: cronjob now SENDS, not just drafts + red-team subagent audit):**
> Red-team: 4 parallel subagents (Accuracy/Completeness/Novelty/Status — all completed) + direct
> parent-agent audit (session Nff8tKtjHf6VDCfRejuNd — EXECUTE RED TEAM SUBAGENTS).
> User mandate: "AUTOMATE OUTREACH CONTACTS ENTIRELY, I'M NOT GOING TO TELL YOU TO INITIATE OUTREACH."
> VERSION-OVERWRITE-1 merge past concurrent v2.11 (session MerOabc5KO_W9Q8BP47ok, MEMORY-TO-SKILL-DRIFT:
> PROCESSED-STUCK-SPAM-1, PER-RECIPIENT-FILTER-GAP-1, HUMAN-ONLY-ROWAN-QUNI). HARD: 0. SOFT: 1. DESIGN: 2.
> Changes:
> (1) [HARD conversion] **Cronjob upgraded to autonomous sending** — the qnfo-email-inbox-check
>     (id 3851f539) now autonomously SENDS outreach emails on Monday (scan Zenodo→arXiv→find emails→
>     draft→send 3-5 per paper) and Friday (auto-send follow-ups to 14d silent contacts). Previously
>     drafted for user approval — now sends directly, reporting what was sent. Notification changed
>     from "drafts ready" to "Sent N emails to: [recipient list]." Dedup: checks D1 before sending
>     (same recipient + same paper DOI = skip). Email verification via Google Scholar; unreachable
>     contacts reported as [SKIPPED: no email found].
> (2) [DESIGN] **Cronjob ping cronjob-ping** — weak exec verification: saved to
>     %TEMP%\ec_cronjob_show.txt and read-back confirmed the autonomous taskPrompt.
> (3) [DESIGN] **Subagent red-team methodology** — 4 parallel reviewers completed; accuracy auditor
>     found subagent-access gap (cronjob tool unavailable in child sessions — parent-verified).
>     Completeness auditor correctly identified draft-only→send gap as HARD. Status auditor
>     discovered concurrent v2.11 bump. Novelty auditor identified multi-channel/D1-tracking/
>     auto-classification/audience-auto-match gaps (all DESIGN, deferred).
> (4) [SOFT] **Kaizen v1.84** — this cycle's retrospective: autonomous outreach pivot, subagent
>     red-team integration, VERSION-OVERWRITE-1 merge validation.
> Cross-reference: kaizen v1.84, outreach-strategy.md, qnfo-email Worker, qnfo-email-inbox-check
> cronjob (3851f539), session Nff8tKtjHf6VDCfRejuNd, subagent sessions (HO-6WyYLOHSGjb_jAH3UI,
> l7gByLaHxlxD1pXOaKxnG, YeG0ZGSBTT2BBD7mzmxGs, caixgX3FFJYjVsELh03Ip).


v2.11 UPDATE (2026-08-07, kaizen — MEMORY-TO-SKILL-DRIFT migration: email red-team audit anti-patterns + rowan.quni@ architecture):**
> Red-team: direct parent-agent 5-adversary audit (session MerOabc5KO_W9Q8BP47ok — SKILLS UPDATE
> directive triggered by email infrastructure audit findings). Watchtower: all 17 QNFO skills N-2
> CLEAN. MEMORY-TO-SKILL-DRIFT found: 3 anti-patterns in durable memory, 0 in email-composer v2.10.
> HARD: 0. SOFT: 2. DESIGN: 2. Changes:
> (1) [SOFT] **PROCESSED-STUCK-SPAM-1 anti-pattern added** — emails stuck in "processed" status
>     may be spam that leaked through filters; any red-team audit must check processed-status items
>     for spam keywords. Canonical case: session MerOabc5KO_W9Q8BP47ok — 7 email audit found 6/7
>     "processed" items were journal solicitations/spam; archived + filters added same-session.
>     Cross-ref: mem-rOoe9DeExL_g.
> (2) [SOFT] **PER-RECIPIENT-FILTER-GAP-1 anti-pattern added** — qnfo-email Worker filters are
>     GLOBAL (apply to ALL recipients); per-recipient routing (e.g., human-only at rowan.quni@)
>     requires Cloudflare Email Routing dashboard configuration. Do not assume Worker filters can
>     segregate by recipient. Cross-ref: mem-O25LuZJ_LBtQ, email-composer Anti-Patterns table.
> (3) [DESIGN] **HUMAN-ONLY-ROWAN-QUNI architecture note** — user mandate: rowan.quni@qnfo.org
>     is STRICTLY human-to-human. Newsletters, automated notifications, journal solicitations,
>     outbound copies, test emails, and briefing reports must NEVER reach this address. Architecture
>     fix requires CF Email Routing rules at the dashboard level. Until then, audit reports must
>     surface ONLY human-sent email at this address.
> (4) [DESIGN] **User preferences codified** — email digests must be CONCISE + ACTION-ORIENTED:
>     no spam, no already-dispatched, no internals. Only NEW actionable inbound. Cross-ref:
>     mem-Ccw6Aiu0TWC2, mem-O25LuZJ_LBtQ.
> Cross-reference: kaizen v1.85, mem-rOoe9DeExL_g, mem-O25LuZJ_LBtQ, mem-Ccw6Aiu0TWC2,
> session MerOabc5KO_W9Q8BP47ok.

> **v2.10 UPDATE (2026-08-06, kaizen — Red-team fixes: outreach templates + paper-audience matrix + deferred DESIGN items):**
> Red-team: direct parent-agent audit (session Nff8tKtjHf6VDCfRejuNd — CONTINUE: apply red-team findings).
> 3 concrete fixes applied, 2 deferred with documented blockers. HARD: 0. SOFT: 2. DESIGN: 1. Changes:
> (1) [SOFT] Funder template added (concrete fill-in, differentiated from academic: lead with record, cite infrastructure, call-to-action=15-min call). (2) [SOFT] Investor template added (differentiated from funder: lead with problem/market-failure, cite Manifesto+JPCUB, pre-empt risk, portfolio-rejection handling). (3) [DESIGN] Paper-to-audience mapping matrix added at §4 of outreach-strategy.md: 4 paper categories x 4 audiences + 5 quick decision rules, golden rule = never send paper to audience it wasn't written for. (4) [DEFERRED/DESIGN] Multi-channel integration (social-media-management v1.6.0 for Bluesky/LinkedIn) — deferred pending cross-skill wiring. (5) [DEFERRED/DESIGN] Gatekeeping auto-classification — Blind Inbox Architecture claims auto-archive but no Worker-side semantic classifier exists; documented as manual-via-agent pending automation.
> Cross-reference: kaizen v1.83, outreach-strategy.md, qnfo-email-inbox-check cronjob (3851f539), QNFO Research Daily Briefing cronjob (fdf1403c), session Nff8tKtjHf6VDCfRejuNd.


> **v2.9 UPDATE (2026-08-06, kaizen — Outreach & Communications Strategy + Blind Inbox Architecture):**
> Red-team: direct parent-agent 5-adversary audit (session Nff8tKtjHf6VDCfRejuNd — user directive:
> systematic outreach strategy for paper sharing, academic networking, funder/investor outreach).
> Trigger: user identified the blind inbox as an emotional shield enabling fearless outreach despite
> introversion, impostor syndrome, and fear of rejection ("self-taught, no PhD, independent researcher").
> Core insight: email routed through Worker→D1→LLM removes emotional friction — the agent drafts,
> user reviews, Worker sends; responses arrive as structured data, never as personal judgment.
> VERSION-OVERWRITE-1 merge past concurrent v2.8 (session SFkcXsRZjmvs4TMr9Fo_m, EMAIL-ROUTE-STRIP-1
> worker fix). HARD: 0. SOFT: 1. DESIGN: 2. Changes:
> (1) [DESIGN] **Outreach & Communications Strategy** — new `references/outreach-strategy.md` (~9,500 words):
>     audience segmentation (academic/funder/investor/collaborator), weekly outreach cadence (Mon scan /
>     Wed draft / Fri send), paper-sharing protocol with pre-flight checklist + D1 tracking schema,
>     response taxonomy (positive/critical/dismissive/read-later/collaboration), the "No Response Protocol"
>     (follow up ONCE at 14-21 days, never twice), the Emotional Operating Manual (7 principles),
>     integration with the research publication pipeline. Companion to qnfo-qwav-strategy.md and
>     email-patterns.md.
> (2) [DESIGN] **The Blind Inbox Architecture** — new foundational section: Worker + D1 + LLM stack as
>     emotional architecture removing psychological barriers to outreach. No email client, no notifications,
>     no inbox dread; criticism extracted as structured argument; gatekeeping auto-archived; silence is a
>     database entry, not rejection. The user engages with ideas, not emotional reactions.
> (3) [SOFT] Phase 3 (Strategic Context) updated to load outreach-strategy.md; quick-start outreach
>     commands added (scan contacts, draft batch, follow up, generate report).
> Cross-reference: kaizen v1.83, qnfo-qwav-strategy.md, email-patterns.md, qnfo-core §0.0,
> session Nff8tKtjHf6VDCfRejuNd.


> **v2.8 UPDATE (2026-08-06, kaizen — EMAIL-ROUTE-STRIP-1 RESOLVED: worker source fix applied, deployed, live-verified):**
> Red-team: direct parent-agent 5-adversary audit (CONTINUE/RESOLVE DEFERRED/CLOSEOUT, session SFkcXsRZjmvs4TMr9Fo_m).
> HARD: 0. SOFT: 0. DESIGN: 1. Changes:
> (1) [DESIGN] **EMAIL-ROUTE-STRIP-1 resolved at the source** — worker strip scoped to
>     `p === '/email' || p.startsWith('/email/')` in qnfo-email.js, deployed (wrangler 4.118.0,
>     version c95134cc-ef57-44f0-bf9b-3183a96b8060), live-verified 2026-08-06: plain `/emails/recent` and `/emails/body?id=N` now return
>     real data (previously the catch-all endpoint index); `/email/emails/*` prefixed form still works
>     for the qnfo.org/email/* custom-domain route. Anti-pattern row + Archive & Hygiene route note updated.
> Cross-reference: kaizen v1.83, qnfo-email worker (qwav-platform commit), EMAIL-ROUTE-STRIP-1 (v2.5),
> session SFkcXsRZjmvs4TMr9Fo_m.

> **v2.7 UPDATE (2026-08-06, kaizen — Archive & Email-Check Hygiene Protocol + filter API schema + HTTP-HEADER-NONE-1):**
> Red-team: direct parent-agent 5-adversary audit (SKILLS UPDATE cycle #4, session SFkcXsRZjmvs4TMr9Fo_m).
> Trigger: user mandate — "don't re-surface emails; what is the archiving procedure?" (archive-on-no-action,
> quiet reports). Canonical case: full-inbox hygiene run — 51 emails batched to archived (48) / spam (3),
> 4 auto-spam filters added (10 total), verification 0 non-archived/non-spam remaining.
> HARD: 1. SOFT: 2. DESIGN: 1. Changes:
> (1) [HARD] **HTTP-HEADER-NONE-1 anti-pattern added** — `urllib.request.Request(..., headers={"Content-Type": None})`
>     raises TypeError "expected string or bytes-like object, got 'NoneType'". Never put None in a headers dict;
>     build headers conditionally (only add Content-Type when a body is sent). Canonical case: this session's
>     hygiene script first run failed on the inventory GET with a None header value.
> (2) [SOFT] **Archive & Email-Check Hygiene Protocol section added** — PATCH /emails/status archive workflow,
>     full valid-status vocabulary, delta-based reporting rule (only NEW actionable inbound; never re-surface
>     archived/spam/sent; quiet report convention), POST /filters schema (field/pattern/action) + action
>     vocabulary (accept/reject/spam) + matching semantics, with the 4 spam filters added this cycle as examples.
> (3) [SOFT] **EMAil-CHECK-RESURFACING-1 anti-pattern added** — re-reporting emails the user already declared
>     no-action on. Archive-on-no-action + delta-only reporting prevents it.
> (4) [DESIGN] **Monitoring checkpoint +1: EMAIL-ROUTE-STRIP-1 PASS** — this cycle used the /email/emails/*
>     prefixed form for all 51 PATCHes + 4 filter POSTs + verification GETs with zero route-strip failures.
> Cross-reference: kaizen v1.82, qnfo-email worker, N-2-FRONTMATTER-DRIFT-1, EMAIL-ROUTE-STRIP-1 (v2.5),
> mem-YoM6-BSfCW_K (user hygiene mandate).

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


version: 2.12
triggers: ["check email", "read email", "send email", "reply to", "compose email", "draft email", "my inbox", "manage filters", "block sender", "auto-reply", "email history", "search email", "qnfo email", "inter-personal communication"]


related: ["qnfo-core", "cloudflare", "knowledge"]


priority: 2


platform: cloudflare


autonomous: true


self_sufficient: true


---





# Email Composer — v2.12
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





## The Blind Inbox Architecture

The qnfo-email Worker + D1 + LLM stack is not just a technical email handler — it is **emotional architecture**. It removes the psychological barriers that prevent independent researchers from doing systematic outreach.

### Why This Matters

Every email you send through the blind inbox follows a path where:
- **You never open an email client.** All inbound routes to the Worker → D1 → accessed through prompts. No notifications. No inbox dread.
- **The LLM reads responses first.** Criticism arrives as structured data (sender, subject, body_text). The agent extracts the argument, not the tone. You engage with the physics, not the attitude.
- **Gatekeeping is auto-archived.** "You're not a real physicist" and credential-attacks are classified as dismissive and routed to archive. You never have to feel them.
- **Silence is a database entry, not rejection.** A non-response isn't personal — professors get 100+ emails/day. The system tracks it, follows up once (if appropriate), and moves on.
- **Volume dissolves fear.** The first outreach email is terrifying. The 50th is routine. The blind inbox makes volume possible.

### The Operational Model

```
You (paper/idea) → Agent drafts outreach → You review (optional) → Worker sends → D1 logs
                                                                       ↓
You (response)   ← Agent frames reply      ← Worker receives ← Recipient replies
```

At no point do you face the recipient's emotional reaction directly. This is not avoidance — it is **emotional architecture**: building a system that lets you do the research and outreach while protecting the person doing it.

### What This Enables

- **Systematic paper sharing** — 12-20 academic outreach emails/month without emotional burnout
- **Fearless engagement with criticism** — every critical response is a free peer review
- **Investor/funder outreach** — the publication record speaks for itself; no CV required
- **Network building at scale** — at 15% response rate, ~36 substantive conversations per year

For the full outreach strategy, cadence, audience segmentation, and response protocols, see `references/outreach-strategy.md`.

---

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





## Canonical Address Registry (2026-08-06 red-team — user directive: 3-5 addresses MAX)

**User directive (2026-08-06):** "DON'T GO CRAZY WITH ALL THESE EMAIL ADDRESSES. WE NEED 3-5 MAX. QNFO@QWAV.ORG IS ENTIRELY SUPERFLUOUS AND UNNECESSARY."

**The live routing set — do NOT provision beyond this without explicit user approval:**

| Domain | Custom rules | Catch-all | Status |
|:-------|:-------------|:----------|:-------|
| **qnfo.org** | `qnfo@`, `rowan.quni@`, `research@`, `alerts@`, `publications@` → worker:qnfo-email | forward → qnfo@qnfo.org | CANONICAL (5 — at the user's 3-5 upper bound) |
| **qwav.tech** | `info@`, `rowan.quni@` → worker:qnfo-email | forward → qnfo@qnfo.org | PRE-EXISTING 2025, functional |
| **q08.org** | `noreply@` → worker:qnfo-email | forward → qnfo@qnfo.org | PRE-EXISTING, platform/bounce use |
| qwav.org, qwav.net, qwav.uk, q-wave.tech, qwave.tech, qnfo.net, qnfo.uk, empoweringchange.today | — (zero) | **drop** | EMAIL-INERT (reverted 2026-08-06) |

**Rules:**
1. Only the 5 qnfo.org addresses are canonical identities. qwav.tech/q08.org are legacy-functional and kept ONLY while they carry real traffic (info@qwav.tech + rowan.quni@qwav.tech since 2025; noreply@q08.org platform use).
2. NEVER create a routing rule on an inert domain. NEVER create an address the user did not ask for.
3. Any new address proposal goes to the user FIRST — never self-authorize.

### EMAIL-ADDRESS-PROLIFERATION-1 (HARD, 2026-08-06)
Creating email routing rules / addresses beyond the canonical set without explicit user direction. Canonical case: 2026-08-06 — agent provisioned 5 literal rules × 11 domains (~55 addresses: qnfo@qwav.org, research@q-wave.tech, alerts@qnfo.uk, ...) when the user wanted 3-5 max. User directive cut it back: 8 domains reverted to catch-all drop (40 rules deleted), only the canonical set remains. Fix: before creating ANY routing rule, ask — "is this address in the canonical set, or explicitly requested?" If no, do not create it. Cross-ref: kaizen v1.81, N-2-SCAN-FALSE-POSITIVE-1 (verify before claim).

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
- If systematic outreach or paper-sharing: read `references/outreach-strategy.md` for audience segmentation, cadence, and response protocols.
- For the Blind Inbox emotional architecture: see §The Blind Inbox Architecture above.


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





## Systematic Outreach (see references/outreach-strategy.md)

### Quick-Start Outreach Commands

| User Trigger | Agent Action |
|---|---|
| "Outreach batch for [paper]" | Find 5-10 relevant researchers, draft personalized emails from the academic template, present for review |
| "Follow up on pending outreach" | Check D1 for emails >14 days without response, draft ONE follow-up each, present for review |
| "Outreach report" | Generate stats: sent, responded, response rate by audience type, active conversations |
| "Weekly outreach routine" | Execute the Mon/Wed/Fri cadence: scan contacts → draft batch → review responses |

### Paper-Sharing Pre-Flight

Before ANY outreach email: verify the paper is DOI-archived, identify ≥3 specific researchers whose work connects to the paper, research each recipient's recent work for a personalized connection point, use the academic researcher template from `references/outreach-strategy.md`.

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





## Archive & Email-Check Hygiene Protocol (v2.7)

**User mandate (2026-08-06, mem-YoM6-BSfCW_K): the user does not want repeated email re-surfacing.**

### Archiving handled email (the "don't make me see it again" procedure)
- **Archive:** `PATCH /email/emails/status` with `{"id": N, "status": "archived"}` — removes the email from
  all future checks. Do this the moment the user declares an email handled / no-action / don't-care.
- **Junk -> spam:** same call with `"status": "spam"` for phishing, spam, and predatory solicitations.
- **Valid statuses (worker source `validStatuses`):** `received`, `processed`, `sent`, `replied`,
  `archived`, `spam`, `read`, `rejected`.
- **Bulk hygiene:** fetch `GET /email/emails/recent?limit=100`, PATCH each id in one loop, then re-fetch and
  assert ZERO emails remain outside `archived`/`spam` (verification gate).
- **Route quirk:** the `/email/emails/*` prefixed path and plain `/emails/*` both work on the workers.dev host since the EMAIL-ROUTE-STRIP-1 worker fix (deployed 2026-08-06, version c95134cc-ef57-44f0-bf9b-3183a96b8060); the prefixed form remains safe for the qnfo.org/email/* custom-domain route.

### Reporting rule (what [EMAIL-CHECK] must do)
1. Report ONLY new actionable inbound: `received`/`processed`, non-archived, non-spam, since last check.
2. Never re-surface archived / spam / sent / replied emails.
3. If nothing new: report one line — "no new actionable mail."
4. After the user says "don't care" about any item: PATCH it to archived (or spam) immediately.

### Filter API (auto-handling recurring senders)
- **Create:** `POST /filters` with `{"field": "from"|"to"|"subject"|"body", "pattern": "<substring>",
  "action": "accept"|"reject"|"spam", "priority": N, "enabled": true}` — case-insensitive substring match
  on the field; first match wins (priority DESC).
- **List/delete:** `GET /filters`, `DELETE /filters/:id`.
- **Proven spam filters (2026-08-06):** from `cfbounces+ndrdrop` -> spam; from `paperworkspot` -> spam;
  subject `manuscript for publication` -> spam; subject `email blasting` -> spam.
- **Warning:** do NOT filter on `bounces@cf-bounce.qnfo.org` — it is the Cloudflare inbound relay for ALL
  qnfo.org mail (legit inbound included).


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





| **HTTP-HEADER-NONE-1: Passing None as a value in a urllib header dict — TypeError "expected string or bytes-like object, got 'NoneType'" (2026-08-06)** | Build request headers conditionally: only add `Content-Type` (or any header) when the value is a real string. `urllib.request.Request(..., headers={...})` does NOT tolerate None values — it crashes on join. Canonical case: session SFkcXsRZjmvs4TMr9Fo_m hygiene script — first run failed on the inventory GET because `Content-Type` was set to `None` when there was no body. Fix pattern: `hdr = {...}; if body is not None: hdr["Content-Type"]="application/json"`. Cross-ref: BLAME-EXTERNAL-1 (bug is always your code). |
| **EMAIL-CHECK-RESURFACING-1: Re-reporting emails the user already declared no-action on (2026-08-06)** | Archive-on-no-action + delta-based reporting: once the user says "don't care" about an email (or a whole class), PATCH it to `archived` (or `spam`) in the same session and exclude archived/spam/sent from all future [EMAIL-CHECK] reports. Quiet report = one line. Canonical case: session SFkcXsRZjmvs4TMr9Fo_m — user: "SO THEREFORE I DON'T CARE ABOUT ANY OF THESE... DON'T WASTE MY TIME"; 48 archived + 3 spammed same session. Cross-ref: mem-YoM6-BSfCW_K. |
| **EMAIL-ROUTE-STRIP-1: qnfo-email Worker route-strip mangles `/emails/*` on the workers.dev host — plain `/emails/*` returns the catch-all endpoint index (HTTP 200, silent wrong payload) (2026-08-06)** | On the workers.dev host use the `/email`-prefixed form (`/email/emails/recent`, `/email/emails/body?id=N`) — the strip normalizes it to `/emails/*`. Fix in worker source: scope strip to `p === '/email' || p.startsWith('/email/')`. Canonical case: session SFkcXsRZjmvs4TMr9Fo_m — ~15 probes burned. Cross-ref: API-DOC-GAP-1. **[RESOLVED 2026-08-06** — worker source scoped strip deployed (version c95134cc-ef57-44f0-bf9b-3183a96b8060); plain `/emails/*` live-verified returning real data; prefixed form still supported].** |
## References





- `references/qnfo-qwav-strategy.md` — QWAV commercial thesis, Qubit Delusion series, Manifesto, Problem-Substrate Mapping, JPCUB positioning


- `references/email-patterns.md` — Communication patterns: declining opportunities, pitching QWAV, follow-ups, relationship maintenance





**Worker source:** `C:\Users\LENOVO\.deepchat\workers\qnfo-email\qnfo-email.js` (v1.6)


**Worker deploy:** `wrangler deploy` from `C:\Users\LENOVO\.deepchat\workers\qnfo-email\`





---





## Version





**API-FAILURE PROTOCOL (HARD):** When any API call returns 403/401/404, run the API-Failure Self-Diagnosis Protocol (windows-command-patterns S-1.0.6): STOP -> VERIFY your HTTP method/headers -> COMPARE with curl -> THEN consider infrastructure. The bug is ALWAYS your code until proven otherwise (kaizen BLAME-EXTERNAL-1).





Current: **v2.12** (email-composer — WORKER-SOURCE-EVICTED-1 + CF API key fallback; 2026-08-05)

