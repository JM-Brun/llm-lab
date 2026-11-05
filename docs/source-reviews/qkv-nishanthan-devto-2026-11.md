# Source review: Nishanthan K — QKV in Transformers

**Source record:** nishanthan-k-qkv-transformers-devto  
**Extraction record:** data/extractions/nishanthan-k-qkv-transformers-devto.yml  
**Source:** [How Query, Key, and Value (QKV) Work in Transformers](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a)  
**Author:** Nishanthan K · **Publisher:** DEV Community · **Language:** English  
**Review date:** 2026-11-04

## 1. Inspection scope and confidence

**Direct recheck — 2026-11-05:** the canonical DEV article is now readable through the page reader. Its metadata shows “Posted on Oct 22” and “Edited on Oct 22” (the year is not exposed in the retrieved header). The complete visible author-authored body, section sequence, equations, examples and multi-head summary were inspected directly. The page exposes two top-level comments: a reader comment by Jessica Williams proposing a KV-cache follow-up, and an author reply by Nishanthan dated Oct 26. The exact provenance and wording are recorded below. The visible article body contains no exposed pedagogical image placement in this page-reader rendering; the author-controlled Medium mirror separately exposes one in-body image placeholder. The image bytes/URL, whether the mirror placeholder corresponds to an asset absent from the DEV rendering, and reuse rights remain unresolved. The linked series articles were identified but not opened. The source therefore remains **partially scanned**, not fully scanned.

No reuse licence was established. The project records links and short paraphrased extraction only; it does not reproduce article prose, code or image files. The original visual is now linked from both bilingual Q/K/V lessons, so readers can consult it at its source.

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
| Verbal distinction among Q, K and V | Low | Moderate: concise narrative may be a useful pre-formal entry point | Reject as a new page edit; the existing Q/K/V page already provides the necessary role distinction |
| Search analogy | Low | Low: same matching-versus-retrieval mapping as the index-card analogy | Reject as redundant by explanatory function, not merely by topic |
| Shared input X and learned projections | Low | Low | Reject as a new page edit; the canonical lesson already has equations, dimensions and self-/cross-attention caveats |
| Score → scale → softmax → aggregation | Low | Low | Reject as a new page edit; retain the full computation in the dedicated attention lesson, which provides stronger derivation and numerical treatment |
| Multi-head summary | Low | Moderate as a simpler summary, but little additional learner value | Reject as a new page edit; the Transformer overview and block walkthrough already serve both levels |
| bank ambiguity → pronoun it | Low | High: lexical ambiguity and cross-position dependency are distinct learner intuitions | Integrate the pronoun example into both contextualized-representations pages, with an explicit caveat that it does not establish attention-head coreference resolution |
| Scores are not semantic similarity | Low | Moderate as a misconception guardrail; reinforces a distinction learners may miss | Reject as a new page edit; the Q/K/V page already warns against nearest-neighbour and semantic-relevance interpretations |
| Weighted aggregation is not argmax selection | Low | Moderate: explicit winner-take-all contrast can help beginners | Reject as a new page edit; the attention lesson's equation and numerical example already show weighted Value aggregation |
| KV-cache follow-up | Not an article contribution | Not assessed as an article item | It appeared only in a reader comment; exclude from article extraction and attribution |

## 4. Technical assessment

The article's central equations and role distinctions are sound at the introductory level. The full text also states that Q/K/V projection matrices are learned by backpropagation and gradient-based optimization, gives a qualitative motivation for scaling, and briefly mentions causal masking. These are now separate atomic extraction items. Several points need careful interpretation if used elsewhere:

1. **X is not necessarily the raw embedding matrix.** It denotes the representation stream entering the attention sublayer; in later blocks it is a contextualized hidden state.
2. **The single-X equations describe self-attention.** In cross-attention, Q comes from the querying stream while K and V come from the source stream. The project already explains this separately.
3. **The scale factor has a more precise justification.** Under simplifying assumptions of independent, zero-mean, unit-variance components, the variance of a query-key dot product grows with d_k; division by sqrt(d_k) controls its scale. The adjacent project lesson already derives this.
4. **Attention weights are not semantic similarity or causal attribution.** The article includes a useful caveat about semantic similarity; the project makes the distinction more explicit.
5. **Head specialization is not guaranteed.** Grammatical or entity-focused heads are possible illustrative patterns, not an architectural guarantee. The existing Transformer overview already states this limitation.

