from __future__ import annotations

import json
import runpy
from fractions import Fraction
from pathlib import Path


def _module() -> dict[str, object]:
    root = Path(__file__).resolve().parents[2]
    return runpy.run_path(str(root / "experiments/predictive-compression/quantized_coder.py"))


def test_quantization_is_positive_deterministic_and_normalized() -> None:
    module = _module()
    probabilities = {
        "A": Fraction(1, 2),
        "B": Fraction(1, 4),
        "C": Fraction(1, 8),
        "D": Fraction(1, 8),
    }
    quantize = module["quantize_probabilities"]
    frequencies = quantize(probabilities, 8)

    assert frequencies == quantize(probabilities, 8)
    assert sum(frequencies.values()) == 256
    assert all(value > 0 for value in frequencies.values())


def test_framed_quantized_coder_round_trips_and_separates_costs() -> None:
    module = _module()
    model = module["train_bigram_model"](module["TRAINING"])
    message = module["MESSAGE"]
    frame, metrics = module["encode"](message, model, precision=12)

    assert module["decode"](frame, model) == message
    assert metrics["float_model_nll_bits"] > 0
    assert metrics["quantized_model_ideal_bits"] > 0
    assert metrics["payload_bits"] <= metrics["quantized_model_ideal_bits"] + 2
    assert metrics["payload_bytes"] == (metrics["payload_bits"] + 7) // 8
    assert metrics["serialized_bytes"] == len(frame)
    assert metrics["serialized_bits"] == 8 * len(frame)
    assert metrics["framing_and_padding_bits"] == (
        metrics["header_bytes"] * 8 + metrics["payload_padding_bits"]
    )


def test_quantized_coder_is_deterministic() -> None:
    module = _module()
    model = module["train_bigram_model"](module["TRAINING"])
    assert module["encode"](module["MESSAGE"], model) == module["encode"](module["MESSAGE"], model)


def test_decoder_rejects_truncated_and_corrupt_frames() -> None:
    module = _module()
    model = module["train_bigram_model"](module["TRAINING"])
    frame, _ = module["encode"](module["MESSAGE"], model)

    for invalid in (frame[:5], frame[:-1], b"BAD!" + frame[4:]):
        try:
            module["decode"](invalid, model)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid frame was accepted")


def test_probability_quantization_rejects_invalid_precision_and_distribution() -> None:
    module = _module()
    quantize = module["quantize_probabilities"]
    valid = {"A": Fraction(1, 2), "B": Fraction(1, 2)}
    for precision in (0, 25):
        try:
            quantize(valid, precision)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid precision was accepted")

    for probabilities in (
        {},
        {"A": Fraction(1, 2), "B": Fraction(1, 3)},
        {"A": Fraction(1), "B": Fraction(0)},
    ):
        try:
            quantize(probabilities, 8)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid probability distribution was accepted")


def test_cli_runs_and_reports_distinct_coding_costs(capsys: object) -> None:
    module = _module()
    module["main"]()
    report = json.loads(capsys.readouterr().out)

    assert report["experiment"] == "quantized-predictive-arithmetic-coding"
    assert report["decoded_exactly"] is True
    assert report["float_model_nll_bits"] > 0
    assert report["quantized_model_ideal_bits"] > 0
    assert report["payload_bits"] > 0
    assert report["serialized_bytes"] >= report["payload_bytes"]
    assert report["model_and_training_cost_transmitted"] is False
