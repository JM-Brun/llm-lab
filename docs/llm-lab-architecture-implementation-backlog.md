# LLM Lab architecture — implementation backlog and session handoff

**Status:** canonical inventory reconciled; five-space vocabulary aligned; specialist implementation and learner-validation work remains  
**Date:** 2026-11-26  
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

This is the historical inventory snapshot at main `f820869` (2026-11-23). Its mutable counts are superseded by the direct current-main refresh in §1.4; its implementation and ownership notes remain useful where not superseded.

| Area | Canonical owner / verified implementation | Current maturity and remaining boundary |
|---|---|---|
| Concepts and domains | `data/concepts.yml`, `data/domains.yml`; `check_concept_registry.py`; concept registry tests; typed relation metadata and generated learning-map/export views. | Implemented and validated at registry level. Full manual review of every relation's scientific/pedagogical rationale and every rendered consumer remains with #416 and its successors. |
| Pages and navigation | `LLM-LAB-PAGE-MAP v1` in bilingual Quarto pages; `check_page_metadata.py`; page index and ProjectIndex. PR #1550 exports the affected page-graph closure, route memberships and typed revision links. | Structural inventory reports 760 page-graph edges in the affected Understand/Build neighbourhood, 184 associated page records, 5 non-page resources, 102 associated concept IDs and zero unresolved associated page/resource IDs. These are scoped inventory counts, not global page/edge totals or pedagogical quality measures. |
| Understand route | `data/guided-route.yml` and `lesson_contracts`; nine stages and 20 core lesson identities per language. | Canonical source and structural tests are implemented. PR #1549 flattened the bilingual Understand sidebar in canonical order and moved optional material to Deepen. |
| Review route | Same `guided-route.yml` plus `lesson_contracts` and typed page-aid relations; generated bilingual stage-grouped review plan and peer sidebar. | The review-plan projection exists, but the page is still a plan/sheet index rather than a complete peer traversal. #1541 owns stage/lesson parity, explicit primary revision destinations, optional revision stops, complete visual-recall/flashcard inventory, route switching, rendered desktop/mobile/keyboard review and learner validation. |
| Revision relations | Page-map `revision_role`, `revision_of` and lesson `revision_support`; `ProjectIndex._load_revision_relations`; `audit_revision_coverage.py` is invoked by CI and emits a report/artifact. | Page-based aid→lesson edges and reverse indexes are implemented. The latest CI artifact inventories 46 Understand pages and 16 Build pages; all 62 have an explicit `integrated_sufficient` assessment with section evidence. It reports 50 typed aid links across 40 pages; 6 Understand pages have no page aid but declare integrated support, while all 16 Build pages rely on integrated support. `check_page_metadata.py` does not itself validate these fields; the CI-invoked ProjectIndex revision audit is the semantic validation boundary. This is a recorded editorial assessment, not independent learner validation. Non-page revision aids remain deferred. |
| Practice & experiment | 45 dedicated exercise pages per language; existing practice catalogue/navigation; page-level related links and explicit heading anchors. #1512 owns the complete lesson↔companion audit. | The Q/K/V pilot is documented in [practice-activity-model-pilot.md](practice-activity-model-pilot.md) and merged in PR #1558: bilingual `page_id#anchor` identities, lesson→hub→collection navigation and regression tests. Python quality, test suite, Quarto render/browser audit and secret scanning pass on the final PR head; the targeted browser harness covers nested companion pages, visible return/collection links, the learner-facing self-check heading and keyboard disclosure. The French typographic-apostrophe false negative was fixed and the fresh full-site/browser audit passed. This validates the technical pilot, not learner value or scale. The full 45-pair visibility/content/parity audit and learner validation remain open. No global activity registry is justified by this pilot. |
| Build | `docs/learning-path.md`, G0–G9 milestones, implementation modules/tests and `data/resources.yml`. | Code/resource identity and module tests exist. There is no single canonical machine-readable cross-graph Build dependency model or complete milestone-to-evidence validator. Do not infer Build dependencies from Understand order. #78 retains ownership. |
| Computation | `data/computational-graph.yml`, canonical computational-spine document, graph validator/tests and rendered Mermaid/JSON projections. | Implemented as a distinct graph. The shared conditional prediction and generation/scoring/training branches remain separate; Q/K/V and attention remain inside each Transformer block. Remaining reader-facing evidence is tracked in #584. |
| Sources and provenance | `data/sources.yml`, `data/extractions/*.yml`, source catalogue validator and source-lineage documentation; opt-in ProjectIndex evidence adapter and `cross_graph_query.py`. | Direct read of main `f8e45989` (2026-11-26): 150 source records and 4 declared collection identities. The source file has 50 explicit collection decisions (48 non-empty, 2 explicit empty) and 100 records without a decision. The last independently verified extraction/join snapshot remains #1306 (2026-11-21): 100 extraction YAML files, 520 atomic items, zero extraction filenames absent from the catalogue and 42 catalogue IDs without a matching extraction filename. Do not present those dated extraction/join counts as refreshed for current main. The full-corpus locator-quality audit remains separate. These queues must not be conflated or used to infer missing extractions or collection membership. |
| Historical genealogy | `data/history-pilot.yml`, history validator, renderer and rendered checks. | Bilingual historical projection is implemented. Historical events are not yet traversable through `cross_graph_query.py`; chronology must not be treated as causal influence. |
| Editorial collections | 2026 independent-story editorial contract and bilingual Quarto story sources. PR #1551 approved the redesign; PR #1560 merged the reusable story template, Day 06 FR/EN source drafts, source dossier and original SVG; PR #1563 corrected the math notation and sharpened frequency/source-scope definitions. | Day 06 remains `status:planned` and outside the render list. The pilot has not passed Quarto rendering, desktop/mobile visual review, accessibility or novice review. No generalized edition manifest or membership validator exists; do not create one before pilots pass. |
| Project Intelligence | Read-only `ProjectIndex`; lightweight default and opt-in evidence adapter; concept coverage matrix, Markdown/JSON report and concept-centred `cross_graph_query.py`. PR #1535 validates five real concept paths and explicit evidence gaps. | Partial. The matrix has an explicit state vocabulary (`present`, `missing`, `not_applicable`, `not_registered`, `needs_review`; revision adds `not_assessed`) but does not cover every graph family. Source/computation adapters are opt-in; complete Build/computation/source/Practice concept mappings remain `not_registered`. Diagnostics are limited to bilingual association findings and explicit evidence gaps; a general `stale`/freshness model, history/decision traversal, generic cross-family impact analysis and recommendations are not implemented. #1233 owns broader evidence-aware discovery and decision traceability. |
| Linked-data export | Derived JSON-LD from concepts, pages and resources; export tests and rendered checks. | Bounded export only. It is not a serialization of every graph family and does not provide complete claim-level PROV-O provenance. |

