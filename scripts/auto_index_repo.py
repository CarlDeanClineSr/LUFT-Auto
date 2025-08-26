#!/usr/bin/env python3
import os, subprocess, sys, time
from pathlib import Path

ROOT = Path(".").resolve()
OUT_DIR = ROOT / "docs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "INDEX.md"

IGNORE_DIRS = {".git", ".github", ".venv", "venv", "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache", ".idea", ".vscode"}
IGNORE_FILES = {"README.md", "readme.md", OUT_FILE.name}

def git_mtime(path: Path) -> int:
    try:
        ts = subprocess.check_output(["git", "log", "-1", "--format=%ct", str(path)], stderr=subprocess.DEVNULL).decode().strip()
        return int(ts) if ts else int(path.stat().st_mtime)
    except Exception:
        return int(path.stat().st_mtime)

def first_heading_and_tags(text: str):
    title = ""
    tags = []
    for i, line in enumerate(text.splitlines()[:40]):
        s = line.strip()
        if s.startswith("# ") and not title:
            title = s[2:].strip()
        if s.lower().startswith("tags:"):
            tags = [t.strip() for t in s.split(":", 1)[1].split(",") if t.strip()]
    return title, tags

def first_paragraph(text: str):
    lines = []
    started = False
    for s in text.splitlines():
        if s.strip().startswith("#"):
            continue
        if not s.strip():
            if started and lines:
                break
            else:
                continue
        started = True
        lines.append(s.strip())
        if len(" ".join(lines)) > 300:
            break
    para = " ".join(lines).strip()
    return (para[:280] + "…") if len(para) > 280 else para

def collect_markdown():
    items = []
    for path in ROOT.rglob("*.md"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.name in IGNORE_FILES and path.parent == ROOT:
            continue
        if path == OUT_FILE:
            continue
        try:
            txt = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        title, tags = first_heading_and_tags(txt)
        if not title:
            title = path.stem.replace("_", " ")
        summary = first_paragraph(txt)
        mtime = git_mtime(path)
        rel = path.relative_to(ROOT)
        top = rel.parts[0] if len(rel.parts) else ""
        items.append({
            "rel": str(rel).replace("\\", "/"),
            "top": top,
            "title": title,
            "tags": tags,
            "summary": summary,
            "mtime": mtime
        })
    return items

def render(items):
    # Latest 20
    latest = sorted(items, key=lambda x: x["mtime"], reverse=True)[:20]
    # Group by top folder
    groups = {}
    for it in items:
        groups.setdefault(it["top"], []).append(it)
    for k in groups:
        groups[k].sort(key=lambda x: (x["title"].lower(), -x["mtime"]))

    lines = []
    lines.append("# Repository Index")
    lines.append("")
    lines.append("_Auto-generated. Edit your files, not this index. The system will update it on push._")
    lines.append("")
    lines.append("## Latest updates")
    lines.append("")
    if not latest:
        lines.append("- No Markdown files found yet.")
    else:
        for it in latest:
            ts = time.strftime("%Y-%m-%d %H:%M", time.gmtime(it["mtime"]))
            tagstr = f" — Tags: {', '.join(it['tags'])}" if it["tags"] else ""
            summary = f" — {it['summary']}" if it["summary"] else ""
            lines.append(f"- [{it['title']}]({it['rel']}) ({ts} UTC){tagstr}{summary}")
    lines.append("")
    lines.append("## By folder")
    lines.append("")
    for top in sorted(groups.keys()):
        if top in ("",):
            section = "Top-level"
        else:
            section = top
        lines.append(f"### {section}")
        lines.append("")
        for it in groups[top]:
            tagstr = f" — Tags: {', '.join(it['tags'])}" if it["tags"] else ""
            lines.append(f"- [{it['title']}]({it['rel']}){tagstr}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"

def main():
    items = collect_markdown()
    content = render(items)
    old = OUT_FILE.read_text(encoding="utf-8") if OUT_FILE.exists() else ""
    if content != old:
        OUT_FILE.write_text(content, encoding="utf-8")
        print(f"Wrote {OUT_FILE}")
    else:
        print("Index unchanged.")

if __name__ == "__main__":
    main()
