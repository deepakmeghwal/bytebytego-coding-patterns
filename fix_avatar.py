"""
fix_avatar.py
-------------
Replaces your Google profile photo (googleusercontent.com) in all saved
lesson HTML files with a cartoon robot avatar.
Run: python3 fix_avatar.py
"""

import re
import base64
from pathlib import Path

HTML_DIR = Path("coding-patterns")

# ── Cartoon robot SVG avatar ──────────────────────────────────────────────────
ROBOT_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">
  <!-- head -->
  <rect x="8" y="10" width="24" height="20" rx="5" fill="#1677ff"/>
  <!-- left eye -->
  <circle cx="15" cy="18" r="4" fill="white"/>
  <circle cx="15" cy="18" r="2" fill="#0040a8"/>
  <circle cx="16" cy="17" r="0.8" fill="white"/>
  <!-- right eye -->
  <circle cx="25" cy="18" r="4" fill="white"/>
  <circle cx="25" cy="18" r="2" fill="#0040a8"/>
  <circle cx="26" cy="17" r="0.8" fill="white"/>
  <!-- smile -->
  <path d="M14 25 Q20 30 26 25" stroke="white" stroke-width="2" fill="none" stroke-linecap="round"/>
  <!-- antenna -->
  <rect x="18" y="4" width="4" height="7" rx="2" fill="#1677ff"/>
  <circle cx="20" cy="3" r="2.5" fill="#52c41a"/>
  <!-- ears/arms -->
  <rect x="2" y="15" width="6" height="4" rx="2" fill="#1677ff"/>
  <rect x="32" y="15" width="6" height="4" rx="2" fill="#1677ff"/>
</svg>"""

ROBOT_B64 = base64.b64encode(ROBOT_SVG.encode()).decode()
ROBOT_DATA_URL = f"data:image/svg+xml;base64,{ROBOT_B64}"

# Match any Google user content profile image URL
PATTERN = re.compile(
    r'src="https://lh3\.googleusercontent\.com/[^"]*s96-c[^"]*"',
    re.IGNORECASE
)

REPLACEMENT = f'src="{ROBOT_DATA_URL}"'


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    new_text, count = PATTERN.subn(REPLACEMENT, text)
    if count > 0:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    files = sorted(HTML_DIR.rglob("*.html"))
    files = [f for f in files if f.name != "index.html"]
    total = len(files)
    changed = 0

    print(f"Scanning {total} lesson pages...\n")
    for path in files:
        if fix_file(path):
            changed += 1
            print(f"  ✓ {path.relative_to(HTML_DIR)}")

    print(f"\nDone — replaced profile photo in {changed}/{total} pages.")
    if changed > 0:
        print("\nNow run:")
        print("  git add coding-patterns/")
        print("  git commit -m 'Replace profile photo with robot avatar'")
        print("  git push")


if __name__ == "__main__":
    main()
