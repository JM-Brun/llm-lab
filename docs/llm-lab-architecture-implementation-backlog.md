# LLM Lab architecture — implementation backlog and session handoff

**Status:** documentation baseline created; implementation work below remains to be verified or completed  
**Date:** 2026-11-23  
**Parent architecture:** [LLM Lab knowledge and learning ecosystem architecture](llm-lab-knowledge-learning-architecture.md)

This document translates the architecture into bounded work. It is deliberately not a claim that every item is missing: existing contracts, code and open issues must be inspected before duplicate work is created. Update this handoff as tasks are completed, superseded or linked to existing issues/PRs.

## 1. Audit boundary and confidence

The review inspected the current main-branch documents and representative canonical files, including README.md, information-architecture.md, knowledge-architecture-interoperability.md, project-intelligence-layer.md, content-section-mapping.md, the revision contract, calendar redesign/handoff and computational-spine documentation.

It did not execute the full test suite, render the complete site, inspect every page/activity/source record, or exhaustively enumerate every issue and PR. Statements below distinguish:
- **documented foundation:** a canonical file or tool is known to exist;
- **known gap:** a source document explicitly marks the feature proposed, deferred or incomplete;
- **audit required:** implementation may have advanced and must be checked before work is opened;
- **future capability:** intentionally not yet required until real content justifies it.

Do not treat “not found in this bounded review” as proof of absence.


## 1.1 Verified implementation update — 2026-11-23

The following work has been checked against current `main` and the cited merged PRs. This snapshot supersedes earlier statements that these components were only planned.

| Area | Verified implementation | Remaining boundary |
|---|---|---|
| Page/resource migration inventory | PR #1550 exports page metadata, 760 incident page-graph edges, direct associated-page/resource closure, route memberships and typed revision-aid links from the existing ProjectIndex. Its generated schema-v5 baseline reports zero unresolved associated page/resource IDs. | This is not a complete audit of every registry or proof of pedagogical completeness. |
| Understand/Review navigation | PR #1549 projects the 20 core lessons in canonical route order and a peer Review sidebar from `guided-route.yml` and `lesson_contracts`. | #1541 still owns full route equivalence, optional revision support, peer navigation and rendered validation. |
| Revision relations | ProjectIndex validates page-aid role, target existence, eligible lesson destination, language compatibility, duplicate targets and assessment evidence; it builds both aid→lesson and lesson→aid indexes. | The separate revision-resource contract and page-metadata validator still need reconciliation with this implementation. Do not assume the validator enforces every field merely because ProjectIndex reads it. |
| Cross-graph evidence queries | PR #1535 adds opt-in source/extraction/computation/route-focus loading, typed concept paths, explicit gaps and a JSON CLI. Tests cover five real concepts, exact locators, caveats, candidate boundaries and opt-in loading. | This is a bounded query projection, not a universal graph, full claim-level provenance model or complete graph-family inventory. |
| Source collection membership | #1306 reports 142 sources, 100 extraction files and 520 items at commit `14d8c7e`; 44 sources have explicit collection decisions and 98 remain undecided. | Human-reviewed membership decisions remain incomplete; do not infer them from tags or filenames. |
| Practice | #1512 reports 45 dedicated exercise pages in each language and documents the visible companion-link rule. | Full bilingual lesson-by-lesson audit of visible links, return links, embedded prompts and semantic parity remains open. |
| Calendar | PR #1551 establishes the independent-story editorial direction; PRs #1539 and #1546 implement the bilingual landing page and days 01–03, plus post-merge artifact/accessibility fixes. | CI/browser revalidation, novice testing and the 03/09/21 content pilot remain release gates. |

**Counting and evidence rule:** a resolved reference proves structural integrity only. It does not prove that a concept is sufficiently explained, that an extraction supports a scientific claim, that a practice page is pedagogically equivalent, or that an editorial collection is complete.

## 2. Priority summary

