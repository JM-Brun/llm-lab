# Source review: Nishanthan K — QKV in Transformers

**Source record:** nishanthan-k-qkv-transformers-devto  
**Extraction record:** data/extractions/nishanthan-k-qkv-transformers-devto.yml  
**Source:** [How Query, Key, and Value (QKV) Work in Transformers](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a)  
**Author:** Nishanthan K · **Publisher:** DEV Community · **Language:** English  
**Review date:** 2026-11-04

## 1. Inspection scope and confidence

The indexed article body was available in search output, covering the introduction, sections 1–6 and conclusion. Direct retrieval of the DEV page returned a cache miss. The publication year, update metadata, comments, linked materials and embedded visual assets were not independently inspected. The source is therefore registered as **partially scanned**, not fully scanned.

No reuse licence was established. The project records a link and short paraphrased extraction only; no article prose or illustration is reproduced.

## 2. What the source contributes

The article is a concise beginner-oriented walkthrough of:
- the functional distinction between Query, Key and Value;
- the shared input stream and learned projections Q = X W_Q, K = X W_K, V = X W_V;
- the score → scaling → softmax → weighted-value aggregation sequence;
- the high-level extension to multi-head attention;
- simple lexical-ambiguity and pronoun-reference examples.

It is broadly consistent with the standard scaled dot-product attention formulation. Its strongest value is as an accessible alternative explanation, not as a source of new technical results, implementation detail or empirical evidence.

## 3. Reconciliation with the current LLM Lab pages

The canonical bilingual Q/K/V page was inspected in both languages, together with the adjacent attention lesson, cross-attention lesson, Transformer overview and implementation walkthrough.

| Article contribution | Existing project coverage | Decision |
|---|---|---|
| Q, K and V are learned representations, not three token types | The Q/K/V lesson explicitly states this and distinguishes their roles | No change |
| Search analogy: query, matching key, retrieved value | The Q/K/V lesson already has an index-card analogy and explicitly limits it; a second search analogy would be redundant | Do not import |
| Shared input X, learned W_Q, W_K, W_V | The lesson gives the equations, matrix dimensions d_k and d_v, optional-bias caveat and shared representation stream | No change |
| Query-key scores, scaling, softmax and value aggregation | The next lesson gives tensor shapes, mask-aware equation, numerical example, scaling rationale and interpretive caveats | Keep on the next page; do not duplicate |
| Multi-head projections and output projection | Transformer overview and guided block walkthrough already cover heads, head slicing, isolation and W_O; the overview cautions against assuming human-interpretable head specialization | No change |
| bank ambiguity and pronoun it | The dedicated contextualized-representations page owns this learner question | No change without a demonstrated gap |
| KV-cache follow-up | Appears only as a reader comment in the indexed result, not as part of the article body; the computational-complexity page already covers KV-cache costs | Exclude from article extraction and attribution |

## 4. Technical assessment

The article's central equations and role distinctions are sound at the introductory level. Several points need careful interpretation if used elsewhere:

1. **X is not necessarily the raw embedding matrix.** It denotes the representation stream entering the attention sublayer; in later blocks it is a contextualized hidden state.
2. **The single-X equations describe self-attention.** In cross-attention, Q comes from the querying stream while K and V come from the source stream. The project already explains this separately.
3. **The scale factor has a more precise justification.** Under simplifying assumptions of independent, zero-mean, unit-variance components, the variance of a query-key dot product grows with d_k; division by sqrt(d_k) controls its scale. The adjacent project lesson already derives this.
4. **Attention weights are not semantic similarity or causal attribution.** The article includes a useful caveat about semantic similarity; the project makes the distinction more explicit.
5. **Head specialization is not guaranteed.** Grammatical or entity-focused heads are possible illustrative patterns, not an architectural guarantee. The existing Transformer overview already states this limitation.

## 5. Integration decision

**No change to the published Q/K/V page is warranted from this source.** The existing bilingual lesson is already more precise and better integrated into the learning route than the article. It covers the useful information without importing the article's simplifications or duplicating its examples.

No new concept, graph edge, page, figure, experiment or bibliography entry is created. The source and its atomic extraction records are retained for traceability and future discovery. All seven extraction items have explicit Phase B dispositions.

This is a valid outcome of the source-to-learning workflow: a source can be catalogued and reviewed without requiring a content change.

## 6. Validation still required

The source record and extraction file must be checked against the schema and taxonomy introduced in the dependent source-catalogue change. The Quarto pages are intentionally unchanged; their existing bilingual content and route are preserved.
