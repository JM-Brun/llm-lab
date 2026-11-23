# Architecture audit #1554 — session handoff

**Last reviewed:** 2026-11-23  
**Main snapshot:** `f820869882b8a745771f11ec07ac3272e9a66738`  
**Scope:** general architecture inventory (#130 / #1554), as preparation for the focused computational architecture work (#575).  
**Purpose:** record the work still required after the bounded audit; this is an operational handoff, not a new architecture specification.

## 1. Decision and boundaries

The general architecture audit must precede consolidation of the computational model. It inventories what is actually implemented in `main`: canonical owners, contracts, validators, responsibilities, adapters and projections.

Keep three representations distinct:

1. **Knowledge graph:** which concepts and semantic entities are related?
2. **Computational graph:** which operations, tensors and data dependencies define the computation?
3. **Pedagogical route:** in which order should a learner encounter and practise concepts?

They may share stable identifiers and explicit typed links. They must not share interchangeable edge semantics. Do not infer computational dependencies or learning prerequisites from tags, route order, filenames, page proximity or generic semantic relations.

Do not introduce a universal registry, universal graph, generic edge schema, duplicate validator, new activity registry or per-concept CI workflow merely for architectural symmetry.

## 2. Verified baseline and evidence

The audit inspected the recursive `main` tree and representative canonical files, contracts, validators, ProjectIndex code and CI workflow. It did **not** execute the complete test suite, render the full site, review every record or conduct a full learner study.

The baseline below is therefore an implementation inventory, not a certification of scientific or pedagogical quality.

| Area | Existing owner / implementation | Remaining boundary |
|---|---|---|
| Concepts and domains | `data/concepts.yml`, `data/domains.yml`; `check_concept_registry.py` | Scientific review of all current typed relations; avoid a second concept registry |
| Page metadata | `LLM-LAB-PAGE-MAP` metadata; `check_page_metadata.py` | Reconcile documentation and consumers; audit reader-facing metadata leakage separately |
| Resources | `data/resources.yml`; `check_resource_registry.py` | Add kinds only for real artifacts with consumers |
| Computation | `data/computational-graph.yml`; `check_computational_graph.py` | Preserve its operation/dependency semantics; validate consistency with #575 |
| Sources and extractions | `data/sources.yml`, `data/extractions/`, `check_source_catalogue.py` | Locator quality, extraction coverage decisions and provenance completeness |
| Understand route | `data/guided-route.yml`; route tooling | Keep route order pedagogical, not a substitute for computation edges |
| Build | Existing learning-path documentation and implementation resources | Determine whether a concrete structured crosswalk is needed; do not assume a new registry |
| Review / revision | ProjectIndex revision relation loader and coverage audit | Reconcile contract documentation and actual enforcement; non-page aids remain a separate decision |
| Practice | Dedicated exercise pages and activity pilot | Complete learner-facing and bilingual audit before deciding whether a registry is justified |
| History | `data/history-pilot.yml`; `check_history_pilot.py` | Confirm scope and evidence; keep chronology separate from prerequisite relations |
| Cross-graph queries | ProjectIndex, opt-in evidence loading, `cross_graph_evidence.py`, `cross_graph_query.py` | Bounded adapters, not a universal graph or complete claim-level provenance system |
| Project Intelligence | Coverage matrix, metrics and reporting tools | Explain unknown states and add evidence-backed coverage only where supported |

The earlier audit counted 102 concepts, 6 domains, 114 concept relations, 57 computational nodes, 75 computational edges, 7 branches, 8 views, 142 source records, 100 extraction files and 17 history events. Treat these as a dated snapshot, not hard-coded invariants: recompute counts from the current canonical files before publishing a new inventory. The source-collection snapshot previously reported 44 explicit decisions and 98 undecided records; confirm whether newer main commits changed it.

### Key architectural interpretation

- `ProjectIndex` is an existing deterministic read/index layer. Its optional evidence mode is intentionally heavier than the lightweight index.
- Cross-graph paths preserve explicit association and provenance metadata. A path from concept to extraction to source is not, by itself, proof that the source supports a scientific claim.
- A page-mediated concept-to-computation path is not necessarily a direct concept-to-operation relation.
- A successful structural validator does not establish conceptual correctness, scientific evidence, pedagogical effectiveness, accessibility or bilingual parity.
- Existing revision checks in ProjectIndex must be reused and reconciled, not duplicated in a second validator.

## 3. Corrections and checks still required

### P0 — Close the #1554 documentation reconciliation

- [ ] Inspect PR [#1561](https://github.com/JM-Brun/llm-lab/pull/1561) against the **current** `main`, not its recorded base snapshot. Its previously inspected base was `534ce3d`; `main` has since advanced to `f820869`.
- [ ] Recompute all inventory counts from canonical files and CI artifacts. In particular, do not reuse the superseded 489-item extraction count; the later source-coverage report recorded 520 items across 100 extraction files, but must be checked against the current tree.
- [ ] Reconcile `docs/llm-lab-knowledge-learning-architecture.md`, `docs/llm-lab-architecture-implementation-backlog.md`, `docs/project-intelligence-layer.md`, metric definitions and the validator/interoperability matrix. Avoid copying the same inventory into several independently maintained documents.
- [ ] Ensure each capability has an honest status: **implemented**, **partially implemented**, **proposed**, **deferred**, **superseded** or **not assessed**.
- [ ] Correct stale explanations about source adapters: the opt-in source/extraction adapter exists; complete concept-to-source/item coverage and claim-level scientific support are separate unfinished capabilities.
- [ ] Confirm whether the source collection counts and revision-coverage counts still match current main and latest CI artifacts.
- [ ] Update this handoff and the backlog with exact evidence links, dates and remaining limitations.

**Acceptance:** one coherent, current inventory with explicit owners, contracts, validators, consumers and evidence; no stale capability claims or duplicate source-of-truth tables.

### P1 — Normalize strict YAML loading

The audit found that `site/tools/strict_yaml.py` is used by several registry validators, while the inspected implementations of `check_computational_graph.py` and `check_history_pilot.py` used `yaml.safe_load`.

- [ ] Recheck those exact call sites on current main before editing.
- [ ] If still true, use the shared strict loader consistently, including metadata extraction where applicable.
- [ ] Add focused negative tests proving duplicate YAML keys are rejected with file/context information.
- [ ] Run the focused validator tests and relevant CI workflow.
- [ ] Do not create a second YAML utility or broaden this into an unrelated parser rewrite.

**Acceptance:** duplicate keys cannot be silently overwritten in canonical computation/history data; errors remain actionable.

### P1 — Reconcile specialist contracts with implementation

- [ ] **Revision:** compare `docs/revision-resource-contract.md`, page metadata guidance, ProjectIndex validation and `audit_revision_coverage.py`. Record exactly which fields are enforced where. Keep page aids and non-page resources distinct.
- [ ] **Practice:** update `docs/practice-activity-model-pilot.md` from merged PR #1558 evidence, but do not mark learner acceptance or unrun checks complete. Preserve the lesson-to-dedicated-exercises-page rule.
- [ ] **Sources/provenance:** run a current locator-quality audit across all extraction files; distinguish absent extraction, not applicable, undecided and invalid. Do not infer collection membership from tags or filenames.
- [ ] **Concept relations:** continue the scientific review owned by #416; structural validation is not a substitute for reviewing edge meaning, direction and rationale.
- [ ] **History and editorial collections:** retain their specialized contracts and projections; do not fold them into the learning route or computational graph.

**Acceptance:** each specialist model has a clear owner and enforced contract; remaining gaps are explicit and routed to existing issues.

### P1 — Complete the graph-family inventory for interoperability

- [ ] List each graph/model family with its canonical owner, node kinds, edge kinds, schema/version, validator, projection and consumers.
- [ ] For each cross-family relation, record source/target kinds, direction, purpose, inverse/symmetry, transitivity, cycle policy, evidence requirements and whether it is eligible to define learning order.
- [ ] Reuse existing ProjectIndex adapters and typed query paths. Extend only for a demonstrated missing use case.
- [ ] Keep unresolved and unassessed references explicit; never synthesize links from lexical similarity, tags or proximity.
- [ ] Add referential-integrity tests for the relations actually declared, not a generic universal graph validator.

**Acceptance:** a readable graph-family inventory and focused tests showing that shared identifiers do not collapse semantic, computational and pedagogical edge meanings.

## 4. Handoff to #575 — computational architecture

Only after the P0 inventory is reconciled should #575 be resumed. The next session should:

1. Read the current `data/computational-graph.yml` and its schema/validator before changing the canonical spine.
2. Compare every proposed #575 node and edge with existing computation nodes/relations. Reuse or refine existing identifiers where semantics match; document justified additions and deprecations.
3. Validate the conceptual placement of Q/K/V: they are projections of each Transformer block's input hidden states, not a stage after the final contextualized representation.
4. Model the shared predictive computation separately from its operational projections:
   - inference/generation: select or sample a token and feed it back into the context;
   - scoring: evaluate an observed target token without updating parameters;
   - training: compute loss and gradients, then update parameters.
5. Represent teacher forcing, prefill, decode and KV cache only where they correspond to real operations, states or execution policies; do not confuse an execution mode with a mathematical dependency.
6. Keep the pedagogical route as a projection chosen for learning, not as the canonical order of every computation.
7. Add schema validation and tests before regenerating diagrams or changing many lesson pages.

The conceptual target remains:

\[
p_\theta(x_t\mid x_{<t}) =
\operatorname{softmax}\!\left(f_\theta(x_{<t})\right)
\]

This equation is a useful shared interface for generation, scoring and learning; it does not mean that those three procedures execute the same control flow.

## 5. Session-start procedure

At the beginning of the next session:

1. Fetch the latest `main` SHA and inspect all commits since the recorded snapshot.
2. Inspect PR #1561 state, base/head divergence, changed files and checks. Do not assume it is mergeable because it was previously reported as such.
3. Read this handoff, the architecture implementation backlog, the canonical registry files and the relevant validator source.
4. Check whether another PR or issue has already addressed each item. Update existing work rather than opening duplicates.
5. Run the smallest relevant tests before editing; record what was and was not run.
6. Make one bounded change set, update its owning documentation and tests, and report exact evidence.
7. Refresh this handoff when a task is completed, superseded or found not applicable.

## 6. Explicit non-goals

- No universal graph, registry, ontology or edge schema.
- No replacement of `ProjectIndex`.
- No automatic conversion of knowledge edges into computation dependencies or learning prerequisites.
- No new activity registry before the Practice pilot demonstrates a real need.
- No bulk YAML/metadata migration as part of the audit.
- No per-concept GitHub Actions.
- No claims of scientific support or learner effectiveness based only on structural links or CI success.

## 7. Completion criteria for #1554

#1554 can be considered documented and closed when:

- [ ] Current main inventory is reproducible from canonical files and recent CI evidence.
- [ ] Every major register/model has a named canonical owner, contract, validator, consumers and maturity state.
- [ ] Projections are distinguished from canonical data and their semantics are explicit.
- [ ] Known gaps have been routed to existing specialist issues without duplication.
- [ ] The backlog and architecture overview agree with the implementation.
- [ ] The handoff to #575 identifies what may be reused, what must be validated and what remains genuinely new.

**Audit limitation:** this document records a source-level review. It does not claim that the complete test suite, complete Quarto render, browser/accessibility audit or learner validation was executed in this session.
