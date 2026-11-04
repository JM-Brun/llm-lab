# Knowledge graph standards profile

**Status:** implemented projection, 2026-11-04  
**Canonical sources:** `data/concepts.yml`, `data/domains.yml`, and published `LLM-LAB-PAGE-MAP v1` blocks.  
**Generated interchange:** `site/knowledge-graph.jsonld` via `scripts/export_knowledge_graph.py`.

## 1. Design decision

LLM Lab already has a bilingual concept registry, controlled domains, typed concept relations, page metadata, a curriculum graph and a separate historical model. This is a standards-alignment layer over those existing sources, not a new authoring system.

- YAML remains the only authoring source.
- The existing page and concept graph remains the reader-facing interactive visualization.
- JSON-LD is a deterministic interchange projection, not a second database.
- No RDF store, OWL reasoner or runtime graph service is required.

## 2. Standards profile and actual use

| Standard | Use in LLM Lab | Status / boundary |
|---|---|---|
| W3C SKOS | `skos:ConceptScheme`, `skos:Concept`, language-tagged `prefLabel` and `definition`, domain membership via `dcterms:subject`, genuine generalization via `skos:narrower` | Implemented in JSON-LD export |
| Schema.org | Published pages as `WebPage` + `LearningResource`; `name`, `inLanguage`, `description`, `abstract`, `learningResourceType`, `about`; editorial depth stays project-specific | Implemented from existing page metadata |
| Dublin Core Terms | `dcterms:subject`, `dcterms:format` | Implemented where semantics fit |
| W3C PROV-O | Export entity, generation activity and source-artifact derivation | Implemented for dataset-level provenance only |
| JSON-LD 1.1 | Interchange serialization with explicit contexts and stable absolute identifiers | Implemented |
| JSON Schema 2020-12 | Structural contract for the canonical YAML model | Deferred; current Python validators enforce source-specific and graph constraints |
| SHACL | RDF graph validation | Deferred until RDF-native validation is needed |
| 1EdTech CASE | Exchange of formal competency frameworks | Not currently needed |

Standards references:
- [SKOS Reference (W3C Recommendation)](https://www.w3.org/TR/skos-reference/)
- [Schema.org LearningResource](https://schema.org/LearningResource)
- [Dublin Core Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- [PROV-O (W3C Recommendation)](https://www.w3.org/TR/prov-o/)
- [JSON-LD 1.1 (W3C Recommendation)](https://www.w3.org/TR/json-ld11/)
- [SHACL (W3C Recommendation)](https://www.w3.org/TR/shacl/)

## 3. Entity identity and resource model

### Concepts

Concept IDs are language-independent and receive stable absolute identifiers under `https://jm-brun.github.io/llm-lab/id/concept/{id}`. These identifiers are currently used in the JSON-LD graph; dereferenceable concept landing pages are not yet published. French and English labels are language-tagged values on one concept node, not duplicate concepts.

### Domains

The six controlled knowledge domains receive stable identifiers under `https://jm-brun.github.io/llm-lab/id/domain/{id}`. They are represented as a separate SKOS concept scheme. A concept can be associated with multiple domains using `dcterms:subject`; membership does not imply prerequisite, containment or exclusivity.

### Learning resources

Each published FR/EN page referenced by the concept registry is described as a Schema.org `LearningResource` and `WebPage`. Its stable public URL is the resource identifier. The export uses `schema:about` because the current `resources` field asserts topical association, not necessarily that every linked page explicitly teaches or assesses the concept. Do not replace this with `schema:teaches` without an explicit learning-outcome mapping. The editorial `level` values (`overview`, `core`, `applied`, `advanced`, `reference`) are exported as `llmlab:editorialLevel`, not `schema:educationalLevel`, because they classify page role/depth rather than learner educational attainment.

Code modules, tests, experiments, external papers and media are not yet first-class resource records in the canonical registry. They remain a future extension; do not infer their identity from arbitrary links in page prose.

## 4. Relation mapping

The source relation vocabulary remains authoritative. Only a genuine generalization relation is mapped to SKOS hierarchy:

| Source relation | Export predicate | Reason |
|---|---|---|
| `generalizes` (general → specific) | `skos:narrower` on the general concept | Correct direction for a direct narrower concept |
| `prerequisite` | `llmlab:prerequisite` | Learning dependency, not taxonomy |
| `part-of` | `llmlab:partOf` | Structural composition is not automatically broader/narrower |
| `contrasts-with` | `llmlab:contrastsWith` | More specific than generic associative relatedness |
| `analogy` | `llmlab:analogy` | Analogy is not equivalence |
| `implemented-by` | `llmlab:implementedBy` | Implementation relation |
| `applies-to` | `llmlab:appliesTo` | Application relation |
| `constrains` | `llmlab:constrains` | Constraint relation |
| `produces` | `llmlab:produces` | Process/output relation |
| `normalized-by` | `llmlab:normalizedBy` | Transformation relation |
| `evaluated-by` | `llmlab:evaluatedBy` | Evaluation relation |
| `represented-by` | `llmlab:representedBy` | Representation relation |
| `contributes-to` | `llmlab:contributesTo` | Contribution, not sufficiency |
| `mapped-by` | `llmlab:mappedBy` | Mapping relation |

The export deliberately does not map every relation to `skos:related`: doing so would erase distinctions needed by the learning map and future queries. It also does not infer inverse edges unless a standard explicitly defines the inverse and the consumer needs it.

## 5. Provenance boundary

PROV-O currently records that the generated JSON-LD entity was derived from:
- `data/concepts.yml`;
- `data/domains.yml`;
- the concrete Quarto source files containing the published page metadata referenced by the concept registry.

The export links each page source to its repository file rather than treating the whole `site/` directory as a single source artifact. These links target the repository's current `main` branch; they are navigational source references, not immutable version-pinned evidence records.

This establishes dataset-level build provenance. It does **not** establish which scientific paper supports each definition or relation. Claim-level evidence provenance requires explicit source assertions and is a separate future data-model change. Historical source records and relations remain governed by `docs/history-data-model.md`.

## 6. Generate and validate

From the repository root:

```bash
uv run python scripts/export_knowledge_graph.py
uv run pytest
```

The exporter is deterministic: it does not embed wall-clock timestamps or environment-specific paths. The generated `site/knowledge-graph.jsonld` must not be hand-edited.

The existing `scripts/check_concept_registry.py` remains responsible for source-level graph semantics and referential integrity. The export tests check the standards projection, stable identifiers, bilingual labels, page links and provenance structure. A future SHACL layer is justified only if the RDF graph itself becomes a maintained validation boundary.

## 7. Model ownership boundaries

- Page routes, page hierarchy and editorial metadata: `LLM-LAB-PAGE-MAP v1`.
- Concept identities and semantic relations: `data/concepts.yml`.
- Controlled knowledge domains: `data/domains.yml`.
- Learning sequence, implementation prerequisites and milestone evidence: `docs/learning-path.md`.
- Historical events, source evidence and genealogy: `data/history-pilot.yml` and `docs/history-data-model.md`.
- Reader-facing projections: `scripts/build_learning_map.py` and the JSON-LD exporter.

Never infer a concept from a page heading, a prerequisite from sidebar order, or historical influence from chronology alone.
