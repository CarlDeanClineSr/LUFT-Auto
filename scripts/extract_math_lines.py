import os
import re

def looks_like_math(line):
    # Naive pattern: contains =, ^, \, numbers, or some math operators
    math_triggers = ['=', '^', '\\', 'Hz', 'kg', 'm/s', '(', ')', '+', '-', '*', '/', '∫', 'Σ', 'π', 'Ω', 'µ', 'Δ', 'λ']
    return any(t in line for t in math_triggers) and len(line.strip()) > 4

def extract_math_from_files(root='.'):
    math_lines = []
    for fname in os.listdir(root):
        if fname.startswith('New Text Document') and fname.endswith('.txt'):
            with open(os.path.join(root, fname), encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f):
                    if looks_like_math(line):
                        math_lines.append(f"{fname} (line {i+1}): {line.strip()}")
    with open('ALL_EXTRACTED_MATH.md', 'w', encoding='utf-8') as outf:
        outf.write("# Extracted Math & Equations from All Text Documents\n\n")
        for line in math_lines:
            outf.write(line + '\n')

if __name__ == "__main__":
    extract_math_from_files()
