"""Tests for the standards-aligned JSON-LD knowledge graph projection."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from export_knowledge_graph import (  # noqa: E402
    BASE,
    CONCEPT_SCHEME,
    DOMAIN_SCHEME,
    build_graph,
    relation_predicate,
    write_export,
)


def test_export_has_stable_skos_schemes_and_bilingual_labels() -> None:
    payload = build_graph()
    nodes = [node for node in payload["@graph"] if "@id" in node]

    assert any(
        node.get("@id") == CONCEPT_SCHEME and node.get("@type") == "skos:ConceptScheme"
        for node in nodes
    )
    assert any(
        node.get("@id") == DOMAIN_SCHEME and node.get("@type") == "skos:ConceptScheme"
        for node in nodes
    )
    concept = next(
        node
        for node in nodes
        if node.get("@id") == f"{BASE}/id/concept/token" and node.get("@type") == "skos:Concept"
    )
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


def test_relation_mapping_preserves_non_taxonomic_semantics() -> None:
    assert relation_predicate("generalizes") == "skos:narrower"
    assert relation_predicate("prerequisite") == "llmlab:prerequisite"
    assert relation_predicate("part-of") == "llmlab:partOf"
    assert relation_predicate("contrasts-with") == "llmlab:contrastsWith"


def test_export_provenance_names_canonical_sources() -> None:
    payload = build_graph()
    export = next(
        node for node in payload["@graph"] if node.get("@id") == f"{BASE}/knowledge-graph.jsonld"
    )

    assert export["@type"] == "prov:Entity"
    assert len(export["prov:wasDerivedFrom"]) == 3


def test_jsonld_context_is_explicit() -> None:
    payload: dict[str, Any] = build_graph()
    assert payload["@context"]["skos"] == "http://www.w3.org/2004/02/skos/core#"
    assert payload["@context"]["schema"] == "https://schema.org/"
    assert payload["@context"]["prov"] == "http://www.w3.org/ns/prov#"


def test_export_writes_valid_jsonld_deterministically() -> None:
    with TemporaryDirectory() as directory:
        output = Path(directory) / "knowledge-graph.jsonld"
        write_export(output)
        first = output.read_text(encoding="utf-8")
        assert json.loads(first)["@context"]["skos"] == "http://www.w3.org/2004/02/skos/core#"
        write_export(output)
        assert output.read_text(encoding="utf-8") == first
