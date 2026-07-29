---
name: cloudflare
description: ULTRA-CONSOLIDATED Cloudflare Full-Stack (9-MCP Coverage) -- Workers, Pages, D1, R2, KV, Vectorize, Queues, Durable Objects, AI, DNS, Zero Trust, Email, WAF, CDN, Turnstile, Infrastructure Audit, MCP Server Management. The ONLY infrastructure skill. NEVER treat Cloudflare components in isolation -- ALL code, outputs, and deliverables must evaluate the full Cloudflare stack end-to-end.
version: "3.6"
triggers: ["cloudflare-deployer", "deploy", "wrangler", "Pages", "Workers", "R2", "D1", "DNS", "KV", "Vectorize", "Queues", "AI", "Durable Objects", "Zero Trust", "Access", "Gateway", "WARP", "Tunnel", "WAF", "CDN", "Turnstile", "email", "SPF", "DKIM", "DMARC", "infrastructure", "audit", "health check", "orphan", "lifecycle", "worker route", "route conflict", "522", "CNAME", "Cloudflare", "upload", "migrate", "Pages Functions", "Workers for Platforms", "Cron Triggers", "Tail Workers", "Smart Placement", "Hyperdrive", "Secrets Store", "Pipelines", "Browser Rendering", "Zaraz", "Argo", "Spectrum", "TURN", "Network Interconnect", "Cache Reserve", "Bot Management", "API Shield", "DDoS", "Analytics Engine", "Web Analytics", "GraphQL API", "Observability", "Miniflare", "Sandbox", "Workerd", "Terraform", "Pulumi", "Snippets", "Containers", "Workflows", "Artifacts", "R2 Data Catalog", "R2 SQL", "Static Assets", "Bindings", "Image", "Stream", "RealtimeKit", "Flagship", "feature flags", "Agents SDK", "AI Gateway", "AI Search", "Workers AI", "do", "durable", "sandbox", "turnstile", "web-perf", "thin client", "IaC", "consolidation", "4-D", "IPFS bridge", "DNSLink", "Arweave", "Filecoin", "distributed", "durable", "discoverable", "duplicated"]
related: ["qnfo-agent", "research"]
priority: 1
platform: cloudflare
autonomous: true
self_sufficient: true
---

# CLOUDFLARE -- v3.7 (10-MCP Coverage + Full-Stack, red-team verified, v2.8 no external IPFS)

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


> **Merges 11:** cloudflare + cloudflare-deployer + cloudflare-one + cloudflare-email-service + email + infrastructure-audit + web-perf + workers-best-practices + wrangler + cloudflare-mcp-servers + logpush (v3.7)
> **Added v3.0:** Worker Consolidation Pattern, R2→IPFS Bridge, DNSLink Deployment, 4-D Architecture
> **Related:** Always load with `qnfo-agent` for production immutability gates + due diligence. Load `research` for 4-D distribution pipeline.
> **Full-Stack Mandate:** Evaluate Workers, D1, R2, KV, DO, AI, Vectorize, Queues, Pages, DNS, Zero Trust, Email, WAF, CDN as ONE integrated platform. NEVER isolate components.

## execute_plan

