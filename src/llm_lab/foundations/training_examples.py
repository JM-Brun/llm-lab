"""Reference construction of autoregressive training examples.

This module turns a flat stream of token IDs into aligned input/target
windows for next-token prediction. It implements the one-token shift and
the sliding-window policy of the training-examples lesson. It does not
implement corpus loading, tokenization, packing, padding or loss masks.
"""

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

IntArray = NDArray[np.int64]


def sliding_input_target_pairs(
    token_ids: Sequence[int] | NDArray[np.integer],
    context_length: int,
    stride: int = 1,
) -> tuple[IntArray, IntArray]:
    """Return aligned input/target windows for next-token prediction.

    Window `k` starts at position `k * stride` in the stream. Its input is
    `token_ids[start : start + context_length]` and its target is the same
    window shifted one position to the right, so every position must predict
    the token that follows it. A window is kept only when its target is
    complete: the last corpus token is never used as an input whose target is
    missing, and no padding or end-of-stream token is invented.

    Args:
        token_ids: One-dimensional stream of integer token IDs.
        context_length: Number of input positions per window; must be at least 1.
        stride: Offset between the starts of consecutive windows; must be at least 1.

    Returns:
        Tuple `(inputs, targets)` of integer arrays with shape
        `(num_windows, context_length)`, where
        `num_windows = 1 + (len(token_ids) - context_length - 1) // stride`.

    Raises:
        ValueError: If `token_ids` is not a one-dimensional integer sequence,
            if it holds fewer than `context_length + 1` tokens, or if
            `context_length` or `stride` is below one.
    """
    if context_length < 1:
        raise ValueError("context_length must be at least 1")
    if stride < 1:
        raise ValueError("stride must be at least 1")

    ids = np.asarray(token_ids)
    if ids.ndim != 1:
        raise ValueError("token_ids must be a one-dimensional stream of token IDs")
    if not np.issubdtype(ids.dtype, np.integer):
        raise ValueError("token_ids must contain integer token IDs")
    if ids.shape[0] < context_length + 1:
        raise ValueError(
            "token_ids must contain at least context_length + 1 tokens to build "
            "one complete input/target example"
        )

    stream = ids.astype(np.int64, copy=False)
    num_windows = 1 + (stream.shape[0] - context_length - 1) // stride
    inputs: IntArray = np.empty((num_windows, context_length), dtype=np.int64)
    targets: IntArray = np.empty((num_windows, context_length), dtype=np.int64)

    for window in range(num_windows):
        start = window * stride
        inputs[window] = stream[start : start + context_length]
        targets[window] = stream[start + 1 : start + context_length + 1]

    return inputs, targets
