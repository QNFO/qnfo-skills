#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BP-3 density-gate.py — Pre-Publication Numerological Risk Bounding

MANDATORY gate (research skill v2.39 BP-3) when a publication claims
"set S approximates observed values V to within epsilon%" and S is dense in R+
(e.g., 5-smooth numbers, rationals, log-linear combinations).

Usage:
    python density-gate.py <paper.md> [--trials N] [--seed 42]

Config format in paper.md (YAML frontmatter or § gate block):
    # If specifying directly:
    density-gate:
      set_description: "5-smooth numbers {2^a·3^b·5^c}"
      is_dense: true
      exponent_bound: 14
      observed_values: [206.77, 3477.2, 16.82, ...]
      tolerance_pct: 0.29

    # Alternative: point to a section in the paper
    density-gate:
      source_section: "§7.2"
      lookup_zenodo: "10.5281/zenodo.21546243"  # if source is in external paper

Output: artifacts/density-gate.md
Exit 0 = p_global <= 0.05 (PASS — claim carries [LOOK-ELSEWHERE GATE: PASSED])
Exit 1 = p_global > 0.05 (BLOCKED — claim is [CONSISTENT WITH LOOK-ELSEWHERE ARTIFACT])
"""
import argparse, json, os, sys, re, math
import numpy as np

# ============================================================
# CONFIG PARSING
# ============================================================
def parse_config(md_path):
    """Extract density-gate config from YAML frontmatter or special block."""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # Try YAML frontmatter
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            frontmatter = text[3:end]
            try:
                import yaml
                cfg = yaml.safe_load(frontmatter)
                return cfg.get('density-gate', {})
            except ImportError:
                pass
    # Fallback: look for density-gate block
    m = re.search(r'density-gate:\s*\n((?:\s{2,}.+\n?)*)', text)
    if m:
        block = m.group(1)
        cfg = {}
        for line in block.split('\n'):
            line = line.strip()
            if ':' in line:
                k, v = line.split(':', 1)
                cfg[k.strip()] = v.strip().strip('"').strip("'")
        return cfg
    return {}

# ============================================================
# MONTE CARLO NULL MODEL
# ============================================================
def run_null(values, exponent_bound, n_trials, seed):
    """Monte Carlo null: random values, best 5-smooth fit, distribution."""
    rng = np.random.default_rng(seed)
    lo, hi = min(values), max(values)
    
    # Precompute sorted log-values of all 5-smooth numbers |a|,|b|,|c| <= B
    log_vals = []
    for a in range(-exponent_bound, exponent_bound + 1):
        for b in range(-exponent_bound, exponent_bound + 1):
            for c in range(-exponent_bound, exponent_bound + 1):
                log_vals.append(a * math.log(2) + b * math.log(3) + c * math.log(5))
    log_vals = np.sort(np.array(log_vals))
    n_triples = len(log_vals)
    
    # Single-ratio null
    log_r = rng.uniform(math.log(lo), math.log(hi), n_trials)
    idx = np.clip(np.searchsorted(log_vals, log_r), 0, n_triples - 1)
    best_log = log_vals[idx]
    alt_log = log_vals[np.maximum(idx - 1, 0)]
    d1 = np.abs(np.exp(best_log) - np.exp(log_r)) / np.exp(log_r)
    d2 = np.abs(np.exp(alt_log) - np.exp(log_r)) / np.exp(log_r)
    best_err = np.minimum(d1, d2) * 100
    
    # Joint null: all N values simultaneously
    n_vals = len(values)
    n_joint = min(n_trials, 100_000)
    log_r_joint = rng.uniform(math.log(lo), math.log(hi), (n_joint, n_vals))
    idx_joint = np.clip(np.searchsorted(log_vals, log_r_joint), 0, n_triples - 1)
    best_log_joint = log_vals[idx_joint]
    alt_log_joint = log_vals[np.maximum(idx_joint - 1, 0)]
    d1_j = np.abs(np.exp(best_log_joint) - np.exp(log_r_joint)) / np.exp(log_r_joint)
    d2_j = np.abs(np.exp(alt_log_joint) - np.exp(log_r_joint)) / np.exp(log_r_joint)
    best_err_joint = np.minimum(d1_j, d2_j) * 100
    max_err_joint = best_err_joint.max(axis=1)
    
    return {
        'median_null_err_pct': float(np.percentile(best_err, 50)),
        'p90_null_err_pct': float(np.percentile(best_err, 90)),
        'n_triples_searched': n_triples,
        'joint_thresholds': {},
        'observed_max_dev_pct': 0.0,
        'p_all_fit_within_observed': 0.0,
    }, best_err, max_err_joint, best_err_joint

# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='BP-3 Density Gate — Monte Carlo null model for dense approximating claims')
    parser.add_argument('paper', nargs='?', help='Path to paper.md')
    parser.add_argument('--trials', type=int, default=1_000_000,
                        help='Number of Monte Carlo trials (default: 1,000,000)')
    parser.add_argument('--seed', type=int, default=20260801,
                        help='Random seed for reproducibility')
    parser.add_argument('--observed', type=str, default=None,
                        help='Comma-separated observed values')
    parser.add_argument('--bound', type=int, default=14,
                        help='Exponent bound (default: 14)')
    parser.add_argument('--values', type=str, default=None,
                        help='Alias for --observed')
    parser.add_argument('--quick', action='store_true',
                        help='Quick check: 100,000 trials instead of 1,000,000')
    args = parser.parse_args()

    # Get values
    values = None
    if args.observed or args.values:
        vals_str = args.observed or args.values
        values = [float(v.strip()) for v in vals_str.split(',') if v.strip()]
    elif args.paper and os.path.exists(args.paper):
        cfg = parse_config(args.paper)
        if cfg.get('observed_values'):
            values = [float(v.strip()) for v in cfg['observed_values'].strip('[]').split(',')]
    if not values:
        print("ERROR: No observed values provided. Use --observed or add density-gate frontmatter.")
        print("Example: python density-gate.py --observed 206.77,3477.2,16.82 --bound 14")
        sys.exit(2)

    n_trials = 100_000 if args.quick else args.trials
    B = args.bound

    print(f'=== BP-3 DENSITY GATE ===')
    print(f'Observed values: {values}')
    print(f'Exponent bound: {B}')
    print(f'Trials: {n_trials:,}')
    print(f'Seed: {args.seed}')

    results, best_err, max_err_joint, _ = run_null(values, B, n_trials, args.seed)

    # Compute observed max deviation (using best 5-smooth fit within bound)
    observed_diffs = []
    for v in values:
        best_d = float('inf')
        for a in range(-B, B + 1):
            for b in range(-B, B + 1):
                c = round((math.log(v) - a*math.log(2) - b*math.log(3)) / math.log(5))
                if abs(c) <= B:
                    fit = (2**a) * (3**b) * (5**c)
                    d = abs(v - fit) / v * 100
                    if d < best_d:
                        best_d = d
        observed_diffs.append(best_d)
    obs_max = max(observed_diffs)

    print(f'\nObserved max deviation: {obs_max:.2f}%')

    # Joint p-value
    p_all = np.mean(max_err_joint <= obs_max)

    print(f'\n--- NULL MODEL ---')
    print(f'Median null error: {results["median_null_err_pct"]:.2f}%')
    print(f'p90 null error: {results["p90_null_err_pct"]:.2f}%')
    print(f'Triples searched: {results["n_triples_searched"]:,}')
    print(f'P(all {len(values)} values fit within {obs_max:.2f}%) = {p_all:.6f} (1 in {1/p_all if p_all > 0 else float("inf"):.1f})')

    # Bonferroni
    p_single = np.mean(best_err <= obs_max)
    bonf = min(1.0, p_single * len(values))
    print(f'Bonferroni-adjusted p = {bonf:.6f}')

    # VERDICT
    print(f'\n{"="*60}')
    if p_all > 0.05:
        print(f'VERDICT: [CONSISTENT WITH LOOK-ELSEWHERE ARTIFACT]')
        print(f'  p_global = {p_all:.4f} > 0.05 — not statistically significant.')
        print(f'  The claim is BOUNDED NUMEROLOGICAL RISK, not a discovery.')
        print(f'  Per BP-3: publication MUST report this verdict.')
        verdict = 1
    else:
        print(f'VERDICT: [LOOK-ELSEWHERE GATE: PASSED]')
        print(f'  p_global = {p_all:.6f} <= 0.05 — the null is rejected.')
        print(f'  The claim carries evidential weight under the look-elsewhere correction.')
        verdict = 0

    # Save report
    report_path = 'artifacts/density-gate.md'
    os.makedirs('artifacts', exist_ok=True)
    with open(report_path, 'w') as f:
        f.write(f'# Density Gate Report\n\n')
        f.write(f'**Date:** 2026-08-01\n')
        f.write(f'**Values:** {values}\n')
        f.write(f'**Exponent bound:** {B}\n')
        f.write(f'**Trials:** {n_trials:,}\n')
        f.write(f'**Seed:** {args.seed}\n\n')
        f.write(f'## Results\n\n')
        for v, d in zip(values, observed_diffs):
            f.write(f'| {v} | {d:.2f}% |\n')
        f.write(f'\n**Observed max deviation:** {obs_max:.2f}%\n')
        f.write(f'**Median null error:** {results["median_null_err_pct"]:.2f}%\n')
        f.write(f'**p_global:** {p_all:.6f}\n')
        verdict_text = '[CONSISTENT WITH LOOK-ELSEWHERE ARTIFACT]' if verdict == 1 else '[LOOK-ELSEWHERE GATE: PASSED]'
    f.write(f'**Verdict:** {verdict_text}\n')
    print(f'\nReport saved to {report_path}')

    sys.exit(verdict)

if __name__ == '__main__':
    main()
