# Project metric registry

**Status:** canonical measurement contract, v2 (2026-11-20).\
**Scope:** deterministic structural metrics and coverage semantics for the Project Intelligence Layer (PIL).  
**Authority:** this document is the canonical registry of PIL metric definitions. It does not replace or duplicate the canonical data files. Definitions are established; computation and the coverage matrix are separate implementation work.

## 1. Purpose and boundaries

This registry defines what a count or coverage statement means before a report computes it. It is a structural inventory, not a learner-outcome KPI catalogue. It must not be conflated with [Project KPIs](project-kpis.md), whose outcomes often require learner data, experiments or human review.

The registry is documentation-first. A future Python catalogue may encode these definitions for execution, but it must not become a second source of truth. Canonical records remain in existing page metadata and registries.

## 2. Mandatory metric definition

Every metric implementation must expose:

| Field | Contract |
|---|---|
| ID | Stable ID from this registry; never derive it from a label |
| Name | Human-readable label |
| Definition | Exact calculation or set operation |
| Unit | Page record, concept, stage, membership, resource, edge, source, node, etc. |
| Population | Canonical entity set included |
| Source | Canonical path(s), schema/marker version and owning reader |
| Filters | Explicit dimensions and default scope |
| Exclusions | What is deliberately not counted |
| Grouping | Language and logical-content grouping semantics |
| Unknown policy | Behavior when data is absent or not enumerable |
| Implementation | available, adapter_pending, human_review or not_registered |
| Tests | Tests pinning the definition, or explicit pending state |

Every computed value must carry repository commit, calculation timestamp, filters, unit and provenance. Rates must expose numerator and denominator; counts must not be presented as rates.

## 3. Global counting rules

1. **Page records are not logical topics.** FR and EN pages are two page records. Count language-specific records separately.
2. **Bilingual page pairing.** The page metadata contract uses `topic` to identify expected FR/EN counterparts. A unique pair supports verification of structural associations. Semantic equivalence and logical-content counts require editorial review.
3. **Concept IDs are language-independent.** Count unique canonical concept IDs once.
4. **Edges have typed units.** Count stored directed associations in their owning registry. Do not symmetrize, transitively close or merge relation families.
5. **Memberships are occurrences.** A page may have multiple route memberships. Count membership records separately from unique member pages.
6. **No volume-as-quality proxy.** Counts are inventories, not evidence of correctness, completeness or learning effectiveness.
7. **No implicit zero.** An absent or unsupported mapping is not a measured zero.
8. **No schema migration by measurement.** Metrics do not authorize changes to the 62-page snapshot, validators or revision contract.

## 4. Canonical metric catalogue

### 4.1 Published page inventory

| ID | Metric and definition | Unit | Canonical source/version | Implementation |
|---|---|---|---|---|
| PIL-PAGE-001 | Unique published page IDs | page record | site/**/*.qmd; LLM-LAB-PAGE-MAP v1; page_index reader | available |
| PIL-PAGE-002 | Published pages grouped by language | page record | Same as above | available |
| PIL-PAGE-003 | Published pages grouped by destination tag | page record | Page-map v1 | available |
| PIL-PAGE-004 | Published pages grouped by editorial type tag | page record | Page-map v1 | available |
| PIL-PAGE-005 | Published pages grouped by explicit topic tag; untagged pages remain visible | page record | Page-map v1 | available |
| PIL-PAGE-006 | Page records grouped by destination, topic and language; distribution only, not parity verdict | page record | Page-map v1 | available |
| PIL-PAGE-007 | Distinct explicit topic values on published page records, including shared pages | declared topic | Page-map v1 | available |
| PIL-PAGE-008 | Topics with exactly one published FR page and one published EN page. Shared pages do not affect pairing. | bilingual topic | Page-map v1 and `group_bilingual_topics` | available |

Exclusions: planned and retired pages, rendered _site copies and generated artifacts. Topic/language imbalance does not prove a missing translation.

### 4.2 Understand route

| ID | Metric and definition | Unit | Canonical source/version | Implementation |
|---|---|---|---|---|
| PIL-ROUTE-001 | Unique stage IDs | route stage | data/guided-route.yml, schema_version 1 | available |
| PIL-ROUTE-002 | Explicit core (stage, language, page) membership occurrences | membership | Same route registry | available |
| PIL-ROUTE-003 | Explicit optional (stage, language, page) membership occurrences | membership | Same route registry | available |
| PIL-ROUTE-004 | Unique page IDs across core and optional memberships | page record | Route schema v1 resolved against published page IDs | available |
| PIL-ROUTE-005 | Published Understand page records with no core or optional membership | page record | Page-map v1 + route schema v1 | available |

