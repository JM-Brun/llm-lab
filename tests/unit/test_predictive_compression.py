from __future__ import annotations

import runpy
from fractions import Fraction
from math import log2
from pathlib import Path


def test_predictive_coder_round_trips_exactly() -> None:
    root = Path(__file__).resolve().parents[2]
    module = runpy.run_path(str(root / "experiments/predictive-compression/run.py"))
    model = module["train_bigram_model"](module["TRAINING"])
    message = module["MESSAGE"]
    low, high = module["interval_for"](message, model)
    numerator, bits = module["dyadic_code_inside"](low, high)
    code_value = Fraction(numerator, 1 << bits)

    assert low <= code_value
    assert Fraction(numerator + 1, 1 << bits) <= high
    assert module["decode"](numerator, bits, len(message), model) == message


def test_predictive_model_beats_uniform_on_fixed_toy_message() -> None:
    root = Path(__file__).resolve().parents[2]
    module = runpy.run_path(str(root / "experiments/predictive-compression/run.py"))
    model = module["train_bigram_model"](module["TRAINING"])
    low, high = module["interval_for"](module["MESSAGE"], model)
    ideal_bits = -log2(float(high - low))
    uniform_bits = len(module["MESSAGE"]) * log2(len(module["ALPHABET"]))

    assert ideal_bits < uniform_bits


def test_domain_shift_increases_predictive_code_length() -> None:
    root = Path(__file__).resolve().parents[2]
    module = runpy.run_path(str(root / "experiments/predictive-compression/run.py"))
    train = module["train_bigram_model"]
    cost = module["sequence_cost_bits"]
    model_ab = train("AB" * 100)
    model_cd = train("CD" * 100)

    assert cost("AB" * 20, model_ab) < cost("CD" * 20, model_ab)
    assert cost("CD" * 20, model_cd) < cost("AB" * 20, model_cd)


def test_huffman_code_is_prefix_free_and_meets_entropy_for_dyadic_source() -> None:
    root = Path(__file__).resolve().parents[2]
    module = runpy.run_path(str(root / "experiments/predictive-compression/run.py"))
    probabilities = {
        "A": Fraction(1, 2),
        "B": Fraction(1, 4),
        "C": Fraction(1, 8),
        "D": Fraction(1, 8),
    }
    codes = module["huffman_code"](probabilities)

    assert module["is_prefix_free"](codes)
    assert module["kraft_sum"](codes) == 1
    assert module["average_code_length"](probabilities, codes) == Fraction(7, 4)


def test_huffman_rejects_invalid_probability_distributions() -> None:
    root = Path(__file__).resolve().parents[2]
    module = runpy.run_path(str(root / "experiments/predictive-compression/run.py"))

    try:
        module["huffman_code"]({"A": Fraction(1, 2), "B": Fraction(1, 3)})
    except ValueError as error:
        assert "sum to one" in str(error)
    else:
        raise AssertionError("Invalid probability distribution was accepted")


def test_kraft_sum_rejects_non_binary_or_empty_codewords() -> None:
    root = Path(__file__).resolve().parents[2]
    module = runpy.run_path(str(root / "experiments/predictive-compression/run.py"))

    for invalid in ({"A": ""}, {"A": "02"}):
        try:
            module["kraft_sum"](invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Invalid codewords were accepted: {invalid}")
