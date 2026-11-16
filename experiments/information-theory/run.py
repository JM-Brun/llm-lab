"""Run a deterministic entropy, cross-entropy, KL and coding example."""

import json

import numpy as np

from llm_lab.foundations.information_theory import (
    cross_entropy,
    ideal_code_lengths,
    kl_divergence,
    perplexity,
    shannon_entropy,
)


def main() -> None:
    target = np.array([0.5, 0.5], dtype=np.float64)
    predicted = np.array([0.75, 0.25], dtype=np.float64)
    one_hot = np.array([0.0, 1.0], dtype=np.float64)
    output = {
        "experiment": "synthetic-information-theory",
        "randomness": "none",
        "target_distribution": target.tolist(),
        "predicted_distribution": predicted.tolist(),
        "nats": {
            "target_entropy": shannon_entropy(target),
            "cross_entropy": cross_entropy(target, predicted),
            "kl_divergence": kl_divergence(target, predicted),
            "perplexity": perplexity(cross_entropy(target, predicted)),
        },
        "bits": {
            "target_entropy": shannon_entropy(target, base=2.0),
            "cross_entropy": cross_entropy(target, predicted, base=2.0),
            "kl_divergence": kl_divergence(target, predicted, base=2.0),
            "perplexity": perplexity(cross_entropy(target, predicted, base=2.0), base=2.0),
            "expected_ideal_code_length": cross_entropy(target, predicted, base=2.0),
            "ideal_code_lengths": ideal_code_lengths(predicted).tolist(),
        },
        "one_hot_target": {
            "observed_probability": float(predicted[1]),
            "cross_entropy": cross_entropy(one_hot, predicted),
            "negative_log_likelihood": float(-np.log(predicted[1])),
            "perplexity": perplexity(cross_entropy(one_hot, predicted)),
        },
        "identity_check": bool(
            np.isclose(
                cross_entropy(target, predicted),
                shannon_entropy(target) + kl_divergence(target, predicted),
            )
        ),
    }
    print(json.dumps(output, indent=2))  # noqa: T201 - experiment CLI output


if __name__ == "__main__":
    main()
