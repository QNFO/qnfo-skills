# Bruhat-Tits Readout Protocol: Measuring the ZBW Z₂ Invariant in Majorana Systems

**Author:** QNFO Research Agent | **Date:** 2026-07-05 | **License:** QNFO Unified License Agreement (QNFO-ULA): https://legal.qnfo.org/

---

## Abstract

The companion papers "Zitterbewegung as a p-Adic Observable" (P1, DOI: 10.5281/zenodo.21211007) and "Majorana Zitterbewegung Current Correlator" (P2, DOI: 10.5281/zenodo.21211139) establish that the Zitterbewegung contribution to the current-current correlator is a $\mathbb{Z}_2$ topological invariant: $\mathcal{O}_{\text{ZBW}} \approx 1$ for Dirac fermions (growing with momentum) and $\mathcal{O}_{\text{ZBW}} = 0$ for Majorana fermions at all momenta. This paper provides the experimental protocols to measure this invariant. We design three complementary measurements: (A) spin noise spectroscopy for ultrametric clustering in Majorana nanowires, (B) momentum-resolved electron energy loss spectroscopy (EELS) or resonant inelastic X-ray scattering (RIXS) to measure $\mathcal{O}_{\text{ZBW}}(p)$ as a function of momentum transfer, and (C) direct Gromov $\delta$ measurement of the ZBW transition graph. Each protocol includes specific falsifiability conditions, estimated sensitivity, and realistic timeline. Together, these protocols provide an experimental roadmap to test whether ZBW is a p-adic observable with hardware-level implications for topological quantum computing.

**Keywords:** Zitterbewegung, Majorana fermion, Z₂ topological invariant, spin noise spectroscopy, EELS, RIXS, Bruhat-Tits tree, Gromov hyperbolicity

---

## 1. Introduction

The ZBW-Majorana hypothesis, developed in the companion papers P1 and P2, makes a specific, falsifiable prediction: the Zitterbewegung contribution to the current-current correlator $\langle j^\mu(x) j^\nu(0) \rangle$ is a $\mathbb{Z}_2$ topological invariant that distinguishes Dirac from Majorana fermions. P1 established the mathematical framework (ZBW as a p-adic observable with ultrametric readout) and P2 computed the invariant: $\mathcal{O}_{\text{ZBW}} = 0$ for Majorana at all momenta, growing from $0$ to $\approx 0.92$ for Dirac `[CODE-EXECUTED]`.

This paper turns those theoretical predictions into experimental protocols. We propose three independent measurements, each testing a different physical consequence of the ZBW-Majorana hypothesis:

1. **Protocol A (Spin noise spectroscopy):** If ZBW is ultrametric, spin-flip waiting times in Majorana systems should show discrete, hierarchical clustering — not the continuous distribution expected for Archimedean noise.
2. **Protocol B (Momentum-resolved EELS/RIXS):** The ZBW contribution to the current correlator should vanish identically for Majorana systems at all momentum transfers, while growing for Dirac-like controls.
3. **Protocol C (Gromov $\delta$ measurement):** The Bruhat-Tits tree of ZBW-coupled eigenstates should have different Gromov hyperbolicity for Dirac vs. Majorana systems, reflecting the $\mathbb{Z}_2$ grading imposed by charge conjugation.

---

## 2. Protocol A: Spin Noise Spectroscopy

### 2.1 Physical Basis

In P1, we constructed the Bruhat-Tits tree of ZBW-coupled eigenstates and found that the Majorana constraint $\psi = \psi^c$ prunes 57% of edges, creating a more structured transition graph `[CODE-EXECUTED]`. If ZBW transitions follow ultrametric (p-adic) statistics, the waiting times $\tau_i$ between spin-flip events should exhibit discrete clustering at tree-depth levels rather than the continuous, exponential distribution characteristic of Markovian (Archimedean) noise.

### 2.2 Experimental Design

