"""
fix_navigation.py
-----------------
Fixes the redirect-to-bytebytego.com problem in all lesson pages by:
  1. Removing the href from the header logo link (so clicking it stays local)
  2. Removing the href from the "My Courses" nav link
  3. Removing broken cid: CSS <link> tags (they never load anyway)
  4. Fixing footnote/anchor hrefs that point to bytebytego.com back to local anchors

Also bypasses the login gate in coding-patterns/index.html so the
site opens directly on the first lesson (no credentials required).

Run once: python3 fix_navigation.py
"""

import re
from pathlib import Path

HTML_DIR = Path("coding-patterns")

# ── Regex patterns ────────────────────────────────────────────────────────────

# 1. Header logo anchor: <a class="...headerLogoLink" href="https://bytebytego.com/">
LOGO_LINK = re.compile(
    r'(<a\b[^>]*\bstyle-module-scss-module__\w+__headerLogoLink\b[^>]*)'
    r'\bhref="https://bytebytego\.com/"',
    re.IGNORECASE,
)

# 2. "My Courses" nav link
MY_COURSES = re.compile(
    r'(<a\b[^>]*)href="https://bytebytego\.com/my-courses"([^>]*>My Courses</a>)',
    re.IGNORECASE,
)

# 3. Broken cid: stylesheet <link> tags
CID_LINK = re.compile(
    r'<link\b[^>]*href="cid:[^"]*"[^>]*/?>',
    re.IGNORECASE,
)

# 4. Footnote hrefs that point to bytebytego.com/courses/...#anchor
#    e.g. href="https://bytebytego.com/courses/coding-patterns/binary-search/foo#user-content-fn-1"
#    → strip the full URL, keep only the fragment: href="#user-content-fn-1"
FOOTNOTE_HREF = re.compile(
    r'href="https://bytebytego\.com/courses/coding-patterns/[^#"]*#([^"]+)"',
    re.IGNORECASE,
)


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    # 1. Remove href from logo link (keep the <a> tag but make it non-navigating)
    text = LOGO_LINK.sub(r'\1href="javascript:void(0)"', text)

    # 2. Remove href from My Courses link
    text = MY_COURSES.sub(r'\1\2', text)

    # 3. Strip broken cid: <link> tags entirely
    text = CID_LINK.sub('', text)

    # 4. Fix footnote anchor links to use local fragment only
    text = FOOTNOTE_HREF.sub(r'href="#\1"', text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def bypass_login_gate():
    """Replace the login wall with an immediate redirect to the first lesson."""
    index = HTML_DIR / "index.html"
    if not index.exists():
        print("  ⚠  coding-patterns/index.html not found — skipping login fix")
        return

    content = index.read_text(encoding="utf-8")

    # If it's already been fixed (no login form), skip
    if 'id="login-btn"' not in content:
        print("  ✓ Login gate already removed — skipping")
        return

    FIRST_LESSON = "two-pointers/introduction-to-two-pointers.html"
    new_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url={FIRST_LESSON}">
  <title>Redirecting…</title>
</head>
<body>
  <script>window.location.replace("{FIRST_LESSON}")</script>
</body>
</html>
"""
    index.write_text(new_content, encoding="utf-8")
    print("  ✓ Login gate removed — index.html now redirects straight to first lesson")


def main():
    files = sorted(HTML_DIR.rglob("*.html"))
    lesson_files = [f for f in files if f.name != "index.html"]
    total = len(lesson_files)

    print(f"\n1) Fixing navigation redirects in {total} lesson pages…\n")
    changed = 0
    for path in lesson_files:
        if fix_file(path):
            changed += 1
            print(f"   ✓ {path.relative_to(HTML_DIR)}")

    print(f"\n   Fixed: {changed}/{total} pages")

    print("\n2) Bypassing login gate…\n  ", end="")
    bypass_login_gate()

    print(f"\n{'='*55}")
    print("  Done! Push to GitHub Pages to see the fix live:")
    print("    git add coding-patterns/")
    print("    git commit -m 'Fix navigation redirects and remove login gate'")
    print("    git push")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
