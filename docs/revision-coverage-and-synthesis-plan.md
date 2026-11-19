# Revision coverage and synthesis work plan

**Status:** inventory implementation is in PR [#1379](https://github.com/JM-Brun/llm-lab/pull/1379); editorial contract and pilot remain tracked by [#1109](https://github.com/JM-Brun/llm-lab/issues/1109). Build-specific implementation expectations remain coordinated with [#78](https://github.com/JM-Brun/llm-lab/issues/78).

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

### A. Close the inventory PR safely

1. Re-run CI on the latest PR head after the formatting-only correction to `audit_revision_coverage.py`.
2. Confirm the formatting, lint, type-check and full test-suite steps all pass on that exact SHA.
3. Confirm Quarto rendering and secret scanning pass on the same head SHA.
4. Inspect the generated JSON/Markdown artifact and job summary; preserve the report as a reproducible CI output.
5. Review the inventory tests for complete destination coverage, duplicate IDs, route membership preservation, and honest Build route semantics.
6. Merge only after all required checks are green and the PR diff has been reviewed.

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

1. Decide the canonical metadata representation for a revision aid and its source lesson.
2. Use stable page IDs and preserve the distinction between canonical lesson, companion aid, and practice page.
3. Do not overload `related`, `parents`, or `children` with this ownership relation.
4. Validate target existence, destination/type constraints, language pairing, reciprocal or one-way semantics as deliberately chosen, and duplicate/orphan aids.
5. Update the page metadata documentation, parser/index projection, generated graph and tests together.
6. Re-run the inventory so `not_assessed` is replaced only by evidence-backed statuses.

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

Do not mass-create synthesis pages or alter the metadata validator yet. First finish and validate the inventory, inspect existing revision support, agree the typed relation and editorial contract, then pilot the smallest end-to-end path. This sequence avoids duplicate pages, false coverage claims, and a second source of truth.
