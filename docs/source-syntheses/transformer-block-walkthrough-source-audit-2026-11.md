# Transformer Block Walkthrough — source-to-code audit pilot

**Audit date:** 2026-11-27  
**Pilot:** #1741, third archetype (implementation-led Build page)  
**Canonical pages:** [FR](../../site/fr/transformer-block-walkthrough.qmd) · [EN](../../site/en/transformer-block-walkthrough.qmd)  
**Reference implementation:** [transformer_block.py](../../src/llm_lab/foundations/transformer_block.py)  
**Related primitive:** [attention.py](../../src/llm_lab/foundations/attention.py)  
**Tests:** [test_transformer_block.py](../../tests/unit/test_transformer_block.py) · [test_attention.py](../../tests/unit/test_attention.py)

## 1. Audit status and evidence boundary

This is a **recognition and source-to-code contract audit**, not yet a completed six-source ingestion. The two language pages and implementation/test files were inspected directly in the repository. The six missing research references were checked against publisher/arXiv landing pages and available paper excerpts to establish bibliographic identity and broad contribution. Their complete focused reviews, atomic extractions, stable source IDs and source-page relations remain to be done.

Do not promote any missing source to scanned or partially-scanned merely because an abstract or search excerpt was read. The two existing source records (Vaswani and Raschka) must be reused, not duplicated.

## 2. Learner contract and implementation boundary

The page's observable contract is to follow the reference block from initialization through forward, trace (B,T,d) through pre-LN attention and MLP residual branches, explain Q/K/V projections, per-head slices and output projection O, and distinguish architectural variants without implying that MQA, GQA, MLA, sliding-window or sparse attention are implemented by this reference block.

The implementation is a small NumPy teaching implementation, not a production kernel and not a trainable model. TransformerBlock initializes parameters but contains no optimizer, backward pass or parameter update. Explicit loops over batch and heads are for inspectability, not performance.

### What the code establishes

| Claim | Direct implementation evidence | What it does not establish |
|---|---|---|
| Pre-LN residual order | forward normalizes inside the attention and MLP branches, then adds each branch output to x | Universal optimization superiority of Pre-LN |
| Q/K/V are distinct projections of the same normalized input | _attention calls linear three times with w_q, w_k and w_v | That every Transformer variant uses this projection layout |
| Head partitioning | Each head receives a contiguous slice of projected width | Separate per-head parameter matrices; this implementation slices full-width projections |
| Head outputs are mixed by O | Head outputs are written into disjoint slices, then passed through w_o | Semantic independence of attention heads |
| Causal self-attention | causal_mask is passed to the single-head primitive | Identical mask semantics across APIs |
| Position-wise MLP | linear → GELU → linear on the last dimension | Token mixing inside the MLP |
| Depth-scaled output initialization | Only w_o and w_fc2 use 0.02 / sqrt(2L) | Constant residual variance or guaranteed stable training |
| Deterministic initialization from caller RNG | The block consumes the supplied NumPy generator | Cross-version/platform reproducibility unless separately tested |

### What the tests establish

| Test family | Assertions | Boundary |
|---|---|---|
| Block forward | Output shape is unchanged and values are finite for a small seeded configuration | Not a training or convergence test |
| Residual update | With stubbed sublayers, both branch outputs are added to the stream | Does not verify learned residual behavior |
| Initialization | Six parameter groups receive expected base/depth-scaled standard deviations | Does not establish deep-network variance propagation |
| Attention primitive | Shape contracts, key-axis normalization, weighted-value calculation, mask validation and fully-masked-row zero convention | No GPU performance or production-kernel equivalence |
| Causal invariance | Future key/value perturbations do not alter earlier outputs under the causal mask | Only the tested primitive/setup |
| Head-count validation | Non-divisible head width is rejected by _attention | Constructor validation belongs to GPTConfig |

Papers justify architectural ideas and report results under their own conditions. Repository code demonstrates one realization. Unit tests verify only their assertions. These evidence classes are not interchangeable.

## 3. Reconciled page bibliography

Both FR and EN pages expose the same eight external references in the same order:

