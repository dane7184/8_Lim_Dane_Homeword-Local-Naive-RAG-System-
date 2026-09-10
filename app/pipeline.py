"""
Connects the online pipeline into one entry point: question in, grounded
answer out. This is the single function main.py (or a future web API)
needs to call — it doesn't need to know retrieval and generation are
separate steps.
"""

from dataclasses import dataclass

from generator import generate_answer
from retriever import RetrievalResult, retrieve


@dataclass
class PipelineResult:
    question: str
    answer: str
    retrieval: RetrievalResult


def answer_question(question: str) -> PipelineResult:
    retrieval = retrieve(question)
    answer = generate_answer(question, retrieval)
    return PipelineResult(question=question, answer=answer, retrieval=retrieval)


if __name__ == "__main__":
    result = answer_question("What is the RoboMower X1's battery life?")
    print(f"Q: {result.question}")
    print(f"A: {result.answer}")
