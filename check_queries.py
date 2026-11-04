"""Run before class (and after any change): prints the top results of every
mode for the queries you plan to show, so the slides match what really happens.

Run: python check_queries.py            (uses the default list below)
     python check_queries.py "your own query" "another one"
"""
import sys

from app import search

QUERIES = sys.argv[1:] or [
    "a quick dinner without meat",
    "dal bhat",
    "easy meatless meals",
    "Nepali food",
    "something sweet to bake",
]

for q in QUERIES:
    print(f"\n{q!r}")
    for mode in ("keyword", "semantic", "hybrid"):
        titles = search(q, mode)
        print(f"  {mode:<9}", " | ".join(titles) if titles else "(no results)")
