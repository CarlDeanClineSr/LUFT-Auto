#!/usr/bin/env python3
"""
CHSH entanglement simulation (singlet state) in the Imperial Math spirit.
- Generates quantum-correlated outcomes with E(θ) = -cos(θ)
- Estimates E(a,b) for four axis pairs and computes S
- Dependency-free: uses only Python stdlib
"""
from __future__ import annotations
import math
import random
import argparse


def simulate_pair(theta: float) -> tuple[int, int]:
    """Return outcomes (A, B) in {+1, -1} with quantum correlation E = -cos(theta).

    Construction: choose AB_product = +1 with P_same = (1 + E)/2, else -1.
    Then draw A uniformly from {+1, -1} and set B = AB_product * A.
    This yields uniform marginals and the desired correlation.
    """
    E = -math.cos(theta)
    p_same = (1.0 + E) / 2.0
    ab = +1 if random.random() < p_same else -1
    A = +1 if random.random() < 0.5 else -1
    B = ab * A
    return A, B


def estimate_E(theta: float, n: int, rng_seed: int | None = None) -> float:
    if rng_seed is not None:
        random.seed(rng_seed)
    s = 0
    for _ in range(n):
        A, B = simulate_pair(theta)
        s += A * B
    return s / float(n)


def main():
    parser = argparse.ArgumentParser(description="Estimate CHSH S for a singlet state.")
    parser.add_argument("--pairs", type=int, default=100000, help="Pairs per axis combination (default: 100000)")
    parser.add_argument("--seed", type=int, default=12345, help="RNG seed (default: 12345)")
    args = parser.parse_args()

    random.seed(args.seed)

    # CHSH-optimal angles (radians)
    a = 0.0
    a_p = math.pi / 2.0
    b = math.pi / 4.0
    b_p = -math.pi / 4.0

    def E(theta):
        return estimate_E(theta, args.pairs)

    E_ab = E(abs(a - b))
    E_abp = E(abs(a - b_p))
    E_apb = E(abs(a_p - b))
    E_apbp = E(abs(a_p - b_p))

    S = E_ab - E_abp + E_apb + E_apbp

    print("CHSH simulation (singlet):")
    print(f"  pairs per combo: {args.pairs}")
    print(f"  E(a,b)    = {E_ab:.6f}")
    print(f"  E(a,b')   = {E_abp:.6f}")
    print(f"  E(a',b)   = {E_apb:.6f}")
    print(f"  E(a',b')  = {E_apbp:.6f}")
    print(f"  S         = {S:.6f}  (quantum target ≈ 2.828; local hidden var bound ≤ 2)")


if __name__ == "__main__":
    main()