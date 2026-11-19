# Revision coverage and synthesis work plan

**Status (2026-11-19):** inventory PR [#1379](https://github.com/JM-Brun/llm-lab/pull/1379) is merged. Its final PR head was `817048ecda141fbf256e42237dc1a4f34bf44a88`; CI, Quarto render and secret scanning passed on that exact SHA. The merge commit is `6f914064a18abbdb6e839c3247139f1295944b55`. Editorial assessment, typed revision links and the learner-facing revision experience remain open under [#1109](https://github.com/JM-Brun/llm-lab/issues/1109). Build-specific implementation expectations remain coordinated with [#78](https://github.com/JM-Brun/llm-lab/issues/78).

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

## 3. Remaining work, in dependency order

### A. Close the inventory PR safely — completed

PR #1379 is merged. On final head `817048ecda141fbf256e42237dc1a4f34bf44a88`, the repository CI, Quarto render and secret-scanning checks all passed. The CI run covered inventory generation, tests, formatting, lint and type checks; the Quarto run covered rendering, bilingual page/concept navigation and local links; the secret scan included repository history. The merge commit is `6f914064a18abbdb6e839c3247139f1295944b55`.

The generated artifact reported 62 published pages in scope (46 Understand, 16 Build), with 31 pages per language. Understand had 40 core and 6 optional route memberships and no unrouted page. These are inventory facts, not editorial coverage claims.

### B. Harden the inventory diagnostics

1. Report pages with absent or invalid `topic` explicitly; do not aggregate them into a synthetic shared topic.
2. Compare the French and English topic sets, not only counts for topics that happened to occur.
3. Flag missing counterparts, multiple pages per topic/language, and unexpected language values separately. Multiple pages in one topic are not automatically duplicates.
4. Keep count parity clearly labelled as structural; do not claim semantic parity.
5. Add tests for missing topics, missing counterparts, topic multiplicity, unexpected language values, and empty destinations.
6. Keep the inventory deterministic and derived from the existing registries and page index.

### C. Define and apply the synthesis editorial contract

Before mass-editing lessons, inspect the 62 pages and classify existing revision support individually:

- integrated recap already present and sufficient;
- dedicated companion synthesis exists;
- flashcards or retrieval questions exist but do not yet provide a sufficient synthesis;
- partial or outdated revision support;
- no revision support;
- not applicable, with a documented reason.

A synthesis should let a learner recover the lesson's essential structure quickly without rereading the full page. For an Understand lesson, assess: central question, essential concepts and distinctions, explanatory mechanism, indispensable equations or diagrams, concise mental model, common misconceptions/limits, retrieval prompts, and links to the full lesson and practice.

For Build, coordinate with #78. A useful revision aid should capture the implementation step's purpose, prerequisites, interfaces and tensor shapes, algorithm, invariants, commands/entry points, tests and expected outputs, common errors, and limitations. A revision sheet does not demonstrate that the learner can implement the system unaided.

Choose the lightest suitable format per page: an integrated synthesis section, a companion revision sheet, flashcards, or a justified exception. Do not create a separate page by default if a well-structured integrated synthesis already meets the contract.

### D. Introduce a typed source-to-synthesis relation

A candidate contract has been documented in #1109: one-way `revision_of` from an aid to one or more canonical source lessons; derive the reverse lesson→aids index rather than storing both directions. Keep this separate from `related`, `parents` and `children`.

Implementation findings from source inspection:

- `page_index.PublishedPage.metadata` already retains the raw page-map dictionary. It does not need a new field merely to carry `revision_of`.
- `check_page_metadata.py` must validate and preserve `revision_of` in its own normalized page projection, then validate targets against published pages and eligible lesson types.
- `check_resource_registry.py` currently accepts only `kind: implementation`; its `referenced_by` relation means page→resource and must not be reused for resource→lesson ownership.
- `audit_revision_coverage.py` must index published aid pages before limiting its output records to Understand/Build lessons.

Before implementing non-page revision aids, decide whether the resource registry should gain a distinct `kind: revision-aid` with its own required fields, or whether such aids warrant a separate registry. Do not make implementation resources appear as revision aids. The validator should receive published-page descriptors (ID, language, destination, type, status), not only a set of IDs, to enforce target eligibility and language compatibility.

Remaining steps:

1. Approve the page-map and resource representation, including the non-page resource-kind decision.
2. Add tests for page→page and (if adopted) resource→page links, multi-source links, bilingual compatibility, unknown/unpublished/ineligible targets, self-links and duplicates.
3. Implement validators and inventory projection without changing generic graph relations.
4. Generate reverse links and aid diagnostics; keep editorial sufficiency assessment separate from link existence.
5. Re-run CI and verify the machine-readable inventory.

### E. Pilot before scaling

1. Select a small but representative sample across Understand and Build, including both languages and different page types.
2. Produce the revision aids in French and English, linked to the canonical pages.
3. Review accuracy against the lesson, usefulness for rapid recall, accessibility, length, navigation, and bilingual equivalence.
4. Check that the aid adds value rather than duplicating the lesson verbatim.
5. Revise the editorial contract and templates from pilot findings before extending to all pages.

### F. Build the learner-facing “Réviser” experience

1. Generate the revision index from the same canonical page metadata and typed relation; do not create a parallel hand-maintained list.
2. Preserve the canonical Understand route order and any deliberately defined Build sequence/dependencies. Do not invent Build ordering.
3. Provide filters or grouping by destination, topic, concept, and language only where the underlying metadata supports them.
4. Link each aid to its full lesson, relevant exercises, concepts, and implementation resources.
5. Keep French and English experiences aligned and ensure missing aids are visible as coverage gaps rather than silently omitted.
6. Add route, link-integrity, ordering, accessibility, and bilingual coverage tests.

### G. Maintain coverage continuously

1. Make every new Understand/Build page declare whether and how it is supported for revision.
2. Make CI detect new pages without an assessed synthesis status once the typed relation is introduced.
3. Publish counts and exceptions in the CI summary and retain machine-readable output.
4. Re-run the audit after page moves, splits, merges, translations, or route changes.
5. Keep #1109 open until the editorial contract, pilot, metadata relation, coverage review, and learner-facing experience are complete.

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

The inventory is complete and merged. Do not mass-create synthesis pages or change the metadata schema until the editorial contract and typed relation are approved. Continue the page-by-page Understand audit and close the pilot decision first. The relation proposal is sufficiently concrete to write tests once the resource representation is settled, but it is not yet an implemented repository contract. This sequence avoids duplicate pages, false coverage claims, and a second source of truth.
