import os
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

for fname in os.listdir('.'):
    if fname.startswith("New Text Document") and fname.endswith(".txt"):
        with open(fname, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip() or "note"
        new_name = slugify(first_line)[:40] + ".md"
        if not os.path.exists(new_name):
            os.rename(fname, new_name)
