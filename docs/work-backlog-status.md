# Remaining-work register

**Snapshot:** 2026-11-03  
**Purpose:** consolidate the active work across `JM-Brun/llm-lab` and `JM-Brun/wiki-knowledge`, expose dependencies, and keep execution lots small enough to review and validate independently.

This is an execution register, not a second curriculum or a replacement for the owner issues. The GitHub issues linked below remain the source of truth for detailed acceptance criteria. Reconcile this snapshot against live issue state before starting a later phase.

## 1. Current status

- `llm-lab`: 47 open issues; the curriculum-docs reconciliation PR [#319](https://github.com/JM-Brun/llm-lab/pull/319) was squash-merged on 2026-11-03 (commit `15832af`), and the advanced-reading reclassification PR [#321](https://github.com/JM-Brun/llm-lab/pull/321) was squash-merged on 2026-11-03 (commit `4218234`).
- `wiki-knowledge`: 4 open issues and no open pull requests at the time of this snapshot.
- LLM Lab PR [#306](https://github.com/JM-Brun/llm-lab/pull/306) (site-wide breadcrumbs) and [#307](https://github.com/JM-Brun/llm-lab/pull/307) (dedicated self-check pattern) are merged.
- PR #307's Quarto render and Python quality workflows completed successfully. The #306 GitHub Pages render and deployment jobs also completed successfully.
- PR #319 (curriculum docs reconciled with the rendered navigation) was squash-merged as `15832af` on 2026-11-03 after both workflows passed: five obsolete sidebar references fixed in `learning-path.md`, `mathematical-foundations` realigned to Deepen, seven missing inventory rows added. Documentation-only change; no browser review is claimed.
- Owner rule recorded 2026-11-03: advanced comprehension belongs in the Deepen destination. The four advanced panorama readings (scaling-laws, emergence, in-context-learning, hybrid-llm-architectures) are retagged from `destination:understand` to `destination:deepen` (FR/EN page maps and keywords), with `content-section-mapping.md` rows and a new editorial rule aligned. Sidebar placement already matched. Merged as PR #321 (`4218234`) after both workflows (Python quality checks incl. `check_page_metadata.py`, bilingual Quarto render) passed; no browser review claimed.
- Owner Deepen rule applied to inline content, 2026-11-03: the advanced soft-target/KL callout in `cross-entropy` and the parameter-cost callout in `embedding-space` (FR/EN) were replaced by short pointer callouts; the moved material now lives in a new section of `language-modeling-math` (soft targets and KL divergence) and of `tensors` (embedding parameter cost). Merged as PR [#331](https://github.com/JM-Brun/llm-lab/pull/331) (`36eb848`) on 2026-11-03 after both workflows (Python quality checks incl. `check_page_metadata.py`, bilingual Quarto render) passed; no browser review is claimed.
- Automated build/deployment success is not browser inspection, accessibility certification, or evidence of learning. No desktop/mobile visual validation is claimed here.

## 2. Recommended execution order

### P0 — Close the foundational browser-review gate

**Owner:** [#82 — text → token IDs → embeddings → contextual states](https://github.com/JM-Brun/llm-lab/issues/82)

The scientific/source work and executable example are largely complete. The remaining acceptance gate is a real rendered browser review of the four bilingual page pairs.

| Lot | Existing issue | Scope | Size assessment |
|---|---|---|---|
| A | [#311](https://github.com/JM-Brun/llm-lab/issues/311) | `text-data` + `embedding-space`, FR/EN, desktop/mobile | Good: two related page pairs, 45–60 min |
| B | [#312](https://github.com/JM-Brun/llm-lab/issues/312) | `positional-encoding` + `tensors`, FR/EN, desktop/mobile | Good: two related page pairs, 45–60 min |
| C | [#82](https://github.com/JM-Brun/llm-lab/issues/82) | Consolidate findings, fix only reproducible defects, verify acceptance | Good as a short close-out after A and B |

**Exit condition:** record browser, viewport dimensions, language, page, observations and severity. Keep source correctness, CI, rendered appearance and learning evidence distinct. Do not start later attention/GPT implementation work merely because the content builds.

### P1 — Validate the shared visual system

**Owner:** [#191 — rendered bilingual design-system validation](https://github.com/JM-Brun/llm-lab/issues/191)

The parent is correctly decomposed already. Execute sequentially; do not combine the lots into a broad redesign.

| Lot | Existing issue | Scope | Size assessment |
|---|---|---|---|
| A | [#308](https://github.com/JM-Brun/llm-lab/issues/308) | Inventory color tokens and real uses; no styling changes | Good: 45–60 min |
| B | [#309](https://github.com/JM-Brun/llm-lab/issues/309) | Rendered review of 3–4 representative pages/components | Good: 45–60 min |
| C | [#310](https://github.com/JM-Brun/llm-lab/issues/310) | Contrast measurements, keyboard, zoom/reflow and reduced motion | Good: 45–60 min |

**Dependency:** PR #189 was merged on 2026-10-30; use its integrated token baseline and verify the current source before making changes. The output must distinguish measured failures, manual observations and untested criteria. A representative sample cannot establish site-wide WCAG conformance.

Include a focused check of the newly deployed breadcrumb from PR #306 (desktop/mobile, FR/EN, hierarchy and keyboard focus). Check the `.self-check` treatment from PR #307 on the overview page as part of the relevant rendered-page pilot (#317); do not create separate visual audits for the same components.

### P1 — Finish the existing pedagogical-template pilot

**Owner:** [#282 — pedagogical templates and page audit](https://github.com/JM-Brun/llm-lab/issues/282)

Research, source audit and template hierarchy are integrated. The remaining pilot is rendered review, already split into two bounded lots:

- [#316](https://github.com/JM-Brun/llm-lab/issues/316): entropy, cross-entropy and scaled-dot-product attention (three page pairs).
- [#317](https://github.com/JM-Brun/llm-lab/issues/317): Transformer architecture and Transformer overview (two page pairs).

Both lots should record FR/EN, desktop/mobile, viewport and reproducible observations. The three page pairs in #316 are explicitly timeboxed to 45–60 minutes. Keep that boundary; if the inspection proves materially larger, split the remaining work into **entropy/cross-entropy** and **attention** rather than expanding the session. Do not create cosmetic fixes from preference alone.

### P1 — Formative exercise sequence, gated by #82

**Owner:** [#220 — bilingual formative exercises](https://github.com/JM-Brun/llm-lab/issues/220)

The six activities TR-01–TR-06 exist as a design draft, but the new child plan intentionally caps the first release at three substantial activities. This is a real scope decision to resolve before writing learner-facing exercises.

| Lot | Existing issue | Scope | Size assessment |
|---|---|---|---|
| A | [#313](https://github.com/JM-Brun/llm-lab/issues/313) | Select and map at most three activities to existing lessons and G0–G9 | Good: 45–60 min |
| B1 | [#314](https://github.com/JM-Brun/llm-lab/issues/314) | Draft activity 1 in FR/EN, including hints, worked solution and misconception feedback | Recommended split: one activity per reviewable slice |
| B2 | #314 follow-up | Draft activity 2, same acceptance contract | Recommended split |
| B3 | #314 follow-up | Draft activity 3, same acceptance contract | Recommended split |
| C | [#315](https://github.com/JM-Brun/llm-lab/issues/315) | Independent solution review, bilingual parity, render and browser review | Good as a 45–60 min validation lot per batch |

**Dependencies:** #313 precedes drafting; #82 remains a release gate. Before #314 begins, explicitly select three of TR-01–TR-06 or justify a different pilot. Do not silently expand the initial release to all six. No transfer assessment, learner-data collection or quiz engine is included.

### P1 — Reconcile learning-depth placement (targeted work, not a global rewrite)

**Owner:** [#296 — keep core understanding separate from deepening](https://github.com/JM-Brun/llm-lab/issues/296)

The issue reports that the QKV workbench fence defect and Unicode route were addressed by an attached change, but the remaining notes still identify work around metadata and RoPE placement. Verify the current `main` source before editing; the issue text is not proof that every recommendation remains applicable.

Recommended sub-lots:

1. **Metadata reconciliation (15–30 min):** set the Unicode page's destination/level metadata and update `docs/content-section-mapping.md`, if still missing.
2. **RoPE core/deep-dive separation (one FR/EN page pair, 45–60 min):** keep the core explanation to why position is needed and where it enters; move detailed RoPE geometry, variants and implementation caveats into clearly optional disclosure or a dedicated Deepen destination.
3. **QKV workbench scope check (30–45 min):** verify that the workbench teaches projections/shapes only and does not duplicate scaled-dot-product attention. Change it only if the source still contradicts the declared scope.
4. **Validation (30–45 min):** metadata graph, FR/EN parity, Quarto render and a focused browser check.

Do not turn this into a general review of every attention page; #61 and #282 have separate ownership.

## 3. Curriculum and navigation coordination

These are parent/coordinator issues with distinct ownership. Keep them as coordination records; do not implement them as one large PR.

- [#130 — high-level learning architecture](https://github.com/JM-Brun/llm-lab/issues/130): final consistency across Understand / Build / Deepen / Practice and coordination of child work. Close only after its child owners have supplied evidence.
- [#87 — three learning depths and milestone map](https://github.com/JM-Brun/llm-lab/issues/87): finish milestone-to-page/deep-dive/code/test/source traceability, then reconcile against rendered FR/EN navigation. Suggested sub-lots: G0–G3, G4–G6, G7–G9, followed by one cross-map consistency pass.
- [#108 — bilingual LLM panorama](https://github.com/JM-Brun/llm-lab/issues/108): a distinct content gap covering model families, lifecycle, training/adaptation, inference and limits. Split into (1) scope/source outline, (2) concise core page in FR/EN, (3) source and parity review. Keep the overview independent of Transformer-specific detail.
- [#154 — homepage orientation and system diagram](https://github.com/JM-Brun/llm-lab/issues/154): split into (1) first-visit information architecture, (2) diagram accuracy/provenance, (3) rendered desktop/mobile validation. Avoid mixing it with global design-system validation.
- [#61 — progressive disclosure and reader experience](https://github.com/JM-Brun/llm-lab/issues/61): continue as a page-family audit, one coherent family per lot. It owns reader depth, not new implementations.
- [#190 — interactive UX benchmark](https://github.com/JM-Brun/llm-lab/issues/190): complete observation and adoption decision first. Any prototype must be a separate issue with one page and one observable learning objective.

**Overlap to resolve:** [#280](https://github.com/JM-Brun/llm-lab/issues/280) is a broad convergence audit whose scope overlaps #282 and #61. Do not run it as a parallel audit. Reconcile its remaining unique items against those owners, then narrow it to uncovered page families or close it as superseded after owner review. [#225](https://github.com/JM-Brun/llm-lab/issues/225) should likewise be checked against the already integrated navigation and #87 before any new ordering changes.

## 4. Concept-to-code implementation — remain gated

**Coordinator:** [#78 — concept-to-code roadmap](https://github.com/JM-Brun/llm-lab/issues/78)

The issue already names concept-level work items. Treat it as an index, not as a single implementation task. Do not advance until #82's foundational acceptance gate and the relevant prerequisite review are complete.

Recommended order after the gate:

1. [#58](https://github.com/JM-Brun/llm-lab/issues/58): tokenized corpus → shifted training examples. Reconcile with #83 first; the roadmap already records a possible duplicate.
2. [#79](https://github.com/JM-Brun/llm-lab/issues/79): logits, softmax, likelihood and cross-entropy.
3. [#80](https://github.com/JM-Brun/llm-lab/issues/80): scaled-dot-product attention and invariants.
4. [#81](https://github.com/JM-Brun/llm-lab/issues/81): causal masking and leakage tests.
5. [#84](https://github.com/JM-Brun/llm-lab/issues/84): generation strategies and evaluation limitations.
6. Later, create or activate narrowly scoped work for the Transformer block and training/optimization. Do not bundle them into one PR.

For each concept, use three small stages: source/notation audit; explanation plus minimal implementation where scientifically useful; adversarial tests, bilingual parity and rendered review. For theory-only concepts, use derivation or pseudocode rather than artificial code.

## 5. Deferred LLM Lab work

These issues remain open, but should not compete with the P0/P1 validation gates unless a concrete dependency emerges.

- **Interactive execution:** [#268](https://github.com/JM-Brun/llm-lab/issues/268). Split into a technology/performance spike, one bilingual pilot cell on one page, then a decision on a second workbench. Do not implement tokenization and attention in parallel before the first pilot meets fallback, accessibility, mobile and maintenance criteria.
- **External resource curation:** [#266](https://github.com/JM-Brun/llm-lab/issues/266), [#147](https://github.com/JM-Brun/llm-lab/issues/147), [#114](https://github.com/JM-Brun/llm-lab/issues/114), [#86](https://github.com/JM-Brun/llm-lab/issues/86). Keep this selective; verify one candidate and its exact pedagogical role at a time. Do not create a resource catalogue or new page by default.
- **Visual rights and project licensing:** [#156](https://github.com/JM-Brun/llm-lab/issues/156) and [#163](https://github.com/JM-Brun/llm-lab/issues/163). Split the remaining asset inventory from owner-level licence decisions. Preserve existing external illustrations; do not infer reuse permission from attribution or public availability. Licence selection requires explicit project-owner approval.
- **Historical timeline:** [#197](https://github.com/JM-Brun/llm-lab/issues/197). Recheck the current timeline and acceptance criteria before treating the open issue as unimplemented; the timeline fragments and parity checks already exist.
- **Raschka chapter/appendix coverage:** issues #95–#106. Treat each chapter/appendix as its own small audit and keep P2/P3 items deferred behind the foundational route.

## 6. Canonical knowledge base — separate repository ownership

Canonical, reusable scientific knowledge belongs in `JM-Brun/wiki-knowledge`; LLM-specific teaching sequence and Quarto presentation stay in `llm-lab`.

### P1 — Registry and source provenance

[Wiki issue #32](https://github.com/JM-Brun/wiki-knowledge/issues/32) is a valid integrity issue, but its current task list combines schema decisions, validator implementation and generated-data repair. Recommended split:

1. **Contract decision (30–45 min):** define whether `source_path` means a local archive, external URL or optional metadata-only reference.
2. **Deterministic synchronization and validation (one focused PR):** unique IDs, source-reference resolution, registry/frontmatter parity and regression tests.
3. **Reconciliation (30–60 min):** regenerate the registry, run `wk-validate`, `wk-lint` and the full test suite, document intentional warnings.

Do not hand-edit generated `REGISTRY.yml` if the documented workflow is generation.

### P1/P2 — Wiki tooling reliability

[Wiki issue #5](https://github.com/JM-Brun/wiki-knowledge/issues/5) is too broad for one implementation PR. First spend one short audit lot revalidating every source-level finding against current code/tests. Then split only confirmed defects into:

- package metadata, installation and CLI contract;
- workflow Python version and clean-install automation;
- search semantics (honestly label BM25 fallback or implement a genuine independent vector retriever as a separate design decision);
- CLI and search edge-case tests;
- README examples and least-privilege workflow review.

Do not start by implementing embeddings: first establish what the repository promises and what is actually required.

### P2 — Tensor concept and computational audit

- [Wiki #30](https://github.com/JM-Brun/wiki-knowledge/issues/30): split into (1) formal source/notation research, (2) domain-neutral concept explanation and distinction from arrays, (3) one worked basis-change example with invariant and counterexample, (4) bilingual/index/render validation. Do not teach all applications (stress, electromagnetism, relativity) in one page.
- [Wiki #29](https://github.com/JM-Brun/wiki-knowledge/issues/29): inventory first, then one concept per PR. Classify each as runnable code useful, symbolic/pseudocode preferable, or not applicable. Avoid bulk code additions and keep LLM-specific conventions out of canonical definitions.

## 7. Lot-size and concurrency rules

Use these rules when opening or executing child issues:

- **Target:** 30–60 minutes of focused work per lot; 60 minutes is a ceiling, not a target to fill.
- **One primary outcome per lot:** inventory, source audit, content change, implementation, or validation. Avoid combining all five.
- **Bound the surface:** normally one concept, one bilingual page pair, or at most 2–3 closely related page pairs for a browser audit.
- **One conceptual change per PR:** keep FR and EN together when they are counterparts; do not split language parity into separate PRs.
- **Independent validation:** specify exactly which tests, render, browser widths, sources and invariants are checked.
- **Explicit exclusions:** state what the lot must not expand into.
- **Dependency gates:** do not draft or release downstream learner-facing work before the upstream gate is complete.
- **Concurrency:** keep at most two active lots, preferably one content/technical lot and one independent browser-validation lot. Avoid three simultaneous editorial audits of the same pages.
- **Stop and split:** if a lot requires more than one session, spans unrelated page families, or has multiple independent acceptance outcomes, split it before implementation.
- **No false completion:** issue open/closed state, CI success, browser review and learning evidence are separate statuses.

## 8. Immediate next actions

1. Complete #311 and #312, then consolidate #82.
2. In parallel only if capacity permits, execute #308 → #309 → #310, or the #316/#317 rendered pilot; avoid running both audits against the same pages at once.
3. Resolve the three-activity pilot decision in #313 before drafting #314.
4. Verify the remaining source-level state of #296 and create only the small follow-up changes still justified.
5. Keep implementation issues #58 and #79–#84 gated until #82 is accepted.
6. In `wiki-knowledge`, prioritize the integrity contract in #32; revalidate #5 before implementation.
7. Reconcile overlapping/possibly stale issues (#280, #225, #197, #83) before creating new work.

## 9. Status discipline

This register records the state visible on 2026-11-03. Update it only when an issue changes status or a validation artifact is produced. For each completed lot, record the commit/PR, exact CI runs, browser/device/viewport where relevant, and unresolved limitations. Do not convert an automated success into a claim of visual quality, accessibility conformance, scientific correctness beyond the tested claims, or learner mastery.


## 10. Execution update — 2026-11-03 (supersedes the immediate actions in §8)

This addendum records work completed after the earlier snapshot in this register.

### Closed or transferred

- **#82 — source/content work:** closed after the source-level acceptance items were completed. Its remaining browser review was explicitly transferred to [#320](https://github.com/JM-Brun/llm-lab/issues/320); closing #82 does not mean the rendered review or learner validation is complete.
- **#311 and #312:** closed as transferred lots. Their four bilingual page pairs are included in #320.
- **#320 — deferred browser review:** created at **P2** for text-data, embedding-space, positional-encoding, and tensors, FR/EN, desktop/mobile. It is a later release check and no longer blocks source-level work.
- **#296:** already closed; a source-level revalidation was added to its discussion.
- **#308 — page-level colour inventory:** closed after a source scan of all 91 bilingual .qmd pages and classification of the actual inline/SVG colour declarations. No palette or SCSS change was justified. Rendered-component comparison remains with #309.
- **#313 — formative activity inventory:** the three-activity inventory is proposed in [PR #322](https://github.com/JM-Brun/llm-lab/pull/322). The six detailed TR-01–TR-06 drafts are preserved and grouped as three bundles; #313 remains open until the PR is reviewed and merged.

### Current recommended sequence

1. **Review and validate PR #322.** Its scope is one 48-line design inventory, not learner-facing publication. Recheck CI on the rebased head before merge.
2. **Continue #220 source review.** Independently review the detailed answer keys, then integrate the three-bundle sequence and verify FR/EN parity. Do not claim a second human expert review or learner evidence unless actually obtained.
3. **Continue the source/design-system handoff:** #309 owns the rendered sample comparison; #310 owns targeted contrast, keyboard and responsive checks. Do not mark either complete from source inspection.
4. **Keep #320 at P2** until browser inspection can be scheduled. Its delay must not be represented as a passed acceptance criterion.
5. Reassess #316/#317 after the higher-priority source and design-system work; they are separate rendered pedagogical audits and should not be mixed into #308.

### Updated evidence boundaries

- Source inventory and source-level reasoning are recorded in the relevant issue discussions.
- #308 did not change SCSS, palette tokens or page content.
- PR #322 adds only the three-activity inventory; it does not rewrite or delete the six detailed exercise drafts.
- Browser appearance, accessibility conformance and learner outcomes remain unverified wherever their dedicated issues remain open.

## 11. Follow-up execution update — 2026-11-03

- **#313:** closed after [PR #322](https://github.com/JM-Brun/llm-lab/pull/322) was merged. The three-activity inventory is now on main.
- **#314:** in progress through [PR #325](https://github.com/JM-Brun/llm-lab/pull/325). The six draft sections are consolidated into three bilingual bundles without deleting prompts, hints, solutions or misconception feedback.
- **#310:** source-level contrast risk documented; targeted correction is proposed in [PR #324](https://github.com/JM-Brun/llm-lab/pull/324). The wider rendered keyboard/responsive review remains open.
- **#114:** primary-source rechecks for Ahia, Petrov, Wegmann and TokLens are recorded in the issue. A small FR/EN parity correction for the TokLens synthesis is identified as follow-up work; no additional content is needed in the essential learning path.
- **#320:** remains the P2 deferred browser review for the four text-to-representation page pairs; it is not a passed release criterion.

### Immediate next actions

1. Validate and merge #324 only after both workflows pass on its current head.
2. Validate #325, including the bilingual Quarto render, then complete #314 with an independent mathematical/content review before learner-facing integration.
3. Correct the TokLens FR/EN synthesis in the advanced tokenizer-design page, preserving the distinction between fertility, character-normalized parity and downstream association.
4. Keep #309/#310 and #316/#317 as separate rendered/accessibility audits; do not claim their browser evidence from source inspection.

## 12. Source-audit and validation update — 2026-11-03

- **#310:** targeted text-contrast correction is merged via PR #324. The issue remains open for remaining color pairs and rendered keyboard/responsive checks; no global WCAG claim is made.
- **#313, #314 and #315:** closed after PRs #322, #325 and #330 were merged. The formative sequence now has three bilingual bundles, preserved detailed solutions and a recorded source-level review.
- **#114:** primary-source rechecks for tokenization and embedding studies are documented in issue comments. PRs #326 and #332 are merged; the source-audit register reconciliation is proposed in [PR #333](https://github.com/JM-Brun/llm-lab/pull/333). Close #114 after this documentation PR is merged, unless a new concrete content gap is found.
- **#320 (P2):** canonical prerequisite-page browser review remains deferred. **#329 (P2):** learner-facing exercise-page review is triggered only after those exercises are integrated into Quarto.
- **#308:** closed after the source inventory of all 91 bilingual QMD pages; rendered component comparison remains #309.

### Next recommended actions

1. Review and merge #333 after source-audit document and bilingual links pass CI; then close #114.
2. Continue #191 design-system rendered/contrast work in #309/#310 without claiming browser evidence from source inspection.
3. Reassess #316/#317 after the design-system work; keep them separate from the tokenizer/embedding source audit.
4. Keep #320 and #329 at P2 until the relevant pages exist in a browser-reviewable form and time is allocated.

## 13. Curriculum-map reconciliation — 2026-11-03

- **#114:** closed after primary-source audits and the source register were reconciled in PR #333.
- **#310:** the text-contrast fix (#324) and semantic SVG outline fixes (#335) are merged. The issue remains open for other color pairs and rendered/keyboard checks.
- **#315:** closed after source-level exercise review; future learner-facing rendering is tracked in #329.
- **#87:** milestone-to-page/source/code/test crosswalk is now reconciled in PR #336. Rendered EN/FR navigation inspection is moved to #337 (P2).
- **#320 / #329 / #337:** all are deferred P2 browser-review tasks with distinct scopes; none is represented as completed.

### Next sequence

1. Validate and merge #336; then close the source-level curriculum-map lot #87 with the rendered navigation check transferred to #337.
2. Continue #130/#78 source-level architecture and concept-to-code sequencing; #82 and #114 are no longer active source gates.
3. Continue #191 remaining design-system checks; do not infer browser/accessibility compliance from source-level contrast ratios.
4. Keep #316/#317 as separate rendered pedagogical audits; reassess after the source architecture and design-system work.

## 14. Execution follow-up — 2026-11-03

- **PR #336** ("docs: reconcile learning path with completed source gates") was squash-merged as `5b61d2f` on 2026-11-03 after the *Python quality checks* workflow passed ([run 41713706282](https://github.com/JM-Brun/llm-lab/actions/runs/41713706282)). Documentation-only; the change reconciled `learning-path.md`, `full-curriculum-plan.md` and `content-section-mapping.md` with the closed source gates #82/#114 and the current implementation/formative evidence states.
- **#87** closed as completed at the source level: the milestone-to-pages/deep-dives/sources/code-tests crosswalk is reconciled, and the rendered EN/FR navigation inspection is explicitly transferred to [#337](https://github.com/JM-Brun/llm-lab/issues/337) (P2). Closure evidence and limits are recorded in the closing issue comment; no browser or learner evidence is claimed.
- **#338** was opened in error during the same closure (duplicate of #337's scope) and immediately closed as a duplicate; no work lost.
- The three deferred browser-review lots remain distinct: #320 (four canonical page pairs), #329 (learner-facing exercises after integration), #337 (rendered navigation vs the curriculum map).

### Next sequence (supersedes §13 item 1)

1. Continue #130/#78 source-level architecture and concept-to-code sequencing; #82, #114 and #87 are no longer active source gates.
2. Continue #191 remaining design-system checks (#309/#310); do not infer browser/accessibility compliance from source inspection.
3. Keep #316/#317 as separate rendered pedagogical audits; reassess after the architecture and design-system work.
4. Keep #320/#329/#337 at P2 until dedicated browser sessions are scheduled.

## 15. Concept-to-code implementation update — 2026-11-03

This addendum records the two concept-to-code implementation lots merged after §14, plus the owner's own documentation merges in the same window. Both follow the register's lot rules: one concept per PR, implementation + adversarial tests + bilingual documentation sync, honest evidence states.

- **PR #342** ("feat: add tested sliding-window input/target construction for training examples", G2 milestone of #58) was squash-merged as `45ae37be` on 2026-11-03 after both workflows passed: *Python quality checks* ([run 41714877317](https://github.com/JM-Brun/llm-lab/actions/runs/41714877317)) and *Render bilingual learning site* ([run 41714877668](https://github.com/JM-Brun/llm-lab/actions/runs/41714877668)). Scope: `training_examples.py` with `sliding_input_target_pairs` (windowed input/target construction with strict validation), one test file, `__init__` re-exports, FR/EN training-examples callouts, evidence-matrix rows and README status. **#58 remains open**: corpus loading, packing, padding/masks, batching and train/validation splits are still unimplemented and not represented as done.
- **PR #345** ("feat: add tested top-k and top-p truncation filters for decoding distributions", G6 milestone of #84) was squash-merged as `56d8419d` on 2026-11-03, merged by the owner after both workflows passed: *Python quality checks* ([run 41715923020](https://github.com/JM-Brun/llm-lab/actions/runs/41715923020)) and *Render bilingual learning site* ([run 41715923175](https://github.com/JM-Brun/llm-lab/actions/runs/41715923175)). Scope: `decoding_filters.py` with `top_k_filter` and `top_p_filter` (renormalization, stable lowest-index tie-breaking, `ValueError` validation, no input mutation, copy semantics for `k >= V` and `p = 1`), one test file, `__init__` re-exports, FR/EN decoding-strategies callouts, evidence-matrix rows and README status. Explicit non-goals, recorded in the PR and on #84: the filters are **not wired into `generate.py`** (which still supports greedy and temperature sampling only); no logits-processor chain, beam search, contrastive decoding or repetition/frequency penalties; the temperature-then-truncation order is a teaching convention, not an implementation standard. **#84 remains open**: evaluation limitations are not addressed by this lot.
- The owner independently merged two documentation PRs in the same window: **#344** (QKV page structure aligned across French and English, `4b23c20`) and **#346** (French word fixed in the English attention lesson, `36174c5`). They are outside the concept-to-code scope and recorded here only for sequence completeness.

### Next sequence (supersedes §14 "Next sequence")

1. Optional bounded follow-up within #84: wire `top_k_filter`/`top_p_filter` explicitly into the sampling path of `generate.py` as one small PR, keeping greedy + temperature as the default path and updating tests, bilingual pages and evidence matrices in the same lot.
2. Continue the #58 remaining gaps (corpus loading, packing, padding/masks, batching, splits) as separate lots, one concept per PR.
3. Keep #79/#80/#81 lesson-level iterations and the deferred browser reviews #320/#329/#337 distinct from this implementation line; no browser or learner evidence is claimed by any entry in §15.