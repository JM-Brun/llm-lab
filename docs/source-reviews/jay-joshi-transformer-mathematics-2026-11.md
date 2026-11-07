# Source review — Jay Joshi: hand-checkable Transformer mathematics, Part 1

**Source:** [The Mathematics of a Transformer Explained With Numbers You Can Check by Hand With Geometric Intuitions Using PyTorch — Part 1: Positional Encoding and Embedding Formation](https://medium.com/@jayjj6272/the-mathematics-of-a-transformer-explained-with-numbers-you-can-check-by-hand-with-geometric-96b5873c95be)  
**Author:** Jay Joshi  
**Inspected:** 2026-11-07  
**Status:** partial source scan; editorial comparison completed against current canonical pages and architecture records.

## 1. Access and evidence boundary

Direct Medium retrieval returned a cache miss. This review uses the indexed article snapshot, which exposes the title, introductory framing, stated outcomes, notation, embedding lookup equation, sinusoidal positional-encoding equations, paired sine/cosine geometric explanation, and descriptions of two PyTorch/Matplotlib code cells.

The snapshot does **not** expose complete code cells, numerical outputs, image bytes, figure captions, or exact visual composition. No code was executed and no figure was visually audited. The publication date is not asserted. Licence and reuse rights are unknown. This is a partial scan, not an exhaustive inspection of the live article.

A related Part 2, [Attention Mechanism](https://medium.com/@jayjj6272/the-mathematics-of-a-transformer-explained-with-numbers-you-can-check-by-hand-with-geometric-3c6abb1181ec), was discovered in search. It is a separate source and is not included in this Part 1 extraction.

## 2. What the source actually contributes

The article aims to bridge a hand-checkable mathematical example and a small PyTorch implementation. Its visible Part 1 content covers:

1. **Notation and tensor convention:** sequence length n, model width d, head/key width d_k, X in R^(n x d), with row vectors and right multiplication xW.
2. **Embedding lookup:** E in R^(V x d), with the initial representation expressed as X0 = E[token_ids] + P.
3. **Why position is needed:** content-only self-attention is permutation equivariant: permuting input rows permutes output rows correspondingly, so it does not independently encode sequence order.
4. **Sinusoidal position encoding:** alternating sine and cosine coordinates with dimension-dependent frequencies.
5. **Geometric interpretation:** each sine/cosine pair lies on a circle; a fixed positional offset corresponds to a fixed rotation for that frequency pair.
6. **Implementation-oriented visualisation:** two described cells using PyTorch and Matplotlib to inspect embedding vectors and positional encodings.

The article's broader promised outcomes include attention, scaling, causal masking, residual connections, LayerNorm, gradients and finite differences. Those topics are not developed in the inspected Part 1 text and must not be recorded as if this part taught them.

## 3. Mathematical review and qualifications

### Embedding geometry

The lookup equation and matrix shape are standard. The statement that training moves vectors for similarly used tokens toward similar directions is an oversimplification: geometry depends on the model, objective, parameterization, context and task. It should not be adopted as a general theorem about Transformer embeddings.

### Permutation equivariance

For ordinary self-attention without position-dependent signals or order-dependent constraints, jointly permuting token rows permutes the outputs correspondingly. This is the relevant symmetry argument for motivating positional information. The claim needs its assumptions; causal masking is an additional structural signal and is not interchangeable with positional encoding.

### Sinusoidal encoding and relative offsets

For one coordinate pair with angular frequency omega_i, write p_i(t) = [sin(omega_i t), cos(omega_i t)]^T. For fixed offset k, angle-addition identities give:

p_i(t+k) = [[cos(omega_i k), sin(omega_i k)], [-sin(omega_i k), cos(omega_i k)]] p_i(t).

The exact matrix sign convention depends on whether the pair is ordered as (sin, cos) or (cos, sin); the invariant is a fixed 2D rotation for each frequency and offset.

This algebraic property makes relative offsets linearly accessible in each pair. It does **not** prove that a trained attention head learns a rule such as “attend three tokens back”. That is an architectural possibility or motivation, not a guaranteed learned behavior.

Sinusoidal input encoding must also remain distinct from RoPE. Both use trigonometric/rotational structure, but standard sinusoidal encodings are added to input representations, whereas RoPE rotates projected queries and keys before their dot products.

### Visualisation

A 3D projection of a few vectors is a teaching aid, not evidence about full high-dimensional geometry. The exact visual output is unavailable, so no claim is made about its quality or correctness.

## 4. Comparison with LLM Lab

| Existing destination | Existing coverage | Incremental value | Decision |
|---|---|---|---|
| French/English embedding-space pages | ID-to-row lookup, matrix dimensions, numerical lookup example, initial vs contextualized representations, geometry caveats | Explicit row-vector convention and geometry-first framing | Already covered; do not duplicate |
| French/English positional-encoding pages | Why order is needed; absolute, relative and rotary mechanisms; insertion points; distinction from causal masking | More concrete sinusoidal formula and paired-coordinate geometric explanation | Candidate for one optional worked example after checking numerical details |
| French/English RoPE pages | Advanced rotary geometry and implementation | Potential conceptual precursor, but overlap in rotation derivation | Defer until line-by-line comparison; do not conflate sinusoidal encodings and RoPE |
| French/English tensor pages | Tensor shapes, axes and implementation invariants | Row-vector convention could be cross-linked if an actual ambiguity is found | No change justified from current evidence |

The current embedding lesson already contains a small numerical lookup example, so the article does not justify another embedding page or a second lookup example. The positional-encoding lesson is deliberately concise and may benefit from one worked sinusoidal pair, but the missing source code and figures mean the exact example must be independently constructed and verified before integration.

## 5. Source-local pedagogical model

The extraction file reconstructs a **partial source graph** and a four-step source teaching route:

- notation and small tensor convention;
- token IDs to embedding lookup;
- sinusoidal positional encoding and paired-frequency geometry;
- PyTorch/Matplotlib visual inspection.

The graph uses source-local IDs prefixed with src- and remains separate from the canonical concept graph, computational graph, guided route and Build path. It does not establish new pedagogical prerequisites.

## 6. Metadata decision

- **Primary theme:** architectures-mechanisms
- **Secondary theme:** mathematical-tools-geometry
- **Tags:** topic:token-embeddings, topic:positional-encoding, method:sinusoidal-encoding, modality:visualization, ecosystem:pytorch
- **Concept IDs:** token-embedding, positional-encoding
- **Technical level:** introductory
- **Contribution types:** mathematical derivation, visualization, pedagogy, implementation
- **Audience:** beginner, learner, practitioner
- **Importance:** no new concept importance field is justified; both concepts already have canonical importance assignments. Source metadata uses existing typed fields, not a generic meta-tag.

## 7. Integration decision

**Keep as a complementary source; do not create a page or new concept.**

1. Retain the bilingual embedding lesson unchanged for now: its lookup equation and numeric row-selection example already cover the source's core contribution.
2. Consider a compact optional worked example in the existing positional-encoding lesson, built from the canonical sinusoidal formula and independently checked. It should show one or two frequency pairs, distinguish absolute position from relative offset, and state assumptions.
3. Compare that candidate against the existing RoPE deep dive before deciding placement.
4. Do not reuse the article's figures or code until their contents are inspectable and reuse terms are established. A link and attribution are appropriate; a public URL is not a licence.
5. Treat Part 2 as a separate ingestion candidate. Its geometric claims need their own extraction and verification before integration.

## 8. Follow-up validation

- Retrieve the full article and inspect the actual code cells, figure content and numeric outputs if access becomes available.
- Recompute a small sinusoidal encoding example independently and test the fixed-offset rotation identity numerically.
- Compare the proposed explanation with the existing French and English RoPE pages to prevent conceptual duplication.
- If Part 2 is ingested, explicitly check dot-product/softmax interpretation, convex hull versus convex cone, and the role of the output projection in multi-head attention.
