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


"""Tests for the review-oriented page metadata audit."""

import runpy
from pathlib import Path
from typing import Any

AUDIT_MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "audit_page_metadata.py"
AUDIT_MODULE: dict[str, Any] = runpy.run_path(str(AUDIT_MODULE_PATH), run_name="page_metadata_audit_test")


def _audit_page(
    scope: str = "A sufficiently detailed scope about language model attention mechanisms.",
    purpose: str = "Explain how attention mechanisms combine contextual information for prediction.",
    *,
    language: str = "en",
    next_page: str | None = None,
    previous_page: str | None = None,
    parents: list[str] | None = None,
    children: list[str] | None = None,
    related: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "scope": scope,
        "purpose": purpose,
        "route": {"next": next_page, "previous": previous_page},
        "parents": parents or [],
        "children": children or [],
        "related": related or [],
        "tags": {"language": language},
    }


def test_lexical_overlap_is_zero_for_short_or_uninformative_text() -> None:
    assert AUDIT_MODULE["lexical_overlap"]("Attention and context", "Attention and context") == 0.0


def test_detects_high_scope_overlap_only_within_same_language() -> None:
    shared_scope = (
        "Explains language model attention mechanisms, contextual representations, "
        "query key value projections, and information aggregation."
    )
    pages = {
        "en/a": _audit_page(scope=shared_scope),
        "en/b": _audit_page(scope=shared_scope),
        "fr/c": _audit_page(scope=shared_scope, language="fr"),
    }

    result = AUDIT_MODULE["audit_pages"](pages)

    assert result["page_count"] == 3
    assert result["editorial_candidates"] == [
        {
            "language": "en",
            "field": "scope",
            "score": 1.0,
            "pages": ["en/a", "en/b"],
        }
    ]


def test_reports_a_truly_isolated_page_as_a_review_candidate() -> None:
    result = AUDIT_MODULE["audit_pages"]({"en/isolated": _audit_page()})

    assert result["isolated_pages"] == ["en/isolated"]
    report = AUDIT_MODULE["render_report"](result)
    assert "not necessarily misplaced" in report
    assert "`en/isolated`" in report


def test_does_not_flag_page_connected_by_route_as_isolated() -> None:
    pages = {
        "en/a": _audit_page(next_page="en/b"),
        "en/b": _audit_page(previous_page="en/a"),
    }

    result = AUDIT_MODULE["audit_pages"](pages)

    assert result["isolated_pages"] == []
