"""Tests for the guided route's page-to-stage membership projection."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
GENERATOR: dict[str, Any] = runpy.run_path(
    str(ROOT / "site/tools/build_learning_map.py"),
    run_name="guided_route_membership_test",
)


def test_membership_projection_preserves_core_optional_and_multiple_contexts(
    language: str,
) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    memberships = GENERATOR["build_guided_route_memberships"](stages)

    stage_ids = [stage.id for stage in stages]
    assert stage_ids[0] == "orientation"
    assert len(stage_ids) == len(set(stage_ids))
    assert all(stage.pages for stage in stages)

    generation = memberships[f"{language}/generation"]
    assert [(item.stage_id, item.role) for item in generation] == [
        ("orientation", "core"),
        ("inference", "core"),
    ]

    context_use = memberships[f"{language}/in-context-learning"]
    assert [(item.stage_id, item.role) for item in context_use] == [("context-use", "core")]
    context_engineering = memberships[f"{language}/context-engineering"]
    assert [(item.stage_id, item.role) for item in context_engineering] == [("context-use", "core")]

    text_input = memberships[f"{language}/text-data"]
    assert [(item.stage_id, item.role) for item in text_input] == [("text-input", "core")]

    tokenization = memberships[f"{language}/tokenization-strategies"]
    assert [(item.stage_id, item.role) for item in tokenization] == [("text-input", "optional")]

    entropy = memberships[f"{language}/entropy"]
    assert [(item.stage_id, item.role) for item in entropy] == [("prediction", "core")]

    likelihood = (
        memberships[f"{language}/vraisemblance"]
        if language == "fr"
        else memberships[f"{language}/likelihood"]
    )
    assert [(item.stage_id, item.role) for item in likelihood] == [("scoring", "core")]

    cross_entropy = memberships[f"{language}/cross-entropy"]
    assert [(item.stage_id, item.role) for item in cross_entropy] == [
        ("scoring", "core"),
        ("training", "optional"),
    ]

    # Training-example construction belongs to the independent Build path,
    # not to the conceptual Theory route.
    assert f"{language}/training-examples" not in memberships

    optional_page = f"{language}/transformer-architectures"
    assert [(item.stage_id, item.role) for item in memberships[optional_page]] == [
        ("orientation", "optional")
    ]

    core_page = f"{language}/embedding-space"
    assert [(item.stage_id, item.role) for item in memberships[core_page]] == [
        ("representations", "core")
    ]

    optional_attention_depth = f"{language}/attention-score-scaling"
    assert [(item.stage_id, item.role) for item in memberships[optional_attention_depth]] == [
        ("computation", "optional")
    ]

    assert f"{language}/build-path" not in memberships
    practice_page = (
        f"{language}/evaluation-experimentale"
        if language == "fr"
        else f"{language}/experimental-evaluation"
    )
    assert practice_page not in memberships


def test_membership_projection_keeps_empty_membership_absent() -> None:
    stages = [
        GENERATOR["ResolvedGuidedRouteStage"](
            id="one",
            title="Stage one",
            objective="An objective",
            pages=[GENERATOR["ResolvedPage"](id="en/core", title="Core", href="core.html")],
            optional_pages=[
                GENERATOR["ResolvedPage"](id="en/optional", title="Optional", href="optional.html")
            ],
        )
    ]

    memberships = GENERATOR["build_guided_route_memberships"](stages)

    assert set(memberships) == {"en/core", "en/optional"}
    assert memberships["en/core"][0].role == "core"
    assert memberships["en/optional"][0].role == "optional"
    assert "en/unassigned" not in memberships


@pytest.mark.parametrize("language", ["fr", "en"])
