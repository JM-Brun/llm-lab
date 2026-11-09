"""Validate generated local navigation from canonical suggested-route metadata."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
GENERATOR: dict[str, Any] = runpy.run_path(
    str(ROOT / "site/tools/build_learning_map.py"),
    run_name="suggested_route_navigation_test",
)


def sample_pages() -> list[dict[str, Any]]:
    """Return a minimal bilingual route fixture."""
    return [
        {
            "id": "fr/current",
            "title": "Page courante",
            "href": "current.html",
            "language": "fr",
            "route": {"previous": "fr/previous", "next": "fr/next"},
        },
        {
            "id": "fr/previous",
            "title": "Étape précédente",
            "href": "previous.html",
            "language": "fr",
            "route": {"previous": None, "next": "fr/current"},
        },
        {
            "id": "fr/next",
            "title": "Étape suivante",
            "href": "next.html",
            "language": "fr",
            "route": {"previous": "fr/current", "next": None},
        },
    ]


def test_render_suggested_route_uses_metadata_titles_and_local_source_links() -> None:
    pages = sample_pages()
    page_by_id = {page["id"]: page for page in pages}

    rendered = GENERATOR["render_suggested_route_markdown"](pages[0], page_by_id, "fr")

    assert '<div class="route-nav-cards">' in rendered
    assert 'href="previous.qmd"' in rendered
    assert 'href="next.qmd"' in rendered
    assert "← Étape précédente" in rendered
    assert "Étape suivante →" in rendered
    assert "Étape précédente</span>" in rendered
    assert "Étape suivante</span>" in rendered


def test_render_suggested_route_uses_localized_english_labels() -> None:
    page = {
        "id": "en/current",
        "title": "Current page",
        "href": "current.html",
        "language": "en",
        "route": {"previous": "en/previous", "next": None},
    }
    previous = {
        "id": "en/previous",
        "title": "Previous lesson",
        "href": "previous.html",
        "language": "en",
        "route": {"previous": None, "next": "en/current"},
    }

    rendered = GENERATOR["render_suggested_route_markdown"](
        page, {page["id"]: page, previous["id"]: previous}, "en"
    )

    assert "← Previous step" in rendered
    assert "Previous lesson" in rendered
    assert "Étape précédente" not in rendered


def test_render_suggested_route_omits_pages_without_route_edges() -> None:
    page = {
        "id": "fr/isolated",
        "title": "Page isolée",
        "href": "isolated.html",
        "language": "fr",
        "route": {"previous": None, "next": None},
    }

    assert GENERATOR["render_suggested_route_markdown"](page, {page["id"]: page}, "fr") == ""


def test_render_suggested_route_rejects_unresolved_targets() -> None:
    page = {
        "id": "fr/current",
        "title": "Page courante",
        "href": "current.html",
        "language": "fr",
        "route": {"previous": None, "next": "fr/missing"},
    }

    with pytest.raises(ValueError, match="unresolved next route"):
        GENERATOR["render_suggested_route_markdown"](page, {page["id"]: page}, "fr")


@pytest.mark.parametrize("language", ["fr", "en"])
def test_writer_creates_page_specific_route_partials(language: str, tmp_path: Path) -> None:
    pages = sample_pages()
    if language == "en":
        pages = [
            {
                **page,
                "id": page["id"].replace("fr/", "en/"),
                "title": f"EN {page['title']}",
                "href": page["href"],
                "language": "en",
                "route": {
                    direction: target.replace("fr/", "en/") if isinstance(target, str) else None
                    for direction, target in page["route"].items()
                },
            }
            for page in pages
        ]

    namespace = GENERATOR["write_suggested_route_fragments"].__globals__
    original_site = namespace["SITE"]
    namespace["SITE"] = tmp_path
    try:
        outputs = GENERATOR["write_suggested_route_fragments"](language, pages)
    finally:
        namespace["SITE"] = original_site

    assert len(outputs) == 3
    expected = tmp_path / "includes" / f"generated-suggested-route-{language}-current.qmd"
    assert expected.is_file()
    rendered = expected.read_text(encoding="utf-8")
    assert "route-nav-cards" in rendered
    assert ("EN Étape précédente" if language == "en" else "Étape précédente") in rendered
    assert ("EN Étape suivante" if language == "en" else "Étape suivante") in rendered
