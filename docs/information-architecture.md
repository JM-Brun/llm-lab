# Information architecture and metadata governance

**Status:** architecture contract, 2026-11-04  
**Scope:** Quarto learning site, page metadata, learning maps, conceptual relationships, controlled tags, templates, generated indexes and validation.

This document is the architectural entry point for the repository's information systems. It defines ownership boundaries and integration rules; it does not replace the detailed contracts linked below.

## 1. Architectural decision

Maintain **one canonical source per kind of information**, then derive reader-facing views from it. A page, a concept, a tag, a route and a template are different entities and must not be used as substitutes for one another.

The repository already has a navigable, bilingual page graph generated from `LLM-LAB-PAGE-MAP v1`, a curriculum source of truth, and a six-domain taxonomy being integrated through PR #391. The intended knowledge architecture has three distinct dimensions—domains, concepts, and resources—and two complementary graph projections: a pedagogical path and a non-sequential knowledge map. Preserve these as distinct models and views. Do not add a competing graph or duplicate taxonomy. This audit distinguishes the intended domain model from what the currently inspected page-map implementation actually serializes; implementation gaps must be recorded, not hidden by renaming page-level metadata as a concept ontology.

## 2. System inventory and ownership

| Concern | Canonical owner | What it owns | Must not become |
|---|---|---|---|
| Learning content | `site/**/*.qmd` | Explanations, examples, equations, references and page body | A second copy in JSON/YAML indexes |
| Page identity and editorial metadata | One `LLM-LAB-PAGE-MAP` block per page, governed by `docs/page-metadata-schema.md` | Stable page ID, scope, purpose, editorial type, destination, level, language, status, page relations | A concept record or a second archetype taxonomy |
| Search keywords | Quarto `keywords` front matter | Search/indexing projection of controlled page tags | An independent tag vocabulary |
| Page classification | Controlled `type`, `destination`, `level`, `language`, `status` tags | Facets for filtering and site organization | A taxonomy of scientific concepts |
| Topic identifier | Controlled `topic:<id>` tag | Bilingual page grouping / subject key for a page | A canonical concept entity or a substitute for concept IDs |
| Suggested learning route | `suggested_route.previous/next` in page metadata | Optional reader navigation | Hard prerequisites or conceptual parenthood |
| Conceptual page hierarchy | `hierarchy.parents/children` in page metadata | Genuine broader/narrower page relationships | Sequence, data flow, implementation dependency or mere association |
| Cross-links | `related` in page metadata | Useful non-hierarchical page relationships | A generic catch-all for every possible edge |
| Interactive page map | Generated `learning-map-data-{fr,en}.json` from page metadata | Reader-facing projection of published pages, their route/hierarchy/related edges, and extracted section headings | The complete three-dimensional knowledge graph or an editable source of truth |
| Knowledge graph (domain model) | Existing project-level model as specified by the project owner; canonical storage/schema must be verified against the active implementation | Six domains, concept entities with typed semantic relations, and reusable resource entities | The page metadata graph or a list of page headings |
| Section labels in map | Extracted headings from page bodies | A small visual summary of page contents | Canonical concepts, ontology nodes or stable IDs |
| Page composition | `docs/page-template-system.md` and quick starts | Soft editorial prompts and reusable structures | Required page schemas or competing metadata types |
| Visual language | `docs/design-system.md` | Components, typography, spacing, accessibility and responsive behavior | Per-template design systems |
| Curriculum sequence and implementation status | `docs/learning-path.md` | Authoritative module order, prerequisites, evidence and build status | A duplicate page graph or public navigation configuration |
| Historical knowledge | `data/history-pilot.yml` with `docs/history-data-model.md` | Events, sources, concepts and typed historical relations | A second general-purpose concept registry |
| Validation | `scripts/check_page_metadata.py`, tests and CI | Contract enforcement | A hidden content authoring system |

### Important boundary: page tags are not a concept taxonomy

The `topic` tag is a stable subject key attached to a page. It is not interchangeable with a concept entity ID. Likewise, headings extracted into the page-map `section_labels` array are display hints, not identified concepts.

The project's intended knowledge graph has three dimensions:

- **Domains:** six controlled knowledge families that classify concepts. Domain membership is classification, not a semantic edge or a reading prerequisite.
- **Concepts:** stable, language-independent entities with bilingual preferred labels, definitions, aliases, provenance, and typed relations such as prerequisite, generalization, application, and opposition.
- **Resources:** pages, demonstrations, experiments, implementations, and references. A resource can support several concepts, and a concept can be supported by several resources; model this as a many-to-many association with an explicit relation role where useful.

It also has two distinct projections: (1) the **pedagogical path**, which represents learning sequence and prerequisites needed to understand/build an LLM; and (2) the **knowledge map**, which exposes domains, concepts, advanced material, and cross-cutting relations without imposing a reading order. These projections must not be conflated with one another or with the page-level map.

