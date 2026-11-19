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

## 7. Disposition and remaining work

- Source identity and structured extraction are proposed in the catalogue and extraction file.
- Keep article figures and prose link-only.
- No code reproduction or numerical verification is claimed.
- Compare all extracted items with the current canonical pages and graph before changing page content.
- Validate YAML and catalogue/extraction contracts with `site/tools/check_source_catalogue.py`, then run relevant CI.
- Inspect the embedded figures and original *Attention Is All You Need* reference in a separate visual/primary-source pass if those assets are needed.

**Overall judgement:** a useful introductory secondary explanation of attention's computational flow, with a strong Q/K versus V mental model. Its technical shortcuts should be corrected before any of its prose is reused pedagogically.
