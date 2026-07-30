# QNFO Cloudflare Level-of-Service Standards

> **Version:** v1.0 (2026-07-30)
> **Derived from:** KIF-50 (Binding Loss), KIF-51 (Account Redirect), KIF-52 (Empty Zones), KIF-53 (API-Worker Domain Routing)
> **Parent skill:** cloudflare v3.11+
> **Canonical home:** `references/level-of-service-standards.md`

---

## Overview

These standards define the **minimum acceptable state** for every Cloudflare asset in the QNFO ecosystem. They are structured into three layers — **Pages** (static/content sites), **Workers** (dynamic API/application logic), and **DNS/Domains** (routing and resolution). Every standard has:

- An **ID** (D-S1, W-S4, etc.)
- A **severity** — `CRITICAL` (public outage), `WARNING` (degraded), `INFO` (drift/noise)
- A **test protocol** — the exact steps to verify compliance
- A **remediation** — the exact steps to fix a failure
- A **verification gate** — how to confirm the fix worked

---

## Tier Definitions

| Tier | Description | Standard Coverage |
|:-----|:------------|:------------------|
| **Tier 1 — Production** | Public-facing domains serving users (qnfo.org, papers.qnfo.org, qwav.org, etc.). All CRITICAL standards apply. | Full |
| **Tier 2 — Internal Tooling** | API workers, MCP servers, lifecycle/archive cron workers. WARNING+ standards apply. | Full minus redirect checks |
| **Tier 3 — Archive/Dormant** | Projects/workers in STALE or ARCHIVED lifecycle state. INFO standards only. | Baseline |

---

## PAGE LEVEL-OF-SERVICE STANDARDS

### P-S1: Root Document Reachable **[CRITICAL for Tier 1]**

**Requirement:** Every Pages project with a custom domain must return HTTP 200 on `GET /`. An HTTP 301/302 redirect to a reachable destination is acceptable. An HTTP 401 (Zero Trust Access gate) is acceptable for auth-gated projects. HTTP 404, 500, 502, 503, or 522 is a CRITICAL failure.

**Test Protocol:**
```bash
curl -sI -o /dev/null -w "%{http_code}" https://{domain}/
```
Or via Node:
```js
const r = await fetch(`https://${domain}/`, { redirect: 'manual' });
console.log(r.status); // Must be 200, 301, 302, or 401
```

**Remediation:**
1. If 522: domain is not registered on the Pages project. Add it via Dashboard → Pages → {project} → Custom Domains.
2. If 500: Pages build failed. Check `cloudflare-builds` MCP or Dashboard → Pages → {project} → Deployments.
3. If 404: project may have been deleted. Check `workers_list` + Pages list against baseline.
4. If 301 to external: check account-level redirect rulesets (KIF-51).

**Verification Gate:** `curl -sI https://{domain}/ | head -1` must show `HTTP/2 200` (or 301/302/401).

---

### P-S2: Zero 522-RISK **[CRITICAL]**

**Requirement:** Every CNAME record pointing to a `*.pages.dev` domain must have a matching custom domain registration on the target Pages project. A CNAME to `{project}.pages.dev` without the apex domain listed in the project's Custom Domains tab produces a 522 error.

**Test Protocol:**
```js
// 1. List all DNS records with content containing ".pages.dev"
// 2. For each, extract the project name
// 3. Check if the apex domain is registered on that Pages project
const pagesDns = zones.flatMap(z => z.dns_records.filter(r => 
  r.type === 'CNAME' && r.content?.includes('.pages.dev')
));
for (const record of pagesDns) {
  const project = record.content.split('.')[0]; // "qnfo-hub" from "qnfo-hub.pages.dev"
  const domains = await cf(`/accounts/${ACCOUNT}/pages/projects/${project}/domains`);
  const match = domains.result?.find(d => d.name === record.name);
  if (!match) flag522Risk(record, project);
}
```

**Remediation:** Register the domain in Dashboard → Pages → {project} → Custom Domains → Add Domain.

**Verification Gate:** `curl -sI https://{domain}/` returns HTTP 200, not 522.

---

### P-S3: Successful Recent Build **[WARNING]**

**Requirement:** Every active Pages project must have at least one successful deployment within the last 30 days, OR be explicitly tagged as `dormant` in D1 `portfolio-state`.

**Test Protocol:**
```js
// Check cloudflare-builds MCP or REST:
// GET /accounts/{ACCOUNT}/pages/projects/{project}/deployments?per_page=1
// Verify latest deployment.created_on > 30 days ago AND latest_deployment.stage === 'success'
```

