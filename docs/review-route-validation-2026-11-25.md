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

**Lot A source scan — completed first pass on 2026-11-25 (20/20 core lesson pairs, FR and EN):**

| Source-level observation | Result | Interpretation |
|---|---:|---|
| Review companion pages resolved from canonical lesson contracts | 20 FR + 20 EN | All 20 core mappings have a language-specific published companion |
| `revision-essentials` section | 40/40 pages | Every companion has a concise synthesis section |
| `revision-check` section | 40/40 pages | Every companion has an active-recall question section |
| Answer disclosure (`<details>`) | 40/40 pages | Each companion exposes an answer; the three visual-card pages have a second disclosure for the card correction |
| Visual-recall block | 3/20 lesson pairs, both languages | Positional information, Q/K/V, and KV-cache decode |
| Literal flashcard/deck marker in companion source | 0/40 pages | No explicitly labelled flashcard/deck structure found by this marker scan |
| Explicit math delimiter marker | 3/20 pairs, both languages | Found on entropy, scaled-dot-product attention and causal masking; this is a prompt for semantic review, not proof that other pages need equations |

The three visual blocks are not additional lessons and should remain attached to their existing review companions. The current pilot in `docs/visual-recall-pilot.md` already covers these same three prompts.

**Limits of the structural scan:** it classifies source structure and simple markers, not the pedagogical quality of each answer, completeness of definitions, correctness of every equation, or the need for a formula-recall prompt. A literal flashcard marker search cannot rule out a question that behaves like a flashcard without being labelled as one. The subsequent content-level review is recorded below; it does not amount to a line-by-line scientific re-review of every source lesson.

The existing revision inventory remains useful evidence about integrated support in the 62 Understand/Build pages, but it is not a substitute for this Review-specific content audit.

**Lot A semantic pass — completed on 2026-11-25 (20 FR/EN lesson–companion pairs):**

The 20 companion pairs were read against the canonical lesson `purpose`/`scope`, the companion scope, its three-to-four synthesis points, its recall prompt and correction, and its visible Practice handoff. This was a content-level review of the companion pages, not a line-by-line scientific re-review of every source lesson.

- The synthesis points consistently cover the central mechanism and the distinctions needed to avoid the main conceptual confusions.
- Every recall prompt has a correction. The prompts are deliberately selective: they test one representative retrieval operation rather than restating the full lesson outcome.
- The larger outcomes are supported by the synthesis itself and, where needed, by visible handoffs to existing dedicated Practice pages. Cross-lesson exercises are retained where they test a genuine boundary (for example, lookup versus contextualization, or attention-position weights versus vocabulary probabilities). This pass did not revalidate every linked exercise body.
- The three visual prompts are attached to the relevant existing pairs: positional encoding, Q/K/V, and prefill/decode with a KV cache. They complement rather than duplicate the text questions.
- Calculation-oriented recall is already present where the target warrants it: scaled-dot-product attention, causal masking, entropy, likelihood, cross-entropy, loss and gradient descent. The remaining conceptual prompts do not need formulas merely to make the format uniform.
- The bilingual versions preserve the tested concept and reasoning. Some running examples differ by language; this is acceptable when the mathematical or conceptual condition is explicit and unchanged.

**Decision from this pass:** no additional flashcard deck, visual card, or mass-generated question set is justified. No clear scope/content mismatch was found that warrants changing one of the 20 companions on this evidence alone. This is not a claim that every possible question is exhaustive or that learner effectiveness has been demonstrated. A prompt that tests only one part of a broad outcome is not automatically a gap when the other parts are represented in the synthesis and Practice handoff.

**Deliverable:** keep the existing generated revision-coverage report and its audit tool as the source for machine-detectable coverage. Record editorial judgments in this validation document or the existing source metadata; do not create a second hand-maintained matrix or a new registry. Keep authored pedagogical judgments separate from mechanically detected source markers.

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

**Code-level audit of the existing implementation:**

- `resolve_lesson_contracts()` in `site/tools/build_learning_map.py` requires the lesson-contract keys to match the core route topics exactly, resolves one same-language synthesis page with an explicit `revision_of` link, rejects duplicate prerequisites, and verifies that each prerequisite was acquired earlier in the core route.
- The resolved lesson outcome is currently taken from the source lesson's `purpose`; the lesson scope comes from its `scope`; the Review companion's displayed coverage comes from the synthesis page's `scope`.
- `render_lesson_contracts()` presents the stage objective/overview, prior-learning links, lesson outcome and revision scope. It does not author a separate objective or prerequisite chain for Review.
- `tests/knowledge/test_lesson_contracts.py` verifies those projections, required anchors, answer disclosures, stage grouping and FR/EN topic parity. It does not prove that the wording and actual content of a companion semantically cover the outcome, nor that every listed prerequisite is pedagogically indispensable.
- The current Review index has no optional stops. Optional learning material remains outside the core Review traversal; no optional stop should be added unless an existing eligible resource and an explicit pedagogical target justify it.

