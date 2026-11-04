# Information architecture and metadata governance

**Status:** architecture contract, 2026-11-04  
**Scope:** Quarto learning site, page metadata, learning maps, conceptual relationships, controlled tags, templates, generated indexes and validation.

This document is the architectural entry point for the repository's information systems. It defines ownership boundaries and integration rules; it does not replace the detailed contracts linked below.

## 1. Architectural decision

Maintain **one canonical source per kind of information**, then derive reader-facing views from it. A page, a concept, a tag, a route and a template are different entities and must not be used as substitutes for one another.

The repository already has a useful page-level contract (`LLM-LAB-PAGE-MAP v1`) and a generated bilingual learning map. The next step is not to add another catalogue or graph. It is to make the boundaries between existing mechanisms explicit and prevent page metadata from silently becoming a concept ontology.

## 2. System inventory and ownership

| Concern | Canonical owner | What it owns | Must not become |
|---|---|---|---|
| Learning content | `site/**/*.qmd` | Explanations, examples, equations, references and page body | A second copy in JSON/YAML indexes |
| Page identity and editorial metadata | One `LLM-LAB-PAGE-MAP` block per page, governed by `docs/page-metadata-schema.md` | Stable page ID, scope, purpose, editorial type, destination, level, language, status, page relations | A concept record or a second archetype taxonomy |
| Search keywords | Quarto `keywords` front matter | Search/indexing projection of controlled page tags | An independent tag vocabulary |
| Page classification | Controlled `type`, `destination`, `level`, `language`, `status` tags | Facets for filtering and site organization | A taxonomy of scientific concepts |
| Topic identifier | Controlled `topic:<id>` tag | Bilingual page grouping / subject key | A complete concept definition or a list of all concepts on a page |
| Suggested learning route | `suggested_route.previous/next` in page metadata | Optional reader navigation | Hard prerequisites or conceptual parenthood |
| Conceptual page hierarchy | `hierarchy.parents/children` in page metadata | Genuine broader/narrower page relationships | Sequence, data flow, implementation dependency or mere association |
| Cross-links | `related` in page metadata | Useful non-hierarchical page relationships | A generic catch-all for every possible edge |
| Learning map | Generated `learning-map-data-{fr,en}.json` from page metadata | Reader-facing projection of published pages | An editable source of truth |
| Section labels in map | Extracted headings from page bodies | A small visual summary of page contents | Canonical concepts, ontology nodes or stable IDs |
| Page composition | `docs/page-template-system.md` and quick starts | Soft editorial prompts and reusable structures | Required page schemas or competing metadata types |
| Visual language | `docs/design-system.md` | Components, typography, spacing, accessibility and responsive behavior | Per-template design systems |
| Curriculum sequence and implementation status | `docs/learning-path.md` | Authoritative module order, prerequisites, evidence and build status | A duplicate page graph or public navigation configuration |
| Historical knowledge | `data/history-pilot.yml` with `docs/history-data-model.md` | Events, sources, concepts and typed historical relations | A second general-purpose concept registry |
| Validation | `scripts/check_page_metadata.py`, tests and CI | Contract enforcement | A hidden content authoring system |

### Important boundary: page tags are not a concept taxonomy

The `topic` tag is a stable subject key attached to a page. It does not define a concept, its preferred label, synonyms, definition, broader/narrower concepts, provenance or links to multiple pages. Likewise, headings extracted into the learning-map `concepts` array are display hints, not identified concepts.

Do not describe either mechanism as a complete knowledge graph or ontology. If a reusable concept registry becomes necessary, introduce it as a separate, explicitly modelled dataset (see section 6), and link pages to concept IDs. Do not overload existing page tags.

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

## 6. Criteria for introducing a canonical concept registry

Do not create a registry merely because many pages mention concepts. Introduce one only when at least one use case becomes real:

- one concept has multiple canonical pages or language-specific labels that must be resolved consistently;
- synonyms, abbreviations, translations or deprecated terms need central management;
- broader/narrower concept navigation is required independently of page hierarchy;
- concepts need evidence/provenance records or links to historical events;
- external tools need stable concept identifiers.

If introduced, use a single language-neutral concept ID and a bilingual record, for example:

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

This is an illustrative project record, not a claim that SKOS is already implemented. A future schema should map these fields explicitly to SKOS rather than invent incompatible relation semantics. Page metadata would reference concept IDs; it would not repeat labels or definitions.

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
2. **Stop calling extracted headings concepts.** Rename the generated `concepts` property to `section_labels` (or equivalent) in learning-map data and UI. It currently contains up to six headings, not concept records.
3. **Make generated outputs explicitly generated.** Keep learning-map JSON out of hand-maintained source and ensure it is ignored or reproducibly refreshed in CI/builds.
4. **Formalize machine-readable schemas when stable.** Extract page metadata shape and controlled vocabularies to JSON Schema Draft 2020-12; validate both shape and graph semantics.
5. **Add an automated architecture consistency check.** Detect duplicate ownership, unknown tag dimensions, unused vocabularies, stale generated data and links to missing source records.
6. **Do not merge the historical model into the page graph.** It is a separate domain model with different entities, evidence requirements and edge types; connect through stable concept IDs only if/when a canonical concept registry exists.

## 10. Canonical documentation index

| Concern | Canonical reference |
|---|---|
| Overall information architecture | This document |
| Page metadata, tags and page graph | [Page metadata schema](page-metadata-schema.md) |
| Learning-map implementation | `scripts/build_learning_map.py`, `tests/unit/test_learning_map.py` |
| Metadata validation | `scripts/check_page_metadata.py`, `tests/unit/test_page_metadata.py` |
| Curriculum and prerequisites | [Learning path](learning-path.md) |
| Page composition | [Page-template system](page-template-system.md) |
| Page type to template mapping | [Site page design system](site-page-design-system.md) |
| Visual design | [Design system](design-system.md) |
| Historical dataset | [History data model](history-data-model.md) |
| Contributor process | [Contributing guide](../CONTRIBUTING.md) |
