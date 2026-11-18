# Source review — Vaswani et al.: scaled dot-product attention

**Review date:** 2026-11-18  
**Source:** Vaswani et al., *Attention Is All You Need* (2017), arXiv:1706.03762, §3.2.1, Equation (1), Figure 2.  
**Canonical source ID:** `vaswani-et-al-attention-is-all-you-need-2017`  
**Extraction item:** `vaswani-et-al-attention-is-all-you-need-2017:scaled-dot-product-attention`  
**Status:** focused primary-source review; not a full-paper re-audit.

## Claim supported by the primary source

For query matrix Q, key matrix K and value matrix V, the paper defines:

`Attention(Q, K, V) = softmax(QKᵀ / √dₖ)V`

The prose in §3.2.1 specifies that query–key dot products are divided by √dₖ, then softmax produces weights applied to the value vectors. Figure 2 shows the operation sequence (matrix multiplication, scaling, optional mask, softmax, weighted-value multiplication).

Primary source: https://arxiv.org/abs/1706.03762  
Publisher-hosted paper: https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf

## Mathematical interpretation and scope

For one fixed query, if softmax is applied over a finite set of admissible keys, the resulting row is a normalized non-negative distribution over those key positions. This follows from the mathematical definition of softmax. Shannon entropy can therefore be applied to that row as a derived statistic, provided the query, head, layer, input, mask and key support are specified.

This does **not** establish that:
- attention weights are mutual information;
- the entropy of one attention row is mutual information;
- the weights quantify semantic importance or causal influence;
- the weighted aggregation is a lossless or rate-distortion-optimal compression code.

Mutual information requires a joint distribution and its marginals. An attention row alone does not provide those objects. The project’s existing `attention_kl_vs_mutual_information.py` experiment and the information-theory synthesis already provide a concrete counterexample to conflating row-wise KL-to-uniform with MI.

## Mapping to existing LLM Lab structures

- Canonical concepts: `query`, `key`, `value`, `attention-score`, `attention-weight`, `softmax`, `scaled-dot-product-attention`, `self-attention`.
- Existing concept relations: score normalized by softmax; softmax produces attention weights; attention weights are part of scaled dot-product attention.
- Computational graph: Q/K/V, attention-score computation, masked scores, attention softmax, attention weights, weighted-value aggregation and output.
- Learning resources: bilingual scaled-dot-product-attention and Q/K/V pages.

The extraction item is attached to these existing IDs. No new concept or edge is introduced by this review.

## Relation to FlashAttention

Vaswani et al. define the mathematical operation. FlashAttention is a later IO-aware algorithm/kernel strategy for executing exact dense attention with reduced HBM traffic and intermediate materialization. These are different abstraction levels:

`mathematical attention function → computational operation → hardware implementation`

The implementation mapping must be supported separately by Dao et al. (2022), FlashAttention-2 and the existing focused review `docs/source-reviews/flashattention-io-aware-2026-11.md`. Do not infer an information-theoretic compression relation from the word “memory-efficient”.

## Integration decision

Add the §3.2.1 extraction item and update the existing source catalogue classification so the paper is associated with the attention concepts and bilingual attention pages, while retaining its positional-encoding associations. Keep scan status `partially-scanned`: this focused pass does not claim a full-paper re-audit.

No new canonical concept, graph, or relation type is needed.
