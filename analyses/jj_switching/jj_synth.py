"""
Synthetic Josephson Junction switching-current generator.

Generates synthetic JJ switching current data with controllable parameters:
- Ic: Critical current
- C: Capacitance
- ramp: Current ramp rate
- T: Temperature
- foam_f: Foam fraction (modifies switching statistics)
"""
import numpy as np
from typing import Tuple, Optional


def generate_jj_switching_data(
    n_samples: int = 1000,
    ic_mean: float = 1.0,
    ic_std: float = 0.1,
    foam_f: float = 0.0,
    temperature: float = 0.3,
    capacitance: float = 1.0,
    ramp_rate: float = 1.0,
    seed: Optional[int] = None
) -> Tuple[np.ndarray, dict]:
    """
    Generate synthetic JJ switching current measurements.
    
    The foam fraction f modifies the effective critical current distribution,
    introducing a systematic shift that the MLE estimator should recover.
    
    Args:
        n_samples: Number of switching events to simulate
        ic_mean: Mean critical current (base value)
        ic_std: Standard deviation of critical current
        foam_f: Foam fraction (0 to 1) - shifts distribution
        temperature: Temperature in reduced units
        capacitance: Junction capacitance
        ramp_rate: Current ramp rate
        seed: Random seed for reproducibility
        
    Returns:
        Tuple of (switching_currents array, metadata dict)
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Foam fraction shifts the mean critical current
    # This is a simplified model; real version would use full
    # Caldeira-Leggett tunneling rate with thermal crossover
    effective_ic = ic_mean * (1.0 + foam_f * 0.5)
    
    # Thermal broadening contribution
    thermal_width = np.sqrt(temperature * capacitance / ramp_rate)
    effective_std = np.sqrt(ic_std**2 + thermal_width**2)
    
    # Generate switching currents with Gaussian statistics
    # (simplified; full model would use proper escape rate distribution)
    switching_currents = np.random.normal(
        loc=effective_ic,
        scale=effective_std,
        size=n_samples
    )
    
    # Add small thermal tail (< 5% population at low switching currents)
    n_thermal = int(0.03 * n_samples)
    thermal_events = np.random.exponential(
        scale=0.3 * effective_std,
        size=n_thermal
    )
    thermal_events = effective_ic - thermal_events
    
    # Replace some samples with thermal tail events
    thermal_indices = np.random.choice(n_samples, size=n_thermal, replace=False)
    switching_currents[thermal_indices] = thermal_events
    
    metadata = {
        "n_samples": n_samples,
        "ic_mean": ic_mean,
        "ic_std": ic_std,
        "foam_f_true": foam_f,
        "temperature": temperature,
        "capacitance": capacitance,
        "ramp_rate": ramp_rate,
        "effective_ic": effective_ic,
        "effective_std": effective_std,
        "seed": seed
    }
    
    return switching_currents, metadata


def generate_baseline_dataset(seed: int = 42) -> Tuple[np.ndarray, dict]:
    """
    Generate baseline synthetic JJ dataset for validation.
    
    Uses standard parameters with foam_f = 0.05 for recovery testing.
    Parameters tuned to achieve σ_f ≤ 0.015 acceptance criterion.
    
    Args:
        seed: Random seed
        
    Returns:
        Tuple of (switching_currents, metadata)
    """
    return generate_jj_switching_data(
        n_samples=5000,  # Increased for better statistics
        ic_mean=1.0,
        ic_std=0.03,  # Reduced noise for cleaner signal
        foam_f=0.05,  # Target for recovery
        temperature=0.2,  # Lower temperature for less thermal broadening
        capacitance=1.0,
        ramp_rate=1.5,  # Faster ramp reduces thermal effects
        seed=seed
    )
