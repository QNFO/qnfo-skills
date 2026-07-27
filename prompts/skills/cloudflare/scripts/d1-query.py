# -*- coding: utf-8 -*-
"""
Canonical D1 Query Script -- KIF-36 (2026-07-27)
Auto-discovers Cloudflare credentials, account ID, and database UUID.
NEVER requires hardcoded account IDs or database UUIDs.

Usage:
    python d1-query.py --db living-paper --sql "SELECT * FROM papers WHERE slug=?" --params zbw-p5-capstone
    python d1-query.py --db living-paper --sql "SELECT slug, doi FROM papers LIMIT 5"
    python d1-query.py --db living-paper --sql "SELECT LENGTH(body_md) FROM papers WHERE slug=?" --params zbw-p5-capstone

Token discovery (in order):
    1. CLOUDFLARE_API_TOKEN environment variable (User scope)
    2. %%USERPROFILE%%\\.cloudflare_token file
    3. %%USERPROFILE%%\\keys.json -> cloudflare_api_token key

Account ID discovery (in order):
    1. %%USERPROFILE%%\\.deepchat\\d1-cache.json -> account_id field
    2. Live: npx wrangler whoami -> parse Account ID column

Database UUID discovery (in order):
    1. %%USERPROFILE%%\\.deepchat\\d1-cache.json -> databases[db_name] field
    2. Live: npx wrangler d1 list -> parse matching name row
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
import argparse
import re
from pathlib import Path

CACHE_FILE = Path(os.environ.get('USERPROFILE', '.')) / '.deepchat' / 'd1-cache.json'


# -- Npx Helper (Windows: npx is a cmd script, needs shell) --------------------

def run_npx(args, timeout=30):
    """Run npx wrangler <args> correctly on Windows."""
    is_windows = sys.platform == 'win32'
    if is_windows:
        cmd = ['cmd', '/c', 'npx', 'wrangler'] + args
    else:
        cmd = ['npx', 'wrangler'] + args
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                          encoding='utf-8')


# -- Token Discovery -----------------------------------------------------------

def discover_token():
    """Discover CLOUDFLARE_API_TOKEN from multiple sources."""
    # 1. Environment variable (User scope - PowerShell sets this)
    token = os.environ.get('CLOUDFLARE_API_TOKEN')
    if token and token.startswith('cfat_') and len(token) > 20:
        return token

    # 2. File: %%USERPROFILE%%\\.cloudflare_token
    token_file = Path(os.environ.get('USERPROFILE', '.')) / '.cloudflare_token'
    if token_file.exists():
        token = token_file.read_text(encoding='utf-8').strip()
        if token and token.startswith('cfat_') and len(token) > 20:
            return token

    # 3. File: %%USERPROFILE%%\\keys.json
    keys_file = Path(os.environ.get('USERPROFILE', '.')) / 'keys.json'
    if keys_file.exists():
        try:
            keys = json.loads(keys_file.read_text(encoding='utf-8'))
            token = keys.get('cloudflare_api_token') or keys.get('CLOUDFLARE_API_TOKEN')
            if token and token.startswith('cfat_') and len(token) > 20:
                return token
        except (json.JSONDecodeError, KeyError):
            pass

    # 4. Environment variable (Process scope - fallback via Win32 API)
    try:
        import ctypes
        buf = ctypes.create_unicode_buffer(1024)
        ctypes.windll.kernel32.GetEnvironmentVariableW(
            'CLOUDFLARE_API_TOKEN', buf, 1024)
        token = buf.value.strip()
        if token and token.startswith('cfat_') and len(token) > 20:
            return token
    except Exception:
        pass

    print("FATAL: Cannot discover CLOUDFLARE_API_TOKEN from any source.",
          file=sys.stderr)
    print("  Checked: env var, ~/.cloudflare_token, ~/keys.json", file=sys.stderr)
    sys.exit(1)


# -- Account ID Discovery ------------------------------------------------------

def discover_account_id():
    """Discover Cloudflare account ID from cache or wrangler whoami --json."""
    # 1. Cache
    if CACHE_FILE.exists():
        try:
            cache = json.loads(CACHE_FILE.read_text(encoding='utf-8'))
            aid = cache.get('account_id')
            if aid and len(aid) == 32 and re.match(r'^[a-f0-9]+$', aid):
                return aid
        except (json.JSONDecodeError, KeyError):
            pass

    # 2. Live: npx wrangler whoami --json
    try:
        result = run_npx(['whoami', '--json'])
        if result.returncode == 0:
            data = json.loads(result.stdout)
            accounts = data.get('accounts', [])
            if accounts:
                aid = accounts[0].get('id')
                if aid:
                    save_to_cache('account_id', aid)
                    return aid
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError,
            json.JSONDecodeError) as e:
        print(f"  wrangler whoami failed: {e}", file=sys.stderr)

    print("FATAL: Cannot discover Cloudflare account ID.", file=sys.stderr)
    print("  Run: npx wrangler whoami", file=sys.stderr)
    sys.exit(1)


# -- Database UUID Discovery ---------------------------------------------------

def discover_db_uuid(db_name):
    """Discover D1 database UUID from cache or wrangler d1 list --json."""
    # 1. Cache
    if CACHE_FILE.exists():
        try:
            cache = json.loads(CACHE_FILE.read_text(encoding='utf-8'))
            dbs = cache.get('databases', {})
            uuid = dbs.get(db_name)
            if uuid and re.match(r'^[a-f0-9-]{36}$', uuid):
                return uuid
        except (json.JSONDecodeError, KeyError):
            pass

    # 2. Live: npx wrangler d1 list --json
    try:
        result = run_npx(['d1', 'list', '--json'])
        if result.returncode == 0:
            databases = json.loads(result.stdout)
            for db in databases:
                if db.get('name') == db_name:
                    uuid = db.get('uuid')
                    if uuid:
                        save_to_cache(f'databases.{db_name}', uuid)
                        return uuid
            # Not found — list available names for diagnostics
            names = [db.get('name', '?') for db in databases]
            print(f"  Database '{db_name}' not found. Available: {names}",
                  file=sys.stderr)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError,
            json.JSONDecodeError) as e:
        print(f"  wrangler d1 list failed: {e}", file=sys.stderr)

    print(f"FATAL: Cannot discover UUID for database '{db_name}'.", file=sys.stderr)
    print(f"  Run: npx wrangler d1 list --json", file=sys.stderr)
    sys.exit(1)


# -- Cache Management ----------------------------------------------------------

def save_to_cache(key, value):
    """Save a discovered value to the session cache file."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    cache = {}
    if CACHE_FILE.exists():
        try:
            cache = json.loads(CACHE_FILE.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, KeyError):
            pass

    # Handle dotted keys like 'databases.living-paper'
    if '.' in key:
        parts = key.split('.')
        d = cache
        for p in parts[:-1]:
            if p not in d:
                d[p] = {}
            d = d[p]
        d[parts[-1]] = value
    else:
        cache[key] = value

    CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False),
                          encoding='utf-8')


