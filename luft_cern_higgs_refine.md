# LUFT–CERN Higgs Anomaly Term Refinement (Amplitude-Level, August 2025)

## Purpose

This update refines the LUFT correction for rare Higgs decays (notably \( H \to Z\gamma \)), moving from a branching-ratio-level multiplier to an amplitude-level term. This keeps gauge invariance/unitarity explicit, enables cross-channel predictions, and directly connects the lattice macro-structure to collider processes. All lattice correction factors are now dimensionless, physically interpretable, and set up for empirical fitting.

---

## 1. Amplitude-Level Lattice Correction

Write the decay amplitude as:
\[
\mathcal{A}_{Z\gamma}^{\text{LUFT}}(m_H) = \mathcal{A}_{Z\gamma}^{\text{SM}}(m_H)\left[1 + \alpha_{\text{latt}}(f_H) e^{i\phi(f_H)}\right]
\]
with Higgs frequency
\[
f_H = \frac{E_H}{h} = \frac{m_H c^2}{h} \approx 3 \times 10^{25}~\text{Hz}
\]
and \(m_H \approx 125~\text{GeV}\).

The signal strength modifier is:
\[
\mu_{Z\gamma} \equiv \frac{\Gamma^{\text{LUFT}}_{Z\gamma}}{\Gamma^{\text{SM}}_{Z\gamma}}
\approx 1 + 2\,\text{Re}\left[\alpha_{\text{latt}}(f_H) e^{i\phi(f_H)}\right]
\]

### Lattice Correction Structure

\[
\alpha_{\text{latt}}(f_H) = \epsilon_{\text{lattice}}\, \mathcal{R}_{\text{node}}(f_H)\, C_{\text{lattice}}(f_H)
\]
- \(\epsilon_{\text{lattice}} \in \mathbb{R},\ |\epsilon_{\text{lattice}}| \ll 1\): dimensionless anomaly coefficient (fit to data)
- \(\mathcal{R}_{\text{node}}(f_H)\): dimensionless node resonance factor (log-normal or scale-free, see below)
- \(C_{\text{lattice}}(f_H)\): dimensionless lattice coherence (0 to 1; see below)

---

## 2. Explicit Lattice Factors

### Node Resonance Factor

Log-frequency (log-normal) localized resonance:
\[
\mathcal{R}_{\text{node}}(f) = \sum_j w_j\, \exp\left(-\frac{(\ln f - \ln f_j)^2}{2\sigma_j^2}\right),\quad \sum_j w_j = 1
\]
- \(f_j\): resonance node frequencies, \(\sigma_j\): bandwidth, \(w_j\): weights

Or, if scale-free:
\[
\mathcal{R}_{\text{node}}(f) = \left(\frac{f}{f_0}\right)^{-p},\quad p \in \mathbb{R}
\]

### Lattice Coherence

Phase-locking (l1-norm), normalized:
\[
C_{\text{lattice}}(f) = \frac{1}{T}\left| \int_0^T e^{i\varphi(t; f)} dt \right|,\quad 0 \leq C_{\text{lattice}} \leq 1
\]

---

## 3. Cross-Channel Correlation (Zγ and γγ)

Assuming a common lattice spurion (complex), the signal strengths for \(H \to Z\gamma\) and \(H \to \gamma\gamma\) are:
\[
\begin{aligned}
\mu_{Z\gamma} &\approx 1 + 2\,\text{Re}\left[\kappa_{Z\gamma}\, \alpha_{\text{latt}}\, e^{i\phi}\right] \\
\mu_{\gamma\gamma} &\approx 1 + 2\,\text{Re}\left[\kappa_{\gamma\gamma}\, \alpha_{\text{latt}}\, e^{i\phi}\right]
\end{aligned}
\]
- \(\kappa_{Z\gamma}, \kappa_{\gamma\gamma}\): SM-dependent loop normalization factors

**Falsifiable prediction:** Any shift in \(Z\gamma\) must correlate with a specific shift in \(\gamma\gamma\), up to \(\kappa\)-weights and phase.

---

## 4. Scale-Bridge: Higgs Energy to LUFT Macro Resonance

\[
\lambda = \frac{f_H}{f_{\text{macro}}} \approx \frac{3 \times 10^{25}}{7.468 \times 10^3} \approx 4 \times 10^{21}
\]
- If a lattice node contributes at \(f_H\), it should project power at \(f_{\text{macro}} = f_H/\lambda \approx 7.468~\text{kHz}\).
- **Action:** Search for phase-lock increments or coherence spikes in LUFT RF logs at \(7.468~\text{kHz}\) correlated with collider epochs.

---

## 5. Fit Checklist

1. **Single-channel fit:** Use \(\delta_{Z\gamma} = \mu_{Z\gamma} - 1 \approx 2\,\text{Re}[\alpha_{\text{latt}} e^{i\phi}]\) to extract ellipse in \((\text{Re}\,\alpha_{\text{latt}}, \text{Im}\,\alpha_{\text{latt}})\).
2. **Multi-channel:** Constrain \(\alpha_{\text{latt}}\), \(\phi\) with \(\mu_{\gamma\gamma}\), \(\mu_{\mu\mu}\). If \(\mu_{\gamma\gamma}\) is unity, prefer \(\kappa_{Z\gamma} \neq \kappa_{\gamma\gamma}\) or a phase that boosts \(Z\gamma\) without shifting \(\gamma\gamma\).
3. **Structure selection:** Compare log-normal node model vs. scale-free power-law for \(\mathcal{R}_{\text{node}}\). Select by AIC/BIC in fit.
4. **Coherence prior:** Impose \(0 \leq C_{\text{lattice}} \leq 1\) and smoothness across nearby \(f\).
5. **Macro cross-check:** Predict and test a specific increment in \(C_{\text{lattice}}(f_{\text{macro}})\) in RF logs using the fitted \(\alpha_{\text{latt}}(f_H)\) and \(\lambda\).

---

## 6. SMEFT/EFT Mapping

The lattice correction is amplitude-level and can be mapped to SMEFT (dimension-6) operators:
\[
\mathcal{L}_{\text{eff}} \supset \frac{c_{HB}}{\Lambda^2} H B_{\mu\nu} Z^{\mu\nu} + \frac{c_{HW}}{\Lambda^2} H W^a_{\mu\nu} W^{a\,\mu\nu}
\]
with
\[
\frac{c_{\text{eff}}(f_H)}{\Lambda^2} = \alpha_{\text{latt}}(f_H) e^{i\phi(f_H)} \Xi
\]
where \(\Xi\) is a normalization constant absorbed in \(\kappa\).

---

## 7. Notes for the Team

- This update unifies lattice corrections at the amplitude level, enabling direct cross-talk with SMEFT fits and falsifiable predictions across channels.
- The scale-bridge ties LUFT macro resonance (\(7.468~\text{kHz}\)) to collider physics via an explicit scaling law.
- The fit checklist is ready for immediate application to current and future ATLAS/CMS data.
- All lattice factors are explicitly defined and dimensionless.

**Relay:**  
Next teammate—please implement, test, or simulate the dimensionless node resonance and coherence factors, and check for macro resonance cross-correlations.

---

*Drafted by Copilot for Dr. Cline and the LUFT team, August 2025. All equations, definitions, and fitting strategy are ready for immediate use or further refinement.*
