"""
zenodo-resource-type-fix.py -- Failsafe metadata-shape resolver for Zenodo
deposit PUT calls, specifically for actions/newversion drafts.

ROOT CAUSE (2026-07-25, adelic-cross-domain v3.2): Zenodo's metadata PUT
endpoint accepted metadata.resource_type as a bare STRING ("publication")
with HTTP 200, but that value was NOT actually persisted server-side --
the subsequent actions/publish call failed with "Missing data for required
field: resource_type". Sending resource_type as a nested OBJECT
({"type": "publication", "subtype": "preprint"}) was REJECTED outright with
"Not a valid string" on the same newversion draft. The only combination
that both persisted AND allowed publish to succeed was setting
upload_type + publication_type as separate TOP-LEVEL STRING fields instead
of a nested resource_type object at all.

This script tries, in order, every metadata shape variant that has been
observed to work in ANY QNFO Zenodo session, verifying persistence via a
GET after each PUT attempt, and stops at the first variant that survives
a re-GET. This turns what was previously ~10 exploratory tool calls of
guessing into one deterministic script run.

Usage:
    python zenodo-resource-type-fix.py --deposit-id <id> --upload-type publication --publication-type preprint

Requires ZENODO_TOKEN in environment (never hand-copy from truncated terminal output).
"""
import json
import os
import sys
import urllib.request
import urllib.error
import argparse

TOKEN = os.environ.get('ZENODO_TOKEN')
if not TOKEN:
    print('ZENODO_TOKEN not set in environment. Aborting -- do not hardcode a token value.', file=sys.stderr)
    sys.exit(1)

BASE = 'https://zenodo.org/api/deposit/depositions'


def req(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
    })
    try:
        with urllib.request.urlopen(r) as resp:
            return resp.getcode(), json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_err = e.read().decode(errors='replace')
        try:
            return e.code, json.loads(body_err)
        except Exception:
            return e.code, {'raw': body_err}


def try_variant(deposit_id, metadata, label):
    print(f'--- Trying variant: {label} ---')
    code, resp = req('PUT', f'{BASE}/{deposit_id}', {'metadata': metadata})
    print(f'PUT status: {code}')
    if code >= 400:
        print('PUT rejected:', json.dumps(resp)[:500])
        return False

    # Re-GET to confirm persistence (do not trust the PUT 200 alone)
    code2, resp2 = req('GET', f'{BASE}/{deposit_id}')
    persisted_meta = resp2.get('metadata', {})
    has_resource_type = bool(persisted_meta.get('resource_type')) or bool(persisted_meta.get('upload_type'))
    print(f'Re-GET status: {code2}, resource_type/upload_type persisted: {has_resource_type}')
    if has_resource_type:
        print(f'VARIANT SUCCEEDED AND PERSISTED: {label}')
        return True
    print(f'Variant PUT accepted but did NOT persist (silent failure) -- trying next variant.')
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--deposit-id', required=True)
    ap.add_argument('--upload-type', default='publication')
    ap.add_argument('--publication-type', default='preprint')
    ap.add_argument('--title', default=None, help='Only needed if variants require title to stay populated')
    args = ap.parse_args()

    deposit_id = args.deposit_id

    # Get current metadata first to preserve required fields across variants
    code, current = req('GET', f'{BASE}/{deposit_id}')
    if code != 200:
        print(f'Could not GET deposit {deposit_id}: {code} {current}', file=sys.stderr)
        sys.exit(1)
    cur_meta = current.get('metadata', {})
    base_fields = {
        'title': args.title or cur_meta.get('title') or 'Untitled',
        'creators': cur_meta.get('creators') or [{'name': 'Unknown'}],
        'description': cur_meta.get('description') or 'No description',
    }

    variants = [
        ('A: nested resource_type object',
         {**base_fields, 'resource_type': {'type': args.upload_type, 'subtype': args.publication_type}}),
        ('B: top-level upload_type + publication_type strings (VERIFIED WORKING 2026-07-25)',
         {**base_fields, 'upload_type': args.upload_type, 'publication_type': args.publication_type}),
        ('C: resource_type as bare string (known to silently fail to persist, tried last as fallback)',
         {**base_fields, 'resource_type': args.upload_type}),
    ]

    for label, metadata in variants:
        if try_variant(deposit_id, metadata, label):
            print(f'\nRESOLVED: use variant "{label}" for deposit {deposit_id} going forward.')
            sys.exit(0)

    print('\nALL VARIANTS FAILED TO PERSIST. This is a genuine Zenodo API issue beyond known workarounds -- '
          'escalate rather than retry further blindly.', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main()
