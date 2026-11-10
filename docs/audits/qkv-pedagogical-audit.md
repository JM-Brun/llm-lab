# Q/K/V lesson — pedagogical audit and revision

**Date:** 2026-11-10  
**Scope:** French and English Understand lessons on queries, keys, and values; the immediately preceding Transformer overview; the following scaled dot-product attention lesson.  
**Comparison reference:** Nishanthan K, [*How Query, Key, and Value (QKV) Work in Transformers*](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a).  
**Status:** Source-level audit and bilingual revision committed to the working branch; rendered and learner validation remain open.

## 1. Evidence level and method

The audit follows the repository's [Understand Path Audit](../../.agents/skills/understand-path-audit/SKILL.md) and the existing contracts for [page composition](../page-template-guide.md), [reader experience](../reader-experience-and-editorial-method.md), [content ownership](../content-section-mapping.md), and [page review status](../page-audit-inventory.md).

Inspected:

- `site/fr/queries-keys-values.qmd` and `site/en/queries-keys-values.qmd`;
- `site/images/queries-keys-values.svg` and its English counterpart;
- the French Transformer overview and scaled dot-product attention lesson;
- the bilingual page metadata and their stated learning objectives.

This is a **source-level review**. It establishes what the Quarto sources and SVGs specify. The published pages could not be inspected in a browser during this pass; no claim is made about rendered typography, responsive behavior, keyboard interaction, or actual learner comprehension. No learner study was conducted.

The comparison with DEV is qualitative, not a controlled usability test. The DEV article is useful as an example of a more narrative progression from an intuitive problem to the mechanism and then to equations. LLM Lab's stronger contribution is its more explicit separation of learned projections, routing weights, and transmitted content, together with its scientific caveats and links to the next canonical lesson.

## 2. Reader journey and page boundaries

| Position | Reader's likely question | Knowledge brought in / added | Transition |
|---|---|---|---|
| Previous: `transformer.qmd` | Where does attention sit inside a GPT forward pass? | The reader has seen that self-attention is a sublayer inside a Transformer block and exchanges information between positions. | The overview identifies Q/K/V as internal projections but does not explain their separate roles. |
| Current: `queries-keys-values.qmd` | Why are three projections made from the same representation, and what does each contribute? | The lesson distinguishes the projections that determine attention weights (Q/K) from the projection that supplies the vectors being aggregated (V); it introduces their shapes and learned matrices. | Once the reader can identify Q, K, and V, the next question is how scores become normalized weights and how those weights combine V. |
| Next: `scaled-dot-product-attention.qmd` | How exactly are scores, softmax weights, and the weighted sum computed? | The next lesson owns the full arithmetic, scaling, normalization, and aggregation. | This boundary prevents the Q/K/V lesson from becoming a duplicate attention-calculation tutorial. |

The route boundary is sound and was preserved. The Q/K/V lesson does not need to teach the full softmax calculation or causal mask; it needs to give enough local context for the reader to understand why the three projections are distinct.

## 3. Findings and decisions

| Priority | Finding and source evidence | Reader impact | Decision |
|---|---|---|---|
| **P1** | The stated outcomes included reconstructing the projections and predicting parameter-change effects, but the lesson had no small worked projection example. | The reader could repeat the equations without seeing how the same input produces three distinct vectors or how the invariance follows from the dependency structure. | Add a hand-checkable two-dimensional example in both languages. Change only W_V and explicitly show that Q/K remain fixed. Keep score/softmax arithmetic on the next page. |
| **P1** | The most concrete linguistic motivation was buried in a collapsed note near the end; the opening moved quickly from the page transition to a summary. | A new reader had to accept the three roles before seeing the problem that makes them useful. | Add a short, carefully qualified coreference example near the beginning, before the one-minute mental model. |
| **P2** | The existing SVG already showed the essential two-path structure: Q and K feed score/weight computation; V feeds weighted aggregation. Its surrounding prose did not explicitly direct the reader to follow those two paths. | The page had a suitable visual anchor, but the reader could treat it as an illustration rather than the central mental model. | Keep the existing project-owned diagram; clarify its alt text and explicitly connect the opening explanation to its two paths. No new visual asset is needed. |
| **P2** | Two adjacent collapsed callouts repeated the coreference example and its caveat, then contrasted it with lexical ambiguity. | Repetition added reading friction without adding a distinct learning objective. | Consolidate them into one optional note preserving both examples, source attribution, and the warning against inferring the behavior of a particular head from an illustration. |
| **P2** | The DEV article uses a more continuous problem → intuition → mechanism → formalization progression. | LLM Lab's scientific detail was valuable, but the main route felt more like a reference note than a guided explanation. | Borrow the narrative sequencing, not the article's exact wording or structure. Preserve the more precise mathematical and architectural treatment in LLM Lab. |
| **P3** | The page includes optional geometry, gradient, and architecture-variant material. | These details can interrupt the core explanation if encountered as mandatory reading. | Keep them in progressive-disclosure callouts. They are useful optional depth and do not need to be deleted or moved merely to shorten the page. |

