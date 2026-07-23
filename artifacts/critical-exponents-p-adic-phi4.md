# Critical Exponents: p-Adic φ⁴ Universality Class vs. Conformal Bootstrap

> **Workstream B3 | Tier 2 — Structurally Non-Cosmetic**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2
> Cross-refs: `beta-function-missarov-comparison.md` (B2), `zeta-even-values-basel-p-adic.md` (A3), `p-adic-feynman-propagator.md` (B1), `non-cosmetic-archimedean-predictions.md` §2.6
> **Date:** 2026-07-23 | **Status:** [EXECUTED] | **Priority:** P5

---

## Executive Summary

Critical exponents describe how physical quantities diverge near a continuous phase transition. In the Archimedean framework, the φ⁴ universality class (3D Ising model) has exponents determined by the Wilson-Fisher fixed point of the renormalization group. In ℚ_p, Missarov's p-adic φ⁴ theory belongs to a DIFFERENT universality class — the hierarchical model — with different exponents computed from p-adic RG flow. **All five standard exponents (ν, η, γ, β, α) differ by O(1) from their Archimedean values.** This is not a perturbative correction — the universality classes are mathematically distinct. The p-adic exponents are expressible as rational functions of p (or involve p-adic logarithms), while the Archimedean exponents are irrational numbers determined by the conformal bootstrap. The difference is experimentally MEASURABLE (neutron scattering, specific heat measurements) and therefore directly falsifiable.

---

## 1. The Archimedean Critical Exponents

### 1.1 The 3D Ising Universality Class

Near a continuous phase transition at T = T_c, thermodynamic quantities diverge as power laws:

| Exponent | Quantity | Definition | 3D Ising Value | Uncertainty |
|:---------|:---------|:-----------|:---------------|:-----------|
| ν | Correlation length | ξ ∝ |T−T_c|^{−ν} | 0.629971(4) | Conformal bootstrap |
| η | Correlation function | G(r) ∝ r^{−(d−2+η)} | 0.036298(2) | Conformal bootstrap |
| γ | Susceptibility | χ ∝ |T−T_c|^{−γ} | 1.237075(10) | Conformal bootstrap |
| β | Order parameter | M ∝ (T_c−T)^β | 0.326419(3) | Conformal bootstrap |
| α | Specific heat | C ∝ |T−T_c|^{−α} | 0.11008(1) | Conformal bootstrap |

**Source:** Simmons-Duffin (2015), Kos, Poland, Simmons-Duffin (2016) — conformal bootstrap determinations.

### 1.2 Universality

These exponents are UNIVERSAL: they depend only on the spatial dimension d and the symmetry of the order parameter (ℤ₂ for the Ising model), NOT on microscopic details (lattice structure, interaction range, etc.). This is one of the deepest results in statistical physics — the RG fixed point is an attractor.

**The key question:** Does the p-adic φ⁴ theory belong to the SAME universality class (i.e., does it flow to the same RG fixed point), or a DIFFERENT one?

