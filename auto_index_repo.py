import os

INDEX = "INDEX.md"

def main():
    files = []
    for root, dirs, filenames in os.walk("."):
        for f in filenames:
            if f.startswith(".") or root.startswith("./.github"):
                continue
            path = os.path.join(root, f)
            files.append(path.lstrip("./"))
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write("# LUFT Repository Index\n\n")
        for fname in sorted(files):
            f.write(f"- {fname}\n")

if __name__ == "__main__":
    main()
