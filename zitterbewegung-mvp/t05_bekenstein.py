#!/usr/bin/env python3
"""T0.5: Bekenstein Bound from ZB Bit-Counting.
Derive the Bekenstein bound I <= 2*pi*R*E/(hbar*c*ln2) from ZB clock ticks.
"""

import json
import math

def main():
    # Physical constants
    hbar = 1.054571817e-34  # J·s
    c = 2.99792458e8        # m/s
    ln2 = math.log(2)
    
    # Test particles
    particles = {
        "electron": 9.1093837e-31,   # kg
        "proton":   1.67262192e-27,  # kg
        "Planck":   2.176434e-8,     # kg (Planck mass)
        "neutron":  1.6749275e-27,   # kg
    }
    
    # Test radii (multiples of Compton wavelength for each particle)
    radius_multipliers = [1, 10, 100, 1000, 1e6]
    
    results_particles = []
    
    for name, mass in particles.items():
        # Compton wavelength
        lambda_C = hbar / (mass * c)
        
        # ZB frequency
        omega_Z = 2 * mass * c**2 / hbar
        
        # Compton time (one ZB tick)
        tau_C = 2 * math.pi / omega_Z  # = pi * hbar / (m c^2)
        
        particle_results = []
        
        for mult in radius_multipliers:
            R = mult * lambda_C
            E = mass * c**2
            
            # Bekenstein bound: I_Bek = 2*pi*R*E / (hbar*c*ln2)
            I_Bek = 2 * math.pi * R * E / (hbar * c * ln2)
            
            # ZB bit count: one bit per Compton time per particle
            # In time R/c (light-crossing time of region), number of ZB ticks:
            # N_ticks = (R/c) / tau_C = R / (c * tau_C)
            # Each tick = 1 bit
            N_ticks = R / (c * tau_C)
            I_ZB = N_ticks  # 1 bit per tick
            
            # Ratio
            ratio = I_ZB / I_Bek if I_Bek > 0 else float('inf')
            
            particle_results.append({
                "R_lambdaC": mult,
                "R_m": R,
                "I_Bekenstein": round(I_Bek, 6),
                "I_ZB": round(I_ZB, 6),
                "ratio_I_ZB_to_I_Bek": round(ratio, 6),
            })
        
        # Average ratio across radii
        avg_ratio = sum(r["ratio_I_ZB_to_I_Bek"] for r in particle_results) / len(particle_results)
        
        results_particles.append({
            "particle": name,
            "mass_kg": mass,
            "lambda_C_m": lambda_C,
            "omega_Z_Hz": omega_Z,
            "tau_C_s": tau_C,
            "radii_results": particle_results,
            "avg_ratio": round(avg_ratio, 6),
        })
    
    # Overall assessment
    all_ratios = [r["ratio_I_ZB_to_I_Bek"] 
                  for p in results_particles 
                  for r in p["radii_results"]]
    mean_ratio = sum(all_ratios) / len(all_ratios)
    min_ratio = min(all_ratios)
    max_ratio = max(all_ratios)
    
    # Check if ratio is O(1)
    is_O1 = 0.1 < mean_ratio < 10.0
    
    results = {
        "experiment": "T0.5 — Bekenstein Bound from ZB",
        "particles_tested": list(particles.keys()),
        "radius_multipliers": radius_multipliers,
        "mean_ratio_I_ZB_to_I_Bek": round(mean_ratio, 4),
        "min_ratio": round(min_ratio, 4),
        "max_ratio": round(max_ratio, 4),
        "is_O1": is_O1,
        "interpretation": (
            f"ZB bit-counting yields I_ZB / I_Bekenstein = {mean_ratio:.4f} (mean across all particles and radii). "
            + ("PASS — Ratio is O(1), suggesting ZB clock ticks naturally saturate "
               "the Bekenstein bound. The ZB frequency provides a physical realization "
               "of the holographic entropy limit." if is_O1 else
               f"FAIL — Ratio = {mean_ratio:.4f} is not O(1). ZB clock does NOT "
               "saturate the Bekenstein bound. The ZB→holography link is unsupported."),
        ),
        "verdict": "PASS" if is_O1 else "FAIL",
        "particle_details": results_particles,
    }
    
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
