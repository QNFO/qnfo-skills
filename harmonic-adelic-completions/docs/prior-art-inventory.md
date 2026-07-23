# Prior-Art Inventory: Overlap Artifacts from Cross-Domain Session

**Date:** 2026-07-23
**Project:** harmonic-adelic-completions
**Context:** Prior session produced 13 artifacts at workspace level (`artifacts/`) covering p-adic/adélic analysis that overlaps with this program. This document inventories, audits consistency with Phase 0 findings, and maps each to the appropriate Phase 2 pillar.

---

## Artifact Catalog

### A. Directly Overlapping with Phase 0

| # | File | Size | Content Summary | Consistency with Phase 0 |
|:--|:-----|:-----|:----------------|:-------------------------|
| 1 | `alpha-137-cosmetic-vs-adelic.md` | 14.9 KB | Evaluation of whether α⁻¹ ≈ 137 is cosmetic or adelic | ✅ **Consistent** — independently reaches same conclusion (cosmetic). Uses different argument structure (decomposition analysis vs product-formula test). |
| 2 | `completion-failures-phase2-wbs.md` | 11.2 KB | Prior WBS structure for "Completion Failures Under Ostrowski's Theorem" synthesis | ✅ **Informative** — documents workstreams A–E that map to our Phases 2–4 |

### B. Directly Overlapping with Phase 2 Pillars

| # | File | Size | Phase 2 Pillar | Content Summary |
|:--|:-----|:-----|:---------------|:----------------|
| 3 | `beta-function-missarov-comparison.md` | 9.9 KB | Pillar A: β-function | Missarov (1989) p-adic Wilson hierarchical model β-function. Compares all 5 critical exponents to Archimedean. Concludes universality class divergence. |
| 4 | `p-adic-stefan-boltzmann.md` | 8.4 KB | Pillar B: Thermodynamics | Phase space integration over ℚ_p³. Haar measure (no 4π factor). ζ_p(4) fundamentally different from ζ(4)=π⁴/90. Product formula constraint on σ_∞. |
| 5 | `causality-in-qp.md` | 13.4 KB | Pillar C: Causality | Proof that ℚ_p is not an ordered field. Cascade analysis: 11/21 predictions affected. No time-ordering operator. No S-matrix via LSZ. No Noether theorem. |
| 6 | `p-adic-casimir-energy.md` | 12.8 KB | Pillar D: Regularization | Haar vs Lebesgue measure. ζ_p(−3) vs ζ(−3). Product formula constraint on C_∞ = π²/240. Lamoreaux experiment context. |
| 7 | `p-adic-feynman-propagator.md` | 12.2 KB | Pillar E: Propagator | p-adic Feynman propagator via Vladimirov operator. No iε prescription. Connection to Bruhat-Tits tree and Wheeler-DeWitt. |

### C. Supporting Artifacts (Phases 3–4)

| # | File | Size | Relevant Phase | Content Summary |
|:--|:-----|:-----|:---------------|:----------------|
| 8 | `falsifiability-matrix.md` | 8.1 KB | Phase 4 | Complete 21-prediction × falsifiability matrix. Tiers 1–4 classification. 8 established (proven non-cosmetic), 10 product-formula constrained, 3 speculative. |
| 9 | `p-adic-physics-literature-scan.md` | 10.6 KB | Phase 1 | External literature scan: 13 references across Dragovich, Missarov, Varadarajan, Vladimirov, Zelenov, Brekke-Freund, Frampton, Khrennikov. QNFO catalog confirmed unique. |
| 10 | `adelic-experimental-protocols.md` | 11.3 KB | Phase 4 | Experimental protocols for testing p-adic predictions. Spin noise, EELS/RIXS, Gromov δ, Casimir, CMB log-periodic. |
| 11 | `adelic-bias-audit.md` | 11.6 KB | Phase 1 | Confirmation bias audit of the adelic physics program. Identifies 7 bias risks. |
| 12 | `axis1-categorical-foundations.md` | 30.1 KB | Phase 3? | Categorical foundations of adelic physics. Heavy category-theoretic framing. Relevance to HP uncertain — needs Phase 1 assessment. |
| 13 | `seed-idea-backlog.md` | 5.3 KB | Future | Backlog of seed ideas for future research directions. |

