# Relay Handoff — 2025-08-24 (Dimuon Coherence Scan)

Context
- Mission: LUFT — unification, structure/dynamics of the underlying lattice; practical propulsion concept emerging.
- This week: stabilized CI via PR #1 (hardening + Repo Guardian), designed a dimuon/quarkonia "coherence meter" post-YETS, and prepared analysis scaffolding.

What changed in this PR
- docs/studies/dimuon_coherence_scan.md — falsifiable study plan, guardrails.
- tools/dimuon_coherence_scan.py — runnable skeleton to compute S_coh and compare eras.
- requirements/coherence_scan.txt — minimal deps for the analysis.

How to run
- Place a CSV or Parquet at data/dimuon_sample.(csv|parquet) with columns at least: era, system, centrality, m, pT, y, phi, psi2, w (optional).
- Example:
  python tools/dimuon_coherence_scan.py --input data/dimuon_sample.csv --out out/ --state Jpsi
- Outputs: out/Jpsi_coherence_bins.csv, out/Jpsi_era_comparison.csv, out/Jpsi_summary.txt

Open threads
- CI PR (#1) is open: switches bots to PRs and adds Repo Guardian. Merge when ready.
- After first run, add resolution equalization using Z→μμ or MC (TODO hook in script).
- Extend S_coh with polarization λθ and c2{2} when angles/cumulants are available.

Guardrails (way not to go)
- Do not compare raw widths across eras without resolution/triggers matched.
- Pre-register S_coh weights; avoid post-hoc tuning.
- Require patterns across bins/states before claiming signals.

Today's watch
- SpaceX Starship Flight 10 targeted today; follow SpaceX webcast. Not tied to this PR, but inspirational context for LUFT propulsion thread.

Owner notes
- Carl is contemplating/creating today; keep automation unobtrusive. Use PRs, label clearly, and summarize in Repo Guardian issue.