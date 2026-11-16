#!/usr/bin/env python3
"""Exact arithmetic-coding demonstration using a tiny conditional bigram model."""

from __future__ import annotations

import heapq
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from math import log2

ALPHABET = ("A", "B", "C", "D")
TRAINING = "ABABACABADABABACABADABABACABADABABACABAD"
MESSAGE = "ABABACABADABABACABAD"
SMOOTHING = 1


def train_bigram_model(training: str) -> dict[str, dict[str, Fraction]]:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    previous = "^"
    for symbol in training:
        if symbol not in ALPHABET:
            raise ValueError(f"Unknown training symbol: {symbol}")
        counts[previous][symbol] += 1
        previous = symbol
    model = {}
    for context, observed in counts.items():
        total = sum(observed.values()) + SMOOTHING * len(ALPHABET)
        model[context] = {
            symbol: Fraction(observed[symbol] + SMOOTHING, total) for symbol in ALPHABET
        }
    return model


def probs_for(model: dict[str, dict[str, Fraction]], context: str) -> dict[str, Fraction]:
    return model.get(context, {s: Fraction(1, len(ALPHABET)) for s in ALPHABET})


def interval_for(message: str, model: dict[str, dict[str, Fraction]]) -> tuple[Fraction, Fraction]:
    low, high = Fraction(0), Fraction(1)
    previous = "^"
    for symbol in message:
        probs = probs_for(model, previous)
        width = high - low
        cumulative = Fraction(0)
        for candidate in ALPHABET:
            next_cumulative = cumulative + probs[candidate]
            if candidate == symbol:
                high = low + width * next_cumulative
                low = low + width * cumulative
                break
            cumulative = next_cumulative
        else:
            raise ValueError(f"Unknown symbol: {symbol}")
        previous = symbol
    return low, high


def sequence_cost_bits(message: str, model: dict[str, dict[str, Fraction]]) -> float:
    """Return the ideal predictive code length for a message, in bits."""
    previous = "^"
    total = 0.0
    for symbol in message:
        if symbol not in ALPHABET:
            raise ValueError(f"Unknown symbol: {symbol}")
        probability = probs_for(model, previous)[symbol]
        total -= log2(float(probability))
        previous = symbol
    return total


def dyadic_code_inside(low: Fraction, high: Fraction) -> tuple[int, int]:
    """Choose a binary fraction safely inside the final interval."""
    bits = 0
    while True:
        denominator = 1 << bits
        # Find the first dyadic value >= low, using integer arithmetic only.
        numerator = (low.numerator * denominator + low.denominator - 1) // low.denominator
        if Fraction(numerator + 1, denominator) <= high:
            return numerator, bits
        bits += 1


def decode(numerator: int, bits: int, length: int, model: dict[str, dict[str, Fraction]]) -> str:
    code_value = Fraction(numerator, 1 << bits)
    low, high = Fraction(0), Fraction(1)
    previous = "^"
    output = []
    for _ in range(length):
        width = high - low
        cumulative = Fraction(0)
        for symbol in ALPHABET:
            probability = probs_for(model, previous)[symbol]
            next_cumulative = cumulative + probability
            candidate_low = low + width * cumulative
            candidate_high = low + width * next_cumulative
            if candidate_low <= code_value < candidate_high:
                output.append(symbol)
                low, high, previous = candidate_low, candidate_high, symbol
                break
            cumulative = next_cumulative
        else:
            raise ValueError("Code value is outside all symbol intervals")
    return "".join(output)



