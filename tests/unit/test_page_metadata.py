"""Tests for source coverage and route-cycle checks in page metadata."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "check_page_metadata.py"
MODULE: dict[str, Any] = runpy.run_path(str(MODULE_PATH), run_name="page_metadata_test")


def _page(next_page: str | None, previous_page: str | None) -> dict[str, Any]:
    return {
        "route": {"next": next_page, "previous": previous_page},
        "parents": [],
        "children": [],
        "related": [],
        "tags": {"status": "published"},
    }


def test_rejects_a_closed_suggested_route_cycle() -> None:
    pages = {"fr/a": _page("fr/b", "fr/b"), "fr/b": _page("fr/a", "fr/a")}
    errors: list[str] = []
    MODULE["_validate_relations"](pages, errors)
    assert any("suggested_route: cycle detected" in error for error in errors)


def test_accepts_a_finite_suggested_route_chain() -> None:
    pages = {"fr/a": _page("fr/b", None), "fr/b": _page(None, "fr/a")}
    errors: list[str] = []
    MODULE["_validate_relations"](pages, errors)
    assert not errors


def test_flags_published_source_missing_from_quarto_render_list(tmp_path: Path) -> None:
    page = tmp_path / "fr" / "new-topic.qmd"
    page.parent.mkdir()
    page.write_text(
        "---\ntitle: New topic\n---\n\n"
        "<!--\nLLM-LAB-PAGE-MAP v1\n"
        "id: fr/new-topic\n"
        "tags:\n  - status:published\n"
        "-->\n",
        encoding="utf-8",
    )
    errors: list[str] = []
    MODULE["_validate_render_coverage"](tmp_path, set(), errors)
    assert errors == [
        "fr/new-topic.qmd: page is marked status:published but is absent from project.render"
    ]


def test_does_not_flag_planned_or_rendered_sources(tmp_path: Path) -> None:
    planned = tmp_path / "fr" / "planned.qmd"
    rendered = tmp_path / "fr" / "rendered.qmd"
    planned.parent.mkdir()
    for path, status in ((planned, "planned"), (rendered, "published")):
        path.write_text(
            f"<!--\nLLM-LAB-PAGE-MAP v1\ntags:\n  - status:{status}\n-->\n",
            encoding="utf-8",
        )
    errors: list[str] = []
    MODULE["_validate_render_coverage"](tmp_path, {"fr/rendered.qmd"}, errors)
    assert not errors
