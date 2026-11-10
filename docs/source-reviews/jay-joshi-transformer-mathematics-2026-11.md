# Source review — Jay Joshi: hand-checkable Transformer mathematics, Part 1

**Source title (as indexed):** *The Mathematics of a Transformer Explained With Numbers You Can Check by Hand With Geometric Intutions Using Pytorch. Part-1 Positional Encoding and Embadding Formation.*  
**Author:** Jay Joshi  
**Source:** [Medium article](https://medium.com/@jayjj6272/the-mathematics-of-a-transformer-explained-with-numbers-you-can-check-by-hand-with-geometric-96b5873c95be)  
**Inspected:** 2026-11-07  
**Status:** partial source scan; selected knowledge integrated into the existing bilingual positional-encoding lesson.

## 1. Evidence boundary

The indexed Medium search result exposes the article body, title, author, a three-minute reading estimate and publication month (October 2026). Direct retrieval of the Medium page itself returns a cache miss. The scan is therefore grounded in the indexed body, not the live page DOM. The exact publication day is unavailable.

The indexed body exposes the introduction, stated learning outcomes, notation, row-vector convention, embedding lookup equation, permutation-equivariance statement, sinusoidal positional-encoding equations, paired sine/cosine geometric explanation, fixed-offset rotation claim, and descriptions of two PyTorch/Matplotlib code cells. It also contains multiple embedded-image placeholders.

The actual code cells, numerical outputs, figure bytes, captions, axes and visual composition were not available for independent execution or visual inspection. No figure is reused. No licence or permission for text, figures or code reuse was established. The source is retained as link-only reading material.

A related [Part 2 — Attention Mechanism](https://medium.com/@jayjj6272/the-mathematics-of-a-transformer-explained-with-numbers-you-can-check-by-hand-with-geometric-3c6abb1181ec) was also discoverable and inspected as a separate indexed result. It is a separate source record and is not silently included in this Part 1 extraction.

## 2. What Part 1 actually teaches

The inspected body contains five connected pieces:

1. **Notation and tensor convention.** It defines sequence length n, model width d, head/key width d_k, an input matrix X in R^(n x d), and explicitly uses row vectors with right-multiplied linear maps xW.
2. **Embedding lookup.** It describes E in R^(V x d) and writes the initial input as X0 = E[token_ids] + P. Token IDs index rows; P is the positional signal.
3. **Why order information is needed.** It states that content-only self-attention treats the input as a set: permuting input rows permutes output rows correspondingly.
4. **Sinusoidal position encoding.** It gives the alternating sine/cosine formula, interprets each coordinate pair as a point on a circle with its own frequency, and explains that a fixed positional offset corresponds to a fixed rotation for each pair.
5. **Implementation and visualization intent.** It describes one cell for visualizing random embedding vectors/tensors and another for comparing positional and non-positional representations with PyTorch and Matplotlib.

The introductory “what you will be able to do” list also promises hand-computed attention, scaling by sqrt(d_k), causal masking, residual connections, LayerNorm, gradients and finite differences. These are **series-level promises**, not topics developed in the inspected Part 1 body. They must not be extracted as if Part 1 explained those mechanisms.

## 3. Scientific verification and qualifications

### 3.1 Embedding lookup and embedding geometry

The lookup equation and dimensions are standard. The project already explains row selection with a concrete numerical matrix and distinguishes initial embeddings from contextualized representations. This part is therefore already covered.

The article's statement that training moves tokens used in similar ways toward similar directions is too broad as a general claim. Embedding geometry depends on the model, objective, parameterization, context and task. It should not be imported as a universal property.

### 3.2 Permutation equivariance of content-only self-attention

The source explicitly states the useful symmetry: shuffling the rows of X shuffles the output rows in the same way. This is **permutation equivariance**, not permutation invariance.

LLM Lab's optional mathematical note supplies an independent verification. Let P be a permutation matrix and consider ordinary content-only self-attention without a positional bias, positional encoding or order-dependent mask. If Q = XW_Q, K = XW_K and V = XW_V, then for input PX the projections become PQ, PK and PV. The score matrix is permuted as P(QK^T)P^T. Row-wise softmax preserves this permutation, so:

Attention(PX) = P Attention(X).

This property explains why content-only self-attention does not, by itself, distinguish absolute sequence positions. The assumptions matter: a fixed causal mask is order-dependent and changes the symmetry. A causal mask is a structural visibility constraint; it is not the same mechanism as an explicit positional encoding.

### 3.3 Sinusoidal encoding and relative offsets

The source gives the standard Transformer sinusoidal construction:

P(pos, 2i) = sin(pos / 10000^(2i/d))  
P(pos, 2i + 1) = cos(pos / 10000^(2i/d)).

For a coordinate pair with angular frequency omega_i, write:

p_i(t) = [sin(omega_i t), cos(omega_i t)]^T.

For a fixed offset k, angle-addition identities give:

p_i(t+k) =
[[cos(omega_i k), sin(omega_i k)],
 [-sin(omega_i k), cos(omega_i k)]] p_i(t).

The sign convention follows from ordering the pair as (sin, cos). The matrix is a fixed two-dimensional rotation for a given frequency and offset. LLM Lab's page includes a minimal d=2 numerical check: p_0(0) = [0,1]^T and p_0(1) = [sin(1),cos(1)]^T, approximately [0.8415,0.5403]^T.

The identity makes relative offsets accessible to a linear transformation on each pair. It does **not** prove that a trained attention head will learn a rule such as “attend three tokens back”. That wording in the source is a motivating possibility, not a guaranteed behavior.

### 3.4 Do not conflate sinusoidal encoding and RoPE

Both constructions use paired coordinates and rotation identities, but they are not the same operation:

- **Sinusoidal absolute encoding:** a position-dependent vector P is added to the token embeddings at the model input, before Transformer projections.
- **RoPE:** position-dependent rotations are applied to projected queries and keys after Q/K projection and before the attention score product.

The sinusoidal fixed-offset identity belongs in the existing general positional-encoding lesson. The Q/K rotation derivation belongs in the existing RoPE deep dive. No RoPE page modification is justified by Part 1.

### 3.5 Visualizations and code

The indexed article describes the purpose of two code cells and shows image placeholders, but the actual code, plots and outputs are not inspectable in the available evidence. We cannot assess axes, projection choices, scales, numerical correctness or whether the figures genuinely clarify high-dimensional geometry. A 3D projection of a few vectors is a pedagogical view, not evidence about the full high-dimensional representation space.

## 4. Correct destination within LLM Lab

| Extracted knowledge | Canonical destination | Decision |
|---|---|---|
| Token IDs index rows of E | fr/en/embedding-space | Already covered; no duplicate |
| Similarity of learned embedding vectors | fr/en/embedding-space | Keep the existing caveat; do not adopt the source's oversimplification |
| Content-only self-attention is permutation equivariant | fr/en/positional-encoding | Added as an optional note with assumptions |
| Sinusoidal formula and frequency-specific sine/cosine pairs | fr/en/positional-encoding | Added as an optional mathematical deepening |
| Fixed-offset rotation of a sinusoidal coordinate pair | fr/en/positional-encoding | Added beside the formula; explicitly distinguished from RoPE |
| Rotations of projected Q and K | fr/en/rope | Existing page remains canonical; no change |
| PyTorch/Matplotlib visualizations | No destination yet | Defer until actual figures/code are inspectable and reuse rights are known |
| Attention, scaling, masking, residuals, LayerNorm and gradients | Separate Part 2 / subsequent sources | Not imported from Part 1 |

The positional-encoding page remains a core conceptual lesson. The new derivations are in **collapsed optional callouts**, so the main route remains concise and the mathematical detail is available without turning the core page into an advanced implementation lesson.

## 5. Canonical architecture impact

No new concept, page, route stage, computational operation or graph registry is warranted.

- data/concepts.yml: reuse self-attention and positional-encoding; no new concept ID.
- data/computational-graph.yml: no new computational node. Permutation equivariance is a mathematical property, not an execution step. The existing graph already represents positional information and the embedding-to-initial-state path.
- data/guided-route.yml: no new stage. The existing “IDs to representations” stage already includes embedding space, positional encoding and contextualized representations.
- data/resources.yml: no new project resource is needed for an external source record.
- site/fr/positional-encoding.qmd and site/en/positional-encoding.qmd: add the two optional explanations and cite the external pedagogical source.
- site/fr/rope.qmd and site/en/rope.qmd: intentionally unchanged.

This preserves the distinction between the source-local pedagogical graph, the canonical concept graph, the computational graph, the learning route and site navigation.

## 6. Source metadata and integration state

- **Primary theme:** architectures-mechanisms
- **Secondary theme:** mathematical-tools-geometry
- **Concept IDs:** token-embedding, positional-encoding, self-attention
- **Tags:** topic:token-embeddings, topic:positional-encoding, topic:self-attention, method:sinusoidal-encoding, method:permutation-equivariance, modality:visualization, ecosystem:pytorch
- **Technical level:** introductory
- **Contribution types:** mathematical derivation, visualization, pedagogy, implementation
- **Scan status:** partially scanned
- **Integration status:** partially integrated

No generic importance/meta-tag is added. The concepts already have canonical importance values; source facets and concept importance remain separate.

## 7. Final integration decision

**Partially integrate the mathematical explanation; do not reproduce the source implementation or visuals.**

The two optional notes now live in the existing bilingual positional-encoding pages. Embedding lookup is marked already covered. The RoPE pages, concept graph, computational graph and guided route remain unchanged. The source record retains the partial-scan and reuse limitations.

## 8. Remaining checks

- Run the source-catalogue validator and bilingual Quarto render after the page and extraction updates.
- Review the rendered callouts on desktop/mobile and check mathematical rendering and language parity.
- Revisit the original code and figures only if the live article or its notebook becomes accessible.
- Ingest Part 2 as a separate source before deciding whether its Q/K/V geometry adds value to the existing attention lessons. In that review, verify the convex-combination claim carefully: a convex combination lies in the convex hull of the values, not generally in the entire cone spanned by them.
