# Day 01 source dossier — Zipf's law and lexical frequency

**Status:** bilingual public-reading revision prepared in PR #1639; novice review and explicit editorial acceptance remain pending  
**Date:** 2026-11-23  
**Languages:** French and English  
**Story question:** FR — Pourquoi le mot « je » revient-il si souvent dans ce texte ? EN — Why does the word “I” appear so often in this text?

## Editorial angle

The story starts from an original first-person text written for this demonstration. It asks why « je » / “I” appears frequently, then uses the resulting lexical counts to introduce the inequality of word frequencies and the rank-frequency relation commonly called Zipf's law. Its value for LLM readers is statistical: language corpora are highly imbalanced, and frequency affects the number of observed learning opportunities.

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

### Lestrade (2017), “Unzipping Zipf's law”

https://doi.org/10.1371/journal.pone.0181987

Supports:
- a proposed model in which syntactic class sizes and semantic specificity/reusability interact to produce a near-Zipfian distribution.

Editorial constraints:
- identify this as Sander Lestrade's proposal, not as a consensus explanation;
- retain the paper's explicit caveat that the origins of Zipf's law remain elusive.

### Pilgrim and Hills (2021), “Bias in Zipf's law estimators”

https://doi.org/10.1038/s41598-021-96214-w

Supports:
- common maximum-likelihood estimators can be biased for rank-frequency data because empirical ranks are not known a priori;
- splitting a corpus can reduce the correlated-error problem discussed by Piantadosi (2014), but does not eliminate all rank-estimation errors;
- estimation remains difficult for natural language because a simple power-law sampling model does not capture the full data-generating process.

Editorial constraints:
- do not imply that corpus splitting completely solves Zipf exponent estimation;
- keep the story's claim narrow: later work documents residual bias, especially in the rare-word tail.

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
| Independent corpus splits reduce correlated errors but do not remove every estimation bias | Piantadosi 2014; Pilgrim and Hills 2021 | Avoid presenting splitting as a complete solution; note residual uncertainty in rare-word ranks |
| Multiple syntactic/semantic factors may contribute | Lestrade 2017 | Proposed explanation, not settled consensus |
| Rare forms have fewer observed training examples in a fixed corpus | Direct consequence of lower count | Do not claim that frequency alone determines model performance |
| Word-frequency counts differ from tokenizer-token counts | Definition of lexical type vs model token | Avoid drifting into a tokenization explanation |

## Numerical example verification

The exercise page's rank-construction example is deliberately a separate, fictional count table (de: 12, et: 7, chat: 4, chien: 3, luciole: 1 in French; the: 12, and: 7, cat: 4, dog: 3, firefly: 1 in English). It teaches that rank is obtained by sorting observed counts; it is not presented as an empirical corpus or as a fitted Zipf distribution.


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

- The first-person pronouns « je » and “I” are hooks arising from the deliberately first-person demonstration text. Their high frequency is a property of this text's viewpoint, not a universal claim about either language.
- The draft distinguishes lexical word types/tokens from model tokenizer tokens, explicitly disambiguating the two meanings of *token*.
- The story does not claim that Zipf's law is exact, universal, or a complete causal explanation.
- The draft does not infer a model's tokenization strategy or rare-word capability from a lexical rank-frequency curve.
- The synthetic plot is illustrative, not fitted to a corpus.

## Visual provenance

The file site/images/advent-zipf-rank-frequency.svg is an original vector diagram generated for this story. It plots the synthetic relation \(f(r)=1000/r\) on log-log axes. No external image is reused. The Quarto figure caption and its fig-alt screen-reader description are authored separately.

## Validation completed and remaining review

- [x] Canonical lesson paths and page-map relation IDs verified in both languages.
- [x] Controlled domain and bilingual metadata validated by the repository checks.
- [x] Both QMD pages rendered by Quarto; the two displayed mathematical expressions rendered through MathJax in each language.
- [x] Original SVG loaded in FR/EN; fig-alt is present and describes the plotted relation independently of the visible caption.
- [x] Desktop (1440 px) and mobile (390 px) browser review passed with no horizontal overflow, console errors or page errors.
- [x] Desktop Axe checks reported zero violations for both language versions.
- [x] Full repository CI, full-site Quarto build, learning-map/graph/timeline checks, local links and secret scanning passed on the restored planned state.
- [x] Relative image path, local links and page-aware language-switch links verified.
- [ ] Obtain a novice read-through and record actual reading time using [the Day 01 review protocol](day-01-novice-review.md).
- [ ] Review with a novice whether the LLM-training implication and challenge are clear and appropriately qualified.
- [ ] Record explicit editorial acceptance before drafting Day 02.

**Post-preview source correction:** a literal escaped newline before the Pilgrim and Hills (2021) bibliography item was found in both QMD files during a final source review. It has been replaced by a real Markdown line break. Re-run the PR preview after this correction before closing technical review.


## Editorial archive — hidden Easter-egg provenance (repository only)

This section records the cultural reference that originally motivated the exercise. **It is repository metadata, not lesson content. Do not copy it into either published language page, page metadata, navigation, search snippets, or public-facing captions.** The published French demonstration uses the complete text supplied by the project maintainer. The public page intentionally contains no character, film, transcript, or source attribution; the source trail is retained only in this repository dossier.

### Reference and source trail

