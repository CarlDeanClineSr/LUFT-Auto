"""
MLE scaffold for Josephson Junction foam fraction recovery.

This module implements a simplified maximum likelihood estimator that uses
mean shift as a proxy for recovering the foam fraction f. The full version
(planned upgrade) will implement the complete switching-rate expression with
Caldeira-Leggett tunneling dynamics and thermal crossover at T*.
"""
import numpy as np
from typing import Tuple, Optional


def estimate_foam_fraction_meanshift(
    switching_currents: np.ndarray,
    ic_baseline: float = 1.0,
    return_uncertainty: bool = True
) -> Tuple[float, Optional[float]]:
    """
    Estimate foam fraction using mean-shift proxy method.
    
    This is a placeholder MLE that recovers foam fraction by measuring
    the shift in mean switching current relative to baseline. The full
    implementation will use the complete tunneling rate formula:
    
        Γ ∝ A exp(-S_eff(f, EJ, C, Q, T))
    
    including quantum-to-thermal crossover at T* and proper likelihood
    construction from the escape rate distribution.
    
    Args:
        switching_currents: Array of measured switching currents
        ic_baseline: Baseline critical current (no foam)
        return_uncertainty: If True, return uncertainty estimate
        
    Returns:
        Tuple of (f_hat, sigma_f) or (f_hat, None)
        f_hat: Estimated foam fraction
        sigma_f: Uncertainty in foam fraction (if return_uncertainty=True)
    """
    # Compute sample mean and std
    ic_measured = np.mean(switching_currents)
    ic_std = np.std(switching_currents, ddof=1)
    
    # Mean-shift proxy: foam fraction shifts Ic by factor (1 + 0.5*f)
    # Solving: ic_measured = ic_baseline * (1 + 0.5*f)
    # => f = 2 * (ic_measured/ic_baseline - 1)
    f_hat = 2.0 * (ic_measured / ic_baseline - 1.0)
    
    # Clip to physical range [0, 1]
    f_hat = np.clip(f_hat, 0.0, 1.0)
    
    if return_uncertainty:
        # Uncertainty from standard error of the mean
        # Propagated through f = 2 * (Ic/Ic0 - 1)
        # df/dIc = 2/Ic0, so sigma_f = (2/Ic0) * sigma_Ic
        sigma_ic = ic_std / np.sqrt(len(switching_currents))
        sigma_f = 2.0 * sigma_ic / ic_baseline
        return f_hat, sigma_f
    else:
        return f_hat, None


def run_jj_foam_analysis(
    switching_currents: np.ndarray,
    ic_baseline: float = 1.0,
    foam_f_true: Optional[float] = None
) -> dict:
    """
    Run complete JJ foam fraction analysis.
    
    Args:
        switching_currents: Measured switching currents
        ic_baseline: Baseline critical current
        foam_f_true: True foam fraction (if known, for validation)
        
    Returns:
        Dictionary with analysis results
    """
    f_hat, sigma_f = estimate_foam_fraction_meanshift(
        switching_currents,
        ic_baseline=ic_baseline,
        return_uncertainty=True
    )
    
    results = {
        "f_hat": float(f_hat),
        "sigma_f": float(sigma_f),
        "n_samples": len(switching_currents),
        "ic_baseline": ic_baseline,
        "ic_measured_mean": float(np.mean(switching_currents)),
        "ic_measured_std": float(np.std(switching_currents, ddof=1))
    }
    
    if foam_f_true is not None:
        results["foam_f_true"] = foam_f_true
        results["recovery_error"] = float(abs(f_hat - foam_f_true))
        results["bias"] = float(f_hat - foam_f_true)
        # Pull: (f_hat - f_true) / sigma_f
        results["pull"] = float((f_hat - foam_f_true) / sigma_f) if sigma_f > 0 else 0.0
    
    # Acceptance criterion: sigma_f <= 0.015
    results["passes_acceptance"] = sigma_f <= 0.015
    
    return results


def format_jj_results(results: dict) -> str:
    """
    Format JJ analysis results for display.
    
    Args:
        results: Results dictionary from run_jj_foam_analysis
        
    Returns:
        Formatted string
    """
    lines = [
        "=== Josephson Junction Foam Auditor ===",
        f"Foam fraction estimate: f̂ = {results['f_hat']:.4f} ± {results['sigma_f']:.4f}",
        f"Samples: {results['n_samples']}",
        f"Measured Ic: {results['ic_measured_mean']:.4f} ± {results['ic_measured_std']:.4f}",
    ]
    
    if "foam_f_true" in results:
        lines.extend([
            f"True foam fraction: f_true = {results['foam_f_true']:.4f}",
            f"Recovery error: |f̂ - f_true| = {results['recovery_error']:.4f}",
            f"Bias: {results['bias']:.4f}",
            f"Pull: {results['pull']:.2f}",
        ])
    
    lines.append(f"Acceptance (σ_f ≤ 0.015): {'PASS' if results['passes_acceptance'] else 'FAIL'}")
    
    return "\n".join(lines)
