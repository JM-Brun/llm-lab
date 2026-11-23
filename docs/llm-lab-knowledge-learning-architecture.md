# LLM Lab knowledge and learning ecosystem architecture

**Status:** architectural synthesis and target contract  
**Date:** 2026-11-23  
**Scope:** shared knowledge foundation, specialized learning systems, graph interoperability, reader-facing experiences and editorial projects.

**Parent documents:** [Information architecture](information-architecture.md), [Knowledge architecture interoperability](knowledge-architecture-interoperability.md), [Knowledge graph standards](knowledge-graph-standards.md), [Project intelligence layer](project-intelligence-layer.md).

This document explains how the repository's existing systems fit together. It is an architecture-level map, not a replacement for specialized schemas and contracts. Where implementation is incomplete, the document says so rather than treating the target design as implemented.

## 1. Product definition

LLM Lab is a bilingual, self-contained learning and experimentation environment about large language models. It combines several complementary products:

1. **Understand:** a curated learning journey synthesizing strong existing explanations and sources.
2. **Review:** a system for consolidating and retrieving knowledge through summaries, revision sheets, flashcards, visual recall and self-assessment.
3. **Practice & experiment:** a growing collection of questions, exercises, coding tasks and controlled experiments.
4. **Build:** an implementation-oriented path for inspecting, testing and progressively constructing a small LLM.
5. **Deepen:** a non-linear knowledge wiki for mathematical, scientific, architectural and research-level extensions.
6. **Editorial projects:** independent collections such as seasonal/advent calendars, potentially recurring with new editions and themes.

These are distinct learner experiences over a shared knowledge foundation. They are not six names for the same curriculum, and they should not be forced into one reading order.

The repository should remain useful as a book-like, independently navigable resource. No private repository or external service is a build-time or reading dependency.

## 2. Core architectural principle

Maintain **one canonical identity and one canonical owner for each kind of information**, then build specialized models and reader-facing projections over those records.

The architecture has three layers:

- **Shared knowledge foundation:** stable identities and reusable semantic records.
- **Specialized models:** pedagogical, revision, practice, build, computational, research and editorial structures that use those identities.
- **Experiences and projections:** Quarto pages, routes, maps, indexes, exercises, calendars, reports and interactive visualizations.

The layers are connected through stable IDs and explicitly typed relations. They are not connected by copying records, inferring relations from filenames, or treating every graph edge as equivalent.

## 3. Shared knowledge foundation

The shared foundation provides reusable referents. It does not own every activity or every sequence.

| Entity | Canonical identity / current owner | Responsibility |
|---|---|---|
| Concept or notion | concept_id, data/concepts.yml | Language-independent meaning, bilingual labels/definitions, aliases and typed semantic relations |
| Knowledge domain | domain_id, data/domains.yml | Controlled scientific classification; concepts may belong to multiple domains |
| Published page | page_id, LLM-LAB-PAGE-MAP v1 | Stable page identity, editorial metadata, language, purpose and page-level relations |
| Non-page resource | resource_id, data/resources.yml | Independently identified artifacts such as implementation modules |
| External source | source_id, source catalogue | Source identity, version and discovery metadata |
| Extracted claim/evidence | extraction records and source-lineage model | Traceable statements, supporting material and integration candidates |
| Activity | target: stable activity_id | A question, exercise, coding task, experiment or assessment; not a concept or lesson |
| Collection / edition | target: stable collection and edition IDs | An editorially bounded collection, such as one annual calendar edition |

The final two entities are target capabilities, not claims about existing canonical registries. Introduce them only with a schema and real content use case.

### Identity and ownership rules

- A concept is not the page that explains it.
- A page is not a resource artifact merely because it links to code.
- A question is not a concept; it is an activity that can assess or use concepts.
- A domain is not a page section, destination or calendar theme.
- A source is not an extracted claim, and neither is a canonical concept.
- Translations share underlying page topic/concept identity where appropriate; language variants do not create duplicate concepts.
- Every field and relation has one authoritative authoring location. Other files may contain generated or validated projections, not competing copies.

## 4. Specialized models and learner experiences

