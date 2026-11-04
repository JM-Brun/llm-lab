# LLM Lab — backlog dashboard

**Snapshot:** 2026-11-04  
**Source of truth:** GitHub issues and pull requests. This page is a navigation layer, not a second task tracker.

## Start here

- [All open issues](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen)
- [P0 — active slice](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP0)
- [P1 — next priorities](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP1)
- [P2 — planned](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP2)
- [P3 — deferred](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP3)
- [Issues needing attention / unclassified](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+-label%3AP0+-label%3AP1+-label%3AP2+-label%3AP3)

40 issues are currently open. Thirty-four carry exactly one priority label (current split: P0=0, P1=11, P2=17, P3=6); six still need classification — #225, #266, #268, #280, #282, #368 — see [Issues needing attention](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+-label%3AP0+-label%3AP1+-label%3AP2+-label%3AP3). Re-run the filters above rather than relying on these dated counts.

## Handoff — PR reconciliation and next sessions (2026-11-04)

This is a **dated maintenance snapshot**, not an alternative issue tracker. Recheck [open PRs](https://github.com/JM-Brun/llm-lab/pulls?q=is%3Apr+is%3Aopen), current branch heads, `mergeable_state`, and the **latest-head** checks at the start of the next session: GitHub may be recomputing mergeability, and a green workflow on an older SHA is insufficient.

For the later #422 merge and outstanding validation gates, see the
[PR #422 follow-up](pr-422-followup-2026-11-04.md).

| PR | Verified reconciliation | Next gate |
|---|---|---|
| [#406](https://github.com/JM-Brun/llm-lab/pull/406) — softmax/probability ownership | Historical conflict with `main` reconciled by merge commit `15d89c8`; subsequent branch work changed the head again. The branch includes the then-current `main`, with six intended files changed. | Recheck its **current head**, mergeability and CI/Quarto checks, then inspect the four FR/EN pages for preserved interaction, mathematical rendering, learning-outcome parity and local links before considering merge. |
| [#410](https://github.com/JM-Brun/llm-lab/pull/410) — optional multi-head attention depth | Newly opened; source-level proposal only at this snapshot. | Check the latest CI/Quarto status, exact bilingual content preservation, callout collapse and placement in the core Transformer lesson. Do not confuse an `unknown` mergeability calculation with a proven Git conflict. |
| [#409](https://github.com/JM-Brun/llm-lab/pull/409), [#408](https://github.com/JM-Brun/llm-lab/pull/408), [#405](https://github.com/JM-Brun/llm-lab/pull/405) | Merged. Older governance PRs [#396](https://github.com/JM-Brun/llm-lab/pull/396) and [#407](https://github.com/JM-Brun/llm-lab/pull/407) were closed without merge and superseded by #409. | Do not reopen or duplicate the superseded work. |

### Small, independently reviewable next lots

1. **P1 — Close open PR gates (one PR at a time).** For #406 and #410, inspect the latest head, GitHub's actual `mergeable_state` after computation, Python CI, Quarto bilingual render, timeline parity and local-link checks. Fix only reproduced failures. Record browser validation separately; a successful Quarto build does not verify the interactive slider, responsive layout or keyboard experience.
2. **P1 — Reconcile editorial-audit findings after merge.** [The boundary audit](editorial-boundary-audit-2026-11-04.md) F1 is implemented in pending #406 but not closed until merged and reviewed. F2 was addressed by merged #405 (whitespace-splitting explanation belongs in tokenization-strategies, not text-data). F3/F4 are intentional distinctions, not invitations to remove useful reminders. Update the audit status rather than create a duplicate content ledger.
3. **P1 — Establish typed resource entities, in a separate PR.** The [knowledge-graph implementation audit](knowledge-graph-implementation-audit.md) identifies the remaining third-dimension gap: concept resources are currently page IDs. First specify stable resource IDs, kinds (page/demo/experiment/implementation/reference), bilingual handling, provenance and location; then add referential-integrity fixtures. Do not redesign the page graph or introduce a second graph database.
4. **P2 — Extend the concept-map projection only after the data contract.** Expose concept→domain membership through the existing canonical six-domain registry; expose non-page resource kinds only after their records and tests exist. Keep domain membership distinct from page primary domain, and never interpret conceptual prerequisites as a reading order.
5. **P2 — Browser and accessibility review in scoped batches.** Follow [the existing dashboard items](#next--at-most-three-follow-up-work-items) and issue [#320](https://github.com/JM-Brun/llm-lab/issues/320); capture page/language/viewport/browser and reproducible defects. The previously deferred screenshot work is not an automatic blocker for unrelated source-level changes.

### Verification and preservation contract

- Before editing a conflicting PR: list its changed files; compare base→branch and base→latest `main`; use a true merge/rebase or an explicit three-way reconciliation. Preserve improvements from **both** sides, including domains, page metadata, interactive exercises, citations and FR/EN parity. Never replace a modified canonical file with the stale PR version.
- After editing: ensure the branch contains latest `main`, compare the resulting PR diff, verify no malformed Quarto fences or duplicate/omitted interactive IDs, then check the **new** head's workflows. Avoid calling `mergeable: false` a conflict when GitHub reports `mergeable_state: unknown`.
- Maintain **one source of truth** per concern: `data/domains.yml`, `data/concepts.yml`, page-map metadata, and `docs/content-section-mapping.md`. Source-level validation, rendered-site CI, browser inspection and pedagogical evidence are separate claims.
- The older [remaining-work register](work-backlog-status.md) is a dated 2026-11-03 snapshot with historical issue counts; refresh it from live GitHub data before using those counts for prioritisation. The [roadmap](roadmap.md) is longer-term, not a live PR queue.

## Operating rule

**One active learning slice at a time.** P0 is a temporary execution designation, not a measure of importance or a permanent severity rating. P1 contains the next work and cross-cutting risks; P2 is planned work; P3 is intentionally deferred or optional.

Do not infer that an entire issue is blocked when only one component is waiting on a prerequisite. The dependency notes below identify the specific blocked workstream.

## Now — active

**No P0 slice is currently designated.** The previous P0 slice, [#82](https://github.com/JM-Brun/llm-lab/issues/82), is closed: the source-level trace (text → token IDs → embeddings → contextual states) is complete, and its rendered-page browser review was transferred to [#320](https://github.com/JM-Brun/llm-lab/issues/320) (P2) — a release check, not an implementation blocker. Attention and GPT-block implementation has since landed under #78/#270.

Select the next single active slice before resuming implementation work; the candidates below are sequencing suggestions, not decisions.

## Next — at most three follow-up work items

These are sequencing candidates, not simultaneous active tasks.

1. [#78 — Reconcile the concept-to-code roadmap](https://github.com/JM-Brun/llm-lab/issues/78). Preserve explicit prerequisite gates and link implementation evidence.
2. [#58 — Corpus → training examples](https://github.com/JM-Brun/llm-lab/issues/58). Continue the remaining gaps (corpus loading, packing, padding/masks, batching, splits), one concept per PR, per the live register.
3. The P2 browser-review lot ([#320](https://github.com/JM-Brun/llm-lab/issues/320), [#329](https://github.com/JM-Brun/llm-lab/issues/329), [#337](https://github.com/JM-Brun/llm-lab/issues/337), [#341](https://github.com/JM-Brun/llm-lab/issues/341), [#347](https://github.com/JM-Brun/llm-lab/issues/347)) as one dedicated review session; no learner or visual evidence is claimed until then.

## Dependency gates

- **Attention and causal masking:** [#80](https://github.com/JM-Brun/llm-lab/issues/80) and [#81](https://github.com/JM-Brun/llm-lab/issues/81) followed the closed #82. #80 owns scaled dot-product attention invariants; #81 owns causal-mask semantics and future-token leakage tests.
- **Homepage:** [#154](https://github.com/JM-Brun/llm-lab/issues/154) is closed (PR #340); its rendered desktop/mobile and accessibility review is tracked in [#341](https://github.com/JM-Brun/llm-lab/issues/341) (P2).
- **GPT/pretraining:** the Chapter 5 source audit [#99](https://github.com/JM-Brun/llm-lab/issues/99) is closed and confirms the training gap; any pretraining implementation must follow the prerequisite sequence maintained in #78. Do not treat page existence as readiness.
- **Curriculum architecture:** #130 coordinates; the curriculum map from #87 (closed, PR #336) is maintained in `docs/content-section-mapping.md`; #78 owns concept-to-code sequencing; page-level reading experience continues under #280/#282 (successors of the closed #61).
- **LLM overview:** [#95](https://github.com/JM-Brun/llm-lab/issues/95) is the upstream Chapter 1 coverage audit; [#108](https://github.com/JM-Brun/llm-lab/issues/108) delivered the reader-facing bilingual panorama (closed via PR #343; rendered review transferred to [#337](https://github.com/JM-Brun/llm-lab/issues/337), P2). The audit found the gap; the panorama implements the synthesis. They are complementary, not duplicates.
- **Visual system:** [#190](https://github.com/JM-Brun/llm-lab/issues/190) owns benchmark-derived design decisions; [#191](https://github.com/JM-Brun/llm-lab/issues/191) owns rendered bilingual validation. [PR #189](https://github.com/JM-Brun/llm-lab/pull/189) is merged; that does not complete #191.
- **Asset governance:** [#156](https://github.com/JM-Brun/llm-lab/issues/156) audits individual asset provenance; [#163](https://github.com/JM-Brun/llm-lab/issues/163) owns the project-level licensing decision.

These are documented dependencies, not native GitHub “blocked by” relations. Do not apply `flow:blocked` to an entire issue when only a subtask is waiting.

## Later

- **P2 — planned:** [#58](https://github.com/JM-Brun/llm-lab/issues/58) corpus-to-training examples; [#79](https://github.com/JM-Brun/llm-lab/issues/79) logits and loss; #80/#81 attention and masking; [#84](https://github.com/JM-Brun/llm-lab/issues/84) generation/evaluation; [#86](https://github.com/JM-Brun/llm-lab/issues/86) resource curation; [#95](https://github.com/JM-Brun/llm-lab/issues/95), [#97](https://github.com/JM-Brun/llm-lab/issues/97), [#102](https://github.com/JM-Brun/llm-lab/issues/102), [#103](https://github.com/JM-Brun/llm-lab/issues/103) chapter/source audits; [#147](https://github.com/JM-Brun/llm-lab/issues/147) complementary pedagogy; [#154](https://github.com/JM-Brun/llm-lab/issues/154) design benchmark. Closed since the 2026-11-02 snapshot: #98, #99, #108, #114, #154.
- **P3 — deferred/optional:** [#100](https://github.com/JM-Brun/llm-lab/issues/100), [#101](https://github.com/JM-Brun/llm-lab/issues/101), [#104](https://github.com/JM-Brun/llm-lab/issues/104), [#105](https://github.com/JM-Brun/llm-lab/issues/105), [#106](https://github.com/JM-Brun/llm-lab/issues/106) advanced chapter/appendix audits; [#197](https://github.com/JM-Brun/llm-lab/issues/197) optional history timeline.
- **P1 — cross-cutting risks:** #130 coordination, #156/#163 asset rights, #191 rendered design-system validation. Prioritize actual risk and dependencies rather than starting all P1 issues in parallel.

## Recently reconciled

- [#83](https://github.com/JM-Brun/llm-lab/issues/83) closed as duplicate of #58; #58 is canonical.
- [#192](https://github.com/JM-Brun/llm-lab/issues/192) closed after its work was transferred to existing owner issues. Closure does not mean the proposed UX features are implemented.
- [PR #189](https://github.com/JM-Brun/llm-lab/pull/189) and [PR #199](https://github.com/JM-Brun/llm-lab/pull/199) merged.
- [PR #200](https://github.com/JM-Brun/llm-lab/pull/200) closed without merge; its implementation is not delivered.
- [PR #214](https://github.com/JM-Brun/llm-lab/pull/214) was merged on 2026-11-02 (*Add bilingual active checks to core LLM concepts*); the previous note describing it as an open draft was stale.
- [#61](https://github.com/JM-Brun/llm-lab/issues/61) closed: progressive-disclosure source audit complete; page convergence continues under [#280](https://github.com/JM-Brun/llm-lab/issues/280) and [#282](https://github.com/JM-Brun/llm-lab/issues/282).
- [#87](https://github.com/JM-Brun/llm-lab/issues/87) closed (PR #336): the three-depth curriculum crosswalk is maintained in `docs/content-section-mapping.md`; the rendered-navigation check is transferred to #337.
- [#108](https://github.com/JM-Brun/llm-lab/issues/108) closed (PR #343): bilingual LLM panorama published; rendered review transferred to #337.
- [PR #383](https://github.com/JM-Brun/llm-lab/pull/383) (interactive learning map), [PR #387](https://github.com/JM-Brun/llm-lab/pull/387) (RoPE separation) and [PR #389](https://github.com/JM-Brun/llm-lab/pull/389) (learning-path gate reconciliation) merged on 2026-11-04.

## Label conventions

Each open issue should carry one label from each mandatory family:

- **Priority:** `P0`, `P1`, `P2`, `P3`.
- **Type:** `type:epic`, `type:feature`, `type:audit`, `type:bug`, `type:research`, `type:documentation`, `type:maintenance`.
- **Area:** `area:curriculum`, `area:pedagogy`, `area:scientific-quality`, `area:sources`, `area:visuals-ux`, `area:i18n`, `area:governance`.
- **Flow (optional):** use only when verified. No open issue currently carries a flow label; the stale `flow:in-progress` on the closed #82 was removed on 2026-11-04. No `flow:blocked` labels are applied.

Examples:
- `is:issue state:open label:P1`
- `is:issue state:open label:"type:audit" label:"area:curriculum"`
- `is:issue state:open -label:P0 -label:P1 -label:P2 -label:P3`

## Review cadence

At the start of each work session:
1. Re-run the priority filters and inspect recently updated issues/PRs.
2. Confirm whether the #320 browser-review gate has changed.
3. Keep one active learning slice; choose at most three next candidates.
4. Update dependency notes only when the underlying prerequisite or owner changes.
5. Record evidence in the canonical issue/PR. This dashboard should remain a concise index, not a duplicate changelog.
