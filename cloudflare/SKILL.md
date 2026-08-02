---
name: cloudflare
description: ULTRA-CONSOLIDATED Cloudflare Full-Stack (17-MCP Coverage) -- Workers, Pages, D1, R2, KV, Vectorize, Queues, Durable Objects, AI, DNS, Zero Trust, Email, WAF, CDN, Turnstile, Infrastructure Audit, MCP Server Management. The ONLY infrastructure skill. NEVER treat Cloudflare components in isolation -- ALL code, outputs, and deliverables must evaluate the full Cloudflare stack end-to-end.
version: "3.19"
triggers: ["cloudflare-deployer", "deploy", "wrangler", "Pages", "Workers", "R2", "D1", "DNS", "KV", "Vectorize", "Queues", "AI", "Durable Objects", "Zero Trust", "Access", "Gateway", "WARP", "Tunnel", "WAF", "CDN", "Turnstile", "email", "SPF", "DKIM", "DMARC", "infrastructure", "audit", "health check", "orphan", "lifecycle", "worker route", "route conflict", "522", "CNAME", "Cloudflare", "upload", "migrate", "Pages Functions", "Workers for Platforms", "Cron Triggers", "Tail Workers", "Smart Placement", "Hyperdrive", "Secrets Store", "Pipelines", "Browser Rendering", "Zaraz", "Argo", "Spectrum", "TURN", "Network Interconnect", "Cache Reserve", "Bot Management", "API Shield", "DDoS", "Analytics Engine", "Web Analytics", "GraphQL API", "Observability", "Miniflare", "Sandbox", "Workerd", "Terraform", "Pulumi", "Snippets", "Containers", "Workflows", "Artifacts", "R2 Data Catalog", "R2 SQL", "Static Assets", "Bindings", "Image", "Stream", "RealtimeKit", "Flagship", "feature flags", "Agents SDK", "AI Gateway", "AI Search", "Workers AI", "do", "durable", "sandbox", "turnstile", "web-perf", "thin client", "IaC", "consolidation", "4-D", "IPFS bridge", "DNSLink", "Arweave", "Filecoin", "distributed", "durable", "discoverable", "duplicated"]
related: ["qnfo-agent", "research"]
priority: 1
platform: cloudflare
autonomous: true
self_sufficient: true
---

# CLOUDFLARE -- v3.19 (Kaizen: MCP OAuth loopback protocol — no default browser)

> **v3.19 UPDATE (2026-08-02, kaizen — MCP OAuth loopback protocol; NO default browser):**
> Red-team: direct parent-agent audit after the Cloudflare Observability MCP OAuth fix.
> HARD: 1. SOFT: 0. DESIGN: 1.
> Changes:
> (1) [HARD] **NEVER repeatedly open the external/default browser for MCP or Cloudflare
>     OAuth flows. Do NOT use the default browser for OAuth consent.** The 2026-08-02
>     Observability MCP OAuth fix initially looped the default browser (frustrating,
>     laborious). Correct autonomous flow (§MCP OAuth Loopback Fix below): recover the
>     PKCE verifier + client_id from `~/.mcp-auth/mcp-remote-<ver>/<hash>_client_info.json`
>     + `_code_verifier.txt`; start a listener on the registered redirect port with
>     AUTO-EXCHANGE inside the listener process; open the auth URL ONCE in the session
>     browser (YoBrowser/CDP) — the session browser is often NOT logged in, and if the
>     flow cannot complete headlessly, STOP and report the blocker; do not spawn more
>     browser windows.
> (2) [DESIGN] Added **§MCP OAuth Loopback Fix** — the full recover→listen→auto-exchange→
>     cache protocol, including the two failure modes found live: (a) code expires in
>     <60s so exchange MUST happen inside the listener process, never a separate tool
>     call; (b) session browser may lack the Cloudflare login while the default browser
>     has it — resolve by completing consent headlessly or reporting the blocker.
> Cross-reference: memory "MCP OAuth loopback fix pattern", kaizen v1.4.1,
> observability.mcp.cloudflare.com/mcp (workers-observability v0.5.2).

