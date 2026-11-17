#!/usr/bin/env python3
"""Controlled forward/reverse codec comparison and a small two-part MDL illustration."""

from __future__ import annotations

import argparse
import bz2
import csv
import lzma
import random
import statistics
import sys
import zlib
from collections import Counter, defaultdict
from math import floor, log2
from typing import Callable

ALPHABET = 4
DEFAULT_LENGTH = 16_384
DEFAULT_SEEDS = tuple(range(20261117, 20261125))
CODECS: dict[str, Callable[[bytes], bytes]] = {
    "zlib-9": lambda data: zlib.compress(data, level=9),
    "bz2-9": lambda data: bz2.compress(data, compresslevel=9),
    "xz-6": lambda data: lzma.compress(data, format=lzma.FORMAT_XZ, preset=6),
}


def _markov(length: int, rng: random.Random, p_stay: float) -> bytes:
    values = [rng.randrange(ALPHABET)]
    for _ in range(length - 1):
        previous = values[-1]
        if rng.random() < p_stay:
            values.append(previous)
        else:
            choices = [value for value in range(ALPHABET) if value != previous]
            values.append(rng.choice(choices))
    return bytes(values)


def generate_sources(length: int, seed: int) -> dict[str, bytes]:
    """Generate IID, stationary Markov, and non-stationary regime-shift controls."""
    if length < 8:
        raise ValueError("length must be at least eight symbols")
    rng = random.Random(seed)
    iid = bytes(rng.randrange(ALPHABET) for _ in range(length))
    stationary = _markov(length, rng, 0.9)
    split = length // 2
    regime_rng = random.Random(seed + 1_000_003)
    first = _markov(split, regime_rng, 0.98)
    second = _markov(length - split, regime_rng, 0.55)
    regime = first + second
    return {
        "iid_uniform": iid,
        "stationary_markov_p_stay_0.9": stationary,
        "nonstationary_regime_shift_0.98_to_0.55": regime,
    }


def directional_rows(
    length: int = DEFAULT_LENGTH, seeds: tuple[int, ...] = DEFAULT_SEEDS
) -> list[dict[str, int | str]]:
    rows: list[dict[str, int | str]] = []
    for seed in seeds:
        for source, payload in generate_sources(length, seed).items():
            reversed_payload = payload[::-1]
            for codec_name, compressor in CODECS.items():
                forward_size = len(compressor(payload))
                reverse_size = len(compressor(reversed_payload))
                rows.append(
                    {
                        "seed": seed,
                        "source": source,
                        "codec": codec_name,
                        "symbols": length,
                        "forward_bytes": forward_size,
                        "reverse_bytes": reverse_size,
                        # Positive delta means the forward sequence compressed smaller.
                        "reverse_minus_forward_bytes": reverse_size - forward_size,
                    }
                )
    return rows


def directional_summary(rows: list[dict[str, int | str]]) -> list[dict[str, int | float | str]]:
    grouped: dict[tuple[str, str], list[int]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["source"]), str(row["codec"]))].append(
            int(row["reverse_minus_forward_bytes"])
        )
    summary = []
    for (source, codec), deltas in sorted(grouped.items()):
        summary.append(
            {
                "source": source,
                "codec": codec,
                "n_seeds": len(deltas),
                "mean_reverse_minus_forward_bytes": statistics.mean(deltas),
                "median_reverse_minus_forward_bytes": statistics.median(deltas),
                "forward_smaller_fraction": sum(delta > 0 for delta in deltas) / len(deltas),
            }
        )
    return summary


def _quantize_probabilities(counts: Counter[int], alphabet: int = ALPHABET) -> list[int]:
    """Quantize a smoothed distribution to positive integer frequencies summing to 255."""
    total = sum(counts.values()) + alphabet
    probabilities = [(counts[value] + 1) / total for value in range(alphabet)]
    remaining = 255 - alphabet
    scaled = [probability * remaining for probability in probabilities]
    frequencies = [1 + floor(value) for value in scaled]
    extras = 255 - sum(frequencies)
    order = sorted(
        range(alphabet),
        key=lambda index: scaled[index] - floor(scaled[index]),
        reverse=True,
    )
    for index in order[:extras]:
        frequencies[index] += 1
    assert sum(frequencies) == 255 and min(frequencies) >= 1
    return frequencies


