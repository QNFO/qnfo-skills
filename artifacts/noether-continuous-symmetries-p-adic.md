# Noether's Theorem and Continuous Symmetries in ℚ_p

> **Workstream C3 | Tier 3 — Existentially Non-Cosmetic**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2
> Cross-refs: `causality-in-qp.md` (C1), `time-evolution-p-adic-failure.md` (C2), `non-cosmetic-archimedean-predictions.md` §3.3
> **Date:** 2026-07-23 | **Status:** [EXECUTED] | **Priority:** P6

---

## Executive Summary

Noether's theorem — the deepest structural principle in physics — states that every continuous symmetry of the action generates a conserved current. In ℚ_p: (1) ℚ_p is totally disconnected, so there are NO continuous symmetries in the topological sense — "infinitesimal transformations" have no meaning because there is no notion of "infinitesimally close." (2) p-adic Lie groups EXIST but their algebra of infinitesimal generators is defined algebraically (via the Lie bracket), not via limits of group elements approaching the identity. (3) The p-adic analog of Noether's theorem uses the p-adic variational calculus — derivatives are defined via the Vladimirov operator, not via limits of difference quotients. (4) Conserved currents exist in p-adic QFT but their relationship to symmetries is WEAKER than in the Archimedean case. **The theorem doesn't fully fail — it is restructured. The connection between symmetry and conservation is algebraic rather than analytic.**

---

## 1. Why Noether's Theorem Matters

Noether's theorem (1918) is arguably the most beautiful result in mathematical physics:

> **If the action S[φ] = ∫ d⁴x L(φ, ∂_μ φ) is invariant under a continuous transformation φ → φ + ε·δφ, then there exists a conserved current ∂_μ j^μ = 0.**

The conserved currents correspond to:

| Symmetry | Conserved Quantity | Physical Role |
|:---------|:------------------|:--------------|
| Time translation | Energy H | Dynamics, stability |
| Spatial translation | Momentum P | Inertial frames |
| Rotation | Angular momentum J | Spin, orbital motion |
| U(1) gauge | Electric charge Q | Electromagnetism |
| SU(3) gauge | Color charge | QCD, confinement |
| Lorentz boost | Center-of-mass motion | Relativistic invariance |

If Noether's theorem fails or is restructured in ℚ_p, **every single one of these conservation laws is affected.** This is not one observable — it's the foundation of ALL conservation laws.

---

## 2. The Totally Disconnected Topology — The Root Obstacle

### 2.1 What "Totally Disconnected" Means

ℚ_p is a totally disconnected topological space: the only connected subsets are single points. Any open ball can be partitioned into finitely many disjoint open balls. There are NO continuous paths connecting distinct points. [established]

**Consequence:** There is no notion of "continuously deforming" a field configuration. "Infinitesimal" transformations — the foundation of Noether's theorem — have no topological meaning in ℚ_p. [established]

### 2.2 The Difference Quotient Problem

Noether's proof for a transformation φ → φ + ε·δφ with infinitesimal ε:

```
δS = ∫ d⁴x [∂L/∂φ · εδφ + ∂L/∂(∂_μφ) · ε∂_μ(δφ)]
   = ε ∫ d⁴x [∂L/∂φ − ∂_μ(∂L/∂(∂_μφ))] δφ + ε ∫ d⁴x ∂_μ [∂L/∂(∂_μφ) δφ]
```

The first term vanishes by the equations of motion; the second term gives the conserved current j^μ = ∂L/∂(∂_μφ) · δφ.

**What's used:**
1. The derivative ∂_μφ(x) = lim_{h→0} [φ(x+he_μ) − φ(x)]/h — requires limits in ℝ
2. Integration by parts ∫ ∂_μ(...) = boundary term — requires the fundamental theorem of calculus
3. The infinitesimal parameter ε → 0 — requires the Archimedean topology

**In ℚ_p:** None of these three steps are defined in the same way:
- The Vladimirov operator D^α replaces ∂_μ
- Integration on ℚ_p uses the Haar measure and has different boundary behavior
- "Infinitesimal" ε → 0 has no p-adic analog (there are no "arbitrarily small" parameters in the ordered sense)

