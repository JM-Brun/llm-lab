"""Tests for the guided learning route."""

from __future__ import annotations

import runpy
from html import escape
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
GENERATOR: dict[str, Any] = runpy.run_path(
    str(ROOT / "site/tools/build_learning_map.py"),
    run_name="guided_route_membership_test",
)


@pytest.mark.parametrize("language", ["fr", "en"])
def test_every_route_member_wires_exactly_its_generated_context_include(language: str) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    memberships = GENERATOR["build_guided_route_memberships"](stages)

    expected_occurrences = sum(len(stage.pages) + len(stage.optional_pages) for stage in stages)
    assert sum(len(page_memberships) for page_memberships in memberships.values()) == (
        expected_occurrences
    )

    expected_page_ids = set(memberships)
    observed_page_ids: set[str] = set()
    for source in (GENERATOR["SITE"] / language).glob("*.qmd"):
        page_id = f"{language}/{source.stem}"
        includes = [
            line.strip()
            for line in source.read_text(encoding="utf-8").splitlines()
            if "generated-guided-context-" in line
        ]
        if page_id in expected_page_ids:
            expected_include = (
                "{{< include ../includes/generated-guided-context-"
                f"{page_id.replace('/', '-')}.qmd >}}}}"
            )
            assert includes == [expected_include], source
            observed_page_ids.add(page_id)
        else:
            assert not includes, source

    assert observed_page_ids == expected_page_ids


@pytest.mark.parametrize("language", ["fr", "en"])
def test_context_use_pages_include_their_generated_suggested_route(language: str) -> None:
    for page_id in ("in-context-learning", "context-engineering"):
        source_path = ROOT / "site" / language / f"{page_id}.qmd"
        source = source_path.read_text(encoding="utf-8")
        include_path = f"generated-suggested-route-{language}-{page_id}.qmd"
        assert source.count(include_path) == 1


@pytest.mark.parametrize(
    ("language", "expected_label"),
    [
        ("fr", "Étapes du parcours abordées dans ce panorama"),
        ("en", "Learning stages covered by this overview"),
    ],
)
def test_overview_preserves_cross_cutting_coverage_and_explicit_next_page(
    language: str, expected_label: str
) -> None:
    """Coverage is a set; Orientation membership and preferred continuation remain distinct."""
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    memberships = GENERATOR["build_guided_route_memberships"](stages)
    overview_id = f"{language}/llm-overview"
    overview = next(page for page in pages if page["id"] == overview_id)
    # The canonical route registry defines the stage set and order.
    # The overview is intentionally cross-cutting: it covers every stage.
    expected_stages = [stage.id for stage in stages]

    assert overview["covered_stages"] == expected_stages
    assert [(item.stage_id, item.role) for item in memberships[overview_id]] == [
        ("orientation", "core")
    ]
    fragments = GENERATOR["prepare_cross_cutting_coverage_fragments"](language, pages, stages)
    output_path = (
        GENERATOR["SITE"] / "includes" / (f"generated-guided-coverage-{language}-llm-overview.qmd")
    )
    coverage = fragments[output_path]
    assert expected_label in coverage
    assert coverage.count("<li>") == len(expected_stages)
    assert "<nav" not in coverage
    assert "<section" in coverage
    stage_positions = [coverage.index(f"guided-stage-{stage.id}") for stage in stages]
    assert stage_positions == sorted(stage_positions)

    source = (ROOT / "site" / language / "llm-overview.qmd").read_text(encoding="utf-8")
    coverage_include = (
        "{{< include ../includes/generated-guided-coverage-"
        f"{language}-llm-overview.qmd >}}"
    )
    suggested_route_include = (
        "{{< include ../includes/generated-suggested-route-"
        f"{language}-llm-overview.qmd >}}"
    )
    assert source.count(coverage_include) == 1
    assert source.count(suggested_route_include) == 1
    assert source.index(suggested_route_include) < source.index(coverage_include)
    assert source.index(coverage_include) < source.index("::: {.language-switch}")
    assert '<div class="route-nav-cards">' not in source

    route_fragments = GENERATOR["prepare_suggested_route_fragments"](language, pages, stages)
    route_path = (
        GENERATOR["SITE"] / "includes" / f"generated-suggested-route-{language}-llm-overview.qmd"
    )
    suggested_route = route_fragments[route_path]
    orientation = next(stage for stage in stages if stage.id == "orientation")
    expected_next_label = (
        f"Continuer {orientation.title} →"
        if language == "fr"
        else f"Continue {orientation.title} →"
    )
    assert suggested_route.count(expected_next_label) == 1
    generation_page = next(page for page in pages if page["id"] == f"{language}/generation")
    assert suggested_route.count(escape(generation_page["title"])) == 1
    generation_href = generation_page["href"].removesuffix(".html") + ".qmd"
    assert suggested_route.count(f'href="{generation_href}"') == 1


@pytest.mark.parametrize(
    ("language", "label", "href"),
    [
        ("fr", "glossaire des LLM et des Transformers", "glossary.qmd"),
        ("en", "LLM and Transformer glossary", "glossary.qmd"),
    ],
)
def test_overview_links_to_the_localized_glossary(language: str, label: str, href: str) -> None:
    """The overview offers a visible, language-localized route to terminology lookup."""
    source = (ROOT / "site" / language / "llm-overview.qmd").read_text(encoding="utf-8")
    assert f"[{label}]({href})" in source
