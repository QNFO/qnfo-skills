# Chapter 4: Tate-Amice Spectral Analysis

**Ultrametric Foundation Thesis** | **Author:** Rowan Brad Quni-Gudzinas  
**Date:** 2026-07-12 | **Status:** Draft v0.1

---

## 4.1 Introduction: Non-Archimedean Harmonic Analysis

Chapters 1-3 established the geometry of ultrametric spaces (ultrametric topology, Bruhat-Tits buildings, Berkovich spectra). This chapter develops the **analysis** on these spaces — the tools needed to decompose functions, solve differential equations, and perform spectral computations in the ultrametric setting [established].

The central theme is that non-Archimedean harmonic analysis differs radically from its Archimedean counterpart. Fourier analysis on $\mathbb{R}$ is built on the characters $e^{ikx}$; Fourier analysis on $\mathbb{Q}_p$ is built on additive characters $\chi(\xi x)$ where $\chi: \mathbb{Q}_p \to \mathbb{C}^\times$ is a non-trivial additive character. The resulting theory — the Amice transform and Mahler expansion — is the foundation for ultrametric signal processing and the computational tools of the Kepler Program [established].

## 4.2 The Amice Transform

### 4.2.1 p-adic Fourier Analysis

The **Amice transform** (or $p$-adic Fourier transform) maps functions on $\mathbb{Z}_p$ to functions on $\mathbb{Q}_p$ via:

$$\mathcal{F}_p[f](\xi) = \int_{\mathbb{Z}_p} f(x) \, \chi(\xi x) \, d\mu(x)$$

where $\chi(\xi x) = e^{2\pi i \{\xi x\}_p}$ is the canonical additive character, $\{\cdot\}_p$ is the fractional part in $\mathbb{Q}_p$, and $d\mu$ is the Haar measure on $\mathbb{Z}_p$ (normalized so $\mu(\mathbb{Z}_p) = 1$) [established].

### 4.2.2 Key Properties

1. **Linearity:** $\mathcal{F}_p[af + bg] = a\mathcal{F}_p[f] + b\mathcal{F}_p[g]$
2. **Convolution:** $\mathcal{F}_p[f * g] = \mathcal{F}_p[f] \cdot \mathcal{F}_p[g]$, where convolution is defined with respect to the Haar measure on $\mathbb{Z}_p$ [established]
3. **Inversion:** $\mathcal{F}_p^{-1}[\hat{f}](x) = \int_{\mathbb{Q}_p} \hat{f}(\xi) \, \chi(-x\xi) \, d\mu(\xi)$ for suitably decaying $\hat{f}$
4. **Locally Constant Functions:** A function $f$ is locally constant (the $p$-adic analogue of smoothness) iff its Amice transform $\hat{f}$ has compact support [established]
5. **Compact Support:** $f$ has support in $p^n\mathbb{Z}_p$ iff $\hat{f}(\xi)$ is constant on cosets of $p^{-n}\mathbb{Z}_p$ [established]

### 4.2.3 Relationship to Classical Fourier Analysis

| Property | Real Fourier | Amice (p-adic) |
|:---------|:------------|:---------------|
| Domain | $\mathbb{R}$ | $\mathbb{Z}_p$ or $\mathbb{Q}_p$ |
| Characters | $e^{ikx}$ | $\chi(\xi x) = e^{2\pi i \{\xi x\}_p}$ |
| Smoothness → decay | $\hat{f}(k) \in O(|k|^{-n})$ | $\hat{f}$ has compact support |
| Compact support → analyticity | $\hat{f}$ is entire | $\hat{f}$ is locally constant |
| Sampling theorem | Nyquist-Shannon | p-adic analogue: $p^n$-periodic functions |

## 4.3 Mahler Expansion

### 4.3.1 Binomial Coefficient Basis

The **Mahler expansion** expresses any continuous function $f: \mathbb{Z}_p \to \mathbb{Q}_p$ as a uniformly convergent series of binomial coefficient polynomials:

$$f(x) = \sum_{n=0}^\infty a_n \binom{x}{n}$$

