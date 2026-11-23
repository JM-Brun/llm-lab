# LLM Lab architecture — implementation backlog and session handoff

**Status:** canonical inventory reconciled in this branch; specialist implementation and learner-validation work remains  
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

This snapshot is reconciled against current `main`, the cited merged PRs, current specialist issues, and the open Q/K/V practice pilot. It supersedes the initial architecture-only status table.

| Area | Canonical owner / verified implementation | Current maturity and remaining boundary |
|---|---|---|
| Concepts and domains | `data/concepts.yml`, `data/domains.yml`; `check_concept_registry.py`; concept registry tests; typed relation metadata and generated learning-map/export views. | Implemented and validated at registry level. Full manual review of every relation's scientific/pedagogical rationale and every rendered consumer remains with #416 and its successors. |
| Pages and navigation | `LLM-LAB-PAGE-MAP v1` in bilingual Quarto pages; `check_page_metadata.py`; page index and ProjectIndex. PR #1550 exports the affected page-graph closure, route memberships and typed revision links. | Structural inventory reports 760 page-graph edges in the affected Understand/Build neighbourhood, 184 associated page records, 5 non-page resources, 102 associated concept IDs and zero unresolved associated page/resource IDs. These are scoped inventory counts, not global page/edge totals or pedagogical quality measures. |
| Understand route | `data/guided-route.yml` and `lesson_contracts`; nine stages and 20 core lesson identities per language. | Canonical source and structural tests are implemented. PR #1549 flattened the bilingual Understand sidebar in canonical order and moved optional material to Deepen. |
| Review route | Same `guided-route.yml` plus `lesson_contracts` and typed page-aid relations; generated bilingual review-path and peer sidebar. | Core peer route is implemented. #1541 remains open for optional revision stops, a complete visual-recall/flashcard inventory, rendered desktop/mobile/keyboard review and learner validation. |
| Revision relations | Page-map `revision_role`, `revision_of` and lesson `revision_support`; `ProjectIndex._load_revision_relations`; `audit_revision_coverage.py` is invoked by CI and emits a report/artifact. | Page-based aid→lesson edges and reverse indexes are implemented. The latest CI artifact inventories 46 Understand pages and 16 Build pages; all 62 have an explicit `integrated_sufficient` assessment with section evidence. It reports 50 typed aid links across 40 pages; 6 Understand pages have no page aid but declare integrated support, while all 16 Build pages rely on integrated support. `check_page_metadata.py` does not itself validate these fields; the CI-invoked ProjectIndex revision audit is the semantic validation boundary. This is a recorded editorial assessment, not independent learner validation. Non-page revision aids remain deferred. |
| Practice & experiment | 45 dedicated exercise pages per language; existing practice catalogue/navigation; page-level related links and explicit heading anchors. #1512 owns the complete lesson↔companion audit. | The Q/K/V pilot is in open PR #1558: bilingual `page_id#anchor` identities, lesson→hub→collection navigation and regression tests. After correcting Ruff SIM300, Python CI, tests, Quarto render/browser audit and secret scanning pass. Browser evidence confirms the Q/K/V lesson and Attention collection render at desktop/mobile with no overflow, zero axe violations and no unrendered math; the nested exercise hub was rendered but has no distinct browser-result record in the targeted report. The full 45-pair visibility/content/parity audit and learner validation remain open. No global activity registry is justified by this pilot. |
| Build | `docs/learning-path.md`, G0–G9 milestones, implementation modules/tests and `data/resources.yml`. | Code/resource identity and module tests exist. There is no single canonical machine-readable cross-graph Build dependency model or complete milestone-to-evidence validator. Do not infer Build dependencies from Understand order. #78 retains ownership. |
| Computation | `data/computational-graph.yml`, canonical computational-spine document, graph validator/tests and rendered Mermaid/JSON projections. | Implemented as a distinct graph. The shared conditional prediction and generation/scoring/training branches remain separate; Q/K/V and attention remain inside each Transformer block. Remaining reader-facing evidence is tracked in #584. |
| Sources and provenance | `data/sources.yml`, `data/extractions/*.yml`, source catalogue validator and source-lineage documentation; opt-in ProjectIndex evidence adapter and `cross_graph_query.py`. | Verified against main tree `534ce3d` on 2026-11-23: 142 unique source records, 100 extraction YAML files, zero extraction filenames absent from the catalogue, and 42 catalogue IDs without a matching extraction filename. A fresh full-corpus atomic-item count was not run; the earlier 489-item figure belongs to the 2026-11-19 / 96-file snapshot and must not be presented as current. Parsing the current source records finds 44 explicit collection decisions (42 non-empty memberships and 2 explicit empty lists) and 98 undecided. These are different queues; neither gap count is an instruction to create empty extractions or infer membership. |
| Historical genealogy | `data/history-pilot.yml`, history validator, renderer and rendered checks. | Bilingual historical projection is implemented. Historical events are not yet traversable through `cross_graph_query.py`; chronology must not be treated as causal influence. |
| Editorial collections | 2026 independent-story editorial contract and bilingual Quarto story sources. PR #1551 approved the redesign; PR #1560 merged the reusable story template, Day 06 FR/EN source drafts, source dossier and original SVG. | Day 06 remains `status:planned` and outside the render list. The pilot has not passed Quarto rendering, desktop/mobile visual review, accessibility or novice review. No generalized edition manifest or membership validator exists; do not create one before pilots pass. |
| Project Intelligence | Read-only `ProjectIndex`; lightweight default and opt-in evidence adapter; coverage/query modules, metric registry and CLI. PR #1535 validates five real concept paths and explicit evidence gaps. | Foundation exists, but the coverage matrix and `report_project_index.py` do not yet integrate all evidence paths or consistently distinguish present, absent, not assessed, not applicable and stale. Historical, Build-dependency and decision-record traversal are not implemented. #1233 owns broader evidence-aware discovery and decision traceability. |
| Linked-data export | Derived JSON-LD from concepts, pages and resources; export tests and rendered checks. | Bounded export only. It is not a serialization of every graph family and does not provide complete claim-level PROV-O provenance. |

