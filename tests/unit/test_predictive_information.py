"""Tests for finite-family predictive V-information."""

import numpy as np
import pytest

from llm_lab.foundations.predictive_information import predictive_v_information


def _predictors_with_signal() -> np.ndarray:
    constants = np.array(
        [
            [[0.9, 0.1], [0.9, 0.1]],
            [[0.5, 0.5], [0.5, 0.5]],
            [[0.1, 0.9], [0.1, 0.9]],
        ]
    )
    uses_feature = np.array([[[0.9, 0.1], [0.1, 0.9]]])
    return np.concatenate([constants, uses_feature], axis=0)


def test_correlated_feature_has_positive_predictive_v_information() -> None:
    joint = np.array([[0.45, 0.05], [0.05, 0.45]])
    baseline, conditional, information = predictive_v_information(
        joint, _predictors_with_signal(), base=2.0
    )
    assert baseline == pytest.approx(1.0)
    assert conditional == pytest.approx(
        -0.9 * np.log2(0.9) - 0.1 * np.log2(0.1)
    )
    assert information == pytest.approx(0.5310044064)


def test_independent_feature_has_zero_predictive_v_information() -> None:
    joint = np.full((2, 2), 0.25)
    baseline, conditional, information = predictive_v_information(
        joint, _predictors_with_signal(), base=2.0
    )
    assert baseline == pytest.approx(1.0)
    assert conditional == pytest.approx(1.0)
    assert information == pytest.approx(0.0)


def test_constant_only_family_has_zero_information_even_for_correlated_data() -> None:
    joint = np.array([[0.45, 0.05], [0.05, 0.45]])
    constant_only = np.array([[[0.5, 0.5], [0.5, 0.5]]])
    _, _, information = predictive_v_information(joint, constant_only, base=2.0)
    assert information == pytest.approx(0.0)


def test_optional_ignorance_requires_constant_versions_of_outputs() -> None:
    joint = np.array([[0.45, 0.05], [0.05, 0.45]])
    invalid_family = np.array(
        [
            [[0.5, 0.5], [0.5, 0.5]],
            [[0.9, 0.1], [0.1, 0.9]],
        ]
    )
    with pytest.raises(ValueError, match="optional ignorance"):
        predictive_v_information(joint, invalid_family)


def test_invalid_joint_distribution_is_rejected() -> None:
    predictors = np.array([[[0.5, 0.5], [0.5, 0.5]]])
    with pytest.raises(ValueError, match="sum to one"):
        predictive_v_information(np.array([[0.2, 0.2], [0.2, 0.2]]), predictors)



def test_invalid_logarithm_base_is_rejected() -> None:
    joint = np.full((2, 2), 0.25)
    with pytest.raises(ValueError, match="base"):
        predictive_v_information(joint, _predictors_with_signal(), base=1.0)


@pytest.mark.parametrize(
    "joint",
    [
        np.array([0.5, 0.5]),
        np.array([[0.5, -0.1], [0.1, 0.5]]),
        np.array([[np.nan, 0.0], [0.0, 1.0]]),
    ],
)
def test_invalid_joint_shapes_and_values_are_rejected(joint: np.ndarray) -> None:
    with pytest.raises(ValueError):
        predictive_v_information(joint, _predictors_with_signal())


@pytest.mark.parametrize(
    "family",
    [
        np.array([[0.5, 0.5]]),
        np.empty((0, 2, 2)),
        np.array([[[0.5, 0.5], [0.5, -0.5]]]),
        np.array([[[0.5, 0.5], [0.4, 0.4]]]),
        np.array([[[np.nan, 0.0], [0.5, 0.5]]]),
    ],
)
def test_invalid_predictive_families_are_rejected(family: np.ndarray) -> None:
    with pytest.raises(ValueError):
        predictive_v_information(np.full((2, 2), 0.25), family)


def test_family_without_constant_predictor_is_rejected() -> None:
    joint = np.array([[0.45, 0.05], [0.05, 0.45]])
    only_contextual = np.array([[[0.9, 0.1], [0.1, 0.9]]])
    with pytest.raises(ValueError, match="constant predictor"):
        predictive_v_information(joint, only_contextual)


def test_family_without_finite_baseline_support_is_rejected() -> None:
    joint = np.array([[0.45, 0.05], [0.05, 0.45]])
    impossible = np.array([[[1.0, 0.0], [1.0, 0.0]]])
    with pytest.raises(ValueError, match="finite baseline"):
        predictive_v_information(joint, impossible)
