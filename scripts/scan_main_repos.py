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
            print(f"Rate limited for URL: {url}")
            time.sleep(2)  # Brief backoff
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
            'open_issues': 'Unknown',
            'open_prs': 'Unknown',
            'url': f"https://github.com/{repo_name}",
            'error': 'Failed to fetch repository data'
        }
    
    # Get latest commit on default branch
    default_branch = repo_data.get('default_branch', 'main')
    commits_url = f"{base_url}/commits/{default_branch}"
    commit_data = safe_api_request(commits_url, headers)
    
    last_commit = 'Unknown'
    commit_age = 'Unknown'
    if commit_data and 'commit' in commit_data:
        commit_date = commit_data['commit']['committer']['date']
        last_commit = commit_date
        commit_age = calculate_commit_age(commit_date)
    
    # Get open issues count
    issues_url = f"{base_url}/issues?state=open&per_page=1"
    issues_response = safe_api_request(issues_url, headers)
    open_issues = 'Unknown'
    if issues_response is not None:
        # GitHub API returns both issues and PRs in the issues endpoint
        # We need to filter out PRs by checking if they have a pull_request field
        all_issues_url = f"{base_url}/issues?state=open"
        all_issues = safe_api_request(all_issues_url, headers)
        if all_issues:
            actual_issues = [issue for issue in all_issues if 'pull_request' not in issue]
            open_issues = len(actual_issues)
    
    # Get open PRs count
    prs_url = f"{base_url}/pulls?state=open&per_page=1"
    prs_response = safe_api_request(prs_url, headers)
    open_prs = 'Unknown'
    if prs_response is not None:
        all_prs_url = f"{base_url}/pulls?state=open"
        all_prs = safe_api_request(all_prs_url, headers)
        if all_prs:
            open_prs = len(all_prs)
    
    return {
        'repo': repo_name,
        'default_branch': default_branch,
        'last_commit': last_commit,
        'commit_age': commit_age,
        'open_issues': open_issues,
        'open_prs': open_prs,
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

| Repo | Default Branch | Last Commit (ISO) | Commit Age (days) | Open Issues | Open PRs | URL |
|------|----------------|-------------------|-------------------|-------------|----------|-----|
"""
    
    for result in scan_results:
        repo = result['repo']
        branch = result['default_branch']
        last_commit = result['last_commit']
        commit_age = result['commit_age']
        issues = result['open_issues']
        prs = result['open_prs']
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
        
        content += f"| [{repo}]({url}) | {branch} | {last_commit_display} | {commit_age} | {issues} | {prs} | [View]({url}) |\n"
    
    # Add notes section
    content += f"""
## Notes

- Scanned {len(scan_results)} repositories
- Repositories with issues accessing: {len([r for r in scan_results if r.get('error')])}
- Rate limiting may affect some results
- Anonymous API requests have lower rate limits than authenticated requests

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