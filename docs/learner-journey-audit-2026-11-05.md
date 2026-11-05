# Main learner journey audit and follow-up plan

**Audit date:** 2026-11-05  
**Scope:** learner-facing conceptual route, guided build, optional depth, practice/experimentation, and the evidence needed to validate the journey.  
**Evidence level:** source-level review of the current default branch and planning artefacts. This is not a browser usability study, a full page-by-page scientific audit, or evidence of learner mastery.

## 1. Executive assessment

LLM Lab has a sound pedagogical architecture: four destinations with distinct responsibilities (Understand, Build, Deepen, Practice & experiment), a conceptual route that introduces inference before training, and a separate implementation route. The project correctly distinguishes a page/resource graph from a recommended learning sequence and distinguishes tested inference mechanics from an end-to-end trained language model.

The main gap is no longer the absence of a curriculum design. It is the distance between the intended route and its demonstrated usability and learning outcomes:

1. The route is represented in several artefacts with different granularity. Their differences are legitimate, but their ownership and correspondence must remain explicit and mechanically checked where practical.
2. The Build route currently guides inspection and execution of an existing NumPy reference implementation. It does not yet establish independent construction, and it does not deliver a complete data-to-training-to-evaluation pipeline.
3. The course contains exercises and tests, but independent evidence that learners can explain, predict, diagnose and transfer the concepts is still limited.
4. Source-level and CI checks do not substitute for rendered browser, responsive, accessibility or learner validation.

**Overall judgement:** strong design foundation; incomplete operational and empirical validation. The previous conversational score of 7.5/10 should be treated only as a qualitative shorthand, not a measured score or benchmark. No aggregate score is maintained in this document.

## 2. Scope and evidence reviewed

Reviewed current repository artefacts:

- `site/index.qmd`: entry routes, conceptual SVG route, operational-process diagram, evidence labels.
- `site/fr/build-path.qmd`: guided implementation promise, five walkthroughs, runnable reference example and limitations.
- `data/guided-route.yml`: six machine-readable conceptual stages and optional pages.
- `docs/learning-path.md`: curriculum order, G0–G9 implementation milestones, dependencies and evidence.
- `docs/content-section-mapping.md`: ownership boundaries for Understand / Build / Deepen / Practice & experiment.
- `docs/information-architecture.md`: canonical ownership of page metadata, curriculum, concepts, resources and graph projections.
- `docs/project-status.md`: implementation, demonstration and remaining-work inventory.
- `docs/roadmap.md`: existing validation-first priorities.
- `docs/learner-validation-pilot.md`: proposed learner-validation protocol.

This audit is a focused synthesis, not a fresh exhaustive inspection of every bilingual lesson, sidebar entry, upstream Raschka chapter, or rendered page. The owning issues below contain the broader page-by-page and browser work.

## 3. What is working

### 3.1 Separation of reader destinations

| Destination | Reader question | Assessment |
|---|---|---|
| Understand | What happens in an LLM, why, and how does it fit together? | Appropriate home for the conceptual system explanation and essential equations. |
| Build | How do I turn the concepts into a small working GPT? | Appropriate distinct route, but the current scope/status must be communicated precisely. |
| Deepen | Why do the mechanisms have these properties, and where do assumptions and limits come from? | Good progressive-disclosure boundary for derivations, variants and research. |
| Practice & experiment | Can I calculate, implement, test, vary or falsify something? | Correctly transversal; it should not become a fourth depth or an unrelated exercise catalogue. |

Classification should continue to follow the primary learner task, not the mere presence of equations or code. Preserve the existing ownership rules in `docs/content-section-mapping.md`; do not introduce a competing taxonomy.

### 3.2 Conceptual sequence

The intended conceptual progression is sound:

1. Orient the reader to LLM families, objectives and lifecycle.
2. Preview a complete generation loop.
3. Explain text, tokens, vocabulary and token IDs.
4. Explain embeddings, positional information and contextualized representations.
5. Explain Transformer computation, Q/K/V, attention and causal masking.
6. Connect hidden states to logits, probabilities and token selection.
7. Explain the learning objective, loss, gradients and optimization.
8. Introduce adaptation and evaluation with their distinct meanings.

The ordering supports a useful distinction: inference uses fixed parameters; training updates parameters. An untrained random-weight GPT can demonstrate the mechanics of inference, but it must not be presented as producing useful learned language.