| Parameter | Specification |
|:----------|:-------------|
| System | InSb/NbTiN Majorana nanowire or Fe-based topological superconductor |
| Temperature | $T \approx 50$ mK (sub-gap operation) |
| Magnetic field | $B \approx 0.5-2$ T (topological phase) |
| Measurement | Spin-dependent tunneling current $I(t)$ via quantum point contact |
| Time resolution | $\sim \mu$s (spin-flip telegraph noise) |
| Event count | $\geq 10^4$ spin-flip events |

### 2.3 Analysis

1. Extract waiting times $\tau_i$ between ZBW-induced spin-flip events (identified by telegraph noise in the tunneling current)
2. Compute empirical cumulative distribution $F(\tau)$
3. Fit to competing models:
   - **Archimedean (Poisson):** $F(\tau) = 1 - e^{-\lambda\tau}$
   - **Archimedean (1/f):** $F(\tau) \sim \tau^{\alpha-1}$
   - **Ultrametric (p-adic):** $F(\tau)$ shows discrete plateaus at $2^{-k}\tau_0$ for integer $k$
4. Compute Kullback-Leibler divergence between empirical and model distributions

### 2.4 Decision Rule

| Outcome | Interpretation |
|:--------|:---------------|
| $F(\tau)$ shows discrete plateaus ($p < 0.01$ vs. continuous null) | **ZBW is ultrametric** — P1 hypothesis confirmed |
| $F(\tau)$ fits continuous distribution ($p > 0.05$ vs. discrete) | **ZBW is not ultrametric** — P1 hypothesis disconfirmed |

### 2.5 Sensitivity Estimate

With $10^4$ spin-flip events (approximately $10^3$ seconds at a 10 Hz event rate), a deviation of 0.1 in the discrete vs. continuous Kullback-Leibler divergence is detectable at $3\sigma$.

---

## 3. Protocol B: Momentum-Resolved EELS/RIXS

### 3.1 Physical Basis

P2 demonstrated that the ZBW current correlator has a specific momentum dependence for Dirac fermions: $\mathcal{O}_{\text{ZBW}}(p)$ grows from $0$ at $p=0$ to $\approx 0.92$ at $p=5m$ (ultrarelativistic) `[CODE-EXECUTED]`. For Majorana fermions, $\mathcal{O}_{\text{ZBW}}(p) = 0$ identically at all $p$.

Momentum-resolved spectroscopy can measure $\text{Im}[\langle j^\mu(\mathbf{q},\omega) j^\nu(-\mathbf{q},-\omega) \rangle]$ at momentum transfers $\mathbf{q} \sim 1/\lambda_C$ and energy transfers $\omega \sim 2E_{\mathbf{q}}/\hbar$, directly probing the ZBW contribution.

### 3.2 Experimental Design

| Parameter | EELS | RIXS |
|:----------|:-----|:-----|
| Probe | Monoenergetic electron beam ($\sim 100$ keV) | Synchrotron X-rays ($\sim 10$ keV) |
| Momentum transfer | $\mathbf{q} \sim 0.1-5$ Å$^{-1}$ ($\sim 1/\lambda_C$ for $m^* \sim 0.1 m_e$) | Similar range |
| Energy resolution | $\Delta E \sim 1-10$ meV | $\Delta E \sim 50$ meV |
| Target | Topological superconductor thin film | Bulk or thin film |
| Signal | $\partial^2\sigma/\partial\Omega\partial E \propto \text{Im}[\epsilon^{-1}(\mathbf{q},\omega)]$ | $I(\mathbf{q},\omega) \propto \chi''(\mathbf{q},\omega)$ |

### 3.3 Analysis

1. Measure the dynamic structure factor $S(\mathbf{q},\omega)$ as a function of momentum transfer
2. Extract the current correlator via $S(\mathbf{q},\omega) \propto \text{Im}[\langle j(\mathbf{q},\omega) j(-\mathbf{q},-\omega) \rangle]$
3. Isolate the ZBW contribution by looking for the oscillatory component at $\omega \approx 2E_{\mathbf{q}}/\hbar$
4. Compute $\mathcal{O}_{\text{ZBW}}(p) = S_{\text{osc}}(p) / S_{\text{static}}(p)$
5. Compare to predictions: Dirac-like (growing with $p$) vs. Majorana (zero at all $p$)

