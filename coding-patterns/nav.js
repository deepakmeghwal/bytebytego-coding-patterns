/**
 * nav.js — Dynamic sidebar for ByteByteGo offline study site
 * Injected into every lesson page. Replaces the static ByteByteGo
 * <aside> with a fully linked, collapsible sidebar.
 */
(function () {

  const CHAPTERS = [
    {num:"01", title:"Two Pointers", slug:"two-pointers", lessons:[
      {slug:"introduction-to-two-pointers",            title:"Introduction to Two Pointers"},
      {slug:"pair-sum-sorted",                         title:"Pair Sum - Sorted"},
      {slug:"triplet-sum",                             title:"Triplet Sum"},
      {slug:"is-palindrome-valid",                     title:"Is Palindrome Valid"},
      {slug:"largest-container",                       title:"Largest Container"},
      {slug:"shift-zeros-to-the-end",                  title:"Shift Zeros to the End"},
      {slug:"next-lexicographical-sequence",           title:"Next Lexicographical Sequence"},
    ]},
    {num:"02", title:"Hash Maps and Sets", slug:"hash-maps-and-sets", lessons:[
      {slug:"introduction-to-hash-maps-and-sets",      title:"Introduction to Hash Maps and Sets"},
      {slug:"pair-sum-unsorted",                       title:"Pair Sum - Unsorted"},
      {slug:"verify-sudoku-board",                     title:"Verify Sudoku Board"},
      {slug:"zero-striping",                           title:"Zero Striping"},
      {slug:"longest-chain-of-consecutive-numbers",    title:"Longest Chain of Consecutive Numbers"},
      {slug:"geometric-sequence-triplets",             title:"Geometric Sequence Triplets"},
    ]},
    {num:"03", title:"Linked Lists", slug:"linked-lists", lessons:[
      {slug:"introduction-to-linked-lists",            title:"Introduction to Linked Lists"},
      {slug:"linked-list-reversal",                    title:"Linked List Reversal"},
      {slug:"remove-the-kth-last-node-from-a-linked-list", title:"Remove the Kth Last Node From a Linked List"},
      {slug:"linked-list-intersection",                title:"Linked List Intersection"},
      {slug:"lru-cache",                               title:"LRU Cache"},
      {slug:"palindromic-linked-list",                 title:"Palindromic Linked List"},
      {slug:"flatten-a-multi-level-linked-list",       title:"Flatten a Multi-Level Linked List"},
    ]},
    {num:"04", title:"Fast and Slow Pointers", slug:"fast-and-slow-pointers", lessons:[
      {slug:"introduction-to-fast-and-slow-pointers",  title:"Introduction to Fast and Slow Pointers"},
      {slug:"linked-list-loop",                        title:"Linked List Loop"},
      {slug:"linked-list-midpoint",                    title:"Linked List Midpoint"},
      {slug:"happy-number",                            title:"Happy Number"},
    ]},
    {num:"05", title:"Sliding Windows", slug:"sliding-windows", lessons:[
      {slug:"introduction-to-sliding-windows",         title:"Introduction to Sliding Windows"},
      {slug:"substring-anagrams",                      title:"Substring Anagrams"},
      {slug:"longest-substring-with-unique-characters",title:"Longest Substring With Unique Characters"},
      {slug:"longest-uniform-substring-after-replacements", title:"Longest Uniform Substring After Replacements"},
    ]},
    {num:"06", title:"Binary Search", slug:"binary-search", lessons:[
      {slug:"introduction-to-binary-search",           title:"Introduction to Binary Search"},
      {slug:"find-the-insertion-index",                title:"Find the Insertion Index"},
      {slug:"first-and-last-occurrences-of-a-number",  title:"First and Last Occurrences of a Number"},
      {slug:"cutting-wood",                            title:"Cutting Wood"},
      {slug:"find-the-target-in-a-rotated-sorted-array",title:"Find the Target in a Rotated Sorted Array"},
      {slug:"find-the-median-from-two-sorted-arrays",  title:"Find the Median From Two Sorted Arrays"},
      {slug:"matrix-search",                           title:"Matrix Search"},
      {slug:"local-maxima-in-array",                   title:"Local Maxima in Array"},
      {slug:"weighted-random-selection",               title:"Weighted Random Selection"},
    ]},
    {num:"07", title:"Stacks", slug:"stacks", lessons:[
      {slug:"introduction-to-stacks",                  title:"Introduction to Stacks"},
      {slug:"valid-parenthesis-expression",            title:"Valid Parenthesis Expression"},
      {slug:"next-largest-number-to-the-right",        title:"Next Largest Number to the Right"},
      {slug:"evaluate-expression",                     title:"Evaluate Expression"},
      {slug:"repeated-removal-of-adjacent-duplicates", title:"Repeated Removal of Adjacent Duplicates"},
      {slug:"implement-a-queue-using-stacks",          title:"Implement a Queue using Stacks"},
      {slug:"maximums-of-sliding-window",              title:"Maximums of Sliding Window"},
    ]},
    {num:"08", title:"Heaps", slug:"heaps", lessons:[
      {slug:"introduction-to-heaps",                   title:"Introduction to Heaps"},
      {slug:"k-most-frequent-strings",                 title:"K Most Frequent Strings"},
      {slug:"combine-sorted-linked-lists",             title:"Combine Sorted Linked Lists"},
      {slug:"median-of-an-integer-stream",             title:"Median of an Integer Stream"},
      {slug:"sort-a-k-sorted-array",                   title:"Sort a K-Sorted Array"},
    ]},
    {num:"09", title:"Intervals", slug:"intervals", lessons:[
      {slug:"introduction-to-intervals",               title:"Introduction to Intervals"},
      {slug:"merge-overlapping-intervals",             title:"Merge Overlapping Intervals"},
      {slug:"identify-all-interval-overlaps",          title:"Identify All Interval Overlaps"},
      {slug:"largest-overlap-of-intervals",            title:"Largest Overlap of Intervals"},
    ]},
    {num:"10", title:"Prefix Sums", slug:"prefix-sums", lessons:[
      {slug:"introduction-to-prefix-sums",             title:"Introduction to Prefix Sums"},
      {slug:"sum-between-range",                       title:"Sum Between Range"},
      {slug:"k-sum-subarrays",                         title:"K-Sum Subarrays"},
      {slug:"product-array-without-current-element",   title:"Product Array Without Current Element"},
    ]},
    {num:"11", title:"Trees", slug:"trees", lessons:[
      {slug:"introduction-to-trees",                   title:"Introduction to Trees"},
      {slug:"invert-binary-tree",                      title:"Invert Binary Tree"},
      {slug:"balanced-binary-tree-validation",         title:"Balanced Binary Tree Validation"},
      {slug:"rightmost-nodes-of-a-binary-tree",        title:"Rightmost Nodes of a Binary Tree"},
      {slug:"widest-binary-tree-level",                title:"Widest Binary Tree Level"},
      {slug:"binary-search-tree-validation",           title:"Binary Search Tree Validation"},
      {slug:"lowest-common-ancestor",                  title:"Lowest Common Ancestor"},
      {slug:"build-binary-tree-from-preorder-and-inorder-traversals", title:"Build Binary Tree From Preorder and Inorder Traversals"},
      {slug:"maximum-sum-of-a-continuous-path-in-a-binary-tree", title:"Maximum Sum of a Continuous Path in a Binary Tree"},
      {slug:"binary-tree-symmetry",                    title:"Binary Tree Symmetry"},
      {slug:"binary-tree-columns",                     title:"Binary Tree Columns"},
      {slug:"kth-smallest-number-in-a-binary-search-tree", title:"Kth Smallest Number in a Binary Search Tree"},
      {slug:"serialize-and-deserialize-a-binary-tree", title:"Serialize and Deserialize a Binary Tree"},
    ]},
    {num:"12", title:"Tries", slug:"tries", lessons:[
      {slug:"introduction-to-tries",                   title:"Introduction to Tries"},
      {slug:"design-a-trie",                           title:"Design a Trie"},
      {slug:"insert-and-search-words-with-wildcards",  title:"Insert and Search Words with Wildcards"},
      {slug:"find-all-words-on-a-board",               title:"Find All Words on a Board"},
    ]},
    {num:"13", title:"Graphs", slug:"graphs", lessons:[
      {slug:"introduction-to-graphs",                  title:"Introduction to Graphs"},
      {slug:"graph-deep-copy",                         title:"Graph Deep Copy"},
      {slug:"count-islands",                           title:"Count Islands"},
      {slug:"matrix-infection",                        title:"Matrix Infection"},
      {slug:"bipartite-graph-validation",              title:"Bipartite Graph Validation"},
      {slug:"longest-increasing-path",                 title:"Longest Increasing Path"},
      {slug:"shortest-transformation-sequence",        title:"Shortest Transformation Sequence"},
      {slug:"merging-communities",                     title:"Merging Communities"},
      {slug:"prerequisites",                           title:"Prerequisites"},
      {slug:"shortest-path",                           title:"Shortest Path"},
      {slug:"connect-the-dots",                        title:"Connect the Dots"},
    ]},
    {num:"14", title:"Backtracking", slug:"backtracking", lessons:[
      {slug:"introduction-to-backtracking",            title:"Introduction to Backtracking"},
      {slug:"find-all-permutations",                   title:"Find All Permutations"},
      {slug:"find-all-subsets",                        title:"Find All Subsets"},
      {slug:"n-queens",                                title:"N Queens"},
      {slug:"combinations-of-a-sum",                   title:"Combinations of a Sum"},
      {slug:"phone-keypad-combinations",               title:"Phone Keypad Combinations"},
    ]},
    {num:"15", title:"Dynamic Programming", slug:"dynamic-programming", lessons:[
      {slug:"introduction-to-dynamic-programming",     title:"Introduction to Dynamic Programming"},
      {slug:"climbing-stairs",                         title:"Climbing Stairs"},
      {slug:"minimum-coin-combination",                title:"Minimum Coin Combination"},
      {slug:"matrix-pathways",                         title:"Matrix Pathways"},
      {slug:"neighborhood-burglary",                   title:"Neighborhood Burglary"},
      {slug:"longest-common-subsequence",              title:"Longest Common Subsequence"},
      {slug:"longest-palindrome-in-a-string",          title:"Longest Palindrome in a String"},
      {slug:"maximum-subarray-sum",                    title:"Maximum Subarray Sum"},
      {slug:"0-1-knapsack",                            title:"0/1 Knapsack"},
      {slug:"largest-square-in-a-matrix",              title:"Largest Square in a Matrix"},
    ]},
    {num:"16", title:"Greedy", slug:"greedy", lessons:[
      {slug:"introduction-to-greedy-algorithms",       title:"Introduction to Greedy Algorithms"},
      {slug:"jump-to-the-end",                         title:"Jump to the End"},
      {slug:"gas-stations",                            title:"Gas Stations"},
      {slug:"candies",                                 title:"Candies"},
    ]},
    {num:"17", title:"Sort and Search", slug:"sort-and-search", lessons:[
      {slug:"introduction-to-sort-and-search",         title:"Introduction to Sort and Search"},
      {slug:"sort-linked-list",                        title:"Sort Linked List"},
      {slug:"sort-array",                              title:"Sort Array"},
      {slug:"kth-largest-integer",                     title:"Kth Largest Integer"},
      {slug:"dutch-national-flag",                     title:"Dutch National Flag"},
    ]},
    {num:"18", title:"Bit Manipulation", slug:"bit-manipulation", lessons:[
      {slug:"introduction-to-bit-manipulation",        title:"Introduction to Bit Manipulation"},
      {slug:"hamming-weights-of-integers",             title:"Hamming Weights of Integers"},
      {slug:"lonely-integer",                          title:"Lonely Integer"},
      {slug:"swap-odd-and-even-bits",                  title:"Swap Odd and Even Bits"},
    ]},
    {num:"19", title:"Math and Geometry", slug:"math-and-geometry", lessons:[
      {slug:"introduction-to-math-and-geometry",       title:"Introduction to Math and Geometry"},
      {slug:"spiral-traversal",                        title:"Spiral Traversal"},
      {slug:"reverse-32-bit-integer",                  title:"Reverse 32-Bit Integer"},
      {slug:"maximum-collinear-points",                title:"Maximum Collinear Points"},
      {slug:"the-josephus-problem",                    title:"The Josephus Problem"},
      {slug:"triangle-numbers",                        title:"Triangle Numbers"},
    ]},
  ];

  // ── Determine current page from URL ────────────────────────────────────────
  const parts = window.location.pathname.replace(/\/$/, '').split('/');
  const currentLesson  = parts[parts.length - 1].replace('.html', '');
  const currentChapter = parts[parts.length - 2];

  // ── CSS ────────────────────────────────────────────────────────────────────
  const CSS = `
  .bbg-nav {
    display: flex !important;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
    background: rgb(62,62,62);
    color: rgba(255,255,255,0.9);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    box-sizing: border-box;
  }
  .bbg-nav *, .bbg-nav *::before, .bbg-nav *::after { box-sizing: border-box; }

  /* Hide the Ant Design ink-bar that ByteByteGo's React JS injects on click */
  .ant-menu-ink-bar { display: none !important; }

  .bbg-nav-head {
    padding: 16px 16px 12px;
    border-bottom: 1px solid rgb(45,45,45);
    flex-shrink: 0;
  }
  .bbg-nav-head h2 {
    font-size: 13px;
    font-weight: 700;
    color: rgba(255,255,255,0.9);
    margin: 0 0 10px;
    line-height: 1.4;
  }

  .bbg-nav-menu {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding-bottom: 20px;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.1) transparent;
  }
  .bbg-nav-menu::-webkit-scrollbar { width: 4px; }
  .bbg-nav-menu::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 4px; }

  .bbg-chapter { border-bottom: 1px solid rgba(255,255,255,0.04); }

  .bbg-chapter-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0 16px;
    height: 44px;
    cursor: pointer;
    user-select: none;
    transition: background .15s;
  }
  .bbg-chapter-header:hover { background: rgb(75,75,75); }

  .bbg-ch-num  { font-size: 11px; font-weight: 700; color: rgba(255,255,255,0.45); min-width: 20px; }
  .bbg-ch-title{ flex: 1; font-size: 13px; font-weight: 600; color: rgba(255,255,255,0.9); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .bbg-ch-count{ font-size: 11px; color: rgba(255,255,255,0.45); background: rgba(255,255,255,0.12); padding: 1px 6px; border-radius: 10px; }
  .bbg-ch-arrow{ font-size: 9px; color: rgba(255,255,255,0.45); transition: transform .2s; }
  .bbg-chapter.open .bbg-ch-arrow { transform: rotate(90deg); }

  .bbg-lesson-list { display: none; padding: 4px 0; background: rgb(50,50,50); }
  .bbg-chapter.open .bbg-lesson-list { display: block; }

  .bbg-lesson-list a {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 16px 0 44px;
    height: 38px;
    color: rgba(255,255,255,0.65);
    text-decoration: none;
    font-size: 13px;
    line-height: 1.35;
    transition: color .15s, background .15s;
  }
  .bbg-lesson-list a:hover { color: #fff; background: rgba(255,255,255,0.06); }
  .bbg-lesson-list a.active { color: #fff; background: rgba(255,255,255,0.12); }

  .bbg-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: rgba(255,255,255,0.25); flex-shrink: 0;
  }
  .bbg-lesson-list a:hover .bbg-dot  { background: rgba(255,255,255,0.6); }
  .bbg-lesson-list a.active .bbg-dot { background: #fff; }
  `;

  const styleEl = document.createElement('style');
  styleEl.textContent = CSS;
  document.head.appendChild(styleEl);

  // ── Build sidebar HTML ─────────────────────────────────────────────────────
  let html = '<div class="bbg-nav"><div class="bbg-nav-head"><h2>Coding Interview Patterns</h2></div><div class="bbg-nav-menu">';

  for (const ch of CHAPTERS) {
    const isCurrent = ch.slug === currentChapter;
    html += `<div class="bbg-chapter${isCurrent ? ' open' : ''}">`;
    html += `<div class="bbg-chapter-header" onclick="this.closest('.bbg-chapter').classList.toggle('open')">`;
    html += `<span class="bbg-ch-num">${ch.num}</span>`;
    html += `<span class="bbg-ch-title">${ch.title}</span>`;
    html += `<span class="bbg-ch-count">${ch.lessons.length}</span>`;
    html += `<span class="bbg-ch-arrow">▶</span>`;
    html += `</div><div class="bbg-lesson-list">`;

    for (const lesson of ch.lessons) {
      const isActive = lesson.slug === currentLesson && isCurrent;
      // All pages are one folder deep → ../chapter/lesson.html
      const href = `../${ch.slug}/${lesson.slug}.html`;
      html += `<a href="${href}"${isActive ? ' class="active"' : ''}>`;
      html += `<span class="bbg-dot"></span>${lesson.title}</a>`;
    }

    html += '</div></div>';
  }

  html += '</div></div>';

  // ── Inject into the existing <aside> ──────────────────────────────────────
  const aside = document.querySelector('aside.ant-layout-sider');
  if (aside) {
    aside.innerHTML = html;
    // Scroll active lesson into view
    setTimeout(() => {
      const active = aside.querySelector('a.active');
      if (active) active.scrollIntoView({ block: 'nearest' });
    }, 50);
  }

})();
