# ATLAS Rare Higgs Decays — LUFT Stats/Controls Benchmark
Date: 2025‑08‑26

Summary (from ATLAS EPS‑HEP 2025)
- Evidence for H→μμ with observed (expected) ≈ 3.4σ (2.5σ) using Run‑2 + early Run‑3.
- Improved sensitivity for H→Zγ with observed (expected) ≈ 2.5σ (1.9σ).
- Purpose here: validate our line‑shape fits and background modeling discipline, then reuse the same discipline in LUFT resonance hunts.

What we benchmark (self‑contained, no external keys)
- Narrow‑peak fitter sanity: Gaussian(core) + polynomial background on synthetic m_μμ around 125 GeV.
- Toys/pulls: generate pseudo‑experiments; confirm unbiased μ and correct pull widths.
- Controls: use sidebands, FDR for multiple tests, and explicit null/decoy checks.

How this helps LUFT
- Proves our statistical handling and null discipline on a “known truth” peak before applying to f0≈7468.779 Hz lab data (RF/magnonics).
- Avoids over‑claiming: collider peaks are not LUFT standing waves; they are for fitter QA.

Next (optional, when ready)
- Add a tiny script tools/hepmass_fit.py that:
  - Generates pseudo m_μμ data
  - Fits Gaussian+poly
  - Outputs mean, sigma, pulls, and a markdown summary
- Log its result in results/SUMMARY_TABLE.md (Benchmark row).

Notes
- Do not add workflows or secret‑dependent steps until guarded.
- Defer quoting κ_μ or κ_Zγ; cite official numbers when public HEPData/json is available.
