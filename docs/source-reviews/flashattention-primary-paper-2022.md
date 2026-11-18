# Source review — Dao et al. (2022): FlashAttention primary paper

**Review date:** 2026-11-18  
**Source ID:** `dao-et-al-flashattention-2022`  
**Extraction items:** `exact-io-aware-attention`, `online-softmax-tiling`, `io-complexity`, `block-sparse-extension`  
**Status:** focused primary-source review of the abstract and Sections 2.2, 3.1–3.3 and selected Section 4 claims; not a full re-audit.

## Primary source

Dao, Tri; Fu, Daniel Y.; Ermon, Stefano; Rudra, Atri; Ré, Christopher. “FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.” NeurIPS 2022, arXiv:2205.14135.

- arXiv: https://arxiv.org/abs/2205.14135
- NeurIPS proceedings: https://proceedings.neurips.cc/paper/2022/hash/67d57c32e20fd0a7a302cb81d36e40d5-Abstract.html
- Publisher PDF: https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf

## Claims and exact locators

1. **IO-aware exact dense attention** — Abstract; Sections 3.1–3.2. The paper proposes tiling to reduce HBM reads/writes and avoid storing the full attention matrix in HBM. Theorem 1 states that Algorithm 1 returns the standard attention output with O(N²d) FLOPs and O(N) additional memory beyond inputs and output.
2. **Online softmax / tiled aggregation** — Section 3.1, Algorithm 1. Running maxima, exponential sums and weighted-value accumulators are rescaled and merged across blocks to preserve the global softmax result.
3. **IO complexity** — Section 3.2, Theorem 2 and Proposition 3. The asymptotic HBM-access bounds are stated under a two-level memory model and a specified SRAM-size range. They are not a direct universal wall-clock guarantee.
4. **Block-sparse extension** — Section 3.3, Proposition 4. This is a separate approximate attention algorithm that skips zero blocks according to a block-sparsity mask. It is not the same algorithmic claim as exact dense FlashAttention.
5. **Empirical performance** — Section 4 and Appendix E. Results are tied to the reported hardware, software, tensor shapes, workloads and baselines; do not generalize paper speedups to arbitrary devices or runtime phases.

## Scientific distinctions for the bridge pilot

### Mathematical function versus implementation

Vaswani et al. define scaled dot-product attention as the mathematical operation. Dao et al. provide a later algorithm for executing that operation with an IO-aware schedule. The relation is an implementation mapping with a correctness claim under the paper's assumptions, not a new definition of attention.

### IO efficiency versus information-theoretic compression

FlashAttention reduces data movement between HBM and on-chip SRAM and avoids materializing large intermediate matrices in HBM. It does not encode the input sequence into a shorter lossless bitstream. The term “memory-efficient” refers to execution memory/IO, not Shannon source coding, rate-distortion compression or MDL.

### Exact dense versus block-sparse approximate attention

The exact dense algorithm and the block-sparse extension must have separate claims and evidence. The paper explicitly describes the latter as approximate. A source-local teaching graph may connect them as an extension/contrast, but must not transfer the exactness claim to the sparse variant.

### Arithmetic versus IO complexity

The paper's IO-complexity theorem concerns HBM accesses. The algorithm still performs O(N²d) FLOPs for exact dense attention. Reduced HBM traffic, reduced intermediate storage, peak allocated memory, latency and throughput are distinct measurements.

## Mapping to existing LLM Lab structures

- Mathematical operation: canonical `scaled-dot-product-attention`, `attention-score`, `attention-weight`, `softmax`.
- Computational projection: `attention-score-computation`, `attention-scores`, `masked-attention-scores`, `attention-softmax`, `attention-weights`, `value-aggregation`, `attention-output`.
- Source-local reconstruction: `data/extractions/the-ai-edge-how-flashattention-speeds-up-llm-attention.yml`.
- Existing measurement plan: `docs/experiments/flashattention-benchmark-protocol.md`.

No new canonical concept or graph is needed. The new source record and extraction items supply primary evidence to the existing structures.

## Integration decision

Add the primary paper to `data/sources.yml` and its focused extraction to `data/extractions/dao-et-al-flashattention-2022.yml`. Keep it `partially-scanned`; the focused review does not claim to have re-audited all appendices or reproduced benchmarks. Continue to use the existing FlashAttention benchmark protocol for future measurements.
