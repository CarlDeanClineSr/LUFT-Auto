"""
DESI χ(t) drift bound estimation via sinusoidal amplitude fitting.

Implements least-squares sinusoidal fit to recover χ amplitude and
compute conservative 95% confidence upper bound on the drift magnitude.
"""
import numpy as np
from scipy import optimize
from typing import Tuple, Optional


def fit_sinusoid(
    times: np.ndarray,
    residuals: np.ndarray,
    omega_hz: float,
    return_covariance: bool = True
) -> dict:
    """
    Fit sinusoidal model to residuals: A*cos(ω*t) + B*sin(ω*t) + C.
    
    Uses least-squares fitting with known frequency ω.
    
    Args:
        times: Time points (seconds)
        residuals: Observed residuals
        omega_hz: Angular frequency (Hz)
        return_covariance: If True, compute parameter covariance
        
    Returns:
        Dictionary with fit results
    """
    n = len(times)
    
    # Build design matrix for linear least squares
    # Model: y = A*cos(ωt) + B*sin(ωt) + C
    cos_term = np.cos(omega_hz * times)
    sin_term = np.sin(omega_hz * times)
    ones = np.ones_like(times)
    
    X = np.column_stack([cos_term, sin_term, ones])
    
    # Solve least squares
    params, residual_sum, rank, s = np.linalg.lstsq(X, residuals, rcond=None)
    A, B, C = params
    
    # Compute amplitude and phase
    chi_hat = np.sqrt(A**2 + B**2)
    phase = np.arctan2(B, A)
    
    # Compute fit residuals and chi-squared
    fit = A * cos_term + B * sin_term + C
    fit_residuals = residuals - fit
    chi2 = np.sum(fit_residuals**2)
    
    # Degrees of freedom: n - 3 parameters
    dof = n - 3
    reduced_chi2 = chi2 / dof if dof > 0 else 0.0
    
    # Estimate noise level from residuals
    sigma_noise = np.sqrt(chi2 / dof) if dof > 0 else np.std(fit_residuals)
    
    results = {
        "chi_hat": float(chi_hat),
        "A": float(A),
        "B": float(B),
        "C": float(C),
        "phase": float(phase),
        "chi2": float(chi2),
        "dof": dof,
        "reduced_chi2": float(reduced_chi2),
        "sigma_noise": float(sigma_noise)
    }
    
    if return_covariance:
        # Compute covariance matrix
        # Cov = σ² (X^T X)^{-1}
        XTX = X.T @ X
        try:
            XTX_inv = np.linalg.inv(XTX)
            cov_matrix = sigma_noise**2 * XTX_inv
            
            # Uncertainty in A and B
            sigma_A = np.sqrt(cov_matrix[0, 0])
            sigma_B = np.sqrt(cov_matrix[1, 1])
            
            # Uncertainty in χ = sqrt(A² + B²)
            # Using error propagation: σ_χ² ≈ (A²σ_A² + B²σ_B²) / χ²
            if chi_hat > 0:
                sigma_chi = np.sqrt((A**2 * sigma_A**2 + B**2 * sigma_B**2)) / chi_hat
            else:
                sigma_chi = np.sqrt(sigma_A**2 + sigma_B**2)
            
            results["sigma_chi"] = float(sigma_chi)
            results["sigma_A"] = float(sigma_A)
            results["sigma_B"] = float(sigma_B)
            
        except np.linalg.LinAlgError:
            results["sigma_chi"] = None
            results["sigma_A"] = None
            results["sigma_B"] = None
    
    return results


def compute_chi_95_bound(chi_hat: float, sigma_chi: float, conservative: bool = True) -> float:
    """
    Compute 95% confidence upper bound on χ.
    
    Args:
        chi_hat: Estimated χ amplitude
        sigma_chi: Uncertainty in χ
        conservative: If True, add extra factor for conservativeness
        
    Returns:
        95% upper bound on χ
    """
    # 95% confidence: ~1.96σ for normal distribution
    # Conservative approach: use 2σ
    factor = 2.0 if conservative else 1.96
    chi_95 = chi_hat + factor * sigma_chi
    return chi_95


def run_desi_chi_analysis(
    times: np.ndarray,
    residuals: np.ndarray,
    omega_hz: float,
    chi_true: Optional[float] = None
) -> dict:
    """
    Run complete DESI χ(t) drift analysis.
    
    Args:
        times: Time points (seconds)
        residuals: Observed residuals
        omega_hz: Angular frequency (Hz)
        chi_true: True χ value (if known, for validation)
        
    Returns:
        Dictionary with analysis results
    """
    # Fit sinusoid
    fit_results = fit_sinusoid(times, residuals, omega_hz, return_covariance=True)
    
    # Compute 95% bound
    chi_hat = fit_results["chi_hat"]
    sigma_chi = fit_results.get("sigma_chi", 0.0)
    chi_95 = compute_chi_95_bound(chi_hat, sigma_chi, conservative=True)
    
    results = {
        "chi_hat": chi_hat,
        "sigma_chi": sigma_chi,
        "chi_95": float(chi_95),
        "omega_hz": omega_hz,
        "n_points": len(times),
        "reduced_chi2": fit_results["reduced_chi2"],
        "fit_offset": fit_results["C"]
    }
    
    if chi_true is not None:
        results["chi_true"] = chi_true
        results["recovery_error"] = float(abs(chi_hat - chi_true))
        results["bias"] = float(chi_hat - chi_true)
        if sigma_chi > 0:
            results["pull"] = float((chi_hat - chi_true) / sigma_chi)
        else:
            results["pull"] = 0.0
        results["chi_95_covers_true"] = chi_95 > chi_true
    
    # Acceptance criterion: χ_95 < 0.01 with χ_true ≈ 0.008
    results["passes_acceptance"] = chi_95 < 0.01
    
    return results


def format_desi_results(results: dict) -> str:
    """
    Format DESI analysis results for display.
    
    Args:
        results: Results dictionary from run_desi_chi_analysis
        
    Returns:
        Formatted string
    """
    lines = [
        "=== DESI Λ(t) Drift Bound ===",
        f"χ estimate: χ̂ = {results['chi_hat']:.6f} ± {results['sigma_chi']:.6f}",
        f"95% upper bound: χ_95 = {results['chi_95']:.6f}",
        f"Samples: {results['n_points']}",
        f"Reduced χ²: {results['reduced_chi2']:.3f}",
    ]
    
    if "chi_true" in results:
        lines.extend([
            f"True χ: {results['chi_true']:.6f}",
            f"Recovery error: |χ̂ - χ_true| = {results['recovery_error']:.6f}",
            f"Bias: {results['bias']:.6f}",
            f"Pull: {results['pull']:.2f}",
            f"χ_95 covers true: {results['chi_95_covers_true']}",
        ])
    
    lines.append(f"Acceptance (χ_95 < 0.01): {'PASS' if results['passes_acceptance'] else 'FAIL'}")
    
    return "\n".join(lines)