**Lot C first semantic pass — completed on 2026-11-25:** the 20 stage/lesson relationships were checked at metadata and synthesis level against the stage objectives, canonical lesson purposes/scopes and the 20 companion scopes/content. No inconsistency surfaced at this level that justifies changing stage membership or rewriting an outcome. This is not a full scientific re-review of each lesson body. The lesson purposes contribute to their stage objectives at the intended granularity: tokenization before lookup; initial and positional representations before contextualization; block computation before Q/K/V and attention; logits before vocabulary probabilities; generation and context design as separate uses; observed-target scoring before parameter optimization.

The prerequisite chain also has a coherent conceptual rationale on first review: text IDs precede lookup; lookup and position precede contextualization; contextualized states precede block internals; Q/K precede attention weights and value aggregation; logits precede probabilities; probabilities precede entropy, generation and observed-target scoring; loss precedes gradients; gradients and loss precede the training loop. The training loop additionally depends on causal masking because shifted targets and teacher-forced prefixes must be interpreted correctly.

One apparently missing edge is intentional, not a defect: `loss` does not declare `cross-entropy` as a prerequisite. The existing `observed-target-to-training-objective` boundary in `data/guided-route.yml` explicitly connects scoring to training **without making scoring a prerequisite**. Do not add that edge merely because the concepts are related. Similarly, `logits` depends on the Transformer output rather than the Q/K/V or attention lessons: its output projection can be understood without making every internal attention mechanism a prerequisite.

This is a reviewed first-pass rationale, not a claim that every prerequisite is the only possible pedagogical choice. Any future change should be justified by an actual learner dependency and tested against the existing canonical route.

**Remaining checks:**

1. Retain the first-pass rationale above and revisit only where a source lesson or stage objective changes.
2. Check FR/EN semantic equivalence when either language's lesson purpose, scope or synthesis content changes.
3. Reassess prerequisite necessity only when a lesson's content or its route position changes; do not mechanically add every related concept as a prerequisite.
4. Record a concise rationale and evidence anchors for any future discrepancy.

Do not require literal equality between stage objectives, lesson outcomes and revision scopes: they operate at different granularities. Add structural assertions only for properties that can be proven from metadata; retain semantic judgments as reviewed evidence rather than brittle string comparisons.

### Lots D/E — Render, accessibility and responsive validation (deferred to the end)

**Priority decision (2026-11-25): these lots are explicitly out of the current content phase.**

The project must first reach content and pedagogical stability: conceptual coverage, lesson correctness, explanations, examples, exercises, learning sequence, prerequisite logic, and the coherence of the knowledge model. Once that foundation is accepted, the site will undergo a deliberate, comprehensive visual redesign. Only against that new design should rendered presentation, accessibility and responsive/mobile behavior be assessed and improved.

Therefore:

- Do not spend current effort extending browser coverage for the Review route, tuning viewport behavior, or validating visual presentation.
- Do not treat the current design as the target baseline; it is expected to be replaced.
- Do not run a premature mobile or accessibility remediation cycle against components that may be redesigned.
- Preserve the existing browser and accessibility tooling. Reuse and adapt it during the final design phase rather than creating new workflows now.
- Existing checks may continue to run as incidental CI safeguards, but their results are not a project acceptance gate for the current content phase.
- Do not add a Review-specific case to `scripts/site-browser-review.mjs` as part of this work. The branch intentionally leaves that script unchanged.

The existing browser tooling has been inventoried for future reuse: it already covers three visual-recall pages in FR/EN and desktop/mobile profiles, includes selected keyboard checks, and runs Axe in its interactive desktop/light profile. That inventory is retained as context, not as a current implementation task.

**Deferred deliverable:** after content freeze and visual redesign, define one coherent FR/EN validation pass covering rendered routes, navigation, responsive breakpoints, keyboard use, screen readers, contrast, zoom/reflow, diagrams and localization. Capture the redesigned site's actual behavior; do not retrofit the old layout merely to satisfy the old matrix.

### Lot F — Independent learner pilot

The existing pilot in `docs/visual-recall-pilot.md` already defines the three visual/text comparisons, delayed transfer prompts, scoring rubric and attrition accounting.

