"""Embed every recipe once and store it in Postgres (appendix A3).

Run: python load.py   (or: uv run load.py)
"""
import csv
import os

import psycopg
from pgvector.psycopg import register_vector

from embedder import embed

DB_URL = os.environ.get("DB_URL", "postgresql://postgres:pw@localhost:5432/demo")

with open("recipes.csv", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

# Title and description together, so both contribute to the meaning.
texts = [f"{r['title']}. {r['description']}" for r in rows]
vectors = embed(texts)  # shape (30, 384)

with psycopg.connect(DB_URL) as conn:
    register_vector(conn)
    # Start from an empty table so running this twice never duplicates rows.
    conn.execute("TRUNCATE recipes RESTART IDENTITY")
    for r, v in zip(rows, vectors):
        conn.execute(
            "INSERT INTO recipes (title, description, embedding) VALUES (%s, %s, %s)",
            (r["title"], r["description"], v),
        )

print(f"Loaded {len(rows)} recipes, {vectors.shape[1]} numbers each.")
