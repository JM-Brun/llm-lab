# Knowledge graph implementation audit

**Snapshot date:** 2026-11-04  
**Scope:** repository source and relevant merged/open pull requests inspected for the information-architecture audit.  
**Purpose:** record implementation ownership and gaps without proposing a replacement graph.

## Executive finding

The repository now has the beginnings of a three-dimensional knowledge model, but its implementation is split across two layers:

- The **page graph** is implemented and rendered by the existing bilingual learning map.
- A **typed concept registry** is proposed in PR [#399](https://github.com/JM-Brun/llm-lab/pull/399). It is a reviewed seed, not yet the full knowledge graph.
- The six **Deepen domains** are currently page-classification metadata, introduced by merged PR [#391](https://github.com/JM-Brun/llm-lab/pull/391).
- The resource dimension is currently represented by concept-to-page references. Independent resource entities for demonstrations, experiments, implementations, and external references have not yet been found in the inspected implementation.

The pedagogical path and the knowledge map must remain distinct projections. The former encodes learner progression; the latter supports non-linear discovery and cross-domain navigation.

## Source-of-truth and implementation matrix

| Dimension / projection | Current source | Implemented semantics | Status and boundary |
|---|---|---|---|
| Domains | docs/page-metadata-schema.md; page-map metadata in site/**/*.qmd; scripts/check_page_metadata.py | Six controlled domain IDs classify Deepen content pages; FR/EN counterparts share the ID; page-map generator exports the field | **Implemented at page level.** No canonical concept-to-domain membership is present in the inspected concept seed. Do not equate a page's primary domain with the complete domain membership of every concept it explains. |
| Concepts | data/concepts.yml in PR #399 | Language-independent kebab-case IDs, FR/EN labels and definitions, typed concept-to-concept relations | **Partial / proposed seed.** 13 concepts and 12 relations at the inspected PR head. Coverage is intentionally incomplete. |
| Concept relations | data/concepts.yml; scripts/check_concept_registry.py in PR #399 | Directed relation vocabulary including prerequisite, generalizes, applies-to, contrasts-with, and more specific types | **Partial / proposed.** Endpoints and relation types are validated. Prerequisite and generalization acyclicity and duplicate relations are now covered by the validator work in PR #399. Inverse/symmetry rules need explicit decisions per relation type. |
| Resources | resources arrays on concept records in PR #399 | References to published FR/EN page IDs; the validator checks page-ID syntax and published-page resolution | **Partial.** A page is currently the resource record. No first-class resource entity with its own stable ID, kind, language, status, provenance, and path/URL was found for demonstrations, experiments, implementations, and external references. |
| Pedagogical path | docs/learning-path.md, docs/full-curriculum-plan.md, docs/roadmap.md | Ordered learning stages, prerequisites, progression and deliverables | **Documented curriculum projection.** Do not derive it from sidebar order or the page-map graph. |
| Knowledge map | Domain metadata, concept registry seed, page metadata and their relations | Non-linear discovery, concept relations and cross-cutting associations | **Partially implemented across layers.** The current interactive map renders page nodes and page-level route/hierarchy/related edges. It does not yet render concept nodes or concept relations. |
| Page-navigation graph | docs/page-metadata-schema.md; scripts/check_page_metadata.py; scripts/build_learning_map.py | Page IDs, suggested route, reciprocal page hierarchy, related links, bilingual page parity | **Implemented.** These are page-level relations, not concept-level semantic relations. |
| Section labels | Extracted headings in scripts/build_learning_map.py | Display/search hints for sections within a page | **Implemented as presentation metadata.** They are not concept entities or stable concept IDs. |

## Relation vocabulary alignment

The four broad semantic families have direct counterparts in the current registry vocabulary:

| Broad knowledge-graph relation | Registry type | Interpretation |
|---|---|---|
| Prerequisite | prerequisite | Source concept is needed to understand the target |
| Generalization | generalizes | Source is more general and subsumes the target |
| Application | applies-to | Source method/mechanism is applied to the target |
| Opposition / contrast | contrasts-with | Source is meaningfully distinguished from the target |

The registry also contains more specific relations such as part-of, contributes-to, constrains, produces, and represented-by. These are useful if their direction and semantics are documented. Do not collapse them into one generic relation, and do not assume that every relation should be reciprocal or acyclic.

## Tests and CI

### Existing controls

- scripts/check_page_metadata.py validates page metadata, page-level relation integrity, route and hierarchy cycles, and bilingual structural parity.
- scripts/build_learning_map.py generates the page-map JSON projection; tests/unit/test_learning_map.py covers extraction, URL generation, and route ranking.
- .github/workflows/ci.yml runs the metadata validators, Ruff, mypy, and pytest.
- .github/workflows/quarto.yml validates page metadata before rendering the bilingual site.

### Concept-registry controls proposed in PR #399

- scripts/check_concept_registry.py validates concept IDs, bilingual labels/definitions, page-resource references, relation vocabulary/endpoints, self-relations, duplicate relations, and cycle constraints for prerequisite/generalization edges.
- tests/unit/test_concept_registry.py covers the checked-in registry, duplicate IDs, unknown endpoints, missing translation, self-relations, malformed relation values, duplicate/unpublished resources, and cycle constraints.
- The validator is integrated into the existing Python CI workflow; no additional workflow is needed.

### Validation evidence

On PR #399 head 7bea7ec (2026-11-04), both workflows completed successfully. Python CI passed page-metadata validation, concept-registry validation, history validation, embedding trace, Ruff format, Ruff lint, mypy, and all 127 pytest tests. The Quarto workflow passed bilingual rendering, history timeline parity, and rendered local-link checks.

## Remaining gaps, ordered by dependency

1. **Stabilize the concept seed.** Confirm PR #399 passes formatting, lint, typing, tests, and Quarto rendering. Review relation direction definitions against actual concept examples.
2. **Make domain membership explicit at the concept layer.** Decide whether concepts may belong to multiple domains. Prefer an explicit concept-to-domain association if cross-domain concepts are expected; do not copy a page's single primary Deepen domain blindly.
3. **Introduce first-class resource records only when the resource dimension is ready to be represented.** Define stable resource IDs, resource kinds (page, demonstration, experiment, implementation, reference), language, status, provenance, and local path/external URL. Then make concept-resource associations many-to-many. Preserve page IDs as page identifiers; do not overload them as universal resource IDs.
4. **Add referential-integrity tests across dimensions.** Check concept-domain membership, resource IDs, resource locations/status, and concept-resource endpoints. Include fixtures for one resource linked to multiple concepts and one concept linked to multiple resource kinds.
5. **Add a concept-map projection.** Generate it from canonical domain/concept/resource records and typed relations. Preserve IDs and edge types. Keep it distinct from the existing page-navigation map and curriculum route.
6. **Test projection determinism and bilingual parity.** Build from the same canonical source twice and compare normalized output; test that FR/EN labels do not create duplicate concept nodes.

## Non-goals

- No second page map or competing concept registry.
- No graph database or RDF store at this stage.
- No conversion of every page heading into a concept.
- No inference of prerequisites from reading order or page hierarchy.
- No automatic merging of pages based on lexical similarity.