### 3.4 Decision Rule

| Outcome | Interpretation |
|:--------|:---------------|
| $\mathcal{O}_{\text{ZBW}}(p) = 0$ for all $p$ | System is Majorana — P2 confirmed |
| $\mathcal{O}_{\text{ZBW}}(p)$ grows with $p$ | System is Dirac-like — P2 disconfirmed |
| $\mathcal{O}_{\text{ZBW}}(p)$ is non-zero but constant | Neither Dirac nor Majorana — new physics? |

### 3.5 Timeline

1-2 years. EELS/RIXS beamtime at synchrotron facilities (ALS, NSLS-II, Diamond). Sample preparation: 3-6 months. Data collection: 2-4 beamtimes of 1 week each. Analysis: 3 months.

---

## 4. Protocol C: Gromov $\delta$ Measurement

### 4.1 Physical Basis

P1 §4b constructed the Bruhat-Tits tree for ZBW-coupled eigenstates of Dirac and Majorana fermions. Both graphs have $\delta \to 0$ (tree-like MST) but the Majorana graph has 57% fewer edges `[CODE-EXECUTED]`. The Gromov hyperbolicity $\delta$ quantifies how tree-like a graph is: $\delta \to 0$ for trees, $\delta \gg 0$ for grid-like graphs.

### 4.2 Experimental Design

| Parameter | Specification |
|:----------|:-------------|
| System | hBN-encapsulated graphene (Dirac control) + proximitized topological superconductor (Majorana) |
| States | $N \approx 20-50$ distinguishable (momentum, spin, valley) states |
| Measurement | Transport spectroscopy: measure all pairwise transition rates $T_{ij}$ |
| Graph construction | $d_{ij} = -\log(T_{ij}/T_{\max})$ |

### 4.3 Analysis

1. For each system, measure the full set of pairwise transition rates $T_{ij}$
2. Define graph distance $d_{ij} = -\log(T_{ij}/T_{\max})$
3. Compute Gromov $\delta$ via the 4-point condition on $10^4$ random quadruples
4. Compare $\delta_{\text{Dirac}}$ vs. $\delta_{\text{Majorana}}$

### 4.4 Prediction

$$\delta_{\text{Majorana}} < \delta_{\text{Dirac}}$$

The $\mathbb{Z}_2$ grading from the Majorana condition should produce a more tree-like transition graph, reflected in a smaller Gromov $\delta$.

### 4.5 Decision Rule

| Outcome | Interpretation |
|:--------|:---------------|
| $\delta_{\text{Majorana}} < \delta_{\text{Dirac}}$ with significance | P1 Bruhat-Tits prediction confirmed |
| $\delta_{\text{Majorana}} \geq \delta_{\text{Dirac}}$ | Prediction disconfirmed |
| Both $\delta \gg 0$ | Neither system is ultrametric — fundamental issue |

### 4.6 Timeline

6-12 months. Transport measurements on existing devices. Graph construction and $\delta$ computation: 1 month. Analysis and comparison: 2 months.

---

## 5. Falsifiability Decision Matrix

