# Review-route validation and remaining work

**Status:** implementation audit and execution plan  
**Snapshot:** 2026-11-25  
**Owner:** [issue #1541](https://github.com/JM-Brun/llm-lab/issues/1541)  
**Contract:** [parallel Review-route contract](parallel-review-route-contract.md)

This document coordinates the remaining work on the reader-facing Review route. It is deliberately **not** a second curriculum matrix, revision-resource registry, or page inventory. The route and lesson identities remain owned by the existing canonical sources below.

## 1. Existing sources and inventories — reuse, do not duplicate

| Concern | Canonical source / existing artifact | What it already owns | How this work uses it |
|---|---|---|---|
| Stages, order, core and optional lessons, stage objectives and overviews | `data/guided-route.yml` | The nine-stage curriculum and its bilingual page membership | Derive every Review projection and coverage report from this file |
| Lesson-to-synthesis mapping, prerequisites | `lesson_contracts` in `data/guided-route.yml` | One primary synthesis destination and ordered prerequisite topics for each of the 20 core lessons | Reuse the mapping; never maintain a parallel list |
| Lesson metadata and page identity | `LLM-LAB-PAGE-MAP` metadata on published Quarto pages | Stable page IDs, language, destination, scope, purpose and typed revision metadata | Use stable IDs and source metadata, not filenames or labels |
| Aid-to-lesson relations and lesson support assessments | `ProjectIndex` in `site/tools/project_index.py` | Typed page-aid relations, inverse lookup and explicit `revision_support` assessments | Query the existing index; do not infer relations from generic links |
| Understand/Build revision support | `docs/revision-aid-inventory-2026-11-19.md` and `site/tools/audit_revision_coverage.py` | A 62-page inventory (46 Understand, 16 Build) and source-level support assessments | Reuse as evidence about lesson-page support; do not treat it as a Review-companion audit |
| Earlier revision inventory | `docs/revision-resource-inventory-2026-11-19.md` | Historical source scan before the typed aid-link pilot | Historical context only; not the current relationship inventory |
| Visual-card experiment | `docs/visual-recall-pilot.md` | Three visual prompts, equivalent text prompts, delayed-transfer tasks and a scoring rubric | Reuse the existing pilot; do not create a second experiment |
| Reader-facing Review projection | `site/{fr,en}/review-path.qmd` and generated route contracts | Stage-grouped alternative route generated from the canonical route | Validate rendered output; do not hand-author another stage sequence |

### 1.1 What is already established

- The canonical route has **nine stages and 20 core lessons**.
- Each core lesson resolves to one primary synthesis destination in each language.
- The Review and Understand routes are peer navigation choices; their stage and lesson topology is shared.
- The current sidebars contain the 20 core lessons, the Review index, 20 primary synthesis pages and two shared cross-lesson review aids.
- The typed page-aid inventory records **50 links across 40 pages**. The separate 62-page inventory records **62 authored `integrated_sufficient` assessments** (46 Understand, 16 Build).
- Those 62 statuses are editorial assessments of integrated support on Understand/Build pages. They are **not** evidence that each Review companion has every revision format, nor evidence of learning effectiveness.
- The Review index currently links three manually curated visual-recall sections: positional information, Q/K/V, and one KV-cache decode step.
- The repository tree scan did not identify a dedicated flashcard/deck file. This is a filename-level finding only; inline retrieval prompts and question-answer structures still need a deliberate source scan.
- The 20 core synthesis mappings and their prerequisites are already in `data/guided-route.yml`. The generated Review projection and existing tests already protect much of the route structure.

### 1.2 Existing tests to preserve and extend only where necessary

`tests/knowledge/test_lesson_contracts.py` already checks:

- exact coverage of core lesson topics by `lesson_contracts`;
- one language-matched synthesis page with an explicit typed revision link;
- rendering of the lesson outcome and synthesis destination;
- required `revision-essentials` and `revision-check` anchors and answer disclosures;
- prerequisite ordering and rejection of unknown, future or self-dependencies;
- stage grouping and French/English topic parity.

`tests/knowledge/test_flat_curriculum_sidebar.py` derives the sidebar sequences from the canonical route and lesson contracts, and protects route order, one-level navigation, optional-page placement and Practice separation.

Do not rewrite these tests or add another test suite for already-covered invariants. The remaining equivalence gap is principally **semantic**: the current contracts resolve the stage objective, lesson outcome, prerequisite IDs and revision-page scope, but a structural link check cannot prove that their meanings agree.

## 2. Coverage vocabulary

Use explicit states per lesson and per support format:

- **present** — a concrete learner-facing support exists and its source is identified;
- **missing** — the audit inspected the relevant source and found no support for the target;
- **not assessed** — the source has not yet been inspected for that format;
- **not applicable** — the format would not serve the stated learning objective;
- **needs review** — a support exists, but its relevance, correctness, answer quality or accessibility is uncertain.

Do not collapse these states into a numeric coverage score. A synthesis page, typed relation, integrated recap, flashcard, visual prompt and Practice exercise are different evidence types. Practice exercises must not be counted as flashcards.

## 3. Work lots and current execution status

### Lot A — Reconcile the lesson-level support inventory

**Goal:** establish what already exists for each of the 20 core lesson/revision pairs, without copying the canonical lesson matrix.

1. Read the 20 core lesson IDs and synthesis targets from `data/guided-route.yml` at runtime.
2. Resolve the corresponding FR/EN pages through the existing published-page index and `ProjectIndex`.
3. Inspect each synthesis page for:
   - conceptual skeleton / concise synthesis;
   - definitions and essential distinctions;
   - equations, notation and assumptions;
   - active-recall questions;
   - answers or feedback;
   - common confusions / limits;
   - visual-recall prompts;
   - explicitly registered flashcards or decks.
4. Record evidence as source page IDs and anchors, not copied prose.
5. Cross-check the three already-known visual prompts against the page content and bilingual counterparts.
6. Search source bodies for inline card/deck structures before concluding that flashcards are absent.
7. Keep the existing 62-page Understand/Build inventory as a separate dimension; do not add its counts to the Review denominator.

**Current status:** the route mapping and three visual prompts are known; the per-format source inspection across all 20 synthesis pairs is not yet complete. The existing revision inventory is useful context but cannot substitute for this Review-specific pass.

**Deliverable:** extend the existing generated revision-coverage report or its existing audit tool with a Review-specific projection. Do not create a second hand-maintained matrix or a new registry. Keep authored pedagogical judgments separate from mechanically detected source markers.

### Lot B — Identify real gaps and add only justified support

**Entry condition:** Lot A has source-level evidence for all 20 lesson/revision pairs.

For every proposed addition, state:
- the exact lesson outcome it supports;
- the retrieval operation (define, distinguish, reconstruct, predict, explain or transfer);
- why the existing synthesis and current Practice material do not already meet that need;
- the correction/feedback that makes the prompt learnable;
- the FR/EN counterpart and source of truth.

Do not add a flashcard merely because a lesson has none. A missing format is not automatically a learning gap. Prefer reusing an existing visual, question or explanation when it tests the intended target. Keep multi-step calculations, coding, implementation and experiments in Practice & experiment.

### Lot C — Check objectives, outcomes and prerequisites

**Existing structural contract:** stage objectives and overviews come from `data/guided-route.yml`; lesson outcomes and scopes come from the canonical lesson-page metadata; prerequisite topic IDs and synthesis targets come from `lesson_contracts`; the Review page exposes the resolved outcome, prerequisites and revision scope.

**Remaining checks:**

1. For each core lesson, compare the stage objective with the lesson's local outcome: the outcome must contribute to the stage objective without silently broadening or narrowing it.
2. Compare the lesson outcome with the synthesis page's stated scope and actual content.
3. Verify that every prerequisite is genuinely needed before the lesson, is earlier in the canonical route, and is represented in the Review context without becoming a new or reordered dependency.
4. Check FR/EN semantic equivalence, not just identical IDs or balanced page counts.
5. Record a concise rationale and evidence anchors for each discrepancy.

Do not require literal equality between stage objectives, lesson outcomes and revision scopes: they operate at different granularities. Add structural assertions only for properties that can be proven from metadata; retain semantic judgments as reviewed evidence rather than brittle string comparisons.

### Lot D — Rendered Review-route validation

Reuse the current site-browser review tooling and existing CI jobs; do not create one workflow per check.

Minimum matrix:

| Dimension | Required cases |
|---|---|
| Language | FR and EN |
| Viewport | Desktop and narrow mobile |
| Route entry | Review index, a middle stage, first and last core lesson |
| Navigation | Understand ↔ Review, stage anchors, lesson → synthesis, synthesis → lesson |
| Context | Stage number, lesson position, prerequisite/outcome cues |
| Keyboard | Tab order, visible focus, Enter/Space activation, disclosure open/close, no keyboard trap |
| Responsive | No horizontal overflow, clipped cards, overlapping controls or unusable tap targets |
| Localization | Correct destination language, labels, accessible names and language changes |

Capture the tested commit, viewport, browser, screenshots and test output. A successful Quarto render or structural test alone is not a rendered UX sign-off.

### Lot E — Manual accessibility review

Keep this separate from automated axe checks and browser assertions.

- Test keyboard-only navigation in both languages, including focus visibility and disclosure controls.
- Test with a real screen reader in FR and EN; inspect heading hierarchy, reading order, link purpose, diagram alternatives, disclosure state and language pronunciation.
- Check contrast, zoom/reflow, touch target size and reduced-motion behavior where applicable.
- Record environment, pages, steps, observed result and unresolved limitations. Mark anything not actually tested as **not verified**.

### Lot F — Independent learner pilot

The existing pilot in `docs/visual-recall-pilot.md` already defines the three visual/text comparisons, delayed transfer prompts, scoring rubric and attrition accounting.

Do not start it until the manual Q/K/V validation gate in [#483](https://github.com/JM-Brun/llm-lab/issues/483) is explicitly closed. Then follow [#447](https://github.com/JM-Brun/llm-lab/issues/447), freeze the materials and time budgets before recruitment, and report incomplete follow-ups separately from incorrect answers. A small pilot is diagnostic, not proof of a general learning effect.

## 4. Execution order and gates

| Order | Lot | Depends on | Exit evidence |
|---:|---|---|---|
| 1 | A — source inventory | Existing canonical registries | All 20 core lesson/revision pairs inspected; source IDs/anchors recorded; no parallel matrix |
| 2 | C — semantic equivalence | A and canonical route contracts | Objective/outcome/prerequisite discrepancies reviewed in FR/EN |
| 3 | B — justified remediation | A and C | Only evidenced gaps receive new or revised support |
| 4 | D — rendered validation | B plus stable content | FR/EN desktop/mobile captures and keyboard results |
| 5 | E — manual accessibility | Stable rendered build | Manual test record in both languages |
| 6 | F — learner pilot | Q/K/V gate #483 and stable cards | Independent delayed-transfer observations under #447 |

The order deliberately places semantic equivalence before content additions: otherwise a new card could reinforce an outcome that is itself misaligned with the canonical lesson.

## 5. Completion criteria

- [ ] All 20 core lesson/revision pairs have an evidence-backed, per-format source inventory.
- [ ] Flashcards are reported as present/missing/not assessed; no absence is inferred solely from filenames.
- [ ] The three existing visual prompts are checked against explicit lesson outcomes and bilingual content.
- [ ] Optional resources are considered only when explicitly registered and pedagogically relevant; optionality is preserved.
- [ ] Stage objectives, lesson outcomes, prerequisite relations and revision scopes have a documented FR/EN semantic review.
- [ ] Any new support has a specific retrieval/transfer target, correction and reason existing support is insufficient.
- [ ] Rendered desktop/mobile and keyboard checks are recorded for FR/EN.
- [ ] Manual accessibility checks are recorded separately from automated checks.
- [ ] The learner pilot is run only after #483, and its results are recorded under #447.

## 6. Explicit non-goals

- No second stage, lesson, prerequisite or revision-resource registry.
- No manually copied 20-row lesson matrix maintained alongside `guided-route.yml`.
- No mass generation of flashcards to reach a coverage percentage.
- No promotion of optional pages into the core Review route.
- No copying of Practice exercises into Review.
- No claim that `integrated_sufficient`, a passing test, or a rendered diagram proves learning effectiveness.
- No new GitHub Actions workflow where the existing browser/CI tooling can be extended.
