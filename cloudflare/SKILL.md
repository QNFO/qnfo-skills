---
name: cloudflare
description: ULTRA-CONSOLIDATED Cloudflare Full-Stack (17-MCP Coverage) -- Workers, Pages, D1, R2, KV, Vectorize, Queues, Durable Objects, AI, DNS, Zero Trust, Email, WAF, CDN, Turnstile, Infrastructure Audit, MCP Server Management. The ONLY infrastructure skill. NEVER treat Cloudflare components in isolation -- ALL code, outputs, and deliverables must evaluate the full Cloudflare stack end-to-end.
version: 3.27
triggers: ["cloudflare-deployer", "deploy", "wrangler", "Pages", "Workers", "R2", "D1", "DNS", "KV", "Vectorize", "Queues", "AI", "Durable Objects", "Zero Trust", "Access", "Gateway", "WARP", "Tunnel", "WAF", "CDN", "Turnstile", "email", "SPF", "DKIM", "DMARC", "infrastructure", "audit", "health check", "orphan", "lifecycle", "worker route", "route conflict", "522", "CNAME", "Cloudflare", "upload", "migrate", "Pages Functions", "Workers for Platforms", "Cron Triggers", "Tail Workers", "Smart Placement", "Hyperdrive", "Secrets Store", "Pipelines", "Browser Rendering", "Zaraz", "Argo", "Spectrum", "TURN", "Network Interconnect", "Cache Reserve", "Bot Management", "API Shield", "DDoS", "Analytics Engine", "Web Analytics", "GraphQL API", "Observability", "Miniflare", "Sandbox", "Workerd", "Terraform", "Pulumi", "Snippets", "Containers", "Workflows", "Artifacts", "R2 Data Catalog", "R2 SQL", "Static Assets", "Bindings", "Image", "Stream", "RealtimeKit", "Flagship", "feature flags", "Agents SDK", "AI Gateway", "AI Search", "Workers AI", "do", "durable", "sandbox", "turnstile", "web-perf", "thin client", "IaC", "consolidation", "4-D", "IPFS bridge", "DNSLink", "Arweave", "Filecoin", "distributed", "durable", "discoverable", "duplicated"]
related: ["qnfo-core", "research"]
priority: 1
platform: cloudflare
autonomous: true
self_sufficient: true
---

# CLOUDFLARE — v3.27 (Infrastructure Audit Anti-Patterns — WBS-coded Plans + False-Positive Remediation)

> **v3.26 UPDATE (2026-08-04, kaizen — infrastructure audit anti-patterns + WBS plan integration):**
> Red-team: direct parent-agent audit of full infrastructure ecosystem (10 Workers, 12 DNS zones, 37 URLs).
> HARD: 2. SOFT: 3. DESIGN: 2.
> Changes:
> (1) [HARD] **AUDIT-FALSE-POSITIVE-1 anti-pattern**: `availability-audit.js` W-S2/W-S4 findings
>     included 6 false positives (POST-only routes tested via GET, catch-all 200 misread as debug endpoints).
>     Added route-map requirement and body-content check to W-S4 standard.
> (2) [HARD] **PAGES-DEPLOY-METADATA-1 + WRANGLER-PATH-REGRESSION-1 + GATEWAY-PROD-STALE-1**
>     anti-patterns: Pages stage parsing bug, wrangler PATH revert, stale staging Worker.
> (3) [SOFT] Fixed corrupted EMAILMSG-1/D1-UPDATE-PATTERN anti-pattern rows (merged during
>     v3.25 cross-ref update).
> (4) [SOFT] Repaired duplicate version banner at end of file.
> (5) [DESIGN] **WBS-PLAN-INTEGRATION-1**: Replaced execute_plan with 7-step WBS-coded template
>     (CLD-E0-T01 through CLD-E0-T07) per `docs/WBS-AGENT-PROTOCOL.md`. Each step carries a
>     verifiable acceptance criterion.
> (6) [DESIGN] Worker baseline updated: 10 (was 9; +qnfo-email legitimate, qnfo-gateway-production
>     is unexplained drift). 4 CRITICAL findings: 3 real (empty zones + redirect), 1 unauthenticated
>     trigger (/cron/debug). 7 WARNING findings: 6 false positives, 1 real (email health auth).
> Cross-reference: kaizen v1.15, research v2.55, session CGS_BRT26CX64OuSP1xJg.


