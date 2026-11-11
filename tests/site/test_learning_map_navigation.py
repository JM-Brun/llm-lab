"""Regression tests for Quarto sidebar-to-resource-map navigation projection."""

from typing import Any

import pytest
from build_learning_map import (
    SITE,
    final_core_page_id,
    load_guided_route,
    load_navigation,
    load_pages,
    load_sidebar_page_neighbors,
    prepare_suggested_route_fragments,
    render_suggested_route_markdown,
)


@pytest.mark.parametrize(
    ("language", "section_title", "entry_page", "child_pages"),
    [
        (
            "fr",
            "Des identifiants aux représentations",
            "fr/embedding-space",
            ["fr/positional-encoding", "fr/contextualized-representations"],
        ),
        (
            "en",
            "From IDs to representations",
            "en/embedding-space",
            ["en/positional-encoding", "en/contextualized-representations"],
        ),
    ],
)
def test_linked_sidebar_section_entry_is_projected_once(
    language: str,
    section_title: str,
    entry_page: str,
    child_pages: list[str],
) -> None:
    """A section href is its entry lesson, not an invisible or duplicated page."""
    pages = [{"id": page_id} for page_id in [entry_page, *child_pages]]
    navigation = load_navigation(language, pages)

    def find_section(sections: list[dict[str, Any]]) -> dict[str, Any] | None:
        for section in sections:
            if section["title"] == section_title:
                return section
            found = find_section(section.get("sections", []))
            if found is not None:
                return found
        return None

    def count_page(sections: list[dict[str, Any]], page_id: str) -> int:
        return sum(
            section["pages"].count(page_id) + count_page(section.get("sections", []), page_id)
            for section in sections
        )

    found = None
    for area in navigation:
        found = find_section(area["sections"])
        if found is not None:
            break

    assert found is not None
    assert found["pages"] == [entry_page, *child_pages]
    assert sum(count_page(area["sections"], entry_page) for area in navigation) == 1


@pytest.mark.parametrize("language", ["fr", "en"])
def test_sidebar_neighbors_match_quarto_order_independently_of_route_metadata(
    language: str,
) -> None:
    """A native sidebar transition must not be mistaken for a suggested route."""
    pages = load_pages()
    page_by_id = {page["id"]: page for page in pages}
    neighbors = load_sidebar_page_neighbors(language)

    text_data = f"{language}/text-data"
    gradients = f"{language}/gradients"
    assert neighbors[text_data]["next"] == f"{language}/embedding-space"
    assert page_by_id[text_data]["route"]["next"] == f"{language}/embedding-space"
    assert gradients in neighbors
    assert page_by_id[gradients]["route"]["next"] == f"{language}/training-loop"


def test_suggested_route_omits_only_directions_already_in_sidebar() -> None:
    """Matching destinations disappear; pedagogical-only destinations remain."""
    page = {
        "id": "fr/example",
        "route": {"previous": "fr/shared-previous", "next": "fr/sidebar-next"},
    }
    page_by_id = {
        "fr/shared-previous": {"title": "Shared previous", "href": "shared-previous.html"},
        "fr/sidebar-next": {"title": "Sidebar next", "href": "sidebar-next.html"},
    }

    rendered = render_suggested_route_markdown(
        page,
        page_by_id,
        "fr",
        sidebar_neighbors={"next": "fr/sidebar-next"},
    )

    assert "Shared previous" in rendered
    assert "Sidebar next" not in rendered
    assert "Étape précédente" in rendered
    assert "Étape suivante" not in rendered


def test_suggested_route_is_empty_when_both_directions_duplicate_sidebar() -> None:
    """Do not render an empty route-card wrapper after removing duplicate links."""
    page = {
        "id": "fr/example",
        "route": {"previous": "fr/previous", "next": "fr/next"},
    }
    page_by_id = {
        "fr/previous": {"title": "Previous", "href": "previous.html"},
        "fr/next": {"title": "Next", "href": "next.html"},
    }

    rendered = render_suggested_route_markdown(
        page,
        page_by_id,
        "fr",
        sidebar_neighbors={"previous": "fr/previous", "next": "fr/next"},
    )

    assert rendered == ""


@pytest.mark.parametrize("language", ["fr", "en"])
def test_guided_route_cards_remain_visible_when_quarto_has_same_destination(
    language: str,
) -> None:
    """Understand's pedagogical cards coexist with identical native Quarto links."""
    page = {
        "id": f"{language}/example",
        "route": {
            "previous": f"{language}/previous",
            "next": f"{language}/next",
        },
    }
    page_by_id = {
        f"{language}/previous": {"title": "Previous lesson", "href": "previous.html"},
        f"{language}/next": {"title": "Next lesson", "href": "next.html"},
    }
    rendered = render_suggested_route_markdown(
        page,
        page_by_id,
        language,
        sidebar_neighbors={"previous": f"{language}/previous", "next": f"{language}/next"},
        preserve_pedagogical_cards=True,
    )

    assert "Previous lesson" in rendered
    assert "Next lesson" in rendered
    previous_label = "← Étape précédente" if language == "fr" else "← Previous step"
    next_label = "Étape suivante →" if language == "fr" else "Next step →"
    assert previous_label in rendered
    assert next_label in rendered


@pytest.mark.parametrize("language", ["fr", "en"])
def test_every_core_guided_route_page_keeps_its_pedagogical_cards(language: str) -> None:
    """Derive navigation-card coverage from the canonical route, not a sample page."""
    pages = load_pages()
    stages = load_guided_route(language, pages)
    fragments = prepare_suggested_route_fragments(language, pages, stages)
    page_by_id = {page["id"]: page for page in pages}
    core_page_ids = {page.id for stage in stages for page in stage.pages}
    final_page_id = final_core_page_id(stages)

    assert core_page_ids
    for page_id in sorted(core_page_ids):
        page = page_by_id[page_id]
        fragment_path = (
            SITE / "includes" / (f"generated-suggested-route-{page_id.replace('/', '-')}.qmd")
        )
        rendered = fragments[fragment_path]
        route = page["route"]
        if route.get("previous") is not None:
            previous_label = "← Étape précédente" if language == "fr" else "← Previous step"
            assert previous_label in rendered, page_id
        if route.get("next") is not None:
            next_label = "Étape suivante →" if language == "fr" else "Next step →"
            assert next_label in rendered, page_id
            target = page_by_id[route["next"]]
            assert target["title"] in rendered, page_id
            assert target["href"].removesuffix(".html") + ".qmd" in rendered, page_id
        if page_id == final_page_id:
            continuation_label = (
                "Parcours terminé · ensuite : construire →"
                if language == "fr"
                else "Path complete · next: build →"
            )
            assert continuation_label in rendered, page_id
