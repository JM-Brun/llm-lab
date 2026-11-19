# Revision coverage and synthesis work plan

**Status (2026-11-19):** inventory PR [#1379](https://github.com/JM-Brun/llm-lab/pull/1379) is merged. Its final PR head was `817048ecda141fbf256e42237dc1a4f34bf44a88`; CI, Quarto render and secret scanning passed on that exact SHA. The merge commit is `6f914064a18abbdb6e839c3247139f1295944b55`. Editorial assessment, typed revision links and the learner-facing revision experience remain open under [#1109](https://github.com/JM-Brun/llm-lab/issues/1109). Build-specific implementation expectations remain coordinated with [#78](https://github.com/JM-Brun/llm-lab/issues/78).

**Detailed existing-resource inventory:** [Understand/Build revision-support inventory — 19 November 2026](revision-resource-inventory-2026-11-19.md). This is a read-only structural inventory; it does not prescribe mass creation of new revision sheets.

## 1. Inventory snapshot

The generated CI report for source commit `e7366639b258c83c37fa9606edd643ebe6ab8789` counted every published page whose metadata declares `destination:understand` or `destination:build`.

| Destination | Published pages | French | English |
|---|---:|---:|---:|
| Understand | 46 | 23 | 23 |
| Build | 16 | 8 | 8 |
| **Total** | **62** | **31** | **31** |

Understand route membership in this snapshot:

- 40 core memberships;
- 6 optional memberships;
- no published Understand page was reported as unrouted.

Memberships are counted separately from distinct pages: a page may occur in more than one route stage. The inventory retains all memberships rather than flattening the route to a single position.

Build is discovered from the published destination metadata. The inventory deliberately does not infer a linear implementation order from filenames, sidebar order, or topic names.

The report found equal French and English page counts for every observed `topic` within each destination: 23 Understand topic groups and 8 Build topic groups, each with one page per language in this snapshot. This is a structural parity signal only. It does not establish equivalent learning outcomes, content quality, completeness, or translation fidelity.

## 2. What the inventory currently measures

The generator `site/tools/audit_revision_coverage.py` reuses existing project sources rather than maintaining a second curriculum registry. Its topic diagnostics exclude blank/missing topics, report unexpected language values, and expose per-language multiplicity without treating multiple pages under one topic as duplicates:

- the published Quarto page index and page metadata;
- `data/guided-route.yml` for Understand route memberships;
- `data/concepts.yml` for explicit concept-to-page links;
- `data/resources.yml` for implementation-resource references.

For each page it projects stable page ID, language, destination, topic, type, level, title and URL, route memberships/status, page-graph edges, concept IDs, implementation-resource IDs, and synthesis status.

The CI workflow generates JSON and Markdown reports, appends the Markdown report to the job summary, and uploads both files as an artifact. The report is an auditable projection; it is not a new source of truth.

### Important limits

- `synthesis_status: not_assessed` means the metadata model does not yet provide a typed relation from a synthesis/revision aid to its canonical lesson. It does **not** mean that the page has no synthesis content.
- Generic `related` edges must not be interpreted as synthesis ownership.
- Topic parity currently compares counts grouped by topic. It is not a semantic bilingual review and should not be presented as proof of equivalence.
- Missing topic metadata is reported explicitly and excluded from bilingual topic aggregation; unexpected language values are also reported.
- Concept/resource counts indicate explicit registry links only; zero links do not automatically mean a page is deficient.

## 3. Remaining work, in the required order

### 1. Formalize the contract and verify validator compatibility — documented proposal

The [revision-resource contract](revision-resource-contract.md) is documented in [PR #1388](https://github.com/JM-Brun/llm-lab/pull/1388) and its integrated-section correction in [PR #1391](https://github.com/JM-Brun/llm-lab/pull/1391).

The proposal distinguishes:
- integrated sections, identified by explicit heading or Quarto block anchors;
- companion Quarto pages;
- non-page resources;
- roles (synthesis, flashcards, revision_sheet) and statuses (not_assessed, assessed, not_applicable).

The compatibility audit is documented. The existing page metadata validator does not yet validate or normalize the optional revision object, and the resource validator still accepts only kind: implementation. The contract remains a proposal, not an approved schema migration. Do not change the validators or migrate the 62 historical page records until the model and constraints have been reviewed.

### 2. Inventory existing Understand and Build resources — complete

The read-only inventory is documented in [revision-resource-inventory-2026-11-19.md](revision-resource-inventory-2026-11-19.md), merged in [PR #1395](https://github.com/JM-Brun/llm-lab/pull/1395).

It covers 46 Understand and 16 Build pages and distinguishes:
- 35 one-minute recap callouts and six additional takeaway sections;
- 20 self-check blocks;
- four integrated Build revision-sheet callouts;
- two existing bilingual companion revision-sheet page pairs outside the 62-page population;
- 162 concept-page associations and ten implementation-resource associations.

No mass creation of revision pages or flashcards is part of this inventory.

### 3. Implement non-page resource and revision relation adapters — complete

The read-only adapters were merged in [PR #1394](https://github.com/JM-Brun/llm-lab/pull/1394). ProjectIndex now adapts non-page resource records and page/resource and concept/resource associations, plus typed revision edges with section, page and resource targets.

The adapter is separate from the existing page graph families. It does not change the page metadata schema, either validator, the resource registry, or any of the 62 pages. No current page declares a revision object, so the real repository currently has no typed revision edges; all 62 remain not_assessed.

### 4. Add inverse queries and test them on the real repository — implemented in this PR

`ProjectIndex` now exposes deterministic inverse queries for page↔non-page-resource and concept↔non-page-resource associations: `resources_for_page`, `pages_for_resource`, `resources_for_concept` and `concepts_for_resource`. Unknown IDs fail explicitly; results use stable ID ordering. Tests cover synthetic fixtures, empty associations, invalid IDs, and round-trip reconciliation of all five resources and ten page/resource associations on the real repository.

The existing revision relation queries remain bidirectional and separate from ordinary page graph edges. The real repository continues to contain four revision edges and the same eight explicit support assessments.



Add deterministic queries for:
- pages using a non-page resource and resources used by a page;
- resources linked to a concept and concepts linked to a resource;
- revision targets declared by a source page;
- source pages that target a companion page or non-page resource;
- page-local section targets, keyed by both page ID and anchor.

Tests must use the real repository as well as synthetic fixtures. Reconcile the five current resources and ten page/resource associations in both directions, verify the current absence of typed revision edges, and cover all three target types with synthetic examples. Keep relation families distinct and return stable, deterministic ordering.

### 5. Define the metric registry, then build the coverage matrix — next

Define a canonical metric register before generating the matrix. Each metric must state its stable ID, definition, counting unit, canonical source, source path/schema version, filters, inclusion/exclusion rules, bilingual grouping, deduplication rule, missing-value semantics and tests.

Then construct a coverage matrix from the query layer. Keep page records, logical bilingual topics, route memberships, concepts, non-page resources, revision support, sources/evidence, practice and Build evidence as separate dimensions. Distinguish present, missing, not_applicable, not_registered and needs_review; do not collapse them into an opaque score or infer a defect from an unregistered association.

### 6. Add diagnostics, and only then interfaces

Implement deterministic, read-only diagnostics from the validated metric and coverage layers. Each finding must include a rule ID, severity, source path, stable entity IDs, supporting evidence and a suggested review action. Keep editorial sufficiency separate from relationship existence.

Only after diagnostics are stable, add the CLI, JSON and review-friendly Markdown/CSV outputs, then a dashboard or site interface. All interfaces must consume the same query and diagnostic results rather than reimplementing counts or relationship semantics.

### Deferred editorial and learner-facing work

After the technical sequence above:
- assess the actual sufficiency, correctness, accessibility and bilingual equivalence of the existing recaps, self-checks and Build callouts;
- pilot a small representative set before creating any new revision aid;
- choose the lightest format per page and avoid duplicating existing companion sheets;
- generate the learner-facing “Réviser” experience from the canonical relation and the Understand route;
- keep issue #1109 open until the editorial contract, pilot, assessed coverage and learner-facing experience are complete.

For Build-specific revision expectations, continue coordinating with [issue #78](https://github.com/JM-Brun/llm-lab/issues/78). A revision sheet does not demonstrate that the learner can implement the system unaided.

## 4. Acceptance criteria for completion

The work is complete only when:

- the inventory covers every published Understand/Build page exactly once per page ID;
- route memberships and explicit concept/resource edges are projected without guessing;
- missing metadata and bilingual counterpart gaps are explicit and tested;
- every in-scope page has an individually assessed revision status;
- each page has a sufficient revision aid or a justified documented exception;
- every companion aid has a validated typed link to its canonical source;
- the learner-facing revision route is generated from canonical metadata, bilingual, accessible, and tested;
- CI keeps the inventory and coverage report current;
- the editorial and technical decisions are documented in the relevant issue(s).

## 5. Current decision

The contract and inventory are documented, the read-only ProjectIndex adapters and inverse queries are implemented, and real-repository round-trip tests cover all current non-page resource associations. The contract remains a proposal: the page metadata validator and resource validator are unchanged, and none of the 62 pages has been migrated. The next task is the metric register and coverage matrix, followed by diagnostics and interfaces. Do not mass-create revision content or change the schema/validators ahead of that sequence and an explicit contract review.
