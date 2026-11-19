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
    assert record["synthesis_status"] == "not_assessed"


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
