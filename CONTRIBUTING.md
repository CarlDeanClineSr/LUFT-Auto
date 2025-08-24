# Contributing to LUFT-Auto

Thanks for helping build LUFT toward unification across energy, matter, space, and time.

How to propose changes
1. Open an issue first (bug or feature) to discuss scope.
2. Create a branch from `main`:
   - Example: `feat/coherence-smoke-test` or `docs/credits-update`.
3. Submit a pull request (PR) referencing the issue.

Coding and docs guidelines
- Keep changes focused and incremental; prefer small PRs.
- Include or update docs where helpful (SMOKE_TEST.md, README, configs).
- Add or adjust sample data only if it helps reproducibility or testing.

Commit messages
- Use clear, imperative style:
  - `feat: add smoke test config and sample data`
  - `fix: handle empty inputs in coherence script`
- Reference issues when applicable: `Fixes #12` or `Refs #34`.

Review process
- PR template checklist must be completed.
- CODEOWNERS will auto-request reviewers (Carl by default).
- Be responsive to feedback; we iterate to get to “mergeable.”

Security
- Never commit secrets or private links.
- Report vulnerabilities via SECURITY.md.