**Additional verified registry counts at main `534ce3d` (2026-11-23):** 102 concepts, 12 relation types and 114 typed concept edges; 6 domains; 57 computational nodes, 75 computational edges, 7 branches and 8 named views; 9 Understand stages; 5 non-page implementation resources; 17 historical events and 20 historical source records. Page-level migration counts remain scoped to PR #1550: 184 associated page records, 760 affected page-graph edges, 5 associated non-page resources and 102 associated concept IDs, with zero unresolved IDs. These counts describe distinct registries and projections and must not be added together as if they shared a grain.

**Counting and evidence rule:** resolved references and passing structural validators prove integrity only. They do not prove that an explanation is complete, a source supports a claim, an activity is pedagogically sufficient, or a calendar story is independent and understandable.

**Status vocabulary:** use `implemented and validated`, `implemented; validation incomplete`, `documented/proposed`, `deferred`, `superseded` and `not assessed`. Never use a single “complete” label for source inspection, CI, rendering, accessibility and learner outcomes.

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

- [x] Link the ecosystem architecture and backlog from docs/information-architecture.md and README.
- [x] Reconcile README claims about the advent calendar with the merged 2026 editorial redesign: README now describes the independent-story direction and explicitly says implementation/migration remain.
- [x] Reconcile the calendar row in docs/information-architecture.md with the superseded old manifest and the independent-story model.
- [x] Update the architecture validator matrix with Review, Project Intelligence, PR #1558 and PR #1560 evidence.
- [ ] Recheck the remaining cross-document status statements after this inventory PR is reviewed; keep specialist work in its owning issues.
- [x] Define and use a clear status vocabulary: implemented and validated, implemented with validation incomplete, documented/proposed, deferred, superseded and not assessed.

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

- [x] Reconcile docs/revision-resource-contract.md with the page-map metadata and the CI-invoked ProjectIndex revision inventory; explicitly document that non-page aids are not supported.
- [x] Confirm the canonical declaration location for page-based aids: page-map metadata; keep page IDs separate from resource IDs. Non-page revision aids remain deferred until a real learner-facing artifact is identified.
- [x] Keep the CI-invoked ProjectIndex revision audit as the single semantic validation boundary. `check_page_metadata.py` remains focused on general page-map structure; do not duplicate revision checks without a second demonstrated consumer.
- [x] Generate reverse lesson-to-aids indexes rather than authoring both directions: ProjectIndex builds aid→lesson and lesson→aid indexes and exposes both query directions. Reader-facing completeness remains under #1541.
- [x] Keep link existence separate from coverage sufficiency; preserve not_assessed as a valid state in ProjectIndex and the revision inventory.
- [x] Generate a full Understand/Build revision inventory without treating missing page aids as missing support: 46 Understand + 16 Build pages assessed; all currently declare integrated_sufficient with section evidence. Keep learner/pedagogical review distinct from this metadata state.
- [x] Preserve the editorial boundary: detailed calculations, coding and experiments belong in Practice; Review prompts are for retrieval/reconstruction. Full page-level compliance remains audited under #1512/#1541.
- [x] Add page-based regression tests for many-to-many links, invalid/unpublished/ineligible targets, duplicate targets, bilingual pairing, assessment evidence and derived reverse indexes.