# -- D1 Query Execution --------------------------------------------------------

def execute_query(account_id, db_uuid, token, sql, params):
    """Execute a D1 SQL query and return JSON result."""
    url = (f'https://api.cloudflare.com/client/v4/accounts/'
           f'{account_id}/d1/database/{db_uuid}/query')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    body = json.dumps({'sql': sql, 'params': params}).encode('utf-8')

    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='replace')
        print(f"HTTP {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)


# -- Main ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Canonical D1 Query Tool (KIF-36) - auto-discovers credentials'
    )
    parser.add_argument('--db', required=True,
                        help='Database name (e.g., living-paper, qnfo-graph)')
    parser.add_argument('--sql', required=True,
                        help='SQL query with ? placeholders')
    parser.add_argument('--params', nargs='*', default=[],
                        help='Query parameters (positional, matched to ? placeholders)')
    parser.add_argument('--raw', action='store_true',
                        help='Output raw JSON response instead of pretty-printed rows')
    parser.add_argument('--refresh', action='store_true',
                        help='Force re-discovery (bypass cache)')
    args = parser.parse_args()

    # Force re-discovery if requested
    if args.refresh and CACHE_FILE.exists():
        CACHE_FILE.unlink()

    # Discover credentials and infrastructure
    token = discover_token()
    account_id = discover_account_id()
    db_uuid = discover_db_uuid(args.db)

    # Execute query
    result = execute_query(account_id, db_uuid, token, args.sql, args.params)

    if args.raw:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Pretty-print results
    if not result.get('success'):
        print(f"Query failed: {json.dumps(result.get('errors', result), indent=2)}",
              file=sys.stderr)
        sys.exit(1)

    rows = result.get('result', [{}])[0].get('results', [])
    if not rows:
        print("(no results)")
        return

    # Print as JSON array for machine consumption
    print(json.dumps(rows, indent=2, ensure_ascii=False))

    # Print row count for human consumption
    print(f"\n-- {len(rows)} row(s) --", file=sys.stderr)


if __name__ == '__main__':
    main()
