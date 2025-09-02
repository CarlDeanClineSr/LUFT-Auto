#!/usr/bin/env python3
import os, requests, datetime as dt
from pathlib import Path

API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN", "")

# Load repositories list from configs/repos.txt
REPOS_FILE = Path("configs/repos.txt")
REPOS = [line.strip() for line in REPOS_FILE.read_text().splitlines() if line.strip() and not line.strip().startswith("#")]


def last_commit(owner_repo, branch="main"):
    url = f"{API}/repos/{owner_repo}/commits"
    params = {"sha": branch, "per_page": 1}
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    r = requests.get(url, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    items = r.json()
    if not items:
        return {"repo": owner_repo, "error": "no commits returned"}
    c = items[0]
    return {
        "repo": owner_repo,
        "sha": c.get("sha", "")[:7],
        "message": c.get("commit", {}).get("message", "").splitlines()[0],
        "date": c.get("commit", {}).get("author", {}).get("date", ""),
        "html_url": c.get("html_url", ""),
    }


def main():
    rows = []
    for rr in REPOS:
        try:
            rows.append(last_commit(rr))
        except Exception as e:
            rows.append({"repo": rr, "error": str(e)})

    out = Path("results")
    out.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [f"# SCAN MAIN — status @ {now}\n"]
    lines.append("| Repository | Last Commit | Date (UTC) |")
    lines.append("|---|---|---|")
    for r in rows:
        if "error" in r:
            lines.append(f"| {r['repo']} | ERROR: {r['error']} | |")
        else:
            lines.append(f"| {r['repo']} | [{r['sha']}]({r['html_url']}) {r['message']} | {r['date']} |")
    (out / "scan_main_STATUS.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()