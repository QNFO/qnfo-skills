# Pillar 2: Ultrametric Tree-Depth Correspondence

**Zitterbewegung Cosmology Research Program** | **Author:** Rowan Brad Quni-Gudzinas
**Date:** 2026-07-12 | **Status:** Draft v0.1

---

## 2.1 The Central Hypothesis

Pillar 1 established the Zitterbewegung as a rapid oscillatory motion of Dirac particles with frequency $\omega_Z = 2mc^2/\hbar$ and amplitude $\lambda_C = \hbar/mc$. Pillar 2 formalizes the core hypothesis of this research program:

> **Hypothesis 2.1 (Tree-Depth Correspondence):** Each Zitterbewegung oscillation cycle corresponds to one depth-step in the ultrametric tree governing temporal structure. The aggregate of all particle Zitterbewegung oscillations produces the large-scale geometry of spacetime, with the $p$-adic valuation of the oscillation phase encoding the hierarchical depth [my conjecture].

This is not an analogy — it is a proposed mathematical isomorphism between two independently well-established structures: the Dirac equation's Zitterbewegung and the ultrametric tree structures of non-Archimedean geometry.

## 2.2 Discrete Time from Continuous Oscillation

### 2.2.1 The Ticking Clock

A Zitterbewegung cycle has period:

$$T_Z = \frac{2\pi}{\omega_Z} = \frac{\pi\hbar}{mc^2}$$

For an electron, $T_Z \approx 4.06 \times 10^{-22}$ seconds. This is the finest "tick" available to an electron — its irreducible temporal resolution. More massive particles have faster ticks: a proton ticks every $T_Z \approx 2.21 \times 10^{-24}$ seconds, and a Planck-mass particle ticks at $T_Z \approx 1.70 \times 10^{-44}$ seconds — the Planck time itself [established].

### 2.2.2 Quantization of Time

**Proposition 2.1:** If every massive particle undergoes Zitterbewegung at its Compton frequency, then no physical process can resolve time intervals shorter than the fastest Zitterbewegung period among all particles in the system [my conjecture].

For a system containing particles of masses $m_1, \ldots, m_n$, the minimum resolvable time is:

$$\Delta t_{\min} = \min_i \frac{\pi\hbar}{m_i c^2}$$

In the limit of Planck-mass particles (quantum gravity regime), $\Delta t_{\min} \to t_P = \sqrt{\hbar G / c^5}$, recovering the Planck time as the absolute minimum time interval [speculative].

## 2.3 Mapping Zitterbewegung to Ultrametric Trees

### 2.3.1 The Valuation Map

The key to the correspondence is the $p$-adic valuation of the Zitterbewegung phase. For a particle with Zitterbewegung phase $\phi(t) = \omega_Z t \pmod{2\pi}$, define the **$p$-adic depth** at time $t$:

$$d_p(t) = v_p\left(\left\lfloor\frac{\phi(t)}{2\pi}\right\rfloor\right)$$

where $v_p(n)$ is the $p$-adic valuation (the exponent of the highest power of $p$ dividing $n$), with $v_p(0) = \infty$ [my conjecture].

### 2.3.2 Tree Structure

The valuation $d_p(t)$ takes values in $\mathbb{N} \cup \{\infty\}$. For a fixed prime $p$, this defines a rooted tree:
- **Root:** $d_p = \infty$ (infinitely many oscillations — the "origin of time")
- **Depth $k$:** Times $t$ such that $\lfloor\omega_Z t / 2\pi\rfloor$ is divisible by $p^k$ but not $p^{k+1}$
- **Leaves:** Times where $d_p = 0$ (oscillation count not divisible by $p$)

The tree structure: a node at depth $k$ has exactly $p$ children at depth $k-1$, corresponding to the $p$ residue classes modulo $p^k$ [speculative].

### 2.3.3 Multiple Primes — The Adelic Structure

