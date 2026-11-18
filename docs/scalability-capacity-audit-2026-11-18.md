# Scalability and capacity audit — 2026-11-18

**Status:** static architecture/code review with a repository-size snapshot. This is not a load test, runtime benchmark, or guarantee of capacity.  
**Baseline:** default branch `main`, inspected 2026-11-18 after merge of PR #1247.  
**Purpose:** determine whether current knowledge-management structures and workflows can grow to thousands of sources, hundreds/thousands of concepts, more resources and larger graphs without losing traceability or making normal contributions prohibitively expensive.

## 1. Executive assessment

**The information model is directionally scalable; the current operating implementation is not yet demonstrated at the requested scale.**

The strongest choices are already present:
- one canonical owner per kind of information;
- stable language-independent IDs and typed relations;
- separate source, extraction, concept, page, resource, computation, history and pedagogical-route models;
- extraction records split by source already;
- set/dictionary-based referential checks in the source and concept validators;
- deterministic generated projections rather than manually maintained duplicate graphs;
- iterative cycle detection for acyclic concept relation families;
- a documented, lossless staged plan for distributing source identity and inspection history.

The principal constraint is not the concept graph itself. It is the combination of:
1. a **single canonical `data/sources.yml` file** still holding every source and scan history;
2. **repository-wide validation and generation** that reread all relevant files on each full CI run;
3. a lack of recorded runtime/size baselines and synthetic growth tests;
4. incomplete automation for lineage and cross-graph evidence traversal;
5. the maintenance cost of a growing number of per-page and per-source artifacts, even after the monolith is removed.

No evidence from this review justifies introducing a database, graph server, search cluster or a new global registry today. Premature infrastructure would add operational complexity before the bottleneck is measured.

## 2. Reproducible repository snapshot

The following counts were computed from the current canonical files on `main` on 2026-11-18. They are a point-in-time baseline, not targets or a complete inventory of every generated artifact.

| Canonical structure | Current count | File size in lines | Evidence |
|---|---:|---:|---|
| External sources | 139 records | 6,276 | `data/sources.yml` |
| Concepts | 102 | 1,193 | `data/concepts.yml` |
| Concept relations | 114 | included above | `data/concepts.yml` |
| Computational nodes | 72 | 778 | `data/computational-graph.yml` |
| Computational edges | 67 | included above | `data/computational-graph.yml` |
| Domains | 6 | 52 | `data/domains.yml` |
| First-class resources | 5 | 113 | `data/resources.yml` |

Extraction files are already separated by source under `data/extractions/`; their aggregate record/item count was not recomputed in this static review. The current source catalogue is approximately 45 lines per source on average, but this average hides large variation in scan histories and metadata. Do not extrapolate file size linearly without measuring representative source types.

## 3. Architecture and implementation findings

### 3.1 Source identity and inspection history — highest near-term risk

**Observed:** `data/sources.yml` is still the canonical write/read catalogue. It contains 139 records and 6,276 lines. The source catalogue validator loads the whole file, builds source/concept/domain/page lookup sets, iterates all source records, then reads every extraction YAML file and validates all extraction items.

**Target already documented:** `docs/source-lineage-architecture.md` defines:
- `data/sources/<source-id>.yml` for source identity;
- append-only `data/source-scans/<source-id>/<event-id>.yml` for inspections;
- `data/source-lineage/<source-id>.yml` for source-owned typed provenance edges;
- `data/extractions/<source-id>.yml` for located extracted knowledge;
- deterministic generated `data/sources.yml` as a compatibility/discovery index.

**Assessment:** the target reduces same-file merge conflicts and permits independent source updates. It does not automatically make full validation cheaper: if every CI run parses every per-source file and every extraction, total work remains (O(S + E + I + R)), with filesystem and YAML parse overhead. Distribution primarily improves ownership, concurrency and incremental change isolation; performance must be measured separately.

**Decision:** finish the inventory and migration gates already specified in the lineage architecture before switching canonical writes. Do not perform a blind split or hand-maintain both the distributed records and a second index.

### 3.2 Extraction validation — sound indexing, full-corpus work

The validator:
- creates sets for source, concept and domain IDs;
- traverses source records once;
- discovers all extraction YAML files with a sorted glob;
- reads each extraction record once and validates each item;
- uses set membership for source, concept, page and item-ID checks.

