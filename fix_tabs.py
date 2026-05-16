"""
fix_tabs.py
-----------
Injects the missing Ant-Design CSS rule that hides non-active code tab panels.
The class .ant-tabs-tabpane-hidden is already on the right elements but the
CSS rule that makes it invisible was never captured in the MHTML save.
Run: python3 fix_tabs.py
"""

from pathlib import Path

HTML_DIR = Path("coding-patterns")

# CSS rules missing from the MHTML capture:
#   1. Hide non-active tab panels
#   2. Lay the tab button bar out horizontally (flex row)
FIX_CSS = """<style>
/* Hide non-active code tab panels */
.ant-tabs-tabpane-hidden{display:none!important}

/* Horizontal tab nav layout (Ant Design flex rules not captured in MHTML) */
.ant-tabs-nav{display:flex;flex:none;align-items:center;position:relative}
.ant-tabs-nav-wrap{position:relative;display:flex;flex:auto;align-self:stretch;overflow:hidden;white-space:nowrap}
.ant-tabs-nav-list{position:relative;display:flex;flex-direction:row;transition:transform .3s}
.ant-tabs-tab{position:relative;display:inline-flex;align-items:center;padding:8px 0;font-size:14px;background:transparent;border:0;outline:none;cursor:pointer;margin:0 32px 0 0}
.ant-tabs-tab:last-child{margin-right:0}
.ant-tabs-tab-btn{outline:none;transition:all .3s}
.ant-tabs-content-holder{flex:auto;min-width:0;min-height:0}
.ant-tabs-content{display:flex;width:100%}
.ant-tabs-tabpane{flex:none;width:100%;outline:none}
</style>"""

def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    # Skip files that already have the full fix (look for the layout rule)
    if "flex-direction:row" in text:
        return False
    # Skip pages that have no code tabs at all
    if "ant-tabs-tabpane" not in text:
        return False
    # Inject right before </head>
    if "</head>" in text:
        new_text = text.replace("</head>", FIX_CSS + "</head>", 1)
    else:
        # Fallback: prepend to body
        new_text = FIX_CSS + text
    path.write_text(new_text, encoding="utf-8")
    return True


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

    print(f"\nDone — fixed code tabs in {changed}/{total} pages.")
    if changed > 0:
        print("\nNow run:")
        print("  git add coding-patterns/")
        print("  git commit -m 'Fix code tab visibility (show Java only)'")
        print("  git push")


if __name__ == "__main__":
    main()