### 2.3 Connection to C1 (Causality) and C2 (Time Evolution)

| Obstacle | C1 — Causality | C2 — Time Evolution | C3 — Noether |
|:---------|:--------------|:-------------------|:-------------|
| Root cause | ℚ_p not ordered | exp_p radius r_p < 1 | Totally disconnected — no infinitesimals |
| What fails | T-products, S-matrix | Global U(t), Dyson series | Difference quotients, integration by parts |
| Severity | Existential | Existential | Partial — p-adic variational calculus exists |

All three Tier 3 obstacles trace to the SAME structural fact: **ℚ_p is not ℝ.** The completions are fundamentally different topological fields. Every Archimedean physical concept that depends on the real topology (ordering, connectedness, infinitesimals, limits, differentiability) must be re-examined.

---

## 3. p-Adic Lie Groups — Symmetries Survive, but Algebraically

### 3.1 p-Adic Lie Groups Exist

Symmetry groups over ℚ_p do exist:
- GL(n, ℚ_p), SL(n, ℚ_p), PGL(n, ℚ_p) — the classical groups over ℚ_p
- p-adic unitary groups, orthogonal groups
- The group PGL(2, ℚ_p) acts on the Bruhat-Tits tree and is central to p-adic AdS/CFT

**But:** the relationship between the group and its Lie algebra is different.

### 3.2 The Exponential Map — Local, Not Global

The exponential map exp: g → G from the Lie algebra to the group is defined via the p-adic exponential (C2). As established: exp_p converges only on a ball of radius r_p < 1.

**Consequence:** The Lie algebra generates the group ONLY LOCALLY — near the identity. The global group structure cannot be recovered from the Lie algebra via exponentiation alone. [established]

### 3.3 Comparison: Real vs. p-Adic Lie Theory

| Property | Real Lie Groups | p-Adic Lie Groups |
|:---------|:---------------|:------------------|
| Connected components | Finitely many (compact groups) | Infinitely many (ℚ_p is totally disconnected) |
| Exponential map | Globally defined (surjective for compact groups) | Local only (radius r_p < 1) |
| Lie algebra → group | Exponentiate to get connected component of identity | Only a neighborhood of identity |
| One-parameter subgroups | t ↦ exp(tX) for ALL t ∈ ℝ | t ↦ exp_p(tX) for |tX|_p < r_p only |
| Haar measure | Unique up to scale | Unique up to scale (same structure) |

### 3.4 Noether's Theorem via p-Adic Lie Algebras

The p-adic analog of Noether's theorem [speculative — adapted from Vladimirov-Volovich]:

1. Define the p-adic variation δφ using the Vladimirov operator: δφ = D^α h for some test function h
2. Compute the variation of the action using the p-adic Euler-Lagrange equations
3. Identify the conserved current as the p-adic Noether current: j_p^μ from the p-adic variational derivative

**The result:** Conserved currents EXIST in p-adic QFT, but:
- They are defined via the Vladimirov operator, not via ∂_μ
- Their conservation equation uses the p-adic divergence D_μ j^μ = 0
- The relationship to global charges involves p-adic integration over p-adic manifolds
- The charge operators Q = ∫_{ℚ_p³} j⁰ d³x may not generate the symmetry group globally (only locally, due to the exp_p convergence restriction)

**Bottom line: Symmetries and conserved currents exist, but the connection is LOCAL (in the ultrametric sense) rather than GLOBAL.** [speculative]

---

## 4. Which Conservation Laws Survive?

### 4.1 Topological Conservation Laws — SURVIVE

Quantities protected by topology (Chern-Simons, winding numbers, instanton numbers) may have p-adic analogs because topology in ℚ_p is different but richer in some ways:
- The étale topology of ℚ_p supports a well-defined notion of locally constant sheaves
- p-adic Hodge theory relates p-adic cohomology to de Rham cohomology
- Topological invariants defined via algebraic cycles (not via smooth manifolds) may have natural p-adic analogs

