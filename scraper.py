"""
ByteByteGo Coding Patterns Scraper
-----------------------------------
Saves pages as .mhtml files (opens perfectly in Chrome offline).

First run  : opens browser → you log in manually → cookies saved to session.json.
Later runs : loads session.json → no login needed.
Expired    : detects expired session → opens browser for manual login again.
No credentials are ever stored — only session cookies.
"""

import asyncio
import json
import random
from pathlib import Path
from playwright.async_api import async_playwright

# ─── Config ────────────────────────────────────────────────────────────────────

BASE_URL     = "https://bytebytego.com/courses/coding-patterns"
COOKIES_FILE = Path("session.json")
OUTPUT_DIR   = Path("coding-patterns")
LOGIN_URL    = "https://bytebytego.com/signin"

# ── Scrape mode ────────────────────────────────────────────────────────────────
# Set SCRAPE_MODE to one of:
#   "single"  → download only the one page defined in SINGLE_PAGE below
#   "chapter" → download all lessons in SCRAPE_CHAPTER
#   "all"     → download all 120 pages
SCRAPE_MODE    = "all"
SCRAPE_CHAPTER = "two-pointers"   # used only when SCRAPE_MODE = "chapter"

SINGLE_PAGE = {
    "chapter": "two-pointers",
    "lesson":  "introduction-to-two-pointers",
}

# ── Delay between pages (seconds) ──────────────────────────────────────────────
# Random range makes requests look human-like and avoids rate limiting.
DELAY_MIN = 3   # minimum seconds to wait between pages
DELAY_MAX = 6   # maximum seconds to wait between pages

# ─── All 120 pages (used when SCRAPE_ALL = True) ───────────────────────────────

