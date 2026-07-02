---
name: worker-route-interference-audit
description: Detects Cloudflare Worker route conflicts where a more specific route silently intercepts traffic intended for another Worker or Pages project. Use when debugging Worker routing issues or during infrastructure audits.
version: 1.0
pinned: false
---

# WORKER ROUTE INTERFERENCE AUDIT — v1.0

## Why This Exists

**2026-07-02:** The `papers.qnfo.org/papers/*` → `seo-metadata-injector` Worker route silently intercepted ALL paper detail page traffic intended for the `papers-server` Worker (`papers.qnfo.org/*` route). The seo-metadata-injector Worker didn't have metadata for most paper slugs, so it fell through to `fetch(request)` which went to the static Pages origin — returning redirect pages. The papers-server Worker was deployed and working, but its route was **overridden** by the more specific route. This pattern is invisible in normal infrastructure audits.

## Detection Protocol

### Cloudflare Worker Route Precedence

Cloudflare Worker routes follow URL pattern specificity: more specific patterns take precedence over less specific ones. When two routes match the same URL, the more specific one wins.

| More Specific (wins) | Less Specific (loses) | Symptom |
|:---------------------|:----------------------|:--------|
| `papers.qnfo.org/papers/*` | `papers.qnfo.org/*` | `papers.qnfo.org/*` Worker appears non-functional |
| `api.example.com/v2/*` | `api.example.com/*` | V1 Worker handles all traffic, V2 never invoked |
| `*.example.com/special` | `*.example.com/*` | General Worker can't handle /special path |

### Detection Script

```python
import urllib.request, ssl, json, os

TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
ctx = ssl.create_default_context()

def cf(endpoint):
    url = f'https://api.cloudflare.com/client/v4/{endpoint}'
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {TOKEN}')
    return json.loads(urllib.request.urlopen(req, timeout=15, context=ctx).read())

# Step 1: Get ALL worker routes across ALL zones
zones = cf('zones?per_page=50').get('result', [])
all_routes = []
for z in zones:
    zone_id = z['id']
    zone_name = z['name']
    try:
        routes = cf(f'zones/{zone_id}/workers/routes').get('result', [])
        for r in routes:
            all_routes.append({
                'zone': zone_name,
                'zone_id': zone_id,
                'pattern': r.get('pattern', ''),
                'script': r.get('script', ''),
                'route_id': r.get('id', '')
            })
    except:
        pass

# Step 2: Find route overlaps (prefix conflicts)
conflicts = []
for i, a in enumerate(all_routes):
    for j, b in enumerate(all_routes):
        if i >= j:
            continue
        # Check if one route pattern is a prefix of another
        a_pat = a['pattern']
        b_pat = b['pattern']
        
        # Normalize: strip trailing * for comparison
        a_base = a_pat.rstrip('*').rstrip('/')
        b_base = b_pat.rstrip('*').rstrip('/')
        
        # One is more specific than another if it shares the same domain prefix
        if (a_base.startswith(b_base) or b_base.startswith(a_base)) and a_pat != b_pat:
            # Determine which is more specific
            if len(a_pat) > len(b_pat):
                conflicts.append({
                    'intercepting': a,
                    'overridden': b,
                    'specificity': 'MORE_SPECIFIC_INTERCEPTS',
                })
            else:
                conflicts.append({
                    'intercepting': b,
                    'overridden': a,
                    'specificity': 'MORE_SPECIFIC_INTERCEPTS',
                })

for c in conflicts:
    ic = c['intercepting']
    ov = c['overridden']
    print(f"  [CONFLICT] {ic['pattern']}→{ic['script']} overrides {ov['pattern']}→{ov['script']}")
    print(f"    FIX: Delete one route or ensure both Workers are compatible")
```

### Fix: Delete the Intercepting Route

```python
# DELETE /zones/{zone_id}/workers/routes/{route_id}
zone_id = '<zone_id>'
route_id = '<route_id>'
url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/workers/routes/{route_id}'
req = urllib.request.Request(url, method='DELETE')
req.add_header('Authorization', f'Bearer {TOKEN}')
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
print(f"Deleted: {json.loads(resp.read()).get('success')}")
```

### Integration with Infrastructure Audit

Add this check to the infrastructure-audit Phase 1.7 DNS Resolution audit. After checking DNS records, scan Worker routes for conflicts:

1. List all Worker routes across all zones
2. Sort by pattern specificity (longer = more specific)
3. For any pair where pattern A starts with pattern B (or vice versa), flag as potential conflict
4. Verify: does the intercepting Worker handle the traffic correctly? If not → fix

### Real-World Example (2026-07-02)

```
Route Conflict Found:
  papers.qnfo.org/papers/* → seo-metadata-injector  (MORE SPECIFIC — intercepts)
  papers.qnfo.org/*        → papers-server          (OVERRIDDEN — never receives /papers/* traffic)

Symptom: Paper detail pages redirect to listing instead of showing content
Root Cause: seo-metadata-injector falls through to fetch(request) → Pages origin → redirect page
Fix: Delete papers.qnfo.org/papers/* route → papers-server handles all traffic
```

## When to Use

| Trigger | Action |
|:--------|:-------|
| Worker appears non-functional but is deployed | Check for route conflicts |
| Specific paths return unexpected responses | Check if a more specific route intercepts |
| Debugging "why is this Worker not receiving traffic" | Run the detection script |
| Infrastructure audit session start | Include in Phase 1.7 |

---

*worker-route-interference-audit v1.0 — learned from 2026-07-02 papers.qnfo.org full-text outage*
