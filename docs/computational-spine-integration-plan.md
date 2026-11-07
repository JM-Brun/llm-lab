# Computational spine integration plan

**Status:** active follow-up plan  
**Date:** 2026-11-06  
**Parent:** [#575 — Provide one persistent computational spine across inference, scoring and learning](https://github.com/JM-Brun/llm-lab/issues/575)  
**Architectural authority:** [Canonical computational spine](canonical-computational-spine.md) and the canonical module topology in [learning-path.md](learning-path.md#canonical-module-topology-shared-core-and-operational-branches).

This document is the durable hand-off for future work sessions. It records what has been completed, what remains, the intended order, and the evidence required to close the work. It is a task plan, not a new concept registry, curriculum hierarchy, or computational graph.

## 0. Current status — 2026-11-07 (after PRs #625 and #627)

| Work package | Status | Evidence / remaining boundary |
|---|---|---|
| Canonical computational model and typed branches | Integrated | `docs/canonical-computational-spine.md`; PRs #577, #578, #589, #599 and follow-ups |
| Eight-stage guided route and bilingual projections | Integrated | `data/guided-route.yml`, generated FR/EN fragments; PRs #578, #586, #594, #616 |
| Teacher forcing, prefill and incremental decode | Integrated in lessons | PR #601; conceptual teaching is present, but the reference code still has no optimized KV-cache decode |
| Concept domains and importance | Integrated | `data/concepts.yml`, `data/domains.yml`; PR #593 |
| Persistent spine and branch views | Integrated | PR #589; bilingual semantic text alternatives generated from the computational registry |
| Scoring and observed-prefix semantics | Integrated at source level | PRs #599 and #604; page-by-page mathematical and rendered review remains |
| Build crosswalk and implementation evidence | Reconciled; implementation gaps remain | PRs #598 and #600; no end-to-end GPT training loop, optimizer/checkpoint path or reproducible training run |
| Contextual suggested-route navigation | Integrated | PR #625 generates route cues from existing `suggested_route.previous/next`; Quarto sidebar remains at `collapse-level: 1` |
| Browser-audit routing for UX branches | Integrated | PR #627 adds `ux/` to the six existing conditions; no separate workflow/job was added |
| Automated rendered/browser review | Passed with one investigation item | PR #627 workflow: 192 cases, 0 audit failures, 0 horizontal overflow, 0 axe violations; 360 SVG transform console errors were recorded on the FR/EN LLM overview cases |
| Manual accessibility and breadcrumb review | Open | Actual screen-reader review and native breadcrumb ancestry/behavior still require explicit evidence |
| Bounded FR/EN content audit | Partial | Existing `docs/page-audit-inventory.md`; shared-core, scoring/training/evaluation review is not complete |

The browser audit ran in the PR #627 workflow against the rendered tree containing the merged #625 navigation changes. The artifact is attached to workflow run [42261660816](https://github.com/JM-Brun/llm-lab/actions/runs/42261660816). It covers 192 browser cases across FR/EN, desktop/mobile and light/dark visual profiles, including the learning map, overview, route-context pages, Build tours and deep-dive parents. It reports no test failures, no horizontal overflow and no axe violations. Keyboard review ran in 90 cases and recorded 3,037 focus targets, all reported as focus-visible.

**Important qualification:** the report also records repeated SVG console errors on `llm-overview.html` in both languages: `<g> attribute transform: Expected number, "translate(undefined, NaN)"` (360 occurrences across the reviewed cases). These did not fail the current audit and did not produce page errors or axe violations, but they are a real rendered defect to trace and fix before treating the overview visualization as clean. Automated axe checks do not replace manual screen-reader testing.

## 1. Architectural invariant

For a context containing preceding tokens (observed or generated), the model computes one conditional next-token distribution:

[
z_t=f_\theta(x_{<t}), \qquad
p_\theta(\cdot\mid x_{<t})=\operatorname{softmax}(z_t).
]

Three sibling operational branches use this shared result:

- **Inference:** decode/select a token, append the generated token to the context, and continue with unchanged parameters.
- **Scoring:** condition on the observed prefix (teacher forcing), compare the distribution with the next observed target, and obtain its target probability and likelihood-related quantities; do not select a token and do not update parameters.
- **Training:** use teacher-forced observed targets to form a loss, compute gradients, and update parameters. The next training computation uses the updated parameters.

Evaluation applies the same observed-prefix scoring procedure to held-out data and stops before differentiation or the optimizer update. These branches are related, but are not one executable loop. The context is extended with a generated token during inference and with an observed token during teacher-forced scoring/training.

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

### P0 — Close the rendered-navigation review without overstating accessibility

The current bilingual Quarto/browser workflow has now run successfully on the merged tree through PR #627. The previous branch-prefix gap is fixed for the `ux/` family by reusing the existing workflow.

- [x] Render the bilingual site and validate the learning-map controls, knowledge-graph export, history timeline parity and local links.
- [x] Review the learning map and its rendered controls in FR/EN, desktop/mobile and light/dark profiles.
- [x] Check Quarto footer previous/next links and localized accessible names independently of document-level `rel` metadata.
- [x] Exercise keyboard focus and interactions in the automated review; confirm no axe violations and no horizontal overflow in the 192 recorded cases.
- [x] Keep `collapse-level: 1` in both language sidebars.
- [ ] Trace and fix the repeated SVG transform error on the FR/EN LLM overview (`translate(undefined, NaN)`); add a regression assertion so console errors of this class are not silently ignored.
- [ ] Verify native breadcrumb ancestry and behavior manually on representative pages at each nesting depth.
- [ ] Perform a real screen-reader pass in FR and EN and record browser, assistive technology, pages, and findings. Axe is not a substitute.
- [ ] Inspect the saved overview screenshots and route cards for information hierarchy and reader usefulness; automated assertions alone do not establish that the cues are pedagogically clear.

**Exit condition:** the browser audit is clean of relevant console/runtime errors; rendered pages, breadcrumbs and suggested-route cues are coherent in both languages; manual keyboard and screen-reader evidence is recorded. The current automated success is an intermediate gate, not full accessibility sign-off.

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


## 7. Next tasks and remaining work — 2026-11-07

The following order minimizes churn and keeps each task independently verifiable.

### P0 — Repair the overview SVG runtime error

- [ ] Identify the SVG/diagram whose group transform receives undefined coordinates on `llm-overview.qmd` in both languages.
- [ ] Trace whether the cause is missing node coordinates, a zero-sized/hidden layout container, or an initialization/measurement race; do not assume the cause from the browser message alone.
- [ ] Fix the shared source or renderer once, not the FR and EN outputs independently.
- [ ] Add a focused regression test for finite SVG transform coordinates or the underlying layout invariant.
- [ ] Re-run the existing Quarto/browser workflow and confirm the console error count is zero on both overview pages.

### P1 — Complete reader-facing accessibility and navigation evidence

- [ ] Manually verify native breadcrumbs and their ancestry/labels at overview, nested concept, Build, scoring/training and deep-dive levels.
- [ ] Perform a screen-reader review in both languages; record the actual browser/AT combination and any reading-order, landmark, disclosure, diagram alternative or navigation issues.
- [ ] Review the contextual route cues from PR #625 in their rendered page context; ensure they are distinct from Quarto previous/next, hierarchy breadcrumbs and related links.
- [ ] Keep the sidebars at `collapse-level: 1`; assess improvements through better entry/exit links and local context rather than expanding all sidebar levels.

### P1 — Finish the bounded scientific/content audit

- [ ] Complete the first shared-core slice: Q/K/V, scaled dot-product attention, causal masking, positional encoding and tensor shapes; verify equations, conventions, dimensions, FR/EN parity and references.
- [ ] Finish the scoring chain: observed prefix/target alignment, target probability, sequence likelihood/log-likelihood, NLL/cross-entropy, masking/reduction and numerical stability.
- [ ] Finish the training/evaluation boundary review: teacher forcing, batch aggregation, gradients, optimizer update, held-out scoring and metric interpretation.
- [ ] Reconcile each finding in `docs/page-audit-inventory.md`; do not mark a page complete merely because it renders or has a source list.
- [ ] Preserve the implementation boundary: the project does not yet provide end-to-end GPT-weight autograd, optimizer training, checkpointing or a reproducible trained checkpoint.

### P2 — Run the remaining page-group and navigation audits

- [ ] #320: text → tokens → embeddings page group, rendered FR/EN.
- [ ] #337: curriculum map, site navigation, breadcrumbs and route crosswalk in the published/rendered site.
- [ ] #347: training-examples → loss → generation → evaluation page group, rendered FR/EN.
- [ ] #415: make the guided route and resource map visibly distinct while reusing the existing curriculum and metadata.
- [ ] #416: improve typed concept-graph readability and relation semantics without implying an unsupported prerequisite DAG.

These are existing audit owners; do not create duplicate issues or a parallel roadmap. Keep #130 as the coordination epic and #584 as the computational-spine integration hand-off.

### Separate implementation roadmap — #78

- [ ] Retain G1 end-to-end tokenizer/corpus pipeline and G3 modularity as separately scoped implementation gaps.
- [ ] Treat G8 end-to-end training (autograd through GPT weights, optimizer, train/validation loop, checkpointing) and G9 reproducible evaluation as future implementation work, subject to the existing prerequisite-knowledge gate.
- [ ] Do not let these implementation gaps block source-level conceptual audits or reader-navigation improvements.