ALL_PAGES = [
    # 01 Two Pointers
    ("two-pointers", "introduction-to-two-pointers"),
    ("two-pointers", "pair-sum-sorted"),
    ("two-pointers", "triplet-sum"),
    ("two-pointers", "is-palindrome-valid"),
    ("two-pointers", "largest-container"),
    ("two-pointers", "shift-zeros-to-the-end"),
    ("two-pointers", "next-lexicographical-sequence"),
    # 02 Hash Maps And Sets
    ("hash-maps-and-sets", "introduction-to-hash-maps-and-sets"),
    ("hash-maps-and-sets", "pair-sum-unsorted"),
    ("hash-maps-and-sets", "verify-sudoku-board"),
    ("hash-maps-and-sets", "zero-striping"),
    ("hash-maps-and-sets", "longest-chain-of-consecutive-numbers"),
    ("hash-maps-and-sets", "geometric-sequence-triplets"),
    # 03 Linked Lists
    ("linked-lists", "introduction-to-linked-lists"),
    ("linked-lists", "linked-list-reversal"),
    ("linked-lists", "remove-the-kth-last-node-from-a-linked-list"),
    ("linked-lists", "linked-list-intersection"),
    ("linked-lists", "lru-cache"),
    ("linked-lists", "palindromic-linked-list"),
    ("linked-lists", "flatten-a-multi-level-linked-list"),
    # 04 Fast And Slow Pointers
    ("fast-and-slow-pointers", "introduction-to-fast-and-slow-pointers"),
    ("fast-and-slow-pointers", "linked-list-loop"),
    ("fast-and-slow-pointers", "linked-list-midpoint"),
    ("fast-and-slow-pointers", "happy-number"),
    # 05 Sliding Windows
    ("sliding-windows", "introduction-to-sliding-windows"),
    ("sliding-windows", "substring-anagrams"),
    ("sliding-windows", "longest-substring-with-unique-characters"),
    ("sliding-windows", "longest-uniform-substring-after-replacements"),
    # 06 Binary Search
    ("binary-search", "introduction-to-binary-search"),
    ("binary-search", "find-the-insertion-index"),
    ("binary-search", "first-and-last-occurrences-of-a-number"),
    ("binary-search", "cutting-wood"),
    ("binary-search", "find-the-target-in-a-rotated-sorted-array"),
    ("binary-search", "find-the-median-from-two-sorted-arrays"),
    ("binary-search", "matrix-search"),
    ("binary-search", "local-maxima-in-array"),
    ("binary-search", "weighted-random-selection"),
    # 07 Stacks
    ("stacks", "introduction-to-stacks"),
    ("stacks", "valid-parenthesis-expression"),
    ("stacks", "next-largest-number-to-the-right"),
    ("stacks", "evaluate-expression"),
    ("stacks", "repeated-removal-of-adjacent-duplicates"),
    ("stacks", "implement-a-queue-using-stacks"),
    ("stacks", "maximums-of-sliding-window"),
    # 08 Heaps
    ("heaps", "introduction-to-heaps"),
    ("heaps", "k-most-frequent-strings"),
    ("heaps", "combine-sorted-linked-lists"),
    ("heaps", "median-of-an-integer-stream"),
    ("heaps", "sort-a-k-sorted-array"),
    # 09 Intervals
    ("intervals", "introduction-to-intervals"),
    ("intervals", "merge-overlapping-intervals"),
    ("intervals", "identify-all-interval-overlaps"),
    ("intervals", "largest-overlap-of-intervals"),
    # 10 Prefix Sums
    ("prefix-sums", "introduction-to-prefix-sums"),
    ("prefix-sums", "sum-between-range"),
    ("prefix-sums", "k-sum-subarrays"),
    ("prefix-sums", "product-array-without-current-element"),
    # 11 Trees
    ("trees", "introduction-to-trees"),
    ("trees", "invert-binary-tree"),
    ("trees", "balanced-binary-tree-validation"),
    ("trees", "rightmost-nodes-of-a-binary-tree"),
    ("trees", "widest-binary-tree-level"),
    ("trees", "binary-search-tree-validation"),
    ("trees", "lowest-common-ancestor"),
    ("trees", "build-binary-tree-from-preorder-and-inorder-traversals"),
    ("trees", "maximum-sum-of-a-continuous-path-in-a-binary-tree"),
    ("trees", "binary-tree-symmetry"),
    ("trees", "binary-tree-columns"),
    ("trees", "kth-smallest-number-in-a-binary-search-tree"),
    ("trees", "serialize-and-deserialize-a-binary-tree"),
    # 12 Tries
    ("tries", "introduction-to-tries"),
    ("tries", "design-a-trie"),
    ("tries", "insert-and-search-words-with-wildcards"),
    ("tries", "find-all-words-on-a-board"),
    # 13 Graphs
    ("graphs", "introduction-to-graphs"),
    ("graphs", "graph-deep-copy"),
    ("graphs", "count-islands"),
    ("graphs", "matrix-infection"),
    ("graphs", "bipartite-graph-validation"),
    ("graphs", "longest-increasing-path"),
    ("graphs", "shortest-transformation-sequence"),
    ("graphs", "merging-communities"),
    ("graphs", "prerequisites"),
    ("graphs", "shortest-path"),
    ("graphs", "connect-the-dots"),
    # 14 Backtracking
    ("backtracking", "introduction-to-backtracking"),
    ("backtracking", "find-all-permutations"),
    ("backtracking", "find-all-subsets"),
    ("backtracking", "n-queens"),
    ("backtracking", "combinations-of-a-sum"),
    ("backtracking", "phone-keypad-combinations"),
    # 15 Dynamic Programming
    ("dynamic-programming", "introduction-to-dynamic-programming"),
    ("dynamic-programming", "climbing-stairs"),
    ("dynamic-programming", "minimum-coin-combination"),
    ("dynamic-programming", "matrix-pathways"),
    ("dynamic-programming", "neighborhood-burglary"),
    ("dynamic-programming", "longest-common-subsequence"),
    ("dynamic-programming", "longest-palindrome-in-a-string"),
    ("dynamic-programming", "maximum-subarray-sum"),
    ("dynamic-programming", "0-1-knapsack"),
    ("dynamic-programming", "largest-square-in-a-matrix"),
    # 16 Greedy
    ("greedy", "introduction-to-greedy-algorithms"),
    ("greedy", "jump-to-the-end"),
    ("greedy", "gas-stations"),
    ("greedy", "candies"),
    # 17 Sort And Search
    ("sort-and-search", "introduction-to-sort-and-search"),
    ("sort-and-search", "sort-linked-list"),
    ("sort-and-search", "sort-array"),
    ("sort-and-search", "kth-largest-integer"),
    ("sort-and-search", "dutch-national-flag"),
    # 18 Bit Manipulation
    ("bit-manipulation", "introduction-to-bit-manipulation"),
    ("bit-manipulation", "hamming-weights-of-integers"),
    ("bit-manipulation", "lonely-integer"),
    ("bit-manipulation", "swap-odd-and-even-bits"),
    # 19 Math And Geometry
    ("math-and-geometry", "introduction-to-math-and-geometry"),
    ("math-and-geometry", "spiral-traversal"),
    ("math-and-geometry", "reverse-32-bit-integer"),
    ("math-and-geometry", "maximum-collinear-points"),
    ("math-and-geometry", "the-josephus-problem"),
    ("math-and-geometry", "triangle-numbers"),
]

