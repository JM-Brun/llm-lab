# Source review — Michael Brenndoerfer, “Query, Key, Value: The Foundation of Transformer Attention”

**Source ID:** `brenndoerfer-query-key-value-attention-2025`  
**Canonical URL:** https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism  
**Author / publisher:** Michael Brenndoerfer · Language AI Handbook  
**Publication / update:** 2025-06-01 / 2025-06-04  
**Accessed:** 2026-11-05 · **Source type:** tutorial · **Language:** English

## 1. Scope and scan status

**Overall status: partially scanned.** All eleven visible chapter sections and the visible author text were inspected directly. The page identifies this as chapter 91 of a larger Language AI Handbook, with eleven sections and an estimated 40-minute reading time.

| Component | Status | Inspected | Not established |
|---|---|---|---|
| Author text | Complete for visible chapter | Motivation, analogy, equations, derivation, dimensions, code, worked example, limitations, parameters, summary and quiz introduction | Immutable archived version |
| Figures / visualizations | Partial | Captions and textual descriptions of variance plots, softmax distributions, attention heatmap and worked example | Original image bytes, visual design, alt text and accessibility |
| Code / data | Partial | Rendered snippets and outputs for projections, attention, scaling, shapes and worked example | Execution, dependencies, environment, reproducibility |
| Quiz | Partial | Eight-question quiz advertised; question 1 visible | Questions 2–8, feedback, scoring and interaction |
| Comments | Partial | One visible comment dated 2026-08-04 | Completeness of thread |
| Linked resources | Partial | Internal links to adjacent handbook chapters | Re-scan of linked chapters |
| Rights | Unknown | No reuse terms established | Text, figure, code and data licence |

No code, image or extended prose is copied into LLM Lab. The source remains link-only. No claim of browser accessibility or learner effectiveness is made.

## 2. Source-local pedagogical reconstruction

The chapter's eleven-section sequence is:

1. Motivate Q/K/V by distinguishing similarity from contextual relevance.
2. Introduce a database/catalog analogy.
3. Derive projections, QK scores, score variance, scaling, softmax and value aggregation.
4. Formalize tensor shapes and the distinction between (d_k) and (d_v).
5. Explain learned transformations and provide projection code.
6. Compose a complete attention layer and inspect shapes/heatmap.
7. Trace a three-token worked example through intermediate tensors and output.
8. Discuss limitations and applications.
9. Connect parameters to dimensions and computational cost.
10. Summarize.
11. Assess with an advertised eight-question quiz (only question one visible).

This is a **progressive formalization** sequence: intuition → statistical derivation → tensor contract → code → worked trace → limitations → assessment. It is a useful source-local model, not proof of an optimal sequence.

## 3. Technical review and caveats

### 3.1 Variance derivation for scaling

The tutorial assumes independent, zero-mean, unit-variance components for (q) and (k). Under those assumptions, each product (q_m k_m) has variance 1, and the sum over (d_k) components has variance (d_k). Dividing the dot product by (sqrt{d_k}) therefore motivates dimension-stabilized score variance.

This is a valid simplifying derivation, not a universal distributional guarantee. Real learned query/key components need not be independent or unit variance. Scaling does not guarantee that softmax never saturates or that gradients remain healthy in every setting. The tutorial's wording that the operation ensures gradients flow to all positions is too strong.

### 3.2 Tensor contracts

The source states the standard single-head, row-major contract:
- (X:(n,d))
- (W_Q,W_K:(d,d_k)), (W_V:(d,d_v))
- (Q,K:(n,d_k)), (V:(n,d_v))
- scores and weights: ((n,n))
- output: ((n,d_v))

This is correct and already covered by the canonical bilingual Q/K/V and scaled-attention lessons. Batch/head axes and fused projection storage are omitted.

### 3.3 Worked example and random initialization

The “The cat sat” trace uses hand-crafted four-dimensional input vectors and random projection matrices. It is useful for following data flow and intermediate tensors, but its feature labels are pedagogical scaffolding, not learned embedding dimensions. Random projections do not demonstrate learned linguistic behavior. The source correctly labels the random-init heatmap as meaningless, but later statements about trained verbs attending to arguments or pronouns attending to antecedents are not supported by a trained model, identified head, measured weights or experiment in this chapter.

### 3.4 Independent projections

The phrase “these projections operate independently” is ambiguous. Separate projection matrices and role-specific representations do not imply independently optimized parameters. Standard Transformer training optimizes the projections jointly through the shared training objective. The current LLM Lab page already states this distinction explicitly; preserve it as an adversarial wording fixture.

### 3.5 Scope and complexity

The tutorial's (O(n^2d_k)) score-computation statement describes the pairwise QK product term. It should not be mistaken for the entire attention-block cost, which also includes projections and value aggregation; memory depends on whether score matrices are materialized. Its claim that modern Transformers rely entirely on QKV attention is also too broad for architectures using alternative sequence-mixing mechanisms.

