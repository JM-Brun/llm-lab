# LLM Lab — remaining work handoff

**Snapshot:** 27 November 2026  
**Purpose:** one operational handoff for the currently active audit/validation threads. This document consolidates the next actions and evidence boundaries; the linked issues remain the owners of their respective work. It does not create a new backlog, registry, workflow or acceptance authority.

## Current execution order

### 1. Post-merge validation of the LLM overview refactor — #1208 (P1)

**Implemented:** the three refactor lots are merged through #1213: shorter bilingual overview, retrieval/RAG/context-engineering ownership, and Generation / complexity / training-loop boundaries. Browser coverage was extended in [PR #1803](https://github.com/JM-Brun/llm-lab/pull/1803) for the moved modules and Practice companions.

**Browser audit evidence from #1803 (head `6db7780`):** Secret scanning and the Python/domain CI job passed, but the Quarto/browser job failed. The failures are actionable findings, not a clean acceptance report:

- `exercises/llm-computational-complexity.html` (FR/EN, desktop/mobile): no native initially-collapsed worked-answer disclosure. The current source contains five self-check questions but no worked answers. This is a genuine Practice-content/contract gap; add answers in the dedicated Practice page, not the core lesson, then rerun the browser check.
- `llm-limits.html` (FR/EN, desktop): browser review found that the rendered page does not expose exactly one native Quarto breadcrumb. Inspect the rendered DOM and source navigation before deciding whether the source or test contract is wrong.
- `rag-memory-boundaries.html`, `document-retrieval.html`, `context-engineering.html` (FR/EN, desktop): generated single-stage context fails the route-context contract (repeated heading, incorrect stage/role or missing labelled stage link). Inspect the generated include and route metadata; fix the shared generator/metadata contract where possible rather than patching six pages independently.

These failures are distinct from the browser coverage addition itself. Do not weaken the assertions or mark the pages reviewed until the cause is resolved. `llm-limits` and the three moved core modules need source/DOM diagnosis; the complexity Practice page needs missing worked-answer content.

**Remaining, in order:**
1. Resolve the three failure groups above; update #1208/#1512 as appropriate and rerun the existing full browser audit.
2. Merge #1803 only after its complete CI/browser report passes and inspect its browser artefacts.
2. On the current main HEAD, inspect the rendered FR/EN overview and moved modules at desktop and mobile widths: equations/figures, responsive tables, anchors, internal links, language switching, focus/keyboard, Axe findings and console errors.
3. Recheck the nine overview self-check anchors and bilingual conservation against the existing inventory; do not infer preservation from source word counts.
4. Obtain a short novice review of the overview and the modules whose ownership changed, or record explicitly that learner review is deferred.
5. Close #1208 only when the technical and learner-review decisions are recorded. Successful Quarto rendering alone is not the full acceptance gate.

**Do not reopen:** the content-transfer plan, the three implementation lots, or the route topology unless the rendered inspection identifies a concrete regression.

### 2. Understand intellectual-contribution traceability — #1739 (P2)

**Contract:** #1778 is merged. The destination-evidence matrix is now at **8/20** lessons after #1794 and [#1802](https://github.com/JM-Brun/llm-lab/pull/1802).

**Verified in batch 2:** `llm-overview`, `text-data`, `positional-encoding`, `contextualized-representations`. The dossier records the learner-facing claim, exact source extraction item or explicit project-derived provenance, FR/EN destination anchors, presence and placement decision. It does not claim deployed-DOM or learner validation.

**Remaining:**
1. Audit the remaining 12 canonical Understand lessons in coherent batches, reusing the existing 20-page inventory and the #1778 contract.
2. For every contribution, distinguish source evidence from project-derived mathematical/computational consequences; do not claim a source supports more than its extracted item.
3. Verify current FR and EN destination, exact anchor and substantive content. A bibliography, related-page link or historical integration note is not proof of presence.
4. Compare contributions across lessons for real redundancy, missing transitions and distinct value. Do not force a quota of two or three.
5. Reconcile intellectual value with #280 (page archetypes), #1732 (Foundations boundaries) and #1741 (source diversity) without duplicating their matrices.
6. Only after the 20/20 evidence matrix exists, decide whether any small update to the existing editorial contract is needed. No parallel register, PAGE-MAP field or new ontology.

**Current evidence file:** [batch 2 destination evidence](understand-destination-evidence-batch-2-2026-11.md). The route index links both batch 1 and batch 2 evidence.

### 3. Foundations Phase 1 acceptance — #1732 (P2)

**Established:** architectural direction #1731 and Phase 1 audit handoff #1764 are merged. The source-level inventory covers 42 targeted bilingual pages, 125 concepts, 6 domains, 394 resource references and 315 reconstructed page IDs, with no unresolved references in the audited projections. These are source/projection findings, not published-page acceptance.

**Remaining blocker:** manual inspection of the 42 published HTML pages and explicit owner acceptance of the coverage matrix.

**Next actions:**
1. Inspect published HTML when Pages/cache access is available: math, figures, anchors, links, responsive/mobile, keyboard and accessibility.
2. Scientifically verify the recorded candidate anomalies against exact source:
   - literal `\\n` sequences in FR/EN Foundations exercise files;
   - double-escaped LaTeX in EN `likelihood.qmd`;
   - the Gaussian assumption wording in `attention-score-scaling`.
