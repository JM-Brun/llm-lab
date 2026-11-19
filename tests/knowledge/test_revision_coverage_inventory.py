"""Tests for the generated Understand/Build revision inventory."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
AUDIT: dict[str, Any] = runpy.run_path(
    str(ROOT / "site/tools/audit_revision_coverage.py"),
    run_name="revision_coverage_test",
)


def page(page_id: str, language: str, destination: str, topic: str | None) -> dict[str, Any]:
    return {
        "id": page_id,
        "language": language,
        "destination": destination,
        "topic": topic,
        "level": "core",
        "type": "concept-lesson",
        "title": page_id,
        "href": page_id + ".html",
        "parents": [],
        "children": [],
        "related": [],
    }


def test_inventory_covers_every_published_understand_and_build_page() -> None:
    pages = AUDIT["load_pages"]()
    inventory = AUDIT["build_revision_inventory"](
        pages,
        AUDIT["registry_entries"](ROOT / "data/concepts.yml", "concepts"),
        AUDIT["registry_entries"](ROOT / "data/resources.yml", "resources"),
    )
    expected = {p["id"] for p in pages if p["destination"] in {"understand", "build"}}
    actual = {p["id"] for p in inventory["pages"]}
    assert actual == expected
    assert len(actual) == len(inventory["pages"])


def test_real_repository_inventory_projects_revision_links_and_assessments() -> None:
    project_index = AUDIT["ProjectIndex"].build(ROOT)
    revision_aids: dict[str, list[dict[str, str]]] = {}
    for edge in project_index.revision_edges:
        revision_aids.setdefault(edge.source_page_id, []).append(
            {"id": edge.aid_page_id, "role": edge.role}
        )
    inventory = AUDIT["build_revision_inventory"](
        AUDIT["load_pages"](),
        AUDIT["registry_entries"](ROOT / "data/concepts.yml", "concepts"),
        AUDIT["registry_entries"](ROOT / "data/resources.yml", "resources"),
        revision_support_by_page=project_index.revision_support_by_page,
        revision_aids_by_lesson=revision_aids,
    )

    understand = inventory["counts"]["understand"]
    build = inventory["counts"]["build"]
    assert understand["revision_aid_links"] == 4
    assert understand["pages_with_revision_aids"] == 4
    assert understand["revision_support_by_status"]["partial"] == 4
    assert understand["revision_support_by_status"]["integrated_sufficient"] == 24
    assert understand["revision_support_by_status"]["not_assessed"] == 18
    assert build["revision_support_by_status"] == {
        "integrated_sufficient": 4,
        "not_assessed": 12,
    }
    by_id = {page["id"]: page for page in inventory["pages"]}
    assert by_id["fr/entropy"]["revision_aids"][0]["id"] == "fr/revision-information-theory"
    assert by_id["en/cross-entropy"]["revision_support"]["status"] == "partial"
    assert by_id["fr/corpus-preparation"]["revision_support"]["status"] == "integrated_sufficient"
    assert by_id["en/training-examples"]["revision_support"]["status"] == "integrated_sufficient"


def test_understand_pages_without_membership_are_reported_not_dropped() -> None:
    pages = [page("fr/unlisted", "fr", "understand", "unlisted")]
    inventory = AUDIT["build_revision_inventory"](pages, [], [], route_memberships={})
    assert inventory["pages"][0]["route_status"] == "unrouted"


def test_build_inventory_does_not_invent_a_guided_route() -> None:
    inventory = AUDIT["build_revision_inventory"](
        [page("fr/build-example", "fr", "build", "implementation")],
        [],
        [],
        route_memberships={},
    )
    record = inventory["pages"][0]
    assert record["route_status"] == "not_applicable"
    assert record["revision_support"]["status"] == "not_assessed"


def test_revision_aids_and_assessments_are_projected_independently() -> None:
    pages = [
        page("fr/attention", "fr", "understand", "attention"),
        page("fr/revision-sheet", "fr", "practice", "attention-revision"),
    ]
    support = {
        "fr/attention": {
            "status": "partial",
            "evidence": [{"aid": "fr/revision-sheet", "note": "Core formulas are covered."}],
            "reason": None,
        }
    }
    aids = {"fr/attention": [{"id": "fr/revision-sheet", "role": "revision_sheet"}]}

    inventory = AUDIT["build_revision_inventory"](
        pages,
        [],
        [],
        route_memberships={},
        revision_support_by_page=support,
        revision_aids_by_lesson=aids,
    )
    record = next(item for item in inventory["pages"] if item["id"] == "fr/attention")

    assert record["revision_support"]["status"] == "partial"
    assert record["revision_aids"] == [
        {
            "id": "fr/revision-sheet",
            "role": "revision_sheet",
            "title": "fr/revision-sheet",
            "href": "fr/revision-sheet.html",
        }
    ]
    counts = inventory["counts"]["understand"]
    assert counts["pages_with_revision_aids"] == 1
    assert counts["revision_aid_links"] == 1
    assert counts["revision_support_by_status"] == {"partial": 1}


def test_inventory_rejects_revision_aid_page_missing_from_published_index() -> None:
    inventory_pages = [page("fr/attention", "fr", "understand", "attention")]
    try:
        AUDIT["build_revision_inventory"](
            inventory_pages,
            [],
            [],
            route_memberships={},
            revision_aids_by_lesson={
                "fr/attention": [{"id": "fr/missing-aid", "role": "synthesis"}]
            },
        )
    except ValueError as error:
        assert "not a published page" in str(error)
    else:
        raise AssertionError("missing revision aid should fail")


def test_explicit_concept_and_implementation_edges_are_projected() -> None:
    inventory = AUDIT["build_revision_inventory"](
        [page("fr/attention", "fr", "understand", "attention")],
        [{"id": "self-attention", "resources": ["fr/attention"]}],
        [{"id": "attention-module", "referenced_by": ["fr/attention"]}],
        route_memberships={},
    )
    record = inventory["pages"][0]
    assert record["concept_ids"] == ["self-attention"]
    assert record["implementation_resource_ids"] == ["attention-module"]


def test_bilingual_parity_flags_missing_topic_counterparts() -> None:
    inventory = AUDIT["build_revision_inventory"](
        [
            page("fr/shared-topic", "fr", "understand", "shared-topic"),
            page("en/other-topic", "en", "understand", "other-topic"),
        ],
        [],
        [],
        route_memberships={},
    )
    parity = inventory["bilingual_parity"]["understand"]
    by_topic = {item["topic"]: item for item in parity}
    assert by_topic["shared-topic"]["balanced"] is False
    assert by_topic["shared-topic"]["fr"] == 1
    assert by_topic["shared-topic"]["en"] == 0
    assert by_topic["other-topic"]["balanced"] is False


def test_report_documents_unrouted_and_unassessed_semantics() -> None:
    inventory = AUDIT["build_revision_inventory"](
        [page("fr/lesson", "fr", "understand", "lesson")],
        [],
        [],
        route_memberships={},
    )
    report = AUDIT["render_markdown"](inventory)
    assert "unrouted" in report
    assert "not_assessed" in report
    assert "does not mean a page lacks a synthesis or revision aid" in report
    assert "a linked aid does not imply sufficient coverage" in report


def test_missing_topics_are_reported_and_excluded_from_parity() -> None:
    inventory = AUDIT["build_revision_inventory"](
        [
            page("fr/no-topic", "fr", "understand", None),
            page("en/no-topic", "en", "understand", ""),
            page("fr/valid", "fr", "understand", "valid"),
            page("en/valid", "en", "understand", "valid"),
        ],
        [],
        [],
        route_memberships={},
    )
    assert {item["id"] for item in inventory["missing_topic_pages"]} == {
        "fr/no-topic",
        "en/no-topic",
    }
    assert [item["topic"] for item in inventory["bilingual_parity"]["understand"]] == ["valid"]


def test_bilingual_parity_reports_multiple_pages_per_topic() -> None:
    inventory = AUDIT["build_revision_inventory"](
        [
            page("fr/one", "fr", "understand", "duplicate"),
            page("fr/two", "fr", "understand", "duplicate"),
            page("en/one", "en", "understand", "duplicate"),
        ],
        [],
        [],
        route_memberships={},
    )
    item = inventory["bilingual_parity"]["understand"][0]
    assert item["balanced"] is False
    assert item["multiple_fr"] is True
    assert item["multiple_en"] is False


def test_unexpected_language_values_are_reported() -> None:
    inventory = AUDIT["build_revision_inventory"](
        [page("shared/page", "shared", "understand", "shared-topic")],
        [],
        [],
        route_memberships={},
    )
    assert inventory["unexpected_languages"] == [{"id": "shared/page", "language": "shared"}]


def test_optional_deepen_pages_are_excluded_from_understand_build_coverage() -> None:
    pages = [
        page("fr/core", "fr", "understand", "core-topic"),
        page("en/core", "en", "understand", "core-topic"),
        page("fr/optional-deep-dive", "fr", "deepen", "optional-topic"),
        page("en/optional-deep-dive", "en", "deepen", "optional-topic"),
    ]
    inventory = AUDIT["build_revision_inventory"](pages, [], [], route_memberships={})
    assert {record["id"] for record in inventory["pages"]} == {"fr/core", "en/core"}
    assert inventory["counts"]["understand"]["total"] == 2
    assert inventory["counts"]["build"]["total"] == 0
