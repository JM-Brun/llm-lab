"""Tests for the standards-aligned JSON-LD knowledge graph projection."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "site" / "tools"))

from check_knowledge_graph_rendered import validate_graph  # noqa: E402
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
    assert concept["llmlab:importance"] == "essential"


def test_export_describes_published_pages() -> None:
    payload = build_graph()
    pages = [
        node
        for node in payload["@graph"]
        if isinstance(node.get("@type"), list) and "schema:LearningResource" in node["@type"]
    ]

    assert pages
    assert all(node["schema:inLanguage"] in {"fr", "en"} for node in pages)
    assert any(node.get("schema:about") for node in pages)
    assert any(not node.get("schema:about") for node in pages)
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
    sources = [item["@id"] for item in export["prov:wasDerivedFrom"]]
    assert "https://github.com/JM-Brun/llm-lab/blob/main/data/concepts.yml" in sources
    assert "https://github.com/JM-Brun/llm-lab/blob/main/data/domains.yml" in sources
    assert "https://github.com/JM-Brun/llm-lab/blob/main/data/resources.yml" in sources
    assert any("/blob/main/src/llm_lab/foundations/" in source for source in sources)
    assert any("/blob/main/site/" in source and source.endswith(".qmd") for source in sources)
    assert not any("/tree/main/site" in source for source in sources)


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


def test_rendered_graph_validator_accepts_complete_references() -> None:
    payload = {
        "@context": {
            "skos": "urn:skos:",
            "schema": "urn:schema:",
            "prov": "urn:prov:",
            "dcterms": "urn:dcterms:",
            "llmlab": "urn:llmlab:",
        },
        "@graph": [
            {"@id": "https://jm-brun.github.io/llm-lab/id/scheme/concepts", "@type": "skos:ConceptScheme"},
            {
                "@id": "urn:concept",
                "@type": "skos:Concept",
                "llmlab:importance": "essential",
                "skos:inScheme": {"@id": "https://jm-brun.github.io/llm-lab/id/scheme/concepts"},
            },
            {
                "@id": "urn:page",
                "@type": ["schema:WebPage", "schema:LearningResource"],
                "schema:about": {"@id": "urn:concept"},
            },
            {
                "@id": "urn:source-code",
                "@type": "schema:SoftwareSourceCode",
                "schema:about": {"@id": "urn:concept"},
                "schema:subjectOf": {"@id": "urn:page"},
            },
            {"@id": f"{BASE}/knowledge-graph.jsonld", "@type": "prov:Entity"},
        ],
    }

    assert validate_graph(payload) == []


def test_rendered_graph_validator_requires_controlled_concept_importance() -> None:
    scheme_id = "https://jm-brun.github.io/llm-lab/id/scheme/concepts"
    payload = {
        "@context": {
            "skos": "urn:skos:",
            "schema": "urn:schema:",
            "prov": "urn:prov:",
            "dcterms": "urn:dcterms:",
            "llmlab": "urn:llmlab:",
        },
        "@graph": [
            {"@id": scheme_id, "@type": "skos:ConceptScheme"},
            {
                "@id": "https://jm-brun.github.io/llm-lab/id/concept/teacher-forcing",
                "@type": "skos:Concept",
                "skos:inScheme": {"@id": scheme_id},
            },
            {"@id": f"{BASE}/knowledge-graph.jsonld", "@type": "prov:Entity"},
        ],
    }

    errors = validate_graph(payload)

    assert any("missing or invalid llmlab:importance" in error for error in errors)


def test_rendered_graph_validator_reports_dangling_references() -> None:
    payload = {
        "@context": {
            "skos": "urn:skos:",
            "schema": "urn:schema:",
            "prov": "urn:prov:",
            "dcterms": "urn:dcterms:",
            "llmlab": "urn:llmlab:",
        },
        "@graph": [
            {"@id": "urn:scheme", "@type": "skos:ConceptScheme"},
            {
                "@id": "urn:concept",
                "@type": "skos:Concept",
                "skos:inScheme": {"@id": "urn:missing"},
            },
            {
                "@id": "urn:page",
                "@type": ["schema:WebPage", "schema:LearningResource"],
                "schema:about": {"@id": "urn:concept"},
            },
            {"@id": f"{BASE}/knowledge-graph.jsonld", "@type": "prov:Entity"},
        ],
    }

    errors = validate_graph(payload)
    assert any("urn:missing" in error for error in errors)


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


def test_page_nodes_are_unique_and_resource_registry_is_in_provenance() -> None:
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


def test_attention_subgraph_exports_intermediate_concepts_and_typed_relations() -> None:
    payload = build_graph()
    graph = payload["@graph"]
    identifiers = {node.get("@id") for node in graph}
    concept_ids = {
        "attention-score",
        "attention-weight",
        "scaled-dot-product-attention",
        "multi-head-attention",
    }

    for concept_id in concept_ids:
        assert f"{BASE}/id/concept/{concept_id}" in identifiers

    pages = {
        node["@id"]: node
        for node in graph
        if isinstance(node.get("@type"), list) and "schema:LearningResource" in node["@type"]
    }
    expected_pages = {
        f"{BASE}/fr/scaled-dot-product-attention.html": {
            "attention-score",
            "attention-weight",
            "scaled-dot-product-attention",
        },
        f"{BASE}/en/scaled-dot-product-attention.html": {
            "attention-score",
            "attention-weight",
            "scaled-dot-product-attention",
        },
        f"{BASE}/fr/transformer.html": {"multi-head-attention"},
        f"{BASE}/en/transformer.html": {"multi-head-attention"},
        f"{BASE}/fr/transformer-block-walkthrough.html": {"multi-head-attention"},
        f"{BASE}/en/transformer-block-walkthrough.html": {"multi-head-attention"},
    }
    for page_uri, expected_concepts in expected_pages.items():
        about = {
            item["@id"].rsplit("/", maxsplit=1)[-1] for item in pages[page_uri]["schema:about"]
        }
        assert expected_concepts.issubset(about)

    relations = {
        (node["@id"], predicate, value["@id"])
        for node in graph
        for predicate, value in node.items()
        if predicate.startswith("llmlab:") and isinstance(value, dict) and "@id" in value
    }
    assert (
        f"{BASE}/id/concept/softmax",
        "llmlab:produces",
        f"{BASE}/id/concept/attention-weight",
    ) in relations
    assert (
        f"{BASE}/id/concept/query",
        "llmlab:contributesTo",
        f"{BASE}/id/concept/attention-score",
    ) in relations
    assert (
        f"{BASE}/id/concept/key",
        "llmlab:contributesTo",
        f"{BASE}/id/concept/attention-score",
    ) in relations
    assert (
        f"{BASE}/id/concept/scaled-dot-product-attention",
        "llmlab:partOf",
        f"{BASE}/id/concept/multi-head-attention",
    ) in relations
    assert (
        f"{BASE}/id/concept/causal-mask",
        "llmlab:constrains",
        f"{BASE}/id/concept/scaled-dot-product-attention",
    ) in relations
    assert (
        f"{BASE}/id/concept/scaled-dot-product-attention",
        "llmlab:appliesTo",
        f"{BASE}/id/concept/self-attention",
    ) in relations