The currently inspected `LLM-LAB-PAGE-MAP v1` implementation is narrower: its nodes are published pages; its edges are suggested route, page hierarchy, and related-page links; its displayed `section_labels` are extracted headings. PR #391 adds a six-value `domain` classification for Deepen pages, but that field is currently page metadata, not proof of a separately serialized domain/concept/resource graph. The typed concept relations and reusable resource entities must be audited against their actual canonical source and schema before changing or duplicating them. This distinction is an implementation audit finding, not a recommendation to create a second graph.

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
| Concept schemes / controlled vocabularies | W3C SKOS | Use for a future explicit concept taxonomy: `skos:ConceptScheme`, `prefLabel`, `altLabel`, `definition`, `broader`, `narrower`, `related` |
| Public educational page description | Schema.org `LearningResource` / `WebPage` | Prefer Quarto-supported metadata or generated JSON-LD if search/discovery needs justify it; do not duplicate it manually per page |
| Graph serialization / linked data | JSON-LD 1.1 | Defer until external graph interoperability or cross-project linking is required |
| Learning-resource interoperability | 1EdTech CASE | Consider only if formal competencies, educational frameworks or curriculum structures must be exchanged with other platforms |

SKOS is appropriate if a true concept taxonomy is added. It is not a replacement for the page graph: page routes, page hierarchy, curriculum prerequisites and historical evidential relations have different semantics and should remain separately typed.

Do not introduce RDF triple stores, graph databases, CASE exports or a full ontology toolchain for the current static bilingual site. A versioned YAML source plus JSON projection and deterministic validators is proportionate.

## 6. Concept and resource model: audit before extension

Do not introduce a new concept registry or resource catalogue until the existing canonical implementation has been located and assessed. The project-level model requires stable language-neutral concept IDs and bilingual records, for example:

```yaml
id: attention.scaled_dot_product
pref_label:
  fr: Attention à produits scalaires mise à l'échelle
  en: Scaled dot-product attention
alt_label:
  fr: Attention à produit scalaire normalisé
  en: Scaled attention
definition:
  fr: ...
  en: ...
broader:
  - attention
narrower: []
related:
  - attention.causal_masking
pages:
  fr: fr/scaled-dot-product-attention
  en: en/scaled-dot-product-attention
sources: []
status: active
```

This is an illustrative shape for evaluating the existing model, not an instruction to create a parallel dataset and not a claim that SKOS is already implemented. If the current model has equivalent fields, document and validate them in place. Map its concept scheme to SKOS where useful. Page metadata and resource records should reference concept IDs; they should not duplicate concept labels or definitions.

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

## 9. Audit findings and next technical steps

The current implementation already has strong foundations: a documented page metadata contract, controlled tag dimensions, stable page IDs, reciprocal relation checks, cycle checks, bilingual parity checks, render-list coverage checks, generated map JSON, unit tests and CI integration.

The following gaps should be addressed incrementally:

1. **Make the ownership map discoverable.** This document is the index for the information architecture; detailed documents remain canonical for their individual concerns.
2. **Use semantically accurate map fields.** The learning-map payload and UI now call extracted headings `section_labels`; they are navigation landmarks, not concept records.
3. **Make generated outputs explicitly generated.** Keep learning-map JSON out of hand-maintained source and ensure it is ignored or reproducibly refreshed in CI/builds.
4. **Formalize machine-readable schemas when stable.** Extract page metadata shape and controlled vocabularies to JSON Schema Draft 2020-12; validate both shape and graph semantics.
5. **Add an automated architecture consistency check.** Detect duplicate ownership, unknown tag dimensions, unused vocabularies, stale generated data and links to missing source records.
6. **Keep graph projections separate.** The page-level navigation graph, pedagogical path, and domain/concept/resource knowledge graph have different node and edge semantics. Integrate them through stable IDs and generated projections; do not merge their relations into one generic `related` edge.
7. **Verify the canonical knowledge-graph source.** Locate the existing domain/concept/resource records and typed relation schema, then make the ownership table and validators point to those exact files before proposing structural changes.
8. **Keep historical data separate.** The history model has its own event/source semantics and evidence requirements; connect it through canonical concept IDs only where the existing model supports it.

## 10. Canonical documentation index

| Concern | Canonical reference |
|---|---|
| Overall information architecture | This document |
| Domain/concept/resource knowledge graph | Existing canonical model: path and schema to be verified in the implementation audit |
| Page metadata, tags and page graph | [Page metadata schema](page-metadata-schema.md) |
| Learning-map implementation | `scripts/build_learning_map.py`, `tests/unit/test_learning_map.py` |
| Metadata validation | `scripts/check_page_metadata.py`, `tests/unit/test_page_metadata.py` |
| Curriculum and prerequisites | [Learning path](learning-path.md) |
| Page composition | [Page-template system](page-template-system.md) |
| Page type to template mapping | [Site page design system](site-page-design-system.md) |
| Visual design | [Design system](design-system.md) |
| Historical dataset | [History data model](history-data-model.md) |
| Contributor process | [Contributing guide](../CONTRIBUTING.md)) |
| Repeatable information-architecture audits | [Knowledge architecture audit skill](../.github/skills/knowledge-architecture-audit/SKILL.md) |
