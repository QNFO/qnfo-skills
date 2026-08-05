#!/usr/bin/env python3
"""Buffer token validation diagnostic (KIF-45).

Runs a minimal GraphQL query to verify the token is valid
and has sufficient scope. Returns exit code 0 if token is OK,
exit code 1 if token is stale, exit code 2 if no token found.

Usage: python buffer-token-check.py
Exit codes: 0 = OK, 1 = STALE, 2 = NO_TOKEN
"""
import os
import sys
import requests

TOKEN_PATH = os.path.expandvars(r'%USERPROFILE%\buffer\token')

if not os.path.exists(TOKEN_PATH):
    print('[BUFFER-TOKEN: NO_TOKEN] No token file at %USERPROFILE%\\buffer\\token')
    sys.exit(2)

TOKEN = open(TOKEN_PATH).read().strip()
if not TOKEN:
    print('[BUFFER-TOKEN: EMPTY] Token file exists but is empty')
    sys.exit(2)

HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# Minimal query — check token validity with Buffer's actual schema
query = '{ organization { __typename } }'

try:
    r = requests.post(
        'https://api.buffer.com/graphql',
        headers=HEADERS,
        json={'query': query},
        timeout=15
    )
    result = r.json()
except Exception as e:
    print(f'[BUFFER-TOKEN: API_ERROR] {e}')
    sys.exit(1)

# Check for errors
if 'errors' in result:
    error_msg = result['errors'][0].get('message', '')
    extensions = result['errors'][0].get('extensions', {})
    code = extensions.get('code', '')

    if 'UNAUTHENTICATED' in code or 'UNAUTHENTICATED' in error_msg:
        print('[BUFFER-TOKEN: STALE] Token is UNAUTHENTICATED — expired or revoked.')
        print('[BUFFER-TOKEN: ACTION] Generate new PAT at https://buffer.com/developers/api with full scopes.')
        print('[BUFFER-TOKEN: SAVE] Save to %USERPROFILE%\\buffer\\token')
        sys.exit(1)
    elif 'FORBIDDEN' in code:
        print('[BUFFER-TOKEN: INSUFFICIENT_SCOPE] Token recognized but lacks organization scope.')
        print('[BUFFER-TOKEN: ACTION] Generate new PAT with organization:read + post:write scopes.')
        sys.exit(1)
    else:
        print(f'[BUFFER-TOKEN: ERROR] {error_msg}')
        sys.exit(1)

# Token is valid
viewer_id = result.get('data', {}).get('organization', {}).get('__typename', 'UNKNOWN')
print(f'[BUFFER-TOKEN: OK] Token valid. Organization accessible.')
sys.exit(0)
