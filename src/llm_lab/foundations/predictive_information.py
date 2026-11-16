"""Finite-family predictive V-information for exact discrete examples."""

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def predictive_v_information(
    joint: FloatArray,
    predictive_family: FloatArray,
    *,
    base: float = np.e,
) -> tuple[float, float, float]:
    """Return (V-entropy, conditional V-entropy, V-information).

    Each family member is a conditional prediction table: one probability
    vector over targets for each context. The family must include a constant
    predictor for every output distribution in any member (optional ignorance).

    This computes exact population risks for a finite, explicitly supplied
    family. It is not a fitted-model estimator.
    """
    if not np.isfinite(base) or base <= 1.0:
        raise ValueError("base must be finite and greater than one")
    probabilities = np.asarray(joint, dtype=np.float64)
    predictors = np.asarray(predictive_family, dtype=np.float64)

    if probabilities.ndim != 2 or min(probabilities.shape) == 0:
        raise ValueError("joint must be a non-empty 2D probability table")
    if not np.all(np.isfinite(probabilities)) or np.any(probabilities < 0.0):
        raise ValueError("joint must contain finite, non-negative values")
    if not np.isclose(probabilities.sum(), 1.0, rtol=1e-9, atol=1e-12):
        raise ValueError("joint must sum to one")
    if predictors.ndim != 3 or predictors.shape[1:] != probabilities.shape:
        raise ValueError("predictive_family must have shape (models, contexts, targets)")
    if predictors.shape[0] == 0:
        raise ValueError("predictive_family must contain at least one predictor")
    if not np.all(np.isfinite(predictors)) or np.any(predictors < 0.0):
        raise ValueError("predictors must contain finite, non-negative probabilities")
    if not np.allclose(predictors.sum(axis=2), 1.0, rtol=1e-9, atol=1e-12):
        raise ValueError("each predictor row must sum to one")

    constant_mask = np.all(
        np.isclose(predictors, predictors[:, :1, :], rtol=1e-9, atol=1e-12),
        axis=(1, 2),
    )
    if not np.any(constant_mask):
        raise ValueError("family must include at least one constant predictor")

    constant_tables = predictors[constant_mask, 0, :]
    for model in predictors:
        for row in model:
            if not any(
                np.allclose(row, candidate, rtol=1e-9, atol=1e-12) for candidate in constant_tables
            ):
                raise ValueError(
                    "family violates optional ignorance: add a constant predictor "
                    "for every output distribution"
                )

    with np.errstate(divide="ignore"):
        log_predictions = np.log(predictors) / np.log(base)
    weighted = np.zeros_like(predictors)
    positive_joint = probabilities > 0.0
    weighted[:, positive_joint] = (
        probabilities[positive_joint][None, :] * log_predictions[:, positive_joint]
    )
    conditional_risks = -weighted.sum(axis=(1, 2))
    conditional_v_entropy = float(np.min(conditional_risks))

    marginal_y = probabilities.sum(axis=0)
    constant_risks = []
    for prediction in constant_tables:
        positive = marginal_y > 0.0
        if np.any(prediction[positive] == 0.0):
            constant_risks.append(float("inf"))
        else:
            risk = -np.sum(marginal_y[positive] * np.log(prediction[positive])) / np.log(base)
            constant_risks.append(float(risk))
    v_entropy = float(min(constant_risks))
    if not np.isfinite(v_entropy):
        raise ValueError("family must provide a finite baseline log-loss on the target support")
    information = max(0.0, v_entropy - conditional_v_entropy)
    return v_entropy, conditional_v_entropy, information