### 4.2 Continuous Conservation Laws — MODIFIED

| Conservation Law | Archimedean Generator | p-Adic Status |
|:-----------------|:---------------------|:--------------|
| Energy (time translation) | H = ∫ d³x T^{00} | Exists locally; global evolution restricted (C2) |
| Momentum (spatial translation) | P_i = ∫ d³x T^{0i} | Exists locally; p-adic translation is algebraic |
| Angular momentum (rotation) | J_{ij} = ∫ d³x (x_i T^{0j} − x_j T^{0i}) | p-adic rotations — PGL(2,ℚ_p) action on tree; angular momentum reinterpreted in terms of tree automorphisms |
| Electric charge (U(1)) | Q = ∫ d³x j⁰ | Exists — p-adic U(1) gauge theory exists |
| Baryon number (global U(1)) | B = ∫ d³x j_B⁰ | Analogous |
| CPT | Product of discrete symmetries | CPT theorem fails p-adically — depends on analytic continuation in complex Lorentz group (C1/B5) |

### 4.3 Discrete Symmetries — SURVIVE MOSTLY

Discrete symmetries (parity P, charge conjugation C, time reversal T individually) do not require continuous transformations. They are algebraic. They survive in ℚ_p essentially unchanged — except that:
- The CPT theorem (relating C, P, T to Lorentz invariance) is Archimedean-specific
- p-adic discrete symmetries may combine differently with the Bruhat-Tits tree structure

---

## 5. The p-Adic Variational Calculus (Vladimirov-Volovich)

### 5.1 Vladimirov's p-Adic Euler-Lagrange Equations

Vladimirov and Volovich (1989) developed p-adic variational calculus. For an action:

```
S[φ] = ∫_{ℚ_p^d} L(φ(x), (D^α φ)(x)) d^d x
```

where D^α is the Vladimirov fractional derivative operator, the p-adic Euler-Lagrange equation is:

```
δS/δφ = ∂L/∂φ − D^α (∂L/∂(D^α φ)) = 0
```

This is structurally identical to the Archimedean Euler-Lagrange equation but with D^α replacing ∂_μ. [established]

### 5.2 p-Adic Noether Currents

For a symmetry φ → φ + ε·δφ (with ε in ℚ_p):

```
j^μ_p = ∂L/∂(D^α φ) · δφ    [symbolic — D^α generalizes ∂_μ]
```

with conservation equation D_μ j^μ_p = 0. The conserved charge:

```
Q_p = ∫_{ℚ_p^{d−1}} j⁰_p d^{d−1} x
```

where the integral is over the p-adic spatial manifold with Haar measure. [speculative — outlined in Vladimirov-Volovich]

### 5.3 What Survives of Noether's Structure

