import re
import os
from pathlib import Path

# Set this to your LUFT-Auto repo root, or "." if running from the root
repo_path = "path/to/LUFT-Auto"  # <- Replace or set to "."

# Improved pattern: captures math-like expressions (LaTeX, inline math, equations)
math_pattern = re.compile(
    r"""
    (
        [A-Za-z]+\s*=\s*[^;\n]+         # Assignments: x = something
        | [A-Za-z]+\s*\([^\)]*\)\s*=    # Functions: f(x) = ...
        | [A-Za-z0-9_]+\^[\dA-Za-z_]+   # Powers: x^2, y^n
        | [\d\.]+[eE][+\-]?\d+          # Scientific notation: 1.23e-4
        | [\d\.]+[\+\-\*/^][\d\.]+      # Arithmetic: 3+4, 2.5*10
        | \\[a-zA-Z]+                   # LaTeX commands: \frac, \int
        | [A-Za-z]_\{[A-Za-z0-9]+\}     # Subscripts: x_{i}
    )
    """,
    re.VERBOSE,
)

output = []
start, end = 2, 125  # Adjust range if needed

for i in range(start, end + 1):
    file_path = os.path.join(repo_path, f"New Text Document ({i}).txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            math_lines = math_pattern.findall(content)
            if math_lines:
                output.append(f"File: New Text Document ({i}).txt")
                for line in math_lines:
                    output.append(f"- {line}")

with open("math_extract.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(output))

print("Extraction complete! See math_extract.txt for results.")
