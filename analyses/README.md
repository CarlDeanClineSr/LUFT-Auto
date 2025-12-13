# LUFT Charter Symbiosis Pipeline

This directory contains the initial Charter Symbiosis Pipeline implementing synthetic + exemplar-ready analysis scaffolds for three LUFT v1 equation validation domains.

## Overview

The pipeline validates LUFT theoretical predictions through synthetic data analysis across three physical systems:

1. **Josephson Junction (JJ) Foam Auditor** - Mean-shift MLE scaffold for recovering foam fraction f
2. **DESI Λ(t) Drift Bound** - Sinusoidal amplitude fit for χ at Ω ≈ 2π·10⁻⁴ Hz
3. **7,468 Hz Resonance Tri-Site Protocol** - Lomb–Scargle peak detection with phase coherence analysis

## Directory Structure

```
analyses/
├── common/
│   ├── __init__.py
│   └── io.py                    # CSV/NPY/JSON helpers, directory utilities
├── jj_switching/
│   ├── __init__.py
│   ├── jj_synth.py              # Synthetic JJ switching-current generator
│   └── jj_mle.py                # MLE scaffold for foam fraction recovery
├── desi_drift/
│   ├── __init__.py
│   ├── desi_synth.py            # Synthetic DESI-like residual generator
│   └── desi_chi_bound.py        # Sinusoid amplitude fit for χ bounds
└── resonance_7468/
    ├── __init__.py
    ├── synth_tri_site.py        # Tri-site synthetic time series generator
    └── pipeline.py              # LS peak detection, phase coherence, RFI handling
```

## Running the Pipeline

Execute the complete validation suite:

```bash
python -m scripts.run_charter_pipeline
```

Or run individual components:

```python
from analyses.jj_switching.jj_synth import generate_baseline_dataset
from analyses.jj_switching.jj_mle import run_jj_foam_analysis

# Generate synthetic JJ data
switching_currents, metadata = generate_baseline_dataset(seed=42)

# Run foam fraction analysis
results = run_jj_foam_analysis(switching_currents, ic_baseline=1.0, 
                                foam_f_true=metadata["foam_f_true"])
```

## Acceptance Criteria (v1 Placeholders)

These are initial validation targets for synthetic data. Real data analysis will require additional calibration and systematic uncertainty assessment.

### 1. JJ Foam Auditor
- **Target**: σ_f ≤ 0.015
- **Metric**: Uncertainty in recovered foam fraction
- **Status**: Placeholder for full Caldeira-Leggett tunneling rate model

The current implementation uses a mean-shift proxy. The upgrade will implement:
- Full switching-rate expression: Γ ∝ A exp(−S_eff(f, EJ, C, Q, T))
- Quantum-to-thermal crossover at T*
- Multi-temperature joint fitting
- Optional microwave spectroscopy cross-check

### 2. DESI Λ(t) Drift Bound
- **Target**: χ_95 < 0.01 with χ_true ≈ 0.008
- **Metric**: 95% confidence upper bound on drift amplitude
- **Parameters**: Ω ≈ 2π·10⁻⁴ Hz, 5-year baseline

Requirements for real DESI data:
- Time-stamped redshift residuals
- Cadence/window null-shuffle test
- Systematic uncertainty budget
- Connection to CAPSULE_LATTICE_LAMBDA phenomenology

### 3. 7,468 Hz Resonance Tri-Site
- **Synthetic Run**: Code path demonstration (this PR)
- **Real Data Criteria** (future):
  - FAP < 0.01 per site
  - Cross-site coherence C > 0.8
  - SNR ≥ 5
  - Bonferroni-corrected p_eff < 5×10⁻⁴

The synthetic validation confirms the analysis pipeline operates correctly. Real data integration requires:
- RFI template ingestion and subtraction
- Multi-bin Bonferroni/FDR corrections
- Phase difference diagnostics
- Site-specific systematics characterization

## Follow-On Tasks

### Capsule 009 – Λ(t) DESI Bridge
Create `capsules/009-lambda_drift_bridge.md` describing:
- Injection of χ·cos(Ω t) into DESI redshift/time domain
- Link to Λ phenomenology (CAPSULE_LATTICE_LAMBDA)
- Loader for public DESI residuals (time-stamped)
- Cadence/window null-shuffle test module

### JJ Likelihood Upgrade
Replace mean-shift proxy with full tunneling dynamics:
- Implement Γ ∝ A exp(−S_eff(f, EJ, C, Q, T))
- Add quantum vs thermal crossover at T*
- Multi-temperature joint fitting
- Microwave spectroscopy cross-check (resolve EJ vs C degeneracy)

### 7,468 Hz Exemplar
Real data integration:
- RFI template ingestion
- Multi-bin Bonferroni/FDR corrections
- Phase difference diagnostics
- Site calibration and systematics

### Metrics / Reports
- Create `results/charter/report.md` with run summaries (R0→R3)
- Document open audits and follow-up actions

### Config Formalization
- Add `configs/charter_symbiosis.yaml` with parameter sets
- Wire orchestration script to parse configuration
- Enable reproducible reruns with version tracking

## Output Structure

Results are saved to `results/charter/`:
- `jj_foam_auditor.json` - JJ analysis results
- `desi_drift_bound.json` - DESI drift analysis results
- `resonance_7468_trisite.json` - Resonance analysis results
- `pipeline_summary.json` - Combined validation summary

## Dependencies

Core dependencies:
- numpy - Numerical computing
- scipy - Signal processing (Lomb-Scargle, optimization)
- Python 3.7+

Optional (for future extensions):
- astropy - Additional periodogram tools
- pandas - Data manipulation
- matplotlib - Visualization

## Physics Background

### LUFT Framework
The Lattice-Universe Field Theory (LUFT) proposes modifications to standard cosmology and quantum dynamics through:
- Pre-matter field lattice structure
- Foam fraction f in junction tunneling
- Time-dependent cosmological constant Λ(t)
- Resonance signatures in gravitational-vacuum coupling

### Validation Strategy
1. **Synthetic validation** (this PR): Establish analysis tools and acceptance criteria
2. **Calibration**: Tune systematics and uncertainty models
3. **Exemplar data**: Apply to real observations
4. **Publication**: Document findings for peer review

## Code Quality

### Testing
- Synthetic data generators include reproducibility seeds
- Analysis functions return structured dictionaries for unit testing
- Pipeline orchestrator provides end-to-end validation

### Documentation
- Inline docstrings follow NumPy style
- Module-level descriptions explain physics context
- README provides user guide and acceptance criteria

### Future Extensions
- Add unit tests for each analysis module
- Implement visualization utilities
- Create Jupyter notebook tutorials
- Add continuous integration for pipeline validation

## Attribution

**Physics By**: You & I Lab  
**LUFT Portal Integration**  
**Maintainer**: Carl Dean Cline Sr.

## License

See repository root LICENSE file.

## References

For LUFT theoretical framework and related work, see:
- Repository root documentation
- `LUFT_README.md`
- Capsule documentation (once created)
