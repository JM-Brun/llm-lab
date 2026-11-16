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
