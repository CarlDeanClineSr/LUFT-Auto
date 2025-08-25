# Correlation Capacity from Interaction Action — Working Notes
Dr.Cline..
Purpose
- Capture minimal, testable math that links “movements of energy” to the strength and growth of nonclassical correlations.
- Keep it modular so we can iterate; no interpretation claimed beyond the equations and cited results.

Core definitions

1) Interaction action (dimensionless) Consider two masses in branch-dependent positions (superpositions). 
- K(T) := (1/ħ) ∫_0^T ||H_int(t)|| dt
- Intuition: how much “entangling work” the interaction can do over time T.

2) Correlation capacity
- For clean 2-qubit entanglers, capacity can be modeled as C_cap(T) := sin(K(T)),
  with K(T) = ∫ g(t) dt when H_int = (ħ g(t)/2) σ_x ⊗ σ_x acting on a product state.
- This reproduces exact concurrence for the σ_x ⊗ σ_x model and upper-bounds for more general cases.

3) Bell-CHSH linkage (Horodecki criterion)
- S_max(T) = 2 sqrt(1 + C_cap(T)^2)
- At C_cap = 1 (maximally entangled), S_max = 2√2 (Tsirelson bound).

Two-qubit exemplar (exact for this model)

- Hamiltonian: H_int = (ħ g/2) σ_x ⊗ σ_x
- Initial state: |00⟩
- Evolved state: |ψ(t)⟩ = cos(θ)|00⟩ − i sin(θ)|11⟩, where θ = g t / 2
- Concurrence: C(t) = sin(2θ) = sin(g t)
- Identify K(t) = ∫ g(t) dt → for constant g, K = g t, so C(t) = sin(K)
- CHSH optimum: S_max(t) = 2 √(1 + sin² K)

Variable coupling

- If g(t) = g0 e^(−t/τ): K(T) = g0 τ (1 − e^(−T/τ))
- Then C_cap(T) = sin(K(T)), S_max(T) = 2 √(1 + sin² K(T))

Energy–momentum–inertia connection (speed limits)

- Faster correlation growth requires energy resources in H_int.
- Quantum speed limits (QSLs) bound the minimal time τ to reach a target state:
  - Mandelstam–Tamm: τ ≥ πħ / (2 ΔE)
  - Margolus–Levitin: τ ≥ ħ / (2 Ē_above_ground)
- These imply practical ceilings on dK/dt and thus on how quickly C_cap can increase, given available energy/variance.

Gravity as a phase-imprinting mediator (toy scaling)

- Consider two masses in branch-dependent positions (superpositions). Differential gravitational potential between branches produces relative phase:
  - φ_ij = (1/ħ) ∫ V_ij(t) dt
- An effective interaction action can be estimated:
  - K_grav ≈ (1/ħ) ∫ |ΔV(t)| dt
- Small-separation approximation for equal masses m, base separation r, branch offset δ ≪ r:
  - ΔV ≈ 2 G m² δ / r²
  - Target concurrence C*: minimal time T ≥ ħ arcsin(C*) / |ΔV|
- This is a falsifiable scaling tying mass, distance, and time to achievable correlation.

Macro → micro intuition checks

- Lattice/spin-chain with nearest-neighbor coupling J shows a Lieb–Robinson “light cone” for correlation spread, with velocity v_LR ~ O(J/ħ). This grounds the idea that local energy movement constrains correlation propagation.

Minimal simulations (see scripts/sim_correlation-capacity.py)

- Sim 1: Constant g. Plot C(t) = sin(g t) and S(t) = 2√(1 + sin²(g t)); verify Tsirelson at t = π/(2g).
- Sim 2: Decaying g(t). Compute K(T) and S_max(T); explore how energy decay caps correlation.
- Sim 3 (optional): Entanglement swapping to confirm how local Bell measurements redistribute correlations while respecting no-signaling.

Assumptions and limitations

- C_cap = sin(K) is exact for the σ_x ⊗ σ_x two-qubit model from product states; for other systems, treat it as an upper bound or a design heuristic.
- Noise, local dephasing, and inefficiencies reduce achievable C and S; include channels in future iterations.

References (facts and formulas cited)

- Bell–CHSH and Tsirelson bound:
  - J. S. Bell, “On the Einstein–Podolsky–Rosen paradox,” Physics 1, 195–200 (1964). DOI: 10.1103/PhysicsPhysiqueFizika.1.195
  - B. S. Cirel’son (Tsirelson), “Quantum generalizations of Bell’s inequality,” Lett. Math. Phys. 4, 93–100 (1980).
- Concurrence–CHSH link:
  - R. Horodecki, P. Horodecki, M. Horodecki, “Violating Bell inequality by mixed spin-1/2 states,” Phys. Lett. A 200, 340–344 (1995).
- Entangling power:
  - P. Zanardi, C. Zalka, L. Faoro, “Entangling power of quantum evolutions,” Phys. Rev. A 62, 030301(R) (2000).
- Quantum speed limits:
  - L. Mandelstam, I. Tamm, J. Phys. (USSR) 9, 249 (1945).
  - N. Margolus, L. B. Levitin, “The maximum speed of dynamical evolution,” Physica D 120, 188–195 (1998).
- Lieb–Robinson bounds:
  - E. H. Lieb, D. W. Robinson, Commun. Math. Phys. 28, 251–257 (1972).
  - M. B. Hastings, Phys. Rev. B 69, 104431 (2004).
- Steering (context for future extensions):
  - H. M. Wiseman, S. J. Jones, A. C. Doherty, Phys. Rev. Lett. 98, 140402 (2007).
- Gravitationally mediated entanglement proposals:
  - S. Bose et al., Phys. Rev. Lett. 119, 240401 (2017).
  - C. Marletto, V. Vedral, Phys. Rev. Lett. 119, 240402 (2017).

Notes
- We’ll keep this as a living document and only add claims that we’ve checked numerically or symbolically.
