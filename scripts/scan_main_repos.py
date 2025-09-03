#!/usr/bin/env python3
"""
LUFT-Auto SCAN MAIN repository health checker.

Reads repos.txt and generates a markdown summary of repository health
including commit status, PR count, and issue count.
"""

import os
import sys
import time
import requests
from datetime import datetime, timezone
from pathlib import Path


def load_repos(repos_file="repos.txt"):
    """Load repository list from repos.txt, skipping comments and empty lines."""
    repos = []
    repo_path = Path(repos_file)
    
    if not repo_path.exists():
        print(f"Warning: {repos_file} not found")
        return repos
    
    with open(repo_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                repos.append(line)
    
    return repos


def get_github_headers():
    """Get GitHub API headers with token if available."""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'LUFT-Auto-Scanner/1.0'
    }
    
    # Check for GitHub token
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'token {token}'
        print("Using GitHub token for API requests")
    else:
        print("No GitHub token found, using anonymous requests")
    
    return headers


def safe_api_request(url, headers, timeout=10):
    """Make a safe API request with error handling and backoff."""
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        
        if response.status_code == 403:
            # Check if it's rate limiting or forbidden access
            if 'X-RateLimit-Remaining' in response.headers:
                remaining = response.headers.get('X-RateLimit-Remaining', '0')
                reset_time = response.headers.get('X-RateLimit-Reset', '0')
                print(f"Rate limited for URL: {url} (remaining: {remaining}, reset: {reset_time})")
                time.sleep(5)  # Longer backoff for rate limiting
            else:
                print(f"Access forbidden for URL: {url}")
            return None
        elif response.status_code == 404:
            print(f"Repository not found: {url}")
            return None
        elif response.status_code != 200:
            print(f"API error {response.status_code} for {url}")
            return None
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None


