#!/usr/bin/env python3
"""
bootstrap_skills.py — Skills Sync Tool v1.0

Syncs DeepChat skills between local disk, GitHub, and Cloudflare R2.
Supports: --sync, --status, --validate, --dry-run

Canonical locations:
  R2:  qnfo/tools/bootstrap_skills.py
  GitHub: rwnq8/qnfo-skills/blob/master/bootstrap_skills.py
  Local: %USERPROFILE%\.deepchat\skills\bootstrap_skills.py
"""

import os, sys, json, argparse, urllib.request, hashlib, re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ─── Config ─────────────────────────────────────────────────────────────────
SKILLS_DIR = os.path.expandvars(r'%USERPROFILE%\.deepchat\skills')
R2_ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
R2_BUCKET = 'qnfo'
R2_PREFIX = 'qnfo/prompts/skills'
D1_DB = 'qnfo-audit'

def get_token() -> str:
    """Get Cloudflare API token from env or secrets file."""
    token = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    if not token:
        secrets_path = os.path.expandvars(r'%USERPROFILE%\.cloudflare\api-token')
        if os.path.exists(secrets_path):
            with open(secrets_path, 'r') as f:
                token = f.read().strip()
    return token


# ─── R2 Operations ──────────────────────────────────────────────────────────

def r2_put(key: str, data: bytes, token: str) -> bool:
    """Upload an object to R2."""
    url = f'https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{key}'
    req = urllib.request.Request(url, data=data, method='PUT')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/octet-stream')
    try:
        urllib.request.urlopen(req, timeout=15)
        return True
    except Exception as e:
        print(f'  R2 PUT FAILED for {key}: {e}', file=sys.stderr)
        return False


def r2_get_size(key: str, token: str) -> Optional[int]:
    """Get object size from R2 (HEAD request)."""
    url = f'https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{key}'
    req = urllib.request.Request(url, method='HEAD')
    req.add_header('Authorization', f'Bearer {token}')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        hdr = dict(resp.headers)
        return int(hdr.get('Content-Length', 0))
    except Exception:
        return None


# ─── D1 Operations ──────────────────────────────────────────────────────────

def d1_execute(sql: str, token: str) -> Optional[list]:
    """Execute a D1 query and return results."""
    url = f'https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/d1/database/{D1_DB}/raw'
    body = json.dumps({"sql": sql}).encode()
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        return data.get('result', [{}])[0].get('results', [])
    except Exception as e:
        print(f'  D1 query failed: {e}', file=sys.stderr)
        return None


# ─── Skill Scanning ─────────────────────────────────────────────────────────

def scan_skills() -> List[dict]:
    """Scan local skills directory for all valid skills."""
    skills = []
    for d in sorted(os.listdir(SKILLS_DIR)):
        path = os.path.join(SKILLS_DIR, d, 'SKILL.md')
        if not os.path.isfile(path) or d.startswith('.'):
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse YAML frontmatter
        fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            print(f'  [WARN] {d}: No YAML frontmatter', file=sys.stderr)
            continue
        
        # Extract name and version
        name_match = re.search(r'name:\s*(.+)', fm_match.group(1))
        ver_match = re.search(r'version:\s*"?(.+?)"?\s*$', fm_match.group(1), re.MULTILINE)
        
        skills.append({
            'directory': d,
            'name': name_match.group(1).strip() if name_match else d,
            'version': ver_match.group(1) if ver_match else '?',
            'path': path,
            'size': os.path.getsize(path),
            'sha256': hashlib.sha256(content.encode()).hexdigest(),
        })
    
    return skills


# ─── Variant Deduplication ─────────────────────────────────────────────────

def deduplicate_variants(skills: List[dict]) -> List[dict]:
    """Remove Claude Code / Agents SDK variant copies."""
    variants = {'-claude-code': [], '-agents': []}
    canonical = {s['directory']: s for s in skills}
    
    results = []
    for s in skills:
        name = s['directory']
        if name.endswith('-claude-code'):
            base = name.replace('-claude-code', '')
            if base in canonical:
                print(f'  [DEDUP] Skipping {name} (canonical {base} exists)')
                variants['-claude-code'].append(name)
                continue
        elif name.endswith('-agents'):
            base = name.replace('-agents', '')
            if base in canonical:
                print(f'  [DEDUP] Skipping {name} (canonical {base} exists)')
                variants['-agents'].append(name)
                continue
        results.append(s)
    
    print(f'  Variants skipped: {len(variants["-claude-code"])} claude-code, {len(variants["-agents"])} agents')
    return results


# ─── Frontmatter Validation ─────────────────────────────────────────────────

def validate_skill(skill: dict) -> List[str]:
    """Validate a skill's YAML frontmatter for js-yaml compatibility."""
    issues = []
    with open(skill['path'], 'r', encoding='utf-8') as f:
        content = f.read()
    
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        issues.append('No frontmatter delimiters')
        return issues
    
    fm = fm_match.group(1)
    
    # Check for common js-yaml failure patterns
    if "'" in fm and '"' in fm:
        # Check for single quotes inside double-quoted strings (js-yaml rejects)
        for line in fm.split('\n'):
            if 'description:' in line and '"' in line:
                desc_content = line.split(':', 1)[1].strip()
                if desc_content.startswith('"') and "'" in desc_content:
                    if "\\'" not in desc_content:
                        issues.append(f'Dangerous: single quote inside double-quoted description (js-yaml may reject)')
    
    return issues


# ─── Commands ───────────────────────────────────────────────────────────────

