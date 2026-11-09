# LLM Lab — current work handoff and priority reconciliation

**Snapshot:** 2026-11-09 (Europe/Paris)  
**Main commit inspected:** `63ac93264f25da80624a7c1fff7d75a52bc47b7f`  
**Purpose:** reconcile live GitHub work, remove stale priority claims, and select one executable next slice.  
**Source of truth:** GitHub issues and pull requests. This document is a dated sequencing aid, not a second task tracker.

## 1. Live repository state

> **Update (later on 2026-11-09):** [#760](https://github.com/JM-Brun/llm-lab/pull/760) and [#778](https://github.com/JM-Brun/llm-lab/pull/778) are merged, so step 1 of § 3 is complete; the issue counts and labels below are unchanged. The only open PR at this update is [#787](https://github.com/JM-Brun/llm-lab/pull/787).

- **62 open issues:** P0=0, P1=6, P2=49, P3=7, unclassified=0.
- **One pre-existing content PR:** [#760 — audit loss and training-path continuity](https://github.com/JM-Brun/llm-lab/pull/760). This handoff is now proposed in [#778](https://github.com/JM-Brun/llm-lab/pull/778), so there are two open PRs including this documentation reconciliation.
- Recent completed work relevant to this handoff:
  - [#744](https://github.com/JM-Brun/llm-lab/pull/744) merged: Raschka Appendix D audit; [#105](https://github.com/JM-Brun/llm-lab/issues/105) closed.
  - [#767](https://github.com/JM-Brun/llm-lab/pull/767) merged: training examples → teacher forcing → loss → gradients audit.
  - [#777](https://github.com/JM-Brun/llm-lab/pull/777) merged: score-centering extraction provenance reconciled.
  - [#225](https://github.com/JM-Brun/llm-lab/issues/225) closed: conceptual curriculum ordering is integrated and source-audited; remaining rendered/accessibility/learner evidence has separate owners.

### PR #760 — current gate, not yet mergeable

The branch has since been updated against current `main`. Current PR head: `3320fa3a29c13bfa675232b247e0d4ed0cd0fcc2`; base: `63ac93264f25da80624a7c1fff7d75a52bc47b7f`. The comparison is now **ahead by 35, behind by 0** (16 changed files); the earlier divergence is resolved. GitHub reports `mergeable_state=unstable` while the current-head checks are running.

On this current head, Python CI run [42641761393](https://github.com/JM-Brun/llm-lab/actions/runs/42641761393) succeeded. The Quarto run [42641761338](https://github.com/JM-Brun/llm-lab/actions/runs/42641761338) has completed site render, registry generation, learning-map/graph/timeline checks and local-link validation; its targeted Playwright/Chromium page review is still in progress and has not produced a final artifact at this snapshot.

The earlier 18-case browser artifact from head `4ca908807e5dd25c5aa4324550922100faff318d` is historical only and must not be reused for the current head.

**Required next action:** wait for the current-head browser review, inspect its report and screenshots, then inspect the complete PR diff against `main` (especially the audit inventory and bilingual lesson edits). Merge only if the final checks and review are satisfactory; do not infer success from the earlier head.

## 2. Priority policy after reconciliation

P0 is intentionally empty: no currently verified urgent production defect justifies a P0 label. P1 is reserved for the small set of core learning, governance and prerequisite-gate owners; it is not a signal to execute all of them in parallel.

### P1 — retain as the genuinely high-value owners

| Issue | Why it remains P1 | Execution constraint |
|---|---|---|
| [#78 — concept-to-code learning path](https://github.com/JM-Brun/llm-lab/issues/78) | Owns the core Build sequence and its evidence boundaries | Coordinate, do not use it to bypass prerequisite gates or duplicate child issues |
| [#130 — high-level learning design](https://github.com/JM-Brun/llm-lab/issues/130) | Cross-cutting curriculum/navigation coordination | Parent/coordinator; no parallel curriculum rewrite |
| [#156 — visual-asset rights audit](https://github.com/JM-Brun/llm-lab/issues/156) | Unresolved provenance/permission status for embedded assets is a real reuse risk | Preserve assets; record rights evidence and escalate decisions, do not remove or relicense unilaterally |
| [#163 — project licensing decision](https://github.com/JM-Brun/llm-lab/issues/163) | Asset-level licensing and contributor scope remain unresolved | Keep the existing code/prose licence boundary; no asset licence without an explicit owner decision |
| [#220 — formative exercise sequence](https://github.com/JM-Brun/llm-lab/issues/220) | Published exercises still need independent subject-matter review of TR-A/B/C answer keys and qualifications | Reuse the existing activities and review protocol; no new quiz framework |
| [#656 — G8 training loop](https://github.com/JM-Brun/llm-lab/issues/656) | End-to-end parameter learning remains a major missing Build capability | **Blocked by the private prerequisite-knowledge gate. No implementation before explicit clearance.** |

P1 does not mean six concurrent workstreams. After #760, choose one P1 slice at a time. The governance work (#156/#163) may be handled as one coordinated decision, but its two acceptance scopes remain distinct.

### P2 — planned work, explicitly not competing with the active slice

- **Reader-facing validation:** [#584](https://github.com/JM-Brun/llm-lab/issues/584) now owns only the remaining manual FR/EN screen-reader and native-breadcrumb evidence. The computational spine, typed registry, route projections, page-group source audits and automated browser checks are already integrated. Do not reopen architecture or create another graph.
- **Q/K/V publication evidence:** [#483](https://github.com/JM-Brun/llm-lab/issues/483) owns deployed-page review, manual accessibility and asset provenance. [#447](https://github.com/JM-Brun/llm-lab/issues/447) is downstream: run the existing 15–20 minute independent learner pilot only after #483's prerequisites are met. One participant is formative evidence, not an efficacy estimate.
- **Other rendered reviews:** [#337](https://github.com/JM-Brun/llm-lab/issues/337), [#347](https://github.com/JM-Brun/llm-lab/issues/347), [#329](https://github.com/JM-Brun/llm-lab/issues/329) and [#341](https://github.com/JM-Brun/llm-lab/issues/341) remain bounded browser/manual evidence tasks. They can share a dedicated review session where the page sets overlap, but each issue keeps its own acceptance criteria.
- **Knowledge-map UX:** [#416](https://github.com/JM-Brun/llm-lab/issues/416) owns relation visualization semantics; [#417](https://github.com/JM-Brun/llm-lab/issues/417) owns interaction robustness. The route/resource distinction in #415 is already closed.
- **Editorial convergence:** [#282](https://github.com/JM-Brun/llm-lab/issues/282), [#317](https://github.com/JM-Brun/llm-lab/issues/317), [#280](https://github.com/JM-Brun/llm-lab/issues/280) and [#368](https://github.com/JM-Brun/llm-lab/issues/368) are pilot/broader page-archetype work, not permission for a site-wide rewrite.
- **Source research:** [#742](https://github.com/JM-Brun/llm-lab/issues/742) owns the Cameron Wolfe corpus; [#733](https://github.com/JM-Brun/llm-lab/issues/733) remains open only for the inaccessible complete Score Centering Substack article, while the primary paper, appendices and bounded code tests have been audited/integrated. Do not infer the article's contents from the paper.
- **Source portfolio:** [#756](https://github.com/JM-Brun/llm-lab/issues/756) coordinates 17 project-level audit tasks. Keep this P2: process one high-value project at a time, reuse existing scans, and create no more project issues until the current allocation is reconciled and evidence justifies expansion.
- **Source-method backfill:** [#472](https://github.com/JM-Brun/llm-lab/issues/472) owns the remaining decision-matrix/quality-transfer work; do not rescan sources or create experiments without a falsifiable protocol and explicit decision.
- **Interoperability:** [#512](https://github.com/JM-Brun/llm-lab/issues/512) is later architecture research. Two-way Wiki Knowledge pilots wait until the local staged-ingestion/provenance workflows are dependable; LLM Lab remains autonomous.

Other P2 items such as [#79](https://github.com/JM-Brun/llm-lab/issues/79), [#84](https://github.com/JM-Brun/llm-lab/issues/84), [#449](https://github.com/JM-Brun/llm-lab/issues/449) and [#632](https://github.com/JM-Brun/llm-lab/issues/632) remain planned; none currently outranks the open PR gate or the P1 evidence work.

### P3 — deliberately deferred

Keep browser-executable micro-code, optional history expansion, Git branch cleanup and later fine-tuning/LoRA chapter audits deferred unless a concrete learner need or maintenance risk changes their value. Do not promote them merely because they are easy to execute.

## 3. Ordered execution sequence

1. **Finish PR #760's current-head validation.** The branch is now based on current `main`; Python CI passed, while the targeted Quarto/Chromium review is still running. Inspect the final artifact and full diff; do not reuse old-head browser evidence.
2. **Select one P1 evidence slice.** Prefer the independent subject-matter review of the existing TR-A/B/C answer keys (#220), then address the asset-provenance/licensing decisions (#156/#163) according to the evidence and explicit owner decisions.
3. **Complete the Q/K/V release evidence (#483) and the manual shared-spine accessibility evidence (#584).** Keep the two scopes distinct even if the same reviewer can perform the screen-reader session.
4. **Run #447 only after #483 is satisfied.** Use the existing protocol; record limitations and avoid collecting identifying data.
5. **Schedule the remaining P2 browser checks as one bounded review block** where page sets overlap (#329/#337/#341/#347); do not create another browser workflow.
6. **Return to source portfolios only after the above evidence work is progressing**: one project/source family at a time under #756/#742/#472. Keep #733 blocked on actual source access.
7. **G8 implementation remains prohibited until the private prerequisite gate is explicitly cleared.** The Wolfe/Raschka audits do not clear it.

## 4. Reconciliation of earlier architecture and backlog notes

The uploaded `Architecture conceptuelle LLM.txt` is an earlier planning snapshot for #575. Its P0 actions (canonical computational YAML, relation types, validation and graph projection) have since been implemented through the merged #577/#578/#581/#586/#589/#594/#598/#600 work. The eight-stage guided route, typed computational registry and persistent-spine views are in `main`; #415 is closed. The remaining #584 work is manual reader/accessibility evidence, and #416 is the separate concept-graph visualization work. **Do not restart the old P0 architecture plan.**

The 2026-11-03 `work-backlog-status.md`, the 2026-11-07 handoff and the old priority headings in `roadmap.md` are dated snapshots. Use this handoff and live GitHub labels for execution. The curriculum order issue #225 is closed; its residual browser and learner checks remain with their current owners.

The [2026-11-09 adversarial project review](reviews/adversarial-project-review-2026-11-09.md) maps each of its recommendations to an existing owner and **changes no label or step above**. Three proposals await an explicit owner decision:

1. **Reference parity (G9) before training (G8):** loading pretrained GPT-2 small weights into the existing NumPy forward pass needs no backward pass, optimizer or training loop, so it stays outside the #656 gate; it would be a child of #78. The roadmap currently orders reference comparison after pre-training (P5, step 2).
   **Accepted by the maintainer on 2026-11-09, G9 part only.** `gpt2_weights.py` and `tests/unit/test_gpt2_reference_parity.py` compare the NumPy GPT with Hugging Face GPT-2 under identical random weights; no checkpoint is downloaded. Loading the published GPT-2 small checkpoint (A1, readable text) is not started: the download was not approved at this step.
2. **#268 from P3 to P2:** the review documents the concrete learner need that the P3 deferral asks for (local setup friction before any code runs).
3. **Clearing the #656 gate as the next P1 learning slice,** ahead of further training-related source audits; the gate itself stays in force until cleared.

## 5. Operating rules

- One active learning slice; at most three follow-up candidates.
- Preserve a single canonical owner per concern; reuse existing issues and inventories.
- Distinguish source audit, Python tests, Quarto render, browser/Axe evidence, manual assistive-technology review and learner outcomes.
- Do not create a new graph registry, workflow, per-concept issue or parallel exercise/ingestion system without a demonstrated limitation.
- Do not treat a P1 label, a merged documentation PR, or green CI as proof of learner mastery or implementation readiness.
