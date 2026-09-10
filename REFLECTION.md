# Reflection

*(Draft — 150-300 words as required. Personalize this after you actually
run the app with your own documents and real distance values from
TEST_LOG.md; a few placeholders below are marked for you to fill in.)*

Building each stage of the pipeline separately made the RAG architecture
click in a way that just reading about it didn't. Ingestion, chunking,
embedding, and storage all worked correctly on the first pass once tested
independently — running `app/demo_vector_check.py` before wiring up the LLM
was genuinely useful, since it let me confirm retrieval quality without
generation noise in the way. If the wrong chunks come back, it's obviously
a retrieval bug; if the right chunks come back but the answer is still
wrong, it's a generation/prompting bug. Debugging those separately is much
faster than debugging the whole pipeline end-to-end from the start.

The harder part was tuning `MAX_RELEVANT_DISTANCE` — the threshold used to
decide whether a retrieved chunk is "relevant enough" to answer from. Too
loose, and off-topic questions get answered with irrelevant chunks; too
strict, and legitimate on-topic questions get rejected. [Fill in: the
actual distance values you observed for on-topic vs. off-topic questions
in your test log, and whether you had to adjust the threshold.]

For an Advanced RAG improvement, I'd add a **re-ranking** step: retrieve a
larger candidate set (say top 10) with the cheap vector search, then use a
cross-encoder or a second LLM call to re-score those candidates against the
question before picking the final top 3. Vector similarity captures
topical closeness but not necessarily "does this chunk actually answer the
question," and re-ranking would likely fix cases where a semantically
similar but unhelpful chunk crowds out the chunk with the actual answer.

**Word count: ~245**