### 3.3 Separate implementation dependency path

G0–G9 and the G2 data-preparation branch express implementation dependencies rather than a second conceptual curriculum. Keep this distinction. Data preparation is needed for training, not for observing the inference loop.

The current reference implementation provides tested NumPy inference mechanics and walkthroughs. Current inventory still identifies an incomplete end-to-end tokenizer/corpus pipeline, incomplete training loop and incomplete held-out evaluation. These gaps must remain visible wherever the Build route is promoted.

## 4. Findings and decisions

### F1 — Multiple route representations need explicit correspondence (P0)

**Observation.** The homepage diagram has eight conceptual nodes; `data/guided-route.yml` has six broader stages; `docs/learning-path.md` also owns G0–G9 implementation milestones; the interactive map represents page/resource relationships. These are not necessarily inconsistent: they answer different questions and use different granularities.

**Risk.** A reader or maintainer may mistake a resource graph for a recommended sequence, or assume that diagram stages and curriculum stages are one-to-one.

**Decision.** Keep the distinct projections. Document their purpose and canonical owner, then validate only genuine correspondences (published page IDs, bilingual counterparts, route links and implementation milestone references). Do not force identical stage counts or duplicate the curriculum in another YAML file.

**Owner work:** #130, #225, #337, #415. The concept graph follow-ups #416/#417 are related UI work, not curriculum-source replacements.

### F2 — Build promise exceeds the currently demonstrated learner outcome (P0)

**Observation.** `site/fr/build-path.qmd` describes five walkthroughs: configuration, numerical operations, Transformer block, model assembly and generation. The walkthroughs guide inspection and execution of existing reference code. The page explicitly says this does not prove independent construction. The current reference model is randomly initialized and generates token IDs; it is not a trained language model.

**Risk.** “Construire un petit GPT” may be read as an already-complete from-scratch training course, when the current demonstrated scope is inference mechanics and guided code inspection.

**Decision.** Retain the title only with the explicit scope/status caveat already present. Separate outcomes in the page and curriculum:
- inspect and explain a reference implementation;
- reproduce it with guided support;
- reconstruct selected components independently;
- eventually implement data preparation, training, validation and checkpoint-based generation.

Do not claim the latter outcomes until code, tests, exercises and reproducible evidence exist. Add independent reconstruction exercises as a focused extension of the existing walkthroughs, not a duplicate implementation.

**Owner work:** #78 owns concept-to-code sequencing; #58 owns the training-data path; #225 owns conceptual order; the private prerequisite-knowledge gate in #78 remains mandatory before new implementation work.

### F3 — Mathematical prerequisites should be introduced just in time (P1)

**Observation.** The Understand/Deepen boundary explicitly keeps advanced derivations and general tensor theory optional while allowing essential equations and small calculations in core lessons.

**Risk.** A learner may be sent to broad prerequisite material before knowing why it is needed, or encounter a calculation without the minimum shape/notation support.

**Decision.** For each core mechanism, expose three levels in context: (1) intuition and purpose, (2) minimum operational calculation/notation, (3) optional derivation and generalization. Link the optional material at the point of need. Do not create a blanket mathematics prerequisite or duplicate a general mathematics course.

**Owner work:** #61 and #355 for progressive disclosure and content boundaries; #220 for the formative exercise sequence. Fix only concrete page-level defects found by those owners.

### F4 — Transfer and mastery evidence are weaker than content/CI evidence (P1)

**Observation.** Exercises, self-checks, executable snippets and tests exist, and a learner-validation pilot protocol is documented. The project status explicitly says that independent learner validation has not yet been established.

**Risk.** Recall questions, page completion, passing unit tests and successful rendering can be mistaken for conceptual understanding or transfer.

**Decision.** Evaluate at least four distinct outcomes: conceptual explanation, quantitative/mechanical prediction, implementation/debugging, and transfer to an unfamiliar case. Use short prompts that require prediction before revealing an answer. Score explanations against explicit criteria and record uncertainty/confidence separately. Keep individual mastery records private in `career-knowledge`, not in the public portfolio.

A small pilot can identify confusing wording and plausible misconceptions; one participant cannot establish population-level effectiveness or causal learning gains.

**Owner work:** #220 (exercise design), #329 (rendered exercise review), #447 (pilot execution), and #310/#320 where relevant to browser review. Reuse the existing pilot protocol; do not create a parallel assessment framework.

