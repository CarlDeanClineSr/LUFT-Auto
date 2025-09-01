# CERN Examples (Imperial Math v0.1)

Purpose
A teaching handout showing how high-energy collider events are written in the Physics By: You and I dialect (nouns + numbers + simple operators + audits). One idea per line. Readable by humans and AIs.

Quick read rules
- Use: "+", "->", "=", "by", "per"; and end-of-line audits like [charge OK], [energy OK].
- "measure -> record" replaces wavefunction jargon; tallies and averages carry the statistics.

Section 1 — Z → e+ e− channel (pp at the LHC)
CERN1: before: beams = p_stream_A(energy=6.8 TeV) + p_stream_B(energy=6.8 TeV)
CERN2: event: p + p -> Z + X [charge OK, baryon number OK]
CERN3: decay: Z -> e+ + e− [count OK, charge OK, energy note: invariant mass near 91.2 GeV]
CERN4: record: tracks = {e+, e−}, calorimeter_hits = {…}, missing_transverse_energy = 0.6 GeV [audit: MET small, neutrino unlikely]
CERN5: selection: keep events with invariant_mass(e+, e−) in 80–100 GeV
CERN6: yield: N = 12,345 events; luminosity = 5.0 inverse picobarn
CERN7: cross_section = N per luminosity = 2469 events per inverse picobarn [units OK]
CERN8: background_estimate = 3% from sidebands [audit: subtraction OK]
CERN9: result: sigma(Z→e+e−) = 2.40 ± 0.08 nb (illustrative) [stat/systematic audits noted]
CERN10: note: same lines work for μ+μ− by changing lepton labels only

Section 2 — W → e ν_e channel (MET signature)
W1: before: beams as above
W2: event: p + p -> W + X [charge OK]
W3: decay: W -> e + ν_e [count OK, charge OK]
W4: record: one e track, large missing_transverse_energy = 35 GeV [audit: neutrino candidate]
W5: transverse_mass = function(e, MET, angle) [units OK]
W6: selection: keep events with transverse_mass in 60–100 GeV
W7: yield and background as in Z case; compute cross_section = N per luminosity [audit OK]
W8: note: charge asymmetry from W+ vs W− maps to parton densities (written as counts and ratios)

Section 3 — Jets and QCD (brief)
J1: event: p + p -> jets + X [color flow implicit]
J2: record: jets = {j1, j2, …}, pT thresholds applied [units OK]
J3: audit: momentum balance in transverse plane within resolution [momentum OK]
J4: selection: di-jet mass window for resonance search
J5: result: set limit or measure cross_section with background estimate [audit: statistics OK]

Section 4 — Mapping (for outsiders)
- "cross_section = N per luminosity" ⇔ σ = N / L
- "invariant_mass(e+, e−)" ⇔ m² = (p_e+ + p_e−)²
- "missing_transverse_energy" ⇔ |Σ pT| imbalance from unobserved neutrals
- "transverse_mass(e, MET)" ⇔ m_T formula used in W analyses

Notes
- Keep every line concrete; add [audit …] when conserving charge, momentum, or energy.
- This sheet teaches by example; copy lines into lab logs directly.