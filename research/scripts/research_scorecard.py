#!/usr/bin/env python3
"""research_scorecard.py — QNFO research-evidence scorecard (0-100).

Pattern: adapted from QNFO/claude-code-aso-skill scorer.py (WEIGHTS + BENCHMARKS ->
calculate_overall_score). Domain: QNFO research-evidence quality per kaizen gates.

Scores a research deliverable on 4 axes (weights total 100):
  - kif60_bayesian (30): pre-registration, falsifiability condition, surprisal
  - source_discipline (30): session-tool-call-only citations, [Background] labeling
  - numeracy (25): sigma traceability, uncertainty source, no false precision
  - verification (15): same-turn tool-call claims, fresh re-query, phantom gates

Usage:
    python research_scorecard.py --input evidence.json [--output out.json]
    --input accepts JSON with keys: kif60, source, numeracy, verification
Exit codes: 0 ok, 1 validation failure, 2 usage error.
Stdlib only. JSON output for integration + human summary to stdout.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

WEIGHTS = {
    "kif60_bayesian": 30,
    "source_discipline": 30,
    "numeracy": 25,
    "verification": 15,
}

BENCHMARKS = {
    "kif60_bayesian": {"min": 0.5, "target": 0.9},
    "source_discipline": {"min": 0.6, "target": 0.95},
    "numeracy": {"min": 0.5, "target": 0.9},
    "verification": {"min": 0.7, "target": 1.0},
}

TIERS = [
    ("POWERFUL", 85.0),
    ("SOLID", 70.0),
    ("GENERIC", 55.0),
    ("WEAK", 0.0),
]


def _read_input(path: str) -> Any:
    if path is None or path == "-":
        return json.load(sys.stdin)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _validate(components: Dict[str, float]) -> None:
    for key in WEIGHTS:
        if key not in components:
            raise ValueError(f"missing component: {key}")
        v = components[key]
        if not (0.0 <= v <= 1.0):
            raise ValueError(f"{key} must be 0.0-1.0, got {v}")


def calculate_overall_score(components: Dict[str, float]) -> Dict[str, Any]:
    _validate(components)
    score = 0.0
    breakdown: Dict[str, Dict[str, Any]] = {}
    for key, weight in WEIGHTS.items():
        raw = components[key]
        b = BENCHMARKS[key]
        # Weighted score: weight * clamp(raw / target, 0, 1.2)
        contrib = weight * min(raw / b["target"], 1.2)
        score += contrib
        breakdown[key] = {
            "raw": raw,
            "weight": weight,
            "contrib": round(contrib, 1),
            "min": b["min"],
            "target": b["target"],
            "status": "PASS" if raw >= b["min"] else "FAIL",
        }
    overall = round(min(score, 100.0), 1)
    tier = next(t for t, thresh in TIERS if overall >= thresh)[0]
    return {
        "overall": overall,
        "tier": tier,
        "breakdown": breakdown,
        "verdict": "SHIP" if overall >= 85.0 else "REVISE" if overall >= 55.0 else "REJECT",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="QNFO research-evidence scorecard")
    ap.add_argument("--input", required=True, help="JSON file or - for stdin")
    ap.add_argument("--output", help="Write JSON result to this path")
    args = ap.parse_args()

    try:
        data = _read_input(args.input)
        result = calculate_overall_score(data)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
    else:
        print(json.dumps(result, indent=2))
        print(f"\nOverall: {result['overall']}/100 ({result['tier']}) — {result['verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
