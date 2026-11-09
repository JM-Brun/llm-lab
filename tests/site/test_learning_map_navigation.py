"""Regression tests for Quarto sidebar-to-resource-map navigation projection."""

import pytest

from build_learning_map import load_navigation


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

    def find_section(sections: list[dict[str, object]]) -> dict[str, object] | None:
        for section in sections:
            if section["title"] == section_title:
                return section
            found = find_section(section.get("sections", []))  # type: ignore[arg-type]
            if found is not None:
                return found
        return None

    found = None
    for area in navigation:
        found = find_section(area["sections"])
        if found is not None:
            break

    assert found is not None
    assert found["pages"] == [entry_page, *child_pages]
    assert sum(
        page_id in section["pages"]
        for area in navigation
        for section in [*area["sections"]]
        for page_id in [entry_page]
    ) == 1
