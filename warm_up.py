"""Run once before class, with internet: downloads the model into ./models and
checks that it gives 384 numbers. After this the demo works offline.
"""
from embedder import embed

v = embed(["a quick dinner without meat"])[0]
print(f"Model ready: {v.shape[0]} numbers, length {float((v**2).sum()) ** 0.5:.3f}")
