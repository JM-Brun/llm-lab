"""Compare unigram and bigram predictive compression on ordered vs permuted data.

This is a teaching toy. It is not an epiplexity estimator or an LLM benchmark.
"""
from __future__ import annotations

import math
import random
from collections import Counter, defaultdict

ALPHABET = ("A", "B", "C", "D")
SEQUENCE_LENGTH = 2400
TRAIN_FRACTION = 0.75
ALPHA = 0.5
SEEDS = (7, 19, 41, 73, 101)


def make_sequence(length: int) -> str:
    """A simple cyclic grammar with a small deterministic exception pattern."""
    base = "AABACADAB"
    return (base * ((length + len(base) - 1) // len(base)))[:length]


def split_sequence(sequence: str) -> tuple[str, str]:
    boundary = int(len(sequence) * TRAIN_FRACTION)
    return sequence[:boundary], sequence[boundary:]


def permute_preserving_marginals(sequence: str, seed: int) -> str:
    symbols = list(sequence)
    random.Random(seed).shuffle(symbols)
    return "".join(symbols)


def unigram_cross_entropy(train: str, test: str) -> float:
    counts = Counter(train)
    total = len(train) + ALPHA * len(ALPHABET)
    return -sum(math.log2((counts.get(symbol, 0) + ALPHA) / total) for symbol in test) / len(test)


def bigram_cross_entropy(train: str, test: str) -> float:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    for left, right in zip(train, train[1:]):
        counts[left][right] += 1

    totals = {left: sum(row.values()) for left, row in counts.items()}
    previous = train[-1]
    loss = 0.0
    for symbol in test:
        denominator = totals.get(previous, 0) + ALPHA * len(ALPHABET)
        probability = (counts[previous].get(symbol, 0) + ALPHA) / denominator
        loss -= math.log2(probability)
        previous = symbol
    return loss / len(test)


def evaluate(sequence: str) -> tuple[float, float]:
    train, test = split_sequence(sequence)
    return unigram_cross_entropy(train, test), bigram_cross_entropy(train, test)


def main() -> None:
    ordered = make_sequence(SEQUENCE_LENGTH)
    print("Compression strategy spectrum — sequential-structure toy")
    print("Metric: held-out cross-entropy (bits/token)")
    for seed in SEEDS:
        permuted = permute_preserving_marginals(ordered, seed)
        for label, sequence in (("ordered", ordered), ("permuted", permuted)):
            unigram, bigram = evaluate(sequence)
            print(f"seed={seed:3d} data={label:9s} unigram={unigram:.4f} bigram={bigram:.4f}")
    print("Interpretation: a lower held-out loss indicates better prediction only.")
    print("This is not an epiplexity, understanding, or subjectivity measurement.")


if __name__ == "__main__":
    main()
