#!/usr/bin/env python3
"""T0.2: ZB Dark Energy Sum.
Sum zero-point ZB energies over all SM particles with species-specific Compton cutoff.
"""

import json

def main():
    # Standard Model particle masses (PDG 2024, in MeV/c^2)
    # Fermions: negative contribution (Pauli exclusion → lower vacuum energy)
    # Bosons: positive contribution
    
    particles = {
        # Leptons (fermions, spin-1/2, -1 weight)
        "electron":   {"mass_MeV": 0.511,     "type": "fermion", "spin_dof": 2},
        "muon":       {"mass_MeV": 105.66,    "type": "fermion", "spin_dof": 2},
        "tau":        {"mass_MeV": 1776.86,   "type": "fermion", "spin_dof": 2},
        "nu_e":       {"mass_MeV": 1e-6,      "type": "fermion", "spin_dof": 1},  # upper bound ~1 eV
        "nu_mu":      {"mass_MeV": 1e-6,      "type": "fermion", "spin_dof": 1},
        "nu_tau":     {"mass_MeV": 1e-6,      "type": "fermion", "spin_dof": 1},
        
        # Quarks (fermions, spin-1/2, -1 weight, 3 colors each)
        "up":         {"mass_MeV": 2.16,      "type": "fermion", "spin_dof": 2, "colors": 3},
        "down":       {"mass_MeV": 4.67,      "type": "fermion", "spin_dof": 2, "colors": 3},
        "strange":    {"mass_MeV": 93.4,      "type": "fermion", "spin_dof": 2, "colors": 3},
        "charm":      {"mass_MeV": 1270,      "type": "fermion", "spin_dof": 2, "colors": 3},
        "bottom":     {"mass_MeV": 4180,      "type": "fermion", "spin_dof": 2, "colors": 3},
        "top":        {"mass_MeV": 172570,    "type": "fermion", "spin_dof": 2, "colors": 3},
        
        # Gauge bosons (bosons, +1 weight)
        "photon":     {"mass_MeV": 0,         "type": "boson",  "spin_dof": 2},  # massless
        "gluon":      {"mass_MeV": 0,         "type": "boson",  "spin_dof": 2, "colors": 8},  # massless
        "W":          {"mass_MeV": 80377,     "type": "boson",  "spin_dof": 3},  # W+, W-, each 3 polarizations
        "Z":          {"mass_MeV": 91187.6,   "type": "boson",  "spin_dof": 3},
        
        # Higgs (boson, +1 weight)
        "higgs":      {"mass_MeV": 125200,    "type": "boson",  "spin_dof": 1},
    }
    
    # Conversion factors
    MeV_to_GeV = 1e-3
    GeV_to_g = 1.78266192e-24  # 1 GeV/c^2 in grams (not needed, working in energy units)
    
    # Critical density of universe (observational)
    # rho_c = 3 H_0^2 / (8 pi G)
    # H_0 = 67.4 km/s/Mpc = 2.19e-18 s^-1 (in natural units)
    # rho_c = 1.878e-29 h^2 g/cm^3 = 8.5e-47 GeV^4 (in natural units with hbar=c=1)
    # rho_Lambda ~ 0.7 * rho_c ~ 6e-47 GeV^4
    
    rho_lambda_obs_GeV4 = 6.0e-47  # GeV^4 (observed dark energy density)
    
    # ZB zero-point energy density per degree of freedom:
    # rho_i = (omega_i^4) / (32 pi^2)  in natural units (hbar=c=1)
    # where omega_i = 2 * m_i (ZB frequency in natural units)
    # So rho_i = (2*m_i)^4 / (32 pi^2) = (16 m_i^4) / (32 pi^2) = m_i^4 / (2 pi^2)
    
    import math
    pi = math.pi
    
    total_rho_GeV4 = 0.0
    details = []
    
    for name, props in particles.items():
        m_GeV = props["mass_MeV"] * MeV_to_GeV
        
        if m_GeV == 0:
            details.append({"particle": name, "mass_GeV": 0, "rho_GeV4": 0, "note": "massless"})
            continue
        
        # ZB frequency in natural units: omega = 2*m
        # Zero-point density: rho = m^4 / (2 pi^2)
        rho_per_dof = m_GeV**4 / (2 * pi**2)
        
        # Total degrees of freedom
        n_dof = props["spin_dof"] * props.get("colors", 1)
        
        # Sign: fermions (-), bosons (+)
        sign = -1 if props["type"] == "fermion" else +1
        
        rho_total = sign * n_dof * rho_per_dof
        total_rho_GeV4 += rho_total
        
        details.append({
            "particle": name,
            "mass_GeV": m_GeV,
            "type": props["type"],
            "n_dof": n_dof,
            "sign": sign,
            "rho_per_dof_GeV4": rho_per_dof,
            "rho_total_GeV4": rho_total,
        })
    
    # Conventional QFT vacuum energy (integrate to Planck scale) would be:
    # rho_QFT ~ M_Planck^4 / (16 pi^2) ~ (1.22e19 GeV)^4 / (16 pi^2) ~ 10^74 GeV^4
    M_Planck_GeV = 1.22e19
    rho_QFT_catastrophe_GeV4 = M_Planck_GeV**4 / (16 * pi**2)
    
    ratio = abs(total_rho_GeV4) / rho_lambda_obs_GeV4
    
    # Check for cancellation
    fermion_sum = sum(d["rho_total_GeV4"] for d in details if d.get("type") == "fermion" or d.get("sign", 0) < 0)
    boson_sum = sum(d["rho_total_GeV4"] for d in details if d.get("type") == "boson" or d.get("sign", 0) > 0)
    
    results = {
        "experiment": "T0.2 — ZB Dark Energy Sum",
        "rho_lambda_obs_GeV4": rho_lambda_obs_GeV4,
        "total_ZB_rho_GeV4": total_rho_GeV4,
        "abs_total_ZB_rho_GeV4": abs(total_rho_GeV4),
        "fermion_contribution_GeV4": fermion_sum,
        "boson_contribution_GeV4": boson_sum,
        "ratio_to_observed": ratio,
        "rho_QFT_catastrophe_GeV4": rho_QFT_catastrophe_GeV4,
        "ZB_to_catastrophe_ratio": abs(total_rho_GeV4) / rho_QFT_catastrophe_GeV4,
        "interpretation": (
            f"The ZB zero-point sum with Compton cutoff yields |ρ| = {abs(total_rho_GeV4):.2e} GeV^4. "
            f"The observed dark energy density is {rho_lambda_obs_GeV4:.2e} GeV^4. "
            f"Ratio = {ratio:.1f}. "
            + ("PASS — Within factor 100 of observed Λ. The 'cosmological constant problem' "
               "may be an artifact of integrating to the Planck scale rather than using "
               "species-specific Compton cutoffs." if ratio < 100 else
               "FAIL — Ratio > 100. ZB zero-point sum does NOT match observed Λ with Compton cutoff alone. "
               "Additional cancellation or suppression mechanism needed.")
        ),
        "verdict": "PASS" if ratio < 100 else "FAIL",
        "details": details,
    }
    
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
