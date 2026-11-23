"""Tests for the concept-centred Project Intelligence coverage matrix."""

from __future__ import annotations

import runpy
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
PROJECT_INDEX = runpy.run_path(
    str(ROOT / "site" / "tools" / "project_index.py"),
    run_name="project_index_coverage_test",
)
COVERAGE = runpy.run_path(
    str(ROOT / "site" / "tools" / "project_coverage.py"),
    run_name="project_coverage_test",
)
FIXTURES = runpy.run_path(
    str(ROOT / "tests" / "knowledge" / "test_project_index.py"),
    run_name="project_index_fixture_test",
)
ProjectIndex = PROJECT_INDEX["ProjectIndex"]
build_concept_coverage = COVERAGE["build_concept_coverage"]


def _state(row: dict, dimension: str) -> str:
    return row["dimensions"][dimension]["state"]


def test_synthetic_matrix_uses_explicit_evidence_and_keeps_unknown_states(tmp_path: Path) -> None:
    index = FIXTURES["_index"](tmp_path)
    matrix = build_concept_coverage(index)
    rows = {row["concept_id"]: row for row in matrix["rows"]}

    assert matrix["unit"] == "canonical concept ID"
    assert matrix["row_count"] == 2
    assert _state(rows["attention"], "definition") == "present"
    assert _state(rows["attention"], "teaching_pages") == "present"
    assert _state(rows["attention"], "understand") == "present"
    assert _state(rows["attention"], "resources") == "present"
    assert _state(rows["attention"], "revision_support") == "not_assessed"
    assert _state(rows["attention"], "bilingual_parity") == "present"
    assert _state(rows["query"], "teaching_pages") == "present"
    assert _state(rows["query"], "understand") == "present"
    assert _state(rows["query"], "resources") == "needs_review"
    assert _state(rows["query"], "build") == "not_registered"
    assert _state(rows["query"], "computation") == "not_registered"
    assert _state(rows["query"], "sources") == "not_registered"
    assert _state(rows["query"], "practice") == "not_registered"
    assert _state(rows["query"], "bilingual_parity") == "missing"
    assert all(
        cell["state"] != "missing"
        for row in rows.values()
        for dimension, cell in row["dimensions"].items()
        if dimension != "bilingual_parity"
    )


def _set_query_pages(root: Path, page_ids: list[str]) -> None:
    path = root / "data" / "concepts.yml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    query = next(concept for concept in data["concepts"] if concept["id"] == "query")
    query["resources"] = page_ids
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


@pytest.mark.parametrize(
    ("linked_pages", "state", "missing_counterparts"),
    [
        (["fr/texte", "en/text", "reference/references"], "present", []),
        (["fr/attention", "en/text"], "missing", ["en/attention", "fr/texte"]),
        (["en/query"], "needs_review", []),
        (["reference/references"], "not_applicable", []),
        ([], "needs_review", []),
    ],
)
def test_bilingual_coverage_uses_topic_pairs_instead_of_language_counts(
    tmp_path: Path, linked_pages: list[str], state: str, missing_counterparts: list[str]
) -> None:
    FIXTURES["_index"](tmp_path)
    write_page = FIXTURES["_write_page"]
    write_page(tmp_path / "site", "fr/texte", "fr", topic="text")
    write_page(tmp_path / "site", "en/text", "en", topic="text")
    write_page(tmp_path / "site", "reference/references", "shared")
    _set_query_pages(tmp_path, linked_pages)

    matrix = build_concept_coverage(ProjectIndex.build(tmp_path))
    assert matrix["registry_version"] == 2
    row = next(row for row in matrix["rows"] if row["concept_id"] == "query")
    cell = row["dimensions"]["bilingual_parity"]
    assert cell["state"] == state
    assert [
        page["id"] for page in cell["evidence"] if page["association"] == "missing_counterpart"
    ] == missing_counterparts
    assert [
        finding["entity_ids"]["page"]
        for finding in COVERAGE["bilingual_association_findings"](matrix)
        if finding["entity_ids"]["concept"] == "query"
    ] == missing_counterparts
    if state == "present":
        assert {page["topic"] for page in cell["evidence"]} == {"text"}
        assert {page["id"] for page in cell["evidence"]} == {"fr/texte", "en/text"}
    elif state == "not_applicable":
        assert [page["language"] for page in cell["evidence"]] == ["shared"]


