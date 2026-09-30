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

From `results/run_2026-09-28_1432_before.md` — the run actually labeled
"before," from the day before `scorer.py` existed at all.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | unscored | unscored | unscored | N/A — not yet measurable |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Sampled chunks read as one complete, usable thought | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Every named source actually supports the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

Criterion 1 is "unscored," not a number, because that's the literal state of
the log: `scorer.py` didn't exist yet, so `run_eval.py` never got a judge to
call and left the Run columns blank rather than guessing. The file says so
itself: *"Judge each question yourself by reading the output below, or build
the scorer first and re-run."* Criteria 2 and 3 don't need a judge at
all — they're checked directly off the raw output below.

**Real output — criterion 4, a pass.** All 5 sample chunks from Unit 1 begin
with a title line and end on a complete sentence — none cut off mid-clause.
E.g. `admin_add_drop_deadline.txt`'s chunk ends "...students find out from
each other," a full thought, not "...students find out from" trailing into
the next paragraph.

**Real output — criterion 5, a pass.** Checked each question's cited source
file directly:

```
Q: How many exams are there for CS 210?             cites course_cs_210_exams.txt
   File says: "Two midterms and a final..."          → supports "three"

Q: When do dining dollars expire?                    cites admin_dining_dollars.txt
   File says: "Whatever is left in May disappears."   → supports "May"

Q: Drop deadline without a W?                         cites admin_add_drop_deadline.txt
   File says: "...a drop after week two shows as a W" → supports "end of week two"

Q: Walk time, Aldridge to science quad?               cites transit_walking.txt
   File says: "Aldridge Hall to the science quad: 4 minutes." → supports "4 minutes"

Q: Laundry, Aldridge vs. Calder Annexe?          cites both laundry files
   Aldridge file says: "...card only."  Calder Annexe file says: "...app-based."
                                                  → supports both halves
```

**Real output — criterion 1, unscored.** From `run_eval.py::main`, before
`scorer.py` existed:

```
Question: How do laundry payment methods differ between Aldridge Hall and Calder Annexe?
Answer:   In Aldridge Hall, laundry is card only, whereas in Calder Annexe, laundry is app-based.

Sources: `housing_aldridge_hall_laundry.txt` and `housing_calder_annexe_laundry.txt` (also found in `housing_calder_annexe.txt`).
```

Read by eye this looks right against `expects: "Aldridge is card only,
Calder Annexe is app-based"` — but "looks right to me, reading it once" is
exactly the judgment `scorer.py` exists to replace with something checkable
three times over. See Diagnoses below for what happened when I tried to
automate that check.

**Real output — criterion 2, a pass.** Every one of the 15 answers across
all 3 runs named its source file, e.g.:

```
It takes 4 minutes to walk from Aldridge Hall to the science quad.

Source: `transit_walking.txt` (and also mentioned in `housing_aldridge_hall.txt`).
```

## Verdicts

Verdicts below are against the Run Log — Before numbers.

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | N/A — not yet measurable | No scorer existed to check the 15 answers against their `expects` values, so there's no count to compare against the 4-of-5 target. Reading them myself, all 15 looked correct — but that impression is exactly what Milestone 2 asks you not to trust, since I can't re-check it the same way twice by eye. |
| 2 | Every answer names a source | MET | All 15 answers across all 3 runs named a source file; the target was 5 of 5 and every run hit exactly that. |
| 3 | Gate stops out-of-corpus questions | MET | 5 of 5 out-of-scope questions were refused, identically in every run since the gate is a deterministic distance comparison — comfortably past the 4-of-5 target. |
| 4 | Sampled chunks read as one complete, usable thought | MET | Read all 5 sample chunks from Unit 1 against the boundary test: each begins with a title line and ends on a complete sentence, none cut off mid-clause. 5 of 5, past the 4-of-5 target. |
| 5 | Every named source actually supports the answer | MET | Opened the actual source file cited for each of the 5 questions and checked the claim is really in it (e.g. `admin_dining_dollars.txt` really does say "Whatever is left in May disappears"). All 5 held up. |

