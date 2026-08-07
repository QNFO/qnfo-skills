#!/usr/bin/env python3
"""OSF profile update — programmatic profile/social-links management via OSF API v2.

AUTH: OSF Bearer token from (in order): OSF_TOKEN env var, C:\\Users\\LENOVO\\.qnfo\\osf-token.

Usage:
  python osf-profile-update.py               # update social links (idempotent)
  python osf-profile-update.py --show        # GET current profile only
  python osf-profile-update.py --projects    # list user projects/registrations

Endpoint: PATCH https://api.osf.io/v2/users/me/  (data.id = user id, e.g. 6hyj8)

SCHEMA (verified live 2026-08-05 — OSF user attributes):
  - social fields camelCase; ARRAY type: github, linkedIn, twitter, profileWebsites;
    STRING type: scholar, researchGate, ssrn, impactStory, baiduScholar,
    academiaProfileID, academiaInstitution, researcherId
  - There is NO writable 'bio' field in the OSF user API — unknown fields are
    silently ignored (HTTP 200). Bio lives only in the profile web UI.
  - employment/education are managed via their own endpoints, not users/me.
"""
import json, os, sys, urllib.request, urllib.error

API = 'https://api.osf.io/v2'
USER_ID = '6hyj8'

def get_token():
    t = os.environ.get('OSF_TOKEN')
    if t: return t
    with open(r'C:\Users\LENOVO\.qnfo\osf-token') as f:
        return f.read().strip()

def api(method, path, body=None):
    token = get_token()
    headers = {'Authorization': f'Bearer {token}', 'User-Agent': 'Mozilla/5.0',
               'Content-Type': 'application/vnd.api+json'}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b'{}')

def main():
    if '--show' in sys.argv:
        status, data = api('GET', '/users/me/')
        attrs = data.get('data', {}).get('attributes', {})
        print(json.dumps({k: attrs.get(k) for k in
              ['full_name', 'social', 'employment', 'external_identity', 'allow_indexing']},
             indent=2, default=str))
        return

    if '--projects' in sys.argv:
        status, data = api('GET', '/users/me/nodes/?page[size]=100')
        for node in data.get('data', []):
            a = node.get('attributes', {})
            print(f"{node.get('id')} | {a.get('title','')[:60]} | {a.get('category')} | public={a.get('public')}")
        return

    # Default: update social links (camelCase per OSF schema — NO bio field exists)
    profile = {
        "data": {
            "id": USER_ID,
            "type": "users",
            "attributes": {
                "social": {
                    "github": ["rwnq8"],
                    "scholar": "eHIbqxkAAAAJ",
                    "twitter": ["RowanQuni"],
                    "linkedIn": ["rowan-quni/"],
                    "researchGate": "Rowan-Quni-Gudzinas",
                    "ssrn": "8240988",
                    "profileWebsites": [
                        "https://rwnq8.github.io/",
                        "https://qnfo-landing.pages.dev/",
                        "https://orcid.org/0009-0002-4317-5604",
                        "https://bsky.app/profile/qnfo.bsky.social",
                    ],
                },
            }
        }
    }
    status, data = api('PATCH', '/users/me/', profile)
    if status in (200, 202):
        attrs = data.get('data', {}).get('attributes', {})
        print(f'PROFILE UPDATED (HTTP {status})')
        print(f'  name: {attrs.get("full_name")}')
        print(f'  social: {json.dumps(attrs.get("social", {}), indent=2)}')
        print(f'  ORCID: {attrs.get("external_identity", {}).get("ORCID")}')
    else:
        print(f'PATCH FAILED: HTTP {status}')
        print(json.dumps(data, indent=2)[:800])

if __name__ == '__main__':
    main()
