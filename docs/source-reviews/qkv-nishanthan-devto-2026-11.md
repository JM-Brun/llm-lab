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
| bank ambiguity → pronoun it | Low | High: lexical ambiguity and cross-position dependency are distinct learner intuitions | Integrate the pronoun example into both contextualized-representations pages, with an explicit caveat that it does not establish attention-head coreference resolution |
| KV-cache follow-up | Not an article contribution | Not assessed as an article item | It appeared only in a reader comment in the indexed result; exclude from article extraction and attribution |

## 4. Technical assessment

The article's central equations and role distinctions are sound at the introductory level. Several points need careful interpretation if used elsewhere:

1. **X is not necessarily the raw embedding matrix.** It denotes the representation stream entering the attention sublayer; in later blocks it is a contextualized hidden state.
2. **The single-X equations describe self-attention.** In cross-attention, Q comes from the querying stream while K and V come from the source stream. The project already explains this separately.
3. **The scale factor has a more precise justification.** Under simplifying assumptions of independent, zero-mean, unit-variance components, the variance of a query-key dot product grows with d_k; division by sqrt(d_k) controls its scale. The adjacent project lesson already derives this.
4. **Attention weights are not semantic similarity or causal attribution.** The article includes a useful caveat about semantic similarity; the project makes the distinction more explicit.
5. **Head specialization is not guaranteed.** Grammatical or entity-focused heads are possible illustrative patterns, not an architectural guarantee. The existing Transformer overview already states this limitation.

## 5. Integration decision

**A targeted page edit is justified.** The existing contextualized-representations lesson already uses lexical ambiguity (bank), while the pronoun example (it → the animal) adds a distinct cross-position dependency. Both language versions now include it as a bounded motivation, not as evidence that one attention head resolves coreference. The concise verbal Q/K/V framing remains deferred pending a separate learner-benefit comparison.

The search analogy is rejected only after comparing its actual mapping and learner function with the existing index-card analogy. The mathematical and multi-head material remains deferred because the project already provides more complete treatments at the appropriate locations.

No new concept, graph edge, page, figure, experiment or bibliography entry is created. The reader comment remains excluded from article-derived content.

This is the intended workflow outcome: preserve plausible complementary value during extraction, then make a reasoned integration decision without forcing publication.

## 6. Integration update

The targeted comparison found a real complementarity: the canonical page used lexical ambiguity (bank) but not cross-position pronoun reference. Both language versions now include the it → the animal example. The wording treats it as an illustration of contextual dependency, not evidence that a particular attention head performs coreference resolution. The extraction disposition is updated to integrate.

The article remains partially scanned. Its licence, embedded visual assets, comments and linked materials remain unverified; no article figure or code was reused. The article is cited as the pedagogical origin of the example, not as a primary scientific source.
