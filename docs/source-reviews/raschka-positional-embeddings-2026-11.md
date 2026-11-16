# Source review — Sebastian Raschka, “Understanding Positional Embeddings in Modern LLMs”

**Source:** [Ahead of AI, 15 November 2026](https://magazine.sebastianraschka.com/p/understanding-positional-embeddings) · [structured extraction](../../data/extractions/sebastian-raschka-understanding-positional-embeddings-2026.yml)

**Inspection:** complete article body (sections 1–7), equations, code snippets, figure captions and conclusion inspected on 16 November 2026. The 38 figures were not individually downloaded or visually inspected. The linked standalone Qwen3 notebook was statically inspected (RoPE utility, GQA and model configuration), but not executed. No reuse rights were established; text, figures and code remain link-only.

## 1. Integration decision

The article's main value is not another introduction: bilingual core pages already explain positional encoding, and a dedicated advanced RoPE derivation already exists. Extend the existing bilingual RoPE deep dives; do not create another positional-encoding introduction or duplicate the current derivation.

## 2. Coverage crosswalk

| Article sections | Contribution | Existing coverage / integration |
|---|---|---|
| 1–2 | Why order matters; GPT-2 learned absolute vectors; original Transformer sinusoidal vectors | Already covered by positional-encoding and sinusoidal lessons |
| 3 | Pairwise rotations and relative-offset effect on Q/K scores | Core derivation already present in the RoPE deep dive |
| 4 | Geometrically spaced frequencies | Add frequency schedule and table generation |
| 5 | PyTorch, broadcasting, Q/K-only rotation and pairing conventions | Add implementation notes and tests; link to Qwen3 implementation |
| 6.1 | Partial RoPE | Add variant and memory caveat |
| 6.2 | NoPE and causal-mask-derived implicit order | Add distinction and limits |
| 6.3 | Learned relative-position bias | Compare with RoPE and T5-style bias |
| 6.4 | Architecture-gallery comparison | Treat as a dated snapshot, not a census |

## 3. Technical reconciliation

- **RoPE geometry:** the relative-offset identity is valid pair by pair for fixed unrotated Q/K components and a fixed frequency. The full attention score does not depend on distance alone; content-derived Q/K also matter. Standard RoPE rotates Q and K after projection, not V.
- **Frequencies:** for even head dimension d, the standard schedule is omega_i = b^(-2i/d), with angle m * omega_i at position m. Real configurations may use other bases or scaling variants.
- **Pairing:** interleaved pairs adjacent features; split-half pairs corresponding features from the two halves. They are equivalent only after a consistent feature permutation. Mixing conventions can silently change scores while preserving tensor shapes.
- **Partial RoPE:** fewer rotary dimensions narrow the precomputed cosine/sine tables; they do not reduce the dimensions of cached K/V tensors. MiniMax-M3's example and its savings are configuration- and dtype-specific.

A primary-source cross-check is Khan et al., [Fractional Rotation, Full Potential?](https://arxiv.org/abs/2603.11611), arXiv v2 (15 October 2026), accepted as an EMNLP 2026 short paper. Its experiments compare 0%, 1–4%, 10%, 25%, 50%, 75% and 100% RoPE in 1B/8B configurations, with FineWeb/FineWeb-Edu and sequence lengths from 1,024 to 8,192. Around 10% or more rotary dimensions generally reached convergence/final-loss bands close to full RoPE in those settings; very low fractions and NoPE showed higher loss or instability in some configurations. The paper reports up to 10× savings in the **precomputed RoPE sine/cosine cache**, not the KV cache (Appendix C).

This qualifies the article author's opinion that partial RoPE may not be worthwhile: practical value depends on context length, head dimension, precision and whether the RoPE table is a material memory bottleneck. The study does not establish a universal 10% rule or universal downstream-task equivalence.
- **NoPE:** omits explicit positional transformations in a layer but retains causal masking. Nested prefixes can carry implicit order, not explicit absolute coordinates or pairwise distances. Length-generalization results are task- and training-dependent.
- **Learned relative bias:** the article describes an Inkling bias added to scaled QK scores before softmax and conditioned on query hidden state and relative distance. Do not conflate this with T5's bucketed bias.
- **Trend claims:** the 2025/2026 counts come from the author's gallery snapshot, with small groups and multiple variants; this is not a representative census.

Useful tests: verify cosine/sine table shapes and broadcasting; compare pairing conventions after explicit permutation; check common-position-shift invariance for fixed Q/K; verify only Q/K are rotated; and test position IDs for prefill and incremental decoding with a KV cache.

## 4. Pedagogical and visual assessment

The article changes scale gradually: sentence order; input-vector addition; one 2D rotation; multiple feature pairs and frequencies; QK score geometry; tensor tables and broadcasting; then architecture comparisons.

High-value original LLM Lab diagrams:
1. Side-by-side pipeline showing where each method acts (input embedding, Q/K path, attention-score bias, or no explicit method).
2. Interleaved versus split-half feature-pair layout.
3. RoPE/NoPE layer strip with version caveats.
4. Memory diagram separating cosine/sine tables from the KV cache.

Do not copy figures without permission. Recreate original diagrams from the mathematics and cite the source, or link to the originals.

## 5. Integration performed

- Registered the source with bounded scan scope and explicit reuse restrictions.
- Added atomic extractions distinguishing established derivations from context-dependent architecture claims.
- Extended the existing bilingual RoPE pages with modern variants, frequency schedule, pairing conventions, PyTorch table construction and test ideas.
- Added the annotated bibliography entry.
- Linked both RoPE deep dives from the canonical positional-encoding concept.

No new concept IDs, introductory pages, copied figures or external code were added.

## 6. Remaining work

- Inspect the 38 figure assets individually and decide which original LLM Lab diagrams to create.
- Execute the statically inspected Qwen3 notebook and compare its numerical outputs; separately add tests for explicit position IDs and incremental KV-cache decoding, which are not covered by the inspected forward path.
- Validate bilingual Quarto rendering, source/extraction schemas, concept graph and navigation in CI.

## 7. Technical references

- [Su et al. (2021), RoFormer](https://arxiv.org/abs/2104.09864)
- [Vaswani et al. (2017), Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [The Impact of Positional Encoding on Length Generalization in Transformers](https://arxiv.org/abs/2305.19466)
- [Raschka, Qwen3 from scratch](https://github.com/rasbt/LLMs-from-scratch) — linked, not independently inspected.
