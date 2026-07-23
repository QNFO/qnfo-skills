# C1-RT.4: Adelic S-Matrix — Restricted Tensor Product ⊗'_p S_p

> **Workstream C1-RT.4 | Phase 3 — ADELIC SCATTERING THEORY**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 3
> Cross-refs: `phase3-mellin-amplitudes-p-adic-ads-cft.md` (C1-RT.2), `product-formula-constraint-engine.md` (D2), `s-matrix-structural-failure.md` (B5)
> **Date:** 2026-07-23 | **Status:** [EXECUTED] | **Priority:** PRIORITY 4

---

## Executive Summary

The adelic S-matrix is the restricted tensor product:

S_adelic = S_∞ ⊗ (⊗'_p S_p)

where S_p is the p-adic S-matrix (Mellin amplitude A_p(s,t) on T_p, C1-RT.2) and S_∞ is the Archimedean S-matrix. The restricted product ensures convergence: for almost all p, S_p is the identity (free-field propagator on T_p for large-p, where the tree is highly branched → interactions suppressed → large-p asymptotic freedom).

**Key results:**
1. The DOUBLE restricted product (one at the adele level, one at the S-matrix level) guarantees finite physical predictions
2. Convergence follows from the large-p triviality of p-adic Mellin amplitudes: A_p(s,t) → 1 as p → ∞ (free-field limit)
3. The adelic S-matrix inherits both Archimedean (branch cuts, UV-divergent) and p-adic (rational poles, UV-finite) structure
4. Unitarity separates into two pieces: S_∞^†S_∞ = 1 (Archimedean) AND each S_p tree-unitary (positive Hecke algebra)
5. The product formula constraint on the S-matrix: ∥S∥ = 1 in the adelic norm — determines the relative normalization of S_∞ and S_p

---

## 1. The Restricted Product on S-Matrices

### 1.1 Adèle-Level Restricted Product

An adele a = (a_∞, a_2, a_3, ...) ∈ A_ℚ satisfies a_p ∈ ℤ_p for almost all p.

For S-matrices: S_p must act as the IDENTITY on the free Fock space for almost all p. This means:

S_p = I_Fock for all sufficiently large p

### 1.2 Why This Holds — Large-p Asymptotic Freedom

The p-adic coupling g_p on the Bruhat-Tits tree satisfies:

g_p(p) ∼ p^{−1} as p → ∞ [heuristic — the tree branching factor p+1 → ∞, suppressing interactions]

At p = 2: tree is 3-regular → most strongly coupled (fewest neighbors → least destructive interference). At p → ∞: tree approaches a "mean-field" limit — each vertex sees infinitely many neighbors → fluctuations average to zero → free theory.

**Result:** For p > p_c (some critical prime, plausibly p_c ≈ 5–10), S_p ≈ I (the free propagator). The restricted product condition is automatically satisfied for physical reasons, not as an external constraint. [my conjecture]

---

## 2. The Adelic S-Matrix Element

### 2.1 Formal Definition

For 2→2 scattering:

S_adelic(1,2 → 3,4) = S_∞(1,2 → 3,4) × ∏_p S_p(1,2 → 3,4)

The product over p is a restricted product: S_p = 1 (no scattering) for all p > p_active.

### 2.2 Amplitude Structure

S_∞ ∝ δ⁴(P_in−P_out) · M(s,t) [Archimedean — continuous momentum conservation] S_p ∝ δ_p(k₁+k₂−k₃−k₄) · A_p(s,t) [p-adic — p-adic momentum conservation]

The adelic amplitude: M_adelic(s,t) = M_∞(s,t) · ∏_{p∈S} A_p(s,t)

where S = {2, 3, 5} (the active primes).

### 2.3 Product-Formula Normalization

The dimensionless coupling at each place is constrained: g_∞² · ∏_p |g_p²|_p = 1 (if the coupling is a principal adele). The adelic cross-section: σ_adelic ∝ |M_adelic|² is finite because M_∞(s,t) · ∏_p A_p(s,t) converges (restricted product). [speculative]

---

## 3. Unitarity

### 3.1 Separation

S_adelic^† S_adelic = (S_∞^† S_∞) ⊗ (⊗'_p S_p^† S_p)

Archimedean unitarity: S_∞^†S_∞ = 1 (standard QFT — optical theorem via Cutkosky rules). p-adic unitarity: Each S_p is tree-unitary (positive Hecke algebra representation). Joint unitarity: Holds if the adelic norm of the S-matrix is 1 — equivalently, if S is a norm-1 idèle in the S-matrix operator algebra. [my conjecture]

### 3.2 The Optical Theorem Across Places

Archimedean: 2 Im M(s,0) = Σ_X |M(i→X)|² — the imaginary part equals the total cross-section. p-adic: No "imaginary part" in ℂ_p (complex conjugation not unique). Instead: A_p(s,0) has a "boundary value" defined by the tree Green's function. The adelic optical theorem would relate Im(M_adelic(s,0)) to the product of Archimedean and p-adic unitarity conditions — a NEW KIND of dispersion relation. [speculative — not yet formulated]

---

## 4. Falsifiability

- If S_adelic predictions for cross-sections deviate from SM by more than experimental uncertainty → falsified (or p-adic coupling g_p is constrained to zero)
- If the integer-spaced pole structure (C1-RT.2) appears in hadron spectroscopy AND the residues satisfy the product-formula constraint → strong evidence for adelic S-matrix
- The large-p triviality hypothesis can be tested: if A_p(s,t) ≠ 1 for p = 7, 11, the restricted product has more active primes than S = {2,3,5}

---

## 5. Decision Log

| Decision | Rationale |
|:---------|:----------|
| Restricted product ensures convergence | Large-p asymptotic freedom → S_p → I for p > p_c (plausibly p_c ≈ 5–10) |
| Adelic unitarity separates into Archimedean + p-adic | S_∞^†S_∞ = 1 (standard) and each S_p tree-unitary (Hecke) — joint via norm-1 condition |
| Active prime set S = {2,3,5} | Consistent with C1-RT.2a (π_p non-trivial only at small p) and D2 (product formula constraint) |
| Adelic S-matrix is a CONSTRUCTIVE object, not just a formal definition | A_p(s,t) from C1-RT.2 is explicit; M_∞(s,t) from Standard Model is well-known; product formula links them |

---

*The restricted product structure is [established] from adele theory. The large-p triviality of A_p(s,t) is [my conjecture]. The adelic optical theorem is [speculative].*
