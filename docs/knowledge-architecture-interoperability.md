# Knowledge architecture interoperability

**Status:** proposal / local design note — 2026-11-05  
**Cross-repository reference:** [Wiki Knowledge architecture contract](https://github.com/JM-Brun/wiki-knowledge/blob/main/docs/architecture/cross-repository-knowledge-architecture.md)

## Purpose and boundary

LLM Lab remains public, self-contained, and independently buildable. This note maps its existing knowledge structures to a technology-neutral contract; it does not introduce a dependency on the private Wiki Knowledge repository or copy its ingestion engine.

Keep three concerns distinct:

1. **Semantic model:** domains, canonical concepts, claims and typed relations.
2. **Holonic/operational model:** bounded responsibilities and artifact handoffs (intake, extraction, resolution, review, compilation, QA).
3. **Pedagogical projections:** guided learning route, implementation path, optional deep dives, source comparisons and exploratory concept/resource graph.

A concept graph is not the curriculum. A source graph is not the canonical concept registry. A source's teaching order is not automatically a prerequisite relation.

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

- **P0:** #416 relation semantics; #130/#415/#225 separation and correspondence of curriculum, navigation, graph and implementation path.
- **P1:** #458 and source-catalogue work — verify claim-level provenance through extraction → concept/page → synthesis; add a compact mapping/validation checklist if a concrete gap remains.
- **P2:** join the two-way transfer pilots defined in the cross-repository contract; record failures and maintenance cost before considering shared code.
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

Inspected `data/concepts.yml` on the default branch. The registry currently declares ten relation types: `represented-by`, `prerequisite`, `part-of`, `constrains`, `contributes-to`, `applies-to`, `mapped-by`, `produces`, `normalized-by`, and `evaluated-by` (all currently declare `direction: directed`). The records provide bilingual labels and descriptions, which is a useful base.

The current contract does **not** yet encode:
- permitted source/target object kinds or concept/domain constraints;
- inverse relation or symmetry policy;
- transitivity policy (including an explicit default of non-transitive);
- cardinality or cycle constraints where applicable;
- evidence/provenance expectations for asserting a relation;
- whether a relation is semantic, structural, functional, evidential, or pedagogical;
- whether it may be used to infer a learning dependency or only to explain a mechanism.

This is a schema/documentation gap, not proof that current edges are factually wrong. It must be resolved by reviewing actual edges and intended usage, not by adding theoretical metadata mechanically.

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

The initial audit is deliberately bounded to the registry. It does not claim the renderer, all relation consumers, or the complete pedagogical effect have been tested.


## Relation contract implemented on the interoperability branch (2026-11-05)

The first implementation increment extends the existing generic `site/tools/check_concept_registry.py` validator and its shared test module. It does not add a second workflow or per-concept CI.

Each relation type now declares:

- `family`: one of structural, pedagogical, representational, constraint, functional, evaluative, or associative;
- `direction`: directed or symmetric (existing field);
- `transitive`: explicit boolean semantic declaration; this does not automatically materialize transitive edges;
- `acyclic`: explicit boolean; cycle validation applies only to relation types that declare it;
- `learning_dependency`: explicit boolean; when true, the relation must be directed, pedagogical and acyclic;
- `inverse`: null or another relation type whose inverse declaration must point back.

Every edge of a relation type marked `learning_dependency: true` must include a bilingual `rationale` mapping with non-empty `fr` and `en` values. This prevents a graph edge from silently becoming a curriculum dependency without an explicit pedagogical justification and keeps the public data contract bilingual.

The current registry's ten relation types have been annotated. `part-of` is declared transitive and acyclic; `prerequisite` is pedagogical, acyclic and learning-relevant but not automatically transitively expanded. All other current relation types are non-transitive and do not drive learning order. No inverse relation is currently declared.

### Domain/range boundary

At present, every edge has canonical concepts as both endpoints. The validator checks that both endpoints resolve to concept IDs. It does not yet constrain endpoints to particular concept domains: domain membership is multi-valued and current relations legitimately cross domains. More granular source/target kinds should be introduced only when the graph includes non-concept entities or a demonstrated invalid edge class; do not invent restrictive domain rules that reject valid cross-domain relations.

### Validation coverage

The existing CI entry point remains `uv run python site/tools/check_concept_registry.py`; the existing `tests/site/test_concept_registry.py` now covers required relation metadata, learning-dependency invariants, relation-specific cycle policy, reciprocal inverse declarations, and mandatory rationale. The PR must pass the existing generic CI and Quarto render workflows before merge.

This is a first contract increment, not proof that every current relation edge is semantically correct or that the rendered graph is pedagogically effective. The remaining manual review of the current edge inventory stays in #416.


## Edge-level review

The initial manual review of all 26 edges is documented separately in [`docs/audits/concept-relation-edge-review.md`](audits/concept-relation-edge-review.md). It records the intended reading and scope limitations for every edge. The review found no immediate direction reversal, but several high-level relations are explicitly not exhaustive computational data-flow claims. Rendered FR/EN graph UX and learner comprehension remain unverified.
