---
name: infrastructure-audit
description: Audit all Cloudflare infrastructure resources (D1, R2, Workers, Pages, Vectorize, Queues). Reports orphaned/duplicate resources, state mismatches, and health issues. Use when checking infrastructure health, pre-execution validation, or session startup due diligence.
version: "1.0"
---

# INFRASTRUCTURE AUDIT SKILL — v1.0

> **On-demand skill.** Load via `skill_view('infrastructure-audit')` for comprehensive Cloudflare infrastructure health checks.

---

## Purpose

The #1 cause of duplicate work in QNFO is agents executing tasks without checking live infrastructure state. This skill automates the Infrastructure State Verification Gate (qnfo-agent §3.2 step 1.6) by querying all Cloudflare resources and comparing against handoff/Discovery Index claims.

## When to Use

| Trigger | Action |
|:--------|:-------|
| Session startup | Full audit + health report |
| "Check infrastructure" | Run all checks |
| "Audit Cloudflare resources" | Full audit with recommendations |
| Before any upload/deploy/data task | Quick pre-execution check |
| "What's orphaned/duplicate?" | Orphan detection only |

## Workflow

### Phase 1: Full Infrastructure Audit

Run the audit script to query all Cloudflare services:

```python
import urllib.request, json, os

TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'

def cf(endpoint):
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/{endpoint}'
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {TOKEN}')
    return json.loads(urllib.request.urlopen(req, timeout=15).read())

# Query all services
d1 = cf('d1/database')
kv = cf('storage/kv/namespaces')
vec = cf('vectorize/indexes')
pages = cf('pages/projects')
workers = cf('workers/scripts')
queues = cf('queues')

print(f'D1: {len(d1.get("result",[]))} | KV: {len(kv.get("result",[]))} | Vectorize: {len(vec.get("result",[]))}')
print(f'Pages: {len(pages.get("result",[]))} | Workers: {len(workers.get("result",[]))} | Queues: {len(queues.get("result",[]))}')
```

### Phase 2: Orphan Detection

Compare live resources against Discovery Index to find unregistered or stale entries.

### Phase 3: Health Recommendations

Based on audit findings, report orphaned resources, stale entries, and cleanup recommendations.

## Output Format

```
# INFRASTRUCTURE AUDIT REPORT
**Date:** YYYY-MM-DD | **Auditor:** QNFO Agent

## Resource Inventory
| Resource | Count | Status |
|:---------|:-----:|:------:|
| D1 Databases | 4 | OK |
| KV Namespaces | 2 | OK |
| Vectorize Indexes | 1 | OK |
| Pages Projects | 10 | OK |
| Workers | 18 | OK |
| Queues | 4 | OK |

## Issues Found
None — all resources accounted for.

## Recommendations
No action needed.
```

## Integration

- Runs automatically at session start (qnfo-agent §3.2 step 1.6)
- Pre-execution gate: before any upload/deploy task
- Feeds into Discovery Index updates

---

*infrastructure-audit v1.0 — Comprehensive Cloudflare infrastructure health checks. Pre-execution validation gate.*
