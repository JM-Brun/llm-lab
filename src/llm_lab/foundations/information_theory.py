"""Reference information-theory quantities for discrete distributions."""

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def _validate_base(base: float) -> None:
    """Require a logarithm base greater than one."""
    if not np.isfinite(base) or base <= 1.0:
        raise ValueError("base must be finite and greater than one")


def _distribution(values: FloatArray, name: str) -> FloatArray:
    """Validate a finite, non-empty, normalized probability vector."""
    probabilities = np.asarray(values, dtype=np.float64)
    if probabilities.ndim != 1 or probabilities.size == 0:
        raise ValueError(f"{name} must be a non-empty one-dimensional vector")
    if not np.all(np.isfinite(probabilities)):
        raise ValueError(f"{name} must contain only finite values")
    if np.any(probabilities < 0.0):
        raise ValueError(f"{name} cannot contain negative probabilities")
    if not np.isclose(probabilities.sum(), 1.0, rtol=1e-9, atol=1e-12):
        raise ValueError(f"{name} must sum to one")
    return probabilities


def shannon_entropy(probabilities: FloatArray, *, base: float = np.e) -> float:
    """Return discrete Shannon entropy, in the selected logarithm base."""
    p = _distribution(probabilities, "probabilities")
    _validate_base(base)
    positive = p > 0.0
    return float(-np.sum(p[positive] * np.log(p[positive])) / np.log(base))


def cross_entropy(target: FloatArray, predicted: FloatArray, *, base: float = np.e) -> float:
    """Return H(target, predicted); infinite if predicted mass misses target support."""
    q = _distribution(target, "target")
    p = _distribution(predicted, "predicted")
    if q.shape != p.shape:
        raise ValueError("target and predicted must have the same shape")
    _validate_base(base)
    if np.any((q > 0.0) & (p == 0.0)):
        return float("inf")
    positive = q > 0.0
    return float(-np.sum(q[positive] * np.log(p[positive])) / np.log(base))


def kl_divergence(target: FloatArray, predicted: FloatArray, *, base: float = np.e) -> float:
    """Return forward KL D_KL(target || predicted), including support checks."""
    q = _distribution(target, "target")
    p = _distribution(predicted, "predicted")
    if q.shape != p.shape:
        raise ValueError("target and predicted must have the same shape")
    if np.any((q > 0.0) & (p == 0.0)):
        return float("inf")
    positive = q > 0.0
    return float(np.sum(q[positive] * np.log(q[positive] / p[positive])) / np.log(base))


def perplexity(mean_nll: float, *, base: float = np.e) -> float:
    """Convert mean negative log-likelihood to perplexity in its matching base."""
    if not np.isfinite(mean_nll) or mean_nll < 0.0:
        raise ValueError("mean_nll must be finite and non-negative")
    _validate_base(base)
    return float(base**mean_nll)


def ideal_code_lengths(probabilities: FloatArray, *, base: float = 2.0) -> FloatArray:
    """Return ideal information lengths -log_base(p); zero mass maps to infinity."""
    p = _distribution(probabilities, "probabilities")
    _validate_base(base)
    lengths = np.full_like(p, np.inf)
    positive = p > 0.0
    lengths[positive] = -np.log(p[positive]) / np.log(base)
    return lengths
