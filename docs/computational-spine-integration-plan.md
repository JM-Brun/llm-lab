# Computational spine integration plan

**Status:** active follow-up plan  
**Date:** 2026-11-06  
**Parent:** [#575 — Provide one persistent computational spine across inference, scoring and learning](https://github.com/JM-Brun/llm-lab/issues/575)  
**Architectural authority:** [Canonical computational spine](canonical-computational-spine.md) and the canonical module topology in [learning-path.md](learning-path.md#canonical-module-topology-shared-core-and-operational-branches).

This document is the durable hand-off for future work sessions. It records what has been completed, what remains, the intended order, and the evidence required to close the work. It is a task plan, not a new concept registry, curriculum hierarchy, or computational graph.

## 0. Current status — 2026-11-06

| Work package | Status | Evidence |
|---|---|---|
| Canonical computational model and registry | Integrated | PR #577, #580, #583, #578 |
| Eight-stage guided route and bilingual generated projections | Integrated | PR #578 and route-refresh PR #586 |
| Teacher forcing, prefill and decode teaching | Integrated | FR/EN training-examples and generation lessons |
| Concept-card domains and importance metadata | Integrated | `data/concepts.yml`, bilingual renderer and registry tests |
| Page metadata audit | Partial | Prediction → entropy → likelihood navigation and reciprocal hierarchy reviewed; broader inventory remains |
| Persistent-spine and evaluation views with text alternatives | In progress on this branch | Existing registry views reused; overview-page integration and renderer tests added |
| Build crosswalk | Partial | G0–G9 and G1b → G2 branch documented; implementation evidence still has gaps |
| Rendered desktop/mobile, keyboard and screen-reader review | Pending | Do not infer this evidence from source tests or a successful static render |

PR #578 is merged to `main`; PR #586 refreshed the tracked bilingual guided-route fragments and corrected the Ruff formatting issue. Its Python CI and Quarto site workflows passed. The current branch is the bounded follow-up for the persistent visual and accessible text alternative.


## 1. Architectural invariant

For a context containing preceding tokens (observed or generated), the model computes one conditional next-token distribution:

[
z_t=f_\theta(x_{<t}), \qquad
p_\theta(\cdot\mid x_{<t})=\operatorname{softmax}(z_t).
]

Three sibling operational branches use this shared result:

- **Inference:** decode/select a token, append the generated token to the context, and continue with unchanged parameters.
- **Scoring:** compare the distribution with an observed target, obtain its target probability and likelihood-related quantities; do not select a token and do not update parameters.
- **Training:** use teacher-forced observed targets to form a loss, compute gradients, and update parameters. The next training computation uses the updated parameters.

Evaluation applies scoring to held-out data and stops before the optimizer update. These branches are related, but are not one executable loop. The context is extended with a generated token during inference and with an observed token during teacher-forced scoring/training.

The common forward computation ends at the conditional distribution. Decoding, likelihood, loss, gradients, and parameter updates must not be drawn as sequential stages of ordinary inference.

## 2. Completed foundations

- [x] Canonical mathematical and conceptual distinction documented in `docs/canonical-computational-spine.md`.
- [x] Curriculum module topology, scope, containment, immediate pedagogical predecessors/successors, page ownership, and Core/Deepen boundaries defined in `docs/learning-path.md`.
- [x] Existing `data/concepts.yml` extended with reviewed concepts and typed semantic relations; do not create a parallel ontology or a second general-purpose graph.
- [x] Regression coverage added for the distinction between inference, scoring, training, teacher forcing, prefill, and KV cache.
- [x] Scope-driven bilingual Quarto Understand hierarchy merged in [PR #582](https://github.com/JM-Brun/llm-lab/pull/582).
- [x] Learning-map extraction/rendering extended to preserve nested sidebar sections in the interactive view and static fallback.
- [x] Navigation contract updated to keep site-location breadcrumbs, guided-route context, conceptual page hierarchy, and suggested page transitions distinct.

The merges above establish the model and one navigation projection. They do **not** mean all page metadata, route stages, page content, or rendered reader experience have been reconciled.

## 3. Remaining work, ordered by dependency

### P0 — Verify the merged navigation in the rendered site

- [ ] Run and inspect the current Quarto render for both languages after PR #582.
- [ ] Verify native breadcrumb ancestry on representative pages at each nesting depth: overview, text input, representations, Transformer computation, prediction, scoring, training, and optional depth.
- [ ] Verify the learning map and its static fallback preserve all nested sections, page counts, links, and empty-section behavior.
- [ ] Review desktop and mobile layouts; check wrapping, nested-card density, focus order, keyboard operation, accessible names, and screen-reader structure.
- [ ] Check Quarto previous/next links. The reader-facing preview-first order is intentional, but no accidental navigation into optional material should interrupt the core sequence.
- [ ] Record screenshots or browser-review evidence and fix concrete defects before generalizing the hierarchy to Build, Deepen, Practice, or Reference.

**Exit condition:** bilingual rendered pages and learning-map views agree with the authored sidebar hierarchy; no dead links, misleading ancestry, inaccessible nested controls, or unintended previous/next transitions remain.

### P1 — Reconcile the guided route with the sibling branches

The eight-stage projection is now integrated in `data/guided-route.yml` and the tracked bilingual route fragments:

`orientation → text-input → representations → computation → prediction → inference → scoring → training`.

- [x] Map stage and page membership to the canonical module IDs in `docs/learning-path.md`.
- [x] Keep the early generation page as a black-box preview and revisit the same canonical page for detailed inference.
- [x] End `prediction` at logits, the conditional distribution and predictive entropy.
- [x] Put likelihood and cross-entropy in `scoring`; reuse cross-entropy as an optional bridge in `training`.
- [x] Keep loss and gradients in `training`; keep `training-examples` optional as the Build bridge for shifted targets and teacher forcing.
- [x] Keep evaluation cross-cutting; the current scientific-passage ranking exercise remains in Practice and is not misrepresented as an LLM-evaluation lesson.
- [x] Preserve optional-page memberships and FR/EN parity.
- [x] Regenerate and test the tracked route fragments in PR #586.

**Exit condition:** met for the route projection. Further rendered-navigation review belongs to the validation section below.

### P1 — Audit page metadata and breadcrumb semantics

Use the existing page-map metadata schema and contract; do not add a new per-page breadcrumb field.

- [x] Review the prediction → entropy → likelihood transition in FR/EN: `suggested_route` now follows the reader-facing path, and the probabilities/entropy hierarchy is reciprocal.
- [x] Keep `hierarchy.parents/children` as conceptual containment/decomposition only; guided-route membership does not create page parents.
- [x] Keep `suggested_route.previous/next` as recommended pedagogical transitions, not computational dependencies.
- [x] Keep concept identity (`notion`), controlled concept domains (`domaine`) and `importance` in the concept registry/card model. Do not add redundant `notion` or `domaine` Quarto page tags; page tags remain editorial classifications (type, destination, topic, level, language, status).
- [x] Add controlled importance and localized domain metadata to concept cards, with registry and renderer tests.
- [ ] Complete the broader bilingual inventory for all pages in the shared core and operational branches.
- [ ] Check cross-links and metadata for the remaining scoring, training and evaluation pages.
- [x] Run the page metadata validator and topology audit on the integrated route and current branch.

**Exit condition:** metadata describes the actual content and intended reading transitions; no module scope is mistaken for conceptual containment or a prerequisite.

### P1 — Reconcile page content without losing knowledge

- [ ] Complete the shared-core page audit from text/tokens through embeddings, positional information, initial hidden states, Transformer blocks, final contextualized states, logits and softmax. The high-level registry and overview now expose the common path; page-by-page depth review remains.
- [x] Verify Q/K/V are operations inside each Transformer block and are projected from that block's input hidden states; the graph and walkthrough preserve this boundary.
- [x] Clarify the common forward pass and its boundary at the conditional distribution in the registry and overview.
- [x] Add the prefill/decode distinction, token-selection boundary, fixed-parameter inference and KV-cache limitation to the bilingual generation lesson.
- [x] Add teacher forcing after shifted input/target construction in the bilingual training-examples lesson; distinguish reference-token conditioning from generated-token feedback and qualify exposure bias.
- [ ] Complete the scoring-page audit for observed target, target probability, sequence likelihood, log-likelihood, NLL, token cross-entropy, reduction, masking and numerical stability.
- [ ] Complete the training-page audit for batch aggregation, gradients, optimizer, parameter update and recomputation with updated parameters; keep missing end-to-end training implementation explicitly marked as a Build gap.
- [x] Distinguish target scoring from held-out evaluation and state that evaluation aggregates metrics without updating parameters; the overview and evaluation graph view now expose this boundary.
- [x] Add explicit contrasts for generated vs observed token and prefill vs teacher forcing; retain likelihood vs loss and evaluation vs training as separate concepts.
- [x] Preserve the existing bilingual examples, equations, citations, exercises and implementation caveats in the teacher-forcing/prefill changes.

**Exit condition:** partially met. The new inference/training concepts and branch boundaries are explicit; the broader shared-core, scoring and training page audits remain.

### P2 — Produce and integrate the persistent visual spine

- [x] Reuse the canonical bilingual computational registry; its `persistent-spine`, generation, observed-target scoring, evaluation and training views already encode the common path and sibling branches.
- [x] Preserve generated-token feedback separately from observed-token/teacher-forced feedback in the graph.
- [x] Keep evaluation on held-out scoring/metrics and stop before gradients or optimizer updates.
- [x] State in the overview that the branches are distinct uses of one conditional distribution, not one executable loop.
- [x] Extend the existing renderer only: render the persistent-spine and evaluation views from the registry, with no new schema or frontend dependency.
- [x] Generate a bilingual semantic HTML text alternative from the same node descriptions and directed edges.
- [x] Pilot the persistent spine and evaluation view on the canonical FR/EN LLM overview; branch-specific views remain on their owning lessons.
- [ ] Validate rendered FR/EN parity, responsive behavior, color contrast, keyboard operation and screen-reader usability; source-level alternatives and automated tests do not replace this review.

**Exit condition:** met at source/render integration level. Manual rendered accessibility and responsive evidence remains.

### P2 — Align Build and practical implementation

- [x] Maintain the G0–G9 Build milestone crosswalk separately from the conceptual graph and guided route.
- [x] Keep G1b corpus preparation → G2 training examples as a training-data branch, not an inference prerequisite.
- [x] Add teacher forcing and shifted-target alignment to the bilingual Build training-examples lesson.
- [x] State that training uses the same shared prediction computation as inference, but differs in reference-target supply, loss, gradient tracking and parameter updates.
- [x] Keep prefill/decode/KV cache in the inference execution path.
- [ ] Complete the implementation evidence for GPT-weight autograd, optimizer, train/validation loop, reproducible run and checkpoint; these remain explicit Build gaps.

**Exit condition:** the conceptual and practical paths are cross-referenced and remain distinct; end-to-end training implementation evidence remains outstanding.

### P2 — Automated and manual validation

- [ ] Extend existing validators only where a real invariant is currently untested; avoid creating a generic graph framework.
- [ ] Test concept IDs and relation endpoints, bilingual page references, domain/tag consistency, branch membership, and Core/Deepen classification.
- [ ] Test guided-route coverage and intentional repeated page appearances.
- [ ] Test page metadata parent/child and previous/next references independently.
- [ ] Test the visual's semantic fallback and generated links.
- [ ] Run format, lint, type checks, unit tests, full site render, and browser review.
- [ ] Review representative pages manually in FR and EN for scientific correctness and reader comprehension.

**Exit condition:** automated checks cover structural invariants, while manual review covers the pedagogical claims that cannot be established by schema validation alone.

## 4. Recommended session sequence

To keep each session reviewable and avoid excessive tooling, continue from the current integrated state:

1. **Complete the persistent-view PR:** validate the generated persistent-spine and evaluation views, bilingual text alternatives, and the overview-page embedding. Keep the existing registry and renderer as the only source.
2. **Rendered navigation and accessibility review:** use the existing Quarto/browser review and issues #337, #347 and #320. Inspect breadcrumbs, nested sidebar, previous/next links, desktop/mobile layout, keyboard operation and screen-reader behavior; record evidence rather than inferring it from source tests.
3. **Finish bounded metadata/content audits:** complete the remaining shared-core, scoring, training and evaluation page inventory. Preserve the distinction between conceptual containment, recommended reading transitions, route membership and computational edges.
4. **Complete the Build crosswalk:** verify G0–G9 against actual implementation evidence, retain G1b → G2 as the separate training-data branch, and record the remaining end-to-end training gaps.
5. **Final validation:** run format, lint, type checks, unit tests, full Quarto render and rendered browser review on the final integrated head.

Each session should produce a small PR or a clearly bounded set of commits, update this checklist, and record test evidence. Do not combine broad page rewrites, route redesign, renderer refactors, and visual design into one large change.

## 5. Explicit non-goals and anti-patterns

- No new parallel concept ontology or duplicate computational graph.
- No generic workflow engine, per-page CI job, or elaborate graph-rendering framework.
- No automatic page-parent assignment from curriculum module membership.
- No prerequisite inferred from sidebar order, route order, or computational dataflow.
- No single linear chain that places scoring/loss/gradients inside ordinary generation.
- No duplicate canonical page for a concept merely because it appears in multiple learning contexts.
- No content deletion during page consolidation.
- No claim that a rendered diagram proves learner comprehension.

## 6. Definition of done for issue #575

Issue #575 can be considered complete when:

1. The shared computational model and module scopes remain canonical and scientifically accurate.
2. Guided route, Quarto hierarchy, page metadata, and Build crosswalk agree with the model while preserving their distinct semantics.
3. The persistent spine and branch views are available in FR and EN, with accessible text fallback.
4. Teacher forcing, prefill, decode, and KV cache have accurate, non-conflicting placements.
5. Automated structural checks and full rendered/browser review pass.
6. Representative FR/EN pages have been manually checked for content preservation and conceptual clarity.
7. The remaining limitations and validation evidence are recorded in this plan.

