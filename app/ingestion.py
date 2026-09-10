"""
Stage 1: Ingestion.

Job: read raw documents off disk and hand back plain text plus metadata.
Nothing in this file knows about chunking, embeddings, or vector stores —
keeping it dumb means you can swap in PDF/HTML loaders later without
touching the rest of the pipeline.
"""

from dataclasses import dataclass
from pathlib import Path

from config import DOCS_DIR

SUPPORTED_EXTENSIONS = {".txt", ".md"}


@dataclass
class Document:
    """One loaded source document."""
    doc_id: str          # stable id, derived from filename
    source: str          # filename, kept for citing answers later
    text: str            # full raw text of the document


def load_documents(docs_dir: Path = DOCS_DIR) -> list[Document]:
    """
    Read every supported file in docs_dir and return a list of Documents.
    Raises FileNotFoundError early if the folder is missing or empty —
    better to fail loudly here than get a confusing empty vector store later.
    """
    if not docs_dir.exists():
        raise FileNotFoundError(
            f"Documents folder not found: {docs_dir}. "
            f"Create it and add 3-5 .txt/.md files."
        )

    paths = sorted(
        p for p in docs_dir.iterdir()
        if p.suffix.lower() in SUPPORTED_EXTENSIONS and p.is_file()
    )

    if not paths:
        raise FileNotFoundError(
            f"No .txt or .md files found in {docs_dir}. "
            f"Add some documents before running the pipeline."
        )

    documents = []
    for path in paths:
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            # Skip empty files rather than embedding nothing.
            continue
        documents.append(
            Document(doc_id=path.stem, source=path.name, text=text)
        )

    return documents


if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} document(s):")
    for d in docs:
        print(f"  - {d.source} ({len(d.text)} chars)")
