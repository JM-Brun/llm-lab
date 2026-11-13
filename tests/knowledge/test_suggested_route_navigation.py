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


def _last_page_fixture(language: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    last = {
        "id": f"{language}/last",
        "title": "Last",
        "href": "last.html",
        "route": {"previous": f"{language}/before", "next": None},
    }
    before = {"id": f"{language}/before", "title": "Before", "href": "before.html", "route": {}}
    build = {
        "id": f"{language}/build-path",
        "title": "Build <a small> GPT",
        "href": "build-path.html",
        "route": {},
    }
    return last, {page["id"]: page for page in (last, before, build)}


@pytest.mark.parametrize(
    ("language", "label"),
    [
        ("en", "Path complete · optional companion path: build a GPT →"),
        ("fr", "Parcours terminé · voie complémentaire : construire un GPT →"),
    ],
)
def test_last_route_page_offers_build_as_an_optional_companion_path(
    language: str, label: str
) -> None:
    last, page_by_id = _last_page_fixture(language)

    rendered = GENERATOR["render_suggested_route_markdown"](
        last, page_by_id, language, completes_route=True
    )

    assert rendered.count('<a class="route-nav-card"') == 2
    assert 'href="before.qmd"' in rendered
    assert 'href="build-path.qmd"' in rendered
    assert label in rendered
    assert "Build &lt;a small&gt; GPT" in rendered
    # One optional companion path; no implication that Build follows Understand as a requirement.
    # Do not repeat the site menu at the end of the page.
    assert "<ul" not in rendered
    assert "<li" not in rendered


def test_forward_card_never_competes_with_a_declared_next_page() -> None:
    last, page_by_id = _last_page_fixture("en")
    last["route"]["next"] = "en/before"

    rendered = GENERATOR["render_suggested_route_markdown"](
        last, page_by_id, "en", completes_route=True
    )

    assert "build-path.qmd" not in rendered


def test_forward_card_requires_a_published_build_path() -> None:
    last, page_by_id = _last_page_fixture("en")
    del page_by_id["en/build-path"]

    with pytest.raises(ValueError, match="unresolved continuation route"):
        GENERATOR["render_suggested_route_markdown"](last, page_by_id, "en", completes_route=True)


@pytest.mark.parametrize("language", ["fr", "en"])
def test_published_route_ends_with_exactly_one_forward_card(language: str) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] == language]
    stages = GENERATOR["load_guided_route"](language, pages)
    fragments = {
        path.name: text
        for path, text in GENERATOR["prepare_suggested_route_fragments"](
            language, pages, stages
        ).items()
    }
    label = GENERATOR["ROUTE_CONTINUATION_LABEL"][language]

    final_id = GENERATOR["final_core_page_id"](stages)
    assert final_id is not None
    final_name = f"generated-suggested-route-{final_id.replace('/', '-')}.qmd"
    assert label in fragments[final_name]
    assert [name for name, text in fragments.items() if label in text] == [final_name]
    source = (ROOT / "site" / f"{final_id}.qmd").read_text(encoding="utf-8")
    assert f"includes/{final_name}" in source


@pytest.mark.parametrize("language", ["fr", "en"])
def test_build_hub_prefers_the_first_guided_implementation_tour(language: str) -> None:
    pages = GENERATOR["load_pages"]()
    page_by_id = {page["id"]: page for page in pages}

    hub = page_by_id[f"{language}/build-path"]
    first_tour = page_by_id[f"{language}/gpt-config-walkthrough"]

    assert hub["route"]["next"] == first_tour["id"]
    practice_hub = page_by_id[f"{language}/exercises"]
    assert practice_hub["route"]["previous"] is None
    assert first_tour["route"]["previous"] == hub["id"]
    rendered = GENERATOR["render_suggested_route_markdown"](first_tour, page_by_id, language)
    expected_return = (
        "← Retour au parcours Build" if language == "fr" else "← Back to the Build path"
    )
    assert expected_return in rendered
    assert 'href="build-path.qmd"' in rendered


@pytest.mark.parametrize("language", ["fr", "en"])
def test_first_build_tour_keeps_visible_return_card_when_sidebar_has_same_parent(
    language: str,
) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] == language]
    fragments = GENERATOR["prepare_suggested_route_fragments"](language, pages)
    fragment_name = f"generated-suggested-route-{language}-gpt-config-walkthrough.qmd"
    rendered = next(content for path, content in fragments.items() if path.name == fragment_name)

    expected = "← Retour au parcours Build" if language == "fr" else "← Back to the Build path"
    assert '<div class="route-nav-cards">' in rendered
    assert 'href="build-path.qmd"' in rendered
    assert expected in rendered


@pytest.mark.parametrize(
    ("language", "page_id"),
    [
        ("fr", "training-examples"),
        ("en", "training-examples"),
        ("fr", "gpt-generation-walkthrough"),
        ("en", "gpt-generation-walkthrough"),
    ],
)
def test_build_terminal_pages_keep_explicit_return_links(language: str, page_id: str) -> None:
    pages = GENERATOR["load_pages"]()
    page = next(item for item in pages if item["id"] == f"{language}/{page_id}")

    assert page["route"]["next"] is None
    source_path = ROOT / "site" / language / f"{page_id}.qmd"
    source = source_path.read_text(encoding="utf-8")
    if page_id == "training-examples":
        expected = "Return to the Build path" if language == "en" else "Revenir au parcours Build"
        assert expected in source
    else:
        heading = "## Connections" if language == "en" else "## Connexions"
        expected = "Back to the Build path" if language == "en" else "Retour au parcours Build"
        connections = source.split(heading, maxsplit=1)[1].split("\n## ", maxsplit=1)[0]
        assert expected in connections


def test_published_build_page_inventory_is_bilingual_and_routes_resolve() -> None:
    pages = GENERATOR["load_pages"]()
    by_id = {page["id"]: page for page in pages}
    build_by_language = {
        language: {
            page["id"].split("/", maxsplit=1)[1]
            for page in pages
            if page["language"] == language and page["destination"] == "build"
        }
        for language in ("fr", "en")
    }

    assert build_by_language["fr"]
    assert build_by_language["fr"] == build_by_language["en"]

    for language in ("fr", "en"):
        build_pages = [
            page
            for page in pages
            if page["language"] == language and page["destination"] == "build"
        ]
        for page in build_pages:
            route = page["route"]
            assert route.get("previous") or route.get("next"), page["id"]
            for direction in ("previous", "next"):
                target_id = route.get(direction)
                if target_id is not None:
                    assert target_id in by_id, (page["id"], direction, target_id)
                    assert target_id.startswith(f"{language}/"), (page["id"], target_id)
