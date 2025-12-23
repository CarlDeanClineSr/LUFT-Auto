# SCAN Dashboard Quickstart (For Grok)

TL;DR
- Run the "SCAN MAIN — nightly dashboard" workflow on branch main.
- Download the artifact → open the Markdown table.
- Fix anything that is red (❌) or stale (60+/90+). Click the links in the table to get to the failing run.
- If a repo is missing a small badge next to its name, add it to that repo's README.

Why this matters for Unification
- We're modeling the structure/dynamics of space-time-energy. Fast, visible CI signals keep theory changes reproducible across repos—your quick checks keep the science loop tight.

What changed
- Repo name now shows a small status badge (links to its workflow page).
- CI Status column is clickable (opens the latest run for main).
- Stale shows how old the repo activity is (Fresh, 30+, 60+, 90+).
- Last Success shows when CI last passed.

Your daily checklist (5–10 minutes)
1) Run the dashboard
   - GitHub → Actions → "SCAN MAIN — nightly dashboard" → Run workflow on main.
2) Review the artifact
   - Download the artifact from the run → open dashboard.md (or similar).
   - Scan rows:
     - ❌ in CI Status → click it → read failing job → file/assign an issue.
     - Stale 60+/90+ → ping owner or file a "refresh" issue.
     - No badge next to repo name → add one (see below).
3) Close the loop
   - If you opened issues, paste links into the notes section at the bottom of the dashboard (if present) or the team log.

How to add a workflow badge to a README
1) Find workflow file path
   - Actions → open the workflow you care about → "View workflow file" → copy path like .github/workflows/WORKFLOW_FILE.yml
2) Insert this under the first # Heading in README.md:
   [![WORKFLOW_NAME](https://github.com/OWNER/REPO/actions/workflows/WORKFLOW_FILE.yml/badge.svg?branch=main)](https://github.com/OWNER/REPO/actions/workflows/WORKFLOW_FILE.yml?query=branch%3Amain)
3) Commit with message:
   chore: add WORKFLOW_NAME badge to README
4) Re-run the dashboard to confirm the badge appears.

What the links do
- Badge next to repo name → workflow page filtered to main.
- CI Status → specific latest run page for main (if none, Actions filtered to main).

Glossary
- Workflow: the CI pipeline (YAML in .github/workflows).
- Badge: small SVG showing pass/fail for a workflow on a branch.
- Default branch: usually main; that's what the dashboard tracks.

If something looks off
- Badge says "no status" → trigger a run on main for that workflow.
- CI Status says "Unknown" → no runs on main yet; run it or adjust workflow triggers.
- Badge broken after rename → update badge URL to the new workflow file path.

End state to aim for daily
- All repos have a badge.
- No ❌ for main. Stale ideally Fresh or 30+.
- Issues filed for any failures or long-stale repos.