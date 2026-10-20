"""Small reference implementations of common training losses."""

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def cross_entropy_from_logits(
    logits: FloatArray,
    targets: Sequence[int] | NDArray[np.integer],
) -> float:
    """Return mean multiclass cross-entropy from unnormalized logits.

    Args:
        logits: Array with shape (batch_size, num_classes).
        targets: Integer class index for each row, shape (batch_size,).

    Raises:
        ValueError: If shapes are incompatible, the batch is empty, or targets are invalid.
    """
    if logits.ndim != 2:
        raise ValueError("logits must have shape (batch_size, num_classes)")
    if logits.shape[0] == 0 or logits.shape[1] == 0:
        raise ValueError("logits must have a non-empty batch and class dimension")

    target_array = np.asarray(targets)
    if target_array.ndim != 1 or target_array.shape[0] != logits.shape[0]:
        raise ValueError("targets must have shape (batch_size,)")
    if not np.issubdtype(target_array.dtype, np.integer):
        raise ValueError("targets must contain integer class indices")
    if np.any(target_array < 0) or np.any(target_array >= logits.shape[1]):
        raise ValueError("target class index is out of range")

    shifted = logits - np.max(logits, axis=1, keepdims=True)
    log_partition = np.log(np.exp(shifted).sum(axis=1))
    target_logits = shifted[np.arange(logits.shape[0]), target_array]
    return float(np.mean(log_partition - target_logits))


def cross_entropy_gradient(
    logits: FloatArray,
    targets: Sequence[int] | NDArray[np.integer],
) -> FloatArray:
    """Return the gradient of mean cross-entropy with respect to logits."""
    if logits.ndim != 2:
        raise ValueError("logits must have shape (batch_size, num_classes)")
    if logits.shape[0] == 0 or logits.shape[1] == 0:
        raise ValueError("logits must have a non-empty batch and class dimension")

    target_array = np.asarray(targets)
    if target_array.ndim != 1 or target_array.shape[0] != logits.shape[0]:
        raise ValueError("targets must have shape (batch_size,)")
    if not np.issubdtype(target_array.dtype, np.integer):
        raise ValueError("targets must contain integer class indices")
    if np.any(target_array < 0) or np.any(target_array >= logits.shape[1]):
        raise ValueError("target class index is out of range")

    shifted = logits - np.max(logits, axis=1, keepdims=True)
    probabilities = np.exp(shifted)
    probabilities /= probabilities.sum(axis=1, keepdims=True)
    probabilities[np.arange(logits.shape[0]), target_array] -= 1.0
    return probabilities / logits.shape[0]
