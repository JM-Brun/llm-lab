# Information architecture and metadata governance

**Status:** architecture contract, 2026-11-04  
**Scope:** Quarto learning site, page metadata, learning maps, conceptual relationships, controlled tags, templates, generated indexes and validation.

This document is the architectural entry point for the repository's information systems. It defines ownership boundaries and integration rules; it does not replace the detailed contracts linked below.

## 1. Architectural decision

Maintain **one canonical source per kind of information**, then derive reader-facing views from it. A page, a concept, a tag, a route and a template are different entities and must not be used as substitutes for one another.

The repository already has a navigable, bilingual page graph generated from `LLM-LAB-PAGE-MAP v1`, a curriculum source of truth, and six controlled page-level Deepen domains (PR #391, merged), and a bilingual concept registry (PR #399, merged). Concept-to-domain membership and the canonical bilingual domain registry were merged in PR #404. First-class non-page resources are now curated in `data/resources.yml`; the initial seed is limited to five guided-build implementation modules. The intended knowledge architecture has three distinct dimensions—domains, concepts, and resources—and two complementary graph projections: a pedagogical path and a non-sequential knowledge map. Preserve these as distinct models and views. Do not add a competing graph or duplicate taxonomy. Record implementation gaps rather than hiding them by renaming page-level metadata as a concept ontology.

## 2. System inventory and ownership

| Concern | Canonical owner | What it owns | Must not become |
|---|---|---|---|
| Learning content | `site/**/*.qmd` | Explanations, examples, equations, references and page body | A second copy in JSON/YAML indexes |
| Page identity and editorial metadata | One `LLM-LAB-PAGE-MAP` block per page, governed by `docs/page-metadata-schema.md` | Stable page ID, scope, purpose, editorial type, destination, level, language, status, page relations | A concept record or a second archetype taxonomy |
| Search keywords | Quarto `keywords` front matter | Search/indexing projection of controlled page tags | An independent tag vocabulary |
| External source catalogue | `data/sources.yml`, governed by `docs/source-catalogue-schema.md` | Source identity, scan history, provenance, primary/secondary themes, retrieval tags and typed metadata | Bibliography, concept registry, page metadata or implementation-resource registry |
| Source extraction records | `data/extractions/<source-id>.yml` | Atomic evidence-linked claims, explanations, visuals, experiments and integration proposals | Source identity, canonical concepts or published page content |
| Source facets | `data/source-taxonomy.yml` plus `data/domains.yml` | Controlled source types, contribution types, audiences, statuses and tag policy | A second domain or concept taxonomy |
| Page classification | Controlled `type`, `destination`, `level`, `language`, `status` tags | Facets for filtering and site organization | A taxonomy of scientific concepts |
| Topic identifier | Controlled `topic:<id>` tag | Bilingual page grouping / subject key for a page | A canonical concept entity or a substitute for concept IDs |
| Suggested learning route | `suggested_route.previous/next` in page metadata | Optional reader navigation | Hard prerequisites or conceptual parenthood |
| Conceptual page hierarchy | `hierarchy.parents/children` in page metadata | Genuine broader/narrower page relationships | Sequence, data flow, implementation dependency or mere association |
| Cross-links | `related` in page metadata | Useful non-hierarchical page relationships | A generic catch-all for every possible edge |
| Interactive learning map | Generated `learning-map-data-{fr,en}.json` from page metadata and `data/concepts.yml` | Two selectable projections: a page graph with route/hierarchy/related edges and section headings, and a concept graph with stable concept nodes, typed relations, and linked resource pages | The canonical authoring source or a unified graph that conflates page and concept relations |
| Knowledge graph (domain model) | `data/domains.yml`, `data/concepts.yml`, and `data/resources.yml` | Controlled domains, stable concepts with typed semantic relations, and reusable non-page resource entities | The page metadata graph or a list of page headings |
| Section labels in map | Extracted headings from page bodies | A small visual summary of page contents | Canonical concepts, ontology nodes or stable IDs |
| Page composition | `docs/page-template-system.md` and quick starts | Soft editorial prompts and reusable structures | Required page schemas or competing metadata types |
| Visual language | `docs/design-system.md` | Components, typography, spacing, accessibility and responsive behavior | Per-template design systems |
| Curriculum sequence and implementation status | `docs/learning-path.md` | Authoritative module order, prerequisites, evidence and build status | A duplicate page graph or public navigation configuration |
| Historical knowledge | `data/history-pilot.yml` with `docs/history-data-model.md` | Events, sources, concepts and typed historical relations | A second general-purpose concept registry |
| Validation | `site/tools/check_page_metadata.py`, tests and CI | Contract enforcement | A hidden content authoring system |

### Important boundary: page tags, source tags and concepts are different things

The `topic` tag in page metadata is a stable subject key attached to a page. Source tags in `data/sources.yml` are namespaced retrieval facets governed by `data/source-taxonomy.yml`. Neither is interchangeable with a concept entity ID. Source domains reuse `data/domains.yml`; source `concept_ids` explicitly reference `data/concepts.yml`. Do not infer concept membership or semantic relations from tag overlap. Likewise, headings extracted into the page-map `section_headings` array are display hints, not identified concepts.

The project's intended knowledge graph has three dimensions:

- **Domains:** six controlled knowledge families. Page-level `domain` metadata classifies a Deepen page into one primary discovery domain. Concept-level membership is a separate association and may be many-to-many; PR #404 implements this in `data/domains.yml` and each concept's `domains` field. Do not infer concept membership from a page's primary domain.
- **Concepts:** stable, language-independent entities with bilingual preferred labels, definitions, aliases, provenance, and typed relations such as prerequisite, generalization, application, and opposition.
- **Resources:** published pages plus independently identified non-page artifacts. `data/resources.yml` currently models five implementation modules; other kinds are deferred until concrete artifacts justify them. A resource may be referenced by several bilingual pages and associated with several concepts; concept-resource links are many-to-many.

It also has two distinct projections: (1) the **pedagogical path**, which represents learning sequence and prerequisites needed to understand/build an LLM; and (2) the **knowledge map**, which exposes domains, concepts, advanced material, and cross-cutting relations without imposing a reading order. These projections must not be conflated with one another or with the page-level map.

The interactive learning map exposes two distinct modes. The page graph reads published page metadata and renders suggested route, page hierarchy, related-page links, and extracted `section_headings`. The concept graph is generated from `data/concepts.yml` and renders stable concept nodes, typed concept relations, and links to their resource pages. These UI modes retain different node and edge semantics; the current UI has not yet been extended to render non-page resource nodes. Separately, `data/resources.yml` supplies five first-class implementation resources to the JSON-LD projection, with shared FR/EN page references and many-to-many concept associations. PR #391's six-value `domain` field still classifies Deepen pages only. PR #399 added the canonical concept seed; PR #404 added the separate domain registry and concept memberships.

## 3. Relationship semantics

Keep the existing relation fields, with these precise meanings:

- `suggested_route`: recommended reading transition; optional and reader-oriented.
- `hierarchy.parents/children`: conceptual containment, generalization or decomposition; reciprocal and acyclic.
- `related`: meaningful connection without containment; use sparingly.
- Curriculum prerequisites: learning dependencies that affect whether a learner can understand or complete a module. These belong in `docs/learning-path.md` unless a future explicit prerequisite model is introduced.
- Historical relations: evidence-backed typed edges between historical events and concepts; these belong to the history data model.

Do not infer one relation from another. A suggested next page is not automatically a child, a parent is not automatically a prerequisite, and chronological succession is not evidence of influence.

## 4. Metadata contract and duplication policy

For the current Quarto site, retain the existing `LLM-LAB-PAGE-MAP v1` comment as the rich source record and Quarto `keywords` as its search-facing projection. The two lists are intentionally synchronized by validation; they are not independent authoring locations.

1. Author controlled tags once in the page-map block, then mirror them exactly into Quarto `keywords` in the same change.
2. Keep the six existing dimensions stable. Do not add `archetype`, `scientific_pattern`, `diataxis` or a duplicate `category` dimension without a demonstrated query/use case.
3. Use repository-relative stable page IDs in relations, never rendered HTML paths.
4. Use the `topic` identifier consistently across translated counterparts; translations may have different slugs.
5. Treat generated JSON as disposable build output. Never hand-edit it.
6. Keep body prose as the source of truth for full explanations; metadata is concise routing and classification data.
7. A metadata schema change requires a versioned migration plan, validator changes, tests and documentation updates in the same pull request.

## 5. Standards: adopt selectively

Use established standards where they solve a real interoperability or validation problem; do not add standards-shaped complexity for appearance.

| Need | Recommended standard / convention | Application |
|---|---|---|
| Human-edited structured metadata | YAML 1.2 | Continue using YAML front matter and page-map blocks |
| Generated interchange data | JSON (RFC 8259) | Continue generating JSON learning-map payloads |
| Stable identifiers | URI design principles (RFC 3986) | Keep durable repository-relative IDs now; use canonical URIs if records are exchanged externally |
| Schema validation | JSON Schema Draft 2020-12 | Adopt when the page/concept data contract is extracted into a machine-readable schema; keep semantic graph checks in Python |
| Concept schemes / controlled vocabularies | W3C SKOS | Align the existing bilingual concept and domain registries using `skos:ConceptScheme`, `skos:Concept`, `prefLabel`, `definition`, and `narrower` only for genuine generalization |
| Public educational page description | Schema.org `LearningResource` / `WebPage` | Generated from published page metadata in `site/knowledge-graph.jsonld`; use `about` for current concept-page associations and do not infer `teaches` |
| Graph serialization / linked data | JSON-LD 1.1 | Implemented as a deterministic generated projection; YAML remains canonical |
| Learning-resource interoperability | 1EdTech CASE | Consider only if formal competencies, educational frameworks or curriculum structures must be exchanged with other platforms |

SKOS is now used for the existing concept and domain schemes. It is not a replacement for the page graph: page routes, page hierarchy, curriculum prerequisites and historical evidential relations have different semantics and should remain separately typed.

Do not introduce RDF triple stores, graph databases, CASE exports or a full ontology toolchain for the current static bilingual site. A versioned YAML source plus JSON projection and deterministic validators is proportionate.



The implemented standards projection is specified in [knowledge-graph-standards.md](knowledge-graph-standards.md) and generated by `site/tools/export_knowledge_graph.py`. It aligns the existing concepts/domains with SKOS, published concept-linked pages with Schema.org, and export derivation with PROV-O. It deliberately preserves project-specific predicates for prerequisite, composition, implementation, process and evaluation relations. The export is not a claim that every scientific definition has claim-level provenance.

## 6. Concept and resource model: canonical sources and remaining gaps

The canonical concept registry now exists at `data/concepts.yml` (PR #399, merged). It uses language-independent kebab-case IDs, bilingual labels and definitions, typed concept relations, and page-ID associations. Its 13 concepts and 12 relations are a reviewed seed, not complete ontology coverage.

The six controlled domain definitions are maintained in `data/domains.yml` in PR #404. The PR also adds a `domains` list to each seeded concept. This is distinct from the page-level `domain` field: a page has one primary Deepen classification, while a concept may belong to several knowledge domains. Membership is classification, not a semantic relation or prerequisite. Concept-domain membership is now canonical data; it remains a classification association, not a semantic relation or prerequisite.

### Relation semantics

Concept relations are directed triples. Their direction must be documented and validated per relation type. The registry validator enforces acyclicity for `prerequisite` and `generalizes`; these constraints must not be generalized to application or contribution relations. `contrasts-with` is symmetric and PR #404 defines a single-storage convention: store the lexicographically smaller concept ID in `from` and the larger in `to`, without a reciprocal duplicate.

### Resource model: current state

Concept records continue to list published page IDs in `concepts[].resources`; this field is intentionally unchanged and must not be reinterpreted as non-page resource IDs. First-class non-page resources are now owned by `data/resources.yml`, with stable IDs distinct from page and concept IDs.

The initial registry is deliberately narrow: exactly the five implementation modules named in the bilingual guided-build route. Each record has a controlled `kind` (`implementation` only in this first slice), bilingual labels/descriptions, a BCP 47 human-language tag, optional programming language, lifecycle status, a discriminated local repository path or external URL, `referenced_by` published page IDs, and concept IDs. The French and English walkthroughs point to one shared resource ID; the resource is not duplicated by language. Provenance fields (`creator`, `publisher`, `source_url`, `license`) are optional and unknown values are omitted. Repository visibility is not evidence of a licence.

`site/tools/check_resource_registry.py` validates unique IDs, vocabularies, bilingual metadata, BCP 47 syntax, locations, local path containment after symlink resolution, HTTP(S) URL syntax without network access, published-page references, concept references, and optional provenance. Concept-resource associations are many-to-many. The JSON-LD projection represents implementation artifacts as `schema:SoftwareSourceCode`; the interactive map UI remains a separate follow-up. Do not add demonstrations, experiments, datasets, tests, papers, or media until concrete artifacts and learner-facing references justify them.


## 7. Templates and page roles

The current separation is sound and should be preserved:

- editorial `type` answers the stable role a page plays in this repository;
- documentation genre helps identify the reader task;
- scientific/implementation pattern determines the explanatory approach;
- composition modules are optional ingredients;
- visual components come from the shared design system.

These dimensions are complementary, not competing taxonomies. The canonical composition guide is `docs/page-template-system.md`; quick-start templates remain examples. `docs/site-page-design-system.md` is an index/mapping only.

## 8. Scalability and maintenance requirements

For every future system or schema change:

- **Single ownership:** every field and relation has one canonical authoring location.
- **Stable identity:** IDs do not depend on translated labels, display titles or output URLs.
- **Typed relations:** each edge has one documented meaning and validation rule.
- **Deterministic projections:** generated maps are reproducible from source files.
- **Bilingual parity:** translations share IDs at topic/concept level and equivalent structural metadata.
- **Validation:** syntax, vocabulary, uniqueness, referential integrity, reciprocity, acyclicity and render coverage are tested.
- **Compatibility:** schema versions and migration steps are explicit before breaking changes.
- **Bounded complexity:** no database or extra dependency until query volume, collaboration or interoperability requires it.
- **Accessibility:** graph/map views have a usable list or textual equivalent and are not the only navigation route.

## 9. Implementation status and bounded follow-up

The source-of-truth index is now established by this document and surfaced from both the repository [README](../README.md) and [contributor guide](../CONTRIBUTING.md). Detailed contracts remain in their owning documents; this index must not repeat their full rules.

Implemented controls include stable page IDs, controlled page metadata, relation validation, bilingual parity checks, render-list coverage, concept/domain/resource registries, deterministic JSON-LD export, unit tests, and CI integration. The [knowledge-graph implementation audit](knowledge-graph-implementation-audit.md) records the evidence and the remaining graph-specific gaps.

Keep the remaining work explicit and separately owned:

1. **Interactive concept graph:** render typed relation semantics and concept-domain membership; add resource nodes only with a reviewed interaction model. Tracked by [#416](https://github.com/JM-Brun/llm-lab/issues/416) and [#418](https://github.com/JM-Brun/llm-lab/issues/418). The JSON-LD export and interactive map are different projections and need separate validation.
2. **Rendered reader experience:** verify the guided route, page graph, concept graph, FR/EN navigation, responsive behavior, keyboard/touch interaction, and textual alternatives in a real browser. Tracked by [#337](https://github.com/JM-Brun/llm-lab/issues/337) and its child issues. A successful Quarto build is not browser evidence.
3. **Machine-readable schema evolution:** consider JSON Schema only when the current Pydantic/YAML contracts demonstrate a concrete interoperability or validation need. Any schema change must include migration notes, fixtures, validators, and compatibility review.
4. **Cross-cutting consistency checks:** extend automated checks only for demonstrated failure modes (duplicate ownership, stale generated output, dangling references, unused controlled values). Do not add a generic framework before a concrete contract needs it.
5. **Evidence and provenance:** dataset/build provenance is not claim-level scientific evidence. Preserve this distinction; claim-level source assertions require a separate, justified model extension.

Historical events and source genealogy remain governed by [the history data model](history-data-model.md); connect them to concepts only through explicit, supported identifiers.

## 10. Maintenance workflow

Apply this workflow whenever a contribution changes a canonical registry, page metadata contract, curriculum structure, shared template, or generated projection.

1. **Locate ownership.** Start with the [canonical documentation index](#11-canonical-documentation-index) and identify the one authoritative source. If no owner exists, update this architecture document before adding a new source or field.
2. **Change source, not projection.** Edit the canonical YAML, page metadata, curriculum document, or shared template. Never hand-edit generated graph JSON, generated route fragments, or rendered output.
3. **Update contract and examples together.** If a field, controlled value, relation meaning, or generation contract changes, update its owning schema/guide, representative records, fixtures, and migration notes in the same PR. Do not copy the full rule into README and CONTRIBUTING; link to its owner.
4. **Validate proportionately.** Run the owning registry validator and focused tests; run the full Python checks for code/schema changes. Render the site when page sources, metadata, generated includes, or navigation change.
5. **Inspect projections.** Check generated links, bilingual parity, and the affected FR/EN rendered pages. Interactive graph changes additionally require keyboard, touch, narrow viewport, empty/error state, and textual-alternative review.
6. **Report evidence precisely.** Record commands and outcomes. Keep source review, unit/integration tests, CI, Quarto render, browser inspection, accessibility evaluation, and learner testing as separate evidence categories.
7. **Close the loop.** Update the owning issue and the [implementation audit](knowledge-graph-implementation-audit.md) when its status changes. Update this index only when ownership, architecture, or maintenance procedures change; do not turn it into a duplicate status dashboard.

### Routine commands

From the repository root, use the focused checks relevant to the changed surface:

```bash
# Core Python quality and tests
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest

# Page metadata and knowledge registries
uv run python site/tools/check_page_metadata.py
uv run python site/tools/check_concept_registry.py
uv run python site/tools/check_resource_registry.py

# Deterministic knowledge-graph export
uv run python site/tools/export_knowledge_graph.py

# Bilingual site build and rendered graph validation
quarto render site
uv run python site/tools/check_knowledge_graph_rendered.py
```

The standards profile documents the graph-export and rendered-output checks; use [knowledge-graph standards](knowledge-graph-standards.md) rather than duplicating their implementation details here.

## 11. Canonical documentation index

| Concern | Canonical reference |
|---|---|
| Overall information architecture | This document |
| Knowledge graph implementation audit | [Implementation audit](knowledge-graph-implementation-audit.md) |
| Domain/concept/resource knowledge graph | `data/concepts.yml`; `data/domains.yml`; `data/resources.yml` |
| External sources, classification and extraction records | [Source catalogue schema](source-catalogue-schema.md); `data/sources.yml`; `data/source-taxonomy.yml`; `data/extractions/` |
| Page metadata, tags and page graph | [Page metadata schema](page-metadata-schema.md) |
| Global and local breadcrumb rendering | [Nested breadcrumb navigation contract](nested-breadcrumb-navigation-contract.md) |
| Learning-map implementation | `site/tools/build_learning_map.py`, `tests/unit/test_learning_map.py` |
| Metadata validation | `site/tools/check_page_metadata.py`, `tests/unit/test_page_metadata.py` |
| Curriculum and prerequisites | [Learning path](learning-path.md) |
| Page composition | [Page-template system](page-template-system.md) |
| Page type to template mapping | [Site page design system](site-page-design-system.md) |
| Visual design | [Design system](design-system.md) |
| Historical dataset | [History data model](history-data-model.md) |
| Contributor process | [Contributing guide](../CONTRIBUTING.md) |
| Repeatable information-architecture audits | [Knowledge architecture audit skill](../.agents/skills/knowledge-architecture-audit/SKILL.md) |
| Page review evidence and remaining checks | [Page audit inventory](page-audit-inventory.md) |
| Editorial ownership and core-route audits | [Editorial boundary audit](editorial-boundary-audit.md); [2026-11-04 core-route audit](editorial-boundary-audit-2026-11-04.md); [repeatable editorial audit skill](../.agents/skills/editorial-boundary-audit/SKILL.md) |