**Historical counts at main `f820869` (2026-11-23), superseded where refreshed below:** 102 concepts, 12 relation types and 124 typed concept edges; 6 domains; 57 computational nodes, 75 computational edges, 7 branches and 8 named views; 9 Understand stages; 5 non-page implementation resources; 17 historical events and 20 historical source records. Page-level migration counts remain scoped to PR #1550: 184 associated page records, 760 affected page-graph edges, 5 associated non-page resources and 102 associated concept IDs, with zero unresolved IDs. These counts describe distinct registries and projections and must not be added together as if they shared a grain.

**Counting and evidence rule:** resolved references and passing structural validators prove integrity only. They do not prove that an explanation is complete, a source supports a claim, an activity is pedagogically sufficient, or a calendar story is independent and understandable.

**Status vocabulary:** use `implemented and validated`, `implemented; validation incomplete`, `documented/proposed`, `deferred`, `superseded` and `not assessed`. Never use a single “complete” label for source inspection, CI, rendering, accessibility and learner outcomes.

## 1.2 Five-space vocabulary reconciliation — 2026-11-26

The architecture now uses one consistent product-level vocabulary:

1. **Main learning path (Understand)** — the guided conceptual route and its attached revision/retrieval resources.
2. **Build from scratch (Build)** — implementation milestones, code, tests and implementation evidence.
3. **Practice & experiment** — dedicated questions, exercises, coding tasks and experiments.
4. **Deepen** — optional, non-linear mathematical, scientific, architectural and research extensions.
5. **Stories** — independent editorial stories and bounded collections/editions.

