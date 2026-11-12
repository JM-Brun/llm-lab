"""Tests for model-independent input-embedding inspection helpers."""

import numpy as np
import pytest

from llm_lab.foundations.embedding_inspection import cosine_top_k, lookup_embedding_rows


def test_lookup_preserves_id_order_and_duplicates() -> None:
    matrix = np.array([[1, 0], [0, 2], [-1, 0]], dtype=np.float32)
    rows = lookup_embedding_rows(matrix, [2, 0, 2])
    np.testing.assert_array_equal(rows, [[-1, 0], [1, 0], [-1, 0]])
    assert rows.dtype == np.float64
    rows[0, 0] = 99
    assert matrix[2, 0] == -1


def test_cosine_top_k_returns_ids_and_descending_scores() -> None:
    matrix = np.array([[1, 0], [0.8, 0.6], [-1, 0], [0, 1]], dtype=np.float64)
    ids, scores = cosine_top_k(matrix, token_id=0, k=2)
    np.testing.assert_array_equal(ids, [1, 3])
    np.testing.assert_allclose(scores, [0.8, 0.0])


def test_cosine_top_k_excludes_self_and_breaks_ties_by_id() -> None:
    matrix = np.array([[1, 0], [0, 1], [0, -1], [-1, 0]], dtype=np.float64)
    ids, scores = cosine_top_k(matrix, token_id=0, k=2)
    np.testing.assert_array_equal(ids, [1, 2])
    np.testing.assert_allclose(scores, [0.0, 0.0])


def test_cosine_top_k_can_include_self_explicitly() -> None:
    matrix = np.eye(3, dtype=np.float64)
    ids, scores = cosine_top_k(matrix, token_id=1, k=2, exclude_self=False)
    np.testing.assert_array_equal(ids, [1, 0])
    np.testing.assert_allclose(scores, [1.0, 0.0])


@pytest.mark.parametrize(
    ("matrix", "token_ids"),
    [
        (np.array([1.0, 2.0]), [0]),
        (np.empty((0, 2)), [0]),
        (np.array([[1.0, np.nan]]), [0]),
        (np.array([[1 + 2j, 0]]), [0]),
        (np.array([[1.0, 0.0]]), [-1]),
        (np.array([[1.0, 0.0]]), [1]),
        (np.array([[1.0, 0.0]]), [0.5]),
        (np.array([[1.0, 0.0]]), [[0]]),
    ],
)
def test_lookup_rejects_invalid_matrix_or_ids(
    matrix: np.ndarray, token_ids: list[int] | np.ndarray
) -> None:
    with pytest.raises(ValueError):
        lookup_embedding_rows(matrix, token_ids)


@pytest.mark.parametrize(
    ("matrix", "token_id", "k", "message"),
    [
        (np.array([[0.0, 0.0], [1.0, 0.0]]), 0, 1, "query embedding"),
        (np.array([[1.0, 0.0]]), 0, 1, "eligible"),
        (np.array([[1.0, 0.0], [0.0, 1.0]]), 0, 0, "positive integer"),
        (np.array([[1.0, 0.0], [0.0, 1.0]]), 0, True, "positive integer"),
        (np.array([[1.0, 0.0], [0.0, 1.0]]), 2, 1, "row range"),
    ],
)
def test_cosine_top_k_rejects_undefined_or_invalid_requests(
    matrix: np.ndarray, token_id: int, k: int, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        cosine_top_k(matrix, token_id, k)


def test_cosine_top_k_excludes_zero_norm_candidates() -> None:
    matrix = np.array([[1.0, 0.0], [0.0, 0.0], [0.0, 1.0]])
    ids, scores = cosine_top_k(matrix, token_id=0, k=1)
    np.testing.assert_array_equal(ids, [2])
    np.testing.assert_allclose(scores, [0.0])
