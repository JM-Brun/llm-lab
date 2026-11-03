"""Truncation filters for next-token sampling distributions.

This module implements the top-k and top-p (nucleus) filters of the
decoding-strategies deep dive: restrict a categorical next-token
distribution to its most probable candidates, then renormalize. Filters
change which tokens can be sampled at one position; they never change
model parameters, and they are not a sequence-search method.
"""

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def _validated_probabilities(probabilities: FloatArray) -> FloatArray:
    """Return the distribution as a validated float64 array."""
    probs = np.asarray(probabilities, dtype=np.float64)
    if probs.ndim != 1 or probs.shape[0] == 0:
        raise ValueError("probabilities must be a non-empty 1D array")
    if not np.all(np.isfinite(probs)):
        raise ValueError("probabilities must contain only finite values")
    if np.any(probs < 0.0):
        raise ValueError("probabilities must be non-negative")
    if not np.isclose(probs.sum(), 1.0, rtol=0.0, atol=1e-8):
        raise ValueError("probabilities must sum to 1")
    return probs


def top_k_filter(probabilities: FloatArray, k: int) -> FloatArray:
    """Return the top-k truncated and renormalized distribution.

    The `k` entries with the highest probabilities are kept, all others are
    set to zero, and the kept entries are renormalized to sum to one. Ties
    are broken by the lowest original index (stable sort), so the result is
    deterministic.

    Args:
        probabilities: One-dimensional categorical distribution summing to 1.
        k: Number of candidates to keep; must be at least 1.

    Returns:
        A new array of the same shape containing the truncated,
        renormalized distribution.

    Raises:
        ValueError: If `k` is below one, or if `probabilities` is not a
            non-empty 1-D finite, non-negative distribution summing to 1.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    probs = _validated_probabilities(probabilities)
    if k >= probs.shape[0]:
        return probs.copy()

    order = np.argsort(-probs, kind="stable")
    kept = order[:k]
    filtered = np.zeros_like(probs)
    filtered[kept] = probs[kept]
    return np.asarray(filtered / filtered.sum(), dtype=np.float64)


def top_p_filter(probabilities: FloatArray, p: float) -> FloatArray:
    """Return the nucleus (top-p) truncated and renormalized distribution.

    The smallest set of most probable entries whose cumulative probability
    reaches or exceeds `p` is kept, including the entry that crosses the
    threshold; all others are set to zero, and the kept entries are
    renormalized to sum to one. Ties are broken by the lowest original index
    (stable sort), so the result is deterministic.

    Args:
        probabilities: One-dimensional categorical distribution summing to 1.
        p: Target probability mass, in (0, 1].

    Returns:
        A new array of the same shape containing the truncated,
        renormalized distribution.

    Raises:
        ValueError: If `p` is outside (0, 1], or if `probabilities` is not
            a non-empty 1-D finite, non-negative distribution summing to 1.
    """
    if not 0.0 < p <= 1.0:
        raise ValueError("p must be in (0, 1]")
    probs = _validated_probabilities(probabilities)
    if p == 1.0:
        return probs.copy()

    order = np.argsort(-probs, kind="stable")
    cumulative = np.cumsum(probs[order])
    crossing = int(np.searchsorted(cumulative, p, side="left")) + 1
    kept = order[: min(crossing, probs.shape[0])]
    filtered = np.zeros_like(probs)
    filtered[kept] = probs[kept]
    return np.asarray(filtered / filtered.sum(), dtype=np.float64)