**Review is not a sixth top-level space.** It is the consolidation/retrieval dimension of the Main learning path. Its specialized aid→lesson relations, coverage assessments and stage-by-stage reader-facing projection remain intact and continue to be owned by #1541. This vocabulary change does not remove the Review projection or weaken its acceptance criteria.

The distinction is intentional:
- **Top-level space** answers where a learner goes and what kind of experience is offered.
- **Route** describes a recommended progression inside a space (for example, the nine-stage Understand route).
- **Resource/revision role** describes material that supports a lesson (for example, a flashcard or synthesis).
- **Projection** is a generated reader-facing view of canonical records (for example, the Review route).

No registry, schema, page metadata migration or navigation rewrite is implied by this documentation alignment. The existing page-based `revision_role`/`revision_of` contract and generated Review route remain revision semantics within the Main learning path; `review` is not a page `destination` value.

## 1.3 Epistemic and pedagogical entity classification — 2026-11-26

The shared-foundation inventory now separates the following roles rather than treating them as interchangeable record types:

- **Concept / notion:** durable, reusable referent owned by `data/concepts.yml`; “notion” is a prose synonym.
- **Idea:** informal umbrella term, not a canonical record kind. Resolve it into a concept, claim, mechanism, derivation, pedagogical contribution, open question, or another explicit extraction kind.
- **Intuition / mental model / analogy:** source-local pedagogical contribution, retained in extraction items and source-local pedagogical models; it is not automatically a concept, claim or evidence.
- **Claim:** attributed proposition retained as a source-scoped extraction item with locator, scope, voice/provenance where needed, evidence fields and separate verification. No general-purpose canonical claim registry is established.
- **Evidence:** material grounding or challenging a claim, retained with type, locator, confidence, scope and provenance. It is distinct from the claim, and citation is not corroboration.
- **Relation:** family-owned typed assertion between identified endpoints. Concept, page, source-local, source-lineage, route, computation, Build, revision and Practice relations keep distinct semantics; no universal edge registry.
- **Pedagogical objective / outcome:** owned by the relevant experience or source reconstruction. Understand objectives/outcomes live in the guided route, Build goals/evidence in the Build path, and source-local outcomes retain `declared`/`inferred` status. None proves learner mastery.