> **v3.21 UPDATE (2026-08-03, kaizen — ODR v3.0 session closeout C1):**
> Red-team: direct parent-agent audit of session R8ZWb04K. HARD: 0. SOFT: 1. DESIGN: 0.
> Changes:
> (1) [SOFT] **C1 — R2 sync path allowlist**: skill-update artifacts (kaizen proposals,
>     remediation handoffs) MUST NOT be synced into production paper prefixes
>     (`qnfo-releases/releases/YYYY/MM/<slug>/`). Only verified paper deliverables
>     (.md, .pdf, PROVENANCE-BUNDLE.zip) belong in paper prefixes. Skill remediation
>     artifacts go to `qnfo-releases/skills/` or `.deepchat/artifacts/`. Case: ODR v3.0
>     closeout had remediation handoffs in the paper prefix after cleanup.
> Cross-reference: research v2.48, kaizen v1.8, session R8ZWb04K4BHAldwEqCX4b.


> **v3.1–v3.20 COLLAPSED HISTORY (20 banners, kaizen de-bloat 2026-08-03):**
> These historical version banners have been collapsed into this summary.
> Full content preserved in git history and skills-archive. Active content below.
  - v3.20: 2026-08-03, kaizen — D1-BIND-1 + VECTORIZE-SILO-1 anti-pattern migration
  - v3.19: 2026-08-02, kaizen — MCP OAuth loopback protocol; NO default browser
  - v3.18: 2026-08-02, kaizen — memory-to-skill migration + CF tool discoverability
  - v3.17: 2026-08-02, kaizen — STALE-AUDIT-1 anti-pattern + red-team v2 validation
  - v3.16: 2026-08-02, kaizen — autonomous P0 remediation session
  - v3.15: 2026-08-02, kaizen — Workers baseline + paper auto-indexing
  - v3.14: 2026-08-01, kaizen — wrangler environment + R2 verification false-negatives
  - v3.13: 2026-07-31, no-dashboard kaizen
  - v3.12: 2026-07-31, red-team kaizen — PowerShell gate + MCP-first execution
  - v3.11: 2026-07-30, LoS codification kaizen
  - v3.10: 2026-07-30, live-incident red-team kaizen
  - v3.9: 2026-07-29, MCP-Driven Operations red-team + kaizen
  - v3.8: 2026-07-29, 17-MCP coverage — FULL COVERAGE
  - v3.7: 2026-07-29, 10-MCP coverage + infra audit
  - v3.6: 2026-07-29, 9-MCP coverage + red-team audit
  - v3.5: 2026-07-25, wrangler false-negative + structured-schema kaizen
  - v3.3: 2026-07-21, phantom-claim audit Added the **Tool-Call
  - v3.4: 2026-07-21, orphan-script audit Deleted
  - v3.1: 2026-07-20, Pinata quota exceeded) — SUPERSEDED, script DELETED v3.4:**
  - v3.2: 2026-07-20, red-team audit Deprecated "R2→IPFS Bridge"


> **Merges 18:** cloudflare + cloudflare-deployer + cloudflare-one + cloudflare-email-service + email + infrastructure-audit + web-perf + workers-best-practices + wrangler + cloudflare-mcp-servers + logpush (v3.7) + browser-mcp + dns-analytics + containers-mcp + casb-mcp + autorag-mcp + blog-mcp + dex-mcp (v3.8)
> **Added v3.0:** Worker Consolidation Pattern, R2→IPFS Bridge, DNSLink Deployment, 4-D Architecture
> **Related:** Always load with `qnfo-core` for production immutability gates + due diligence. Load `research` for 4-D distribution pipeline.
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

