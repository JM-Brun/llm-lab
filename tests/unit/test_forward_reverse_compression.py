from __future__ import annotations

import runpy
from pathlib import Path


def _module() -> dict[str, object]:
    root = Path(__file__).resolve().parents[2]
    return runpy.run_path(str(root / "experiments/forward-reverse-compression/run.py"))


def test_synthetic_sources_are_deterministic_and_reversible() -> None:
    module = _module()
    sources = module["generate_sources"](128, 20261117)
    assert sources == module["generate_sources"](128, 20261117)
    assert all(payload == payload[::-1][::-1] for payload in sources.values())


def test_directional_rows_are_paired_and_cover_each_codec() -> None:
    module = _module()
    rows = module["directional_rows"](128, (1, 2))
    assert len(rows) == 2 * 3 * 3
    assert {row["codec"] for row in rows} == {"zlib-9", "bz2-9", "xz-6"}
    assert all(row["forward_bytes"] > 0 and row["reverse_bytes"] > 0 for row in rows)


def test_model_description_cost_changes_two_part_accounting() -> None:
    module = _module()
    rows = module["mdl_rows"](2048, 20261117)
    assert len(rows) == 4
    by_model = {row["model"]: row for row in rows if row["direction"] == "forward"}
    assert by_model["iid"]["fixed_width_model_description_bits"] == 33
    assert by_model["bigram"]["fixed_width_model_description_bits"] == 129
    assert by_model["bigram"]["two_part_score_bits"] > by_model["bigram"]["ideal_test_data_bits"]
