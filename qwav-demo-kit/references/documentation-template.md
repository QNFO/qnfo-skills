# Documentation Template for Scientific Demos

Use this template for every demo README.md. Fill in all sections marked with `< >`.
Remove this intro paragraph from the final output.

---

# <Demo Title>

**Status:** ✅ LIVE — deployed <YYYY-MM-DD>
**URL:** https://qnfo.github.io/<repo-name>/

## What This Shows

<One paragraph explaining the concept in plain language. Assume the reader
has basic scientific literacy (undergraduate physics/CS) but no domain
expertise in this specific topic. Answer: what would a colleague from
a different field understand in 30 seconds?>

## The Math

<The key equation(s) in Unicode math. If the demo page uses KaTeX/MathJax,
use LaTeX. Otherwise use Unicode: epsilon, sigma^2, sum, product, sqrt, integral, partial, approx, le, ge, arrow, cross, dot>

```
Key equation:  LER(d) = f^d(epsilon) where f(epsilon) = sum_{j=floor(p/2)+1}^{p} C(p,j) epsilon^j (1-epsilon)^{p-j}
```

<Explain what each variable means in one line each.>

## How to Use

1. **Start here:** <The primary interaction — the first thing a user should try>
   - What to click/drag
   - What to look for in the output
   - Expected immediate result

2. **Try changing:** <Secondary controls and what they reveal>
   - Parameter 1: effect on visualization
   - Parameter 2: effect on readouts

3. **Watch for:** <Key insight the demo is designed to demonstrate>
   - Observable phenomenon 1
   - Observable phenomenon 2

## Parameters

| Parameter | Symbol | Range | Default | Description |
|:----------|:-------|:------|:--------|:------------|
| <name> | <symbol> | <range> | <default> | <what it controls and why you would change it> |

## Interpreting the Output

### Visualization
<What each visual element represents: colors, shapes, positions, sizes>

### Readouts
| Readout | Meaning |
|:--------|:--------|
| <label> | <what this number tells you and its units> |

## Reproducibility

- **Seed:** <seed value> (fixed for deterministic output)
- **PRNG:** mulberry32 (32-bit seeded generator)
- **Algorithm:** <brief description of the computational core>
- **Monte Carlo trials:** <N> (if applicable)
- **Deterministic:** Yes — same seed + same parameters = identical output

## Limitations

<What this demo does NOT show. Be honest about simplifications, assumptions,
and pedagogical choices. Examples:
- This is a pedagogical model; it does not simulate actual quantum hardware
- The tree is fixed at build time; it does not grow adaptively
- Monte Carlo uses only N trials; statistical noise is ~1/sqrt(N)
- Color scale is linear; log-scale may be more appropriate for some regimes
>

## Source

- **Strategy:** QNFO/QWAV strategy/3.0.md — Tier 1 Artifact <A#>
- **Publication:** <paper title with link>
- **Build:** single-file HTML, canvas rendering, zero external dependencies
- **Repository:** https://github.com/QNFO/<repo-name>

## Testing

- **Test suite:** `python scripts/test-demo.py --url <live-url>`
- **Math verification:** `__qwavMathVerify.verifyAll(window.S)` in browser console
- **Last test run:** <YYYY-MM-DD> — <N>/<N> passing, zero console errors

---

*Generated with DeepChat | All page content is AI-generated and for reference only.*