**Remediation:**
1. Re-trigger build via `npx wrangler pages deploy` or Dashboard.
2. If project is intentionally dormant, tag it in `portfolio-state.resources` with `status: 'dormant'`.

**Verification Gate:** Latest deployment shows `stage: "success"` and date within threshold.

---

### P-S4: DNS Resolution Integrity **[CRITICAL for Tier 1]**

**Requirement:** Every custom domain on a Pages project must resolve in DNS. Proxied records must resolve to Cloudflare IPs. Unproxied records must point to valid origin IPs.

**Test Protocol:**
```bash
# Proxied records: dig should return Cloudflare IPs (104.x.x.x, 172.64.x.x)
dig +short {domain}
# Verify returned IPs are in Cloudflare's range (check for 104.* or 172.64/65.*)

# Unproxied records: verify origin reachable
curl -sI http://{origin_ip}/ # Should return something (even a redirect)
```

**Remediation:**
1. If domain returns NXDOMAIN: DNS record missing or deleted. Add CNAME record in the zone.
2. If proxied but returns non-Cloudflare IPs: the `proxied: true` flag may be off. Re-enable in Dashboard DNS tab.

**Verification Gate:** `dig +short {domain}` returns at least one valid IP.

---

### P-S5: D1 Traceability **[INFO]**

**Requirement:** Every Pages project should have a row in D1 `portfolio-state.resources` (table: `audit_pages`) to prevent unexplained disappearance (I-05 still open: 5 projects vanished without audit trail).

**Test Protocol:**
```sql
SELECT project_name, status, last_deployed FROM portfolio_state.resources 
WHERE type = 'pages' AND project_name = ?
```

**Remediation:** Insert or update the D1 row with current project metadata.

**Verification Gate:** `SELECT` returns exactly 1 row.

---

## WORKER LEVEL-OF-SERVICE STANDARDS

### W-S1: Health Endpoint **[CRITICAL]**

**Requirement:** Every Worker must expose a `/health` (or `/status` for cron Workers) endpoint that returns HTTP 200 with a JSON body containing at least `{"status": "ok"}` or equivalent.

**Test Protocol:**
```bash
# Workers.dev subdomain (always available):
curl -s https://{worker}.{subdomain}.workers.dev/health

# If no /health, try /status:
curl -s https://{worker}.{subdomain}.workers.dev/status

# For cron-only Workers: /status is the canonical endpoint
```

**Remediation:** Add a `/health` route handler returning `new Response(JSON.stringify({status:"ok"}), {headers:{"content-type":"application/json"}})`.

**Verification Gate:** `curl -s https://{worker}.q08.workers.dev/health | grep -q '"ok"' && echo PASS || echo FAIL`

---

### W-S2: Binding Integrity Gate (KIF-50 Gate) **[CRITICAL for D1/R2 Workers]**

**Requirement:** For every Worker with D1, R2, KV, or Vectorize bindings, at least TWO distinct data-dependent routes must return HTTP 200 with non-trivial body content (≥ 50 bytes). A passing `/health` endpoint is INSUFFICIENT — `/health` typically doesn't touch data bindings.

**Test Protocol:**
```bash
# Gateway Worker example:
curl -sI https://qnfo-gateway.q08.workers.dev/papers    # Must 200
curl -sI https://qnfo-gateway.q08.workers.dev/stats     # Must 200
# For AI Workers:
curl -sI https://qnfo-ai.q08.workers.dev/v1/search?q=test   # Must 200
# For IPatent Workers:
curl -sI https://qnfo-ipatent.q08.workers.dev/api/disclosures  # Must 200
```

**Remediation:** If routes return HTTP 500 with "Cannot read properties of undefined (reading 'prepare')" — the binding is MISSING. Redeploy via `npx wrangler deploy` from a properly-configured `wrangler.toml`/`wrangler.jsonc`.

**Verification Gate:** At least 2 data routes return HTTP 200, not 500.

---

### W-S3: Active Deployment Window **[WARNING]**

**Requirement:** Every Worker must have a deployment within the last 90 days, OR be explicitly tagged as `archive`/`dormant`.

**Test Protocol:**
```bash
npx wrangler deployments list --name {worker}
```
Or via `cloudflare-builds` MCP.

**Remediation:** If Worker is still in use, redeploy current code. If dormant, tag it.

**Verification Gate:** Latest deployment date ≤ 90 days ago.

---

### W-S4: No Unauthenticated Debug Routes **[CRITICAL]**