def calculate_commit_age(commit_date_str):
    """Calculate age of commit in days."""
    try:
        commit_date = datetime.fromisoformat(commit_date_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        age_days = (now - commit_date).days
        return age_days
    except Exception as e:
        print(f"Error calculating commit age: {e}")
        return "Unknown"


def get_stale_badge(commit_age):
    """Generate stale badge based on commit age."""
    if commit_age == "Unknown" or not isinstance(commit_age, int):
        return "❓ Unknown"
    
    if commit_age <= 30:
        return "🟢 Fresh"  # Green - Recent activity
    elif commit_age <= 60:
        return "🟡 Aging"  # Yellow - Getting old
    elif commit_age <= 90:
        return "🟠 Stale"  # Orange - Quite old
    else:
        return "🔴 Very Stale"  # Red - Very old


def get_ci_status(repo_name, default_branch, headers):
    """Get CI status and last successful run for a repository."""
    base_url = f"https://api.github.com/repos/{repo_name}"
    
    # Get latest workflow runs for the default branch
    runs_url = f"{base_url}/actions/runs?branch={default_branch}&per_page=1"
    runs_data = safe_api_request(runs_url, headers)
    
    ci_status = "No runs"
    last_successful_run = "Never"
    
    if runs_data and 'workflow_runs' in runs_data:
        workflow_runs = runs_data['workflow_runs']
        
        if workflow_runs:
            # Get latest run status
            latest_run = workflow_runs[0]
            status = latest_run.get('status', 'unknown')
            conclusion = latest_run.get('conclusion', 'unknown')
            
            # Format CI status
            if status == 'completed':
                if conclusion == 'success':
                    ci_status = "✅ Success"
                elif conclusion == 'failure':
                    ci_status = "❌ Failed"
                elif conclusion == 'cancelled':
                    ci_status = "🚫 Cancelled"
                else:
                    ci_status = f"⚠️ {conclusion.title()}"
            elif status == 'in_progress':
                ci_status = "🔄 Running"
            elif status == 'queued':
                ci_status = "⏳ Queued"
            else:
                ci_status = f"❓ {status.title()}"
            
            # Find last successful run
            successful_runs_url = f"{base_url}/actions/runs?branch={default_branch}&status=completed&conclusion=success&per_page=1"
            successful_data = safe_api_request(successful_runs_url, headers)
            
            if successful_data and 'workflow_runs' in successful_data and successful_data['workflow_runs']:
                last_successful = successful_data['workflow_runs'][0]
                success_timestamp = last_successful.get('updated_at') or last_successful.get('run_started_at')
                if success_timestamp:
                    try:
                        dt = datetime.fromisoformat(success_timestamp.replace('Z', '+00:00'))
                        last_successful_run = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        last_successful_run = success_timestamp
    
    return ci_status, last_successful_run


def scan_repository(repo_name, headers):
    """Scan a single repository and return health information."""
    print(f"Scanning {repo_name}...")
    
    base_url = f"https://api.github.com/repos/{repo_name}"
    
    # Get repository info
    repo_data = safe_api_request(base_url, headers)
    if not repo_data:
        return {
            'repo': repo_name,
            'default_branch': 'Unknown',
            'last_commit': 'Unknown',
            'commit_age': 'Unknown',
            'stale_badge': '❓ Unknown',
            'open_issues': 'Unknown',
            'open_prs': 'Unknown',
            'ci_status': 'Unknown',
            'last_successful_run': 'Unknown',
            'url': f"https://github.com/{repo_name}",
            'error': 'Failed to fetch repository data'
        }
    
    # Get latest commit on default branch
    default_branch = repo_data.get('default_branch', 'main')
    commits_url = f"{base_url}/commits/{default_branch}"
    commit_data = safe_api_request(commits_url, headers)
    
    last_commit = 'Unknown'
    commit_age = 'Unknown'
    stale_badge = '❓ Unknown'
    if commit_data and 'commit' in commit_data:
        commit_date = commit_data['commit']['committer']['date']
        last_commit = commit_date
        commit_age = calculate_commit_age(commit_date)
        stale_badge = get_stale_badge(commit_age)
    
    # Get open issues count (actual issues, not PRs)
    open_issues = 'Unknown'
    all_issues_url = f"{base_url}/issues?state=open"
    all_issues = safe_api_request(all_issues_url, headers)
    if all_issues is not None:
        # Filter out PRs by checking if they have a pull_request field
        actual_issues = [issue for issue in all_issues if 'pull_request' not in issue]
        open_issues = len(actual_issues)
    
    # Get open PRs count
    open_prs = 'Unknown'
    all_prs_url = f"{base_url}/pulls?state=open"
    all_prs = safe_api_request(all_prs_url, headers)
    if all_prs is not None:
        open_prs = len(all_prs)
    
    # Get CI status and last successful run
    ci_status, last_successful_run = get_ci_status(repo_name, default_branch, headers)
    
    return {
        'repo': repo_name,
        'default_branch': default_branch,
        'last_commit': last_commit,
        'commit_age': commit_age,
        'stale_badge': stale_badge,
        'open_issues': open_issues,
        'open_prs': open_prs,
        'ci_status': ci_status,
        'last_successful_run': last_successful_run,
        'url': f"https://github.com/{repo_name}",
        'error': None
    }


def generate_markdown_summary(scan_results, output_file="results/scan_main_STATUS.md"):
    """Generate markdown summary of scan results."""
    
    # Ensure results directory exists
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    content = f"""# LUFT-Auto SCAN MAIN Status Report

**Generated:** {timestamp}

## Repository Health Summary

| Repo | Default Branch | Last Commit (ISO) | Commit Age (days) | Stale Badge | Open Issues | Open PRs | CI Status | Last Successful Run | URL |
|------|----------------|-------------------|-------------------|-------------|-------------|----------|-----------|-------------------|-----|
"""
    
    for result in scan_results:
        repo = result['repo']
        branch = result['default_branch']
        last_commit = result['last_commit']
        commit_age = result['commit_age']
        stale_badge = result['stale_badge']
        issues = result['open_issues']
        prs = result['open_prs']
        ci_status = result['ci_status']
        last_successful_run = result['last_successful_run']
        url = result['url']
        
        # Format commit timestamp for display
        if last_commit != 'Unknown':
            try:
                dt = datetime.fromisoformat(last_commit.replace('Z', '+00:00'))
                last_commit_display = dt.strftime("%Y-%m-%d %H:%M")
            except:
                last_commit_display = last_commit
        else:
            last_commit_display = last_commit
        
        content += f"| [{repo}]({url}) | {branch} | {last_commit_display} | {commit_age} | {stale_badge} | {issues} | {prs} | {ci_status} | {last_successful_run} | [View]({url}) |\n"
    
    # Add notes section
    content += f"""
## Notes

- Scanned {len(scan_results)} repositories
- Repositories with issues accessing: {len([r for r in scan_results if r.get('error')])}
- Authentication: {'✅ Authenticated' if get_github_headers().get('Authorization') else '❌ Anonymous (rate limited)'}
- **Stale Badge Legend**: 🟢 Fresh (≤30 days), 🟡 Aging (31-60 days), 🟠 Stale (61-90 days), 🔴 Very Stale (>90 days)
- **CI Status**: Shows latest workflow run status and last successful run timestamp

## Error Details

"""
    
    # Add error details if any
    errors = [r for r in scan_results if r.get('error')]
    if errors:
        for error_result in errors:
            content += f"- **{error_result['repo']}**: {error_result['error']}\n"
    else:
        content += "No errors encountered during scan.\n"
    
    # Write to file
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Report written to {output_path}")
    return output_path


def main():
    """Main function to run the repository scan."""
    print("Starting LUFT-Auto SCAN MAIN...")
    
    # Load repositories
    repos = load_repos()
    if not repos:
        print("No repositories found to scan")
        sys.exit(1)
    
    print(f"Found {len(repos)} repositories to scan")
    
    # Get GitHub API headers
    headers = get_github_headers()
    
    # Scan each repository
    scan_results = []
    for repo in repos:
        result = scan_repository(repo, headers)
        scan_results.append(result)
        time.sleep(0.5)  # Be nice to the API
    
    # Generate markdown summary
    output_file = generate_markdown_summary(scan_results)
    
    print(f"SCAN MAIN completed successfully. Results in {output_file}")
    sys.exit(0)


if __name__ == "__main__":
    main()