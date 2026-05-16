"""
convert.py
----------
Converts all .mhtml files in coding-patterns/ to self-contained .html files.
- Inlines all CSS as <style> tags
- Converts all images to base64 data URLs
- Updates coding-patterns/index.html links from .mhtml → .html
- Deletes .mhtml files after successful conversion

Run once: python3 convert.py
"""

import email
import base64
import re
from pathlib import Path

PATTERNS_DIR = Path("coding-patterns")


def parse_mhtml(mhtml_path: Path):
    """
    Parse an MHTML file and return (html_content, resources_dict).
    resources_dict maps content-id → (mime_type, bytes)
    """
    raw = mhtml_path.read_bytes()
    msg = email.message_from_bytes(raw)

    resources = {}   # key (cid or url) → (mime_type, raw_bytes)
    html_content = None

    for part in msg.walk():
        ct  = part.get_content_type()
        cid = part.get("Content-ID", "").strip("<>").strip()
        loc = part.get("Content-Location", "").strip()

        payload = part.get_payload(decode=True)
        if payload is None:
            continue

        # First text/html part = the actual page
        if ct == "text/html" and html_content is None:
            charset = part.get_content_charset() or "utf-8"
            html_content = payload.decode(charset, errors="replace")
            continue

        # Index every resource by cid and by location URL
        for key in filter(None, [cid, loc]):
            resources[key] = (ct, payload)

    return html_content, resources


def inline_resources(html: str, resources: dict) -> str:
    """
    Replace all cid: references in HTML:
    - <link rel="stylesheet" href="cid:..."> → <style>...</style>
    - src="cid:..."                          → src="data:mime;base64,..."
    - href="cid:..." (non-CSS)               → data URL
    """

    # ── Inline CSS <link> tags ───────────────────────────────────────────────
    def replace_css_link(m):
        full_tag = m.group(0)
        cid_key  = m.group(1)
        r = resources.get(cid_key)
        if r:
            mime, data = r
            if "css" in mime:
                css_text = data.decode("utf-8", errors="replace")
                return f"<style>{css_text}</style>"
        return full_tag

    # Matches <link ... href="cid:KEY" ...> in various attribute orders
    html = re.sub(
        r'<link\b[^>]*\bhref="cid:([^"]+)"[^>]*/?>',
        replace_css_link,
        html,
        flags=re.IGNORECASE,
    )

    # ── Inline src="cid:..." (images, fonts, etc.) ───────────────────────────
    def replace_src(m):
        cid_key = m.group(1)
        r = resources.get(cid_key)
        if r:
            mime, data = r
            b64 = base64.b64encode(data).decode()
            return f'src="data:{mime};base64,{b64}"'
        return m.group(0)

    html = re.sub(r'src="cid:([^"]+)"', replace_src, html)

    # ── Inline remaining href="cid:..." (e.g. fonts) ─────────────────────────
    def replace_href(m):
        cid_key = m.group(1)
        r = resources.get(cid_key)
        if r:
            mime, data = r
            b64 = base64.b64encode(data).decode()
            return f'href="data:{mime};base64,{b64}"'
        return m.group(0)

    html = re.sub(r'href="cid:([^"]+)"', replace_href, html)

    return html


def convert_file(mhtml_path: Path) -> bool:
    """Convert one .mhtml to .html. Returns True on success."""
    html, resources = parse_mhtml(mhtml_path)
    if not html:
        print(f"  ✗ Could not parse: {mhtml_path}")
        return False

    html = inline_resources(html, resources)

    html_path = mhtml_path.with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")
    return True


def update_index():
    """Rewrite index.html so all .mhtml links become .html links."""
    index = PATTERNS_DIR / "index.html"
    if not index.exists():
        return
    content = index.read_text(encoding="utf-8")
    updated = content.replace('.mhtml"', '.html"')
    index.write_text(updated, encoding="utf-8")
    print("  index.html links updated (.mhtml → .html)")


def main():
    mhtml_files = sorted(PATTERNS_DIR.rglob("*.mhtml"))
    total = len(mhtml_files)

    if total == 0:
        print("No .mhtml files found in coding-patterns/")
        return

    print(f"Converting {total} files...\n")
    ok = 0
    fail = 0

    for i, path in enumerate(mhtml_files, 1):
        rel = path.relative_to(PATTERNS_DIR)
        print(f"[{i}/{total}] {rel}")
        if convert_file(path):
            path.unlink()          # delete .mhtml after successful conversion
            ok += 1
        else:
            fail += 1

    print(f"\nUpdating navigator links...")
    update_index()

    print(f"\n{'='*50}")
    print(f"  Converted : {ok}")
    print(f"  Failed    : {fail}")
    print(f"  Total     : {total}")
    print(f"{'='*50}")
    print(f"\nDone! Now run:")
    print(f"  git add coding-patterns/")
    print(f"  git commit -m 'Convert MHTML to self-contained HTML'")
    print(f"  git push")


if __name__ == "__main__":
    main()