**Requirement:** No production Worker may expose `/debug/*`, `/init/*`, or `/seed/*` routes that execute DROP TABLE, CREATE TABLE, or schema-reset logic without authentication. Root cause of the 2026-07-18 `living-paper` 616→3 row data loss.

**Test Protocol:**
```bash
# Probe known dangerous patterns:
curl -sI https://{worker}.q08.workers.dev/debug/init
curl -sI https://{worker}.q08.workers.dev/debug/seed
# Any non-404 response is a flag. HTTP 200 = CRITICAL.
```

**Remediation:** Remove the route OR gate it behind an auth header check + non-production compatibility flag.

**Verification Gate:** All debug/init/seed probes return HTTP 404.

---

### W-S5: Workers.dev Subdomain Reachable **[WARNING]**

**Requirement:** Every Worker's `.workers.dev` subdomain must be reachable. This is the canary URL — if it's down, custom domains are likely also affected.

**Test Protocol:**
```bash
curl -sI https://{worker}.{subdomain}.workers.dev/health
```

**Remediation:** If 404, the Worker may not exist or the subdomain may be disabled. Check `workers_get_worker`.

**Verification Gate:** `.workers.dev/health` returns HTTP 200.

---

### W-S6: Binding Declaration Consistency **[WARNING]**

**Requirement:** Every binding declared in a Worker's `wrangler.toml`/`wrangler.jsonc` must be referenced in the Worker's fetch handler code. A binding that is declared but never used is a dead binding (found in both `qnfo-ipatent` and `qnfo-qwav` in 2026-07-18 audit).

**Test Protocol:**
```js
// 1. Fetch Worker bindings via cloudflare-bindings MCP or REST
// 2. Fetch Worker source code via workers_get_worker_code
// 3. For each binding name, grep the source code
// 4. Flag any binding NOT found in source
```

**Remediation:** Either remove the unused binding from `wrangler.toml` OR add the code to use it.

**Verification Gate:** All declared bindings appear in source code.

---

## DNS/DOMAIN LEVEL-OF-SERVICE STANDARDS

### D-S1: Minimum DNS Records (KIF-52) **[CRITICAL]**

**Requirement:** Every active DNS zone must contain at least 1 DNS record (A, AAAA, CNAME, TXT, MX — any type). A zone with zero records resolves to nothing. 3 of 12 zones had this condition on 2026-07-30.

**Test Protocol:**
```bash
# For each active zone:
curl -s "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records?per_page=5" \
  -H "Authorization: Bearer $TOKEN" | jq '.result_info.total_count'
# If count === 0: CRITICAL
```

**Remediation:**
1. Add a proxied CNAME record pointing to an active gateway Worker domain.
2. Add a zone-level Worker route: `POST /zones/{ZONE_ID}/workers/routes` with `{pattern: "domain/*", script: "qnfo-gateway"}`.

**Verification Gate:** Zone returns `dns_records count ≥ 1`.

---

### D-S2: Domain Resolution **[CRITICAL]**

**Requirement:** Every custom domain that points to QNFO infrastructure must resolve in DNS (no NXDOMAIN, no SERVFAIL).

**Test Protocol:**
```bash
# Quick check:
nslookup {domain}
# Programmatic:
dig +short {domain} | grep -q '.' && echo RESOLVES || echo FAIL
```

**Remediation:**
1. NXDOMAIN: DNS record missing. Add appropriate CNAME/A record.
2. SERVFAIL: DNS configuration error. Check zone configuration in Cloudflare Dashboard.
3. Non-Cloudflare IP: proxying may be off. Toggle orange cloud in DNS tab.

**Verification Gate:** Domain resolves to at least 1 IP.

---

### D-S3: No CNAME Chains **[WARNING]**

**Requirement:** No CNAME record may point to another CNAME that itself points to a `*.pages.dev` or `*.workers.dev` domain. CNAME chains (A → B → C.pages.dev) break when intermediate names change.

**Test Protocol:**
```js
// For each CNAME record:
// Resolve its target. If target is also a CNAME, resolve that.
// If the chain terminates on *.pages.dev or *.workers.dev, it's valid but fragile.
// If chain length > 1, flag as WARNING.
```

**Remediation:** Replace the intermediate CNAME with a direct CNAME to the final Cloudflare target.

**Verification Gate:** All CNAMEs resolve in ≤ 1 hop.

---

### D-S4: No Dead Worker CNAMEs **[CRITICAL]**

**Requirement:** No CNAME record may point to a non-existent Worker's `.workers.dev` subdomain. A CNAME to `{deleted-worker}.{subdomain}.workers.dev` produces unreachable errors.

