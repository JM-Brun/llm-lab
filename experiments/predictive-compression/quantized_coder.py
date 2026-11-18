"""Quantized-probability arithmetic coding with explicit bitstream framing.

The interval arithmetic is exact (Fraction); probabilities are quantized to an
integer frequency table. This is deliberately not presented as a bounded-state
production range coder. The model is shared out of band; only the message frame
and payload are serialized here.
"""

from __future__ import annotations

import struct
from collections import Counter, defaultdict
from fractions import Fraction
from math import log2
from typing import TypeAlias

ALPHABET = ("A", "B", "C", "D")
TRAINING = "ABABACABADABABACABADABABACABADABABACABAD"
MESSAGE = "ABABACABADABABACABAD"
SMOOTHING = 1
MAGIC = b"LLPC"
VERSION = 1
HEADER = struct.Struct(">4sBBII")
Model: TypeAlias = dict[str, dict[str, Fraction]]


def train_bigram_model(training: str) -> Model:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    previous = "^"
    for symbol in training:
        if symbol not in ALPHABET:
            raise ValueError(f"Unknown training symbol: {symbol}")
        counts[previous][symbol] += 1
        previous = symbol
    model: Model = {}
    for context, observed in counts.items():
        total = sum(observed.values()) + SMOOTHING * len(ALPHABET)
        model[context] = {
            symbol: Fraction(observed[symbol] + SMOOTHING, total) for symbol in ALPHABET
        }
    return model


def probabilities_for(model: Model, context: str) -> dict[str, Fraction]:
    return model.get(context, {symbol: Fraction(1, len(ALPHABET)) for symbol in ALPHABET})


def quantize_probabilities(probabilities: dict[str, Fraction], precision: int) -> dict[str, int]:
    """Convert a distribution to positive integer frequencies summing to 2**precision.

    One count is reserved for every symbol; remaining counts use deterministic
    largest-remainder apportionment. Ties follow the input symbol order.
    """
    if not 1 <= precision <= 24:
        raise ValueError("precision must be between 1 and 24 bits")
    symbols = tuple(probabilities)
    if not symbols or len(symbols) > (1 << precision):
        raise ValueError("frequency precision cannot represent every symbol")
    if any(value <= 0 for value in probabilities.values()):
        raise ValueError("all probabilities must be positive")
    if sum(probabilities.values(), Fraction(0)) != 1:
        raise ValueError("probabilities must sum to one")

    total = 1 << precision
    distributable = total - len(symbols)
    quotas = {symbol: probabilities[symbol] * distributable for symbol in symbols}
    frequencies = {
        symbol: 1 + quota.numerator // quota.denominator for symbol, quota in quotas.items()
    }
    remaining = total - sum(frequencies.values())
    ranked = sorted(
        symbols,
        key=lambda symbol: (-(quotas[symbol] - (frequencies[symbol] - 1)), symbols.index(symbol)),
    )
    for symbol in ranked[:remaining]:
        frequencies[symbol] += 1
    return frequencies


def quantized_model(model: Model, precision: int) -> dict[str, dict[str, int]]:
    return {context: quantize_probabilities(row, precision) for context, row in model.items()}


def frequencies_for(
    model: dict[str, dict[str, int]], context: str, precision: int
) -> dict[str, int]:
    return model.get(
        context,
        quantize_probabilities(
            {symbol: Fraction(1, len(ALPHABET)) for symbol in ALPHABET}, precision
        ),
    )


def sequence_nll_bits(message: str, model: Model) -> float:
    previous = "^"
    total = 0.0
    for symbol in message:
        if symbol not in ALPHABET:
            raise ValueError(f"Unknown symbol: {symbol}")
        total -= log2(float(probabilities_for(model, previous)[symbol]))
        previous = symbol
    return total


def quantized_nll_bits(message: str, model: dict[str, dict[str, int]], precision: int) -> float:
    total = 0.0
    previous = "^"
    denominator = 1 << precision
    for symbol in message:
        if symbol not in ALPHABET:
            raise ValueError(f"Unknown symbol: {symbol}")
        total -= log2(frequencies_for(model, previous, precision)[symbol] / denominator)
        previous = symbol
    return total


def _final_interval(
    message: str, model: dict[str, dict[str, int]], precision: int
) -> tuple[Fraction, Fraction]:
    denominator = 1 << precision
    low, high = Fraction(0), Fraction(1)
    previous = "^"
    for symbol in message:
        if symbol not in ALPHABET:
            raise ValueError(f"Unknown symbol: {symbol}")
        row = frequencies_for(model, previous, precision)
        width = high - low
        cumulative = 0
        for candidate in ALPHABET:
            frequency = row[candidate]
            if candidate == symbol:
                high = low + width * Fraction(cumulative + frequency, denominator)
                low = low + width * Fraction(cumulative, denominator)
                break
            cumulative += frequency
        previous = symbol
    return low, high


