# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
My five questions are specific and each has an answer in a single document, but
they span different parts of the corpus: course information, accessibility,
transit, board games, and student advice. I expect retrieval to work for most
of them, but set 4 of 5 rather than all 5 because wording differences or a
closely related document could cause one question to retrieve useful context
without the exact answer.
---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
The pipeline keeps the source filename as metadata for every retrieved chunk,
and the answer is generated only from those retrieved chunks. Because source
information is available for every in-scope answer without depending on the
model to remember it, all five answers should be able to name a source. Missing
a source would indicate a problem in how the answer or its retrieval metadata
is presented, not an unavoidable limitation of this corpus.
---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
When I tested the relevance cutoff, the out-of-scope questions had worse
(higher) nearest-chunk distances than most of my in-scope questions, although
there was not a perfectly clean separation. A target of 4 of 5 gives the gate
room for one generic question to resemble a document by accident, while still
requiring it to reject out-of-corpus questions reliably. Requiring only 3 of 5
would allow too many unsupported answers through.

---

## 4. Something about your chunks

Of five chunks sampled from different source documents, at least four read as
one complete, usable thought: they begin and end at a sentence or paragraph
boundary and include enough context to understand the claim.


**Why this target:**
Most documents in this corpus are short, self-contained posts, while the
longer guides are organised into headings and sections. A good chunking method
should preserve those ideas rather than splitting a sentence or separating a
claim from its qualification. I chose 4 of 5 rather than all 5 because a very
long guide section may still need one imperfect boundary; fewer than four would
suggest that fragmented chunks are a recurring problem.


---

## 5. Your choice

For at least 4 of my 5 test questions, every source named in the answer
actually contains information that supports the answer.


**Why this target:**
My corpus includes related documents that could be retrieved together, such as
course descriptions and course exam information, or official campus documents
and student discussion threads. Naming any source is easy, but an irrelevant
citation would make the answer less trustworthy. I chose 4 of 5 because one
question may retrieve a closely related document that is useful context but
does not directly state the answer; a lower target would allow incorrect
citations too often.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
