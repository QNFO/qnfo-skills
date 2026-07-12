---
title: 'Vortex-Enhanced Zitterbewegung: Amplification Feasibility for Trapped-Ion Dirac Simulators'
author: 'Rowan Quni'
date: '2026-07-06'
tags: [zitterbewegung, p-adic, vortex, wave-packet, Dirac, trapped-ion, amplification, quantum-simulation]
---

# Vortex-Enhanced Zitterbewegung: Amplification Feasibility for Trapped-Ion Dirac Simulators

**Rowan Quni — QNFO Research**

## Abstract

Zitterbewegung (ZBW), the relativistic trembling motion predicted by the Dirac equation, has eluded direct experimental observation in free electrons because its characteristic length scale is the Compton wavelength $\lambda_C \approx 2.4 \times 10^{-12}$ m. Guo, Xu & Gu (2025, arXiv:2511.21142) demonstrated that relativistic vortex electron wave packets carrying orbital angular momentum can amplify the ZBW amplitude far beyond the Gaussian-packet baseline. Predin (2026, arXiv:2604.08145) established an exact relation between ZBW dynamics and Berry curvature, identifying a time-independent observable. This paper assesses whether these advances enable ZBW detection in trapped-ion Dirac simulators, and connects the vortex mechanism to the p-adic observable framework of the Adelic Physics Program (Quni 2026, P1/P3/P7). [speculative]

## 1. The Zitterbewegung Gap

ZBW oscillates at $\omega_{\mathrm{ZBW}} = 2mc^2/\hbar \approx 1.6 \times 10^{21}$ Hz with amplitude $\sim \lambda_C \approx 2.4 \times 10^{-12}$ m [established]. Trapped-ion Dirac simulators operate at $\sim 10^{-6}$ m resolution, requiring $\sim 10^{6}\times$ amplification.

## 2. Vortex-Enhanced ZBW

Guo et al. construct a relativistic vortex wave packet:

$$ \Psi_{\ell}(\mathbf{r}, t) = \int d^3 p \, e^{i\ell \phi_p} \, [c_+ u(\mathbf{p}) e^{-i E_p t/\hbar} + c_- v(\mathbf{p}) e^{+i E_p t/\hbar}] e^{i \mathbf{p}\cdot\mathbf{r}/\hbar} $$

Vortex OAM enhances ZBW amplitude "far beyond" Gaussian packets while maintaining coherence. The physical mechanism: the vortex singularity forces overlapping interference between positive- and negative-energy Dirac components.

## 3. Observable Framework

Predin (2026) defines the areal rate of Zitterbewegung: $\dot{\mathcal{A}}_{\mathrm{ZBW}} = \frac{1}{2} \langle [\hat{x}, \hat{v}_y] - [\hat{y}, \hat{v}_x] \rangle$. This observable is time-independent, determined by Berry curvature, and encodes chirality via its sign.

## 4. Connection to p-Adic Framework

The Adelic Physics Program formulates ZBW as a p-adic $\mathbb{Z}_2$ topological invariant. Protocol C (Gromov $\delta$-hyperbolicity) compares Dirac vs. Majorana ZBW trajectories. Vortex amplification is synergistic with Protocol C if it preserves the $\mathbb{Z}_2$ distinction.

## 5. Conclusion

The Guo et al. vortex mechanism, Predin areal-rate observable, and p-adic framework collectively point toward ZBW experimental feasibility. The key unknown is $\mathcal{A}(\ell)$, the amplification factor vs. topological charge. If $\mathcal{A}(\ell) \gtrsim 10^{6}$ for realizable OAM, ZBW becomes experimentally accessible for the first time.

**Disconfirmed if** $\mathcal{A}(\ell) \lesssim 10^{2}$ for any realizable $\ell$.

## References

1. Guo, Z., Xu, B. & Gu, Q. (2025). Vortex-Enhanced Zitterbewegung. arXiv:2511.21142v1.
2. Predin, S. (2026). Chirality of ZBW and Berry curvature. arXiv:2604.08145v2.
3. Quni, R. (2026). ZBW as a p-Adic Observable. doi:10.5281/zenodo.21214264.
4. Quni, R. (2026). Bruhat-Tits Readout Protocol. doi:10.5281/zenodo.21214274.
5. Quni, R. (2026). Adelic Physics Program. doi:10.5281/zenodo.21268809.
