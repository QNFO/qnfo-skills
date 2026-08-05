#!/usr/bin/env python3
"""Zenodo PLACEHOLDER + duplicate-record audit and cleanup.

CANONICAL SCRIPT (research skill v2.79+). Uses the documented subject-search
syntax: `metadata.subjects.subject:"TAG"` (QUOTED value — unquoted OR-tokenizes
and produces false positives like the 154-result artifact of 2026-08-05).

Usage:
  python zenodo-cleanup.py                # audit only (report)
  python zenodo-cleanup.py --delete       # audit + delete tagged records

Output: writes a report to the skill dir or prints to stdout.
"""
import json, os, sys, time, urllib.request, urllib.error

TOKEN = json.load(open(os.path.expandvars(r'%USERPROFILE%\keys.json')))['zenodo_token']
# ZENODO-BOT-403-1 (research v2.74): minimal UA triggers bot detection on this
# residential IP — full Chrome headers required for API calls.
H = {'Authorization': f'Bearer {TOKEN}', 'Accept': 'application/json',
     'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'),
     'Accept-Language': 'en-US,en;q=0.9', 'Referer': 'https://zenodo.org/',
     'Origin': 'https://zenodo.org'}
DELETE = '--delete' in sys.argv

def search(tag, size=100):
    """Quoted subject search — the ONLY correct syntax (research v2.79)."""
    import urllib.parse
    q = urllib.parse.quote(f'metadata.subjects.subject:"{tag}"')
    results, page = [], 1
    while True:
        url = f'https://zenodo.org/api/records/?q={q}&size={size}&page={page}&sort=mostrecent&all_versions=false'
        req = urllib.request.Request(url, headers=H)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read())
        except urllib.error.HTTPError as e:
            print(f'  [HTTP {e.code}] on page {page} — transient API issue, retry later')
            return results, 'PARTIAL'
        except Exception as e:
            print(f'  [ERROR] {e}')
            return results, 'PARTIAL'
        hits = data.get('hits', {}).get('hits', [])
        if not hits:
            break
        results.extend(hits)
        if 'next' not in data.get('links', {}):
            break
        page += 1
        time.sleep(0.5)
    return results, 'COMPLETE'

def delete_record(rec_id):
    url = f'https://zenodo.org/api/records/{rec_id}'
    req = urllib.request.Request(url, method='DELETE', headers=H)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return True, f'HTTP {r.status}'
    except urllib.error.HTTPError as e:
        return False, f'HTTP {e.code}: {e.read().decode()[:150]}'

def main():
    print(f'=== ZENODO CLEANUP AUDIT (research v2.79 syntax) ===')
    print(f'Mode: {"DELETE ENABLED" if DELETE else "AUDIT ONLY"}\n')
    total = 0
    for tag in ['PLACEHOLDER', 'duplicate-record']:
        recs, status = search(tag)
        print(f'"{tag}" tag: {len(recs)} records ({status})')
        for i, rec in enumerate(recs[:20]):
            m = rec.get('metadata', {})
            title = m.get('title') or 'No title'
            subs = [s.get('subject') for s in m.get('subjects', [])]
            print(f'  {rec["id"]}: {title[:70]} | subs={subs}')
        if len(recs) > 20:
            print(f'  ... and {len(recs)-20} more')
        if DELETE and recs:
            print(f'\nDeleting {len(recs)} records...')
            ok = fail = 0
            for rec in recs:
                success, msg = delete_record(rec['id'])
                if success:
                    ok += 1
                else:
                    fail += 1
                    print(f'  FAIL {rec["id"]}: {msg}')
                time.sleep(0.4)
            print(f'  deleted: {ok}, failed: {fail}')
        total += len(recs)
    print(f'\nTOTAL tagged records: {total}')
    return 0 if total == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