| Source | Role in the page | Canonical provenance status |
|---|---|---|
| Xiong et al. (2020), On Layer Normalization in the Transformer Architecture | Pre-LN/Post-LN placement; initialization-time gradient analysis and warm-up implications | Missing from data/sources.yml |
| Vaswani et al. (2017), Attention Is All You Need | Original multi-head attention and Transformer architecture | Existing canonical record; reuse |
| Shazeer (2019), Fast Transformer Decoding: One Write-Head is All You Need | MQA: shared K/V heads and incremental-decoding bandwidth motivation | Missing |
| Ainslie et al. (2023), GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints | GQA and uptraining from MHA checkpoints | Missing |
| DeepSeek-AI et al. (2024), DeepSeek-V2 | MLA: low-rank joint K/V compression into a cached latent | Missing |
| Jiang et al. (2023), Mistral 7B | Model case combining GQA and sliding-window attention | Missing |
| Beltagy et al. (2020), Longformer: The Long-Document Transformer | Local/windowed plus task-motivated global attention | Missing |
| Sebastian Raschka, A Visual Guide to Attention Variants in Modern LLMs | Secondary pedagogical/visual comparison | Existing canonical record; reuse |

Internal links to implementation, primitive, tests, project status and roadmap are internal implementation evidence, not external sources.

The current main initially exposed seven non-bibliographic `related.pages` associations, not five. After checking each against the actual page scope, five are retained as discovery links and two FlashAttention-only associations are removed; the eight direct bibliography relations are recorded separately.

## 4. Preliminary contribution map

| Source | Distinct contribution relevant to this page | Qualification |
|---|---|---|
| Xiong et al. (2020) | Mean-field analysis connects Post-LN's large expected gradients near the output at initialization to warm-up sensitivity; Pre-LN has better-behaved initialization gradients in the paper's setting. | Does not prove universal Pre-LN superiority. Architecture, initialization, optimizer and training protocol matter. Verify exact section/equation locators in the focused review. |
| Vaswani et al. (2017) | Original MHA: multiple learned Q/K/V projections, concatenation and output projection. | Original encoder-decoder Transformer is not identical to every decoder-only GPT block. |
| Shazeer (2019) | MQA shares one K head and one V head across query heads to reduce repeated KV reads during incremental decoding. | Experimental speed/quality findings are workload-specific. MQA changes KV-head multiplicity; it does not compress K/V into a latent. |
| Ainslie et al. (2023) | GQA interpolates between MHA and MQA with an intermediate number of K/V heads; proposes uptraining MHA checkpoints, including mean-pooling K/V projections. | Quality/speed trade-offs and the reported 5% uptraining budget are paper-specific. GQA is not MLA. |
| DeepSeek-AI et al. (2024) | MLA jointly compresses K/V into a low-rank latent cached during inference, reconstructs per-head K/V and adds a decoupled RoPE path. | Not simply fewer shared KV heads. DeepSeek-V2 also includes MoE; keep MoE outside this attention-variant claim. |
| Jiang et al. (2023) | Mistral 7B combines GQA with sliding-window attention; stacked local windows allow information to propagate beyond one layer's window. | GQA changes K/V sharing; SWA restricts attended positions. These are orthogonal axes. |
| Beltagy et al. (2020) | Longformer combines local windowed attention (optionally dilated) with task-selected global attention. | Encoder-oriented long-document design, not a drop-in description of causal decoder attention. Linear complexity depends on bounded windows and a small number of global tokens. |
| Raschka | Secondary visual synthesis for comparing modern attention variants. | Not independent primary evidence for each architecture or benchmark claim. Reuse its existing review/extraction and inspection boundary. |

## 5. Keep four architectural axes separate

The variants are not mutually exclusive alternatives on one axis:

- **MHA / MQA / GQA:** number and sharing pattern of K/V heads relative to query heads.
- **MLA:** low-rank joint representation of K/V and what is stored in the cache.
- **Sliding-window / local / global / sparse patterns:** which positions may interact.
- **Pre-LN / Post-LN:** normalization placement relative to residual branches.

These mechanisms can be combined. Mistral is a concrete example of GQA plus sliding-window attention. MLA's latent cache is not a synonym for K/V sharing. Longformer's global/local pattern is not a KV-cache compression method.

## 6. Claim × paper × implementation × test map