# ─── Helpers ───────────────────────────────────────────────────────────────────

def build_url(chapter: str, lesson: str) -> str:
    return f"{BASE_URL}/{chapter}/{lesson}"


def build_output_path(chapter: str, lesson: str) -> Path:
    folder = OUTPUT_DIR / chapter
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{lesson}.mhtml"


async def save_as_mhtml(page, filepath: Path):
    """Capture full page snapshot as MHTML via Chrome DevTools Protocol."""
    cdp = await page.context.new_cdp_session(page)
    result = await cdp.send("Page.captureSnapshot", {"format": "mhtml"})
    filepath.write_text(result["data"], encoding="utf-8")
    await cdp.detach()


async def wait_for_content(page):
    """
    Wait for the page to fully render with hard timeouts on every step.
    Nothing here can hang forever — every call has a deadline.
    """
    # Step 1: wait for basic DOM + resources (max 20s)
    try:
        await page.wait_for_load_state("load", timeout=20000)
    except Exception:
        pass

    # Step 2: scroll to trigger lazy-loaded images — capped at 10 seconds max
    try:
        await asyncio.wait_for(
            page.evaluate("""
                () => new Promise(resolve => {
                    const step  = 500;
                    const pause = 200;
                    let   max   = 30;          // at most 30 steps = 6 s
                    const id = setInterval(() => {
                        window.scrollBy(0, step);
                        max--;
                        const atBottom =
                            window.scrollY + window.innerHeight >=
                            document.body.scrollHeight - 10;
                        if (atBottom || max <= 0) {
                            clearInterval(id);
                            window.scrollTo(0, 0);
                            resolve();
                        }
                    }, pause);
                })
            """),
            timeout=10
        )
    except Exception:
        # If scroll hangs or errors, just scroll back to top and move on
        try:
            await page.evaluate("window.scrollTo(0, 0)")
        except Exception:
            pass

    # Step 3: fixed buffer for final renders (images, syntax highlighting)
    await asyncio.sleep(2)


async def switch_all_code_blocks_to_java(page):
    """
    Click every Java tab on the page. Each click has a hard 3-second timeout
    so a single stuck element cannot block the whole scrape.
    """
    java_tab_selectors = [
        'button:has-text("Java")',
        '[role="tab"]:has-text("Java")',
        'li:has-text("Java")',
        'span:has-text("Java")',
    ]
    clicked = 0
    for selector in java_tab_selectors:
        try:
            tabs = await asyncio.wait_for(
                page.query_selector_all(selector), timeout=3
            )
        except Exception:
            continue
        for tab in tabs:
            try:
                visible = await asyncio.wait_for(tab.is_visible(), timeout=2)
                if visible:
                    await asyncio.wait_for(tab.click(), timeout=2)
                    await asyncio.sleep(0.3)
                    clicked += 1
            except Exception:
                pass

    if clicked > 0:
        print(f"        → Switched {clicked} code block(s) to Java")
        await asyncio.sleep(0.5)
    else:
        print("        → No Java tabs found")


# ─── Session ───────────────────────────────────────────────────────────────────

async def load_session(context) -> bool:
    """Restore cookies from a previous run."""
    if COOKIES_FILE.exists():
        cookies = json.loads(COOKIES_FILE.read_text())
        await context.add_cookies(cookies)
        return True
    return False


async def save_session(context):
    """Persist current browser cookies to disk."""
    cookies = await context.cookies()
    COOKIES_FILE.write_text(json.dumps(cookies, indent=2))


