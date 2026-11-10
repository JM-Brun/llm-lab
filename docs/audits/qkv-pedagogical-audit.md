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
- the French and English Transformer overviews and scaled dot-product attention lessons;
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
| **P1** | The concept lesson had no worked projection example, while its learning outcomes risked implying that matrix calculation belonged to the conceptual route. | The conceptual page should establish the roles and dependencies; numerical manipulation belongs in the practice route. | Keep the concept lesson qualitative. Move the two-dimensional hand calculation and W_V-only intervention into the Attention exercise collection in both languages. |
| **P1** | The most concrete linguistic motivation was buried in a collapsed note near the end; the opening moved quickly from the page transition to a summary. | A new reader had to accept the three roles before seeing the problem that makes them useful. | Add a short, carefully qualified coreference example near the beginning, before the one-minute mental model. |
| **P2** | The existing SVG already showed the essential two-path structure: Q and K feed score/weight computation; V feeds weighted aggregation. Its surrounding prose did not explicitly direct the reader to follow those two paths. | The page had a suitable visual anchor, but the reader could treat it as an illustration rather than the central mental model. | Keep the existing project-owned diagram; clarify its alt text and explicitly connect the opening explanation to its two paths. No new visual asset is needed. |
| **P2** | Two adjacent collapsed callouts repeated the coreference example and its caveat, then contrasted it with lexical ambiguity. | Repetition added reading friction without adding a distinct learning objective. | Move the coreference example and its source attribution to the opening; retain lexical ambiguity as one optional note. Preserve the warning against inferring the behavior of a particular head from an illustration. |
| **P2** | The DEV article uses a more continuous problem → intuition → mechanism → formalization progression. | LLM Lab's scientific detail was valuable, but the main route felt more like a reference note than a guided explanation. | Borrow the narrative sequencing, not the article's exact wording or structure. Preserve the more precise mathematical and architectural treatment in LLM Lab. |
| **P3** | The page includes optional geometry, gradient, and architecture-variant material. | These details can interrupt the core explanation if encountered as mandatory reading. | Keep them in progressive-disclosure callouts. They are useful optional depth and do not need to be deleted or moved merely to shorten the page. |

## 4. Changes applied

The French and English concept pages now share the same qualitative pedagogical sequence:

1. Existing page-to-page orientation.
2. Collapsed, observable learning outcomes.
3. A short motivating example that makes the need for contextual information concrete, with an explicit limitation on what the example proves.
4. The existing one-minute Q/K/V mental model.
5. The existing role analogy and central two-path diagram.
6. The learned-projection equations and tensor shapes.
7. The existing symbolic projection equations and tensor-shape explanation, without a worked numerical calculation.
8. Optional explanations of learning, geometry, and architecture variants.
9. A conceptual self-check that asks the reader to explain the Q/K versus V dependency without calculating.
10. A clear hand-off to the separate exercise collection for numerical projection work.

### Practice exercise relocation

The two-dimensional calculation is no longer part of either concept page. It has been moved into the Attention collection in the French and English exercise catalogues as **“calculer Q, K et V puis isoler l'effet de V” / “calculate Q, K, and V, then isolate the effect of V.”** The task asks learners to compute the three projections by hand, change only W_V, verify the unchanged Q/K-derived scores and weights, and explain why the aggregated content may change. A worked solution is collapsed by default.

The arithmetic remains the same and was checked:

- With x=[1, 2], W_Q=identity, W_K=the coordinate swap, and W_V=[[1, 1], [0, 1]], the results are q=[1, 2], k=[2, 1], v=[1, 3].
- Replacing only W_V with [[2, 0], [0, 1]] gives v'=[2, 2], while q and k remain unchanged.

The exercise explicitly identifies the matrices as fictional and hand-computable. The concept lesson retains only the symbolic equations, role distinction, qualitative invariance, and its existing link to the practice hub.
 
## 5. Preservation and scientific checks

- The page IDs, destination, level, suggested route, hierarchy, and related-page metadata were not changed.
- The existing project-owned SVGs were retained; no figure was copied from DEV or another external source.
- The original-paper reference and existing optional explanations of gradients, vector geometry, cross-attention, GQA/MQA, and projection-sharing research were retained.
- Numerical matrix calculations are kept out of the concept lesson and placed in the separate Attention exercise collection; the concept page links to the existing exercise hub.
- The examples are described as motivation for contextual information flow, not evidence that one attention head independently resolves coreference or lexical ambiguity.
- The invariance claim is scoped correctly: changing V alone does not change Q/K-derived scores or weights; the aggregate can change, but need not change in every possible numerical case.

## 6. Validation status

| Check | Status | Evidence / limitation |
|---|---|---|
| French and English concept/practice edits | **Done at source level** | Both concept lessons are qualitative; the matching hand-calculation exercise and collapsed solution are present in both exercise catalogues. |
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

**Audit verdict:** the conceptual route was already coherent, but the opening and the transition from equations to operational understanding had avoidable friction. The revision addresses the narrative gap while keeping numerical manipulation in the practice route, without broadening the concept page's scope or duplicating the next lesson.


## Q/K/V reading-flow revision — 2026-11-10

A second editorial pass focused on the requested reader-experience criteria: an understandable opening problem, short intuitive definitions, a narrative in which each section prepares the next, and fewer interruptions or digressions. It follows the same source-level evidence boundary as the first audit.

### Changes applied to the bilingual concept lessons