This is a good near-linear shape in the number of source records, extraction records, items and references, excluding YAML parse cost and the cost of building page IDs by scanning bilingual page files. It is not an incremental validator: a normal invocation still rechecks the full corpus.

The coverage report groups extraction records by their explicit `source_id`, then aggregates concept coverage. This avoids repeated filename-based lookups and is the right indexing pattern. Keep that contract.

**Risks as volume grows:**
- parsing thousands of YAML files on every run may become dominated by filesystem latency;
- a large single extraction file can become a local review/merge bottleneck;
- accumulating every validation error in memory can produce large logs and slow human diagnosis;
- global page/concept/source lookups need to be built once and reused in each run;
- path traversal order must remain deterministic.

**Do not solve this by skipping validation.** Introduce incremental validation only as an additional fast feedback path, while retaining a periodic/full-corpus integrity check.

### 3.3 Concept graph — appropriate for hundreds; prove larger depths

The concept validator uses ID sets, a set of typed triples for duplicate detection, adjacency maps by relation type, and iterative DFS for cycle checks. The iterative traversal avoids Python recursion-depth failure on long prerequisite/generalization chains. This is a strong basis for hundreds or thousands of concepts.

A small avoidable cost remains: for each relation type marked as a learning dependency, the validator loops over the full relation list again to validate bilingual rationales. The vocabulary is currently bounded, so this is not an urgent bottleneck, but grouping edges by type in one pass would make the intended (O(V+E)) traversal clearer and avoid multiplying work if the vocabulary grows.

The graph's semantic risks are more important than raw speed:
- adding every extracted noun as a concept creates ontology bloat;
- generic untyped edges destroy query precision;
- reciprocal duplicates and inconsistent symmetric-edge storage create false counts;
- relation meaning and evidence must remain explicit;
- concept/page/resource associations are many-to-many and need coverage reports, not forced completeness.

### 3.4 Computational graph and other graph families

The computational graph is separately owned and currently small (72 nodes, 67 edges). The project also has page/navigation, concept, source-local pedagogical, source lineage, historical and learning-route structures. They must not be fused into one universal graph.

For scale, each graph needs its own:
- stable node and edge identity rules;
- allowed relation types and direction;
- owner and lifecycle;
- validation and cycle constraints;
- provenance/evidence policy;
- query and projection consumers.

Cross-graph discovery should be a query over explicit typed links/IDs and evidence locators, not a materialized duplicate graph that copies all nodes and edges.

### 3.5 Generated learning maps and JSON-LD

The learning-map builder loads page data and prepares bilingual outputs, route fragments, per-page context fragments, map payloads and presentation artifacts. The JSON-LD exporter builds an in-memory graph from concepts, domains, resources and published pages, then serializes it deterministically.

At present, this is a full regeneration model. It is easy to reason about and reproducible, but as page/resource/concept counts grow:
- per-page generated fragment count grows with page count;
- complete JSON and JSON-LD serialization rewrites large outputs;
- each language build repeats page discovery and derived graph work;
- the generated map payload becomes a browser download/rendering constraint before YAML validation necessarily becomes one;
- a single global interactive visualization will not remain usable simply because the data model can hold more nodes.

Keep full deterministic generation as the correctness oracle. Add incremental build caching only when profiling shows material cost. For the browser, plan filtered/topic subgraphs, server/static precomputed slices or search-first navigation rather than rendering thousands of nodes at once.

### 3.6 CI and repository collaboration

The current checks are full-corpus validators and site generation/render workflows. They are valuable global integrity gates, but the project has not yet published timing, memory, file-count or merge-conflict baselines.

The right long-term arrangement is layered:
1. fast changed-file/schema checks for contributor feedback;
2. affected-neighborhood referential checks using indexes;
3. full-corpus validation on PRs or scheduled CI, as cost permits;
4. deterministic projection freshness checks;
5. periodic scale/performance jobs with synthetic fixtures;
6. browser tests on representative filtered views, not only successful serialization.

A PR that changes one source should not require a human to inspect thousands of unrelated YAML lines, but the repository must still detect cross-file breakage.

## 4. Capacity verdict by growth dimension

