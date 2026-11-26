# Knowledge architecture interoperability

**Status:** implemented concept-relation contract; broader cross-graph bridge model remains in progress — reconciled 2026-11-23  
**Cross-repository reference:** [Wiki Knowledge architecture contract](https://github.com/JM-Brun/wiki-knowledge/blob/main/docs/architecture/cross-repository-knowledge-architecture.md)

## Purpose and boundary

LLM Lab remains public, self-contained, and independently buildable. This note maps its existing knowledge structures to a technology-neutral contract; it does not introduce a dependency on the private Wiki Knowledge repository or copy its ingestion engine.

Keep three concerns distinct:

1. **Semantic model:** domains, canonical concepts, claims and typed relations.
2. **Holonic/operational model:** bounded responsibilities and artifact handoffs (intake, extraction, resolution, review, compilation, QA).
3. **Pedagogical projections:** guided learning route, implementation path, optional deep dives, source comparisons and exploratory concept/resource graph.

A concept graph is not the curriculum. A source graph is not the canonical concept registry. A source's teaching order is not automatically a prerequisite relation.

## Entity, epistemic and pedagogical boundaries

The project uses several related vocabularies, but they do not all denote canonical entities. Classify a record by the role it plays, not by the informal word used in an editorial discussion.

| Term | Meaning in LLM Lab | Current owner / representation | Boundary |
|---|---|---|---|
| **Concept / notion** | A durable, reusable referent with a language-independent identity and a bilingual definition. “Notion” is a prose synonym, not a second entity kind. | `data/concepts.yml`: stable `id`, bilingual `labels`/`definitions`, `importance`, domain memberships and published page references; concept-to-concept semantic edges are declared separately in the same registry. | A concept is not a page, source, extracted statement, activity, learning objective or arbitrary named phrase. `importance` (`core`, `supporting`, `specialized`) is a project importance annotation, not evidence confidence or learner mastery. |
| **Idea** | An informal umbrella word, not a sufficiently precise entity type. | Resolve each occurrence into its actual role: concept, proposition/claim, mechanism, method, derivation, assumption, result, limitation, pedagogical contribution, open question, etc. Existing extraction `kind` values provide this finer vocabulary. | Do not create an `ideas` registry or promote every interesting source phrase into a concept. |
| **Intuition / mental model / analogy** | An explanatory or pedagogical contribution that helps a learner interpret a mechanism or relationship. | Source-local extraction items (`mental-model`, `analogy`, and related kinds), optional `pedagogical_profile`/`pedagogical_assessment`, source-local pedagogical graph nodes, and ultimately authored page prose when selected for synthesis. | It is not automatically a scientific claim, a canonical concept, evidence for the mechanism, or a formal relation. Preserve its source, scope and limitations; distinguish analogy from literal mechanism. |
| **Claim / assertion** | A proposition attributed to a source, commenter, maintainer or published synthesis, with a scope and epistemic status. | Source-scoped extraction item (`kind: claim` or a more specific kind), exact locator, optional voice provenance, evidence kind/confidence/scope/assumptions/limitations and, where applicable, separate verification metadata. | The current project has no general-purpose canonical claim registry. Do not merge the proposition into a concept definition or treat the source's statement as verified merely because it was extracted or cited. Claim-level lineage remains a distinct interoperability concern. |
| **Evidence** | Material that grounds, qualifies, challenges or records an assertion: source passages, primary papers, equations, code/tests, datasets/protocols, project artifacts or learner observations. | Source-local extraction evidence fields and locators; source inspection events; typed source-lineage evidence pointers (target architecture); project and learner evidence recorded by the relevant validation process. | Evidence is not the claim itself. Evidence kind, confidence, inspection completeness, verification status and pedagogical value are separate dimensions; none should be collapsed into one score. A citation alone is not corroboration. |
| **Relation** | A typed assertion connecting two identified entities or records, with direction and a family-specific meaning. | Each owner retains its own relation semantics: concept→concept in `data/concepts.yml`; page→page in page metadata; source-local nodes/edges inside an extraction; source→artifact lineage in the source-lineage model; stage/lesson progression in `data/guided-route.yml`; operation/state flow in `data/computational-graph.yml`; and specialized Build, revision and Practice contracts. | There is no universal edge vocabulary. Do not infer a relation from tags, co-occurrence, page order, analogy, shared citation or visual proximity. A cross-family bridge must identify endpoint kinds/IDs and its own meaning/evidence policy. |
| **Pedagogical objective / learning outcome** | An intended teaching aim or an observable learner-facing result for a defined stage/lesson; not a scientific entity. | Understand stage `objective` in `data/guided-route.yml`; lesson-level `conceptual_focus.outcome` in the route; Build outcomes/evidence in `docs/learning-path.md`; source-local `learning_outcomes` in extraction records, explicitly marked `declared` or `inferred`. | An objective is not a concept or prerequisite edge. A declared/inferred outcome is not proof that learners achieved it. Measured learner outcomes require separate learner-task evidence and review. |

### Consequences for canonical ownership

1. Keep `data/concepts.yml` deliberately limited to durable shared concepts and their semantic relations. Add a concept only when it has a stable meaning reused across pages or experiences; do not use the registry as a general notebook of ideas.
2. Keep claims, intuitions, examples, teaching moves and source-specific interpretations in their source extraction or editorial context unless a concrete cross-source claim-lifecycle use case justifies a separately identified claim model.
3. Keep evidence attached to the assertion or decision it supports, with exact provenance and scope. Do not create a detached evidence catalogue without a consumer and a clear identity model.
4. Keep pedagogical objectives and route semantics with their owning learning experience. Source-reconstructed outcomes remain source-local and must retain declared/inferred status.
5. Keep relation families separate. Cross-graph interoperability resolves stable IDs and validates explicit typed bridges; it does not unify all edges into a universal graph.

These boundaries are already reflected in the [source extraction contract](source-catalogue-schema.md), [source-lineage architecture](source-lineage-architecture.md), [source-to-knowledge validation protocol](workflows/source-to-knowledge-validation.md), and [learning path](learning-path.md). This section consolidates their ownership implications; it does not introduce a new schema or assert that the target source-lineage migration is fully implemented.

## LLM Lab structures to preserve

- `data/concepts.yml`: canonical, language-independent concept IDs with bilingual labels and definitions.
- `docs/source-catalogue-schema.md`: separate source records, source-specific extraction, source-local pedagogical models, domains, concepts and page metadata.
- Source-local pedagogical graph nodes use `src-` IDs; they must never be copied automatically into the canonical concept registry.
- Page hierarchy, suggested route, concept relations, curriculum sequence and implementation dependencies have distinct semantics.
- Guided learning path and exploratory resource graph are different projections.

## Selective transfer from Wiki Knowledge

Reuse design principles, not implementation wholesale:

- source fingerprinting and version-aware identity;
- extraction artifacts distinct from canonical integration;
- atomic claims with locators, epistemic status, evidence quality and scope;
- explicit no-op/link/update/create/merge-proposal/conflict decisions;
- inspectable change proposals and human review for ambiguous or destructive changes;
- idempotent processing and selective invalidation;
- separate structural validation, semantic review and learner/transfer evaluation.

LLM Lab should not reproduce a general-purpose ingestion engine unless a concrete local use case justifies it.

## Relation governance

Issue [#416](https://github.com/JM-Brun/llm-lab/issues/416) owns the relation-aware concept graph. It should define for every relation type: meaning, direction, domain/range, inverse, symmetry, transitivity, cardinality where relevant, evidence policy, and whether the edge can drive navigation or learning order.

Keep `prerequisite` distinct from display order, hierarchy, association and source teaching order. Graph layout must not imply an unsupported DAG or global learning sequence. FR/EN labels and descriptions should come from canonical metadata, not duplicated rendering code.

Review existing relation families before adding new ones: taxonomy (`is-a`, `part-of`), representation/implementation (`represented-by`, `implements`), computation (`uses`, `produces`), learning (`prerequisite`), evidence (`supports`, `contradicts`, `derived-from`). Add no type without a real use case and validation rule.

## Mapping boundary

| Wiki Knowledge artifact | LLM Lab counterpart | Rule |
|---|---|---|
| Source identity/fingerprint | `data/sources.yml` and scan history | Map identity/version explicitly; local IDs are not globally unique |
| ExtractionArtifact | `data/extractions/<source-id>.yml` | Preserve source-local scope, locators, limitations and pedagogy |
| ExtractedClaim | extraction item / claim provenance | Keep atomic evidence and epistemic status; do not flatten to a source-level citation |
| ConceptCandidate | canonical `data/concepts.yml` match | Resolve by meaning and aliases, never label alone |
| ChangePlan | reviewed integration proposal / PR checklist | Keep changes inspectable; human review for conflicts |
| Canonical synthesis | scoped lesson or synthesis | Retain claim-to-concept-to-page lineage |
| Holonic stage contract | local skill/workflow responsibility | Reuse boundaries and gates; no agent/action per stage |

This mapping is conceptual; it does not claim every row is implemented end-to-end.

## Existing work and priorities

Do not duplicate existing issues:

- **Concept relation contract:** #416's schema/validator work is implemented. The current main inventory contains 12 relation types and 124 typed concept edges (see the current registry and `docs/audits/concept-relation-edge-review.md`). The contract constrains learning dependencies to explicitly justified `prerequisite` edges. Remaining work is the updated edge-level scientific review as the registry evolves, plus manual rendered, touch and screen-reader validation and consumer audit; do not reopen schema design without a concrete failing case.
- **Cross-graph bridges:** #1233 owns the broader typed bridge contract and evidence/decision traversal. It must reuse canonical identities and specialized relation semantics; it is not a universal graph or a second registry. #512 owns claim provenance/interoperability, #1211 source provenance reconciliation, and #1306 explicit collection membership.
- **Curriculum/navigation separation:** #130/#415/#225 and the canonical route owner remain authoritative. Concept relations must not generate or reorder the guided route.
- **Source-to-synthesis provenance:** #458 and source-catalogue work own verification of claim-level provenance through extraction → concept/page → synthesis; add a compact mapping/validation checklist only for a demonstrated gap.
- **Cross-repository transfer:** use the two-way pilots defined in the cross-repository contract; record failures and maintenance cost before considering shared code.
- Coordinate content ownership with #355.

## Non-goals

- No Wiki Knowledge dependency at build or runtime.
- No shared Python package at this stage.
- No duplicate concept registry or parallel curriculum.
- No GitHub Action/workflow per concept.
- No automatic promotion of source-local pedagogical nodes to canonical concepts.
- No inference of prerequisites from order, proximity or visual layout.

## Session handoff

Before implementation, inspect #416, #415, #130, #225, #355, #458 and the active PR queue. Reuse current issues; create a child issue only for a demonstrated gap. Keep public LLM Lab documentation complete without relying on private implementation details.


## Initial audit of the current canonical relation registry (2026-11-05)

Historical snapshot (2026-11-05): the registry then declared ten relation types and 26 edges. This section records the original gap analysis; it is not a description of current main. The contract and validator work described below were subsequently implemented, and the current inventory is 12 relation types / 124 typed edges (2026-11-23).

The initial schema did not encode the above properties. The implemented contract now declares family, direction, transitivity, acyclicity, learning-dependency eligibility and inverse policy, with bilingual rationale required for learning-dependency edges. Concept endpoints remain the only supported endpoint kind; fine-grained domain/range restrictions are intentionally deferred because concepts are multi-domain. The remaining gap is not the absence of a relation schema: it is keeping the 124-edge scientific review current and validating the semantics of bridges between distinct graph families.

### Concrete review cases

- `token --represented-by--> token-embedding`: verify the intended reading (a token is represented by its embedding) and whether the edge's source/target wording is consistent in both locales.
- `query/key/value --part-of--> self-attention`: verify whether these are parts of the mechanism, projections used by it, or outputs/representations; choose the relation semantics that best matches the mathematical description.
- `attention-score --normalized-by--> softmax` and `logits --normalized-by--> softmax`: distinguish a transformation applied to a score vector from a generic “normalizes” relation; consider a relation name whose direction is unambiguous.
- `softmax --evaluated-by--> cross-entropy`: verify the edge's intended direction and object roles (predicted distribution vs loss function).
- `training-objective --evaluated-by--> cross-entropy`: verify whether this means “objective is measured using the loss” or “objective is the loss”; avoid conflating an optimization objective with an evaluation relation.
- `prerequisite`: require an explicit pedagogical justification and do not infer it from curriculum order, page hierarchy, source order, or graph layout.

### Proposed acceptance criteria for #416

- [ ] Inventory every declared relation type and every current edge; identify unused types and undefined semantics.
- [ ] For each type, document a precise verbal reading, source/target direction, relation family, domain/range, inverse/symmetry, transitivity (default false unless justified), and evidence requirements.
- [ ] Decide which relation types may support learning prerequisites; only those edges may influence a guided route.
- [ ] Review all current edges for direction and semantic fit; record rejected/ambiguous edges rather than silently coercing them.
- [ ] Add validation for unknown concept IDs and unknown relation types; validate bilingual metadata and required semantic fields.
- [ ] Add checks for impossible self-edges and only those cycles prohibited by the relation's declared semantics. Do not impose a global DAG on all relations.
- [ ] Keep the registry as the single source of truth; render labels/legend from metadata, not duplicated code.
- [ ] Confirm that the learner-facing graph, guided route, and curriculum sequence remain distinct projections.

The initial audit was deliberately bounded to the registry. Later browser reviews cover rendered FR/EN graph behavior, but touch/screen-reader validation, all consumer paths and learner comprehension remain separate acceptance items.


## Relation contract implemented in main (initial implementation 2026-11-05; reconciled 2026-11-23)

The implementation extends the existing generic `site/tools/check_concept_registry.py` validator and its shared test module. It does not add a second workflow or per-concept CI. The contract is now part of the canonical registry; this is no longer merely an interoperability-branch proposal.

Each relation type now declares:

- `family`: one of structural, pedagogical, representational, constraint, functional, evaluative, or associative;
- `direction`: directed or symmetric (existing field);
- `transitive`: explicit boolean semantic declaration; this does not automatically materialize transitive edges;
- `acyclic`: explicit boolean; cycle validation applies only to relation types that declare it;
- `learning_dependency`: explicit boolean; when true, the relation must be directed, pedagogical and acyclic;
- `inverse`: null or another relation type whose inverse declaration must point back.

Every edge of a relation type marked `learning_dependency: true` must include a bilingual `rationale` mapping with non-empty `fr` and `en` values. This prevents a graph edge from silently becoming a curriculum dependency without an explicit pedagogical justification and keeps the public data contract bilingual.

The initial ten relation types were annotated. The current main registry has since grown to 12 controlled relation types and 124 typed concept edges; re-run the edge inventory and review whenever the registry changes. `part-of` is declared transitive and acyclic; `prerequisite` is pedagogical, acyclic and learning-relevant but not automatically transitively expanded. All other current relation types are non-transitive and do not drive learning order. No inverse relation is currently declared.

### Domain/range boundary

At present, every edge has canonical concepts as both endpoints. The validator checks that both endpoints resolve to concept IDs. It does not yet constrain endpoints to particular concept domains: domain membership is multi-valued and current relations legitimately cross domains. More granular source/target kinds should be introduced only when the graph includes non-concept entities or a demonstrated invalid edge class; do not invent restrictive domain rules that reject valid cross-domain relations.

### Validation coverage

The existing CI entry point remains `uv run python site/tools/check_concept_registry.py`; `tests/knowledge/test_concept_registry.py` covers required relation metadata, learning-dependency invariants, relation-specific cycle policy, reciprocal inverse declarations and mandatory rationale. This validator remains the single semantic schema boundary; it is not a replacement for edge-level scientific review or rendered learner validation.

This is a first contract increment, not proof that every current relation edge is semantically correct or that the rendered graph is pedagogically effective. The remaining manual review of the current edge inventory stays in #416.


## Edge-level review

The edge-level review is documented in [`docs/audits/concept-relation-edge-review.md`](audits/concept-relation-edge-review.md). It covers 66 retained assertions, while the current registry has 124; 58 current assertions remain outside that historical review. Refresh the review against current main, explicitly classify new/changed edges, and retain the non-exhaustive nature of conceptual relations. Rendered FR/EN graph UX, touch/screen-reader behavior and learner comprehension remain distinct validation tasks.


## Cross-graph interoperability: remaining contract

The concept graph's relation schema is not a substitute for cross-graph bridges. Keep the following relation families distinct:

| Bridge family | Canonical owners | Required interpretation |
|---|---|---|
| Concept ↔ page | `data/concepts.yml` and page-map metadata | A page explains or applies a concept; not proof that every page claim is supported. |
| Concept ↔ computation | `data/concepts.yml` and `data/computational-graph.yml` | Explicit explanatory/implementation bridge; never merge concept and operation IDs. |
| Source/extraction ↔ concept/page | `data/sources.yml`, `data/extractions/` and canonical page/concept registries | Preserve source version, extraction item and locator where available; distinguish evidence, interpretation and editorial integration. |
| Build ↔ computation/resource/page | Build path, computational graph and `data/resources.yml` | Implementation evidence, not an Understand prerequisite. |
| Historical event ↔ source/concept | `data/history-pilot.yml` and source/concept registries | Chronological association is not causal influence. |
| Practice activity ↔ lesson/concept | Dedicated Practice pages and explicit page/anchor identities | Page-level links do not imply every activity covers every lesson or concept. |
| Editorial story ↔ concept/source/page | Story source and dossier | Editorial order is not a learning dependency; a story remains independently readable. |

#1233 owns the integrated cross-graph contract, exact endpoint identity, evidence expectations and bounded traversal tests. The current `ProjectIndex` and `cross_graph_query.py` provide a partial, read-only concept-centred query projection; they do not yet validate every bridge family, traverse historical/decision records, or provide complete Build/Practice/source coverage. Do not introduce a generic edge dispatcher or a new graph store merely to make the families look uniform.

**Remaining acceptance criteria:**
- [ ] Define source/target identity, relation direction, semantic family and evidence requirements for each bridge that has a real use case.
- [ ] Reuse existing validators and add only cross-family checks that no owning validator currently performs.
- [ ] Test at least five traversals from #1233 with explicit expected paths and explicit gaps.
- [ ] Verify that no route/prerequisite is inferred from generic semantic, computational, source or editorial edges.
- [ ] Include negative tests for tag overlap, shared citations, filename similarity, page order and source-local node names.
- [ ] Keep output read-only and evidence-bearing; no automatic canonical mutation.

### Projection preservation

The bilingual learning-map data builder now carries the relation contract into its generated projection: family, direction, transitivity, acyclicity, learning-dependency eligibility, inverse declaration, localized label/description, and any localized edge rationale. The interactive renderer currently uses direction, label and description; retaining the additional metadata prevents the projection boundary from silently discarding semantics and leaves future presentation/consumer choices explicit. Tests cover both metadata and localized rationale preservation.

The guided curriculum generator remains independent of concept relations. In particular, `learning_dependency` is descriptive metadata for concept edges; it is not currently consumed to generate or reorder the guided route.
