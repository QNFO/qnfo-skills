#!/usr/bin/env python3
r"""zenodo-ownership-check.py — P5.OWNERSHIP enforcement gate (research v2.54).

Audits D1 `papers` + `paper_ids` tables for any zenodo_url/zenodo_doi that points
at a NON-QNFO-owned DOI. BLOCKS (exit 1) if any row links an external/unknown DOI.

Canonical incident (2026-08-04): a blanket `zenodo_url='https://doi.org/'||doi`
backfill created 1,245+ fake links to external citations + garbage. This gate
prevents recurrence. NEVER derive zenodo_url from `doi LIKE '%zenodo%'` alone.

Usage:
    python zenodo-ownership-check.py            # reads C:/Users/LENOVO/tokens/*
    python zenodo-ownership-check.py --json     # machine-readable report
    python zenodo-ownership-check.py --fix      # NULL offending zenodo_url rows

Exit codes: 0 = clean (all links QNFO-owned), 1 = violations found (or error).
"""
import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
import time

# ---- config ----
DEFAULT_TOKENS = {
    'cloudflare': r'C:\Users\LENOVO\tokens\cloudflare',
    'zenodo': r'C:\Users\LENOVO\tokens\zenodo',
}
ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
LIVING_PAPER = '70a58cb3-b2cd-498d-877f-ecca86859a22'
# QNFO creator names to search (person variant covers mis-attributed records,
# e.g. Adelic Shannon chain 21698550/21698976/21710934).
CREATOR_QUERIES = [
    'metadata.creators.person_or_org.name:QNFO',
    'metadata.creators.person_or_org.name:"Rowan Brad Quni-Gudzinas"',
]
VALID_ZENODO = re.compile(r'^10\.5281/zenodo\.\d{5,8}$', re.IGNORECASE)

REPORT = {'owned': 0, 'external': 0, 'garbage': 0, 'violations': []}


def read_token(kind):
    path = DEFAULT_TOKENS[kind]
    if not os.path.exists(path):
        raise SystemExit(f"[ERROR] token file missing: {path}")
    with open(path, encoding='utf-8') as f:
        return f.read().strip()


def api_zenodo(token, url, retries=3):
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = int(e.headers.get('Retry-After', '60'))
                print(f"  [rate-limited] sleeping {retry_after}s (attempt {attempt + 1})")
                time.sleep(retry_after + 2)
                continue
            raise
    raise SystemExit("[ERROR] rate-limited after retries")


def fetch_owned_dois(zenodo_token):
    """Build the QNFO-owned DOI set (record + concept) from the live API."""
    owned = set()
    for query in CREATOR_QUERIES:
        page = 1
        while page <= 8:
            url = (f'https://zenodo.org/api/records?q={urllib.parse.quote(query)}'
                   f'&size=50&sort=mostrecent&all_versions=true&page={page}')
            data = api_zenodo(zenodo_token, url)
            hits = data.get('hits', {}).get('hits', [])
            for r in hits:
                owned.add((r.get('doi') or '').strip().lower())
                owned.add((r.get('conceptdoi') or '').strip().lower())
            if len(hits) < 50:
                break
            page += 1
    return owned


def d1_query(cf_token, sql, params=None):
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/d1/database/{LIVING_PAPER}/query'
    body = json.dumps({'sql': sql, 'params': params or []}).encode('utf-8')
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Authorization', f'Bearer {cf_token}')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"[ERROR] D1 query failed: {e.code} {e.read().decode()[:300]}")


def extract_doi(url_or_doi):
    """Strip any URL prefix from a value to get the bare DOI.

    Handles: doi.org/{doi}, zenodo.org/doi/{doi}, zenodo.org/records/{id}
    and zenodo.org/record/{id} (legacy record-page format → 10.5281/zenodo.{id}).
    """
    v = (url_or_doi or '').strip()
    for prefix in ('https://doi.org/', 'http://doi.org/', 'https://zenodo.org/doi/', 'doi.org/'):
        if v.startswith(prefix):
            return v[len(prefix):].lower()
    # Zenodo record-page URL format: https://zenodo.org/records/{id} or /record/{id}
    m = re.match(r'^https?://zenodo\.org/records?/(\d{5,8})(/.*)?$', v, re.IGNORECASE)
    if m:
        return f'10.5281/zenodo.{m.group(1)}'
    return v.lower()


