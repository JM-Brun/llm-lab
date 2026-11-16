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

## 4. Figure-by-figure pedagogical audit

**Inspection boundary:** the article's complete HTML text, figure captions, mathematical descriptions and surrounding explanations were reviewed on 16 November 2026. This is a caption-and-context audit of all 38 numbered figures, **not a pixel-level inspection of the original image files**. Subscriber-only bulk image exports and gallery metadata were not accessed. The classifications below describe instructional function inferred from captions and placement.

| Figure | Instructional role | Assessment | LLM Lab decision |
|---:|---|---|---|
| 1 | Preview of 2026 architecture families | Useful orientation, but time-sensitive and information-dense before foundations | Recreate only as a small, explicitly dated teaser; keep full comparison late |
| 2 | Locate token embeddings in GPT-2 and MiniMax-M3 | Strong architectural anchoring | Recreate as a two-lane "where position enters" diagram |
| 3 | Word-order contrast changes meaning | Excellent accessible motivation | Create a new minimal sentence-pair graphic |
| 4 | Token IDs versus positions | Essential distinction; word-level toy tokenizer can hide subword reality | Show token IDs and position indices separately; note subword tokenization |
| 5 | GPT-2 absolute-position insertion point | Strong placement diagram | Recreate and link to GPT-2 implementation lesson |
| 6 | Element-wise sum of token and position vectors | Excellent numerical micro-example | Recreate with step-by-step values |
| 7 | Sinusoidal encoding insertion point | Useful bridge to original Transformer | Recreate as compact encoder/decoder input diagram |
| 8 | Sine/cosine values assigned to feature pairs | Helpful coordinate-level bridge | Show paired feature indices |
| 9 | Position times angular frequency | Strong single-variable explanation | Recreate as a one-pair angle construction |
| 10 | All pair angles at one position | Useful progression from one pair to many | Merge with Figures 8–9 into a progressive frequency-bank visual |
| 11 | Sampling sine/cosine curves into a position vector | Strong signal-processing intuition | Recreate as a timeline sampled at multiple frequencies |
| 12 | Compare learned absolute and fixed sinusoidal encodings | High-value historical summary | Keep as concise comparison matrix |
| 13 | Equal offset induces equal rotation in sinusoidal pairs | Important bridge; must not imply whole-model translation invariance | Show fixed-offset animation labelled "position vectors only" |
| 14 | RoPE placement on Q/K inside attention | Essential contrast with input-level addition | Recreate as central RoPE insertion-point diagram; show V bypass |
| 15 | Hidden state to Q/K projections, heads and pair layout | Important tensor-shape bridge; dense for beginners | Reveal projection, reshape and pairing in stages |
| 16 | Pairwise rotations and QK score path | Central mechanism overview | Recreate as end-to-end computation flow |
| 17 | Close-up of one query feature pair | Useful focus cue | Merge into interactive pair explainer with Figure 18 |
| 18 | Rotate query/key pairs by position-dependent angles | Excellent geometric intuition | Vector diagram with independent positions and angle controls |
| 19 | QK dot product at different relative offsets | Critical link from geometry to attention | Show numerical pair contribution and distinguish it from full head score |
| 20 | Shared position shift preserves relative angle | Core RoPE property | Synchronized shift control with fixed-Q/K assumption |
| 21 | Attention-score matrix and causal mask | Essential sequence-level connection | Separate raw scores, causal mask and post-softmax weights |
| 22 | Prefix shift moves score-matrix cell but preserves value | Good long-prefix example | Merge with Figures 20–21; warn that real prefixes can change hidden states and Q/K |
| 23 | Compare shared shifts under sinusoidal, learned absolute and RoPE | Excellent synthesis, potentially overloaded | Keep after all three mechanisms |
| 24 | Apply all pair rotations to a full head | Useful scaling from 2D to d dimensions | Recreate as staged feature-pair animation |
| 25 | Block-diagonal rotation matrix | Mathematically valuable for advanced learners | Optional math view linked to Figure 24 |
| 26 | rope_params and rope_split_half pipeline | Strong code-to-math mapping | Code-linked tensor-flow diagram with shapes |
| 27 | Cosine/sine lookup tables | Essential implementation concept | Heatmap with position rows and pair-frequency columns |
| 28 | Split-half versus interleaved pairing | Important implementation correctness issue | Index maps plus permutation-equivalence test |
| 29 | Full versus partial RoPE dimensions | High-value modern variant | Show rotary/untouched channels and separate memory accounting |
| 30 | Causal visibility pattern | Clear foundational mask visual | Triangular matrix with query/key axes |
| 31 | Uniform-attention prefix averaging toy example for NoPE | Clever but easy to overgeneralize | Slider over prefix length; label as toy signal, not universal guarantee |
| 32 | SmolLM3 repeating RoPE/NoPE layer pattern | Useful hybrid example | Layer strip, dated and sourced |
| 33 | State- and distance-dependent relative bias before softmax | Important alternative mechanism | Score decomposition: scaled QK + learned bias → mask → softmax |
| 34 | Inkling architecture placement of learned bias | Useful but model-snapshot dependent | Keep as linkable example, separate from general mechanism |
| 35 | Architecture gallery distribution by positional family | Trend hypothesis, not stable population statistic | Dated evidence panel with denominator and inclusion rules |
| 36 | Partial versus full RoPE among RoPE-using models | Useful secondary trend | Merge with Figure 35 or details view; retain denominators |
| 37 | Individual 2026 architectures by position type | Reference poster, low value in core teaching path | Link to live gallery; avoid hard-coded static copy |
| 38 | GPT-2 XL baseline architecture | Strong orientation for the series | Reuse conceptual role as simplified original baseline map |

