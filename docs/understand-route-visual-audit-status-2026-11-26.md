# Understand route — visual audit status (2026-11-26)

**Purpose:** one status page for the source-level visual audit of the canonical Understand route. This document consolidates the applied pilots; the individual pilot records remain the detailed design evidence.

## Current status

| Validation layer | Status |
|---|---|
| Page-by-page source review | **20/20 core pages reviewed** |
| Figure purpose, redundancy and placement decisions | Recorded in the pilot audit documents |
| EN/FR source pairing and image references | Checked for the pages changed in the pilots |
| Mobile source compositions | Added where wide existing diagrams needed them; existing responsive visuals retained where already adequate |
| Quarto build | **Passed on pre-sync head** `84fed3f`; full-site render succeeded in run [45962930428](https://github.com/JM-Brun/llm-lab/actions/runs/45962930428). Rerun on synced head `fb75013` is pending. |
| Rendered browser inspection | **Automated review passed on pre-sync head**: 42 cases, zero audit failures. Rerun on synced head is pending. |
| Mobile viewport inspection | **Partial**: 20 cases at 390 px across selected pages; not all 20 core pages have mobile evidence. No tablet-wide review is claimed. |
| Accessibility-tree inspection | **Not completed**. Axe reported zero violations in 22 desktop page-language scans. The report also recorded 14 MathJax 4 page errors on EN `embedding-space` during keyboard focus traversal; investigate separately. |
| New-asset owner provenance confirmation | **Pending** |
| New-asset licence decision | **Pending** under #156/#163 |

Source-level review is not equivalent to rendered validation. No claim is made that every figure is visually correct at runtime or accessible in the rendered site.

## Page coverage and decisions

| Understand page | Decision / change | Detailed record |
|---|---|---|
| LLM overview | Six-stage generation diagram now has EN/FR mobile variants. Position handling is architecture-dependent; the loop returns to initial representations. The “one computation, three uses” figure already had mobile variants. | [Fourth pilot](visual-audit-fourth-pilot-2026-11-26.md) |
| Text data / tokenization | No new figure. Keep token/ID examples, tokenizer comparison, explanatory flow and reproducible exercise trace. Reassess only if rendered inspection reveals a genuine gap. | [Second pilot](visual-audit-second-pilot-2026-11-26.md) |
| Embedding space | Keep ID → matrix row → vector → point figure; add EN/FR mobile variants. | [Third pilot](visual-audit-third-pilot-2026-11-26.md) |
| Positional encoding | Promote the three-mechanism comparison (absolute addition, RoPE on Q/K, relative score bias) into the main lesson; remove the partial duplicate stepper; add mobile variants. | [Second pilot](visual-audit-second-pilot-2026-11-26.md) |
| Contextualized representations | Keep same lookup/different context figure; add mobile variants. Remove the redundant collapsed text→IDs→lookup→position→Transformer embed while preserving the external reading link and source assets. | [Third pilot](visual-audit-third-pilot-2026-11-26.md) |
| Transformer | Keep architecture/block diagram and end-to-end GPT flow as distinct views; add EN/FR mobile variants. Make residual additions and architecture-dependent position handling explicit. | [Third pilot](visual-audit-third-pilot-2026-11-26.md) |
| Queries, Keys, Values | Keep the computational-path and S/A/O matrix figures; both already have responsive EN/FR variants. | [Fourth pilot](visual-audit-fourth-pilot-2026-11-26.md) |
| Scaled dot-product attention | Keep desktop computation diagram; add mobile layout with A and V as separate inputs to O=AV. | [Second pilot](visual-audit-second-pilot-2026-11-26.md) |
| Causal masking | Keep causal matrix; add French-localized desktop version and EN/FR mobile versions with query rows, key columns and j ≤ i semantics. | [Second pilot](visual-audit-second-pilot-2026-11-26.md) |
| Logits | Keep common-shift invariance figure; add EN/FR mobile versions. | [Fourth pilot](visual-audit-fourth-pilot-2026-11-26.md) |
| Probabilities | No new figure. Existing numerical table and ordered decoding flow already explain normalization and selection; a second chart would duplicate entropy. | [Fourth pilot](visual-audit-fourth-pilot-2026-11-26.md) |
| Entropy | Keep concentrated/example/uniform comparison; add EN/FR mobile versions. | [Fourth pilot](visual-audit-fourth-pilot-2026-11-26.md) |
| Generation | Keep existing responsive prefill/decode timeline. | [Fourth pilot](visual-audit-fourth-pilot-2026-11-26.md) |
| In-context learning | Keep Mermaid flow separating context/RAG at inference from fine-tuning parameter updates. No second static figure. | [Fourth pilot](visual-audit-fourth-pilot-2026-11-26.md) |
| Context engineering | Add a four-stage visual: available sources → selection/organization → supplied sequence → position-specific causal access. | [First pilot](visual-audit-priority-pages-2026-11-26.md) |
| Likelihood | Add observed-prefix scoring trace, conditional product and log-probability sum. | [First pilot](visual-audit-priority-pages-2026-11-26.md) |
| Cross-entropy | Keep one-hot target probability comparison; add mobile variants with common scales within each metric. | [Fourth pilot](visual-audit-fourth-pilot-2026-11-26.md) |
| Loss | Add separate causal-attention and target-loss masks, plus valid-position averaging. | [First pilot](visual-audit-priority-pages-2026-11-26.md) |
| Gradients | Add forward values, backward derivative flow and separate optimizer update. | [First pilot](visual-audit-priority-pages-2026-11-26.md) |
| Training loop | Keep responsive training-update/validation figure and optional optimizer comparison. | [Fourth pilot](visual-audit-fourth-pilot-2026-11-26.md) |

## Applied pull requests

- [PR #1733](https://github.com/JM-Brun/llm-lab/pull/1733) — likelihood, loss, gradients and context engineering figures.
- [PR #1734](https://github.com/JM-Brun/llm-lab/pull/1734) — positional, attention and causal-mask visual review.
- [PR #1736](https://github.com/JM-Brun/llm-lab/pull/1736) — embedding, contextualization and Transformer mobile compositions.
- [PR #1737](https://github.com/JM-Brun/llm-lab/pull/1737) — overview, logits, cross-entropy, entropy, and adjacent prediction/inference visuals.
- [PR #1730](https://github.com/JM-Brun/llm-lab/pull/1730) — original design/review process documentation.

The listed PRs are applied change sets; their current review and merge state must be checked on GitHub. PR #1737 remains open and unmerged. It is synchronized with `main` and currently mergeable at the branch level. Its pre-sync head passed CI, the full Quarto render and the automated browser review; the same workflows are rerunning after synchronization. This does not constitute complete manual desktop/mobile inspection, accessibility-tree review or rights clearance, and it does not close #1729.

## Remaining work — required before closure

### 1. Establish a real render

- Determine why Quarto/CI workflows are skipped for the current draft PRs and what supported trigger should be used.
- Run the project's normal Quarto build on the complete candidate change set.
- Resolve broken image paths, Markdown/HTML parsing, duplicated IDs, figure numbering and language-specific build errors.
- Check both language builds; do not infer EN correctness from FR or vice versa.

### 2. Inspect rendered pages

At minimum inspect desktop (1440 px), tablet (768 px) and narrow mobile (390 px) widths. For each page:

- confirm the intended desktop/mobile asset is selected;
- inspect text size, wrapping, cropping, clipping, aspect ratio, whitespace and caption placement;
- confirm no figure is separated from the prose that explains it;
- inspect the page as a whole, not only the SVG in isolation;
- inspect neighbouring pages to catch repeated diagrams, inconsistent examples or broken conceptual transitions.

Priority mobile checks:
- the six-stage overview and its feedback loop;
- positional three-mechanism comparison;
- context-engineering and attention flows;
- causal mask query/key axes;
- embedding lookup and contextualized-embedding branch comparison;
- Transformer stack and autoregressive data flow;
- logits, entropy and cross-entropy scales;
- optional FlashAttention figures, which have not all received mobile-specific compositions.

### 3. Inspect accessibility

- Inspect the rendered accessibility tree for every new or modified figure.
- Ensure page-level alt text, SVG `title`/`desc` and `figcaption` do not produce redundant announcements.
- Check reading order, contrast, font size, line breaks and whether essential distinctions are available in nearby text.
- Do not use alt text as a substitute for a caption or for explaining complex relationships in the lesson.

### 4. Resolve provenance and licensing

- Confirm owner provenance for each newly authored or adapted SVG.
- Record the asset-level licence explicitly under the existing #156/#163 policy.
- Keep external source attribution separate from claims of asset ownership.
- Decide whether the now-unembedded contextualization pipeline assets remain reusable references or should be marked retired; do not delete them without an asset-lifecycle decision.

### 5. Complete route-level coherence review

- Check consistent examples and notation across the full sequence.
- Check color semantics, arrow direction, axes, matrix orientation and the meaning of masks.
- Keep concept maps, computation diagrams, architecture diagrams and curriculum navigation visually distinct.
- Reassess “no new figure” decisions only when rendered inspection identifies a specific learner problem.
- Remove or revise any figure that is redundant, unreadable or scientifically misleading.

## Closure criteria for #1729

The issue can be closed only when:
1. the full EN/FR Quarto build succeeds;
2. all 20 core pages have rendered desktop/mobile inspection evidence;
3. accessibility review is complete for modified figures;
4. asset provenance/licensing is resolved;
5. the visual register matches the actual site;
6. remaining issues are either fixed or explicitly deferred with a reason.

Until then, the audit status remains **source-reviewed and partially render-validated; not fully route-validated**.
