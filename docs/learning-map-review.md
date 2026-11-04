# Interactive learning map — source audit and remaining work

**Review date:** 2026-11-04  
**Scope:** source-level metadata integrity, curriculum alignment, and follow-up work for the bilingual interactive map.  
**Coordination:** [#337](https://github.com/JM-Brun/llm-lab/issues/337), [#415](https://github.com/JM-Brun/llm-lab/issues/415), [#416](https://github.com/JM-Brun/llm-lab/issues/416), [#417](https://github.com/JM-Brun/llm-lab/issues/417).

## 1. Executive result

The repository already has a structural metadata validator: `site/tools/check_page_metadata.py`. Do not create a second validator for the same invariants.

The validator reads the explicit Quarto `project.render` inventory and checks:

- page-map metadata placement, YAML structure, required fields, stable IDs, and controlled tags;
- source-path/render-list coverage and duplicate IDs/paths;
- existence and published status of every referenced page;
- reciprocity of parent/child relations;
- reciprocity of `suggested_route.previous/next` links;
- acyclicity of the suggested-next graph and the conceptual hierarchy;
- French/English counterpart parity using the stable `topic` identifier rather than translated slugs.

### Current CI evidence

On `main` commit `64cb6fcf44508438fbea6ff2e90973baedaaa42e` (2026-11-04):

- [Python CI](https://github.com/JM-Brun/llm-lab/actions/runs/41843482932) passed, including **Validate page metadata learning graph**.
- [Quarto site workflow](https://github.com/JM-Brun/llm-lab/actions/runs/41843482902) passed, including metadata validation, bilingual site rendering, knowledge-graph export and local rendered-link checks.
- [Site publication workflow](https://github.com/JM-Brun/llm-lab/actions/runs/41843482969) completed successfully.

**Interpretation:** no broken page references, route reciprocity violations, hierarchy reciprocity violations, cycles, or FR/EN metadata-parity violations were reported by the existing validator on this commit. This is structural evidence, not evidence that the recommended sequence is pedagogically optimal or that the rendered interaction is accessible.

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

`site/tools/build_learning_map.py::assign_route_rank()` performs a breadth-first traversal that follows both `suggested_route.next` and `hierarchy.children`. The resulting `rank` is therefore only a deterministic display-order heuristic for arranging page nodes. It is not:

- a pedagogical sequence;
- a prerequisite ordering;
- a topological ordering of the page graph;
- a substitute for the explicit curriculum milestones.

The page-map schema correctly distinguishes route, hierarchy and related links. The generated graph must preserve those distinctions and must not label the BFS rank as learning order.

## 4. Remaining source-level work

### P1 — topology report and curriculum reconciliation (#415)

- [ ] Extend `site/tools/audit_page_metadata.py` (rather than duplicating the validator) with a concise topology report: route starts/ends, route chains, hierarchy branches, high-degree hubs, isolated pages, and pages with intentionally null routes.
- [ ] Separate observed graph facts from editorial interpretations. A null route can be a deliberate deep-dive entry; isolation is a review candidate, not automatically a defect.
- [ ] Compare route chains to the conceptual sequence and Build branches in `docs/learning-path.md`.
- [ ] Record deliberate exceptions: generation preview, Build hub, G2 data branch, Deepen pages, Practice pages, and reference resources.
- [ ] Review whether the current BFS display rank should be replaced by a stable sort key or explicitly named `display_rank`. Do not use it to generate the guided curriculum.
- [ ] Only change page metadata when a concrete semantic inconsistency is confirmed; preserve a useful `related` link when a hierarchy edge is removed.

### P2 — guided route view (#415)

- [ ] Define a small number of reader-facing stages from existing curriculum milestones, with objective, expected outcome, entry page, recommended continuation and optional deepening.
- [ ] Model branches explicitly; do not turn every page into a step.
- [ ] Keep the exhaustive page graph as a separate exploratory view.
- [ ] Keep the practical small-GPT route connected to relevant conceptual stages without forcing it into one linear theoretical route.
- [ ] Provide equivalent French and English labels and a textual alternative.

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

1. Produce the topology report using the existing metadata loader and validator.
2. Reconcile the route topology with the canonical curriculum; record exceptions and only then correct confirmed metadata defects.
3. Clarify the generator's display-order semantics and add focused tests.
4. Implement the guided route view from explicit curriculum data.
5. Rework the concept graph and interaction layer.
6. Complete bilingual browser and accessibility inspection.

## 6. Evidence boundaries

- Passing metadata validation proves structural invariants only.
- Passing Quarto proves successful generation, not browser-level visual quality.
- Passing local-link checks proves rendered local destinations resolve, not that the navigation is pedagogically optimal.
- No claim about learner mastery or learning effectiveness is made without learner evaluation.
