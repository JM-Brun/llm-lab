# Source review: Nishanthan K — QKV in Transformers

**Source record:** nishanthan-k-qkv-transformers-devto  
**Extraction record:** data/extractions/nishanthan-k-qkv-transformers-devto.yml  
**Source:** [How Query, Key, and Value (QKV) Work in Transformers](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a)  
**Author:** Nishanthan K · **Publisher:** DEV Community · **Language:** English  
**Review date:** 2026-11-04

## 1. Inspection scope and confidence

The initial review used indexed article content covering the introduction, sections 1–6 and conclusion. At that point direct retrieval returned a cache miss, and the source was correctly recorded as partially scanned.

A follow-up inspection on 2026-11-04 successfully retrieved the DEV article directly. It confirmed the same complete article body and allowed inspection of the two visible reader comments and the author's reply. The publication year and update metadata remain unverified. Linked series articles, other external materials and embedded visual assets were not inspected separately. The source therefore remains **partially scanned**, not fully scanned.

No reuse licence was established. The project records a link and short paraphrased extraction only; no article prose, code or illustration is reproduced.

## 2. What the source contributes

The article is a concise beginner-oriented walkthrough of:
- the functional distinction between Query, Key and Value;
- the shared input stream and learned projections Q = X W_Q, K = X W_K, V = X W_V;
- the score → scaling → softmax → weighted-value aggregation sequence;
- the high-level extension to multi-head attention;
- simple lexical-ambiguity and pronoun-reference examples.
- two interpretive caveats: query-key scores are not direct semantic-similarity measures, and standard attention performs weighted Value aggregation rather than winner-take-all selection.

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
| Scores are not semantic similarity | Low | Moderate as a misconception guardrail; reinforces a distinction learners may miss | Defer; Q/K/V page already warns against nearest-neighbour and semantic-relevance interpretations |
| Weighted aggregation is not argmax selection | Low | Moderate: explicit winner-take-all contrast can help beginners | Defer; the attention lesson's equation and numerical example already show weighted Value aggregation |
| KV-cache follow-up | Not an article contribution | Not assessed as an article item | It appeared only in a reader comment; exclude from article extraction and attribution |

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

At this initial page-integration stage, no new concept, graph edge, page, figure, experiment or bibliography entry was created. A later differential graph audit identified a separate modelling gap in LLM Lab's existing registry; the justified graph refinement is documented in section 9. The reader comment remains excluded from article-derived content.

This is the intended workflow outcome: preserve plausible complementary value during extraction, then make a reasoned integration decision without forcing publication.

## 6. Integration update

The targeted comparison found a real complementarity: the canonical page used lexical ambiguity (bank) but not cross-position pronoun reference. Both language versions now include the it → the animal example. The wording treats it as an illustration of contextual dependency, not evidence that a particular attention head performs coreference resolution. The extraction disposition is updated to integrate.

The article is cited as the pedagogical origin of the example, not as a primary scientific source. The source catalogue records the integration as partial because only the pronoun-reference contribution was integrated; other items were deferred or rejected. The source remains partially scanned because linked materials, embedded assets, publication metadata and reuse rights remain unverified.

## 7. Follow-up scan reconciliation

The initial review records a direct article-body inspection and two visible reader comments plus the author's reply. On the latest recheck (2026-11-04), the canonical DEV page and the DEV API endpoints were not retrievable through the available page reader (cache miss / inaccessible endpoint). The complete article body remains available through indexed DEV search content and the author-controlled [Medium mirror](https://nishanthan-k.medium.com/how-query-key-and-value-qkv-work-in-transformers-1274bfa14ea8). The current indexed result exposes the KV-cache comment; the earlier comment/reply inspection remains recorded as a separate historical event. The publication year and update metadata remain unverified.

The KV-cache suggestion is now preserved as its own extraction item, with `provenance.voice: reader-comment`, a comment locator and a parent-source reference. It is not attributed to the article author. Its technical lead has been checked independently against the [Hugging Face Transformers caching explanation](https://huggingface.co/docs/transformers/main/en/cache_explanation), registered as a separate source and extracted separately.

The technical interpretation is precise: during incremental causal decoding at position `t`, the current position produces `q_t`, `k_t` and `v_t`; `q_t` attends over the cached past keys/values together with the current `k_t`/`v_t); then the current key and value are appended to the per-layer cache. Thus, “only a fresh Query” describes which query is needed for the incremental attention calculation; it does **not** mean that the current token's K and V are skipped. The cache reduces recomputation but consumes memory proportional to the retained K/V states; exact usage depends on model dimensions and cache strategy. This verification is grounded in the independent Hugging Face documentation, not in the QKV article or the commenter.

The source catalogue preserves earlier scan events and adds this recheck with its actual access limitations. The QKV article remains `partially-scanned`; its integration remains `partially-integrated`. The separate Hugging Face documentation source is also partial because the mutable `main` revision was not pinned and implementation variants were not exhaustively audited.

## 8. Visual asset follow-up

The visual remains the most important unresolved part of this source scan. The indexed result for the author's [Medium profile](https://nishanthan-k.medium.com/) lists two image entries carrying the QKV article title. However, opening the profile directly returned a stale snapshot (labelled 1.4 years old) that does not include the QKV article. The two image entries are therefore only search-index metadata in this pass; they do not expose underlying image bytes, a stable asset URL, captions, DOM positions or rights-holder information. They cannot yet be classified confidently as cover versus in-body media, nor confirmed as duplicate renditions of one asset.

The canonical DEV article HTML and its API endpoints were not retrievable in this recheck. The Medium mirror's indexed article text and profile metadata are insufficient to inspect the actual illustration. Therefore the image is still **not visually inspected**. The user's observation that it is more attractive than the current project diagram remains a useful review lead, not a verified visual comparison. No generic image-search result is substituted.

**Decision: inspection pending; no reuse.** The next successful retrieval must identify the exact image URL and its position in the article, download/open the original at readable resolution, compare the visual's information design with `site/images/queries-keys-values.svg` and `site/images/queries-keys-values-en.svg`, and separately establish creator and reuse rights. If the visual is pedagogically stronger but reuse rights remain unclear, link to it and design an independent visual from the underlying concept without tracing or cosmetically altering the source.

The extraction workflow now has explicit procedures for a retrieval ladder (canonical HTML/metadata, documented publisher API/RSS/JSON, then confirmed author-controlled mirror), exact media identity, and separate provenance for comments embedded in a parent source. A text scan, a mirror's image labels, and a visual inspection are three different evidence states.

## 9. Source learning graph and route comparison

The article's local concept/process graph and its implied learning route have now been reconstructed and compared with the canonical LLM Lab graph and route in [QKV source learning graph and route comparison](qkv-learning-graph-comparison-2026-11.md).

The comparison found no reason to copy the article's section order into the project: the current route already places contextualized representations and the Transformer overview before Q/K/V, then separates scaled attention and causal masking. The article's examples are already integrated in the contextualization lesson. Its compact multi-head overview is already served by the Transformer overview, with implementation depth in the block walkthrough.

It did reveal a representational gap in the canonical concept graph. Four stable concepts are now registered: `attention-score`, `attention-weight`, `scaled-dot-product-attention`, and `multi-head-attention`. Their bilingual definitions, canonical page mappings and typed relations make explicit distinctions that the existing lessons already teach. The QKV source record and relevant extraction items now reference these canonical IDs.

No new page or route edge was added. The graph change is a refinement of the project's existing conceptual model, not a new content requirement generated by the article.
