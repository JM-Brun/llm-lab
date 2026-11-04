# Interactive learning map — source audit and remaining work

**Review date:** 2026-11-04  
**Scope:** source-level metadata integrity, curriculum alignment, and follow-up work for the bilingual interactive map.  
**Coordination:** [#337](https://github.com/JM-Brun/llm-lab/issues/337), [#415](https://github.com/JM-Brun/llm-lab/issues/415), [#416](https://github.com/JM-Brun/llm-lab/issues/416), [#417](https://github.com/JM-Brun/llm-lab/issues/417).

## 1. Executive result

The repository already has a structural metadata validator: `scripts/check_page_metadata.py`. Do not create a second validator for the same invariants.

The validator reads the explicit Quarto `project.render` inventory and checks:

- page-map metadata placement, YAML structure, required fields, stable IDs, and controlled tags;
- source-path/render-list coverage and duplicate IDs/paths;
- existence and published status of every referenced page;
- reciprocity of parent/child relations;
- reciprocity of `suggested_route.previous/next` links;
- acyclicity of the suggested-next graph and the conceptual hierarchy;
- French/English counterpart parity using the stable `topic` identifier rather than translated slugs.

### Current CI and audit evidence

The existing validator remains the source of truth for structural invariants. The topology audit in [learning-map-topology-audit.md](learning-map-topology-audit.md) was run against the published-page inventory on `main` commit `82606ee4a9c77f9be2dc5a1e8c8931bc79e370b1` (2026-11-04):

- 103 published pages were analyzed (51 FR, 51 EN, one shared reference page).
- FR and EN each have six separate suggested-route chains, 28 route edges, 34 participating pages, and no convergence or unrooted route components.
- 17 pages per language intentionally or potentially sit outside the suggested route; they are grouped by destination rather than labelled as orphans.
- The structural validator reported no broken references, route/hierarchy reciprocity errors, cycles or FR/EN parity errors.
- The hierarchy contains fan-out and multi-parent hubs; these are not prerequisites and are not merged into the route graph.

The report is being added with PR #429. Its first CI execution successfully ran the audit and printed the topology, but the workflow subsequently stopped at Ruff formatting; that formatting is being corrected. These are structural findings, not evidence that the route is pedagogically optimal or that rendered interactions are accessible.

## 2. Curriculum contract to preserve

The canonical source is [`docs/learning-path.md`](learning-path.md), with page ownership and destination classification in [`docs/content-section-mapping.md`](content-section-mapping.md).

The map must preserve these distinct structures:

1. **Conceptual inference route:** LLM orientation → generation preview → text/tokens → representations → Transformer/attention → prediction/decoding.
2. **Learning/training explanation:** introduced after inference, including next-token objective, likelihood, cross-entropy/loss, gradients and optimization.
3. **Build dependency route:** implementation order for the small GPT; it may branch into corpus preparation and training examples (G2) and must not be conflated with the conceptual route.
4. **Deepen:** optional advanced material, not mandatory prerequisites.
5. **Practice & experiment:** transversal activity, not a final stage or a fourth learning depth.

Generation appearing before detailed tokenization and probability is intentional: it provides a black-box preview of autoregressive inference with fixed parameters. Corpus preparation and shifted training examples belong to a later Build branch, not to the inference prerequisites.

## 3. Generator caveat

`scripts/build_learning_map.py::assign_route_rank()` performs a breadth-first traversal that follows both `suggested_route.next` and `hierarchy.children`. The resulting `rank` is therefore only a deterministic display-order heuristic for arranging page nodes. It is not:

- a pedagogical sequence;
- a prerequisite ordering;
- a topological ordering of the page graph;
- a substitute for the explicit curriculum milestones.

The page-map schema correctly distinguishes route, hierarchy and related links. The generated graph must preserve those distinctions and must not label the BFS rank as learning order.

## 4. Remaining source-level work

### P1 — topology report and curriculum reconciliation (#415)

- [x] Extend the existing `scripts/audit_page_metadata.py` with a topology report; reuse the structural validator rather than duplicating it (PR #429).
- [x] Separate suggested-route chains from hierarchy fan-out, multi-parent nodes and related links.
- [x] Record route starts/ends, chains, convergence, unrooted components, route-free pages by destination and isolated pages.
- [x] Compare the six-stage conceptual route with the G0–G9 Build milestones; record the deliberate G2 training-data branch and G1b corpus-preparation branch.
- [x] Repair the malformed G0–G9 tables in `docs/content-section-mapping.md`: normalize the summary table, correct the G3/G2 labels, add the missing G2 evidence row, and align G1/G1b and G6 claims with the source implementation (PR #429).
- [ ] Review the `glossary → transformer-history` suggested-route chain against the editorial rule that history is optional reference context.
- [ ] Decide whether the three route-free Understand pages (entropy, LLM limits and Transformer architectures) are intentionally standalone; do not add route links merely to eliminate nulls.
- [ ] Review the five fully isolated landing/reference pages and record why they intentionally sit outside the graph.

### P2 — guided route view (#415)

- [x] Define six bilingual reader-facing conceptual stages with objectives, core pages and optional deepening (PR #424).
- [x] Keep the exhaustive page graph separate from the guided route.
- [x] Keep the small-GPT Build path as a practical companion and the G2 data branch separate from inference.
- [x] Generate the guided route as native Quarto Markdown with Python and validate all bilingual page references.
- [ ] Complete browser, mobile, keyboard and touch inspection; CI rendering is not a substitute for this evidence (#337/#417).

### P2 — concept graph (#416)

- [ ] Keep `data/concepts.yml` as the canonical language-independent concept registry.
- [ ] Show relation direction and semantic families persistently; expose the exact relation type on selection/focus.
- [ ] Choose a layout based on the actual relation semantics; do not imply a prerequisite DAG where none exists.
- [ ] Reduce visual density through overview plus local-neighbourhood exploration.

### P2 — interaction and accessibility (#417)

- [ ] Separate node selection from the explicit “open page” action.
- [ ] Provide equivalent mouse, keyboard and touch interactions, persistent selection, visible focus and focus restoration.
- [ ] Add fit/reset controls, responsive behavior, informative empty/error states and retry.
- [ ] Explain when filters hide relation endpoints.
- [ ] Retain a usable list alternative independent of the SVG.

### P2 — rendered inspection (#337)

- [ ] Inspect the published FR and EN maps at desktop, tablet and narrow-mobile widths.
- [ ] Record browser, language, page and viewport dimensions.
- [ ] Check link destinations, keyboard-only operation, touch behavior, screen-reader order and focus management.
- [ ] Keep this evidence separate from successful Quarto rendering and CI.

## 5. Recommended execution order

1. Reconcile the site-tool relocation across PRs #422, #424 and #429 before merging: keep the audit and map generators, their imports, tests, workflow commands and local instructions together.
2. Repair the G0–G9 crosswalk tables and review the two route exceptions identified above.
3. Rework the concept graph relation semantics and layout (#416).
4. Complete desktop/mobile, keyboard, focus, touch and screen-reader inspection (#337/#417).
5. Only then consider any metadata changes justified by the editorial review.

## 6. Evidence boundaries

- Passing metadata validation proves structural invariants only.
- Passing Quarto proves successful generation, not browser-level visual quality.
- Passing local-link checks proves rendered local destinations resolve, not that the navigation is pedagogically optimal.
- No claim about learner mastery or learning effectiveness is made without learner evaluation.
