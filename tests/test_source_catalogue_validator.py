from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "site" / "tools" / "check_source_catalogue.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("check_source_catalogue", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _write_yaml(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def _corpus(root: Path, *, source_type: str = "paper", with_extraction: bool = False) -> None:
    _write_yaml(
        root / "data" / "source-taxonomy.yml",
        {
            "schema_version": 1,
            "source_types": ["paper", "blog", "tutorial", "course", "book-chapter"],
            "scan_statuses": [
                "discovered",
                "selected",
                "scanned",
                "partially-scanned",
                "inaccessible",
                "superseded",
                "rejected",
            ],
            "integration_statuses": [
                "not-reviewed",
                "reviewed",
                "partially-integrated",
                "integrated",
                "deferred",
                "rejected",
            ],
            "extraction_kinds": ["claim", "definition", "mechanism"],
            "evidence_confidence_levels": [
                "established",
                "well-supported",
                "context-dependent",
                "disputed",
                "speculative",
                "unverified",
            ],
            "assessment_levels": ["low", "moderate", "high", "uncertain"],
            "item_dispositions": ["integrate", "defer", "reject"],
        },
    )
    _write_yaml(
        root / "data" / "domains.yml",
        {"schema_version": 1, "domains": [{"id": "foundations"}]},
    )
    _write_yaml(
        root / "data" / "concepts.yml",
        {"schema_version": 2, "concepts": [{"id": "attention"}]},
    )
    _write_yaml(
        root / "data" / "sources.yml",
        {
            "schema_version": 1,
            "sources": [
                {
                    "id": "example-source",
                    "source_type": source_type,
                    "scan_status": "partially-scanned",
                    "integration_status": "not-reviewed",
                    "classification": {
                        "primary_theme": "foundations",
                        "secondary_themes": [],
                        "tags": ["topic:attention"],
                        "concept_ids": ["attention"],
                    },
                    "scan_history": [
                        {
                            "accessed_at": "2026-11-18T10:00:00Z",
                            "status": "partially-scanned",
                            "inspected_scope": ["Abstract"],
                            "limitations": ["Full text unavailable"],
                        }
                    ],
                    "related": {"pages": [], "concepts": ["attention"]},
                    # Unknown optional bibliography/rights metadata is intentionally retained.
                    "publication_date": None,
                    "licence": {"status": "unknown"},
                }
            ],
        },
    )
    if with_extraction:
        _write_yaml(
            root / "data" / "extractions" / "example-source.yml",
            {
                "schema_version": 1,
                "source_id": "example-source",
                "items": [
                    {
                        "id": "example-source:item-1",
                        "kind": "claim",
                        "summary": "A concise, source-grounded paraphrase.",
                        "locator": {"type": "section", "value": "Abstract"},
                        "evidence": {"confidence": "well-supported"},
                    }
                ],
            },
        )
    else:
        (root / "data" / "extractions").mkdir(parents=True, exist_ok=True)


def test_minimal_valid_source_and_unknown_optional_metadata_are_accepted(tmp_path: Path) -> None:
    _corpus(tmp_path)

    assert MODULE.validate_source_catalogue(tmp_path) == []


def test_valid_extraction_item_is_accepted(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)

    assert MODULE.validate_source_catalogue(tmp_path) == []


def test_malformed_scan_history_and_unknown_status_are_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path)
    source_path = tmp_path / "data" / "sources.yml"
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    data["sources"][0]["scan_history"][0]["accessed_at"] = "not-a-date"
    data["sources"][0]["scan_history"][0]["status"] = "maybe-scanned"
    _write_yaml(source_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("scan_history[0].accessed_at" in error for error in errors)
    assert any("scan_history[0].status" in error for error in errors)


def test_missing_extraction_locator_and_unknown_confidence_are_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    item = data["items"][0]
    item["locator"] = {"type": "section"}
    item["evidence"]["confidence"] = "certain"
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("items[0].locator" in error for error in errors)
    assert any("evidence.confidence" in error for error in errors)


def test_instructional_source_requires_pedagogical_model(tmp_path: Path) -> None:
    _corpus(tmp_path, source_type="blog", with_extraction=True)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("pedagogical_model: required for instructional sources" in error for error in errors)


def test_source_without_scan_history_is_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path)
    source_path = tmp_path / "data" / "sources.yml"
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    data["sources"][0]["scan_history"] = []
    _write_yaml(source_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("scan_history: expected at least one inspection event" in error for error in errors)
