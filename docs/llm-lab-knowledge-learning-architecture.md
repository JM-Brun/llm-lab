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
| Revision graph | Aids/resources → lessons supported; role and coverage assessment | Contract proposed; enforcement and inventory reconciliation remain |
| Practice graph | Activities ↔ concepts, lessons, skills and evidence/solutions | Dedicated practice content exists; complete canonical activity model remains future work |
| Build dependency graph | Implementation modules/components and dependency/verification edges | Build route, data/resources.yml, docs/learning-path.md; bounded scope |
| Computational graph | Operations, state/data artifacts and computational flow | data/computational-graph.yml and docs/canonical-computational-spine.md |
| Source/provenance graph | Sources, inspections, extracted claims and supported project artifacts | Source catalogue, extraction records and source-lineage architecture |
| Editorial graph | Collections, editions, stories and editorial membership/order | Calendar redesign documented; generalized model not yet implemented |
| Historical graph | Events, concepts, sources and evidence-backed historical relations | data/history-pilot.yml and docs/history-data-model.md; specialized, not a second concept registry |

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

A coverage matrix is a diagnostic projection, not an editorial quality score. Distinguish at least present, absent, not assessed, not applicable and stale. Do not infer quality or sufficiency from a non-empty link.

## 9. Existing implementation map

The following foundations should be preserved and extended:

- docs/information-architecture.md: canonical ownership and metadata governance.
- docs/knowledge-architecture-interoperability.md: technology-neutral and cross-repository boundaries.
- data/concepts.yml, data/domains.yml: shared semantic foundation.
- LLM-LAB-PAGE-MAP v1: page identity and page graph.
- data/guided-route.yml, docs/learning-path.md: Understand route and implementation learning path.
- data/resources.yml: current non-page implementation resources.
- docs/revision-resource-contract.md: proposed aid-to-lesson relation contract.
- data/computational-graph.yml, docs/canonical-computational-spine.md: computation model and branches.
- data/sources.yml, data/extractions/, source-lineage documentation: source ingestion and provenance.
- data/history-pilot.yml, docs/history-data-model.md: specialized historical model.
- docs/project-intelligence-layer.md: read-only project index and diagnostics direction.
- docs/advent-calendar-editorial-redesign.md, docs/advent-calendar-next-steps.md: 2026 editorial decision and handoff.

This inventory does not claim equivalent maturity or complete validation. See [the implementation backlog](llm-lab-architecture-implementation-backlog.md) for verified gaps and acceptance gates.

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
