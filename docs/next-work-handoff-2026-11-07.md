# LLM Lab — current work handoff

**Snapshot:** 2026-11-07  
**Purpose:** identify the next useful work, record what is complete, and avoid reopening completed or superseded tasks.  
**Source of truth:** GitHub issues and pull requests. This document is a dated sequencing aid, not a second issue tracker.

## Current repository state

- 51 open issues; 11 P1, 17 P2, 6 P3 and 17 without exactly one priority label. No P0 slice is designated.
- One open PR was present in the live issue listing: [#628 — multimodal primary-source cross-check](https://github.com/JM-Brun/llm-lab/pull/628).
- [PR #623](https://github.com/JM-Brun/llm-lab/pull/623), the AiEdge CUDA Graphs source registration and extraction, is merged.
- [PR #626](https://github.com/JM-Brun/llm-lab/pull/626), the correction of the CUDA Graphs source-review status, is merged. Its Python CI and Quarto workflow both passed. The status `reviewed` means the integration decision was documented; it does **not** mean the article was fully scanned or accepted for canonical integration.
- [PR #628](https://github.com/JM-Brun/llm-lab/pull/628) extends the multimodal source review with primary-paper checks. Its head has changed during validation; previous workflow attempts were cancelled after subsequent pushes. Recheck the latest head and its latest CI + Quarto runs before considering merge.

## 1. Completed foundations — do not rebuild

### Canonical computational architecture

The central architecture in [#575](https://github.com/JM-Brun/llm-lab/issues/575) is implemented in `main`:

- One shared conditional next-token distribution is the boundary between the forward computation and its uses.
- Inference/generation, observed-target scoring/evaluation and teacher-forced training are sibling branches, not one execution loop.
- Generated-token feedback is distinct from observed-token conditioning.
- Prefill/decode are inference phases; teacher forcing is a training/scoring conditioning method.
- Q/K/V are projections computed inside each Transformer block from that block's input hidden states.
- The concept graph, computational graph, guided pedagogical route and Build implementation path remain separate representations.

The architecture, typed computational registry, eight-stage route, bilingual projections, persistent-spine/evaluation views and Build crosswalk have already been merged through PRs #577, #578, #581, #582, #586, #589, #594, #596, #598, #600, #601 and #604 (see the live [#584 integration record](https://github.com/JM-Brun/llm-lab/issues/584) for its detailed history).

**Constraint:** do not create another graph registry, convert computational edges into pedagogical prerequisites, or add a second visualization framework.

### Source ingestion — CUDA Graphs

The AiEdge CUDA Graphs source is registered, partially extracted and reviewed. The article's complete body and figures were not available for inspection, so its scan remains `partially-scanned`.

Current decision:
- Keep CUDA Graphs outside the core text-LM learning spine.
- Preserve the distinction from KV-cache reuse and continuous batching.
- Do not add a canonical concept, computational node, guided-route stage or reader-facing page from the partial evidence alone.
- Revisit only if the complete article/figures become accessible or a separate implementation-level source audit is justified.

### Multimodal source review

The multimodal visual-guide review has additional primary-source checks in [PR #628](https://github.com/JM-Brun/llm-lab/pull/628). Its editorial decision is to keep modality-specific mechanisms as an optional extension, not flatten them into the text autoregressive spine. The article's figures, comments, rights and implementation repositories remain unaudited; the source must remain partially scanned.

## 2. Immediate execution order

Keep one active learning slice and no more than three concurrent follow-up lots.

| Order | Work item | Why next | Required evidence |
|---|---|---|---|
| 0 — gate | [PR #628](https://github.com/JM-Brun/llm-lab/pull/628) | Finish the already-open source-review change before opening another source-ingestion PR. | Latest-head Python CI and Quarto site workflows pass; inspect changed extraction/review text; preserve partial-scan status and no premature curriculum integration. |
| 1 — active P1 | [#584 — reader-facing computational spine and crosswalk](https://github.com/JM-Brun/llm-lab/issues/584) | The architecture is integrated, but the bounded shared-core content audit and manual accessibility checks remain. | FR/EN scientific and editorial review of the first shared-core slice; then scoring/training page audit; manual screen-reader and native-breadcrumb evidence. |
| 2 — next P1/release gate | [#483 — Q/K/V rendered review and media provenance](https://github.com/JM-Brun/llm-lab/issues/483) and [#488 — citable public Q/K/V resource](https://github.com/JM-Brun/llm-lab/issues/488) | The Q/K/V content integration is complete; publication readiness still depends on rendered review, asset provenance and citation/release hygiene. | Desktop/mobile FR/EN review; keyboard and accessibility checks; each image either has verified provenance/reuse terms or remains link-only; then citation metadata, citation blocks, immutable release and changelog. |

The learner pilot [#447](https://github.com/JM-Brun/llm-lab/issues/447) is **downstream of #483**. Do not run it until the deployed Q/K/V pages pass the required rendered/accessibility review. One participant provides formative evidence only.

## 3. Remaining work by workstream

### A. Shared computational spine and reader experience — P1

Owner: [#584](https://github.com/JM-Brun/llm-lab/issues/584), parent [#575](https://github.com/JM-Brun/llm-lab/issues/575).

1. Complete the first bounded FR/EN source audit:
   - Q/K/V;
   - scaled dot-product attention;
   - causal masking;
   - positional encoding;
   - tensor shapes and conventions.
2. For each page pair, verify equations, dimensions, notation, mask polarity, citations, examples, cross-links and semantic parity. Reuse `docs/page-audit-inventory.md`; do not repeat already-completed checks.
3. Continue with the scoring branch: observed prefix/target, target probability, sequence likelihood, log-likelihood, NLL, cross-entropy, reduction, masking and numerical stability.
4. Continue with the training branch: shifted targets, teacher forcing, batch aggregation, gradients, optimizer and parameter update. Keep the missing end-to-end training implementation explicit.
5. Record manual screen-reader testing and native breadcrumb behavior separately from axe/Chromium checks.
6. Coordinate resource-map and typed-concept-graph UX with [#415](https://github.com/JM-Brun/llm-lab/issues/415) and [#416](https://github.com/JM-Brun/llm-lab/issues/416); do not duplicate their ownership.

### B. Q/K/V publication and validation — P1 / release readiness

Owners: [#483](https://github.com/JM-Brun/llm-lab/issues/483), [#488](https://github.com/JM-Brun/llm-lab/issues/488); dependent learner evidence: [#447](https://github.com/JM-Brun/llm-lab/issues/447).

- Inspect the deployed EN/FR pages at desktop and mobile sizes; verify equations, diagrams, local links, language switching, keyboard behavior and focus.
- Audit each original visual individually: creator, canonical source URL, context/caption, alt text, licence/permission and retrieval date. Keep unverified assets link-only; attribution alone is not a licence.
- Only after visual/provenance acceptance, prepare `CITATION.cff`, bilingual citation blocks, a changelog entry and an immutable release.
- Run the existing 15–20 minute learner pilot only after #483 is satisfied; report observations and interpretation separately.

### C. Tokenization and embeddings source family — P2

Owners: [#472](https://github.com/JM-Brun/llm-lab/issues/472) (handoff) and [#458](https://github.com/JM-Brun/llm-lab/issues/458) (structured backfill).

- Reconcile existing scans and PR evidence against current `main`; do not rescan sources without an identified evidence gap.
- Build a migration map from already-audited material to the current source registration/extraction templates.
- Complete only missing structured extractions and the cross-source comparison of convergence, complementary perspectives, disagreements and deliberate omissions.
- Validate catalogue/extraction records. Do not modify reader-facing pages, maps, routes or figures during extraction-only work.
- Keep unknown scan coverage and asset rights explicit; do not mark sources fully scanned from indexed text or repository snapshots.

### D. Minimal GPT build and training implementation — P1/P2

Owners: [#446](https://github.com/JM-Brun/llm-lab/issues/446), [#78](https://github.com/JM-Brun/llm-lab/issues/78), [#58](https://github.com/JM-Brun/llm-lab/issues/58).

- Keep the minimal inference path independent of optional decoding extensions and site tooling.
- Preserve existing public imports/behavior or document an approved migration.
- Maintain the concept-to-code prerequisite sequence.
- The complete corpus → examples → batching/splits → training loop → train/validation → checkpoint → trained-model evaluation pipeline is not yet demonstrated end to end. Do not imply that a page or random-weight inference demo proves training readiness.
- Implement one bounded component at a time, with tests and a direct link to the relevant concept/page.

### E. Learning maps and typed knowledge graph — P2

Owners: [#415](https://github.com/JM-Brun/llm-lab/issues/415), [#416](https://github.com/JM-Brun/llm-lab/issues/416), interaction follow-up [#417](https://github.com/JM-Brun/llm-lab/issues/417).

- Clarify guided route versus exploratory resource map using the existing curriculum; no competing taxonomy.
- Make relation types and direction semantically legible without imposing an artificial reading order.
- Preserve pointer, keyboard and touch behavior; touch and screen-reader checks remain distinct from mobile viewport/keyboard tests.
- Avoid a new graph database, schema or frontend framework.

### F. Page archetypes and progressive disclosure — P2

Owners: [#368](https://github.com/JM-Brun/llm-lab/issues/368), [#280](https://github.com/JM-Brun/llm-lab/issues/280), [#282](https://github.com/JM-Brun/llm-lab/issues/282).

- Audit page pairs by purpose, opening, learning outcomes, exposition, navigation, exercises, callouts and FR/EN parity.
- Apply archetypes selectively; do not force overview, concept, reference, build and practice pages into one rigid template.
- Preserve information when moving material between pages and keep editorial metadata out of reader-facing content.

### G. Reproducibility and contributor setup — P2

Owner: [#449](https://github.com/JM-Brun/llm-lab/issues/449).

- Verify documented setup in a genuinely clean Python 3.12/uv environment.
- Verify that generated bilingual route fragments match fresh output from the canonical generator.
- Run the documented Quarto generation/render and static checks locally; record environment and revision.
- Do not infer local reproducibility from hosted CI alone.

### H. Holonic interoperability — later P1 architecture research

Owner: [#512](https://github.com/JM-Brun/llm-lab/issues/512).

- Keep LLM Lab autonomous and self-contained.
- Map the interoperability contract to existing concept, source, extraction, page metadata and pedagogical structures.
- Transfer only demonstrated useful semantics; do not import Wiki Knowledge code or create a parallel ingestion engine.
- Resume cross-repository pilots only after local provenance and staged-ingestion workflows are validated.

## 4. Cross-cutting quality gates

For any reader-facing change:

- preserve existing information, figures, citations, exercises and implementation caveats;
- maintain FR/EN semantic parity, not merely matching page structure;
- keep `notion` / domain identity in the canonical concept registry rather than duplicating them as page tags;
- keep concept graph, computational graph, guided route and Build path distinct;
- validate source structure and Python tests, then Quarto render and local links;
- use the existing browser workflow for responsive, keyboard, focus and axe checks;
- report manual screen-reader and learner-pilot evidence separately;
- never claim training, evaluation, licence clearance or pedagogical effectiveness without the corresponding evidence.

## 5. Explicitly deferred / not justified yet

- A reader-facing CUDA Graphs lesson or canonical graph node: wait for complete source evidence and a distinct learner need.
- A single linear chain combining inference, scoring and training: architecturally incorrect.
- A new generic graph/diagram framework or per-concept workflow automation: unnecessary unless an existing concrete limitation is demonstrated.
- More sources for a topic when they repeat existing explanations without adding a distinct perspective, correcting an error or closing a documented gap.
- Broad site-wide redesign during bounded scientific/page audits.

## 6. Session operating sequence

1. Recheck live GitHub state, PR head SHAs and latest workflow runs.
2. Finish the current PR gate (#628) before starting a new source-ingestion change.
3. Select one active learning slice: #584 is the recommended next content slice.
4. Work in a bounded FR/EN page group; record evidence in the existing inventory and owning issue.
5. Merge only after latest-head CI and Quarto checks pass; keep browser and manual learner evidence claims precise.
6. Refresh this handoff only when ownership, order or evidence materially changes.

