# The Unofficial Guide

<!-- Hieu Quach - Campus Life -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This project uses the `campus_life` corpus, a collection of campus information
about courses, housing, dining, academic policies, study spaces, and
transportation. It is a retrieval-augmented generation (RAG) system: it finds
relevant documents first, then uses those documents as evidence for its answer.
The system can answer specific questions such as how many exams a course has,
when dining dollars expire, how housing laundry payment methods differ, and
walking times between campus locations. Each answer includes the source
document so users can verify where the information came from.

## Chunking Strategy

**Chunk size: Varies based on paragraph length**
**Overlap: None**

I first examined the fallback splitter with an 800-character chunk size and
120-character overlap. It kept many campus-life documents in one chunk because
the documents are short. For example, a single housing chunk could contain
room layout, building condition, laundry costs, and noise information together.
Although that preserves context, it gives retrieval more unrelated information
than a focused question needs.

I chose paragraph-based chunks instead because each paragraph in this corpus
usually communicates one distinct idea: workload, exams, laundry, noise,
walking time, or a practical recommendation. This creates smaller, more
specific chunks without cutting through sentences.

I do not use character overlap. Repeating nearby text would create near-duplicate
chunks even when the preceding or following paragraph concerns a different
topic. Instead, I repeat the document title in every paragraph chunk. The title
keeps the course, residence hall, dining location, or service name available as
context, while the paragraph supplies the focused answer.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_340_exams.txt` — produced by: `chunker.py::split_documents`

```
CS 340 Databases — assessment

Start the term project in week three, not week eight; everyone learns this the hard way.
```

**Chunk 3** — source: `course_phys_130_workload.txt` — produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.
```

**Chunk 4** — source: `dining_verrill_street_grill_followup.txt` — produced by: `chunker.py::split_documents`

```
Re: Verrill Street Grill

Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_morrow_house.txt` — produced by: `chunker.py::split_documents`

```
Morrow House — what it's actually like

The good: cheapest housing tier by about $900 a year, and the singles are real singles.
```

## Sample Answer

**Question: How do laundry payment methods differ between Aldridge Hall and Calder Annexe?**

**Answer:**

```
(best distance 0.426, cutoff 0.55)

In Calder Annexe, laundry is app-based (from `housing_calder_annexe.txt` and `housing_calder_annexe_laundry.txt`), whereas in Aldridge Hall, laundry is card only (from `housing_aldridge_hall_laundry.txt`).

Sources retrieved: housing_aldridge_hall_laundry.txt, housing_calder_annexe.txt, housing_calder_annexe_laundry.txt
```

**My relevance cutoff: 0.5**

I set `TOP_K` to 4. With the original value of 5, questions about a specific
course sometimes retrieved documents about other courses in the same subject
area, even when those documents did not answer the question. Four results still
allow comparison questions about two residence halls or dining locations to
retrieve supporting evidence for both places, while reducing unrelated results.

I set the relevance cutoff to `0.55`. In my tests, in-corpus questions had
best-match distances roughly between 0.20 and 0.50, so a lower distance
indicated a closer semantic match. A cutoff of 0.55 is stricter than 0.60 and
should reject questions whose closest retrieved document is too unrelated to
support an evidence-based answer. I recorded the exact best distances for all
five in-corpus and five out-of-scope questions in the table below.

| Question | In corpus? | Best distance |
|---|---|---|
| How many exams are there for the CS 210 course? | Yes | 0.381 |
| How do laundry payment methods differ between Aldridge Hall and Calder Annexe? | Yes | 0.426 |
| When do unused dining dollars expire? | Yes | 0.367 |
| Until when can I drop a course without receiving a W on my transcript? | Yes | 0.212 |
| How long does it take to walk from Aldridge Hall to the science quad? | Yes | 0.270 |
| What is the capital of Mongolia? | No | 0.787 |
| How do I change the oil in a diesel engine? | No | 0.923 |
| Who won the 1994 World Cup? | No | 0.847 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.849 |
| How do I write a for loop in Rust? | No | 0.860 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1. I prompted the Codex to help me write the chunking function using my strategies and then I asked it to double check if the chunks using the strategy is informative enough to answer any question like the instruction suggested it said no so I told it to update the strategy to include the title to give the chunk more information.**

**2. I asked AI to help me check if all of the pairs of sample questions and expected answers are good questions for test the RAG system because testing purpose is very important to make sure that the project is implemented in a proper way.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
