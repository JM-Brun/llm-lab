"""Tests for the standards-aligned knowledge-graph export."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "export_knowledge_graph.py"
MODULE: dict[str, Any] = runpy.run_path(str(MODULE_PATH), run_name="knowledge_graph_export_test")
build_graph = MODULE["build_graph"]


def test_exports_first_class_resources_with_stable_ids_and_typed_metadata() -> None:
    payload = build_graph()
    graph = payload["@graph"]
    resources = [node for node in graph if node.get("@type") == "schema:SoftwareSourceCode"]
    assert len(resources) == 5
    by_id = {node["@id"].rsplit("/", maxsplit=1)[-1]: node for node in resources}
    assert set(by_id) == {
        "gpt-config-module",
        "gpt-ops-module",
        "transformer-block-module",
        "gpt-model-module",
        "gpt-generation-module",
    }

    block = by_id["transformer-block-module"]
    assert block["schema:inLanguage"] == "en"
    assert block["schema:programmingLanguage"] == "Python"
    assert {item["@value"] for item in block["schema:name"]} == {
        "Bloc Transformer de référence",
        "Reference Transformer block",
    }
    assert "schema:codeRepository" not in block
    assert "dcterms:license" not in block


def test_resource_concept_and_bilingual_page_links_resolve() -> None:
    payload = build_graph()
    graph = payload["@graph"]
    identifiers = {node["@id"] for node in graph}
    by_id = {
        node["@id"].rsplit("/", maxsplit=1)[-1]: node
        for node in graph
        if node.get("@type") == "schema:SoftwareSourceCode"
    }
    block = by_id["transformer-block-module"]
    assert {
        "https://jm-brun.github.io/llm-lab/id/concept/self-attention",
        "https://jm-brun.github.io/llm-lab/id/concept/causal-mask",
    }.issubset({item["@id"] for item in block["schema:about"]})
    assert {
        "https://jm-brun.github.io/llm-lab/fr/transformer-block-walkthrough.html",
        "https://jm-brun.github.io/llm-lab/en/transformer-block-walkthrough.html",
    }.issubset({item["@id"] for item in block["schema:subjectOf"]})
    for key in ("schema:about", "schema:subjectOf"):
        for reference in block[key]:
            assert reference["@id"] in identifiers

    logits_uri = "https://jm-brun.github.io/llm-lab/id/concept/logits"
    model = by_id["gpt-model-module"]
    generation = by_id["gpt-generation-module"]
    assert logits_uri in {item["@id"] for item in model["schema:about"]}
    assert logits_uri in {item["@id"] for item in generation["schema:about"]}


def test_page_nodes_are_unique_and_registry_is_in_export_provenance() -> None:
    payload = build_graph()
    graph = payload["@graph"]
    page_ids = [
        node["@id"]
        for node in graph
        if isinstance(node.get("@type"), list) and "schema:WebPage" in node["@type"]
    ]
    assert len(page_ids) == len(set(page_ids))
    export = next(
        node
        for node in graph
        if node.get("@id") == "https://jm-brun.github.io/llm-lab/knowledge-graph.jsonld"
    )
    derived_from = {item["@id"] for item in export["prov:wasDerivedFrom"]}
    assert "https://github.com/JM-Brun/llm-lab/blob/main/data/resources.yml" in derived_from
