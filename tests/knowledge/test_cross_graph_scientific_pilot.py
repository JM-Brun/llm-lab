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
    extraction = _load_yaml(
        ROOT / "data" / "extractions" / "vaswani-et-al-attention-is-all-you-need-2017.yml"
    )

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
    assert "high-bandwidth memory (HBM)" in item["summary"]
    limitations = " ".join(item["evidence"]["limitations"]).lower()
    assert "floating-point" in limitations
    assert "o(n^2" in limitations


def test_predictive_coding_path_resolves_to_primary_coding_evidence() -> None:
    concepts = _load_yaml(ROOT / "data" / "concepts.yml")
    computational = _load_yaml(ROOT / "data" / "computational-graph.yml")
    shannon = _load_yaml(
        ROOT / "data" / "extractions" / "shannon-mathematical-theory-communication-1948.yml"
    )
    rissanen = _load_yaml(
        ROOT / "data" / "extractions" / "rissanen-langdon-arithmetic-coding-1979.yml"
    )

    concept_ids = {item["id"] for item in concepts["concepts"]}
    assert {
        "cross-entropy",
        "negative-log-likelihood",
        "predictive-compression",
        "entropy-coding",
        "arithmetic-coding",
        "model-compression",
        "quantization",
    } <= concept_ids

    concept_edges = {(item["from"], item["type"], item["to"]) for item in concepts["relations"]}
    assert ("predictive-compression", "contributes-to", "entropy-coding") in concept_edges
    assert ("arithmetic-coding", "part-of", "entropy-coding") in concept_edges
    assert ("quantization", "part-of", "model-compression") in concept_edges
    assert ("model-compression", "contrasts-with", "predictive-compression") in concept_edges

    computation_ids = {item["id"] for item in computational["nodes"]}
    assert {"token-nll", "sequence-log-likelihood", "kv-cache"} <= computation_ids

    shannon_item = next(
        item
        for item in shannon["items"]
        if item["id"]
        == "shannon-mathematical-theory-communication-1948:noiseless-channel-coding-theorem"
    )
    assert "§9" in shannon_item["locator"]["value"]
    assert "Theorem 9" in shannon_item["locator"]["value"]
    assert any(
        "finite encoded file" in limitation
        for limitation in shannon_item["evidence"]["limitations"]
    )

    rissanen_items = {item["id"].split(":")[-1]: item for item in rissanen["items"]}
    assert "pp. 150–152" in rissanen_items["probability-derived-ideal-length"]["locator"]["value"]
    assert "pp. 157–159" in rissanen_items["finite-precision-and-decodability"]["locator"]["value"]

    readme = (ROOT / "experiments" / "predictive-compression" / "README.md").read_text(
        encoding="utf-8"
    )
    assert "quantized_coder.py" in readme
    assert "not transmitted or included" in readme
    assert "not a bounded-state production range coder" in readme
    quantized_tests = (
        ROOT / "tests" / "unit" / "test_quantized_predictive_coder.py"
    ).read_text(encoding="utf-8")
    assert 'module["main"]()' in quantized_tests


def test_v_information_path_preserves_source_local_scope_and_partial_evidence() -> None:
    concepts = _load_yaml(ROOT / "data" / "concepts.yml")
    sources = _load_yaml(ROOT / "data" / "sources.yml")
    extraction = _load_yaml(
        ROOT / "data" / "extractions" / "xu-et-al-usable-information-2020.yml"
    )

    concept_ids = {item["id"] for item in concepts["concepts"]}
    assert {"v-information", "mutual-information"} <= concept_ids

    source = next(
        item
        for item in sources["sources"]
        if item["id"] == "xu-et-al-usable-information-2020"
    )
    assert source["scan_status"] == "partially-scanned"
    assert extraction["pedagogical_model"]["reconstruction"]["status"] == "partial"

    source_graph_ids = {
        item["id"] for item in extraction["pedagogical_model"]["source_graph"]["nodes"]
    }
    assert {
        "src-predictive-family",
        "src-predictive-v-entropy",
        "src-v-information",
        "src-pac-estimation",
    } <= source_graph_ids
    assert source_graph_ids.isdisjoint(concept_ids)

    items = {item["id"].split(":")[-1]: item for item in extraction["items"]}
    assert items["predictive-family-definition"]["locator"]["label"] == "Definition 1"
    assert items["v-information-definition"]["locator"]["label"] == "Definition 3"
    assert items["pac-estimation"]["locator"]["label"] == "Theorem 1"
    assert "bounded log-probabilities" in " ".join(
        items["pac-estimation"]["evidence"]["assumptions"]
    )