async def manual_login(page, context):
    """
    Open the login page and wait for the user to log in manually.
    Once done, they press ENTER in the terminal — cookies are saved automatically.
    This is the only time login is ever needed (until the session expires).
    """
    await page.goto(LOGIN_URL)
    print("\n" + "=" * 60)
    print("  Please log in to ByteByteGo in the browser window.")
    print("  After you are fully logged in and see lesson content,")
    print("  come back here and press ENTER.")
    print("=" * 60)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, input, "\n  >>> Press ENTER after login: ")
    await save_session(context)
    print("  Session saved — you won't be asked to log in again.\n")


async def handle_login(page, context):
    """
    Ask the user whether login is needed.
    - If yes  → open browser to login page, wait for them to finish, confirm, save cookies.
    - If no   → load saved session cookies and continue.
    Session cookies are always saved after a successful login so future runs skip this step.
    """
    loop = asyncio.get_event_loop()

    print("\n" + "=" * 60)
    needs_login = await loop.run_in_executor(
        None, input,
        "  Do you need to log in to ByteByteGo? (y/n): "
    )
    print("=" * 60 + "\n")

    if needs_login.strip().lower() == "y":
        # Open the login page in the browser
        await page.goto(LOGIN_URL)
        print("Browser opened — please log in now.")
        print("Come back here once you can see a lesson page.\n")

        await loop.run_in_executor(
            None, input,
            "  >>> Login done? Press ENTER to continue: "
        )

        await save_session(context)
        print("\n  Session saved — future runs will skip login automatically.\n")
    else:
        # Try to restore a saved session
        if await load_session(context):
            print("Loaded saved session — continuing without login.\n")
        else:
            print("No saved session found. Re-run and choose 'y' to log in first.\n")
            raise SystemExit(1)


# ─── Index builder ─────────────────────────────────────────────────────────────

