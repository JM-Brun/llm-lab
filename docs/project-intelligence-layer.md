# Project intelligence layer

**Status:** partial implementation, reconciled against main on 2026-11-23. The read-only `ProjectIndex`, page/concept/domain/resource/route indexes, page-based revision relations and reverse lookups are implemented. The concept-centred coverage matrix and Markdown/JSON report are implemented. An opt-in source/computation/route-focus evidence projection and concept-centred `cross_graph_query.py` are implemented and tested (PR #1535). Complete Build/computation/source/Practice coverage mappings, cross-family diagnostics, history/decision traversal, a unified CLI and recommendations remain incomplete.  
**Scope:** reusable, deterministic queries and explainable diagnostics over the canonical LLM Lab metadata, registries, routes, graph families and project artifacts.  
**Related architecture:** [Information architecture](information-architecture.md), [scalability audit](scalability-capacity-audit-2026-11-18.md), [knowledge-graph implementation audit](knowledge-graph-implementation-audit.md), [cross-graph discovery issue #1233](https://github.com/JM-Brun/llm-lab/issues/1233).

## 1. Purpose

LLM Lab should be able to inspect and reason about its own structure through documented, reusable tools. Metadata must be more than passive annotations: it should support reliable inventories, counts, reverse lookups, coverage analysis, consistency checks, impact analysis and carefully governed construction recommendations.

The **Project Intelligence Layer (PIL)** is a read-only query and analysis layer over existing canonical sources. Its implemented subset is not a new registry, ontology, curriculum, graph, database or source of truth. Keep the implemented read model distinct from the broader target described in the remaining sections.

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

## 1.1 Verified implementation state — 2026-11-23

| Component | Implemented behavior | Current limit |
|---|---|---|
| Default read model | `ProjectIndex.build(root)` joins published pages, concepts/domains, page relations, guided-route memberships, non-page implementation resources and page-based revision relations. It exposes deterministic statistics and forward/reverse queries. | It is an in-memory read model, not a canonical store. Planned/retired pages are excluded. |
| Revision adapter | Page-based `revision_role`, `revision_of` and `revision_support` are validated by ProjectIndex; aid→lesson and lesson→aid indexes are derived. CI invokes `audit_revision_coverage.py`. | Non-page revision aids are unsupported. Coverage states are authored assessments, not learner-validation results. |
| Concept coverage | `project_coverage.py` builds a concept-centred matrix with explicit evidence and state counts; `report_project_index.py` renders Markdown or JSON with snapshot provenance and units. | Build, computation, source and Practice dimensions are currently `not_registered` in this matrix because complete canonical concept mappings do not exist. This does not mean that no isolated cross-graph paths exist. |
| Evidence projection | `ProjectIndex.build(root, include_evidence=True)` opts into source/extraction, computational and route-focus evidence adapters. | The default index remains lightweight; evidence loading is opt-in. |
| Cross-graph query | `cross_graph_query.py --concept ID` returns typed paths and explicit gaps for item-level source evidence, catalogue-only gaps, page-mediated and stage-mediated computation, Practice links and non-page resources. | Concept-centred only. It does not yet traverse history, Build milestone dependencies, source-local pedagogical graphs or structured decision records; it is not a reverse page-originating evidence query or recommendation engine. |
| Validation | ProjectIndex, coverage and query behavior have synthetic regression tests; PR #1535 adds five real concept cases and explicit gap checks. | There is no complete cross-family validator or project-wide deterministic diagnostic suite. Existing owning validators remain authoritative. |

The current coverage vocabulary includes `present`, `missing`, `not_applicable`, `not_registered`, `needs_review` and `not_assessed` (the latter for revision assessment). A distinct `stale` state is not yet implemented. The matrix does not currently model all five states for every dimension.

**Counting boundary:** the report distinguishes published page records, unique topics, concepts, domains, stored page edges, route memberships and revision links. Do not add these counts together or interpret a missing matrix dimension as proof that no underlying record exists.

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

## 5. Python API: implemented core and proposed extensions

The shared in-memory adapter is `site/tools/project_index.py`. Use its existing typed queries rather than adding a second facade.

Implemented default-index calls include:

~~~python
index = ProjectIndex.build(root=ROOT)

index.stats()
index.select_pages(language="fr", destination="understand")
index.select_concepts(domain="architectures-mechanisms")
index.pages_for_concept("attention")
index.concepts_for_page("en/attention")
index.resources_for_page("en/attention")
index.pages_for_resource("attention-module")
index.resources_for_concept("attention")
index.concepts_for_resource("attention-module")
index.incoming_pages("en/attention")
index.outgoing_pages("en/attention")
index.route_stage("computation", language="en", role="core")
index.revision_aids_for_lesson("en/queries-keys-values")
index.lessons_for_revision_aid("en/revision-queries-keys-values")
index.revision_support_for_lesson("en/queries-keys-values")
~~~

The larger evidence projection is opt-in:

~~~python
index = ProjectIndex.build(root=ROOT, include_evidence=True)
result = query_concept(index, "attention")
~~~

Do not assume that convenience methods such as generic `incoming()`, `page_impact()`, `audit()`, `route_coverage()` or a unified `project_intelligence.py` CLI exist; they remain possible future interfaces, not current APIs.

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

Current read-model projection: `resources_by_id`, page/resource and concept/resource associations, `revision_support_by_page`, page-based `revision_edges`, and derived `revision_aids_by_lesson` / `revision_lessons_by_aid`. Revision edges remain separate from ordinary page-graph edges. Page-based revision declarations are present and validated through ProjectIndex; the CI revision inventory exercises those checks. Non-page revision aids remain unsupported. The general page-metadata validator does not duplicate revision semantics.

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
| `revision_support_by_page` | lesson page ID | explicit assessment status, evidence anchors and rationale |
| `revision_edges` | revision-aid page ID | typed page-aid→eligible lesson relations |
| `revision_aids_by_lesson` / `revision_lessons_by_aid` | lesson or aid page ID | derived reverse/forward indexes; no reciprocal duplicate authoring |
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

The current implementation uses `present`, `missing`, `not_applicable`, `not_registered` and `needs_review`; revision coverage additionally uses `not_assessed`. It does not yet implement a general `stale` state. Build, computation, source and Practice cells are explicitly `not_registered` in the current concept matrix because no complete canonical concept mapping exists for those dimensions. The opt-in cross-graph query may still return individual explicit paths; those paths must not be promoted into complete coverage. Do not interpret an absent association as a defect if no completeness contract exists. The canonical metric IDs, units, source versions and state semantics are defined in [project-metric-registry.md](project-metric-registry.md).

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

Current command-line entry points (the earlier unified command family below is not implemented):

~~~bash
# Lightweight project counts and concept-centred coverage (Markdown by default)
uv run python site/tools/report_project_index.py
uv run python site/tools/report_project_index.py --format json
uv run python site/tools/report_project_index.py --language fr --destination understand

# Opt-in evidence paths and explicit gaps for one or more concepts
uv run python site/tools/cross_graph_query.py --concept attention
uv run python site/tools/cross_graph_query.py --concept attention --concept entropy
~~~


Output contracts:
- stable JSON keys and explicit schema version;
- deterministic ordering (IDs, then canonical order where order is pedagogically meaningful);
- no timestamps in deterministic content unless supplied as snapshot metadata;
- Markdown summary for human review;
- CSV only for flat tabular exports;
- non-zero exit status for command failure or configured blocking diagnostics, not for every informational gap.

`report_project_index.py` currently emits Markdown or JSON; `cross_graph_query.py` emits typed JSON paths/gaps. There is no CSV output or unified command dispatcher yet. Any future CLI should reuse the same API and result models as tests and other scripts.

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

## 11. Implementation roadmap — reconciled 2026-11-23

### Phase 0 — contract and inventory
- [x] Map the current read model to canonical owners and existing validators.
- [x] Establish typed identity/edge families and count units for the implemented subset.
- [x] Add synthetic fixtures and regression tests for index integrity.
- [ ] Refresh the complete registry inventory and full-corpus evidence snapshot as the source corpus changes.

**Status:** implemented for the current ProjectIndex subset; broader ownership/metric inventory continues in the architecture backlog.

### Phase 1 — deterministic read model
- [x] Implement `ProjectIndex` with page, concept, domain, resource, route, page-edge and revision adapters.
- [x] Add deterministic statistics and page/concept/resource/revision forward and reverse queries.
- [x] Add a lightweight default index and opt-in evidence projection.
- [x] Add synthetic tests and CI revision-inventory integration.

**Status:** implemented for the current canonical owners; do not add a second index or duplicate validator.

### Phase 2 — Build and cross-structure coverage
- [x] Add the concept-centred coverage matrix and Markdown/JSON report.
- [x] Add opt-in source/extraction, computational and route-focus evidence adapters; test concept-centred paths and explicit gaps (PR #1535).
- [ ] Define a canonical Build milestone/evidence crosswalk.
- [ ] Define complete concept-to-computation, source-evidence and Practice mappings only where the owning model can justify them.
- [ ] Add history traversal and broader entity-impact queries.

**Status:** partial. The matrix reports Build/computation/source/Practice as `not_registered`; isolated explicit paths do not imply complete coverage.

### Phase 3 — diagnostics and useful projections
- [x] Report structural bilingual association findings and explicit evidence gaps in the current query output.
- [ ] Define cross-registry diagnostic rules and ownership so existing validators are reused rather than duplicated.
- [ ] Add a general stale-state/freshness model and report provenance for all projections.
- [ ] Decide which reports should be CI artifacts and review false positives before making any finding blocking.
- [ ] Add a unified, stable CLI only if multiple consumers justify it.

**Status:** not complete; current diagnostics are bounded to bilingual association findings and concept-centred evidence gaps.

### Phase 4 — explainable recommendations
- [ ] Defer until deterministic diagnostics and coverage states are stable.
- [ ] If justified, evaluate candidates against a manually reviewed sample and preserve counter-evidence.
- [ ] Keep AI assistance proposal-only with exact IDs and evidence paths.

**Status:** not started; no recommendation engine is implemented or currently required.

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
