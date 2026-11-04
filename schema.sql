-- schema.sql: run once against the "demo" database (appendix A2)
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS recipes (
    id          bigserial PRIMARY KEY,
    title       text NOT NULL,
    description text NOT NULL,
    embedding   vector(384),  -- all-MiniLM-L6-v2 outputs 384 numbers
    tsv         tsvector GENERATED ALWAYS AS
                (to_tsvector('english', title || ' ' || description)) STORED
);

-- Cosine index: serves the <=> operator. With 30 rows Postgres will still
-- choose an exact scan; the index is here to show the real-world setup.
CREATE INDEX IF NOT EXISTS recipes_embedding_idx
    ON recipes USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS recipes_tsv_idx ON recipes USING gin (tsv);
