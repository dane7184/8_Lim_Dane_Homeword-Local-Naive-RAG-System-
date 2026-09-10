"""
Stage 5 (online pipeline, part 1): Retriever.

Job: given a raw user question, embed it and pull back the top-k most
relevant chunks from the vector store. Also flags whether the best match
is actually relevant, so the generator can say "not in your documents"
instead of hallucinating an answer from the model's own memory.
"""

from dataclasses import dataclass

from config import MAX_RELEVANT_DISTANCE, TOP_K
from vector_store import search


@dataclass
class RetrievalResult:
    chunks: list[dict]     # each: {id, text, source, distance}
    is_relevant: bool      # False if even the best match is too far off


def retrieve(question: str, top_k: int = TOP_K) -> RetrievalResult:
    hits = search(question, top_k=top_k)

    is_relevant = bool(hits) and hits[0]["distance"] <= MAX_RELEVANT_DISTANCE

    return RetrievalResult(chunks=hits, is_relevant=is_relevant)


if __name__ == "__main__":
    result = retrieve("How long is the warranty on the RoboMower X1?")
    print(f"Relevant: {result.is_relevant}")
    for c in result.chunks:
        print(f"- [{c['source']}] distance={c['distance']:.4f}")
