#!/usr/bin/env python3
"""
Relativistic and timing corrections for LUFT analyses.

Functions:
- doppler_shift(freq, v_r): first-order kinematic Doppler
- grav_redshift(freq, phi): first-order gravitational redshift
- apply_barycentric_times(t_utc, dt_bary): add precomputed barycentric correction
- shapiro_delay(M, r_e, r_s, R): optional Shapiro delay (seconds)

Notes:
- For SDR/astro, get dt_bary from an ephemeris tool (e.g., barycorrpy).
- For lab/collider, use measured v_r and local geopotential phi as needed.
"""

import numpy as np
c = 299_792_458.0  # m/s
G = 6.67430e-11    # SI

def doppler_shift(freq_hz: np.ndarray, v_r: float) -> np.ndarray:
    """Shift frequencies for small radial velocity v_r (m/s): f_obs ≈ f_src (1 - v_r/c)."""
    beta = v_r / c
    return freq_hz * (1.0 - beta)

def grav_redshift(freq_hz: np.ndarray, phi: float) -> np.ndarray:
    """Apply gravitational redshift for potential phi (J/kg): f_obs ≈ f_emit (1 + phi/c^2)."""
    return freq_hz * (1.0 + phi / c**2)

def apply_barycentric_times(t_utc: np.ndarray, dt_bary: np.ndarray) -> np.ndarray:
    """Return barycentric-corrected time stamps t_bary = t_utc + dt_bary (seconds)."""
    return t_utc + dt_bary

def shapiro_delay(M: float, r_e: float, r_s: float, R: float) -> float:
    """Shapiro delay near mass M (kg), distances r_e, r_s, separation R (m). Returns seconds."""
    return (2.0 * G * M / c**3) * np.log((r_e + r_s + R) / (r_e + r_s - R + 1e-30))