## 4. Changes applied

The French and English pages now share the same pedagogical sequence:

1. Existing page-to-page orientation.
2. Collapsed, observable learning outcomes.
3. A short motivating example that makes the need for contextual information concrete, with an explicit limitation on what the example proves.
4. The existing one-minute Q/K/V mental model.
5. The existing role analogy and central two-path diagram.
6. The learned-projection equations and tensor shapes.
7. A small numerical example of three projections from one input.
8. A controlled change to W_V showing that Q/K-derived scores and weights remain fixed, while the aggregated content may change.
9. The existing optional treatments of gradients, vector geometry, and architecture variants.
10. The existing exercise-hub link and short self-check.

### Numerical example check

Using row-vector convention and

`x_t = [1, 2]`,

`W_Q = [[1, 0], [0, 1]]`,  
`W_K = [[0, 1], [1, 0]]`,  
`W_V = [[1, 1], [0, 1]]`,

the projections are:

- `q_t = [1, 2]`;
- `k_t = [2, 1]`;
- `v_t = [1, 3]`.

If only `W_V` is replaced by `[[2, 0], [0, 1]]`, then `v_t` becomes `[2, 2]`; `q_t` and `k_t` are unchanged. Therefore the scores and weights derived from Q and K are unchanged. The resulting weighted content may change, although a particular aggregate can remain unchanged if weighted changes cancel.

The matrices are explicitly labelled illustrative, not learned parameters from a real model. The example deliberately stops before computing attention scores or softmax, preserving the next lesson's ownership.

## 5. Preservation and scientific checks

- The page IDs, destination, level, suggested route, hierarchy, and related-page metadata were not changed.
- The existing project-owned SVGs were retained; no figure was copied from DEV or another external source.
- The original-paper reference and existing optional explanations of gradients, vector geometry, cross-attention, GQA/MQA, and projection-sharing research were retained.
- The exercise collection remains separate from the concept lesson; the page links to the existing Attention exercise section rather than embedding a growing exercise bank.
- The examples are described as motivation for contextual information flow, not evidence that one attention head independently resolves coreference or lexical ambiguity.
- The invariance claim is scoped correctly: changing V alone does not change Q/K-derived scores or weights; the aggregate can change, but need not change in every possible numerical case.

## 6. Validation status

| Check | Status | Evidence / limitation |
|---|---|---|
| French and English source edits | **Done** | Both Quarto sources updated in the same branch. |
| Bilingual learning-outcome parity | **Done at source level** | Both versions state the same three observable capabilities. |
| Worked-example arithmetic | **Checked** | Matrix products and the W_V-only change were independently calculated. |
| Page-boundary consistency | **Checked at source level** | The current lesson still delegates score/softmax/aggregation to the next lesson and retains its existing route metadata. |
| Figure preservation and alt text | **Done at source level** | Existing FR/EN SVG files remain unchanged; source alt text now names the two paths. |
| Local links and exercise separation | **Source-inspected** | Existing relative links and the central exercise-hub destination were preserved. |
| Quarto render and site validators | **Not run** | No repository execution environment was available in this audit. |
| Published-page browser review | **Not run** | Responsive layout, rendered math, callout behavior, focus, and language switching remain to be inspected. |
| Learner task testing | **Not run** | Comprehension improvement is a design hypothesis, not an observed outcome. |

## 7. Follow-up review

After the branch is rendered, inspect both language versions at desktop and narrow widths. In particular:

- confirm that the new learning-outcomes callout follows the shared styling and remains collapsed by default;
- check matrix alignment, line wrapping, and readability of the worked example;
- check the diagram's size and the relationship between its two paths and the nearby prose;
- verify the page's first screen, local links, exercise anchor, language switch, and previous/next navigation;
- ask a learner unfamiliar with Q/K/V to explain why changing only V cannot change the attention weights, then compare the explanation with the page's learning outcomes.

**Audit verdict:** the conceptual route was already coherent, but the opening and the transition from equations to operational understanding had avoidable friction. The revision addresses those two gaps without broadening the page's scope or duplicating the next lesson.
