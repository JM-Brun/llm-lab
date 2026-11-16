#!/usr/bin/env python3
"""Exact arithmetic-coding demonstration using a tiny conditional bigram model."""

from __future__ import annotations
from collections import Counter, defaultdict
from fractions import Fraction
from math import ceil, log2

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


def dyadic_code_inside(low: Fraction, high: Fraction) -> tuple[int, int]:
    """Choose a binary fraction safely inside the final interval."""
    width = high - low
    bits = ceil(-log2(float(width))) + 1
    denominator = 1 << bits
    midpoint = (low + high) / 2
    numerator = (midpoint.numerator * denominator) // midpoint.denominator
    code_value = Fraction(numerator, denominator)
    if not low <= code_value < high:
        raise ArithmeticError("Chosen binary fraction is outside the coding interval")
    return numerator, bits


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


def main() -> None:
    model = train_bigram_model(TRAINING)
    low, high = interval_for(MESSAGE, model)
    numerator, bit_count = dyadic_code_inside(low, high)
    recovered = decode(numerator, bit_count, len(MESSAGE), model)
    ideal_bits = -log2(float(high - low))
    uniform_bits = len(MESSAGE) * log2(len(ALPHABET))
    print("Predictive compression — exact toy experiment")
    print(f"Training symbols: {len(TRAINING)}")
    print(f"Message:          {MESSAGE}")
    print(f"Ideal model cost: {ideal_bits:.3f} bits")
    print(f"Uniform baseline: {uniform_bits:.3f} bits")
    print(f"Actual code:      {bit_count} bits")
    print(f"Decoded exactly:  {recovered == MESSAGE}")
    print(f"Decoded message:  {recovered}")
    if recovered != MESSAGE:
        raise AssertionError("Lossless round-trip failed")


if __name__ == "__main__":
    main()
