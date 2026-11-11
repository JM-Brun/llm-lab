"""Tests for the canonical, bilingual guided-route transition model."""

from __future__ import annotations

import runpy
from copy import deepcopy
from pathlib import Path

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[2]
GENERATOR = runpy.run_path(
    str(ROOT / "site/tools/build_learning_map.py"),
    run_name="guided_route_transition_test",
)
TRANSITIONS = runpy.run_path(
    str(ROOT / "site/tools/guided_route_transitions.py"),
    run_name="guided_route_transition_validator_test",
)
validate_guided_route_transitions = TRANSITIONS["validate_guided_route_transitions"]


def route_payload() -> dict:
    from strict_yaml import load_yaml

    return load_yaml(ROOT / "data/guided-route.yml")


def published_ids() -> set[str]:
    return {page["id"] for page in GENERATOR["load_pages"]()}


@pytest.mark.parametrize("language", ["fr", "en"])
def test_route_document_uses_the_strict_transition_schema() -> None:
    document = GENERATOR["GuidedRouteDocument"].model_validate(route_payload())
    assert len(document.transitions) == 2
    assert document.transitions[0].id == "predictive-distribution-to-generation"


def test_reference_transitions_are_explicit_and_bilingual(language: str) -> None:
    transitions = validate_guided_route_transitions(route_payload(), published_ids())
    by_id = {item.id: item for item in transitions}

    generation = by_id["predictive-distribution-to-generation"]
    assert (generation.from_stage, generation.to_stage, generation.direction) == (
        "prediction",
        "inference",
        "directed"
    )
    assert getattr(generation.pages, language) == [f"{language}/generation"]
    assert getattr(generation.purpose, language)

    cross_entropy = by_id["observed-target-to-training-objective"]
    assert (cross_entropy.from_stage, cross_entropy.to_stage, cross_entropy.direction) == (
        "scoring",
        "training",
        "symmetric"
    )
    assert getattr(cross_entropy.pages, language) == [f"{language}/cross-entropy"]
    assert getattr(cross_entropy.purpose, language)


def test_one_page_can_explain_multiple_transitions_and_one_transition_multiple_pages() -> None:
    payload = route_payload()
    payload["transitions"][0]["pages"]["fr"].append("fr/decoding-strategies")
    payload["transitions"][0]["pages"]["en"].append("en/decoding-strategies")
    payload["transitions"].append(
        {
            "id": "generation-as-inference-example",
            "from": "orientation",
            "to": "inference",
            "direction": "directed",
            "pages": {"fr": ["fr/generation"], "en": ["en/generation"]},
            "purpose": {
                "fr": "Relier la vue d'ensemble à l'exécution détaillée.",
                "en": "Connect the overview to detailed execution.",
            },
        }
    )
    result = validate_guided_route_transitions(payload, published_ids())
    assert len(result[0].pages.fr) == 2
    assert [item.id for item in result if "fr/generation" in item.pages.fr] == [
        "predictive-distribution-to-generation",
        "generation-as-inference-example",
    ]


def test_unknown_endpoint_is_rejected() -> None:
    payload = route_payload()
    payload["transitions"][0]["to"] = "not-a-stage"
    with pytest.raises(ValueError, match="unknown stage"):
        validate_guided_route_transitions(payload, published_ids())


def test_missing_or_unpublished_page_is_rejected() -> None:
    payload = route_payload()
    payload["transitions"][0]["pages"]["fr"] = ["fr/not-published"]
    with pytest.raises(ValueError, match="unpublished or missing"):
        validate_guided_route_transitions(payload, published_ids())


def test_page_must_be_associated_with_an_endpoint_stage() -> None:
    payload = route_payload()
    payload["transitions"][0]["pages"]["fr"] = ["fr/text-data"]
    with pytest.raises(ValueError, match="at least one endpoint stage"):
        validate_guided_route_transitions(payload, published_ids())


def test_duplicate_transition_ids_are_rejected() -> None:
    payload = route_payload()
    payload["transitions"].append(deepcopy(payload["transitions"][0]))
    with pytest.raises(ValidationError, match="identifiers must be unique"):
        validate_guided_route_transitions(payload, published_ids())


def test_blank_bilingual_purpose_is_rejected() -> None:
    payload = route_payload()
    payload["transitions"][0]["purpose"]["en"] = "  "
    with pytest.raises(ValidationError, match="must not be blank"):
        validate_guided_route_transitions(payload, published_ids())


def test_ambiguous_direction_and_extra_fields_are_rejected() -> None:
    payload = route_payload()
    payload["transitions"][0]["direction"] = "maybe"
    with pytest.raises(ValidationError):
        validate_guided_route_transitions(payload, published_ids())
    payload = route_payload()
    payload["transitions"][0]["prerequisite"] = True
    with pytest.raises(ValidationError):
        validate_guided_route_transitions(payload, published_ids())