update_plan([
  {"step": "Identify service via decision trees below", "status": "pending"},
  {"step": "Check full-stack cross-service implications", "status": "pending"},
  {"step": "Execute with Cloudflare-native tools (wrangler CLI, REST API, Dashboard)", "status": "pending"},
  {"step": "Verify deployment health + DNS integrity + lifecycle state", "status": "pending"},
  {"step": "Audit: check for orphans, 522-RISK, CNAME chains, resource drift", "status": "pending"},
  {"step": "Core Distribution Gate: Verify GitHub, Zenodo, R2, D1/KG layers", "status": "pending"},
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
6. If verification cannot be run in this turn, the response MUST read `[NOT-VERIFIED: <reason>]` — never "deployed", "fixed", "healthy", or "confirmed".

---

## DeepChat MCP Server Coverage (v3.6 — 9 of 17 available)

DeepChat connects to Cloudflare MCP servers via `npx mcp-remote` (stdio → hosted Streamable HTTP). All servers expose `/mcp` and `/sse` (compatibility alias) through MCP SDK v2 factories. OAuth triggers automatically on first use.

### Configured (10/17 — 59% coverage)

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

### Not Configured (7 — add on demand)

| MCP Server | Endpoint | Priority |
|:-----------|:---------|:--------:|
| `cloudflare-browser-mcp-server` | `browser.mcp.cloudflare.com/mcp` | LOW (already have qnfo-browser-run) |
| `dns-analytics` | `dns-analytics.mcp.cloudflare.com/mcp` | LOW |
| `containers-mcp` | `containers.mcp.cloudflare.com/mcp` | LOW |
| `cloudflare-casb-mcp-server` | `casb.mcp.cloudflare.com/mcp` | LOW |
| `cloudflare-autorag-mcp-server` | `autorag.mcp.cloudflare.com/mcp` | LOW |
| `cloudflare-blog` | `blog.mcp.cloudflare.com/mcp` | TRIVIAL |
| `dex-analysis` | `dex.mcp.cloudflare.com/mcp` | TRIVIAL |

### MCP Verification Gate

Before claiming "MCP server X is working", verify with:
```bash
# All endpoints should return HTTP 401 (OAuth required) or HTTP 200 (public)
curl.exe -s -o NUL -w "%{http_code}" https://<subdomain>.mcp.cloudflare.com/mcp
```
- **401** = endpoint live, auth required (normal for OAuth servers)
- **404/530** = endpoint not deployed or DNS not propagated
- **200** = public endpoint (docs, radar)

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
### R2 CLI Syntax (wrangler v4+)
**CRITICAL:** wrangler v4 uses `{bucket}/{key}` as a single positional argument:
```bash
# CORRECT (v4+):
npx wrangler r2 object get qnfo-releases/path/to/file.md --remote --pipe
npx wrangler r2 object put qnfo-releases/path/to/file.md --file=local.md --remote

# WRONG (v3 and earlier, removed in v4):
npx wrangler r2 object get qnfo-releases "path/to/file.md" --remote --pipe  # FAILS
```
The `r2 object list` subcommand was removed in wrangler v4. Use the REST API for listings:
```bash
curl -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"   "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/r2/buckets/{BUCKET}/objects?prefix={PREFIX}"
```



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
Baseline: 7 (post-consolidation 2026-07-18).
**Fleet:** `qnfo-gateway` (unified API+graph+legal+papers, 17 routes), `qnfo-archive`, `qnfo-lifecycle` (v1.1 — 7 cron handlers with real logic, `/status` fixed), `qnfo-ai`, `qnfo-ipatent`, `qnfo-memory-mcp` (v1.0.1 — debug endpoints removed), `qnfo-qwav`

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
| Workers | 7 | 8-9 | 10+ |
| Pages Projects | 5 | 6-7 | 8+ |
| Vectorize Indexes | 4 | +/- 1 | +/- 2+ |
| R2 Buckets | 13 | +/- 1 | +/- 3+ |
| Queues | 1 | +/- 1 | +/- 2+ |
| KV Namespaces | 1 | +/- 1 | +/- 2+ |
| DNS Zones | 12 active | +/- 1 | +/- 3+ |
| 522-RISK | 0 | 1+ | -- |
| CNAME Chains | 0 | 1+ | -- |
| DEAD-WORKER | 0 | 1+ | -- |

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

## Retrieval Sources (Prefer over pre-training)

| Source | Method | Use for |
|:-------|:-------|:--------|
| Cloudflare docs | `search_cloudflare_documentation({query})` | Limits, pricing, API reference |
| Workers types | `npm pack @cloudflare/workers-types` | Type signatures, binding shapes |
| Wrangler config schema | `node_modules/wrangler/config-schema.json` | Config fields, binding shapes |

---

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
| Concluding "wrangler is not installed" from `npm ls -g wrangler`, a bare `where wrangler` miss, or a Python `subprocess.run()` PATH failure (KIF-19) | Run `node scripts/wrangler-check.js` — the ONLY sufficient test is `npx wrangler --version` + `npx wrangler whoami` executed directly via `exec`. Wrangler is invoked exclusively via `npx`, never globally installed. |
| Guessing D1/Zenodo/Workers/Buffer API request shapes from memory each session | Consult `references/d1-rest-api-schema.json`, `references/workers-deploy-metadata-schema.json` (this skill) and `../research/references/zenodo-deposit-schema.json`, `../research/references/buffer-graphql-schema.json` (research skill) BEFORE constructing the call. |
| `ON CONFLICT` upsert against a D1 table with FTS5 shadow tables (HTTP 400) | Use `scripts/d1-safe-write.js` (CHECK-THEN-WRITE, never a combined upsert) — see `references/d1-rest-api-schema.json`. |
| Large D1 write payloads built via PowerShell `ConvertTo-Json` silently corrupting to `"[object Object]"` (KIF-21) | Use `scripts/d1-safe-write.js` (Node-native JSON construction + mandatory length-verification re-GET) instead of PowerShell string-building for any payload > a few hundred characters. |
| Not configuring Cloudflare MCP servers that are directly relevant to QNFO operations (KIF-48) | DeepChat's `mcp-settings.json` must include all high-value Cloudflare MCP servers: `cloudflare` (main), `cloudflare-docs`, `cloudflare-bindings`, `cloudflare-builds`, `cloudflare-observability`, `cloudflare-ai-gateway`, `cloudflare-graphql`, `cloudflare-auditlogs`, and `cloudflare-radar`. See §DeepChat MCP Server Coverage for the canonical list. |
| Trusting that an MCP server is reachable without a live HTTP probe | Verify with `curl.exe -s -o NUL -w "%{http_code}" https://<subdomain>.mcp.cloudflare.com/mcp` — 401 = live (auth required), 404/530 = not deployed. Never claim an MCP server "is working" from config validation alone. |