| Page claim | External evidence | Repository evidence | Test evidence / limitation |
|---|---|---|---|
| Pre-LN places normalization inside each residual branch | Xiong et al. (2020); original architecture contrast in Vaswani (2017) | TransformerBlock.forward | Residual-addition test; no optimization experiment |
| Distinct learned Q/K/V projections and output O | Vaswani (2017), MHA section | _attention and parameter initialization | Shape/forward tests; not all MHA layouts |
| MQA shares K/V across query heads | Shazeer (2019) | Not implemented | No MQA test |
| GQA uses an intermediate K/V-head count | Ainslie et al. (2023) | Not implemented | No GQA test |
| MLA caches a compressed latent and reconstructs K/V | DeepSeek-V2 §2.1 | Not implemented | No MLA test |
| Mistral combines GQA and SWA | Mistral 7B paper | Not implemented | No Mistral architecture test |
| Local/global sparse attention | Longformer §§2–3 | Not implemented | No Longformer test |
| Reference attention is causal and row-normalized over allowed keys | Vaswani (2017) for base attention; project mask contract is implementation-specific | attention.py | test_attention.py checks mask, normalization and future perturbation invariance |
| Reference block preserves input shape | No external source needed | TransformerBlock.forward | test_block_forward_preserves_shape_and_stays_finite |

## 7. Diversity, independence and evidence diagnosis

- **Format:** seven research papers and one tutorial. Appropriate for a Build page comparing research-defined architecture choices; another generic blog would not address the main provenance gap.
- **Language:** all eight external references are English. This is a real concentration, but no French source is currently shown to add a distinct primary or implementation contribution. Do not add one to satisfy a quota.
- **Perspective:** theory/optimization (Xiong), original architecture (Vaswani), inference bandwidth (Shazeer), K/V head grouping (Ainslie), latent compression (DeepSeek), combined model case (Mistral), sparse position pattern (Longformer), pedagogical synthesis (Raschka).
- **Independence:** distinct publications and author groups, but not independent replications of one common claim. Several are sequential architectural developments. Treat them as complementary design evidence, not corroboration of a universal performance claim.
- **Evidence class:** papers support definitions, methods and paper-specific experiments; source code demonstrates the project's implementation; tests establish only asserted properties.
- **Freshness:** papers are stable historical references; implementation is branch/commit-sensitive. The page currently points to main, which is convenient but not a reproducibility pin.

No aggregate diversity score is warranted. The useful diagnostic is whether each architectural distinction and implementation claim has the right evidence class.

## 8. Actions — ordered and minimal

### P0 — provenance and primary-source review

- [x] Reuse the existing canonical IDs for Vaswani and Raschka; do not duplicate either.
- [x] Add canonical source records for Xiong, Shazeer, Ainslie, DeepSeek-V2, Mistral 7B and Longformer after verifying creators, publication/version, URL, licence and taxonomy values.
- [x] Inspect only the paper sections used by the page; record precise section/equation/table locators and limitations.
- [x] Add one bounded extraction file per newly registered paper; extract only page-relevant definitions, mechanisms, assumptions, results and limitations.
- [x] Add focused reviews or extend existing reviews where appropriate; do not create a review file per source by default.

### P1 — page and code reconciliation

- [x] Compare exact FR/EN external URLs, order and surrounding claims at the final branch head.
- [x] Resolve the five related.pages associations by canonical source ID and purpose; add the eight explicit page relationships only after IDs are confirmed.
- [x] Pin code links to a commit or line anchors and record the reviewed commit SHA.
- [x] Check that every variant paragraph states whether it is implemented, tested, compared or optional context.
- [x] Add tests only where an implemented behavior is part of the teaching contract.

### P2 — validation

- [ ] Run source registry and extraction schema validators.
- [ ] Run focused Python tests and the relevant full suite.
- [ ] Render FR and EN with Quarto and inspect both.
- [ ] Inspect mobile layout, interactive diagram keyboard behavior and accessibility.
- [ ] Keep scientific review, code/test validation, visual inspection, accessibility and learner transfer as separate gates.

## 9. Conclusion after the source-to-code reconciliation

The page now has canonical records and bounded extractions for all eight visible external papers. Its documentary graph distinguishes direct bibliography from discovery associations. The implementation and tests remain a separate evidence stream: papers cannot prove what this code executes, and tests cannot establish the research claims in those papers.

The main intellectual risk is collapsing four orthogonal design axes—normalization placement, K/V-head sharing, latent KV compression and position sparsity—into one list of competing attention variants. Teach these axes separately and use Mistral as an example of combination, not interchangeability.

**Status:** recognition/source-to-code audit documented; six-source ingestion, relation reconciliation and final validation remain open. No claim is made that the six papers have been fully inspected or that the public page has changed.


## 10. Phase A ingestion and relation reconciliation — 2026-11-27

### Direct bibliography: eight source-page relations

The FR and EN pages expose the same eight external papers, in the same order. The two existing canonical records were reused; six records and six extraction files were added. Every new source remains `partially-scanned`: the exact sections used by the page were inspected, but this pass does not claim a full-paper, supplementary-material, code or data audit.