def test_ambiguous_topic_requires_review_even_with_both_languages_linked(tmp_path: Path) -> None:
    FIXTURES["_index"](tmp_path)
    FIXTURES["_write_page"](tmp_path / "site", "en/attention-alternate", "en", topic="attention")
    matrix = build_concept_coverage(ProjectIndex.build(tmp_path))
    row = next(row for row in matrix["rows"] if row["concept_id"] == "attention")
    cell = row["dimensions"]["bilingual_parity"]
    assert cell["state"] == "needs_review"
    assert {page["id"]: page["association"] for page in cell["evidence"]} == {
        "en/attention": "linked",
        "en/attention-alternate": "candidate",
        "fr/attention": "linked",
    }
    assert COVERAGE["bilingual_association_findings"](matrix) == []


def test_sufficient_integrated_revision_support_projects_as_present(tmp_path: Path) -> None:
    write_page = FIXTURES["_write_page"]
    write_sources = FIXTURES["_write_sources"]
    support = {
        "status": "integrated_sufficient",
        "evidence": [{"anchor": "revision-summary", "note": "Integrated recap."}],
    }
    for page_id, language in (
        ("fr/attention", "fr"),
        ("en/attention", "en"),
    ):
        write_page(
            tmp_path / "site",
            page_id,
            language,
            revision_support=support,
            body="\n## Revision summary {#revision-summary}\n",
        )
    write_page(tmp_path / "site", "en/query", "en")
    write_sources(tmp_path)

    matrix = build_concept_coverage(ProjectIndex.build(tmp_path))
    rows = {row["concept_id"]: row for row in matrix["rows"]}

    assert _state(rows["attention"], "revision_support") == "present"
    assert _state(rows["query"], "revision_support") == "present"
    assert {
        "id": "fr/attention#revision-summary",
        "path": "site/fr/attention.qmd#revision-summary",
    } in rows["attention"]["dimensions"]["revision_support"]["evidence"]


def test_revision_not_applicable_is_not_counted_as_missing(tmp_path: Path) -> None:
    write_page = FIXTURES["_write_page"]
    write_sources = FIXTURES["_write_sources"]
    for page_id, language in (
        ("fr/attention", "fr"),
        ("en/attention", "en"),
        ("en/query", "en"),
    ):
        write_page(
            tmp_path / "site",
            page_id,
            language,
            revision_support={"status": "not_applicable", "reason": "outside scope"},
        )
    write_sources(tmp_path)
    matrix = build_concept_coverage(ProjectIndex.build(tmp_path))
    rows = {row["concept_id"]: row for row in matrix["rows"]}

    assert _state(rows["attention"], "revision_support") == "not_applicable"
    assert _state(rows["query"], "revision_support") == "not_applicable"
    assert matrix["state_counts"]["revision_support"] == {"not_applicable": 2}


def test_optional_deepen_page_counts_for_route_but_not_revision(tmp_path: Path) -> None:
    write_page = FIXTURES["_write_page"]
    write_page(
        tmp_path / "site",
        "en/attention",
        "en",
        revision_support={
            "status": "companion_sufficient",
            "evidence": [
                {
                    "aid": "en/summary",
                    "note": "Worked example.",
                },
            ],
        },
    )
    write_page(
        tmp_path / "site",
        "fr/attention",
        "fr",
        revision_support={"status": "not_applicable", "reason": "Outside pilot scope."},
    )
    write_page(tmp_path / "site", "en/query", "en", destination="deepen")
    write_page(
        tmp_path / "site",
        "en/summary",
        "en",
        destination="deepen",
        revision_role="synthesis",
        revision_of=["en/attention"],
    )
    FIXTURES["_write_sources"](tmp_path)
    concepts_path = tmp_path / "data" / "concepts.yml"
    concepts = yaml.safe_load(concepts_path.read_text(encoding="utf-8"))
    concepts["concepts"][0]["resources"].append("en/query")
    concepts["concepts"][1]["resources"] = ["en/query"]
    concepts_path.write_text(yaml.safe_dump(concepts), encoding="utf-8")

    matrix = build_concept_coverage(ProjectIndex.build(tmp_path))
    rows = {row["concept_id"]: row["dimensions"] for row in matrix["rows"]}

    assert rows["query"]["understand"]["state"] == "present"
    assert rows["query"]["understand"]["evidence"][0]["role"] == "optional"
    assert rows["query"]["revision_support"]["state"] == "not_applicable"
    assert rows["query"]["revision_support"]["evidence"] == []
    revision = rows["attention"]["revision_support"]
    assert revision["state"] == "present"
    assert [item["id"] for item in revision["evidence"]] == [
        "en/attention",
        "en/summary:synthesis:en/attention",
        "fr/attention",
    ]
    assert revision["evidence"][-1]["reason"] == "Outside pilot scope."


