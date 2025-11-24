"""
Synthetic DESI-like residual generator with controllable drift.

Generates time-series data mimicking DESI cosmological observations with
injected sinusoidal modulation representing Λ(t) drift at specific frequency.
"""
import numpy as np
from typing import Tuple, Optional


def generate_desi_residuals(
    n_points: int = 500,
    time_span_years: float = 5.0,
    chi_true: float = 0.008,
    omega_hz: float = 2e-4 * 2 * np.pi,  # 2π * 10^-4 Hz
    noise_level: float = 0.01,
    seed: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray, dict]:
    """
    Generate synthetic DESI-like residual time series.
    
    Models redshift residuals with sinusoidal time-dependent Λ(t) signal:
        residual(t) = χ_true * cos(Ω * t) + noise
    
    Args:
        n_points: Number of time points
        time_span_years: Total observation time in years
        chi_true: True amplitude of χ modulation (dimensionless)
        omega_hz: Angular frequency Ω in Hz
        noise_level: Gaussian noise standard deviation
        seed: Random seed for reproducibility
        
    Returns:
        Tuple of (times array, residuals array, metadata dict)
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate time points (convert years to seconds)
    seconds_per_year = 365.25 * 24 * 3600
    t_seconds = np.linspace(0, time_span_years * seconds_per_year, n_points)
    
    # Generate signal: χ * cos(Ω * t)
    signal = chi_true * np.cos(omega_hz * t_seconds)
    
    # Add Gaussian noise
    noise = np.random.normal(0, noise_level, size=n_points)
    
    residuals = signal + noise
    
    metadata = {
        "n_points": n_points,
        "time_span_years": time_span_years,
        "chi_true": chi_true,
        "omega_hz": omega_hz,
        "omega_per_2pi_hz": omega_hz / (2 * np.pi),
        "noise_level": noise_level,
        "seed": seed,
        "signal_to_noise": chi_true / noise_level if noise_level > 0 else np.inf
    }
    
    return t_seconds, residuals, metadata


def generate_baseline_desi_dataset(seed: int = 42) -> Tuple[np.ndarray, np.ndarray, dict]:
    """
    Generate baseline DESI synthetic dataset for validation.
    
    Uses standard parameters with χ_true = 0.008 at Ω ≈ 2π·10^-4 Hz.
    
    Args:
        seed: Random seed
        
    Returns:
        Tuple of (times, residuals, metadata)
    """
    return generate_desi_residuals(
        n_points=500,
        time_span_years=5.0,
        chi_true=0.008,
        omega_hz=2 * np.pi * 1e-4,  # 2π * 10^-4 Hz
        noise_level=0.01,
        seed=seed
    )
