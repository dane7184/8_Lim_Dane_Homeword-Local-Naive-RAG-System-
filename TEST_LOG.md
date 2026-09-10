# Test Log

Run against the sample documents in `data/` (`company_handbook.md`,
`onboarding_guide.md`, `product_faq.md`).

Fill in the `Answer` and exact `Retrieved chunks` for each question after
running `poetry run python main.py` with `SHOW_RETRIEVED_CHUNKS = True`
(already the default) on your machine with Ollama running.

---

### Question 1 (on-topic)
**Q:** How many vacation days do employees get in their first three years?

**Retrieved chunks:**
- [company_handbook.md] distance=___ — "...accrue 15 vacation days per year during their first three years..."
- [company_handbook.md] distance=___ — (overlapping/adjacent chunk)
- [___] distance=___

**Answer:** _(paste generated answer here)_

---

### Question 2 (on-topic)
**Q:** What is the battery life of the RoboMower X1?

**Retrieved chunks:**
- [product_faq.md] distance=___ — "...Battery life is rated at 90 minutes per charge..."
- [___] distance=___
- [___] distance=___

**Answer:** _(paste generated answer here)_

---

### Question 3 (on-topic)
**Q:** Who is my onboarding buddy and how long does the buddy program last?

**Retrieved chunks:**
- [onboarding_guide.md] distance=___ — "...Buddy pairings last for your first 90 days..."
- [___] distance=___
- [___] distance=___

**Answer:** _(paste generated answer here)_

---

### Question 4 (on-topic, tests boundary handling)
**Q:** Does the RoboMower X1's warranty cover accidental damage from driving into a pool?

**Retrieved chunks:**
- [product_faq.md] distance=___ — "...Accidental damage...is not covered under the standard warranty..."
- [___] distance=___
- [___] distance=___

**Answer:** _(paste generated answer here)_

---

### Question 5 (OFF-topic — not in any document)
**Q:** What is the CEO's favorite programming language?

**Retrieved chunks:**
- [___] distance=___ (expected: high distance, above `MAX_RELEVANT_DISTANCE`)
- [___] distance=___
- [___] distance=___

**Answer:** _(expected: "I could not find this in your documents." — confirm
this actually happened, and note the distance value that triggered it)_

---

## Notes While Testing

- Record the actual distance values you see for Question 5 vs. the
  on-topic questions. If they're closer together than expected, you may
  need to adjust `MAX_RELEVANT_DISTANCE` in `app/config.py`.
- If an on-topic question gets a wrong or incomplete answer, check whether
  the *retrieval* step pulled the right chunk (retrieval problem) or the
  right chunk was retrieved but the model ignored it (generation problem)
  — these need different fixes.
