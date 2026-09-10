"""
Stage 4: Vector store.

Uses ChromaDB in persistent mode (writes to disk under CHROMA_PERSIST_DIR),
so the offline pipeline (build once) and online pipeline (query many times)
can be run as separate processes without re-embedding everything each time.

Note: we call our own embeddings.py explicitly rather than handing Chroma
an embedding_function, so the exact same embedding path is used whether
we're indexing or querying — one less place for a subtle mismatch to hide.
"""

import chromadb

from chunking import Chunk
from config import CHROMA_PERSIST_DIR, COLLECTION_NAME
from embeddings import embed_batch, embed_text


def get_collection():
    """Open (or create) the persistent Chroma collection."""
    client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def index_chunks(chunks: list[Chunk]) -> None:
    """Embed every chunk and upsert it into the vector store."""
    if not chunks:
        print("No chunks to index.")
        return

    collection = get_collection()
    texts = [c.text for c in chunks]
    vectors = embed_batch(texts)

    collection.upsert(
        ids=[c.chunk_id for c in chunks],
        embeddings=vectors,
        documents=texts,
        metadatas=[{"doc_id": c.doc_id, "source": c.source} for c in chunks],
    )
    print(f"Indexed {len(chunks)} chunk(s) into '{COLLECTION_NAME}'.")


def search(query: str, top_k: int = 3) -> list[dict]:
    """
    Embed a query and return the top_k most similar chunks as a list of
    dicts: {id, text, source, distance}. Lower distance = more similar.
    """
    collection = get_collection()
    query_vector = embed_text(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
    )

    hits = []
    for i in range(len(results["ids"][0])):
        hits.append(
            {
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "distance": results["distances"][0][i],
            }
        )
    return hits


def reset_collection() -> None:
    """Delete and recreate the collection. Handy when re-running ingestion."""
    client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))
    client.delete_collection(name=COLLECTION_NAME)
    print(f"Collection '{COLLECTION_NAME}' reset.")


if __name__ == "__main__":
    from chunking import chunk_documents
    from ingestion import load_documents

    docs = load_documents()
    chunks = chunk_documents(docs)
    index_chunks(chunks)

    hits = search("test query", top_k=3)
    for h in hits:
        print(h["id"], h["distance"])
