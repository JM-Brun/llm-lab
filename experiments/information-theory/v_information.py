"""Run an exact toy example of predictive V-information."""

import json

import numpy as np

from llm_lab.foundations.predictive_information import predictive_v_information


def candidate_family() -> np.ndarray:
    """Finite predictive family with optional-ignorance constant functions."""
    constants = np.array(
        [
            [[0.9, 0.1], [0.9, 0.1]],
            [[0.5, 0.5], [0.5, 0.5]],
            [[0.1, 0.9], [0.1, 0.9]],
        ],
        dtype=np.float64,
    )
    feature_rule = np.array([[[0.9, 0.1], [0.1, 0.9]]], dtype=np.float64)
    return np.concatenate([constants, feature_rule], axis=0)


def main() -> None:
    # X predicts Y correctly with probability 0.9.
    correlated_joint = np.array([[0.45, 0.05], [0.05, 0.45]])
    # Z is balanced and independent of Y.
    independent_joint = np.full((2, 2), 0.25)
    family = candidate_family()

    correlated = predictive_v_information(correlated_joint, family, base=2.0)
    independent = predictive_v_information(independent_joint, family, base=2.0)
    constant_only = predictive_v_information(
        correlated_joint,
        np.array([[[0.5, 0.5], [0.5, 0.5]]], dtype=np.float64),
        base=2.0,
    )

    output = {
        "experiment": "finite-predictive-v-information",
        "randomness": "none",
        "logarithm_base": 2,
        "predictive_family": {
            "description": (
                "Finite family containing three constant Bernoulli predictors "
                "and one context-dependent rule; every output distribution has "
                "a corresponding constant predictor (optional ignorance)."
            ),
            "candidate_probabilities_for_y1": [0.1, 0.5, 0.9],
            "feature_rule": {"x0": 0.1, "x1": 0.9},
        },
        "correlated_feature": {
            "joint_distribution": correlated_joint.tolist(),
            "v_entropy_bits": correlated[0],
            "conditional_v_entropy_bits": correlated[1],
            "predictive_v_information_bits": correlated[2],
        },
        "independent_feature": {
            "joint_distribution": independent_joint.tolist(),
            "v_entropy_bits": independent[0],
            "conditional_v_entropy_bits": independent[1],
            "predictive_v_information_bits": independent[2],
        },
        "constant_only_family_on_correlated_data": {
            "predictive_v_information_bits": constant_only[2],
        },
        "interpretation": [
            "The same correlated data yields zero V-information for a constant-only observer.",
            "A finite family that can exploit the feature obtains about 0.531 bits.",
            "An independent feature provides no predictive improvement in this family.",
            "This is an exact population calculation for a toy finite family, not a fitted LLM or a benchmark of attention against bag-of-words.",
        ],
    }
    print(json.dumps(output, indent=2))  # noqa: T201 - experiment CLI output


if __name__ == "__main__":
    main()