## 5. Integration decision

**A targeted page edit is justified.** The existing contextualized-representations lesson already uses lexical ambiguity (bank), while the pronoun example (it → the animal) adds a distinct cross-position dependency. Both language versions now include it as a bounded motivation, not as evidence that one attention head resolves coreference. The concise verbal Q/K/V framing is rejected as a new page edit because the current lesson already explains it more precisely; the source is now linked as an optional external visual reference.

The search analogy is rejected only after comparing its actual mapping and learner function with the existing index-card analogy. The mathematical and multi-head material is rejected as new page content because the project already provides more complete treatments at the appropriate locations.

At this initial page-integration stage, no new concept, graph edge, page, figure, experiment or bibliography entry was created. A later differential graph audit identified a separate modelling gap in LLM Lab's existing registry; the justified graph refinement is documented in section 9. The reader comment remains excluded from article-derived content.

This is the intended workflow outcome: preserve plausible complementary value during extraction, then make a reasoned integration decision without forcing publication.

## 6. Integration update

The targeted comparison found a real complementarity: the canonical page used lexical ambiguity (bank) but not cross-position pronoun reference. Both language versions now include the it → the animal example. The wording treats it as an illustration of contextual dependency, not evidence that a particular attention head performs coreference resolution. The extraction disposition is updated to integrate.

The article is cited as the pedagogical origin of the example, not as a primary scientific source. The source catalogue records the integration as partial because only the pronoun-reference contribution was integrated; other items were deferred or rejected. The source remains partially scanned because linked materials, embedded assets, publication metadata and reuse rights remain unverified.

## 7. Follow-up scan reconciliation

