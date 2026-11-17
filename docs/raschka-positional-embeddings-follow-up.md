# Positional embeddings follow-up: execution and validation plan

**Status:** follow-up plan after PR [#1152](https://github.com/JM-Brun/llm-lab/pull/1152) was merged on 17 November 2026.  
**Scope:** validate the Qwen3 implementation path, test RoPE position handling during cached decoding, and complete focused accessibility checks for the eight bilingual positional-encoding experiences.  
**Non-goals:** add another positional-encoding introduction, reproduce the source article's figures, claim model-level generalization from toy interactions, or redesign the existing explorers.

This plan separates three kinds of evidence: (1) source/code execution, (2) mathematical and behavioral tests, and (3) rendered user-interface accessibility. A successful Quarto render is not evidence that each control works; a passing toy test is not evidence that a production model behaves identically.

## 1. Current baseline

PR #1152 integrated the Raschka positional-embedding review and original bilingual experiences into the existing French and English RoPE lessons:

1. Position entry-point map.
2. RoPE pair explorer.
3. Q/K/V attention pipeline.
4. Interleaved versus split-half pairing explorer.
5. RoPE frequency explorer.
6. Partial-RoPE memory ledger.
7. NoPE causal-prefix experiment.
8. Hybrid RoPE/NoPE layer strip.
9. Relative-bias score decomposition.

The implementation and the full Quarto/browser workflow passed on the PR head. The workflow reviewed full-site rendering, learning-map controls, graph export, history-timeline parity, local links, and rendered bilingual learning-page/navigation output. It did **not** constitute exhaustive manual keyboard or screen-reader testing of every custom interactive control.

The Qwen3 notebook was inspected statically, not executed. In particular, cached incremental decoding and explicit position-ID behavior remain unverified.

## 2. Work packages and priority

### P0 — Execute and validate the Qwen3 RoPE reference notebook

**Question:** does the inspected reference implementation execute in a reproducible environment, and do its numerical outputs agree with the documented tensor conventions?

**Tasks**
- Identify the exact notebook path, upstream repository revision, model/config revision, and relevant cells; pin immutable revisions rather than relying on a moving default branch.
- Record Python, PyTorch, CUDA (if used), device, package versions, dtype, and whether execution is CPU-only or accelerator-backed.
- Execute the smallest self-contained RoPE path first. Avoid downloading full model weights if the RoPE utility and configuration can be exercised independently.
- Check actual tensor shapes and pairing convention (split-half or interleaved), frequency base, rotary dimension, and whether Q/K normalization occurs before rotation.
- Verify that Q and K are rotated and V is not; verify cosine/sine table shapes, dtype, device, broadcasting and position indexing.
- Compare a small deterministic input against an independent, simple reference calculation in float64 or another clearly specified high-precision mode.
- Capture the exact command, environment lock/requirements, output, and any skipped cells. If full notebook execution requires unavailable weights or hardware, record that as a bounded limitation rather than silently treating partial execution as complete.

**Acceptance criteria**
- A clean, documented command executes the selected self-contained cells.
- The tested tensor shapes, rotary dimensions, pairing convention and operation order are asserted.
- Reference and notebook outputs agree within a documented dtype-specific tolerance.
- The test explicitly establishes that V is unchanged by the RoPE operation.
- Any unavailable full-model path is listed with the exact blocker and is not described as validated.

**Deliverable:** a small reproducible test or notebook-validation script plus a concise execution report linked from the source review. Do not vendor third-party notebook code without checking its licence; prefer a minimal independent test.

### P0 — Test explicit position IDs and incremental KV-cache decoding

**Question:** does the implementation use the correct absolute positions when processing a prompt and then appending tokens one at a time with a KV cache?

**Tasks**
- Build a tiny deterministic fixture with fixed Q/K tensors and a small rotary dimension; no pretrained weights are required for the mathematical unit tests.
- Test prefill positions for a sequence of length T, then decode positions T, T+1, … one token at a time.
- Compare the rotated Q/K values for each token between (a) full-sequence computation and (b) cached incremental computation using the same absolute position IDs.
- Test non-zero position offsets, explicit position-ID tensors, batch dimensions, and any supported padding/position convention.
- Verify cache growth and alignment: each appended key/value is stored once, at the intended sequence index; previously cached entries are not rotated a second time.
- Test a deliberately wrong reset-to-zero position-ID path and ensure the test detects the mismatch.
- Where practical, compare attention outputs from full causal prefill and incremental cached decoding on the same deterministic inputs. Explain any differences due to implementation details or floating-point order.
- Keep this test separate from the toy NoPE prefix experiment: this is an implementation correctness check, not evidence that causal visibility alone guarantees length generalization.

**Acceptance criteria**
- Full-sequence and incremental paths agree for each token within documented tolerances when supplied equivalent absolute positions.
- A non-zero starting offset is handled correctly.
- A reset-position or double-rotation regression is caught by a negative test.
- Cache length, indices, and K/V contents are asserted before and after each append.
- The test states whether it covers a local reference implementation, the inspected Qwen3 code, or both. Do not generalize beyond the tested path.

**Deliverable:** focused unit tests and a short explanation in the RoPE implementation/reference notes. If no executable cache path exists in the repository, first isolate the minimal adapter or add a narrowly scoped reference fixture; do not introduce a full model implementation just to close this check.

### P1 — Keyboard and screen-reader review of the bilingual interactive experiences

**Question:** can a learner operate and understand each experience without a pointer, and are control names, values, updates and visual outputs conveyed accessibly?

**Inventory to review**
- RoPE pair explorer.
- QK attention pipeline.
- Pair-layout explorer.
- Frequency explorer.
- Partial-RoPE memory ledger.
- NoPE causal-prefix experiment.
- Hybrid RoPE/NoPE layer strip.
- Relative-bias score decomposition.

The static position-entry-point SVG is included in the visual/alternative-text review, but is not counted as a custom interactive control.

**Test matrix**
- French and English versions.
- Keyboard-only: Tab/Shift+Tab order, visible focus, native range/checkbox/select behavior, activation, and no keyboard trap.
- Screen reader: meaningful accessible names, instructions, current values and units; state changes are announced when needed without excessively chatty output.
- Zoom/reflow: 200% zoom and narrow viewport; no clipped controls, hidden outputs, or forced horizontal scrolling for ordinary content.
- Reduced motion: no essential information depends on animation; honor the user's reduced-motion preference wherever motion is present.
- Static fallback: explanatory text and a meaningful static state remain available if JavaScript is disabled or fails.
- Color and graphics: meaning is not conveyed by color alone; SVGs have an appropriate accessible name or adjacent text equivalent.
- Error/edge states: minimum/maximum slider values, empty or invalid states where applicable, and rapid repeated changes do not leave stale or contradictory output.

**Acceptance criteria**
- Each experience has a recorded result for FR and EN, keyboard and screen-reader review, and desktop/narrow viewport.
- Every control has a programmatic label and, where needed, associated help text and units.
- Dynamic output updates are discoverable to assistive technology without announcing an entire visualization on every keystroke.
- Focus is visible and logical; no keyboard trap exists.
- Essential conclusions remain understandable without color, animation, or JavaScript.
- Defects are fixed only when reproducible; unresolved limitations are documented.
- Do not claim WCAG conformance from a small manual sample. Record browser, operating system, screen reader/version, viewport, date and tested interaction.

**Suggested bounded lots**
1. Pair explorer + QK pipeline (FR/EN).
2. Pair-layout + frequency explorer (FR/EN).
3. Memory ledger + NoPE experiment (FR/EN).
4. Hybrid layer strip + relative-bias decomposition (FR/EN).
5. Consolidate findings, fix verified defects, and rerun CI.

Each lot should be timeboxed to one focused review session. If the screen-reader review cannot be completed in that window, record the exact remaining cases rather than implying completion.

### P2 — Pixel-level audit of the source article's 38 figures (conditional)

The current review inspected all 38 figure captions and their surrounding explanations, not the original image files at pixel level. A deeper audit is conditional on legitimate access to the original assets.

**Tasks if assets become available**
- Confirm lawful access and reuse restrictions; do not commit or republish source figures without permission.
- Record figure number, actual visual content, labels, axes, notation, source credit and relation to surrounding prose.
- Compare each figure with the recorded instructional-role assessment; correct any caption/context inference that the image contradicts.
- Prioritize figures that carry mathematical content or implementation details (especially the Q/K geometry, attention scores, pairing layout, cache/memory and relative-bias figures).
- Keep the original figure audit distinct from LLM Lab's independently authored diagrams.

**Acceptance criteria**
- The audit records which original files were actually inspected and which remained inaccessible.
- Any correction to the review is evidence-linked.
- No image is copied into LLM Lab without explicit reuse permission.

If access is not available, retain the current transparent limitation; do not spend time trying to bypass access controls.

## 3. Recommended execution order and dependencies

| Order | Work package | Dependency | Exit evidence |
|---:|---|---|---|
| 1 | Qwen3 notebook execution | Identify pinned notebook/revision and minimal dependencies | Reproducible execution report and numerical comparison |
| 2 | Position IDs + incremental KV cache | Small deterministic fixture; Qwen3 path if executable | Full-vs-incremental tests, offset and negative regression tests |
| 3 | Accessibility lots 1–4 | Rendered current main branch | FR/EN manual test matrix and reproducible defect records |
| 4 | Fixes and final validation | Findings from 1–3 | Python CI, Quarto render/browser workflow, focused retest |
| 5 | Figure pixel audit (conditional) | Lawful access to original assets | Figure-by-figure visual audit or explicit continued limitation |

Do not block the numerical work on access to the source article's image gallery. Do not treat successful numerical tests as a substitute for the accessibility work.

## 4. Reporting template

For each test or review, record:

- **Question / claim under test:**
- **Scope:** exact file, function, page, component and language.
- **Environment:** commit, OS, browser/runtime, versions, device and dtype as relevant.
- **Method:** commands, steps, inputs, seed and comparison baseline.
- **Observed result:** measured output or reproducible observation.
- **Expected result:**
- **Conclusion:** pass, fail, partial, blocked or not tested.
- **Limitations:** what this result does not establish.
- **Follow-up:** issue/PR and owner, if applicable.

Keep four statuses separate: implemented, automated-test passed, manually reviewed, and independently evidenced. A component must not be marked accessible merely because it renders, and a reference notebook must not be marked executed merely because its source was inspected.

## 5. Overall definition of done

This follow-up is complete only when:
- the selected Qwen3 RoPE path has a reproducible execution record and independent numerical checks;
- explicit position IDs and cached incremental decoding have passing positive and negative tests for the declared scope;
- all eight interactive experiences have a recorded FR/EN keyboard and screen-reader review, with verified defects fixed or explicitly accepted as limitations;
- the full CI and rendered-site workflow pass on the final commit;
- the source review links to the evidence and preserves the pixel-level figure-audit limitation unless lawful access changes.

The pixel-level audit is **conditional**, not a blocker for closing the core implementation and accessibility follow-up.
