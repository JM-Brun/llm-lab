# Q/K/V visual comparison and bounded refinement — 2026-11-12

## Decision

Use Nishanthan K's illustration as a design benchmark, not as a reusable asset. The original image is linked from the canonical EN/FR Q/K/V lessons. Its figure-specific licence/permission remains unverified; do not embed, trace, crop, recolor or recreate it.

The project-owned SVGs remain the canonical diagrams. A small, independently authored refinement is justified: make the projection operations and the scale/softmax step visible while preserving the existing two-path mental model (Q/K determine weights; V supplies content).

## Feature comparison

| Feature | Previous project SVG | Nishanthan K reference | Refined project SVG |
|---|---|---|---|
| Shared input X | Yes | Yes | Yes |
| Three parallel Q/K/V branches | Yes | Yes | Yes |
| Learned projection equations | Not shown | Shown | Shown in each branch |
| Sequence/tensor shapes | Omitted | Simplified shapes shown | X, Q/K and V sequence-level shapes labelled |
| QKᵀ compatibility | Yes | Yes | Yes |
| Scaling and softmax | Softmax named; scaling delegated | Both shown | Scaling by √d_k and softmax named |
| Attention weights | Yes | Yes | Yes |
| Weighted aggregation of V | Yes | Yes | Yes |
| Full derivation | Deliberately delegated | Compact equation | Still delegated to scaled dot-product attention |
| Batch/head axes and causal mask | Omitted | Omitted | Explicitly declared omitted |

## What changed

- Added Q = XW_Q, K = XW_K and V = XW_V inside the three existing projection-role cards.
- Added sequence-level shapes: X is T × d_model; Q and K are T × d_k; V is T × d_v.
- Made the scale-by-√d_k step explicit before softmax.
- Updated the footer to show A = softmax(QKᵀ / √d_k) and output = AV.
- Clarified that the figure is a sequence-level, single-head view; batch and head axes are omitted.
- Updated both bilingual figure alternatives to describe the complete pipeline and its omissions.

## Scope boundary

This remains an orientation diagram, not a replacement for the dedicated scaled dot-product attention lesson or the advanced Q/K/V deep dive. The detailed derivation, masking variants, multi-head transformations, batch/head shapes, numerical examples and implementation contracts remain in their canonical destinations. The visual does not imply that attention weights are semantic explanations or that one head necessarily resolves coreference.

The source illustration remains link-only. The project SVG changes are independently authored and do not copy its layout or artwork.

## Validation evidence — 2026-11-12

The refinement was merged in [PR #1030](https://github.com/JM-Brun/llm-lab/pull/1030) at merge commit `af2d7ecc43ed9a6fdc4a59c63169a67ec2102886`.

The post-fix Quarto/browser workflow completed successfully on the merged PR head (`1a8a0c1a803f71ae4bfbd1d4c8bd00bda5c74c79`):

- Quarto full-site render succeeded; local-link checks and the generated learning-map, knowledge-graph and history-timeline checks also succeeded.
- Chromium reviewed all four Q/K/V route cases: EN/FR × desktop (1440 px) / mobile (390 px), light theme.
- All four routes returned HTTP 200, loaded the expected localized SVG, and emitted the expected localized image alternative. No console errors or uncaught page errors were reported.
- No document-level horizontal overflow was detected at either viewport. The SVG rendered at 810 px on desktop and 313 px on mobile.
- The page's previous/next links resolve to the Transformer lesson and the scaled-dot-product-attention lesson in both languages.
- Desktop Axe checks (one per language) reported zero violations, 31 passes and one incomplete item. Axe was intentionally skipped on mobile because the audit runs once per page/language on desktop/light.
- The desktop keyboard probe completed its tab cycle in both languages: 35 focus targets, all 35 visibly focused; the learning-outcome disclosure toggled with Enter. No mobile keyboard probe was run.

The CI workflow also completed successfully: source catalogue/extraction validation, page metadata and learning graph, bilingual concept registry, resource checks, formatting, lint, type checking and the full test suite all passed.

**Browser artifact:** [site-browser-review artifact from workflow run 43252332474](https://github.com/JM-Brun/llm-lab/actions/runs/43252332474/artifacts/13959757114). It contains EN/FR desktop and mobile screenshots plus `report.json`.

## Remaining evidence and boundaries

- The automated browser review is a PR-local render of the merged source, not proof that the public deployed pages have updated. Verify the deployed EN/FR pages separately.
- The mobile viewport has no horizontal overflow, but the SVG is scaled to 313 px; its fine internal labels are naturally less legible at that size. The surrounding lesson text and mathematical equations remain the readable explanation. A dedicated mobile composition could be considered separately if learner testing shows it is needed.
- Axe reports one incomplete item per desktop page; inspect the relevant incomplete rule before treating automated accessibility review as exhaustive.
- No manual screen-reader session or touch-device test was performed. The browser audit confirms the image alternative in the rendered DOM, not its announcement by assistive technology.
- The external DEV image remains link-only: figure-specific reuse permission is still unverified.



## Mobile-specific composition — 2026-11-12

A dedicated narrow-screen SVG was added in both languages rather than shrinking the desktop overview further. The mobile composition uses a vertical sequence with larger labels: shared input, the three learned projections, Q/K score computation and normalization, attention weights, V aggregation, and output. The orange dashed V path remains separate from the Q/K weighting path until aggregation, preserving the central conceptual distinction.

The bilingual lesson pages now use a responsive `picture` element: viewports up to 600 CSS pixels receive the mobile SVG; wider viewports retain the existing desktop SVG. Both variants have localized accessible image alternatives. The external DEV illustration remains link-only; the mobile artwork is independently authored and does not reproduce its composition.

Validation required: Quarto full render and local-link checks; Chromium checks at 390 px and desktop widths in EN/FR; verify the correct SVG is selected at each breakpoint, no overflow/clipping, legible text, and accessible alternative text. Manual screen-reader review remains separate.
