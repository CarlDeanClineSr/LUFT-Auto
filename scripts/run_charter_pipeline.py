"""
Charter Symbiosis Pipeline Orchestrator.

Runs all three LUFT v1 equation validation synthetic analyses end-to-end:
1. Josephson Junction foam auditor
2. DESI Λ(t) drift bound
3. 7,468 Hz resonance tri-site protocol

Prints PASS/FAIL results and persists JSON outputs to results/charter/.
"""
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from analyses.common.io import ensure_directory, save_json
from analyses.jj_switching.jj_synth import generate_baseline_dataset as gen_jj_data
from analyses.jj_switching.jj_mle import run_jj_foam_analysis, format_jj_results
from analyses.desi_drift.desi_synth import generate_baseline_desi_dataset
from analyses.desi_drift.desi_chi_bound import run_desi_chi_analysis, format_desi_results
from analyses.resonance_7468.synth_tri_site import generate_baseline_trisite_dataset
from analyses.resonance_7468.pipeline import run_trisite_resonance_analysis, format_resonance_results


def run_jj_validation(output_dir: Path) -> dict:
    """
    Run Josephson Junction foam auditor validation.
    
    Args:
        output_dir: Directory for output files
        
    Returns:
        Results dictionary
    """
    print("\n" + "="*60)
    print("Running JJ Foam Auditor Validation...")
    print("="*60)
    
    # Generate synthetic data
    switching_currents, metadata = gen_jj_data(seed=42)
    
    # Run analysis
    results = run_jj_foam_analysis(
        switching_currents,
        ic_baseline=1.0,
        foam_f_true=metadata["foam_f_true"]
    )
    
    # Add metadata
    results["metadata"] = metadata
    results["timestamp"] = datetime.now(timezone.utc).isoformat()
    results["analysis_type"] = "jj_foam_auditor"
    
    # Print results
    print("\n" + format_jj_results(results))
    
    # Save to JSON
    output_file = output_dir / "jj_foam_auditor.json"
    save_json(results, output_file)
    print(f"\nResults saved to {output_file}")
    
    return results


def run_desi_validation(output_dir: Path) -> dict:
    """
    Run DESI Λ(t) drift bound validation.
    
    Args:
        output_dir: Directory for output files
        
    Returns:
        Results dictionary
    """
    print("\n" + "="*60)
    print("Running DESI Drift Bound Validation...")
    print("="*60)
    
    # Generate synthetic data
    times, residuals, metadata = generate_baseline_desi_dataset(seed=42)
    
    # Run analysis
    results = run_desi_chi_analysis(
        times,
        residuals,
        omega_hz=metadata["omega_hz"],
        chi_true=metadata["chi_true"]
    )
    
    # Add metadata
    results["metadata"] = metadata
    results["timestamp"] = datetime.now(timezone.utc).isoformat()
    results["analysis_type"] = "desi_drift_bound"
    
    # Print results
    print("\n" + format_desi_results(results))
    
    # Save to JSON
    output_file = output_dir / "desi_drift_bound.json"
    save_json(results, output_file)
    print(f"\nResults saved to {output_file}")
    
    return results


def run_resonance_validation(output_dir: Path) -> dict:
    """
    Run 7,468 Hz resonance tri-site validation.
    
    Args:
        output_dir: Directory for output files
        
    Returns:
        Results dictionary
    """
    print("\n" + "="*60)
    print("Running 7,468 Hz Resonance Tri-Site Validation...")
    print("="*60)
    
    # Generate synthetic data
    times, site_data, metadata = generate_baseline_trisite_dataset(seed=42)
    
    # Run analysis
    results = run_trisite_resonance_analysis(
        times,
        site_data,
        freq_target=metadata["resonance_freq_hz"],
        search_width=50.0
    )
    
    # Add metadata
    results["metadata"] = metadata
    results["timestamp"] = datetime.now(timezone.utc).isoformat()
    results["analysis_type"] = "resonance_7468_trisite"
    
    # Print results
    print("\n" + format_resonance_results(results))
    
    # Save to JSON
    output_file = output_dir / "resonance_7468_trisite.json"
    save_json(results, output_file)
    print(f"\nResults saved to {output_file}")
    
    return results


