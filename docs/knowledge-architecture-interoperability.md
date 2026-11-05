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