# WBS-CODED PLAN (per docs/WBS-AGENT-PROTOCOL.md). Priority field carries WBS code.
# Each step MUST include a verifiable acceptance criterion (exit code, count threshold, cross-ref match).
update_plan([
  {"step": "CLD-E0-T01: Gather Workers list + details + source code (MCP: workers_list, workers_get_worker, workers_get_worker_code) → expect count=10, confirm all handlers exist", "status": "pending", "priority": "CLD-E0-T01"},
  {"step": "CLD-E0-T02: Run url-health-check.js → probe all public URLs, expect exitCode=0 Tier-1 CRITICAL=0", "status": "pending", "priority": "CLD-E0-T02"},
  {"step": "CLD-E0-T03: Run availability-audit.js → full LoS standards audit, expect exitCode=0 all CRITICAL=0 WARNING≤3", "status": "pending", "priority": "CLD-E0-T03"},
  {"step": "CLD-E0-T04: Verify Worker health + data-dependent routes → ≥2 data routes per Worker return 200 (KIF-50 gate)", "status": "pending", "priority": "CLD-E0-T04"},
  {"step": "CLD-E0-T05: Audit DNS zones → check empty zones (KIF-52), redirects (KIF-51), 522-RISK, CNAME chains", "status": "pending", "priority": "CLD-E0-T05"},
  {"step": "CLD-E0-T06: Cross-system integrity → D1 paper count matches KG Paper nodes (KIF-23), Vectorize search returns results", "status": "pending", "priority": "CLD-E0-T06"},
  {"step": "CLD-E0-T07: Synthesize findings → priority fix queue with verification protocol, store in memory, deliver report", "status": "pending", "priority": "CLD-E0-T07"},
])

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — MANDATORY)

No claim that a Worker is "deployed", a DNS record is "live", a D1 write
"succeeded", an R2 object "exists", or an infrastructure issue is "fixed"
may appear in a response without an actually-invoked tool call in the SAME
turn whose output is shown. Future-tense or narrative-only claims
("this should now route correctly", "the deploy will fix it") are PHANTOM
CLAIMS per `qnfo-core` §9.11 Rule 14 — BLOCKED.

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

**HEALTH CHECK SCRIPT:** `scripts/fleet-mcp-health-check.py` (this skill) probes ALL 17
configured Cloudflare MCP servers — token-cache presence + MCP initialize probe for the 14
OAuth servers, POST-initialize probe for the 3 public servers. Run it to detect
`invalid_token` / expired / missing-token fleet-wide BEFORE errors surface in the UI
(2026-08-03 outage class). Integrated into the `kaizen-watchtower-daily` cronjob.
Exit codes: 0 = all live, 1 = warnings (no-token/expired), 2 = failures.

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
5. **Cache the token** to `<hash>_tokens.json` in the same mcp-remote dir (format:
   `{access_token, token_type, expires_in, scope, refresh_token}`). Verify with
   `POST /mcp` `initialize` → HTTP 200 (`serverInfo.name`, `version`).
6. **Agent-level MCP tools may still time out** until the host app re-initializes the MCP
   connection — that is an app-level reconnect, not an OAuth problem.

**Failure modes (both confirmed live 2026-08-02):**
- **Expired code**: manual exchange in a separate tool call → `invalid_grant`. Fix: auto-exchange in listener.
- **Session browser not logged in**: YoBrowser lacks the Cloudflare session → login redirect.
  Fix: stop and report; never spawn the default browser.
- **Fleet-wide token expiration (FLEET-OAUTH-1, 2026-08-03)**: Tokens expire silently across all
  14 OAuth servers. Only `cloudflare-observability` had a cached token at time of audit;
  the other 13 servers returned `invalid_token` on every request with zero cached tokens.
  Fix: disable/re-enable each server in DeepChat MCP settings, OR use the Token Refresh
  Protocol below to auto-refresh all 14 tokens without browser consent once each server has
  been authenticated at least once.
- **mcp-remote v0.1.37 naming**: uses `_tokens.json` (plural), not `_token.json` (singular).

### Token Refresh Protocol (v3.23 — MANDATORY for fleet-wide OAuth renewal)

**BUNDLED SCRIPT:** `scripts/fleet-oauth-refresh.py` (this skill) implements the full
protocol below — run it with `--verify` to refresh AND probe every cached token:
```bash
python scripts/fleet-oauth-refresh.py --verify     # refresh + MCP initialize verify
python scripts/fleet-oauth-refresh.py --dry-run    # report what WOULD refresh
```
Cronjob `cloudflare-mcp-token-refresh-daily` (03:00 UTC) runs it automatically.
Servers without a token report `[NO-TOKEN]` → needs one-time browser OAuth.

After at least ONE successful browser-based OAuth flow per server (producing a token cache),
subsequent token refreshes can be automated WITHOUT browser consent using the `refresh_token` grant:

```python
import urllib.request, json, os, hashlib

CACHE_DIR = os.path.expandvars(r"%USERPROFILE%\.mcp-auth\mcp-remote-0.1.37")
SERVER_URL = "https://observability.mcp.cloudflare.com/mcp"
HASH = hashlib.md5(SERVER_URL.encode()).hexdigest()

# Read existing token cache
with open(os.path.join(CACHE_DIR, f"{HASH}_tokens.json")) as f:
    token = json.load(f)

# Exchange refresh_token for new access_token (no browser needed)
data = urllib.parse.urlencode({
    "grant_type": "refresh_token",
    "refresh_token": token["refresh_token"],
    "client_id": json.load(open(os.path.join(CACHE_DIR, f"{HASH}_client_info.json")))[
        "client_id"
    ],
}).encode("ascii")

resp = urllib.request.urlopen(
    urllib.request.Request(
        f"{SERVER_URL.rstrip('/mcp')}/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"},
    )
)
new_token = json.loads(resp.read().decode())

# Cache refreshed token (access_token + refresh_token both rotated)
with open(os.path.join(CACHE_DIR, f"{HASH}_tokens.json"), "w") as f:
    json.dump(new_token, f, indent=2)

# Verify
verify_req = urllib.request.Request(
    SERVER_URL,
    data=json.dumps({"jsonrpc": "2.0", "method": "initialize", ...}).encode(),
    headers={"Authorization": f"Bearer {new_token['access_token']}", 
             "Accept": "application/json, text/event-stream", "User-Agent": "Mozilla/5.0"},
)
print(f"Refresh: {'OK' if urllib.request.urlopen(verify_req).status == 200 else 'FAIL'}")
```

**Key behaviors verified live 2026-08-03:**
- `refresh_token` grant works without browser consent (✅ HTTP 200)
- Access token rotated (✅ new `access_token` issued)
- Refresh token rotated (✅ old `refresh_token` invalidated, new one issued)
- Scopes preserved across refresh (✅ all scopes unchanged)
- MCP initialize succeeds post-refresh (✅ HTTP 200, server info returned)
- Token valid for 3600s (60 min) per refresh cycle

**Fleet-wide renewal strategy:** Once all 14 OAuth servers have been authenticated at least
once (via DeepChat MCP settings disable/re-enable), a single Python script can iterate all
14 hashes and refresh every token. This eliminates the 13-server manual re-auth burden.

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
  "send_email": [{ "name": "SEND_EMAIL" }]
}

