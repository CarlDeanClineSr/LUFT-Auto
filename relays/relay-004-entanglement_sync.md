# Relay 004: Entanglement Sync and Measurement Audit

## R0: Imperial Claim
entangled_pair = (A, B) prepared as opposite_spins along axis n
prediction:
- measure A along axis n -> outcome_A
- measure B along axis n -> outcome_B = opposite of outcome_A
[audit: no energy/charge transfer in prediction step; correlations seen only in records over many pairs]

## R1: Grok Alternate
correlation(n_A, n_B) = −cos(theta_between(n_A, n_B))
stats_plan:
- choose two axes for A: a, a′
- choose two axes for B: b, b′
- compute CHSH S = E(a,b) − E(a,b′) + E(a′,b) + E(a′,b′)
[pending audit: if |S| > 2 within uncertainty, keep entanglement model; else revise]

## R2: Carl_AI Audit
Operational lines (paper-fast):
E1: prepare: pair_k = (e_Ak, e_Bk) opposite_spins along axis z
E2: choose axes: for A use {a, a′}, for B use {b, b′}
E3: measure A along chosen axis -> record outcome_Ak ∈ {+1, −1}
E4: measure B along chosen axis -> record outcome_Bk ∈ {+1, −1}
E5: compute E(a,b) = average(outcome_Ak × outcome_Bk) over matching axis choices
E6: compute S = E(a,b) − E(a,b′) + E(a′,b) + E(a′,b′) [audit: statistics OK]

Notes:
- One idea per line; audits at the end when matter/energy/probability are involved.
- No "collapse symbols"—only "measure -> record" and audits on tallies.
- Prediction vs. record kept separate to avoid confusion.

## R3: Decision
Stage entanglement_sync_v1
- No heavy simulation or fitting in this capsule
- Next: optional logbook template (axes, tallies, S with uncertainty)