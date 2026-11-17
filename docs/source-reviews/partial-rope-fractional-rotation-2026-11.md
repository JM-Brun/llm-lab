# Source review — Khan et al., “Fractional Rotation, Full Potential?”

**Source:** [arXiv:2603.11611, version 2](https://arxiv.org/abs/2603.11611) · [HTML full text](https://arxiv.org/html/2603.11611v2) · [structured extraction](../../data/extractions/khan-et-al-fractional-rotation-partial-rope-2026.yml)

**Bibliographic status:** v1 submitted 12 March 2026; v2 revised 15 October 2026; accepted as an EMNLP 2026 short paper. The arXiv HTML declares CC BY 4.0. Figures, code and checkpoints are linked, not copied.

## 1. Research question and design

The paper studies how many dimensions of each attention head need rotary position embeddings. It compares 0% (NoPE), 1–4%, 10%, 25%, 50%, 75% and 100% RoPE in sequential and parallel attention designs, using 1B- and 8B-scale configurations, FineWeb/FineWeb-Edu and sequence lengths from 1,024 to 8,192 tokens.

The authors report that approximately 10% or more rotary dimensions generally reaches convergence and final-loss behaviour close to full RoPE in their tested settings. Very low fractions and NoPE show higher loss or training instability in some configurations. QK-Norm mitigates observed NoPE loss spikes.

## 2. Memory result: what is being saved?

Appendix C estimates the memory of the precomputed RoPE sine/cosine cache as a function of maximum sequence length, head dimension and storage precision. The paper reports up to 10× savings by reducing the rotary dimensions.

**This is not a 10× reduction in the KV cache.** The estimate concerns auxiliary RoPE tables; cached keys and values remain full-width. It should not be presented as end-to-end serving-memory savings.

## 3. Relation to Raschka's article

The paper provides primary experimental support for the article's summary that around 10% rotation can match full-RoPE convergence in selected experiments. It also qualifies the article author's opinion that partial RoPE may have limited practical value: at sufficiently long contexts and when the precomputed RoPE cache is material, table-memory savings may be significant.

The difference between the paper's up-to-10× estimate and Raschka's MiniMax-M3 example (roughly 128 MiB saved for 50% rotary dimensions at a 1M context in BF16) reflects different head dimensions, rotary fractions, precision and assumptions. The result scales with the size of the precomputed tables and must be reported with its configuration.

The paper's NoPE instability does not straightforwardly contradict Kazemnejad et al. (2023): the earlier study emphasizes smaller synthetic length-generalization tasks, while this paper studies larger-scale language-model pretraining and convergence. They answer different empirical questions.

## 4. Limits

- Results are bounded to selected 1B/8B configurations, training data, sequence lengths and training protocol.
- The benchmark suite is limited; similar multiple-choice accuracy does not imply equivalence on every downstream task.
- The authors do not establish that 10% is optimal for every architecture, context length or positional-scaling scheme.
- Appendices A, B, D and E were not exhaustively inspected; training artifacts, checkpoints and code were not run.
- No independent reproduction was performed.

## 5. Integration decision

Use this paper to qualify the Partial RoPE sections of the bilingual RoPE deep dives and the Raschka source review. Keep the distinction explicit: **RoPE sine/cosine cache ≠ KV cache**. No new concept IDs are needed.