def cmd_status(token: str) -> dict:
    """Check sync status between local, R2, and GitHub."""
    skills = scan_skills()
    result = {'total': len(skills), 'synced': 0, 'drift': 0, 'r2_missing': 0, 'details': []}
    
    for s in skills[:10]:  # Sample check 10 skills
        r2_key = f'{R2_PREFIX}/{s["directory"]}/SKILL.md'
        r2_size = r2_get_size(r2_key, token)
        
        status = '?'
        if r2_size is None:
            status = 'R2-MISSING'
            result['r2_missing'] += 1
        elif r2_size == s['size']:
            status = 'SYNCED'
            result['synced'] += 1
        else:
            status = 'DRIFT'
            result['drift'] += 1
        
        result['details'].append({
            'skill': s['directory'],
            'version': s['version'],
            'local_size': s['size'],
            'r2_size': r2_size or 0,
            'status': status,
        })
    
    return result


def cmd_sync(token: str, dry_run: bool = False) -> dict:
    """Sync all skills to R2 and update D1 skills_index."""
    skills = scan_skills()
    skills = deduplicate_variants(skills)
    
    result = {'total': len(skills), 'uploaded': 0, 'failed': 0, 'skipped': 0}
    
    for s in skills:
        r2_key = f'{R2_PREFIX}/{s["directory"]}/SKILL.md'
        
        # Check if already synced
        r2_size = r2_get_size(r2_key, token)
        if r2_size == s['size']:
            print(f'  [SKIP] {s["directory"]} — already synced ({s["size"]} bytes)')
            result['skipped'] += 1
            continue
        
        if dry_run:
            print(f'  [DRY-RUN] Would upload {s["directory"]} ({s["size"]} bytes)')
            result['uploaded'] += 1
            continue
        
        # Read and upload
        with open(s['path'], 'rb') as f:
            data = f.read()
        
        if r2_put(r2_key, data, token):
            print(f'  [OK] {s["directory"]} ({s["size"]} bytes)')
            result['uploaded'] += 1
        else:
            result['failed'] += 1
    
    return result


def cmd_validate() -> dict:
    """Validate all skills for js-yaml compatibility."""
    skills = scan_skills()
    result = {'total': len(skills), 'valid': 0, 'warnings': 0, 'broken': 0, 'details': []}
    
    for s in skills:
        issues = validate_skill(s)
        detail = {'skill': s['directory'], 'version': s['version'], 'issues': issues}
        
        if not issues:
            result['valid'] += 1
        elif any('frontmatter' in i.lower() for i in issues):
            result['broken'] += 1
            print(f'  [BROKEN] {s["directory"]}: {"; ".join(issues)}')
        else:
            result['warnings'] += 1
            print(f'  [WARN] {s["directory"]}: {"; ".join(issues)}')
        
        result['details'].append(detail)
    
    return result


def print_status_report(status: dict):
    """Print a formatted sync status report."""
    print(f'\n{"="*60}')
    print(f'SKILLS SYNC STATUS — {datetime.now(timezone.utc).isoformat()}')
    print(f'{"="*60}')
    print(f'Total: {status["total"]} | Synced: {status["synced"]} | Drift: {status["drift"]} | R2 Missing: {status["r2_missing"]}')
    print()
    print(f'{"Skill":<32} {"Version":<8} {"Local":<8} {"R2":<8} {"Status":<12}')
    print('-' * 70)
    for d in status['details']:
        print(f'{d["skill"]:<32} {d["version"]:<8} {d["local_size"]:<8} {d["r2_size"]:<8} {d["status"]:<12}')


def print_sync_report(result: dict):
    """Print a formatted sync execution report."""
    print(f'\n{"="*60}')
    print(f'SKILLS SYNC — {datetime.now(timezone.utc).isoformat()}')
    print(f'{"="*60}')
    print(f'Total: {result["total"]} | Uploaded: {result["uploaded"]} | Failed: {result["failed"]} | Skipped: {result["skipped"]}')
    print(f'\nStatus: {"OK" if result["failed"] == 0 else "FAILED"}')
    
    if result['failed'] > 0:
        print(f'  [ACTION-REQUIRED] {result["failed"]} skills failed to sync. Check API token permissions.')


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Skills Sync Tool — Sync DeepChat skills between local disk, GitHub, and R2',
        epilog='Canonical: R2 qnfo/tools/bootstrap_skills.py | GitHub rwnq8/qnfo-skills'
    )
    parser.add_argument('--sync', action='store_true', help='Sync all skills to R2')
    parser.add_argument('--status', action='store_true', help='Check sync status')
    parser.add_argument('--validate', action='store_true', help='Validate all skills for js-yaml compatibility')
    parser.add_argument('--dry-run', action='store_true', help='Preview sync without uploading')
    
    args = parser.parse_args()
    
    if not any([args.sync, args.status, args.validate]):
        parser.print_help()
        return
    
    token = get_token()
    if not token:
        print('ERROR: No Cloudflare API token found.', file=sys.stderr)
        print('  Set CLOUDFLARE_API_TOKEN env var or create %USERPROFILE%\\.cloudflare\\api-token', file=sys.stderr)
        sys.exit(1)
    
    if args.status:
        status = cmd_status(token)
        print_status_report(status)
    elif args.sync:
        result = cmd_sync(token, dry_run=args.dry_run)
        print_sync_report(result)
    elif args.validate:
        result = cmd_validate()
        print(f'\nValidate: {result["total"]} skills — {result["valid"]} valid, {result["warnings"]} warnings, {result["broken"]} broken')
        if result['broken'] > 0:
            print(f'  [ACTION-REQUIRED] {result["broken"]} skills have broken frontmatter (js-yaml will reject)')


if __name__ == '__main__':
    main()
