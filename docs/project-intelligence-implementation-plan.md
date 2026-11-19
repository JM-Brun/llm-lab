# Project Intelligence Layer — implementation plan

**Status date:** 2026-11-19  
**Implementation branch:** `feat/project-intelligence-index`  
**Initial implementation:** [PR #1380](https://github.com/JM-Brun/llm-lab/pull/1380)  
**Architecture:** [Project intelligence layer](project-intelligence-layer.md)  
**Tracking:** [Issue #1378](https://github.com/JM-Brun/llm-lab/issues/1378)

This document is the operational backlog for turning the proposed Project Intelligence Layer (PIL) into a tested, documented, reusable repository capability. It records what exists, what remains, dependencies, and acceptance criteria. It does not declare unimplemented capabilities complete.

## 1. Current implementation state

### Delivered in the first slice (PR #1380)

- Read-only in-memory `ProjectIndex` composed from the existing published-page reader and canonical YAML readers.
- Published page lookup by stable page ID.
- Canonical concept and domain records loaded from `data/concepts.yml` and `data/domains.yml`.
- Exact tag lookup, page-domain lookup, and explicit concept-to-page associations from `concepts[].resources`.
- Typed page-edge records preserving relation family and direction for `suggested_route`, `hierarchy`, and `related`.
- Understand guided-route membership by stage, language, and core/optional role from `data/guided-route.yml`.
- Deterministic query methods for tag filters, concept/page reverse lookups, incoming/outgoing page edges, route-stage membership, and basic counts.
- Synthetic tests for distinct count units, bilingual page records, explicit associations, edge direction/family, route roles, and unknown identifiers.

### Deliberate boundaries of the first slice

- It does not yet inventory non-page resources from `data/resources.yml`.
- It does not yet model source records, extraction items, source lineage, computational graph nodes/edges, historical records, experiments, or Build milestones.
- It does not infer semantic concept links from tags, titles, body text, or lexical similarity.
- It does not treat page tags as route membership or the Understand route as the Build path.
- It does not yet provide a stable CLI, JSON/Markdown report, cache, dashboard, recommendation engine, or repository-wide audit.
- Synthetic tests do not establish real repository totals or full-registry correctness.

## 2. Remaining work — ordered backlog

### P0 — Stabilize and review the first slice

1. **Close CI defects on PR #1380.**
   - Re-run Python quality/domain checks after the Ruff fixes.
   - Confirm the test suite, Secret scanning, and Quarto site workflow on the exact PR head.
   - Inspect any failure logs; do not infer success from a queued or skipped workflow.
2. **Review semantics against the real repository.**
   - Check all indexed page relations against the page metadata schema and existing graph conventions.
   - Verify whether reciprocal hierarchy declarations are stored as separate authored edges; document count semantics rather than silently deduplicating.
   - Verify page-domain and concept-domain dimensions remain distinct.
3. **Add real-corpus integration tests.**
   - Build the index from the repository root in CI.
   - Assert invariants and referential integrity, not brittle hard-coded counts unless the test intentionally snapshots a reviewed baseline.
   - Check unknown page/concept IDs, missing references, and deterministic ordering.

**Acceptance:** PR #1380 passes required CI on its current head; public methods and count units are documented; at least one real-repository build is exercised in tests.

### P1 — Complete the source inventory and metric contracts

4. **Create a canonical source/metric registry.**
   For every metric, record: name, definition, unit, canonical owner, reader/validator, inclusion rules, exclusions, language treatment, deduplication rule, and tests.
5. **Inventory every structured source before adding adapters.**
   Inspect the actual schemas and readers for:
   - page metadata and Quarto render inventory;
   - Understand guided route;
   - Build path and its implementation/test evidence;
   - concepts and domains;
   - first-class resources;
   - sources, extraction records, locators and lineage;
   - computational graph;
   - history pilot;
   - experiments, source code, tests and generated reports.
6. **Specify count units.**
   Keep separate counts for page records, logical bilingual topics, lessons, route memberships, route stages, Build milestones, concepts, domains, resource records, source records, extraction items, experiments, tests and typed graph edges. Never combine unlike units into a single “content count”.
7. **Define page identity and language grouping.**
   Use stable page IDs. Bilingual page records count separately; logical-topic grouping is only reported when a canonical topic ID or reviewed pairing exists.

**Acceptance:** the registry identifies one canonical source per fact; each metric has an explicit unit and reproducible inclusion rule; no unsupported Build/resource/source totals are published.

### P1 — Extend the read model by typed adapters

8. **First-class resource adapter.**
   Read `data/resources.yml` through its existing schema/reader; expose resources by ID and explicit resource↔concept/page links. Do not reinterpret `concepts[].resources` page IDs as resource IDs.
9. **Concept relation adapter.**
   Preserve typed concept-to-concept relations and domain membership, with forward and reverse queries.
10. **Build evidence adapter.**
    Identify the actual structured milestone/evidence contract in the Build path. If evidence is currently distributed across documentation, code and tests without a canonical mapping, first propose and review a minimal mapping contract; do not derive completion from file names or page tags.
11. **Source and extraction adapters.**
    Link source records, versions, extraction items, locators and lineage only through explicit IDs. Keep source citation, extraction provenance and concept association as distinct relations.
12. **Computational graph adapter.**
    Preserve node/edge types and computational semantics; add explicit bridges to pages/resources only where the source model provides them.
13. **History and experiment adapters.**
    Expose historical relations and experiment evidence without treating chronology, co-occurrence or file proximity as causality/association.

**Acceptance:** each adapter has schema-backed tests, stable IDs, source provenance, reverse lookup, and explicit edge semantics; no generic graph flattening loses relation family.

### P1 — Coverage and diagnostics

14. **Concept coverage matrix.**
    For each concept, report explicit coverage by teaching page, Understand route placement, Build evidence, resource, source/evidence, exercise and experiment. Use statuses such as present, absent, not applicable, and unknown; absence is not automatically an error.
15. **Route coverage.**
    Report stage membership, core/optional role, language parity and unresolved page references. Keep Understand and Build separate.
16. **Page relationship inspection.**
    Provide incoming/outgoing views grouped by relation family and relation type; distinguish navigation, hierarchy, related links, concept associations and cross-resource links.
17. **Integrity diagnostics.**
    Detect dangling IDs, duplicate stable IDs, invalid relation targets, orphaned registry entries, invalid domain references and inconsistent bilingual links where the relevant schema defines a contract.
18. **Explainable findings.**
    Every finding includes severity, rule ID, source path, stable record ID, evidence and suggested review action. Heuristic similarity remains triage-only.

**Acceptance:** diagnostics are deterministic and read-only; optional/intentional gaps are not reported as errors; every warning is traceable to canonical data.

### P2 — Reporting and usability

19. **CLI.**
    Add a small command interface only after the query API and metric definitions stabilize. Initial commands should cover `stats`, `inventory`, `concept-coverage`, `route`, `page-links`, and `audit`.
20. **Machine-readable output.**
    Provide deterministic JSON with schema/version metadata, source commit, generated-at timestamp, source paths and metric definitions. Avoid embedding full page bodies.
21. **Human-readable reports.**
    Provide Markdown and optionally CSV projections from the same result objects; include scope, limitations and counts by unit.
22. **Documentation and examples.**
    Document public API, CLI, metric definitions, source provenance, and examples of reverse lookups and coverage investigations.

**Acceptance:** CLI/report output is deterministic for the same checkout; JSON is versioned; Markdown/CSV are projections of the same calculations, not separate implementations.

### P3 — Performance and optional intelligence

23. **Benchmark before optimization.**
    Measure YAML/page parsing, normalization, index construction, query latency and serialization separately on representative repository size.
24. **Cache only with evidence.**
    If full rebuild is measurably expensive, add content-hash-based caching with adapter/schema versioning and explicit invalidation. Full rebuild remains the correctness oracle.
25. **Recommendations last.**
    Only after explicit coverage and diagnostics are reliable, offer candidate page/resource/lesson suggestions. Every candidate must show the gap it addresses, supporting records, likely overlap, confidence and human-review status. Never write canonical metadata automatically.

**Acceptance:** performance targets are measured and recorded; caching never hides stale inputs; recommendations are non-authoritative and reviewable.

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