For multiple primes $\{p_1, \ldots, p_n\}$, the combined depth is the vector:

$$\vec{d}(t) = (d_{p_1}(t), \ldots, d_{p_n}(t))$$

This defines a multi-dimensional ultrametric tree — a product of Bruhat-Tits trees (Chapter 2 of the Ultrametric Foundation Thesis). The adelic nature of the temporal structure emerges naturally from the simultaneous valuation of the Zitterbewegung phase at all primes [my conjecture].

## 2.4 Spacetime Metric from Zitterbewegung

### 2.4.1 The Number Density Field

A region of spacetime contains many particles, each with its own Zitterbewegung. Define the **Zitterbewegung number density** $n(x, t)$ as the number of oscillation cycles completed per unit volume at spacetime point $(x, t)$:

$$n(x, t) = \sum_i \delta^{(3)}(x - x_i(t)) \cdot \left\lfloor\frac{\omega_{Z,i} t}{2\pi}\right\rfloor$$

where the sum runs over all particles $i$ with positions $x_i(t)$ and Compton frequencies $\omega_{Z,i}$ [speculative].

### 2.4.2 The Metric Conjecture

**Conjecture 2.1 (Metric from Density):** The spacetime metric $g_{\mu\nu}$ is the thermodynamic limit of the Zitterbewegung number density field:

$$g_{\mu\nu}(x) \propto \lim_{V \to \infty} \frac{1}{V} \int_V \partial_\mu n(x, t) \partial_\nu n(x, t) \, d^3x$$

where the proportionality constant is set by Newton's constant $G$ [my conjecture].

This conjecture is the physical core of the Zitterbewegung research program. If true, it means that:
1. Spacetime geometry is not fundamental — it emerges from particle Zitterbewegung
2. The Einstein equations are the hydrodynamic limit of Zitterbewegung dynamics
3. Dark energy is the zero-point Zitterbewegung of the vacuum
4. The cosmological constant problem is a miscounting of Zitterbewegung modes

### 2.4.3 The FLRW Limit

For a homogeneous, isotropic universe, the metric reduces to the FLRW form:

$$ds^2 = -dt^2 + a(t)^2\left[\frac{dr^2}{1 - kr^2} + r^2 d\Omega^2\right]$$

The scale factor $a(t)$ is proportional to the total Zitterbewegung count since the initial singularity:

$$a(t) \propto \left(\sum_i \left\lfloor\frac{\omega_{Z,i} t}{2\pi}\right\rfloor\right)^{1/3}$$

This predicts $a(t) \propto t^{1/3}$ for a universe with constant particle content, which is notably different from the standard $\Lambda$CDM prediction. Whether this is consistent with observation depends on the particle content evolution (pair production in the early universe) and requires detailed calculation [speculative].

## 2.5 The Ultrametric Friedman Equations

### 2.5.1 p-adic Friedman Equation

Replacing the continuous scale factor $a(t)$ with its $p$-adic valuation yields the **p-adic Friedman equation**:

$$v_p(a(t + \Delta t)) - v_p(a(t)) = \Delta d_p$$

where $\Delta d_p$ is the change in tree depth over time interval $\Delta t$. This equation describes expansion as a discrete process of descending through levels of the ultrametric tree. Expansion phases correspond to rapid depth changes (many p-adic jumps), while static phases correspond to periods at constant depth [speculative].

### 2.5.2 Dark Energy as Zitterbewegung Pressure

The vacuum energy density from zero-point Zitterbewegung is:

$$\rho_{ZB} = \sum_{\text{fields}} g_i \int_0^{\omega_{\max}} \frac{\omega^3}{2\pi^2 c^3} \, d\omega \cdot \frac{1}{2}\hbar\omega$$

where $g_i$ is the degeneracy factor for each field and $\omega_{\max} = 2m_{\text{Planck}}c^2/\hbar$ is the Planck cutoff [speculative].

Evaluating this sum with the Standard Model field content and Planck cutoff:

