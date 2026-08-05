#!/usr/bin/env python3
"""
watchtower-version-scan.py — Canonical N-2 version-drift scanner (kaizen Watchtower).

THIN-CLIENT CANONICAL ASSET (git-github v2.17 / kaizen v1.43):
  - PRIMARY canonical:  QNFO/qnfo-skills:kaizen/scripts/watchtower-version-scan.py
  - SECONDARY durable:  R2 deepchat bucket via skill-sync.js
  - Runtime view:       .deepchat\\skills\\kaizen\\scripts\\ (re-hydrated from git/R2)
  - NEVER save copies to Desktop/Documents/Program Files.

Purpose: scan every installed skill SKILL.md for qnfo-core N-2 compliance —
frontmatter `version:` field, H1 header version, and footer `Current: **vX.Y**`
MUST be identical. Detects the N-2-FRONTMATTER-DRIFT-1 class (any direction).

Usage:
  python watchtower-version-scan.py [--skills-root DIR] [--json]

Output: per-skill fm/hdr/ft triple + OK/DRIFT/INCOMPLETE status; nonzero exit
if any skill is DRIFT or INCOMPLETE (for cronjob/cron watchdog integration).

Version history:
  v1.0 (2026-08-05) — promoted to canonical asset from temp k43_watchtower_v2.py.
    Lessons baked in:
    - header regex MUST be case-tolerant (# DeepChat Settings — v1.3, # PERSONAL
      KNOWLEDGE, # QNFO Core) — all-caps-only regex produces false INCOMPLETE
    - footer MUST use LAST 'Current:' occurrence (first may be a banner quote,
      e.g. kaizen's v1.42 banner quotes the old system 2.12 footer)
    - banner-history text is EXEMPT from drift (kaizen v1.25) — only compare
      the three canonical version locations.
"""
import argparse
import json
import os
import re
import sys

DEFAULT_ROOT = os.path.join(os.path.expanduser('~'), '.deepchat', 'skills')

# Case-tolerant: # NAME — vX.Y / # NAME -- vX.Y / # NAME vX.Y / # NAME: vX.Y
HDR_RE = re.compile(r'^#\s+.+?[—-]\s*v?(\d+\.\d+[\.\d]*)', re.MULTILINE)
FM_RE = re.compile(r'^version:\s*"?([\d.]+)', re.MULTILINE)
FT_RE = re.compile(r'Current:\s*\*\*v?([\d.]+)')


def scan_skill(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    fm = FM_RE.search(content)
    hdr = HDR_RE.search(content)
    # LAST occurrence — first may be a banner quote
    fts = list(FT_RE.finditer(content))
    ft = fts[-1].group(1) if fts else None
    vals = {
        'fm': fm.group(1) if fm else None,
        'hdr': hdr.group(1) if hdr else None,
        'ft': ft,
    }
    present = [v for v in vals.values() if v]
    if len(set(present)) == 1 and len(present) >= 2:
        vals['status'] = 'OK'
        vals['version'] = present[0]
    elif len(present) < 2:
        vals['status'] = 'INCOMPLETE'
    else:
        vals['status'] = 'DRIFT'
    return vals


def main():
    ap = argparse.ArgumentParser(description='N-2 version-drift scanner (kaizen Watchtower)')
    ap.add_argument('--skills-root', default=DEFAULT_ROOT)
    ap.add_argument('--json', action='store_true', help='Output JSON')
    ap.add_argument('--only-problems', action='store_true', help='Only report DRIFT/INCOMPLETE')
    args = ap.parse_args()

    results = {}
    for entry in sorted(os.listdir(args.skills_root)):
        path = os.path.join(args.skills_root, entry, 'SKILL.md')
        if not os.path.exists(path):
            continue
        results[entry] = scan_skill(path)

    problems = {k: v for k, v in results.items() if v['status'] != 'OK'}

    if args.json:
        print(json.dumps(results if not args.only_problems else problems, indent=2))
    else:
        for skill, r in sorted(results.items()):
            if args.only_problems and r['status'] == 'OK':
                continue
            print(f"{skill:35s} fm={r['fm'] or '-':8s} hdr={r['hdr'] or '-':8s} "
                  f"ft={r['ft'] or '-':8s} -> {r['status']}")

    # Nonzero exit if any problem (cron watchdog integration)
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
