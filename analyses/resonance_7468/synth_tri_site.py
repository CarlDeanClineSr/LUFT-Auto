"""
Tri-site synthetic time series generator for 7,468 Hz resonance.

Creates synthetic sensor time series data for three monitoring sites with
controllable resonance signal, phase relationships, and noise characteristics.
"""
import numpy as np
from typing import Tuple, Dict, Optional


def generate_tri_site_timeseries(
    n_samples: int = 10000,
    sample_rate_hz: float = 20000.0,
    resonance_freq_hz: float = 7468.0,
    signal_amplitude: float = 0.1,
    noise_level: float = 0.05,
    phase_offsets: Optional[Tuple[float, float, float]] = None,
    rfi_freq_hz: Optional[float] = None,
    rfi_amplitude: float = 0.02,
    seed: Optional[int] = None
) -> Tuple[np.ndarray, Dict[str, np.ndarray], dict]:
    """
    Generate synthetic tri-site time series data.
    
    Creates data for three monitoring sites with a common resonance signal
    at 7,468 Hz plus independent noise. Optionally includes RFI contamination.
    
    Args:
        n_samples: Number of time samples per site
        sample_rate_hz: Sampling rate in Hz
        resonance_freq_hz: Target resonance frequency (default 7468 Hz)
        signal_amplitude: Amplitude of resonance signal
        noise_level: Standard deviation of Gaussian noise per site
        phase_offsets: Phase offsets (radians) for each site, or None for random
        rfi_freq_hz: RFI contamination frequency, or None for no RFI
        rfi_amplitude: Amplitude of RFI signal
        seed: Random seed for reproducibility
        
    Returns:
        Tuple of (times array, site_data dict, metadata dict)
        site_data keys: 'site_1', 'site_2', 'site_3'
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate time array
    times = np.arange(n_samples) / sample_rate_hz
    
    # Generate or use provided phase offsets
    if phase_offsets is None:
        # Random phases for sites (but correlated signal)
        phase_offsets = (0.0, 
                        np.random.uniform(0, 2*np.pi), 
                        np.random.uniform(0, 2*np.pi))
    
    # Angular frequency of resonance
    omega_res = 2 * np.pi * resonance_freq_hz
    
    # Generate base resonance signal
    base_signal = signal_amplitude * np.sin(omega_res * times)
    
    # Generate data for each site
    site_data = {}
    for i, site_name in enumerate(['site_1', 'site_2', 'site_3']):
        # Resonance with site-specific phase
        site_signal = signal_amplitude * np.sin(omega_res * times + phase_offsets[i])
        
        # Add independent Gaussian noise
        noise = np.random.normal(0, noise_level, size=n_samples)
        
        # Combine signal and noise
        site_timeseries = site_signal + noise
        
        # Add RFI if specified
        if rfi_freq_hz is not None:
            omega_rfi = 2 * np.pi * rfi_freq_hz
            rfi_signal = rfi_amplitude * np.sin(omega_rfi * times)
            site_timeseries += rfi_signal
        
        site_data[site_name] = site_timeseries
    
    metadata = {
        "n_samples": n_samples,
        "sample_rate_hz": sample_rate_hz,
        "resonance_freq_hz": resonance_freq_hz,
        "signal_amplitude": signal_amplitude,
        "noise_level": noise_level,
        "phase_offsets": list(phase_offsets),
        "rfi_freq_hz": rfi_freq_hz,
        "rfi_amplitude": rfi_amplitude if rfi_freq_hz else 0.0,
        "seed": seed,
        "duration_seconds": n_samples / sample_rate_hz,
        "snr": signal_amplitude / noise_level if noise_level > 0 else np.inf
    }
    
    return times, site_data, metadata


def generate_baseline_trisite_dataset(seed: int = 42) -> Tuple[np.ndarray, Dict[str, np.ndarray], dict]:
    """
    Generate baseline tri-site synthetic dataset for validation.
    
    Uses standard parameters for 7,468 Hz resonance with coherent phases.
    
    Args:
        seed: Random seed
        
    Returns:
        Tuple of (times, site_data, metadata)
    """
    # Use small phase offsets for high coherence
    phase_offsets = (0.0, 0.1, -0.15)  # Radians
    
    return generate_tri_site_timeseries(
        n_samples=10000,
        sample_rate_hz=20000.0,
        resonance_freq_hz=7468.0,
        signal_amplitude=0.1,
        noise_level=0.05,
        phase_offsets=phase_offsets,
        rfi_freq_hz=None,  # No RFI in baseline
        rfi_amplitude=0.0,
        seed=seed
    )