| Dimension | Current architecture | Main scaling risk | Verdict |
|---|---|---|---|
| Sources: 139 → 1,000–10,000 | Distributed target is documented; monolithic catalogue still canonical | Single-file conflicts and full YAML parsing | **Not yet ready operationally** |
| Extractions: many files/items | Per-source files and explicit source IDs; linear traversal patterns | Per-file I/O and full-corpus validation | **Good model; benchmark required** |
| Concepts: 102 → 500–2,000+ | Stable IDs, typed relations, iterative cycle detection | Semantic bloat, edge quality, full graph validation | **Structurally promising** |
| Concept edges: 114 → 10k–100k | Set-based duplicate checks and adjacency maps | Query UX, evidence coverage and large output | **Validation likely tractable; not measured** |
| Computational graph | Separate canonical model | No demonstrated large-graph query/render behavior | **Keep separate; benchmark only if it grows** |
| Resources: 5 → hundreds/thousands | First-class resource registry with many-to-many concept/page links | Type/lifecycle/provenance consistency; large exports | **Model promising; coverage still narrow** |
| Pages: bilingual and generated per-page artifacts | Stable page IDs and deterministic generation | Full page scans, output count, browser payload | **Build and browser performance unmeasured** |
| Cross-graph paths | Explicit IDs and evidence records; five manual pilot paths | No general deterministic query API/test fixture yet | **Not yet scalable as a discovery capability** |
| Human review | Source reviews, syntheses and decision records | Review queue volume and stale decisions | **Needs triage/indexing and ownership rules** |

“Not yet ready” means no demonstrated migration/performance evidence, not that the architecture must be replaced.

## 5. Scale-test matrix

Run synthetic tests against disposable fixtures or temporary worktrees. Never inflate canonical production registries just to benchmark them. Preserve realistic distributions: source type, scan-history length, extraction items/source, concepts/source, page associations, cross-domain degree, and relation types.

| Scenario | Sources | Extraction records | Extraction items | Concepts | Concept edges | Resources | Pages (FR+EN) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Current baseline | 139 | Measure | Measure | 102 | 114 | 5 | Measure |
| S1 — near-term | 1,000 | 1,000 | 10,000 | 500 | 2,000 | 100 | 500 |
| S2 — medium | 5,000 | 5,000 | 75,000 | 2,000 | 10,000 | 500 | 2,000 |
| S3 — stress | 10,000 | 10,000 | 250,000 | 10,000 | 50,000 | 2,000 | 5,000 |

These are workload scenarios, not forecasts. Include adversarial graph shapes: long acyclic chains, high-degree hubs, disconnected components, dense local neighborhoods, duplicate IDs, dangling endpoints, and cycles in both constrained and unconstrained relation families.

### Metrics to record

For each scenario, separately time and measure:
- source/extraction parsing and structural validation;
- concept and computational graph validation;
- coverage report generation;
- lineage/index generation and stale-output check;
- learning-map and JSON-LD generation;
- Quarto incremental and full render;
- browser payload size, parse time, interaction responsiveness and memory;
- CI wall-clock time, peak memory, file count and bytes read/written;
- contributor operation: add one source, add one concept, edit one edge, update one page;
- merge conflict frequency and median review diff size.

Record hardware/runner class, OS, Python/Quarto versions, dependency lock, commit SHA, fixture seed and exact commands. Keep raw machine-readable results as CI artifacts and a small trend summary in the repository. Compare ratios and growth curves first; set budgets only after the baseline is measured.

## 6. Required engineering gates before claiming scale readiness

### Gate A — distributed source migration
- Complete the reader/writer inventory, including tests, workflows, docs and agent skills.
- Add versioned schemas and valid/invalid fixtures for source, scan and lineage records.
- Build a deterministic lossless converter and generated compatibility index.
- Shadow-compare all records and metadata; prove zero loss and zero unresolved references.
- Migrate all consumers before changing canonical writes.
- Test rollback and concurrent edits to different source records.
- Keep unknown rights/version/date states unchanged.

### Gate B — incremental validation with full audit retained
- Build one in-memory index per run: source IDs, extraction source IDs, concept IDs, page IDs, resource IDs and lineage endpoints.
- For PR feedback, validate changed files and their dependency neighborhood.
- Re-run affected graph components when an edge or canonical ID changes.
- Retain a scheduled/full-corpus validator that checks all references and projections.
- Make invalidation explicit: source identity changes invalidate source index/lineage/coverage; concept changes invalidate concept projections and linked pages; page metadata changes invalidate navigation and relevant page-resource projections.
- Add tests proving both that affected outputs rebuild and unrelated outputs remain byte-identical.

