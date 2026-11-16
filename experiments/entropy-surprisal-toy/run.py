#!/usr/bin/env python3
"""Show why predictive entropy is not the surprisal of an observed event.

This is a mathematical toy example, not an LLM or token-pruning benchmark.
Uses only the Python standard library.
"""

from __future__ import annotations

import math
import sys


def entropy_bits(probabilities: tuple[float, ...]) -> float:
    if not probabilities:
        raise ValueError("at least one probability is required")
    if any(not math.isfinite(p) or p < 0.0 or p > 1.0 for p in probabilities):
        raise ValueError("probabilities must be finite values in [0, 1]")
    if not math.isclose(sum(probabilities), 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError("probabilities must sum to 1")
    return -sum(p * math.log2(p) for p in probabilities if p > 0.0)


def surprisal_bits(probability: float) -> float:
    if not 0.0 < probability <= 1.0:
        raise ValueError("probability must be in (0, 1]")
    return -math.log2(probability)


def main() -> None:
    probabilities = (0.99, 0.01)
    entropy = entropy_bits(probabilities)
    common_surprisal = surprisal_bits(probabilities[0])
    rare_surprisal = surprisal_bits(probabilities[1])

    lines = (
        "Entropy vs. realized surprisal — binary toy example",
        f"P(A) = {probabilities[0]:.2f}",
        f"P(B) = {probabilities[1]:.2f}",
        f"Predictive entropy = {entropy:.6f} bits per draw",
        f"Surprisal if A occurs = {common_surprisal:.6f} bits",
        f"Surprisal if B occurs = {rare_surprisal:.6f} bits",
        "The source has low average entropy, yet B is highly surprising.",
        "This does not measure token usefulness or justify pruning.",
    )
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