| Priority | Workstream | Outcome |
|---|---|---|
| P0 | Reconcile architecture documentation and status | One accurate entry point; no stale claims |
| P0 | Inventory and audit canonical registries | Verified ownership, IDs, relations and migrations |
| P1 | Revision model | Enforced aid-to-lesson relations and honest coverage status |
| P1 | Practice model | Stable activity identities and explicit links without bloating lessons |
| P1 | Cross-graph interoperability | Consistent relation contracts and referential validation |
| P1 | Calendar/collection model | Reusable edition model independent of Understand |
| P1 | Project intelligence | Explainable multi-system coverage diagnostics |
| P2 | Build/resource model expansion | Add resource kinds only when concrete use cases require them |
| P2 | Learner-facing projections | Accessible cross-system discovery and useful views |
| Continuous | Bilingual, scientific, visual and maintenance QA | Preserve quality as the corpus grows |

## 3. Work packages

### P0 — Reconcile architecture documentation and status

- [ ] Link the ecosystem architecture and backlog from docs/information-architecture.md, README and relevant documentation indexes.
- [ ] Reconcile README claims about the advent calendar with the merged 2026 editorial redesign and actual published Quarto files. README currently describes the old manifest as a future, unpublished experience; that statement is stale relative to the 2026-11-23 redesign decision and published prototype.
- [ ] Reconcile the calendar row in docs/information-architecture.md with the superseded status of the old manifest and the new independent-story model.
- [ ] Review architecture documents for claims now stale after recent PRs; update only with verified evidence.
- [ ] Keep a clear status vocabulary: implemented, partially implemented, proposed, deferred, superseded and not assessed.

**Acceptance:** links resolve; README, architecture index and calendar handoff describe the same state; no superseded manifest is presented as the canonical new calendar model.

### P0 — Verify the shared knowledge foundation

- [ ] Inventory every concept, domain, page, resource and source registry, including ID counts and references. **Partial baseline now exists:** #1550 covers page/resource closure and route membership; #1306 covers source/extraction/collection counts. The concept/domain relation review and historical/editorial registry reconciliation remain.
- [ ] Check concept IDs, bilingual labels/definitions, aliases, domain membership and page associations.
- [ ] Review every concept relation's direction, family, inverse/symmetry, transitivity, acyclicity and rationale against its actual meaning.
- [ ] Verify page IDs and FR/EN counterparts; identify orphan pages, duplicate identities and broken references.
- [ ] Confirm the distinction between page-level domain, concept domains, topic tags and source taxonomy in validators and author guidance.
- [ ] Verify generated maps/JSON-LD remain deterministic projections, not editable sources.
- [ ] Record an explicit baseline and route each concrete defect to an existing issue or a small new issue.

**Acceptance:** registry inventory report, referential-integrity checks and reviewed exception list; no taxonomy migration without evidence.

### P1 — Complete the revision system

- [ ] Reconcile docs/revision-resource-contract.md with metadata actually used by revision pages.
- [ ] Decide the canonical declaration location for page-based aids and non-page aids; preserve separate page/resource ID namespaces.
- [ ] Reconcile the existing ProjectIndex revision checks with the owning page-metadata validator and the proposed revision-resource contract. ProjectIndex already checks role vocabulary, target existence, eligible destination, language pairing, duplicate targets and assessment evidence; the validator/contract alignment is not yet established.
- [x] Generate reverse lesson-to-aids indexes rather than authoring both directions: ProjectIndex builds aid→lesson and lesson→aid indexes and exposes both query directions. Reader-facing completeness remains under #1541.
- [ ] Keep link existence separate from coverage sufficiency; preserve not_assessed as a valid state.
- [ ] Audit Understand and Build lessons for revision coverage without automatically declaring every lesson deficient.
- [ ] Keep detailed questions/exercises in Practice; revision questions should have a clear retrieval/reconstruction purpose.
- [ ] Add tests for many-to-many links, invalid targets, duplicate edges, bilingual pairing and generated indexes.

**Acceptance:** one enforced contract, inventory report and tests; every published relation resolves to a real lesson/aide and every coverage judgement has evidence.

### P1 — Formalize Practice & Experiment

