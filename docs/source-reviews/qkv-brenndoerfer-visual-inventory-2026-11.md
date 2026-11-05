# Visual asset and teaching-move inventory — Brenndoerfer Q/K/V

**Source ID:** `mbrenndoerfer-qkv-attention-mechanism`  
**Source:** [Michael Brenndoerfer, *Query, Key, Value: The Foundation of Transformer Attention*](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism)  
**Accessed:** 2026-11-05  
**Status:** descriptive inventory; original asset bytes and reuse rights not verified.

## Scope and rights

The article exposes figure/visualization descriptions and rendered outputs in its interactive chapter. This inventory records the visual teaching moves visible in the page text; it does **not** claim that the original image files were downloaded, visually inspected, or licensed for reuse. Do not copy the original plots, screenshots, code outputs, or page layout. If LLM Lab needs these teaching moves, recreate them independently from documented data and code, with project-owned assets and accessible captions/alt text.

## Figure and visualization inventory

| ID | Visual described in source | Pedagogical question | Best use in LLM Lab | Decision |
|---|---|---|---|---|
| V1 | Empirical and theoretical dot-product variance versus $d_k$ | Why does the unscaled dot-product variance grow with dimension? | Optional figure in the existing attention-score-scaling deep dive, paired with assumptions and derivation | Existing derivation is canonical; consider a reproducible plot only if the current lesson lacks this comparison |
| V2 | Three softmax bar plots at increasing score scales | How can multiplying scores by a constant change softmax concentration while preserving ranking? | Small interactive/side-by-side probe in the scaling lesson | Useful visual design; do not add if the existing scaling workbench already demonstrates it |
| V3 | Unscaled versus scaled attention-weight bars | What does division by $\sqrt{d_k}$ change in the resulting distribution? | Controlled comparison with fixed Q/K and a stated seed | Candidate for a regression visual; recompute values rather than reproducing the source's prose claims |
| V4 | Two-dimensional scatter plots for query, key and value spaces | Why do the same input tokens have distinct role-specific representations? | Optional conceptual visual in the Q/K/V lesson | Recreate with explicitly synthetic points; label axes as illustrative, not semantic dimensions |
| V5 | Attention-weight heatmap for a four-token sequence | How does each query distribute weight across keys? | Existing attention lesson / workbench | Use only with a conspicuous random-initialization caveat; a random heatmap demonstrates tensor flow/normalization, not interpretability |
| V6 | Shape table across X, W_Q/W_K/W_V, Q/K/V, weights and output | How do dimensions propagate through the operation? | Tensor reference or existing Q/K/V dimension note | Already covered; do not duplicate |
| V7 | “The cat sat” intermediate Q/K/V vectors and score matrix | Can a learner follow every intermediate value? | Deterministic, reproducible worked-example alternative | Source inputs are hand-crafted and projections random; do not present outputs as learned semantics |
| V8 | Row-wise softmax weights with row sums | Why do attention-weight rows sum to one? | Existing scaled-attention exercise / invariant test | Already covered; retain as a validation invariant |
| V9 | Weighted value vectors and output mixtures | How do weights become contextualized output vectors? | Existing attention worked example | Already covered; source adds useful message-passing and convex-geometry interpretations |

## Additional conceptual teaching moves

### 1. Routing versus payload

A key participates in deciding whether a position receives attention; its value supplies the content contributed if selected. These roles need not encode the same feature. A hypothetical token could attract attention because its key signals a useful grammatical role while its value carries semantic content. This is a functional example, not evidence that a trained head implements that linguistic behavior.

**Integrated:** a short, source-attributed, collapsible note in both canonical Q/K/V pages. It preserves the important distinction without adding a second full explanation or another analogy.

### 2. Attention as message passing

Each position can be viewed as broadcasting its value vector; each query receives a weighted mixture of the accessible positions' values. This is a useful bridge to graph neural networks and message-passing language: positions act as nodes, values as messages, and attention weights as content-dependent routing weights. It is an analogy for the computation, not a claim that the Transformer uses a fixed graph.

**Integrated:** a collapsible note in both scaled-attention pages.

### 3. Convex-hull interpretation

For a fixed query row with at least one accessible key, softmax weights are nonnegative and sum to one. The weighted sum of the corresponding value vectors therefore lies in their convex hull. This is a precise geometric consequence. It applies to the pre-output-projection weighted sum; subsequent output projections, residual additions or other transformations need not remain in that convex hull. Fully masked rows are excluded.

**Integrated:** a bounded mathematical note in both scaled-attention pages, adjacent to the worked numerical example. This supersedes the initial deferral because the statement is now paired with a precise scope and a concrete geometric interpretation of the existing weighted-sum equation.

### 4. Linear projections are not the whole network's expressive limit

Each Q/K/V projection is linear, but this does not make the whole Transformer a linear function: attention uses input-dependent softmax weights and is composed with residual pathways, stacked layers and nonlinear feed-forward blocks. Preserve the distinction between a local linear map and the full architecture.

**Disposition:** retain as a source-review caveat; no extra paragraph is needed on the Q/K/V page.

### 5. Permutation symmetry needs qualification

Without positional information, masks or other position-dependent mechanisms, self-attention is permutation-equivariant: permuting input positions permutes outputs correspondingly. It is not accurate to say without qualification that attention treats all positions symmetrically once causal masks, positional embeddings, RoPE or cross-attention structure are present.

**Disposition:** retain as an advanced source-quality check; do not expand the core lesson.

## Integration decisions

- **Integrated into Q/K/V EN/FR:** routing versus payload, with an explicitly hypothetical linguistic example.
- **Integrated into scaled attention EN/FR:** message-passing interpretation and convex-hull property, with precise mathematical scope.
- **Reference only:** database analogy, progressive eleven-section teaching route and the source's worked example. The canonical page already has an index-card analogy and the project owns a deterministic implementation.
- **Visuals:** no original assets reused. Candidate recreations must be independently generated, reproducible, licensed by the project and accessible.
- **Do not promote to factual claims:** random-init heatmap patterns as linguistic evidence; guaranteed healthy gradients; literal database retrieval; claims that a specific head performs coreference or syntactic parsing.

## Validation checklist for any future visual recreation

- [ ] Store source URL, access date and the exact pedagogical question addressed.
- [ ] Recompute plot data from a deterministic script or notebook.
- [ ] Add a caption stating assumptions and whether values are synthetic, random-initialized or trained.
- [ ] Provide meaningful alt text and a textual equivalent for the key conclusion.
- [ ] Check mobile scaling, contrast, keyboard access if interactive and screen-reader behavior.
- [ ] Verify no source image/code has been copied without an explicit compatible licence.
- [ ] Confirm that the visual adds a learning outcome not already served by the existing workbench.