def _fit_iid(training: bytes) -> list[int]:
    return _quantize_probabilities(Counter(training))


def _fit_bigram(training: bytes) -> dict[int, list[int]]:
    transitions: dict[int, Counter[int]] = defaultdict(Counter)
    for previous, current in zip(training, training[1:]):
        transitions[previous][current] += 1
    return {
        previous: _quantize_probabilities(transitions[previous])
        for previous in range(ALPHABET)
    }


def _ideal_bits_iid(test: bytes, frequencies: list[int]) -> float:
    return sum(-log2(frequencies[symbol] / 255) for symbol in test)


def _ideal_bits_bigram(test: bytes, training_last: int, tables: dict[int, list[int]]) -> float:
    previous = training_last
    total = 0.0
    for current in test:
        total -= log2(tables[previous][current] / 255)
        previous = current
    return total


def mdl_rows(
    length: int = DEFAULT_LENGTH, seed: int = 20261117
) -> list[dict[str, int | float | str]]:
    """Compare test-data code cost alone with a fixed-width model-description charge."""
    source = generate_sources(length, seed)["stationary_markov_p_stay_0.9"]
    split = length // 2
    rows: list[dict[str, int | float | str]] = []
    for direction, sequence in (("forward", source), ("reverse", source[::-1])):
        training, test = sequence[:split], sequence[split:]
        iid_table = _fit_iid(training)
        bigram_tables = _fit_bigram(training)
        candidates = (
            ("iid", _ideal_bits_iid(test, iid_table), 1 + ALPHABET * 8),
            (
                "bigram",
                _ideal_bits_bigram(test, training[-1], bigram_tables),
                1 + ALPHABET * ALPHABET * 8,
            ),
        )
        for model, data_bits, model_bits in candidates:
            rows.append(
                {
                    "direction": direction,
                    "model": model,
                    "test_symbols": len(test),
                    "ideal_test_data_bits": data_bits,
                    "fixed_width_model_description_bits": model_bits,
                    "two_part_score_bits": data_bits + model_bits,
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--length", type=int, default=DEFAULT_LENGTH)
    parser.add_argument("--seeds", type=int, default=len(DEFAULT_SEEDS))
    parser.add_argument(
        "--csv", action="store_true", help="print paired per-seed codec results as CSV"
    )
    args = parser.parse_args()
    if args.seeds < 1:
        parser.error("--seeds must be positive")
    seeds = tuple(range(20261117, 20261117 + args.seeds))
    rows = directional_rows(args.length, seeds)
    if args.csv:
        writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
        return

    print("Forward/reverse compression — paired synthetic controls")
    print("Positive delta = reverse output larger, hence forward compressed smaller.")
    print("source | codec | seeds | mean delta B | median delta B | forward-win fraction")
    for row in directional_summary(rows):
        print(
            f"{row['source']} | {row['codec']} | {row['n_seeds']} | "
            f"{row['mean_reverse_minus_forward_bytes']:.2f} | "
            f"{row['median_reverse_minus_forward_bytes']:.2f} | "
            f"{row['forward_smaller_fraction']:.2f}"
        )

    print("\nConditional two-part MDL illustration (stationary Markov source)")
    print("direction | model | ideal test bits | model-description bits | total score bits")
    for row in mdl_rows(args.length, seeds[0]):
        print(
            f"{row['direction']} | {row['model']} | {row['ideal_test_data_bits']:.1f} | "
            f"{row['fixed_width_model_description_bits']} | {row['two_part_score_bits']:.1f}"
        )


if __name__ == "__main__":
    main()
