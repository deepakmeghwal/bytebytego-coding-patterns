"""
fix_layout_css.py
-----------------
Injects a local layout.css link into every lesson page and removes the dead
bytebytego.com external CSS <link> tags (they all return 404 now).

Run once: python3 fix_layout_css.py
"""

import re
from pathlib import Path

HTML_DIR = Path("coding-patterns")

# Remove dead external bytebytego.com stylesheet <link> tags
EXTERNAL_CSS = re.compile(
    r'<link\b[^>]*href="https://bytebytego\.com/_next/static/chunks/[^"]+\.css[^"]*"[^>]*/?>',
    re.IGNORECASE,
)

# Also remove related <link rel="preload" as="style"> for same files
EXTERNAL_PRELOAD_CSS = re.compile(
    r'<link\b[^>]*rel="preload"[^>]*as="style"[^>]*href="https://bytebytego\.com/_next/static/chunks/[^"]*\.css[^"]*"[^>]*/?>',
    re.IGNORECASE,
)

# The local CSS tag to inject — path is always relative to chapter subfolder
LOCAL_CSS_TAG = '<link rel="stylesheet" href="../layout.css">'

INJECT_MARKER = "</head>"


def fix_file(path: Path) -> str:
    """Returns 'changed', 'already_fixed', or 'no_head'."""
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    # Skip if already has our local stylesheet
    if 'href="../layout.css"' in text:
        return "already_fixed"

    # Strip dead external CSS links
    text = EXTERNAL_CSS.sub("", text)
    text = EXTERNAL_PRELOAD_CSS.sub("", text)

    # Inject local layout.css just before </head>
    if INJECT_MARKER in text:
        text = text.replace(INJECT_MARKER, LOCAL_CSS_TAG + "\n" + INJECT_MARKER, 1)
    else:
        return "no_head"

    if text != original:
        path.write_text(text, encoding="utf-8")
        return "changed"

    return "already_fixed"


def main():
    files = sorted(HTML_DIR.rglob("*.html"))
    lesson_files = [f for f in files if f.name != "index.html"]
    total = len(lesson_files)

    print(f"\nInserting layout.css into {total} lesson pages…\n")
    changed = already = no_head = 0

    for path in lesson_files:
        result = fix_file(path)
        rel = path.relative_to(HTML_DIR)
        if result == "changed":
            changed += 1
            print(f"  ✓ {rel}")
        elif result == "already_fixed":
            already += 1
        elif result == "no_head":
            no_head += 1
            print(f"  ⚠ no </head> found: {rel}")

    print(f"\n  Updated  : {changed}")
    print(f"  Skipped  : {already} (already fixed)")
    if no_head:
        print(f"  Warning  : {no_head} files had no </head>")
    print(f"\nDone! Restart local server and refresh to verify layout.")
    print("\nThen push:")
    print("  git add coding-patterns/")
    print("  git commit -m 'Add fallback layout.css, remove dead external CSS'")
    print("  git push")


if __name__ == "__main__":
    main()
