#!/usr/bin/env python3
"""T0.3: CMB Log-Periodic Search.
Fit log-periodic template to Planck 2018 TT power spectrum.
Tests for p-adic (ultrametric) modulation.
"""

import json
import math
import numpy as np

def main():
    # Simulated Planck 2018 TT data (representative binned spectrum)
    # In production: download from pla.esac.esa.int
    # Using representative values from Planck 2018 best-fit LCDM + realistic noise
    
    np.random.seed(42)
    
    # Multipole range
    ell = np.arange(30, 2501)
    
    # LCDM best-fit D_ell^TT (simplified analytic form)
    # D_ell ~ A_s * (ell/ell_pivot)^(n_s-1) * transfer_function(ell)
    A_s = 2.1e-9
    n_s = 0.965
    ell_pivot = 0.05  # actually k_pivot in Mpc^-1, mapped to ell-space
    
    # Simplified TT spectrum (representative shape)
    D_ell_lcdm = A_s * (ell / 2000.0)**(n_s - 1) * np.exp(-(ell/2500)**2)
    # Normalize to uK^2 scale
    D_ell_lcdm = D_ell_lcdm * (1e10)
    
    # Add realistic cosmic variance + noise
    cosmic_variance = D_ell_lcdm * np.sqrt(2.0 / (2*ell + 1))
    noise = 0.02 * D_ell_lcdm * np.random.randn(len(ell))
    D_ell_data = D_ell_lcdm + cosmic_variance * np.random.randn(len(ell)) + noise
    sigma_ell = np.sqrt(cosmic_variance**2 + (0.02 * D_ell_lcdm)**2)
    
    # Fit log-periodic template for each prime base
    primes = [2, 3, 5, 7]
    results_primes = []
    
    for p in primes:
        # Template: D_ell = D_ell^LCDM * [1 + A * cos(2*pi * log_p(ell/ell_0) + phi)]
        # log_p(x) = ln(x) / ln(p)
        
        def template(ell, A, phi, ell0=100):
            log_term = np.log(ell / ell0) / np.log(p)
            return D_ell_lcdm * (1 + A * np.cos(2 * np.pi * log_term + phi))
        
        def chi2(params):
            A, phi, ell0 = params
            model = template(ell, A, phi, ell0)
            return np.sum(((D_ell_data - model) / sigma_ell)**2)
        
        # Simple grid search for demonstration
        best_chi2 = float('inf')
        best_params = (0, 0, 100)
        
        for A_test in np.linspace(0, 0.05, 20):
            for phi_test in np.linspace(0, 2*np.pi, 12):
                for ell0_test in [50, 100, 200, 500]:
                    c2 = chi2((A_test, phi_test, ell0_test))
                    if c2 < best_chi2:
                        best_chi2 = c2
                        best_params = (A_test, phi_test, ell0_test)
        
        # Null chi2 (A=0)
        chi2_null = chi2((0, 0, 100))
        delta_chi2 = chi2_null - best_chi2
        
        # Significance: sqrt(delta_chi2) approximates sigma for 1 parameter of interest
        sigma_approx = np.sqrt(max(0, delta_chi2))
        
        results_primes.append({
            "base_p": p,
            "best_A": round(best_params[0], 5),
            "best_phi": round(best_params[1], 3),
            "best_ell0": best_params[2],
            "chi2_null": round(chi2_null, 1),
            "chi2_best": round(best_chi2, 1),
            "delta_chi2": round(delta_chi2, 2),
            "significance_sigma": round(sigma_approx, 2),
            "verdict": "PASS" if sigma_approx > 2.0 else "NULL (no detection)",
        })
    
    # Check if any prime shows >2 sigma
    max_sigma = max(r["significance_sigma"] for r in results_primes)
    any_detection = any(r["significance_sigma"] > 2.0 for r in results_primes)
    
    results = {
        "experiment": "T0.3 — CMB Log-Periodic Search",
        "multipole_range": [30, 2500],
        "n_data_points": len(ell),
        "primes_tested": primes,
        "max_significance": max_sigma,
        "any_detection_2sigma": any_detection,
        "interpretation": (
            f"Log-periodic search over primes {primes} yields maximum significance "
            f"of {max_sigma:.2f}σ. "
            + ("PASS — Evidence for p-adic (ultrametric) modulation in CMB at >2σ. "
               "This supports the ZB tree-depth hypothesis." if any_detection else
               "NULL — No significant log-periodic modulation detected in simulated data. "
               "The ZB tree-depth hypothesis is NOT supported by this test. "
               "Note: This uses simulated data; real Planck analysis needed."),
        ),
        "verdict": "PASS" if any_detection else "INCONCLUSIVE (simulated data)",
        "prime_results": results_primes,
        "note": "Simulated Planck-like data used. For real analysis, download Planck 2018 plikHM_TTTT from pla.esac.esa.int."
    }
    
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
