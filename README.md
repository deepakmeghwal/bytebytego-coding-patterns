# ByteByteGo — Coding Interview Patterns (Offline)

An offline study tool for all 120 lessons from ByteByteGo's **Coding Interview Patterns** course.

🌐 **Live Site:** [deepakmeghwal.github.io/bytebytego-coding-patterns/coding-patterns](https://deepakmeghwal.github.io/bytebytego-coding-patterns/coding-patterns/)

---

## What's Inside

- **19 chapters** covering core DSA patterns
- **120 lessons** — fully saved offline
- **Java code** pre-selected in all code blocks
- Clean sidebar navigator matching ByteByteGo's design
- Works in any browser, no login required

## Chapters

| # | Chapter | Lessons |
|---|---------|---------|
| 01 | Two Pointers | 7 |
| 02 | Hash Maps and Sets | 6 |
| 03 | Linked Lists | 7 |
| 04 | Fast and Slow Pointers | 4 |
| 05 | Sliding Windows | 4 |
| 06 | Binary Search | 9 |
| 07 | Stacks | 7 |
| 08 | Heaps | 5 |
| 09 | Intervals | 4 |
| 10 | Prefix Sums | 4 |
| 11 | Trees | 13 |
| 12 | Tries | 4 |
| 13 | Graphs | 11 |
| 14 | Backtracking | 6 |
| 15 | Dynamic Programming | 10 |
| 16 | Greedy | 4 |
| 17 | Sort and Search | 5 |
| 18 | Bit Manipulation | 4 |
| 19 | Math and Geometry | 6 |

---

## Files

| File | Purpose |
|------|---------|
| `scraper.py` | Playwright script to download all lesson pages |
| `convert.py` | Converts MHTML snapshots to self-contained HTML |
| `coding-patterns/index.html` | Offline navigator UI |
| `coding-patterns/**/*.html` | 120 lesson pages |
| `requirements.txt` | Python dependencies |

## How to Re-download (if needed)

```bash
# Install dependencies
pip3 install -r requirements.txt
playwright install chromium

# Run scraper (opens browser for manual login)
python3 scraper.py

# Convert saved MHTML files to HTML
python3 convert.py

# Push updates
git add coding-patterns/
git commit -m "Update lesson pages"
git push
```

---

*Personal study reference — content belongs to [ByteByteGo](https://bytebytego.com).*
