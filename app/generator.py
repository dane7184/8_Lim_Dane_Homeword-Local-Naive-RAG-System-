"""
Stage 5 (online pipeline, part 2): Generator.

Job: build a grounded prompt from the question + retrieved chunks, send it
to the local LLM via Ollama, and return the answer. The system prompt
explicitly instructs the model to only use the provided context and to say
so when it can't answer — this is what makes it RAG rather than "an LLM
that happens to have some text nearby."
"""

import ollama

from config import GENERATION_MODEL
from retriever import RetrievalResult

SYSTEM_PROMPT = """You are a helpful assistant that answers questions using \
ONLY the context provided below. 

Rules:
- If the answer is fully or partially contained in the context, answer using it.
- Cite which source(s) you used, e.g. "(from onboarding_guide.md)".
- If the context does not contain the answer, say clearly: \
"I could not find this in your documents." Do not guess or use outside knowledge.
- Keep answers concise and directly responsive to the question."""


def _build_context_block(chunks: list[dict]) -> str:
    parts = []
    for c in chunks:
        parts.append(f"[Source: {c['source']}]\n{c['text']}")
    return "\n\n---\n\n".join(parts)


def generate_answer(question: str, retrieval: RetrievalResult) -> str:
    """
    Produce a grounded answer. Short-circuits with a fixed message if
    retrieval already flagged nothing relevant, so we never send the model
    a near-empty context and hope it does the right thing.
    """
    if not retrieval.is_relevant:
        return "I could not find this in your documents."

    context_block = _build_context_block(retrieval.chunks)
    user_prompt = f"Context:\n{context_block}\n\nQuestion: {question}"

    response = ollama.chat(
        model=GENERATION_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response["message"]["content"].strip()


if __name__ == "__main__":
    from retriever import retrieve

    question = "What is the vacation policy?"
    result = retrieve(question)
    answer = generate_answer(question, result)
    print(answer)