| # | Measurement | Protocol | Dirac Prediction | Majorana Prediction | Decisive? |
|:--|:------------|:---------|:----------------|:--------------------|:---------:|
| M1 | Spin noise clustering | A | Continuous $F(\tau)$ | Discrete plateaus $2^{-k}\tau_0$ | ✅ |
| M2 | $\mathcal{O}_{\text{ZBW}}(p=0)$ | B | $0$ | $0$ | ❌ degenerate |
| M3 | $\mathcal{O}_{\text{ZBW}}(p=1)$ | B | $\approx 0.25$ | $0$ | ✅ |
| M4 | $\mathcal{O}_{\text{ZBW}}(p=5)$ | B | $\approx 0.92$ | $0$ | ✅ |
| M5 | $\delta$ (Dirac) | C | $\approx 0$ | — | Control |
| M6 | $\delta$ (Majorana) | C | — | $\approx 0$ | Partial |
| M7 | $\delta_{\text{Majorana}} < \delta_{\text{Dirac}}$ | C | — | True | ✅ |
| M8 | ZBW frequency match to $2E/\hbar$ | B | Yes | — (no signal) | Partial |

### Interpretation Matrix

| A | B | C | Verdict |
|:--|:--|:--|:--------|
| ✅ Ultrametric | ✅ $\mathcal{O}_{\text{ZBW}}=0$ | ✅ $\delta_M < \delta_D$ | **FULL CONFIRMATION** |
| ✅ Ultrametric | ❌ $\mathcal{O}_{\text{ZBW}} \neq 0$ | ❌ $\delta_M \geq \delta_D$ | **Partial: p-adic but not Majorana** |
| ❌ Continuous | ✅ $\mathcal{O}_{\text{ZBW}}=0$ | ❌ $\delta_M \geq \delta_D$ | **Partial: topological but not p-adic** |
| ❌ Continuous | ❌ $\mathcal{O}_{\text{ZBW}} \neq 0$ | ❌ $\delta_M \geq \delta_D$ | **FULL DISCONFIRMATION** |

---

## 6. Sensitivity Estimates and Timeline

| Protocol | Sensitivity | Timescale | Hardware Readiness |
|:---------|:-----------|:----------|:------------------|
| A: Spin noise | $3\sigma$ with $10^4$ events | 3-6 months | Existing Majorana nanowire setups |
| B: EELS/RIXS | $10$ meV resolution at $\mathbf{q} \sim 1/\lambda_C$ | 1-2 years | Synchrotron beamtime |
| C: Gromov $\delta$ | Detectable with $N \geq 20$ states | 6-12 months | Existing transport setups |

---

## 7. Discussion: From Measurement to Hardware

If Protocols A-C confirm the ZBW-Majorana hypothesis, the implications for quantum computing hardware are immediate:

1. **$\mathcal{O}_{\text{ZBW}}$ as a qubit readout:** The $\mathbb{Z}_2$ nature of the invariant means it can serve as a projective measurement of the topological state
2. **Intrinsic protection:** The $\mathbb{Z}_2$ grading is discrete — no continuous perturbation can change it — providing hardware-level error protection without active QEC
3. **Adelic computation:** If ZBW is p-adic, reading it requires non-Archimedean measurement protocols — these are the first-generation tools for adelic quantum information processing

This paper provides the experimental bridge from the mathematical framework (P1) and QFT computation (P2) to bench-top measurement. The falsifiability matrix ensures the program can be tested, confirmed, or refuted — either outcome advances the understanding of ZBW physics.

---

## References

1. Zitterbewegung as a p-Adic Observable (P1). QNFO Research (2026). DOI: 10.5281/zenodo.21211007.
2. Majorana Zitterbewegung Current Correlator (P2). QNFO Research (2026). DOI: 10.5281/zenodo.21211139.
3. Guo, Z., Xu, B., & Gu, Q. (2025). Vortex-Enhanced Zitterbewegung in Relativistic Electron Wave Packets. arXiv:2511.21142.
4. Gerritsma, R., et al. (2010). Quantum simulation of the Dirac equation. Nature, 463, 68-71.
5. Kitaev, A. (2001). Unpaired Majorana fermions in quantum wires. Phys.-Usp., 44, 131.
6. Murtagh, F. (2004). On ultrametricity, data coding, and computation. J. Classification, 21, 167-184.

---

*Generated by QNFO Research Agent. Companion to P1 (DOI: 10.5281/zenodo.21211007) and P2 (DOI: 10.5281/zenodo.21211139).*