@pytest.mark.parametrize(
    ("en_status", "expected_state"),
    [("missing", "missing"), ("not_assessed", "needs_review")],
)
def test_missing_requires_an_explicit_assessment_for_each_in_scope_lesson(
    tmp_path: Path, en_status: str, expected_state: str
) -> None:
    write_page = FIXTURES["_write_page"]
    missing = {"status": "missing", "reason": "The lesson has no revision support."}
    write_page(tmp_path / "site", "fr/attention", "fr", revision_support=missing)
    write_page(
        tmp_path / "site",
        "en/attention",
        "en",
        revision_support=missing if en_status == "missing" else None,
    )
    write_page(tmp_path / "site", "en/query", "en")
    FIXTURES["_write_sources"](tmp_path)

    matrix = build_concept_coverage(ProjectIndex.build(tmp_path))
    rows = {row["concept_id"]: row for row in matrix["rows"]}

    assert _state(rows["attention"], "revision_support") == expected_state
    assert _state(rows["query"], "revision_support") == "missing"


def test_assessed_without_declared_aid_requires_review_not_missing(tmp_path: Path) -> None:
    write_page = FIXTURES["_write_page"]
    write_sources = FIXTURES["_write_sources"]
    for page_id, language in (
        ("fr/attention", "fr"),
        ("en/attention", "en"),
        ("en/query", "en"),
    ):
        write_page(
            tmp_path / "site",
            page_id,
            language,
            revision_support={"status": "partial", "reason": "Coverage needs editorial review."},
        )
    write_sources(tmp_path)
    matrix = build_concept_coverage(ProjectIndex.build(tmp_path))
    rows = {row["concept_id"]: row for row in matrix["rows"]}

    assert _state(rows["attention"], "revision_support") == "needs_review"
    assert _state(rows["query"], "revision_support") == "needs_review"


def test_matrix_evidence_paths_are_repository_relative_and_deterministic() -> None:
    index = ProjectIndex.build(ROOT)
    first = build_concept_coverage(index)
    second = build_concept_coverage(index)

    assert first == second
    assert first["row_count"] == len(index.concepts_by_id)
    assert [row["concept_id"] for row in first["rows"]] == sorted(index.concepts_by_id)
    for row in first["rows"]:
        for cell in row["dimensions"].values():
            for evidence in cell["evidence"]:
                path = evidence.get("path")
                if path is not None:
                    assert not path.startswith("/")
                    assert ".." not in Path(path).parts
    assert sum(first["state_counts"]["revision_support"].values()) == first["row_count"]
    for row in first["rows"]:
        associated = index.pages_by_concept.get(row["concept_id"], ())
        assessments = index.revision_support_by_page
        cell = row["dimensions"]["revision_support"]
        assert {item["id"] for item in cell["evidence"] if "status" in item} == {
            page_id for page_id in associated if page_id in assessments
        }
    assert first["state_counts"]["build"] == {"not_registered": first["row_count"]}
    assert first["state_counts"]["computation"] == {"not_registered": first["row_count"]}
    assert first["state_counts"]["sources"] == {"not_registered": first["row_count"]}
    assert first["state_counts"]["practice"] == {"not_registered": first["row_count"]}


def test_unregistered_source_coverage_explains_existing_opt_in_adapter() -> None:
    message = COVERAGE["UNREGISTERED_DIMENSIONS"]["sources"].casefold()
    assert "opt-in source adapter exists" in message
    assert "concept-to-source/item coverage is not registered" in message
}