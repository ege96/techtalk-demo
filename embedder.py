"""The embedding model, shared by load.py, app.py and warm_up.py.

FastEmbed runs all-MiniLM-L6-v2 on ONNX Runtime, so there is no PyTorch to
install. The model (about 90 MB) is downloaded once into ./models and reused,
so after the first run everything works offline.
"""
import numpy as np
from fastembed import TextEmbedding

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # 384 dimensions
model = TextEmbedding(MODEL_NAME, cache_dir="models")


def embed(texts: list[str]) -> np.ndarray:
    """One row per text, each scaled to length 1 (so cosine = inner product)."""
    vectors = np.array(list(model.embed(texts)), dtype=np.float32)
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
