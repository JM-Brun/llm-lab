# Jose Parreño Garcia — Understanding Transformers (Part 4): Attention is just a few matrices

**Source:** [Understanding Transformers (Part 4)](https://joseparreogarcia.substack.com/p/understanding-transformers-part-4)  
**Author:** Jose Parreño Garcia · **Publisher/date:** Substack, 20 June 2026  
**Inspection:** 19 November 2026 · complete visible author-authored article text  
**Structured extraction:** [YAML extraction](../../data/extractions/jose-parreno-garcia-understanding-transformers-part-4-2026.yml)

## 1. Executive assessment

An accessible introductory walkthrough of scaled dot-product self-attention. Its strongest contribution is the explicit separation between Q/K relevance scoring and V information aggregation, supported by a Netflix recommendation analogy and a worked cake/it example. The four computational stages are broadly correct, but several explanations need qualification.

**Decision: integrate by reference into existing bilingual Q/K/V, scaled-dot-product-attention and contextualized-representation lessons. Do not create new canonical concepts or duplicate pages.** Existing concepts cover the substance.

## 2. Inspection scope and limits

The complete visible article body was inspected, including its positional-encoding recap, Q/K/V analogy, learned projections, QK transpose, scaling, row-wise softmax, AV aggregation, multi-head discussion and conclusion. The article's visible series outline and metadata were also inspected.

The embedded figures were not retrieved as image bytes or visually inspected. Parts 1–3, the linked original paper, comments and external resources were not audited. No code or numerical example was executed. Text and figures remain link-only; no reuse licence was established.

## 3. Reconstructed mechanism

For one attention head:

\[
S = \frac{QK^\top}{\sqrt{d_k}},\qquad
A = \operatorname{softmax}(S),\qquad
O = AV.
\]

- Learned projections produce Q, K and V from input representations.
- QKᵀ yields compatibility logits, with one row per query and one column per key.
- Scaling by √d_k controls logit variance before softmax.
- Row-wise softmax yields nonnegative weights summing to one over key positions.
- Multiplication by V computes a weighted sum for each query; the result is a contextualized representation, not a probability.
- Multi-head attention repeats the operation with distinct learned projections, concatenates head outputs and conventionally applies an output projection W_O.

The source-local pedagogical graph and route are recorded separately in the extraction. They are not canonical concept-graph additions.

## 4. Technical assessment

### Correct and useful

- **Q/K/V role separation:** queries and keys determine compatibility; values carry the information being aggregated.
- **Matrix orientation:** QKᵀ produces query rows and key columns.
- **Scaling:** the standard denominator is √d_k, where d_k is the per-head key dimension.
- **Softmax:** normalization is row-wise over keys for each query.
- **Aggregation:** AV returns one weighted value vector per query; its entries may be negative or outside [0,1].
- **Multi-head motivation:** multiple learned subspaces can capture different patterns, although the example patterns are hypotheses rather than guaranteed head specializations.

### Corrections and qualifications

1. **Softmax does not itself learn richer token interactions.** It is a fixed nonlinear normalization of the logits. Learned Q/K projections and subsequent network layers provide the trainable representational capacity.
2. **Scaling is not simply protection from “exploding softmax”.** Under standard assumptions, dot-product variance grows with d_k; dividing by √d_k controls logit scale and helps avoid saturated softmax and weak gradients.
3. **Attention scores are not semantic similarity.** They are learned compatibility logits, dependent on projections, layer, head and context.
4. **The cake/it example is motivational, not empirical evidence of coreference resolution.** Attention weights alone do not establish a human-interpretable relation or causal explanation.
5. **The mask is not only a training-time option.** Causal masking is required whenever autoregressive predictions must not depend on future positions, including inference/prefill implementations that process multiple prompt positions together. Other masks also encode padding or task constraints.
6. **Parallelism needs a boundary.** Full-sequence training and prompt prefill can process positions in parallel subject to masks; autoregressive generation of new tokens remains sequential across time steps.
7. **Multi-head attention is incomplete as presented.** Standard MHA concatenates head outputs and applies a learned output projection W_O; dimensions are configuration-dependent.
8. **“The model builds meaning” is pedagogical shorthand.** The operation computes learned contextual representations. The example's named semantic features (noun, dessert, sentiment) are illustrative labels, not dimensions guaranteed to be explicitly represented.

## 5. Pedagogical assessment

**Strengths:** progressive derivation; approachable analogy; explicit matrix dimensions; clear warning that AV outputs are not probabilities; useful separation of scoring and aggregation.

**Limits:** the Netflix analogy can make continuous learned vectors sound like discrete labels; the pronoun example may overstate interpretability; the article omits output projection and detailed masking/inference distinctions.

## 6. Relationship to LLM Lab

| Contribution | Existing destination | Decision |
|---|---|---|
| Q/K/V roles and projections | [Q/K/V lessons](../../site/fr/queries-keys-values.qmd) and English counterpart | Reuse existing concepts; optional analogy |
| QKᵀ, scaling and softmax | [Scaled dot-product attention](../../site/fr/scaled-dot-product-attention.qmd) and English counterpart | Existing coverage; preserve technical corrections |
| AV and contextualized vectors | Contextualized-representations lessons | Already covered |
| Multi-head attention | Transformer block walkthrough | Existing destination; ensure W_O is represented |
| Parallelism and causal masking | Generation and causal-masking lessons | Cross-link/qualify, not a new page |

No new canonical concepts, pages, diagrams or route nodes are justified by this source alone. Reconcile the proposed links against current page/resource metadata before publishing any page changes.

### 6.1 Repository page-by-page comparison (19 November 2026)

The current bilingual pages were opened and checked against the extracted items. This confirms that the candidate destinations are real page-map IDs and that the core content is already present:

| Existing resource | Verified coverage | Consequence for this source |
|---|---|---|
| [Q/K/V — FR](../../site/fr/queries-keys-values.qmd) / [EN](../../site/en/queries-keys-values.qmd) | Contextual motivation, three roles, parallel learned projections, QKᵀ → scores → softmax → weights, weights × V → output; advanced dimensions and variants are routed to dedicated deep dives. | No duplicate explanation. The Netflix analogy is an optional source alternative, not a page gap. |
| [Scaled dot-product attention — FR](../../site/fr/scaled-dot-product-attention.qmd) / [EN](../../site/en/scaled-dot-product-attention.qmd) | Five-step computation, score/weight/output distinctions, scaling rationale, masking as a separate step, misconceptions and attention-weight interpretation limits. | Already more complete than the article's four-step summary. No page edit required. |
| [Contextualized representations — FR](../../site/fr/contextualized-representations.qmd) / [EN](../../site/en/contextualized-representations.qmd) | Position/context distinction, pronoun-reference example, explicit caveat that this does not prove an individual head resolves coreference. | The article's cake/it example is redundant in function; no second pronoun example is warranted. |
| [Causal masking — FR](../../site/fr/causal-masking.qmd) / [EN](../../site/en/causal-masking.qmd) | Lower-triangular access rule, mask before softmax, and parallel training without future-token leakage. | The article's training-only wording is already corrected by the existing page; link only. |
| [Transformer block Build — FR](../../site/fr/transformer-block-walkthrough.qmd) / [EN](../../site/en/transformer-block-walkthrough.qmd) | Explicit Q/K/V/O projections, head isolation until W_O, causal mask implementation, MHA/MQA/GQA/MLA and local/sparse variants. | The missing W_O and head-shape details are already implemented and explained. No new Build page. |
| [Build path — FR](../../site/fr/build-path.qmd) / [EN](../../site/en/build-path.qmd) | Existing guided construction route and milestones. | The article does not justify a new route node or milestone. |

**Page audit decision:** no bilingual Understand or Build page changes are justified. The source record's page links are navigational associations, not proposals to duplicate content. The canonical routes and resource graph remain unchanged.

### 6.2 Primary-source cross-check

The article's central equations and architecture were cross-checked against the already-catalogued primary source, Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), especially §§3.2.1–3.2.2 and Figure 2. The project already has the focused review [Vaswani attention formulation](vaswani-attention-formulation-2026-11.md), so no duplicate primary-source record or extraction was created.

The primary paper explicitly specifies:
- scaled dot-product attention as softmax(QKᵀ / √dₖ)V;
- the optional mask between scaling and softmax in Figure 2;
- multiple learned Q/K/V projections, parallel head computations, concatenation, and a final learned linear projection;
- the variance argument: under independent zero-mean, unit-variance components, q·k has variance dₖ, motivating division by √dₖ.

This confirms that the missing output projection W_O is a genuine omission in the article's brief MHA account, not a new feature proposed by LLM Lab. The article's broad parallelism wording remains subject to the causal-generation distinction documented in the existing masking and generation lessons.

## 7. Disposition and remaining work

- Source identity, structured extraction and source-local pedagogical graph are recorded in the catalogue and extraction file; the source is marked `reviewed` while remaining `partially-scanned` because article images are unresolved.
- Keep article figures and prose link-only.
- No code reproduction or numerical verification is claimed.
- The primary-source formulation and all eight bilingual Understand/Build destinations have now been checked; no page, concept, resource or route changes are warranted.
- The page-by-page comparison found the current canonical pages already cover all extracted technical content; retain the no-duplication decision.
- Validate YAML and catalogue/extraction contracts with `site/tools/check_source_catalogue.py`, then inspect the CI run for the final PR HEAD.
- Inspect the embedded figures only if visual integration is later proposed; their absence does not block link-only source registration.

**Overall judgement:** a useful introductory secondary explanation of attention's computational flow, with a strong Q/K versus V mental model. Its technical shortcuts should be corrected before any of its prose is reused pedagogically.