- **Opening hook:** the coreference sentence now introduces the need for contextual information before any Q/K/V terminology. The learning-outcomes disclosure no longer precedes the hook; it is placed after the explanatory sequence.
- **Intuitive definitions:** Q, K, and V are introduced in parallel, one short role statement each, followed immediately by the routing-versus-content distinction.
- **Visual sequence:** the existing project-owned two-path diagram now follows those definitions directly. A short reading cue explicitly tells the learner what to follow in the figure.
- **Narrative hand-off:** the next section answers the question raised by the diagram—why three projections are needed from one input—then introduces the symbolic equations and tensor shapes. The following scaled-dot-product lesson is named as the owner of score, normalization, and aggregation calculations.
- **Reduced interruptions:** the duplicate one-minute summary, source-hosted supplementary illustration note, standalone history aside, repeated routing/content callout, and operational checklist that invited matrix calculation on a conceptual page were removed from the central reading path. Geometry, training, architecture variants, and lexical ambiguity remain available as optional depth.
- **Scope retained:** cross-attention is explicitly preserved in the collapsed architecture/scope note. The conceptual pages remain qualitative; numerical manipulation remains in the Attention exercise collection.

### Editorial trade-offs and further proposals

1. Keep the first screen focused on the learner's question. Avoid placing a summary, external references, or advanced terminology before the motivating problem.
2. Treat the Q/K/V diagram as the central explanatory visual, not as one illustration among several competing illustrations. The source-hosted article image was therefore removed from the main lesson; its reference remains in the audit history.
3. Keep the gradient, GQA/MQA, projection-sharing, vector-geometry, and lexical-ambiguity material collapsed. If rendered review shows that the page still feels long, the next candidate is to move gradient derivation and projection-variant research to the dedicated advanced pages—not to delete them or interrupt the core explanation.
4. Validate the hook with a learner unfamiliar with attention: after reading only the opening and the three role definitions, ask them to explain why the model needs both a weighting path and a content path.

### Source-level checks

- French and English pages use the same section sequence and preserve matching conceptual outcomes.
- The concept pages contain no worked numerical projection example and no instruction to calculate matrix products.
- Both pages retain symbolic Q/K/V equations, tensor-shape information, the existing diagram, cross-attention scope note, and links to the next concept lesson and the separate exercise collection.
- This pass does not claim a fresh Quarto render, responsive/browser review, accessibility check, or learner study.


## Content-preservation audit after the reading-flow refactor — 2026-11-10

A line-by-line comparison was made between the pre-refactor Q/K/V lessons and the merged bilingual pages. The refactor did not lose the central mathematical model, but it did remove or compress several secondary explanations. The following disposition distinguishes genuine content preservation from intentional editorial removal.

### Preserved in the concept lessons

- The same-input self-attention formulation, symbolic matrix equations, tensor shapes, and the fact that the same projection matrices are applied at every position.
- The distinction between separately parameterized projections and joint optimization during training.
- The gradient pathways through Q/K scores and softmax versus V's weighted aggregation, including the local linear-layer gradient expressions.
- The boundary between self-attention and cross-attention, including the different provenance of Q versus K/V.
- GQA/MQA head sharing, KV-cache motivation, and research on sharing projection parameters.
- The limits of interpreting attention as semantic relevance or nearest-neighbour search in the initial embedding space.
- The lexical ambiguity example and its caveat: a contextualized representation may help, but an isolated head or attention map does not by itself establish a linguistic explanation.

### Restored in the follow-up

- The previously removed **routing-versus-content** nuance: a key can contribute to deciding whether a position is attended to, while its value determines what that position contributes; the two need not encode the same feature. The hypothetical grammatical-role/semantic-content example is explicitly marked as illustrative, not as an observed head behaviour.
- The explicit warning that values are not compared with the query or with one another to select a nearest value.
- A compact practice hand-off that maps the former operational competencies to existing Attention exercises: projection/dimension calculations, parameter interventions, gradient flow, cross-attention, and GQA/MQA.
- The removed historical route and the external DEV article are retained as collapsed supplementary references, not as competing content in the main narrative.

### Content intentionally compressed or removed

| Earlier content | Disposition | Reason |
|---|---|---|
| Index-card analogy | Replaced by direct Q/K/V role definitions | The analogy is not needed to preserve the mechanism and risks making learned vectors sound like literal labels or symbolic records. |
| Per-position equations $q_t=x_tW_Q$, $k_t=x_tW_K$, $v_t=x_tW_V$ | Equivalent information retained in matrix equations and the statement that each row is one position | The per-position form is a notational expansion, not a separate mechanism. |
| One-minute mental-model callout and distinction table | Their core statements are present in the opening, role definitions, diagram, and takeaway | Repetition was removed, not the core facts. |
| Detailed operational learning objectives | Their practice competencies are represented by the Attention exercise set and are now explicitly mapped from the lesson | Matrix calculations and interventions should remain in the practice route. |
| Dot-product scaling, softmax and accessible-key details | The Q/K/V lesson keeps the role-level explanation; the following scaled-dot-product lesson owns the derivation | Avoids duplicating the next lesson. The no-nearest-neighbour and no-universal-relevance caveats remain. |
| Separate Nishanthan visual callout and history aside | References retained in a collapsed supplementary-resource callout | The main diagram remains the single central visual; the related resources remain discoverable. |

### Verification boundary

The bilingual exercise pages already contain the corresponding projection, intervention, gradient, cross-attention, and GQA/MQA exercises. The concept pages remain free of worked numerical matrix examples. This is a source-content audit; it does not certify rendered layout, link resolution, accessibility, or learner outcomes.