- Character: Otis, the scribe in *Astérix et Obélix : Mission Cléopâtre* (2002), portrayed by Édouard Baer.
- Recognizable opening line used during the initial editorial exploration: « Vous savez, moi je ne crois pas qu'il y ait de bonne ou de mauvaise situation. » This short identification cue is retained here only to document the source of the easter egg; do not publish it as part of the teaching text.
- Source URL supplied by the project maintainer for the current text: [IMDb — Astérix & Obélix: Mission Cléopâtre, Otis quotes](https://www.imdb.com/fr/title/tt0250223/characters/nm0046347/#quotes). The page could not be independently fetched during this revision (HTTP 403); the public lesson therefore reproduces the text as supplied by the maintainer, without asserting independent transcript verification.
- Earlier exploratory transcript: [Happy Scribe — Le scribe, Astérix : Mission Cléopâtre](https://podcasts.happyscribe.com/happy-scribe-s-favorites/le-scribe-asterix-mission-cleopatre). It is an automated transcript, not a certified verbatim transcript of the film audio.
- Context, duration and history of the scene: [Le Parisien, 4 July 2023 — Ressortie d’« Astérix et Obélix : Mission Cléopâtre » : le monologue d’Otis encore plus interminable](https://www.leparisien.fr/culture-loisirs/cinema/ressortie-d-asterix-et-obelix-mission-cleopatre-le-monologue-dotis-encore-plus-interminable-04-07-2023-NA6P2W7M2JE6RA5WYVXEND4B4Q.php).
- The theatrical cut is approximately 54 seconds; a longer alternative version of approximately 1 minute 20 seconds was reported around the restored re-release. These durations refer to different edits and should not be conflated.

### Treatment decision

The full text supplied by the project maintainer is used in the French public lesson as an unattributed Easter egg. The public page contains no source name or link. This dossier retains the source URL for internal provenance only; it is not intended for publication. The old corpus statistics (216 lexical occurrences and 125 orthographic types) described the earlier automated transcript under its former segmentation rules; they are historical and superseded. Under the current stated orthographic convention, the supplied French text contains 217 lexical occurrences and 125 distinct types. The English page remains an independently written demonstration corpus (196 occurrences / 127 types); it is not a translation of the French monologue.


### Current published demonstration corpus — reproducibility record

The French public page uses the complete user-supplied first-person text as an unattributed Easter egg; the English page retains its independently written demonstration text. The complete texts are maintained in their corresponding QMD files; this dossier does not duplicate them. Reproduce the counts by lowercasing, removing punctuation as a counted unit, preserving accented letters, retaining internal apostrophes as part of an orthographic unit, splitting on hyphens, and applying no lemmatization. The tokenizer used for this editorial count is equivalent to the Unicode pattern `[^\\W_]+(?:['’][^\\W_]+)*`.

- French: **217 lexical occurrences**, **125 distinct orthographic types**. The leading frequency groups are: `je` (13), `de` (9), `la` (7), `à` and `le` (6 each), then `et`, `goût`, `moi`, `ne`, `pas`, `que`, `qui` and `vie` (4 each). There are 86 singleton types and 20 types occurring twice.
- English: **196 lexical occurrences**, **127 distinct orthographic types**. The leading forms are: `I` (13), `a` (9), `the` (7), `that` (6), `and` (5), `my` and `what` (4 each).

These counts are exact for the current page texts and stated orthographic convention. They are pedagogical corpus counts, not observations from a naturally occurring language corpus and not a basis for fitting a Zipf exponent.


## Revision log — PR #1639

- The public French lesson contains the complete user-supplied monologue as an unattributed Easter egg; no source name, character, film, or source link appears on the page. Provenance is confined to this dossier.
- The French question remains focused on the frequency of « je ». Counts are computed from the complete quoted text, excluding the question and surrounding explanatory prose: FR: 217 occurrences, 125 types, 86 singleton types and 20 types occurring twice. EN remains independent: 196 occurrences, 127 types, 98 singleton types and 16 types occurring twice.
- The complete frequency tables now list every form occurring twice; rank intervals make ties explicit.
- The generated FR/EN learning-map artifacts have been synchronized with the new titles, summaries and section headings.
- The technical build and CI for the final revision are being checked in PR #1639. The novice-reader review and editorial acceptance gate remain separate and are not satisfied by CI.

### CI diagnosis and repair — 2026-11-25

The first CI rerun after the map-fragment syntax repair reported **831 passed, 1 failed, 1 skipped**. The only failure was `tests/knowledge/test_map_artifacts_freshness.py::test_tracked_interactive_map_matches_renderer[en]`: the English generated data fragment still contained the previous Day 01 title (with the French pronoun “je”) in its resource index. The French artifact matched the renderer. Python quality/domain checks, the Quarto site build and secret scanning all passed on that revision.

The stale English resource title has now been synchronized in `site/includes/generated-map-data-en.qmd`. This is a generated artifact: the authoritative validation remains the freshness test against `site/tools/build_learning_map.py`, not a visual inspection or a hand-maintained copy. If the test reports another mismatch, regenerate both language artifacts with:

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt --python 3.12 python site/tools/build_learning_map.py
```

The new commit still requires a complete CI rerun; no claim of a green final CI is made until that run completes.

### Remaining work before acceptance

- [ ] Confirm all CI jobs pass on the latest PR head, especially the bilingual generated-map freshness test.
- [ ] Inspect the rendered FR and EN pages at desktop and mobile widths; verify the question, full replacement text, frequency tables, tie intervals, links and exercise entry point.
- [ ] Perform a novice-reader review: can a reader identify the counted text, reproduce the normalization, distinguish lexical occurrences/types from tokenizer tokens, and understand why this tiny text does not establish Zipf’s law?
- [ ] Check that no cultural-source identifiers or source links leak into rendered pages, metadata, navigation, search summaries or generated map labels; keep provenance confined to this dossier.
- [ ] Record explicit editorial acceptance (or concrete revisions) before treating Day 01 as closed and moving to Day 02.
