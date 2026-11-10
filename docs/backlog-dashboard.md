# LLM Lab — backlog dashboard

**Snapshot:** 2026-11-09  
**Source of truth:** GitHub issues and pull requests. This page is a navigation layer, not a second task tracker.

## Start here

- **Current handoff and ordered remaining work:** [next-work-handoff-2026-11-09.md](next-work-handoff-2026-11-09.md)
- **Latest strategic review and proposals awaiting an owner decision:** [adversarial project review 2026-11-09](reviews/adversarial-project-review-2026-11-09.md) (summarised in handoff § 4; no label changed)

- [All open issues](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen)
- [P0 — active slice](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP0)
- [P1 — next priorities](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP1)
- [P2 — planned](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP2)
- [P3 — deferred](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+label%3AP3)
- [Issues needing attention / unclassified](https://github.com/JM-Brun/llm-lab/issues?q=is%3Aissue+state%3Aopen+-label%3AP0+-label%3AP1+-label%3AP2+-label%3AP3)

Live snapshot 2026-11-09: **62 open issues**; priority labels P0=0, P1=6, P2=49, P3=7; **0 unclassified**. [#760](https://github.com/JM-Brun/llm-lab/pull/760) and the dashboard/handoff refresh [#778](https://github.com/JM-Brun/llm-lab/pull/778) are merged; the only open PR is [#787](https://github.com/JM-Brun/llm-lab/pull/787). The dated handoff linked above is the current ordered plan; older sections and snapshots are historical unless refreshed.

## Historical handoff — PR reconciliation (2026-11-04; superseded by the current handoff above)

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

**No active slice is selected.** [PR #760](https://github.com/JM-Brun/llm-lab/pull/760) was merged on 2026-11-09, which completes step 1 of the [handoff's ordered sequence](next-work-handoff-2026-11-09.md#3-ordered-execution-sequence). The next step is to choose one P1 evidence slice; the candidates below are unchanged.

There is deliberately no P0 issue. Choose one P1 slice at a time before starting implementation or source-ingestion work.

## Next — at most three follow-up work items

These are ordered candidates, not simultaneous active tasks.

1. **P1 evidence:** independent subject-matter review of the existing TR-A/B/C answer keys in [#220](https://github.com/JM-Brun/llm-lab/issues/220); no new exercise framework.
2. **P1 governance:** reconcile asset provenance and project-level licensing under [#156](https://github.com/JM-Brun/llm-lab/issues/156) and [#163](https://github.com/JM-Brun/llm-lab/issues/163), preserving all existing media pending an explicit decision.
3. **P2 release/accessibility evidence:** [#483](https://github.com/JM-Brun/llm-lab/issues/483) Q/K/V deployed review and media provenance, plus [#584](https://github.com/JM-Brun/llm-lab/issues/584) manual FR/EN screen-reader and breadcrumb checks. The learner pilot [#447](https://github.com/JM-Brun/llm-lab/issues/447) is downstream of #483.

## Dependency gates

- **G8:** [#656](https://github.com/JM-Brun/llm-lab/issues/656) remains P1 but blocked by the private prerequisite-knowledge review. No backward/optimizer/training-loop implementation before explicit clearance. #78 owns the broader concept-to-code sequence.
- **Q/K/V learner pilot:** #447 runs only after #483's deployed-page/accessibility prerequisites are met.
- **Score centering:** #733 waits for actual access to the complete Wolfe article; #742 owns the wider Wolfe corpus. The primary paper and implementation audit are already integrated.
- **Project portfolio:** #756 is P2; process one project audit at a time, reuse existing scans and do not expand the 17-task allocation without evidence.
- **Interoperability:** #512 is P2 and later; two-way Wiki Knowledge pilots wait for validated local staged-ingestion/provenance workflows.
- **Curriculum architecture:** #575 and #225 are closed. #415 route/resource projection is closed. #584 is residual manual accessibility evidence; #416 owns concept-graph visualization semantics. No new registry or route is required.

## Later

- **P2 — planned:** #329/#337/#341/#347 rendered reviews; #416/#417 knowledge-map UX; #472 source-method decision matrix; #742/#756 source audits; #79/#84 content/implementation follow-ups; #449 clean setup; #632 optional multimodal extension.
- **P3 — deferred:** #652 branch cleanup, #268 browser-executable micro-code, #197 optional history timeline and the later fine-tuning/LoRA chapter audits.
- **P1 — core owners:** #78, #130, #156, #163, #220 and #656. P1 does not mean parallel execution; #656 is gated.

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
