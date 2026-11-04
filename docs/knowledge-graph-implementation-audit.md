# Knowledge graph implementation audit

**Snapshot date:** 2026-11-04  
**Scope:** repository source and relevant merged/open pull requests inspected for the information-architecture audit.  
**Purpose:** record implementation ownership and gaps without proposing a replacement graph.

## Executive finding

The repository now has the beginnings of a three-dimensional knowledge model, but its implementation is split across two layers:

- The **page graph** is implemented and rendered by the existing bilingual learning map.
- A **typed concept registry** is implemented in `data/concepts.yml` by merged PR [#399](https://github.com/JM-Brun/llm-lab/pull/399). It is a reviewed seed, not yet the full knowledge graph.
- The six **Deepen domains** are currently page-classification metadata, introduced by merged PR [#391](https://github.com/JM-Brun/llm-lab/pull/391).
- Concept-to-domain membership and the canonical bilingual domain registry were merged in PR [#404](https://github.com/JM-Brun/llm-lab/pull/404). First-class non-page resource identities are now introduced in `data/resources.yml`; the initial seed curates only the five implementation modules explicitly named by the bilingual guided-build route. This does not replace the existing page-ID associations in `concepts[].resources`.

The pedagogical path and the knowledge map must remain distinct projections. The former encodes learner progression; the latter supports non-linear discovery and cross-domain navigation.

## Source-of-truth and implementation matrix

| Dimension / projection | Current source | Implemented semantics | Status and boundary |
|---|---|---|---|
| Domains | docs/page-metadata-schema.md; page-map metadata in site/**/*.qmd; scripts/check_page_metadata.py | Six controlled domain IDs classify Deepen content pages; FR/EN counterparts share the ID; page-map generator exports the field | **Implemented at both levels.** Page primary-domain classification remains distinct from many-to-many concept-domain membership. |
| Concepts | data/concepts.yml in PR #399 | Language-independent kebab-case IDs, FR/EN labels and definitions, typed concept-to-concept relations | **Merged seed.** 13 concepts and 12 relations; coverage is intentionally incomplete. |
| Concept relations | data/concepts.yml; scripts/check_concept_registry.py in PR #399 | Directed relation vocabulary including prerequisite, generalizes, applies-to, contrasts-with, and more specific types | **Implemented for the seed.** Endpoints, relation types, self-links, duplicates, and prerequisite/generalization acyclicity are validated. PR #404 added a canonical single-storage orientation for symmetric `contrasts-with` edges. |
| Resources | `data/resources.yml` plus `concepts[].resources` in `data/concepts.yml` | Stable non-page resource IDs; controlled kind/status; bilingual labels/descriptions; BCP 47 human-language tag; optional programming language and provenance; local/external location; `referenced_by` page IDs; many-to-many concept associations | **Implemented for a bounded seed.** Five implementation modules only. `concepts[].resources` remains page IDs; tests and other resource kinds are not inferred or migrated. |
| Pedagogical path | docs/learning-path.md, docs/full-curriculum-plan.md, docs/roadmap.md | Ordered learning stages, prerequisites, progression and deliverables | **Documented curriculum projection.** Do not derive it from sidebar order or the page-map graph. |
| Knowledge map | Domain metadata, concept registry, page metadata, and resource registry | Non-linear discovery, concept relations, page links, and first-class resource descriptions in JSON-LD | **Partially implemented across layers.** The JSON-LD projection now includes five `SoftwareSourceCode` resource nodes and their concept/page associations. The interactive map UI has not yet been extended to render non-page resource nodes or concept-domain membership. |
| Page-navigation graph | docs/page-metadata-schema.md; scripts/check_page_metadata.py; scripts/build_learning_map.py | Page IDs, suggested route, reciprocal page hierarchy, related links, bilingual page parity | **Implemented.** These are page-level relations, not concept-level semantic relations. |
| Section headings | `section_headings` extracted by scripts/build_learning_map.py | Display/search hints for sections within a page | **Implemented as presentation metadata.** They are not concept entities or stable concept IDs. |

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

### Merged concept-registry controls (PR #399)

- `scripts/check_concept_registry.py` validates concept IDs, bilingual labels/definitions, page-resource references, relation vocabulary/endpoints, self-relations, duplicate relations, and cycle constraints for prerequisite/generalization edges.
- `scripts/check_resource_registry.py` validates non-page resource IDs, controlled kind/status, BCP 47 tags, bilingual metadata, discriminated locations, path containment after symlink resolution, external URL syntax, page references, concept references, and optional provenance.
- `tests/unit/test_concept_registry.py` covers the checked-in concept registry and its graph invariants.
- `tests/unit/test_resource_registry.py` covers resource identity, many-to-many concept links, shared FR/EN page references, path traversal and symlink escapes, external URL syntax, lifecycle values, and language tags.
- `tests/unit/test_knowledge_graph_export.py` checks `SoftwareSourceCode` projection, stable resource IDs, bilingual labels, page/concept links, unique page nodes, and registry provenance.
- The validator is integrated into the existing Python CI workflow; no additional workflow is needed.

### Validation evidence

On merged PR #399 head 7bea7ec (2026-11-04), Python CI passed all 127 tests and the Quarto workflow passed bilingual rendering, history timeline parity, and rendered local-link checks. On merged PR #404 head f1bc8da (2026-11-04), Python CI passed the concept/domain validator, page metadata checks, Ruff format/lint, mypy, and all 131 pytest tests. The Quarto workflow also passed bilingual rendering, history timeline parity, and rendered local-link checks.

## Remaining gaps, ordered by dependency

1. **Review the merged concept seed.** Expand `data/concepts.yml` only alongside reviewed content; audit relation direction and avoid implying ontology completeness.
2. **Maintain concept-domain membership.** PR #404 merged `data/domains.yml`, many-to-many concept membership, and a canonical symmetry rule for `contrasts-with`. Review memberships as the concept seed expands; do not infer them from page-level classifications.
3. **Extend the resource model only with evidence.** The initial first-class resource registry now covers the five guided-build implementation modules. Add demonstrations, experiments, datasets, papers, or media only when concrete repository artifacts and learner-facing references justify them.
4. **Extend graph projections deliberately.** The JSON-LD export describes the resource entities; the interactive concept-map UI remains a separate follow-up and must not be changed as part of the source-model migration.
5. **Extend and test the existing concept-map projection.** Expose concept-domain membership from `data/domains.yml`, with deterministic bilingual output and no duplicate concept nodes or reinterpretation of prerequisites as navigation. Expose non-page resource kinds only when their canonical records exist; preserve concept IDs and typed relation directions.
6. **Review the rendered interaction separately.** Check accessibility, meaningful relationship direction, browser behavior, and responsive layout after the data model and tests; Quarto rendering and static link checks alone do not establish those properties.

## Non-goals

- No second page map or competing concept registry.
- No graph database or RDF store at this stage.
- No conversion of every page heading into a concept.
- No inference of prerequisites from reading order or page hierarchy.
- No automatic merging of pages based on lexical similarity.
