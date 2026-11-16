from __future__ import annotations

import runpy
from pathlib import Path


def _module() -> dict[str, object]:
    root = Path(__file__).resolve().parents[2]
    return runpy.run_path(str(root / "experiments/sequence-compression/run.py"))


def test_generated_sequences_are_deterministic() -> None:
    module = _module()
    assert module["generate_sequences"](100) == module["generate_sequences"](100)


def test_markov_source_has_lower_conditional_than_marginal_entropy() -> None:
    module = _module()
    sequences = module["generate_sequences"]()
    marginal, conditional = module["entropy_metrics"](
        sequences["Markov (P[stay]=0.9)"]
    )
    assert conditional < marginal


def test_zlib_size_is_reproducible_and_markov_compresses_better_than_iid() -> None:
    module = _module()
    rows = module["summarize"](module["generate_sequences"]())
    by_name = {row["source"]: row for row in rows}
    assert (
        by_name["Markov (P[stay]=0.9)"]["zlib_bits_per_symbol"]
        < by_name["IID uniform"]["zlib_bits_per_symbol"]
    )
