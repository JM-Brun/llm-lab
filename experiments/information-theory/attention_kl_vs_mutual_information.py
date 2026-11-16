"""Contrast row-to-uniform KL with mutual information in a toy attention table."""

import json
from collections.abc import Iterable

import numpy as np

from llm_lab.foundations.information_theory import kl_divergence, mutual_information


def mean_row_kl_to_uniform(rows: np.ndarray, context_probabilities: np.ndarray) -> float:
    """Average KL(row || uniform keys); this measures row concentration."""
    uniform = np.full(rows.shape[1], 1.0 / rows.shape[1])
    return float(
        sum(
            weight * kl_divergence(row, uniform, base=2.0)
            for weight, row in zip(context_probabilities, rows, strict=True)
        )
    )


def joint_from_conditionals(
    context_probabilities: np.ndarray, conditional_rows: np.ndarray
) -> np.ndarray:
    """Build P(context, key) from P(context) and P(key | context)."""
    return context_probabilities[:, None] * conditional_rows


def describe_case(rows: np.ndarray, context_probabilities: np.ndarray) -> dict[str, float]:
    joint = joint_from_conditionals(context_probabilities, rows)
    return {
        "mean_row_kl_to_uniform_bits": mean_row_kl_to_uniform(rows, context_probabilities),
        "mutual_information_bits": mutual_information(joint, base=2.0),
        "mean_row_kl_to_marginal_bits": weighted_expectation(
            weight * kl_divergence(row, joint.sum(axis=0), base=2.0)
            for weight, row in zip(context_probabilities, rows, strict=True)
        ),
    }


def weighted_expectation(values: Iterable[float]) -> float:
    """Sum already-weighted values to form a finite expectation."""
    return float(sum(values))


def main() -> None:
    context_probabilities = np.array([0.5, 0.5], dtype=np.float64)
    repeated_rows = np.array([[0.9, 0.1], [0.9, 0.1]], dtype=np.float64)
    contrasting_rows = np.array([[0.9, 0.1], [0.1, 0.9]], dtype=np.float64)

    output = {
        "experiment": "attention-row-kl-is-not-mutual-information",
        "logarithm_base": 2,
        "context_probabilities": context_probabilities.tolist(),
        "same_non_uniform_row_for_every_context": describe_case(
            repeated_rows, context_probabilities
        ),
        "opposite_rows_with_balanced_contexts": describe_case(
            contrasting_rows, context_probabilities
        ),
        "interpretation": [
            "A non-uniform row can have positive KL to uniform even when every context has the same row; then context and key are independent and mutual information is zero.",
            "For a genuine joint distribution, mutual information equals the context-weighted KL from each conditional key distribution to the marginal key distribution.",
            "Attention weights are not automatically calibrated conditional probabilities P(key | query); the identity applies only when a valid joint distribution and its conditionals have been specified.",
            "The numerical equality in the contrasting toy case is incidental: KL-to-uniform and mutual information use different reference distributions.",
        ],
    }
    print(json.dumps(output, indent=2))  # noqa: T201 - experiment CLI output


if __name__ == "__main__":
    main()
