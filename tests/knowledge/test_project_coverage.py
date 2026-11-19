"""Tests for the concept-centred Project Intelligence coverage matrix."""

from __future__ import annotations

import runpy
from pathlib import Path

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
    assert _state(rows["attention"], "bilingual_parity") == "needs_review"
    assert _state(rows["query"], "teaching_pages") == "present"
    assert _state(rows["query"], "understand") == "present"
    assert _state(rows["query"], "resources") == "needs_review"
    assert _state(rows["query"], "build") == "not_registered"
    assert _state(rows["query"], "computation") == "not_registered"
    assert _state(rows["query"], "sources") == "not_registered"
    assert _state(rows["query"], "practice") == "not_registered"
    assert all(
        cell["state"] != "missing"
        for row in rows.values()
        for cell in row["dimensions"].values()
    )


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
            revision={"status": "not_applicable", "reason": "outside scope"},
        )
    write_sources(tmp_path)
    matrix = build_concept_coverage(ProjectIndex.build(tmp_path))
    rows = {row["concept_id"]: row for row in matrix["rows"]}

    assert _state(rows["attention"], "revision_support") == "not_applicable"
    assert _state(rows["query"], "revision_support") == "not_applicable"
    assert all(
        cell["state"] != "missing"
        for row in rows.values()
        for cell in row["dimensions"].values()
    )


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
            revision={"status": "assessed", "resources": []},
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
    assert first["state_counts"]["build"] == {"not_registered": first["row_count"]}
    assert first["state_counts"]["computation"] == {"not_registered": first["row_count"]}
    assert first["state_counts"]["sources"] == {"not_registered": first["row_count"]}
    assert first["state_counts"]["practice"] == {"not_registered": first["row_count"]}