def print_summary(jj_results: dict, desi_results: dict, resonance_results: dict) -> None:
    """
    Print summary of all validation results.
    
    Args:
        jj_results: JJ analysis results
        desi_results: DESI analysis results
        resonance_results: Resonance analysis results
    """
    print("\n" + "="*60)
    print("CHARTER SYMBIOSIS PIPELINE SUMMARY")
    print("="*60)
    
    # JJ summary
    jj_pass = jj_results.get("passes_acceptance", False)
    print(f"\n1. JJ Foam Auditor: {'PASS ✓' if jj_pass else 'FAIL ✗'}")
    print(f"   σ_f = {jj_results['sigma_f']:.4f} (target: ≤ 0.015)")
    print(f"   f̂ = {jj_results['f_hat']:.4f}, f_true = {jj_results.get('foam_f_true', 'N/A')}")
    
    # DESI summary
    desi_pass = desi_results.get("passes_acceptance", False)
    print(f"\n2. DESI Drift Bound: {'PASS ✓' if desi_pass else 'FAIL ✗'}")
    print(f"   χ_95 = {desi_results['chi_95']:.6f} (target: < 0.01)")
    print(f"   χ̂ = {desi_results['chi_hat']:.6f}, χ_true = {desi_results.get('chi_true', 'N/A')}")
    
    # Resonance summary
    resonance_pass = resonance_results.get("synthetic_run_complete", False)
    print(f"\n3. 7,468 Hz Resonance: {'CODE PATH OK ✓' if resonance_pass else 'FAIL ✗'}")
    print(f"   Coherence = {resonance_results['cross_site']['phase_coherence']:.3f}")
    print(f"   Mean peak = {resonance_results['cross_site']['mean_peak_freq']:.2f} Hz")
    
    # Overall status
    all_pass = jj_pass and desi_pass and resonance_pass
    print("\n" + "="*60)
    if all_pass:
        print("OVERALL STATUS: ALL VALIDATIONS PASSED ✓")
    else:
        print("OVERALL STATUS: SOME VALIDATIONS FAILED")
    print("="*60 + "\n")


def main():
    """Main orchestration function."""
    print("\n" + "="*60)
    print("CHARTER SYMBIOSIS PIPELINE")
    print("LUFT v1 Equation Validation - Synthetic Analysis")
    print("="*60)
    
    # Setup output directory
    repo_root = Path(__file__).parent.parent
    output_dir = repo_root / "results" / "charter"
    ensure_directory(output_dir)
    print(f"\nOutput directory: {output_dir}")
    
    # Run validations
    try:
        jj_results = run_jj_validation(output_dir)
        desi_results = run_desi_validation(output_dir)
        resonance_results = run_resonance_validation(output_dir)
        
        # Print summary
        print_summary(jj_results, desi_results, resonance_results)
        
        # Save combined summary
        summary = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pipeline_version": "v1.0-charter-symbiosis",
            "jj_foam_auditor": {
                "passes": jj_results.get("passes_acceptance", False),
                "sigma_f": jj_results["sigma_f"],
                "f_hat": jj_results["f_hat"]
            },
            "desi_drift_bound": {
                "passes": desi_results.get("passes_acceptance", False),
                "chi_95": desi_results["chi_95"],
                "chi_hat": desi_results["chi_hat"]
            },
            "resonance_7468": {
                "code_path_ok": resonance_results.get("synthetic_run_complete", False),
                "coherence": resonance_results["cross_site"]["phase_coherence"],
                "mean_peak_freq": resonance_results["cross_site"]["mean_peak_freq"]
            }
        }
        
        summary_file = output_dir / "pipeline_summary.json"
        save_json(summary, summary_file)
        print(f"Pipeline summary saved to {summary_file}\n")
        
        return 0
        
    except Exception as e:
        print(f"\n!!! PIPELINE ERROR !!!")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