| Page claim | Canonical source | Precise inspected locator | Evidence boundary |
|---|---|---|---|
| Pre-LN/Post-LN placement and optimization rationale | Xiong et al. (2020) | §3.3, Theorem 1; §4.2, Figures 4–5 | Theoretical result depends on the paper's simplified initialization assumptions; experiments are configuration-specific |
| MHA definition and learned projections | Vaswani et al. (2017) | §3.2.2–3.2.3 | Primary architecture definition; page's NumPy implementation is a teaching implementation, not a reproduction of the full paper |
| MQA shared K/V heads | Shazeer (2019) | §3; §3.1; §§4.2–4.3 | Primary MQA definition; speed and quality trade-offs are hardware/model-specific |
| GQA grouping and MHA→GQA uptraining | Ainslie et al. (2023) | §§2.1–2.2, Figure 2; §§3.2–3.3 | Primary GQA definition; 5% uptraining and quality/speed claims are T5-experiment-specific |
| MLA low-rank joint K/V compression | DeepSeek-AI (2024) | §2.1.2, equations 9–11 and Figure 3; §2.1.4, Table 1 | Primary MLA equations; reported cache savings are DeepSeek-V2-specific |
| GQA + sliding-window configuration | Jiang et al. (2023), Mistral 7B | §2, Table 1, Figure 1 | Concrete model case; GQA definition remains sourced to Ainslie |
| Local, dilated and global sparse attention | Beltagy et al. (2020), Longformer | §3.1–3.2, Figure 2 | Linear scaling assumes fixed local window and a small number of global positions |
| Visual cross-variant comparison | Raschka (2026) | Article introduction, GQA/sparse-attention sections and conclusion (existing partial scan) | Pedagogical comparison only; not primary evidence for the research claims |

### Canonical records and extractions

- Existing records reused and related to both walkthrough pages: `vaswani-et-al-attention-is-all-you-need-2017`, `raschka-visual-attention-variants`.
- New source records: `xiong-et-al-layer-normalization-transformer-2020`, `shazeer-fast-transformer-decoding-mqa-2019`, `ainslie-et-al-gqa-2023`, `deepseek-ai-deepseek-v2-2024`, `jiang-et-al-mistral-7b-2023`, `beltagy-et-al-longformer-2020`.
- Each new paper has one `data/extractions/<source-id>.yml` with atomic items, exact locators, assumptions, limitations, candidate destinations and a bounded `integrate-by-reference` disposition.
- No new concept ID, concept page, source collection or page was created. Only existing canonical concept IDs are referenced where justified.

### Discovery associations: five retained, two removed

The seven non-bibliographic associations found on the current main branch were:
- Retain Nishanthan K (Q/K/V pedagogical explanation), Zsombor Veres Lakos (attention implementation), Jay Alammar (Transformer overview), PyTorch SDPA API (implementation/API reference) and Jose Parreño García (Q/K/V and attention explanation) as discovery resources.
- Remove Dao et al. FlashAttention and The AI Edge FlashAttention guide from the Transformer Block Walkthrough relation. The page does not teach IO-aware/FlashAttention kernels; those sources remain associated with the scaled-dot-product-attention and attention-score-scaling pages where their scope belongs.

The eight direct citations are now linked through canonical source records; the five retained discovery associations remain explicitly distinct from the bibliography.

### Implementation and test boundary

The current page states that its NumPy block is a pedagogical MHA example: (H_{KV}=H_q), separate K/V projections per head and dense causal attention. It does **not** implement MQA/GQA sharing, an inference KV cache, MLA compression or sparse attention. Those variants are research-grounded comparisons, not code features.

Code references now use line anchors:
- `transformer_block.py#L50-L186`: pre-LN block, attention and MLP branches, residual forward pass.
- `attention.py#L9-L128`: causal mask and single-head scaled-dot-product primitive.
- `test_attention.py#L13-L34` and `#L229-L270`: mask structure, shape/invariant and causal-invariance tests.
- `test_transformer_block.py#L23-L85`: shape/finite-output, input validation, initialization and residual-stream behavior.

Reviewed against main commit `edaef38438baeac46cb807a926fcdda8512da1b2`. These tests establish the implemented primitive/block contract only; they do not validate the research variants as implementations.

### Remaining validation gates

Source records and extraction files are ready for the source-catalogue validator and focused/full test runs in the PR. Rendered-page inspection, manual figure review, accessibility and learner transfer remain separate gates. The page has no interactive attention diagram requiring a new keyboard interaction contract; do not create one just to satisfy this audit.
