#!/usr/bin/env python3
"""Zitterbewegung Cosmology — Phase 0 MVP Runner.
Executes all 5 critical experiments and aggregates results.
"""

import json
import sys
import time

def run_experiment(module_name, display_name):
    """Run an experiment module and return results."""
    print(f"\n{'='*60}")
    print(f"  {display_name}")
    print(f"{'='*60}")
    
    try:
        start = time.time()
        module = __import__(module_name)
        results = module.main()
        elapsed = time.time() - start
        results["runtime_seconds"] = round(elapsed, 2)
        print(f"  Runtime: {elapsed:.1f}s")
        print(f"  Verdict: {results.get('verdict', 'UNKNOWN')}")
        return results
    except Exception as e:
        print(f"  ERROR: {e}")
        return {"experiment": display_name, "verdict": "ERROR", "error": str(e)}

def main():
    print("=" * 60)
    print("  ZITTERBEWEGUNG COSMOLOGY — PHASE 0 MVP")
    print("  5 Critical Experiments")
    print("=" * 60)
    
    experiments = [
        ("t01_fw_residual",       "T0.1 — FW Residual in Curved Spacetime"),
        ("t02_dark_energy",        "T0.2 — ZB Dark Energy Sum"),
        ("t03_cmb_search",         "T0.3 — CMB Log-Periodic Search"),
        ("t04_dirac_materials",    "T0.4 — Dirac Material ZB Meta-Analysis"),
        ("t05_bekenstein",         "T0.5 — Bekenstein from ZB"),
    ]
    
    all_results = []
    
    for module_name, display_name in experiments:
        result = run_experiment(module_name, display_name)
        all_results.append(result)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"  PHASE 0 SUMMARY")
    print(f"{'='*60}")
    
    verdicts = [r.get("verdict", "UNKNOWN") for r in all_results]
    n_pass = sum(1 for v in verdicts if v == "PASS")
    n_fail = sum(1 for v in verdicts if v == "FAIL")
    n_inconclusive = sum(1 for v in verdicts if v not in ("PASS", "FAIL", "ERROR"))
    n_error = sum(1 for v in verdicts if v == "ERROR")
    
    for i, (r, v) in enumerate(zip(all_results, verdicts)):
        name = r.get("experiment", f"Experiment {i+1}")
        symbol = "✅" if v == "PASS" else ("❌" if v == "FAIL" else "⚠️")
        runtime = r.get("runtime_seconds", "?")
        print(f"  {symbol} {name} — {v} ({runtime}s)")
    
    print(f"\n  Results: {n_pass} PASS, {n_fail} FAIL, {n_inconclusive} INCONCLUSIVE, {n_error} ERROR")
    
    # Save results
    output = {
        "project": "Zitterbewegung Cosmology — Phase 0 MVP",
        "date": "2026-07-12",
        "total_experiments": len(experiments),
        "n_pass": n_pass,
        "n_fail": n_fail,
        "n_inconclusive": n_inconclusive,
        "n_error": n_error,
        "experiments": all_results,
    }
    
    with open("phase0_results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n  Results saved to phase0_results.json")
    
    # Overall assessment
    if n_pass >= 3:
        print(f"\n  ★ OVERALL: PROMISING — {n_pass}/5 experiments support the framework")
        print(f"  Recommendation: Proceed to Phase 1 (Foundational Clarification)")
    elif n_pass >= 1:
        print(f"\n  ★ OVERALL: MIXED — {n_pass}/5 experiments support, more work needed")
        print(f"  Recommendation: Refine critical tests before Phase 1")
    else:
        print(f"\n  ★ OVERALL: WEAK — no experiments support the framework")
        print(f"  Recommendation: Re-examine seed assumptions")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