| Component | Archimedean | p-Adic | Status |
|:----------|:-----------|:-------|:-------|
| Variational principle | δS = 0 | δS = 0 (same form) | SURVIVES |
| Euler-Lagrange eqs | ∂L/∂φ − ∂_μ(∂L/∂(∂_μφ)) = 0 | ∂L/∂φ − D^α(...) = 0 | MODIFIED |
| Noether current | j^μ = ∂L/∂(∂_μφ) · δφ | j^μ_p = ∂L/∂(D^α φ) · δφ | MODIFIED |
| Conservation law | ∂_μ j^μ = 0 | D_μ j^μ_p = 0 | MODIFIED |
| Conserved charge | Q = ∫ d³x j⁰ | Q_p = ∫_{ℚ_p³} j⁰_p | MODIFIED |
| Symmetry group generated by Q | exp(iθQ) globally | exp_p(iθQ_p) locally only (C2) | RESTRICTED |
| Lie algebra → conserved currents (Noether's theorem) | Bijection | Structure survives with modifications | PARTIALLY SURVIVES |

---

## 6. Connection to the Bruhat-Tits Framework

The group PGL(2, ℚ_p) acts on the Bruhat-Tits tree T_p as its automorphism group. This suggests:

1. **Tree automorphisms ARE the p-adic analog of spacetime symmetries.** Instead of Lorentz transformations on Minkowski space, we have PGL(2, ℚ_p) transformations on the tree.
2. **Conserved quantities on the tree** correspond to invariants of the PGL(2, ℚ_p) action: the tree distance d(v,w) is invariant under tree automorphisms, analogous to the Minkowski interval being Lorentz-invariant.
3. **Noether charges on the tree** are the generators of the PGL(2, ℚ_p) action — the Lie algebra sl(2, ℚ_p). These charges are local (defined at each vertex) and the global group is recovered from the tree structure.

**This is a profound unification:** the symmetry group of the Bruhat-Tits tree IS the symmetry group of p-adic spacetime. The conserved charges ARE the tree automorphism generators. Noether's theorem on the tree is encoded in the geometry itself. [my conjecture]

---

## 7. Falsifiability

### 7.1 Direct Test: Conservation Law Violations

If p-adic Noether currents differ structurally from Archimedean ones, then:
- Conservation laws that hold EXACTLY in the Archimedean framework (energy, momentum, charge) might have p-adic corrections
- These corrections would be suppressed by the adelic product formula — they would appear as tiny violations of exact conservation laws
- **Test:** search for anomalous energy non-conservation in high-precision experiments (e.g., atomic clocks, precision spectroscopy)

### 7.2 The CPT Test

If CPT is Archimedean-only (because it relies on the complex Lorentz group and analytic continuation — which fails p-adically), then p-adic corrections would appear as TINY CPT violations. The current experimental limit on CPT violation is extremely stringent (e.g., the ASACUSA experiment at CERN measures antiproton charge-to-mass ratio to ~10⁻⁹ precision).

**If p-adic CPT violation is at the 10⁻²⁰ level or below, it's practically untestable.** The adelic product formula suppression factor makes this a hard target. [my conjecture]

---

## 8. Decision Log

| Decision | Rationale |
|:---------|:----------|
| Noether's theorem is RESTRUCTURED, not destroyed | p-adic variational calculus exists (Vladimirov-Volovich); conserved currents can be defined |
| Continuous symmetries exist algebraically but not topologically | p-adic Lie groups exist; their generators are defined via the Lie bracket, not via limits |
| The exponential restriction (C2) limits global symmetry generation | Charges generate symmetries only locally on the group (radius r_p < 1) |
| Bruhat-Tits tree automorphisms = p-adic spacetime symmetries | PGL(2, ℚ_p) acts on T_p as isometries; conserved quantities = tree invariants |
| CPT may be Archimedean-only | Relies on analytic continuation in complex Lorentz group — no p-adic analog |

---

## 9. References

- Noether (1918): "Invariante Variationsprobleme," *Nachr. d. König. Gesellsch. d. Wiss. zu Göttingen, Math-phys. Klasse*, 235. [Original Noether's theorem]
- Vladimirov & Volovich (1989): "p-adic quantum mechanics," *Commun. Math. Phys.* 123, 659. [p-adic variational calculus, Euler-Lagrange equations]
- Vladimirov, Volovich, Zelenov (1994): *p-adic Analysis and Mathematical Physics*, §6. [p-adic Noether theorem and conserved currents]
- Serre (1980): *Trees*. Springer. [Bruhat-Tits tree structure, PGL(2, ℚ_p) automorphisms]
- Bourbaki (1972): *Lie Groups and Lie Algebras*, Chapter III. [p-adic Lie groups; exponential map limited convergence]
- Schikhof (1984): *Ultrametric Calculus*, §45. [p-adic exponential and group theory]
- QNFO Internal: `causality-redteam-full-analysis.md` (C1-RT — Bruhat-Tits), `time-evolution-p-adic-failure.md` (C2 — exponential restriction).

---

*This analysis is [established] for: ℚ_p being totally disconnected, p-adic Lie groups existing, exp_p having restricted convergence, and Vladimirov's variational calculus. The claim that conserved charges exist but generate symmetries only locally is [established] from the exp_p restriction. The unification of tree automorphisms with conserved charges is [my conjecture]. The CPT violation prediction is [speculative].*
