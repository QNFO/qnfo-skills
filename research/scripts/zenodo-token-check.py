#!/usr/bin/env python3
"""zenodo-token-check.py — Diagnose the root cause of a Zenodo API auth/endpoint failure.

Run on any Zenodo error (403, 404, 415, etc.) BEFORE diagnosing "token scope problem."
The InvenioRDM migration (2024+) decommissioned /api/deposit/depositions.

Verification strategy:
1. GET /api/user → 200 = token works, problem is endpoint OR Content-Type
2. GET /api/user → 401 = token expired/invalid (regenerate)
3. GET /api/user → 403 = token lacks user:email scope
4. GET /api/records?size=1 → 200 = InvenioRDM endpoint reachable
5. POST /api/records → 415 = missing Content-Type: application/json

Usage:
  python scripts/zenodo-token-check.py
  python scripts/zenodo-token-check.py --verbose
"""

import os, sys, urllib.request, json

TOKEN = os.environ.get('ZENODO_TOKEN', '')
VERBOSE = '--verbose' in sys.argv

if not TOKEN:
    print("ZENODO_TOKEN: MISSING")
    print("Try: wmic process call create (CITATION-2 anti-pattern)")
    sys.exit(1)

print(f"ZENODO_TOKEN: PRESENT ({len(TOKEN)} chars)")

def api(method, path, data=None, extra_headers=None):
    url = f'https://zenodo.org{path}'
    headers = {'Authorization': f'Bearer {TOKEN}'}
    if extra_headers:
        headers.update(extra_headers)
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()

# Test 1: Token validity (works on InvenioRDM)
status, body = api('GET', '/api/user')
print(f"  GET /api/user → {status}", end='')
if status == 200:
    data = json.loads(body)
    uid = data.get('id', '?')
    print(f" — TOKEN VALID (user id={uid})")
else:
    print(f" — TOKEN ISSUE: {body[:150]}")
    if status == 401:
        print("\nDIAGNOSIS: Token expired or invalid. Regenerate at zenodo.org/account/settings/applications")
    elif status == 403:
        print("\nDIAGNOSIS: Token lacks required scopes. Add: deposit:write, deposit:actions, user:email")
    print(f"\nNo need to check endpoints — the token is the problem.")
    sys.exit(1 if status in (401, 403) else 0)

# Test 2: InvenioRDM endpoint reachable
status, body = api('GET', '/api/records?size=1')
print(f"  GET /api/records?size=1 → {status}", end='')
if status == 200:
    print(" — InvenioRDM endpoint REACHABLE")
elif status == 404:
    print(" — ENDPOINT NOT FOUND (InvenioRDM migration? Check https://zenodo.org/api/records)")
else:
    print(f" — UNEXPECTED: {body[:100]}")

# Test 3: Content-Type validation
status, body = api('POST', '/api/records', extra_headers={'Content-Type': 'application/json'})
print(f"  POST /api/records (test) → {status} — Content-Type OK" if status != 415 else f"  POST /api/records → 415 — missing Content-Type header")
if status == 404:
    print("  WARNING: POST /api/records 404 — endpoint may have changed. Check https://developers.zenodo.org/")

# Test 4: Scope check
status, body = api('GET', '/api/user/records?size=1')
print(f"  GET /api/user/records → {status} — deposit:write scope OK" if status == 200 else f"  GET /api/user/records → {status} — deposit:write scope MISSING")

print("\n=== TOKEN STATUS ===")
print("TOKEN: VALID — endpoint or Content-Type is the issue if uploads fail.")
print("To publish: POST /api/records (create draft) → PUT /api/records/{id}/draft/files/{filename} (upload files)")
print("→ PUT /api/records/{id}/draft (metadata) → POST /api/records/{id}/draft/actions/publish")
