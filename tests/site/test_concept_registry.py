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
        "relation_types": {
            kind: {
                "direction": "symmetric" if kind in {"contrasts-with", "analogy"} else "directed",
                "family": (
                    "associative"
                    if kind in {"contrasts-with", "analogy"}
                    else "pedagogical"
                    if kind == "prerequisite"
                    else "structural"
                    if kind in {"part-of", "generalizes"}
                    else "functional"
                ),
                "transitive": kind in {"part-of", "generalizes"},
                "acyclic": kind in {"prerequisite", "part-of", "generalizes"},
                "learning_dependency": kind == "prerequisite",
                "inverse": None,
                "labels": {"fr": kind, "en": kind},
                "descriptions": {"fr": "Relation.", "en": "Relationship."},
            }
            for kind in MODULE["RELATION_TYPES"]
        },
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


def test_registry_requires_bilingual_definitions_for_used_relation_types() -> None:
    data = _valid_registry()
    data["relation_types"]["implemented-by"]["descriptions"].pop("en")
    errors = validate_registry(data)
    assert any(
        "relation_types.implemented-by.descriptions: expected exactly fr and en" in error
        for error in errors
    )

    data = _valid_registry()
    data["relation_types"].pop("implemented-by")
    errors = validate_registry(data)
    assert any("missing definitions for used types" in error for error in errors)


def test_registry_validates_relation_direction_metadata() -> None:
    data = _valid_registry()
    data["relation_types"]["implemented-by"]["direction"] = "symmetric"
    errors = validate_registry(data)
    assert any("is not defined as symmetric" in error for error in errors)


def test_relation_contract_requires_semantic_metadata() -> None:
    data = _valid_registry()
    data["relation_types"]["implemented-by"].pop("family")
    data["relation_types"]["implemented-by"].pop("transitive")
    data["relation_types"]["implemented-by"].pop("acyclic")
    data["relation_types"]["implemented-by"].pop("learning_dependency")

    errors = validate_registry(data)

    assert any(".family:" in error for error in errors)
    assert any(".transitive:" in error for error in errors)
    assert any(".acyclic:" in error for error in errors)
    assert any(".learning_dependency:" in error for error in errors)


def test_only_acyclic_relation_types_reject_cycles() -> None:
    data = _valid_registry()
    data["relations"] = [
        {"from": "token", "type": "part-of", "to": "embedding"},
        {"from": "embedding", "type": "part-of", "to": "token"},
        {"from": "token", "type": "applies-to", "to": "embedding"},
        {"from": "embedding", "type": "applies-to", "to": "token"},
    ]

    errors = validate_registry(data)

    assert any("part-of graph must be acyclic" in error for error in errors)
    assert not any("applies-to graph must be acyclic" in error for error in errors)


def test_learning_dependency_contract_must_be_directed_pedagogical_and_acyclic() -> None:
    data = _valid_registry()
    data["relation_types"]["prerequisite"]["family"] = "functional"
    data["relation_types"]["prerequisite"]["acyclic"] = False
    data["relation_types"]["prerequisite"]["direction"] = "symmetric"

    errors = validate_registry(data)

    assert any("learning_dependency: must be directed" in error for error in errors)
    assert any("learning_dependency: must be acyclic" in error for error in errors)
    assert any("learning_dependency: family must be pedagogical" in error for error in errors)


def test_inverse_relation_declarations_must_be_reciprocal() -> None:
    data = _valid_registry()
    data["relation_types"]["implemented-by"]["inverse"] = "applies-to"
    data["relation_types"]["applies-to"]["inverse"] = None

    errors = validate_registry(data)

    assert any("must point back" in error for error in errors)
