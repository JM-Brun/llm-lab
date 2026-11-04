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


def _graph_page(
    page_id: str,
    *,
    previous: str | None = None,
    following: str | None = None,
    parents: list[str] | None = None,
    children: list[str] | None = None,
    related: list[str] | None = None,
    language: str = "fr",
    topic: str | None = None,
) -> dict[str, Any]:
    """Build a minimal published node for semantic page-graph tests."""
    return {
        "path": f"{page_id}.qmd",
        "id": page_id,
        "route": {"previous": previous, "next": following},
        "parents": parents or [],
        "children": children or [],
        "related": related or [],
        "tags": {
            "status": "published",
            "language": language,
            "topic": topic or page_id.split("/", maxsplit=1)[-1],
            "type": "concept-lesson",
            "destination": "understand",
            "level": "core",
        },
    }


def test_accepts_reciprocal_page_hierarchy() -> None:
    pages = {
        "fr/overview": _graph_page("fr/overview", children=["fr/attention"]),
        "fr/attention": _graph_page("fr/attention", parents=["fr/overview"]),
    }
    errors: list[str] = []

    MODULE["_validate_relations"](pages, errors)

    assert errors == []


def test_rejects_unknown_page_relation_target() -> None:
    pages = {
        "fr/attention": _graph_page("fr/attention", related=["fr/missing"]),
    }
    errors: list[str] = []

    MODULE["_validate_relations"](pages, errors)

    assert any("unknown page ID 'fr/missing'" in error for error in errors)


def test_rejects_non_reciprocal_hierarchy() -> None:
    pages = {
        "fr/overview": _graph_page("fr/overview", children=["fr/attention"]),
        "fr/attention": _graph_page("fr/attention"),
    }
    errors: list[str] = []

    MODULE["_validate_relations"](pages, errors)

    assert any("does not list 'fr/overview' as parent" in error for error in errors)


def test_rejects_hierarchy_cycle() -> None:
    pages = {
        "fr/a": _graph_page("fr/a", children=["fr/b"], parents=["fr/c"]),
        "fr/b": _graph_page("fr/b", children=["fr/c"], parents=["fr/a"]),
        "fr/c": _graph_page("fr/c", children=["fr/a"], parents=["fr/b"]),
    }
    errors: list[str] = []

    MODULE["_validate_relations"](pages, errors)

    assert any("hierarchy: cycle detected" in error for error in errors)


def test_bilingual_parity_uses_topic_identity_not_translated_slug() -> None:
    pages = {
        "fr/attention": _graph_page(
            "fr/attention", children=["fr/attention-scaled"], language="fr", topic="attention"
        ),
        "en/attention-mechanism": _graph_page(
            "en/attention-mechanism",
            children=["en/scaled-attention"],
            language="en",
            topic="attention",
        ),
        "fr/attention-scaled": _graph_page(
            "fr/attention-scaled", parents=["fr/attention"], language="fr", topic="scaled-attention"
        ),
        "en/scaled-attention": _graph_page(
            "en/scaled-attention",
            parents=["en/attention-mechanism"],
            language="en",
            topic="scaled-attention",
        ),
    }
    errors: list[str] = []

    MODULE["_validate_bilingual_parity"](pages, errors)

    assert errors == []


def test_bilingual_parity_detects_relation_divergence() -> None:
    pages = {
        "fr/attention": _graph_page(
            "fr/attention", children=["fr/attention-scaled"], language="fr", topic="attention"
        ),
        "en/attention": _graph_page("en/attention", language="en", topic="attention"),
        "fr/attention-scaled": _graph_page(
            "fr/attention-scaled", parents=["fr/attention"], language="fr", topic="scaled-attention"
        ),
        "en/attention-scaled": _graph_page(
            "en/attention-scaled", language="en", topic="scaled-attention"
        ),
    }
    errors: list[str] = []

    MODULE["_validate_bilingual_parity"](pages, errors)

    assert any("FR/EN children relations differ" in error for error in errors)
