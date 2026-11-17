# 3Blue1Brown Reinventing Entropy — audit of pedagogical integration

Date: 2026-11-16

## Scope

This audit checks whether the pedagogical ideas in the Part 1 lesson and its companion source repository are integrated as a learning progression in LLM Lab, rather than merely cited. The 3Blue1Brown source code was inspected at `3b1b/videos/_2026/cross_entropy`, including `entropy.py`, `distribution.py`, `language_models.py`, `next_char.py`, and `part2_supplements.py`. No source animation, figure, or code was copied.

## What was already integrated well

- The source synthesis reconstructs the progression from a coding problem, through prefix-free codes, surprisal, entropy, conditional language probabilities, and entropy rate.
- The predictive-compression experiment includes arithmetic coding and exact decoding, plus a Huffman code, prefix validation, Kraft sum, expected code length, and unit tests.
- The canonical entropy lesson distinguishes predictive entropy from observed surprisal.
- The canonical cross-entropy lesson derives the one-hot target case, distinguishes cross-entropy from predictive entropy, and treats causal alignment, masking, and reduction.
- The bilingual revision sheet already distinguishes sequence compression, model compression, and runtime memory, and qualifies the “compression is intelligence” interpretation.

## Pedagogical gap found

The ingredients existed, but the learner-facing revision sheet did not explicitly expose the complete discovery sequence as a set of linked steps. In particular, the transition from the visual prefix-code tree to the average information of a source, then to context-dependent next-token probabilities, and finally to cross-entropy as model evaluation was implicit across several pages.

The companion code repository also makes the visual/computational progression more concrete than a video-only citation suggests: it contains distributions, Huffman material, next-token prediction and language-model scenes, and Part 2 cross-entropy/KL supplements. These were treated as supporting pedagogical evidence, not as a claim that every scene or asset had been visually audited.

## Change made

The French and English compression revision sheets now include the same six-step reconstruction:
1. symbol frequencies;
2. prefix-free code tree and Kraft check;
3. event surprisal;
4. average surprisal / entropy;
5. context-dependent probabilities and sequence cost;
6. target distribution versus model distribution / cross-entropy.

A compact Mermaid flow and a numerical checkpoint use the dyadic distribution `(1/2, 1/4, 1/8, 1/8)`, whose Huffman average length equals its entropy (1.75 bits). The text explicitly warns that this equality is not general for arbitrary distributions.

## What remains intentionally separate

- The canonical lessons remain the authoritative definitions and derivations; the revision sheet is a bridge, not a duplicate lesson.
- Part 1's entropy narrative and Part 2's cross-entropy/KL treatment remain distinct.
- No 3Blue1Brown visuals, animations, transcript, or source code are reproduced.
- The existing practice pages remain the detailed exercise hubs; the revision-sheet checkpoint is a short retrieval-practice prompt, not a replacement.

## Acceptance criteria for future improvements

- A learner can explain why a prefix-free tree enables unambiguous decoding.
- A learner can distinguish event surprisal, entropy, conditional entropy, and empirical average NLL.
- A learner can explain why a model's cross-entropy under target data differs from the model's own predictive entropy.
- A learner can reproduce exact decoding and identify which shared model/tokenizer/metadata costs are excluded.
- Claims about compression and intelligence remain explicitly qualified.
