"""Run once before class, with internet: downloads the model into the local
Hugging Face cache and checks that it gives 384 numbers. After this the demo
works offline (set HF_HUB_OFFLINE=1 to make sure it never touches the network).
"""
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
v = model.encode("a quick dinner without meat", normalize_embeddings=True)
print(f"Model ready: {v.shape[0]} numbers, length {float((v**2).sum()) ** 0.5:.3f}")