**Acceptance:** one enforced contract, inventory report and tests; every published relation resolves to a real lesson/aide and every coverage judgement has evidence.

### P1 — Formalize Practice & Experiment

- [x] Establish the page-level baseline: 45 dedicated exercise pages per language, with catalogue/render/navigation parity. The activity-by-activity inventory and quality audit remain open in #1512.
- [ ] Define the minimum activity record: stable ID, kind, language, content location, expected outcome/evidence, solution/hints where applicable, status and references.
- [ ] Define explicit activity-to-concept and activity-to-lesson relations; add skills or resource links only where useful.
- [ ] Preserve the editorial rule: lesson pages link to dedicated practice pages and do not accumulate large exercise banks.
- [ ] Separate retrieval questions, conceptual questions, mathematical exercises, coding tasks, experiments and transfer projects.
- [ ] Decide whether an activity registry is justified by the inventory; do not create one solely for architectural symmetry.
- [ ] Complete and review the bounded Q/K/V pilot in PR #1558; record the authoring/maintenance overhead and learner findings before deciding whether a structured activity record is justified.
- [ ] Add validators and a generated practice index only after the pilot demonstrates value.

**Acceptance:** a pilot with stable IDs, explicit concept/lesson links, learner-usable navigation and no duplicated lesson content; documented decision on registry scope.

### P1 — Define cross-graph interoperability

- [x] Inventory graph families and current owners in the architecture matrix: semantic, page, pedagogical, revision, practice, build, computational, source/provenance, editorial and historical. Remaining work is relation-contract completeness, not naming the families.
- [ ] For each relation family, document source/target kinds, direction, purpose, inverse/symmetry, transitivity, cycle policy, evidence and learning-order eligibility.
- [ ] Define shared ID resolution without imposing a universal node/edge schema that erases domain semantics.
- [x] Add a documented read-only graph-family/validator inventory in the architecture matrix; continue to update it as contracts evolve.
- [x] Add a bounded opt-in adapter and typed query paths over existing source/extraction, computational, route-focus, page and resource associations (PR #1535); preserve explicit gaps and relation provenance. Broader coverage of all graph families and validators remains open.
- [x] Preserve the computational spine's distinction between the shared predictive distribution and generation/scoring/training branches (canonical model and projections are integrated under #575/#584).
- [x] Record the conceptual/computational distinction inside Transformer blocks: Q/K/V are projections of each block's input states, not a stage after final contextualized representations.
- [ ] Test that pedagogical routes are not silently generated from generic semantic or computational edges.

**Acceptance:** graph inventory and cross-reference validator; tests demonstrate that one concept can be referenced by several graph families without conflating edge semantics.

### P1 — Generalize editorial collections and calendar editions

- [x] Reconcile the old 2026 calendar prototype with the independent-story editorial decision; preserve the old material as historical and keep the new Day 06 draft source-only.
- [ ] Complete the inventory/migration map required by docs/advent-calendar-next-steps.md.
- [ ] Decide the minimal collection/edition/story metadata based on the 2026 pilot; do not build a generic publication CMS.
- [ ] Define how stories reference canonical concepts, sources, pages and optional practice resources.
- [ ] Ensure a story is independently readable; editorial order is not a hard prerequisite graph.
- [ ] Keep annual edition-specific theme, dates, selection and editorial navigation separate from shared concept/domain data.
- [ ] Render and visually validate the Day 06 story/template in FR and EN, then obtain scientific and novice review before starting the Day 17/23 pilots.
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

1. Merge the current inventory reconciliation after review; keep the verified registry snapshot current.
2. Close the page-based revision validation decision; finish only the remaining contract/route gaps, deferring non-page aids unless a real artifact requires them.
3. Complete the Q/K/V Practice pilot (PR #1558), then continue the bilingual 45-pair audit in bounded batches.
4. Use #1233 to formalize the smallest cross-graph bridge/validation contract; reuse the closed scientific pilot #1237 and existing #512/#416 work.
5. Render and scientifically/visually/novice-validate Day 06; only then consider Days 17 and 23 and a minimal edition model.
6. Extend Project Intelligence with explicit unknown states and evidence-backed diagnostics; do not build a general recommendation engine yet.
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
