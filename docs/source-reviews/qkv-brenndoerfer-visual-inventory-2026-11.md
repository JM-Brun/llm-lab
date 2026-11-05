# Visual asset and teaching-move inventory — Brenndoerfer Q/K/V

**Source:** [Michael Brenndoerfer, *Query, Key, Value: The Foundation of Transformer Attention*](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism)  
**Accessed:** 2026-11-05  
**Status:** descriptive inventory; original asset bytes and reuse rights not verified.

## Scope and rights

The article exposes figure/visualization descriptions and rendered outputs in its interactive chapter. This inventory records the visual teaching moves visible in the page text; it does **not** claim that the original image files were downloaded, visually inspected, or licensed for reuse. Do not copy the original plots, screenshots, code outputs, or page layout. If LLM Lab needs these teaching moves, recreate them independently from documented data and code, with project-owned assets and accessible captions/alt text.

## Figure and visualization inventory

| ID | Visual described in source | Pedagogical question | Best use in LLM Lab | Decision |
|---|---|---|---|---|
| V1 | Empirical and theoretical dot-product variance versus $d_k$ | Why does the unscaled dot-product variance grow with dimension? | Optional figure in the existing attention-score-scaling deep dive, paired with the assumptions and derivation | Recreate only if the existing page lacks an empirical/theoretical juxtaposition; otherwise link to the derivation |
| V2 | Three softmax bar plots at increasing score scales | How can multiplying scores by a constant change softmax concentration while preserving ranking? | Small interactive/side-by-side probe in the scaling lesson | Strong teaching move; do not add if current scaling workbench already demonstrates it |
| V3 | Unscaled versus scaled attention-weight bars | What does division by $\sqrt{d_k}$ change in the resulting distribution? | Controlled comparison with fixed Q/K and a stated seed | Candidate for a regression visual; verify values rather than reproducing the source's prose claims |
| V4 | Two-dimensional scatter plots for query, key and value spaces | Why do the same input tokens have distinct role-specific representations? | Optional conceptual visual in the Q/K/V lesson | Recreate with explicitly synthetic points; label axes as illustrative and do not imply semantic dimensions |
| V5 | Attention-weight heatmap for a four-token sequence | How does each query distribute weight across keys? | Existing attention lesson / workbench | Use only with a conspicuous random-initialization caveat; a random heatmap is a tensor-shape/normalization demonstration, not interpretability evidence |
| V6 | Shape table across X, W_Q/W_K/W_V, Q/K/V, weights and output | How do dimensions propagate through the operation? | Tensor reference or existing Q/K/V dimension note | Already covered; do not duplicate |
| V7 | “The cat sat” intermediate Q/K/V vectors and score matrix | Can a learner follow every intermediate value? | A deterministic, reproducible worked-example alternative | Source's inputs are hand-crafted and its projection matrices random; do not present outputs as learned semantics |
| V8 | Row-wise softmax weights with row sums | Why do attention-weight rows sum to one? | Existing scaled-attention exercise / invariant test | Already covered; retain as a validation invariant |
| V9 | Weighted value vectors and output mixtures | How do weights become contextualized output vectors? | Existing attention worked example | Already covered; source adds a useful message-passing interpretation |

## Additional conceptual teaching moves

### 1. Routing versus payload

The most useful extra explanation for the canonical Q/K/V lesson is the explicit distinction between **what makes a position receive attention** and **what content it contributes**. A key participates in routing; its value supplies payload. The two may encode different features. The bilingual Q/K/V lesson now has a short, source-attributed, collapsible note for this distinction.

### 2. Attention as message passing

The source describes self-attention as positions broadcasting values and receiving weighted mixtures of other positions' broadcasts. This is a useful bridge to graph neural networks and message-passing language. Keep it in the scaled-attention lesson or an advanced note: each position is a node, accessible positions are potential senders, attention weights are data-dependent edge weights, and values are messages. This is an analogy to the computation, not a claim that the Transformer is literally a fixed graph neural network.

### 3. Convex-hull interpretation

For a fixed query row, softmax weights are nonnegative and sum to one. Therefore the weighted sum of the corresponding value vectors lies in their convex hull. This is a precise geometric consequence, not just an intuition. It belongs with the weighted-sum equation in the scaled-attention lesson, not the Q/K/V role page. State the scope carefully: it applies to the pre-output-projection weighted sum for the set of values included in that row; subsequent output projections, residual additions, or other transformations need not remain in that convex hull.

### 4. Linear projections are not the whole network's expressive limit

The source notes that each Q/K/V projection is linear. Avoid the misleading inference that the whole Transformer is therefore limited to linear functions: attention combines learned linear projections with input-dependent softmax weights, residual pathways, stacked layers and nonlinear feed-forward blocks. This is a useful limitation/counter-limitation pair for the architecture overview.

### 5. Permutation symmetry needs qualification

Without positional information, masks, or other position-dependent mechanisms, self-attention is permutation-equivariant: permuting input positions permutes outputs correspondingly. It is not generally correct to say simply that attention “treats all positions symmetrically” once causal masks, positional embeddings, RoPE, or cross-attention structure are present. Keep this as a precise advanced caveat rather than a core Q/K/V addition.

## Integration decisions

- **Integrated into Q/K/V EN/FR:** routing versus payload (key controls compatibility/routing; value supplies transmitted content), with an explicit hypothetical-example caveat.
- **Reference only:** database analogy, progressive eleven-section teaching route, and the source's worked example. The canonical page already has an index-card analogy and the project already owns a deterministic implementation.
- **Potential integration into scaled attention:** convex-hull interpretation and message-passing lens. First compare against the current bilingual scaled-attention pages to avoid duplication.
- **Visuals:** no original assets reused. Candidate visual recreations must be independently generated, reproducible, licensed by the project, and accessible.
- **Do not integrate as factual claims:** random-init heatmap patterns as linguistic evidence; guaranteed healthy gradients; literal database retrieval; claims that a specific head performs coreference or syntactic parsing.

## Validation checklist for any future recreation

- [ ] Store source URL, access date, and the exact pedagogical question addressed.
- [ ] Recompute plot data from a deterministic script or notebook.
- [ ] Add a caption that states assumptions and whether values are synthetic, random-initialized, or trained.
- [ ] Provide meaningful alt text and a textual equivalent for the key conclusion.
- [ ] Check mobile scaling, contrast, keyboard access if interactive, and screen-reader behavior.
- [ ] Verify no source image/code has been copied without an explicit compatible licence.
- [ ] Confirm that the new visual adds a learning outcome not already served by the existing workbench.
