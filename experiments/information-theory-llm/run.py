#!/usr/bin/env python3
"""Small information-theory calculations for synthetic categorical distributions."""

from __future__ import annotations

import sys
from math import log2

EPSILON = 1e-12


def entropy(distribution: tuple[float, ...]) -> float:
    if any(p < 0 for p in distribution) or abs(sum(distribution) - 1.0) > EPSILON:
        raise ValueError("Distribution must be non-negative and sum to one")
    return -sum(p * log2(p) for p in distribution if p > 0)


def cross_entropy(target: tuple[float, ...], model: tuple[float, ...]) -> float:
    if len(target) != len(model):
        raise ValueError("Distributions must have the same support")
    if any(p < 0 for p in model) or abs(sum(model) - 1.0) > EPSILON:
        raise ValueError("Model distribution must sum to one")
    if any(p > 0 and q == 0 for p, q in zip(target, model, strict=True)):
        return float("inf")
    return -sum(p * log2(q) for p, q in zip(target, model, strict=True) if p > 0)


def kl_divergence(target: tuple[float, ...], model: tuple[float, ...]) -> float:
    return cross_entropy(target, model) - entropy(target)


def mutual_information(joint: tuple[tuple[float, ...], ...]) -> float:
    rows, columns = len(joint), len(joint[0])
    if any(len(row) != columns for row in joint):
        raise ValueError("Joint distribution must be rectangular")
    if any(p < 0 for row in joint for p in row):
        raise ValueError("Joint probabilities must be non-negative")
    if abs(sum(sum(row) for row in joint) - 1.0) > EPSILON:
        raise ValueError("Joint probabilities must sum to one")
    px = tuple(sum(joint[i]) for i in range(rows))
    py = tuple(sum(joint[i][j] for i in range(rows)) for j in range(columns))
    return sum(
        joint[i][j] * log2(joint[i][j] / (px[i] * py[j]))
        for i in range(rows)
        for j in range(columns)
        if joint[i][j] > 0
    )



def xor_demo() -> dict[str, float]:
    """Exact balanced-XOR illustration of predictive-family dependence.

    Both toy families can ignore the input (optional ignorance). The richer
    family additionally contains a predictor assigning probability 0.9 to
    the correct XOR label for each input pair.
    """
    baseline_cross_entropy = 1.0
    constant_conditional_cross_entropy = 1.0
    interaction_conditional_cross_entropy = -log2(0.9)
    return {
        "shannon_mi": 1.0,
        "constant_family": baseline_cross_entropy - constant_conditional_cross_entropy,
        "interaction_family": baseline_cross_entropy - interaction_conditional_cross_entropy,
    }


def main() -> None:
    target = (0.75, 0.25)
    models = (("good", (0.70, 0.30)), ("uniform", (0.50, 0.50)))
    h_target = entropy(target)
    demo = xor_demo()
    lines = []
    for label, model in models:
        h_cross = cross_entropy(target, model)
        kl = kl_divergence(target, model)
        assert abs(h_cross - h_target - kl) < EPSILON
        lines.append(f"{label:7s} cross-entropy: {h_cross:.4f} bits; KL: {kl:.4f} bits")
    joint = ((0.4, 0.1), (0.1, 0.4))
    lines.extend(
        (
            f"target entropy: {h_target:.4f} bits",
            f"mutual information of toy joint distribution: {mutual_information(joint):.4f} bits",
            "Reminder: attention weights are not mutual information.",
            f"Shannon MI for balanced XOR: {demo['shannon_mi']:.4f} bits",
            f"V-information, constant-only family: {demo['constant_family']:.4f} bits",
            f"V-information, interaction-aware family: {demo['interaction_family']:.4f} bits",
        )
    )
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
