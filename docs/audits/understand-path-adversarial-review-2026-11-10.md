# Adversarial review — Understand learning path

**Date:** 2026-11-10
**Scope:** the eight-stage Theory / Understand route (`data/guided-route.yml`), its sidebar, its `suggested_route` chain and the lessons it links, as of `origin/main` at `0b0110d`.
**Method:** source inspection only. No rendered-page review, no link check, FR pages not read in depth.
**Status:** recommendations; F1 option B (a new `training-loop` Understand page) has since been drafted on branch `feat/understand-training-loop-page`. All other findings remain open.
**Constraint:** every proposal below adds, moves or re-links content. None removes information.

## Preserve

- The "one predictive computation, three uses" framing (generate, score, learn).
- Early generation preview, revisited in detail later.
- Separation of Understand and Build; Deepen and Practice as attached, growing destinations (see the 2026-11-09 decision in `docs/learning-path.md`).
- Scoped claims and cited sources.

## Findings

### P1 — the path stops before it delivers what it promises

**F1. Stage 8 over-promises.** The objective says "optimization, pretraining and validation". The stage contains `loss` and `gradients` only.
- `gradients` has `suggested_route.next: null`.
- Optimizers appear in one collapsed callout and one sentence on SGD. AdamW appears nowhere on the site. Learning rate appears only on the `gradients` page.
- No Understand page covers the training loop as a concept, a train/validation split, overfitting or generalization, or pretraining at scale. `scaling-laws` is only an optional link from stage 8.
- Reconciliation with `docs/audits/raschka-appendix-d-training-loop-audit-2026-11-09.md`: that audit decided **no new pages or route stages for warmup, cosine decay, clipping and monitoring**, and keeps them as G8 (Build) / Deepen material. F1 does not contradict it. It concerns the *conceptual* minimum (loop, optimizer idea, validation, overfitting) that the existing stage objective already claims. Maintainer decision required on which option below.
  - **Option A (smallest):** reword the stage-8 objective to match the two pages it contains, and move "pretraining and validation" to a stated optional extension. Loses nothing.
  - **Option B:** add one Understand page, "From gradients to a trained model": the training loop as repeated forward / loss / backward / update, SGD to adaptive optimizers in one paragraph, train versus validation loss, overfitting and generalization, and a recall that the test set stays held out. AdamW internals, warmup, cosine decay and clipping stay in Deepen / Build as the audit decided. Needs FR/EN pages, route data, both sidebars, `suggested_route`, page-audit inventory, and a note in `docs/learning-path.md`.

**F2. The "adaptation and use" extension is declared, not delivered.** `docs/learning-path.md` promises pretrained checkpoints, SFT, instruction tuning, prompting and RAG as a discoverable optional extension. Today the material is spread across a table in `llm-overview`, `in-context-learning` (Deepen), `llm-evolution`, `hybrid-llm-architectures` and the glossary. There is no preference-optimization / RLHF treatment. A learner who finishes the path cannot say how a base model becomes an assistant.
- **Fix:** an optional route stage 9, composed first from existing pages (`llm-overview` learning row, `in-context-learning`, `llm-limits`), with a new page only for the residual gap. Keep it optional and outside the mandatory eight stages, as the learning-path doc already specifies.

**F3. Orphan tail in the sidebar.** `transformer-architectures` and `llm-limits` follow "Loss and gradients" in the EN sidebar, yet both have `previous: null` and `next: null`, and the route lists them as optional pages of stage 1 (`orientation`). The sidebar implies "end of path"; the route implies "side material for stage 1".
- **Fix:** make sidebar and route agree. Either they become the chain of F2's stage 9 (with real `suggested_route`), or the sidebar places them under the orientation block. Moving them removes no content.

### P2 — ordering and pedagogy

**F4. `generation` appears twice in the route and once in the chain.** It is stage 1 and stage 6. The `suggested_route` chain goes `llm-overview → generation → text-data` and later `causal-masking → logits`, so a reader following the arrows never reaches the stage-6 detail pass.
- `decoding-strategies` (2.8k words) is optional in stage 6, yet temperature, top-k and top-p are the core of "select a token with a decoding policy".
- **Fix:** promote `decoding-strategies` to a core page of stage 6, and add the stage-6 revisit to the arrow chain after `entropy`, or split the preview from the decode detail.

**F5. Stage-5 `entropy` feeds stage-7 `cross-entropy` across an interruption (stage 6).** `likelihood` opens the scoring stage with `previous: entropy`.
- **Fix:** a short recall at the start of `likelihood` / `cross-entropy`, or `entropy` placed first in stage 7.

