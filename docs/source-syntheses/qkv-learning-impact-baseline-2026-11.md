# Q/K/V — learning-impact baseline and assessment plan

**Review date:** 2026-11-05  
**Status:** editorial audit and proposed evaluation; no learner outcome data collected  
**Source collection:** [Q/K/V source collection](../source-reviews/qkv-source-collection.md)  
**Related synthesis:** [Complementary perspectives](qkv-complementary-perspectives-2026-11.md)  
**Coverage matrix:** [Pedagogical coverage matrix](qkv-pedagogical-coverage-matrix-2026-11.md)

## 1. Purpose and evidence boundary

The three-source Q/K/V collection has already changed the bilingual lesson through a geometric perspective, a contextual-language contrast and more explicit misconception boundaries. The next question is not whether more source material can be added, but whether the resulting learning experience supports better discrimination, calculation and transfer.

This dossier establishes a **content-based baseline** and proposes a small assessment. It does not claim measured improvement: no learner study, pre/post comparison, item analysis or usability test has been conducted.

The audit is based on the current canonical EN/FR Q/K/V lesson, scaled-dot-product-attention lesson and exercise hub. It does not rescan the external sources.

## 2. Existing project coverage

| Learner outcome | Existing location | Current treatment | Baseline judgement |
|---|---|---|---|
| Distinguish Q/K from V roles | Q/K/V lesson, essential-idea callout and self-check | Q/K determine weights; V supplies aggregated content; asks what changes if V changes alone | Explicitly covered |
| Explain why projections are separate | Q/K/V lesson, projection section | Matching views versus content/payload; learned projections from a shared representation | Explicitly covered |
| Infer Q/K/V tensor shapes | Q/K/V lesson and exercise hub | Different output dimensions; NumPy projection exercise with Q/K=(3,2), V=(3,3) | Explicitly practiced |
| Distinguish self-attention from cross-attention | Q/K/V lesson and cross-attention link | Query stream versus key/value stream | Covered conceptually; not a focus of current exercises |
| Distinguish coreference from lexical polysemy | Q/K/V optional contextual contrast | Pronoun antecedent versus competing senses of one word | Explicitly illustrated; transfer not assessed |
| Relate Q/K geometry to compatibility | Q/K/V optional geometric note | Dot-product identity and norm/angle qualification | Explained; no numerical comparison exercise |
| Calculate scores, scaling, softmax and aggregation | Scaled-dot-product-attention lesson | Equations and one-query/two-key worked example | Worked once; exercises are limited |
| Distinguish soft weighting from hard nearest-neighbour lookup | Q/K/V and attention misconception notes | Explicit prose guardrails | Explained; not directly assessed |
| Interpret attention weights cautiously | Attention lesson and Q/K/V page | Relative weighting, not semantic relevance or causal explanation | Strongly qualified; no dedicated exercise |

The existing attention exercise hub contains two relevant activities:
1. a hand calculation of a weighted value aggregation, including swapping values while holding weights fixed;
2. a NumPy projection exercise that checks Q/K/V shapes and explains why changing W_V does not change QK-derived scores.

The exercise hub itself labels further score/weight calculations, cautious interpretation and causal-invariance reasoning as planned work. Therefore, a proposal for more generic projection or weighted-sum exercises would duplicate existing material.

## 3. Actual incremental gaps

The most defensible remaining opportunities are **assessment gaps**, not missing explanations.

### A. Dot product versus cosine similarity

The optional geometric note already states
\[
q^\top k = \lVert q\rVert\,\lVert k\rVert\cos(\theta).
\]
A short numerical contrast can test whether learners understand that equal angles do not imply equal dot products when vector norms differ.

Target misconception: treating the dot product as cosine similarity or an angle-only measure.

### B. Softmax weighting versus hard retrieval

The lessons already explain that softmax distributes weight across accessible positions. A small numerical item can test whether the learner expects a weighted mixture or an argmax selection.

Target misconception: assuming that attention always selects one best-matching key/value pair.

### C. Functional role discrimination

The Q/K/V self-check tests the central distinction, while Codefinity contributes a useful role-confusion distractor pattern. A diagnostic item can test the distinction under a changed condition (e.g. change W_V while keeping Q and K fixed).

Target misconception: believing that V determines attention weights, or that changing V changes QK scores.

### D. Contextual transfer