A page in multiple memberships is counted once by PIL-ROUTE-004 and once per occurrence by PIL-ROUTE-002/003. Optional Deepen or Practice pages retain their own destination.

### 4.3 Concepts and explicit associations

| ID | Metric and definition | Unit | Canonical source/version | Implementation |
|---|---|---|---|---|
| PIL-CONCEPT-001 | Unique canonical concept IDs | concept | data/concepts.yml, schema_version 2 | available |
| PIL-CONCEPT-002 | Explicit concept-to-domain memberships | concept-domain membership | concepts.yml v2 + data/domains.yml | available |
| PIL-CONCEPT-003 | Unique explicit (concept_id, page_id) associations in concepts[].resources | directed association | concepts.yml v2; page IDs only | available |
| PIL-CONCEPT-004 | Distinct associated page IDs per concept | page per concept | Same as above | available |
| PIL-CONCEPT-005 | Concepts with non-empty FR and EN labels and definitions | concept | concepts.yml v2 | available |

The concepts[].resources field contains page IDs. It must not be counted as, or extended to contain, non-page resource IDs.

### 4.4 Non-page resources

| ID | Metric and definition | Unit | Canonical source/version | Implementation |
|---|---|---|---|---|
| PIL-RESOURCE-001 | Unique non-page resource IDs | resource | data/resources.yml, schema_version 1 | available |
| PIL-RESOURCE-002 | Resource records grouped by kind, status or language | resource | Same resource registry | available |
| PIL-RESOURCE-003 | Unique explicit (resource_id, page_id) pairs in referenced_by | association | Same resource registry | available |
| PIL-RESOURCE-004 | Unique explicit (resource_id, concept_id) pairs in concepts | association | Same resource registry | available |
| PIL-RESOURCE-005 | Distinct pages referencing each non-page resource | page per resource | Same resource registry | available |

The current resource schema admits implementation resources. referenced_by is not a revision role, nor proof of learner-facing publication or pedagogical coverage.

### 4.5 Revision-support assessment

| ID | Metric and definition | Unit | Canonical source/version | Implementation |
|---|---|---|---|---|
| PIL-REV-001 | Inventoried pages grouped by assessment state emitted by the revision inventory | page record | audit_revision_coverage.py output schema v1; page-map v1 | human_review |
| PIL-REV-002 | Validated source-page to typed-target declarations grouped by role and target type | directed revision edge | Proposed revision contract; not an approved schema | not_registered |
| PIL-REV-003 | Pages explicitly assessed as having revision support | page record | Future approved contract + revision inventory | not_registered |

The inventory's not_assessed value is an audit placeholder, not a claim that a page lacks a recap, self-check or companion resource. Until the contract and validator are approved, PIL-REV-002/003 must not be reported as zero-coverage findings. The page validator does not currently validate a revision field.

### 4.6 Sources, computation, practice and Build

| ID | Metric and definition | Unit | Canonical source/version | Implementation |
|---|---|---|---|---|
| PIL-SOURCE-001 | Unique source IDs | source record | data/sources.yml, schema_version 1 | adapter_pending |
| PIL-SOURCE-002 | Extraction records and extraction item IDs, counted separately | record or item | data/extractions/; schema to be verified per family | adapter_pending |
| PIL-COMP-001 | Unique computational node IDs | node | data/computational-graph.yml, schema_version 1 | adapter_pending |
| PIL-COMP-002 | Stored typed directed computational edges | edge | Same computational graph | adapter_pending |
| PIL-PRACTICE-001 | Reviewed typed page/concept-to-exercise, test or experiment associations only | association | No complete canonical crosswalk established | not_registered |
| PIL-BUILD-001 | Unique Build milestone IDs in an approved machine-readable registry | milestone | docs/learning-path.md is narrative, not a validated milestone registry | not_registered |
| PIL-BUILD-002 | Explicit milestone-to-page and milestone-to-code/test evidence associations | association | No complete machine-readable crosswalk established | not_registered |

File presence, filename similarity, imports, test proximity and textual mentions do not create practice or Build associations.

## 5. Coverage matrix contract

The first matrix is concept-centred: one row per canonical concept ID. It is a set of independent dimensions, not a score.

