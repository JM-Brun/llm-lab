# Source review — PyTorch scaled dot-product attention API

**Review date:** 2026-11-27  
**Source ID:** `pytorch-scaled-dot-product-attention-api`  
**Source:** [`torch.nn.functional.scaled_dot_product_attention`](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)  
**Observed documentation version:** PyTorch 2.15; the stable URL redirected to the versioned `/docs/2.15/` page during this review.  
**Status:** focused official API-reference review; not a source-code or runtime audit.

## 1. Why this source belongs in the page corpus

The bilingual scaled-dot-product-attention pages cite the PyTorch SDPA API alongside the original Transformer paper and FlashAttention. These sources have different evidentiary roles:

- **Vaswani et al. (2017):** primary mathematical definition of scaled dot-product attention.
- **Dao et al. (2022):** primary algorithmic contribution for IO-aware exact attention.
- **PyTorch SDPA API:** official framework contract for arguments, masks, dropout, backend selection and implementation caveats.

The API reference is authoritative for the documented PyTorch function contract, not a substitute for the mathematical paper and not evidence that a specific optimized backend ran in a particular environment.

## 2. Material inspected

The versioned API page was inspected for:
- function signature and reference pseudocode;
- default scale and query/key/value tensor shapes;
- boolean and additive mask semantics;
- causal-mask argument constraints;
- dropout behavior;
- supported implementation families, automatic dispatch and numerical differences;
- Grouped Query Attention support notes and constraints.

No implementation source code was inspected or executed. No CPU/GPU backend was selected, benchmarked or compared. No output parity test was run.

## 3. Findings that matter to LLM Lab

### Mathematical operator and scale

The documented reference path computes query–key products, applies the scale (defaulting to the inverse square root of the query's last dimension), adds the attention bias, applies softmax over the final/key dimension, applies the requested dropout, and multiplies by values.

This is consistent with the mathematical operator in Vaswani et al. The PyTorch pseudocode is an API-level reference path; fused kernels may execute an equivalent operation without materializing the same intermediates.

### Boolean mask polarity

For `scaled_dot_product_attention`, boolean `True` means that a position **participates** in attention. The documentation explicitly warns that this is the inverse of the boolean `key_padding_mask` convention used by `MultiheadAttention`.

This is an implementation-critical distinction for Build material. Do not copy mask polarity between APIs by name alone.

### Causal masking

The API documents `is_causal=True` as a causal mask and rejects simultaneous use of `attn_mask` and `is_causal`. The exact alignment for non-square query/key lengths is version-specific and documented through the causal-bias behavior. The conceptual lesson should continue to delegate mask construction and edge cases to the canonical causal-masking page.

### Dropout

The functional API applies dropout according to `dropout_p`; it does not infer the enclosing module's training/evaluation state. The caller must pass `0.0` for evaluation. This belongs in implementation guidance, not the core mathematical derivation.

### Backend dispatch and numerical behavior

The inspected documentation describes multiple implementation families and automatic selection among eligible backends. Fused implementations have input constraints, and floating-point operation fusion can produce numerically different outputs. Therefore:

- calling the SDPA API does not by itself prove that FlashAttention ran;
- the selected backend must be observed or explicitly controlled in a benchmark;
- output comparisons require appropriate tolerances and recorded dtype/device/backend details;
- a benchmark must not attribute speedups to FlashAttention without backend evidence.

### Grouped Query Attention

The inspected PyTorch 2.15 documentation labels GQA experimental and lists head-count and backend constraints. Treat this as a versioned API capability note, not a timeless architectural guarantee.

## 4. Source and page diversity assessment

The API reference adds a distinct source type and evidence function to the page's visible bibliography: official implementation documentation. It is not another pedagogical tutorial and should not be counted as independent scientific corroboration of the paper.

The page's external references remain English-only. This is not automatically a defect for a mathematical/computational page whose authoritative references are the original paper, a primary algorithm paper and framework API documentation. The bilingual LLM Lab explanation is the learner-facing language layer. A French resource should be sought only if it adds a distinct mathematical or implementation contribution.

## 5. Integration decision

**Register and cite by reference; do not expand the core Understand page with every API caveat.**

- Keep Vaswani as the mathematical anchor.
- Keep Dao et al. as the primary FlashAttention algorithm source.
- Keep PyTorch SDPA as the official API/implementation contract.
- Route mask polarity, dropout and backend-specific details to Build or optional Deepen material where they affect executable code.
- Never claim that the SDPA call selected FlashAttention without runtime/backend evidence.

## 6. Remaining limits

- The stable URL's redirect was observed once; recheck before any version-sensitive implementation change.
- The PyTorch source code and release history were not inspected.
- No backend, device, dtype, performance or numerical-equivalence test was executed.
- The API page's own beta/version warnings remain relevant; this review does not guarantee future compatibility.
