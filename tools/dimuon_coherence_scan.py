"""
Dimuon/Quarkonia Coherence Meter — minimal analysis skeleton.
Inputs: CSV/Parquet with columns: era, system, centrality, m, pT, y, phi, psi2, w, like_sign, run_number, ...
Outputs: tables/plots and an S_coh summary CSV.
"""

import os
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import ks_2samp

# -----------------------
# Utilities
# -----------------------

def voigt(x, amp, mean, sigma, gamma, b0, b1):
    """Voigt + linear background. sigma: Gaussian, gamma: Lorentzian."""
    # Approximate Voigt via scipy if available; otherwise pseudo-Voigt
    # pseudo-Voigt approximation:
    f = sigma**2 + gamma**2
    eta = 1.36603 * (gamma / (gamma + sigma)) - 0.47719 * (gamma / (gamma + sigma))**2 + 0.11116 * (gamma / (gamma + sigma))**3
    gauss = np.exp(-(x - mean)**2 / (2 * sigma**2))
    lorentz = 1.0 / (1.0 + ((x - mean)/gamma)**2)
    pv = eta * lorentz + (1 - eta) * gauss
    return amp * pv + b0 + b1 * x

def fit_peak(mass, counts, init):
    try:
        popt, pcov = curve_fit(voigt, mass, counts, p0=init, maxfev=20000)
        perr = np.sqrt(np.diag(pcov))
        return popt, perr
    except Exception as e:
        return None, None

def bin_by(df, keys):
    return df.groupby(keys, dropna=False)

def zscore(x):
    x = np.asarray(x, float)
    mu, sd = np.nanmean(x), np.nanstd(x) if np.nanstd(x) > 0 else 1.0
    return (x - mu) / sd

# -----------------------
# Core analysis
# -----------------------

def analyze_quarkonium(df, state="Jpsi", mass_window=(2.95, 3.25), mass_init=3.096, era_pairs=("pre", "post")):
    """Return per-bin results including effective width and S_coh components."""
    results = []
    keys = ["era", "system", "centrality"]
    mask = (df["m"] >= mass_window[0]) & (df["m"] <= mass_window[1])
    for (era, system, cent), g in bin_by(df[mask], keys):
        # Histogram
        bins = np.linspace(mass_window[0], mass_window[1], 120)
        w = g["w"].to_numpy() if "w" in g.columns else np.ones(len(g))
        hist, edges = np.histogram(g["m"], bins=bins, weights=w)
        centers = 0.5 * (edges[1:] + edges[:-1])

        # Initial params: amp, mean, sigma, gamma, b0, b1
        init = [max(hist.max(), 1.0), mass_init, 0.02, 0.02, float(np.median(hist[:5]) if len(hist) >= 5 else 0.0), 0.0]
        fit, err = fit_peak(centers, hist, init)
        if fit is None:
            continue
        amp, mean, sigma, gamma, b0, b1 = fit
        # Effective width proxy (pseudo-Voigt): combine sigma & gamma
        gamma_eff = float(np.sqrt(sigma**2 + gamma**2))

        # Simple v2{EP} proxy from muon azimuths relative to psi2
        if "phi" in g.columns and "psi2" in g.columns:
            dphi = (g["phi"] - g["psi2"]).to_numpy()
            v2 = float(np.nanmean(np.cos(2.0 * dphi))) if len(dphi) else np.nan
            denom = np.nanstd(np.cos(2.0 * dphi)) / np.sqrt(max(len(dphi), 1)) if len(dphi) else np.nan
            v2_sig = float(v2 / denom) if denom and denom != 0 else np.nan
        else:
            v2, v2_sig = np.nan, np.nan

        # Placeholders for polarization λθ and cumulant c2{2}
        lam_theta = np.nan
        c2_sig = np.nan

        results.append(dict(
            state=state, era=era, system=system, centrality=cent, mean=float(mean),
            gamma_eff=gamma_eff, v2=v2, v2_sig=v2_sig, lam_theta=lam_theta, c2_sig=c2_sig
        ))
    out = pd.DataFrame(results)
    if out.empty:
        return out

    # Build S_coh z-scored across comparable bins
    for col in ["gamma_eff", "v2_sig", "lam_theta", "c2_sig"]:
        try:
            out[f"z_{col}"] = zscore(out[col])
        except Exception:
            out[f"z_{col}"] = np.nan

    # Smaller gamma_eff suggests narrower peaks; invert sign so higher is more coherent.
    out["z_gamma_inv"] = -out["z_gamma_eff"]

    # First-pass S_coh: equal weights across available components
    components = [c for c in ["z_gamma_inv", "z_v2_sig", "z_lam_theta", "z_c2_sig"] if c in out.columns]
    out["S_coh"] = out[components].mean(axis=1, skipna=True)

    return out

def compare_eras(df_res, era_pairs=("pre", "post")):
    """Statistical comparison of S_coh between eras per centrality/system."""
    comps = []
    if df_res is None or df_res.empty:
        return pd.DataFrame(comps)
    for (system, cent), g in bin_by(df_res, ["system", "centrality"]):
        a = g.loc[g["era"] == era_pairs[0], "S_coh"].dropna()
        b = g.loc[g["era"] == era_pairs[1], "S_coh"].dropna()
        if len(a) >= 3 and len(b) >= 3:
            stat, p = ks_2samp(a, b)
            comps.append(dict(system=system, centrality=cent, ks_stat=float(stat), p_value=float(p), n_pre=int(len(a)), n_post=int(len(b))))
    return pd.DataFrame(comps)

# -----------------------
# Entry point
# -----------------------

def main(input_path: str, output_dir: str, state="Jpsi"):
    os.makedirs(output_dir, exist_ok=True)
    if input_path.endswith(".parquet"):
        df = pd.read_parquet(input_path)
    else:
        df = pd.read_csv(input_path)
    # Basic cleaning
    df = df.dropna(subset=["m", "centrality", "era", "system"])
    # Choose mass window based on state
    if state.lower() == "jpsi":
        mw, m0 = (2.95, 3.25), 3.096
    elif state.lower() in ("upsilon", "y1s", "upsilon1s"):
        mw, m0 = (9.0, 10.5), 9.46
    else:
        mw, m0 = (2.95, 3.25), 3.096

    res = analyze_quarkonium(df, state=state, mass_window=mw, mass_init=m0, era_pairs=("pre", "post"))
    res.to_csv(os.path.join(output_dir, f"{state}_coherence_bins.csv"), index=False)

    era_cmp = compare_eras(res, era_pairs=("pre", "post"))
    era_cmp.to_csv(os.path.join(output_dir, f"{state}_era_comparison.csv"), index=False)

    # Simple text summary
    sig = era_cmp[era_cmp["p_value"] < 0.01] if not era_cmp.empty else pd.DataFrame()
    with open(os.path.join(output_dir, f"{state}_summary.txt"), "w") as f:
        if sig.empty:
            f.write("No significant S_coh differences (p<0.01) found.\n")
        else:
            f.write(f"Significant S_coh differences (p<0.01): {len(sig)} bins\n")
            for _, r in sig.iterrows():
                f.write(f"- {r['system']} centrality {r['centrality']}: KS={r['ks_stat']:.3f}, p={r['p_value']:.2e}\n")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to CSV/Parquet with dimuon/quarkonia candidates")
    ap.add_argument("--out", required=True, help="Output directory")
    ap.add_argument("--state", default="Jpsi", help="Quarkonium state: Jpsi or Upsilon")
    args = ap.parse_args()
    main(args.input, args.out, args.state)
