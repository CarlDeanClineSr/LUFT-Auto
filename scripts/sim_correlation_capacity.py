"""
Correlation capacity demos.

This script illustrates:
1) Two-qubit entanglement growth under H_int = (ħ g/2) σ_x ⊗ σ_x
2) Variable coupling g(t) and resulting S_max from K(T) = ∫ g(t) dt
3) Rough gravitational K estimate (toy)

Citations:
- Bell (1964); Tsirelson (1980); Horodecki et al. (1995)
- Mandelstam–Tamm (1945); Margolus–Levitin (1998)
- Bose et al. (2017); Marletto & Vedral (2017)
"""

import numpy as np

def concurrence_and_S(t, g):
    """
    For constant g (rad/s) and H_int = (ħ g/2) σx⊗σx starting from |00>:
    C(t) = sin(g t)
    S(t) = 2 * sqrt(1 + C(t)^2)
    """
    C = np.sin(g * t)
    S = 2.0 * np.sqrt(1.0 + C**2)
    return C, S

def K_from_g_of_t(T, g0, tau):
    """
    For g(t) = g0 * exp(-t/tau): K(T) = ∫_0^T g(t) dt = g0 * tau * (1 - exp(-T/tau))
    """
    return g0 * tau * (1.0 - np.exp(-T / tau))

def Smax_from_K(K):
    """
    S_max(K) = 2 * sqrt(1 + sin(K)^2)
    """
    return 2.0 * np.sqrt(1.0 + np.sin(K)**2)

def K_grav_deltaV(deltaV, T, hbar=1.054_571_817e-34):
    """
    Effective gravitational interaction action from a branch-dependent potential difference ΔV (Joules):
    K = (ΔV / ħ) * T
    """
    return (deltaV / hbar) * T

def deltaV_grav_approx(m, r, delta, G=6.674_30e-11):
    """
    ΔV ≈ 2 G m^2 δ / r^2  (valid for δ << r)
    m: mass (kg), r: separation (m), delta: branch offset (m)
    Returns Joules.
    """
    return 2.0 * G * m**2 * delta / (r**2)

if __name__ == "__main__":
    # Example 1: constant g
    g = 2.0 * np.pi * 1e6  # 1 MHz (rad/s)
    t_star = np.pi / (2.0 * g)  # time to reach near-max entanglement
    C_star, S_star = concurrence_and_S(t_star, g)
    print("Constant g example:")
    print(f" g = {g:.3e} rad/s, t* = {t_star:.6e} s")
    print(f" C(t*) = {C_star:.6f}, S(t*) = {S_star:.6f} (Tsirelson ~ 2.828)")

    # Example 2: decaying g(t)
    g0 = 2.0 * np.pi * 1e6
    tau = 5e-6
    T = 10e-6
    K_T = K_from_g_of_t(T, g0, tau)
    Smax = Smax_from_K(K_T)
    print("\nDecaying g(t) example:")
    print(f" g0 = {g0:.3e} rad/s, tau = {tau:.3e} s, T = {T:.3e} s")
    print(f" K(T) = {K_T:.6f} rad, S_max(T) = {Smax:.6f}")

    # Example 3: gravitational toy scaling
    m = 1e-14     # kg (10 picograms)
    r = 1e-4      # 100 microns
    delta = 1e-7  # 100 nm branch offset
    dV = deltaV_grav_approx(m, r, delta)
    T_target = 1.0  # 1 second coherence (just for scale)
    K_g = K_grav_deltaV(dV, T_target)
    Sg = Smax_from_K(K_g)
    print("\nGravitational toy example:")
    print(f" m = {m:.3e} kg, r = {r:.3e} m, delta = {delta:.3e} m")
    print(f" ΔV ≈ {dV:.6e} J, K_grav(T=1s) = {K_g:.6e} rad, S_max ≈ {Sg:.6f}")
