# LUFT Codex

The LUFT Codex indexes concepts, math, protocols, datasets, and findings across your recent repositories.

Quick start
1) Install: pip install -r requirements-optional.txt
2) Set GitHub token (optional but recommended to increase rate limits):
   - PowerShell: $env:GITHUB_TOKEN="YOUR_TOKEN"
   - Bash: export GITHUB_TOKEN="YOUR_TOKEN"
3) Run:
   python tools/knowledge_miner.py --owner "CarlDeanClineSr" --since-days 90
4) Outputs:
   - codex/index.json — structured index
   - codex/index.md — human-readable index
   - codex/dashboard.md — overview linking into repos/files

Notes
- Without a token, only public data is scanned and rate limits are low.
- You can filter to specific repos with --repos repo1 repo2.
