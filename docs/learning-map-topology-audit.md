# Learning-map topology audit

**Snapshot:** 2026-11-04  
**Metadata base:** `main` at `82606ee4a9c77f9be2dc5a1e8c8931bc79e370b1`  
**Audit implementation:** `scripts/audit_page_metadata.py` (PR #429)  
**Scope:** published page metadata from the explicit Quarto render inventory. This is a structural and editorial triage report, not a learner study or a claim that the current route is pedagogically optimal.

## Executive findings

- **103 published pages** were analyzed: 51 French, 51 English, and one shared reference page.
- The FR and EN suggested-route graphs each contain **28 directed edges**, **34 participating pages**, **six rooted chains**, and **six starts / six ends**.
- There are **no route convergence points** and **no unrooted route participants** in either language.
- **17 pages per language** have null `suggested_route.previous/next`: 12 Deepen, 3 Understand, 1 Orient, and 1 Practice page. Null route links do not make a page an orphan.
- The existing structural validator reports **no errors**: page references, route reciprocity, cycle checks, hierarchy reciprocity and FR/EN parity all pass.
- The hierarchy is substantially more connected than the linear route: eight fan-out hubs and eight multi-parent nodes occur in each language. Those relations must not be presented as a single learning sequence.
- No scope/purpose pair crossed the audit's conservative 0.60 lexical-overlap threshold. This does not establish semantic non-duplication.

## Suggested-route chains

The current metadata defines six distinct chains in each language, not one global route.

| Chain | French IDs | English IDs | Interpretation |
|---|---|---|---|
| Conceptual inference and learning | `index → llm-overview → generation → text-data → tokenization-strategies → embedding-space → positional-encoding → contextualized-representations → transformer → queries-keys-values → scaled-dot-product-attention → causal-masking → logits → probabilites → vraisemblance → cross-entropy → loss → gradients` | `index → llm-overview → generation → text-data → tokenization-strategies → embedding-space → positional-encoding → contextualized-representations → transformer → queries-keys-values → scaled-dot-product-attention → causal-masking → logits → probabilities → likelihood → cross-entropy → loss → gradients` | The early `generation` page is an intentional black-box preview before the input and internal-computation explanations. The chain then moves from inference mechanics into the learning objective. |
| Corpus and training examples | `corpus-preparation → training-examples` | `corpus-preparation → training-examples` | A separate Build/training-data branch (G1b/G2), not a prerequisite for understanding inference. |
| GPT module walkthroughs | `gpt-config-walkthrough → gpt-ops-walkthrough → transformer-block-walkthrough → gpt-model-walkthrough → gpt-generation-walkthrough` | Same stable topic sequence with English IDs | Practical implementation sequence, distinct from the conceptual route. |
| Build and practice | `build-path → exercises → evaluation-experimentale` | `build-path → exercises → experimental-evaluation` | Practice/evaluation path. |
| Glossary and history | `glossary → transformer-history` | Same stable topic sequence | Potential editorial mismatch: history is documented as optional reference context, so this chain must not be presented as a mandatory next learning step. |
| Mathematical deepening | `mathematical-foundations → tensors → cosine-similarity → linearite-embeddings` | `mathematical-foundations → tensors → cosine-similarity → embedding-linearity` | Optional Deepen chain; not a prerequisite chain for the first GPT implementation. |

The chain structure is equivalent in French and English. The existing validator compares route targets by canonical topic identity rather than requiring translated slugs to match.

## Pages outside the suggested route

Per language, 17 pages have both route pointers set to null:

| Destination | Count | Examples |
|---|---:|---|
| Deepen | 12 | cross-attention, decoding-strategies, language-modeling-math, llm-computational-complexity |
| Understand | 3 | entropy, llm-limits, transformer-architectures |
| Orient | 1 | learning-map |
| Practice | 1 | transformer-explainer |

This is broadly consistent with optional deepening and standalone activities. The three Understand pages deserve a light editorial check: decide whether they are intentionally independent or should have an explicit suggested-route link. Do not add links merely to eliminate nulls.

## Hierarchy hubs and multi-parent nodes

The following structures are the same in FR and EN (with translated page IDs):

| Page | Children | Parents | Interpretation |
|---|---:|---:|---|
| `llm-overview` | 8 | 0 | Broad conceptual hub |
| `index` | 7 | 0 | Site learning/navigation entry point |
| `transformer` | 7 | 2 | Architectural hub with several conceptual parents |
| `build-path` | 6 | 2 | Practical implementation hub |
| `embedding-space` | 4 | 2 | Representation hub |
| `generation` | 3 | 0 | Inference preview and output hub |
| `text-data` | 3 | 0 | Input pipeline hub |
| `positional-encoding` | 2 | 2 | Representation mechanism with multiple conceptual links |
| `contextualized-representations` | 0 | 3 | Shared outcome of embedding, position and Transformer context |
| `logits` | 0 | 2 | Output representation linked from generation and Transformer |
| `probabilities` / `probabilites` | 0 | 2 | Distribution interpretation linked from logits and generation |
| `queries-keys-values` | 0 | 2 | Attention projection concept linked from contextualization and Transformer |

The report distinguishes hierarchy fan-out from route edges. These parent/child links describe conceptual organization; they are not automatically prerequisites or a pedagogical order.

## Isolated pages

Five pages have no route, hierarchy or related links:

- `fr/deepen`
- `en/deepen`
- `fr/learning-map`
- `en/learning-map`
- `reference/references`

These appear to be landing/navigation/reference pages rather than lesson nodes. Keep them outside the concept/page graph unless there is a concrete reader task that requires a relation.

## Crosswalk: six conceptual stages versus Build milestones G0–G9

The six-stage reader-facing route introduced in PR #424 is intentionally not isomorphic to the implementation milestones. The mapping should be read as a crosswalk, not a new prerequisite graph.

| Guided conceptual stage | Build milestone(s) | Boundary |
|---|---|---|
| Orientation | G0, plus a black-box preview of G7 | The early generation page demonstrates inference before explaining internals; it is not a build dependency. |
| Text input | G1 | Text, Unicode and tokenization. G1b corpus preparation belongs to the practical data branch. |
| Representations | G3 | Embedding lookup, position and contextualized states. |
| Transformer computation | G4–G5 | Attention/masking, then block/model composition. |
| Prediction | G6–G7 | Logits, probabilities, token selection and autoregressive generation. |
| Learning and evaluation | G8–G9 | Training examples/objective/gradients and evaluation. |

**G2 is deliberately absent from the conceptual inference route.** It covers training-example construction (context windows, shifted targets, batches and masks) and belongs to the separate training-data branch after corpus preparation. Build has its own implementation dependencies; it should reuse the conceptual pages rather than merge its order with the inference route.

### Documentation inconsistency requiring correction

The current `docs/content-section-mapping.md` needs a focused repair before it can serve as the definitive G0–G9 crosswalk:

1. In section 3, a four-column Build table is followed by rows with a different seven-column shape and no intervening header. The G2 training-examples row is duplicated, and a later row is labelled `G3 — Create training examples`, which conflicts with the authoritative G3 representation milestone.
2. In section 4, the evidence matrix contains G0, G1, G1b, G3–G9 and A1–A4, but has no G2 evidence row.
3. The canonical `docs/learning-path.md` identifies G2 as the parallel training-data branch. Keep G1b (corpus preparation) and G2 (training examples) explicit and distinct; do not renumber G3–G9 to hide the omission.

This report records the inconsistency; it does not silently rewrite the curriculum or invent missing implementation evidence.

## Recommended follow-up

1. Repair the two Build milestone tables in `docs/content-section-mapping.md` against `docs/learning-path.md`; add the missing G2 evidence row and preserve G1b as a separate corpus-preparation branch.
2. Review the `glossary → transformer-history` chain against the editorial rule that history is optional reference context.
3. Decide whether the three route-free Understand pages are intentionally standalone.
4. Preserve the distinction between suggested route, hierarchy, related links, and the six-stage reader-facing route.
5. Complete manual rendered inspection (desktop/mobile, keyboard, focus, touch and link destinations) in #337/#417.

## Method and limits

The report is generated from the explicit Quarto render list. Route chains use only `suggested_route.next`; hierarchy and related relations are analyzed separately. Structural validity and FR/EN parity are delegated to `scripts/check_page_metadata.py` (or its future `site/tools/` location), not reimplemented here. Lexical overlap is a conservative triage signal only. No metadata values were changed by this audit.
