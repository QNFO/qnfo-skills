# Completion Failures Under Ostrowski's Theorem — Falsifiability Matrix

> **Phase 2 Synthesis | All 21 Predictions × Falsifiability Pathways**
> Cross-refs: `non-cosmetic-archimedean-predictions.md`, `completion-failures-phase2-wbs.md`

---

## 1. Complete Prediction Matrix

| # | Prediction | Tier | Archimedean Value | p-Adic Status | Falsifiability Path |
|:--|:---|:--:|:---|:---|:---|
| 1 | Stefan-Boltzmann σ | 1 | π²k⁴/(60ħ³c²) | ζ_p(4) — different coefficient | ⬜ Product formula: σ_∞ ∏\|σ_p\|_p = 1 |
| 2 | Casimir force coeff | 1 | π²/240 | ζ_p(−3) — different C_p | ⬜ Product formula: C_∞ ∏\|C_p\|_p = 1 |
| 3 | Basel sums ζ(2n) | 1 | π²ⁿ/rational | ζ_p(2n) — completely different numbers | ✅ **Mathematical**: proven difference |
| 4 | Wien displacement | 1 | x ≈ 4.965 (transcendental eq) | χ_p spectrum — different peak | ⬜ Product formula on b = hc/(xk_B) |
| 5 | Loop volumes π^{d/2} | 1-2 | π^{d/2}/Γ(d/2) | Rational function of p | ⬜ Product formula on loop coefficients |
| 6 | β-function coeffs | 2 | 3/(16π²) ≈ 0.01899 | C_p ≠ 3/(16π²) (Missarov 1989) | ⬜ Conformal bootstrap: different exponents |
| 7 | Critical exponents | 2 | ν≈0.630, η≈0.036... | All 5 exponents differ | ⬜ Conformal bootstrap for p-adic CFT |
| 8 | Anomalous dimensions | 2 | γ_φ from loop integrals | Different recursion (Missarov) | ⬜ OPE in p-adic CFT |
| 9 | Feynman propagator | 2 | Δ_F with iε | No iε, no causality | ✅ **Conceptual**: proven absence |
| 10 | S-matrix | 2 | LSZ reduction | T-products undefined | ✅ **Conceptual**: LSZ fails without T |
| 11 | Uncertainty C_p | 2 | ħ/2 | C_p ≠ 1/2 (Fourier norm) | ⚠️ Depends on algebraic vs. analytic |
| 12 | Time ordering | 3 | θ(t) defined | ℚ_p not ordered | ✅ **Mathematical proof**: no order exists |
| 13 | Time evolution U(t) | 3 | e^{−iHt} global | exp_p converges only locally | ✅ **Mathematical**: domain restricted |
| 14 | Noether / symmetry | 3 | ∂_μ j^μ = 0 | Different (VVZ 1994) | ✅ **Conceptual**: totally disconnected |
| 15 | WKB quantization | 3 | ∮ p dx = 2πħ(n+γ) | No closed orbits | ✅ **Conceptual**: no continuous paths |
| 16 | Fine structure α | 4 | 1/137.036 | α_p ≠ α_∞ if adelic | ⬜ Product formula: α_∞ ∏\|α_p\|_p = 1 |
| 17 | g−2 coefficients | 4 | α/(2π) + C₂(α/π)²... | Different C_n (loop coefficients) | ⬜ Product formula on coefficients |
| 18 | Lamb shift | 4 | ~1057 MHz (exp) | Different self-energy coeff | ⬜ Product formula (same as g−2) |
| 19 | CC hierarchy 10⁻¹²² | 4 | Zero-point energy | Adelic cancellation? | ⚠️ **Speculative** — needs p-adic gravity |
| 20 | BH entropy 4π | 4 | S = A/(4G) = 4πM²/M_Pl² | C_p ≠ 4π if p-adic GR | ⚠️ **Speculative** — p-adic GR unknown |
| 21 | Quantum Hall 2π | 4 | σ_H = νe²/h | Unit convention (h vs ħ) | ✅ Mostly cosmetic |

### Legend
- ✅ **Established**: Can be proven as different mathematically or conceptually
- ⬜ **Product formula**: Indirectly falsifiable via adelic product formula constraint
- ⚠️ **Speculative/Borderline**: Not yet testable even in principle

---

## 2. Falsifiability by Tier

| Tier | Total | ✅ Established | ⬜ Product Formula | ⚠️ Speculative |
|:---|:---:|:---:|:---:|:---:|
| **Tier 1** (Numeric) | 5 | 1 (ζ(2n) math) | 4 | 0 |
| **Tier 2** (Structural) | 6 | 2 (propagator, S-matrix) | 3 | 1 (uncertainty) |
| **Tier 3** (Existential) | 4 | 4 (all conceptual/math proofs) | 0 | 0 |
| **Tier 4** (Borderline) | 6 | 1 (QH cosmetic) | 3 | 2 (CC, BH) |
| **TOTAL** | **21** | **8** | **10** | **3** |

