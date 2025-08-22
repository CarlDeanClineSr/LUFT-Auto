import os

MANIFEST = "repo_manifest.txt"

def main():
    files = []
    for root, dirs, filenames in os.walk("."):
        for f in filenames:
            if f.startswith(".") or root.startswith("./.github"):
                continue
            path = os.path.join(root, f)
            files.append(path.lstrip("./"))
    with open(MANIFEST, "w", encoding="utf-8") as f:
        for fname in sorted(files):
            f.write(f"{fname}\n")

if __name__ == "__main__":
    main()
