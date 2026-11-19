# Project Intelligence Layer — implementation plan

**Status date:** 2026-11-19  
**Initial implementation branch:** `feat/project-intelligence-index`  
**Initial implementation:** [PR #1380](https://github.com/JM-Brun/llm-lab/pull/1380); resource/revision adapters: [PR #1394](https://github.com/JM-Brun/llm-lab/pull/1394)  
**Architecture:** [Project intelligence layer](project-intelligence-layer.md)  
**Tracking:** [Issue #1378](https://github.com/JM-Brun/llm-lab/issues/1378)

This document is the operational backlog for turning the proposed Project Intelligence Layer (PIL) into a tested, documented, reusable repository capability. It records what exists, what remains, dependencies, and acceptance criteria. It does not declare unimplemented capabilities complete.

## 1. Current implementation state

### Delivered in the first slice (PR #1380)

- Read-only in-memory `ProjectIndex` composed from the published-page reader and canonical YAML readers.
- Stable page lookup, concept/domain records, tag and domain indexes, and explicit concept-to-page associations.
- Typed page-edge records preserving `suggested_route`, `hierarchy` and `related` families and their direction.
- Understand guided-route membership by stage, language and core/optional role.
- Deterministic page/concept/route queries and basic count units.

### Delivered in the second slice (PR #1394)

- First-class non-page `ResourceRecord` objects from `data/resources.yml`.
- Explicit page/resource and concept/resource association records.
- A separate `RevisionEdge` adapter for the proposed page-map relation, with `section`, `page` and `resource` target types.
- Status, duplicate, reference, publication, language and explicit-anchor checks in the read-model adapter.
- Synthetic tests plus a real-repository assertion for five resources, ten page/resource associations, zero declared revision edges and 62 pages still `not_assessed`.

### Deliberate boundaries

- The revision contract is documentation/proposal only. The adapter does not change the page metadata schema, `check_page_metadata.py`, `check_resource_registry.py`, or any of the 62 page records.
- No current page declares a `revision` object; the adapter therefore exposes no current revision edges.
- Inverse resource/revision query methods are not yet implemented; they are the next step.
- Source/extraction, computational graph, historical, experiment and Build-milestone adapters remain future work.
- No semantic links are inferred from tags, titles, body text or lexical similarity.
- No metrics registry, coverage matrix, diagnostics, stable CLI, JSON/Markdown interface, cache, dashboard or recommendation engine exists yet.

## 2. Remaining work — ordered backlog

The revision-support and ProjectIndex work follows this dependency order. Do not skip ahead to interfaces or bulk page migration.

### Step 1 — Contract and validator compatibility (documented proposal)

- Contract: [revision-resource-contract.md](revision-resource-contract.md), documented in PRs [#1388](https://github.com/JM-Brun/llm-lab/pull/1388) and [#1391](https://github.com/JM-Brun/llm-lab/pull/1391).
- The proposed page-map relation distinguishes integrated sections, companion pages and non-page resources; statuses remain `not_assessed`, `assessed` and `not_applicable`.
- The current page/resource validators are not changed. The proposal is not an approved schema migration.
- Before changing validators or any historical page records, review canonical ownership, role vocabulary, anchor conventions, lifecycle rules, language compatibility and the non-page resource representation.

### Step 2 — Existing-resource inventory (complete)

- Inventory: [revision-resource-inventory-2026-11-19.md](revision-resource-inventory-2026-11-19.md), merged in [PR #1395](https://github.com/JM-Brun/llm-lab/pull/1395).
- The report distinguishes in-page recaps, takeaway sections, self-checks, dedicated companion pages, concept links and implementation resources.
- No mass creation of revision sheets or flashcards is part of this step.

### Step 3 — Non-page resource and revision relation adapters (complete)

- Implemented in [PR #1394](https://github.com/JM-Brun/llm-lab/pull/1394).
- `ProjectIndex` now adapts `data/resources.yml` and the optional proposed page-map `revision` object.
- Revision relations remain separate from generic page graph edges. No current page has been migrated and no validator/schema change was made.

### Step 4 — Inverse queries and real-repository tests (next)

Add deterministic forward/reverse query methods for:
- pages ↔ non-page resources;
- concepts ↔ non-page resources;
- source pages ↔ revision targets of type section, page or resource;
- revision status by source page.

Tests must exercise the real repository, not only synthetic fixtures. Cover all five current resources and ten page/resource associations, verify the inverse results, confirm the current 62-page revision inventory has no declared edges, and retain synthetic coverage for all three target types. Section-target keys must include the owning page ID because anchors are page-local.

**Acceptance:** reverse lookups are deterministic, preserve relation family and direction, return stable IDs, and do not double-count bilingual page records or symmetric page relations.

### Step 5 — Metric registry, then coverage matrix

First define a canonical metric registry. Each metric records:
- stable metric ID and human-readable name;
- exact definition and counting unit;
- canonical source, source path and schema version;
- inclusion/exclusion rules and filters;
- bilingual grouping and deduplication semantics;
- missing/unknown/not-applicable behavior;
- owning reader/validator and tests.

Then build the coverage matrix from the query layer. Keep separate dimensions for pages, route membership, concepts, resources, revision support, sources/evidence, practice and Build evidence where canonical mappings exist. Do not collapse dimensions into an opaque score or treat an unregistered association as a defect.

**Acceptance:** every published metric has a reproducible definition and explicit unit; matrix cells distinguish present, missing, not applicable, not registered and needs review.

### Step 6 — Diagnostics, then interfaces

Implement deterministic, read-only diagnostics from the validated query and coverage layers first. Every finding must carry a rule ID, severity, source path, stable entity IDs, evidence and suggested review action. Do not infer semantic relationships from lexical similarity.

Only after diagnostics are stable, add:
- CLI commands;
- machine-readable JSON and review-friendly Markdown/CSV projections;
- a dashboard or site interface consuming the same query results.

The CLI, JSON and dashboard must not implement separate counting or relationship semantics.

### Later ProjectIndex extensions (after the six-step sequence)

- Typed concept-to-concept relation queries and domain membership.
- Build milestone/evidence adapter, only after its canonical mapping contract is reviewed.
- Source, extraction, locator and lineage adapters.
- Computational graph adapter and explicit page/resource bridges.
- History, experiment and test-evidence adapters.
- Incremental cache and AI-assisted candidate recommendations, only after profiling and human-review rules.

## 3. Cross-cutting test strategy

- Unit tests: each adapter, index, query, relation family and metric definition.
- Contract tests: schemas and canonical reader behavior.
- Integration tests: build from a clean repository checkout and verify referential integrity.
- Regression tests: stable ordering, count units, bilingual grouping and relation direction.
- Negative tests: missing IDs, malformed records, duplicate IDs, unsupported relation types and partial registries.
- Performance tests: benchmark artifacts with dataset size and environment recorded; avoid timing assertions in ordinary unit tests.
- Workflow tests: run on the exact PR SHA; record each workflow's conclusion independently.

## 4. Decisions that must remain explicit

| Decision | Current rule | Revisit only when |
|---|---|---|
| Source of truth | Existing canonical registries and page metadata | A reviewed schema migration changes ownership |
| Understand vs Build | Separate pathways and evidence models | Curriculum owners explicitly revise the model |
| Page vs concept | Separate entities and count units | Never merge these units |
| Page tags vs concepts | Tags are facets, not semantic concept links | A reviewed explicit mapping is introduced |
| Missing association | Finding, not automatic error | A contract marks the association mandatory |
| AI/heuristics | Candidate generation only | Human review promotes a candidate to canonical metadata |
| Persistence | In-memory full rebuild first | Profiling demonstrates a material bottleneck |

## 5. Immediate next actions

1. Finish PR #1380 CI verification and semantic review.
2. Add real-corpus integration coverage.
3. Inspect resource, concept-relation, source/extraction, computational-graph and Build schemas/readers.
4. Publish the source/metric registry with explicit count definitions.
5. Implement the resource adapter, then concept relations and Build evidence as separately reviewed increments.
6. Add the concept coverage matrix and deterministic audit report.
7. Add CLI and output formats only after metric contracts stabilize.

## 6. Definition of done for the PIL

The Project Intelligence Layer is considered operational when a clean checkout can produce a reproducible inventory and coverage report; every displayed metric names its unit and canonical source; page, concept, route, Build, resource, source and computational relations remain typed; reverse lookups and diagnostics are tested; output includes provenance and limitations; and the full repository validators remain green.
