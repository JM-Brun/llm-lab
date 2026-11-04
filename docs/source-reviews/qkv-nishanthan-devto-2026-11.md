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

It is broadly consistent with the standard scaled dot-product attention formulation. It contributes no new technical result, implementation detail or empirical evidence. Its possible value is pedagogical: a concise verbal entry point, an introductory multi-head summary, and especially a two-example progression from lexical ambiguity to pronoun reference. These possibilities must be evaluated independently of topical novelty.

## 3. Reconciliation with the current LLM Lab pages

The canonical bilingual Q/K/V page was inspected in both languages, together with the adjacent attention lesson, cross-attention lesson, Transformer overview and implementation walkthrough.

| Contribution | Novelty | Complementarity / learner value | Existing coverage and decision |
|---|---|---|---|
| Verbal distinction among Q, K and V | Low | Moderate: concise narrative may be a useful pre-formal entry point | Defer; compare the exact opening before making a small editorial change |
| Search analogy | Low | Low: same matching-versus-retrieval mapping as the index-card analogy | Reject as redundant by explanatory function, not merely by topic |
| Shared input X and learned projections | Low | Low | Defer; canonical lesson already has equations, dimensions and self-/cross-attention caveats |
| Score → scale → softmax → aggregation | Low | Low | Keep in the dedicated attention lesson, which provides stronger derivation and numerical treatment |
| Multi-head summary | Low | Moderate as a simpler summary, but little additional learner value | Defer; current Transformer overview and block walkthrough already serve both levels |
| bank ambiguity → pronoun it | Low | Moderate: potentially useful progression from lexical ambiguity to cross-position reference | Defer, not reject; compare the actual examples and sequence on the contextualized-representations page before deciding |
| KV-cache follow-up | Not an article contribution | Not assessed as an article item | It appeared only in a reader comment in the indexed result; exclude from article extraction and attribution |

## 4. Technical assessment

The article's central equations and role distinctions are sound at the introductory level. Several points need careful interpretation if used elsewhere:

1. **X is not necessarily the raw embedding matrix.** It denotes the representation stream entering the attention sublayer; in later blocks it is a contextualized hidden state.
2. **The single-X equations describe self-attention.** In cross-attention, Q comes from the querying stream while K and V come from the source stream. The project already explains this separately.
3. **The scale factor has a more precise justification.** Under simplifying assumptions of independent, zero-mean, unit-variance components, the variance of a query-key dot product grows with d_k; division by sqrt(d_k) controls its scale. The adjacent project lesson already derives this.
4. **Attention weights are not semantic similarity or causal attribution.** The article includes a useful caveat about semantic similarity; the project makes the distinction more explicit.
5. **Head specialization is not guaranteed.** Grammatical or entity-focused heads are possible illustrative patterns, not an architectural guarantee. The existing Transformer overview already states this limitation.

## 5. Integration decision

**No immediate page edit is justified, but the source is not pedagogically empty.** The revised assessment identifies two possible complementary contributions: the article's concise verbal entry point for Q/K/V, and its paired examples moving from lexical ambiguity to pronoun reference. The latter is retained as a genuine candidate for a targeted comparison with the existing contextualized-representations page; it is deferred rather than dismissed.

The search analogy is rejected only after comparing its actual mapping and learner function with the existing index-card analogy. The mathematical and multi-head material remains deferred because the project already provides more complete treatments at the appropriate locations.

No new concept, graph edge, page, figure, experiment or bibliography entry is created. A small existing-page improvement may still be warranted after a focused side-by-side review of the contextualized-representations examples. The reader comment remains excluded from article-derived content.

This is the intended workflow outcome: preserve plausible complementary value during extraction, then make a reasoned integration decision without forcing publication.

## 6. Validation still required

The source record and extraction file must be checked against the source-catalogue contract. Each extracted item now carries a qualitative pedagogical assessment across novelty, complementarity, learner value, applicability, redundancy and evidence quality. The Quarto pages remain unchanged pending the targeted comparison noted above.