**F6. Block internals are thin in Understand.** MLP, residual connections and normalization share one overview page (`transformer`, about 1.8k words) plus an advanced Q/K/V page. The numeric block trace lives in `transformer-block-walkthrough`, which sits only in Build.
- **Fix:** a contextual link from `transformer` to the walkthrough, or a short worked block example in Understand. Per the contracts, keep depth in Deepen.

**F7. No stage-level completion signal.** Self-checks are in end-of-page blocks (PR #943) and exercises are separate. Nothing tells a reader a stage is understood.
- **Fix, within the contracts:** one question per stage stored in `data/guided-route.yml` and shown once, on the learning map. No end-of-page list duplicating the menu.

### P3 — entry and orientation

**F8. No prerequisites on entry.** No maths or Python level is stated. An unvalidated reading-time figure is forbidden by the contracts, so state prerequisites instead (vectors and matrices, basic probability, basic Python).

**F9. Three overlapping path descriptions.** The landing page's three entries, the five-movement summary in `docs/understand-path-overview.md` and the eight canonical stages. The docs explain the relationship; a reader of the live site sees only some of them.
- **Fix:** keep eight stages canonical; reuse the five movement labels as stage groups on the learning map. Do not render the same dimension twice (contract).

**F10. "Run locally" friction.** The landing page notes that code blocks do not execute in the page. An Understand-only reader cannot try an example without a local Python environment.
- **Fix:** optional in-browser execution for a few key blocks, or a hosted-notebook link. Separate decision; needs a security and maintenance review.

### P4 — hygiene

**F11. Parity checks should key on page ID, not filename.** EN and FR use different file names for some pages (`probabilities` / `probabilites`, `likelihood`, `embedding-linearity`, `experimental-evaluation`). A filename-based check would report false gaps and could miss a real one.

**F12. `docs/learning-path.md` is about 63 KB** and mixes decisions, a weekly rhythm and dated status snapshots. Split into a short canonical path document and an archive file. Move text, delete none.

## Corrections after the first implementation pass

Re-reading the pages before editing showed three findings were overstated. They are kept above for traceability and corrected here.

- **F4 (partly withdrawn).** `decoding-strategies` is a `level:advanced`, `destination:deepen` page, and `generation` already covers greedy selection, temperature, top-k and top-p. Promoting it to core would contradict its level and the ownership contract. The remaining issue is only that the single `previous`/`next` pair cannot place `generation` twice in the arrow chain; the route data already lists it in stages 1 and 6. A reader-facing signal for the stage-6 revisit is still open.
- **F5 (withdrawn).** `cross-entropy` already warns against confusing it with the entropy of the predicted distribution, and `likelihood` does not depend on `entropy`. A recall adds little.
- **F6 (withdrawn).** `transformer` already links the block walkthrough (EN line 116, FR line 188) and the worked configuration page. The open question is whether Understand readers should meet a worked block trace without entering Build; that is an editorial choice, not a missing link.

## Implemented so far

- F1, option B: new `training-loop` lesson (EN/FR), route stage 8, sidebars, registries, docs.
- F8: one prerequisite sentence on each landing page (EN `site/en/index.qmd`, FR `site/index.qmd`). The stated prerequisites come from the lessons' content and have not been validated with learners.

## Proposed issues (not yet created)

| # | Title | Findings | Priority |
|---|---|---|---|
| 1 | Decide stage-8 scope: reword (A) or add "From gradients to a trained model" (B) | F1 | P1 |
| 2 | Optional route stage 9, "From base model to assistant", composed from existing pages | F2, F3 | P1 |
| 3 | Reconcile sidebar tail and route for `transformer-architectures` / `llm-limits` | F3 | P1 |
| 4 | Reader-facing signal for the stage-6 revisit of `generation` (not promotion of `decoding-strategies`) | F4 | P2 |
| 5 | (withdrawn) entropy recall | F5 | — |
| 6 | Decide whether Understand gets a worked block trace | F6 | P3 |
| 7 | Per-stage check question in `guided-route.yml`, shown on the learning map | F7 | P2 |
| 8 | (done on landing pages) prerequisites; consider `llm-overview` | F8 | P3 |
| 9 | Use five movements as stage groups on the learning map | F9 | P3 |
| 10 | Parity check keyed on page ID | F11 | P4 |
| 11 | Split `docs/learning-path.md` into canonical doc and archive | F12 | P4 |

Findings F10 (in-browser execution) needs a separate decision before an issue is opened.

## Verification still owed

- Render EN and FR and walk the arrow chain end to end, including the `generation` revisit (F4).
- Confirm the FR pages mirror F1–F3 before any change (parity rule).
- Check the sidebar against `guided-route.yml` in the rendered output (F3).
