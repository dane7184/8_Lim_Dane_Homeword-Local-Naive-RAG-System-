"""
Stage 2: Chunking.

Strategy: fixed-size character chunking with overlap, splitting on
paragraph/sentence boundaries where possible so we don't slice a sentence
in half. This is the simplest strategy from class and a reasonable default
for a baseline system — see README.md for the tradeoff discussion
(recursive/semantic chunking would likely do better on longer documents).
"""

from dataclasses import dataclass

from config import CHUNK_OVERLAP, CHUNK_SIZE
from ingestion import Document


@dataclass
class Chunk:
    """One chunk of text, traceable back to its source document."""
    chunk_id: str      # unique id: "<doc_id>-<index>"
    doc_id: str
    source: str
    text: str


def _split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Greedy fixed-size splitter with overlap. Tries to break on a paragraph
    or sentence boundary near the target size instead of mid-word, which
    keeps chunks semantically coherent without needing a heavier splitter.
    """
    if overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)

        # If we're not at the end of the text, try to back off to a
        # paragraph break, then a sentence break, so chunks read cleanly.
        if end < text_len:
            paragraph_break = text.rfind("\n\n", start, end)
            sentence_break = text.rfind(". ", start, end)
            boundary = max(paragraph_break, sentence_break)
            if boundary != -1 and boundary > start + overlap:
                end = boundary + (2 if boundary == paragraph_break else 1)

        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(chunk_text)

        if end >= text_len:
            break

        # Step forward, leaving `overlap` characters of context for the
        # next chunk so we don't lose meaning right at chunk boundaries.
        start = max(start + 1, end - overlap)

    return chunks


def chunk_documents(
    documents: list[Document],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[Chunk]:
    """Chunk every document, returning a flat list of Chunks."""
    all_chunks: list[Chunk] = []
    for doc in documents:
        pieces = _split_text(doc.text, chunk_size, overlap)
        for i, piece in enumerate(pieces):
            all_chunks.append(
                Chunk(
                    chunk_id=f"{doc.doc_id}-{i}",
                    doc_id=doc.doc_id,
                    source=doc.source,
                    text=piece,
                )
            )
    return all_chunks


if __name__ == "__main__":
    from ingestion import load_documents

    docs = load_documents()
    chunks = chunk_documents(docs)
    print(f"Produced {len(chunks)} chunk(s) from {len(docs)} document(s):\n")
    for c in chunks[:5]:
        print(f"[{c.chunk_id}] ({len(c.text)} chars)")
        print(c.text[:150].replace("\n", " ") + "...\n")
