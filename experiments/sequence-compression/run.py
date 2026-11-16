#!/usr/bin/env python3
"""Deterministic comparison of marginal/conditional entropy and zlib size."""

from __future__ import annotations

import random
import sys
import zlib
from collections import Counter, defaultdict
from math import log2

SEED = 20261116
LENGTH = 20_000
ALPHABET = "ABCD"


def generate_sequences(length: int = LENGTH, seed: int = SEED) -> dict[str, str]:
    if length < 2:
        raise ValueError("length must be at least two")
    rng = random.Random(seed)
    iid_uniform = "".join(rng.choice(ALPHABET) for _ in range(length))
    markov = [rng.choice(ALPHABET)]
    for _ in range(length - 1):
        previous = markov[-1]
        if rng.random() < 0.9:
            markov.append(previous)
        else:
            alternatives = [symbol for symbol in ALPHABET if symbol != previous]
            markov.append(rng.choice(alternatives))
    repeated = ("ABCD" * ((length + 3) // 4))[:length]
    return {"repeated motif": repeated, "Markov (P[stay]=0.9)": "".join(markov), "IID uniform": iid_uniform}


def entropy(counts: Counter[str]) -> float:
    total = sum(counts.values())
    return -sum((count / total) * log2(count / total) for count in counts.values())


def entropy_metrics(sequence: str) -> tuple[float, float]:
    marginal = entropy(Counter(sequence))
    transitions: dict[str, Counter[str]] = defaultdict(Counter)
    for previous, current in zip(sequence, sequence[1:], strict=False):
        transitions[previous][current] += 1
    total = len(sequence) - 1
    conditional = sum(sum(counts.values()) / total * entropy(counts) for counts in transitions.values())
    return marginal, conditional


def summarize(sequences: dict[str, str]) -> list[dict[str, float | str]]:
    rows = []
    for label, sequence in sequences.items():
        marginal, conditional = entropy_metrics(sequence)
        compressed = zlib.compress(sequence.encode("ascii"), level=9)
        rows.append({"source": label, "H0_bits_per_symbol": marginal, "H1_bits_per_symbol": conditional, "zlib_bits_per_symbol": len(compressed) * 8 / len(sequence), "raw_bytes": float(len(sequence)), "zlib_bytes": float(len(compressed))})
    return rows


def main() -> None:
    rows = summarize(generate_sequences())
    header = f"{'source':24s} {'H0':>8s} {'H1':>8s} {'zlib':>8s}"
    lines = [header, "-" * len(header)]
    for row in rows:
        lines.append(f"{row['source']:24s} {row['H0_bits_per_symbol']:8.3f} {row['H1_bits_per_symbol']:8.3f} {row['zlib_bits_per_symbol']:8.3f}")
    lines.append("H0 = marginal entropy; H1 = empirical first-order conditional entropy.")
    lines.append("zlib includes container/codec overhead; it is not an ideal entropy code.")
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