> **v3.18 UPDATE (2026-08-02, kaizen — memory-to-skill migration + CF tool discoverability):**
> Red-team: direct parent-agent audit (user mandate: DeepChat memories are EPHEMERAL —
> critical operational rules MUST live in SKILL.md, not durable memory).
> HARD: 0. SOFT: 3. DESIGN: 1.
> Changes:
> (1) [SOFT] **HARDCODED-HEALTH-1: Worker health endpoints that hardcode binding names
>     (e.g. `d1: "living-paper"`) produce false-positive health checks.** `/health` MUST
>     verify at runtime with `!!env.BINDING_NAME` (e.g. `ai: !!env.AI`) — never echo the
>     expected name as a string. Case: qnfo-qwav reported `d1:"living-paper"` while
>     `env.LIVING_PAPER` was undefined at runtime ("Cannot read properties of undefined
>     (reading 'prepare')"). Migrated from durable memory (ephemeral) into this skill.
> (2) [SOFT] **CF-WAF-1: Cloudflare WAF blocks non-browser user-agents (urllib default).**
>     When testing Worker endpoints with Python, ALWAYS pass
>     `headers={'User-Agent':'Mozilla/5.0'}`; without it urllib gets HTTP 403.
>     To read error bodies: catch `urllib.error.HTTPError` and call `e.read().decode()`
>     — this surfaces the real Worker error (e.g. 1101 body, "Cannot read properties...").
>     Migrated from durable memory (ephemeral).
> (3) [SOFT] **MCP-OFFLOAD-1: QNFO MCP tools (search_papers, query_graph, etc.) return
>     "OK" with results offloaded** — offload files may not be readable in-session.
>     For verification of infra claims, use DIRECT probes (Python urllib with browser UA
>     against the live Worker endpoint) instead of relying solely on MCP tool output.
> (4) [DESIGN] Added **§Skill Cross-Reference: Cloudflare Tool/Resource Discoverability**
>     — a map of which skills touch Cloudflare resources and how to discover the right
>     MCP agent tools (below). Every skill that references D1/R2/Vectorize/Pages/Workers
>     MUST name the actual agent tool (`workers_list`, `query_worker_observability`,
>     `search_cloudflare_documentation`, `search_papers`, `query_graph`) in its
>     instructions, per the ephemeral-memory mandate.
> Cross-reference: kaizen v1.4.1, memory-management, windows-command-patterns v2.4,
> git-github v2.4, frontend-design v2.3, documents v2.4.

> **v3.17 UPDATE (2026-08-02, kaizen — STALE-AUDIT-1 anti-pattern + red-team v2 validation):**
> Red-team: direct parent-agent audit of session bWLdtP54lAjqfblr2cUKH.
> HARD: 0. SOFT: 1. DESIGN: 0.
> Changes:
> (1) [SOFT] **STALE-AUDIT-1: Auditing Cloudflare infra WITHOUT checking `workers_list`
>     modified_on timestamps first** — produces findings that can be fully invalidated by
>     remediation that landed minutes earlier. Case: v1 audit (same session) found qnfo-qwav
>     dead (ai:false) and webhook 1101 — but both Workers had been redeployed ~30 min prior
>     (qnfo-paper-indexer 04:28:57Z, qnfo-qwav 04:30:59Z, workers_dev=true). Red-team v2
>     re-verified: qnfo-qwav /health now reports ai:true, vector search returns 0.75-0.90
>     scores on 4/4 queries, webhook returns 200 for real slugs (24 chunks). Fix: ALWAYS
>     call `workers_list` and check modified_on BEFORE trusting any infra-state claim;
>     findings older than the latest deployment are provisional. This complements KIF-61
>     (the 1101 root cause was DNS NXDOMAIN route, NOT missing AI binding — confirmed
>     by red-team v2: 1101 now fires ONLY for non-existent slugs, cosmetic 500-vs-404).
> (2) [SOFT] Duplicate v3.16 entry removed from `.kaizen_history` (Status Auditor).
> Cross-reference: kaizen v1.4.1, session OL00bCz3AJlaz_NjUi4eS (v3.16), KIF-61.

> **v3.16 UPDATE (2026-08-02, kaizen — autonomous P0 remediation session):**
> Red-team: direct parent-agent audit of session OL00bCz3AJlaz_NjUi4eS.
> HARD: 4. SOFT: 2. DESIGN: 1.
> Changes:
> (1) [HARD] **KIF-61: Workers WITHOUT `workers_dev = true` have NO public HTTP route**
>     — webhook/health endpoints return DNS NXDOMAIN (curl exit 1), misread as HTTP 1101.
>     Root cause of the qnfo-paper-indexer webhook failure: NOT a missing AI binding
>     (binding WAS present — `wrangler deploy --dry-run` proved it). Fix: add
>     `workers_dev = true` to wrangler.toml + `wrangler deploy`. Verified live:
>     https://qnfo-paper-indexer.q08.workers.dev and https://qnfo-qwav.q08.workers.dev.
> (2) [HARD] **AI binding format: `[[ai]]` (array of tables), NOT `[ai]` (single table)**
>     — `[ai]` fails config validation with "The field `ai` should be an object but got
>     [{\"binding\":\"AI\"}]". Both qnfo-paper-indexer and qnfo-qwav deployed with `[[ai]]`;
>     qnfo-qwav /health then reported `ai: true` (previously false → D1 LIKE fallback).
> (3) [HARD] **REST bindings endpoint 9106 ≠ token lacks Workers permission** — `GET
>     /accounts/{id}/workers/scripts/{name}/bindings` returned 9106 "Authentication failed
>     (status: 400)" while `wrangler deploy` (same CLOUDFLARE_API_TOKEN) succeeded. The
>     REST bindings sub-endpoint has a different auth requirement; NEVER conclude "token
>     lacks Workers Scripts:Edit" from a single REST 9106 — test `wrangler deploy` directly.
> (4) [HARD] **`wrangler routes list` REMOVED in v4.118.0** — returns "Unknown arguments:
>     routes, list". Route management is via wrangler.toml `workers_dev`/`routes` or API.
> (5) [SOFT] `wrangler pages project list` — canonical Pages discovery (5 projects: qwav,
>     qnfo-hub, ipatent-me, qnfo-publications, ask-qwav). cfpe-dashboard.pages.dev down =
>     project NEVER existed (not a runtime issue).
> (6) [SOFT] ipatent.me chain: 301 (CF proxy OK) → ipatent-v4-0-1-183501038626.us-west1.run.app
>     → 500 (Google Cloud Run backend). NOT a Cloudflare issue — GCP side.
> (7) [DESIGN] Added §Workers.dev Route Enablement protocol (below).
> Cross-reference: qnfo-paper-indexer (created 2026-08-01), qnfo-qwav v2.0-cors-fixed,
> memory "Walking Cat v_p^max", LoS W-S5.

> **v3.15 UPDATE (2026-08-02, kaizen — Workers baseline + paper auto-indexing):**
> Reactive kaizen triggered by session dc5191VzXRICu4vd_cIEo — full paper Vectorize
> reindexing + automation layer deployed.
> Red-team: direct parent-agent 5-adversary audit. HARD: 0. SOFT: 3. DESIGN: 1.
> Changes:
> (1) [SOFT] Workers baseline 8 → 9. Fleet: +`qnfo-paper-indexer` (auto-indexes
>     all 233 paper full-text bodies into `qwav-research-v2` Vectorize; cron every
>     30 min + webhook for real-time; D1 + PAPER_VZ + AI bindings).
> (2) [SOFT] Resource Baselines: Workers Expected 7→9, Warning 8-11→10-11,
>     Critical 10+→12+.
> (3) [SOFT] Cronjob count: +1 "Paper Vectorize Auto-Indexer" (every 4h backup).
>     Scheduler running, 8 enabled jobs.
> (4) [DESIGN] Cross-reference: qnfo-paper-indexer Worker at
>     qnfo-paper-indexer.q08.workers.dev (/health, /count, /index?offset=N,
>     /webhook?slug=XXX, /cron/debug).

> **v3.14 UPDATE (2026-08-01, kaizen — wrangler environment + R2 verification false-negatives):**
> Red-team: direct parent-agent 5-adversary audit of a full session's execution errors
> (wrangler install EPERM, R2 "key does not exist" false negatives, R2 list pagination
> false negative, R2 HEAD 405 misread, stale workers baseline). HARD findings: 4.
> SOFT: 2. DESIGN: 1.
> Changes:
> (1) [HARD] **KIF-19 anti-pattern UPDATED:** Wrangler is NO LONGER "npx-only, never
>     globally installed." As of 2026-08-01 wrangler **4.118.0 IS globally installed**
>     at `C:\Users\LENOVO\npm-global\node_modules\wrangler\bin\wrangler.js` with a
>     persistent PATH entry. The old npx-cached 4.114.0 copy was CORRUPT (truncated
>     download → SyntaxError at cli.js:81194), which is why npx tried to re-fetch and
>     hung. The correct availability test is `wrangler --version` (now on PATH) or
>     `node scripts/wrangler-check.js` (Accuracy Auditor, parent-agent).
> (2) [HARD] Added **§Wrangler Environment Setup (PERMANENT FIX)** — documents the
>     root cause of the EPERM block (npm prefix pointed at admin-only
>     `C:\Program Files\DeepChat\resources\app.asar.unpacked\runtime\node`) and the
>     permanent fix (`npm config set prefix C:\Users\LENOVO\npm-global`, absolute
>     paths in `~/.npmrc` — NEVER `%VAR%` syntax which npm treats literally, plus
>     persistent PATH via setx). Also added the `%VAR%`-literal gotcha: `.npmrc`
>     does NOT expand Windows `%VAR%` — use absolute paths or `${VAR}` (Completeness
>     Auditor, parent-agent).
> (3) [HARD] R2 CLI docs: added **`--remote` MANDATORY note** — wrangler v4 `r2 object`
>     commands default to LOCAL storage; without `--remote` a live object returns
>     `"The specified key does not exist."` (false negative). Every R2 read/verify
>     MUST pass `--remote` (Accuracy Auditor, parent-agent).
> (4) [HARD] R2 REST listing: added **pagination note** — default page size is 20
>     objects; pass `&limit=1000` and follow `cursor` for full listings. The old
>     snippet returned 20 objects and produced a false "resume NOT in bucket"
>     conclusion (Completeness Auditor, parent-agent).
> (5) [SOFT] R2 REST verification: added **HEAD-405 note** — R2 object API does NOT
>     support HEAD (returns 405, misread as "not found"); use GET and compare
>     Content-Length or hash (Accuracy Auditor, parent-agent).
> (6) [SOFT] Workers baseline 7 → **8** — live `workers_list` MCP returned 8 incl.
>     `qnfo-gateway-production` (created 2026-07-31, modified_on 2026-07-31T12:36Z).
>     Baseline row updated; treat any future count ≠ 8 as drift (Status Auditor,
>     parent-agent).
> (7) [DESIGN] Added anti-pattern rows: R2 object GET without `--remote`, R2 REST
>     listing without pagination, R2 HEAD-for-verification, literal `%VAR%` in
>     `.npmrc` (Novelty Auditor, parent-agent).
> Cross-reference: windows-command-patterns v2.2, kaizen v1.2.5, research v2.40,
> memory "Wrangler PERMANENTLY resolved on this machine (2026-08-01)".

> **v3.13 UPDATE (2026-07-31, no-dashboard kaizen):**
> User mandate: NO Cloudflare Dashboard — no web UI, no manual browser login, no
> human intervention for anything that CLI/API can do. Changes:
> (1) [HARD] **KIF-51 FALSE CLAIM RETRACTED:** "API Tokens typically cannot read/modify/
>     delete account-level redirect rulesets" was WRONG. Account-level rulesets ARE
>     manageable via REST API (`GET/DELETE /accounts/{id}/rulesets`). The 2026-07-30
>     incident was a token-permissions issue, not an API limitation.
> (2) [HARD] Updated KIF-51 fix protocol: "manual Cloudflare Dashboard → delete the
>     rule" → "DELETE /accounts/{id}/rulesets/{id}" with `Account:Rulesets:Edit` scope.
> (3) [HARD] Added **KIF-60: Using Cloudflare Dashboard** — HARD BLOCK on all Dashboard
>     operations. All operations MUST be CLI/API/command-line only. Every Dashboard
>     action has an API equivalent.
> (4) [HARD] Updated EXECUTION GATE: "NO DASHBOARD" added to the decision ladder.
> (5) [HARD] Added step 5 (API deletion) to Account-Level Redirect detection protocol.
> Cross-reference: KIF-51, KIF-60, windows-command-patterns v2.0.

> **v3.12 UPDATE (2026-07-31, red-team kaizen — PowerShell gate + MCP-first execution):**
> Red-team review: 5 parallel subagents attempted, all truncated; fell back to direct
> parent-agent 5-adversary audit (Accuracy, Completeness, Dependency, Novelty, Status).
> HARD findings: 4. SOFT findings: 4. DESIGN findings: 2.
> Changes:
> (1) [HARD] **EXECUTION GATE (KIF-59):** Added mandatory HARD GATE at skill top —
>     PowerShell is FORBIDDEN for Cloudflare operations. Decision ladder: MCP tools FIRST,
>     `npx wrangler` SECOND, Python REST API THIRD. PowerShell is NEVER acceptable.
>     Rationale: 15+ documented PowerShell failures (UTF-8 corruption, quote mangling,
>     `curl` alias breakage, `ConvertTo-Json` garbage). This gate prevents the exact
>     incident that triggered this kaizen (Completeness Auditor, parent-agent).
> (2) [HARD] Fixed `execute_plan` step 3: "wrangler CLI, REST API, Dashboard" →
>     "MCP tools FIRST (workers_list, workers_get_worker, query_worker_observability,
>     search_cloudflare_documentation), fallback wrangler CLI" — the old text was the
>     ROOT CAUSE of the PowerShell incident (Accuracy Auditor, parent-agent).
> (3) [HARD] Added anti-pattern KIF-59: "Using PowerShell for ANY Cloudflare operation"
>     — HARD BLOCK with the full decision ladder (Completeness Auditor, parent-agent).
> (4) [HARD] Bumped frontmatter `version: "3.8"` → `"3.12"` — the v3.11 kaizen didn't
>     bump it (Status Auditor, parent-agent).
> (5) [SOFT] Updated stale cross-refs: "research v2.25" → "research v2.38 (confirmed live
>     2026-07-31)" in v3.9 banner (Dependency Auditor, parent-agent).
> (6) [SOFT] Fixed Resource Baselines table: Vectorize Indexes 4→5 to match Vectorize
>     section text (Status/Dependency Auditors, parent-agent).
> (7) [SOFT] Added §MCP Server → Agent Tool Mapping — maps MCP server names to actual
>     agent tool names (workers_list, query_worker_observability, etc.) so agents
>     know exactly which tool to call (Completeness Auditor, parent-agent).
> (8) [SOFT] Added MCP-first preference note to execute_plan comment area (Completeness
>     Auditor, parent-agent).
> (9) [DESIGN] Infrastructure Audit section: added MCP-first preamble (Novelty Auditor,
>     parent-agent).
> (10) [DESIGN] Reusable Scripts section: added MCP-first preference note (Novelty
>     Auditor, parent-agent).
> Cross-reference: kaizen v1.2.3, research v2.38, KIF-59.

> **v3.11 UPDATE (2026-07-30, LoS codification kaizen):**
> Codified formal **Level-of-Service (LoS) standards** across three tiers — Pages (P-S1..P-S5),
> Workers (W-S1..W-S6), and DNS/Domains (D-S1..D-S7) — with severity ratings (CRITICAL/WARNING/INFO),
> test protocols, remediation steps, and verification gates. Created **`scripts/availability-audit.js`**
> (unified LoS auditor running all 18 standards in a single pass) and **`scripts/url-health-check.js`**
> (quick HTTP probe of all 28 known QNFO public URLs). Added canonical standards document at
> `references/level-of-service-standards.md`. See §Level-of-Service Standards below.

> **v3.10 UPDATE (2026-07-30, live-incident red-team kaizen):**
> Full infrastructure audit + live incident response on production QNFO outage.
> **Root cause:** `qnfo-gateway` Worker silently lost D1/R2 bindings during a REST API
> deploy, returning HTTP 500 on all data-dependent routes (papers.qnfo.org, legal.qnfo.org,
> graph-api.qnfo.org, qnfo.org hub). **Fix:** redeployed via `npx wrangler deploy` from a
> properly-configured `wrangler.toml` with all bindings declared. **Impact:** 4 public
> domains down for ~30 minutes. Added 4 new anti-patterns covering:
> 1. **KIF-50: Binding Loss During REST Deploy** — PUT to `/workers/scripts` without
>    metadata silently drops ALL D1/R2/KV bindings. ALWAYS use wrangler deploy.
> 2. **KIF-51: Account-Level Redirect Blocks Pages** — `http_request_redirect` rulesets
>    at account level execute at position 5 in Rules Engine, before Workers (position 10).
>    Custom domains that match a redirect rule will never reach Pages or Workers.
>    **Fix (v3.13):** Account-level rulesets ARE manageable via API — `GET /accounts/{id}/rulesets` to list, `DELETE /accounts/{id}/rulesets/{id}` to delete. The prior "API Tokens can't" claim was a permissions/scope issue, not an API limitation. NEVER use the Dashboard — use the REST API with a properly-scoped token (`Account:Rulesets:Edit`).
> 3. **KIF-52: Empty DNS Zones** — 3 of 12 active zones had 0 DNS records (qnfo.net,
>    qnfo.uk, q-wave.tech). A zone with no records resolves to nothing. Infra audits
>    must flag `dns_records count = 0` as CRITICAL and add CNAME + Worker route.
> 4. **KIF-53: API-Only Workers Under Custom Domains** — `qnfo-ipatent` Worker returns
>    404 for `/` but ipatent.me CNAME pointed at it. Route custom domains to Pages
>    projects that serve HTML; keep Workers as API endpoints only.
> All 4 FINDING-X entries closed. See `tape_handoff binding-loss-2026-07-30`.

> **v3.9 UPDATE (2026-07-29, MCP-Driven Operations red-team + kaizen):**
> Red-team audit of all skills/settings against the 17-MCP server fleet identified 7
> integration gaps: skills referenced Cloudflare MCP servers in their documentation but
> gave zero operational guidance on WHEN and HOW to use specific MCP servers during
> research, infrastructure, and operations workflows. This update adds:
> 1. **MCP-Driven Operations section** (new, below) — a decision matrix mapping every
>    common Cloudflare operation to its preferred MCP server(s), ensuring agents reach
>    for `cloudflare-observability` not `curl` for Worker health checks, `cloudflare-graphql`
>    not raw REST for cross-product analytics, and `cloudflare-auditlogs` not `wrangler`
>    for deployment audit trails.
> 2. **Updated Infrastructure Audit** to use `cloudflare-observability` (per-Worker
>    metrics), `cloudflare-graphql` (cross-product analytics), `cloudflare-auditlogs`
>    (compliance verification), and `dns-analytics` (zone query volumes) as first-class
>    audit tools — not as an afterthought.
> 3. **Updated Retrieval Sources** with `cloudflare-docs` MCP and `cloudflare-blog` MCP
>    as preferred doc search channels.
> 4. **New anti-patterns** for reaching for raw CLI/REST when an MCP server exists.
> Companion kaizen updates: research skill v2.38 (Phases 1,6,7,8 MCP integration, confirmed live 2026-07-31),
>    code skill v2.2 (MCP server deploy/verify workflow), knowledge skill v2.2
>    (AutoRAG + AI Gateway references). See `tape_handoff mcp-driven-operations-2026-07-29`
>    for full audit findings and skill delta map.

> **v3.8 UPDATE (2026-07-29, 17-MCP coverage — FULL COVERAGE):**
> Configured all 7 remaining Cloudflare MCP servers: `cloudflare-browser-mcp-server` (browser automation),
> `dns-analytics` (DNS analytics), `containers-mcp` (Docker containers on edge),
> `cloudflare-casb-mcp-server` (SaaS security), `cloudflare-autorag-mcp-server` (AutoRAG),
> `cloudflare-blog` (blog search, public), `dex-analysis` (Digital Experience).
> All 7 endpoints verified live (6× 401 OAuth, 1× 405 blog — all reachable).
> Full infrastructure audit re-verified: 7/7 Workers healthy, D1 papers=918, KG paper:*=902 (delta=16, 98.3%).
> Config: 17/17 Cloudflare MCP servers (100% coverage), 35 total MCP servers, 13,519 bytes. KIF-48 CLOSED.
> Backup created: `mcp-settings.json.bak-2026-07-29-v2`.

> **v3.7 UPDATE (2026-07-29, 10-MCP coverage + infra audit):**
> Added `cloudflare-logpush` (10th MCP server, 59% coverage). Full infrastructure
> audit confirmed: 7/7 Workers healthy, lifecycle/status=200 (I-02 FIXED),
> archive/health=200 (I-03 FIXED), D1 papers=918, KG paper:*=902 (delta=16,
> 98.3% coverage — down from prior 610 gap). Backup file created
> (`mcp-settings.json.bak-2026-07-29`, 10,985 bytes). Config red-team: zero
> drift, JSON valid. See `qnfo-agent` KIF-48 (MCP coverage mandate).
>
> **v3.6 UPDATE (2026-07-29, 9-MCP coverage + red-team audit):**
> DeepChat now connects to 9 Cloudflare MCP servers (up from 5), covering
> 53% of the available Cloudflare MCP ecosystem. Added AI Gateway
> (`cloudflare-ai-gateway`, log search + prompt inspection), GraphQL
> Analytics (`cloudflare-graphql`, cross-product analytics), Audit Logs
> (`cloudflare-auditlogs`, compliance trail), and Radar
> (`cloudflare-radar`, internet insights — public, read-only). All
> endpoints DNS-verified (104.18.24.159/25.159) and return HTTP 401
> (OAuth, consistent with existing servers). Config red-team: zero
> drift in 23 existing entries, 4/4 new entries validated, backup at
> `mcp-settings.json.bak-2026-07-29`. Full MCP endpoint reference table
> added below (§DeepChat MCP Server Coverage). See `qnfo-agent`
> KIF-48 (MCP coverage mandate).

> **v3.5 UPDATE (2026-07-25, wrangler false-negative + structured-schema kaizen):**
> Root-caused a live "wrangler is not installed" claim in this session's own
> reasoning output — direct re-verification via `npx wrangler --version` +
> `npx wrangler whoami` (executed via `exec`, same turn) both succeeded
> (account `quniverse`, token valid). The false claim traced to checking the
> WRONG signal (`npm ls -g wrangler` / bare PATH lookup / subprocess PATH
> loss) instead of the only sufficient test (`npx wrangler <cmd>` directly).
> Added canonical **`scripts/wrangler-check.js`** probe — run this instead of
> re-deriving an availability check ad hoc. Also added
> **`references/d1-rest-api-schema.json`** (D1 REST schema + FTS5/upsert
> gotchas) and **`references/workers-deploy-metadata-schema.json`** (Worker
> multipart deploy schema + binding shapes + the CRLF-boundary code-corruption
> bug), plus **`scripts/d1-safe-write.js`** (Node-native CHECK-THEN-WRITE
> helper that avoids the PowerShell `ConvertTo-Json` large-payload corruption
> bug and always re-verifies via length comparison). See `qnfo-agent`
> KIF-19/20/21.

> **v3.3 UPDATE (2026-07-21, phantom-claim audit):** Added the **Tool-Call
> Execution Mandate** section below (immediately after `execute_plan`).
> Every "deployed"/"fixed"/"live"/"healthy" claim in this domain now
> requires an independently re-queried live-state tool result in the same
> turn — a `"success": true` API response or a Dashboard-style assumption
> is NOT sufficient evidence.

> **v3.4 UPDATE (2026-07-21, orphan-script audit):** Deleted
> `scripts/filebase-upload.js` — a stale SigV4 helper for the Filebase
> pinning service that the v3.2 deprecation banner below already declared
> removed, but the script file itself survived that commit untouched,
> creating a live contradiction between this skill's text (Filebase
> deprecated) and its shipped scripts (a working Filebase uploader still
> present). Filebase/Pinata/Lighthouse/Arweave remain fully out of scope;
> the v3.1 banner immediately below is retained ONLY as historical record
> of why the (now-deleted) script once existed — do not resurrect it.