### 4.1 Understand — guided conceptual learning

**Purpose:** develop a coherent mental model of LLMs through a curated, pedagogically justified progression.

Owns learning objectives, expected outcomes, recommended stage order, transitions, explicit learning prerequisites where justified, lesson membership and route-level status.

Canonical route: data/guided-route.yml, with page identities and metadata in the existing page map. The route is not the knowledge graph, page hierarchy or implementation dependency graph.

### 4.2 Review — retrieval and consolidation

**Purpose:** help learners reconstruct, retain and check knowledge already introduced.

Resource roles may include synthesis/summary, revision sheet, flashcard/active-recall prompt, visual reconstruction, retrieval question and self-assessment.

The canonical relation is an explicit aid-to-supported-lesson relation. One aid may support several lessons; one lesson may have several aids. Reverse lesson-to-aid views should be generated. Coverage sufficiency is a separate assessment from link existence. Missing assessment metadata means **not assessed**, not **no support**.

The proposed contract in [revision-resource-contract.md](revision-resource-contract.md) is the starting point; its status and implementation must be reconciled before it is treated as a fully enforced schema.

Review is not a duplicate copy of Understand. It is a different activity over the same concepts and lessons.

### 4.3 Practice & experiment — application and transfer

**Purpose:** move from recognition to problem solving, reconstruction, implementation and experimental reasoning.

Potential activity kinds include conceptual/retrieval questions, mathematical derivations and calculations, tensor-shape and mechanism reconstruction, programming/debugging exercises, controlled numerical experiments and transfer tasks/mini-projects.

An activity can reference several concepts, lessons, skills and (where relevant) implementation resources. Keep its own identity, prompt, expected evidence, hints, solution, difficulty and validation separate from the concepts it uses.

The established editorial decision is to keep substantial exercises/questions on dedicated practice pages rather than growing main lesson pages. Lessons may link to the corresponding practice resource. The exact activity registry and graph are not yet a complete canonical system.

### 4.4 Build — implementation and verification

**Purpose:** inspect, implement, test and explain a small model and its components.

Owns implementation milestones and dependencies, code modules and stable resource identities, tensor contracts/interfaces/invariants, tests and observable outputs, reproducibility evidence and implementation status/limitations.

Build dependencies are not automatically conceptual prerequisites. A component may be required by the implementation while its underlying mathematics is taught earlier, later or in an optional deep dive.

Existing foundations include the guided-build pages, docs/learning-path.md and data/resources.yml. The resource registry is currently a narrow seed centered on implementation modules; do not assume all code, tests, experiments and datasets are already first-class resources.

### 4.5 Deepen — non-linear knowledge wiki

**Purpose:** explain advanced and adjacent ideas beyond the minimum mental model needed for the core route.

May contain mathematical derivations, alternative architectures, assumptions, limitations, research findings, comparisons, historical context and interdisciplinary connections.

Deepen is organized for discovery by question/domain, not as a second mandatory curriculum. Its page-level primary discovery domain must not be confused with multi-valued concept membership in data/domains.yml.

### 4.6 Editorial collections — calendars and future projects

**Purpose:** provide a bounded editorial experience with its own theme, format, selection and navigation.

A calendar edition should own collection/edition identity, dates and editorial brief, story/article membership and local ordering/grouping, article-specific learning intent, sources and review state, and optional links to canonical concepts, pages, activities and computational nodes.

The edition must not copy canonical concept definitions or become a weaker parallel Understand route. A story may be independently readable and still connect to several shared concepts. Future annual editions should reuse the collection model and shared foundation without sharing a single editorial sequence.

The 2026 redesign decision in [advent-calendar-editorial-redesign.md](advent-calendar-editorial-redesign.md) defines independent scientific stories. [advent-calendar-next-steps.md](advent-calendar-next-steps.md) remains the operational handoff; its implementation checklist must be kept current.

## 5. Graph families: specialized semantics, shared identities

LLM Lab should have an ecosystem of interoperable graph families, not one universal graph with ambiguous edges. These are semantic models/projections; they do not each require a separate graph database or runtime.

