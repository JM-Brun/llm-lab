# Day 01 — empirical evidence and LLM connection follow-up

**Date:** 2026-11-26  
**Scope:** French and English Day 01 stories; calendar promise checked against the current landing pages  
**Status:** focused editorial revision prepared; novice-reader acceptance remains open

## Why this revision

The previous audit found that the story explained the rank–frequency formula and showed a synthetic curve, but did not make the transition from mathematical model to empirical evidence sufficiently tangible. The LLM connection also named the marginal/conditional distinction without walking the reader through a concrete context.

The revision strengthens those two bridges without changing the story's six-part structure, adding a second experiment, or moving calculations into the main lesson.

## Changes made

### 1. Put empirical estimates in context

The cross-linguistic paragraph now reports the range of fitted parameters in the five languages covered by Lavi-Rotbain and Arnon (2023):

- $\\alpha$: 1.30–1.57;
- $\\beta$: 7.12–19.48.

The text explicitly bounds these values to the studied child-directed-speech corpora. They are fitted parameters for those datasets, not constants belonging to languages and not estimates that can be transferred to all text genres. The full corpus table and methodological details remain in the Zipf deep dive; the calendar story does not duplicate them.

### 2. Connect the synthetic curve to an empirical visualization

The limitations section now points to Figure 1 in Piantadosi (2014), based on the American National Corpus. The linked figure provides an empirical density view and a Zipf–Mandelbrot fit, with rank and frequency estimated from independent subcorpora.

The story highlights the two observations relevant to its argument: dispersion increases in the long tail, and residuals retain structure not captured by the fitted curve. This makes the distinction explicit:

- the local SVG teaches the shape of the mathematical relation using synthetic values;
- the linked paper provides an empirical example and a more careful estimation procedure.

The external figure is linked, not copied into the project. No image-rights or asset-provenance claim is made.

### 3. Make the LLM connection concrete

The marginal-versus-conditional paragraph now uses the prefix “La capitale de la France est…” / “The capital of France is…”.

It contrasts:
- a corpus question: how often does the form “Paris” occur across all contexts?
- a model question: what distribution does the model assign to the next token after this particular prefix?

The wording explicitly notes that the continuation depends on the prefix and tokenizer segmentation. It does not invent model probabilities or imply that a lexical form always corresponds to one model token.

### 4. Restore a small bilingual navigation parity gap

The English “Go further” list now links to the same Zipf deep dive that the French page already exposed there. Both stories therefore offer a clear final route to the optional depth, while retaining their existing local links to text data and tokenization.

## What was deliberately preserved

- The opening first-person text and its distinctive question.
- The reproducible French count: 217 lexical occurrences and 125 orthographic types.
- The independent English demonstration corpus: 196 occurrences and 127 types.
- The distinction between lexical types, lexical occurrences and tokenizer tokens.
- The synthetic rank–frequency SVG and its explicit caption/alt text.
- The six-part story structure and the approximately 15-minute target.
- The dedicated Practice page as the home for calculations and exercises.
- The companion deep dive as the home for history, extended comparisons, model variants and applications.

No calendar door titles, day ordering, status labels, page-map metadata, concept registry, or learning routes were changed. The landing pages already expose the first story as available and keep the second as a preview; their current public promise remains consistent with the separation between stories and Practice.

## Validation and evidence limits

**Checked at source level:**
- the reported parameter ranges match the five-language table in the companion deep dive;
- the Piantadosi description matches the paper's Figure 1 and its independent-subsample procedure;
- the LLM example distinguishes a corpus-wide marginal frequency from a context-conditioned next-token distribution;
- the new FR/EN paragraphs are semantically aligned;
- the English final deep-dive link now matches the French destination;
- the story body retains its existing section structure and Practice link.

**Not yet established:**
- a fresh Quarto render of this branch;
- rendered desktop/mobile, theme, keyboard and accessibility checks on the changed branch;
- CI results;
- actual reading time;
- novice comprehension and an explicit editorial accept/revise decision.

## Remaining acceptance work

1. Render both language pages and verify the new links, equations, typography and paragraph placement.
2. Check the Piantadosi figure link and the two deep-dive anchors in the rendered pages.
3. Run the existing relevant site/browser checks; do not create a new workflow for this page.
4. Conduct the existing [Day 01 novice-reader protocol](../advent-calendar-pilots/day-01-novice-review.md). In particular, ask the reader to explain the empirical figure's role and the difference between the global frequency of “Paris” and its probability after a prefix.
5. Record observed reading time, comprehension evidence, and an explicit accept/revise decision. A source audit or successful CI is not a substitute for this learner test.

## Sources

- Lavi-Rotbain, O. & Arnon, I. (2023), [Zipfian Distributions in Child-Directed Speech](https://doi.org/10.1162/opmi_a_00070).
- Piantadosi, S. T. (2014), [Zipf’s word frequency law in natural language: A critical review and future directions](https://doi.org/10.3758/S13423-014-0585-6).
- Project companion: [Zipf deep dive — French](../../site/fr/zipf-law-deep-dive.qmd).
