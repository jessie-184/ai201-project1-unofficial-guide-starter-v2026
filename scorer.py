"""
The scorer: does an answer actually state the fact `expects` names?

Strategy: LLM-as-judge, not string similarity. `expects` is a short fact
("three", "4 minutes", "Aldridge is card only, Calder Annexe is app-based")
while answers are full sentences that may phrase it differently or use a
different number form ("3" vs "three"). No similarity score handles both
paraphrase and compound facts reliably, so this asks the model directly,
reusing `generate()` for its pacing, budget guard, and retries.
"""

import gate
from generate import generate

JUDGE_SYSTEM = """You are grading a short-answer quiz. You will be given a QUESTION, a FACT the correct answer must contain, and an ANSWER someone gave.

Decide whether the ANSWER states the FACT — same meaning counts even if the wording or number format differs (e.g. "3" vs "three"). If the FACT has multiple parts, the ANSWER must state all of them. Hedging, vagueness, or refusing to answer does not count as stating the fact.

If the FACT is a count and the ANSWER instead lists the individual items (e.g. FACT "three" and ANSWER "two midterms and a final"), add the items up yourself before deciding — do not require the ANSWER to spell out the total in words.

First, reason about it in one or two short sentences. Then, on its own final line, write exactly "VERDICT: YES" or "VERDICT: NO"."""


def judge(question, expects, answer, results) -> bool:
    """
    True if `answer` states the fact in `expects`, False otherwise.

    A refusal (the gate's fixed text) never states anything, so it's scored
    False without spending a model call. temperature=0.0 because this is a
    grading call: the same answer graded twice should get the same verdict,
    not a coin flip on borderline cases like counting listed items.
    """
    if not expects.strip() or answer.strip() == gate.REFUSAL:
        return False

    prompt = f"QUESTION: {question}\n\nFACT: {expects}\n\nANSWER: {answer}"
    response = generate(prompt, system=JUDGE_SYSTEM, cache=False, temperature=0.0)
    verdict_line = response.strip().splitlines()[-1].upper()
    return "YES" in verdict_line
