"""Search API with three modes, plus a side-by-side page (appendix A4).

Run: uvicorn app:app --reload   then open http://localhost:8000
"""
import os
from pathlib import Path
from typing import Literal

import psycopg
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).parent
DB_URL = os.environ.get("DB_URL", "postgresql://postgres:pw@localhost:5432/demo")
model = SentenceTransformer("all-MiniLM-L6-v2")
# One shared connection is fine for a demo; a real app would use psycopg_pool.
conn = psycopg.connect(DB_URL, autocommit=True)
register_vector(conn)
app = FastAPI()

KEYWORD = """SELECT title FROM recipes, websearch_to_tsquery('english', %(q)s) tq
    WHERE tsv @@ tq ORDER BY ts_rank_cd(tsv, tq) DESC LIMIT 5"""
SEMANTIC = "SELECT title FROM recipes ORDER BY embedding <=> %(v)s LIMIT 5"
HYBRID = (HERE / "hybrid.sql").read_text()
QUERIES = {"keyword": KEYWORD, "semantic": SEMANTIC, "hybrid": HYBRID}


@app.get("/search")
def search(q: str, mode: Literal["keyword", "semantic", "hybrid"] = "hybrid") -> list[str]:
    v = model.encode(q, normalize_embeddings=True)  # embed only the query, live
    return [row[0] for row in conn.execute(QUERIES[mode], {"q": q, "v": v})]


@app.get("/")
def page() -> FileResponse:
    return FileResponse(HERE / "index.html")
