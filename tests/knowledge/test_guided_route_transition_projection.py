"""Regression tests for bilingual guided-route transition projection."""

from __future__ import annotations

import runpy
from html import escape
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
    # Native <summary> must remain a single non-nested disclosure control.
    assert "<summary><a " not in cross_entropy_context
    summary_text = cross_entropy_context.split("<summary>", 1)[1].split("</summary>", 1)[0]
    assert "<a " not in summary_text
    assert cross_entropy_context.count('href="learning-map.html#guided-stage-') == 2
    assert 'class="guided-page-transitions__stages"' in cross_entropy_context
    assert escape(generation[0].from_stage_title) in generation_context
    assert escape(generation[0].to_stage_title) in generation_context
    assert escape(generation[0].purpose) in generation_context
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


def test_transition_visual_identity_is_distinct_from_stage_membership() -> None:
    styles = (ROOT / "site/styles.scss").read_text(encoding="utf-8")
    transition_start = styles.index(".guided-page-transitions {")
    transition_end = styles.index("/* Keep Quarto navigation text", transition_start)
    transition_styles = styles[transition_start:transition_end]

    assert "border-left: 4px dashed #7651A8" in transition_styles
    assert "background: #FAF8FD" in transition_styles
    assert ".guided-page-transitions__stages" in transition_styles
    assert "border-left: 2px dashed #A78BC9" in transition_styles
    # Membership remains its own green pill/context treatment.
    membership_start = styles.index(".guided-page-context {")
    membership_end = styles.index("/* Explanatory stage transitions", membership_start)
    membership_styles = styles[membership_start:membership_end]
    assert "#E5F1E8" in membership_styles
    assert "#7651A8" not in membership_styles


@pytest.mark.parametrize(
    ("language", "generation_title", "context_title", "text_data", "in_context", "likelihood"),
    [
        (
            "fr",
            "Exécuter l'inférence et générer du texte",
            "Exploiter et concevoir le contexte",
            "text-data.qmd",
            "in-context-learning.qmd",
            "vraisemblance.qmd",
        ),
        (
            "en",
            "Run inference and generate text",
            "Use and design context",
            "text-data.qmd",
            "in-context-learning.qmd",
            "likelihood.qmd",
        ),
    ],
)
def test_suggested_route_navigation_is_projected_per_stage_membership(
    language: str,
    generation_title: str,
    context_title: str,
    text_data: str,
    in_context: str,
    likelihood: str,
) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    contexts = GENERATOR["build_suggested_route_contexts"](stages)

    generation = contexts[f"{language}/generation"]
    assert len(generation) == 2
    orientation = next(item for item in generation if item["stage_id"] == "orientation")
    inference = next(item for item in generation if item["stage_id"] == "inference")
    assert orientation["previous"].id == f"{language}/llm-overview"
    assert orientation["next"].id == f"{language}/text-data"
    assert inference["previous"].id == f"{language}/entropy"
    assert inference["next"].id == f"{language}/in-context-learning"

    context_engineering = contexts[f"{language}/context-engineering"]
    assert len(context_engineering) == 1
    assert context_engineering[0]["stage_id"] == "context-use"
    assert context_engineering[0]["previous"].id == f"{language}/in-context-learning"
    assert (
        context_engineering[0]["next"].id
        == f"{language}/{'vraisemblance' if language == 'fr' else 'likelihood'}"
    )

    # The legacy global scoring chain remains intact; contextual navigation
    # supplies the additional branch without rewriting likelihood.previous.
    likelihood_page = next(
        page
        for page in pages
        if page["id"] == f"{language}/{'vraisemblance' if language == 'fr' else 'likelihood'}"
    )
    assert likelihood_page["route"]["previous"] == f"{language}/entropy"

    fragments = GENERATOR["prepare_suggested_route_fragments"](language, pages, stages)
    by_name = {path.name: content for path, content in fragments.items()}
    generation_html = by_name[f"generated-suggested-route-{language}-generation.qmd"]
    context_html = by_name[f"generated-suggested-route-{language}-context-engineering.qmd"]
    assert f'href="{text_data}"' in generation_html
    assert f'href="{in_context}"' in generation_html
    assert escape(generation_title) in generation_html
    assert escape(context_title) in context_html
    assert f'href="{likelihood}"' in context_html


@pytest.mark.parametrize("language", ["fr", "en"])
def test_contextual_route_keeps_optional_build_companion_at_terminal_page(language: str) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    fragments = GENERATOR["prepare_suggested_route_fragments"](language, pages, stages)
    by_name = {path.name: content for path, content in fragments.items()}
    terminal = by_name[f"generated-suggested-route-{language}-training-loop.qmd"]
    assert "build-path.qmd" in terminal
    assert (
        "voie complémentaire" in terminal
        if language == "fr"
        else "optional companion path" in terminal
    )