where $\binom{x}{n} = \frac{x(x-1)\cdots(x-n+1)}{n!}$ and $a_n \to 0$ as $n \to \infty$ [established].

### 4.3.2 Mahler Coefficients

The coefficients $a_n$ can be computed via finite differences:

$$a_n = \sum_{k=0}^n (-1)^{n-k} \binom{n}{k} f(k)$$

This is a discrete transform that maps continuous functions on $\mathbb{Z}_p$ to sequences $(a_n)_{n \geq 0}$ with $|a_n|_p \to 0$ [established].

### 4.3.3 Mahler Compression

The Mahler expansion provides natural compression for $p$-adic data. Functions that are "smooth" in the $p$-adic sense (locally constant at finer scales) have Mahler coefficients that decay rapidly in $p$-adic valuation: $v_p(a_n) \to \infty$ as $n \to \infty$ [established].

**Theorem 4.1 (Mahler Compression):** Let $f: \mathbb{Z}_p \to \mathbb{Q}_p$ be $p^n$-locally constant (i.e., $f(x + p^n) = f(x)$ for all $x$). Then $a_m = 0$ for all $m \geq p^n$ [established].

This compression property is the $p$-adic analogue of the Shannon sampling theorem: a bandlimited signal can be exactly represented by a finite number of coefficients. The Mahler expansion gives exact representation for locally constant $p$-adic functions.

## 4.4 p-adic Wavelets and Multiresolution Analysis

### 4.4.1 Haar Basis on $\mathbb{Z}_p$

The Haar wavelet basis on $\mathbb{Z}_p$ is constructed from the indicator functions of residue classes:

$$\phi_{n,k}(x) = p^{n/2} \cdot \mathbf{1}_{k + p^n\mathbb{Z}_p}(x)$$

for $n \geq 0$ and $0 \leq k < p^n$. These functions form an orthonormal basis for $L^2(\mathbb{Z}_p)$ [established].

### 4.4.2 Multiresolution Structure

The subspaces $V_n = \text{span}\{\phi_{n,k} : 0 \leq k < p^n\}$ form a multiresolution analysis (MRA):

$$V_0 \subset V_1 \subset \cdots \subset L^2(\mathbb{Z}_p)$$

with $\dim V_n = p^n$ and $\bigcup_n V_n$ dense in $L^2(\mathbb{Z}_p)$ [established].

The wavelet spaces $W_n = V_{n+1} \ominus V_n$ capture the detail at scale $n$, and the decomposition:

$$L^2(\mathbb{Z}_p) = V_0 \oplus \bigoplus_{n=0}^\infty W_n$$

provides a complete multiscale representation of $p$-adic signals [established].

### 4.4.3 Connection to Bruhat-Tits Trees

The multiresolution structure $V_0 \subset V_1 \subset \cdots$ corresponds precisely to the tree structure of the Bruhat-Tits building for $\mathrm{SL}(2, \mathbb{Q}_p)$ (Chapter 2). Each subspace $V_n$ corresponds to functions constant on the balls of radius $p^{-n}$, and the wavelet spaces $W_n$ correspond to the edges of the Bruhat-Tits tree at depth $n$ [my conjecture].

## 4.5 Spectral Theorem for Compact Operators

### 4.5.1 Non-Archimedean Banach Spaces

Let $X$ be a Banach space over a complete non-Archimedean field $K$. An operator $T: X \to X$ is **compact** if the image of the unit ball is relatively compact. The spectral theory for such operators differs dramatically from the Archimedean case [established].

### 4.5.2 The Non-Archimedean Spectral Theorem

**Theorem 4.2 (Serre, 1962):** Let $T$ be a completely continuous (compact and limit of finite-rank) operator on a non-Archimedean Banach space $X$ over a spherically complete field $K$. Then:

1. The spectrum $\sigma(T)$ consists of $0$ and a sequence $\lambda_n \to 0$
2. For each $\lambda \neq 0$, the eigenspace $E_\lambda = \ker(T - \lambda I)$ is finite-dimensional
3. $X$ decomposes as a topological direct sum of generalized eigenspaces [established]

