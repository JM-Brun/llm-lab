# Remaining-work register

**Snapshot:** 2026-11-03  
**Purpose:** consolidate the active work across `JM-Brun/llm-lab` and `JM-Brun/wiki-knowledge`, expose dependencies, and keep execution lots small enough to review and validate independently.

This is an execution register, not a second curriculum or a replacement for the owner issues. The GitHub issues linked below remain the source of truth for detailed acceptance criteria. Reconcile this snapshot against live issue state before starting a later phase.

## 1. Current status

- `llm-lab`: 47 open issues and no open pull requests at the time of this snapshot.
- `wiki-knowledge`: 4 open issues and no open pull requests at the time of this snapshot.
- LLM Lab PR [#306](https://github.com/JM-Brun/llm-lab/pull/306) (site-wide breadcrumbs) and [#307](https://github.com/JM-Brun/llm-lab/pull/307) (dedicated self-check pattern) are merged.
- PR #307's Quarto render and Python quality workflows completed successfully. The #306 GitHub Pages render and deployment jobs also completed successfully.
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

**Dependency:** confirm the design-token baseline from PR #189 is on `main` before treating it as authoritative. The output must distinguish measured failures, manual observations and untested criteria. A representative sample cannot establish site-wide WCAG conformance.

### P1 — Finish the existing pedagogical-template pilot

**Owner:** [#282 — pedagogical templates and page audit](https://github.com/JM-Brun/llm-lab/issues/282)

Research, source audit and template hierarchy are integrated. The remaining pilot is rendered review, already split into two bounded lots:

- [#316](https://github.com/JM-Brun/llm-lab/issues/316): entropy, cross-entropy and scaled-dot-product attention (three page pairs).
- [#317](https://github.com/JM-Brun/llm-lab/issues/317): Transformer architecture and Transformer overview (two page pairs).

Both lots should record FR/EN, desktop/mobile, viewport and reproducible observations. Three page pairs in #316 may exceed one hour if equations and interactive disclosures need detailed inspection; if so, split it into **#316-A: entropy/cross-entropy** and **#316-B: attention**, keeping the existing parent issue as the tracker. Do not create cosmetic fixes from preference alone.

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
5. Later, create or activate narrowly scoped work for the Transformer block, training/optimization, generation and evaluation. Do not bundle them into one PR.

For each concept, use three small stages: source/notation audit; explanation plus minimal implementation where scientifically useful; adversarial tests, bilingual parity and rendered review. For theory-only concepts, use derivation or pseudocode rather than artificial code.

## 5. Deferred LLM Lab work

These issues remain open, but should not compete with the P0/P1 validation gates unless a concrete dependency emerges.

- **Interactive execution:** [#268](https://github.com/JM-Brun/llm-lab/issues/268). Split into a technology/performance spike, one bilingual pilot cell on one page, then a decision on a second workbench. Do not implement tokenization and attention in parallel before the first pilot meets fallback, accessibility, mobile and maintenance criteria.
- **External resource curation:** [#266](https://github.com/JM-Brun/llm-lab/issues/266), [#147](https://github.com/JM-Brun/llm-lab/issues/147), [#86](https://github.com/JM-Brun/llm-lab/issues/86). Keep this selective; verify one candidate and its exact pedagogical role at a time. Do not create a resource catalogue or new page by default.
- **Visual rights and project licensing:** [#156](https://github.com/JM-Brun/llm-lab/issues/156) and [#163](https://github.com/JM-Brun/llm-lab/issues/163). Split the remaining asset inventory from owner-level licence decisions. Preserve existing external illustrations; do not infer reuse permission from attribution or public availability. Licence selection requires explicit project-owner approval.
- **Historical timeline:** [#197](https://github.com/JM-Brun/llm-lab/issues/197). Recheck the current timeline and acceptance criteria before treating the open issue as unimplemented; the timeline fragments and parity checks already exist.
- **Raschka chapter/appendix coverage:** [#95–#106](https://github.com/JM-Brun/llm-lab/issues/95). Treat each chapter/appendix as its own small audit and keep P2/P3 items deferred behind the foundational route.

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
