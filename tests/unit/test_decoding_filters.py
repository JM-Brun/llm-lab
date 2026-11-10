"""Tests for the top-k and top-p truncation filters."""

import numpy as np
import pytest

from llm_lab.foundations.attention import softmax_with_temperature
from llm_lab.foundations.decoding_filters import top_k_filter, top_p_filter


def test_top_k_with_k_one_matches_greedy_selection() -> None:
    probabilities = np.array([0.1, 0.55, 0.05, 0.3], dtype=np.float64)

    filtered = top_k_filter(probabilities, k=1)

    np.testing.assert_allclose(filtered, [0.0, 1.0, 0.0, 0.0])


def test_top_k_keeps_exactly_k_renormalized_candidates() -> None:
    probabilities = np.array([0.4, 0.1, 0.3, 0.2], dtype=np.float64)

    filtered = top_k_filter(probabilities, k=2)

    np.testing.assert_allclose(filtered, [0.4 / 0.7, 0.0, 0.3 / 0.7, 0.0])
    assert filtered.sum() == pytest.approx(1.0)
    assert int((filtered > 0).sum()) == 2


def test_top_k_with_k_at_least_vocabulary_is_identity_copy() -> None:
    probabilities = np.array([0.2, 0.3, 0.5], dtype=np.float64)

    filtered = top_k_filter(probabilities, k=3)

    np.testing.assert_array_equal(filtered, probabilities)
    filtered[0] = 0.9
    assert probabilities[0] == pytest.approx(0.2)


def test_top_k_breaks_ties_by_lowest_index_deterministically() -> None:
    probabilities = np.array([0.25, 0.25, 0.25, 0.25], dtype=np.float64)

    filtered = top_k_filter(probabilities, k=2)

    np.testing.assert_allclose(filtered, [0.5, 0.5, 0.0, 0.0])
    np.testing.assert_array_equal(top_k_filter(probabilities, 2), filtered)


def test_top_p_includes_the_token_that_crosses_the_threshold() -> None:
    probabilities = np.array([0.5, 0.3, 0.2], dtype=np.float64)

    # 0.5 < 0.7 <= 0.5 + 0.3: the crossing entry (0.3) must be kept.
    filtered = top_p_filter(probabilities, p=0.7)
    np.testing.assert_allclose(filtered, [0.5 / 0.8, 0.3 / 0.8, 0.0])

    # A threshold exactly reached by a prefix keeps that prefix only.
    exact = top_p_filter(np.array([0.5, 0.25, 0.25], dtype=np.float64), p=0.75)
    np.testing.assert_allclose(exact, [2.0 / 3.0, 1.0 / 3.0, 0.0])

    single = top_p_filter(probabilities, p=0.5)
    np.testing.assert_allclose(single, [1.0, 0.0, 0.0])


def test_top_p_nucleus_size_adapts_to_distribution_shape() -> None:
    concentrated = np.array([0.8, 0.1, 0.05, 0.05], dtype=np.float64)
    diffuse = np.array([0.3, 0.25, 0.25, 0.2], dtype=np.float64)

    concentrated_filtered = top_p_filter(concentrated, p=0.9)
    diffuse_filtered = top_p_filter(diffuse, p=0.9)

    assert int((concentrated_filtered > 0).sum()) == 2
    assert int((diffuse_filtered > 0).sum()) == 4


def test_top_p_with_p_equal_to_one_is_identity_copy() -> None:
    probabilities = np.array([0.6, 0.4], dtype=np.float64)

    filtered = top_p_filter(probabilities, p=1.0)

    np.testing.assert_array_equal(filtered, probabilities)
    filtered[0] = 0.2
    assert probabilities[0] == pytest.approx(0.6)


def test_top_p_breaks_ties_by_lowest_index() -> None:
    probabilities = np.array([0.4, 0.4, 0.2], dtype=np.float64)

    filtered = top_p_filter(probabilities, p=0.5)

    np.testing.assert_allclose(filtered, [0.5, 0.5, 0.0])


def test_temperature_before_filtering_changes_the_nucleus() -> None:
    logits = np.array([2.0, 1.5, 1.0, 0.5], dtype=np.float64)

    sharp = top_p_filter(softmax_with_temperature(logits, temperature=0.5), p=0.8)
    flat = top_p_filter(softmax_with_temperature(logits, temperature=5.0), p=0.8)

    # A lower temperature concentrates the distribution, so fewer candidates
    # reach the same target mass. Processing order matters.
    assert int((sharp > 0).sum()) <= int((flat > 0).sum())
    assert sharp.sum() == pytest.approx(1.0)
    assert flat.sum() == pytest.approx(1.0)


def test_filters_do_not_mutate_the_input() -> None:
    probabilities = np.array([0.4, 0.35, 0.25], dtype=np.float64)
    original = probabilities.copy()

    top_k_filter(probabilities, k=2)
    top_p_filter(probabilities, p=0.7)

    np.testing.assert_array_equal(probabilities, original)


@pytest.mark.parametrize("k", [0, -1])
def test_top_k_invalid_k_raises(k: int) -> None:
    with pytest.raises(ValueError):
        top_k_filter(np.array([0.5, 0.5]), k)


@pytest.mark.parametrize("p", [0.0, -0.5, 1.5])
def test_top_p_invalid_p_raises(p: float) -> None:
    with pytest.raises(ValueError):
        top_p_filter(np.array([0.5, 0.5]), p)


@pytest.mark.parametrize(
    "probabilities",
    [
        np.array([], dtype=np.float64),
        np.array([[0.5, 0.5]]),
        np.array([0.6, 0.6]),
        np.array([-0.5, 1.5]),
        np.array([np.nan, 1.0]),
        np.array([np.inf, 0.0]),
    ],
)
def test_invalid_distributions_raise_value_error(probabilities: np.ndarray) -> None:
    with pytest.raises(ValueError):
        top_k_filter(probabilities, k=1)
    with pytest.raises(ValueError):
        top_p_filter(probabilities, p=0.5)