### 4.5.3 The Volterra Property

In the non-Archimedean setting, many natural operators (integration, convolution with smooth kernel) are **Volterra operators** — they are compact and have spectrum $\sigma(T) = \{0\}$. This is completely different from the Archimedean case where integral operators typically have non-zero point spectrum [established].

**Example:** The operator $(Tf)(x) = \int_0^x f(t) dt$ on the space of continuous functions on $\mathbb{Z}_p$ is a Volterra operator. Its spectrum is $\{0\}$, and its resolvent is entire [established].

## 4.6 Mahler Compression as a Computational Primitive

### 4.6.1 The Kepler Program Connection

The Mahler expansion and its compression property are the mathematical foundation for the Multi-Prime Hensel Codec (Kepler Phase 3). The codec encodes quantum states as $p$-adic integers and uses Mahler compression for efficient representation:

$$\text{encode}: \text{quantum state} \to (a_0, a_1, \ldots, a_{N-1}) \text{ (Mahler coefficients)}$$
$$\text{decode}: (a_0, \ldots, a_{N-1}) \to f(x) = \sum_{n=0}^{N-1} a_n \binom{x}{n}$$

where the truncation at $N$ corresponds to the $p^n$-local constancy of the encoded state [established, Kepler Phase 3 verified].

### 4.6.2 p-adic Caching

The Mahler compression naturally enables **p-adic caching**: storing quantum state data at the coarsest scale (smallest $n$) that preserves the required precision. Lower-precision reconstructions simply use fewer coefficients, enabling progressive refinement and bandwidth-adaptive transmission — a direct consequence of the multiresolution structure [my conjecture].

## 4.7 The Amice Transform as Intrinsic Geometry

### 4.7.1 Intrinsic Formulation

The Amice transform can be formulated intrinsically without reference to the additive character. Let $\mathbf{Ult}$ be the category of ultrametric spaces (Chapter 1). The functor:

$$\mathcal{F}_{\text{int}}: \mathbf{Sh}(\mathbf{Ult}) \to \mathbf{Sh}(\mathbf{Ult}^{\text{op}})$$

maps sheaves on $\mathbf{Ult}$ to sheaves on the opposite category, implementing Fourier duality at the level of the topos [my conjecture].

### 4.7.2 Connection to the Ultrametric Topos

This intrinsic formulation will be developed fully in Chapter 6 (The Ultrametric Topos). The Amice transform emerges as the geometric morphism between the topos of sheaves on $\mathbf{Ult}$ and its dual — a non-Archimedean analogue of Pontryagin duality [speculative].

## 4.8 Open Questions

| RQ | Question | Status |
|:---|:---------|:------|
| RQ-043 | Can the Amice transform be derived from ultrametric topos structure? | Open |
| RQ-044 | Does Mahler compression correspond to a geometric morphism? | Open |
| RQ-043a | Is there a non-Archimedean Plancherel theorem for the intrinsic Amice transform? | Open |

## References

1. Amice, Y. (1975). *Les Nombres p-adiques*. Presses Universitaires de France.
2. Schikhof, W. H. (1984). *Ultrametric Calculus*. Cambridge University Press.
3. van Rooij, A. C. M. (1978). *Non-Archimedean Functional Analysis*. Marcel Dekker.
4. Vladimirov, V. S., Volovich, I. V., & Zelenov, E. I. (1994). *p-Adic Analysis and Mathematical Physics*. World Scientific.
5. Kozyrev, S. V. (2002). Wavelet theory as p-adic spectral analysis. *Izvestiya: Mathematics*, 66(2), 367–376.
6. Khrennikov, A. Yu. & Shelkovich, V. M. (2006). Distributional asymptotics and p-adic wavelets. *Journal of Mathematical Physics*, 47, 113505.

---

*Chapter 4 of the Ultrametric Foundation Thesis. Next: Chapter 5 — Witt Vectors and Deformation Theory.*