The earlier indexed-only and intermittent-access records are retained as history. On 2026-11-05, the canonical [DEV article](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a) became directly readable and exposed its two-comment thread. The article header says “Posted on Oct 22” and “Edited on Oct 22”; the year remains unverified from the visible header. The author-controlled [Medium mirror](https://nishanthan-k.medium.com/how-query-key-and-value-qkv-work-in-transformers-1274bfa14ea8) remains useful for cross-checking the text but exposes one in-body image placeholder not seen in the DEV article-body rendering. Neither view exposed the image bytes or stable image URL.

The KV-cache suggestion is a comment by Jessica Williams, not article-author content. Nishanthan's visible reply is a brief acknowledgement (“Thanks @williamsj04. Looking forward to KV cache mechanism!”), not a technical endorsement or validation. The reader suggestion remains a separate extraction item with `provenance.voice: reader-comment`, a comment locator and a parent-source reference; neither the suggestion nor the technical explanation is attributed to Nishanthan. Its technical lead has been checked independently against the [Hugging Face Transformers caching explanation](https://huggingface.co/docs/transformers/main/en/cache_explanation), registered as a separate source and extracted separately.

The technical interpretation is precise: during incremental causal decoding at position `t`, the current position produces `q_t`, `k_t` and `v_t`; `q_t` attends over the cached past keys/values together with the current `k_t`/`v_t`; then the current key and value are appended to the per-layer cache. Thus, “only a fresh Query” describes which query is needed for the incremental attention calculation; it does **not** mean that the current token's K and V are skipped. The cache reduces recomputation but consumes memory proportional to the retained K/V states; exact usage depends on model dimensions and cache strategy. This verification is grounded in the independent Hugging Face documentation, not in the QKV article or the commenter.

The source catalogue preserves earlier scan events and adds this recheck with its actual access limitations. The QKV article remains `partially-scanned`; its integration remains `partially-integrated`. The separate Hugging Face documentation source is also partial because the mutable `main` revision was not pinned and implementation variants were not exhaustively audited.

## 8. Visual asset follow-up

The visual remains the most important unresolved part of this source scan. The indexed result for the author's [Medium profile](https://nishanthan-k.medium.com/) lists two image entries carrying the QKV article title. However, opening the profile directly returned a stale snapshot (labelled 1.4 years old) that does not include the QKV article. The two image entries are therefore only search-index metadata in this pass; they do not expose underlying image bytes, a stable asset URL, captions, DOM positions or rights-holder information. They cannot yet be classified confidently as cover versus in-body media, nor confirmed as duplicate renditions of one asset.

The canonical DEV article HTML and its API endpoints were not retrievable in this recheck. The Medium mirror's indexed article text and profile metadata are insufficient to inspect the actual illustration. Therefore the image is still **not visually inspected**. The user's observation that it is more attractive than the current project diagram remains a useful review lead, not a verified visual comparison. No generic image-search result is substituted.

**Decision: use as an externally hosted visual reference; do not copy the file.** Both bilingual Q/K/V lessons now provide an explicitly attributed link to the author's Medium mirror, where the article and its associated illustration can be consulted. The original image bytes and stable asset URL are still unavailable to this scan, so the visual has not been independently inspected and cannot yet be compared on visual-design merits with `site/images/queries-keys-values.svg` and `site/images/queries-keys-values-en.svg`. This is a source link, not a claim that the image has been embedded or that reuse permission exists. If a direct asset URL and reuse permission are later established, the project can reconsider local embedding.

The extraction workflow now has explicit procedures for a retrieval ladder (canonical HTML/metadata, documented publisher API/RSS/JSON, then confirmed author-controlled mirror), exact media identity, and separate provenance for comments embedded in a parent source. A text scan, a mirror's image labels, and a visual inspection are three different evidence states.

## 9. Source learning graph and route comparison

The article's local concept/process graph and its implied learning route have now been reconstructed and compared with the canonical LLM Lab graph and route in [QKV source learning graph and route comparison](qkv-learning-graph-comparison-2026-11.md).

The comparison found no reason to copy the article's section order into the project: the current route already places contextualized representations and the Transformer overview before Q/K/V, then separates scaled attention and causal masking. The article's examples are already integrated in the contextualization lesson. Its compact multi-head overview is already served by the Transformer overview, with implementation depth in the block walkthrough.

It did reveal a representational gap in the canonical concept graph. Four stable concepts are now registered: `attention-score`, `attention-weight`, `scaled-dot-product-attention`, and `multi-head-attention`. Their bilingual definitions, canonical page mappings and typed relations make explicit distinctions that the existing lessons already teach. The QKV source record and relevant extraction items now reference these canonical IDs.

No new page or route edge was added. The graph change is a refinement of the project's existing conceptual model, not a new content requirement generated by the article.


## 10. Integration closure

**The article's pedagogical integration is complete; its source scan is not.** These are separate lifecycle dimensions and must remain separate in the catalogue.

The article's author-authored contributions have now all received a final disposition (11 atomic items: one integrated and ten rejected as unnecessary new edits):

| Extracted contribution | Final disposition | Integration outcome |
|---|---|---|
| Q/K/V role distinction | Rejected as a new edit | Already explained more precisely in the bilingual Q/K/V lesson |
| Shared-input learned projections | Rejected as a new edit | Equations, dimensions and self-/cross-attention boundary already covered |
| Scaled dot-product computation | Rejected as a new edit | Dedicated attention lesson provides fuller derivation and numerical treatment |
| Multi-head attention overview | Rejected as a new edit | Transformer overview and implementation walkthrough cover the conceptual and implementation levels |
| Search/document analogy | Rejected | Explanatory mapping duplicates the existing index-card analogy |
| Lexical ambiguity and pronoun reference | Integrated | The complementary pronoun-reference example is present in both contextualized-representations lessons |
| Attention score is not semantic similarity | Rejected as a new edit | Existing bilingual misconception guardrails are more precise |
| Weighted aggregation is not argmax | Rejected as a new edit | Existing equation and numerical example already demonstrate weighted aggregation |
| Q/K/V projections learned by backpropagation | Rejected as a new edit | Existing Q/K/V page identifies learned parameters; the gradients lesson owns optimization |
| Scaling prevents peaked softmax | Rejected as a new edit | Existing attention lesson derives the variance-based rationale more rigorously |
| Causal masking blocks future positions | Rejected as a new edit | Dedicated bilingual causal-masking lesson provides the full mechanism |

The reader-comment KV-cache lead remains **deferred** as a separately attributed community contribution, not as an unfinished article claim. Its technical content has been independently checked against the separately registered Hugging Face documentation source; it belongs in a future inference-efficiency learning destination, not in the introductory Q/K/V lesson.

The canonical graph refinement is complete: the four stable concepts and their typed relations are registered, linked to existing bilingual resources, and covered by the source-graph comparison dossier. The article's six-section teaching sequence was compared with the canonical guided route, page routes and Build route; no route or navigation change was justified. No new page, local visual asset or experiment is added merely to mirror the source; the external source link is an optional visual detour.

Accordingly, the parent article's `integration_status` is **integrated**: every author-authored contribution has been integrated or explicitly rejected as redundant. The separate KV-cache reader comment remains deferred. The article's `scan_status` remains **partially-scanned** because the embedded image has not been visually inspected, linked materials and publication metadata remain unverified, and reuse rights are unknown. This does not block the completed pedagogical integration, but it does block claiming a complete source audit or any figure reuse.

No source content has been deleted from the extraction record; rejected items remain available as provenance-backed corroborating evidence.


## 11. Final access recheck

A final public-web recheck on 2026-11-04 again returned a cache miss for the canonical DEV article page. The indexed DEV result nevertheless exposes the complete introduction, six numbered sections, conclusion and reader comment, consistent with the extraction already recorded. The author-controlled Medium mirror also exposes the complete article body. These indexed/mirror copies support text-level reconciliation, but do not establish successful direct retrieval of the canonical page.

The Medium profile search result now lists the QKV article and two image entries under its title. Opening the profile itself still returns a stale page snapshot that omits the QKV article; the image entries do not expose a stable original asset URL, image bytes, caption/placement or rights-holder information. Thus the visual inspection remains blocked. The direct DEV page and profile snapshot are evidence of access limitations, not grounds to infer the figure's content.

**Final scan boundary:** the article's text and visible comment are reconciled; the source-local graph and route are compared; all author-authored extraction items have final integration dispositions. The source remains partially scanned for the unretrieved comment/reply thread, external linked material, publication metadata, the actual visual asset and rights. No figure reuse is permitted on the current evidence.


## 12. Complete text extraction and remaining scan boundary

The author-authored text reconstruction is now marked **complete** in the extraction's `pedagogical_model.reconstruction`. It covers the introduction, all six numbered sections and the conclusion, using the full indexed DEV result and the matching author-controlled Medium mirror. This is deliberately distinct from the source record's `scan_status`, which remains `partially-scanned` because the asset/comment/metadata boundary is not fully resolved.

The extraction now explicitly records three details that were previously represented only indirectly:
- the Q/K/V projection matrices are learned through backpropagation and gradient-based optimization (Section 3);
- the scaling factor is motivated qualitatively by preventing large scores and overly peaked softmax distributions, without deriving the variance argument (Section 4);
- causal masking is mentioned as a future-position restriction before softmax, but is not developed as a separate mechanism (Section 4).

The source-local graph also now connects Q/K/V projections to a learning-process node for gradient-based optimization. These additions preserve the article's full instructional content without creating duplicate explanations in the public lessons.

The currently indexed result exposes the substantive KV-cache reader comment, which remains a separate community item. An earlier scan recorded a second visible comment and an author reply, but their exact text is not recoverable from the current snapshot. They are not reconstructed from memory or guessed. The parent source remains partially scanned until this thread can be re-opened and reconciled.

**Illustration handling:** the two Q/K/V lessons now link directly to the author-controlled Medium article and cite Nishanthan K and the DEV Community publication. This makes the source illustration accessible to readers at its origin without copying an uninspected image or implying a reuse licence. It is not yet an embedded project asset.
