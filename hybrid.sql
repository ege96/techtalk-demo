-- Hybrid search with Reciprocal Rank Fusion (slide 13).
-- %(v)s = query embedding, %(q)s = query text (psycopg named parameters).
WITH semantic AS (
    SELECT id, RANK() OVER (ORDER BY embedding <=> %(v)s) AS rank
    FROM recipes
    ORDER BY embedding <=> %(v)s
    LIMIT 20
), keyword AS (
    SELECT id, RANK() OVER (ORDER BY ts_rank_cd(tsv, q) DESC) AS rank
    FROM recipes, websearch_to_tsquery('english', %(q)s) q
    WHERE tsv @@ q
    ORDER BY ts_rank_cd(tsv, q) DESC
    LIMIT 20
)
SELECT r.title,
       COALESCE(1.0 / (60 + s.rank), 0) +
       COALESCE(1.0 / (60 + k.rank), 0) AS score
FROM semantic s
FULL OUTER JOIN keyword k ON s.id = k.id
JOIN recipes r ON r.id = COALESCE(s.id, k.id)
ORDER BY score DESC
LIMIT 5;