def build_index():
    """
    Generate index.html — a clean offline navigator for all downloaded pages.
    Shows chapters as collapsible sections; links open the local .mhtml file.
    Re-run any time to refresh after more pages are downloaded.
    """
    from collections import defaultdict

    # Group downloaded files by chapter
    chapters: dict[str, list[str]] = defaultdict(list)
    for chapter, lesson in ALL_PAGES:
        path = OUTPUT_DIR / chapter / f"{lesson}.mhtml"
        if path.exists():
            chapters[chapter].append(lesson)

    if not chapters:
        return  # Nothing downloaded yet

    chapter_order = []
    seen = set()
    for chapter, _ in ALL_PAGES:
        if chapter not in seen:
            chapter_order.append(chapter)
            seen.add(chapter)

    def prettify(slug: str) -> str:
        return slug.replace("-", " ").title()

    rows = []
    for chapter in chapter_order:
        lessons = chapters.get(chapter, [])
        if not lessons:
            continue
        rows.append(f'<details open><summary class="chapter">{prettify(chapter)}</summary><ul>')
        for lesson in lessons:
            href = f"{chapter}/{lesson}.mhtml"
            rows.append(f'  <li><a href="{href}" target="_blank">{prettify(lesson)}</a></li>')
        rows.append("</ul></details>")

    total = sum(len(v) for v in chapters.values())
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ByteByteGo — Coding Patterns (Offline)</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          background: #0f172a; color: #e2e8f0; display: flex;
          min-height: 100vh; }}
  nav  {{ width: 300px; min-width: 260px; background: #1e293b;
          padding: 24px 16px; overflow-y: auto; height: 100vh;
          position: sticky; top: 0; border-right: 1px solid #334155; }}
  nav h1 {{ font-size: 15px; font-weight: 700; color: #f8fafc;
             margin-bottom: 4px; letter-spacing: .3px; }}
  nav p  {{ font-size: 12px; color: #64748b; margin-bottom: 20px; }}
  details {{ margin-bottom: 6px; }}
  summary.chapter {{
    cursor: pointer; list-style: none; padding: 8px 10px;
    font-size: 13px; font-weight: 600; color: #94a3b8;
    text-transform: uppercase; letter-spacing: .6px;
    border-radius: 6px; user-select: none;
  }}
  summary.chapter:hover {{ background: #273549; color: #e2e8f0; }}
  ul {{ list-style: none; padding-left: 10px; margin-top: 2px; }}
  li a {{
    display: block; padding: 6px 12px; font-size: 13px; color: #cbd5e1;
    text-decoration: none; border-radius: 5px; line-height: 1.4;
  }}
  li a:hover {{ background: #334155; color: #f1f5f9; }}
  main {{
    flex: 1; display: flex; align-items: center; justify-content: center;
    flex-direction: column; gap: 12px; padding: 40px;
  }}
  main h2 {{ font-size: 24px; color: #f8fafc; }}
  main p  {{ color: #64748b; font-size: 14px; text-align: center; max-width: 420px; }}
  .badge {{
    background: #1d4ed8; color: #fff; font-size: 12px; font-weight: 600;
    padding: 3px 10px; border-radius: 12px; margin-left: 8px;
  }}
</style>
</head>
<body>
<nav>
  <h1>Coding Patterns <span class="badge">{total}</span></h1>
  <p>Click any lesson to open it offline</p>
  {"".join(rows)}
</nav>
<main>
  <h2>ByteByteGo — Offline Study</h2>
  <p>Select a lesson from the sidebar. Each page opens in a new tab with full content and Java code.</p>
</main>
</body>
</html>"""

    index_path = OUTPUT_DIR / "index.html"
    index_path.write_text(html, encoding="utf-8")
    print(f"Navigator updated → {index_path.resolve()}")


# ─── Main ──────────────────────────────────────────────────────────────────────

async def main():
    if SCRAPE_MODE == "all":
        pages_to_scrape = ALL_PAGES
    elif SCRAPE_MODE == "chapter":
        pages_to_scrape = [(c, l) for c, l in ALL_PAGES if c == SCRAPE_CHAPTER]
        if not pages_to_scrape:
            print(f"Chapter '{SCRAPE_CHAPTER}' not found. Check the spelling.")
            return
    else:
        pages_to_scrape = [(SINGLE_PAGE["chapter"], SINGLE_PAGE["lesson"])]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        context = await browser.new_context(viewport=None)
        page    = await context.new_page()

        # ── Ask about login ───────────────────────────────────────────────────
        await handle_login(page, context)

        # ── Scrape pages one by one ───────────────────────────────────────────
        total     = len(pages_to_scrape)
        saved     = 0
        skipped   = 0
        failed    = 0
        print(f"Starting download of {total} page(s)...\n")

        for i, (chapter, lesson) in enumerate(pages_to_scrape, 1):
            url = build_url(chapter, lesson)
            out = build_output_path(chapter, lesson)

            if out.exists():
                skipped += 1
                print(f"[{i}/{total}] Skipped (already saved): {lesson}")
                continue

            print(f"[{i}/{total}] {chapter} / {lesson}")
            try:
                await page.goto(url)

                # ── Session expiry check ──────────────────────────────────────
                # If the site redirected us to login mid-scrape, pause for re-login.
                if "signin" in page.url or "login" in page.url:
                    print("\n  Session expired mid-scrape — please log in again.")
                    print("  (OTP will be sent to your email — complete login in the browser)")
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(
                        None, input,
                        "  >>> Press ENTER once you are logged in: "
                    )
                    await save_session(context)
                    print("  Session refreshed — continuing...\n")
                    await page.goto(url)

                print(f"       Waiting for content to load...")
                await wait_for_content(page)

                print(f"       Switching code blocks to Java...")
                await switch_all_code_blocks_to_java(page)

                print(f"       Saving...")
                await save_as_mhtml(page, out)
                saved += 1
                print(f"       Done → {out}\n")

            except Exception as e:
                failed += 1
                print(f"       Failed: {e}\n")

            # Human-like random delay between pages to avoid rate limiting
            if i < total:
                delay = random.uniform(DELAY_MIN, DELAY_MAX)
                print(f"       Waiting {delay:.1f}s before next page...")
                await asyncio.sleep(delay)

        print(f"\n{'='*50}")
        print(f"  Saved:   {saved}")
        print(f"  Skipped: {skipped} (already existed)")
        print(f"  Failed:  {failed}")
        print(f"  Total:   {total}")
        print(f"{'='*50}")
        print(f"\nFiles saved in: {OUTPUT_DIR.resolve()}")
        await browser.close()

    # Build/refresh the offline navigation index
    build_index()
    print(f"\nOpen this in Chrome to browse offline:\n  {(OUTPUT_DIR / 'index.html').resolve()}")


if __name__ == "__main__":
    asyncio.run(main())