> **v3.1 UPDATE (2026-07-20, Pinata quota exceeded) — SUPERSEDED, script DELETED v3.4:**
> Removed Pinata from the R2→IPFS Bridge. Filebase (free 5GB S3-compatible,
> no request-volume limit, auto-pins on write) was made PRIMARY pinner;
> Lighthouse (free Filecoin tier) was SECONDARY. `scripts/filebase-upload.js`
> and the `research` skill's `scripts/filebase-pin.js` implemented this —
> BOTH are deprecated per the v3.2 banner below and the script has now
> been physically deleted (v3.4). Do not add `PINATA_API_KEY`/
> `PINATA_API_SECRET`/`FILEBASE_ACCESS_KEY`/`FILEBASE_SECRET_KEY` back to
> any Worker env or wrangler secret.

> **v3.2 UPDATE (2026-07-20, red-team audit):** Deprecated "R2→IPFS Bridge"
> section, Filebase S3 SigV4 upload script, and all external pinning service
> references. Core stack: Cloudflare R2 (canonical durable host) + D1 (records)
> + Workers (serving) + DNS (DNSLink for optional IPFS resolution). No external
> pinning services (Filebase, Lighthouse, Arweave) are required or referenced.
> Fixed wrangler r2 CLI syntax docs (`{bucket}/{key}` single arg, no `list`
> subcommand in v4), Workers routes API endpoint (zone-level, not account-level).


> **Merges 18:** cloudflare + cloudflare-deployer + cloudflare-one + cloudflare-email-service + email + infrastructure-audit + web-perf + workers-best-practices + wrangler + cloudflare-mcp-servers + logpush (v3.7) + browser-mcp + dns-analytics + containers-mcp + casb-mcp + autorag-mcp + blog-mcp + dex-mcp (v3.8)
> **Added v3.0:** Worker Consolidation Pattern, R2→IPFS Bridge, DNSLink Deployment, 4-D Architecture
> **Related:** Always load with `qnfo-agent` for production immutability gates + due diligence. Load `research` for 4-D distribution pipeline.
> **Full-Stack Mandate:** Evaluate Workers, D1, R2, KV, DO, AI, Vectorize, Queues, Pages, DNS, Zero Trust, Email, WAF, CDN as ONE integrated platform. NEVER isolate components.

---

## EXECUTION GATE — MANDATORY, READ FIRST (v3.12, KIF-59)

**HARD GATE: PowerShell is FORBIDDEN for Cloudflare operations. Period. No exceptions.**

Use this decision ladder for EVERY Cloudflare operation:

| Priority | Tool | When |
|:---------|:-----|:-----|
| **1st** | Cloudflare MCP tools (`workers_list`, `workers_get_worker`, `query_worker_observability`, `search_cloudflare_documentation`, etc.) | ALWAYS — these are auto-authenticated, structured, and cannot corrupt data |
| **2nd** | `npx wrangler <cmd>` (via `exec`, NOT via PowerShell) | When MCP tools don't cover the specific operation |
| **3rd** | Cloudflare REST API (Python `urllib.request` with `CLOUDFLARE_API_TOKEN` env var) | For D1 queries / R2 listings when wrangler hangs |
| **NEVER** | PowerShell, `curl` (PowerShell alias), Cloudflare Dashboard (web UI), `Invoke-WebRequest`, `ConvertTo-Json` | PowerShell corrupts UTF-8; the Dashboard requires manual browser login and human interaction — ALL Cloudflare operations MUST be CLI/API/command-line only. Every Dashboard action has an API equivalent. See KIF-60. |

**Why this gate exists:** PowerShell has caused 15+ documented tool-call failures in QNFO sessions (KIF-21, KIF-27, KIF-37, KIF-59) through: UTF-8 double-encoding (mojibake), inline `python -c` quote collisions, `curl` → `Invoke-WebRequest` alias breakage, `ConvertTo-Json` corruption of large D1 payloads, and `&&` chaining not supported. Every PowerShell invocation for Cloudflare is a trapped error waiting to happen. Use MCP tools, `npx wrangler`, or Python scripts — never PowerShell.

## execute_plan

update_plan([
  {"step": "Identify service via decision trees below", "status": "pending"},
  {"step": "Check full-stack cross-service implications", "status": "pending"},
  {"step": "Execute with MCP tools FIRST (workers_list, workers_get_worker, query_worker_observability, search_cloudflare_documentation), fallback wrangler CLI", "status": "pending"},
  {"step": "Verify deployment health + DNS integrity + lifecycle state", "status": "pending"},
  {"step": "Audit: check for orphans, 522-RISK, CNAME chains, resource drift", "status": "pending"},
  {"step": "Core Distribution Gate: Verify GitHub, Zenodo, R2, D1/KG layers", "status": "pending"},
  {"step": "LoS Availability Audit: run availability-audit.js or url-health-check.js", "status": "pending"},
])

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — MANDATORY)

No claim that a Worker is "deployed", a DNS record is "live", a D1 write
"succeeded", an R2 object "exists", or an infrastructure issue is "fixed"
may appear in a response without an actually-invoked tool call in the SAME
turn whose output is shown. Future-tense or narrative-only claims
("this should now route correctly", "the deploy will fix it") are PHANTOM
CLAIMS per `qnfo-agent` §9.11 Rule 14 — BLOCKED.

**Domain-specific verification (pick the ones relevant to the claim):**
1. **Worker deploy** — `npx wrangler deployments list --name <worker>` shows the new deployment, AND `curl -sI https://<worker>.<subdomain>.workers.dev/` (or the production route) returns the expected status. A `200 OK` from the deploy API response body alone is NOT verification.
2. **D1 write** — re-run a `SELECT` against the exact row/table just written; do not trust the `"success": true` wrapper on the `INSERT`/`UPDATE` response.
3. **R2 object** — `npx wrangler r2 object get <bucket>/<key> --remote` round-trip after every `put`; compare byte length or hash to the source file.
4. **DNS record** — `GET /zones/{id}/dns_records` (or `dig`) after any create/update; confirm the record resolves as intended, not just that the API accepted the write.
5. **Health/status endpoints** — actually call the endpoint (`curl`/`fetch`) and show the HTTP status + body; do not infer health from deploy success alone.
6. **Data-dependent routes after deploy (KIF-50 Gate — MANDATORY)** — after ANY Worker deploy (even via wrangler), probe at least TWO distinct data-dependent routes (e.g., `/papers`, `/stats`, `/legal`) and confirm they return HTTP 200 with non-trivial body content. A passing `/health` endpoint is INSUFFICIENT evidence of binding health — `/health` typically doesn't touch D1/R2 bindings. A 500 with `"Cannot read properties of undefined (reading 'prepare')"` means a D1 binding is missing. If any data route fails this check, redeploy with correct bindings before claiming "deployed."
7. If verification cannot be run in this turn, the response MUST read `[NOT-VERIFIED: <reason>]` — never "deployed", "fixed", "healthy", or "confirmed".

---

## DeepChat MCP Server Coverage (v3.8 — 17 of 17 available)

DeepChat connects to Cloudflare MCP servers via `npx mcp-remote` (stdio → hosted Streamable HTTP). All servers expose `/mcp` and `/sse` (compatibility alias) through MCP SDK v2 factories. OAuth triggers automatically on first use.

### Configured (17/17 — 100% coverage)

| # | MCP Server ID | Endpoint | Auth | Purpose |
|:--|:--------------|:---------|:----:|:--------|
| 1 | `cloudflare` | `mcp.cloudflare.com/mcp` | OAuth | Full-stack Workers, Pages, R2, D1, KV, Queues, AI, DNS |
| 2 | `cloudflare-docs` | `docs.mcp.cloudflare.com/mcp` | None | Documentation search (autoApprove: all) |
| 3 | `cloudflare-bindings` | `bindings.mcp.cloudflare.com/mcp` | OAuth | Workers bindings, wrangler.toml configs |
| 4 | `cloudflare-builds` | `builds.mcp.cloudflare.com/mcp` | OAuth | Pages + Workers CI/CD, build logs |
| 5 | `cloudflare-observability` | `observability.mcp.cloudflare.com/mcp` | OAuth | Workers logs, metrics, invocation tracing |
| 6 | `cloudflare-ai-gateway` | `ai-gateway.mcp.cloudflare.com/mcp` | OAuth | AI Gateway log search, prompt/response inspection |
| 7 | `cloudflare-graphql` | `graphql.mcp.cloudflare.com/mcp` | OAuth | Cross-product GraphQL Analytics API |
| 8 | `cloudflare-auditlogs` | `auditlogs.mcp.cloudflare.com/mcp` | OAuth | Account audit trail, compliance reports |
| 9 | `cloudflare-radar` | `radar.mcp.cloudflare.com/mcp` | None | Internet insights, BGP, traffic trends (autoApprove: all) |
| 10 | `cloudflare-logpush` | `logs.mcp.cloudflare.com/mcp` | OAuth | Workers log export, logpush job management |
| 11 | `cloudflare-browser-mcp-server` | `browser.mcp.cloudflare.com/mcp` | OAuth | Headless browser automation, screenshots, PDF generation |
| 12 | `dns-analytics` | `dns-analytics.mcp.cloudflare.com/mcp` | OAuth | DNS query analytics, query volumes, top domain queries |
| 13 | `containers-mcp` | `containers.mcp.cloudflare.com/mcp` | OAuth | Deploy & manage Docker containers on Cloudflare edge |
| 14 | `cloudflare-casb-mcp-server` | `casb.mcp.cloudflare.com/mcp` | OAuth | CASB — Cloud Access Security Broker, SaaS security audits |
| 15 | `cloudflare-autorag-mcp-server` | `autorag.mcp.cloudflare.com/mcp` | OAuth | AutoRAG — Automated RAG with Workers AI + Vectorize |
| 16 | `cloudflare-blog` | `blog.mcp.cloudflare.com/mcp` | None | Search blog.cloudflare.com posts (public, no auth) |
| 17 | `dex-analysis` | `dex.mcp.cloudflare.com/mcp` | OAuth | Digital Experience monitoring, network performance analysis |

### Coverage Complete — 17/17 (100%)

All 17 available Cloudflare MCP servers are now configured. No servers remain to add.

### MCP Verification Gate

Before claiming "MCP server X is working", verify with:
```bash
# All endpoints should return HTTP 401 (OAuth required) or HTTP 200 (public)
curl.exe -s -o NUL -w "%{http_code}" https://<subdomain>.mcp.cloudflare.com/mcp
```
- **401** = endpoint live, auth required (normal for OAuth servers)
- **404/530** = endpoint not deployed or DNS not propagated
- **200** = public endpoint (docs, radar)

### MCP OAuth Loopback Fix (v3.19 — MANDATORY protocol)

