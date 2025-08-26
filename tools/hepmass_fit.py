#!/usr/bin/env python3
"""
ATLAS-style narrow-peak fitter (self-contained, no secrets)

Purpose
- Generate pseudo invariant-mass data with a narrow Gaussian signal on top of a smooth background.
- Fit a Gaussian(core) + polynomial(background) model to binned data.
- Optionally run toy pseudo-experiments to check pull distributions.
- Optionally save a simple plot (if matplotlib is available) and a markdown summary.

Dependencies
- Python 3.8+
- numpy
- scipy (optimize.curve_fit)
- matplotlib (optional, only if --plot is passed)

Examples
- One fit with defaults (125 GeV peak):
  python tools/hepmass_fit.py

- More background, narrower bins, 100 toys:
  python tools/hepmass_fit.py --n-bkg 30000 --bins 150 --toys 100

- Save plot and summary:
  python tools/hepmass_fit.py --plot --summary

Outputs (created under results/)
- hepmass_fit_<timestamp>.md  (if --summary)
- hepmass_fit_<timestamp>.png (if --plot)
- hepmass_fit_<timestamp>.csv (binned histogram with model, always saved)

Notes
- This is a stats/controls benchmark for LUFT workflows. It does NOT claim any LUFT resonance.
- You can adjust the window, yields, resolution, and background shape via CLI flags.
"""

import argparse
import datetime as dt
import os
import sys
from dataclasses import dataclass
from typing import Tuple, Dict

import numpy as np

try:
    from scipy.optimize import curve_fit
except Exception as e:
    sys.stderr.write(
        "Error: scipy is required (for curve_fit). Install with:\n"
        "  pip install scipy\n"
    )
    raise

# Matplotlib is optional; only used if --plot is passed
_MP_OK = False
try:
    import matplotlib.pyplot as plt  # noqa: F401
    _MP_OK = True
except Exception:
    _MP_OK = False


# -----------------------------
# Models and helpers
# -----------------------------

def gaussian(x, mu, sigma, A):
    """Unit-density Gaussian amplitude A (counts per GeV)."""
    z = (x - mu) / np.maximum(sigma, 1e-9)
    return A * np.exp(-0.5 * z * z)


def poly_bg(x, coeffs):
    """
    Polynomial background: coeffs in ascending order
    y = c0 + c1*x + c2*x^2 + ...
    """
    # np.polyval expects descending order; reverse here
    return np.polyval(list(reversed(coeffs)), x)


def signal_plus_bg_density(x, mu, sigma, A, *bg_coeffs):
    """Total density (counts per GeV): Gaussian + polynomial background."""
    return gaussian(x, mu, sigma, A) + poly_bg(x, list(bg_coeffs))


def hist_model_counts(xcenters, binw, mu, sigma, A, *bg_coeffs):
    """
    Convert continuous density to expected bin counts for a histogram with bin width binw.
    """
    dens = signal_plus_bg_density(xcenters, mu, sigma, A, *bg_coeffs)
    return np.clip(dens, 0.0, np.inf) * binw


@dataclass
class FitResult:
    mu: float
    mu_err: float
    sigma: float
    sigma_err: float
    A: float
    A_err: float
    bg_coeffs: np.ndarray
    bg_errs: np.ndarray
    nsig_hat: float
    nbkg_hat: float
    chi2: float
    ndof: int
    cov: np.ndarray


# -----------------------------
# Pseudo-data generation
# -----------------------------

def sample_exp_background(n: int, mmin: float, mmax: float, k: float, rng: np.random.Generator) -> np.ndarray:
    """
    Sample from a truncated exponential on [mmin, mmax] with pdf ∝ exp(-k(x - mmin)).
    Inverse-CDF sampling.
    """
    if k <= 0:
        # k=0 means flat; just uniform
        return rng.uniform(mmin, mmax, size=n)
    L = mmax - mmin
    u = rng.uniform(0.0, 1.0, size=n)
    # Inverse CDF for truncated exp
    # F(x) = (1 - exp(-k(x - mmin))) / (1 - exp(-k L))
    # => x = mmin - (1/k) * ln(1 - u*(1 - exp(-k L)))
    denom = (1.0 - np.exp(-k * L))
    x = mmin - (1.0 / k) * np.log(1.0 - u * denom)
    return x


def generate_data(n_sig: int, n_bkg: int, mu: float, sigma: float,
                  mmin: float, mmax: float, bkg_k: float,
                  rng: np.random.Generator) -> np.ndarray:
    sig = rng.normal(loc=mu, scale=sigma, size=n_sig)
    # Keep only within window
    sig = sig[(sig >= mmin) & (sig <= mmax)]
    # Background
    bkg = sample_exp_background(n_bkg, mmin, mmax, bkg_k, rng)
    x = np.concatenate([sig, bkg])
    rng.shuffle(x)
    return x


