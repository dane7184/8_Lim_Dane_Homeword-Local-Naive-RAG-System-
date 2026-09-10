"""
Stage 3: Embeddings.

Job: turn text into vectors using a local embedding model served by Ollama.
Kept as a thin wrapper so the rest of the app doesn't care whether the
embedding call is local (Ollama) or remote (an API) — swap this file and
nothing else changes.
"""

import ollama

from config import EMBEDDING_MODEL


def embed_text(text: str, model: str = EMBEDDING_MODEL) -> list[float]:
    """Embed a single string. Used for both chunks and incoming queries."""
    response = ollama.embed(model=model, input=text)
    # ollama-python returns {"embeddings": [[...]]} for embed()
    return response["embeddings"][0]


def embed_batch(texts: list[str], model: str = EMBEDDING_MODEL) -> list[list[float]]:
    """
    Embed many strings at once. Ollama's embed() accepts a list directly,
    which is faster than looping one-by-one for larger document sets.
    """
    if not texts:
        return []
    response = ollama.embed(model=model, input=texts)
    return response["embeddings"]


if __name__ == "__main__":
    vec = embed_text("This is a test sentence for embedding.")
    print(f"Embedding length: {len(vec)}")
    print(f"First 5 values: {vec[:5]}")
