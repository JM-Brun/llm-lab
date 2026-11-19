# Project intelligence layer

**Status:** proposed architecture with a read-only `ProjectIndex`, resource/revision adapters and inverse queries merged in [PR #1399](https://github.com/JM-Brun/llm-lab/pull/1399). The metric registry is documented in [project-metric-registry.md](project-metric-registry.md); the coverage matrix, diagnostics and interfaces remain planned.  
**Scope:** reusable, deterministic queries and explainable diagnostics over the canonical LLM Lab metadata, registries, routes, graph families and project artifacts.  
**Related architecture:** [Information architecture](information-architecture.md), [scalability audit](scalability-capacity-audit-2026-11-18.md), [knowledge-graph implementation audit](knowledge-graph-implementation-audit.md), [cross-graph discovery issue #1233](https://github.com/JM-Brun/llm-lab/issues/1233).

## 1. Purpose

LLM Lab should be able to inspect and reason about its own structure through documented, reusable tools. Metadata must be more than passive annotations: it should support reliable inventories, counts, reverse lookups, coverage analysis, consistency checks, impact analysis and carefully governed construction recommendations.

The proposed **Project Intelligence Layer (PIL)** is a read-only query and analysis layer over existing canonical sources. It is not a new registry, ontology, curriculum, graph, database or source of truth.

It should answer questions such as:

- How many published, planned and retired pages exist, by language, destination, editorial type, topic and domain?
- How many actual stages, lessons, milestones and pages belong to each canonical learning route?
- How many canonical concepts exist, and how many pages, resources, domains, source records, exercises or experiments are explicitly associated with each concept?
- Which pages link to a given page, and which pages are linked from it?
- Which concepts have no canonical teaching page, no bilingual counterpart, no route placement or no implementation/example coverage?
- Which changes affect a page, concept, route stage, computational node or source?
- Which metadata inconsistencies or missing links should be reviewed next?
- Which proposed learning resources would address a demonstrated gap without duplicating existing material?

The layer must make each result explainable and reproducible: users should be able to identify the canonical records, relation semantics, filters and snapshot used to produce it.

## 2. Architectural principles

1. **One canonical owner per fact.** Read existing registries and metadata; never copy them into a parallel hand-maintained index.
2. **Explicit semantics.** A page link, concept relation, curriculum prerequisite, computational edge, source lineage edge and resource association are different relation families.
3. **Deterministic before intelligent.** Counts, lookups, integrity checks and coverage facts must be deterministic. Heuristics and AI produce candidates, never canonical facts.
4. **Stable identity.** Use existing page, concept, resource, source, extraction-item, route-stage and computational-node IDs. Never use titles, translated slugs or generated URLs as identity.
5. **Bilingual parity without double-counting.** Report language-specific page counts and language-independent concept counts separately. Offer an explicit logical-content grouping when comparing translated counterparts.
6. **Provenance and explainability.** Every non-trivial result should expose the records and edges that support it, its scope, and any limitations.
7. **Read-only by default.** Query and audit tools do not mutate canonical metadata. Recommendations require human review and an explicit authoring workflow.
8. **Bounded complexity.** Start with Python, YAML, existing validators and deterministic JSON/Markdown reports. Do not add a database, graph server or new dependency without measured need.
9. **Full validation remains the correctness oracle.** Incremental checks may improve feedback time but must not silently replace repository-wide validation.
10. **No false completeness.** Missing associations are findings only where a contract or reviewed coverage expectation says they are required. Optional resources and intentionally partial registries remain valid.

## 3. Canonical inputs and boundaries

The index should compose existing readers and validators rather than parse every format independently.

| Entity/fact | Canonical owner | PIL use | Boundary |
|---|---|---|---|
| Page content and identity | `site/**/*.qmd`, `LLM-LAB-PAGE-MAP v1` | Published/planned inventory, page metadata and page graph | Body text is not copied into a second content store |
| Controlled page tags | Page-map tags and Quarto `keywords` | Facets: type, destination, topic, level, language, status | Tags do not identify scientific concepts |
| Understand route | `data/guided-route.yml` | Canonical stages, core/optional page membership and transitions | Not inferred from sidebar order or suggested page links |
| Build path | `docs/learning-path.md` and its referenced implementation/test evidence | Milestones, dependencies, evidence and implementation status | Not conflated with Understand |
| Concepts and semantic relations | `data/concepts.yml` | Concept inventory, domain membership, typed relations and explicit page associations | Do not infer concepts from headings or tag overlap |
| Domains | `data/domains.yml` | Domain-level aggregation | Page primary domain and many-to-many concept membership differ |
| Non-page resources | `data/resources.yml` | Resource inventory and concept/page associations | Do not reinterpret `concepts[].resources` page IDs as resource IDs |
| Computational model | `data/computational-graph.yml` | Node/edge queries and page/resource bridges where explicit | Computational dataflow is not pedagogy |
| Sources and evidence | `data/sources.yml`, `data/extractions/`, source-lineage records as migrated | Source coverage and evidence traceability | A citation or shared source does not prove a concept relation |
| Experiments and code | Existing `experiments/`, `src/`, `tests/` and report artifacts | Explicit implementation/evaluation evidence where registered or mapped | File proximity is not an association |
| Historical model | `data/history-pilot.yml` | Historical events and explicitly linked concepts/sources | Chronology does not imply influence |
| Generated projections | Learning-map JSON, JSON-LD and rendered artifacts | Optional consistency/freshness checks | Generated files are never canonical input when source exists |

### 3.1 Distinguish page counts from logical learning objects

A French and English page are two published page records but may represent one bilingual teaching object. Reports should expose both values where relevant:

- `page_records`: actual published page IDs;
- `logical_topics`: distinct controlled topic IDs or an explicitly reviewed page-pair grouping;
- `concepts`: unique canonical concept IDs;
- `route_memberships`: membership occurrences, not unique pages;
- `relations`: unique stored edges according to each registry's storage convention.

Never sum route memberships and call the result a page count. A page may occur in more than one view or stage if the route contract permits it.

### 3.2 Page type and route membership are separate dimensions

A page tagged `destination:understand` is not automatically a core Understand-route lesson. A Build page is not automatically a completed Build milestone. The route and milestone sources determine membership and status; page metadata supplies the linked page identity and editorial facets.

## 4. Logical architecture

The layer has five responsibilities, not five new services:

1. **Adapters:** reuse existing page, concept, domain, resource, route, computational graph and source readers. Each adapter retains source path, schema version and record identity.
2. **Normalized read model:** a short-lived in-memory `ProjectIndex` with typed entity records and relation-family-specific adjacency indexes.
3. **Query API:** stable functions for filtering, aggregation, forward/reverse traversal, route inspection, coverage and impact analysis.
4. **Diagnostics and recommendations:** deterministic audit rules first; optional explainable candidate generation second.
5. **Projections:** JSON for automation, Markdown/CSV for review, and optional site/dashboard views generated from the same query results.

The index is built from the current checkout and is not persisted as canonical data. A generated snapshot may be cached later, but it must include the source commit SHA, schema versions, build timestamp, input fingerprints and tool version. A stale snapshot must be detectable and never silently presented as current.

## 5. Proposed Python API

Initial read-model module: `site/tools/project_index.py`. Keep the existing `ProjectIndex` as the shared in-memory adapter; add a separate facade only if a concrete API need emerges.

The API should be typed, documented, deterministic, and usable from tests, command-line commands and other repository scripts.

```python
index = ProjectIndex.build(root=ROOT)

# Inventory and aggregation
index.stats()
index.pages(destination="understand", language="fr")
index.pages(type="concept-lesson", topic="attention")
index.route("understand")
index.route("build")
index.concepts(domain="architectures-mechanisms")

# Identity and associations
index.page("en/scaled-dot-product-attention")
index.concept("attention")
index.pages_for_concept("attention")
index.concepts_for_page("en/scaled-dot-product-attention")
index.resources_for_concept("attention")
index.sources_for_concept("attention")  # explicit catalogue/extraction links only

# Page relation queries
index.incoming_pages("en/attention", relation="related")
index.outgoing_pages("en/attention", relation="suggested_route")
index.incoming("page:en/attention", relation_family="page")
index.outgoing("concept:attention", relation_family="concept")

# Coverage and impact
index.concept_coverage()
index.route_coverage("understand")
index.page_impact("en/attention")
index.audit()
```

Exact signatures and return types must be decided against the real schemas during implementation. The example is an API design, not a claim that these functions already exist.

### 5.1 Typed records and edge families

A query result should carry typed references rather than flatten every relationship into a generic edge. At minimum, distinguish:

- `PageRouteEdge`: suggested previous/next navigation;
- `PageHierarchyEdge`: reciprocal parent/child hierarchy;
- `RelatedPageEdge`: non-hierarchical page association;
- `ConceptRelation`: typed concept-to-concept semantic relation;
- `ConceptDomainMembership`: classification association;
- `ConceptPageAssociation`: explicit concept-to-page association;
- `ResourceRecord`: a first-class non-page record from `data/resources.yml`;
- `ResourcePageAssociation` and `ResourceConceptAssociation`;
- `RevisionEdge`: a source page, revision role and typed target (`section`, `page` or `resource`);
- `GuidedRouteMembership`: stage, language and core/optional role;
- `BuildMilestoneEvidence`: explicit page/code/test/evidence mapping;
- `ComputationalEdge`: typed computation relation;
- `SourceEvidenceLink`: source/version, extraction item and locator where available;
- `HistoricalRelation`: history-model-specific relation.

Current read-model projection (PR #1394): `resources_by_id`, `page_resource_associations`, `concept_resource_associations`, `revision_status_by_page` and `revision_edges`. Revision edges remain separate from page graph edges. The revision adapter consumes the optional proposal documented in [revision-resource-contract.md](revision-resource-contract.md); no current page declares a revision object, and neither page nor resource validator has been changed. Reverse resource/revision lookup methods are the next implementation step.

Cross-structure traversal composes these typed links. It does not materialize a replacement universal graph or reinterpret the edge types of one graph as another.

### 5.2 Forward and reverse lookup

Provide generic `incoming(ref, family, type)` and `outgoing(ref, family, type)` only as dispatchers over typed family-specific indexes. Keep explicit convenience methods such as `incoming_pages` for discoverability.

Every returned edge should include:
- family and relation type;
- source and target stable IDs;
- canonical owner/path;
- direction and symmetry/storage convention;
- evidence or rationale reference when the source model provides one.

Counts must state whether they count unique entities, unique stored edges, memberships or traversal paths. Symmetric relations stored once must not be doubled.

## 6. Index design and complexity

Build dictionaries and adjacency maps once per snapshot:

| Index | Key | Value |
|---|---|---|
| `pages_by_id` | page ID | page record |
| `pages_by_tag` | namespace/value | set of page IDs |
| `pages_by_type` / `pages_by_destination` | controlled value | set of page IDs |
| `pages_by_topic` / `pages_by_domain` | ID | set of page IDs |
| `concepts_by_id` | concept ID | concept record |
| `pages_by_concept` | concept ID | set of page IDs |
| `concepts_by_page` | page ID | set of concept IDs |
| `resources_by_id` | resource ID | `ResourceRecord` |
| `page_resource_associations` | page ID | explicit page→resource associations |
| `concept_resource_associations` | concept ID | explicit resource↔concept associations |
| `revision_status_by_page` | page ID | `not_assessed`, `assessed` or `not_applicable` |
| `revision_edges` | source page ID | typed page→section/page/resource revision edges |
| `resources_by_concept` | concept ID | reverse index planned in the next query slice |
| `pages_by_route_stage` | stage ID + language + role | ordered page IDs |
| `page_incoming` / `page_outgoing` | page ID | typed page edges |
| `concept_incoming` / `concept_outgoing` | concept ID | typed concept relations |
| `computational_adjacency` | node ID | typed computational edges |

For (V) entities and (E) explicit relations, index construction should be approximately (O(V+E)) after source parsing. A direct lookup should be expected (O(1)) average; retrieving a neighborhood should be (O(k)) in the number of returned edges; a filtered aggregation should iterate the smallest relevant candidate set where practical.

Do not optimize prematurely. Measure parse, normalization, index build, query and serialization separately. A single build per command or test session is preferable to rebuilding for every metric.

### 6.1 Incremental operation

Initial implementation: full deterministic in-memory rebuild. This is simpler and is the reference behavior.

Later, if profiling demonstrates a material bottleneck, add an optional incremental cache keyed by:
- source file path and content hash;
- parser/adapter version;
- schema version;
- dependency IDs affected by the changed record.

Invalidation must follow explicit references and affected neighborhoods. Full rebuild and full validation remain available as correctness checks. Never use modification time alone as a reliable content identity.

## 7. Query and reporting catalogue

### 7.1 Inventory and counts

Required first-class dimensions:

- pages by publication status, language, destination, type, level, topic and domain;
- Understand route stages, ordered core pages and optional pages, by language;
- Build milestones, prerequisites, referenced pages and evidence status;
- concepts by domain and importance;
- concept relations by type/family;
- resources by kind/status/language;
- source and extraction counts, with catalogue-to-extraction reconciliation;
- computational nodes/edges by kind, branch and relation type;
- experiments/tests/code artifacts only where an explicit registry or reviewed mapping defines their role.

Each report should include the filter, counting unit, exclusions and snapshot commit.

### 7.2 Coverage matrix

A concept coverage report should separate dimensions instead of collapsing them into a single opaque score:

| Dimension | Evidence of coverage |
|---|---|
| Canonical definition | Concept record has reviewed bilingual labels/definitions |
| Teaching pages | Explicit concept-to-page association |
| Understand | Associated page is a core or optional member of a canonical stage |
| Build | Explicit milestone/page/evidence mapping |
| Computation | Explicit bridge to a computational node |
| Resources | Explicit first-class resource association |
| Sources | Explicit concept IDs in source catalogue/extraction records |
| Practice | Explicit exercise/test/experiment mapping |
| Bilingual parity | Expected FR/EN counterparts exist and satisfy page contracts |

Use states such as `present`, `missing`, `not_applicable`, `not_registered` and `needs_review`. Do not interpret an absent association as a defect if no completeness contract exists. The report must identify which dimensions are fully enumerable today and which await an explicit mapping. The canonical metric IDs, units, source versions and state semantics are defined in [project-metric-registry.md](project-metric-registry.md).

### 7.3 Page and entity impact analysis

For a page or concept, return direct incoming/outgoing links and bounded typed paths to related structures. An impact report should distinguish:
- direct references;
- route membership;
- concept associations;
- resources and source evidence;
- generated projections likely to change;
- tests/validators that cover the contract.

Impact analysis is a review aid, not a claim that every transitive neighbor must be edited.

## 8. Diagnostics and recommendation engine

### 8.1 Deterministic rules

Start with auditable rules:
- dangling page/concept/resource/source references;
- duplicate IDs and invalid controlled values (normally caught by owning validators);
- inconsistent FR/EN page structure or missing expected counterpart;
- route references to missing/unpublished/unrendered pages;
- orphan pages or concepts, with explicit exclusions for valid reference/experimental material;
- concepts with no associated teaching page;
- route pages with no explicit concept associations, reported as an inventory rather than an automatic error;
- unused controlled tags/domains and unexpectedly empty categories;
- inconsistent relation direction, reciprocity or duplicate storage;
- stale generated outputs;
- ambiguous or conflicting page ownership candidates.

The PIL should call the owning validators where possible and add only cross-registry checks not already owned elsewhere. Do not duplicate every validator in one new monolith.

### 8.2 Explainable candidate recommendations

Candidate rules may use:
- missing explicit associations;
- route-stage coverage gaps;
- repeated reviewed concepts in source extractions without a canonical page;
- a concept with many linked pages but no synthesis/revision resource;
- an implementation milestone without linked code/tests/evidence;
- a page with incoming references but no outgoing discovery path;
- candidate bilingual gaps;
- possible duplicate pages or concepts.

Each candidate must contain:
- proposed action and target entity IDs;
- reason and measurable signal;
- supporting canonical records and paths;
- confidence or rule class, not a misleading precision number;
- known counter-evidence and limitations;
- review state: `candidate`, `accepted`, `rejected`, `deferred`;
- optional issue/PR link.

A candidate must never automatically create a concept, edit a page map, add a relation, change a route or close an issue.

### 8.3 AI-assisted analysis

AI may summarize deterministic reports, compare page content, suggest possible concept mappings or propose a synthesis resource. It must return proposals with exact IDs and evidence references. Promotion requires human review and the relevant source-owner workflow.

Measure recommendation precision on a manually reviewed sample before treating suggestions as useful automation. Record rejected suggestions as evaluation evidence where appropriate; do not silently learn canonical truth from prior model output.

## 9. Command-line interface and output contracts

Proposed command family (names provisional):

```bash
# Global inventory and route counts
uv run python site/tools/project_intelligence.py stats
uv run python site/tools/project_intelligence.py routes

# Queries
uv run python site/tools/project_intelligence.py pages --destination understand --language fr
uv run python site/tools/project_intelligence.py concept attention
uv run python site/tools/project_intelligence.py incoming page:en/attention
uv run python site/tools/project_intelligence.py coverage concepts

# Diagnostics and impact
uv run python site/tools/project_intelligence.py audit
uv run python site/tools/project_intelligence.py impact page:en/attention

# Machine-readable output
uv run python site/tools/project_intelligence.py stats --format json
uv run python site/tools/project_intelligence.py coverage concepts --format csv
```

Output contracts:
- stable JSON keys and explicit schema version;
- deterministic ordering (IDs, then canonical order where order is pedagogically meaningful);
- no timestamps in deterministic content unless supplied as snapshot metadata;
- Markdown summary for human review;
- CSV only for flat tabular exports;
- non-zero exit status for command failure or configured blocking diagnostics, not for every informational gap.

The CLI should reuse the same API and result models as tests and other scripts. Avoid a second implementation hidden in argument handlers.

## 10. Testing, CI and evidence

Required tests:
1. Synthetic fixtures for each entity and edge family, including bilingual pairs, shared pages and optional route membership.
2. Forward/reverse symmetry for each directed relation family and the documented single-storage behavior for symmetric relations.
3. Counting semantics: unique pages vs route memberships vs logical topics vs concepts.
4. No false inference from matching tags, headings, titles, page order, citations or shared domains.
5. Dangling references and intentionally optional/missing associations.
6. Deterministic output across repeated builds and filesystem enumeration order.
7. Impact analysis with bounded traversal and cycle-safe behavior.
8. Cache invalidation equivalence to a full rebuild if/when caching is added.
9. CLI JSON/Markdown/CSV schema and exit codes.
10. Scale fixtures at increasing page/concept/relation/source counts, with separate timing and memory measurements.

CI integration should be staged:
- first run focused unit tests and read-only CLI smoke tests;
- then add non-blocking report artifacts to CI;
- only promote diagnostics to blocking checks after false-positive review and explicit ownership;
- retain all current canonical validators and full-corpus integrity checks.

Record Python version, platform, dependency versions, fixture sizes, repetitions, medians and peak memory for benchmarks. Do not claim scale readiness from a static complexity argument alone.

## 11. Implementation roadmap

### Phase 0 — contract and inventory
- Map every required metric to its canonical source and precise counting semantics.
- Inventory existing readers, validators, tests and generated projections.
- Identify already-covered checks to avoid duplication.
- Establish representative fixtures and a baseline snapshot.

**Exit:** query catalogue, ownership map and test plan reviewed.

### Phase 1 — deterministic read model
- Build typed adapters on existing readers.
- Implement `ProjectIndex` and first-pass dictionaries/adjacency indexes.
- Add page, concept, domain, resource and Understand route queries.
- Add stats and reverse page lookups.

**Exit:** required page/lesson/concept counts and page/concept reverse queries are reproducible and tested.

### Phase 2 — Build and cross-structure coverage
- Add Build milestones and explicit code/test evidence mappings.
- Add source/extraction, computational graph and history adapters where canonical IDs permit.
- Implement coverage matrices and entity impact reports.

**Exit:** reports distinguish complete, partial, unregistered and inapplicable dimensions.

### Phase 3 — diagnostics and useful projections
- Add deterministic cross-registry audits.
- Add stable JSON/Markdown/CSV CLI outputs.
- Publish CI artifacts and review false positives before enforcing new rules.

**Exit:** maintainers can inspect and reproduce project-wide findings without bespoke scripts.

### Phase 4 — explainable recommendations
- Add candidate rules and human review states.
- Evaluate against manually reviewed examples.
- Introduce AI assistance only as a proposal generator with evidence paths.

**Exit:** recommendation precision and limitations are documented; no autonomous canonical mutations.

### Phase 5 — measured scale and incremental operation
- Benchmark realistic and synthetic growth.
- Profile parse, index, query and export costs separately.
- Add incremental caching only where measurements justify it.
- Keep full rebuild as reference and fallback.

**Exit:** scale claims are supported by reproducible benchmarks and cache/full-rebuild equivalence tests.

## 12. Non-goals and safeguards

- No second page, concept, source, resource, route or relation registry.
- No generic universal graph that erases relation-family semantics.
- No inference of concepts from tags/headings or semantic relations from co-occurrence.
- No inference of prerequisites from page order, suggested navigation or computational dataflow.
- No forced completeness for optional resources, experiments or references.
- No automatic page/concept/resource creation or metadata mutation.
- No graph database, search service or external dependency before a measured requirement.
- No public dashboard before stable metric definitions and accessibility/text alternatives exist.
- No single opaque project-quality score.

## 13. Initial acceptance criteria

The first implementation slice is complete only when it can:

1. Report published page counts by language, destination, type and status.
2. Report canonical Understand stages and core/optional page counts separately.
3. Report Build milestones and lesson counts from their actual canonical owner, without guessing from page tags.
4. Report unique concept counts and concept counts by domain/importance.
5. Return all explicitly associated pages for a concept and all concepts explicitly associated with a page.
6. Return incoming and outgoing page relations by relation type.
7. Distinguish page records, logical bilingual topics, route memberships, concepts and relation counts.
8. Produce deterministic machine-readable output with source commit and counting semantics.
9. Demonstrate through tests that tags, headings, co-occurrence and navigation order are not silently promoted to semantic relations.
10. Document which coverage dimensions are currently queryable and which require a separate explicit mapping.

This design complements [issue #1233](https://github.com/JM-Brun/llm-lab/issues/1233): the PIL provides a general, reusable project inventory/query foundation, while #1233 owns evidence-aware cross-domain discovery, typed bridges and decision traceability. The implementation should coordinate with #1233 and related graph/source issues rather than duplicate their work.