[PR #1712](https://github.com/JM-Brun/llm-lab/pull/1712) merged this classification into `docs/knowledge-architecture-interoperability.md`. The architecture table was aligned in this branch to separate extracted claims from evidence and to avoid assigning aliases/provenance fields to the current concept schema.

**No new registry or schema is justified by this classification.** Remaining specialist boundaries stay with #512 (claim provenance/interoperability), #1233 (typed cross-graph bridges), #416 (concept relation semantics), #1541 (revision route), #1512 (Practice), and #78 (Build). Use the merged classification as the boundary for subsequent work; do not create duplicate tasks or promote source-local records automatically.

## 1.4 Current canonical count refresh — 2026-11-26

Direct reads of the canonical YAML files on main `6eaedf` give the following current record counts. They are structural counts, not quality or completeness scores.

| Canonical owner | Current count | Qualification |
|---|---:|---|
| `data/concepts.yml` | 125 concepts; 147 typed edges; 12 declared relation types | The concept validator remains the semantic integrity boundary; edge review and scientific correctness are separate. |
| `data/domains.yml` | 6 domains | Concept membership is many-to-many classification, not a semantic relation. |
| `data/computational-graph.yml` | 7 branches; 57 nodes; 67 edges; 8 views | The computational graph is distinct from the concept graph and learning route. |
| `data/guided-route.yml` | 9 stages; 20 lesson contracts | The Understand route remains separate from Build dependencies and other graph families. |
| `data/resources.yml` | 5 non-page resources | Current seed remains implementation resources only. |
| `data/sources.yml` | 150 source records | Direct YAML count; extraction coverage has not been refreshed against this expanded catalogue. |
| `data/source-collections.yml` | 4 collection identities | Source records currently contain 50 explicit membership decisions (48 non-empty, 2 explicit empty) and 100 records without a decision. This is a direct field count, not a replacement for #1306's validator/report ownership. |
| `data/history-pilot.yml` | 17 events; 20 source records | Historical pilot, not an exhaustive chronology. |

The last independently verified extraction inventory remains the #1306 snapshot at commit `14d8c7e` (2026-11-21): 100 extraction files and 520 atomic items. It also recorded 42 catalogue IDs without matching extraction files and zero orphan extraction filenames. Since the source catalogue now contains 150 records, those extraction/join counts must be refreshed before being described as current. The locator-quality audit remains a separate gate.

## 2. Priority summary

| Priority | Workstream | Outcome |
|---|---|---|
| P0 | Reconcile architecture documentation and status | One accurate entry point; five top-level spaces and nested revision dimension |
| P0 | Inventory and audit canonical registries | Verified ownership, IDs, relations and migrations |
| P1 | Main-path revision support | Enforced aid-to-lesson relations and honest coverage status, surfaced within the Main learning path |
| P1 | Practice model | Stable activity identities and explicit links without bloating lessons |
| P1 | Cross-graph interoperability | Consistent relation contracts and referential validation |
| P1 | Stories / collection model | Reusable edition model independent of the Main learning path |
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
- [x] Align the product-level vocabulary on five top-level spaces: Main learning path, Build from scratch, Practice & experiment, Deepen and Stories; nest Review/revision under the Main learning path while preserving its specialized contracts and #1541 ownership.
- [x] Separate canonical concepts, source-scoped extracted claims/contributions, evidence/verification and experience-specific pedagogical objectives in the shared-foundation inventory; do not create generic idea, claim, evidence or relation registries.

**Acceptance:** links resolve; README, architecture index and calendar handoff describe the same state; no superseded manifest is presented as the canonical new calendar model; the architecture does not describe Review as a sixth top-level space.

### P0 — Verify the shared knowledge foundation

- [ ] Inventory every concept, domain, page, resource and source registry, including ID counts and references. **Partial baseline now exists:** #1550 covers page/resource closure and route membership; #1306 covers source/extraction/collection counts. The concept/domain relation review and historical/editorial registry reconciliation remain.
- [x] Refresh the atomic-item count from the current 100-file source-coverage report: 520 items (issue #1306, 2026-11-21). Keep the 42 catalogue IDs without extraction filenames distinct from explicit no-extraction dispositions.
- [ ] Run or retrieve a current full-corpus locator-quality audit for all 100 extraction files; the 489-item / 96-file locator audit is historical and must not be extrapolated.
- [ ] Continue the 98 undecided source-collection decisions under #1306 using source-specific evidence; do not infer membership from tags or create empty extraction files.
- [ ] Check concept IDs, bilingual labels/definitions, aliases, domain membership and page associations.
- [ ] Review every concept relation's direction, family, inverse/symmetry, transitivity, acyclicity and rationale against its actual meaning.
- [ ] Verify page IDs and FR/EN counterparts; identify orphan pages, duplicate identities and broken references.
- [ ] Confirm the distinction between page-level domain, concept domains, topic tags and source taxonomy in validators and author guidance.
- [ ] Verify generated maps/JSON-LD remain deterministic projections, not editable sources.
- [ ] Record an explicit baseline and route each concrete defect to an existing issue or a small new issue.

**Acceptance:** registry inventory report, referential-integrity checks and reviewed exception list; no taxonomy migration without evidence.

### P1 — Finalize the page-based revision model

- [x] Reconcile docs/revision-resource-contract.md with the page-map metadata and the CI-invoked ProjectIndex revision inventory; explicitly document that non-page aids are not supported.
- [x] Confirm the canonical declaration location for page-based aids: page-map metadata; keep page IDs separate from resource IDs. Non-page revision aids remain deferred until a real learner-facing artifact is identified.
- [x] Keep the CI-invoked ProjectIndex revision audit as the single semantic validation boundary. `check_page_metadata.py` remains focused on general page-map structure; do not duplicate revision checks without a second demonstrated consumer.
- [x] Generate reverse lesson-to-aids indexes rather than authoring both directions: ProjectIndex builds aid→lesson and lesson→aid indexes and exposes both query directions. Reader-facing completeness remains under #1541.
- [x] Keep link existence separate from coverage sufficiency; preserve not_assessed as a valid state in ProjectIndex and the revision inventory.
- [x] Generate a full Understand/Build revision inventory without treating missing page aids as missing support: 46 Understand + 16 Build pages assessed; all currently declare integrated_sufficient with section evidence. Keep learner/pedagogical review distinct from this metadata state.
- [x] Preserve the editorial boundary: detailed calculations, coding and experiments belong in Practice; Review prompts are for retrieval/reconstruction. Full page-level compliance remains audited under #1512/#1541.
- [x] Add page-based regression tests for many-to-many links, invalid/unpublished/ineligible targets, duplicate targets, bilingual pairing, assessment evidence and derived reverse indexes.

**Acceptance (page-based scope):** one enforced contract, CI inventory report and regression tests; every published relation resolves to a real lesson/aide; all 62 Understand/Build pages have an explicit coverage assessment with section evidence. Non-page revision aids remain deferred until a real artifact requires them. Review-route completeness and learner validation remain under #1541.

### P1 — Formalize Practice & Experiment

- [x] Establish the page-level baseline: 45 dedicated exercise pages per language, with catalogue/render/navigation parity. The activity-by-activity inventory and quality audit remain open in #1512.
- [ ] Define the minimum activity record: stable ID, kind, language, content location, expected outcome/evidence, solution/hints where applicable, status and references.
- [ ] Define explicit activity-to-concept and activity-to-lesson relations; add skills or resource links only where useful.
- [ ] Preserve the editorial rule: lesson pages link to dedicated practice pages and do not accumulate large exercise banks.
- [ ] Separate retrieval questions, conceptual questions, mathematical exercises, coding tasks, experiments and transfer projects.
- [ ] Decide whether an activity registry is justified by the inventory; do not create one solely for architectural symmetry.
- [x] Complete the technical Q/K/V pilot in PR #1558 (merged; CI, Quarto/browser audit and secret scan pass).
- [ ] Record authoring/maintenance overhead and obtain learner findings before deciding whether a structured activity record is justified.
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

### P1 — Generalize Stories collections and calendar editions

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
- [x] Validate the read-only ProjectIndex, concept coverage matrix and opt-in evidence adapter against real repository data; PR #1535 tests five real concepts and explicit gap behavior. Broad Build/computation/source/Practice coverage remains unregistered.
- [x] Define current states for the implemented matrix: present, missing, not_applicable, not_registered, needs_review and (for revision only) not_assessed.
- [ ] Define a distinct stale state only after source freshness and invalidation semantics are specified; do not use absent as a synonym for not_registered.
- [x] Document that structural presence, authored revision sufficiency, source evidence and scientific quality are different claims; no current coverage state is independent learner/scientific validation.
- [ ] Add explainable diagnostics for concept coverage across Understand, Review, Practice, Build and Deepen.
- [x] Implement a separate opt-in concept-centred evidence-path query in `cross_graph_query.py`; it preserves exact evidence and explicit gaps without changing the lightweight concept matrix. The matrix and `report_project_index.py` continue to mark Build, computation, sources and Practice as not_registered where complete concept mappings do not exist.
- [ ] Add computation-to-concept/page/resource mapping diagnostics.
- [ ] Add provenance completeness diagnostics from source → extraction/claim → concept/page/artifact.
- [ ] Add editorial duplication/complementarity diagnostics for calendar stories.
- [x] Ensure current concept-centred evidence paths/gaps and bilingual association findings expose exact supporting records/relations; never infer a missing relation from tag overlap.
- [ ] Extend that evidence contract to future cross-registry diagnostics before making any finding blocking.
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
2. Complete the reader-facing Review route in #1541: turn the current plan/sheet index into a true stage-by-stage peer traversal, verify one primary synthesis destination per core lesson, justify optional revision stops, complete the visual-recall/flashcard inventory, and pass rendered desktop/mobile/keyboard and learner review. The page-based revision validation boundary is already settled; non-page aids remain deferred.
3. Treat the Q/K/V technical pilot (#1558, merged) as the reference implementation; obtain learner review of its eight activities and measure authoring/maintenance overhead, then continue the bilingual 45-pair audit in bounded batches.
4. Use #1233 to formalize the smallest cross-graph bridge/validation contract; reuse the closed scientific pilot #1237 and existing #512/#416 work.
5. Render and scientifically/visually/novice-validate Day 06; only then consider Days 17 and 23 and a minimal edition model.
6. Extend Project Intelligence from the implemented state vocabulary and concept-centred evidence query to owned cross-registry diagnostics, a stale/freshness model and complete coverage mappings; keep recommendations deferred. Refresh the current 100-file extraction item/locator inventory before making scale or provenance-completeness claims.
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


## 5. Current handoff — 2026-11-23

### Active pull requests

- **PR #1567 — registry inventory / Project Intelligence reconciliation:** open on current main. It updates this backlog, the ecosystem architecture/interoperability matrix, relation-edge review status, revision contract, Project Intelligence design and metric registry; it also reconciles the calendar handoff, records the Q/K/V pilot outcome, corrects the source-coverage diagnostic wording and adds a regression test. After the latest documentation edits (head `2d89f69`), CI, Quarto/browser audit and secret scanning have restarted and are pending. Python quality and secret scanning passed on the preceding head, not yet on this final head. Merge only after all required checks pass.
- **PR #1561:** closed as superseded after #1558/#1563 advanced main and caused a merge conflict; its changes were replayed on current main in #1567.
- **PR #1558 — Q/K/V practice pilot:** merged as `4f0302a`. Python quality, test suite, Quarto/browser audit and secret scanning passed on the final head. Learner review and the full 45-pair audit remain separate gates.
- **PR #1523 — companion-link visibility batch:** merged; 20 hidden-only links and 9 mixed visible/hidden cases were reconciled across 29 bilingual page pairs, preserving distinct deep links.
- **PR #1563 — Day 06 mathematical correction:** merged; FR/EN math notation and frequency/source-scope definitions were corrected. The story remains planned and outside the production render list.
- **PR #1560 — Day 06 story/template pilot:** merged. The bilingual source drafts and template remain planned/source-only and outside the render list; publication review is not complete.
- **PR #1553 — ecosystem architecture:** merged. **Issue #575** is closed; residual reader-facing computational-spine review remains in #584.

### Deferred validation commands

The standard CI workflow skips the opt-in full-corpus extraction locator inventory and concept-registry scale benchmark. The last independently verified source-coverage report records 520 atomic items across 100 extraction files (#1306, 2026-11-21). The catalogue now contains 150 source records on main, so refresh extraction coverage, source/extraction joins and locator quality before asserting current corpus totals. Do not reuse the historical 489-item / 96-file locator report.

### Merge and migration guardrails

- Do not merge PR #1567 until the latest test suite and Quarto/browser audit pass; secret scanning and Python quality have already passed. PR #1558 is merged after all required checks passed.
- Do not bulk-migrate page metadata or create a universal graph/registry.
- Keep source membership, revision sufficiency, scientific evidence and learner outcomes as distinct assertions.
- Update this dated handoff when CI/PR states change; the specialist issues remain the source of truth for their detailed acceptance criteria.


## Backlog reconciliation — 2026-11-27

This is a bounded operational refresh, not a new roadmap or a claim that every open issue has been re-reviewed line by line.

### Repository-level snapshot

- The open-issue search was partitioned by creation period to avoid the 100-result search cap: 0 issues created before October 2026, 8 in October, 91 from 1–26 November, and 4 on 27 November (103 open issues returned across the disjoint periods).
- The only open PR identified in the preceding snapshot, #1770, was merged on 2026-11-27. No open PR was returned by the subsequent open-PR search.
- The initial no-label sweep identified 25 open issues. Labels were applied to the 24 calendar/story issues and to #1637; selected recent workstreams were also classified. Search-index results for `no:label` can lag writes, so use direct issue fetches before treating a zero-result search as proof that every issue is labelled.

### Recent issue ownership and boundaries

| Workstream | Canonical owner(s) | Boundary |
|---|---|---|
| Foundations and mathematical depth | #1732 | Audit coverage and reuse existing concepts/domains; no parallel registry or automatic page-per-topic expansion. |
| Distinctive pedagogical contribution | #1739 | Page-by-page audit of intellectual value; do not turn the 2–3 contribution heuristic into a quota. |
| Source quality by learning page | #1741 | Evidence diversity/complementarity and claim support; distinct from source membership and ingestion. |
| Source collection membership | #1306 | Explicit reviewed membership decisions only. |
| Source provenance and coverage | #1211 | Provenance, scan history, locator quality and graph reconciliation; do not create extractions just to close count gaps. |
| Registry and experience contracts | #1554 | Bounded inventory/reconciliation of canonical owners; no universal registry. |
| Cross-domain evidence queries | #1233 | Read/query adapters over existing canonical records; no second graph. |
| Scalability evidence | #1257 | Benchmarks and measured bottlenecks; no speculative infrastructure. |
| Tokenization editorial architecture | #1698 | Understand/Deepen boundary and page ownership; implementation edits remain with #1492 and the page-specific tasks. |
| Practice separation | #1512 | Learning pages teach; dedicated Practice pages assess. |
| Advent Calendar | #1513 | Collection-level editorial and learner validation; individual story changes remain with their day-specific issues. |

### Status corrections recorded on 2026-11-27

- #584: PRs #1602, #1604 and #1606 are merged. Their pre-merge CI failures are historical; remaining work is the targeted route audit, manual screen-reader/breadcrumb review and learner validation under #447.
- #1637: PR #1636 is merged; the checklist now reflects completion.
- #1664: PRs #1691, #1692 and #1693 are merged; individual page follow-ups remain with #1653, #1666 and #1667.
- #1306 and #1211: current-main source inventory is 150 source records, 100 extraction files and 520 atomic items; 50 collection decisions are explicit (48 non-empty, 2 explicitly empty), 100 remain undecided, and 42 source IDs lack a matching extraction filename. These are separate queues. The latest locator-quality report still covers 96 files / 489 items and must be refreshed before making current locator-completeness claims.
- #1770: merged on 2026-11-27; no longer an open PR.

### Recommended execution order

1. **Finish active learner-facing work already in progress:** #1492 → #1493, with #1698 coordinating the Understand/Deepen tokenization boundary; keep #1499 as the separate positional-concepts task.
2. **Complete the source-quality pilot:** #1741, while keeping #1306 membership decisions and #1211 provenance/locator checks separate.
3. **Run the Foundations and distinctive-value audits:** #1732 and #1739, using #1554's canonical contract inventory rather than introducing new metadata systems.
4. **Continue ingestion only where a source has a documented use:** #1761 and #1768; ingestion does not imply page integration.
5. **Keep learner validation explicit:** #584 technical route/manual checks and #447 independent learner evidence are not interchangeable.

### Backlog hygiene rules reaffirmed

- A parent issue coordinates and links work; it does not duplicate child checklists.
- A merged PR or completed subtask must be reflected in the owning issue, while preserving historical snapshots with dates.
- P1 means a near-term blocker or committed next execution slice, not merely important long-term work. Do not add P1 labels until the active sequence is genuinely narrowed.
- Use `area:*` for ownership domain, `type:*` for work nature, and existing priority labels for sequencing. Do not invent new label families until the current taxonomy has been audited against actual queries.
- Keep content, source ingestion/provenance, architecture/meta contracts, CI/maintenance and learner validation as distinct work types.
- Do not create a second canonical registry, a per-concept workflow, or a duplicate issue when an existing owner already covers the work.

### Audit limits

The period-partitioned search establishes the 103-issue open inventory at the time of this review, but it does not constitute a semantic re-read of all 103 issue bodies, all comments, all milestones or all assignees. The owner/boundary table above covers the principal overlapping workstreams examined in detail. Remaining older and specialist issues still require targeted review before declaring the entire backlog fully reconciled.


### Priority reconciliation — 2026-11-27

A direct review of all 20 open P1 issues led to five justified P1 → P2 changes:

- #1579: explicitly deferred until the main learning-path redesign is complete; implementation is split into #1580–#1583.
- #1233: the first read/query slice exists, but the remaining cross-domain contract is broad and evidence-dependent; keep specialist evidence owners (#1211, #512, #416, #1237) authoritative.
- #1257: concept-registry and topology benchmark slices are merged; broader end-to-end capacity work should follow a measured workload.
- #156: the remaining asset-rights audit is important but bounded follow-up (four provenance confirmations and rendered-DOM inventory), not a current release blocker.
- #163: code/prose licensing is complete; remaining non-text asset rights and contributor-permission review depends on #156 and explicit owner decisions.

The stale [P1] prefixes were removed from #1233 and #1257 titles. The P2 changes do not mean these issues are unimportant or closed; they mean they are not the next execution slice.

The P1 review also found:
- #1208's statement that its referenced PR was still a draft was stale; PR #1213 was merged on 2026-11-18. Remaining Quarto/browser verification is now stated as the closure gate.
- #1492's statement that PR #1489 was open was stale; it was merged on 2026-11-21. The issue now distinguishes the merged handoff from remaining lesson verification.
- #1741 and #1211 are classified as audits rather than generic research tasks.

The remaining P1 set is not a promise that all items should be executed concurrently. Several are conditional/gated: #78/#656 (private prerequisite review before G8 implementation), #220 (independent subject-matter review before learner pilot), #1513 (pilot evidence before scaling the calendar), and #1541/#988 (manual rendered/accessibility evidence before closure).

No milestones or assignees were added: the repository's available milestone taxonomy and project-owner assignment policy were not sufficiently established by this review. Do not invent milestones or assign the user automatically.


### Priority and PR snapshot — 2026-11-27 20:04 UTC

After the priority reconciliation and classification of newly created work, the partitioned open-issue search returns **104 open issues**: **17 P1**, **81 P2**, and **6 P3**. The four creation windows used for the inventory are disjoint (before October; October; 1–26 November; 27 November). The direct no-label search now returns zero issues. P3 issues are intentionally not folded into the P1/P2 counts.

Newly classified work:
- #1773 is P1 / architecture / audit because it documents concrete contradictions in canonical paths and skill contracts that can misroute future work.
- #1653 is P1 / pedagogy / documentation as the active Day 01 editorial slice.
- #1664 and #1666–#1689 are P2 / pedagogy / documentation (with #1664 also an audit): the story collection is coordinated as a portfolio, while page-specific work remains individually owned.
- #1732, #1739, #1761 and #1768 are P2 pending their bounded audits/ingestion checks; they are important but not all immediate parallel work.
- #1633 and #1637 are P2; #1637's first latency improvement PR #1636 is merged, while comparable timing/profile evidence remains.

At this snapshot, three PRs are open and mergeable:
- #1771 — this backlog reconciliation.
- #1772 — Otis running example in the bilingual language-representation lesson.
- #1774 — first implementation slice for #1773's workflow/skill contract audit.

The workflow-run lookup returned no PR-triggered runs for these branch heads at the time of this check. Do not describe their CI as green; verify checks on GitHub before merging. The open-PR inventory is time-sensitive and must be refreshed before a later handoff.


### PR status refresh — 2026-11-27 20:35 UTC

This section supersedes the earlier **20:04 UTC** statement that PRs #1771, #1772 and #1774 were open:

- [#1771 — backlog snapshot and workstream ownership](https://github.com/JM-Brun/llm-lab/pull/1771) was merged at 20:13 UTC. This document is now on `main`; the merged snapshot is a hand-off, not a second roadmap.
- [#1772 — Otis running example](https://github.com/JM-Brun/llm-lab/pull/1772) was merged at 20:13 UTC.
- [#1774 — workflow and skill architecture contracts](https://github.com/JM-Brun/llm-lab/pull/1774) was merged at 20:13 UTC. Static link checks passed. The final PR-head runs are now verified: test suite and Python quality succeeded, Quarto site & browser audit succeeded, and secret scanning succeeded; the two opt-in full-corpus/scale jobs were skipped. These results are recorded in #1773.

The three PRs in the earlier snapshot are therefore no longer open. This refresh does **not** claim a complete repository-wide open-PR inventory; refresh that separately before the next hand-off. The static ownership/delegation matrix, link/path checks and six representative routing cases are now documented in #1773. The only remaining evidence limitation is actual runtime skill activation, which requires invocation traces and is not established by static repository checks. The two opt-in full-corpus/scale jobs remain skipped by design for this change.
