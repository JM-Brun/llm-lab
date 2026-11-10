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


def _membership(stage_id: str, stage_index: int, title: str, role: str) -> Any:
    return GENERATOR["GuidedRouteMembership"](
        stage_id=stage_id,
        stage_index=stage_index,
        stage_title=title,
        stage_objective="objective",
        role=role,
    )


@pytest.mark.parametrize(
    ("language", "label"),
    [("en", "↩ Back to the learning path"), ("fr", "↩ Retour au parcours")],
)
def test_optional_resource_links_back_to_each_stage_that_lists_it(
    language: str, label: str
) -> None:
    page = {"id": f"{language}/extra", "title": "Extra", "href": "extra.html", "route": {}}

    rendered = GENERATOR["render_suggested_route_markdown"](
        page,
        {page["id"]: page},
        language,
        return_memberships=[
            _membership("representations", 3, "From IDs <to> vectors", "optional"),
            _membership("training", 8, "Learning", "optional"),
        ],
    )

    assert rendered.count("route-nav-card--return") == 2
    assert 'href="learning-map.html#guided-stage-representations"' in rendered
    assert 'href="learning-map.html#guided-stage-training"' in rendered
    assert label in rendered
    assert "03 · From IDs &lt;to&gt; vectors" in rendered
    assert "08 · Learning" in rendered


def test_optional_resource_does_not_surface_edges_from_another_reading_order() -> None:
    pages = sample_pages()
    page_by_id = {page["id"]: page for page in pages}

    rendered = GENERATOR["render_suggested_route_markdown"](
        page_by_id["fr/current"],
        page_by_id,
        "fr",
        return_memberships=[_membership("training", 8, "Apprentissage", "optional")],
    )

    assert "previous.qmd" not in rendered
    assert "next.qmd" not in rendered
    assert rendered.count('<a class="route-nav-card') == 1


@pytest.mark.parametrize(
    ("language", "title"),
    [
        ("en", "You have reached the end of the path"),
        ("fr", "Vous êtes arrivé au bout du parcours"),
    ],
)
def test_route_completion_block_offers_the_four_exits(language: str, title: str) -> None:
    rendered = GENERATOR["render_route_completion_markdown"](language)

    assert title in rendered
    # Quarto relocates <aside> into the margin column; the block must stay in the body.
    assert "<aside" not in rendered
    for href in ("build-path.qmd", "exercises.qmd", "deepen.qmd", "learning-map.qmd"):
        assert f'href="{href}"' in rendered
        assert (ROOT / "site" / language / href).is_file()


def test_route_completion_block_rejects_unknown_language() -> None:
    with pytest.raises(ValueError, match="unsupported suggested-route language"):
        GENERATOR["render_route_completion_markdown"]("de")


@pytest.mark.parametrize("language", ["fr", "en"])
def test_real_route_ends_with_a_closing_block_and_optional_pages_lead_back(
    language: str,
) -> None:
    """Guard the published route: no dead end, no optional page without a way back."""
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] == language]
    stages = GENERATOR["load_guided_route"](language, pages)
    fragments = {
        path.name: text
        for path, text in GENERATOR["prepare_suggested_route_fragments"](
            language, pages, stages
        ).items()
    }

    final_id = GENERATOR["final_core_page_id"](stages)
    assert final_id is not None
    final_name = f"generated-suggested-route-{final_id.replace('/', '-')}.qmd"
    assert 'class="route-complete"' in fragments[final_name]
    assert sum('class="route-complete"' in text for text in fragments.values()) == 1

    core_ids = {page.id for stage in stages for page in stage.pages}
    optional_only = {
        page.id for stage in stages for page in stage.optional_pages if page.id not in core_ids
    }
    assert optional_only
    for page_id in sorted({final_id, *optional_only}):
        name = f"generated-suggested-route-{page_id.replace('/', '-')}.qmd"
        if page_id in optional_only:
            assert "route-nav-card--return" in fragments[name], page_id
        source = (ROOT / "site" / f"{page_id}.qmd").read_text(encoding="utf-8")
        assert f"includes/{name}" in source, f"{page_id} does not include {name}"
