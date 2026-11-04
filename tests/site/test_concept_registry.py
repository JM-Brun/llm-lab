"""Tests for the controlled concept registry."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import yaml

MODULE_PATH = Path(__file__).resolve().parents[2] / "site" / "tools" / "check_concept_registry.py"
MODULE: dict[str, Any] = runpy.run_path(str(MODULE_PATH), run_name="concept_registry_test")
validate_registry = MODULE["validate_registry"]
validate_domains = MODULE["validate_domains"]


def _valid_registry() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "concepts": [
            {
                "id": "token",
                "labels": {"fr": "Token", "en": "Token"},
                "definitions": {"fr": "Unité discrète.", "en": "Discrete unit."},
                "domains": ["architectures-mechanisms"],
                "resources": ["fr/text-data", "en/text-data"],
            },
            {
                "id": "embedding",
                "labels": {"fr": "Plongement", "en": "Embedding"},
                "definitions": {"fr": "Vecteur.", "en": "Vector."},
                "domains": ["mathematical-tools-geometry"],
                "resources": ["fr/embedding-space", "en/embedding-space"],
            },
        ],
        "relations": [{"from": "token", "type": "implemented-by", "to": "embedding"}],
    }


def test_checked_in_registry_is_valid() -> None:
    registry_path = Path(__file__).resolve().parents[2] / "data" / "concepts.yml"
    data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    published_pages = MODULE["_published_page_ids"]()
    domain_data = yaml.safe_load((registry_path.parent / "domains.yml").read_text(encoding="utf-8"))
    domain_ids, domain_errors = validate_domains(domain_data)
    assert domain_errors == []
    assert validate_registry(data, published_pages, domain_ids) == []


def test_registry_rejects_duplicate_ids_and_unknown_relation_endpoints() -> None:
    data = _valid_registry()
    data["concepts"].append(data["concepts"][0].copy())
    data["relations"].append({"from": "missing", "type": "part-of", "to": "token"})
    errors = validate_registry(data)
    assert any("duplicate identifier" in error for error in errors)
    assert any("unknown concept" in error for error in errors)


def test_registry_rejects_missing_translation_and_self_relation() -> None:
    data = _valid_registry()
    data["concepts"][0]["labels"].pop("en")
    data["relations"] = [{"from": "token", "type": "part-of", "to": "token"}]
    errors = validate_registry(data)
    assert any("expected exactly fr and en" in error for error in errors)
    assert any("self-relations" in error for error in errors)


def test_registry_rejects_duplicate_and_unpublished_resource_ids() -> None:
    data = _valid_registry()
    data["concepts"][0]["resources"] = [
        "fr/text-data",
        "fr/text-data",
        "fr/not-published",
    ]

    errors = validate_registry(data, {"fr/text-data", "en/text-data"})

    assert any("duplicate resource IDs" in error for error in errors)
    assert any("not a published page" in error for error in errors)


def test_registry_requires_resources_in_both_languages() -> None:
    data = _valid_registry()
    data["concepts"][0]["resources"] = ["fr/text-data"]

    errors = validate_registry(data)

    assert any("missing language(s) en" in error for error in errors)
    data["concepts"][0]["resources"] = ["en/text-data"]
    errors = validate_registry(data)
    assert any("missing language(s) fr" in error for error in errors)


def test_cycle_detection_handles_long_chains_without_recursion() -> None:
    length = 1500
    edges = {f"concept-{index}": [f"concept-{index + 1}"] for index in range(length - 1)}
    assert not MODULE["_has_cycle"](edges)

    edges[f"concept-{length - 1}"] = ["concept-0"]
    assert MODULE["_has_cycle"](edges)


def test_registry_handles_malformed_relation_value_types() -> None:
    data = _valid_registry()
    data["relations"] = [{"from": [], "type": {}, "to": None}]

    errors = validate_registry(data)

    assert any(".from: unknown concept" in error for error in errors)
    assert any(".to: unknown concept" in error for error in errors)
    assert any(".type: unsupported relation" in error for error in errors)


def test_registry_rejects_duplicate_relations_and_prerequisite_cycles() -> None:
    data = _valid_registry()
    data["relations"] = [
        {"from": "token", "type": "prerequisite", "to": "embedding"},
        {"from": "embedding", "type": "prerequisite", "to": "token"},
        {"from": "token", "type": "prerequisite", "to": "embedding"},
    ]

    errors = validate_registry(data)

    assert any("duplicate relation" in error for error in errors)
    assert any("prerequisite graph must be acyclic" in error for error in errors)


def test_generalization_cycles_are_rejected_but_application_cycles_are_allowed() -> None:
    data = _valid_registry()
    data["relations"] = [
        {"from": "token", "type": "generalizes", "to": "embedding"},
        {"from": "embedding", "type": "generalizes", "to": "token"},
        {"from": "token", "type": "applies-to", "to": "embedding"},
        {"from": "embedding", "type": "applies-to", "to": "token"},
    ]

    errors = validate_registry(data)

    assert any("generalization graph must be acyclic" in error for error in errors)
    assert not any("applies-to" in error for error in errors)


def test_domain_registry_rejects_missing_bilingual_fields_and_duplicate_ids() -> None:
    data = {
        "schema_version": 1,
        "domains": [
            {
                "id": "architectures-mechanisms",
                "labels": {"fr": "Architectures", "en": "Architectures"},
                "descriptions": {"fr": "Structures."},
                "guiding_questions": {"fr": "Pourquoi ?", "en": "Why?"},
            },
            {
                "id": "architectures-mechanisms",
                "labels": {"fr": "Autre", "en": "Other"},
                "descriptions": {"fr": "Autre.", "en": "Other."},
                "guiding_questions": {"fr": "Pourquoi ?", "en": "Why?"},
            },
        ],
    }

    identifiers, errors = validate_domains(data)

    assert "architectures-mechanisms" in identifiers
    assert any("expected exactly fr and en" in error for error in errors)
    assert any("duplicate identifier" in error for error in errors)
    assert any("six controlled domain IDs" in error for error in errors)


def test_concept_domain_membership_is_required_and_resolved() -> None:
    data = _valid_registry()
    data["concepts"][0]["domains"] = ["unknown-domain"]
    data["concepts"][1]["domains"] = []

    errors = validate_registry(data, domain_ids={"architectures-mechanisms"})

    assert any("unknown domain" in error for error in errors)
    assert any(".domains: expected a non-empty list" in error for error in errors)


def test_concept_can_belong_to_multiple_domains() -> None:
    data = _valid_registry()
    data["concepts"][0]["domains"] = [
        "architectures-mechanisms",
        "mathematical-tools-geometry",
    ]

    errors = validate_registry(
        data,
        domain_ids={"architectures-mechanisms", "mathematical-tools-geometry"},
    )

    assert errors == []


def test_symmetric_contrast_relation_uses_one_canonical_orientation() -> None:
    data = _valid_registry()
    data["relations"] = [{"from": "embedding", "type": "contrasts-with", "to": "token"}]
    assert validate_registry(data) == []
    data["relations"].append({"from": "token", "type": "contrasts-with", "to": "embedding"})

    errors = validate_registry(data)

    assert any("canonical lexical order" in error for error in errors)
