# Dimuon/Quarkonia “Coherence Meter” — Post-YETS Study Plan

Purpose
- Measure whether heavy-ion dimuon/quarkonia observables show signatures consistent with enhanced “coherence” after YETS muon upgrades (better timing/chambers/trigger).
- Keep it falsifiable: either we see consistent, controlled trends (academic), or we learn and refine LUFT math.

Key idea (operational)
- Define a dimensionless Coherence Index S_coh built from robust, detector-corrected quantities that are sensitive to collective/ordered behavior but resilient to resolution changes.

Targets and observables
- States: J/ψ (≈3.1 GeV), ψ(2S), Υ(1S,2S,3S).
- Channels: μ+μ− (dimuon), central/forward rapidity as available.
- Observables (binned in centrality, multiplicity, pT, rapidity, run era):
  - Peak width/shape: Voigt fit Γeff vs. control (resolution-unfolded).
  - v2{EP} of quarkonia: event-plane anisotropy (coherence with medium flow).
  - Polarization alignment: λθ from decay angular distribution (Collins–Soper or helicity frame).
  - Long-range correlation proxy: two-particle cumulants c2{2} using muons vs ref flow.
  - Yield ratios: ψ(2S)/J/ψ, Υ(2S)/Υ(1S) vs centrality (suppression/regeneration patterns).

Coherence Index (first pass)
- Define S_coh in each bin (centrality × pT × era):
  S_coh = z(Γref − Γeff) + z(v2_sig) + z(λθ_consistency) + z(c2{2}_sig)
  where:
  - Γeff: fitted width; Γref: resolution-corrected expectation from pp/pPb or MC.
  - v2_sig: v2/σ_v2 (significance).
  - λθ_consistency: |λθ| within physically consistent range across frames (penalize instability).
  - c2{2}_sig: cumulant significance.
  - z() rescales to zero-mean, unit-variance across bins to avoid unit bias.
- Expectation: Post-YETS “coherent ordering” would manifest as higher S_coh at fixed experimental resolution after control corrections.

Data and controls
- Datasets: Public heavy-ion dimuon/quarkonia data (HEPData/JHEP papers) for pre-YETS vs post-YETS eras; pp and pPb as baselines.
- Controls:
  - Resolution control using narrow resonances (Z→μ+μ−) and detector MC; unfold or apply mass-resolution smearing to equalize eras.
  - Background control via like-sign and sidebands; mixed events for shape checks.
  - Trigger/acceptance maps per era; apply per-event weights.
- Sanity: If post-YETS Γeff narrows in data and also in Z→μμ by same fraction → likely detector effect; must be removed before calling “coherence.”

Statistical tests
- Model comparison (AIC/BIC) for peak shapes: single Voigt vs Voigt+coherent-shoulder.
- KS/AD tests for shape residuals after resolution equalization.
- Bootstrap CIs on S_coh; multiple-testing adjustment across bins (Benjamini–Hochberg).
- Null: S_coh distributions identical pre vs post after controls. Alternative: post > pre in targeted bins (centrality 20–60%, moderate pT).

Pipeline (minimal)
1) Ingest per-event or binned spectra (CSV/Parquet) with columns:
   era, system, centrality, multiplicity, m, pT, y, phi, psi2, w, is_like_sign, …
2) Select windows: J/ψ (2.95–3.25 GeV), Υ(9–10.5 GeV).
3) Fit line shapes with Voigt; extract Γeff with uncertainties; resolution-correct using Z-control or MC.
4) Compute v2{EP} for quarkonia candidates (decay-muon angles vs event plane).
5) Build S_coh; produce pre vs post comparisons with identical selection and resolution.
6) Report: tables + plots + a short note.

Deliverables
- Plots: Γeff vs centrality (pre/post, corrected), v2 vs centrality, S_coh heatmaps.
- Tables: S_coh per bin with uncertainties and p-values.
- Note: 2–3 pages summarizing method, controls, results, and decision (Go/Refine/Stop).

Go/No-Go criteria
- Go: At least one quarkonium state shows post>pre S_coh with p<0.01 after controls, replicated in independent binning.
- Refine: Mixed results; revise S_coh weights or controls.
- Stop: Effects vanish after resolution equalization; conclude no coherence beyond detector changes.

Way not to go (pitfalls)
- Do not compare raw widths across eras without resolution equalization.
- Do not tune S_coh weights to maximize significance post-hoc (pre-register weights).
- Do not use only one state or one centrality bin; require pattern across bins/states.
- Avoid over-claiming “new physics”; frame as coherence metric exploration.

Timeline (lightweight)
- Day 1–2: Set schema, ingest one public dataset, get J/ψ width control with Z.
- Day 3–4: Add v2 and S_coh; first pre/post comparison.
- Day 5: Document, decide Go/Refine/Stop.

Appendix: Minimal column schema
- event_id, era, system(pp/pPb/PbPb), centrality, multiplicity, m (GeV), pT (GeV), y, phi, psi2, w (weight), like_sign (0/1), run_number
