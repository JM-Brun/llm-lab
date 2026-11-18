from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "site" / "tools" / "report_source_coverage.py"
SPEC = importlib.util.spec_from_file_location("report_source_coverage", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _write_yaml(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def test_report_joins_extractions_by_source_id_and_surfaces_review_queues(tmp_path: Path) -> None:
    _write_yaml(
        tmp_path / "data" / "sources.yml",
        {
            "schema_version": 1,
            "sources": [
                {
                    "id": "source-one",
                    "publication_date": None,
                    "licence": {"status": "unknown"},
                    "scan_status": "scanned",
                    "integration_status": "integrated",
                    "scan_history": [{"status": "partially-scanned"}],
                    "classification": {"concept_ids": []},
                    "related": {"concepts": [], "pages": []},
                },
                {
                    "id": "source-two",
                    "publication_date": "2026-01-01",
                    "licence": {"status": "verified"},
                    "scan_status": "partially-scanned",
                    "integration_status": "integrated",
                    "scan_history": [{"status": "partially-scanned"}],
                    "classification": {"concept_ids": []},
                    "related": {"concepts": [], "pages": []},
                },
            ],
        },
    )
    _write_yaml(
        tmp_path / "data" / "concepts.yml",
        {
            "schema_version": 2,
            "concepts": [{"id": "concept-one"}, {"id": "concept-uncovered"}],
        },
    )
    _write_yaml(
        tmp_path / "data" / "extractions" / "filename-does-not-match-source-id.yml",
        {
            "schema_version": 1,
            "source_id": "source-one",
            "items": [
                {
                    "classification": {"concept_ids": ["concept-one"]},
                    "candidate_destinations": {"pages": ["en/example"]},
                }
            ],
        },
    )

    report = MODULE.build_report(tmp_path)
    counts = report["counts"]

    assert counts["sources"] == 2
    assert counts["extraction_records"] == 1
    assert counts["sources_without_extraction"] == 1
    assert counts["integrated_sources_without_extraction"] == 1
    assert counts["sources_without_concept_link"] == 1
    assert counts["sources_without_page_destination"] == 1
    assert counts["concepts_without_source"] == 1
    assert counts["concepts_with_one_source"] == 1
    assert counts["publication_dates_unknown"] == 1
    assert counts["licence_status_unknown"] == 1
    assert counts["extraction_source_references_unknown"] == 0
    assert counts["scan_history_status_mismatches"] == 1
    assert report["review_queues"]["integrated_sources_without_extraction"] == ["source-two"]


def test_markdown_report_explains_that_gaps_are_review_queues() -> None:
    report = {
        "counts": {"sources": 1},
        "status_distribution": {"scan": {"scanned": 1}},
        "review_queues": {"sources_without_extraction": []},
        "interpretation": {"contradictions": "Require human review."},
    }

    markdown = MODULE.render_markdown(report)

    assert "Source-to-knowledge coverage report" in markdown
    assert "sources without extraction (0)" in markdown
    assert "Require human review." in markdown