**When an MCP server OAuth flow fails with ZodError (`code`/`scope` undefined) after consent
was granted, the problem is the LOOPBACK callback, not the consent.** The browser consented,
Cloudflare redirected to `http://localhost:<port>/oauth/callback`, but no listener was up at
callback time → the authorization code expired before exchange → the client reports a parse
error. Confirmed live 2026-08-02 on `observability.mcp.cloudflare.com/mcp`.

**User mandate (HARD): NEVER open the external/default browser repeatedly for OAuth.**
Do NOT use the default browser for consent. One session-browser attempt max; if the flow
can't complete, STOP and report the blocker.

**Autonomous fix protocol (no default browser):**

1. **Recover OAuth state** from the mcp-remote cache (`~/.mcp-auth/mcp-remote-<ver>/`):
   - `<hash>_client_info.json` → `client_id`, `redirect_uris[0]` (e.g. `http://localhost:22875/oauth/callback`)
   - `<hash>_code_verifier.txt` → PKCE verifier
   - `<hash>` = MD5 of the MCP server URL (e.g. `https://observability.mcp.cloudflare.com/mcp`)
2. **Fetch discovery doc** (RFC 8414): `GET https://<server>/.well-known/oauth-authorization-server`
   → `token_endpoint`, `authorization_endpoint`. Cloudflare's observability server:
   `https://observability.mcp.cloudflare.com/token`.
3. **Start a local listener** on the registered redirect port (`oauth_listener.py` pattern)
   with **AUTO-EXCHANGE inside the listener process** — the code exchange MUST happen in the
   same process as the callback (zero latency). A separate tool-call exchange ALWAYS fails:
   codes expire in <60s (`invalid_grant: Grant not found or authorization code expired`).
4. **Open the auth URL ONCE in the SESSION browser (YoBrowser/CDP)**. If the session browser
   is not logged into Cloudflare (redirects to `dash.cloudflare.com/login`), do NOT loop —
   STOP and report: consent requires a logged-in browser session.
5. **Cache the token** to `<hash>_token.json` in the same mcp-remote dir (format:
   `{access_token, token_type, expires_in, scope, refresh_token}`). Verify with
   `POST /mcp` `initialize` → HTTP 200 (`serverInfo.name`, `version`).
6. **Agent-level MCP tools may still time out** until the host app re-initializes the MCP
   connection — that is an app-level reconnect, not an OAuth problem.

**Failure modes (both confirmed live 2026-08-02):**
- **Expired code**: manual exchange in a separate tool call → `invalid_grant`. Fix: auto-exchange in listener.
- **Session browser not logged in**: YoBrowser lacks the Cloudflare session → login redirect.
  Fix: stop and report; never spawn the default browser.

---

## Worker Consolidation Pattern (MANDATORY)

### Rule
Workers sharing the same D1/R2 bindings MUST be consolidated into a single unified gateway Worker. Queue/cron Workers stay separate (they require dedicated bindings).

### Consolidation Decision Matrix
| Worker Type | Consolidatable? | Reason |
|:------------|:---------------|:-------|
| HTTP API (same bindings) | **Yes** | Routes merge into gateway, domains point to same Worker |
| Queue consumer | **No** | Requires queue binding — dedicated Worker per queue |
| Cron trigger | **No** | Requires cron binding — dedicated Worker per schedule |
| MCP protocol | **Maybe** | If D1/R2 overlap with gateway, merge; else separate |
| AI/LLM inference | **Maybe** | If Workers AI binding shared, merge; else separate |

### Consolidation Workflow
1. Audit all Workers: list bindings, routes, domains
2. Identify sharing groups (same D1/R2 bindings)
3. Merge HTTP routes into gateway Worker
4. Add all D1 bindings to gateway metadata
5. Deploy consolidated gateway
6. Migrate domains from old Workers → gateway
7. Delete old Workers
8. Verify all routes respond

### Example: 2026-07-18 Consolidation (9→7)
```
qnfo-api     ─┐
graph-api    ─┼──► qnfo-gateway v2.0 (17 routes, 7 domains)
qnfo-legal   ─┘
```

---

## Reusable Scripts (Copy-Paste into any execution context)

### Wrangler Environment Setup (PERMANENT FIX — v3.14)

**Root cause of the 2026-08-01 EPERM block:** npm's `prefix` pointed at
`C:\Program Files\DeepChat\resources\app.asar.unpacked\runtime\node` — an
admin-only directory. Any `npm install -g <pkg>` failed with
`EPERM: operation not permitted, mkdir`. The npx-cached wrangler 4.114.0 was
ALSO corrupt (truncated download → `SyntaxError` at cli.js:81194), so npx tried
to re-fetch 4.118.0 fresh and hung on network.

**Permanent fix (already applied 2026-08-01 — verify before assuming):**
```bash
# 1. Redirect npm prefix + cache to USER-writable dirs (absolute paths!):
npm config set prefix "C:\Users\LENOVO\npm-global"
npm config set cache  "C:\Users\LENOVO\AppData\Local\npm-cache"
#    → writes ~/.npmrc. NEVER use %VAR% syntax — npm treats it as a LITERAL
#      directory name (created a stray "%USERPROFILE%" folder in cwd once).
# 2. Install wrangler to the user prefix (no admin needed):
npm install -g wrangler
# 3. Persist PATH (registry HKCU\Environment via setx):
setx Path "%Path%;C:\Users\LENOVO\npm-global"
# 4. Verify:
wrangler --version            # → 4.118.0
wrangler whoami               # → account quniverse (edb167b78c9fb901ea5bca3ce58ccc4b)
```
Invocation paths (all equivalent):
- `wrangler <cmd>` — PATH-registered shim at `C:\Users\LENOVO\npm-global\wrangler.cmd`
- `node C:\Users\LENOVO\npm-global\node_modules\wrangler\bin\wrangler.js <cmd>` — explicit

**Availability test (never trust `npm ls -g` or `where` alone):** run
`wrangler --version` directly. If not found, check BOTH `C:\Users\LENOVO\npm-global`
(global v4.118.0) AND `%LOCALAPPDATA%\npm-cache\_npx\*\node_modules\wrangler`
(npx-cached — delete and re-install if corrupt).

### Workers.dev Route Enablement (KIF-61 — v3.16)

**A Worker without `workers_dev = true` in its wrangler.toml has NO public HTTP
route.** Its `.workers.dev` URL returns DNS NXDOMAIN (curl exit code 1), and any
webhook/health probe misreads this as a binding failure or HTTP 1101. Cron-only
Workers are reachable ONLY through their `scheduled` handler — never via HTTP.

**Diagnosis order for a "webhook 1101" / "worker unreachable" report:**
1. `curl -s https://<worker>.q08.workers.dev/health` — if exit code 1 (NXDOMAIN),
   the Worker has no workers.dev route. This is a CONFIG gap, not a binding gap.
2. `wrangler deploy --dry-run` (from a dir containing the worker JS) — prints the
   LIVE binding set. If `env.AI`/`env.PAPER_VZ`/`env.LIVING_PAPER` are listed, the
   bindings are NOT the problem. (2026-08-02: this proved qnfo-paper-indexer's AI
   binding was present all along.)
3. Fix: add `workers_dev = true` to wrangler.toml, `wrangler deploy`.

**Canonical minimal wrangler.toml (both QNFO index/search Workers):**
```toml
name = "<worker-name>"
main = "<worker-name>.js"
compatibility_date = "2026-08-01"
workers_dev = true

[[d1_databases]]
binding = "LIVING_PAPER"
database_name = "living-paper"
database_id = "70a58cb3-b2cd-498d-877f-ecca86859a22"

[[vectorize]]
binding = "PAPER_VZ"      # or QWAV_VZ for qnfo-qwav
index_name = "qwav-research-v2"

[[ai]]
binding = "AI"            # ARRAY form [[ai]] — NOT [ai] single-table
```

**AI binding format (v3.16):** use `[[ai]]` (array of tables). `[ai]` (single table)
fails with `The field "ai" should be an object but got [{"binding":"AI"}]`.
Verify materialization via `/health` — qnfo-qwav reports `ai: true` only after the
`[[ai]]` deploy (previously `ai: false` → D1 LIKE fallback).

**Known live workers.dev URLs (verified 2026-08-02):**
- `https://qnfo-paper-indexer.q08.workers.dev` — /health, /count, /index?offset=N,
  /webhook?slug=XXX, /cron/debug (cron: every 30 min, 233 papers, 0 errors)
- `https://qnfo-qwav.q08.workers.dev` — /health (ai: true), /ask, /ai/ask, /ai/search

### R2 CLI Syntax (wrangler v4+)
**CRITICAL:** wrangler v4 uses `{bucket}/{key}` as a single positional argument AND
**defaults to LOCAL storage** — for live objects you MUST pass `--remote`:
```bash
# CORRECT (v4+):
npx wrangler r2 object get qnfo-releases/path/to/file.md --remote --pipe
npx wrangler r2 object put qnfo-releases/path/to/file.md --file=local.md --remote

# WRONG (v3 and earlier, removed in v4):
npx wrangler r2 object get qnfo-releases "path/to/file.md" --remote --pipe  # FAILS

# FALSE NEGATIVE (v4.118.0 — do NOT do this):
npx wrangler r2 object get qnfo-releases/path/to/file.md --pipe   # WITHOUT --remote
#   → "The specified key does not exist." even though the object EXISTS.
#   Default is LOCAL simulation storage. ALWAYS pass --remote for live reads.
```
The `r2 object list` subcommand was removed in wrangler v4. Use the REST API for
listings — **and paginate** (default page size is 20 objects!):
```bash
# First page (20 objects — may be a FALSE "empty" if the target is beyond page 1):
curl -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/r2/buckets/{BUCKET}/objects?prefix={PREFIX}&limit=1000"
# Follow result.cursor for the next page until absent.
```
**R2 object verification — use GET, not HEAD:** the R2 object API does NOT
support HEAD (returns HTTP 405, which was misread as "not found" in a session).
Use GET and compare `Content-Length` (or MD5 of body) to the local source.



### Worker Deployment (via REST API)
```js
// _deploy_worker.js — Deploy/update a Cloudflare Worker
const T = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT = '...'; // Cloudflare account ID
const WORKER = 'worker-name';

(async () => {
  const form = new FormData();
  form.append('worker.js', new Blob([workerCode], { type: 'application/javascript+module' }), 'worker.js');
  form.append('metadata', JSON.stringify({
    main_module: 'worker.js',
    bindings: [
      { type: 'r2_bucket', name: 'MY_BUCKET', bucket_name: 'bucket-name' },
      { type: 'd1', name: 'MY_DB', database_id: 'database-uuid' }
    ]
  }));
  const r = await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/workers/scripts/' + WORKER, {
    method: 'PUT', headers: { 'Authorization': 'Bearer ' + T }, body: form
  });
  const d = await r.json();
  console.log('Deploy:', d.success ? 'OK' : 'FAIL: ' + (d.errors ? d.errors.map(e=>e.message).join(', ') : ''));
})();
```

### R2 Object Upload Script
```js
// _r2_upload.js — Upload any file to R2 bucket
const T = process.env.CLOUDFLARE_API_TOKEN;
await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/r2/buckets/' + BUCKET + '/objects/' + encodeURIComponent(KEY), {
  method: 'PUT', headers: { 'Authorization': 'Bearer ' + T }, body: content
});
// Alt: npx wrangler r2 object put {BUCKET}/{KEY} --file path --remote
```

### D1 Query Script (CANONICAL — KIF-36, v3.2, 2026-07-27)

**NEVER hardcode account IDs or database UUIDs in scripts.** Use the canonical
auto-discovery script `scripts/d1-query.py` which discovers credentials,
account ID, and database UUID from live infrastructure:

```bash
# Query by database NAME (never by UUID)
python scripts/d1-query.py --db living-paper --sql "SELECT slug, doi FROM papers WHERE slug=?" --params zbw-p5-capstone

# Force re-discovery (bypass session cache)
python scripts/d1-query.py --refresh --db qnfo-graph --sql "SELECT COUNT(*) FROM nodes"

# Raw JSON output for programmatic use
python scripts/d1-query.py --db living-paper --sql "SELECT * FROM papers LIMIT 5" --raw
```

**Token discovery** (automatic, in order): env var → `~/.cloudflare_token` → `~/keys.json` → Win32 API.
**Account ID discovery**: `npx wrangler whoami` → cache.
**DB UUID discovery**: `npx wrangler d1 list` → cache by name.

Cache file: `%USERPROFILE%\.deepchat\d1-cache.json` (session-scoped, regenerated on `--refresh`).

**DEPRECATED (pre-KIF-36):**
```js
// DO NOT USE — hardcoded ACCOUNT + DB constants cause silent 401s
const T = process.env.CLOUDFLARE_API_TOKEN;
await fetch('...accounts/' + ACCOUNT + '/d1/database/' + DB + '/query', ...);
```

### DNSLink Creation Script
```js
// _dnslink_create.js — Map domain to IPFS CID
await fetch('https://api.cloudflare.com/client/v4/zones/' + ZONE + '/dns_records', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + process.env.CLOUDFLARE_API_TOKEN, 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'TXT', name: '_dnslink.' + SUB, content: 'dnslink=/ipfs/' + CID, ttl: 1 })
});
```

