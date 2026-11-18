"""Small, reproducible tools for inspecting token embedding tables.

These NumPy helpers operate on a model's input embedding matrix. They do not
tokenize text, load checkpoints, or produce contextualized hidden states.
Token IDs remain the canonical row identities throughout lookup and ranking.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

FloatMatrix = NDArray[np.float64]
IntArray = NDArray[np.int64]


def _as_embedding_matrix(embedding_matrix: np.ndarray) -> FloatMatrix:
    """Validate and convert a vocabulary-by-dimension matrix to float64."""
    matrix = np.asarray(embedding_matrix)
    if matrix.ndim != 2 or min(matrix.shape, default=0) < 1:
        raise ValueError("embedding_matrix must be a non-empty 2D matrix")
    if not (np.issubdtype(matrix.dtype, np.integer) or np.issubdtype(matrix.dtype, np.floating)):
        raise ValueError("embedding_matrix must contain real numeric values")
    result = np.asarray(matrix, dtype=np.float64)
    if not np.isfinite(result).all():
        raise ValueError("embedding_matrix must contain only finite values")
    return result


def _as_token_ids(token_ids: np.ndarray | list[int], vocab_size: int) -> IntArray:
    """Validate token IDs and preserve their order and duplicates."""
    ids = np.asarray(token_ids)
    if ids.ndim != 1 or not np.issubdtype(ids.dtype, np.integer):
        raise ValueError("token_ids must be a one-dimensional sequence of integers")
    result = ids.astype(np.int64, copy=False)
    if np.any(result < 0) or np.any(result >= vocab_size):
        raise ValueError("token_ids must be within the embedding matrix row range")
    return result


def lookup_embedding_rows(
    embedding_matrix: np.ndarray,
    token_ids: np.ndarray | list[int],
) -> FloatMatrix:
    """Return input embedding rows for IDs, preserving order and duplicates.

    The returned array is a copy. No decoding or re-tokenization is involved.
    """
    matrix = _as_embedding_matrix(embedding_matrix)
    ids = _as_token_ids(token_ids, matrix.shape[0])
    return np.array(matrix[ids], dtype=np.float64, copy=True)


def cosine_top_k(
    embedding_matrix: np.ndarray,
    token_id: int,
    k: int,
    *,
    exclude_self: bool = True,
) -> tuple[IntArray, NDArray[np.float64]]:
    """Return k nearest non-zero rows by cosine similarity.

    Similarities are computed against the input embedding table, not
    contextualized states. The query row must have non-zero norm. Zero-norm
    candidates are excluded because cosine similarity is undefined for them.
    Ties are deterministic: lower token IDs come first. The query ID is
    excluded by default, and k must fit the remaining candidate set.
    """
    matrix = _as_embedding_matrix(embedding_matrix)
    ids = _as_token_ids(np.asarray([token_id]), matrix.shape[0])
    query_id = int(ids[0])
    if (
        isinstance(k, (bool, np.bool_))
        or not isinstance(k, (int, np.integer))
        or k < 1
    ):
        raise ValueError("k must be a positive integer")
    if not isinstance(exclude_self, bool):
        raise ValueError("exclude_self must be a boolean")

    # Scale each row before computing its norm. Direct sum-of-squares can
    # overflow for large finite values or underflow for tiny ones.
    scales = np.max(np.abs(matrix), axis=1)
    scaled = np.divide(
        matrix,
        scales[:, None],
        out=np.zeros_like(matrix),
        where=scales[:, None] > 0,
    )
    scaled_norms = np.sqrt(np.sum(scaled * scaled, axis=1))
    nonzero = scales > 0
    if not nonzero[query_id]:
        raise ValueError("the query embedding row must have non-zero norm")

    candidate_ids = np.flatnonzero(nonzero)
    if exclude_self:
        candidate_ids = candidate_ids[candidate_ids != query_id]
    if k > candidate_ids.size:
        raise ValueError("k exceeds the number of eligible non-zero candidate rows")

    normalized = np.divide(
        scaled,
        scaled_norms[:, None],
        out=np.zeros_like(scaled),
        where=scaled_norms[:, None] > 0,
    )
    normalized_query = normalized[query_id]
    normalized_candidates = normalized[candidate_ids]
    similarities = normalized_candidates @ normalized_query
    order = np.lexsort((candidate_ids, -similarities))[:k]
    return (
        np.asarray(candidate_ids[order], dtype=np.int64),
        np.asarray(similarities[order], dtype=np.float64),
    )
