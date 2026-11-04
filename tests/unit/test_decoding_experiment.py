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