### Worker Routes API (zone-level, NOT account-level)

**FIXED (v3.2):** Workers routes for custom domains use the **zone-level** API endpoint,
not the account-level endpoint. The old docs incorrectly referenced `/accounts/{id}/workers/routes`.

```js
// CORRECT: zone-level routes endpoint
GET  https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/workers/routes  // List routes
POST https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/workers/routes  // Create route
// WRONG: account-level endpoint returns "Could not route to .../workers/routes"
```

### Worker Route Creation Script
```js
// _worker_route.js — Route domain to Worker
await fetch('https://api.cloudflare.com/client/v4/zones/' + ZONE + '/workers/routes', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + process.env.CLOUDFLARE_API_TOKEN, 'Content-Type': 'application/json' },
  body: JSON.stringify({ pattern: DOMAIN + '/*', script: WORKER })
});
```

### R2 Hygiene Check
```js
// _r2_hygiene.js — Check for qnfo/qnfo/ double-prefix
const r = await fetch('https://api.cloudflare.com/client/v4/accounts/' + A + '/r2/buckets/qnfo/objects?prefix=qnfo/&limit=5', {
  headers: { 'Authorization': 'Bearer ' + T }
});
const d = await r.json();
const bad = (d.result?.objects||[]).filter(o => o.key.startsWith('qnfo/'));
if (bad.length > 0) bad.forEach(o => console.log('FIX: ' + o.key));
```



### "I need to run code"
```
Serverless functions at edge -> Workers
Full-stack web app with Git -> Pages
Stateful coordination/real-time -> Durable Objects
Long-running multi-step jobs -> Workflows
Run Docker containers -> Containers
Multi-tenant platform -> Workers for Platforms
Scheduled tasks (cron) -> Cron Triggers
Lightweight edge logic -> Snippets
Process Worker execution events -> Tail Workers
Optimize latency to backend -> Smart Placement
```

### "I need to store data"
```
Key-value (config/sessions/cache) -> KV
Relational SQL -> D1 (SQLite) or Hyperdrive (existing Postgres/MySQL)
Object/file storage (S3-compatible) -> R2
Versioned file trees -> Artifacts
Message queue (async processing) -> Queues
Vector embeddings (AI/semantic search) -> Vectorize
Strongly-consistent per-entity state -> Durable Objects (DO Storage)
Secrets management -> Secrets Store
Streaming ETL to R2 -> Pipelines
Managed Apache Iceberg catalog on R2 -> R2 Data Catalog
Serverless SQL analytics over Iceberg -> R2 SQL
Persistent cache -> Cache Reserve
```

### "I need AI/ML"
```
Run inference (LLMs/embeddings/images) -> Workers AI
Vector database for RAG/search -> Vectorize
Build stateful AI agents -> Agents SDK
Gateway for any AI provider -> AI Gateway
AI-powered search widget -> AI Search
Browser automation/screenshots -> Browser Rendering
```

### "I need networking"
```
Expose local service to internet -> Tunnel (cloudflared)
TCP/UDP proxy (non-HTTP) -> Spectrum
WebRTC TURN server -> TURN
Private network connectivity -> Network Interconnect
Optimize routing -> Argo Smart Routing
Workers private network -> Workers VPC
Real-time video/audio -> RealtimeKit or Realtime SFU
```

### "I need security"
```
Web Application Firewall -> WAF
DDoS protection -> DDoS
Bot detection/management -> Bot Management
API protection -> API Shield
CAPTCHA alternative -> Turnstile
Credential leak detection -> WAF Managed Ruleset
```

### "I need media/content"
```
Image optimization/transformation -> Images
Video streaming/encoding -> Stream
Third-party script management -> Zaraz
```

### "I need analytics/data"
```
Query across all Cloudflare products -> GraphQL Analytics API
Custom high-cardinality metrics -> Analytics Engine
Client-side (RUM) performance data -> Web Analytics
Workers Logs and real-time debugging -> Observability
SQL over Iceberg data lake -> R2 SQL (+ Pipelines + R2 Data Catalog)
Raw logs (Logpush to external) -> Cloudflare docs
```

### "I need infrastructure-as-code"
```
Pulumi -> Pulumi provider
Terraform -> Terraform provider
REST API -> Cloudflare API
```

---

## DNSLink Deployment

### Pattern
Every QNFO publication subdomain gets a DNSLink TXT record:
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -d '{"type":"TXT","name":"_dnslink.{subdomain}","content":"dnslink=/ipfs/{CID}","ttl":1}'
```

### Verification (script/policy consistency)
- [ ] No skill script implements a service the SKILL.md text declares deprecated (orphan-script check — v3.4 caught `filebase-upload.js`)
- [ ] `git log --oneline -- <script>` reviewed for any script older than the SKILL.md's last deprecation banner before trusting it as current

## Verification
- `https://dweb.link/ipns/{subdomain}.qnfo.org` → serves content from IPFS
  (RED-TEAM FIX 2026-07-20: `cloudflare-ipfs.com` and `cf-ipfs.com` no
  longer resolve via DNS at all — confirmed by direct probe, ENODATA.
  Cloudflare decommissioned its public IPFS gateway. `dweb.link` supports
  both `/ipfs/` and `/ipns/` paths and was verified live.)
- `nslookup -type=TXT _dnslink.{subdomain}.qnfo.org` → returns `dnslink=/ipfs/{CID}`

---

## Cloudflare One (Zero Trust & SASE)

### Product Suite
- **Access:** Zero Trust application access. Replace VPN with identity-aware proxy.
- **Gateway:** DNS filtering, HTTP filtering, SWG (Secure Web Gateway)
- **WARP:** Device client that routes traffic through Cloudflare network
- **Tunnel:** `cloudflared` -- expose local services to Cloudflare edge without public IPs
- **DLP:** Data Loss Prevention -- scan data in transit for sensitive content
- **CASB:** Cloud Access Security Broker -- API-based SaaS security
- **Device Posture:** Check device health before granting access
- **Browser Isolation:** Remote browser session for risky sites

### Migrations (from Zscaler, VPN, etc.)
1. Deploy WARP client to endpoints
2. Configure Gateway DNS + HTTP policies equivalent to legacy
3. Set up Tunnel for internal applications (replacing VPN)
4. Migrate access policies to Access
5. Phase out legacy infrastructure

---

## Email (Workers Binding + Email Routing)

### Sending Email (Workers Binding)
```javascript
// wrangler.jsonc
{
  "send_email": [{
    "name": "SEND_EMAIL",
    "destination_address": "me@example.com"
  }]
}

// In Worker
await env.SEND_EMAIL.send(
  new EmailMessage(
    "from@example.com",
    "to@example.com",
    "Subject line",
    "Plain text body",
    "<p>HTML body</p>"
  )
);
```

### Email Routing (Inbound Processing)
```jsonc
// wrangler.jsonc
{
  "email_routing": [{
    "name": "INBOUND",
    "destination_address": "catchall@example.com"
  }]
}

// In Worker -- handle incoming emails
export default {
  async email(message, env, ctx) {
    const { to, from, subject, raw } = message;
    await message.forward("forwarded@example.com");
  }
};
```

### SPF/DKIM/DMARC Setup
```
SPF:  TXT @ "v=spf1 include:_spf.mx.cloudflare.net ~all"
DKIM: CNAME <selector>._domainkey <selector>._domainkey.<zone>.onmicrosoft.com
DMARC: TXT _dmarc "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

---

## Level-of-Service Standards (v3.11 — MANDATORY audit framework)

**Canonical document:** `references/level-of-service-standards.md`
**Audit script:** `scripts/availability-audit.js`
**Quick probe:** `scripts/url-health-check.js`

Every QNFO Cloudflare asset is classified into one of three tiers and audited against
18 standards covering Pages, Workers, and DNS/Domains. Standards are severity-rated:
**CRITICAL** (public outage), **WARNING** (degraded), **INFO** (drift/noise).

### Standards Quick Reference

| ID | Layer | Standard | Severity | Test |
|:---|:------|:---------|:---------|:-----|
| P-S1 | Page | Root document reachable (200/301/302/401) | CRITICAL (T1) | `curl -sI https://{domain}/` |
| P-S2 | Page | Zero 522-RISK (CNAME→pages.dev must be registered) | CRITICAL | Cross-ref DNS records vs Pages custom domains |
| P-S3 | Page | Successful build within 30 days | WARNING | Check latest deployment stage+date |
| P-S4 | Page | DNS resolution integrity | CRITICAL (T1) | `dig +short` → must return IPs |
| P-S5 | Page | D1 traceability (`portfolio-state`) | INFO | SELECT from audit_pages table |
| W-S1 | Worker | Health endpoint (`/health` or `/status`) | CRITICAL | `curl -s https://{worker}.q08.workers.dev/health` |
| W-S2 | Worker | Binding integrity gate (≥2 data routes → 200) | CRITICAL (D1/R2) | Probe data-dependent routes post-deploy |
| W-S3 | Worker | Active deployment within 90 days | WARNING | `wrangler deployments list` or builds MCP |
| W-S4 | Worker | No unauthenticated `/debug/*` routes | CRITICAL | Probe `/debug/init`, `/debug/seed` → must 404 |
| W-S5 | Worker | `.workers.dev` subdomain reachable | WARNING | Probe root URL |
| W-S6 | Worker | Binding declaration consistency | WARNING | Cross-ref bindings vs source code |
| D-S1 | DNS | Minimum 1 DNS record per zone (KIF-52) | CRITICAL | GET zones/{id}/dns_records → count > 0 |
| D-S2 | DNS | Domain resolution (no NXDOMAIN) | CRITICAL | `dig +short` or DNS-over-HTTPS probe |
| D-S3 | DNS | No CNAME chains (A→B→C.pages.dev) | WARNING | Resolve CNAME targets recursively |
| D-S4 | DNS | No dead Worker CNAMEs | CRITICAL | Cross-ref CNAME targets vs workers_list |
| D-S5 | DNS | No account-level redirect intercept (KIF-51) | CRITICAL (T1) | `curl -sv` → check Location header |
| D-S6 | DNS | At least 1 proxied record per zone | INFO | Check `proxied: true` flag |
| D-S7 | DNS | Worker route coverage | WARNING | Check zone-level workers/routes |

### Availability Audit Workflow

**Full audit (all layers, all standards):**
```bash
skill_run cloudflare scripts/availability-audit.js
```
Produces structured findings with severity, detail, and fix hints. Exit codes:
- **0**: All pass
- **1**: WARNING findings present
- **2**: CRITICAL findings present

**Quick URL health probe (HTTP only, no API token):**
```bash
skill_run cloudflare scripts/url-health-check.js
```
Probes all 28 known QNFO public URLs. Reports status, latency, body size.

**Targeted audit:**
```bash
skill_run cloudflare scripts/availability-audit.js --tier workers
skill_run cloudflare scripts/availability-audit.js --tier pages
skill_run cloudflare scripts/availability-audit.js --tier dns
skill_run cloudflare scripts/url-health-check.js --domain qnfo.org
```

**Machine-readable output:**
```bash
skill_run cloudflare scripts/availability-audit.js --json
skill_run cloudflare scripts/url-health-check.js --json
```

### Post-Incident Protocol
After any availability incident (binding loss, 522, redirect intercept, empty zone):

1. **Run full audit:** `availability-audit.js` — identify all affected assets
2. **Fix CRITICAL findings:** Binding redeploy → KIF-50. Empty zone fix → KIF-52. Redirect → KIF-51.
3. **Verify fix:** Re-run `availability-audit.js` — all CRITICAL must be CLEAR
4. **Probe URLs:** `url-health-check.js` — confirm all Tier-1 URLs return 200
5. **Write tape handoff:** Document root cause, impact duration, fix applied, new anti-pattern if any
6. **Update standards:** If a new failure mode was discovered, add a new standard to `level-of-service-standards.md`

### Public URL Inventory (28 URLs across 19 domains)

| Layer | Count | Examples |
|:------|:------|:---------|
| Tier-1 Gateway | 4 | qnfo.org, papers.qnfo.org, legal.qnfo.org, graph-api.qnfo.org |
| Tier-1 Pages | 2 | qwav.org, qwav.tech |
| Tier-1 Broken | 1 | ipatent.me (KIF-51 redirect) |
| Tier-2 Workers | 7 | qnfo-gateway, qnfo-ai, qnfo-ipatent, qnfo-qwav, qnfo-memory-mcp, qnfo-lifecycle, qnfo-archive |
| Tier-2 Pages | 5 | qnfo-publications, qwav, qnfo-hub, ipatent-me, ask-qwav |
| Tier-3 Dormant | 8 | qnfo.net, qnfo.uk, q-wave.tech + qwav variants, empoweringchange.today |

> **Full inventory and probe targets are in `scripts/url-health-check.js` — update that script when domains are added/removed.**

---

## Infrastructure Audit (Full Ecosystem)

### D1 Databases
Baseline: 6. Database IDs: `ipatent-db`, `qnfo-cms`, `living-paper`, `portfolio-state`, `qnfo-graph`, `qnfo-audit`