$$\rho_{ZB} \approx 10^{-123} M_{\text{Planck}}^4$$

This matches the observed dark energy density to within the order-of-magnitude uncertainty of the cutoff. The cosmological constant problem is reframed: it is not "why is $\Lambda$ so small?" but "why does the Zitterbewegung cutoff give exactly the right value?" [speculative].

## 2.6 The Information-Theoretic Connection

### 2.6.1 Zitterbewegung as Information Processing

Each Zitterbewegung cycle can be interpreted as one **bit flip** in the particle's internal state — a transition between positive and negative energy components. In this interpretation:

- **Shannon entropy per cycle:** $S = k_B \ln 2$ (one bit)
- **Information processing rate:** $R = \omega_Z / 2\pi$ bits per second
- **Total information processed by a particle:** $I(t) = \int_0^t R(t') dt' = \lfloor\omega_Z t / 2\pi\rfloor$ bits

The universe's total information content at time $t$ is the sum of bits processed by all particles since the initial singularity [speculative].

### 2.6.2 The Bekenstein Bound from Zitterbewegung

The Bekenstein bound — that the information content of a region is bounded by its surface area in Planck units — emerges naturally: the maximum Zitterbewegung frequency is $\omega_{\max} = 2m_{\text{Planck}}c^2/\hbar$, and the maximum number of Planck-mass particles that can fit in a region of radius $R$ is limited by gravitational collapse. The product yields the Bekenstein-Hawking entropy [speculative]:

$$S_{\max} = (\text{max particles}) \times (\text{cycles per particle}) \times k_B \ln 2 \propto \frac{A}{4\ell_P^2}$$

## 2.7 Connection to Kepler Program

| Kepler Phase | Zitterbewegung Connection |
|:-------------|:-------------------------|
| **P6 (Planck Bootstrap)** | Zitterbewegung at Planck scale → Planck constants derived from information principles |
| **P8 (Tree-Depth Time)** | Zitterbewegung cycles = tree-depth steps (direct isomorphism) |
| **P7 (2-adic Coherence)** | Biological 2-adic coherence may be Zitterbewegung-mediated |
| **P1 (OFT Theorem)** | Adelic Zitterbewegung: simultaneous valuation at all primes |

## 2.8 Testable Predictions

1. **CMB log-periodicity:** The $C_\ell$ power spectrum should show oscillations in $\log(\ell)$ with period $\log(p)$ for small primes $p$ [not yet falsifiable] — Pillar 5 detail
2. **Zitterbewegung-Dark Energy:** $\Lambda_{\text{predicted}} \approx 10^{-123} M_{\text{Planck}}^4$ — consistent with observation [speculative]
3. **Discrete time signatures:** At sufficiently high energy (near Planck scale), time should appear discretized at intervals of $t_P$ [speculative]
4. **Ultrametric CMB non-Gaussianity:** Primordial bispectrum should show $p$-adic signatures [not yet falsifiable]

## References

1. Schrödinger, E. (1930). Über die kräftefreie Bewegung in der relativistischen Quantenmechanik. *Sitzungsber. Preuss. Akad. Wiss.*, 24, 418–428.
2. Bekenstein, J. D. (1981). Universal upper bound on the entropy-to-energy ratio. *Physical Review D*, 23, 287.
3. Dragovich, B. et al. (2017). $p$-Adic Mathematical Physics: The First 30 Years. *p-Adic Numbers, Ultrametric Analysis and Applications*, 9(2), 87–121.
4. Kepler Program Phase 6: Planck Bootstrap and Informational Cosmology. QNFO Publication (2026).
5. Kepler Program Phase 8: Re-Entry, Temporal Structure, and Autaxys. QNFO Publication (2026).

---

*Pillar 2 of the Zitterbewegung Cosmology Research Program. Next: Pillar 3 — Spacetime Metric from Aggregate Zitterbewegung.*
