"""Tests for the reference loss implementation."""

import numpy as np
import pytest

from llm_lab.foundations.losses import cross_entropy_from_logits, cross_entropy_gradient


def test_cross_entropy_matches_known_value() -> None:
    logits = np.array([[2.0, 0.0]], dtype=np.float64)
    targets = np.array([0], dtype=np.int64)

    loss = cross_entropy_from_logits(logits, targets)

    assert loss == pytest.approx(np.log1p(np.exp(-2.0)))


def test_gradient_matches_central_finite_differences() -> None:
    logits = np.array([[0.2, -0.4, 1.1], [1.0, 0.0, -0.5]], dtype=np.float64)
    targets = np.array([2, 0], dtype=np.int64)
    analytical = cross_entropy_gradient(logits, targets)
    epsilon = 1e-6
    numerical = np.zeros_like(logits)

    for row in range(logits.shape[0]):
        for column in range(logits.shape[1]):
            plus = logits.copy()
            minus = logits.copy()
            plus[row, column] += epsilon
            minus[row, column] -= epsilon
            numerical[row, column] = (
                cross_entropy_from_logits(plus, targets)
                - cross_entropy_from_logits(minus, targets)
            ) / (2 * epsilon)

    np.testing.assert_allclose(analytical, numerical, rtol=1e-5, atol=1e-7)


def test_loss_is_stable_for_large_logits() -> None:
    logits = np.array([[10000.0, 9999.0, 9998.0]], dtype=np.float64)
    loss = cross_entropy_from_logits(logits, np.array([0], dtype=np.int64))

    assert np.isfinite(loss)
    assert loss >= 0.0


@pytest.mark.parametrize(
    ("logits", "targets"),
    [
        (np.zeros(3), np.array([0])),
        (np.zeros((0, 3)), np.array([], dtype=np.int64)),
        (np.zeros((2, 3)), np.array([0])),
        (np.zeros((1, 3)), np.array([3])),
        (np.zeros((1, 3)), np.array([-1])),
        (np.zeros((1, 3)), np.array([0.5])),
    ],
)
def test_invalid_inputs_raise_value_error(
    logits: np.ndarray,
    targets: np.ndarray,
) -> None:
    with pytest.raises(ValueError):
        cross_entropy_from_logits(logits, targets)