### R2 Buckets
Baseline: 13 buckets (corrected 2026-07-25 systemwide audit — live enumeration returned 13:
`deepchat`, `git-repos`, `ipatent`, `palimpsest-research`, `play-the-ball`, `qnfo`, `qnfo-assets`,
`qnfo-audit`, `qnfo-backups`, `qnfo-projects`, `qnfo-releases`, `qnfo-skills`, `releases`.
The prior "14" baseline could not be reconciled against any deletion record — OPEN ITEM F-1,
see `qnfo-audit/audits/2026/07/SYSTEMWIDE-AUDIT-2026-07-25.md`. Any future count ≠ 13 without
an audit-trail row is drift.)

### Workers
Baseline: 9 (updated 2026-08-02 — live `workers_list` MCP returned 9 incl.
`qnfo-paper-indexer`, created 2026-08-01; treat any future count ≠ 9 as drift).
**Fleet:** `qnfo-gateway` (unified API+graph+legal+papers, 17 routes), `qnfo-gateway-production` (staging/prod variant, created 2026-07-31), `qnfo-paper-indexer` (auto-indexes paper full-text into Vectorize; cron every 30 min + webhook for real-time; v1.0, 2026-08-01), `qnfo-archive`, `qnfo-lifecycle` (v1.1 — 7 cron handlers with real logic, `/status` fixed), `qnfo-ai`, `qnfo-ipatent`, `qnfo-memory-mcp` (v1.0.1 — debug endpoints removed), `qnfo-qwav`

### Pages
Baseline: 5 projects (post-consolidation 2026-07-17: `qnfo-publications`, `qwav`, `qnfo-hub`, `ipatent-me`, `ask-qwav`).

### Vectorize
Baseline: 5 indexes (2026-07-25: added `qnfo-ai-log`, 768-dim cosine — qnfo-ai v4.1 query-log semantic recall; joins `ipatent-disclosures`, `qnfo-handoffs`, `qnfo-tasks`, `qwav-research-v2`).

### AI Gateway (consolidated 2026-07-25)
Baseline: **1 gateway** — `default` (authenticated, collect_logs on, 10M log retention, unified billing FUNDED). `quni-io` and `0pus` deleted same date (0 logs each, verified live before deletion). Any second gateway appearing without an audit-trail row is drift.
**Single point of entry for ALL AI:** `qnfo-ai` Worker v4.1 (`https://qnfo-ai.q08.workers.dev`) — auto-routing (5D), pinned models, ensembles, internal RAG (papers+memory Vectorize), query logging (D1 `qnfo-audit.ai_queries` + Vectorize `qnfo-ai-log`), `/v1/search`, `/v1/history`. Auth key at `%USERPROFILE%\.qnfo\router-auth-key` (rotated 2026-07-25).
**Tier-3 provider quirks (verified live 2026-07-25):** use the gateway COMPAT endpoint `gateway.ai.cloudflare.com/v1/{acct}/{gw}/compat/chat/completions` — the account-level `/ai/v1/chat/completions` endpoint returns HTTP 200 with an EMPTY anthropic message body (silent failure). anthropic claude-5 series rejects `temperature` (400 "deprecated"). openai gpt-5.x requires `max_completion_tokens`, rejects `max_tokens`.

### DNS Integrity Checks

#### 522-RISK Detection (MANDATORY)
For every CNAME record pointing to `.pages.dev`, verify the domain is registered on the target Pages project.

#### CNAME Chain Detection
Detect CNAME chains: A -> B -> C.pages.dev

#### Dead Worker Detection
CNAME pointing to non-existent Worker.

#### Empty Zone Detection (KIF-52 — MANDATORY)
**During every infrastructure audit, query `GET /zones/{id}/dns_records?per_page=5` for EACH zone in the account.** If any zone returns `count=0`, flag it as CRITICAL and add a proxied CNAME + zone-level Worker route. An "active" zone with zero DNS records resolves to nothing — users see "server not found." 3 of 12 zones had this condition on 2026-07-30: qnfo.net, qnfo.uk, q-wave.tech.

#### Account-Level Redirect / Intercept Detection (KIF-51)
For every custom domain that returns HTTP 301/302 to an unexpected destination or HTTP 503 with a Cloudflare body:
1. Run `curl -v https://domain/` — inspect the `Location:` header
2. Check `GET /accounts/{id}/rulesets` for non-managed `http_request_redirect` rulesets
3. Check `GET /zones/{id}/workers/routes` for misconfigured routes
4. If the redirect destination is NOT Cloudflare infrastructure (e.g., Google Cloud Run), it's an account-level redirect rule — fix via API (step 5 below), NEVER via Dashboard
5. **Delete the offending ruleset via API (NO DASHBOARD):**
   ```bash
   # List all account-level rulesets to find the offending one:
   curl -s -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
     https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/rulesets
   # Delete the ruleset containing the redirect:
   curl -s -X DELETE -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
     https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/rulesets/{RULESET_ID}
   ```
   Alternatively, `PUT` to update the ruleset with the offending rule removed from the `rules` array (less destructive). Requires token scope: `Account:Rulesets:Edit`.

### Lifecycle Pipeline

| Worker | Purpose | Cron | Health Check |
|:-------|:--------|:-----|:-------------|
| `qnfo-lifecycle` | Scans `last_active`, transitions ACTIVE->STALE->ARCHIVED | Daily 06:00 UTC | `curl https://qnfo-lifecycle.q08.workers.dev/status` |
| `qnfo-archive` | Consumes queue, migrates R2 files | On queue trigger | `curl https://qnfo-archive.q08.workers.dev/health` |

### Lifecycle Timeline
| Days Inactive | Status | Action |
|:-------------:|:-------|:-------|
| 0-90 | ACTIVE | Normal operation |
| 90-180 | STALE | Flagged by Lifecycle Worker. Project intact. |
| 180+ | ARCHIVED | R2 files auto-migrated to `qnfo/archive/projects/<name>/` |

### Resource Baselines (post-consolidation)

| Resource | Expected | Warning | Critical |
|:---------|:--------|:--------|:---------|
| D1 Databases | 6 | +/- 1 | +/- 2+ |
| Workers | 9 | 10-11 | 12+ |
| Pages Projects | 5 | 6-7 | 8+ |
| Vectorize Indexes | 5 | +/- 1 | +/- 2+ |
| R2 Buckets | 13 | +/- 1 | +/- 3+ |
| Queues | 1 | +/- 1 | +/- 2+ |
| KV Namespaces | 1 | +/- 1 | +/- 2+ |
| DNS Zones | 12 active | +/- 1 | +/- 3+ |
| 522-RISK | 0 | 1+ | -- |
| CNAME Chains | 0 | 1+ | -- |
| DEAD-WORKER | 0 | 1+ | -- |
| **LoS CRITICAL** | **0** | **1+** | **3+** |
| **LoS WARNING** | **≤3** | **4-7** | **8+** |

> **LoS baselines added v3.11:** After every `availability-audit.js` run, CRITICAL must be 0 and WARNING should be ≤3. Any drift from these baselines requires a post-incident protocol run. See `references/level-of-service-standards.md` for full standards definitions.

### DNS Zones (verified 2026-07-18)
12 active zones: `empoweringchange.today`, `ipatent.me`, `q08.org`, `qnfo.net`, `qnfo.org`, `qnfo.uk`, `q-wave.tech`, `qwave.tech`, `qwav.net`, `qwav.org`, `qwav.tech`, `qwav.uk`. Growth from prior baseline (7) reflects legitimate qwav/ipatent product domain expansion, not drift.

### OPEN ITEM — I-05: Unexplained Pages Project Deletions (2026-07-18)
`audit_pages` D1 table lists 10 projects with `status='active'` as of the last sync, but only 5 exist live. `qnfo-legal` deletion is **explained** (consolidated into `qnfo-gateway` Worker v2.0). The following 4 are **UNEXPLAINED** — no matching `deployment_history` or `audit_trail` row, and Pages project deletion has no soft-delete/undo via API:
- `quantum-advantage-audit` (last deployed 2026-07-13)
- `ultrametric-ai-poc` (last deployed 2026-07-12)
- `two-ways-of-measuring` (last deployed 2026-07-12)
- `qnfo-design-system` (last deployed 2026-07-13)
- `hensel-code` (last deployed 2026-07-13)

**Action needed:** Investigate whether these were manually deleted, hit a Pages project quota/cleanup automation, or another undocumented process. If content is needed, check R2 `qnfo-backups`/`qnfo-releases` for build artifacts predating deletion. Until root-caused, treat any future Pages project disappearance as CRITICAL and halt automated cleanup scripts touching Pages.

### D1 Backup Coverage (MANDATORY — added 2026-07-18)
`qnfo-lifecycle` runs a daily 05:00 UTC cron (`runBackup`) that exports `portfolio-state.resources` and `qnfo-audit.audit_sessions` to `qnfo-backups/{db}/{table}-{date}.json`. **Before this fix, `qnfo-backups` was 0 objects for the database's entire lifetime** — a silent single-point-of-failure that turned a 3-row data-loss incident (C-01, 2026-07-18) into an unrecoverable event without D1 Time Travel. Extend `runBackup`'s `tables` array whenever a new production-critical D1 table is added (e.g., `living-paper.papers` once schema stabilizes).

**C-01 RESOLVED (2026-07-18):** `living-paper.papers` fully restored to 616 rows via `wrangler d1 time-travel restore --bookmark=00000b67-...`. KG-D1 reconciled to 616=616 (26 missing KG Paper nodes seeded via `qnfo-gateway` `/sync`). Zero data loss confirmed — a concurrent session's 189-row write (13 orphan chapter files) was verified already contained within the restored 616-row set.

**BACKUP GAP CLOSED (2026-07-25, KIF-22):** `qnfo-lifecycle` v1.2 deployed with `living-paper.papers` added to the daily `runBackup` tables array (LIVING_PAPER D1 binding). The mandate above ("extend runBackup whenever a new production-critical table is added") had sat unexecuted for 7 days while the table grew to 931 rows with zero scheduled backups. First backup verified: `qnfo-backups/living-paper/papers-2026-07-25.json` (4.9 MB, 931 rows).

### Gateway /sync Bulk Contract (documented 2026-07-25, F-6)
`POST https://qnfo-gateway.q08.workers.dev/sync` requires EXACTLY:
```json
{"action": "bulk", "nodes": [{"id": "...", "name": "...", "label": "...", "properties": {}}], "edges": []}
```
Any other body shape returns the unhelpful `{"error":"Only bulk sync supported"}`. Nodes upsert via `ON CONFLICT(id)`. Use `id: "paper:<slug>"` convention for Paper nodes. Batch ≤50 per call.

### KG-D1 Paper Reconciliation (MANDATORY periodic check, KIF-23)
Publication pipelines write D1 but KG seeding is session-dependent — drift accumulates silently (257 missing Paper nodes found 2026-07-25, 29% of corpus invisible to KG-first due diligence). Reconcile by diffing `SELECT DISTINCT slug FROM papers` (living-paper) against KG `paper:<slug>` ids + `properties.slug`, then bulk-seed missing via `/sync`. Run this diff during every infrastructure audit.

### R2 Path Hygiene
**CRITICAL RULE:** Bucket name IS the namespace. NEVER prefix keys with `qnfo/` inside the `qnfo` bucket.

---

## Retrieval Sources (Prefer over pre-training — MCP-first)

| Source | Method | Use for |
|:-------|:-------|:--------|
| Cloudflare docs MCP | `cloudflare-docs` MCP server (`search_cloudflare_documentation`) | Limits, pricing, API reference (PREFERRED over `search_cloudflare_documentation` tool) |
| Cloudflare blog MCP | `cloudflare-blog` MCP server | Recent announcements, product updates, migration guides |
| Workers types | `npm pack @cloudflare/workers-types` | Type signatures, binding shapes |
| Wrangler config schema | `node_modules/wrangler/config-schema.json` | Config fields, binding shapes |

---

## MCP-Driven Operations (v3.9 — MANDATORY preference order)

**HARD RULE:** When a Cloudflare MCP server exists for an operation, use it BEFORE falling back to raw `npx wrangler`, REST API, or `curl`. MCP servers provide structured, typed, auto-authenticated results — CLI/REST are error-prone (wrong account IDs, silent encoding issues, PowerShell quoting traps). Every QNFO operational domain is mapped below.

### MCP Server → Agent Tool Mapping (v3.12)

The deepchat agent has these Cloudflare MCP tools available directly — use them by name:

| Agent Tool | Covers | Replaces |
|:-----------|:-------|:---------|
| `workers_list()` | List all Workers | `npx wrangler deploy list` / `GET /accounts/.../workers/scripts` |
| `workers_get_worker(scriptName)` | Get Worker details | `GET /accounts/.../workers/scripts/{name}` |
| `workers_get_worker_code(scriptName)` | Get Worker source code | Manual Dashboard code view |
| `query_worker_observability(query, timeframe)` | Worker logs, metrics, invocation tracing | `curl /health` endpoint, `cloudflare-observability` MCP |
| `search_cloudflare_documentation(query)` | Search Cloudflare docs | Web search, `cloudflare-docs` MCP |
| `search_papers(query)` / `search_papers_enriched(query)` | Semantic paper search via Vectorize | Manual D1 queries |
| `query_graph(endpoint, params)` | Knowledge graph queries | Manual Cypher/SQL |
| `skill_run cloudflare scripts/<name>` | Run bundled skill scripts | Manual `exec` with hardcoded paths |

