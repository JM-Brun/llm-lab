# LLM Lab — backlog dashboard

**Snapshot:** 2026-11-02  
**Source of truth:** GitHub issues and pull requests. This page is a navigation layer, not a second task tracker.

## Start here

- [All open issues](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen)
- [P0 — active slice](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP0)
- [P1 — next priorities](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP1)
- [P2 — planned](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP2)
- [P3 — deferred](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP3)
- [Issues needing attention / unclassified](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+-label%3AP0+-label%3AP1+-label%3AP2+-label%3AP3)

All 31 open issues have exactly one priority, one `type:*` label and one `area:*` label. The current priority split is P0=1, P1=8, P2=16, P3=6. Re-run the filters above rather than relying on these dated counts.

## Operating rule

**One active learning slice at a time.** P0 is a temporary execution designation, not a measure of importance or a permanent severity rating. P1 contains the next work and cross-cutting risks; P2 is planned work; P3 is intentionally deferred or optional.

Do not infer that an entire issue is blocked when only one component is waiting on a prerequisite. The dependency notes below identify the specific blocked workstream.

## Now — active

### [#82 — Trace text → token IDs → embeddings → contextual states](https://github.com/JM-Brun/llm-lab/issues/82)

- Status: P0; `flow:in-progress`.
- Completed: bilingual worked trace, numerical example, shape reasoning, counterexamples, executable example, CI and Quarto checks.
- Remaining gate: browser inspection of the rendered FR/EN pages and relevant SVGs at desktop and mobile widths; record actual observations.
- Do not expand into attention implementation, full GPT implementation or training before this gate and the separate prerequisite review are complete.

## Next — at most three follow-up work items

These are sequencing candidates, not simultaneous active tasks.