def audit_table(cf_token, owned, table, key_col):
    sql = f"SELECT {key_col}, doi, zenodo_url FROM {table} WHERE zenodo_url IS NOT NULL AND zenodo_url != ''"
    r = d1_query(cf_token, sql)
    rows = r['result'][0]['results']
    for row in rows:
        key = row.get(key_col)
        doi = (row.get('doi') or '').strip()
        url = (row.get('zenodo_url') or '').strip()
        url_doi = extract_doi(url)
        if not VALID_ZENODO.match(url_doi):
            REPORT['garbage'] += 1
            REPORT['violations'].append({
                'table': table, 'key': key, 'doi': doi, 'zenodo_url': url,
                'type': 'garbage_url',
            })
        elif url_doi not in owned:
            REPORT['external'] += 1
            REPORT['violations'].append({
                'table': table, 'key': key, 'doi': doi, 'zenodo_url': url,
                'type': 'non_qnfo_doi',
            })
        else:
            REPORT['owned'] += 1
    return rows


def fix_violations(cf_token, table, key_col, violations):
    for v in violations:
        key = v['key']
        url = v['zenodo_url']
        if key is None:
            continue  # NULL-key rows: use keyless match below
        sql = f"UPDATE {table} SET zenodo_url = NULL, updated_at = datetime('now') WHERE {key_col} = ?1 AND zenodo_url = ?2"
        r = d1_query(cf_token, sql, [key, url])
        if 'error' in r:
            print(f"  [fix-fail] {table} {key}: {r['error'][:150]}")
        else:
            print(f"  [fixed] {table} {key}: NULLed {url[:60]}")
    # NULL-key rows: keyless bulk (safe: only touches rows whose url == derived doi)
    if any(v['key'] is None for v in violations):
        sql = (f"UPDATE {table} SET zenodo_url = NULL, updated_at = datetime('now') "
               f"WHERE zenodo_url IS NOT NULL AND zenodo_url != '' "
               f"AND lower(zenodo_url) IN (SELECT lower('https://doi.org/' || doi) FROM {table} "
               f"WHERE doi IS NOT NULL AND doi != '') "
               f"AND lower(COALESCE(doi,'')) LIKE '%zenodo%' "
               f"AND lower(COALESCE(doi,'')) NOT IN ({_owned_inlist(REPORT_OWNED)})")
        # NOTE: REPORT_OWNED must be injected before calling fix; see main().


def _owned_inlist(owned):
    return ",".join("'" + d.replace("'", "''") + "'" for d in sorted(owned))


def main():
    parser = argparse.ArgumentParser(description='P5.OWNERSHIP enforcement gate')
    parser.add_argument('--json', action='store_true', help='machine-readable report')
    parser.add_argument('--fix', action='store_true', help='NULL offending zenodo_url rows')
    args = parser.parse_args()

    try:
        cf_token = read_token('cloudflare')
        zenodo_token = read_token('zenodo')
    except SystemExit as e:
        print(e)
        sys.exit(1)

    print("Fetching QNFO-owned DOI set from live API...")
    owned = fetch_owned_dois(zenodo_token)
    REPORT['owned_doi_count'] = len(owned)
    print(f"  owned DOIs: {len(owned)}")

    print("Auditing papers.zenodo_url...")
    audit_table(cf_token, owned, 'papers', 'identifier')
    print("Auditing paper_ids.zenodo_url...")
    audit_table(cf_token, owned, 'paper_ids', 'slug')

    if args.fix and REPORT['violations']:
        global REPORT_OWNED
        REPORT_OWNED = owned
        for table, key_col in (('papers', 'identifier'), ('paper_ids', 'slug')):
            tbl_violations = [v for v in REPORT['violations'] if v['table'] == table]
            if tbl_violations:
                print(f"Fixing {table} ({len(tbl_violations)} violations)...")
                fix_violations(cf_token, table, key_col, tbl_violations)

    print(json.dumps(REPORT, indent=2) if args.json else
          f"\nREPORT: owned={REPORT['owned']} external={REPORT['external']} "
          f"garbage={REPORT['garbage']} violations={len(REPORT['violations'])}")

    if REPORT['violations']:
        sys.exit(1)  # BLOCK: linkage integrity violated
    print("PASS: all zenodo_url links are QNFO-owned.")
    sys.exit(0)


if __name__ == '__main__':
    import urllib.parse  # noqa: E402 (needed by fetch_owned_dois)
    REPORT_OWNED = set()
    main()