The coreference/polysemy contrast is already present in the lesson. A short classification prompt can test whether learners can distinguish the two phenomena without implying that an attention head has been empirically shown to perform either task.

Target misconception: treating all contextual interpretation examples as the same linguistic phenomenon, or as evidence of a specific head's specialization.

## 4. Recommended minimal assessment bundle

Do not create a new page or duplicate the existing worked examples. Add a small optional diagnostic set to the existing Attention section of `site/en/exercises.qmd` and `site/fr/exercises.qmd`, only after review.

| Item | Format | Expected reasoning | Main outcome |
|---|---|---|---|
| 1. Norms matter | Two vector pairs with the same angle but different norms; compare dot products and cosine similarities | Dot products differ in magnitude while cosine similarities agree | Geometric precision |
| 2. Soft mixture | Two scores with non-degenerate softmax weights and two distinct values; compare softmax aggregation with argmax retrieval | Both values contribute to the weighted sum unless a weight is exactly zero | Computational interpretation |
| 3. Projection roles | Change W_V while holding X, W_Q and W_K fixed; predict which intermediate quantities change | Q, K, scores and weights stay fixed; V and generally the output can change | Functional discrimination |
| 4. Context transfer | Classify a pronoun-antecedent example and a polysemous-word example | Coreference relates expressions; polysemy selects a sense of one expression | Transfer and conceptual distinction |

Items 1–3 are the recommended minimum. Item 4 is optional because the current lesson already contains the contrast and it may be better suited to a quick self-check than an extended calculation.

## 5. Evaluation rubric

Use a criterion-based rubric rather than treating a single correct multiple-choice answer as proof of understanding.

| Criterion | 0 — not yet | 1 — partial | 2 — demonstrated |
|---|---|---|---|
| Geometric distinction | Equates dot product with cosine | Mentions norms but cannot use them | Correctly explains and computes the norm effect |
| Soft versus hard attention | Describes attention as selecting one winner | Recognizes multiple weights but miscomputes output | Correctly computes and interprets a weighted mixture |
| Q/K/V roles | Confuses V with matching/score computation | States roles but fails a changed-parameter case | Correctly predicts invariants under W_V-only changes |
| Linguistic transfer | Conflates the two phenomena | Identifies examples but not the distinction | Correctly distinguishes coreference and lexical polysemy |

Suggested interpretation:
- 0–2: revisit the functional intuition and worked example;
- 3–5: core roles are emerging; revisit the specific failed criterion;
- 6–8: the assessed distinctions are demonstrated on these items.

These thresholds are provisional instructional heuristics, not validated psychometric cut-offs. Do not report them as a validated measure of mastery.

## 6. How to evaluate whether the integration helped

If the project later has access to learner feedback or a small pilot:

1. Record the version of the lesson and exercise set.
2. Use the same learning outcomes and equivalent, not identical, diagnostic items before and after the lesson.
3. Score explanations with the rubric above; retain written reasoning, not just correctness.
4. Inspect item-level error patterns and distractor selections.
5. Ask learners which explanation (index-card, geometric, linguistic contrast) helped and what remained confusing.
6. Report sample size, recruitment context, missing responses and limitations. A small convenience sample is formative feedback, not a generalizable efficacy study.

Without learner data, limit claims to content coverage, assessment design and technical validation.

## 7. Integration decision

- **Canonical Q/K/V page:** no new section required; current multi-perspective explanation is appropriately layered.
- **Canonical attention page:** no duplicate derivation required; it already owns scores, scaling, softmax and aggregation.
- **Concept graph and learning route:** no change justified.
- **Exercise hub:** candidate for a bounded optional diagnostic bundle focused on the four gaps above.
- **Visual assets:** no external illustration reuse proposed; existing asset decisions remain unchanged.
- **External source scans:** no further scan required for this assessment design.

## 8. Traceability and next work

- Q/K/V source reviews and extractions are linked from the [living collection](../source-reviews/qkv-source-collection.md).
- The multi-source synthesis records source contributions and their dispositions.
- The coverage matrix distinguishes source coverage from project coverage.
- The current EN/FR pages remain the canonical learning resources.

**Next implementation gate:** inspect exercise conventions and bilingual parity, then add only the three minimal diagnostic items if they remain non-duplicative. Keep the linguistic transfer prompt optional. Validate the arithmetic independently and preserve existing exercises.
