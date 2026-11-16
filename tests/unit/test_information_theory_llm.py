from __future__ import annotations

import runpy
from pathlib import Path

import pytest


def _module() -> dict[str, object]:
    root = Path(__file__).resolve().parents[2]
    return runpy.run_path(str(root / "experiments/information-theory-llm/run.py"))


def test_cross_entropy_decomposes_into_entropy_and_kl() -> None:
    module = _module()
    target = (0.75, 0.25)
    model = (0.70, 0.30)
    assert (
        abs(
            module["cross_entropy"](target, model)
            - module["entropy"](target)
            - module["kl_divergence"](target, model)
        )
        < 1e-12
    )


def test_mutual_information_is_zero_for_independent_variables() -> None:
    module = _module()
    assert abs(module["mutual_information"](((0.25, 0.25), (0.25, 0.25)))) < 1e-12


def test_invalid_distribution_is_rejected() -> None:
    module = _module()
    with pytest.raises(ValueError):
        module["entropy"]((0.2, 0.2))
