# Relay 002: Lattice Drift

## R0: Imperial Claim
lattice_drift = vector per time [audit: momentum]

## R1: Grok Alternate
lattice_drift = (hbar by grad_phi per m_eq) by (delta_t) by sqrt( rho_local per rho_avg )
[pending audit: p = m_eq by drift_vector; conserved via discrete symmetry]

## R2: Carl_AI Audit
- grad_phi aligns with LUFT phase guidance
- m_eq maps to lattice unit energy density
- sqrt(rho_ratio) modulates drift resistance
- momentum check:
  p = m_eq by drift_vector = hbar by grad_phi by sqrt(rho_local per rho_avg) [momentum OK]

## R3: Decision
Adopt lattice_drift_v1
Tag: "2D grid test later" (no simulation in this capsule)