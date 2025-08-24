# LUFT-Auto Coherence Scan — Smoke Test

Goal: run the coherence scan end-to-end on a tiny CSV to verify the toolchain, not physics.

Steps
1) Ensure the repo has:
   - configs/coherence.yaml
   - data/sample_dimuon.csv

2) Run the analysis (adjust the script path if different in your repo):
   ```bash
   python path/to/your_coherence_script.py \
     --config configs/coherence.yaml \
     --input data/sample_dimuon.csv \
     --out out/quickcheck.json
   ```

3) Expected:
   - Creates the `out/` directory.
   - Writes `quickcheck.json` with summary fields (including a placeholder S_coh).
   - No exceptions.

If the entrypoint script differs, update the command above and submit a quick PR to fix this doc.
