"""Small reference implementations of attention mechanisms and score transformations."""

import numpy as np

from llm_lab.foundations.types import FloatArray

__all__ = [
    "causal_mask",
    "scaled_dot_product_attention",
    "softmax_with_temperature",
]


def causal_mask(seq_len: int) -> FloatArray:
    """Return an additive causal attention mask of shape (seq_len, seq_len).

    Position i can attend to positions j <= i (mask value 0.0).
    Positions j > i receive -inf to ensure zero weight after softmax.

    Args:
        seq_len: Number of sequence positions. Must be positive.

    Raises:
        ValueError: If seq_len is not a positive integer.
    """
    if seq_len <= 0:
        raise ValueError("seq_len must be a positive integer")

    mask = np.full((seq_len, seq_len), -np.inf, dtype=np.float64)
    indices = np.tril_indices(seq_len)
    mask[indices] = 0.0
    return mask


def softmax_with_temperature(
    logits: FloatArray,
    temperature: float = 1.0,
    axis: int = -1,
) -> FloatArray:
    """Apply numerically stable softmax with temperature scaling along specified axis.

    Args:
        logits: Input array containing real-valued scores.
        temperature: Temperature parameter > 0. Values < 1 make the distribution
            sharper; values > 1 make it more uniform.
        axis: Dimension along which softmax is applied.

    Raises:
        ValueError: If logits contains non-finite values or temperature <= 0.
    """
    if temperature <= 0:
        raise ValueError("temperature must be strictly positive")
    if not np.all(np.isfinite(logits)):
        raise ValueError("logits must contain only finite values")

    scaled = logits / temperature
    max_val = np.max(scaled, axis=axis, keepdims=True)
    shifted = scaled - max_val
    exp_vals = np.exp(shifted)
    sum_exp = np.sum(exp_vals, axis=axis, keepdims=True)
    return np.asarray(exp_vals / sum_exp, dtype=np.float64)


def scaled_dot_product_attention(
    queries: FloatArray,
    keys: FloatArray,
    values: FloatArray,
    mask: FloatArray | None = None,
) -> tuple[FloatArray, FloatArray]:
    """Compute scaled dot-product attention for single-head matrices.

    O = softmax(Q K^T / sqrt(d_k) + M) V

    Args:
        queries: Array of shape (T_q, d_k).
        keys: Array of shape (T_k, d_k).
        values: Array of shape (T_k, d_v).
        mask: Optional additive mask of shape (T_q, T_k), where 0.0 allows
            attention and -inf forbids it.

    Returns:
        A tuple (output, weights) where:
            output has shape (T_q, d_v),
            weights has shape (T_q, T_k).

    Raises:
        ValueError: If array dimensions or shapes do not match the attention contract.
    """
    if queries.ndim != 2 or keys.ndim != 2 or values.ndim != 2:
        raise ValueError("queries, keys, and values must be 2D arrays")
    if queries.shape[1] != keys.shape[1]:
        raise ValueError("queries and keys must have identical key dimension d_k")
    if keys.shape[0] != values.shape[0]:
        raise ValueError("keys and values must have identical sequence length T_k")
    if (
        not np.all(np.isfinite(queries))
        or not np.all(np.isfinite(keys))
        or not np.all(np.isfinite(values))
    ):
        raise ValueError("queries, keys, and values must contain finite numbers")

    t_q, d_k = queries.shape
    t_k, _ = keys.shape

    if d_k == 0 or t_q == 0 or t_k == 0:
        raise ValueError("dimensions cannot be empty")

    scores = (queries @ keys.T) / np.sqrt(d_k)

    if mask is not None:
        if mask.shape != (t_q, t_k):
            raise ValueError(f"mask shape {mask.shape} does not match expected ({t_q}, {t_k})")
        scores = scores + mask

    # Handle numerical stability for softmax
    max_scores = np.max(scores, axis=-1, keepdims=True)
    # If a row is fully masked (-inf), max_scores is -inf; avoid nan
    valid_rows = np.isfinite(max_scores)
    shifted = np.zeros_like(scores)
    shifted[valid_rows.squeeze(-1)] = (scores - max_scores)[valid_rows.squeeze(-1)]
    exp_scores = np.exp(shifted)
    exp_scores[~np.isfinite(scores)] = 0.0

    sum_exp = np.sum(exp_scores, axis=-1, keepdims=True)
    # Avoid division by zero on entirely masked rows
    safe_sum = np.where(sum_exp > 0, sum_exp, 1.0)
    weights = exp_scores / safe_sum

    output = weights @ values
    return np.asarray(output, dtype=np.float64), np.asarray(weights, dtype=np.float64)