## 4. Cross-source comparison against existing LLM Lab coverage

Compared directly with:
- `site/en/queries-keys-values.qmd` and `site/fr/queries-keys-values.qmd`;
- `site/en/scaled-dot-product-attention.qmd` and `site/fr/scaled-dot-product-attention.qmd`;
- `site/en/attention-score-scaling.qmd` and `site/fr/attention-score-scaling.qmd`;
- the Q/K/V source collection, complementary-perspectives dossier and pedagogical coverage matrix.

| Source contribution | Existing treatment | Decision |
|---|---|---|
| Database lookup analogy | Index-card analogy already explains functional roles | Already covered; retain as alternative source perspective, do not stack analogies |
| Variance derivation and softmax concentration | Dedicated bilingual attention-score-scaling deep dive | Integrate by reference; no duplicated derivation. Retain assumptions and non-guarantee caveat |
| (d_k)/(d_v) tensor contract | Canonical Q/K/V page and tensor reference | Already covered |
| End-to-end Python trace | Canonical deterministic worked example and Build walkthrough | Integrate by reference; no second implementation or copied code |
| Random-init heatmap caveat | Existing warnings against interpreting attention weights causally | Clarify as a distinct epistemic point in source synthesis/regression tests; no page edit until learner gap is evidenced |
| “Operate independently” wording | Canonical page explicitly says separately parameterized but jointly optimized | Already covered; retain as adversarial regression fixture |
| Eleven-section teaching route | Existing route intentionally separates Q/K/V roles, score computation, scaling and Build | Integrate by reference as a comparison case; do not reorder canonical curriculum |
| Eight-question quiz | Only first question visible; existing #447 protocol and exercise hub exist | Defer assessment comparison until all items and feedback are inspectable |

## 5. Integration decision

No new canonical page, concept, relation, route edge, exercise or implementation is justified.

The strongest incremental contribution is the **assumption-explicit variance-to-softmax teaching chain**. It belongs conceptually with the existing attention-score-scaling deep dive, but that lesson already owns the topic. The correct integration is a traceable external reference, not duplicated text.

The source also contributes two useful workflow regression cases:
- distinguish separate parameterization from independent optimization;
- distinguish a random-initialization visualization from evidence about trained attention behavior.

At least one plausible learner-facing candidate was tested: adding the variance derivation to the core Q/K/V page would duplicate the dedicated scaling lesson and overload the conceptual entry point. The existing advanced scaling page is the appropriate owner; the external chapter can be linked there if a precise gap is found. This supports a justified no-op for canonical content.

## 6. Workflow transfer and effort record

This is an incremental source addition to an already populated Q/K/V collection, not a full rescan.

| Stage | Work performed | Human effort measurement |
|---|---|---|
| Discovery / identity | Canonical URL, author, title, dates, chapter metadata; dedup check against source catalogue | Active minutes not instrumented |
| Inspection | Eleven sections, visible code/output, figure descriptions, one comment, quiz visibility | Active minutes not instrumented |
| Extraction | One catalogue record, one structured extraction, 16 source-local nodes, 15 relations, six inferred outcomes, three prerequisites, eleven route steps, seven atomic items | Active minutes not instrumented |
| Comparison | Six canonical EN/FR pages plus existing source collection, coverage matrix and synthesis | Active minutes not instrumented |
| Decision | Item-level dispositions and one tested no-op candidate | Active minutes not instrumented |
| Validation | Schema validator and CI/Quarto on the final PR head | Pending at report creation |

**No elapsed-time or active-human-time estimate is fabricated.** Repository operations and artifact counts are reproducible, but they are not a proxy for human effort. The next iteration should record stage start/end timestamps, active review minutes, manual interventions, retries, blocked events and automated check outcomes. Waiting time should be reported separately from active work.

## 7. Method defects and follow-up

1. The page is mutable and lacks an immutable revision; retain access date and visible publication/update metadata.
2. Rendered code outputs invite a false reproducibility assumption; add a separate execution gate before treating them as reproducible.
3. The interactive quiz exposes only one of eight questions to the current retrieval path; keep quiz inspection partial.
4. The source's teaching route is long and integrated; the project should preserve its own depth split rather than copy the whole sequence.
5. Pedagogical quality remains unmeasured. The source's clear sequence is observable, but no learner task or outcome data establishes effectiveness.

## 8. Reproducibility

- Source: https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism
- Source catalogue: `data/sources.yml`
- Structured extraction: `data/extractions/brenndoerfer-query-key-value-attention-2025.yml`
- Q/K/V collection: `docs/source-reviews/qkv-source-collection.md`
- Coverage matrix: `docs/source-syntheses/qkv-pedagogical-coverage-matrix-2026-11.md`
- Existing method: `docs/workflows/source-to-knowledge-validation.md`
