# Computational spine integration plan

**Status:** active follow-up plan  
**Date:** 2026-11-06  
**Parent:** [#575 — Provide one persistent computational spine across inference, scoring and learning](https://github.com/JM-Brun/llm-lab/issues/575)  
**Architectural authority:** [Canonical computational spine](canonical-computational-spine.md) and the canonical module topology in [learning-path.md](learning-path.md#canonical-module-topology-shared-core-and-operational-branches).

This document is the durable hand-off for future work sessions. It records what has been completed, what remains, the intended order, and the evidence required to close the work. It is a task plan, not a new concept registry, curriculum hierarchy, or computational graph.

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

### Metadata ownership invariant

The repository has distinct canonical sources for distinct questions: `data/concepts.yml` owns concept identity, definitions, domains and typed semantic relations; `data/computational-graph.yml` owns computational dataflow and branch membership; `data/guided-route.yml` owns the reader-facing stage sequence; Quarto page-map metadata owns page editorial role and page-to-page navigation. These structures are connected through explicit references, but they are not interchangeable graphs. In particular, page tags must not duplicate concept IDs or domain memberships, computational edges must not be read as pedagogical prerequisites, and importance must not be used to infer route order. See [the concept-card metadata audit](audits/concept-card-metadata-audit-2026-11-06.md) for the detailed ownership contract.


### P0 — Verify the merged navigation in the rendered site

- [ ] Run and inspect the current Quarto render for both languages after PR #582.
- [ ] Verify native breadcrumb ancestry on representative pages at each nesting depth: overview, text input, representations, Transformer computation, prediction, scoring, training, and optional depth.
- [ ] Verify the learning map and its static fallback preserve all nested sections, page counts, links, and empty-section behavior.
- [ ] Review desktop and mobile layouts; check wrapping, nested-card density, focus order, keyboard operation, accessible names, and screen-reader structure.
- [ ] Check Quarto previous/next links. The reader-facing preview-first order is intentional, but no accidental navigation into optional material should interrupt the core sequence.
- [ ] Record screenshots or browser-review evidence and fix concrete defects before generalizing the hierarchy to Build, Deepen, Practice, or Reference.

**Exit condition:** bilingual rendered pages and learning-map views agree with the authored sidebar hierarchy; no dead links, misleading ancestry, inaccessible nested controls, or unintended previous/next transitions remain.

### P1 — Reconcile the guided route with the sibling branches

Current source to audit: `data/guided-route.yml`. Its six-stage route currently includes generation in Orientation and again in Prediction, and includes likelihood in Prediction. The new topology gives generation a canonical Inference role and likelihood a Scoring role. This is not automatically a defect: the guided route may deliberately preview or revisit a page, but each appearance must have a clear learning objective and depth.

- [ ] Map every current stage and page membership to the canonical module IDs in `docs/learning-path.md`.
- [ ] Decide whether the route should expose separate reader-facing stages for **Inference**, **Observed-target scoring**, **Training**, and **Evaluation**, or retain fewer stages with explicit branch labels. Do not force one stage per module if that makes the route harder to learn.
- [ ] Preserve the early generation preview only if it is clearly labelled as an overview/black-box preview; distinguish it from the later detailed inference treatment without duplicating canonical page identity.
- [ ] Move the conceptual role of likelihood out of the shared prediction stage: it is computed by comparing the shared distribution with an observed target.
- [ ] Ensure cross-entropy is explained as target scoring and as a training objective component, without duplicate canonical ownership.
- [ ] Place predictive entropy with the distribution/prediction concepts, not under observed-target scoring.
- [ ] Represent evaluation as held-out scoring/metrics without a parameter-update edge.
- [ ] Make teacher forcing explicit in the training/scoring context where observed targets are fed back; do not describe it as prefill.
- [ ] Preserve optional-page memberships and reading-depth distinctions.
- [ ] Validate FR/EN parity, page references, ordering, generated partials, and all consumers of the route data.

**Exit condition:** every route stage has one clear objective; every page membership has a justified role; the route explains the shared distribution and its sibling branches without suggesting one linear execution chain.

### P1 — Reconcile concept-card metadata ownership

- [ ] Use [the 2026-11-06 concept-card metadata audit](audits/concept-card-metadata-audit-2026-11-06.md) as the source-level baseline.
- [ ] Keep canonical notion identity in `data/concepts.yml`; do not add a redundant `notion:` page tag or page-level concept list.
- [ ] Keep concept-domain membership many-to-many in `data/concepts.yml` and the controlled vocabulary in `data/domains.yml`; do not copy it into the Deepen-only page `domain` field.
- [x] Review a controlled `core` / `supporting` / `specialized` classification for all 41 concepts against the canonical route and computational branches; rationale is recorded in the concept-card metadata audit. Values are project-relative, not universal rankings.
- [x] Add required `importance` to concept-registry schema version 2, validate the enum in the existing registry checker, pass it through the existing JSON projection, and render a localized secondary cue in the existing concept cards and details.
- [ ] Verify bilingual rendered output and accessibility; ensure importance does not change domain grouping, search, typed relations, or route order.

**Exit condition:** notion identity, subject domain, concept importance, page depth, and page destination each have one clear owner and no duplicated metadata dimensions.
 
### P1 — Audit page metadata and breadcrumb semantics

Use the existing page-map metadata schema and contract; do not add a new per-page breadcrumb field.

- [ ] Inventory pages belonging to the shared core and its three operational branches, in both languages.
- [ ] For each page, review `hierarchy.parents/children` as **conceptual containment only**. Do not copy module membership into page parent/child edges mechanically.
- [ ] Review `suggested_route.previous/next` as recommended pedagogical transitions. Do not infer them from sidebar order or computational dataflow alone.
- [ ] Keep page tags within the existing editorial vocabulary. Do not introduce `notion:` or `domaine:` tags: concept identity and multi-domain membership are already owned by `data/concepts.yml`. If page-to-concept discoverability needs improvement, extend the existing learning-map projection from canonical concept resources rather than duplicating IDs in page metadata.
- [ ] Ensure concepts such as prefill, decode step, KV cache, teacher forcing, observed target, likelihood, NLL, cross-entropy, gradient, optimizer, parameter update, and held-out evaluation are discoverable at their canonical pages.
- [ ] Preserve existing stable slugs, especially French `probabilites`; do not create duplicate FR/EN concepts or pages.
- [ ] Add or correct cross-links for cross-branch concepts rather than assigning misleading additional parents.
- [ ] Check that the page metadata validator catches invalid IDs, asymmetric or dangling hierarchy links, inconsistent bilingual tags, and invalid route references.

**Exit condition:** metadata describes the actual content and intended reading transitions; no module scope is mistaken for conceptual containment or a prerequisite.

### P1 — Reconcile page content without losing knowledge

- [ ] Audit the shared-core pages from text/tokens through embeddings, positional information, initial hidden states, Transformer blocks, final contextualized states, logits, and softmax.
- [ ] Verify Q/K/V are presented as operations inside each Transformer block, not after final contextualized representations.
- [ ] Clarify the common forward pass and its boundary at the conditional distribution.
- [ ] Audit generation/decoding content: greedy selection, sampling, temperature, top-k/top-p, stopping, generated-token feedback, prefill, decode steps, and optional KV-cache details.
- [ ] Audit scoring content: observed target, target probability, sequence likelihood, log-likelihood, NLL, token cross-entropy, reduction, masking, and numerical stability.
- [ ] Audit training content: shifted inputs/targets, teacher forcing, token losses, batch aggregation, gradients, optimizer, parameter update, and recomputation with updated parameters.
- [ ] Audit evaluation content: held-out split, leakage boundaries, metrics and uncertainty; make explicit that evaluation does not update model parameters.
- [ ] Add explicit contrasts where confusion is likely: generated vs observed token; prefill vs teacher forcing; likelihood vs loss; evaluation vs training.
- [ ] Keep mathematical derivations and implementation details at the appropriate Core/Deepen depth.
- [ ] Map every moved or consolidated explanation to its canonical destination before editing; preserve examples, equations, citations, exercises, and caveats.

**Exit condition:** each page states its scope, shared-spine position, branch role, prerequisites, and onward links; no scientific distinction or existing useful content is lost.

### P2 — Produce and integrate the persistent visual spine

- [ ] Design one canonical, bilingual visual representation of the shared context → forward pass → logits → conditional distribution core and the sibling inference/scoring/training branches.
- [ ] Show the two context-extension policies distinctly: generated-token feedback versus observed-token/teacher-forced feedback.
- [ ] Show evaluation as a scoring/measurement path that stops before gradients and optimizer updates.
- [ ] Make the visual explicit that these are conceptual connections, not one execution loop.
- [ ] Decide the smallest maintainable implementation: preferably one reusable visual/include or a compact data-backed renderer, not a new graph framework or per-page pipeline.
- [ ] Provide a semantic text/list equivalent and meaningful alternative text; the diagram must not be the only carrier of information.
- [ ] Integrate the visual on a small representative page set first, then expand only where it materially improves orientation.
- [ ] Validate FR/EN parity, responsive rendering, color contrast, keyboard/screen-reader fallback, and links to canonical pages.

**Exit condition:** one maintained source yields a consistent visual and accessible textual representation; no duplicated hand-authored diagrams drift across pages.

### P2 — Align Build and practical implementation

- [ ] Crosswalk the shared conceptual model to Build milestones without treating the Build sequence as the conceptual graph.
- [ ] Locate tokenizer fitting/freezing, corpus preparation, context windows, shifted targets, batches, and masks in the training-data branch.
- [ ] Ensure Build examples demonstrate teacher forcing and next-token target alignment explicitly.
- [ ] Show that the training forward pass uses the same model prediction mechanism as inference, while differing in target supply, loss computation, gradient tracking, and parameter updates.
- [ ] Keep prefill/decode/KV cache in the inference execution path; do not make them prerequisites for the training path.
- [ ] Avoid duplicating conceptual explanations already owned by Understand pages; Build should emphasize implementation and evidence.

**Exit condition:** the conceptual and practical paths cross-reference each other while preserving their distinct ordering and purpose.

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

To keep each session reviewable and avoid excessive tooling, use this order:

1. **Session A — Rendered navigation audit:** inspect the merged PR #582 result; fix only evidenced breadcrumb, learning-map, responsive, or accessibility defects.
2. **Session B — Guided-route design:** produce a short FR/EN stage-to-module crosswalk and resolve generation/likelihood/entropy placement before editing route YAML.
3. **Session C — Page metadata audit:** audit a bounded representative set first (prediction, generation, likelihood/cross-entropy, training examples/loss/gradients, evaluation), then expand based on findings.
4. **Session D — Page-content audit:** review the same representative set for conceptual accuracy and content preservation; handle teacher forcing and prefill explicitly.
5. **Session E — Persistent visual:** implement one maintainable bilingual visual and text fallback, then pilot it on the representative pages.
6. **Session F — Build crosswalk and final validation:** reconcile practical milestones, run the full validation suite, and complete the rendered/browser review.

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

