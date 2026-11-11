"""Regression tests for bilingual guided-route transition projection."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
GENERATOR: dict[str, Any] = runpy.run_path(
    str(ROOT / "site/tools/build_learning_map.py"),
    run_name="guided_route_transition_projection_test",
)

@pytest.mark.parametrize("language", ["fr", "en"])
def test_transition_projection_and_rendering_are_bilingual_and_separate_from_membership(
    language: str,
) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    transitions = GENERATOR["load_guided_route_transitions"](language, pages)
    index = GENERATOR["build_guided_route_transition_index"](transitions)

    generation_id = f"{language}/generation"
    cross_entropy_id = f"{language}/cross-entropy"
    generation = index[generation_id]
    cross_entropy = index[cross_entropy_id]
    assert len(generation) == 1
    assert len(cross_entropy) == 1
    assert generation[0].direction == "directed"
    assert cross_entropy[0].direction == "symmetric"
    assert generation[0].from_stage_title
    assert generation[0].to_stage_title
    assert generation[0].purpose
    assert cross_entropy[0].purpose

    generation_context = GENERATOR["render_guided_page_transitions"](generation, language)
    cross_entropy_context = GENERATOR["render_guided_page_transitions"](cross_entropy, language)
    assert "→" in generation_context
    assert "↔" in cross_entropy_context
    assert generation[0].from_stage_title in generation_context
    assert generation[0].to_stage_title in generation_context
    assert generation[0].purpose in generation_context
    assert "predictive-distribution-to-generation" not in generation_context
    assert "observed-target-to-training-objective" not in cross_entropy_context

    memberships = GENERATOR["build_guided_route_memberships"](stages)
    assert [(item.stage_id, item.role) for item in memberships[generation_id]] == [
        ("orientation", "core"),
        ("inference", "core"),
    ]
    assert [(item.stage_id, item.role) for item in memberships[cross_entropy_id]] == [
        ("scoring", "core"),
        ("training", "optional"),
    ]
    # Mentioning corpus preparation does not create a transition or Build membership.
    assert f"{language}/text-data" not in index
    assert f"{language}/build-path" not in memberships


@pytest.mark.parametrize("language", ["fr", "en"])
def test_transition_context_is_added_only_to_declared_transition_pages(language: str) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    transitions = GENERATOR["load_guided_route_transitions"](language, pages)
    fragments = GENERATOR["prepare_guided_page_context_fragments"](language, stages, transitions)
    by_name = {path.name: content for path, content in fragments.items()}

    generation = by_name[f"generated-guided-context-{language}-generation.qmd"]
    cross_entropy = by_name[f"generated-guided-context-{language}-cross-entropy.qmd"]
    text_data = by_name[f"generated-guided-context-{language}-text-data.qmd"]

    assert "guided-page-context--multiple" in generation
    assert "guided-page-transitions" in generation
    assert "guided-page-transitions" in cross_entropy
    assert "guided-page-transitions" not in text_data


def test_transition_rendering_escapes_authored_text_and_is_deterministic() -> None:
    transition = GENERATOR["ResolvedGuidedRouteTransition"](
        id="internal-only-id",
        from_stage_id="source-stage",
        from_stage_title='<script>alert("source")</script>',
        to_stage_id="target-stage",
        to_stage_title="Target & stage",
        direction="symmetric",
        purpose='<img src=x onerror="alert(1)">',
        pages=[GENERATOR["ResolvedPage"](id="en/example", title="Example", href="example.html")],
    )

    rendered = GENERATOR["render_guided_page_transitions"]([transition], "en")

    assert rendered == GENERATOR["render_guided_page_transitions"]([transition], "en")
    assert "&lt;script&gt;" in rendered
    assert "&lt;img" in rendered
    assert "<script>" not in rendered
    assert "<img" not in rendered
    assert "internal-only-id" not in rendered
    assert "↔" in rendered


def test_transition_index_supports_multiple_pages_and_multiple_transitions_per_page() -> None:
    page_a = GENERATOR["ResolvedPage"](id="en/a", title="A", href="a.html")
    page_b = GENERATOR["ResolvedPage"](id="en/b", title="B", href="b.html")
    first = GENERATOR["ResolvedGuidedRouteTransition"](
        id="first",
        from_stage_id="one",
        from_stage_title="One",
        to_stage_id="two",
        to_stage_title="Two",
        direction="directed",
        purpose="First relation",
        pages=[page_a, page_b],
    )
    second = GENERATOR["ResolvedGuidedRouteTransition"](
        id="second",
        from_stage_id="two",
        from_stage_title="Two",
        to_stage_id="three",
        to_stage_title="Three",
        direction="symmetric",
        purpose="Second relation",
        pages=[page_a],
    )

    index = GENERATOR["build_guided_route_transition_index"]([first, second])

    assert [item.id for item in index["en/a"]] == ["first", "second"]
    assert [item.id for item in index["en/b"]] == ["first"]
