import os, re, datetime
from googletrans import Translator

README = "README.md"
MANIFEST = "repo_manifest.txt"
LANGUAGES = {
    'en': 'English',
    'fr': 'Français',
    'ru': 'Русский',
    'ja': '日本語'
}

def get_manifest_stats():
    try:
        with open(MANIFEST, "r", encoding="utf-8") as f:
            files = [l.strip() for l in f if l.strip()]
        return len(files), files
    except FileNotFoundError:
        return 0, []

def make_stats_block(total, lang_code, translator):
    base_text = f"### 📊 LUFT Repo Manifest\n\n- **Total files:** {total}\n- **Last update:** {datetime.datetime.utcnow().isoformat()}Z\n"
    if lang_code == 'en':
        return base_text
    try:
        translated = translator.translate(base_text, src='en', dest=lang_code).text
        return translated
    except Exception:
        return base_text  # fallback to English

def insert_or_replace_block(readme, new_block, marker):
    if marker in readme:
        pattern = re.compile(rf"(<!-- {marker} START -->).*?(<!-- {marker} END -->)", re.DOTALL)
        return pattern.sub(rf"\1\n{new_block}\n\2", readme)
    else:
        return f"<!-- {marker} START -->\n{new_block}\n<!-- {marker} END -->\n\n" + readme

def main():
    total, _ = get_manifest_stats()
    translator = Translator()
    try:
        with open(README, "r", encoding="utf-8") as f:
            readme = f.read()
    except FileNotFoundError:
        readme = ""

    for lang_code, lang_name in LANGUAGES.items():
        block = make_stats_block(total, lang_code, translator)
        marker = f"LUFT_MANIFEST_{lang_code.upper()}"
        readme = insert_or_replace_block(readme, block, marker)

    with open(README, "w", encoding="utf-8") as f:
        f.write(readme)

if __name__ == "__main__":
    main()
