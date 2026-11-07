# Source review — Jay Joshi, Transformer mathematics Part 2 (attention)

**Review date:** 2026-11-07  
**Source:** [The Mathematics of a Transformer Explained With Numbers You Can Check by Hand With Geometric Intutions Using Pytorch. Part-2: Attention Mechanism](https://medium.com/@jayjj6272/the-mathematics-of-a-transformer-explained-with-numbers-you-can-check-by-hand-with-geometric-3c6abb1181ec)  
**Author:** Jay Joshi  
**Publication metadata:** Medium indexed the article as October 2026; the search snapshot described it as a five-minute read and showed “7 hours ago”. The exact publication date was not independently established.  
**Retrieval:** Indexed Medium search snapshot. Direct retrieval of the canonical Medium URL returned a cache miss.

## 1. Scope actually inspected

The indexed snapshot exposed the full article text:

1. Introduction: a position-encoded input tensor with shape `[1, 3, 3]`.
2. Stage 1: three learned, bias-free linear layers `W_q`, `W_k`, `W_v`.
3. Stage 2: query-key dot products, division by `sqrt(d_k)`, row-wise softmax and a described 3×3 attention matrix.
4. Stage 3: weighted aggregation of value vectors, described as a convex combination.
5. Stage 4: output projection `W_o` and its relation to the residual stream and multi-head attention.
6. A preview of the next article: residual connections, LayerNorm, feed-forward networks, backpropagation and masked attention.

The four panels and PyTorch code are described but were not retrieved as inspectable image/code assets. No numerical Q/K/V matrices, softmax matrix values, W_o parameters or executable cells were exposed in the available snapshot. Therefore the article's promised hand-checkability and the visual accuracy of its figures remain unverified.

The preview of later topics is not evidence that this Part 2 teaches those topics. They are not extracted as taught content.

## 2. Source-local teaching model

The article uses a compact four-stage narrative:

`position-encoded X → Q,K,V → scaled QKᵀ scores → softmax weights → weighted V context → W_o output`

Its distinguishing approach is a geometric rendering of the same small 3D example across the four stages. This source-local route is not the canonical LLM Lab computational spine or learning route.

## 3. Mathematical review

### 3.1 Q/K/V projections

The article correctly describes three separately learned projections from a common input. Its statement that a linear map “rotates and stretches” a vector into a new subspace is an intuition, not a general property: a learned linear map may rotate, scale, shear, project or combine dimensions. The current Q/K/V lesson already explains the three projections, their dimensions and their distinct functions.

### 3.2 Dot-product geometry

For nonzero vectors,

[
q^	op k=lVert qVert,lVert kVertcos(	heta).
]

The sign is determined by whether the angle is acute, right or obtuse, but the magnitude depends on both norms as well as the angle. A zero dot product establishes orthogonality in the chosen projected space, not semantic unrelatedness. A negative score does not produce a negative attention weight: softmax weights are positive (for finite logits) and sum to one. A negative logit lowers relative weight; it does not hard-mask the position.

The current Q/K/V lesson already makes the norm-versus-angle distinction explicit, and the scaled-attention lesson distinguishes scores from normalized weights.

### 3.3 Scaling and softmax

The sequence (QK^	op/sqrt{d_k}), followed by row-wise softmax over accessible keys, is standard. The article's claim that increasing dimension pushes softmax into vanishing-gradient regions is too categorical as stated. The familiar variance argument assumes conditions on component distributions and explains why unscaled dot products tend to grow in scale; it does not mean every high-dimensional attention row necessarily saturates or that gradients universally vanish. The dedicated LLM Lab scaling page already gives the derivation and simulation.

### 3.4 Value aggregation: convex hull, not generally a cone

For a query row (i), if at least one key is accessible, softmax yields (alpha_{ij}geq0) and (sum_jalpha_{ij}=1). Thus

[
o_i=sum_jalpha_{ij}v_j
]

is a **convex combination** of the accessible value vectors and belongs to their **convex hull**.

The article correctly recognizes the convex-combination property but calls the containing set a “convex cone” or “wedge”. These are not interchangeable: a convex cone permits arbitrary nonnegative scaling, whereas a convex hull consists of convex combinations whose coefficients sum to one. The article's “dead-center inside the triangle” intuition for equal weights is useful for three value vectors, but the general statement should use convex hull.

This is already stated precisely in the current bilingual scaled-attention lessons, including the important boundary that the subsequent output projection and residual addition need not preserve membership in that hull. No page edit is justified.

### 3.5 Output projection (W_o)

In standard multi-head attention, per-head outputs are concatenated and passed through a learned output projection to the model dimension. This projection can mix information across head-coordinate blocks and makes the sublayer output dimension compatible with the residual stream.

However, describing (W_o) as “rotating back” into the residual coordinate system is too strong. A general learned matrix is not necessarily orthogonal, invertible, or the inverse of (W_v). It is a learned linear projection/mixing map. The article's small single-head 3D example cannot demonstrate cross-head mixing; that explanation applies to the multi-head construction.

The current architecture material already situates the output projection in the block. Do not import the rotation-back metaphor.

## 4. Comparison with the canonical project

| Source contribution | Existing destination | Decision |
|---|---|---|
| Three learned Q/K/V projections from one input | FR/EN Q/K/V lessons | Already covered |
| Dot-product angle interpretation | FR/EN Q/K/V lessons | Already covered; retain norm caveat |
| Scaling and row-wise softmax | FR/EN scaled-attention and score-scaling lessons | Already covered; do not import unqualified gradient claim |
| Convex weighted sum of values | FR/EN scaled-attention lessons | Already covered with exact convex-hull terminology |
| Output projection (W_o) | Transformer architecture / multi-head treatment | Already covered; retain learned-projection terminology |
| Four-panel 3D visualization and PyTorch code | Q/K/V and scaled-attention lessons as possible external reference | Defer: assets/code not inspectable; rights unknown |
| Residuals, LayerNorm, FFN, backpropagation, masked attention | Existing dedicated concepts and later series material | Not taught in this article; do not extract as content |

No new concept ID, page, computational operation, route stage, knowledge-graph relation or navigation node is warranted. The source's local sequence is preserved in its extraction record without turning it into another canonical route.

## 5. Source metadata and rights

- Primary theme: `architectures-mechanisms`
- Secondary theme: `mathematical-tools-geometry`
- Existing concepts: query, key, value, self-attention, attention-score, attention-weight, scaled-dot-product-attention, softmax, multi-head-attention
- Tags: `topic:qkv`, `topic:self-attention`, `topic:attention-score`, `topic:scaled-dot-product-attention`, `topic:attention-output`, `topic:multi-head-attention`, `method:dot-product`, `method:convex-combination`, `modality:visualization`, `ecosystem:pytorch`
- Scan status: partially scanned
- Integration status: reviewed
- Text/figures: link-only; code/data: unknown
- No licence or reuse permission established.

## 6. Decision

**Retain as a reviewed complementary source; do not modify published lessons in this pass.**

The main mechanisms and mathematical insights are already present in the project, often more precisely. The only potentially differentiating contribution is the continuous four-panel geometric visualization, but it cannot be judged without the actual figures and code. Revisit that item if the notebook or visual assets become directly accessible. Until then, preserve the source link and extraction evidence without adding visual clutter or duplicating existing explanations.