### F5 — Scientific experimentation should be a recurring learning loop (P1)

**Observation.** The project distinguishes definitions, derivations, tests and experiments, but this distinction is not yet operationalized uniformly in every core activity.

**Decision.** Where a mechanism can be experimentally inspected, structure an activity around: question → prediction → controlled change → observation → comparison → interpretation and limitation. Use a worked numerical example where appropriate. A test verifies specified cases/properties; an experiment supports conclusions only within its protocol and sample.

**Owner work:** #220 and the existing concept-specific experiment issues. Do not add decorative widgets or experiments without a stated learning question.

### F6 — Rendered route and accessibility still require separate evidence (P1/P2)

**Observation.** CI can validate source contracts, links and rendering, but it does not prove the actual reading experience at different viewports or input modes.

**Decision.** Keep the existing browser-review work distinct and record language, browser, viewport, page, reproducible observation and evidence. Do not claim accessibility conformance from a partial sample.

**Owner work:** #337 (navigation/map), #341 (homepage), #320 (text-to-representation pages), #329 (exercise pages), and #191 (design system).

## 5. Recommended learner journey

This is a reader-facing sequence, not a new canonical data model. It reuses the current pages and owners.

| Stage | Learner outcome | Core material | Optional detours / evidence |
|---|---|---|---|
| 1. Orient | Distinguish model family, architecture, objective and use | LLM panorama and limits | Architecture comparison; short classification prompt |
| 2. Observe generation | Explain the loop at a high level and why random weights do not produce useful language | Generation overview | Predict next loop state; inspect fixed-parameter behavior |
| 3. Encode input | Distinguish text, tokens, vocabulary and IDs | Text/data and tokenization | Unicode and tokenizer design; encode/decode exercise |
| 4. Represent input | Trace IDs to embeddings, positional information and contextualized states | Embedding, position and contextualized representations | Tensor shapes, RoPE; representation-tracing exercise |
| 5. Compute | Explain the forward computation and causal information flow | Transformer, Q/K/V, attention, causal masking | Score-scaling derivation, alternatives; controlled future-token intervention |
| 6. Predict | Trace hidden states to logits, probabilities and selection | Logits, probabilities, likelihood and generation | Decoding strategies; hand-calculated distribution |
| 7. Learn | Explain target alignment, loss, gradients and parameter updates | Cross-entropy, loss and gradients | Optimization; prediction of a small update |
| 8. Build and validate | Implement, test and eventually train a small model within declared scope | Guided build plus G1–G9 milestones | G2 data branch; independent reconstruction and reproducible training |
| 9. Adapt and evaluate | Distinguish prompting, in-context learning, fine-tuning and retrieval; evaluate claims appropriately | Existing adaptation/evaluation pages | LoRA/QLoRA and advanced evaluation when covered |

Stages 2 and 6 intentionally revisit generation at different depths: stage 2 is an orientation preview; stage 6 explains the full mechanism after the reader knows the components. Avoid repeating the same full explanation in the panorama, Transformer overview and generation lesson.

## 6. Work register and ownership

The GitHub issues remain authoritative. This table maps audit findings to existing work to avoid duplicate issues.

| Priority | Work package | Existing owner | Required output / exit evidence | Dependency / constraint |
|---|---|---|---|---|
| P0 | Reconcile route, curriculum, page graph and bilingual links | #130, #225, #337, #415 | Explicit view semantics; route-to-page crosswalk; no broken or misleading transitions | Reuse current curriculum and metadata; no competing route schema |
| P0 | Clarify Build outcome and G0–G9 implementation status | #78, #58 | Honest distinction between inspect, reproduce, independently build and train; status agrees with code/tests | Respect private prerequisite gate before implementation |
| P0 | Resolve duplicate/overlapping explanations along overview → Transformer → generation | #355 | Canonical ownership retained; unique caveats preserved; FR/EN parity | No bulk rewrite; coordinate with #225 and #130 |
| P1 | Improve formative exercises and transfer tasks | #220 | Small bilingual sequence with stable IDs, hints, worked solutions, misconception feedback and scoring criteria | Do not treat answer recall as mastery |
| P1 | Execute learner-validation pilot | #447 | Anonymized observation log, task responses, confidence and rubric-based analysis; limitations stated | Use `docs/learner-validation-pilot.md`; consent and privacy |
| P1/P2 | Inspect rendered navigation, map, homepage and lesson experiences | #337, #341, #320, #329, #191 | Reproducible FR/EN browser log by viewport/input mode; defects linked to owners | Browser evidence is separate from CI |
| P1 | Add prediction/experiment/interpretation loop to selected activities | #220 and concept-specific owners | At least one controlled, bounded activity per suitable core concept | No generic widgets; no unsupported generalization |
| P2 | Reassess route with multiple learner profiles | New follow-up only if pilot reveals a distinct gap | Comparative friction and transfer observations across profiles | Do not infer general effectiveness from a single participant |

