# Source review — How FlashAttention Speeds Up LLM Attention

**Review date:** 2026-11-13  
**Source:** Damien Benveniste, *How FlashAttention Speeds Up LLM Attention*, The AI Edge, 13 November 2026.  
**URL:** https://newsletter.theaiedge.io/p/how-flashattention-speeds-up-llm-attention  
**Status:** partial source inspection; technical claims cross-checked against primary and official sources.

## Assessment

This is a useful pedagogical entry point for distinguishing the mathematical attention function from the GPU kernel that executes it. Exact FlashAttention changes data movement and intermediate storage; it does not remove attention connections allowed by the mask. It is not synonymous with sparse attention.

The retrieved newsletter page exposes the title, date, introductory text, running-state explanation, exact-versus-sparse distinction, PyTorch SDPA mention and table of contents. The page labels the full article paid and provides a courtesy excerpt. Later sections on GPU execution, backward recomputation, training, decoding and limits were not accessible. This review does not claim to have read the complete article.

## Claims supported by the accessible excerpt

1. Attention is processed in tiles; the complete score matrix need not be materialized in GPU high-bandwidth memory (HBM).
2. A compact running state combines contributions across key/value tiles.
3. Rescaling when the running row maximum changes preserves stable softmax normalization.
4. Exact FlashAttention preserves allowed attention connectivity; sparse attention changes which positions participate.
5. PyTorch exposes optimized implementations through scaled-dot-product attention (SDPA); the API and the selected backend are distinct.

## Technical reconciliation

- The original NeurIPS paper defines FlashAttention as an IO-aware exact attention algorithm. Tiling reduces reads/writes between HBM and on-chip SRAM. It primarily optimizes data movement, not dense attention's arithmetic complexity.
- Dense self-attention still performs pairwise query-key interactions; arithmetic remains quadratic in sequence length. The full score/probability matrices need not be materialized in HBM.
- “Exact” means mathematical equivalence subject to floating-point effects and implementation tolerances, not universal bitwise identity.
- Online softmax maintains a running maximum m, exponential sum l and weighted-value accumulator u. For a new tile with local maximum mt, sum lt and weighted sum ut: m' = max(m, mt); a = exp(m - m'); b = exp(mt - m'); l' = a*l + b*lt; u' = a*u + b*ut. The final output is u/l. This merges partial statistics without approximation.
- Backward recomputation trades additional arithmetic for avoiding storage of the full probability matrix. It is not free.
- FlashAttention is a family of algorithm/kernel generations, not one immutable kernel. FlashAttention-2 improves parallelism and work partitioning; FlashAttention-3 targets Hopper GPUs with asynchronous overlap, warp specialization, TMA and low-precision execution. Its reported gains are tied to the paper's hardware and workload and must not be generalized to every GPU or dtype. See https://arxiv.org/abs/2307.08691 and https://arxiv.org/abs/2407.08608.
- Speed depends on sequence length, head dimension, batch size, dtype, masks, layout, GPU architecture, backend eligibility, launch overhead and baseline quality.
- Training, prefill and autoregressive decode have different shapes and bottlenecks. Do not generalize one phase's speedup to all others.
- PyTorch SDPA dispatches among eligible implementations. Calling SDPA does not prove that a FlashAttention kernel ran.

## Integration decision

**Integrate by reference and develop a bounded optional Deepen companion; do not add a core-route stage.**

- Keep the Understand lesson on scaled dot-product attention focused on the mathematical operation.
- Link an optional Deepen page covering HBM/SRAM, tiling, online-softmax derivation, fusion, backward recomputation, prefill/decode distinctions and performance caveats.
- Keep the NumPy Build implementation readable and framework-independent. Do not replace it with a GPU kernel or present a Python tile loop as FlashAttention.
- A future PyTorch experiment should compare a materialized reference, SDPA and (where selectable) FlashAttention on identical inputs and masks. Verify the actual backend; record correctness tolerances, peak memory, latency distributions, warm-up, synchronization, hardware, software versions and shapes. CPU-only results cannot establish GPU kernel speedups.
- Do not create a canonical concept node solely for a paper or product name. Consider a stable online-softmax / IO-aware-kernel concept only through a separate bilingual graph review.

## Provenance and reuse

The newsletter is a secondary pedagogical source and its full text was unavailable. No prose, figures or diagrams are reproduced. Rights are unknown; link only. Scientific claims are checked against:

- Dao et al. (2022), *FlashAttention*, NeurIPS: https://arxiv.org/abs/2205.14135
- Dao (2024), *FlashAttention-2*: https://arxiv.org/abs/2307.08691
- Shah et al. (2024), *FlashAttention-3*: https://arxiv.org/abs/2407.08608
- PyTorch SDPA API: https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html
- PyTorch SDPA tutorial: https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial.html
