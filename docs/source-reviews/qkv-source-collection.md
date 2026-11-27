# Q/K/V source collection and comparative synthesis

**Status:** living dossier · **Last reviewed:** 2026-11-27  
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
| `mbrenndoerfer-qkv-attention-mechanism` | [Michael Brenndoerfer — Query, Key, Value: The Foundation of Transformer Attention](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism) | 2025-06-01; updated 2025-06-04 | [YAML extraction](../../data/extractions/mbrenndoerfer-qkv-attention-mechanism.yml) | [Review](qkv-mbrenndoerfer-2026-11.md) · [Visual inventory](qkv-brenndoerfer-visual-inventory-2026-11.md) | Partially scanned: chapter text inspected; nine visual teaching moves inventoried but original assets/rights unresolved; code not executed; quiz interactions and linked resources uninspected |
| `zsombor-veres-lakos-attention-from-scratch-2026` | [Zsombor Veres-Lakos — Attention from scratch](https://zsomborvereslakos.substack.com/p/attention-from-scratch) | 2026-11-16 | [YAML extraction](../../data/extractions/zsombor-veres-lakos-attention-from-scratch-2026.yml) | [Review](zsombor-veres-lakos-attention-from-scratch-2026-11.md) | Partially scanned: complete 12-page PDF inspected, including worked matrices and figures; live page, comments, links and reuse rights unresolved |
| `huggingface-transformers-kv-cache-explanation` | [Hugging Face Transformers — Caching](https://huggingface.co/docs/transformers/main/en/cache_explanation) | Living documentation | [Source catalogue](../../data/sources.yml) | [DEV review, community follow-up](qkv-nishanthan-devto-2026-11.md#7-follow-up-scan-reconciliation) | Partially scanned; technical follow-up source, not an additional Q/K/V tutorial |

**Medium scan refinement (2026-11-05):** the canonical page is now directly readable through the page reader; the visible text reconciles with the earlier indexed snapshot. Four in-body image placements remain visible (three captioned figures and one uncaptioned placeholder), but none was retrieved as image bytes or visually inspected. A “No responses yet” state was visible at this recheck; this is point-in-time evidence only. The raw DOM, cover/hero asset and reuse rights remain unresolved.

**Important provenance rule:** the KV-cache suggestion is a reader-comment contribution associated with the DEV discussion. It is not part of Nishanthan's author-authored article and must not be attributed to him. Hugging Face documentation is a separate corroborating source.

## 1.1 Pedagogical coverage matrix

The [Q/K/V pedagogical coverage matrix](../source-syntheses/qkv-pedagogical-coverage-matrix-2026-11.md) maps learner questions against each scanned source and the current project. It distinguishes source coverage from project coverage, identifies genuine candidate improvements, and records explicit scan boundaries. Update it whenever a new source is fully reviewed or the canonical learning content changes.

## 2. Cross-source synthesis

The three initial tutorials converge on the standard introductory account; Brenndoerfer is compared separately in section 10 and in the four-source audit:

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

## 2.1 Three-source baseline: differentiated pedagogical value

The collection now compares three introductory tutorials, not just their repeated definitions.

| Source | Strongest distinctive contribution | Example / teaching device | What it should change in the project |
|---|---|---|---|
| Nishanthan K (DEV) | Compact visual/functional walkthrough linking roles to the attention pipeline; explicit warnings against semantic-similarity and winner-take-all readings | Search/retrieval framing; bank ambiguity and pronoun reference | Keep the article as a reader-facing visual reference. Its role, projection and misconception items are rejected as redundant; its context-example item is not integrated as a distinct Nishanthan-specific page contribution. The illustration was visually inspected on 2026-11-12 but remains link-only because reuse rights are unknown. |
| Neha KK (Medium) | Explicit design question: why learn three projections, separating matching from payload; concise score-to-output sequence | Pronoun “it” with competing antecedents | The rationale is made explicit in the existing Q/K/V lesson; the pronoun example illustrates cross-position information flow, not measured coreference resolution. |
| Codefinity | Geometric perspective on query-key compatibility, plus a role-discrimination check | Q/K vector alignment; “bank” in a river context | Add the bounded geometric lens and contrast lexical polysemy with coreference; preserve its quiz distractor pattern for later exercise revision. |

### Cross-source distinctions worth preserving

1. **Role analogy versus vector geometry.** The search/database/index-card framing explains functional roles; geometric alignment explains the numerical objects compared. They are complementary levels, not competing definitions.
2. **Design rationale versus operation sequence.** Neha’s “why three?” framing explains why matching and payload have distinct learned projections. The four-step score/softmax/aggregation sequence explains what attention computes. Keep these as separate teaching questions.
3. **Coreference versus lexical polysemy.** A pronoun choosing an antecedent and a word choosing among senses are different language phenomena. Their juxtaposition broadens the learner’s understanding of contextual dependence.
4. **Soft weighting versus hard retrieval.** Nishanthan and Neha use retrieval-style language that can suggest selecting one nearest item; Codefinity’s alignment language can suggest cosine-only matching. The canonical treatment must retain the exact distinction: scaled dot products feed a softmax distribution over accessible positions, and the resulting weights aggregate values.
5. **Illustration versus evidence.** None of the linguistic examples demonstrates measured attention weights or proves that an individual head performs coreference resolution or word-sense disambiguation. They are explanatory scenarios only.

### Source-to-project disposition

- **Integrated in current pages:** Neha’s role-decoupling clarification and pronoun example; Codefinity’s geometric lens and bank/river example in the advanced Q/K/V deep dive; Brenndoerfer’s routing/payload distinction in the core Q/K/V prose.
- **Not integrated as new page content:** Nishanthan’s role, shared-projection, computation and misconception items are rejected as redundant; its combined context-example item is also rejected as a distinct page edit. The DEV article remains a reader-facing visual reference.
- **Retain as references:** Codefinity’s Q/K/V role-confusion distractors for the next exercise revision; alternative database/search analogies in source-specific extractions.
- **Do not duplicate:** the complete score/scale/softmax/weighted-sum derivation, already owned by the scaled-dot-product-attention lesson.
- **Do not promote to canonical graph nodes:** no new stable mechanism is introduced by these tutorial perspectives; they enrich explanations and examples, not the semantic ontology.

See the [initial three-source complementary-perspectives synthesis](../source-syntheses/qkv-complementary-perspectives-2026-11.md) for that baseline, and the [four-source comparison and canonical-page audit](../source-syntheses/qkv-four-source-comparison-2026-11.md) for the reconciled four-source view.

## 3. What changed in LLM Lab

### Learning content
- The Q/K/V explanation makes the separation between matching (Q/K) and payload (V) explicit, including Neha KK’s design rationale for learning these roles through separate projections.
- The Codefinity geometric lens is located in the advanced Q/K/V deep dive, where it connects Q/K compatibility to the dot product, vector norms and angle and distinguishes dot product from cosine similarity; it is not a collapsible note on the core lesson.
- The core Q/K/V page's pronoun-context example is explicitly adapted from Neha KK. The Codefinity bank/river example appears in the advanced Q/K/V deep dive; it is not owned by the current contextualized-representations pages.
- Both linguistic examples remain illustrations, not evidence of measured attention, coreference resolution or interpretability.
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
No new Q/K/V page, curriculum stage, prerequisite edge, navigation edge, Build step or duplicated numerical explanation is justified by these four tutorials. The project route remains broader and more explicit than either article's local sequence.

## 4. Comparison dossier

The detailed source-graph and route crosswalk is maintained in [QKV tutorial: source learning graph and route comparison](qkv-learning-graph-comparison-2026-11.md). The current four-source pedagogical and canonical-page comparison is in the [four-source audit](../source-syntheses/qkv-four-source-comparison-2026-11.md). That dossier is the place to append detailed comparisons as further sources are scanned. This collection page should remain a concise index and synthesis, not another copy of every extraction.

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
| Geometric Q/K framing | A spatial/vector lens alongside the existing index-card analogy; bridges the conceptual role to dot-product geometry | Integrated in the advanced Q/K/V deep dive in both languages; not a collapsible note on the core lesson |
| Bank / river example | Lexical polysemy (competing senses of one word), distinct from the pronoun-coreference example on the core Q/K/V page | Integrated in the advanced Q/K/V deep dive in both languages; not owned by the current contextualized-representations pages |
| Three-question knowledge check | Compact checks of Q/K/V purpose, dynamic attention versus pooling, and contextual aggregation | Retained as a future exercise-design reference; no duplicate quiz |
| Course-level sequence | Places Q/K/V between motivation and relevance scoring, then lists later attention topics | Confirms compatibility with current route; no route change from titles alone |

### What the combined explanation now offers

1. **Core intuition:** the core Q/K/V lesson uses one functional analogy and a pronoun-coreference motivation.
2. **Advanced geometry:** the advanced Q/K/V deep dive connects query/key vectors to the dot product, with its magnitude-and-angle dependence.
3. **Advanced linguistic transfer:** the advanced deep dive uses bank/river lexical ambiguity; the core pronoun example is attributed to Neha KK.
4. **Formal computation:** the next page remains responsible for scaling, softmax, masking and weighted aggregation.

The new perspectives are optional and attributed. No canonical concept, graph edge, new page or route dependency is added. No source image is copied. The original examples remain illustrations, not evidence that one particular attention head performs a linguistic task.

The extraction and review preserve source-specific evidence and scan limitations. The cross-source dossier records the comparative reasoning and the contribution-to-page mapping.


## 10. Learning-impact baseline

The current bilingual lesson and exercise hub have been audited to distinguish existing coverage from genuine assessment gaps. The [Q/K/V learning-impact baseline and assessment plan](../source-syntheses/qkv-learning-impact-baseline-2026-11.md) proposes a small diagnostic bundle without claiming measured learning gains or duplicating existing projection/aggregation exercises.


## 11. Michael Brenndoerfer — “Query, Key, Value: The Foundation of Transformer Attention” (2026-11-05)

[Canonical chapter](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism) · [structured extraction](../../data/extractions/mbrenndoerfer-qkv-attention-mechanism.yml) · [source review](qkv-mbrenndoerfer-2026-11.md) · [incremental workflow pilot report](../source-syntheses/qkv-incremental-source-pilot-2026-11-05.md)

**Scan status: partially scanned.** The 11-section chapter's visible text, equations, selected code/output blocks, worked example, limitations and quiz section were inspected. Code was not executed; the visualizations were not inspected as image files; interactive controls, quiz feedback, comments, linked references and rights remain unresolved.

### Differential contribution

| Contribution | Comparison with current LLM Lab | Decision |
|---|---|---|
| Database/library lookup analogy | Same functional role mapping as the canonical index-card analogy; carries the same hard-retrieval risk | Already covered; do not stack another analogy |
| Variance derivation for the scale factor | Explicitly derives Var(qᵀk)=d_k under independence and unit-variance assumptions | Integrate by reference as optional intermediate depth; do not duplicate the attention lesson |
| Tensor shape walkthrough | Alternative compact reference; canonical Build/attention material already owns shape reasoning | Already covered |
| Full “The cat sat” numerical trace | Useful transparent trace, but duplicates the existing workbench; random weights are not learned linguistic behavior | Integrate by reference; preserve the random-vs-trained caveat |
| Convex-hull property | Valid for each normalized weighted sum over that row's value vectors, before later projections/residual/MLP | Defer until a learner task justifies geometric depth |
| Broad symmetry and learned-head claims | Several statements need qualification around masks, positional mechanisms, softmax nonlinearity and evidence for linguistic specialization | Keep as source-review regression examples; no learner-facing rebuttal page |

### Workflow result

The fourth Q/K/V tutorial was processed without a new registry, concept, page or route edge. The source-local model reconstructs the 11-section route. Six selected items have explicit dispositions. The candidate scaling derivation was tested against the canonical lesson and retained as a reference rather than copied into the page.

The pilot identifies two operational improvements only: record text reconstruction completeness separately from whole-source inspection, and record effort by workflow phase. No new skill, taxonomy or composite score is justified. See the pilot report for coverage, effort and remaining validation gates.


## 12. Page-level diversity and coverage audit — 2026-11-27

**Audit owner:** issue [#1741 — page-level source diversity, complementarity and blind-spot audit](https://github.com/JM-Brun/llm-lab/issues/1741).  
**Pilot pages:** [Q/K/V FR](../../site/fr/queries-keys-values.qmd) · [Q/K/V EN](../../site/en/queries-keys-values.qmd).  
**Method:** reconcile page-visible citations, source catalogue associations, the four-resource pedagogical comparison corpus, source-specific reviews and claim-level primary-source reviews. This is a review of repository artefacts; it does not repeat external scans, inspect unavailable image bytes, execute code or validate learner outcomes.

### 12.1 Four distinct source sets

Do not use “the page's sources” as if it denoted one unambiguous set.

| Set | Definition | Q/K/V pilot result |
|---|---|---|
| Page-visible citations | External URLs explicitly cited in the published page body | Four URLs, identical in FR and EN: Neha KK, Jose Parreño Garcia, Vaswani et al., Nishanthan K |
| Construction/comparison corpus | Sources whose contributions were inspected and compared while shaping the explanation | Four tutorial sources in the historical matrix: Nishanthan, Neha, Codefinity and Brenndoerfer; Jose was reviewed later and should be reconciled with that matrix |
| Canonical primary/technical evidence | Sources used to support specific technical claims, equations or implementation behavior | Vaswani et al. is the primary formulation anchor; its focused review now covers §§3.2.1–3.2.3 for attention computation, learned per-head projections and self-attention data flow; this is not a complete paper review |
| Thematic associations | Sources linked to a page through the source catalogue's related-page associations | A broader discovery set; association alone does not prove page use, citation or claim support |

The Hugging Face KV-cache documentation belongs primarily to the generation/inference topic. It is not an additional Q/K/V explanatory tutorial and must not inflate the Q/K/V diversity count.

The catalogue's `related.pages` field is a topic/page association, not a typed claim that the source was cited, inspected for this page, used during construction or recommended to the learner. The audit must preserve this distinction rather than infer use from association.

**Collection contract (resolved 2026-11-27):** `qkv-attention` identifies the curated source set selected to construct or technically ground the Q/K/V lesson; it is not a synonym for every resource whose `related.pages` happens to mention Q/K/V. Membership includes the four bounded pedagogical comparison resources (Nishanthan, Neha, Codefinity, Brenndoerfer), the later cited pedagogical source Jose Parreño Garcia, and the primary technical anchor Vaswani et al. The four-source comparison matrix remains intentionally bounded to its original four pedagogical resources. The broader collection and the comparison subset therefore have different, explicit scopes. The KV-cache documentation and general attention/visualization resources remain related or adjacent resources unless they are deliberately selected for a Q/K/V claim or construction decision.

### 12.2 Sources compared for construction

| Source | Type / origin | Language | Recorded level | Distinct function | Scan / integration |
|---|---|---|---|---|---|
| Nishanthan K, DEV | Blog / DEV Community | English | Introductory | Functional walkthrough, visual/pipeline framing, misconception warnings | Partially scanned / integrated |
| Neha KK, Medium | Blog / Medium | English | Introductory | Design rationale for separate projections; contextual/coreference example | Partially scanned / integrated |
| Codefinity | Course / Codefinity | English | Mixed | Concise role explanation, geometric alignment lens, formative-check patterns | Partially scanned / integrated |
| Michael Brenndoerfer | Tutorial / Language AI Handbook | English | Intermediate | Variance derivation, tensor shapes, numerical trace, aggregation geometry and implementation perspective | Partially scanned / reviewed |

The four records have distinct creators/platforms and distinct teaching contributions. The metadata shows a genuine variety of source types (two blogs, one course, one tutorial), but all four are English-language secondary teaching resources. Their intellectual independence is **unknown**: different authors and platforms do not establish independent derivation or corroboration.

Codefinity's parent course is labelled Advanced, but the inspected lesson is introductory in style. The catalogue's mixed classification avoids incorrectly assigning the whole course's label to the specific lesson. Keep that distinction.

### 12.3 Additional sources actually cited by the page

| Source | Page role | Metadata/evidence boundary | Audit decision |
|---|---|---|---|
| Jose Parreño Garcia, *Understanding Transformers (Part 4)* | Complementary intuition linked from the Q/K/V page | English introductory blog; visible article body reviewed; figures not inspected; no code/experiment executed; licence unknown; no explicit qkv-attention collection membership | Add to the page-level comparison, but do not silently rewrite historical collection membership. Decide whether the collection is a tutorial comparison set or a complete topic source family before changing membership. |
| Vaswani et al., *Attention Is All You Need* | Primary formulation cited for learned Q/K/V projections | English advanced research paper; partially scanned; focused review now covers §§3.2.1–3.2.3 for scaled attention, learned projections and self-attention data flow | Retain as primary anchor. The exact projection claim is now traced to §3.2.2, with §3.2.3 supporting the shared input stream in self-attention; the page's XW_Q notation is identified as a compact specialization. |

The page-visible citation inventory is four URLs in both languages:
- Neha KK (example adapted from the article);
- Jose Parreño Garcia (complementary recommendation/routing intuition);
- Vaswani et al. (primary architecture formulation);
- Nishanthan K (complementary visual explanation).

Codefinity and Brenndoerfer are legitimate construction/comparison inputs, but are not direct citations in the current Q/K/V page body. This is not a defect; the public page need not list every source considered during editorial synthesis.

### 12.4 Diversity profile and interpretation

| Dimension | Observed distribution | Interpretation |
|---|---|---|
| Construction corpus type | 2 blog, 1 course, 1 tutorial | Useful format diversity; still mostly secondary pedagogy |
| Construction corpus language | 4/4 English | Complete language concentration; monitor as a selection bias, not an automatic publication defect |
| Construction corpus technical level | 2 introductory, 1 mixed, 1 intermediate | A useful progression from orientation to mathematical/implementation depth |
| Construction corpus origin | 4 distinct creators/platforms | No single-author/platform concentration in this small sample |
| Page-visible sources | 2 blogs, 1 research paper, 1 blog on Substack (three blog posts plus one paper) | The public citation set includes a primary research anchor, but the explanatory citations remain secondary |
| Inspection completeness | All four pedagogical-resource records and both additional cited sources remain partially scanned | Do not present any of them as exhaustively audited |
| Independent corroboration | Not established | Repeated tutorial descriptions are pedagogical convergence, not independent experimental evidence |

No entropy score is calculated for this four-source pilot. With four deliberately selected, non-representative resources, a numerical diversity score would add false precision. The counts above are descriptive only; they are not targets or quality grades.

### 12.5 Coverage against the Q/K/V page contract

The page's stated purpose is to explain why the attention sublayer projects its input state into Q, K and V, distinguish compatibility (Q/K) from aggregated content (V), and let the learner reason about changing one projection in isolation.

| Learner need / claim family | Existing support | Assessment |
|---|---|---|
| Motivation for contextual information | Page narrative and Neha's coreference example; contextualized-representations is the upstream page | Covered; keep the example explicitly illustrative, not empirical evidence of head-level coreference |
| Functional roles of Q, K and V | Canonical page explanation, Nishanthan and Codefinity | Covered; repeated definitions do not require more sources |
| Why three learned projections? | Neha's design rationale and canonical page's joint learned-projection explanation | Covered |
| Shared input and projection equations | Canonical equations and Vaswani primary paper | Covered; §3.2.2 supports the learned per-head projections and §3.2.3 supports the shared previous-layer input in self-attention |
| Routing/compatibility versus payload/content | Brenndoerfer's comparative treatment and canonical page | Covered; preserve the distinction as a functional explanation, not a claim that dimensions are human-readable semantic features |
| Geometric intuition | Codefinity and Brenndoer; canonical advanced Q/K/V deep dive | Covered at the deeper destination through the Q–K compatibility geometry section; the core lesson links onward rather than duplicating the derivation. Avoid equating dot product with cosine similarity |
| Convex-hull consequence / message-passing analogy | Brenndoerfer | Not present in the current scaled-attention pages; keep both deferred until a concrete learner task justifies the added geometric or graph-oriented interpretation |
| Scores, scaling, softmax and weighted aggregation | Dedicated scaled-dot-product-attention page and Vaswani §3.2.1 | Deliberately delegated to the next page; do not duplicate the full derivation here |
| Causal masking and accessible positions | Dedicated causal-masking page | Correctly outside this page's main scope |
| Implementation and tensor-level behavior | Transformer-block walkthrough and Build resources | Covered by a neighboring implementation destination; not a missing source requirement for this Understand page |
| Independent empirical claims about learned head behavior | No measured head-level experiment in the tutorial corpus | Not an objective of this page; keep illustrative examples clearly labelled and avoid stronger empirical claims |

### 12.6 Findings and decisions

1. **No additional generic Q/K/V tutorial is justified now.** The current page and its adjacent pages already cover the relevant pedagogical functions; a fifth tutorial would likely repeat the same role definitions.
2. **The page has meaningful source diversity, but not uniform evidence diversity.** The construction corpus includes distinct formats, levels and explanatory lenses; it remains English-only and secondary. The primary paper is cited separately.
3. **The primary citation needs claim-level precision.** The focused Vaswani review now covers §§3.2.1–3.2.3. The projection claim is supported by §3.2.2; §3.2.3 establishes the common previous-layer source in self-attention. The page's XW_Q notation is explicitly distinguished from the paper's per-head multi-head notation.
4. **Jose Parreño Garcia must be reconciled with the historical matrix.** Its source review and page citation post-date the four-source comparison. Update the comparison rather than treating the old matrix as a complete current inventory.
5. **Do not infer collection membership.** Decide whether `qkv-attention` represents the four-source pedagogical comparison set or the broader set of all page-relevant sources before adding Jose or Vaswani to its membership.
6. **Keep related-page associations separate from evidence usage.** A source associated through `related.pages` is a candidate for review, not automatically a source used by the page.
7. **No language quota.** The English-only resource set is a documented bias. Search for French material only if it serves a concrete learner need and adds a distinct contribution; do not add a weak source to improve a count.
8. **No public lesson change is justified by this audit alone.** The page's current content is already sufficiently complementary for its stated Understand role. Remaining work is source-matrix freshness and claim-level primary provenance.

### 12.7 Follow-up checklist

- [x] Compare external citations in Q/K/V FR and EN; confirm the same four URLs.
- [x] Separate the four-source construction/comparison corpus from the four page-visible citations.
- [x] Classify the four pedagogical resources by type, origin, language, level, function, scan and integration status.
- [x] Identify Jose Parreño Garcia as a later page-cited source absent from the historical four-source matrix.
- [x] Identify Vaswani as the primary source and preserve the focused/partial scan boundary.
- [x] Record that `related.pages` does not establish source usage or claim support.
- [x] Verify Vaswani §3.2.2 for the learned projection claim and §3.2.3 for the shared source in self-attention; update the existing review, extraction and source scan history with exact locators.
- [x] Define `qkv-attention` as the curated set selected for Q/K/V construction or claim grounding; add the cited Jose and Vaswani sources while keeping the four-resource comparison subset bounded.
- [x] Explicitly bound the historical comparison to its four-resource pedagogical subset; Jose and Vaswani remain separately characterized in the page-level audit.
- [x] Re-run the page citation/FR-EN parity check after the dossier update; the four external URLs match in the same order.

**Pilot conclusion:** the Q/K/V corpus is not merely homogeneous: its four-source construction set has useful pedagogical diversity, while its page-visible references include both a primary paper and a later complementary blog. The main weakness is not a shortage of resources but a stale boundary between the historical comparison matrix, the live page citations and the source catalogue's topical associations. Fix provenance and claim mapping before expanding the source set.


### 12.8 Claim-to-source traceability (page-level, not a bibliography count)

The table below maps the important claim families in the Q/K/V lesson to the source roles that can actually support them. “Pedagogical explanation” is not treated as primary technical proof, and repeated explanations are not counted as independent corroboration.

| Claim / learner question | Pedagogical or explanatory sources | Technical / primary support | What the evidence does not establish |
|---|---|---|---|
| Why context is needed; why a token's interpretation can depend on other positions | Neha KK (coreference illustration); Jose Parreño Garcia (cake/it motivation); Nishanthan K (bank/pronoun examples) | The Transformer attention formulation provides the contextual interaction mechanism, but these examples are teaching motivations | No example proves that a trained individual head reliably resolves coreference or word-sense ambiguity |
| Functional distinction between Q, K and V | Nishanthan, Neha, Codefinity, Brenndoerfer, Jose | Vaswani et al. §§3.2.1–3.2.2 defines the attention operation and the learned projections used by heads | The analogies do not make Q/K/V human-readable labels or discrete database fields |
| Why separate learned projections are used | Neha's matching-versus-payload rationale; Jose's recommendation analogy; Brenndoerfer's mathematical/implementation explanation | Vaswani et al. §3.2.2 specifies distinct learned per-head projections; §3.2.3 distinguishes self-attention's shared previous-layer source from encoder–decoder attention's separate streams | The primary paper supports the architecture, not every explanatory analogy or a universal design claim across all modern variants |
| Same input stream in self-attention; cross-attention contrast | Jose and the canonical page provide explanatory framing | Vaswani et al. §3.2.3 explicitly identifies the common previous-layer source for Q/K/V in self-attention and the decoder-query / encoder-memory K/V split in encoder–decoder attention | Do not generalize the original paper's exact data flow to every architecture without checking its block design |
| Projection dimensions and output shapes | Brenndoerfer offers an implementation-oriented walkthrough; the canonical page derives the project's row-major shapes | Vaswani §3.2.2 gives per-head projection dimensions; the page specializes this to its compact single-head notation | The paper's multi-head notation is not a verbatim source for the page's compact (Q=XW_Q), (K=XW_K), (V=XW_V) equations |
| QK compatibility scores, scaling, softmax and weighted V aggregation | Nishanthan, Neha, Codefinity, Brenndoerfer and Jose offer explanatory sequences | Vaswani §3.2.1, Equation (1), is the primary mathematical definition; the dedicated scaled-dot-product-attention lesson owns the full derivation | These operations are deliberately handed off from the Q/K/V lesson; their full mathematical derivation should not be duplicated here |
| How projection parameters are learned and how gradients flow | Nishanthan mentions gradient-based adjustment; the canonical advanced Q/K/V deep dive owns the detailed explanation | The primary attention paper defines the architecture, not a complete backpropagation derivation for this page's pedagogical question | Do not use a general architecture citation as evidence for the page's detailed gradient-path explanation; use the dedicated training/gradient source chain |
| Whether learned heads encode interpretable semantic relations | No inspected pedagogical source provides an empirical head-level experiment | No primary evidence in this Q/K/V source set establishes reliable semantic or causal interpretation of individual heads | Explicitly unsupported; retain the page's epistemic caveat |

**Evidence-family interpretation:**
- Vaswani is one primary research source, not multiple independent sources because it has several sections or extraction items.
- The five pedagogical explanations are secondary resources with unknown intellectual independence. Their convergence is useful for teaching synthesis, not independent scientific corroboration.
- Jose's extraction contains claims about scaling, softmax and weighted aggregation, but those claims are not additional primary evidence; where needed, use Vaswani and the dedicated mathematical lesson.
- The page's equations and explanations are project-authored synthesis. A page citation is not automatically a claim-level citation for every sentence in its section.

### 12.9 Collection membership and bilingual parity closure

- `qkv-attention` now contains five pedagogical comparison resources plus Jose Parreño Garcia and Vaswani et al.; the new Veres-Lakos source is registered as an optional worked analogy, not a new canonical explanation.
- The four-source pedagogical matrix remains unchanged in scope; it is not expanded with a primary paper or a later page-cited blog because its comparison question is specifically the original four pedagogical resources.
- The current Q/K/V FR and EN pages now include the Veres-Lakos article as an optional external worked analogy alongside the existing resources; bilingual parity must be rechecked by the project validation workflow.
- No public page edit is required. This audit changes source provenance and traceability, not the learner-facing content.


### 12.10 Veres-Lakos — meeting analogy and residual update (2026-11-27)

The complete 12-page PDF export was inspected. Its distinctive contribution is a continuous numerical analogy: a competence matrix is projected into needs (Q), offers (K) and transmissible information (V); scores are normalized row-wise; values are aggregated; W_O maps the context back to the state coordinates; and the resulting Delta X is added to X.

**Integration decision:** add the source to the collection and link it from both Q/K/V pages as optional further reading. Do not copy its tables or attention figure. The project already owns the general Q/K/V and attention derivations, numerical workbench, causal masking and multi-head material.

**Technical guardrails:** the source's scalar 10 is a pedagogical sharpness multiplier, not the standard 1/sqrt(d_k) factor; its zero-score row becomes uniform because no mask is applied; W_O is the attention sublayer's output projection, not the final vocabulary head; the GPT mapping omits the MLP residual branch. The bank, pronoun and adjective examples are illustrations, not empirical head-level evidence. The page-11 attention matrix is credited to Raschka Figure 3.11 and remains link-only because asset rights are unknown. The article also describes a hypothetical second meeting in which Cara's negative needs invert her matching preference toward Bob; retain this as a limitation of the unconstrained toy update, not as a general Transformer behavior.
