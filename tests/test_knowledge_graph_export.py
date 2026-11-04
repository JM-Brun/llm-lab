"""Tests for the standards-aligned JSON-LD knowledge graph projection."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from export_knowledge_graph import (  # noqa: E402
    BASE,
    CONCEPT_SCHEME,
    DOMAIN_SCHEME,
    build_graph,
)


def test_export_has_stable_skos_schemes_and_bilingual_labels() -> None:
    payload = build_graph()
    nodes = {node.get("@id"): node for node in payload["@graph"] if "@id" in node}

    assert nodes[CONCEPT_SCHEME]["@type"] == "skos:ConceptScheme"
    assert nodes[DOMAIN_SCHEME]["@type"] == "skos:ConceptScheme"
    concept = nodes[f"{BASE}/id/concept/token"]
    assert concept["@type"] == "skos:Concept"
    assert {item["@language"] for item in concept["skos:prefLabel"]} == {"fr", "en"}


def test_export_describes_published_pages() -> None:
    payload = build_graph()
    pages = [
        node
        for node in payload["@graph"]
        if isinstance(node.get("@type"), list) and "schema:LearningResource" in node["@type"]
    ]

    assert pages
    assert all(node["schema:inLanguage"] in {"fr", "en"} for node in pages)
    assert all(node["schema:about"] for node in pages)
    assert all("schema:educationalLevel" not in node for node in pages)
    assert all("llmlab:editorialLevel" in node for node in pages)


def test_only_generalization_uses_skos_hierarchy() -> None:
    payload = build_graph()
    concept_nodes = [
        node
        for node in payload["@graph"]
        if str(node.get("@id", "")).startswith(f"{BASE}/id/concept/")
    ]

    assert any("skos:narrower" in node for node in concept_nodes)
    assert any("llmlab:prerequisite" in node for node in concept_nodes)
    assert all("skos:related" not in node for node in concept_nodes)


def test_export_provenance_names_canonical_sources() -> None:
    payload = build_graph()
    export = next(
        node for node in payload["@graph"] if node.get("@id") == f"{BASE}/data/knowledge-graph.jsonld"
    )

    assert export["@type"] == "prov:Entity"
    assert len(export["prov:wasDerivedFrom"]) == 3


def test_jsonld_context_is_explicit() -> None:
    payload: dict[str, Any] = build_graph()
    assert payload["@context"]["skos"] == "http://www.w3.org/2004/02/skos/core#"
    assert payload["@context"]["schema"] == "https://schema.org/"
    assert payload["@context"]["prov"] == "http://www.w3.org/ns/prov#"
