import argparse
import base64
import datetime as dt
import os
import re
import sys
import textwrap
from typing import List, Dict, Any, Optional

import yaml

try:
    from github import Github
except Exception as e:
    print("Please install PyGithub: pip install PyGithub", file=sys.stderr)
    raise

DEFAULT_CONFIG_PATH = "codex/config.yaml"

EXT_OK = {".md", ".txt", ".py"}

def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def within_days(updated_at: dt.datetime, days: int) -> bool:
    now = dt.datetime.now(dt.timezone.utc)
    return (now - updated_at).days <= days

def is_text_file(name: str, include_ext: List[str]) -> bool:
    return any(name.lower().endswith(ext) for ext in include_ext)

def extract_highlights(name: str, content: str, keywords: List[str]) -> Dict[str, Any]:
    lines = content.splitlines()
    heads = [l.strip() for l in lines if l.strip().startswith("#")]
    todos = [l.strip() for l in lines if re.search(r"\\b(TODO|OPEN|QUESTION|NEXT)\\b", l, re.I)]
    mentions = {}
    for kw in keywords:
        cnt = len(re.findall(re.escape(kw), content, flags=re.I))
        if cnt:
            mentions[kw] = cnt
    return {
        "headings": heads[:20],
        "todos": todos[:20],
        "mentions": mentions,
    }

def fetch_content(repo, path: str) -> Optional[str]:
    try:
        f = repo.get_contents(path)
        if isinstance(f, list):
            return None
        if f.encoding == "base64":
            return base64.b64decode(f.content).decode("utf-8", errors="ignore")
        return f.decoded_content.decode("utf-8", errors="ignore")
    except Exception:
        return None

def gather_repo(repo, conf: Dict[str, Any]) -> Dict[str, Any]:
    summary = {
        "name": repo.full_name,
        "url": repo.html_url,
        "updated_at": repo.updated_at.isoformat(),
        "files": [],
        "keyword_totals": {},
    }
    try:
        tree = repo.get_git_tree(repo.default_branch, recursive=True).tree
    except Exception:
        return summary

    include_ext = conf.get("include_extensions", list(EXT_OK))
    exclude_dirs = set(conf.get("exclude_dirs", []))
    keywords = conf.get("keywords", [])

    count = 0
    for blob in tree:
        if blob.type != "blob":
            continue
        p = blob.path
        parts = p.split("/")
        if any(part in exclude_dirs for part in parts):
            continue
        if not is_text_file(p, include_ext):
            continue
        content = fetch_content(repo, p)
        if not content:
            continue
        hi = extract_highlights(p, content, keywords)
        summary["files"].append({
            "path": p,
            "url": f"{repo.html_url}/blob/{repo.default_branch}/{p}",
            "headings": hi["headings"],
            "todos": hi["todos"],
            "mentions": hi["mentions"],
        })
        for k, v in hi["mentions"].items():
            summary["keyword_totals"][k] = summary["keyword_totals"].get(k, 0) + v

        count += 1
        if count >= int(conf.get("max_files_per_repo", 400)):
            break

    return summary

def render_index_md(repos_data: List[Dict[str, Any]]) -> str:
    out = ["# LUFT Codex Index", ""]
    for rd in repos_data:
        out.append(f"## {rd['name']}  ")
        out.append(f"Updated: {rd['updated_at']}  ")
        out.append(f"Repo: {rd['url']}")
        if rd.get("keyword_totals"):
            tags = ", ".join(f"{k}:{v}" for k, v in sorted(rd["keyword_totals"].items()))
            out.append(f"Keywords: {tags}")
        out.append("")
        for f in rd.get("files", [])[:20]:
            out.append(f"- [{f['path']}]({f['url']})")
            if f["headings"]:
                out.append(f"  - Headings: {' | '.join(f['headings'][:3])}")
            if f["todos"]:
                out.append(f"  - TODOs: {' | '.join(f['todos'][:2])}")
        out.append("")
    return "\n".join(out)

def render_dashboard_md(repos_data: List[Dict[str, Any]]) -> str:
    out = ["# LUFT Dashboard", ""]
    out.append("Recent repositories and highlights (last 90 days).")
    out.append("")
    out.append("## Recent Repositories")
    for rd in repos_data:
        out.append(f"- {rd['name']} — {rd['url']}")
    out.append("")
    out.append("## Top Keywords")
    totals = {}
    for rd in repos_data:
        for k, v in rd.get("keyword_totals", {}).items():
            totals[k] = totals.get(k, 0) + v
    if totals:
        out += [f"- {k}: {v}" for k, v in sorted(totals.items(), key=lambda kv: kv[1], reverse=True)]
    out.append("")
    out.append("## Notable Files")
    for rd in repos_data:
        for f in rd.get("files", [])[:3]:
            out.append(f"- {rd['name']}: [{f['path']}]({f['url']})")
    return "\n".join(out)

def main():
    parser = argparse.ArgumentParser(description="Mine LUFT knowledge across recent repositories.")
    parser.add_argument("--owner", default=None, help="GitHub owner/org (defaults from config)")
    parser.add_argument("--since-days", type=int, default=None, help="Lookback window in days")
    parser.add_argument("--repos", nargs="*", help="Specific repos (optional)")
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    args = parser.parse_args()

    conf = load_config(args.config)
    owner = args.owner or conf.get("owner")
    since_days = args.since_days or int(conf.get("since_days", 90))

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    gh = Github(login_or_token=token) if token else Github()

    user = gh.get_user(owner)
    repos = []
    if args.repos:
        for r in args.repos:
            repos.append(gh.get_repo(f"{owner}/{r}") if "/" not in r else gh.get_repo(r))
    else:
        # Auto-discover repos updated in lookback window
        for r in user.get_repos(type="owner", sort="updated"):
            try:
                if within_days(r.updated_at, since_days):
                    repos.append(r)
            except Exception:
                continue

    repos_data = []
    for r in repos:
        print(f"Indexing {r.full_name} (updated {r.updated_at}) ...")
        repos_data.append(gather_repo(r, conf))

    os.makedirs("codex", exist_ok=True)
    with open("codex/index.json", "w", encoding="utf-8") as f:
        import json
        json.dump(repos_data, f, ensure_ascii=False, indent=2)
    with open("codex/index.md", "w", encoding="utf-8") as f:
        f.write(render_index_md(repos_data))
    with open("codex/dashboard.md", "w", encoding="utf-8") as f:
        f.write(render_dashboard_md(repos_data))

    print("Codex generated: codex/index.md, codex/index.json, codex/dashboard.md")

if __name__ == "__main__":
    main()