| Graph family | Nodes and edges | Canonical basis / status |
|---|---|---|
| Semantic knowledge graph | Concepts, domains and typed conceptual relations | data/concepts.yml, data/domains.yml; implemented seed and validators |
| Page/navigation graph | Published pages; route, hierarchy and related-page edges | Page-map metadata; generated bilingual learning-map projection |
| Pedagogical route graph | Lessons/stages; recommended order and justified learning prerequisites | data/guided-route.yml, docs/learning-path.md; separate from concept relations |
| Revision relations | Page-based aids → lessons; typed role and separate lesson coverage assessment | `ProjectIndex` validates page-aid relations and assessments; `audit_revision_coverage.py` derives both directions and runs in CI. Non-page revision aids remain unsupported. See the revision-resource contract. |
| Review route | A reader-facing projection of the same nine-stage curriculum, using primary synthesis destinations and revision aids | `guided-route.yml` + `lesson_contracts`; generated bilingual review plan and peer sidebar (PR #1549). Optional revision stops, complete flashcard inventory and manual rendered/learner review remain incomplete. |
| Practice graph | Per-lesson exercise hubs, shared collections and anchored activities; page-level lesson associations | 45 exercise pages per language are catalogued/rendered. The Q/K/V activity pilot (PR #1558, merged after Python, Quarto/browser and secret-scan success) validates bilingual `page_id#anchor` identities and lesson→hub→collection navigation. Its 120-case browser audit checks the nested FR/EN hub at desktop/mobile, including links and keyboard disclosure. Learner validation and the complete 45-pair audit remain open; no global activity registry or complete per-activity concept mapping is established. |
| Build dependency graph | G0–G9 implementation milestones, modules, code evidence and verification dependencies | docs/learning-path.md, implementation modules and data/resources.yml. Resource/code validators exist, but no single canonical cross-graph Build dependency validator is established. |
| Computational graph | Operations, state/data artifacts and typed computational flow | `data/computational-graph.yml`; `check_computational_graph.py` and tests/site/test_computational_graph.py; opt-in ProjectIndex evidence adapter. The shared-spine design issue #575 is closed; remaining manual screen-reader/rendered-content review is tracked in #584. |
| Source/provenance graph | Source records, scan/integration status, extraction items, locators and evidence mappings | `check_source_catalogue.py`; opt-in `cross_graph_evidence.py` adapter and `cross_graph_query.py`. Main/source-coverage snapshot recorded in #1306 (2026-11-21): 142 source records, 100 extraction files and 520 atomic items; 42 catalogue IDs have no matching extraction filename and there are zero orphan filenames. There are 44 explicit collection decisions (42 non-empty, 2 empty) and 98 undecided. The 489-item count belongs to the earlier 96-file snapshot and is superseded. A current 100-file locator-quality audit remains separate. |
| Editorial graph | Collections, editions, stories and editorial membership/order | The independent-story redesign and Day 06 FR/EN story/template are merged (PRs #1551 and #1560); the spectral-bias revision and mathematical notation corrections are merged (PRs #1562 and #1563). The pages remain `planned` and outside the render list; Quarto/visual/accessibility/novice validation remains open. No generalized manifest or membership validator exists. |
| Historical graph | Events, sources, dated evidence and historical relations | data/history-pilot.yml; check_history_pilot.py, render_history_pilot.py and rendered timeline checks. Not yet traversed by cross_graph_query.py. |

Not every family needs an independently persisted graph file. A graph can be a deterministic projection from a canonical route, resource registry or relationship declaration.

### Relation semantics

Every relation must document source and target entity kinds, direction and verbal reading, family/purpose, symmetry/inverse policy, transitivity (default: not transitive), cycle/cardinality constraints where justified, evidence/rationale requirements, and whether it is eligible to influence learning order.

Never infer:
- a prerequisite from page order, graph proximity or a link;
- a computational dependency from conceptual association;
- a concept relation from tag overlap;
- historical influence from chronology alone;
- revision support from a body link or topic match;
- editorial membership from shared theme tags.

## 6. Cross-cutting classifications and tags

Use controlled vocabularies by entity type, with shared governance and validation—not one undifferentiated tag field.

| Facet | Applies to | Example / owner |
|---|---|---|
| Editorial page type | Page | type, page metadata schema |
| Destination / experience | Page | understand, build, deepen, practice; review only where explicitly supported |
| Page topic key | Page | topic:<id>; page grouping key, not a concept entity |
| Page level/status/language | Page | Existing controlled page metadata |
| Scientific domain | Concept | domains in data/concepts.yml referencing data/domains.yml |
| Deepen discovery domain | Deepen page | Existing page-level primary domain; distinct from concept memberships |
| Source facets | Source | data/source-taxonomy.yml and source catalogue |
| Revision role | Revision aid | Controlled role from the revision contract |
| Activity kind/difficulty/status | Activity | Future activity schema |
| Editorial theme/format/status | Collection/story | Future editorial schema |

A common vocabulary registry or validation utility may be shared, but allowed values and meanings remain scoped to the owning entity. Do not add duplicate dimensions such as a second category, archetype or scientific_pattern without a demonstrated query/use case.

## 7. Interoperability contract

1. **Stable references:** use canonical IDs, never translated titles, filenames or rendered URLs as cross-system identity.
2. **Typed links:** declare which entity kinds a relation may connect.
3. **Single ownership:** store each fact once; derive inverse indexes and display views.
4. **No implicit inference:** tags, proximity, order and hyperlinks are not evidence of typed relations.
5. **Separate sufficiency from existence:** a link can exist while its pedagogical or evidential quality remains unassessed.
6. **Preserve provenance:** claims and imported material retain source identity, version and evidence links.
7. **Bilingual parity:** FR/EN projections preserve equivalent claims, qualifications and stable cross-language identity.
8. **Deterministic projections:** JSON, JSON-LD, learning maps and coverage reports are generated from canonical sources.
9. **Versioned change:** schema changes require migration, validator, tests, documentation and compatibility review.
10. **Bounded technology:** YAML + Python validation + generated JSON/Quarto are sufficient for the current static project. Do not introduce a database or graph platform without measured need.
11. **Accessible alternatives:** interactive graphs have textual/list equivalents and are not the only way to navigate.
12. **No per-concept automation:** use shared validators and a small number of meaningful workflows, not one CI workflow per concept.

## 8. Project-wide intelligence

The Project Intelligence Layer should query canonical systems through read-only adapters and explainable joins. It should not become another authoring database or silently repair metadata.

Useful diagnostics include concepts in Understand without a reviewed revision aid; lessons with no linked practice activity; concepts used by Build modules but lacking a suitable conceptual explanation; computational nodes with no mapped concept/page or implementation evidence; Deepen topics disconnected from the shared concept foundation; calendar stories that duplicate a canonical lesson without adding a distinct perspective; source claims not traceable to a synthesis or project artifact; bilingual parity gaps; stale, orphaned or multiply-owned resources.

A coverage matrix is a diagnostic projection, not an editorial quality score. The current concept matrix uses `present`, `missing`, `not_applicable`, `not_registered` and `needs_review`; revision coverage additionally uses `not_assessed`. A general `stale` state is not implemented, and `absent` is not a synonym for `not_registered`. Do not infer quality or sufficiency from a non-empty link.

## 9. Existing implementation map

The following foundations should be preserved and extended:

- docs/information-architecture.md: canonical ownership and metadata governance.
- docs/knowledge-architecture-interoperability.md: technology-neutral and cross-repository boundaries.
- data/concepts.yml, data/domains.yml: shared semantic foundation.
- LLM-LAB-PAGE-MAP v1: page identity and page graph.
- data/guided-route.yml, docs/learning-path.md: Understand route and implementation learning path.
- data/resources.yml: current non-page implementation resources.
- docs/revision-resource-contract.md: partially implemented page-based aid-to-lesson relations and lesson coverage assessments; non-page revision aids remain unsupported.
- data/computational-graph.yml, docs/canonical-computational-spine.md: computation model and branches.
- data/sources.yml, data/extractions/, source-lineage documentation: source ingestion and provenance.
- data/history-pilot.yml, docs/history-data-model.md: specialized historical model.
- docs/project-intelligence-layer.md: read-only project index and diagnostics direction.
- docs/advent-calendar-editorial-redesign.md, docs/advent-calendar-next-steps.md: 2026 editorial decision and handoff.

This inventory does not claim equivalent maturity or complete validation. See [the implementation backlog](llm-lab-architecture-implementation-backlog.md) for verified gaps and acceptance gates.

## 9.1 Validator and interoperability matrix

The canonical owner and its validator must be explicit. A cross-graph adapter may check references that span owners, but it does not replace the validator of either owner.

| Family | Canonical owner | Integrity validator / regression tests | Current projection or bridge | Explicit boundary |
|---|---|---|---|---|
| Concepts and domains | data/concepts.yml, data/domains.yml | site/tools/check_concept_registry.py; tests/knowledge/test_concept_registry.py | ProjectIndex, learning-map concept view, export_knowledge_graph.py | Snapshot at main `534ce3d` (2026-11-23): 102 concepts, 6 domains, 12 relation types and 114 typed concept edges. Typed concept relations and multi-domain membership; page tags are not concepts. |
| Page/navigation | LLM-LAB-PAGE-MAP v1 in site/**/*.qmd | site/tools/check_page_metadata.py | page_index.py, ProjectIndex, build_learning_map.py | Hierarchy, related and suggested-route edges remain page relations; they do not imply concept semantics or prerequisites. |
| Understand route | data/guided-route.yml and lesson_contracts | Strict Pydantic models in build_learning_map.py; guided_route_transitions.py; tests/knowledge/test_lesson_contracts.py and test_flat_curriculum_sidebar.py | Generated bilingual guided route, conceptual-focus groups and peer Review navigation | Snapshot: 9 canonical stages and 20 core lesson contracts. Route focus is a pedagogical association, not a direct concept→computation edge. |
| Revision | Page-map revision_role, revision_of and revision_support fields | ProjectIndex._load_revision_relations; tests/knowledge/test_project_index.py; CI-invoked audit_revision_coverage.py | Generated reverse aid/lesson indexes, 50 typed aid links across 40 pages, and a coverage inventory for 46 Understand + 16 Build pages | All 62 pages currently declare integrated_sufficient with section evidence; 6 Understand pages have integrated support without a page aid and all 16 Build pages use integrated support. This is an authored assessment, not learner validation. Non-page revision aids are not supported by resources.yml. |
| Practice | Published pages tagged destination:practice; authored related links and explicit heading anchors | check_page_metadata.py; ProjectIndex page-edge checks; bilingual page tests | Per-lesson exercise hubs, shared collections and Q/K/V activity pilot | No global activity registry. Page-level related links do not imply that every activity maps to every lesson or concept. |
| Build | docs/learning-path.md, implementation modules/tests and data/resources.yml | check_resource_registry.py plus module-specific tests; no single Build graph validator identified | Build milestones and code/resource references | The milestone dependency model is not yet a unified machine-readable cross-graph owner. Do not infer implementation dependencies from lesson order. |
| Computation | data/computational-graph.yml | site/tools/check_computational_graph.py; tests/site/test_computational_graph.py | render_computational_graph.py; ProjectIndex evidence adapter | Snapshot: 57 nodes, 75 computational edges, 7 branches and 8 named views. Edges describe data/operation flow; page-mediated and route-focus associations remain distinct from direct concept edges. |
| Sources and extraction evidence | data/sources.yml and data/extractions/*.yml | site/tools/check_source_catalogue.py | include_evidence=True adapter in cross_graph_evidence.py; cross_graph_query.py; tests/knowledge/test_cross_graph_query.py | Snapshot at main `534ce3d`: 142 source records, 100 extraction files and 520 atomic items (source-coverage report #1306, 2026-11-21); 42 catalogue IDs have no matching extraction filename and there are zero orphan extraction filenames. The current catalogue has 44 explicit collection decisions (42 non-empty, 2 explicit empty) and 98 undecided. The 489-item count belongs to the earlier 96-file snapshot. A current 100-file locator-quality audit remains separate. Only explicit item-level concept mappings create source-evidence paths. |
| Non-page resources | data/resources.yml | site/tools/check_resource_registry.py; tests/knowledge/test_resource_registry.py | ProjectIndex resource associations and JSON-LD export | Snapshot: 5 implementation resources. This is not a generic activity, revision-aid or source-extraction registry. |
| Historical genealogy | data/history-pilot.yml | site/tools/check_history_pilot.py; site/tools/render_history_pilot.py; site/tools/check_history_rendered.py | Bilingual historical timeline | Snapshot: 17 events and 20 historical source records. Chronology is not causal influence. Historical paths are not yet part of cross_graph_query.py. |
| Editorial collections | Calendar editorial documents and authored story pages | No generalized editorial membership validator established | 2026 calendar and story pages | Calendar membership/order is editorial, not a new curriculum or concept graph. |
| Project Intelligence | Read-only `ProjectIndex`, coverage/query adapters and metric definitions over canonical owners | `tests/knowledge/test_project_index.py`, `test_project_coverage.py`, `test_cross_graph_query.py`; shared CI/test entry points | `report_project_index.py`, coverage matrix, opt-in `cross_graph_query.py` JSON paths | Existing read model is implemented; coverage matrix/report still omit or label some Build/computation/source/Practice dimensions as unregistered. No complete evidence-aware diagnostic suite, history/decision traversal, recommendation engine or autonomous mutation. |
| Linked-data export | Derived from concepts, pages and resources | tests/knowledge/test_knowledge_graph_export.py; site/tools/check_knowledge_graph_rendered.py | site/knowledge-graph.jsonld | This is a bounded export projection, not a universal serialization of every graph family or complete claim-level PROV-O provenance. |

### ProjectIndex and cross-graph query boundary

- ProjectIndex.build(root) is the default, read-only joined view of pages, concepts/domains, guided-route membership, resources, page relations and page-based revision relations.
- ProjectIndex.build(root, include_evidence=True) opts into the larger source/extraction, computational and route-focus projection. The default must remain lightweight.
- cross_graph_query.py currently supports concept-centred paths for item-level source evidence, catalogue-only gaps, page-mediated computation, stage-mediated route-focus computation, Practice links and non-page resources.
- The query layer preserves exact locators, source scan/integration status, extraction disposition, confidence, assumptions and limitations. It explicitly reports missing locators and unpromoted candidate destinations.
- The current query layer does not yet traverse historical events, Build milestone dependencies, source-local pedagogical graphs or structured decision records; it is not a page-originating reverse evidence query or a general recommendation engine.
- The concept coverage matrix and `report_project_index.py` remain separate from the opt-in evidence-path query. The matrix has an explicit state vocabulary but does not integrate every evidence path or every coverage dimension; `stale` is not yet modelled. Build/computation/source/Practice remain `not_registered` until complete canonical concept mappings exist. A missing matrix dimension must not be interpreted as proof that no underlying records exist.

### CI and validation orchestration

The existing workflows already provide shared validation entry points; do not add a workflow per graph or concept.

- `.github/workflows/ci.yml` runs the source catalogue, page metadata, concept registry, resource registry and history validators, generates the Understand/Build revision-coverage inventory through `ProjectIndex`, then runs the repository test suite.
- .github/workflows/quarto.yml validates page/resource metadata, renders history and computational graph fragments, checks rendered learning-map/knowledge-graph/history outputs and verifies local rendered links.
- The computational graph validator is exercised by tests/site/test_computational_graph.py; it is not a separate per-concept workflow.
- Cross-graph query behavior is covered by tests/knowledge/test_cross_graph_query.py. Its five checked-in concept cases are a bounded regression set, not a general precision/recall benchmark.

## 10. Change-control rule

Before adding a registry, graph, tag dimension or workflow, answer:

1. Which entity or relation is currently missing?
2. Why can no existing canonical owner represent it?
3. Which learner/editorial/engineering decision will query it?
4. What stable ID and relation semantics are required?
5. What is the smallest source-of-truth change?
6. Which validator, tests, projections and documentation must change?
7. How will migration preserve existing content and bilingual references?

If these questions have no concrete answer, prefer extending an existing contract or recording a deferred need.