# -----------------------------
# Fitting
# -----------------------------

def initial_guesses(y, x, binw, mu0, sigma0, poly_order, n_sig_guess=None, n_bkg_guess=None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create initial parameter guesses and bounds.
    params = [mu, sigma, A, c0, c1, ..., c_poly_order]
    A relates to signal yield by Nsig ~ A * sqrt(2π)*sigma
    """
    if n_sig_guess is None:
        n_sig_guess = max(int(np.max(y)), 100)
    if n_bkg_guess is None:
        n_bkg_guess = int(np.sum(y)) - n_sig_guess
        n_bkg_guess = max(n_bkg_guess, 0)

    # Estimate A from n_sig_guess and sigma0
    A0 = n_sig_guess / (np.sqrt(2.0 * np.pi) * max(sigma0, 1e-3))

    # Estimate background density roughly flat:
    L = x[-1] - x[0] + binw
    c0 = (n_bkg_guess / max(L, 1e-6))  # counts per GeV
    coeffs0 = [c0] + [0.0] * poly_order

    p0 = np.array([mu0, sigma0, A0] + coeffs0, dtype=float)

    # Bounds: keep sigma positive, moderate ranges; bg coeffs wide
    mu_bounds = (x[0], x[-1])
    sigma_bounds = (1e-3, (x[-1] - x[0]))
    A_bounds = (0.0, np.inf)
    coeff_bounds = [(-np.inf, np.inf)] * (poly_order + 1)

    lb = [mu_bounds[0], sigma_bounds[0], A_bounds[0]] + [b[0] for b in coeff_bounds]
    ub = [mu_bounds[1], sigma_bounds[1], A_bounds[1]] + [b[1] for b in coeff_bounds]

    return p0, (np.array(lb, float), np.array(ub, float))


def fit_histogram(x, bins, poly_order, mu0, sigma0, verbose=False) -> FitResult:
    counts, edges = np.histogram(x, bins=bins, range=(x.min(), x.max()))
    binw = edges[1] - edges[0]
    centers = 0.5 * (edges[:-1] + edges[1:])

    # Weights: Poisson sqrt(N), avoid zero by floor at 1
    sigma_y = np.sqrt(np.maximum(counts, 1.0))

    # Initial guesses and bounds
    p0, bounds = initial_guesses(
        y=counts, x=centers, binw=binw, mu0=mu0, sigma0=sigma0, poly_order=poly_order
    )

    # Wrapper for curve_fit expects f(x, *params) -> y_model
    def model_for_fit(xx, *params):
        mu, sig, A, *bg = params
        return hist_model_counts(xx, binw, mu, sig, A, *bg)

    # curve_fit with weights
    popt, pcov = curve_fit(
        model_for_fit,
        centers,
        counts,
        p0=p0,
        sigma=sigma_y,
        absolute_sigma=True,
        bounds=bounds,
        maxfev=20000
    )

    # Unpack parameters
    mu, sig, A = popt[:3]
    bg = np.array(popt[3:], dtype=float)

    # Errors (sqrt of diagonal)
    perr = np.sqrt(np.clip(np.diag(pcov), 0.0, np.inf))
    mu_err, sig_err, A_err = perr[:3]
    bg_errs = perr[3:]

    # Derived yields
    nsig_hat = float(A * np.sqrt(2.0 * np.pi) * sig)
    # Background yield by summing model background over bins
    y_bg = poly_bg(centers, bg) * binw
    nbkg_hat = float(np.sum(np.clip(y_bg, 0.0, np.inf)))

    # Chi2 / ndof
    y_fit = model_for_fit(centers, *popt)
    chi2 = float(np.sum(((counts - y_fit) / sigma_y) ** 2))
    nparams = len(popt)
    ndof = max(len(counts) - nparams, 1)

    if verbose:
        print(f"Fit: mu={mu:.3f}±{mu_err:.3f}, sigma={sig:.3f}±{sig_err:.3f}, "
              f"A={A:.3f}±{A_err:.3f}, nsig≈{nsig_hat:.1f}, nbkg≈{nbkg_hat:.1f}, "
              f"chi2/ndof={chi2:.1f}/{ndof}")

    return FitResult(
        mu=mu, mu_err=mu_err,
        sigma=sig, sigma_err=sig_err,
        A=A, A_err=A_err,
        bg_coeffs=bg, bg_errs=bg_errs,
        nsig_hat=nsig_hat, nbkg_hat=nbkg_hat,
        chi2=chi2, ndof=ndof,
        cov=pcov
    ), (centers, counts, binw, y_fit, y_bg)


def run_toys(n_toys: int, true_mu: float, true_sigma: float, n_sig: int, n_bkg: int,
             mmin: float, mmax: float, bkg_k: float, bins: int, poly_order: int,
             rng: np.random.Generator) -> Dict[str, float]:
    pulls_mu = []
    pulls_sigma = []
    for _ in range(n_toys):
        x = generate_data(n_sig, n_bkg, true_mu, true_sigma, mmin, mmax, bkg_k, rng)
        (fit, _) = fit_histogram(x, bins=bins, poly_order=poly_order, mu0=true_mu, sigma0=true_sigma, verbose=False)
        if fit.mu_err > 0:
            pulls_mu.append((fit.mu - true_mu) / fit.mu_err)
        if fit.sigma_err > 0:
            pulls_sigma.append((fit.sigma - true_sigma) / fit.sigma_err)
    pulls_mu = np.array(pulls_mu) if pulls_mu else np.array([np.nan])
    pulls_sigma = np.array(pulls_sigma) if pulls_sigma else np.array([np.nan])
    return {
        "pull_mu_mean": float(np.nanmean(pulls_mu)),
        "pull_mu_std": float(np.nanstd(pulls_mu)),
        "pull_sigma_mean": float(np.nanmean(pulls_sigma)),
        "pull_sigma_std": float(np.nanstd(pulls_sigma)),
        "n_toys": int(n_toys)
    }


def save_csv(path: str, centers, counts, model, bg, binw):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("bin_center_gev,bin_width_gev,count,model_count,model_bg_count\n")
        for xc, c, ym, yb in zip(centers, counts, model, bg):
            f.write(f"{xc:.6f},{binw:.6f},{int(c)},{ym:.6f},{yb:.6f}\n")


def save_summary_md(path: str, cfg: argparse.Namespace, fit: FitResult, toy_stats: Dict[str, float] | None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    now = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# ATLAS-style mass peak fit — {now}\n\n")
        f.write("Config\n")
        f.write(f"- Window: [{cfg.mmin}, {cfg.mmax}] GeV; bins={cfg.bins}; binw≈{(cfg.mmax-cfg.mmin)/cfg.bins:.3f} GeV\n")
        f.write(f"- Truth: mu={cfg.mu_true} GeV, sigma={cfg.sigma_true} GeV, Nsig={cfg.n_sig}, Nbkg={cfg.n_bkg}, bkg_k={cfg.bkg_k}\n")
        f.write(f"- Poly order: {cfg.poly_order}\n\n")

        f.write("Fit (Gaussian + polynomial background)\n")
        f.write(f"- mu = {fit.mu:.4f} ± {fit.mu_err:.4f} GeV\n")
        f.write(f"- sigma = {fit.sigma:.4f} ± {fit.sigma_err:.4f} GeV\n")
        f.write(f"- A (amp) = {fit.A:.4f} ± {fit.A_err:.4f} counts/GeV\n")
        f.write(f"- nsig_hat ≈ {fit.nsig_hat:.1f} counts, nbkg_hat ≈ {fit.nbkg_hat:.1f} counts\n")
        f.write(f"- chi2/ndof = {fit.chi2:.1f} / {fit.ndof}\n\n")

        f.write("Background coefficients (ascending order)\n")
        for i, (c, e) in enumerate(zip(fit.bg_coeffs, fit.bg_errs)):
            f.write(f"- c{i} = {c:.6g} ± {e:.6g}\n")
        f.write("\n")

        if toy_stats:
            f.write("Toy pull summary\n")
            f.write(f"- n_toys = {toy_stats['n_toys']}\n")
            f.write(f"- pull(mu): mean={toy_stats['pull_mu_mean']:.3f}, std={toy_stats['pull_mu_std']:.3f}\n")
            f.write(f"- pull(sigma): mean={toy_stats['pull_sigma_mean']:.3f}, std={toy_stats['pull_sigma_std']:.3f}\n")


def maybe_plot(path_png: str, centers, counts, model, bg, mu, sigma, mmin, mmax):
    if not _MP_OK:
        sys.stderr.write("matplotlib not available; skipping plot (install with `pip install matplotlib`).\n")
        return
    os.makedirs(os.path.dirname(path_png), exist_ok=True)
    import matplotlib.pyplot as plt  # local import for clarity

    plt.figure(figsize=(8, 5))
    plt.step(centers, counts, where="mid", label="Data", color="black")
    plt.plot(centers, model, label="Fit: Gauss + poly", color="#1f77b4", lw=2)
    plt.plot(centers, bg, label="Background", color="#ff7f0e", lw=2, ls="--")
    plt.axvline(mu, color="green", lw=1.5, ls=":")
    plt.title(f"Narrow-peak fit (μ≈{mu:.2f} GeV, σ≈{sigma:.2f} GeV)")
    plt.xlabel("Invariant mass [GeV]")
    plt.ylabel("Counts / bin")
    plt.xlim(mmin, mmax)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path_png, dpi=120)
    plt.close()


def main():
    ap = argparse.ArgumentParser(description="Self-contained ATLAS-style narrow-peak fitter (Gaussian + polynomial background).")
    ap.add_argument("--mmin", type=float, default=110.0, help="Mass window min [GeV]")
    ap.add_argument("--mmax", type=float, default=140.0, help="Mass window max [GeV]")
    ap.add_argument("--bins", type=int, default=120, help="Number of histogram bins")

    ap.add_argument("--mu-true", type=float, default=125.0, dest="mu_true", help="True Gaussian mean [GeV]")
    ap.add_argument("--sigma-true", type=float, default=1.6, dest="sigma_true", help="True Gaussian sigma [GeV]")
    ap.add_argument("--n-sig", type=int, default=1200, dest="n_sig", help="Number of signal events to generate")
    ap.add_argument("--n-bkg", type=int, default=20000, dest="n_bkg", help="Number of background events to generate")
    ap.add_argument("--bkg-k", type=float, default=0.15, dest="bkg_k", help="Exponential background slope k [1/GeV] (0=flat)")

    ap.add_argument("--poly-order", type=int, default=1, choices=[0, 1, 2, 3], help="Polynomial order for background model")

    ap.add_argument("--toys", type=int, default=0, help="Number of toy pseudo-experiments for pull checks")
    ap.add_argument("--seed", type=int, default=42, help="Random seed")
    ap.add_argument("--plot", action="store_true", help="Save a PNG plot of the fit")
    ap.add_argument("--summary", action="store_true", help="Write a markdown summary under results/")
    ap.add_argument("--out-prefix", type=str, default="hepmass_fit", help="Output file prefix in results/")

    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    # Generate one dataset
    x = generate_data(
        n_sig=args.n_sig, n_bkg=args.n_bkg,
        mu=args.mu_true, sigma=args.sigma_true,
        mmin=args.mmin, mmax=args.mmax,
        bkg_k=args.bkg_k, rng=rng
    )

    fit, (centers, counts, binw, y_fit, y_bg) = fit_histogram(
        x, bins=args.bins, poly_order=args.poly_order, mu0=args.mu_true, sigma0=args.sigma_true, verbose=True
    )

    # Toys (optional)
    toy_stats = None
    if args.toys > 0:
        toy_stats = run_toys(
            n_toys=args.toys,
            true_mu=args.mu_true, true_sigma=args.sigma_true,
            n_sig=args.n_sig, n_bkg=args.n_bkg,
            mmin=args.mmin, mmax=args.mmax, bkg_k=args.bkg_k,
            bins=args.bins, poly_order=args.poly_order,
            rng=np.random.default_rng(args.seed + 1)
        )
        print(f"Toys: n={toy_stats['n_toys']}, pull(mu) mean={toy_stats['pull_mu_mean']:.3f} std={toy_stats['pull_mu_std']:.3f}, "
              f"pull(sigma) mean={toy_stats['pull_sigma_mean']:.3f} std={toy_stats['pull_sigma_std']:.3f}")

    # Outputs
    ts = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    outdir = "results"
    base = f"{args.out_prefix}_{ts}"
    csv_path = os.path.join(outdir, f"{base}.csv")
    save_csv(csv_path, centers, counts, y_fit, y_bg, binw)
    print(f"Saved binned CSV: {csv_path}")

    if args.summary:
        md_path = os.path.join(outdir, f"{base}.md")
        save_summary_md(md_path, args, fit, toy_stats)
        print(f"Saved summary: {md_path}")

    if args.plot:
        png_path = os.path.join(outdir, f"{base}.png")
        maybe_plot(png_path, centers, counts, y_fit, y_bg, fit.mu, fit.sigma, args.mmin, args.mmax)
        if os.path.exists(png_path):
            print(f"Saved plot: {png_path}")

    # Final concise print (useful in CI logs if desired)
    print(f"Fit mu={fit.mu:.3f}±{fit.mu_err:.3f} GeV, sigma={fit.sigma:.3f}±{fit.sigma_err:.3f} GeV, "
          f"nsig≈{fit.nsig_hat:.1f}, nbkg≈{fit.nbkg_hat:.1f}, chi2/ndof={fit.chi2:.1f}/{fit.ndof}")


if __name__ == "__main__":
    main()