---

## Consistency Audit: Prior Art vs Phase 0 Gate Memo

### Agreement Points

| Domain | Phase 0 Finding | Prior Art Position | Agreement |
|:-------|:----------------|:-------------------|:----------|
| "Harmonic" is place-dependent | Vladimirov oscillator ≠ Archimedean HO | `causality-in-qp.md` §"No continuous paths" | ✅ Strong |
| IR attractor ∞-place-specific | β-function has no p-adic analogue | `beta-function-missarov-comparison.md` §"Different universality class" | ✅ Strong |
| RS-1 α⁻¹ cosmetic | Rational core satisfies product formula trivially | `alpha-137-cosmetic-vs-adelic.md` (independent argument) | ✅ Strong |
| ℚ_p not ordered → no time evolution | Implicit in β-function analysis | `causality-in-qp.md` — explicit proof | ✅ Reinforcing |
| ζ-regularization diverges across places | Not covered in Phase 0 | `p-adic-casimir-energy.md` — explicit derivation | ✅ New pillar |

### Potential Tensions

| Domain | Potential Issue | Resolution |
|:-------|:----------------|:-----------|
| Product formula as constraint | Phase 0: "trivial for rationals, inapplicable to α⁻¹" | Prior art: "product formula constrains |Q_∞| via ∏|Q_p|_p" | These are not contradictory — Phase 0 argues no constraint on α⁻¹ specifically because it's not known to be rational; prior art argues product formula WOULD constrain observables IF they were adelic. Resolution: Phase 3 synthesis must formalize the distinction. |
| "Non-cosmetic" predictions | Phase 0 classifies RS-1 as cosmetic | Prior art classifies 8 predictions as "established non-cosmetic" | Different scope: Phase 0 evaluates α⁻¹ specifically; prior art evaluates Stefan-Boltzmann, Casimir, ζ(2n), etc. Not contradictory — complementary. |

---

## Migration Plan

Each prior artifact should be migrated to `docs/prior-art-<slug>.md` with:
1. Original content preserved
2. Cross-reference header linking to related Phase 0 deliverables
3. Consistency note: agreement or tension with Phase 0 findings

| Original | Destination | Priority |
|:---------|:------------|:---------|
| `p-adic-physics-literature-scan.md` | `docs/prior-art-literature-scan.md` | PHASE 1 — needed for due diligence |
| `alpha-137-cosmetic-vs-adelic.md` | `docs/prior-art-alpha-137.md` | PHASE 1 — consistency check |
| `completion-failures-phase2-wbs.md` | `docs/prior-art-wbs.md` | PHASE 1 — structural reference |
| `beta-function-missarov-comparison.md` | `docs/prior-art-missarov-beta.md` | PHASE 2 — Pillar A source |
| `p-adic-stefan-boltzmann.md` | `docs/prior-art-stefan-boltzmann.md` | PHASE 2 — Pillar B source |
| `causality-in-qp.md` | `docs/prior-art-causality-qp.md` | PHASE 2 — Pillar C source |
| `p-adic-casimir-energy.md` | `docs/prior-art-casimir.md` | PHASE 2 — Pillar D source |
| `p-adic-feynman-propagator.md` | `docs/prior-art-feynman-propagator.md` | PHASE 2 — Pillar E source |
| `falsifiability-matrix.md` | `docs/prior-art-falsifiability-matrix.md` | PHASE 4 — source matrix |
| `adelic-experimental-protocols.md` | `docs/prior-art-experimental-protocols.md` | PHASE 4 — protocol source |
| `adelic-bias-audit.md` | `docs/prior-art-bias-audit.md` | PHASE 1 — bias awareness |
| `axis1-categorical-foundations.md` | `docs/prior-art-categorical-foundations.md` | PHASE 1 — assess relevance |
| `seed-idea-backlog.md` | `docs/prior-art-seed-backlog.md` | Future reference |
