"""
Chat interface. Run with:  poetry run python main.py

On first run (empty vector store), this builds the offline pipeline
(ingest -> chunk -> embed -> store) automatically, then drops you into a
question loop. Type 'exit' to quit.
"""

from chunking import chunk_documents
from ingestion import load_documents
from pipeline import answer_question
from vector_store import get_collection, index_chunks

SHOW_RETRIEVED_CHUNKS = True  # bonus challenge: show sources before the answer


def ensure_index_built():
    collection = get_collection()
    if collection.count() == 0:
        print("No index found — building it from data/ ...")
        docs = load_documents()
        chunks = chunk_documents(docs)
        index_chunks(chunks)
        print()


def print_retrieved_chunks(retrieval):
    if not retrieval.chunks:
        return
    print("  Retrieved chunks:")
    for c in retrieval.chunks:
        preview = c["text"][:80].replace("\n", " ")
        print(f"    - [{c['source']}] (distance={c['distance']:.3f}) {preview}...")
    print()


def main():
    print("=== Chat with Your Documents (Naive RAG) ===")
    ensure_index_built()
    print("Type a question, or 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        result = answer_question(question)

        if SHOW_RETRIEVED_CHUNKS:
            print_retrieved_chunks(result.retrieval)

        print(f"Assistant: {result.answer}\n")


if __name__ == "__main__":
    main()