// In Worker — MODERN Email Service object API (v2026):
// send() takes an object builder, NOT the deprecated positional EmailMessage constructor
await env.SEND_EMAIL.send({
  to: "recipient@example.com",
  from: "me@example.com",
  subject: "Subject line",
  text: "Plain text body",
  html: "<p>HTML body</p>"
});
```

**CRITICAL — EmailMessage API change (2026-08-03, qnfo-email v1.5):**
The old `new EmailMessage(from, to, subject, body, html)` positional constructor is
DEPRECATED. It silently produces `{"error":"missing From: header"}` because the runtime
no longer maps positional args to headers. Use the object builder:
`send({ to, from, subject, text, html })`. Response: `{ messageId: string }`.
Cross-ref: email-composer v2.0, qnfo-email Worker v1.5, docs
`/email-service/api/send-emails/workers-api/`.

**Send binding restriction semantics (docs /email-service/configuration/send-bindings/):**
- No attributes → send to ANY verified destination address
- `destination_address` → send ONLY to that single address (recipient restriction!)
- `allowed_destination_addresses` → recipient allowlist
- `allowed_sender_addresses` → sender allowlist
For general send capability, use NO restriction attributes. Setting `destination_address`
silently blocks all other recipients with `email to X not allowed`.

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
| `research` | D1 living-paper, R2 releases, papers-server Worker, Zenodo | search_papers, query_graph, workers_list | ✅ v2.56 (verified 2026-08-04) |
| `knowledge` | D1 qnfo-graph, Vectorize, graph-api.qnfo.org | query_graph, search_memories, recall_facts | ✅ v2.2 (verify) |
| `system` | Skills R2 bucket (qnfo-skills), skill-sync.js | workers_list (sync target) | ✅ v2.4 |
| `code` | Workers deploys (MCP servers — merged code-review + mcp-builder v2.2) | workers_list, workers_get_worker | ✅ v2.2 (verified 2026-08-03) |
| `git-github` | GitHub-D1 sync (GitHub is canonical, D1 is mirror) | workers_list, query_graph | ✅ v2.5 (verified 2026-08-04) |
| `web-artifacts-builder` | Pages deploys, R2 static assets (merged frontend-design 2026-08-03) | workers_list, search_cloudflare_documentation | ✅ (verified 2026-08-03) |
| `documents` | R2 archive (r2-archive.js, merged doc-coauthoring 2026-08-03) | search_cloudflare_documentation, workers_list | ✅ v2.4 (verified 2026-08-03) |
| `windows-command-patterns` | D1 writes, bloat cleanup (merged bloat-cleanup 2026-08-03, Python-first, no PowerShell) | workers_list (verification) | ✅ v3.1 (verified 2026-08-03) |
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
| **D1-BIND-1: D1 `.bind().first()` chain throws 1101 on Workers (2026-08-03)** | `prepare(...).bind(slug).first()` throws 1101 (JS exception) for ALL slugs while `.first()` without `.bind()` works on the same table. Confirmed on qnfo-paper-indexer: handleSingle with `.bind()` → 1101; handleBatch without `.bind()` → OK. Fix: use parameterized `?1` syntax instead of `.bind()`, OR update `compatibility_date` to latest, OR wrap in try/catch with `.all()` fallback. Suspected D1 client version mismatch with `.bind()`. Discovered in session bWLdtP54lAjqfblr2cUKH (2026-08-02). |
| **VECTORIZE-SILO-1: Vectorize content indexed by one Worker is invisible to MCP search tools (2026-08-03)** | Qnfo-paper-indexer upserts 646 chunks via PAPER_VZ binding (qwav-research-v2), but `search_papers`/`search_papers_enriched` MCP tools return `{}` (empty). Probable cause: embedding model mismatch between indexer and searcher Workers, or Vectorize binding name mismatch in MCP server config. Fix: verify same embedding model (`@cf/baai/bge-base-en-v1.5`) used for both indexing and querying; verify Vectorize binding name in the MCP server's wrangler config matches the index alias. Discovered in session bWLdtP54lAjqfblr2cUKH (2026-08-02). |
| **Relying on durable memory for critical Cloudflare operational rules (2026-08-02)** | DeepChat memories are EPHEMERAL (may be purged). Critical rules (KIF-*, anti-patterns, endpoint maps, binding formats) MUST be embedded in this SKILL.md. Memory is for session outcomes, not operational authority. Migrate any rule found only in memory into this skill. |

| **EMAILMSG-1: Using deprecated positional `new EmailMessage(from, to, ...)` constructor (2026-08-03)** | The modern Email Service `send()` API takes an object builder: `send({to, from, subject, text, html})`. The old positional constructor silently fails with `missing From: header` — no exception, just a 500 at send time. Diagnosed live on qnfo-email Worker (v1.4→v1.5). Cross-ref: cloudflare v3.23 Email section. |
| **D1-UPDATE-PATTERN (2026-08-04): DELETE + INSERT silently returns OLD body_md** | When updating a paper's body_md in D1, use `UPDATE papers SET body_md = ? WHERE slug = ?` - NOT `DELETE FROM papers WHERE slug=?` followed by INSERT. DELETE+INSERT can silently leave the old row (FTS5 shadow-table interaction or write-consistency lag), making the paper appear "stuck" at an old size. Always re-read the row after write and verify body_len AND doi match expected values. Cross-ref: SCS-1, research v2.55. |
| **SEND-BIND-RESTRICT: Setting `destination_address` on send_email binding thinking it's the From (2026-08-03)** | `destination_address` RESTRICTS the recipient to that single address (`email to X not allowed` for everything else). It is NOT the From/sender. For general send: no restriction attributes (unrestricted). To restrict senders: `allowed_sender_addresses`. Diagnosed live on qnfo-email Worker. |
| **FLEET-OAUTH-1: Single-server OAuth re-auth leaves fleet-wide gap — 13/14 MCP servers return `invalid_token` (2026-08-03)** | When one Cloudflare MCP server's OAuth token expires, it's likely ALL 14 OAuth servers' tokens are expired. Authentication one server leaves the other 13 dead. Fix: (1) disable/re-enable ALL 14 servers in DeepChat MCP settings (~65 seconds, 39 clicks), OR (2) after each server has been authenticated once, use the Token Refresh Protocol (refresh_token grant) to auto-renew all 14 tokens without browser consent. Session -3rxrml7G5tAjlb77t9E1: only observability authenticated; 13 servers (cloudflare main, bindings, builds, ai-gateway, graphql, auditlogs, logs, browser, dns-analytics, containers, casb, autorag, dex) returned invalid_token and had zero cached tokens. |
| **OAUTH-REFRESH-1: Not using `refresh_token` grant after first-time OAuth authentication, forcing manual browser re-auth every hour (2026-08-03)** | Every Cloudflare MCP OAuth token cache includes `refresh_token` with `offline_access` scope. The `grant_type=refresh_token` flow at each server's `/token` endpoint works server-side without browser consent — proven live 2026-08-03: access token refreshed, refresh token rotated, MCP initialize HTTP 200. Fix: implement automated fleet-wide token refresh script using refresh_token grants. See §Token Refresh Protocol. |

| **AUDIT-FALSE-POSITIVE-1: `availability-audit.js` flags legitimate Worker behavior as CRITICAL (2026-08-04)** | Many W-S2 and W-S4 audit findings are false positives: GET /sync returns 404 because it requires POST; GET /mcp returns 404 because it's an MCP protocol endpoint; GET /ask?q=test on qwav returns 404 because it requires POST with JSON body; GET /papers on qwav returns 404 because qwav doesn't serve papers; /debug/* returning 200 on paper-indexer is the catch-all handler returning status JSON, not destructive routes. Fix: route-map per Worker to distinguish "route doesn't exist" from "route exists but requires different method"; W-S4 probe must check response BODY for destructive keywords (DROP/CREATE/INSERT), not just HTTP 200. Case: 2026-08-04 infrastructure audit — 6 of 11 CRITICAL findings were false positives. |
| **PAGES-DEPLOY-METADATA-1: Pages deploy stage shows "[object Object]" — JSON parsing bug (2026-08-04)** | The `availability-audit.js` P-S3 check calls the Pages API and parses `latest_deployment.latest_stage` but the field is an object, not a string. All 5 Pages projects show "[object Object]" for latest deploy stage. Fix: access `latest_deployment.latest_stage.name` or `JSON.stringify` the stage object. Found in 2026-08-04 infrastructure audit — P-S3 build freshness verification is impossible. |
| **WRANGLER-PATH-REGRESSION-1: Wrangler PATH fix from prior session silently reverts (2026-08-04)** | The permanent wrangler PATH fix (npm config set prefix + setx Path) applied 2026-08-01 was reverted by 2026-08-04 — `wrangler --version` returns "not recognized". The npm global prefix at `C:\Users\LENOVO\npm-global` may have been cleared or overwritten. Fix: re-apply the permanent fix from the Wrangler Environment Setup section AND add a verification step to `availability-audit.js` or `url-health-check.js` that checks `wrangler --version` as a pre-flight gate. |
| **GATEWAY-PROD-STALE-1: `qnfo-gateway-production` created 2026-07-31, never deployed with HTTP routes (2026-08-04)** | The staging/production variant Worker was created 2026-07-31 and returns 404 on /health. Likely a test Worker that was never deployed with `workers_dev = true` (KIF-61) or never had HTTP route handlers. If unused, delete to prevent drift from the 9-Worker baseline. Flagged in 2026-08-04 infrastructure audit — `workers_list` shows 10 Workers (baseline 9), but "+qnfo-email" is legitimate growth while "+qnfo-gateway-production" is unexplained drift. |

## Version

**API-FAILURE PROTOCOL (HARD):** When any API call returns 403/401/404, run the API-Failure Self-Diagnosis Protocol (windows-command-patterns S-1.0.6): STOP -> VERIFY your HTTP method/headers -> COMPARE with curl -> THEN consider infrastructure. The bug is ALWAYS your code until proven otherwise (kaizen BLAME-EXTERNAL-1).

Current: **v3.27** (research — N-2 nomenclature: H1 version-header delimiter standardized from -- to — (em-dash) per qnfo-core N-2 ecosystem audit; 2026-08-04) (cloudflare — infrastructure audit anti-patterns: AUDIT-FALSE-POSITIVE-1, PAGES-DEPLOY-METADATA-1, WRANGLER-PATH-REGRESSION-1, GATEWAY-PROD-STALE-1; WBS-coded execute_plan; Worker baseline 10; corrupted anti-pattern rows repaired; 2026-08-04)
