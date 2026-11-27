"""Protect the flat Understand and review sidebar projections."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import pytest
from strict_yaml import load_yaml

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
GENERATOR: dict[str, Any] = runpy.run_path(
    str(ROOT / "site/tools/build_learning_map.py"),
    run_name="flat_curriculum_sidebar_test",
)


def _sidebar(language: str) -> dict[str, Any]:
    config = load_yaml(SITE / "_quarto.yml")
    sidebars = config["website"]["sidebar"]
    return next(item for item in sidebars if item.get("id") == language)


def _section(sidebar: dict[str, Any], title: str) -> dict[str, Any]:
    return next(
        item
        for item in sidebar["contents"]
        if isinstance(item, dict) and item.get("section") == title
    )


def _page_paths(items: list[Any]) -> list[str]:
    """Collect page paths from a nested Quarto navigation section."""
    paths: list[str] = []
    for item in items:
        if isinstance(item, str):
            paths.append(item)
        elif isinstance(item, dict):
            href = item.get("href")
            if isinstance(href, str) and href.endswith(".qmd"):
                paths.append(href)
            paths.extend(_page_paths(item.get("contents", [])))
    return paths


def _direct_page_paths(items: list[Any]) -> list[str]:
    """Collect only direct page entries, excluding optional nested sections."""
    paths: list[str] = []
    for item in items:
        if isinstance(item, str):
            paths.append(item)
        elif isinstance(item, dict):
            href = item.get("href")
            if isinstance(href, str) and href.endswith(".qmd"):
                paths.append(href)
    return paths


@pytest.mark.parametrize(
    ("language", "understand_title", "review_title", "extra_review_pages"),
    [
        (
            "fr",
            "Comprendre les LLM",
            "Réviser",
            ["fr/synthese-entropie.qmd", "fr/revision-information-theory.qmd"],
        ),
        (
            "en",
            "Understand LLMs",
            "Review",
            ["en/entropy-synthesis.qmd", "en/revision-information-theory.qmd"],
        ),
    ],
)
def test_understand_and_review_sidebars_are_flat_canonical_projections(
    language: str,
    understand_title: str,
    review_title: str,
    extra_review_pages: list[str],
) -> None:
    sidebar = _sidebar(language)
    understand = _section(sidebar, understand_title)
    review = _section(sidebar, review_title)

    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    core_page_ids = [page.id for stage in stages for page in stage.pages]
    document = GENERATOR["GuidedRouteDocument"].model_validate(
        load_yaml(ROOT / "data/guided-route.yml")
    )
    contracts = GENERATOR["resolve_lesson_contracts"](document, stages, pages)
    review_page_ids = [contracts[page_id].synthesis.id for page_id in core_page_ids]

    expected_understand = [f"{page_id}.qmd" for page_id in core_page_ids]
    expected_review = [
        f"{language}/review-path.qmd",
        *(f"{page_id}.qmd" for page_id in review_page_ids),
        *extra_review_pages,
    ]

    assert _direct_page_paths(understand["contents"]) == expected_understand
    optional_title = (
        "Architectures et variantes (facultatif)"
        if language == "fr"
        else "Architecture comparison (optional)"
    )
    optional_sections = [
        item for item in understand["contents"] if isinstance(item, dict) and "section" in item
    ]
    assert optional_sections == [
        {
            "section": optional_title,
            "contents": [
                {
                    "text": (
                        "Comparer les architectures Transformer"
                        if language == "fr"
                        else "Compare Transformer architectures"
                    ),
                    "href": f"{language}/transformer-architectures.qmd",
                }
            ],
        }
    ]
    assert _page_paths(review["contents"]) == expected_review
    assert all(
        isinstance(item, dict) and set(item) == {"text", "href"}
        for item in understand["contents"]
        if "section" not in item
    )
    # Review entries intentionally retain their canonical path-only labels;
    # unlike the main learning path, they are not part of the compact-label pass.
    assert all(isinstance(item, str) for item in review["contents"])
    assert len(core_page_ids) == 21
    assert len(review_page_ids) == 21


@pytest.mark.parametrize(
    ("language", "understand_title", "deepen_title", "practice_title"),
    [
        ("fr", "Comprendre les LLM", "Approfondir", "S'exercer et expérimenter"),
        ("en", "Understand LLMs", "Deepen your understanding", "Practice and experiment"),
    ],
)
def test_foundational_lessons_are_not_misclassified_as_deep_dive_or_core_sidebar(
    language: str,
    understand_title: str,
    deepen_title: str,
    practice_title: str,
) -> None:
    sidebar = _sidebar(language)
    understand = _section(sidebar, understand_title)
    deepen = _section(sidebar, deepen_title)
    practice = _section(sidebar, practice_title)

    core_paths = set(_direct_page_paths(understand["contents"]))
    deepen_paths = set(_page_paths(deepen["contents"]))
    practice_paths = set(_page_paths(practice["contents"]))
    editorial_hub = (SITE / language / "deepen.qmd").read_text(encoding="utf-8")

    # These pages are foundational Understand lessons, not optional deep dives.
    # The Deepen hub may point to them as related lessons without reclassifying
    # them or adding them to the Deepen sidebar.
    for slug in ("transformer-architectures", "llm-limits", "post-training"):
        path = f"{language}/{slug}.qmd"
        assert path not in core_paths
        assert path not in deepen_paths
        assert f"({slug}.qmd)" in editorial_hub

    assert f"{language}/experience-information-theory.qmd" in practice_paths
    assert f"{language}/experience-information-theory.qmd" not in core_paths
