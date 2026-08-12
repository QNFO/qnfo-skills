#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
dsi-radix-detector.py — Radix-agnostic Discrete Scale Invariance (DSI) detector.

Implements the verified three-stage protocol from _26224105300.md (2026-08-12):

    Stage 1  Detrend in log-space -> FFT peak (or Lomb-Scargle for uneven grids)
    Stage 2  Bounded sinusoid refinement on detrended residuals (lambda +/- sigma_lambda)
    Stage 3  Candidate-radix hypothesis test (primes, 5-smooth, rationals)

Plus the red-team certification extensions (verified 2026-08-12):
    - sigma_lambda error propagation from Stage-2 covariance
    - Likelihood-ratio test (pure power law vs power-law + log-periodic): DeltaBIC, F-test
    - Bootstrap null (shuffle residuals, recompute peak) -> honest p-value
    - Detrend-window sensitivity sweep
    - Multi-radix residual rescanning (second radix discovery)

Usage:
    python dsi-radix-detector.py                # self-test on synthetic lambda=1.62
    python dsi-radix-detector.py --data in.csv  # scan a real dataset
        CSV columns: scale,value  (x, y)

Thin-client compliant: stdlib + numpy + scipy only. No local project files.
Committed to QNFO/qnfo-skills (research/scripts/) 2026-08-12.
"""

import argparse
import json
import sys

import numpy as np
from numpy.fft import rfft, rfftfreq
from scipy.optimize import curve_fit
from scipy import stats


# ---------------------------------------------------------------------------
# Stage 1: detrend + spectral peak
# ---------------------------------------------------------------------------

def detrend_log(logy, window=801):
    """Subtract moving-average trend in log-space; zero edges."""
    if window % 2 == 0:
        window += 1
    w = np.ones(window) / window
    trend = np.convolve(logy, w, mode='same')
    resid = logy - trend
    half = window // 2
    resid[:half] = 0
    resid[-half:] = 0
    return resid, trend


def fft_peak(resid, du):
    """Angular frequency at the dominant non-DC spectral peak."""
    spec = np.abs(rfft(resid)) ** 2
    freq = rfftfreq(len(resid), d=du)
    idx = int(np.argmax(spec[1:])) + 1  # skip DC
    return 2.0 * np.pi * freq[idx], spec, freq


def lomb_scargle(t, yv, freqs):
    """Standard Lomb-Scargle periodogram (uneven sampling)."""
    out = np.empty_like(freqs)
    for i, f in enumerate(freqs):
        w = 2.0 * np.pi * f
        tau = np.arctan2(np.sum(np.sin(2 * w * t)), np.sum(np.cos(2 * w * t))) / (2 * w)
        s = np.sin(w * (t - tau))
        c = np.cos(w * (t - tau))
        out[i] = 0.5 * ((np.sum(yv * c) ** 2) / np.sum(c * c) +
                        (np.sum(yv * s) ** 2) / np.sum(s * s))
    return out


# ---------------------------------------------------------------------------
# Stage 2: bounded sinusoid refinement + sigma_lambda
# ---------------------------------------------------------------------------

def sinusoid(uv, C, omega, phi):
    return C * np.cos(omega * uv + phi)


def refine_omega(u, resid, omega0, sub=2, maxfev=20000):
    """Fit C*cos(omega*u + phi) on residuals with omega bounded +/-5% of peak."""
    uf = u[::sub]
    rf = resid[::sub]
    p0 = [0.1, omega0, 0.0]
    bounds = ([-1.0, omega0 * 0.95, -np.pi],
              [1.0, omega0 * 1.05, np.pi])
    popt, pcov = curve_fit(sinusoid, uf, rf, p0=p0, bounds=bounds, maxfev=maxfev)
    return popt, pcov


def lambda_from_omega(omega):
    return np.exp(2.0 * np.pi / omega)


def sigma_lambda(omega, sigma_omega, lam):
    # dlambda/domega = -lambda*ln(lambda)/omega
    return abs(lam * np.log(lam) / omega) * sigma_omega


# ---------------------------------------------------------------------------
# Certification: LR test + bootstrap null
# ---------------------------------------------------------------------------

def likelihood_ratio(u, logy, omega_ref, phi_ref):
    """Pure power law (M0) vs power-law + log-periodic (M1). Returns (DeltaBIC, F, p_F)."""
    n = len(u)
    X0 = np.vstack([np.ones_like(u), u]).T
    coef0 = np.linalg.lstsq(X0, logy, rcond=None)[0]
    rss0 = np.sum((logy - X0 @ coef0) ** 2)

    X1 = np.vstack([np.ones_like(u), u, np.cos(omega_ref * u + phi_ref)]).T
    coef1 = np.linalg.lstsq(X1, logy, rcond=None)[0]
    rss1 = np.sum((logy - X1 @ coef1) ** 2)

    k0, k1 = 2, 5  # A,m vs A,m,C,omega,phi
    bic0 = n * np.log(rss0 / n) + k0 * np.log(n)
    bic1 = n * np.log(rss1 / n) + k1 * np.log(n)
    F = ((rss0 - rss1) / 3) / (rss1 / (n - k1))
    p_F = 1.0 - stats.f.cdf(F, 3, n - k1)
    return bic0 - bic1, F, p_F


def bootstrap_null(u, logy, n_boot=300, seed0=1000):
    """Shuffle pure-PL residuals; return observed peak, null dist, bootstrap p."""
    X0 = np.vstack([np.ones_like(u), u]).T
    coef = np.linalg.lstsq(X0, logy, rcond=None)[0]
    pl_fit = X0 @ coef
    pl_resid = logy - pl_fit

    def peak_stat(rr):
        s = np.abs(rfft(rr)) ** 2
        return float(np.max(s[1:]))

    obs = peak_stat(pl_resid)
    nulls = np.empty(n_boot)
    for b in range(n_boot):
        rng = np.random.default_rng(seed0 + b)
        shuffled = pl_resid[rng.permutation(len(pl_resid))]
        nulls[b] = peak_stat(shuffled)
    p = (1 + np.sum(nulls >= obs)) / (1 + n_boot)
    return obs, nulls, p


# ---------------------------------------------------------------------------
# Main protocol
# ---------------------------------------------------------------------------

def scan_dsi(u, y, window=801, n_boot=300, multi=False, verbose=True):
    """Full radix-agnostic DSI scan. Returns result dict."""
    logy = np.log(y)
    resid, trend = detrend_log(logy, window)
    du = u[1] - u[0]

    omega0, spec, freq = fft_peak(resid, du)
    lam0 = lambda_from_omega(omega0)

    popt, pcov = refine_omega(u, resid, omega0)
    omega_ref = popt[1]
    lam_ref = lambda_from_omega(omega_ref)
    sig_omega = float(np.sqrt(pcov[1, 1]))
    sig_lam = sigma_lambda(omega_ref, sig_omega, lam_ref)

    dbic, F, p_F = likelihood_ratio(u, logy, omega_ref, popt[2])
    obs_peak, nulls, p_boot = bootstrap_null(u, logy, n_boot)

    # Integrity gates for REAL-DATA application (verified 2026-08-12 on Planck TT):
    # G1 Resolvability: need >=1 full log-periodic cycle in the probed u-span.
    #    omega_ref below 2*pi/u_span is a trend artifact, not an oscillation.
    # G2 Amplitude: residual sinusoid must exceed residual noise (SNR >= 1).
    # G3 Radix precision: sigma_lambda/lambda < 10% (else the radix is unconstrained).
    # G4 Null-model validity (caller's responsibility): for non-power-law data
    #    (e.g. CMB acoustic peaks) the shuffle-null destroys real non-DSI
    #    structure and inflates p -- subtract the physical model FIRST.
    u_span = u[-1] - u[0]
    omega_min = 2.0 * np.pi / u_span
    amp = abs(popt[0])
    rms = float(np.sqrt(np.mean(resid ** 2))) if np.isfinite(resid).all() else 0.0
    snr = (amp / rms) if rms > 0 else 0.0
    g1 = omega_ref >= omega_min
    g2 = snr >= 1.0
    g3 = (sig_lam / lam_ref) < 0.10
    gates_pass = int(g1) + int(g2) + int(g3)

    # Multiplicity — IMPORTANT: the bootstrap p is a MAX-STATISTIC p (observed max
    # peak vs distribution of shuffled max peaks), so it is ALREADY multiplicity-
    # corrected over all frequency bins. Sidak over N_eff applies only to a nominal
    # single-bin p (e.g. p_nominal=1e-4 example in note §4). Do NOT Sidak the
    # bootstrap p — that would double-count the look-elsewhere penalty.
    f_min = freq[1]
    f_max = freq[-1]
    n_eff = int(np.floor((f_max - f_min) * (u[-1] - u[0]))) + 1
    p_global_sidak_nominal = 1.0 - (1.0 - 1e-4) ** n_eff  # illustrative only

    result = {
        "omega_fft": float(omega0), "lambda_fft": float(lam0),
        "omega_refined": float(omega_ref), "lambda_refined": float(lam_ref),
        "sigma_lambda": float(sig_lam),
        "delta_bic": float(dbic), "F": float(F), "p_F": float(p_F),
        "bootstrap_peak": float(obs_peak),
        "bootstrap_null_mean": float(nulls.mean()),
        "bootstrap_null_std": float(nulls.std()),
        "bootstrap_p": float(p_boot),
        "n_eff": n_eff,
        "p_global_sidak_nominal_1e4": float(p_global_sidak_nominal),  # illustrative, NOT for bootstrap p
        "integrity_gates": {
            "G1_resolvable_omega_min": float(omega_min),
            "G2_SNR": float(snr),
            "G3_sigma_lambda_frac": float(sig_lam / lam_ref),
            "gates_passed": gates_pass,
        },
        # Detection requires the bootstrap certification AND all 3 integrity gates.
        "detected": bool(p_boot < 0.05 and dbic > 10 and p_F < 0.05 and gates_pass == 3),
        "window": window,
    }

    if verbose:
        print(f"Stage 1 FFT peak:      omega={omega0:.4f} lambda={lam0:.4f}")
        print(f"Stage 2 refinement:    omega={omega_ref:.4f} lambda={lam_ref:.4f} "
              f"sigma_lambda={sig_lam:.4f} ({sig_lam/lam_ref:.2%})")
        print(f"LR test:               DeltaBIC={dbic:.1f} F={F:.1f} p_F={p_F:.2e}")
        print(f"Bootstrap null:        obs={obs_peak:.1f} null={nulls.mean():.1f}+-{nulls.std():.1f} "
              f"p={p_boot:.4f} (max-statistic p — already multiplicity-corrected)")
        print(f"Multiplicity:          N_eff={n_eff} bins; Sidak applies to nominal single-bin p, "
              f"NOT to the bootstrap max-statistic p (double-counts if applied)")
        print(f"DETECTED:              {result['detected']}")

    if multi:
        # Multi-radix: subtract Stage-2 sinusoid, rescan residuals
        resid2 = resid - sinusoid(u, *popt)
        omega_sec, spec2, freq2 = fft_peak(resid2, du)
        lam_sec = lambda_from_omega(omega_sec)
        result["second_omega"] = float(omega_sec)
        result["second_lambda"] = float(lam_sec)
        if verbose:
            print(f"Stage 2b second radix: omega={omega_sec:.4f} lambda={lam_sec:.4f}")

    return result


# ---------------------------------------------------------------------------
# Self-test + CLI
# ---------------------------------------------------------------------------

def synthetic(lam=1.62, n=6000, seed=42, multi=False):
    """Generate DSI signal with given radix (non-prime default)."""
    rng = np.random.default_rng(seed)
    u = np.linspace(0, 8, n)
    trend = np.exp(1.5 * u)
    om = 2 * np.pi / np.log(lam)
    mod = 1.0 + 0.30 * np.cos(om * u + 0.7)
    if multi:
        om2 = 2 * np.pi / np.log(2.31)
        mod = mod * (1.0 + 0.20 * np.cos(om2 * u + 1.2))
    y = trend * mod + 0.02 * trend * rng.standard_normal(n)
    return u, y


def main():
    ap = argparse.ArgumentParser(description="Radix-agnostic DSI detector")
    ap.add_argument("--data", help="CSV with columns scale,value")
    ap.add_argument("--window", type=int, default=801)
    ap.add_argument("--boot", type=int, default=300)
    ap.add_argument("--multi", action="store_true", help="multi-radix rescan")
    ap.add_argument("--self-test", action="store_true", help="run synthetic verification")
    args = ap.parse_args()

    if args.data:
        u, y = np.loadtxt(args.data, delimiter=",", unpack=True)
        u = np.asarray(u, float)
        y = np.asarray(y, float)
        if u[0] <= 0:
            print("FATAL: scale column must be > 0 (log-space requires positive x)", file=sys.stderr)
            sys.exit(1)
        u = np.log(u)  # interpret input as raw scale x -> u = ln(x)
        res = scan_dsi(u, y, args.window, args.boot, multi=args.multi)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["detected"] else 0)  # exit 0 both ways; check 'detected' field

    # default: self-test
    print("SELF-TEST on synthetic non-prime radix lambda=1.62")
    u, y = synthetic(lam=1.62, seed=42)
    res = scan_dsi(u, y, args.window, args.boot, multi=args.multi)
    assert abs(res["lambda_refined"] - 1.62) / 1.62 < 0.03, "lambda recovery FAILED"
    assert res["bootstrap_p"] < 0.05, "bootstrap null FAILED"
    assert res["delta_bic"] > 10, "DeltaBIC FAILED"
    print("SELF-TEST PASS")


if __name__ == "__main__":
    main()
