"""
Step 4 of the homework: a standalone script to verify the vector store
works BEFORE building the full chat app. Run this after running
vector_store.py once (or run it directly — it builds the index if empty).

Usage:
    poetry run python demo_vector_check.py "your test question"
"""

import sys

from chunking import chunk_documents
from ingestion import load_documents
from vector_store import get_collection, index_chunks, search


def ensure_indexed():
    """Build the index if the collection is currently empty."""
    collection = get_collection()
    if collection.count() == 0:
        print("Collection is empty — building index from data/ ...")
        docs = load_documents()
        chunks = chunk_documents(docs)
        index_chunks(chunks)
    else:
        print(f"Collection already has {collection.count()} chunk(s).")


def main():
    question = " ".join(sys.argv[1:]) or "What is the vacation policy?"
    ensure_indexed()

    print(f"\nQuery: {question}\n")
    hits = search(question, top_k=3)

    for rank, hit in enumerate(hits, start=1):
        print(f"--- Result {rank} (distance={hit['distance']:.4f}, source={hit['source']}) ---")
        print(hit["text"])
        print()


if __name__ == "__main__":
    main()