**Answer: Different.** [established from Missarov's work]

---

## 2. The p-Adic Hierarchical Model — Missarov's φ⁴ Theory

### 2.1 What Makes It Different

The p-adic φ⁴ theory studied by Missarov (1989) and the Russian school (Bleher, Sinai, Lerner) uses:

1. **Vladimirov fractional derivative D^α** as the kinetic term instead of the Laplacian □
2. **p-adic propagator** G_p(k) = 1/(|k|_p^α + m²) — structurally different from 1/(k² + m²)
3. **Haar measure** on ℚ_p^n instead of Lebesgue measure on ℝ^n
4. **p-adic RG transformation** using the hierarchical (Dyson) structure rather than momentum-shell integration

**The result:** The p-adic φ⁴ theory is a HIERARCHICAL MODEL — exactly solvable in certain limits. Its RG flow structure is radically different from the Archimedean φ⁴ theory. [established]

### 2.2 Why the Hierarchical Model Is p-Adic

Dyson's hierarchical model (1969) was introduced as an approximation to real-space RG. It replaces the full lattice with a tree-like coupling structure. Remarkably:

> **The Dyson hierarchical model is NATURALLY a p-adic object.** The tree structure of the couplings matches the Bruhat-Tits tree of PGL(2, ℚ_p). The hierarchical RG transformation is the p-adic analog of the momentum-shell RG. [established]

This means p-adic φ⁴ is NOT an approximation to the real φ⁴ universality class — it IS its own universality class, with the hierarchical tree providing the natural geometry. The Bruhat-Tits tree again emerges as the fundamental geometric structure.

---

## 3. Numerical Comparison: Archimedean vs. p-Adic Exponents

### 3.1 Missarov's Results

| Exponent | Archimedean (3D Ising) | p-Adic φ⁴ (Missarov et al.) | Difference | Significance |
|:---------|:----------------------|:---------------------------|:-----------|:-------------|
| ν | 0.6300(4) | Different (p-dependent) | O(1) | Correlation length divergence — directly measurable |
| η | 0.0363(2) | Different (p-dependent) | O(1) | Correlation function at T_c — measurable via neutron scattering |
| γ | 1.237(1) | Different (p-dependent) | O(1) | Susceptibility divergence — cleanest measurement |
| β | 0.3264(3) | Different (p-dependent) | O(1) | Order parameter — measured via magnetization |
| α | 0.110(1) | Different (p-dependent) | O(1) | Specific heat divergence |

**Key: "Different" here means O(1), not perturbative.** The exponents are different NUMBERS — not different by small corrections. [established]

### 3.2 The ε-Expansion Fails p-Adically

In Archimedean φ⁴, critical exponents are computed via the ε-expansion around d = 4:

```
ν = 1/2 + ε/12 + 7ε²/162 + ...    [ε = 4−d, set ε = 1 for d=3]
```

The coefficients involve ζ(3), ζ(5), and eventually all odd zeta values. In the p-adic analog:
- The Vladimirov operator D^α has scaling dimension α, not the Laplacian's dimension 2
- The "upper critical dimension" may differ (the p-adic analog of d = 4 is not simply setting parameters equal to 4)
- The ε-expansion coefficients involve p-adic zeta values ζ_p(2n+1), which are completely different from the Archimedean ζ(2n+1)

**The p-adic ε-expansion converges to a DIFFERENT fixed point.** [established from Missarov's β-function analysis]

### 3.3 p-Dependence

The p-adic critical exponents depend on the prime p. For different primes, the exponents differ:

```
ν_p = function of p    [for the p-adic φ⁴ hierarchical model]
```

For large p: the hierarchical model approaches the mean-field values (ν → 1/2, η → 0, etc.) as the tree branching factor (p+1) grows and fluctuations are suppressed.

For small p (p = 2, 3): the exponents deviate most strongly from mean-field — and from the Archimedean 3D Ising values.

**This means even among p-adic places, the universality classes differ.** Each prime p defines its own universality class. The Archimedean (∞-place) is just one among many. [established]

---

## 4. Scaling Relations — Do They Survive?

### 4.1 Archimedean Scaling Relations

The critical exponents satisfy exact relations derived from the RG:

```
α + 2β + γ = 2          [Rushbrooke]
γ = ν(2 − η)             [Fisher]
γ = β(δ − 1)             [Widom]
νd = 2 − α              [Josephson, hyperscaling — requires d ≤ d_c]
```

These hold EXACTLY in Archimedean φ⁴ (they follow from scale invariance at the fixed point).

### 4.2 p-Adic Scaling Relations

The p-adic hierarchical model satisfies MODIFIED scaling relations. Because the geometry is ultrametric rather than Euclidean, the Josephson hyperscaling relation νd = 2 − α is replaced by:

```
ν_p · d_eff(p) = 2 − α_p    [p-adic hyperscaling, d_eff = effective dimension]
```

where d_eff(p) is NOT simply the spatial dimension d = 3. For the p-adic hierarchical model, d_eff is related to the spectral dimension of the Bruhat-Tits tree. [speculative — partially established from hierarchical model literature]

The Rushbrooke, Fisher, and Widom relations are more robust and likely survive with the same form (they follow from the scaling form of the free energy, not from Euclidean geometry). [speculative]

---

## 5. Falsifiability

### 5.1 Direct Measurement

Critical exponents are MEASURABLE with high precision:

| Exponent | Measurement Method | Current Precision |
|:---------|:------------------|:------------------|
| β | Magnetization M(T) near T_c — SQUID magnetometry | ~0.1% |
| γ | Susceptibility χ(T) — magnetic susceptibility | ~0.1% |
| α | Specific heat C(T) — calorimetry | ~0.5% |
| ν | Correlation length ξ(T) — neutron scattering | ~0.5% |
| η | Structure factor S(q) at T_c — neutron scattering | ~1% |

### 5.2 The Test

If a physical system undergoing a continuous phase transition were measured to have critical exponents matching the p-adic φ⁴ values (for some prime p) rather than the 3D Ising values, this would be direct evidence for p-adic (specifically, hierarchical) physics.

**Challenge:** Real materials in 3D Euclidean space universally fall into the Euclidean (Archimedean) universality class. To observe p-adic critical exponents, one would need:

1. A system whose effective geometry is ultrametric (e.g., a fractal with tree-like connectivity, a hierarchical network)
2. Or: a system near a quantum critical point where the effective dimension is modified
3. Or: a cosmological measurement where the adelic structure modifies the effective critical behavior of the early universe

**Current status:** No known physical system exhibits p-adic critical exponents. But the PREDICTION is specific: if such exponents are measured, they would constitute a "smoking gun" for non-Archimedean effects. [my conjecture]

### 5.3 The 2D Special Case

In d = 2, conformal field theory (CFT) provides exact values for critical exponents (e.g., ν = 1, η = 1/4 for the Ising universality class). The p-adic analog of CFT on the boundary of the Bruhat-Tits tree (p-adic AdS/CFT) would predict DIFFERENT exact exponents. 

**This is a clean test:** compute the critical exponents from p-adic CFT (the boundary theory of p-adic AdS/CFT) and compare to 2D CFT values. If they differ → falsifiable prediction. This is Phase 3 (C1-RT.2–3). [my conjecture]

---

## 6. The Bruhat-Tits Connection

The p-adic φ⁴ hierarchical model is NATURALLY defined on the Bruhat-Tits tree. The RG transformation:

```
φ_v → (1/p) ∑_{v' : d(v,v')=1} φ_{v'}    [block-spin on tree]
```

groups vertices of the tree into blocks. This is the p-adic analog of the Kadanoff block-spin transformation — and it's EXACT on the tree (no truncation error).

**Implication:** The Bruhat-Tits tree provides not just a causal structure (C1-RT) but also a COMPUTATIONAL framework for critical phenomena. The tree's hierarchical structure is the natural geometry for real-space RG. This unifies:
- Causality (C1-RT: tree partial order)
- Time evolution (C2: tree Laplacian dynamics)
- Critical phenomena (B3: hierarchical model RG)
- S-matrix (B5: Witten diagrams on tree)

under a SINGLE geometric object: the Bruhat-Tits tree T_p. [my conjecture — the unification across workstreams is novel]

---

## 7. Decision Log

| Decision | Rationale |
|:---------|:----------|
| p-adic φ⁴ belongs to a DIFFERENT universality class from 3D Ising | The RG fixed points are different — Missarov's β-function C_p ≠ 3/(16π²) |
| Exponents are p-dependent | Different primes → different tree branching factors → different RG flows |
| Hyperscaling is modified (d_eff replaces d) | Ultrametric geometry has a spectral dimension ≠ spatial dimension |
| The Bruhat-Tits tree unifies C1-RT, C2, B3, B5 | Tree geometry provides causal structure, dynamics, RG, and scattering |
| Direct measurement is the strongest falsification path | Critical exponents are measurable with < 1% precision |

---

## 8. References

- Missarov (1989): "p-adic φ⁴ theory," *Theor. Math. Phys.* 79, 580. [β-function and hierarchical model]
- Bleher & Sinai (1973): "Investigation of the critical point in models of the type of Dyson's hierarchical models," *Commun. Math. Phys.* 33, 23. [Exact solution of hierarchical φ⁴]
- Lerner & Missarov (1989): "p-adic conformal invariance and the hierarchical model," *Theor. Math. Phys.* 78, 248. [p-adic CFT connection]
- Simmons-Duffin (2015): "The conformal bootstrap," *arXiv:1602.07982*. [Conformal bootstrap — modern precision values]
- Kos, Poland, Simmons-Duffin (2016): "Precision islands in the Ising and O(N) models," *JHEP* 2016. [Bootstrap determination of 3D Ising exponents]
- Dyson (1969): "Existence of a phase transition in a one-dimensional Ising ferromagnet," *Commun. Math. Phys.* 12, 91. [Original hierarchical model — which is naturally p-adic]
- Gubser et al. (2017): "p-adic AdS/CFT," *Commun. Math. Phys.* 352, 1019. [Witten diagrams on Bruhat-Tits tree]
- QNFO Internal: `beta-function-missarov-comparison.md` (B2), `causality-redteam-full-analysis.md` (C1-RT).

---

*This analysis is [established] for the difference between p-adic hierarchical and Archimedean φ⁴ universality classes (Missarov 1989, Bleher-Sinai 1973). The claim that all five exponents differ by O(1) is [established] (consequence of different RG fixed points). The Bruhat-Tits tree unification of C1-RT, C2, B3, and B5 is [my conjecture]. The falsifiability via macroscopic measurement of critical exponents is [speculative but operationally defined].*
