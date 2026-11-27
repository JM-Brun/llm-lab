# Visual audit pilot — tokenization, positional information and attention (2026-11-26)

**Scope:** EN/FR Understand lessons for text data/tokenization, positional encoding, scaled dot-product attention and causal masking. The optional FlashAttention visual sequence was also reviewed at source level.  
**Status:** source changes and source-level checks recorded; no Quarto build or browser rendering is claimed.

## Decisions

| Lesson | Existing visual support | Decision | Rationale |
|---|---|---|---|
| Text data / tokenization | Exact token/ID examples, a two-tokenizer comparison table, an explanatory three-step transformation, a route stepper, and a reproducible tokenizer/embedding trace on the exercise page | **Keep without a new figure** | A generic text → tokens → IDs → vectors diagram would repeat the page's stepper and table. The reproducible trace belongs in the exercise because it exposes exact tokenizer output and lookup. The remaining source-level gap is the absence of a rendered visual trace directly on the lesson, but adding one is not justified until browser review shows the tables and stepper are insufficient. |
| Positional encoding | A core two-branch stepper and a three-lane diagram comparing absolute addition, RoPE on Q/K and relative score bias; the detailed diagram was hidden in a collapsed callout | **Promote and consolidate** | The prose explicitly relies on the three-way comparison, but the most complete visual was hidden. The visible stepper omitted relative score bias and duplicated only part of the diagram. The three-lane diagram is now in the main reading flow; the less complete stepper and collapsed duplicate were removed. |
| Scaled dot-product attention | A desktop flow diagram showing Q/K → scores → optional mask → row-wise softmax → weights A, with V joining at O=AV; a five-step text/stepper and detailed optional step disclosures | **Retain and add a mobile composition** | The desktop diagram already teaches the correct split between score/weight formation and value aggregation. A second desktop diagram would be redundant. The original 1200 px wide composition would scale down too far on narrow screens, so a vertical mobile variant was added. It explicitly draws A and V as separate inputs converging on O=AV. |
| Causal masking | A four-position lower-triangular matrix, with rows = queries and columns = keys; source page also defines j ≤ i and distinguishes attention, padding, document-boundary and loss masks | **Retain, localize and add mobile variants** | The original SVG's visible labels were English-only despite its use on the French page. The FR page now uses a localized desktop asset; EN and FR pages select mobile matrices at narrow widths. Captions explicitly state row/column semantics, the j ≤ i rule and why the diagonal is allowed. |
| FlashAttention optional deepening | IO-aware tiling, online-softmax merge, and dense-versus-sparse comparison | **Retain as optional deepening** | The sequence already separates the hardware/IO optimization from the mathematical dense attention definition. The third visual is useful because the nearby prose and caption explicitly state that FlashAttention preserves dense exact attention (up to floating-point tolerance), whereas sparse attention changes the allowed connectivity. No extra figure is needed. |

## Changes made

### Positional encoding

- Moved the three-lane insertion-point diagram into the main lesson flow, immediately after the paragraph that defines its three compared mechanisms.
- Removed the collapsed callout that hid the diagram.
- Removed the adjacent two-branch stepper because it repeated only absolute addition and RoPE while omitting relative score biases.
- Added EN/FR mobile compositions that stack the three mechanism paths vertically.
- Kept the conceptual boundary explicit: absolute vs relative is the family distinction; RoPE is one relative mechanism; causal masking is a separate visibility constraint.
- The French desktop SVG description was localized.

### Scaled dot-product attention

- Retained the existing desktop diagram and caption.
- Added EN/FR mobile compositions.
- The mobile composition makes the computational dependency explicit: Q and K determine attention weights A; V is a separate input; both converge in O = AV.
- It retains the key distinction between raw scores, normalized weights over key positions, and the weighted value output.

### Causal masking

- Added a French-localized desktop SVG; the English page retains the existing English asset.
- Added EN/FR mobile variants with a larger matrix and explicit query-row/key-column labels.
- Replaced the bare image embeds with responsive `picture` elements and meaningful captions.
- The captions connect the diagonal to next-token target alignment: the input token at position i is visible, while the target is x_(i+1).

## New assets

- `positional-entry-points-en-mobile.svg`
- `positional-entry-points-fr-mobile.svg`
- `causal-attention-mask-fr.svg`
- `causal-attention-mask-mobile.svg`
- `causal-attention-mask-fr-mobile.svg`
- `attention-calculation-flow-en-mobile.svg`
- `attention-calculation-flow-fr-mobile.svg`

The seven SVGs were authored for this contribution. They contain SVG `title` and `desc` elements and no embedded external image. This contribution record does not replace the repository's owner provenance-confirmation rule and does not grant an asset-level licence. Both remain pending for these files unless explicitly confirmed under the existing policy.

## Source-level validation completed

- EN/FR page source and existing visual references inspected.
- Positional comparison moved to the core reading flow in both languages; redundant stepper/collapsed duplicate removed.
- All newly embedded files use paths present in the branch.
- EN/FR pages use matching language variants where available.
- Page-level alt text and captions state the diagram's learning point and relevant caveat.
- The attention mobile composition shows A and V as distinct inputs to the aggregation rather than a sequential pipeline.
- The causal-mask figure labels rows as queries and columns as keys.
- The tokenization no-new-figure decision is explicit, rather than an unexamined omission.

## Not yet validated

1. Run the normal Quarto site build and fix any source, HTML or asset-path failures.
2. Inspect all affected pages at desktop and narrow mobile widths. In particular, check text legibility inside SVGs, long French labels, crop/overflow, figure height and caption wrapping.
3. Inspect the accessibility tree to confirm that page-level alt text, SVG title/description and figure caption are not redundantly announced.
4. Verify the rendered page ordering after the positional figure move and confirm the diagram appears before the permutation example.
5. Check the three optional FlashAttention figures at mobile width; they were reviewed for conceptual correctness but not given mobile variants in this pilot.
6. Confirm owner provenance for the seven new SVGs and record the separate asset-level licence decision; do not infer licence from authorship or commit attribution.

## Remaining route-wide work

This pilot covers four lessons and one optional subsection only. It does not close issue #1729. Continue the route audit page-by-page, with a distinct decision for each existing visual: retain, revise, move, replace, remove, or leave the page without a new figure. Prioritize rendered inspection of the existing overview, embeddings, contextualized representations, Transformer, Q/K/V, logits, probabilities, entropy, generation, ICL, loss, gradients and training-loop figures. Also inspect cross-page visual grammar: token examples, notation, colour semantics, axis conventions, arrows and the boundary between conceptual maps, computation diagrams and architecture diagrams.
