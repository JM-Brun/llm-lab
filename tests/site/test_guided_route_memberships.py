"""Validate the explicit page-to-stage membership projection."""

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


@pytest.mark.parametrize("language", ["fr", "en"])
def test_membership_projection_preserves_core_optional_and_multiple_contexts(
    language: str,
) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    memberships = GENERATOR["build_guided_route_memberships"](stages)

    generation = memberships[f"{language}/generation"]
    assert [(item.stage_id, item.role) for item in generation] == [
        ("orientation", "core"),
        ("prediction", "core"),
    ]

    optional_page = f"{language}/transformer-architectures"
    assert [(item.stage_id, item.role) for item in memberships[optional_page]] == [
        ("orientation", "optional")
    ]

    core_page = f"{language}/embedding-space"
    assert [(item.stage_id, item.role) for item in memberships[core_page]] == [
        ("representations", "core")
    ]

    assert f"{language}/build-path" not in memberships
    practice_page = (
        f"{language}/evaluation-experimentale"
        if language == "fr"
        else f"{language}/experimental-evaluation"
    )
    assert practice_page in memberships


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
def test_guided_route_stage_anchors_are_stable(language: str) -> None:
    pages = [
        page
        for page in GENERATOR["load_pages"]()
        if page["language"] in {language, "shared"}
    ]
    stages = GENERATOR["load_guided_route"](language, pages)
    rendered = GENERATOR["render_guided_route_markdown"](stages, language)

    for stage in stages:
        assert f"#guided-stage-{stage.id}" in rendered


def test_single_membership_renders_as_context_not_as_a_parent_claim() -> None:
    membership = GENERATOR["GuidedRouteMembership"](
        stage_id="representations",
        stage_title="From IDs to representations",
        stage_objective="Trace embedding lookup and contextualization.",
        role="optional",
    )
    page = GENERATOR["ResolvedPage"](
        id="en/rope", title="Rotary Position Embeddings", href="rope.html"
    )

    rendered = GENERATOR["render_guided_page_context_markdown"](page, [membership], "en")

    assert '<nav class="guided-page-context"' in rendered
    assert 'href="learning-map.html#guided-stage-representations"' in rendered
    assert 'aria-current="page">Rotary Position Embeddings</li>' in rendered
    assert "Optional resource" in rendered


def test_multiple_memberships_are_all_rendered_with_their_purposes() -> None:
    memberships = [
        GENERATOR["GuidedRouteMembership"](
            stage_id="orientation",
            stage_title="Orient yourself",
            stage_objective="Observe a complete generation loop.",
            role="core",
        ),
        GENERATOR["GuidedRouteMembership"](
            stage_id="prediction",
            stage_title="From hidden states to predictions",
            stage_objective="Connect logits, probabilities and next-token selection.",
            role="core",
        ),
    ]
    page = GENERATOR["ResolvedPage"](
        id="en/generation", title="Text generation", href="generation.html"
    )

    rendered = GENERATOR["render_guided_page_context_markdown"](page, memberships, "en")

    assert "guided-page-context--multiple" in rendered
    assert "guided-stage-orientation" in rendered
    assert "guided-stage-prediction" in rendered
    assert "Observe a complete generation loop." in rendered
    assert "Connect logits, probabilities and next-token selection." in rendered
    assert "Core stage" in rendered


def test_page_without_route_membership_has_no_context_fragment() -> None:
    page = GENERATOR["ResolvedPage"](
        id="en/build-path", title="Build a small GPT", href="build-path.html"
    )

    assert GENERATOR["render_guided_page_context_markdown"](page, [], "en") == ""
