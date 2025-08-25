# On the Einstein–Podolsky–Rosen Paradox (Bell, 1964) — Team Guide

Citation
- J. S. Bell, “On the Einstein Podolsky Rosen Paradox,” Physics Physique Fizika 1, 195–200 (1964). DOI: 10.1103/PhysicsPhysiqueFizika.1.195
- Open-access PDF: https://journals.aps.org/ppf/pdf/10.1103/PhysicsPhysiqueFizika.1.195
- CERN mirror: https://cds.cern.ch/record/111654/files/vol1p195-200_001.pdf

Why this paper matters
- Shows that any “local hidden variable” (LHV) theory obeys inequalities that quantum mechanics can violate.
- Experimental violations mean locality + classical realism cannot jointly explain entangled correlations.
- Foundation for quantum information science (QKD, teleportation, device-independent security).

Key assumptions and structure
1) Locality: for space-like separated measurements with settings A, B and outcomes a, b,
   P(a,b|A,B,λ) = P(a|A,λ) P(b|B,λ).
2) Hidden variables λ with distribution ρ(λ) reproduce observed stats by averaging over λ.
3) Derives constraints (Bell inequalities). The later CHSH (1969) form is widely tested:
   S = |E(A,B) + E(A,B′) + E(A′,B) − E(A′,B′)| ≤ 2 (LHV bound).
4) Quantum prediction (singlet state) can reach S = 2√2 (Tsirelson bound).

Minimal worked example (CHSH framing)
- For the spin-1/2 singlet, choose analyzer angles (A,A′; B,B′) = (0°, 90°; 45°, −45°) to get S = 2√2 > 2.

Implications and experiments
- Aspect (1982): first strong tests with time-varying analyzers.
- Loophole-free ~2015 (Hensen; Giustina; Shalm): close detection + locality loopholes.
- Consensus: nature violates Bell inequalities, consistent with quantum mechanics and no-signaling.

Related concepts
- Entanglement vs Bell nonlocality vs EPR steering (Schrödinger; Wiseman–Jones–Doherty 2007).
- Steering review (RMP 2020): https://arxiv.org/abs/1903.06663

Suggested reading sequence
1) EPR (1935): https://journals.aps.org/pr/pdf/10.1103/PhysRev.47.777
2) Bell (1964): this paper.
3) CHSH (1969): https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.23.880
4) Aspect (1982): https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.49.1804
5) Loophole-free (2015): https://www.nature.com/articles/nature15759