### Gate C — bounded and useful graph discovery
- Keep graph families separate; use typed cross-graph joins.
- Add deterministic queries for concept → evidence → source version → locator → page/experiment/resource.
- Return evidence status, scope and limitations with every path.
- Support pagination, domain filters and bounded neighborhood depth.
- Never return all nodes/edges to the browser by default.
- Measure candidate ranking precision on a human-labelled set; never equate link count with relevance.

### Gate D — resource and page growth
- Treat resources as first-class records with stable IDs, typed kind, lifecycle, language, provenance, location and many-to-many associations.
- Add resource-specific validators and orphan/duplicate reports.
- Keep bilingual page pairing at the concept/topic level; do not duplicate one resource per language.
- Generate search and filtered map payloads by topic/domain rather than one unbounded visualization.
- Keep textual/list alternatives for accessibility and large graph navigation.

### Gate E — operational observability
- Publish per-run counts, duration, peak memory and changed-file scope.
- Track full-validation duration and CI queue duration over time.
- Track source ingestion effort and review queue age, not just data volume.
- Define warning budgets from measured baselines and trends, not arbitrary thresholds.
- Schedule periodic synthetic scale tests and fail only on agreed regressions.

## 7. Architecture decisions

**Keep now**
- YAML as canonical authoring format;
- current typed concept and computational graph owners;
- per-source extraction records;
- deterministic JSON/JSON-LD and learning-map projections;
- explicit evidence locators and lifecycle boundaries;
- full-corpus validation as the integrity reference.

**Implement next**
- source registry/scan/lineage migration with the existing staged plan;
- workload baselines and synthetic fixtures;
- indexes reused within validation runs;
- incremental changed-file checks with full validation retained;
- bounded graph queries and filtered browser projections;
- resource coverage and source-to-evidence observability.

**Do not implement yet**
- a graph database, triple store, search cluster or distributed service;
- a universal graph replacing current models;
- a generic event bus or microservice pipeline;
- automatic concept creation from every extraction;
- an always-loaded full interactive graph;
- a cache whose invalidation semantics are not tested.

Reconsider storage technology only if measured workloads show that file-based authoring plus generated indexes cannot meet the agreed contributor/CI/query budgets, or if concurrent editing and external consumers require transactional query capabilities that Git/YAML cannot provide.

## 8. Existing issue ownership and follow-up

Reuse existing issues; do not create parallel tickets:
- [#1211 — provenance coverage and canonical graph reconciliation](https://github.com/JM-Brun/llm-lab/issues/1211): source/extraction coverage, evidence completeness and migration inventory.
- [#1225 — field-level provenance for sensitive source metadata](https://github.com/JM-Brun/llm-lab/issues/1225): date/version/licence provenance remains independent of scale mechanics.
- [#1226 — extraction contract and validator coverage](https://github.com/JM-Brun/llm-lab/issues/1226): validator indexing, fixtures and changed-file/full-corpus modes.
- [#1233 — evidence-aware cross-domain discovery and decision traceability](https://github.com/JM-Brun/llm-lab/issues/1233): bounded cross-graph queries, evidence paths and discovery tests.
- [#1237 — attention / information theory / compression pilot](https://github.com/JM-Brun/llm-lab/issues/1237): retain as a scientific bridge-quality fixture, not a performance benchmark.
- [#416](https://github.com/JM-Brun/llm-lab/issues/416) and [#418](https://github.com/JM-Brun/llm-lab/issues/418): interactive concept-graph rendering and interaction model.

## 9. Limitations of this audit

- Repository files and implementation were inspected statically; no local benchmark or full test suite was run for this audit.
- Counts are a point-in-time snapshot of canonical files; extraction record/item and bilingual page counts were not recomputed here.
- No x1k/x5k/x10k synthetic load tests have been run.
- No claim is made that the distributed source architecture is already implemented.
- Algorithmic complexity observations are based on inspected code paths, not measured runtime.
- This report assesses information architecture and engineering capacity, not scientific correctness or pedagogical effectiveness.

**Conclusion:** LLM Lab has a credible path to scale without replacing its information model. The next proof is operational: measure the current baseline, complete the already-designed source migration safely, and demonstrate full plus incremental validation and bounded discovery on synthetic workloads before claiming readiness for thousands of sources and hundreds or thousands of concepts.
