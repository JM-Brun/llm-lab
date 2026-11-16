"""Tests for discrete information-theory quantities."""

import numpy as np
import pytest

from llm_lab.foundations.information_theory import (
    cross_entropy,
    ideal_code_lengths,
    kl_divergence,
    mutual_information,
    perplexity,
    shannon_entropy,
)


def test_cross_entropy_decomposes_into_entropy_and_kl() -> None:
    target = np.array([0.5, 0.5])
    predicted = np.array([0.75, 0.25])
    assert cross_entropy(target, predicted) == pytest.approx(
        shannon_entropy(target) + kl_divergence(target, predicted)
    )


def test_known_example_in_nats_and_bits() -> None:
    target = np.array([0.5, 0.5])
    predicted = np.array([0.75, 0.25])
    assert shannon_entropy(target) == pytest.approx(np.log(2.0))
    assert shannon_entropy(target, base=2.0) == pytest.approx(1.0)
    assert cross_entropy(target, predicted) == pytest.approx(0.8369882168)
    assert kl_divergence(target, predicted) == pytest.approx(0.1438410362)


def test_one_hot_target_cross_entropy_is_token_nll() -> None:
    target = np.array([0.0, 1.0, 0.0])
    predicted = np.array([0.2, 0.3, 0.5])
    assert cross_entropy(target, predicted) == pytest.approx(-np.log(0.3))
    assert shannon_entropy(target) == pytest.approx(0.0)


def test_zero_target_mass_is_ignored_but_missing_support_is_infinite() -> None:
    assert cross_entropy(np.array([1.0, 0.0]), np.array([1.0, 0.0])) == 0.0
    assert np.isinf(cross_entropy(np.array([0.5, 0.5]), np.array([1.0, 0.0])))


def test_ideal_code_lengths_and_perplexity() -> None:
    probabilities = np.array([0.5, 0.25, 0.25])
    np.testing.assert_allclose(ideal_code_lengths(probabilities), [1.0, 2.0, 2.0])
    assert perplexity(np.log(4.0)) == pytest.approx(4.0)
    assert perplexity(2.0, base=2.0) == pytest.approx(4.0)


def test_mutual_information_is_zero_for_independent_variables() -> None:
    joint = np.array([[0.25, 0.25], [0.25, 0.25]])
    assert mutual_information(joint, base=2.0) == pytest.approx(0.0)


def test_mutual_information_of_perfectly_correlated_bits_is_one_bit() -> None:
    joint = np.array([[0.5, 0.0], [0.0, 0.5]])
    assert mutual_information(joint, base=2.0) == pytest.approx(1.0)


@pytest.mark.parametrize(
    "joint",
    [
        np.array([0.5, 0.5]),
        np.array([[0.2, 0.2], [0.2, 0.2]]),
        np.array([[0.5, -0.1], [0.1, 0.5]]),
        np.array([[np.nan, 0.0], [0.0, 1.0]]),
    ],
)
def test_mutual_information_rejects_invalid_joint_tables(joint: np.ndarray) -> None:
    with pytest.raises(ValueError):
        mutual_information(joint)


@pytest.mark.parametrize(
    "probabilities",
    [
        np.array([]),
        np.array([[0.5, 0.5]]),
        np.array([0.2, 0.2]),
        np.array([-0.1, 1.1]),
        np.array([np.nan, np.nan]),
    ],
)
def test_invalid_distributions_are_rejected(probabilities: np.ndarray) -> None:
    with pytest.raises(ValueError):
        shannon_entropy(probabilities)


def test_mismatched_shapes_are_rejected() -> None:
    with pytest.raises(ValueError):
        cross_entropy(np.array([1.0, 0.0]), np.array([1.0]))


def test_invalid_log_bases_are_rejected() -> None:
    with pytest.raises(ValueError):
        shannon_entropy(np.array([0.5, 0.5]), base=1.0)


@pytest.mark.parametrize("metric", ["entropy", "cross_entropy", "kl", "perplexity", "code_lengths"])
def test_invalid_log_bases_are_rejected_by_every_metric(metric: str) -> None:
    probabilities = np.array([0.5, 0.5])
    with pytest.raises(ValueError):
        if metric == "entropy":
            shannon_entropy(probabilities, base=1.0)
        elif metric == "cross_entropy":
            cross_entropy(probabilities, probabilities, base=1.0)
        elif metric == "kl":
            kl_divergence(probabilities, probabilities, base=1.0)
        elif metric == "perplexity":
            perplexity(0.5, base=1.0)
        else:
            ideal_code_lengths(probabilities, base=1.0)


def test_kl_support_and_shape_edge_cases() -> None:
    assert np.isinf(kl_divergence(np.array([0.5, 0.5]), np.array([1.0, 0.0])))
    with pytest.raises(ValueError):
        kl_divergence(np.array([1.0, 0.0]), np.array([1.0]))


def test_perplexity_rejects_negative_or_non_finite_nll() -> None:
    with pytest.raises(ValueError):
        perplexity(-0.1)
    with pytest.raises(ValueError):
        perplexity(float("inf"))


def test_zero_probability_has_infinite_ideal_code_length() -> None:
    lengths = ideal_code_lengths(np.array([1.0, 0.0]))
    assert lengths[0] == 0.0
    assert np.isinf(lengths[1])
