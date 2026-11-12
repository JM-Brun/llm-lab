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

## Validation still required

- Quarto build and existing EN/FR Chromium page checks.
- Inspect the generated SVGs at desktop and mobile sizes for label clipping, arrow routing and footer wrapping.
- Confirm localized image alternatives are emitted by the rendered pages.
- Keep manual screen-reader/accessibility-tree review separate from source metadata and automated checks.