- [ ] Inventory existing practice pages, exercises, questions, coding tasks and experiment reports.
- [ ] Define the minimum activity record: stable ID, kind, language, content location, expected outcome/evidence, solution/hints where applicable, status and references.
- [ ] Define explicit activity-to-concept and activity-to-lesson relations; add skills or resource links only where useful.
- [ ] Preserve the editorial rule: lesson pages link to dedicated practice pages and do not accumulate large exercise banks.
- [ ] Separate retrieval questions, conceptual questions, mathematical exercises, coding tasks, experiments and transfer projects.
- [ ] Decide whether an activity registry is justified by the inventory; do not create one solely for architectural symmetry.
- [ ] Build one pilot topic (preferably an already audited topic such as Q/K/V or tokenization) and measure authoring/maintenance overhead.
- [ ] Add validators and a generated practice index only after the pilot demonstrates value.

**Acceptance:** a pilot with stable IDs, explicit concept/lesson links, learner-usable navigation and no duplicated lesson content; documented decision on registry scope.

### P1 — Define cross-graph interoperability

- [ ] Inventory graph families and current owners: semantic, page, pedagogical, revision, practice, build, computational, source/provenance, editorial and historical.
- [ ] For each relation family, document source/target kinds, direction, purpose, inverse/symmetry, transitivity, cycle policy, evidence and learning-order eligibility.
- [ ] Define shared ID resolution without imposing a universal node/edge schema that erases domain semantics.
- [ ] Add a read-only graph inventory describing each graph's owner, schema/version, node and edge kinds, projection and validator.
- [x] Add a bounded opt-in adapter and typed query paths over existing source/extraction, computational, route-focus, page and resource associations (PR #1535); preserve explicit gaps and relation provenance. Broader coverage of all graph families and validators remains open.
- [ ] Preserve the computational spine's distinction between the shared predictive distribution and generation/scoring/training branches.
- [ ] Verify the conceptual/computational distinction inside Transformer blocks: Q/K/V are projections of block input states, not a stage after final contextualized representations.
- [ ] Test that pedagogical routes are not silently generated from generic semantic or computational edges.

**Acceptance:** graph inventory and cross-reference validator; tests demonstrate that one concept can be referenced by several graph families without conflating edge semantics.

### P1 — Generalize editorial collections and calendar editions

- [ ] Reconcile the published 2026 calendar prototype with the new independent-story editorial decision.
- [ ] Complete the inventory/migration map required by docs/advent-calendar-next-steps.md.
- [ ] Decide the minimal collection/edition/story metadata based on the 2026 pilot; do not build a generic publication CMS.
- [ ] Define how stories reference canonical concepts, sources, pages and optional practice resources.
- [ ] Ensure a story is independently readable; editorial order is not a hard prerequisite graph.
- [ ] Keep annual edition-specific theme, dates, selection and editorial navigation separate from shared concept/domain data.
- [ ] Build and visually validate one pilot story/template in FR and EN before migrating a whole calendar.
- [ ] Decide how historical editions are archived and discovered without competing with the current edition.
- [ ] Only then create a 2027 edition manifest.

**Acceptance:** one end-to-end pilot edition/story with validated metadata, sources, bilingual parity, accessible navigation and archive strategy.

### P1 — Strengthen Project Intelligence

- [x] Re-read current ProjectIndex, coverage matrix, query CLI, metric registry and recent PRs before extending them (2026-11-23 audit).
- [x] Validate the read-only ProjectIndex and opt-in evidence adapter against real repository data; PR #1535 tests five real concepts and explicit gap behavior. Full matrix/report integration is still pending.
- [ ] Define explicit coverage states: present, absent, not assessed, not applicable and stale.
- [ ] Distinguish structural presence from pedagogical sufficiency and scientific quality.
- [ ] Add explainable diagnostics for concept coverage across Understand, Review, Practice, Build and Deepen.
- [ ] Integrate the existing opt-in evidence projection into a separate evidence-path report where useful; do not relabel source mappings as scientific support. The current concept matrix and `report_project_index.py` still use the lightweight index and report Build, computation, sources and Practice as unregistered.
- [ ] Add computation-to-concept/page/resource mapping diagnostics.
- [ ] Add provenance completeness diagnostics from source → extraction/claim → concept/page/artifact.
- [ ] Add editorial duplication/complementarity diagnostics for calendar stories.
- [ ] Ensure every finding reports exact supporting records/relations and never infers a missing relation from tag overlap.
- [ ] Benchmark runtime and maintenance cost before scaling to larger corpora.

**Acceptance:** reproducible report with evidence paths, explicit unknown states and tests; no automatic metadata mutation.

### P2 — Expand resources only when justified

- [ ] Inventory concrete non-page artifacts beyond existing implementation modules.
- [ ] Consider datasets, notebooks, experiments, test suites, visual assets, documents or media only when stable artifacts and consumers exist.
- [ ] Preserve page/resource ID namespaces and bilingual page references.
- [ ] Define lifecycle, provenance, licence and location fields per kind where needed.
- [ ] Keep code artifacts and learner activities distinct even when an exercise links to a module.
- [ ] Extend JSON-LD or map projections only when a new resource type has a meaningful public representation.

**Acceptance:** each new kind has at least one real artifact, one consumer, a schema, validation and provenance/licence handling.

### P2 — Improve learner-facing discovery

- [ ] Identify reader questions current navigation cannot answer.
- [ ] Add cross-experience views only when backed by validated relations (for example, revise this concept, practice this mechanism, inspect its implementation).
- [ ] Keep the main Understand route uncluttered; place growing exercise banks in Practice and optional depth in Deepen.
- [ ] Provide text/list alternatives for interactive graphs and ensure keyboard/mobile usability.
- [ ] Audit visible metadata leakage, duplicate breadcrumbs, broken links and inconsistent FR/EN structures.
- [ ] Validate visual changes with desktop/mobile captures and keyboard interaction, not render success alone.

**Acceptance:** reader tasks can be completed from relevant pages; no new navigation layer duplicates an existing one.

### Continuous — Quality, provenance and maintenance

- [ ] Preserve source citations and licence checks when integrating external material.
- [ ] Do not remove third-party visuals solely because rights are uncertain; record and resolve asset-level status.
- [ ] Keep French and English claims, equations, caveats, exercises and navigation structurally equivalent.
- [ ] Validate equations and mathematical notation in rendered pages.
- [ ] Maintain source scans, extraction records and synthesis links as the catalogue evolves.
- [ ] Prefer shared validators and a small number of meaningful CI workflows; never create one workflow per concept.
- [ ] Record maintenance effort and failure modes in pilots before claiming scalability.
- [ ] Keep the project self-contained and avoid private-repository dependencies.

## 4. Recommended execution sequence

1. Reconcile documentation/status and produce a verified registry inventory.
2. Finish the revision contract, because lesson-to-revision relationships are already in active use.
3. Run a bounded Practice pilot using existing content; decide whether an activity registry is warranted.
4. Specify graph-family interoperability and implement read-only cross-reference validation.
5. Finish one 2026 calendar story pilot and use it to derive the minimal collection/edition model.
6. Extend Project Intelligence to produce explainable cross-experience coverage diagnostics.
7. Add new resource kinds and reader-facing views only when pilots show a concrete benefit.

Do not launch all workstreams in parallel. Avoid broad metadata migrations before inventories and validators exist.

## 5. Session-start checklist

At the beginning of a future implementation session:

1. Read this backlog and the parent architecture.
2. Inspect current main, open PRs and related issues; identify merged work since this document's date.
3. Reuse existing issues and skills; do not create duplicates.
4. Confirm actual files/schema and run the smallest relevant tests before editing.
5. Make one coherent change set with tests and documentation.
6. Update this backlog with completed work, evidence, PR/issue links and remaining limitations.

## 6. Definition of done for the architecture program

The architecture program is not complete merely because graph families have names or concepts have tags. It is complete when canonical owners and stable IDs are documented and validated; specialized models have explicit semantics and useful consumers; cross-system references are resolvable and tested; generated projections are deterministic and accessible; unknown/unassessed states are represented honestly; bilingual content and provenance remain intact; pilots demonstrate pedagogical value without excessive maintenance burden; and the site remains self-contained and understandable without its internal metadata.