**Test Protocol:**
```js
// 1. List all CNAME records with content containing ".workers.dev"
// 2. Extract Worker name
// 3. Check if Worker exists in workers_list
```

**Remediation:** Either recreate the Worker or update the CNAME to a valid target.

**Verification Gate:** All Workers referenced in CNAME records exist in the fleet.

---

### D-S5: No Account-Level Redirect Intercept (KIF-51) **[CRITICAL for Tier 1]**

**Requirement:** No account-level `http_request_redirect` ruleset must silently intercept traffic to custom domains. These execute at Rules Engine position 5, BEFORE Workers (position 10), and redirect to external URLs. Found on 2026-07-30: `ipatent.me` was blocked by an account-level redirect to Google Cloud Run.

**Test Protocol:**
```bash
# For every custom domain:
curl -sv https://{domain}/ 2>&1 | grep -E "^(< HTTP|< location:|< Location:|cf-ray:)"
# If response is HTTP 301/302 with Location NOT pointing to Cloudflare:
```

**Remediation:** Requires manual Cloudflare Dashboard intervention: Manage Account → Configurations → Bulk Redirects/Single Redirects → delete the rule. API Tokens typically cannot manage account-level redirects.

**Verification Gate:** Domain returns HTTP 200 from QNFO infrastructure, not a redirect to an external URL.

---

### D-S6: At Least One Proxied Record **[INFO]**

**Requirement:** Every zone should have at least 1 proxied (orange-cloud) record to benefit from Cloudflare's CDN, DDoS protection, and WAF.

**Test Protocol:**
```bash
# Check proxied status:
curl -s "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records" \
  -H "Authorization: Bearer $TOKEN" | jq '.result[] | select(.proxied == true) | .name'
```

**Remediation:** Toggle the orange cloud on at least one A/CNAME record in the DNS tab.

**Verification Gate:** At least 1 record has `proxied: true`.

---

### D-S7: Worker Route Coverage **[WARNING]**

**Requirement:** Every domain that routes to a Worker must have a matching zone-level Worker route. Without this, Cloudflare's edge doesn't know which Worker to invoke for the domain.

**Test Protocol:**
```bash
curl -s "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/workers/routes" \
  -H "Authorization: Bearer $TOKEN" | jq '.result[] | {pattern, script}'
```

**Remediation:**
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/workers/routes" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"pattern":"{domain}/*","script":"{worker}"}'
```

**Verification Gate:** GET /zones/{id}/workers/routes shows matching pattern for each routed domain.

---

## Unified Audit Protocol

### Full Availability Audit (all layers, all standards)

```bash
# Run the unified audit script:
skill_run cloudflare scripts/availability-audit.js

# Or via npx:
node "%USERPROFILE%\.deepchat\skills\cloudflare\scripts\availability-audit.js"
```

The script produces:

```
=== QNFO Availability Audit ===
Date: 2026-07-30T...
Account: quniverse
Workers: 7 | Pages: 5 | Zones: 12

--- Worker Tier ---
PASS  W-S1  qnfo-gateway       /health → 200
PASS  W-S2  qnfo-gateway       /papers → 200, /stats → 200
FAIL  W-S2  qnfo-ipatent       /api/disclosures → 500 (CRITICAL)
...

--- Page Tier ---
PASS  P-S1  qnfo.org           / → 200
FAIL  P-S2  522-RISK: ...      (CRITICAL)
...

--- DNS Tier ---
PASS  D-S1  qnfo.org           4 records
FAIL  D-S1  qnfo.net           0 records (CRITICAL)
...

=== SUMMARY ===
CRITICAL: 3  |  WARNING: 5  |  INFO: 2  |  PASS: 31
```

### Quick Health Probe (URL-level only)

```bash
skill_run cloudflare scripts/url-health-check.js
```

Probes all known public URLs and reports status/body size.

---

## Severity Escalation Rules

| Finding | Auto-Fix? | Escalation |
|:--------|:----------|:-----------|
| CRITICAL — Binding loss (KIF-50) | Yes (`npx wrangler deploy`) | Open tape handoff |
| CRITICAL — Empty zone (KIF-52) | Yes (add CNAME + route) | DNS propagation wait |
| CRITICAL — Account redirect (KIF-51) | No (needs Dashboard) | Flag for manual remediation |
| CRITICAL — 522-RISK | Yes (register custom domain) | Verify post-fix |
| WARNING — Dead binding | Maybe (need source analysis) | Flag for code review |
| INFO — D1 traceability gap | Yes (D1 INSERT) | None |