## Diagnoses

**Criterion 1 — not one of the five pipeline stages.** The gap wasn't in
loading, chunking, embedding, retrieval, or generation — every retrieved
chunk and every generated answer in the Before log already looks correct by
eye. The problem was that "looks correct by eye" was the only check that
existed. Building `scorer.py` — Milestone 2's actual task — turned out to
be its own two-stage debugging process, not a one-shot write:

**First attempt (`results/run_2026-09-29_0817_after_simple_scorer.md`):** a
literal-substring match, `expects.lower().strip() in answer.lower()`.
Mechanism: it needs my exact phrase to appear verbatim, in that exact word
order, inside the answer. It never does, because nothing tells the model to
echo my wording back:

- `expects="Aldridge is card only, Calder Annexe is app-based"` failed all 3
  runs against "In Aldridge Hall, laundry is card only, whereas in Calder
  Annexe, laundry is app-based." — same fact, different sentence structure.
- `expects="End of week two"` failed the same way against "...through the
  end of the second week..." — "week two" vs "the second week."
- `expects="three"` was the flaky one (pass/fail/pass): the model sometimes
  wrote "three exams" and sometimes only "two midterms and a final," and the
  substring check can only match the literal digit-word "three," not the sum
  of the two numbers it's next to.

That's three different questions failing for one reason, not three
problems — the target itself wasn't wrong, the measurement was. Per
`criteria.md`'s own note on this ("the criterion couldn't be measured the
same way twice"), this is a revision, not a lowered target — see the
`criteria.md` update under criterion 1.

**Second attempt (`results/run_2026-09-29_0830_after_llm_scorer.md`):**
switching to an LLM-as-judge — asking the model directly whether the answer
states the fact, same meaning regardless of wording — fixed the paraphrase
cases immediately. But it reintroduced a narrower version of the same
problem on the arithmetic case: run 1 scored the exact same "two midterms
and a final" answer as `fail`, while runs 2 and 3 scored it `pass` — an
identical prompt, judged three different ways, because the judge call
sampled at the default (non-zero) temperature and wasn't told to compute
2 + 1 before answering. That's the same "couldn't be measured twice"
failure one level up, now in the judge itself rather than in string
matching.

**Criteria 4 and 5 — nothing to diagnose.** Both hit their target (5 of 5
against 4 of 5) in the Before run already — see Verdicts above — so there's
no miss here to trace to a stage.

## The Improvement

**What I changed:** Replaced the substring scorer in `scorer.py::judge` with
an LLM-as-judge — a call through `generate.py::generate` that asks the model
whether the answer states the fact, same meaning regardless of wording.
When that judge itself scored the same "two midterms and a final" answer as
`fail` on one run and `pass` on the next two, I fixed the judge rather than
the pipeline: added a `temperature` parameter to `generate()` (unused by
every other caller, so nothing else changed) and call the judge at
`temperature=0.0`, and rewrote `JUDGE_SYSTEM` to explicitly say "if the FACT
is a count and the ANSWER lists items instead, add them up yourself" and to
reason for a sentence before a final `VERDICT: YES/NO` line, instead of
forcing a single word straight away.

**Why I picked it:** Both diagnosed problems were measurement problems, not
retrieval or generation problems — the chunks and answers were already
right. Tuning chunking or `TOP_K` wouldn't have touched either failure mode
(literal-phrase mismatch, then judge non-determinism on an unstated sum), so
the fix had to be in `scorer.py` and in how the judge call was made, not in
the RAG pipeline itself.

### Run Log — After

