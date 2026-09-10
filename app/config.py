"""
Central config so every module agrees on model names, paths, and chunk sizing.
Change values here rather than hunting through each file.
"""

from pathlib import Path

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "data" if (PROJECT_ROOT / "data").exists() else Path(__file__).resolve().parent / "data"
CHROMA_PERSIST_DIR = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "homework_docs"

# --- Ollama models ---
EMBEDDING_MODEL = "nomic-embed-text"
GENERATION_MODEL = "llama3.2"

# --- Chunking ---
# Fixed-size chunking with overlap. Simple, deterministic, and good enough
# for a baseline (Naive) RAG system. See README for why this was chosen
# over sentence- or paragraph-based splitting.
CHUNK_SIZE = 500       # characters per chunk
CHUNK_OVERLAP = 75     # characters shared between consecutive chunks

# --- Retrieval ---
TOP_K = 3

# --- Generation ---
# If the best match isn't close enough, we tell the user instead of
# guessing. Distance is Chroma's default (cosine-ish squared L2 depending
# on backend); this threshold was tuned by eyeballing distances on the
# sample docs in demo_vector_check.py — adjust for your own documents.
MAX_RELEVANT_DISTANCE = 1.1
