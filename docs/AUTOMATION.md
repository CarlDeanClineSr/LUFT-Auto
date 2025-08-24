# Automation Overview

This repository uses two GitHub Actions workflows to keep changes safe and visibility high:

## 1) Auto Update via PR (.github/workflows/auto-update.yml)

- **When**: Runs on a schedule (daily at 10:17 UTC) or manually via workflow_dispatch
- **What it does**:
  - Checks out the full history of main branch
  - Optionally runs `scripts/auto_update.sh` if present (hooks into existing LUFT automation)
  - If files changed, commits them with `[skip ci]` tag and opens a PR from `autobot/auto-update` to main
- **Why PRs?**: To avoid non-fast-forward push races and respect branch protection rules

### Project-specific automation hook

The workflow looks for `scripts/auto_update.sh` and runs it if executable. This script currently:
- Generates repo manifest and index files
- Updates multilingual README sections  
- Creates contributor maps and diff logs
- Handles note file organization

You can modify `scripts/auto_update.sh` to add any project-specific automation tasks.

## 2) Repo Guardian (.github/workflows/repo-guardian.yml)

- **When**: Runs daily (11:33 UTC) and whenever the auto-update workflow completes
- **What it does**:
  - Summarizes recent CI failures and auto-update PRs that have been waiting >24 hours
  - Creates or updates a single issue titled "Repo Guardian: CI status and pending bot PRs"
  - Provides at-a-glance visibility into repo health without requiring constant monitoring

### What Repo Guardian monitors

- **CI Health**: Lists any failed, timed-out, or cancelled workflow runs on main in the last 24 hours
- **Stale Bot PRs**: Identifies auto-update PRs older than 24 hours that may need attention
- **Consolidated Reporting**: Maintains a single issue that gets updated rather than creating noise

## Configuration Notes

- **Commit messages**: Auto-commits include `[skip ci]` to avoid recursive action triggers
- **Permissions**: Auto-update needs `contents: write` and `pull-requests: write`; Guardian needs `contents: read` and `issues: write`
- **Concurrency**: Auto-update uses concurrency control to prevent overlapping runs
- **Safety**: PRs allow review before merging, avoiding the collision issues that occurred with direct main pushes

## Customization

- **Scheduling**: Adjust cron schedules in each workflow to your preference
- **Auto-merge**: Can be added later if desired by configuring branch protection rules
- **Notifications**: Repo Guardian issue can be watched/subscribed to for updates
- **Disable**: Comment out or remove workflows if automation is not needed

## Troubleshooting

- If auto-update PRs fail to create, check repository permissions and branch protection settings
- If Guardian reports issues constantly, adjust the 24-hour time window or filtering criteria
- Check workflow logs in the Actions tab for detailed error information
- Bot PRs are safe to ignore until convenient for review and merge