From `results/run_2026-09-29_0842_after_llm_scorer_fixed_v1.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Sampled chunks read as one complete, usable thought | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Every named source actually supports the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

Criteria 4 and 5 carry the same numbers as the Before log rather than being
re-checked from scratch: criterion 4 is about the 5 sample chunks from
Unit 1, which this session's change never touched, and retrieval is
deterministic on an unchanged corpus and config, so `Sources retrieved` for
all 5 questions is identical between the two logs (checked directly — same
filenames, same order, in both). The scorer/judge change only affects
which answers get recognized as correct, not which sources get retrieved or
cited.

**Real output — criterion 1, now passing.** Same question, same kind of
answer as the miss above, now judged correctly:

```
Answer: Based on the document `course_cs_210_exams.txt`, there are two
midterms and a final exam for the CS 210 course.
Judge:  The answer lists two midterms and one final, which totals three
exams — matching the fact. VERDICT: YES
```

**Did it help?** Yes. Criterion 1 went from N/A — not measurable at all,
since no scorer existed in the Before log — to a stable 5 of 5 across all
three After runs, clearing the 4-of-5 target. The two diagnostic runs in
between show the path there: 3-of-5 / 2-of-5 / 3-of-5 with the substring
scorer, then 4-of-5 / 5-of-5 / 5-of-5 (one flaky run) with the first,
non-deterministic LLM judge, before the `temperature=0.0` fix settled it
at 5-of-5 across the board. Criteria 2 and 3 didn't move at all (5 of 5
and 5 of 5 in the Before log and again in the After log), which is
expected: nothing about this change touches source-naming or the gate.
The underlying answers themselves look unchanged between Before and
After — this fix made the scorer able to recognize correctness that was
arguably already there, not made the system produce better answers.

## What's Still Broken

All five criteria are MET as of the After log — nothing outstanding there.

For criterion 1: the fix is a targeted patch for the one failure mode I
actually saw (a count stated as a sum of listed items). It's untested
against other paraphrase styles the judge might not generalize to as
cleanly — e.g. a fact stated as a range, or contradicted partway through a
longer answer. I stopped once the observed flakiness was gone and didn't
go looking for failure modes I hadn't seen yet.

## What I'd Do Differently

Criteria 3, 4, and 5 turned out to be too easy. All three landed at a clean
5 of 5 against a target of 4 of 5, and none of them ever came close to
missing — which in hindsight means they were only ever tested against easy
cases, not cases that could actually surface a failure:

- **Criterion 3** (the gate) was only tested against `OUT_OF_SCOPE`
  questions that are topically miles from campus life (capital of Mongolia,
  oil changes, Rust for-loops), so their retrieval distances (0.787–0.923)
  were never going to sneak under the 0.55 threshold. A real test needs
  near-miss questions that reuse the corpus's own vocabulary but still
  aren't answerable from it — e.g. "What's the wifi password in Aldridge
  Hall?" — which would land much closer to the threshold.
- **Criterion 4** (chunk quality) sampled 5 chunks that happened to look
  clean, instead of specifically sampling from the corpus's longest or most
  structurally complex documents — exactly where my own Unit 1 notes said
  a paragraph-based splitter was most likely to cut something awkwardly.
- **Criterion 5** (citation support) only used questions with one dominant,
  obviously-relevant document. A real test needs a question where two
  similar-but-distinct documents both come back in the top-k (e.g. a
  course's workload doc vs. its exams doc), to check whether the answer
  cites the one that actually supports the specific claim rather than just
  a related one.

Next time, I'd pick test questions and samples for these three by
deliberately looking for the boundary case each criterion is supposed to
catch, rather than by picking whatever looked representative.

One more thing worth considering, from criterion 1: I found the judge's
flakiness by accident, from a real `run_eval.py` run turning up a fail
where I expected a pass. Writing a handful of hand-picked adversarial
`(expects, answer)` pairs — a paraphrase, a numeral-vs-word case, a partial
compound fact — and running them through `scorer.judge` directly, the way
we did in this session's terminal checks, would have caught the
temperature-flakiness before it showed up in a graded run instead of after.
