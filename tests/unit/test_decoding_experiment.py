"""Check the conclusions of the small, deterministic decoding experiment."""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np


def test_decoding_experiment_outputs_expected_comparisons() -> None:
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, str(root / "experiments/decoding-distribution/run.py")],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    cold, baseline, hot, top_k = data["results"]
    assert cold["entropy_nats"] < baseline["entropy_nats"] < hot["entropy_nats"]
    assert 0 < top_k["retained_mass_before_renormalization"] < 1
    assert np.count_nonzero(top_k["probabilities"]) == 2
    for row in data["results"]:
        assert np.isclose(sum(row["probabilities"]), 1.0)


def test_decoding_experiment_reproduces_the_recorded_report() -> None:
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, str(root / "experiments/decoding-distribution/run.py")],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    actual = json.loads(result.stdout)
    recorded = json.loads((root / "reports/decoding-distribution.json").read_text())
    assert actual["synthetic_logits"] == recorded["synthetic_logits"]
    assert len(actual["results"]) == len(recorded["results"])
    for observed, expected in zip(actual["results"], recorded["results"], strict=True):
        assert observed["temperature"] == expected["temperature"]
        assert observed["top_k"] == expected["top_k"]
        np.testing.assert_allclose(observed["probabilities"], expected["probabilities"], rtol=1e-12)
        np.testing.assert_allclose(observed["entropy_nats"], expected["entropy_nats"], rtol=1e-12)
        np.testing.assert_allclose(
            observed["retained_mass_before_renormalization"],
            expected["retained_mass_before_renormalization"],
            rtol=1e-12,
        )
