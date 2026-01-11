# LUFT Master Index — Reality-based-Space-and-its-functionality

This Master Index maps the major LUFT repositories, key files, and the role each repo or file plays in the LUFT program. Use this page as the single entry point for navigation, onboarding, and sprint planning.

Last updated: 2025-11-11  
Maintainer: Dr. Carl Dean Cline Sr. (CarlDeanClineSr)

---

## Project Summary
LUFT (Lattice Unified Field Theory) is a multi-repo project containing theory, experiments, simulations, device designs, and data. This index gives a high-level map so contributors (and AIs) can find the important artifacts quickly.

---

## Repositories (collection overview)

- CarlDeanClineSr/Reality-based-Space-and-its-functionality — Role: central coordination, theory, docs, and data index (this repo)
- CarlDeanClineSr/May-2025- — Role: Mathematica notebooks and early derivations (theory & derivations)
- CarlDeanClineSr/LUFT-WinSPC-Data — Role: measurement datasets (WinSPC instrument logs)
- CarlDeanClineSr/Chronological-Craft-Inventions-LUFT — Role: design notebooks & historical device builds (hardware + experiments)
- CarlDeanClineSr/LUFT-Unified-Field-Project — Role: Mathematica-based unified-field derivations (theory)
- CarlDeanClineSr/Lattice-Unified-Field-Theory-L.U.F.T — Role: core Jupyter notebooks describing LUFT concepts (theory + demos)
- CarlDeanClineSr/LUFT_Recordings — Role: SDR/Audio recordings and spectrograms (raw signal data)
- CarlDeanClineSr/Unified-Field-Theory-Solutions-2025 — Role: Python analysis and solution notebooks (simulations and tests)
- CarlDeanClineSr/Unification-Utilization-Physics- — Role: applied physics, instrument scripts, and collapse utilities (code & utilities)
- CarlDeanClineSr/LUFT-Auto — Role: automation, bots, and indexing; code for bots and anomaly relays (automation)
- CarlDeanClineSr/Unification-Utilization-Physics- (duplicate note) — Role: active instrument/code repo used for Notebook 5 and lattice code

---

## Key files in this repo (Reality-based-Space-and-its-functionality)

These are the important items I indexed from your repo content. See the accompanying `metadata_master_list.csv` for machine‑readable entries.

- `LUFT/UFT Project Ideas: Unification, Structure, and Dynamic Substrate`  
  Role: Project roadmap and idea list (project concepts, next steps).

- `graphics/luft_harmonic_scaling_map.png`  
  Role: Frequency hierarchy visualization — the 7,468 Hz core resonance map.

- `Summary Table: LUFT Frequency Hierarchy`  
  Role: Short summary table describing the 7,468 Hz hierarchy and sub-lattice modes.

- `AI_Audit_and_Research_Status_Report.md`  
  Role: Automated AI audit and current project health/status.

- `Auto Multi-Repo LUFT Index` (GitHub Action workflow)  
  Role: Automates weekly aggregated indexing across LUFT repos.

- `Copilot and Cline Creations`  
  Role: Notes, mind-dumps, speculative ideas and emergent thoughts.

- `Core Discoveries LUFT`  
  Role: High-level summary of key claims and experimental results.

- `Dynamic Couplings & Emergent Anomaly Fields — LUFT Unification Tracker`  
  Role: Living model of dynamic coupling constants and anomaly field tracking.

- `Einstein-LUFT 2025`  
  Role: Drafts linking LUFT to Einstein’s field equations and modified EFE forms.

- `LUFT Unification Analysis Results`  
  Role: Folder of auto-generated spectrograms, CSV peak lists, and analysis outputs.

- `Copilot Chat — LUFT Resonance Atlas: Phase 2 Overview`  
  Role: Session transcripts + project planning artifacts.

---

## How to use this master index
1. Clone the repo and open `MASTER_INDEX.md`.  
2. Use `metadata_master_list.csv` to search/filter files by tag or type.  
3. Add a new entry to `metadata_master_list.csv` when you add important files (one line per artifact). Keep the `id` field unique.  
4. For new experiments: create a `/capsules` Markdown file following the capsule template (see `/capsules/TEMPLATE_CAPSULE.md` if present).

---

## Short-term priorities (recommended)
1. Add the metadata CSV (`metadata_master_list.csv`) to the repo root — this file (supplied alongside this index) will be the engine for quick search.  
2. Create `/capsules` and add knowledge capsules for the three highest-impact claims:  
   - Lattice → Λ mapping (vacuum energy)  
   - JJ foam auditor (MQT metrology)  
   - 7,468 Hz frequency hierarchy (resonance atlas)  
3. Enable the `Auto Multi-Repo LUFT Index` workflow to keep indexes fresh weekly.

---

## Contact & contribution
- To propose a change to the index: open an Issue in this repo with label `infra:index`.  
- To add a data or file: add a row to `metadata_master_list.csv` and attach a short `/capsules/<id>.md` summary.

---

Thank you — this index is the start of making LUFT discoverable and durable.  
If you want, I’ll now:
- generate the capsule template and 3 starter capsules,
- or create a GitHub Action to auto-update the metadata CSV weekly.

Say: “Make capsule templates” or “Auto-index action” and I’ll produce them next.
