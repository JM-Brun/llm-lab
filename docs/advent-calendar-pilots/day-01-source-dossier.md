# Day 01 source dossier — Zipf's law and lexical frequency

**Status:** first draft for editorial and scientific review  
**Date:** 2026-11-23  
**Languages:** French and English  
**Story question:** Why does the word “the” appear everywhere?

## Editorial angle

The story explains the inequality of lexical frequencies through the rank-frequency relation commonly called Zipf's law. Its value for LLM readers is statistical: language corpora are highly imbalanced, and frequency affects the number of observed learning opportunities.

This is not a tokenization tutorial and does not claim to explain the causal origin of Zipf's law.

## Primary and authoritative sources

### Piantadosi (2014)

Steven T. Piantadosi, “Zipf’s word frequency law in natural language: A critical review and future directions,” *Psychonomic Bulletin & Review* 21, 1112–1130 (2014). DOI: https://doi.org/10.3758/S13423-014-0585-6

Supports:
- the approximate rank-frequency relation \(f(r) \propto 1/r^\alpha\), with \(\alpha\) often near 1;
- the existence of a few very frequent words and many rare words;
- the fact that actual word-frequency distributions are more complex than one simple law;
- a statistical visualization pitfall: rank and frequency estimated on the same sample have correlated errors;
- the recommendation to examine frequency and rank using independent data splits when testing the relation.

Editorial constraints:
- say “approximately”, “often” and “in the corpora/settings studied”;
- do not say the distribution is exactly Zipfian or that a power law is the uniquely correct model;
- do not infer a causal explanation from the observed curve.

### Piantadosi (2017), “Unzipping Zipf's law”

https://doi.org/10.1371/journal.pone.0181987

Supports:
- discussion of syntactic and semantic factors as contributors to word-frequency distributions;
- an account in which multiple ingredients are considered rather than one universal cause.

Editorial constraints:
- the article proposes a model; do not present its account as settled consensus or a complete explanation.

### Zipf (1949), *Human Behavior and the Principle of Least Effort*

https://archive.org/details/humanbehaviorpri00zipf

Historical source for Zipf's popularization and broader framing. The draft does not attribute a modern exact statistical test or a universal causal mechanism to Zipf.

## Claim-to-source ledger

| Draft claim | Source / basis | Qualification |
|---|---|---|
| A few words are very frequent and many are rare | Piantadosi 2014 | Corpus-dependent; no universal fixed ranking |
| \(f(r) \approx C/r^\alpha\), often with \(\alpha\) near 1 | Piantadosi 2014; Zipf 1949 | Approximation, not exact identity |
| Log-log transformation yields slope \(-\alpha\) | Algebraic derivation | Exact for the stated power-law model |
| Rank/frequency estimates from the same sample can create correlated errors | Piantadosi 2014 | State as a methodological warning, not a claim that all Zipf plots are false |
| Multiple syntactic/semantic factors may contribute | Piantadosi 2017 | Proposed explanation, not settled consensus |
| Rare forms have fewer observed training examples in a fixed corpus | Direct consequence of lower count | Do not claim that frequency alone determines model performance |
| Word-frequency counts differ from tokenizer-token counts | Definition of lexical type vs model token | Avoid drifting into a tokenization explanation |

## Numerical example verification

For the deliberately synthetic model \(f(r)=C/r\) with \(C=1000\):

- rank 1: 1000
- rank 2: 500
- rank 5: 200
- rank 10: 100
- rank 100: 10
- rank 1000: 1

For the challenge with \(C=12000\):

- rank 4: 3000
- rank 20: 600

All values are mathematical consequences of the toy model, not corpus measurements.

## Scope and non-claims

- The word “the” is an English hook; the French story uses “de” as its natural counterpart. Neither is claimed to be the most frequent word in every corpus.
- The draft distinguishes lexical word types/tokens from model tokenizer tokens.
- The story does not claim that Zipf's law is exact, universal, or a complete causal explanation.
- The draft does not infer a model's tokenization strategy or rare-word capability from a lexical rank-frequency curve.
- The synthetic plot is illustrative, not fitted to a corpus.

## Visual provenance

The file site/images/advent-zipf-rank-frequency.svg is an original vector diagram generated for this story. It plots the synthetic relation \(f(r)=1000/r\) on log-log axes. No external image is reused.

## Review still required

- Verify the exact canonical lesson paths in both languages.
- Render both QMD versions and inspect math, figure, caption and responsive layout.
- Confirm Quarto's relative image path for the new story location.
- Obtain a novice read-through and record actual reading time.
- Review the strength and placement of the LLM-training implication.