1. [#61 — Audit progressive disclosure and page-level reader experience](https://github.com/JM-Brun/llm-lab/issues/61). Keep this as a bounded audit; do not turn it into a bulk rewrite.
2. [#78 — Reconcile the concept-to-code roadmap](https://github.com/JM-Brun/llm-lab/issues/78). Preserve explicit prerequisite gates and link implementation evidence.
3. [#87 — Finalize the three-depth curriculum map](https://github.com/JM-Brun/llm-lab/issues/87). Map panorama, guided build and deep dives to actual pages and honest coverage states.

## Dependency gates

- **Attention and causal masking:** [#80](https://github.com/JM-Brun/llm-lab/issues/80) and [#81](https://github.com/JM-Brun/llm-lab/issues/81) follow #82. #80 owns scaled dot-product attention invariants; #81 owns causal-mask semantics and future-token leakage tests.
- **Homepage attention demo:** only this component of [#154](https://github.com/JM-Brun/llm-lab/issues/154) depends on #82, #80 and #81. Independent homepage orientation work may proceed.
- **GPT/pretraining:** [#98](https://github.com/JM-Brun/llm-lab/issues/98) and [#99](https://github.com/JM-Brun/llm-lab/issues/99) must follow the prerequisite sequence maintained in #78; do not treat their existence as readiness.
- **Curriculum architecture:** #130 coordinates; #87 owns the curriculum map; #78 owns concept-to-code sequencing; #61 owns page-level reading experience.
- **LLM overview:** [#95](https://github.com/JM-Brun/llm-lab/issues/95) is the upstream Chapter 1 coverage audit; [#108](https://github.com/JM-Brun/llm-lab/issues/108) owns the reader-facing bilingual panorama. The audit found the gap; the panorama implements the synthesis. They are complementary, not duplicates.
- **Visual system:** [#190](https://github.com/JM-Brun/llm-lab/issues/190) owns benchmark-derived design decisions; [#191](https://github.com/JM-Brun/llm-lab/issues/191) owns rendered bilingual validation. [PR #189](https://github.com/JM-Brun/llm-lab/pull/189) is merged; that does not complete #191.
- **Asset governance:** [#156](https://github.com/JM-Brun/llm-lab/issues/156) audits individual asset provenance; [#163](https://github.com/JM-Brun/llm-lab/issues/163) owns the project-level licensing decision.

These are documented dependencies, not native GitHub “blocked by” relations. Do not apply `flow:blocked` to an entire issue when only a subtask is waiting.

## Later

- **P2 — planned:** [#58](https://github.com/JM-Brun/llm-lab/issues/58) corpus-to-training examples; [#79](https://github.com/JM-Brun/llm-lab/issues/79) logits and loss; #80/#81 attention and masking; [#84](https://github.com/JM-Brun/llm-lab/issues/84) generation/evaluation; [#86](https://github.com/JM-Brun/llm-lab/issues/86) resource curation; [#95](https://github.com/JM-Brun/llm-lab/issues/95), [#97](https://github.com/JM-Brun/llm-lab/issues/97), [#98](https://github.com/JM-Brun/llm-lab/issues/98), [#99](https://github.com/JM-Brun/llm-lab/issues/99), [#102](https://github.com/JM-Brun/llm-lab/issues/102), [#103](https://github.com/JM-Brun/llm-lab/issues/103) chapter/source audits; [#108](https://github.com/JM-Brun/llm-lab/issues/108) overview; [#114](https://github.com/JM-Brun/llm-lab/issues/114) tokenization/embedding source audit; [#147](https://github.com/JM-Brun/llm-lab/issues/147) complementary pedagogy; [#154](https://github.com/JM-Brun/llm-lab/issues/154) homepage; [#190](https://github.com/JM-Brun/llm-lab/issues/190) design benchmark.
- **P3 — deferred/optional:** [#100](https://github.com/JM-Brun/llm-lab/issues/100), [#101](https://github.com/JM-Brun/llm-lab/issues/101), [#104](https://github.com/JM-Brun/llm-lab/issues/104), [#105](https://github.com/JM-Brun/llm-lab/issues/105), [#106](https://github.com/JM-Brun/llm-lab/issues/106) advanced chapter/appendix audits; [#197](https://github.com/JM-Brun/llm-lab/issues/197) optional history timeline.
- **P1 — cross-cutting risks:** #130 coordination, #156/#163 asset rights, #191 rendered design-system validation. Prioritize actual risk and dependencies rather than starting all P1 issues in parallel.

## Recently reconciled

- [#83](https://github.com/JM-Brun/llm-lab/issues/83) closed as duplicate of #58; #58 is canonical.
- [#192](https://github.com/JM-Brun/llm-lab/issues/192) closed after its work was transferred to existing owner issues. Closure does not mean the proposed UX features are implemented.
- [PR #189](https://github.com/JM-Brun/llm-lab/pull/189) and [PR #199](https://github.com/JM-Brun/llm-lab/pull/199) merged.
- [PR #200](https://github.com/JM-Brun/llm-lab/pull/200) closed without merge; its implementation is not delivered.
- [PR #214](https://github.com/JM-Brun/llm-lab/pull/214) remains open in Draft. No merge decision is implied.

## Label conventions

Each open issue should carry one label from each mandatory family:

- **Priority:** `P0`, `P1`, `P2`, `P3`.
- **Type:** `type:epic`, `type:feature`, `type:audit`, `type:bug`, `type:research`, `type:documentation`, `type:maintenance`.
- **Area:** `area:curriculum`, `area:pedagogy`, `area:scientific-quality`, `area:sources`, `area:visuals-ux`, `area:i18n`, `area:governance`.
- **Flow (optional):** use only when verified. Currently only #82 has `flow:in-progress`; no `flow:blocked` labels are applied.

Examples:
- `is:issue state:open label:P1`
- `is:issue state:open label:"type:audit" label:"area:curriculum"`
- `is:issue state:open -label:P0 -label:P1 -label:P2 -label:P3`

## Review cadence

At the start of each work session:
1. Re-run the priority filters and inspect recently updated issues/PRs.
2. Confirm whether #82's browser gate has changed.
3. Keep one active learning slice; choose at most three next candidates.
4. Update dependency notes only when the underlying prerequisite or owner changes.
5. Record evidence in the canonical issue/PR. This dashboard should remain a concise index, not a duplicate changelog.
