"""Tests for source coverage and route-cycle checks in page metadata."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = next(
    path
    for path in (
        REPOSITORY_ROOT / "scripts" / "check_page_metadata.py",
        REPOSITORY_ROOT / "site" / "tools" / "check_page_metadata.py",
    )
    if path.is_file()
)
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


AUDIT_MODULE_PATH = next(
    path
    for path in (
        REPOSITORY_ROOT / "scripts" / "audit_page_metadata.py",
        REPOSITORY_ROOT / "site" / "tools" / "audit_page_metadata.py",
    )
    if path.is_file()
)
AUDIT_MODULE: dict[str, Any] = runpy.run_path(
    str(AUDIT_MODULE_PATH), run_name="page_metadata_audit_test"
)


def _audit_page(
    scope: str = "A sufficiently detailed scope about language model attention mechanisms.",
    purpose: str = (
        "Explain how attention mechanisms combine contextual information for prediction."
    ),
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
        "en/b": _audit_page(
            scope=shared_scope,
            purpose="A distinct learner outcome about sequence modelling and evaluation.",
        ),
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
    destination: str = "understand",
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
            "destination": destination,
            "level": "core",
        },
    }


def test_route_topology_separates_route_chains_from_hierarchy() -> None:
    pages = {
        "fr/start": _graph_page(
            "fr/start",
            following="fr/middle",
            children=["fr/branch-a", "fr/branch-b"],
        ),
        "fr/middle": _graph_page("fr/middle", previous="fr/start", following="fr/end"),
        "fr/end": _graph_page("fr/end", previous="fr/middle"),
        "fr/branch-a": _graph_page("fr/branch-a", destination="deepen"),
        "fr/branch-b": _graph_page("fr/branch-b", destination="deepen"),
        "en/start": _graph_page("en/start", following="en/end", language="en"),
        "en/end": _graph_page("en/end", previous="en/start", language="en"),
    }

    result = AUDIT_MODULE["route_topology"](pages)

    french = result["fr"]
    assert french["route_starts"] == ["fr/start"]
    assert french["route_ends"] == ["fr/end"]
    assert french["chains"] == [["fr/start", "fr/middle", "fr/end"]]
    assert french["outside_suggested_route_by_destination"]["deepen"] == [
        "fr/branch-a",
        "fr/branch-b",
    ]
    assert french["hierarchy_fan_out"] == [
        {"page": "fr/start", "children": ["fr/branch-a", "fr/branch-b"]}
    ]
    assert result["en"]["chains"] == [["en/start", "en/end"]]


def test_route_topology_reports_unrooted_components_and_convergence() -> None:
    pages = {
        "fr/a": _graph_page("fr/a", following="fr/c"),
        "fr/b": _graph_page("fr/b", following="fr/c"),
        "fr/c": _graph_page("fr/c", previous="fr/b"),
        "fr/x": _graph_page("fr/x", previous="fr/y", following="fr/y"),
        "fr/y": _graph_page("fr/y", previous="fr/x", following="fr/x"),
    }

    result = AUDIT_MODULE["route_topology"](pages)["fr"]

    assert result["route_merges"] == [{"page": "fr/c", "incoming_from": ["fr/a", "fr/b"]}]
    assert result["unrooted_route_pages"] == ["fr/x", "fr/y"]


def test_report_discloses_existing_metadata_validator_findings() -> None:
    result = AUDIT_MODULE["audit_pages"](
        {"fr/isolated": _graph_page("fr/isolated")},
        ["topic 'attention': FR/EN suggested-route next differs"],
    )

    report = AUDIT_MODULE["render_report"](result)

    assert "Structural metadata validator" in report
    assert "FR/EN suggested-route next differs" in report
    assert "Hierarchy fan-out is not a route" in report


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