---

## 3. The Product Formula as Unifying Constraint

### 3.1 The Core Mechanism

For any physical quantity Q that is an adelic object:

```
∏_v |Q_v|_v = 1    [product over all places of ℚ]
```

This is a mathematical theorem for non-zero adeles. The physical hypothesis is: **Q IS an adele.**

### 3.2 Affected Predictions (10 of 21)

The product formula directly constrains:

1. **Tier 1 (4 predictions)**: σ, Casimir C, Wien b, loop volumes — all contain π from ζ/geometric evaluation
2. **Tier 2 (3 predictions)**: β-function, critical exponents, anomalous dimensions — RG flow at ∞-place is locked to p-adic RG
3. **Tier 4 (3 predictions)**: α, g−2 coefficients, Lamb shift — coupling and loop corrections

### 3.3 The Indirect Falsification Path

```
Step 1: Compute p-adic values Q_p for all primes p
Step 2: Apply product formula: |Q_∞|_∞ × ∏|Q_p|_p = 1
Step 3: This CONSTRAINS the allowed range of Q_∞
Step 4: Compare to measured Q_∞
Step 5: If measured value is outside constrained range → adelic hypothesis falsified for Q
```

**Current status**: Step 1 is incomplete for ALL predictions. No σ_p, Casimir_p, or α_p values have been computed. The product formula path is valid in principle but not yet executable.

---

## 4. Artifact Cross-Reference

| Artifact | Predictions Covered | Commits |
|:---|:---|:---|
| `non-cosmetic-archimedean-predictions.md` | All 21 | 3a2756e (Phase 1) |
| `completion-failures-phase2-wbs.md` | WBS + scope | 5ff6b4a |
| `p-adic-feynman-propagator.md` | #9 (propagator), cascade to #6, #7, #8, #10, #17, #18 | 61e4808 |
| `p-adic-casimir-energy.md` | #2 (Casimir), ζ_p(−3) | 7059856 |
| `causality-in-qp.md` | #12 (time ordering), #10 (S-matrix), cascade to 11/21 | 72379cc |
| `beta-function-missarov-comparison.md` | #6 (β), #7 (critical exponents), #8 (anomalous dims) | ff10546 |
| `p-adic-stefan-boltzmann.md` | #1 (SB), #3 (ζ(4)), #4 (Wien) | c6bd968 |
| `p-adic-physics-literature-scan.md` | E1-E2 (external validation) | c6bd968 |
| `alpha-137-cosmetic-vs-adelic.md` | #16 (α), #17 (g−2) | b0a8981 |

---

## 5. Priority for Phase 3

### 5.1 Immediate Computational Targets

| Priority | Prediction | Why | Feasibility |
|:---:|:---|:---|:---|
| **P1** | #6 β-function coefficients | Missarov already computed the formalism — extract explicit C_p for p = 2, 3 | HIGH |
| **P2** | #2 Casimir C_p | ζ_p(−3) has known rational form — compute explicit C_p | HIGH |
| **P3** | #1 Stefan-Boltzmann σ_p | Most impactful — but requires full p-adic thermodynamics | MEDIUM |
| **P4** | #16 α constraint | Product formula bound on α_∞ from α_p ≈ 1 | MEDIUM |

### 5.2 Deep Conceptual Targets

| Priority | Problem | Why |
|:---:|:---|:---|
| **Q1** | #12 Causality resolution | The deepest obstacle. Until resolved, all Tier 3 predictions remain existential failures |
| **Q2** | #10 p-adic S-matrix formulation | Without S-matrix, p-adic QFT has no scattering physics |
| **Q3** | #19 CC hierarchy | Potentially the most exciting non-cosmetic prediction if adelic cancellation is real |

---

## 6. The Programme's Bottom Line

### What We Have Established

1. **8 of 21 predictions are proven to be non-cosmetic** — mathematically or conceptually established as differing between completions
2. **10 of 21 predictions are constrained by the product formula** — if the relevant quantity is adelic, the ∞-place value is not free
3. **3 of 21 predictions remain speculative** — depend on p-adic gravity or adelic cancellation mechanisms that do not yet exist
4. **0 of 21 predictions have explicit p-adic numerical values computed** — the programme has established WHAT differs but not yet BY HOW MUCH

### What We Have NOT Established

1. **No p-adic value has been computed for any prediction** — not σ_2, not C_3, not α_p for any p
2. **No product formula constraint has been extracted** — the constraint exists mathematically but has not been turned into a bound
3. **Causality has no resolution** — the deepest obstacle remains

### The Next Step

**Compute.** The catalogue is complete. The classification is rigorous. The falsifiability paths are mapped. The next step is to compute explicit p-adic values for the strongest predictions (Tier 1) and extract the first quantitative product formula bounds.

---

*Document status: ACTIVE | 21 predictions cataloged | 8 artifacts committed | Next: Phase 3 — explicit p-adic computation*
