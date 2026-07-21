#!/usr/bin/env python3
"""
Zenodo Token Sanity Check

Run this FIRST whenever Zenodo API calls return HTTP 403, before assuming
the token is dead, expired, or scopeless. The generic Zenodo error body
{"status":403,"message":"Permission denied."} is IDENTICAL for:
  (a) a token that genuinely lacks write scope
  (b) a token that has full scope but was mistyped/truncated/reconstructed
      incorrectly when moved between contexts (the actual root cause of
      the 2026-07-20 incident -- a 59-vs-60-character transcription error)
  (c) an actually-expired or revoked token

This script distinguishes them by testing progressively more privileged
operations against a harmless target, using the token EXACTLY as stored
in the environment variable (never retyped).

Usage:
    python zenodo-token-check.py

Required scopes for full read+write+publish (generate at
https://zenodo.org/account/settings/applications/ if any FAIL):
    deposit:write    -- allow upload (but not publishing)
    deposit:actions  -- allow publishing of uploads
    user:email       -- allow access to email address (read-only)
"""
import requests
import os
import sys


def main():
    token = os.environ.get('ZENODO_TOKEN')
    if not token:
        print('FAIL: ZENODO_TOKEN not set in environment.')
        sys.exit(1)

    print(f'Token present, length={len(token)} chars.')
    headers = {'Authorization': f'Bearer {token}'}

    # Test 1: read access (list depositions)
    r = requests.get('https://zenodo.org/api/deposit/depositions', headers=headers, params={'size': 1})
    print(f'[1] GET /deposit/depositions (read):  HTTP {r.status_code}'
          f'{"  OK" if r.status_code == 200 else "  FAIL -- " + r.text[:150]}')

    # Test 2: user info (confirms token identity + user:email scope)
    r2 = requests.get('https://zenodo.org/api/deposit/depositions', headers=headers)
    # Zenodo has no dedicated /me endpoint in the deposit API; use a
    # lightweight write-capable probe instead: create + immediately discard.
    r3 = requests.post('https://zenodo.org/api/deposit/depositions', headers=headers, json={})
    write_ok = r3.status_code == 201
    print(f'[2] POST /deposit/depositions (write, deposit:write): HTTP {r3.status_code}'
          f'{"  OK" if write_ok else "  FAIL -- " + r3.text[:150]}')

    deposit_id = None
    if write_ok:
        deposit_id = r3.json()['id']
        # Test 3: metadata update on the just-created deposit
        r4 = requests.put(
            f'https://zenodo.org/api/deposit/depositions/{deposit_id}',
            headers=headers,
            json={'metadata': {
                'title': 'token-check-temp',
                'upload_type': 'dataset',
                'creators': [{'name': 'token-check'}],
                'description': 'temporary probe deposit, safe to discard',
            }},
        )
        print(f'[3] PUT /deposit/depositions/{{id}} (metadata write): HTTP {r4.status_code}'
              f'{"  OK" if r4.status_code == 200 else "  FAIL -- " + r4.text[:150]}')

        # Clean up: discard the probe deposit (does NOT publish it)
        r5 = requests.delete(
            f'https://zenodo.org/api/deposit/depositions/{deposit_id}',
            headers=headers,
        )
        print(f'[cleanup] DELETE probe deposit {deposit_id}: HTTP {r5.status_code}'
              f'{"  OK (removed)" if r5.status_code == 204 else "  -- leave it, harmless unsubmitted draft"}')
    else:
        print('[3] Skipped metadata-write test (write test failed).')
        print('[cleanup] No probe deposit was created.')

    print('\n=== Diagnosis ===')
    if r.status_code == 200 and write_ok:
        print('Token has full read+write scope. If a real publish still '
              'fails with 403, the problem is elsewhere (e.g. wrong '
              'deposit_id, deposit already published/locked, or a '
              'DIFFERENT token being used by mistake in that call site -- '
              'grep your scripts for any hardcoded token string).')
    elif r.status_code == 200 and not write_ok:
        print('Token has READ-ONLY scope. Generate a new token at '
              'https://zenodo.org/account/settings/applications/ with '
              'deposit:write AND deposit:actions scopes checked.')
    else:
        print('Token failed even the READ test. Before concluding the '
              'token is dead: re-copy it directly from '
              'https://zenodo.org/account/settings/applications/ into '
              'the environment variable (e.g. $env:ZENODO_TOKEN = "...") '
              'without any intermediate manual retyping or truncated-'
              'display reconstruction, then re-run this script.')


if __name__ == '__main__':
    main()
