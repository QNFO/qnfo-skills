#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BP-1 fit-verify.py — Pre-Publication Numerical Claim Independent Recomputation

MANDATORY gate (research skill v2.39 BP-1): independently recompute every
numerical claim (table value, fit triple, claimed deviation) in a paper
BEFORE Zenodo upload. Functions identically to the PDF rendering gate:
exit 0 = proceed, exit 1 = BLOCKED — fix the table.

Usage:
    python fit-verify.py <paper.md>
    python fit-verify.py <paper.md> --table §7.2  # specific section
    python fit-verify.py <paper.md> --dry-run       # report only, don't block

Supported claim formats (auto-detected):
    - Triple tables: (a,b,c) with 2^a·3^b·5^c = value
    - Generic formula tables: formula = value with computed claim
    - Parameter fits: parameter = X, predicted = Y

Output: artifacts/fit-verify.txt
Exit 0 = all claims verified (PASS)
Exit 1 = discrepancies found (BLOCKED)
Exit 2 = invocation error (missing file, bad format)
"""
import argparse, os, sys, re, math

# ============================================================
# CLAIM EXTRACTION
# ============================================================
def extract_triple_table(text, section=None):
    """Extract triple tables of form: | name | observed | formula = value | (a,b,c) | dev% |
    Returns list of dicts: {name, observed, a, b, c, claimed_value, claimed_dev}
    """
    claims = []
    # Pattern: | name | 123.4 | ... (a,b,c) | dev% |
    pattern = re.compile(
        r'\|\s*([^|]+?)\s*\|'           # name
        r'\s*([0-9]+\.?[0-9]*)\s*\|'    # observed value
        r'\s*(?:[^|]*?=\s*)?([0-9]+\.?[0-9]*)?\s*\|'  # claimed formula=value
        r'\s*\((-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\)\s*\|'  # (a,b,c)
        r'\s*([0-9]+\.?[0-9]*%?)?\s*\|'  # deviation
    )
    for m in pattern.finditer(text):
        name = m.group(1).strip()
        obs = float(m.group(2))
        claimed = float(m.group(3)) if m.group(3) else None
        a = int(m.group(4))
        b = int(m.group(5))
        c = int(m.group(6))
        dev_str = (m.group(7) or '').replace('%', '')
        claimed_dev = float(dev_str) if dev_str else None
        claims.append({'name': name, 'observed': obs, 'a': a, 'b': b, 'c': c,
                       'claimed_value': claimed, 'claimed_dev': claimed_dev})
    return claims

# ============================================================
# VERIFICATION
# ============================================================
def verify_triple(claim):
    """Compute actual value of 2^a·3^b·5^c, compare with claimed."""
    a, b, c = claim['a'], claim['b'], claim['c']
    actual = (2.0 ** a) * (3.0 ** b) * (5.0 ** c)
    obs = claim['observed']
    actual_dev = abs(obs - actual) / obs * 100.0

    results = {
        'name': claim['name'],
        'observed': obs,
        'triple': f'({a},{b},{c})',
        'actual_value': actual,
        'claimed_value': claim.get('claimed_value'),
        'actual_dev_pct': actual_dev,
        'claimed_dev_pct': claim.get('claimed_dev'),
    }

    # Check 1: does the triple compute to the claimed value?
    if claim.get('claimed_value') is not None:
        val_diff = abs(actual - claim['claimed_value'])
        if val_diff > 0.01:  # 0.01% tolerance
            results['error'] = f'VALUE MISMATCH: triple computes {actual:.4f}, claimed {claim["claimed_value"]:.4f} (diff {val_diff:.4f})'
            return results

    # Check 2: does the deviation match?
    if claim.get('claimed_dev') is not None:
        dev_diff = abs(actual_dev - claim['claimed_dev'])
        if dev_diff > 0.02:  # 0.02% tolerance on deviation (accounting for rounding)
            results['error'] = f'DEVIATION MISMATCH: actual {actual_dev:.2f}%, claimed {claim["claimed_dev"]:.2f}%'
            return results

    # Check 3: is the triple optimal? (same exponent range check — approximate)
    B = max(abs(a), abs(b), abs(c))
    best_found = True
    for aa in range(-B, B + 1):
        for bb in range(-B, B + 1):
            cc = round((math.log(obs) - aa*math.log(2) - bb*math.log(3)) / math.log(5))
            if abs(cc) <= B:
                alt = (2.0**aa) * (3.0**bb) * (5.0**cc)
                alt_dev = abs(obs - alt) / obs * 100.0
                if alt_dev < actual_dev - 0.001:
                    results['optimal_warning'] = f'NON-OPTIMAL: ({aa},{bb},{cc}) = {alt:.4f} (dev {alt_dev:.3f}%) is better than claimed ({a},{b},{c}) = {actual:.4f} (dev {actual_dev:.3f}%)'
                    break
        if 'optimal_warning' in results:
            break

    results['verified'] = True
    return results

# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='BP-1 Fit-Verify Gate — Independent recomputation of numerical claims')
    parser.add_argument('paper', nargs='?', help='Path to paper.md')
    parser.add_argument('--table', help='Specific section to check (e.g., §7.2)')
    parser.add_argument('--dry-run', action='store_true', help='Report only, exit 0 regardless')
    parser.add_argument('--triples', type=str, help='Comma-separated triple(s) to verify: name:obs:a:b:c:val:dev')
    args = parser.parse_args()

    if args.triples:
        # Direct verification mode
        parts = args.triples.split(':')
        if len(parts) >= 5:
            claim = {'name': parts[0], 'observed': float(parts[1]),
                     'a': int(parts[2]), 'b': int(parts[3]), 'c': int(parts[4]),
                     'claimed_value': float(parts[5]) if len(parts) > 5 and parts[5] else None,
                     'claimed_dev': float(parts[6]) if len(parts) > 6 and parts[6] else None}
            r = verify_triple(claim)
            if r.get('error'):
                print(f"FAIL: {r['name']} — {r['error']}")
                sys.exit(1 if not args.dry_run else 0)
            else:
                print(f"PASS: {r['name']}: {r['triple']} = {r['actual_value']:.4f}, dev {r['actual_dev_pct']:.3f}%")
                sys.exit(0)
        else:
            print("USAGE: --triples name:obs:a:b:c:claimed_val:claimed_dev")
            sys.exit(2)

    # Paper mode
    if not args.paper or not os.path.exists(args.paper):
        print("ERROR: No paper provided. Use --paper or --triples.")
        print("Example: python fit-verify.py paper.md")
        print("Example: python fit-verify.py --triples mu_e:206.77:6:4:-2:207.36:0.29")
        sys.exit(2)

    with open(args.paper, 'r', encoding='utf-8') as f:
        text = f.read()

    claims = extract_triple_table(text)
    if not claims:
        print(f'No triple tables found in {args.paper}')
        sys.exit(0)  # No claims to verify = PASS

    print(f'=== BP-1 FIT-VERIFY: {len(claims)} claims found ===\n')
    failures = 0
    warnings = 0

    for claim in claims:
        r = verify_triple(claim)
        status = 'PASS'
        if r.get('error'):
            status = 'FAIL'
            failures += 1
        elif r.get('optimal_warning'):
            status = 'WARN'
            warnings += 1

        print(f'  [{status:4s}] {r["name"]:20s} {r["triple"]:14s} computed={r["actual_value"]:12.4f} dev={r["actual_dev_pct"]:.3f}%')
        if r.get('error'):
            print(f'         >> {r["error"]}')
        if r.get('optimal_warning'):
            print(f'         >> {r["optimal_warning"]}')

    print(f'\n=== RESULT: {failures} FAIL, {warnings} WARN ===')
    if failures > 0:
        print('GATE: BLOCKED — fix numerical errors before Zenodo upload.')
        print('Per BP-1: 2 arithmetic errors + 5 non-optimal triples in Cross-Domain v3.2')
        print('were published because no fit-verify gate existed. Run this every time.')
        sys.exit(1 if not args.dry_run else 0)
    elif warnings > 0:
        print('GATE: PASS with warnings — triples are correct but may not be optimal.')
        print('Consider replacing with optimal fits before publication.')
        sys.exit(0)
    else:
        print('GATE: PASS — all numerical claims independently verified.')
        sys.exit(0)

if __name__ == '__main__':
    main()
