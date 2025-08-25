#!/usr/bin/env python3
"""
Normalize filenames to a safe, cross-platform set:
- ascii lowercase
- replace spaces with '-'
- keep letters, digits, '-', '_', and '.'
- drop other punctuation (e.g., ':', '*', quotes)
Dry run by default; pass --apply to perform git mv.
"""

import os
import re
import sys
import subprocess
import unicodedata

ALLOWED = set("abcdefghijklmnopqrstuvwxyz0123456789-_.")
ILLEGAL = set('<>:"\\|?*')

def slugify(name: str) -> str:
    # normalize unicode to ascii
    s = unicodedata.normalize('NFKD', name)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = s.strip()
    s = s.replace(' ', '-')
    # collapse consecutive dashes
    s = re.sub(r'-{2,}', '-', s)
    out = []
    for ch in s:
        ch_low = ch.lower()
        if ch_low in ALLOWED:
            out.append(ch_low)
        elif ch_low == '.':
            out.append('.')
        # otherwise drop
    # avoid leading/trailing dots
    cleaned = ''.join(out).strip('.')
    # avoid empty names
    return cleaned or 'unnamed'

def git_mv(src, dst):
    subprocess.check_call(["git", "mv", "-f", src, dst])


def main():
    apply = "--apply" in sys.argv
    changes = []
    for root, dirs, files in os.walk(".", topdown=True):
        if root.startswith("./.git"):
            continue
        entries = [(True, d) for d in dirs] + [(False, f) for f in files]
        for is_dir, name in entries:
            full = os.path.join(root, name)
            rel = os.path.relpath(full, ".")
            if rel.startswith(".git"):
                continue
            # skip the script itself
            if rel == os.path.relpath(__file__, "."):
                continue
            # detect illegal chars or spaces or uppercase
            bad = any(ch in ILLEGAL for ch in name) or (' ' in name) or (name != name.lower())
            if bad:
                target_name = slugify(name)
                if target_name != name:
                    target_path = os.path.join(root, target_name)
                    # ensure unique by appending numeric suffix if needed
                    base, ext = os.path.splitext(target_path)
                    k = 1
                    unique = target_path
                    while os.path.exists(unique):
                        unique = f"{base}-{k}{ext}"
                        k += 1
                    changes.append((rel, os.path.relpath(unique, ".")))
    if not changes:
        print("No changes needed.")
        return
    print("Planned renames:")
    for src, dst in changes:
        print(f" - {src} -> {dst}")
    if apply:
        for src, dst in changes:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            git_mv(src, dst)
        print("Applied renames with git mv.")
    else:
        print("\nDry run. Re-run with --apply to perform renames.")

if __name__ == "__main__":
    main()