def _dyadic_code_inside(low: Fraction, high: Fraction) -> tuple[int, int]:
    bits = 0
    while True:
        denominator = 1 << bits
        numerator = (low.numerator * denominator + low.denominator - 1) // low.denominator
        if Fraction(numerator + 1, denominator) <= high:
            return numerator, bits
        bits += 1


def _pack_payload(numerator: int, bit_count: int) -> bytes:
    if bit_count < 0 or numerator < 0 or numerator >= (1 << bit_count):
        raise ValueError("invalid dyadic payload")
    byte_count = (bit_count + 7) // 8
    padding = byte_count * 8 - bit_count
    return (numerator << padding).to_bytes(byte_count, "big")


def encode(
    message: str, model: Model, *, precision: int = 12
) -> tuple[bytes, dict[str, float | int]]:
    if not 1 <= precision <= 24:
        raise ValueError("precision must be between 1 and 24 bits")
    frequencies = quantized_model(model, precision)
    low, high = _final_interval(message, frequencies, precision)
    numerator, bit_count = _dyadic_code_inside(low, high)
    payload = _pack_payload(numerator, bit_count)
    header = HEADER.pack(MAGIC, VERSION, precision, len(message), bit_count)
    frame = header + payload
    payload_padding_bits = len(payload) * 8 - bit_count
    metrics: dict[str, float | int] = {
        "float_model_nll_bits": sequence_nll_bits(message, model),
        "quantized_model_ideal_bits": quantized_nll_bits(message, frequencies, precision),
        "payload_bits": bit_count,
        "payload_bytes": len(payload),
        "payload_padding_bits": payload_padding_bits,
        "header_bytes": HEADER.size,
        "serialized_bytes": len(frame),
        "serialized_bits": len(frame) * 8,
        "framing_and_padding_bits": HEADER.size * 8 + payload_padding_bits,
    }
    return frame, metrics


def decode(frame: bytes, model: Model) -> str:
    if len(frame) < HEADER.size:
        raise ValueError("truncated frame header")
    magic, version, precision, message_length, bit_count = HEADER.unpack(frame[: HEADER.size])
    if magic != MAGIC or version != VERSION:
        raise ValueError("unknown frame format")
    if not 1 <= precision <= 24:
        raise ValueError("invalid probability precision")
    payload = frame[HEADER.size :]
    expected_bytes = (bit_count + 7) // 8
    if len(payload) != expected_bytes:
        raise ValueError("payload length does not match header")
    padding = expected_bytes * 8 - bit_count
    packed = int.from_bytes(payload, "big") if payload else 0
    if padding and packed & ((1 << padding) - 1):
        raise ValueError("non-zero payload padding")
    numerator = packed >> padding
    if numerator >= (1 << bit_count):
        raise ValueError("payload value exceeds declared bit length")

    frequencies = quantized_model(model, precision)
    code_value = Fraction(numerator, 1 << bit_count)
    low, high = Fraction(0), Fraction(1)
    previous = "^"
    output: list[str] = []
    denominator = 1 << precision
    for _ in range(message_length):
        width = high - low
        scaled = (code_value - low) * denominator / width
        target = scaled.numerator // scaled.denominator
        cumulative = 0
        for symbol in ALPHABET:
            frequency = frequencies_for(frequencies, previous, precision)[symbol]
            if cumulative <= target < cumulative + frequency:
                next_low = low + width * Fraction(cumulative, denominator)
                next_high = low + width * Fraction(cumulative + frequency, denominator)
                output.append(symbol)
                low, high, previous = next_low, next_high, symbol
                break
            cumulative += frequency
        else:
            raise ValueError("code value is outside all symbol intervals")
    return "".join(output)


def main() -> None:
    model = train_bigram_model(TRAINING)
    frame, metrics = encode(MESSAGE, model)
    recovered = decode(frame, model)
    report = {
        "experiment": "quantized-predictive-arithmetic-coding",
        "precision_bits": 12,
        "message_symbols": len(MESSAGE),
        **metrics,
        "decoded_exactly": recovered == MESSAGE,
        "model_and_training_cost_transmitted": False,
    }
    import json

    print(json.dumps(report, indent=2))  # noqa: T201 - experiment CLI output
    if recovered != MESSAGE:
        raise AssertionError("lossless round-trip failed")


if __name__ == "__main__":
    main()