| Dimension ID | Positive evidence | Canonical source | Enumeration status |
|---|---|---|---|
| definition | Non-empty canonical bilingual labels and definitions | concepts.yml v2 | available |
| teaching_pages | Explicit page IDs in concepts[].resources resolved to published pages | concepts.yml v2 + page-map v1 | available |
| understand | Associated page has explicit core/optional membership in guided route | Concept/page associations + route schema v1 | available |
| build | Reviewed milestone/page/evidence association | No machine-readable milestone crosswalk | not_registered |
| computation | Explicit concept-to-computational-node bridge | No canonical bridge established | not_registered |
| resources | Explicit first-class resource association | resources.yml v1 + ProjectIndex | available |
| revision_support | Editorial assessments of associated Understand/Build lessons and their explicit section anchors or companion aids | Page-map v1 through the ProjectIndex revision adapter | human_review |
| sources | Explicit concept IDs in source/extraction records with valid lineage | sources.yml and extraction manifests; adapter pending | not_registered |
| practice | Explicit reviewed exercise/test/experiment mapping | No complete canonical mapping | not_registered |
| bilingual_parity | Explicit concept links to both published counterparts of every associated localized page topic | concepts.yml v2 + page-map v1 pairing by `topic` | available |

### 5.1 Allowed cell states

| State | Meaning and use |
|---|---|
| present | Positive explicit evidence exists and resolves |
| missing | An expected association is absent; only when an approved completeness/eligibility rule defines the expectation and the source is exhaustive |
| not_applicable | Dimension does not apply, supported by a documented rule or reviewed decision |
| not_registered | No canonical mapping or adapter exists to determine this dimension |
| needs_review | Evidence is ambiguous, incomplete or requires editorial judgment |
| not_assessed | An assessment has not been performed; never use as a synonym for missing |

Each cell must include evidence IDs/paths and the rule assigning its state. present does not mean pedagogically sufficient or scientifically correct. missing is not permitted merely because a list is empty.

### 5.2 Revision-support scope

The revision adapter supplies assessments for published Understand and Build lessons. An optional Deepen page contributes to Understand route membership and stays outside revision assessment. An explicit `not_applicable` lesson assessment retains its rationale in the evidence and is excluded from the aggregation.

| Applicable lesson assessments for one concept | Matrix state |
|---|---|
| No associated published pages | `needs_review` |
| Associated pages exist, all outside the scope or explicitly `not_applicable` | `not_applicable` |
| All await assessment | `not_assessed` |
| All were assessed as `integrated_sufficient` or `companion_sufficient` | `present` |
| All were explicitly assessed as `missing`, with a reason on each lesson | `missing` |
| Partial assessments or any other mixture of applicable statuses | `needs_review` |

Assessment evidence points to the lesson metadata and any explicit section anchors. A typed link to a companion aid is evidence of the relationship. The lesson assessment determines sufficiency.

### 5.3 Structural FR/EN parity of concept links

For each concept, use the published page IDs explicitly listed in `concepts[].resources`. Each `topic` represented by an associated FR or EN page must resolve to exactly one published page in each language. The validator and matrix use the same topic grouping. The cell records the topic, page IDs and paths, and indicates which associations exist. Language-neutral pages do not take part in pairing.

| Evidence on localized page links for one concept | Matrix state |
|---|---|
| All topics resolve to unique pairs and both pages of every pair are linked | `present` |
| All topics resolve to unique pairs and at least one published counterpart lacks an explicit concept link | `missing` |
| A localized linked page has no topic, a topic has no unique pair, or the concept has no page links | `needs_review` |
| The concept links only to language-neutral pages | `not_applicable` |

For a `needs_review` cell, the evidence still identifies any known missing links from other, resolved pairs. `present` verifies link symmetry. Comparing the lessons' content and objectives requires editorial review. Registry v2 introduces this rule while retaining the matrix schema and dimension ID.

### 5.4 Aggregation rules

- Denominator: distinct canonical concept IDs in concepts.yml v2.
- Each concept appears once, independent of language.
- Page evidence retains page IDs and language; do not collapse FR/EN pages without an explicit reviewed pair.
- Multiple evidence links do not create multiple concept rows.
- Do not compute an overall percentage by treating not_registered, not_applicable, needs_review or not_assessed as failures.
- Any future percentage must publish its eligible denominator and excluded-state counts.

## 6. Provenance and reproducibility

Every computed metric and matrix export must record repository and commit SHA, calculation timestamp, registry version, source paths and schema/marker versions, filters, population, unit, count (and numerator/denominator for rates), excluded/unresolved/non-enumerable records, and query/reader/test version.

Generated reports are disposable projections. Never edit a generated matrix as canonical input.

## 7. Validation and acceptance

The registry is accepted when every metric has a stable ID, exact unit and definition; every metric names a canonical owner/version or explicitly states no registry exists; bilingual grouping and exclusions are explicit; unsupported dimensions are not_registered rather than zero; revision status distinguishes not_assessed from missing; and future implementations are tested on synthetic fixtures and a real repository snapshot.

The read-only matrix builder uses ProjectIndex and is tested with synthetic fixtures and the canonical repository data.