3. Record corrections only after confirming the source and preserve the distinction between derivation assumptions and simulation choices.
4. Obtain explicit owner acceptance of Phase 1. Do not start Phase 2 before that gate.
5. Only then arbitrate `scaling-laws`, `tensor` and `cosine-similarity`, typed relations/prerequisites and navigation representation. Keep the six existing domains unless evidence demonstrates a gap.

No mass metadata, domain, route or navigation migration is authorized by the current audit.

### 4. Advent Calendar collection validation — #1513 (P1)

**Established:** the 24 doors and bilingual titles are reconciled; #1546, #1670 and #1703 close the technical map/CTA, tracking-link and title-alignment repairs. The first-five source-level triage is recorded in #1664. #1793 refreshed the operational handoff.

**Remaining collection-level gates:**
1. Resolve the KL-divergence / cross-entropy prerequisite question with #416; do not add a prerequisite edge merely because two notions are mathematically related.
2. Verify the 24-day crosswalk against canonical concepts and computational nodes, preserving the distinct uses of a conditional distribution (generation, observed-target scoring/evaluation, training) and Q/K/V placement inside Transformer blocks.
3. Complete the varied pilots through their page owners: Day 03 tokenization (#1667), Day 09 Q/K/V (#1674), Day 21 cross-entropy (#1686).
4. Complete scientific, rendered-page and novice evidence for Days 01–03 through #1653–#1667. For Days 04–05, finish the outstanding XOR/representation and contextualization/prerequisite decisions in #1668–#1669.
5. Review the rendered archive as a collection: keyboard, screen reader, reduced motion, responsive layout, contrast, provenance and evergreen navigation.
6. Consume page-level decisions and only then record collection release readiness.

The 24 stories are independent editorial units, not a second prerequisite path. No learner-validation claim may be inferred from CI or source review.

### 5. Six LLM misconceptions — #1633 (P2)

**Completed:** Phase A source registration and extraction is merged in #1799. The Lin Perspective is registered with scoped source metadata and six atomic extraction items.

**Next phase is evidence mapping, not registry construction:**
1. For the six P0 cases, inspect current FR/EN pages and exact anchors, claims, limits, examples, Practice questions, worked answers and experiments.
2. Assign a justified coverage level per language and proof dimension; a related link alone is not coverage.
3. Verify concept/domain/resource IDs against canonical registries.
4. Test the proposed fields against these six cases only; distinguish coverage links from semantic, computational and prerequisite relations.
5. Decide whether existing Practice activities suffice before proposing new experiments. Teacher forcing/scoring/generation and RAG activities must reuse existing work where possible.
6. Validate the pilot and minimal schema before any `misconceptions.yml`, validator or generated index.

No per-misconception workflow or parallel ontology.

### 6. CI performance measurements — #1637 (P2)

**Completed:** documentation correction #1780 and repeated timing/profile record #1801 are merged. Three comparable 845-item observations have a median 166.98 s and range 126.17–174.29 s; the 841-item group is reported separately. Log-derived pre-test setup for the 845 group is 5.63 / 6.92 / 6.61 s (median 6.61 s). This is an estimate from first-log to pytest invocation, not the official job duration.

**Remaining:**
1. Collect further same-configuration observations; the 845-item range is still wide.
2. Separate pytest execution from runner/setup and dependency-install time with consistent measurements.
3. Profile named slow tests on the same baseline before proposing fixture sharing.
4. Run one measured fixture-sharing experiment only where repeated construction is demonstrated; test isolation and mutation safety.
5. Benchmark worker counts/scheduling; do not infer that more workers are faster.
6. Keep full-suite, coverage and full-corpus checks unchanged.

No performance improvement is claimed causally from the current small sample.

## Closed or superseded work — do not re-open without new evidence

- Practice page structural refactor: #1779 merged; #1512 remains the owner of the Practice inventory/acceptance rather than the implementation PR.
- Understand destination evidence batch 2: #1802 merged; coverage now 8/20.
- Browser-review coverage extension: #1803 is open; it extends the existing workflow, not a separate workflow.
- Source intake for Lin misconceptions: #1799 merged.
- LLM overview post-merge reconciliation: #1800 merged; #1208 remains open for current rendered review and learner evidence.
- CI timing documentation and repeated measurements: #1801 merged; #1637 remains open for more comparable observations and profiling.

## Operating rules for the next session

1. Start with the highest-priority unblocked acceptance gate: #1208 after #1803 checks, then collection-level #1513 gates.
2. Continue #1739 in bounded batches; never represent source inspection as learner validation.
3. Keep #1732 Phase 1 blocked until published HTML review and owner acceptance.
4. Advance #1633 only through the six-case evidence pilot; no schema or registry first.
5. Treat #1637 as a measured optimization task, not a correctness emergency.
6. Every status update must separate implementation, CI, source/scientific review, rendered/accessibility review and learner validation.
7. Reuse existing registries, validators, CI workflows and ownership issues. Do not create per-concept workflows, duplicate matrices or parallel canonical models.