### Existing issue ownership (do not duplicate)

- #130 is the high-level coordination epic.
- #225 owns conceptual curriculum order.
- #78 owns concept-to-code sequencing and implementation status.
- #355 owns residual duplication/content ownership.
- #415 owns the distinction between guided route and exploratory resource graph.
- #220 owns formative exercise design.
- #447 owns execution of the learner-validation pilot.
- #337, #341, #320 and #329 own their bounded rendered/browser reviews.
- #191 owns design-system validation.

If an owner issue has changed state, update this mapping during execution rather than creating a duplicate issue.

## 7. Execution sequence

1. **Documentation baseline (this change):** record the audit, decisions, evidence boundaries and owner crosswalk.
2. **P0 reconciliation:** inspect the latest state of #225/#355/#415 and close only the concrete route/content discrepancies they own. Update the canonical curriculum and route only when a verified mismatch exists.
3. **Build honesty and reconstruction:** align the Build landing page, learning-path milestones and project status. Keep implementation blocked until the prerequisite gate is cleared.
4. **Exercise and transfer design:** complete the bounded bilingual activities under #220, with tasks tied to stages 3–7.
5. **Pilot:** execute #447 using the existing protocol; report observations, not broad efficacy claims.
6. **Rendered review:** complete the relevant browser issues and connect confirmed defects to their owners.
7. **Reassessment:** revise the route only if the pilot/browser evidence identifies a concrete issue.

Do not perform all seven steps in one large PR. Keep documentation, curriculum corrections, exercise content, implementation and browser evidence in separate reviewable increments.

## 8. Acceptance criteria for the overall journey

The journey is considered **design-coherent** when:
- the entry page clearly distinguishes Understand, Build, Deepen and transversal Practice & experiment;
- the recommended route is visibly distinct from the resource/concept graph;
- each core stage has a learner outcome, entry page and sensible next step;
- optional detours are visibly optional and are linked at the point of need;
- the conceptual order is not confused with G0–G9 implementation dependencies;
- FR/EN route labels and destinations are semantically equivalent;
- the Build status distinguishes inference mechanics from a trained model.

The journey is considered **operationally validated** only when, in addition:
- the relevant pages render and work across the recorded desktop/mobile and keyboard/touch checks;
- local links and page references are valid;
- the exercise sequence has worked solutions and explicit assessment criteria;
- a learner pilot has been run and its limitations documented;
- the evidence shows what learners could explain, predict, implement and transfer, without equating task completion with mastery.

The journey is **not** considered fully validated merely because the source files are internally consistent, CI passes, or one participant completes the route.

## 9. Non-goals and guardrails

- No wholesale curriculum redesign or new navigation framework.
- No new page solely to mirror a stage in this table.
- No duplicate route registry or graph ontology.
- No new GPT training implementation before the existing prerequisite gate is explicitly cleared.
- No claim of a complete from-scratch training course until the data pipeline, training, validation and checkpoint generation exist and are tested.
- No public learner records or personal data.
- No use of a numeric pedagogical score as if it were empirical evidence.
- No deletion of useful derivations, counterexamples, figures or source context merely to shorten the route.

## 10. Handoff checklist for the next session

- [ ] Read this audit and the current state of #130, #225, #355, #415, #220 and #447.
- [ ] Check whether the mapped owner issues are still open and whether their scope has changed.
- [ ] Start with the smallest verified P0 discrepancy; do not reopen completed source audits.
- [ ] Preserve canonical ownership in `docs/information-architecture.md`, `docs/learning-path.md` and `docs/content-section-mapping.md`.
- [ ] Update `docs/project-status.md` only when implementation or learner evidence actually changes.
- [ ] Record browser evidence separately from source/CI evidence.
- [ ] Record pilot observations and limitations; keep individual learner data private.
- [ ] Do not merge a pull request without explicit user approval.
