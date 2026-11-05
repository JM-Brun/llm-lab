# Q/K/V source collection and comparative synthesis

**Status:** living dossier · **Last reviewed:** 2026-11-05  
**Scope:** external explanations of Query, Key, Value, self-attention and closely related mechanisms.

**Project self-assessment:** the [LLM Lab Q/K/V self-audit and comparative positioning](llm-lab-qkv-self-audit-2026-11.md) evaluates the canonical bilingual lesson as a potential public source, separately from this catalogue of external sources.  
**Purpose:** accumulate complementary perspectives without turning the public curriculum into a stack of duplicated tutorials.

This page is the entry point for the Q/K/V source collection. It is intentionally separate from the canonical concept graph and the learner route. Each source keeps its own extraction, evidence, pedagogical reconstruction and review record; this dossier compares their contributions across sources.

## 1. Source register

| Source ID | Source | Date | Source-specific extraction | Review | Current scan status |
|---|---|---|---|---|---|
| `nishanthan-k-qkv-transformers-devto` | [Nishanthan K — How Query, Key, and Value (QKV) Work in Transformers](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a) | Header shows Oct 22; year not independently verified | [YAML extraction](../../data/extractions/nishanthan-k-qkv-transformers-devto.yml) | [Review](qkv-nishanthan-devto-2026-11.md) | Partially scanned: DEV author text and two-comment thread directly inspected; Medium mirror exposes one unresolved image placeholder; linked resources, image bytes and rights unresolved |
| `neha-kk-understanding-qkv-medium` | [Neha KK — Understanding Queries, Keys and Values in Transformers](https://medium.com/@nkk18072004/understanding-queries-keys-and-values-in-transformers-149ed07c9f8b) | 2025-12-31 | [YAML extraction](../../data/extractions/neha-kk-understanding-qkv-medium.yml) | [Review](qkv-neha-kk-medium-2026-11.md) | Partially scanned: visible author text now directly reconciled against the live page-text view; actual figure files, linked resources and rights unresolved |
| `codefinity-qkv-course` | [Codefinity — Queries, Keys, and Values](https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/7ce26687-f7a7-4728-be33-7014c6c7b707/a5ac1dbf-dbec-4dd1-a8d6-f3d83cbb905b) | Course date not independently verified | [YAML extraction](../../data/extractions/codefinity-qkv-building-blocks.yml) | [Review](qkv-codefinity-course-2026-11.md) | Partially scanned: lesson and parent outline inspected; two interface SVG URLs identified but bytes/rights unresolved; full interactive course, other lessons, assignments and linked resources uninspected |
| `huggingface-transformers-kv-cache-explanation` | [Hugging Face Transformers — Caching](https://huggingface.co/docs/transformers/main/en/cache_explanation) | Living documentation | [Source catalogue](../../data/sources.yml) | [DEV review, community follow-up](qkv-nishanthan-devto-2026-11.md#7-follow-up-scan-reconciliation) | Partially scanned; technical follow-up source, not a third Q/K/V tutorial |

**Medium scan refinement (2026-11-05):** the canonical page is now directly readable through the page reader; the visible text reconciles with the earlier indexed snapshot. Four in-body image placements remain visible (three captioned figures and one uncaptioned placeholder), but none was retrieved as image bytes or visually inspected. A “No responses yet” state was visible at this recheck; this is point-in-time evidence only. The raw DOM, cover/hero asset and reuse rights remain unresolved.

**Important provenance rule:** the KV-cache suggestion is a reader-comment contribution associated with the DEV discussion. It is not part of Nishanthan's author-authored article and must not be attributed to him. Hugging Face documentation is a separate corroborating source.

## 1.1 Pedagogical coverage matrix

The [Q/K/V pedagogical coverage matrix](../source-syntheses/qkv-pedagogical-coverage-matrix-2026-11.md) maps learner questions against each scanned source and the current project. It distinguishes source coverage from project coverage, identifies genuine candidate improvements, and records explicit scan boundaries. Update it whenever a new source is fully reviewed or the canonical learning content changes.

## 2. Cross-source synthesis

The three tutorials converge on the standard introductory account:

- Q and K provide learned representations used to compute compatibility scores.
- V provides learned representations aggregated using the normalized attention weights.
- The usual sequence is score computation → scaling → normalization → weighted aggregation.
- Multi-head attention repeats attention computation across heads and combines the head outputs.

That agreement is useful pedagogical convergence, not independent experimental validation. Technical claims should be grounded in the primary Transformer formulation and suitable implementation/documentation sources, not counted as true because multiple tutorials repeat them.

### Complementary contributions

| Contribution | DEV / Nishanthan | Medium / Neha KK | Project decision |
|---|---|---|---|
| Search/database analogy | Search/retrieval framing | Database-search framing | Keep one canonical analogy; preserve alternatives in source extractions rather than stacking them on the lesson |
| Why separate Q/K/V? | Roles and learned projections | Explicitly foregrounds decoupling matching from payload | Clarify the rationale in the existing bilingual Q/K/V lesson |
| Linguistic motivation | Lexical ambiguity (*bank*) and pronoun reference | Pronoun *it* with candidate antecedents | Use the examples where they teach distinct learner difficulties; avoid repeating the same example on adjacent pages |
| Score-to-output calculation | Compact formula sequence | Compact four-step sequence | Keep the more detailed derivation, shapes and numerical workbench in the dedicated attention lesson |
| Multi-head attention | Concise architecture summary | Follow-on topic only | Preserve the project's depth split: overview first, tensor implementation in Build |
| Interpretability | Warns against semantic-similarity / winner-take-all readings | Broadly suggests attention maps aid interpretation | Retain the project's stronger caveat: weights are not, by themselves, causal explanations |
| Input representation | Shared representation stream | Uses “word embeddings” as shorthand | Use the canonical general notation for the current attention input; distinguish first-layer embeddings from later hidden states |
| Input representations / positional information | Uses word embeddings as Q/K/V input shorthand | Does not explain positional-information injection | The current bilingual Q/K/V pages now clarify current hidden states, first-block embeddings, and input-level versus RoPE-style positional mechanisms |
| Soft versus hard retrieval | “Closest matches” wording risks implying discrete selection | Four-step formula shows softmax-weighted aggregation | Preserve the distinction; existing attention lesson already teaches the weighted mixture |
| Directionality / asymmetry | Claims attention is directional/non-symmetric without a matrix example | Not developed | Defer a worked matrix example; qualify that distinct Q/K projections typically yield non-symmetric scores, not universally |
| KV cache | Reader comment, not article body | Not covered | Track as a separately sourced inference-efficiency topic |

## 2.1 Three-source comparison: differentiated pedagogical value

The collection now compares three introductory tutorials, not just their repeated definitions.

| Source | Strongest distinctive contribution | Example / teaching device | What it should change in the project |
|---|---|---|---|
| Nishanthan K (DEV) | Compact visual/functional walkthrough linking roles to the attention pipeline; explicit warnings against semantic-similarity and winner-take-all readings | Search/retrieval framing; bank ambiguity and pronoun reference | Keep the source as an optional alternative explanation; retain its misconception checks where they reinforce the canonical treatment. Its visual remains uninspected and is link-only. |
| Neha KK (Medium) | Explicit design question: why learn three projections, separating matching from payload; concise score-to-output sequence | Pronoun “it” with competing antecedents | The rationale is made explicit in the existing Q/K/V lesson; the pronoun example illustrates cross-position information flow, not measured coreference resolution. |
| Codefinity | Geometric perspective on query-key compatibility, plus a role-discrimination check | Q/K vector alignment; “bank” in a river context | Add the bounded geometric lens and contrast lexical polysemy with coreference; preserve its quiz distractor pattern for later exercise revision. |

### Cross-source distinctions worth preserving

1. **Role analogy versus vector geometry.** The search/database/index-card framing explains functional roles; geometric alignment explains the numerical objects compared. They are complementary levels, not competing definitions.
2. **Design rationale versus operation sequence.** Neha’s “why three?” framing explains why matching and payload have distinct learned projections. The four-step score/softmax/aggregation sequence explains what attention computes. Keep these as separate teaching questions.
3. **Coreference versus lexical polysemy.** A pronoun choosing an antecedent and a word choosing among senses are different language phenomena. Their juxtaposition broadens the learner’s understanding of contextual dependence.
4. **Soft weighting versus hard retrieval.** Nishanthan and Neha use retrieval-style language that can suggest selecting one nearest item; Codefinity’s alignment language can suggest cosine-only matching. The canonical treatment must retain the exact distinction: scaled dot products feed a softmax distribution over accessible positions, and the resulting weights aggregate values.
5. **Illustration versus evidence.** None of the linguistic examples demonstrates measured attention weights or proves that an individual head performs coreference resolution or word-sense disambiguation. They are explanatory scenarios only.

### Source-to-project disposition

- **Already integrated:** Neha’s matching-versus-payload rationale and pronoun example; Nishanthan’s contextual examples and misconception cautions; Codefinity’s optional geometric lens and bank/polysemy contrast.
- **Retain as references:** Codefinity’s Q/K/V role-confusion distractors for the next exercise revision; alternative database/search analogies in source-specific extractions.
- **Do not duplicate:** the complete score/scale/softmax/weighted-sum derivation, already owned by the scaled-dot-product-attention lesson.
- **Do not promote to canonical graph nodes:** no new stable mechanism is introduced by these tutorial perspectives; they enrich explanations and examples, not the semantic ontology.

See the [three-source complementary-perspectives synthesis](../source-syntheses/qkv-complementary-perspectives-2026-11.md) for the full comparison and integration rationale.

## 3. What changed in LLM Lab

### Learning content
- The Q/K/V explanation makes the separation between matching (Q/K) and payload (V) explicit, including Neha KK’s design rationale for learning these roles through separate projections.
- The optional geometric lens from Codefinity connects Q/K compatibility to the dot product, vector norms and angle, while distinguishing dot product from cosine similarity.
- A bounded pronoun-context example is used as an illustration of cross-position information flow; Codefinity’s bank example is contrasted with it as lexical polysemy rather than coreference.
- The example is explicitly not presented as evidence of measured attention, coreference resolution or interpretability.
- The attention equations and detailed computation remain in the dedicated scaled-dot-product-attention lesson.
- The current input to Q/K/V is described as the representation entering the attention sublayer, not always as raw token embeddings; positional information may be injected at different points, including mechanisms such as RoPE.

### Canonical knowledge model
The DEV comparison exposed that the concept registry did not give stable identities to several intermediate objects already taught in the lessons. The canonical graph now includes:
- `attention-score`
- `attention-weight`
- `scaled-dot-product-attention`
- `multi-head-attention`

These nodes formalize existing teaching; they do not imply that either tutorial introduced a new scientific mechanism. The semantic graph and pedagogical route remain distinct structures.

### Curriculum and navigation
No new Q/K/V page, curriculum stage, prerequisite edge, navigation edge, Build step or duplicated numerical explanation is justified by these three tutorials. The project route remains broader and more explicit than either article's local sequence.

## 4. Comparison dossier

The detailed source-graph and route crosswalk is maintained in [QKV tutorial: source learning graph and route comparison](qkv-learning-graph-comparison-2026-11.md). That dossier is the place to append detailed comparisons as further sources are scanned. This collection page should remain a concise index and synthesis, not another copy of every extraction.

## 5. Adding future Q/K/V sources

Every additional source must be added as a new row and a separate source-specific extraction/review. Do not overwrite prior source assessments when a new source disagrees. Instead:

1. Preserve the new source's author, URL, date/version, source type, retrieval method and scan limitations.
2. Reconstruct its author-authored content separately from comments, linked resources, captions, code and community contributions.
3. Build its source-local concept/process graph and teaching route; label inferred nodes, edges, prerequisites and outcomes as inferred.
4. Extract atomic claims/examples/analogies with locators, evidence, confidence, technical review and integration disposition.
5. Compare each candidate contribution with the canonical pages, concepts, routes, exercises, figures and Build implementation.
6. Update the cross-source matrix only after source-specific review is complete.
7. Record what changed, what was already covered, what was rejected, what is deferred, and why.
8. Keep scan status component-specific. Complete text extraction does not imply complete media, comment, link, metadata or rights inspection.

### Comparison dimensions to retain

- Conceptual roles and definitions
- Mathematical formulation and assumptions
- Computational/data-flow sequence
- Input representation and positional information
- Self-attention versus cross-attention
- Causal masking and accessible positions
- Single-head versus multi-head attention
- Examples, analogies and counterexamples
- Learning prerequisites and inferred outcomes
- Teaching sequence and cognitive load
- Exercises, numerical examples and experiments
- Implementation details, tensor shapes and performance
- Visual assets, accessibility, provenance and reuse rights
- Claims that require qualification or independent corroboration

### Contribution dispositions

Use one of the following for each atomic item:

- **Integrate** — a concrete learner-facing, scientific or implementation gap is addressed.
- **Integrate by reference** — useful alternative perspective, but the canonical lesson should not duplicate it.
- **Already covered** — no change; cite the stronger canonical treatment.
- **Defer** — potentially useful, but evidence, scope or prerequisites are insufficient.
- **Reject** — inaccurate, misleading, unsupported or not useful for the project's goals.

A source can be text-complete and still partially scanned. A contribution can be valuable without changing a page. A source can reveal a graph-modeling gap without changing the learner route.

## 6. Evidence and rights policy

- Distinguish direct page inspection, indexed text, author-controlled mirrors, repository source, comments and secondary summaries.
- Never describe indexed reconstruction as direct DOM inspection.
- Never infer absence of comments, links or media from a retrieval path that did not expose them.
- Record exact unresolved media scope; captions/placeholders are not inspected images.
- Do not copy or recreate third-party figures merely because attribution is possible. Link to the original until exact assets, creator and reuse terms are verified.
- Treat reader comments as separate provenance records and independently verify technical suggestions before integrating them.
- Prefer primary papers, official documentation and reproducible code for technical validation; tutorials are pedagogical sources, not authority by repetition.

## 7. Reusable integration artifacts

The collection is maintained using the [external-source integration workflow](../workflows/source-to-learning-system-integration.md) and its [standard deliverable templates](../workflows/templates/):

- [Source registration template](../workflows/templates/source-registration-template.yml)
- [Structured extraction template](../workflows/templates/source-extraction-template.yml)
- [Source review template](../workflows/templates/source-review-template.md)
- [Multi-source comparison template](../workflows/templates/multi-source-comparison-template.md)
- [Visual asset audit template](../workflows/templates/visual-asset-audit-template.md)

These are complementary records, not duplicate versions of the same document: catalogue = provenance; extraction = atomic evidence; review = technical/pedagogical judgement; comparison = cross-source synthesis; visual audit = media and rights.

## 8. Current follow-up queue

- [ ] Reinspect both original articles' actual embedded figures and stable asset URLs; record creator/licence/reuse status before any embedding.
- [x] Recheck the DEV comment thread: two top-level comments are directly visible (Jessica Williams's KV-cache suggestion and Nishanthan's acknowledgement). The suggestion remains attributed to the reader, not the article author.
- [ ] Verify DEV publication/update metadata if a reliable page or API snapshot becomes available.
- [ ] Pin and inspect the Hugging Face documentation revision and relevant cache implementation when the KV-cache topic is developed.
- [ ] Add future Q/K/V sources here and extend the comparison dossier without duplicating source-specific extraction.

## 9. Codefinity — “Queries, Keys, and Values: The Building Blocks” (2026-11-05)

[Codefinity lesson](https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/7ce26687-f7a7-4728-be33-7014c6c7b707/a5ac1dbf-dbec-4dd1-a8d6-f3d83cbb905b) · [structured extraction](../../data/extractions/codefinity-qkv-building-blocks.yml) · [source review](qkv-codefinity-course-2026-11.md) · [cross-source synthesis dossier](../source-syntheses/qkv-complementary-perspectives-2026-11.md)

**Scan status: partially scanned.** The visible lesson text was retrieved directly and the parent course outline was inspected. Linked image bytes, the interactive environment, other lesson bodies, assignments, linked resources and reuse rights remain uninspected.

### Differential contribution and integration

| Contribution | What it adds beyond current LLM Lab content | Integration |
|---|---|---|
| Q/K/V role definitions | Reinforces the canonical functional split but adds no new definition | Already covered; retain provenance |
| Geometric Q/K framing | A spatial/vector lens alongside the existing index-card analogy; bridges the conceptual role to dot-product geometry | Integrated as an optional collapsible note on both Q/K/V pages, with dot-product norms/angle and warnings against cosine/nearest-neighbour interpretations |
| Bank / river example | Lexical polysemy (competing senses of one word), distinct from the pronoun-coreference example already on the Q/K/V page | Integrated as a compact optional contrast on both pages; full bank discussion remains on contextualized-representations |
| Three-question knowledge check | Compact checks of Q/K/V purpose, dynamic attention versus pooling, and contextual aggregation | Retained as a future exercise-design reference; no duplicate quiz |
| Course-level sequence | Places Q/K/V between motivation and relevance scoring, then lists later attention topics | Confirms compatibility with current route; no route change from titles alone |

### What the combined explanation now offers

1. **Functional analogy:** index cards distinguish what Q, K and V do.
2. **Geometric perspective:** query/key vectors connect that role distinction to the dot product, with its magnitude-and-angle dependence.
3. **Linguistic transfer:** pronoun coreference and lexical polysemy illustrate two different reasons context matters.
4. **Formal computation:** the next page remains responsible for scaling, softmax, masking and weighted aggregation.

The new perspectives are optional and attributed. No canonical concept, graph edge, new page or route dependency is added. No source image is copied. The original examples remain illustrations, not evidence that one particular attention head performs a linguistic task.

The extraction and review preserve source-specific evidence and scan limitations. The cross-source dossier records the comparative reasoning and the contribution-to-page mapping.


## 10. Learning-impact baseline

The current bilingual lesson and exercise hub have been audited to distinguish existing coverage from genuine assessment gaps. The [Q/K/V learning-impact baseline and assessment plan](../source-syntheses/qkv-learning-impact-baseline-2026-11.md) proposes a small diagnostic bundle without claiming measured learning gains or duplicating existing projection/aggregation exercises.
