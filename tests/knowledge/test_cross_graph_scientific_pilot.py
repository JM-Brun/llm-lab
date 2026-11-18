"""Regression checks for the manually reviewed attention/information pilot."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = runpy.run_path(
    str(ROOT / "experiments" / "information-theory" / "attention_kl_vs_mutual_information.py"),
    run_name="attention_kl_pilot_test",
)


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def test_attention_computation_resolves_to_primary_source_locator() -> None:
    concepts = _load_yaml(ROOT / "data" / "concepts.yml")
    computational = _load_yaml(ROOT / "data" / "computational-graph.yml")
    extraction = _load_yaml(ROOT / "data" / "extractions" / "vaswani-et-al-attention-is-all-you-need-2017.yml")

    concept_ids = {item["id"] for item in concepts["concepts"]}
    assert {"attention-weight", "softmax", "entropy", "mutual-information"} <= concept_ids

    nodes = {item["id"] for item in computational["nodes"]}
    assert {
        "attention-score-computation",
        "attention-softmax",
        "attention-weights",
        "value-aggregation",
    } <= nodes

    edges = {(item["from"], item["type"], item["to"]) for item in computational["edges"]}
    assert ("attention-softmax", "produces", "attention-weights") in edges
    assert ("attention-weights", "consumes", "value-aggregation") in edges

    item = next(
        item
        for item in extraction["items"]
        if item["id"] == "vaswani-et-al-attention-is-all-you-need-2017:scaled-dot-product-attention"
    )
    assert item["locator"]["type"] == "section"
    assert item["locator"]["value"] == "3.2.1"
    assert any("mutual information" in limit.lower() for limit in item["evidence"]["limitations"])


def test_row_to_uniform_kl_is_not_mutual_information() -> None:
    import numpy as np

    rows = np.array([[0.9, 0.1], [0.9, 0.1]], dtype=np.float64)
    context_probabilities = np.array([0.5, 0.5], dtype=np.float64)

    metrics = EXPERIMENT["describe_case"](rows, context_probabilities)

    assert metrics["mean_row_kl_to_uniform_bits"] > 0.0
    assert abs(metrics["mutual_information_bits"]) < 1e-12
    assert abs(metrics["mean_row_kl_to_marginal_bits"]) < 1e-12


def test_flashattention_evidence_is_an_io_implementation_not_source_coding() -> None:
    extraction = _load_yaml(ROOT / "data" / "extractions" / "dao-et-al-flashattention-2022.yml")
    item = next(
        item
        for item in extraction["items"]
        if item["id"] == "dao-et-al-flashattention-2022:exact-io-aware-attention"
    )

    assert item["locator"]["type"] == "section"
    assert "3.1" in item["locator"]["value"]
    assert "3.2" in item["locator"]["value"]
    assert "IO-aware" in item["summary"]
    limitations = " ".join(item["evidence"]["limitations"]).lower()
    assert "floating-point" in limitations
    assert "o(n^2" in limitations
