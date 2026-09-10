# Chat with Documents — Naive RAG Baseline

A local, terminal-based Retrieval-Augmented Generation app. It reads a small
folder of documents, chunks and embeds them, stores the vectors in ChromaDB,
and answers questions grounded in that content using a local LLM via Ollama.

## How to Run It

1. **Install and start Ollama**, then pull the two models this project uses:
   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```

2. **Install dependencies** (from the project folder):
   ```bash
   poetry install
   ```

3. **Add your documents.** Drop 3–5 `.txt` or `.md` files into `data/`.
   Three sample documents are already included (`company_handbook.md`,
   `onboarding_guide.md`, `product_faq.md`) — swap in your own or add more.

4. **(Optional) Sanity-check the vector store first**, per the assignment:
   ```bash
   poetry run python demo_vector_check.py "How to Configure Email Settings?"
   ```
   This builds the index on first run and prints the top 3 matching chunks
   so you can confirm retrieval looks reasonable before wiring up the LLM.

5. **Run the chat app:**
   ```bash
   poetry run python main.py
   ```
   Ask questions, type `exit` to quit. The first run builds the index
   automatically; later runs reuse the persisted ChromaDB store in
   `chroma_db/`.

   If you change the documents in `data/`, delete `chroma_db/` (or call
   `vector_store.reset_collection()`) so the index gets rebuilt with the
   updated content.

## Project Structure

| File | Job |
|---|---|
| `app/config.py` | Central constants: model names, chunk size, paths |
| `app/ingestion.py` | Loads raw `.txt`/`.md` files from `data/` |
| `app/chunking.py` | Splits documents into overlapping chunks |
| `app/embeddings.py` | Wraps Ollama's embedding model |
| `app/vector_store.py` | Persists/searches vectors in ChromaDB |
| `app/demo_vector_check.py` | Standalone script to test retrieval before building the chat app |
| `app/retriever.py` | Embeds a question, returns top-k chunks, flags relevance |
| `app/generator.py` | Builds a grounded prompt, calls the local LLM |
| `app/pipeline.py` | Connects retriever + generator into one function |
| `app/main.py` | Terminal chat loop |

## Chunking Strategy: Fixed-Size with Overlap (and boundary snapping)

I used **fixed-size character chunking with overlap** (500 characters per
chunk, 75-character overlap), with a small tweak: instead of cutting at a
hard character count, the splitter looks backward from that cutoff for the
nearest paragraph break (`\n\n`) or sentence end (`. `) and splits there
instead. This avoids the classic failure mode of naive fixed-size chunking
— slicing a sentence in half so neither resulting chunk reads cleanly or
embeds well.

**Why this over alternatives:**
- *Pure fixed-size (no boundary snapping)* is simpler but produces chunks
  that sometimes start or end mid-sentence, which hurts embedding quality
  because the embedding model is encoding a sentence fragment instead of a
  complete thought.
- *Paragraph-based chunking* would have worked well for these documents
  since they're already organized into short sections (e.g. "## Vacation
  Policy"), but it doesn't generalize to unstructured text without
  paragraph breaks, and paragraph sizes can vary wildly in length.
- *Semantic/recursive chunking* (splitting on structural markers first,
  falling back to smaller units) is generally the better choice for
  production systems, but it's more code than needed for a baseline, and
  the assignment goal here is to understand the naive version first.

The overlap (75 chars, ~15% of chunk size) exists so that a fact mentioned
right at a chunk boundary still shows up with surrounding context in at
least one chunk, rather than being split awkwardly between two chunks with
neither having full context.

## Embedding Model & Vector Database

- **Embedding model:** `nomic-embed-text` via Ollama — a solid, fast local
  embedding model with a reasonable context window for chunk-sized text.
- **Vector database:** ChromaDB in **persistent mode** (`PersistentClient`),
  storing to `./chroma_db/`. Chosen because it requires no separate server
  or Docker container — it's a Python-native, file-backed store, which
  keeps the whole project runnable with just `poetry install` and Ollama.
  Distance metric is cosine similarity (`hnsw:space: cosine`), which is the
  standard choice for comparing normalized text embeddings.
- **Generation model:** `llama3.2` via Ollama.


## Test Log

See `TEST_LOG.md` for the 5 required test questions, retrieved chunks, and
generated answers (run against the sample `data/` documents included here).

## Reflection

See `REFLECTION.md`.