For other Cloudflare MCP servers (bindings, builds, auditlogs, graphql, etc.), the agent accesses them through the configured `mcp-settings.json` OAuth connections — use them when their specific capabilities are needed.

### Operation → MCP Server Decision Matrix

| When you need to... | Use this MCP server (1st choice) | Fallback (2nd) | NEVER (wasteful) |
|:--------------------|:---------------------------------|:---------------|:-----------------|
| Deploy/manage Workers, Pages, R2, D1, KV, Queues, AI, DNS | `cloudflare` (main) | wrangler CLI | Raw REST when MCP is available |
| Search Cloudflare docs/prod limits | `cloudflare-docs` | `search_cloudflare_documentation` tool | Web search for Cloudflare docs |
| Inspect Workers bindings/wrangler.toml | `cloudflare-bindings` | Read wrangler.jsonc locally | Guess from memory |
| Check Pages/Worker build logs, CI/CD deploy history | `cloudflare-builds` | `npx wrangler deployments list` | Claim "deployed" without build confirmation |
| Monitor Worker health, logs, invocation tracing | `cloudflare-observability` | `curl /health` endpoint | `workers_get_worker_code` alone |
| Inspect AI Gateway logs, prompt/response tracing | `cloudflare-ai-gateway` | Raw Gateway REST API | Assume AI calls worked |
| Cross-product analytics (all Cloudflare products) | `cloudflare-graphql` | Per-product REST APIs | Manual aggregation |
| Query account audit trail, compliance reports | `cloudflare-auditlogs` | Manual `GET /accounts/{id}/audit_logs` | Trust "it was deployed" narrative |
| Internet insights, BGP, traffic trends, domain rankings | `cloudflare-radar` | External internet stats tools | Guess traffic patterns |
| Export/stream Workers logs to external destinations | `cloudflare-logpush` | Manual log download via REST | Lose logs between sessions |
| Headless browser automation, screenshots, PDF gen | `cloudflare-browser-mcp-server` | YoBrowser / CDP | Local browser (thin-client) |
| DNS query analytics, query volumes, top queries | `dns-analytics` | `nslookup` / `dig` | Guess zone traffic |
| Deploy Docker containers on Cloudflare edge | `containers-mcp` | Manual REST + Container Registry | Local Docker (no edge) |
| SaaS security audits, CASB scanning | `cloudflare-casb-mcp-server` | Manual SaaS config review | Assume connected apps are secure |
| Automated RAG with Workers AI + Vectorize | `cloudflare-autorag-mcp-server` | Manual Vectorize insert + Workers AI call | Skip RAG entirely |
| Search blog.cloudflare.com for announcements | `cloudflare-blog` | Web search for "Cloudflare blog" | Assume nothing changed |
| Digital Experience monitoring, network perf | `dex-analysis` | Manual `curl` latency tests | Assume "it's fine" |

### Multi-Server Workflows

**Infrastructure Audit (full ecosystem):**
```
1. cloudflare             → list Workers, D1, R2, KV, Pages, Queues, DNS zones
2. cloudflare-observability → per-Worker metrics, error rates, invocation counts
3. cloudflare-graphql     → cross-product analytics (bandwidth, requests, threat data)
4. cloudflare-auditlogs   → deployment audit trail, who changed what when
5. dns-analytics          → per-zone query volumes, top domain queries
6. cloudflare-builds      → verify latest deployment for each Worker/Pages project
7. cloudflare-bindings    → cross-reference declared vs actual bindings per Worker
```
**Result:** A single audit that answers "what exists, is it healthy, who touched it, and how much traffic does it get" — all from MCP servers without a single `curl` or `wrangler` call.

**Post-Deploy Verification:**
```
1. cloudflare-builds      → confirm deploy succeeded, get build ID
2. cloudflare-observability → confirm new Worker is receiving healthy invocations
3. cloudflare-auditlogs   → confirm deploy action appears in audit trail
4. cloudflare-bindings    → verify bindings match wrangler.jsonc
5. dns-analytics          → (if custom domain) confirm DNS resolution traffic
6. dex-analysis           → verify end-user latency is within baseline
```

**Research Publication → Production (full pipeline):**
```
1. cloudflare             → D1 insert (living-paper), R2 archive, DNS DNSLink
2. cloudflare-observability → confirm papers-server Worker serves new paper
3. cloudflare-graphql     → confirm CDN cache hit ratio increasing (paper gaining readers)
4. cloudflare-radar       → check papers.qnfo.org domain ranking trend
5. cloudflare-blog        → search for relevant Cloudflare announcements to cite
6. cloudflare-auditlogs   → complete publication audit trail
```

**Security Posture Review:**
```
1. cloudflare-casb-mcp-server → audit all connected SaaS apps
2. cloudflare-auditlogs       → review recent privileged operations
3. cloudflare                 → check WAF rules, DDoS protection status, API Shield
4. cloudflare-graphql         → threat analytics, blocked request trends
5. cloudflare-docs            → verify security feature configurations against best practices
```

### MCP Anti-Phantom Gate for Operations

When an MCP server call returns a success response, treat it with the same verification rigor as CLI/REST:
1. **`cloudflare-observability`** — a Worker listed as "healthy" by the MCP is a STARTING POINT, not verification. Cross-reference against `cloudflare-builds` (deploy date matches) and `cloudflare-auditlogs` (deploy action recorded).
2. **`cloudflare-builds`** — "deploy succeeded" must be paired with `cloudflare-observability` showing healthy invocations within the same timeframe.
3. **`cloudflare-graphql`** — analytics results must be time-bounded and cross-referenced against `cloudflare-observability` for consistency.
4. **MCP-only verification chain:** two MCP servers independently confirming the same fact (e.g., Worker X is healthy per observability AND its latest deploy succeeded per builds AND the deploy action appears in auditlogs) constitutes a verified claim. Single-MCP-server results are directionally useful but not verified.

---

## Skill Cross-Reference: Cloudflare Tool/Resource Discoverability (v3.18)

**Ephemeral-memory mandate (2026-08-02):** DeepChat memories are NOT permanent.
Every skill that references Cloudflare resources MUST name the actual agent tools
for discovery and verification — never assume the agent will recall them from memory.

### Agent Tool Names (canonical — use these exact names in skill instructions)

| Agent Tool | Covers | Use when |
|:-----------|:-------|:---------|
| `workers_list` | Enumerate all Workers + modified_on timestamps | ANY infra audit (STALE-AUDIT-1 gate) |
| `workers_get_worker(scriptName)` | Worker details | Single-worker inspection |
| `workers_get_worker_code(scriptName)` | Worker source | Verify handler actually uses a binding |
| `query_worker_observability(query, timeframe)` | Logs, metrics, invocations | Health verification post-deploy |
| `observability_keys` / `observability_values` | Log field discovery | Building observability queries |
| `search_cloudflare_documentation(query)` | Cloudflare docs | Limits, API reference, config schema |
| `migrate_pages_to_workers_guide` | Pages→Workers migration | Migration tasks |
| `search_papers` / `search_papers_enriched` | Vectorize semantic search | Paper retrieval (MCP layer) |
| `query_graph(endpoint, params)` | Knowledge Graph | KG queries |
| `get_paper_context(slug)` | D1 paper body | Paper body retrieval |
| `resolve_paper_id(id)` | DOI→slug cross-resolve | Identity resolution |

### Skill → Cloudflare Resource Map (which skills touch what)

| Skill | Cloudflare Resources | Tool Names Required | Status |
|:------|:--------------------|:--------------------|:-------|
| `cloudflare` (this skill) | All (Workers, D1, R2, Vectorize, Pages, DNS) | All agent tools above | ✅ v3.18 |
| `research` | D1 living-paper, R2 releases, papers-server Worker, Zenodo | search_papers, query_graph, workers_list | ✅ v2.45 (verify) |
| `knowledge` | D1 qnfo-graph, Vectorize, graph-api.qnfo.org | query_graph, search_memories, recall_facts | ✅ v2.2 (verify) |
| `system` | Skills R2 bucket (qnfo-skills), skill-sync.js | workers_list (sync target) | ✅ v2.4 |
| `code` / `mcp-builder` | Workers deploys (MCP servers) | workers_list, workers_get_worker | ✅ (verify) |
| `git-github` | GitHub-D1 sync (GitHub is canonical, D1 is mirror) | workers_list, query_graph | ⬅ v2.3 needs pointer |
| `frontend-design` | Pages deploys, R2 static assets | workers_list, search_cloudflare_documentation | ⬅ v2.2 needs pointer |
| `documents` | R2 archive (r2-archive.js) | search_cloudflare_documentation, workers_list | ⬅ v2.3 needs pointer |
| `windows-command-patterns` | D1 writes (Python-first, no PowerShell) | workers_list (verification) | ⬅ v2.3 needs pointer |
| `linkedin-mcp` | (incidental — session persistence only) | — | no action |

**Verification rule:** any skill claiming "synced to R2" / "deployed to Workers" / "D1 updated"
MUST reference the verification tool (`workers_list`, `query_worker_observability`, or the
live Worker endpoint probe) in its own instructions — not rely on the agent remembering.

## Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| Treating Cloudflare services in isolation | Evaluate full-stack: Workers + D1 + R2 + KV + DNS + WAF as ONE system |
| Deploying without infrastructure audit | Audit resource baselines BEFORE and AFTER deployment |
| Skipping DNS integrity on Pages deploy | Verify CNAME->.pages.dev domain registration (522-RISK check) |
| Using `qnfo/` prefix in R2 keys on `qnfo` bucket | Bucket IS the namespace. Use `category/subpath` convention. |
| Trusting local files over R2 | R2 is canonical. Local files are ephemeral caches. |
| `wrangler deploy` without verifying `wrangler whoami` | Always verify authentication first |
| Pages-per-publication | Use single Pages project or Workers + D1 for dynamic serving |
| Non-Cloudflare infrastructure | Architecture Compliance Gate: D1/R2/Workers ONLY |
| Duplicated Workers with same bindings | Consolidate into gateway Worker per Consolidation Pattern |
| Publishing without DNSLink | Every publication subdomain must have `_dnslink` TXT record |
| Single copy of critical assets | 4-D: Distributed, Durable, Discoverable, Duplicated |
| Single cloud copy of critical assets | Core stack: R2 (canonical) + GitHub (replicated) + Zenodo (archival). At least 2 independent copies for all deliverables. |
| Unauthenticated `/debug/*` routes bound to production D1 (DROP/CREATE/INSERT) | NEVER ship debug/init/seed endpoints to production Workers. Root cause of 2026-07-18 living-paper 616→3 row data loss (`qnfo-memory-mcp /debug/init`). Gate: any route containing DROP/CREATE TABLE/schema-reset logic requires auth header + non-production-only compatibility flag, or must not exist post-deploy. |
| Empty backup bucket with no verification | Add a scheduled backup Worker cron (`runBackup`) writing to R2 on day 1 of any new production D1 database. Verify object count > 0 within first 24h, not just bucket existence. |
| Assuming infra-audit narrative (handoff notes) over live D1 row counts | ALWAYS query live D1 `SELECT COUNT(*)` before trusting audit_sessions.notes — narrative logs can be stale or describe a different table than what actually shipped. |
| Vectorize binding declared in wrangler config but never called in fetch handler (dead binding masked by LIKE/stub fallback) | Read full Worker source and cross-reference every declared binding name against actual usage in handler code. Found 2026-07-18 in both `qnfo-ipatent` (`/api/search` literal stub despite populated 1024-dim `DISCLOSURES_VZ` index) and `qnfo-qwav` (`/ask` used SQL `LIKE` despite unused `QWAV_VZ` binding to 768-dim `qwav-research-v2` index). Fix: embed query via Workers AI (matching the index's original embedding model), `.query()` the Vectorize index, keep LIKE only as a fallback when AI/Vectorize is unavailable. |
| Restoring a production D1 database via Time Travel without first exporting a full row/table snapshot of ANY concurrent writes to R2 | Before any Time Travel restore, run `SELECT *` (explicit column list, avoid FTS5 tables which break `d1 export`) and upload the JSON to R2 as a safety net. Verified 2026-07-18: C-01 living-paper restore preceded by snapshot to `qnfo-backups/living-paper/pre-restore-snapshot-*.json`; post-restore diff confirmed zero data loss. |
| Using external IPFS pinning services (REMOVED v3.2) | All external pinning (Pinata, Filebase, Lighthouse, Arweave) deprecated. Core stack: R2+D1+Workers+DNS. DNSLink is optional. |
| Concluding "wrangler is not installed" from `npm ls -g wrangler`, a bare `where wrangler` miss, or a Python `subprocess.run()` PATH failure (KIF-19) | Run `wrangler --version` directly (PATH-registered since 2026-08-01: `C:\Users\LENOVO\npm-global`) or `node scripts/wrangler-check.js`. The only sufficient test is `wrangler --version` + `wrangler whoami` executed directly. Note: wrangler 4.118.0 IS now globally installed at the user prefix; an npx-cached 4.114.0 copy was found corrupt (truncated download → SyntaxError) — check both locations and delete-and-reinstall corrupt caches. |
| Guessing D1/Zenodo/Workers/Buffer API request shapes from memory each session | Consult `references/d1-rest-api-schema.json`, `references/workers-deploy-metadata-schema.json` (this skill) and `../research/references/zenodo-deposit-schema.json`, `../research/references/buffer-graphql-schema.json` (research skill) BEFORE constructing the call. |
| `ON CONFLICT` upsert against a D1 table with FTS5 shadow tables (HTTP 400) | Use `scripts/d1-safe-write.js` (CHECK-THEN-WRITE, never a combined upsert) — see `references/d1-rest-api-schema.json`. |
| Large D1 write payloads built via PowerShell `ConvertTo-Json` silently corrupting to `"[object Object]"` (KIF-21) | Use `scripts/d1-safe-write.js` (Node-native JSON construction + mandatory length-verification re-GET) instead of PowerShell string-building for any payload > a few hundred characters. |
| **KIF-59: Using PowerShell for ANY Cloudflare operation (2026-07-31 incident)** | **HARD BLOCK.** PowerShell corrupts UTF-8, mangles quoting, aliases `curl` to `Invoke-WebRequest`, and `ConvertTo-Json` silently produces garbage. Use MCP tools (`workers_list`, `query_worker_observability`, etc.) FIRST, `npx wrangler` SECOND, REST API with Python THIRD. PowerShell is NEVER acceptable for Cloudflare operations — even `curl.exe` must be invoked directly (not via PowerShell which may intercept it). See §EXECUTION GATE for the full decision ladder. |
| Not configuring Cloudflare MCP servers that are directly relevant to QNFO operations (KIF-48) | DeepChat's `mcp-settings.json` must include all high-value Cloudflare MCP servers: `cloudflare` (main), `cloudflare-docs`, `cloudflare-bindings`, `cloudflare-builds`, `cloudflare-observability`, `cloudflare-ai-gateway`, `cloudflare-graphql`, `cloudflare-auditlogs`, and `cloudflare-radar`. See §DeepChat MCP Server Coverage for the canonical list. |
| Trusting that an MCP server is reachable without a live HTTP probe | Verify with `curl.exe -s -o NUL -w "%{http_code}" https://<subdomain>.mcp.cloudflare.com/mcp` — 401 = live (auth required), 404/530 = not deployed. Never claim an MCP server "is working" from config validation alone. |
| Using raw `npx wrangler` or REST API when an MCP server exists for that operation (KIF-49) | Consult §MCP-Driven Operations decision matrix FIRST. `cloudflare-observability` replaces `curl /health`. `cloudflare-builds` replaces `npx wrangler deployments list`. `cloudflare-auditlogs` replaces manual audit log REST queries. CLI/REST are FALLBACKS, not defaults. |
| Claiming "deployed" or "healthy" from a single MCP server response alone (MCP Anti-Phantom Gate) | Cross-reference any operational claim against at least TWO independent MCP servers (e.g., observability + builds + auditlogs = verified). Single-MCP feed is directional, not confirmed. |
| Skipping `cloudflare-observability` during infrastructure audits in favor of REST/curl health checks | Observability MCP provides structured metrics (error rates, p50/p99 latency, invocation counts) that a raw `curl /health` cannot. Use it as the FIRST health check, not the last. |
| Running DNS zone audits without `dns-analytics` | `dns-analytics` MCP shows actual query volumes and top queries per zone — a zone could have perfect DNS records but zero traffic (dead domain). `nslookup` alone misses this. |
| Deploying Workers/Pages without checking `cloudflare-builds` for build confirmation | `cloudflare-builds` MCP is the canonical deploy-history source. Wrangler's `deploy` exit code confirms the REQUEST was accepted, not that the build pipeline succeeded and the artifact is serving. |
| **KIF-50:** Deploying Workers via REST API PUT without binding metadata (2026-07-30 incident) | A `PUT /accounts/{id}/workers/scripts/{name}` without `metadata.bindings` silently drops ALL D1, R2, KV, and Vectorize bindings from the Worker. The Worker code still references `env.LIVING_PAPER`/`env.DB`/`env.QNFO_BUCKET` but they are `undefined` at runtime → HTTP 500. **ALWAYS use `npx wrangler deploy` from a `wrangler.toml`/`wrangler.jsonc` that declares EVERY binding.** After any deploy, verify ALL data-dependent routes return 200 (not just `/health`). Impact: 4 public domains down for ~30 min when gateway lost 3 bindings. |
| **KIF-51:** Account-level `http_request_redirect` rulesets silently intercepting traffic before Pages/Workers (2026-07-30 finding, FIXED v3.13) | The Cloudflare Rules Engine executes redirect phases at position 5, BEFORE Workers (position 10). **Diagnose with `curl -v https://domain/`** — look for `Location:` and `CF-RAY`. **Fix via API (NO DASHBOARD):** `GET /accounts/{id}/rulesets` to find the ruleset, then `DELETE /accounts/{id}/rulesets/{id}`. Requires token scope `Account:Rulesets:Edit`. The prior claim that API tokens couldn't manage these was a permissions issue, not an API limitation. |
| **KIF-52:** DNS zones with zero records flagged as "active" (2026-07-30 finding) | 3 of 12 active zones had 0 DNS records: qnfo.net, qnfo.uk, q-wave.tech. A zone with no A/AAAA/CNAME records resolves to nothing — 100% dead. **Every infrastructure audit MUST check `dns_records count` per zone and flag count=0 as CRITICAL.** Fix: add a proxied CNAME pointing to an active gateway Worker domain + a zone-level Worker route. DNS propagation takes minutes to hours. |
| **KIF-53:** Custom domains CNAME'd to API-only Workers with no root handler (2026-07-30 finding) | `qnfo-ipatent` Worker returns `{error:"Not found"}` (404) for `/` but `ipatent.me` CNAME pointed at it. The Worker has handlers for `/health`, `/api/disclosures`, `/api/search` only. **If a custom domain's users expect HTML, the CNAME must point to a Pages project or a Worker that serves HTML.** API-only Workers should get subdomain routes (e.g., `api.ipatent.me`), not the apex domain. Found during red-team: ipatent-me.pages.dev serves a professional landing page (5,655 bytes) but ipatent.me was blocked by an account-level redirect (KIF-51) AND pointed at the wrong Worker. |
| **KIF-60: Using Cloudflare Dashboard (web UI / manual login) for ANY operation (2026-07-31 mandate)** | **HARD BLOCK.** The Cloudflare Dashboard requires web UI, manual browser login, and human interaction — all operations MUST be CLI/API/command-line only. Every Dashboard operation has an API equivalent: redirect rulesets → `GET/DELETE /accounts/{id}/rulesets`, Pages deploy → `npx wrangler pages deploy` or REST API, DNS management → `GET/POST /zones/{id}/dns_records`, Workers deploy → `npx wrangler deploy`. If an API endpoint doesn't exist for a specific operation, use the Cloudflare MCP server (`workers_list`, `query_worker_observability`, etc.) FIRST, then fall back to REST API. Dashboard is NEVER acceptable — the user shall not manually intervene in any operation that can be executed by CLI, API, or command line. |
| **R2 object get/put/delete WITHOUT `--remote` (v3.14, 2026-08-01)** | Wrangler v4 `r2 object` commands default to LOCAL storage. Without `--remote`, a live object read returns `"The specified key does not exist."` — a FALSE NEGATIVE that led to a "resume not in R2" misdiagnosis. ALWAYS pass `--remote` for live storage operations; use `--local` only for simulation. |
| **R2 REST listing without pagination (v3.14, 2026-08-01)** | The object-list API returns **20 objects per page by default**. A script that fetches one page and checks for a key beyond page 1 produces a false "NOT FOUND" conclusion. Pass `&limit=1000` and follow `result.cursor` until absent. |
| **R2 object verification via HEAD (v3.14, 2026-08-01)** | The R2 object API does NOT support HEAD — it returns HTTP 405, which a verification script misread as "not found". Use GET and compare `Content-Length` (or MD5 of the body) against the local source. |
| **Literal `%VAR%` in `.npmrc` / npm config values (v3.14, 2026-08-01)** | npm config files do NOT expand Windows `%VAR%` — the string is used LITERALLY, creating a stray `%USERPROFILE%` directory. Use absolute paths (`C:\Users\LENOVO\npm-global`) or `${VAR}` syntax in `.npmrc`. |
| **KIF-61: Deploying a Worker without `workers_dev = true` and expecting HTTP/webhook access (2026-08-02)** | Cron-only or route-less Workers have NO public HTTP route — `.workers.dev` returns DNS NXDOMAIN (curl exit 1), misread as HTTP 1101 or a binding failure. Fix: `workers_dev = true` in wrangler.toml + `wrangler deploy`. Diagnose with `curl -s https://<worker>.q08.workers.dev/health` FIRST, then `wrangler deploy --dry-run` to read the live binding set. Root cause of the qnfo-paper-indexer webhook failure — the AI binding was present all along. |
| **Using `[ai]` (single table) for Workers AI binding in wrangler.toml (2026-08-02)** | Fails config validation: `The field "ai" should be an object but got [{"binding":"AI"}]`. Use `[[ai]]` (array of tables). Verify materialization via the Worker's `/health` endpoint (`ai: true`). |
| **Concluding the token lacks Workers Scripts:Edit from a REST 9106 bindings error (2026-08-02)** | `GET /accounts/{id}/workers/scripts/{name}/bindings` returned 9106 while `wrangler deploy` with the same CLOUDFLARE_API_TOKEN succeeded. The bindings sub-endpoint has a different auth path. NEVER trust a single REST 9106 as proof of missing scope — test `wrangler deploy` directly before declaring a blocker. |
| **Using `wrangler routes list` (removed in v4.118.0)** | Returns "Unknown arguments: routes, list". Route management in wrangler v4 is via wrangler.toml `workers_dev`/`routes` keys or the zone-level REST API. Use `wrangler pages project list` for Pages discovery (verified 2026-08-02: 5 projects — qwav, qnfo-hub, ipatent-me, qnfo-publications, ask-qwav). |
| **Misattributing a non-Cloudflare outage to Cloudflare (2026-08-02)** | ipatent.me: 301 (CF proxy OK) → ipatent-v4-0-1-183501038626.us-west1.run.app → 500 on Google Cloud Run. The CF layer is healthy; the 500 is the GCP backend. Always trace the full redirect chain (`curl -sI` + follow Location) before declaring "Cloudflare issue". |
| **STALE-AUDIT-1: Auditing infra without checking `workers_list` modified_on timestamps (2026-08-02)** | Findings can be invalidated by remediation that landed minutes earlier. Case: v1 audit reported qnfo-qwav dead (ai:false) + webhook 1101, but both Workers were redeployed ~30 min prior (04:28/04:30Z, workers_dev=true). Red-team v2 re-verified: ai:true, vector search 0.75-0.90, webhook 200 for real slugs. **Fix: call `workers_list` and check modified_on BEFORE trusting any infra-state claim; treat findings older than the latest deployment as provisional.** Pairs with KIF-61 (1101 root cause = DNS NXDOMAIN route, not AI binding). |

| **HARDCODED-HEALTH-1: Health endpoint hardcodes binding names (2026-08-02)** | `/health` MUST verify bindings at runtime with `!!env.BINDING_NAME` (e.g. `ai: !!env.AI`), NEVER echo the expected name as a string (`d1: "living-paper"`). Case: qnfo-qwav reported d1:"living-paper" while env.LIVING_PAPER was undefined → "Cannot read properties of undefined (reading 'prepare')" on /ask. Fix: `bindings: { d1: !!env.LIVING_PAPER ? "living-paper" : null, ai: !!env.AI, ai_search: !!env.QNFO_SEARCH }`. |
| **CF-WAF-1: Python urllib blocked by Cloudflare WAF without browser UA (2026-08-02)** | ALWAYS pass `headers={'User-Agent':'Mozilla/5.0'}` when probing Worker endpoints from Python. Default urllib UA → HTTP 403. To read the real error body, catch `urllib.error.HTTPError` and `e.read().decode()` — surfaces 1101 text, "Cannot read properties...", etc. |
| **MCP-OFFLOAD-1: Trusting MCP tool "OK" output for infra verification (2026-08-02)** | QNFO MCP tools (search_papers, query_graph, resolve_paper_id) often return "OK" with results offloaded to unreadable files. For INFRA state claims, verify with DIRECT probes (Python urllib + browser UA against the live Worker endpoint) — do not treat MCP "OK" as evidence of resource state. |
| **Relying on durable memory for critical Cloudflare operational rules (2026-08-02)** | DeepChat memories are EPHEMERAL (may be purged). Critical rules (KIF-*, anti-patterns, endpoint maps, binding formats) MUST be embedded in this SKILL.md. Memory is for session outcomes, not operational authority. Migrate any rule found only in memory into this skill. |