Treat this as a content-evaluation activity, not as a rendering/accessibility/mobile audit. Start it only once the relevant learning content and prompts are stable, and once the specific Q/K/V content-validation gate in [#483](https://github.com/JM-Brun/llm-lab/issues/483) is explicitly closed. Then follow [#447](https://github.com/JM-Brun/llm-lab/issues/447), freeze the pedagogical materials and time budgets before recruitment, and report incomplete follow-ups separately from incorrect answers. A small pilot is diagnostic, not proof of a general learning effect.

## 4. Execution order and gates

| Order | Lot | Depends on | Exit evidence |
|---:|---|---|---|
| 1 | A — source inventory | Existing canonical registries | All 20 core lesson/revision pairs inspected; source IDs/anchors recorded; no parallel matrix |
| 2 | C — semantic equivalence | A and canonical route contracts | Objective/outcome/prerequisite discrepancies reviewed in FR/EN |
| 3 | B — justified remediation | A and C | Only evidenced content gaps receive new or revised support |
| 4 | Content completion | A, B and C | Lessons, explanations, examples, exercises and learning sequence are pedagogically stable |
| 5 | F — learner pilot (if retained) | Stable pedagogical materials and Q/K/V content gate | Independent delayed-transfer observations under #447 |
| 6 | Visual redesign | Content freeze | New design system and redesigned site |
| 7 | D/E — rendered, responsive and accessibility validation | Visual redesign | One final FR/EN validation pass on the new design |

The order deliberately places semantic equivalence before content additions: otherwise a new card could reinforce an outcome that is itself misaligned with the canonical lesson.

## 5. Completion criteria

- [ ] All 20 core lesson/revision pairs have an evidence-backed, per-format source inventory.
- [ ] Flashcards are reported as present/missing/not assessed; no absence is inferred solely from filenames.
- [ ] The three existing visual prompts are checked against explicit lesson outcomes and bilingual content.
- [ ] Optional resources are considered only when explicitly registered and pedagogically relevant; optionality is preserved.
- [ ] Stage objectives, lesson outcomes, prerequisite relations and revision scopes have a documented FR/EN semantic review.
- [ ] Any new support has a specific retrieval/transfer target, correction and reason existing support is insufficient.
- [ ] Content is frozen before visual redesign begins.
- [ ] After redesign, rendered desktop/mobile and keyboard checks are recorded for FR/EN.
- [ ] After redesign, manual accessibility checks are recorded separately from automated checks.
- [ ] The learner pilot is run only after #483, and its results are recorded under #447.

## 6. Explicit non-goals

- No second stage, lesson, prerequisite or revision-resource registry.
- No manually copied 20-row lesson matrix maintained alongside `guided-route.yml`.
- No mass generation of flashcards to reach a coverage percentage.
- No promotion of optional pages into the core Review route.
- No copying of Practice exercises into Review.
- No claim that `integrated_sufficient`, a passing test, or a rendered diagram proves learning effectiveness.
- No current-phase browser, responsive/mobile or accessibility remediation against the pre-redesign interface.
- No new GitHub Actions workflow where the existing browser/CI tooling can be extended.


### Targeted scientific-caveat audit — output and scoring branch (2026-11-27)

A focused FR/EN review covered the four connected lessons **Logits**, **Output probabilities**, **Entropy** and **Likelihood**. This is a targeted claim-level check, not a completed scientific re-review of all 20 core lessons.

- **Logits:** the pages distinguish raw scores from probabilities, absolute confidence and factual truth. They explain that a common additive shift leaves softmax unchanged, while positive scaling can change distribution concentration without changing ranking.
- **Output probabilities:** both languages state that softmax gives a normalized conditional distribution, not calibration or factual truth. They also locate probabilities on tokenized units rather than words or semantic propositions, and distinguish temperature from candidate filtering.
- **Entropy:** both languages describe entropy as dispersion of the next-token distribution, dependent on context, model/tokenizer and temperature. They explicitly reject interpreting low entropy as truth or calibrated uncertainty.
- **Likelihood and perplexity:** both languages qualify comparisons by corpus, tokenizer, evaluated positions and reduction convention. They state that likelihood is fit to selected observations, not proof of truth, and perplexity is not general answer quality.

The bilingual caveats are materially aligned. Different running examples are acceptable because the mathematical conditions and conclusions are preserved.

**Correction found:** the English Likelihood page had a double-escaped bit-scale formula, `2^{\\bar{\\ell}}`, while the French page correctly used a single LaTeX command. [PR #1782](https://github.com/JM-Brun/llm-lab/pull/1782) changes it to `2^{\bar{\ell}}`. This is a rendering-level source correction, not a change to the mathematical claim.

**Remaining scope:** continue the same targeted method on the loss/cross-entropy and training-loop group, then the Transformer/attention group. Do not infer that the full 20-lesson scientific caveat audit is complete from this slice. Keep findings in this validation document; do not create another claim or lesson registry.
