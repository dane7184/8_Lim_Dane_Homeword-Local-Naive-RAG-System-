# Project Documentation: Local Naive RAG System

## 1. Overview
This project is a local, terminal-based **Retrieval-Augmented Generation (RAG)** application. It indexes text documents into a vector database (ChromaDB) and answers user questions grounded strictly in the provided content using local models served by **Ollama**.

---

## 2. Architecture & Pipeline Overview

The project consists of two distinct workflows:

```
+---------------------------------------------------------------+
|                       OFFLINE PIPELINE                        |
|                                                               |
|  [ data/*.txt, *.md ]                                         |
|         │                                                     |
|         ▼                                                     |
|  1. Ingestion (ingestion.py)                                  |
|         │                                                     |
|         ▼                                                     |
|  2. Chunking (chunking.py)                                    |
|     (500 chars, 75 overlap, boundary snapping)                |
|         │                                                     |
|         ▼                                                     |
|  3. Embeddings (embeddings.py)                                |
|     (Ollama: nomic-embed-text)                                |
|         │                                                     |
|         ▼                                                     |
|  4. Vector Store (vector_store.py)                            |
|     (ChromaDB Persistent Store in chroma_db/)                 |
+---------------------------------------------------------------+

+---------------------------------------------------------------+
|                        ONLINE PIPELINE                        |
|                                                               |
|  User Question                                                |
|         │                                                     |
|         ▼                                                     |
|  5. Retriever (retriever.py)                                  |
|     - Embed query (nomic-embed-text)                          |
|     - ChromaDB cosine similarity search (Top-3)               |
|     - Check threshold (distance <= MAX_RELEVANT_DISTANCE)     |
|         │                                                     |
|         ├───────────────────────────────┐                     |
|         ▼ (Relevant)                    ▼ (Not Relevant)      |
|  6. Generator (generator.py)     Return canned response:      |
|     - Format context prompt      "I could not find this in    |
|     - Instruct LLM (llama3.2)     your documents."            |
|     - Require source citations                                |
|         │                                                     |
|         ▼                                                     |
|  Grounded Assistant Answer                                    |
+---------------------------------------------------------------+
```

---

## 3. Step-by-Step Component Details

### Step 1: Configuration (`app/config.py`)
Central source of truth for all parameters:
- **Paths**: Locates the raw document folder (`data/`) and persistent database (`chroma_db/`).
- **Models**: Specifies `nomic-embed-text` for vector generation and `llama3.2` for response generation.
- **Chunk Parameters**: 
  - `CHUNK_SIZE = 500`: Character length per chunk.
  - `CHUNK_OVERLAP = 75`: Characters shared between consecutive chunks.
- **Retrieval Threshold**:
  - `TOP_K = 3`: Number of candidate chunks retrieved.
  - `MAX_RELEVANT_DISTANCE = 1.1`: Maximum cosine distance allowed before flagging a query as out-of-scope.

### Step 2: Ingestion (`app/ingestion.py`)
- Scans `data/` for supported document formats (`.txt`, `.md`).
- Reads raw text with UTF-8 encoding.
- Encapsulates documents into `Document` objects with metadata (`doc_id`, `source`, `text`).
- Validates the existence of documents to prevent indexing empty directories.

### Step 3: Chunking & Boundary Snapping (`app/chunking.py`)
- Splits long documents into manageable chunks for embeddings and LLM context windows.
- **Boundary Snapping**: Avoids splitting mid-sentence or mid-word. When scanning a window, it looks backward for paragraph breaks (`\n\n`) or sentence endings (`. `) to snap cleanly to natural textual boundaries.
- **Forward-Progress Guarantee**: Snapping requires `boundary > start + overlap`, ensuring every step advances strictly forward and preventing infinite loops.

### Step 4: Vector Embeddings (`app/embeddings.py`)
- Interfaces with Ollama's `/api/embed` endpoint using `nomic-embed-text`.
- Generates 768-dimensional semantic vector embeddings.
- Supports both single text embedding (`embed_text`) for user queries and batch embedding (`embed_batch`) for bulk indexing.

### Step 5: Vector Store (`app/vector_store.py`)
- Backed by **ChromaDB** using `PersistentClient` targeting `./chroma_db/`.
- Configured with cosine distance metric (`{"hnsw:space": "cosine"}`).
- Stores embeddings, raw text, and document metadata (source filename and chunk ID).
- Allows separate execution of the indexing phase and query phase without re-computing embeddings.

### Step 6: Retrieval & Guardrail Filtering (`app/retriever.py`)
- Embeds incoming user queries and queries ChromaDB for the closest `TOP_K` matching chunks.
- Computes cosine distance for each match.
- Evaluates `is_relevant`: If the closest chunk's distance exceeds `MAX_RELEVANT_DISTANCE`, retrieval is marked irrelevant, preventing LLM hallucinations.

### Step 7: Grounded Answer Generation (`app/generator.py`)
- Implements strict RAG prompt engineering:
  - System prompt instructs the model to answer **ONLY** using provided context.
  - Mandates explicit citations of source documents (e.g., `[Source: filename.txt]`).
  - Forbids guessing or outside world knowledge.
- If retrieval is flagged as irrelevant, short-circuits immediately with `"I could not find this in your documents."` without calling the LLM.

### Step 8: Execution & Chat Interface (`app/main.py`, `app/pipeline.py`)
- Orchestrates the full query pipeline via `answer_question()`.
- Checks on boot whether the vector index exists; if empty, builds it automatically.
- Provides an interactive CLI loop displaying the user query, retrieved chunks with cosine distances, and the grounded assistant response.

---

## 4. How to Run the Project

### Prerequisites
Ensure Ollama is running and both models are downloaded:
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### Install Dependencies
```bash
poetry install
```

### Run Sanity Check (Vector Retrieval Test)
```bash
poetry run python demo_vector_check.py "How to configure email settings?"
```

### Start Interactive Chat
```bash
poetry run python main.py
```
Type your query, or type `exit` to quit.