### 4.1 What the visual sequence does especially well

The strongest pedagogical move is progressive zoom: semantic word-order motivation → token/position distinction → where position enters the architecture → one 2D rotation → QK dot product → attention matrix → multi-frequency head → implementation tables → architecture variants. This is a sound sequence from intuition to mechanism to implementation and comparison.

The series alternates representational levels: sentence examples, architecture maps, vector geometry, matrices, tensor layouts, code-linked tables and model-layer strips. LLM Lab should preserve this variety while making transitions between levels explicit.

### 4.2 Gaps and editorial risks

1. **No explicit learning checkpoints.** Add prediction prompts before revealing each transformation.
2. **Invariance assumptions need persistent labels.** RoPE shared-shift invariance applies to the positional QK rotation for fixed pre-rotation Q/K. Adding a real prefix may alter hidden states and therefore Q/K.
3. **Absolute versus relative can be oversimplified.** Sinusoidal vectors are absolute position vectors with useful relative-shift structure; RoPE makes relative offsets explicit in QK interactions.
4. **NoPE's toy signal is not a theorem.** Uniform-attention averaging demonstrates one way causal prefixes can encode length; it does not prove every causal-only Transformer robustly infers all positions or generalizes arbitrarily.
5. **Architecture galleries are snapshots, not population statistics.** Charts must expose release-date bins, counted unit (gallery card), duplicates/variants, unknown classifications and sample sizes.
6. **Memory requires two separate ledgers.** RoPE cosine/sine table size and KV-cache size are different quantities. Partial RoPE changes the former, not the full-width cached K/V vectors.
7. **Pairing layouts need a correctness checkpoint.** Split-half and interleaved layouts are equivalent only under a consistent feature permutation and frequency assignment. Mixing conventions silently changes scores.
8. **There is a figure-number cross-reference inconsistency.** The paragraph introducing Q/K projection and head reshaping refers to "Figure 12", while the actual caption is Figure 15; Figure 12 is already the absolute-versus-sinusoidal comparison. Use stable diagram IDs and link checks rather than sequential numbering alone.

### 4.3 Original LLM Lab visual components to build

Priority order; all diagrams should be newly authored, not copied:

- **P0 — Position entry-point map (implemented):** original bilingual SVGs compare absolute addition, RoPE on Q/K and learned bias on attention scores.
- **P0 — RoPE pair explorer (implemented):** bilingual controls change query/key positions, pair frequency and shared shift; the vector plot and numerical pair contribution update live. Fixed pre-rotation Q/K are explicitly stated.
- **P0 — QK attention pipeline (implemented bilingually):** inspect Q/K/V projections, toggle Q/K RoPE, select a query position, toggle the causal mask, and observe scaled scores, allowed keys, softmax weights and the weighted V output. The numerical example is explicitly synthetic.
- **P0 — Pair-layout explorer (implemented bilingually):** split-half/interleaved maps, frequency-pair assignment, consistent permutation and a deliberate mismatch mode that exposes silent numerical errors.
- **P1 — Multi-frequency explorer (implemented bilingually):** control head dimension, model base and position; compare inverse frequencies, wavelengths and accumulated angles for representative pairs. Numerical monotonicity checks cover dimensions 64/128/256 and bases 10,000/1,000,000.
- **P1 — Partial RoPE memory ledger (implemented bilingually):** controls estimate cosine/sine table bytes separately from full-width K/V cache bytes, with explicit one-layer and dtype assumptions.
- **P1 — NoPE causal-prefix experiment:** vary visible prefix length and attention distribution; include limitations and counterexamples.
- **P1 — Hybrid layer strip:** toggle RoPE/NoPE by layer and trace inherited positional information.
- **P1 — Relative-bias score decomposition:** distinguish T5 distance buckets from an input-conditioned bias such as Inkling.
- **P2 — Architecture evidence dashboard:** dated, filterable gallery summary with denominators and uncertainty; outside the core path.

### 4.4 Interaction pattern

For each P0/P1 component: **predict → manipulate one variable → observe tensor/geometry → explain invariant or failure → run a small test**. Visuals should be experiments, not decoration. Provide a static annotated fallback and text explanation so lessons remain usable without interaction.


## 5. Integration performed

- Registered the source with bounded scan scope and explicit reuse restrictions.
- Added atomic extractions distinguishing established derivations from context-dependent architecture claims.
- Extended the existing bilingual RoPE pages with modern variants, frequency schedule, pairing conventions, PyTorch table construction and test ideas.
- Added a bilingual six-stage QK attention pipeline with a synthetic three-token example, Q/K positional rotations, causal-mask toggle, softmax weights and weighted V aggregation; registered its local JS/CSS resources.
- Added a bilingual pair-layout explorer comparing interleaved and split-half storage, showing the required permutation and demonstrating how mixing conventions changes the numerical rotation even when tensor shapes remain valid.
- Extended the concept-resource graph so Q/K/V, attention scores and weights, scaled dot-product attention, softmax and causal masking now link to the bilingual RoPE lessons; updated page relations to include causal masking.
- Added a bilingual interactive RoPE pair explorer with a shared-shift control, live SVG vectors, pair-level dot product and explicit fixed-Q/K caveat; added shared JS/CSS assets and registered them as Quarto resources.
- Added a bilingual RoPE frequency explorer with controls for head dimension, model base and position; it displays representative inverse frequencies, wavelengths and accumulated angles. Added a dedicated `rope-inverse-frequency` concept and registered the component assets.
- Added a bilingual Partial RoPE memory ledger that independently estimates precomputed cosine/sine tables and full-width K/V cache memory, with explicit assumptions for batch, sequence length, KV heads, head dimension and bytes per element.
- Added the annotated bibliography entry.
- Linked both RoPE deep dives from the canonical positional-encoding concept.

No new concept IDs, introductory pages, copied figures or external code were added.

## 6. Remaining work

- If access to the original image assets becomes available, perform a pixel-level visual audit; the complete caption-and-context audit is already recorded in §4.
- The P0 position-entry-point map, RoPE pair explorer, six-stage QK attention pipeline and split-half/interleaved pair-layout explorer are implemented bilingually. The P1 frequency explorer and Partial RoPE memory ledger are implemented bilingually. Remaining P1 work: NoPE causal-prefix, hybrid-layer and relative-bias experiments.
- Browser-test all five interactive components in the rendered French and English pages, including keyboard and screen-reader behaviour; no browser rendering has yet been run in this branch.
- Execute the statically inspected Qwen3 notebook and compare its numerical outputs; separately add tests for explicit position IDs and incremental KV-cache decoding, which are not covered by the inspected forward path.
- Validate bilingual Quarto rendering, source/extraction schemas, concept graph and navigation in CI.

## 7. Technical references

- [Su et al. (2021), RoFormer](https://arxiv.org/abs/2104.09864)
- [Vaswani et al. (2017), Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [The Impact of Positional Encoding on Length Generalization in Transformers](https://arxiv.org/abs/2305.19466)
- [Raschka, Qwen3 from scratch](https://github.com/rasbt/LLMs-from-scratch) — the linked standalone notebook was statically inspected for RoPE, QK normalization, GQA and buffers; it was not executed.
