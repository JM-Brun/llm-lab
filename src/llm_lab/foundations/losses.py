"""Small reference implementations of common training losses."""

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from llm_lab.foundations.types import FloatArray


def _validate_logits_targets(
    logits: FloatArray,
    targets: Sequence[int] | NDArray[np.integer],
) -> tuple[FloatArray, NDArray[np.integer]]:
    """Validate and return cleaned logits and target arrays."""
    if logits.ndim != 2:
        raise ValueError("logits must have shape (batch_size, num_classes)")
    if not np.all(np.isfinite(logits)):
        raise ValueError("logits must contain only finite values")
    if logits.shape[0] == 0 or logits.shape[1] == 0:
        raise ValueError("logits must have a non-empty batch and class dimension")

    target_array = np.asarray(targets)
    if target_array.ndim != 1 or target_array.shape[0] != logits.shape[0]:
        raise ValueError("targets must have shape (batch_size,)")
    if not np.issubdtype(target_array.dtype, np.integer):
        raise ValueError("targets must contain integer class indices")
    if np.any(target_array < 0) or np.any(target_array >= logits.shape[1]):
        raise ValueError("target class index is out of range")
    return logits, target_array


def cross_entropy_from_logits(
    logits: FloatArray,
    targets: Sequence[int] | NDArray[np.integer],
) -> float:
    """Return mean multiclass cross-entropy from unnormalized logits.

    Uses logaddexp.reduce to avoid an overflowing max-subtraction
    intermediate for finite logits with opposite signs near float64 limits.
    A mathematically valid loss outside the finite float64 range is rejected.
    """
    logits, target_array = _validate_logits_targets(logits, targets)
    log_partition = np.logaddexp.reduce(logits, axis=1)
    target_logits = logits[np.arange(logits.shape[0]), target_array]
    with np.errstate(over="ignore", invalid="raise"):
        per_example_losses = log_partition - target_logits
    if not np.all(np.isfinite(per_example_losses)):
        raise ValueError("cross-entropy loss exceeds the finite float64 range")
    return float(np.sum(per_example_losses / logits.shape[0]))


def cross_entropy_gradient(
    logits: FloatArray,
    targets: Sequence[int] | NDArray[np.integer],
) -> FloatArray:
    """Return the gradient of mean cross-entropy with respect to logits."""
    logits, target_array = _validate_logits_targets(logits, targets)
    log_partition = np.logaddexp.reduce(logits, axis=1, keepdims=True)
    # Underflow of a very unlikely class to probability zero is intentional.
    with np.errstate(over="ignore", under="ignore", invalid="raise"):
        probabilities = np.exp(logits - log_partition)
    probabilities[np.arange(logits.shape[0]), target_array] -= 1.0
    return np.asarray(probabilities / logits.shape[0], dtype=np.float64)
