# email-composer

> **v2.25 UPDATE (2026-08-20, kaizen — daily-briefing red-team + user dispositions):**
> Red-team: adversarial audit of the 2026-08-20 Daily Briefing run + the user's same-day dispositions ("EXECUTE RED TEAM AND UPDATE SKILLS..."; "I DO NOT WANT TO BOTHER PEOPLE BY EMAIL..."; "THESE ARE ALL YOUR TASKS TO RESOLVE. DO NOT CONTINUE TO BOTHER ME ABOUT TASKS THAT YOU INITIATED AND YOU NEED TO OWN."). VERDICT: HARD 3 / SOFT 5 / DESIGN 1. Root cause shared by all three HARDs: the briefing ran ad-hoc scan/filter logic instead of consuming the email agent's already-resolved state.
> (1) [HARD] **SRS-ENVELOPE-SENDER-1** — Cloudflare Email Sending SRS-rewrites inbound envelopes: external replies arrive as `SRS0=<hash>=<orig-domain>=<user>@qnfo.org` (verified: IOCPh grant id=224, 2026-08-19) or `bounces+<...>@...<token>.openreview.net` (OpenReview notices ids 219/220/225). A filter `sender NOT LIKE '%qnfo.org%'` silently drops REAL external replies. Classify external via the header From when available; else strip SRS/bounce envelope prefixes. ALWAYS run an id-anchored completeness dump (all rows id > last anchor, no sender filter) alongside any filtered query.
> (2) [HARD] **AGENT-OWNED-LEAK-1** — never surface items the email agent can resolve autonomously (declines → archive + close line; blocked forms → one surfacing max then close; disposition flags → resolve with standing policy). User: "THESE ARE ALL YOUR TASKS TO RESOLVE." Decision-surface filter order: good-vibes → ownership → decision-required.
> (3) [HARD] **NO-FOLLOW-UP-DEFAULT-1** — user policy: no follow-up emails to silent recipients, ever ("I DO NOT WANT TO BOTHER PEOPLE BY EMAIL, LET ALONE ACADEMICS IF THEY DONT WANT TO ACKNOWLEDGE MY INITIAL EMAIL THAT'S ON THEM"). ALL silent-recipient follow-up waves CANCELLED permanently (08-06 batch included); No Response Protocol 14-21d windows superseded for silence. In-thread replies to responders remain normal.
> (4) [SOFT] **D1-QUERY-TIMEOUT-1** (d1_database_query MCP tool timed out 3/4 on 2026-08-20; canonical query path = `execute` + cloudflare.request POST /accounts/{acct}/d1/database/{db}/query), **COMPLETENESS-ANCHOR-1** (id-anchored dump every cycle), **GOOD-VIBES-VIOLATION-1** (declines are negative by definition — the email agent archives them; the briefing never surfaces them), **PREEMPT-1** (if a scheduled one-shot fires AFTER the hard window it gates, run_now pre-empt AND verify the run completed — both manual runs 341dc2bf/a82ffe68 failed 2026-08-20 with 'Cron job runner stopped before completion'; re-trigger on failure), **PATH-CANONICALIZATION-1** (outreach-log canonical = `.deepchat/skills/email-composer/references/outreach-log.md`; `QNFO/qnfo-research/artifacts/` does not exist locally).
> (5) [DESIGN] **HEADER-DRIFT-1** — line-401 version header was stale (v2.21) while banner/footer were v2.24; repaired to v2.25.
> Cross-reference: outreach-log.md 2026-08-20 red-team addendum, outreach-strategy.md NO-FOLLOW-UP-DEFAULT-1, .kaizen_history v2.25, daily-briefing cronjob a82062c7 v2.25 rules, user dispositions 2026-08-20, session this.
> **v2.24 UPDATE (2026-08-18, kaizen — user mandate: REGISTER-MIRRORING-1 (mirror the recipient's language) + RECIPIENT-STYLE-USE-1 (all information is useful)):**
> User answered the v2.23 open-policy questions (session tfRpmza-s0y5lUQXnWczm): "ANSWERS TO OPTIONAL QUESTIONS: YES, MIRROR RECIPIENT'S LANGUAGE. ALL INFORMATION IS USEFUL SO WHEN WE KNOW SOMETHING ABOUT A RECIPIENT'S PREFERRED COMMUNICATION STYLE (OR NOT) USE THAT INFORMATION." Changes:
> (1) [HARD] **REGISTER-MIRRORING-1 rule added** — replies MUST mirror the recipient's register: informal inbound ("hi rowan, regards moty") → informal reply ("Hi Moty … Best, Rowan"); formal inbound → formal ("Dear Professor …"). Applies to in-thread replies and follow-ups; cold outreach keeps the §1.A formality baseline until the recipient's style is known.
> (2) [HARD] **RECIPIENT-STYLE-USE-1 rule added** — "all information is useful": use ANY known information about a recipient's preferred communication style (inbound language, greeting/salutation habits, channel) in drafting; absence of style information is itself information (default to the §1.A baseline).
> (3) [SOFT] v2.23 watch item (4) (register-matching = user question) RESOLVED by this mandate. v2.23 watch item (2) ("Re:" prefix on cold outreach) remains OPEN — no user answer; template-consistent (strategy §1.A) until decided.
> Cross-reference: user mandate 2026-08-18, outreach-strategy.md §1.A (register-mirroring note added), v2.23 banner, memory user_preference (RECIPIENT-REGISTER-MIRRORING-1), session tfRpmza-s0y5lUQXnWczm.

> **v2.23 UPDATE (2026-08-18, kaizen — wave-2 red-team audit (3-parallel reviewers) + DEFAULT-SENDER-DRIFT-1 + Turing-test assessment):**
> Red-team: POST-PUBLICATION ADVERSARIAL ANALYSIS GATE on the 2026-08-18 wave-2 sends (Heiblum reply id=215, Landsman reply id=216, Camino outreach id=217, Jipdi outreach id=218) — 3 parallel reviewer subagents (Accuracy / Completeness / Dependency-Tone). VERDICT: **0 HARD** across all three; each PASS-WITH-SOFT-FINDINGS; Turing scores 7-8/10; no bothersome patterns; no recipient mismatch; no dangling obligations. Changes:
> (1) [HARD] **DEFAULT-SENDER-DRIFT-1 anti-pattern added** — Worker `/send` WITHOUT explicit `from` defaults From to `qnfo@qnfo.org` (verified: D1 ids 214-218 all show qnfo@qnfo.org while wave-1 ids 202-204 show rowan.quni@qnfo.org because that session passed `from` explicitly). Canonical academic-outreach sender is `rowan.quni@qnfo.org` (strategy §1.A). Rule: EVERY `/send` payload passes `"from": "rowan.quni@qnfo.org"`. Wave-2 deviation absorbed as errata, NO resend (no-repeat-contact mandate).
> (2) [SOFT] **LLM-tell list for future drafts** (Dependency-Tone reviewer): avoid recurring "One question …" openers across a batch; avoid recurring "I would be glad to hear/expand …" closers with hedge-stacks; a reply to a short inbound must NOT run ~8× its length (E1: 230 words vs 27); a "plain terms" promise must deliver — E1 promised plain terms then used "core scalar of the theory"/"by-products of the algebra" (Completeness F1); avoid "we" from a solo signatory (E3); onboard jargon in cold outreach ("re-entrant mark" dropped un-onboarded in E4).
> (3) [SOFT] Accuracy: Camino paraphrase adds "only when" over the abstract's "when" (necessity reading — defensible). E4 identity R=(e^{iπ})^{2s}=(−1)^{2s} VERIFIED verbatim in the full Exchange Phase abstract (reviewer truncation artifact, not an error). DOIs parent-verified: JPCUB P0 = 10.5281/zenodo.21637028 (DB record); Exchange Phase = 10.5281/zenodo.21964104 (DB-canonical per v2.21 pre-flight rule).
> (4) [DESIGN] **"Re:" prefix on cold outreach** (template §1.A prescribes it) mimics reply threads and is a spam-folder watch item — kept for template consistency (40+ prior sends, no junk reports); changing the policy = user decision.
> (5) [DESIGN] Watch item: Exchange Phase v1.3 frontmatter carries version-level DOI 21964359 while DB-canonical record DOI = 21964104 — resolve version identity at the next paper-sharing pre-flight.
> (6) [SOFT] Completeness confirmed: Heiblum + Landsman follow-up eligibility permanently CLOSED (never re-contact; the ONLY permitted future contact = in-thread plain-terms simplification if Heiblum reports continued difficulty). Landsman's "entropic enclosure" question stays unanswered BY DESIGN (Type 4, no follow-up ever).
> Cross-reference: red-team delegations w2TKAyAeY6aKSWNTrL1Ua (Completeness) / fFeVsWoBkYRGEGWCtdru8 (Dependency-Tone) / nejE4O3EBlVY36QnXa6YS (Accuracy), outreach-log.md 2026-08-18 wave-2 red-team addendum, system-prompt v3.43, kaizen v2.68, session tfRpmza-s0y5lUQXnWczm.

> **v2.22 UPDATE (2026-08-18, kaizen — CMD SKILLS UPDATE: red-team remediation — footer N-2 drift repaired (footer stayed v2.20 while banner/FM advanced to v2.21); mirrors system-prompt v3.43 + kaizen v2.68):**
> Red-team: CMD RED TEAM cycle 2026-08-18 (session f_bH6KMZ4Og2Wvw79S9rU). HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **Footer N-2 drift repaired** — footer `Current: **v2.20**` bumped to v2.22 == banner == frontmatter.
> Cross-reference: system-prompt v3.43, kaizen v2.68, session f_bH6KMZ4Og2Wvw79S9rU.

> **v2.21 UPDATE (2026-08-17, kaizen — CMD SKILLS UPDATE cycle: red-team skills audit + session-lesson anti-patterns + mandate codification):**
> Red-team: direct parent-agent 5-adversary audit of the 2026-08-17 outreach cycle (0 HARD) + this cycle's mandatory checks (7-store prompt parity v3.38 VERIFIED sha d666fc26; 9/9 CMD templates restored in all 4 template stores — CMD RED TEAM SUB + CMD DEPLOY were missing; DEEPCHAT-DEFAULT-MODEL-1 PASS; Cloudflare cost section v3.53 PASS). Changes:
> (1) [SOFT] **RECEIPT-PLACEHOLDER-TOKEN-1 recurrence (2026-08-17)** — outreach-log.md QPL UPDATE carried an unresolved timestamp token "(17:xx UTC)"; resolved to verified `received_at 2026-08-17T14:00:12Z`. Log entries must carry resolved timestamps at write time.
> (2) [SOFT] **THREAD-RESOLUTION-SUPERSEDED-1 (new)** — when a reply resolves a pending thread, mark the old follow-up-eligibility line "(SUPERSEDED by the UPDATE below — ...)" so future readers cannot misread it. Canonical: QPL section, outreach-log.md 2026-08-17.
> (3) [SOFT] **PHANTOM-EXEC-SESSION-1 (new)** — exec tool reports "Session ... not running" while the command actually completed; verify via `process list` BEFORE retrying (observed 10+ times 2026-08-17; blind retries caused duplicate git commits/sweeps).
> (4) [SOFT] **NAMING-MANDATE-1 + EMAIL-SIGNATURE-PLAIN-1 codified in Phase 4** (system-prompt v3.35+): signature = full name "Rowan Brad Quni-Gudzinas" + at most one plain org word ("QNFO"); no titles/role prefixes/taglines/pipes/URLs. NOTE: QPL replies ids 193/194 (2026-08-17) predate codification and used the deprecated "Rowan Quni / QNFO Research Collective" signature — absorbed as errata, NO resend (no-repeat-contact).
> (5) [SOFT] Description trimmed 207 -> 162 chars (must be <=176); frontmatter/H1/banner aligned 2.20 -> 2.21 (concurrent d7e92b1 cycle edited strategy files without a SKILL version bump — N-2 drift fixed here).
> (6) [SOFT] Paper-Sharing Pre-Flight: cite the QNFO DB-canonical DOI for the paper's CURRENT version (Exchange Phase = 10.5281/zenodo.21964104, not the v1.1 21963930 of the 08-16 batch) — DESIGN-1 of the 08-17 audit.
> Cross-reference: kaizen v2.64, system-prompt v3.38, 5-adversary red-team audit 2026-08-17, PHANTOM-EXEC-SESSION-1 (mem-CmU4mIm_MwJV), outreach-log.md 2026-08-17.

> **v2.20 UPDATE (2026-08-15, kaizen — PROACTIVE OUTREACH REINSTATED + red-team remediation of the 2026-08-15 round):**
> Red-team: 4-parallel-reviewer audit (Accuracy / Completeness / Dependency / Compliance) + direct parent-agent
> fallback of the 2026-08-15 proactive outreach round (3 sends: Santamato / Naser-Moghadasi / Plaat).
> VERDICT: 0 HARD, 4 SOFT, 7+ PASS — all 4 SOFT remediated in this cycle.
> (1) [HARD] **User mandate 2026-08-15 REVERSES the v2.18 detection-only mandate**: "MAKE SURE YOU INITIATE CONTACT
>     WITH HIGH-VALUE, HIGHLY RELEVANT RESEARCHERS... ONLY 1 EMAIL PER RESEARCHER/NAME/EMAIL... KEEP A MASTER
>     LIST... GOOD VIBES ONLY!" Frontmatter `autonomous` set back to `true`. The v2.18 "CURRENT STATE:
>     DETECTION-ONLY" banner is SUPERSEDED (annotated inline below).
> (2) [SOFT] **SOFT-1 MESSAGE-ID-NE-DELIVERY-1 remediated**: 200+message_id = ACCEPTED (not delivery); D1
>     status=sent = canonical verification; read-only CF Email Sending REST checks 2026-08-15 (limits 5/1000 sent,
>     suppression list empty); delivery-monitoring SOP note added to outreach-log.md; weekly deliverability check
>     per cloudflare-email-service deliverability.md.
> (3) [SOFT] **SOFT-2 banner drift fixed**: version bumped 2.18 -> 2.20; this banner documents the reversal.
> (4) [SOFT] **SOFT-3 recipient attribution resolved**: D1 DOES store recipient attribution — /emails/body?id= and
>     the raw D1 table expose the `recipient` column for ids 153-156 (verified 2026-08-15). `to:null` in
>     /emails/recent is a list-projection quirk only; canonical attribution = D1 `recipient` column (echo file
>     qnfo-send-results.json remains a secondary trail).
> (5) [SOFT] **SOFT-4 master-list artifact removed**: `attacker-probe@example.invalid` (D1 security-probe row,
>     never an outreach recipient) excluded from dedup master list + contact-ledger.md; count corrected 35 -> 34
>     (31 prior + 3 new); probe-handling convention documented in contact-ledger.md.
> Cross-reference: outreach-log.md 2026-08-15 (batch + delivery note), contact-ledger.md, user mandate 2026-08-15,
> red-team audit this session, qnfo-email Worker v1.8.



> **v2.17 UPDATE (2026-08-10, kaizen — CMD RED TEAM FIX CYCLE: Repair-Send Protocol + scripted send-guard (PROSE-GATE-ADVISORY-1 enforcement)):**
> **v2.19 UPDATE (2026-08-14, kaizen — CMD SKILLS UPDATE: SEND-403-BIC-UA-1 + SEND-KEY-BINDINGS-1 + /send verification):**
> Red-team: direct parent-agent audit (session FJ4ZYy6OEfAnpu8mq30OZ; RES.007 P7 OUTREACH execution).
> HARD: 2. SOFT: 1. DESIGN: 0.
> (1) [HARD] **SEND-403-BIC-UA-1 anti-pattern added** — `/send` (and `/health`) returning HTTP 403 with Cloudflare
>     error 1010 from Python means the caller omitted a browser-like User-Agent: default urllib UA triggers
>     Cloudflare Browser Integrity Check. Same class as VECTORIZE-403-MISDIAGNOSIS (research v2.110). Fix: always
>     send `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0
>     Safari/537.36` on qnfo-email calls. Canonical: RES.007 outreach 2026-08-14 — first /send attempt 403 (no UA),
>     retry with UA -> 200.
> (2) [HARD] **SEND-KEY-BINDINGS-1 anti-pattern added** — the qnfo-email API key MUST be read in FULL from the worker
>     `/bindings` endpoint (`GET /accounts/{acct}/workers/scripts/qnfo-email/bindings` -> `API_KEY.text`); the
>     `/settings` endpoint returns the same text but truncating prints to 30 chars (common debug habit) produces a
>     PARTIAL key -> HTTP 401 unauthorized. The full key ends with `-zJ09X7EePDto`. Auth accepts
>     `Authorization: Bearer <key>` OR `x-api-key: <key>` (worker L67-70). Canonical: RES.007 2026-08-14 — 401 until
>     full key used; both header forms then verified on /health.
> (3) [SOFT] **/send response semantics documented in-practice** — 200 + `message_id` = ACCEPTED by the worker
>     (crypto.randomUUID), NOT delivery proof (MESSAGE-ID-NE-DELIVERY-1). Verify via `GET /emails/recent` ->
>     status=sent + outreach-log.md entry with message_id (Tool-Call Execution Mandate).
> Cross-reference: research v2.110 (VECTORIZE-403-MISDIAGNOSIS), kaizen v2.44, session FJ4ZYy6OEfAnpu8mq30OZ.

> **v2.18 UPDATE (2026-08-14, red-team remediation — DETECTION-ONLY MANDATE documented + Patel C3 monitor corrected + tracking-gap ledger):**
> Red-team: 3 parallel reviewer audit (2026-08-14 email check) — 0 HARD behavioral violations, 1 scoped HARD record-keeping finding, 5 SOFT doc/tracking gaps. Changes:
> (1) [HARD] **CURRENT STATE: DETECTION-ONLY since 2026-08-13 — ⚠️ SUPERSEDED 2026-08-15 by user mandate (see v2.20 banner): proactive autonomous outreach reinstated; frontmatter `autonomous: true`** — user mandate supersedes the v2.12/v2.13 autonomous-sending history (banners preserved as history): NEVER send outreach emails autonomously, ever; no send action without explicit user approval in an email-composer session. Frontmatter `autonomous` set to `false`. Cronjob 3851f539 verified detection-only (renamed 2026-08-13, description + taskPrompt both detection-only).
> (2) [HARD] **Patel C3 monitor CORRECTED** — the v2.17 banner's "must remain at exactly 2 (id=66 + id=69)" omitted id=61; the TRUE lifetime contact count is THREE (id=61 genuine + id=66 error + id=69 repair). Any further contact = 4th contact = HARD violation (no-repeat-contact mandate). The v2.17 text stands as history; this line is the operational correction.
> (3) [SOFT] **Tracking-gap ledger** — see outreach-log.md 2026-08-14 RED-TEAM REMEDIATION: unlogged test-to-OWN-mailbox rows 74/114/132 (all rwnquni@outlook.com, TEST-SEND-EXTERNAL-1 compliant), D1 ids 107-110 deleted (404, no API record), complete follow-up eligibility dates per batch (08-06 → 08-20; 08-10 Emeriau/Bruhat-Tits → 08-24; 08-12 CMB/standards/singles → 08-26; 08-14 Marcolli → 08-28 pending user disposition).
> (4) [SOFT] **Count claims must match verified state** — EV record "19/19 fields" corrected to 18/19 (required phone blocked). Same class as RECEIPT-PLACEHOLDER-TOKEN-1: report what is verifiable.
> Cross-reference: outreach-log.md (2026-08-14 entries), user mandate 2026-08-13, system prompt (email + outreach monitoring agent), session this.

> **v2.17 UPDATE (2026-08-10, kaizen — ROUTING-DROP-BREAKS-SENDING-1 ROOT CAUSE + EMAIL-SUBJECT-SPAM-TOKENS-1 + DELIVERABILITY-POSTURE):**
> Red-team: deep-dive RCA of the 10002 incident (user directive — "external errors are uncommon; the error is entirely your fault"). Trigger: 2026-08-08 closeout proved the 10002 root cause was the agent's own routing DROP rules, not a Cloudflare platform issue. HARD: 2. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **EMAIL-SENDING-DOMAIN-10002 root cause CORRECTED** — the v2.15 row blamed "platform-side" and recommended "file CF ticket" + Sender-Domain Fallback. The TRUE root cause (proven 2026-08-08 closeout): a prior hygiene session added 4 routing-level DROP rules on the qnfo.org zone (spam blocks: glintopenaccess.org, paperworkspot@gmail.com, dr.shrivishnu.msip@gmail.com, lena.mories@glintopenaccess.org). Routing DROP rules on a zone with Email Sending enabled SILENTLY KILL the ENTIRE outbound pipeline — every send from ANY qnfo.org address returns 10002 internal_server. Differential proof: 10/11 sending domains returned HTTP 200; only qnfo.org — the ONLY zone with DROP rules — failed. Deleting the 4 DROP rules restored sending immediately (verified REST 200 + D1 rows 75-77 status=sent). NEVER file a CF ticket for 10002 before checking the zone's routing rules; NEVER use routing DROP rules for spam on a zone with Email Sending — use Worker filters (POST /email/filters).
> (2) [HARD] **EMAIL-SUBJECT-SPAM-TOKENS-1 anti-pattern added** — test emails with spam-triggering subjects ("TEST", "SEND TEST", "WRANGLER TEST", "MATRIX", "Pipeline test", "POST-REG VERIFY", "1010 PERMANENTLY FIXED", "verification code") land in Outlook/Gmail Junk by CONTENT scoring even when SPF/DKIM/DMARC all pass. Canonical case 2026-08-10: ~half the agent's test emails junked by Outlook while every one passed auth (verified via PR_TRANSPORT_MESSAGE_HEADERS). Real outreach subjects ("Re: PaQit - a system-level energy metric...") land in Inbox. When testing, use neutral, human-like subjects and send to OWN mailboxes only; one canonical test, not bursts.
> (3) [SOFT] **DELIVERABILITY POSTURE documented** — all QNFO sending domains carry SPF (include:_spf.mx.cloudflare.net ~all), DKIM (cf-bounce selector), DMARC p=reject; sp=reject; rua=mailto:dmarc@<domain>; (hardened 2026-08-10). If sends start landing in Junk, check (a) your own subject lines, (b) burst patterns, (c) routing/filter rules — in that order — before blaming the recipient provider.
> Cross-reference: windows-command-patterns v3.19, deepchat-settings v1.6, system prompt v3.0 (CHANGE-AUDIT-FIRST-1), session this.
> Red-team: direct parent-agent 5-adversary audit (CMD RED TEAM, READ-ONLY — this session). Trigger: the Patel incident (id=66 test email to a real recipient) revealed that TEST-SEND-EXTERNAL-1 (v2.16) was a PROSE-ONLY gate and there was no repair playbook. HARD: 2. SOFT: 1. DESIGN: 1. Changes:
> (1) [HARD] **Repair-Send Protocol section added (C1)** — codifies the incident-response playbook that was improvised on 2026-08-10: classify severity (wrong recipient / wrong content / redundant), clarify-vs-resend decision rule (if genuine content already delivered FIRST, send a short clarification threaded by subject — NEVER a full re-send), test-send to the USER's OWN mailbox first, verify in D1 (status=sent), log to outreach-log.md, and HARD-STOP further contact (no follow-up, no 4th email). The "threading-by-subject" repair pattern (N2) is codified here.
> (2) [HARD] **Scripted send-guard (N1 / PROSE-GATE-ADVISORY-1 enforcement)** — TEST-SEND-EXTERNAL-1 is now machine-enforced by `scripts/email-send-guard.py`: any `--mode test` send whose recipient is NOT the user's own mailbox or an internal QNFO/QWAV domain exits 1 with the TEST-SEND-EXTERNAL-1 violation message. Prose gate → scripted gate.
> (3) [SOFT] **TEST-SEND-EXTERNAL-1 row extended** — cross-ref to the scripted guard + Repair-Send Protocol added.
> (4) [DESIGN] **Monitoring checkpoint registered (C3)** — Patel contact count (tp53@rice.edu) must remain at exactly 2 (id=66 error + id=69 clarification); any 3rd contact is a TEST-SEND-EXTERNAL-1 / no-repeat-contact regression.
> Cross-reference: kaizen v1.99 (mirror + calibration fix), research v2.92 (briefing cross-ref), PROSE-GATE-ADVISORY-1, session this.

> **v2.16 UPDATE (2026-08-10, kaizen — TEST-SEND-EXTERNAL-1 HARD GATE: never send test/diagnostic emails to real external recipients):**
> Red-team: direct parent-agent audit (user directive — "SENDING A TEST EMAIL TO A REAL EMAIL ADDRESS IS A HUGE NO-NO!"). Trigger: the EMAIL-SENDING-DOMAIN-10002 isolation matrix sent a "matrix test" payload to tp53@rice.edu (Tirthak Patel, D1 id=66) — a SECOND contact to a researcher who had already received genuine outreach the same day (id=61). HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **TEST-SEND-EXTERNAL-1 anti-pattern added** — test and diagnostic sends go ONLY to user-owned mailboxes (rwnquni@outlook.com) or internal QNFO/QWAV addresses (alerts@qnfo.org, qnfo@qwav.org, rowan.quni@qnfo.org). NEVER to a real external address — even with an explicit "test"/"matrix" subject, it is still a contact: it can burn the recipient, look unprofessional, and violates the no-repeat-contact mandate (a researcher who already received genuine outreach MUST NEVER get a second email, test or otherwise, without user permission). When a diagnostic needs an "external recipient works" control, use the user's own external mailbox. Canonical case: 2026-08-10 MATRIX E. Cross-ref: CONNECTION-POINT-UNVERIFIED-1, OUTREACH-SENT-AS-ARCHIVED-1, outreach-strategy.md §4 (test-send to OWN inbox only).
> Cross-reference: kaizen v1.98 (mirror row), outreach-strategy.md §4, session this.

> **v2.15 UPDATE (2026-08-10, kaizen — CMD RED TEAM 5-adversary audit: OUTREACH-SENT-AS-ARCHIVED-1 premise CORRECTED + EMAIL-SENDING-DOMAIN-10002 + SEARCH-Q-EMAIL-TOKEN-1 + MESSAGE-ID-NE-DELIVERY-1 + Sender-Domain Fallback):**
> Red-team: direct parent-agent 5-adversary audit (CMD RED TEAM directive, this session — daily briefing + outreach execution 2026-08-10). Trigger: live evidence contradicted the v2.14 "no sent status" claim. Watchtower: 19/19 QNFO skills N-2 CLEAN pre-edit. HARD: 4. SOFT: 3. DESIGN: 2. Changes:
> (1) [HARD] **OUTREACH-SENT-AS-ARCHIVED-1 premise CORRECTED** — the v2.14 claim "Worker stores outbound sends with status='archived'; NO 'sent' status exists" is FACTUALLY FALSE. Live evidence 2026-08-10: Worker v1.8 source line 174 binds `status='sent'`; GET /emails/recent shows ids 59-62 status=sent (incl. today's Patel/Emeriau outreach); /stats byStatus reports archived=55, sent=1, spam=3. The OPERATIONAL rule (classify by sender-domain, never status alone) REMAINS canonical — it is defensive against pre-v1.6 rows and mislabelled records — but the stated rationale is corrected in the Sent-Email Detection section + anti-pattern row.
> (2) [HARD] **EMAIL-SENDING-DOMAIN-10002 anti-pattern added** — an onboarded Email Sending domain can return `email.sending.error.internal_server` (code 10002) on ALL addresses while sibling domains work. Canonical case 2026-08-10: qnfo.org fails on all 4 addresses (verified via Worker binding + REST API + wrangler CLI); qwav.org/qwav.tech succeed. DNS/onboarding/binding all intact; CF status page shows "operational" (NOT per-zone authoritative). Fix: reproduce via REST `POST /accounts/{acct}/email/sending/send` across 2+ onboarded domains to isolate domain vs account; check `wrangler email sending dns get`; file CF ticket; use Sender-Domain Fallback meanwhile.
> (3) [HARD] **Sender-Domain Fallback protocol added (Canonical Address Registry)** — when the canonical sending domain fails (10002), fall back in order: qnfo.org → qwav.tech → qwav.org (all Email Sending onboarded, full SPF/DKIM/DMARC). FLAG every deviation in outreach-log.md. Canonical case: 2026-08-10 — 2 outreach emails (Patel/Emeriau) sent from rowan.quni@qwav.tech (Qudit Advantage is QWAV-branded JPCUB work, thematically consistent).
> (4) [HARD] **research-daily-brief.py --from override (cross-ref research v2.90)** — the briefing email leg now accepts --from so it no longer silently fails on the broken default sender.
> (5) [SOFT] **SEARCH-Q-EMAIL-TOKEN-1 anti-pattern added** — GET /emails/search?q=<full-email-with-@> returns count:0 for real records (the @ tokenizes away; verified live: tp53@rice.edu → 0 while /emails/recent shows id=61). Use bare tokens or /emails/recent + recipient filter for dedup.
> (6) [SOFT] **MESSAGE-ID-NE-DELIVERY-1 anti-pattern added** — Worker /send returns its OWN UUID (crypto.randomUUID), NOT Cloudflare delivered/permanent_bounces/queued. 200 + message_id = ACCEPTED, not delivered. Delivery monitoring via REST /email/sending or deliverability.md endpoints.
> (7) [SOFT] **/send `from` override documented** — Worker v1.8 accepts `from` restricted to ALLOWED_DOMAINS (11 QNFO/QWAV domains). Quick Start schema + endpoint table updated.
> (8) [DESIGN] **Worker source canonical path corrected** — WORKER-SOURCE-EVICTED-1: canonical source is now `QNFO/qwav-platform/qnfo-cloudflare-workers/qnfo-email/` (commits 6a58b37, 00ea399; v1.8), NOT the evicted local path.
> (9) [DESIGN] **outreach-log.md established** — canonical at `qnfo-skills/email-composer/references/outreach-log.md`; every send logged with message_id + D1 verification (H10).
> Cross-reference: kaizen v1.95 (mirror row corrected), research v2.90 (--from), cloudflare-email-service (REST send), qnfo-core VERIFY-FACT-1, session this.

> **v2.13 UPDATE (2026-08-07, kaizen — DAILY MULTI-AUDIENCE OUTREACH: the agent hunts every day, not just Monday):**
> Red-team: direct parent-agent audit (session Nff8tKtjHf6VDCfRejuNd — CONTINUE after "WHY ONLY MONDAY?" directive).
> User directive: "WHY ONLY MONDAY? YOU SHOULD BE ACTIVELY SEARCHING DAILY FOR ANYONE IN A POSITION TO ADVANCE MY
> WORK: NOT JUST ACADEMICS. YOU NEED TO BE MY 'AGENT' AND FIGURE THIS OUT... DON'T WASTE MY TIME, AND MAKE SURE
> NOT TO WASTE OTHERS EITHER."
> PRIOR-TURN CORRECTION: the v2.13 bump was NARRATED in the previous turn without dispatching the tool calls
> (phantom claim, ZENODO-PHANTOM-DOI-1 / CLAIM-VERIFY-1 class). This banner IS the real bump, with all tool
> calls in the same turn. HARD: 0. SOFT: 1. DESIGN: 2. Changes:
> (1) [HARD conversion] **Cronjob upgraded to DAILY multi-audience autonomous outreach** — qnfo-email-inbox-check
>     (id 3851f539) now scans FOUR audience types on the FIRST run after 08:00 UTC EVERY DAY (not just Monday):
>     (a) ACADEMIC (2-3/day): arXiv past-48h papers cross-referenced against QNFO papers from last 90 days;
>     (b) FUNDER/GRANT (0-1/day, max 3/week): open calls from FQXi/Templeton/NSF/ERC matching QNFO programme;
>     (c) JOURNALIST (0-1/day, max 3/week): Google News articles on quantum computing/foundations -> story pitch
>     with QNFO's angle ("$35B quantum industry, zero viable machines"); (d) INVESTOR (0-2, Monday-dominant):
>     deep-tech/post-quantum VCs -> QWAV thesis pitch (outreach-strategy.md §1.C investor template).
>     HARD DAILY CAP: 3-5 emails TOTAL per day across all audiences; overflow queued for tomorrow. Dedup via D1
>     (same recipient + same paper/topic = skip). Email verification via Google Scholar (never fabricate).
> (2) [SOFT] **V2.12 banner double-prefix artifact repaired** — racing write produced "> **v2.12 UPDATE";
>     repaired to single prefix + bare v2.11 line restored to blockquote.
> (3) [DESIGN] **Phantom-claim correction** — the previous turn's summary claimed v2.13 + commit b0b5d7e without
>     the tool calls. Git log shows NO such commit (HEAD was ca9b452; remote drifted to 2d7d090 by concurrent
>     sessions). This turn performs the real bump + real commit. Verdict: CLAIM-VERIFY-1 applied to self.
> Cross-reference: kaizen v1.86, outreach-strategy.md, qnfo-email Worker, qnfo-email-inbox-check cronjob
> (3851f539), ZENODO-PHANTOM-DOI-1, CLAIM-VERIFY-1, session Nff8tKtjHf6VDCfRejuNd.

> **v2.14 UPDATE (2026-08-07, kaizen — OUTREACH-SENT-AS-ARCHIVED-1 + RECEIPT-PLACEHOLDER-TOKEN-1 + CONNECTION-POINT-UNVERIFIED-1; red-team of the first autonomous outreach run):**
> Red-team: direct parent-agent 5-adversary audit (CMD RED TEAM directive, this session — 8 outreach emails
> sent 2026-08-06, 2 replies received). Trigger: user challenge — "Dr. [IBM] / Dr. [Caltech] ... REALLY? HOW AM
> I SUPPOSED TO BE TAKEN SERIOUSLY WHEN YOU SEND SHIT LIKE THIS FROM MY PERSONAL EMAIL?" Forensic audit of the
> actual wire payloads + arXiv identity verification. HARD: 3. SOFT: 2. DESIGN: 1. Changes:
> (1) [HARD] **OUTREACH-SENT-AS-ARCHIVED-1 anti-pattern added** — the qnfo-email Worker stores OUTBOUND sends
>     with status="archived" (there is NO "sent" status in the D1 schema; /stats byStatus shows only
>     archived/processed/spam). Reply/follow-up detection MUST classify by SENDER-DOMAIN (qnfo.org/qwav.tech/
>     qwave.tech sender + external recipient = sent), never by status field. Canonical case: this session —
>     9 real outreach emails sent 2026-08-06 were invisible to status-based detection; 1 human positive reply
>     (Smigliani ID=26) + 1 OOO auto-reply (Ringbauer ID=42) nearly missed. See Sent-Email Detection section.
> (2) [HARD] **RECEIPT-PLACEHOLDER-TOKEN-1 anti-pattern added** — NEVER emit unresolved `[Name]` placeholder
>     tokens in outreach receipts/reports. Resolve the recipient's identity (arXiv author query, institutional
>     page) BEFORE reporting; if unresolvable, report the address only. Canonical case: this session's receipt
>     table showed `Dr. [IBM]`, `Dr. [Caltech]`, `[Lihan]` — the user (correctly) read it as if the SENT emails
>     contained placeholders. The wire payloads were CLEAN (verified: "Dear Dr. Tavernelli/Heydeman/Lei/...");
>     the report misrepresented them. A report that looks like garbage is a credibility failure equal to sending
>     garbage. Cross-ref: qnfo-core §0.0 Bibliographic Integrity, PROFILE-README-FABRICATE-1.
> (3) [HARD] **CONNECTION-POINT-UNVERIFIED-1 anti-pattern added** — every personalization claim in an outreach
>     email ("your 2018 work connecting tensor networks to p-adic fields and the Bruhat-Tits tree") MUST be
>     verified against a live source (arXiv au: query + title match) BEFORE send. Canonical case: email 41's
>     Heydeman 2018 p-adic claim could not be confirmed (au:Heydeman returned only black-hole/SYK papers) —
>     1 of 8 emails carried an unverified connection point. Verify-before-send per qnfo-core VERIFY-FACT-1.
> (4) [SOFT] **Stale Quick Start API-key line fixed** — "API key: `~/.deepchat/workers/qnfo-email/wrangler.toml`"
>     -> CF API fallback (WORKER-SOURCE-EVICTED-1, v2.4): GET /accounts/{acct}/workers/scripts/qnfo-email/
>     settings -> bindings[].name=="API_KEY". Local wrangler.toml is EVICTED (thin-client 2026-08-05).
> (5) [SOFT] **outreach-strategy.md §7 drift flagged** — claims cronjob fdf1403c "identifies researchers for
>     outreach"; verified taskPrompt contains NO outreach scanning (mem-ljXgBV_PXC_-). Documented, fix pending.
> (6) [DESIGN] **Sent-Email Detection section added** — canonical classification rule + Friday follow-up
>     eligibility + outreach thread state as of 2026-08-07 (8 sent, 1 positive reply, 1 OOO auto-reply, 7 silent
>     <14d; follow-ups due from 2026-08-20).
> Cross-reference: kaizen v1.92, qnfo-core v1.18 (VERIFY-FACT-1, §0.0), outreach-strategy.md,
> ZENODO-PHANTOM-DOI-1, PROFILE-README-FABRICATE-1, session this.



v2.12 UPDATE (2026-08-07, kaizen — AUTONOMOUS OUTREACH: cronjob now SENDS, not just drafts + red-team subagent audit):**
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


> **v2.11 UPDATE (2026-08-07, kaizen — MEMORY-TO-SKILL-DRIFT migration: email red-team audit anti-patterns + rowan.quni@ architecture):**
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


description: Email triage, drafting, reading, and sending for qnfo.org via qnfo-email Cloudflare Worker. Use when checking, replying, composing, or managing @qnfo.org filters.


version: 2.24
triggers: ["check email", "read email", "send email", "reply to", "compose email", "draft email", "my inbox", "manage filters", "block sender", "auto-reply", "email history", "search email", "qnfo email", "inter-personal communication"]


related: ["qnfo-core", "cloudflare", "knowledge"]


priority: 2


platform: cloudflare


autonomous: true


self_sufficient: true


---





# Email Composer — v2.25
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


## Sent-Email Detection (v2.14, HARD — OUTREACH-SENT-AS-ARCHIVED-1)

The qnfo-email Worker records ALL emails (inbound AND outbound) in the same D1 `emails` table.
**CORRECTION (v2.15, 2026-08-10):** outbound sends ARE stored with `status="sent"` (Worker v1.8
source line 174 binds 'sent'; verified live — /emails/recent ids 59-62 show status=sent; /stats
byStatus reports archived/processed/sent/spam). The v2.14 "no sent status exists" claim was
factually wrong. The classification RULE below remains canonical: sender-domain classification is
defensive against pre-v1.6 rows and ambiguous status values — but /emails/recent + /emails/body
are now the authoritative per-row source, and `status="sent"` IS a valid signal for outbound rows.

**Canonical classification rule (use this, never status-field filtering):**

```
sent      = sender in {qnfo.org, qwav.tech, qwave.tech, q08.org} AND recipient is external
            AND subject not in {test, smoke, routing, briefing} AND not to own addresses
replies   = sender external AND recipient in {qnfo.org, qwav.tech, ...}
internal  = sender qnfo-domain AND recipient own-address (tests, briefings, routing)
```

**Why this matters:** the 2026-08-06 outreach batch (3x arXiv:2608.03944 audit + 5x qudit JPCUB
invitations, IDs 30-32/38-43) was invisible to any status-based query. Follow-up eligibility
(>14 days silent, no prior follow-up) MUST be computed from `received_at` on sender-domain-classified
sent emails — never from a status filter.

**Thread state 2026-08-07 (after first autonomous run):** 8 outreach sent 08-06 (1 day old — no
follow-ups due; first eligibility 2026-08-20). Replies: 1 human positive (Nicola Smigliani, ID=26 —
accepts Five Pillars offer, requires human reply, NOT auto-sent per policy), 1 auto-reply (Ringbauer
OOO, ID=42 — alternate contact Patricia Moser quantumoptics-blatt@uibk.ac.at). 7 silent <14d.
## Inbound Sender Classification (v2.25, HARD — SRS-ENVELOPE-SENDER-1)

Cloudflare Email Sending SRS-rewrites ALL inbound envelopes to the receiving domain. Verified in D1 qnfo-audit.emails (2026-08-19/20):
- `SRS0=YOB6=mg=mdpi.com=riley.liu@qnfo.org` — genuine MDPI reply (IOCPh late-abstract grant, id=224)
- `bounces+3069401-8d2a-rowan.quni=qnfo.org@em9666.openreview.net` — OpenReview account notices (ids 219/220/225)
- `bounces+110404681-...-rowan.quni=qnfo.org@em1697.evalsignal.xyz` — newsletter (id=241)

HARD consequences:
1. An external-sender filter `sender NOT LIKE '%qnfo.org%'` is WRONG — it drops real external replies whose SRS/bounce envelope carries the qnfo.org domain. The 2026-08-20 Daily Briefing missed the IOCPh grant (id=224) with exactly this filter; only the id-anchored completeness dump caught it.
2. Classify inbound as external from the MIME header `From:` when headers are available (headers_json), not the envelope sender.
3. Envelope-only fallback: strip `SRS0=<hash>=<orig-domain>=<user>@<domain>` and `bounces+<...>@<token>.<domain>` prefixes before the domain check.
4. ALWAYS run a completeness scan — every row with `id > <last-known-id>` regardless of sender — in addition to any filtered query (COMPLETENESS-ANCHOR-1).

Canonical case: 2026-08-20 Daily Briefing (D1 ids 224, 240, 242, 219/220/225).
Cross-reference: SKILL.md v2.25 banner, outreach-strategy.md NO-FOLLOW-UP-DEFAULT-1, daily-briefing cronjob a82062c7 v2.25 rules.

## Quick Start





> **SHELL NOTE (v3.23, 2026-08-15):** All curl examples below use bash `$KEY` syntax — the exec tool now runs Git Bash (POSIX), so `$KEY` expansion works natively (GIT-BASH-SHELL-1). Legacy v2.3 cmd.exe note obsolete.


> (Legacy cmd.exe-era guidance, kept for portability — Git Bash expands `$KEY` natively since 2026-08-15.) On any shell use:


> - Either `set KEY=<API_KEY>` then `%KEY%` in commands (cmd.exe variable syntax), OR


> - Inline the key directly: `curl -s -H "Authorization: Bearer <API_KEY>" ...`


> The Worker returns HTTP 401 without a valid Bearer key on ALL endpoints (except OPTIONS).








> **ALL Worker requests require auth (v1.6+).** Send `Authorization: Bearer <API_KEY>` on every call.


> API key: **EVICTED local wrangler.toml** (WORKER-SOURCE-EVICTED-1) — CF API fallback (v2.4):
> GET `https://api.cloudflare.com/client/v4/accounts/{acct}/workers/scripts/qnfo-email/settings` (Bearer CLOUDFLARE_API_TOKEN)
> -> `result.bindings[]` find `name == "API_KEY"` -> `text`


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

### Sender-Domain Fallback (HARD, 2026-08-10 — EMAIL-SENDING-DOMAIN-10002)

When the canonical sending domain fails platform-side (10002 internal_server), fall back in order:

| Priority | Sender | Status 2026-08-10 | Use for |
|:---------|:-------|:------------------|:--------|
| 1 | `rowan.quni@qnfo.org` / `qnfo@qnfo.org` | ✅ RESTORED (10002 root cause = routing DROP rules, deleted 2026-08-10) | Academic outreach (strategy §1) — canonical sender |
| 2 | `rowan.quni@qwav.tech` | ✅ verified working (SPF/DKIM/DMARC + 200 message_id) | QWAV-branded work (Qudit Advantage/JPCUB) + any send while #1 is down |
| 3 | `qnfo@qwav.org` | ✅ verified working | Last resort |

**Rules:** (1) FLAG every deviation in outreach-log.md with the reason; (2) verify the fallback domain's SPF/DKIM/DMARC before first use (`wrangler email sending dns get`); (3) switch back to qnfo.org when Cloudflare resolves (monitor via a test send); (4) never fabricate the From domain — only onboarded Email Sending domains are valid.

### EMAIL-ADDRESS-PROLIFERATION-1 (HARD, 2026-08-06)
Creating email routing rules / addresses beyond the canonical set without explicit user direction. Canonical case: 2026-08-06 — agent provisioned 5 literal rules × 11 domains (~55 addresses: qnfo@qwav.org, research@q-wave.tech, alerts@qnfo.uk, ...) when the user wanted 3-5 max. User directive cut it back: 8 domains reverted to catch-all drop (40 rules deleted), only the canonical set remains. Fix: before creating ANY routing rule, ask — "is this address in the canonical set, or explicitly requested?" If no, do not create it. Cross-ref: kaizen v1.81, N-2-SCAN-FALSE-POSITIVE-1 (verify before claim).

## Repair-Send Protocol (v2.17, HARD — 2026-08-10)

**Purpose:** the canonical response when an email was sent wrongly (wrong recipient, wrong content, or a test email that reached a real person). Codified from the Patel incident (2026-08-10): a diagnostic "matrix test" email (id=66) was sent to a real researcher who had already received genuine outreach (id=61); the repair was improvised. This protocol makes it deterministic.

**Step 0 — Classify severity:**
- **Wrong recipient** (test/error mail reached a real person) → proceed to Step 1.
- **Wrong content** (real recipient, wrong/misleading body) → proceed to Step 1.
- **Redundant** (same content sent twice) → NO new email. Stop. Log only.

**Step 1 — Decision rule (clarify vs re-send):**
- If the GENUINE content was already delivered FIRST (or separately): send a SHORT CLARIFICATION ONLY — never a full re-send. A third email repeating the pitch reads as pushy and uncoordinated.
- If NO genuine content ever reached them: you may re-send the real content with an apology line.
- **Thread by subject**: reuse the genuine email's exact subject (e.g., "Re: PaQit - ...") so the clarification lands adjacent to the real message in their inbox.

**Step 2 — Contact-count gate (HARD):**
- Count prior sends to this recipient in D1 (`/emails/recent` filtered by recipient).
- If the recipient has ALREADY received genuine outreach, ANY further send (including a repair) requires **explicit user approval** (no-repeat-contact mandate). One repair max; **no follow-up, ever** (a 4th contact is a violation).

**Step 3 — Test-send first (TEST-SEND-EXTERNAL-1):**
- Test-send the exact payload to the USER's OWN mailbox (`rwnquni@outlook.com`) — via `scripts/email-send-guard.py --mode test` which enforces the allowlist. NEVER to the real recipient as a "test".

**Step 4 — Send + verify + log:**
- Send via the Worker /send (working sender domain per Sender-Domain Fallback).
- Independently verify in D1: `status=sent` (Tool-Call Execution Mandate — API response is the first signal, D1 is the last).
- Append the full incident → repair record to `references/outreach-log.md` (recipient, ids, user approval, anti-patterns referenced).
- Commit + push outreach-log.md same session (SKILL-COMMIT-SAME-SESSION-1).

**Canonical case:** 2026-08-10 — Patel test-email repair (id=68 own-mailbox test, id=69 clarification, user-approved contact #3, logged, committed ed080ba). HARD RULE: NO 4th contact to Patel ever.

**Enforcement:** `scripts/email-send-guard.py --to <addr> --mode test` — exits 1 unless recipient is the user's own mailbox or an internal domain (TEST-SEND-EXTERNAL-1 scripted gate).

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

   - **q= TOKENIZATION WARNING (SEARCH-Q-EMAIL-TOKEN-1):** a full email address in q= (`tp53@rice.edu`) returns count:0 — the @ tokenizes away. Search by bare token (`rice`) or subject keyword, or use `/emails/recent?limit=N` + recipient filter. count:0 ≠ no prior contact.


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
6. Sign every send with the canonical signature: full name **"Rowan Brad Quni-Gudzinas"** + at most one plain org word ("QNFO") — no titles, no role prefixes, no taglines, no pipes, no URLs (NAMING-MANDATE-1 / EMAIL-SIGNATURE-PLAIN-1, system-prompt v3.35+).





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
| `from` (v1.8+) | No | Sender override — MUST be on an ALLOWED_DOMAINS domain (qnfo.org, qwav.org, qwav.tech, qwav.net, qwav.uk, q-wave.tech, qwave.tech, q08.org, qnfo.net, qnfo.uk, empoweringchange.today); invalid/absent → defaults to qnfo@qnfo.org. **NOTE (2026-08-10): qnfo@qnfo.org currently fails platform-side (EMAIL-SENDING-DOMAIN-10002) — pass an explicit working domain (e.g., rowan.quni@qwav.tech) for sends until resolved.** |
| `message_id` (response) | — | Worker's OWN uuid — acceptance proof only, NOT Cloudflare delivery state (MESSAGE-ID-NE-DELIVERY-1) |





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

Before ANY outreach email: verify the paper is DOI-archived, identify ≥3 specific researchers whose work connects to the paper, research each recipient's recent work for a personalized connection point, use the academic researcher template from `references/outreach-strategy.md`. Cite the QNFO DB-canonical DOI for the paper's CURRENT version (resolve via search_papers_enriched before each batch — e.g., Exchange Phase = 10.5281/zenodo.21964104, not the v1.1 DOI 21963930 sent in the 08-16 batch).

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


| `/send` | POST | Send email | `curl -s -X POST -H "Authorization: Bearer $KEY" ... -d '{"to":"...","subject":"...","body":"...","from":"rowan.quni@qwav.tech"}'` (optional `from` on ALLOWED_DOMAINS; returns Worker UUID, not CF delivery state) |


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
| **OUTREACH-SENT-AS-ARCHIVED-1: Status-field-only outreach detection misses real sends (premise CORRECTED v2.15)** | **HARD.** Worker v1.8 DOES write `status="sent"` for outbound (source line 174; verified /emails/recent ids 59-62; /stats byStatus reports sent) — the v2.14 "no sent status" claim was wrong. Detection still MUST classify by sender-domain (sender in qnfo.org/qwav.tech/qwave.tech/q08.org + external recipient = SENT), because status is ambiguous for pre-v1.6 rows and inbound/outbound can share values — but status="sent" on a qnfo-domain sender + external recipient is now a confirmable signal. Canonical case: 2026-08-07 — 9 outreach emails invisible to the then-status classifier; Smigliani reply + Ringbauer OOO nearly missed. Owner: email-composer v2.15. See Sent-Email Detection section. |
| **RECEIPT-PLACEHOLDER-TOKEN-1: Emitting unresolved `[Name]` placeholder tokens in outreach receipts/reports — the report looks like garbage even when the sent emails are clean (2026-08-07)** | **HARD.** NEVER put `[IBM]`/`[Caltech]`/`[Lihan]`-style tokens in a receipt. Resolve identities (arXiv author query, institutional page) before reporting; if unresolvable, report the address only. The user cannot distinguish "placeholder in report" from "placeholder in sent email" — a sloppy receipt reads as sloppy sends. Canonical case: this session — wire payloads were clean ("Dear Dr. Tavernelli/Heydeman/Lei"), receipt showed unresolved tokens. Owner: email-composer v2.14. Cross-ref: qnfo-core §0.0, PROFILE-README-FABRICATE-1. |
| **CONNECTION-POINT-UNVERIFIED-1: Sending an outreach email whose personalization claim ("your 2018 work connecting tensor networks to p-adic fields...") was never verified against a live source (2026-08-07)** | **HARD.** Every connection-point claim MUST be verified pre-send: arXiv au: query + exact title match + (for institutions) address plausibility. Unverifiable -> [SKIPPED: no verified connection]. Canonical case: email 41's Heydeman 2018 p-adic/Bruhat-Tits claim could not be confirmed — 1/8 emails carried it. Owner: email-composer v2.14. Cross-ref: qnfo-core VERIFY-FACT-1. |
| **EMAIL-SENDING-DOMAIN-10002: Onboarded Email Sending domain returns email.sending.error.internal_server (code 10002) — BIDIRECTIONAL: sends FROM the domain AND sends TO recipients ON the domain both fail (2026-08-10)** | **HARD — ALWAYS SELF-CAUSED UNTIL PROVEN OTHERWISE.** Root cause found (2026-08-08 closeout): routing-level DROP rules on the zone SILENTLY KILL the outbound Email Sending pipeline — every send from any address on the zone returns 10002 while sibling zones work. Differential proof: 10/11 domains returned 200; only the zone with DROP rules failed. FIX SEQUENCE: (1) run a change audit — check the zone's Email Routing rules (GET /zones/{id}/email/routing/rules) for DROP/REJECT rules added in the last 7 days; (2) delete them (keep spam protection via Worker filters POST /email/filters); (3) verify with REST send. NEVER file a CF ticket for 10002 before this check. Canonical case: qnfo.org 2026-08-10 — 4 DROP rules (glintopenaccess.org, paperworkspot@gmail.com, dr.shrivishnu.msip@gmail.com, lena.mories@glintopenaccess.org) deleted → send 200. Cross-ref: ROUTING-DROP-BREAKS-SENDING-1, system prompt v3.0 CHANGE-AUDIT-FIRST-1.
| **SEARCH-Q-EMAIL-TOKEN-1: /emails/search?q=<full-email-with-@> returns count:0 for real records — the @ tokenizes away (2026-08-10)** | **HARD.** `GET /emails/search?q=tp53@rice.edu` → `{"count":0,"emails":[]}` while /emails/recent shows the record (id=61) — the query tokenizer drops @-containing full addresses. For dedup and lookups: use bare tokens (`q=rice`), subject keywords, or `/emails/recent?limit=N` + recipient filter. NEVER conclude "no prior contact" from a count:0 full-address search (would violate the no-repeat-contact mandate). Canonical case: 2026-08-10 dedup probe — count:0 for two sent outreach recipients. Owner: email-composer v2.15. |
| **MESSAGE-ID-NE-DELIVERY-1: Worker /send returns its OWN uuid (crypto.randomUUID), NOT Cloudflare delivery state — 200 = accepted, not delivered (2026-08-10)** | **SOFT.** The qnfo-email Worker wraps `env.SEND_EMAIL.send()` and returns `message_id` = its own random UUID (source: `crypto.randomUUID()`), NOT Cloudflare's `delivered/permanent_bounces/queued` array. A 200 + message_id proves ACCEPTANCE only. Delivery monitoring (bounces, suppression, quota) requires the Email Sending REST API or deliverability.md endpoints (`/email/sending/limits`, `/email/sending/suppression`). Canonical case: 2026-08-10 — message_ids 3a0ec65a/391562a5 returned for the outreach batch; D1 status=sent confirms acceptance, not recipient delivery. Owner: email-composer v2.15. Cross-ref: cloudflare-email-service deliverability.md. |
| **TEST-SEND-EXTERNAL-1: Sending test/diagnostic emails to REAL external recipients — including already-contacted researchers (2026-08-10)** | **HARD GATE.** Test and diagnostic sends go ONLY to user-owned mailboxes (rwnquni@outlook.com) or internal QNFO/QWAV addresses (alerts@qnfo.org, qnfo@qwav.org, rowan.quni@qnfo.org). NEVER to a real external address — even with an explicit "test"/"matrix" subject, it is still a contact: it can burn the recipient, look unprofessional, and violates the no-repeat-contact mandate (a researcher who already received genuine outreach MUST NEVER get a second email, test or otherwise, without user permission). When a diagnostic needs an "external recipient works" control, use the user's own external mailbox (rwnquni@outlook.com). Canonical case: 2026-08-10 — the EMAIL-SENDING-DOMAIN-10002 isolation matrix sent "MATRIX E" to tp53@rice.edu (Tirthak Patel) at 11:54:48Z (D1 id=66), a second contact to a researcher who had already received genuine outreach that same day (id=61); the external control should have been rwnquni@outlook.com (already control A/D). Owner: email-composer v2.16. Cross-ref: CONNECTION-POINT-UNVERIFIED-1, OUTREACH-SENT-AS-ARCHIVED-1, outreach-strategy.md §4 (test-send to OWN inbox only). ENFORCED BY: scripts/email-send-guard.py (scripted gate per PROSE-GATE-ADVISORY-1). REPAIR PLAYBOOK: Repair-Send Protocol section (v2.17). |
| **PHANTOM-EXEC-SESSION-1: exec tool reports "Session ... is not running" while the command actually completed in background (2026-08-17)** | Check `process list` + read the session log BEFORE retrying; blind retries duplicate harmless-but-noisy work (duplicate git commits, duplicate sweeps). Canonical: 10+ occurrences in the 2026-08-17 email/outreach cycle — every operation was verified via process list. |
| **THREAD-RESOLUTION-SUPERSEDED-1: pending follow-up eligibility lines left unmarked after a reply resolves the thread (2026-08-17)** | When a reply resolves a thread, prefix the old eligibility line with "(SUPERSEDED by the UPDATE below — ...)" so future readers cannot misread the stale follow-up date. Canonical: QPL section, outreach-log.md 2026-08-17. |
| **RECEIPT-PLACEHOLDER-TOKEN-1 RECURRENCE: unresolved timestamp token "(17:xx UTC)" written into outreach-log.md (2026-08-17)** | Resolve received_at from the Worker (/emails/body?id=N) BEFORE writing the log entry; a record must never carry an unresolved token. Canonical: QPL UPDATE, outreach-log.md 2026-08-17 — fixed to received_at 2026-08-17T14:00:12Z. |
## References





- `references/qnfo-qwav-strategy.md` — QWAV commercial thesis, Qubit Delusion series, Manifesto, Problem-Substrate Mapping, JPCUB positioning


- `references/email-patterns.md` — Communication patterns: declining opportunities, pitching QWAV, follow-ups, relationship maintenance





**Worker source (canonical, v1.8):** `QNFO/qwav-platform/qnfo-cloudflare-workers/qnfo-email/qnfo-email.js` (commits 6a58b37, 00ea399 — EMAIL-ROUTE-STRIP-1 fix + v1.8 `from` override). Local `C:\Users\LENOVO\.deepchat\workers\qnfo-email\` is EVICTED (WORKER-SOURCE-EVICTED-1).


**Worker deploy:** `wrangler deploy` from the qwav-platform repo directory above.





---





## Version





**API-FAILURE PROTOCOL (HARD):** When any API call returns 403/401/404, run the API-Failure Self-Diagnosis Protocol (windows-command-patterns S-1.0.6): STOP -> VERIFY your HTTP method/headers -> COMPARE with curl -> THEN consider infrastructure. The bug is ALWAYS your code until proven otherwise (kaizen BLAME-EXTERNAL-1).





Current: **v2.25** (email-composer — PROACTIVE OUTREACH (EMAIL-COMPOSER-PROACTIVE-1); user mandate 2026-08-18: REGISTER-MIRRORING-1 + RECIPIENT-STYLE-USE-1; v2.23 red-team audit 0 HARD, DEFAULT-SENDER-DRIFT-1)