def huffman_code(probabilities: dict[str, Fraction]) -> dict[str, str]:
    """Build a deterministic binary Huffman code for a positive distribution."""
    if not probabilities:
        raise ValueError("At least one symbol probability is required")
    if any(probability <= 0 for probability in probabilities.values()):
        raise ValueError("All symbol probabilities must be positive")
    if sum(probabilities.values(), Fraction(0)) != 1:
        raise ValueError("Symbol probabilities must sum to one")
    if len(probabilities) == 1:
        return {next(iter(probabilities)): "0"}

    heap: list[tuple[Fraction, int, object]] = []
    serial = 0
    for symbol, probability in probabilities.items():
        heapq.heappush(heap, (probability, serial, symbol))
        serial += 1
    while len(heap) > 1:
        left_weight, _, left = heapq.heappop(heap)
        right_weight, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (left_weight + right_weight, serial, (left, right)))
        serial += 1

    codes: dict[str, str] = {}

    def visit(node: object, prefix: str) -> None:
        if isinstance(node, str):
            codes[node] = prefix or "0"
            return
        left, right = node
        visit(left, prefix + "0")
        visit(right, prefix + "1")

    visit(heap[0][2], "")
    return codes


def is_prefix_free(codes: dict[str, str]) -> bool:
    """Return whether distinct codewords form a prefix-free set."""
    words = list(codes.values())
    return len(set(words)) == len(words) and all(
        not other.startswith(word)
        for word in words
        for other in words
        if word != other
    )


def kraft_sum(codes: dict[str, str]) -> Fraction:
    """Return the binary Kraft sum for a collection of codewords."""
    if any(not word or set(word) - {"0", "1"} for word in codes.values()):
        raise ValueError("Codewords must be non-empty binary strings")
    return sum((Fraction(1, 2 ** len(word)) for word in codes.values()), Fraction(0))


def average_code_length(
    probabilities: dict[str, Fraction], codes: dict[str, str]
) -> Fraction:
    """Return expected code length; require exactly matching symbol sets."""
    if probabilities.keys() != codes.keys():
        raise ValueError("Probabilities and codewords must have identical symbols")
    return sum(
        (probabilities[symbol] * len(codes[symbol]) for symbol in probabilities),
        Fraction(0),
    )


def main() -> None:
    model = train_bigram_model(TRAINING)
    low, high = interval_for(MESSAGE, model)
    numerator, bit_count = dyadic_code_inside(low, high)
    recovered = decode(numerator, bit_count, len(MESSAGE), model)
    ideal_bits = -log2(float(high - low))
    uniform_bits = len(MESSAGE) * log2(len(ALPHABET))
    prefix_probabilities = {
        "A": Fraction(1, 2),
        "B": Fraction(1, 4),
        "C": Fraction(1, 8),
        "D": Fraction(1, 8),
    }
    prefix_codes = huffman_code(prefix_probabilities)
    prefix_average = average_code_length(prefix_probabilities, prefix_codes)
    prefix_kraft = kraft_sum(prefix_codes)
    report = (
        "Prefix-code control distribution: A=1/2, B=1/4, C=1/8, D=1/8",
        f"Huffman codewords: {prefix_codes}",
        f"Prefix-free:      {is_prefix_free(prefix_codes)}",
        f"Kraft sum:        {prefix_kraft}",
        f"Entropy:          1.750 bits/symbol",
        f"Average length:   {prefix_average} bits/symbol",
        "",
        "Predictive compression — exact toy experiment",
        f"Training symbols: {len(TRAINING)}",
        f"Message:          {MESSAGE}",
        f"Ideal model cost: {ideal_bits:.3f} bits",
        f"Uniform baseline: {uniform_bits:.3f} bits",
        f"Actual code:      {bit_count} bits",
        f"Decoded exactly:  {recovered == MESSAGE}",
        f"Decoded message:  {recovered}",
    )
    sys.stdout.write("\n".join(report) + "\n")
    if not is_prefix_free(prefix_codes) or prefix_kraft > 1:
        raise AssertionError("Prefix-code validity check failed")
    if prefix_average != Fraction(7, 4):
        raise AssertionError("Unexpected Huffman average length")
    if recovered != MESSAGE:
        raise AssertionError("Lossless round-trip failed")


if __name__ == "__main__":
    main()
