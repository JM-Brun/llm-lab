from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "site"
    / "tools"
    / "report_extraction_destination_inventory.py"
)
SPEC = importlib.util.spec_from_file_location("report_extraction_destination_inventory", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _write_yaml(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def test_inventory_separates_candidate_destinations_legacy_fields_and_local_routes(
    tmp_path: Path,
) -> None:
    _write_yaml(
        tmp_path / "data" / "sources.yml",
        {
            "sources": [
                {
                    "id": "source-one",
                    "related": {
                        "pages": ["en/example"],
                        "concepts": ["known-concept"],
                    },
                    "classification": {"concept_ids": ["known-concept", "missing-source-concept"]},
                }
            ]
        },
    )
    _write_yaml(
        tmp_path / "data" / "concepts.yml",
        {"concepts": [{"id": "known-concept"}]},
    )
    _write_yaml(
        tmp_path / "data" / "extractions" / "source-one.yml",
        {
            "source_id": "source-one",
            "pedagogical_model": {
                "teaching_route": [{"order": 1}, {"order": 2}],
            },
            "items": [
                {
                    "id": "source-one:item-one",
                    "kind": "definition",
                    "summary": "An extracted definition.",
                    "candidate_destinations": {
                        "pages": ["en/example"],
                        "concepts": ["known-concept", "missing-candidate-concept"],
                    },
                    "classification": {"concept_ids": ["known-concept"]},
                    "mapped_concepts": ["known-concept", "missing-mapped-concept"],
                    "target_resources": ["fr/example-resource"],
                },
                {
                    "id": "source-one:item-two",
                    "kind": "claim",
                    "summary": "Another extracted claim.",
                    "candidate_destinations": [],
                    "target_routes": ["route-one"],
                },
            ],
        },
    )

    report = MODULE.build_report(tmp_path)

    assert report["counts"] == {
        "sources": 1,
        "extraction_files": 1,
        "extraction_items": 2,
        "items_with_candidate_destinations": 2,
        "unknown_extraction_source_ids": 0,
        "filename_source_id_mismatches": 0,
        "malformed_records_or_items": 0,
        "source_local_teaching_route_steps": 2,
    }
    assert report["candidate_destination_shapes"] == {"mapping": 1, "non-mapping": 1}
    assert report["source_destinations"]["related.pages"]["references"] == 1
    assert report["item_destinations"]["candidate_destinations.pages"]["references"] == 1
    assert report["item_destinations"]["mapped_concepts"]["references"] == 2
    assert report["item_destinations"]["target_resources"]["unique_references"] == [
        "fr/example-resource"
    ]
    assert report["item_destinations"]["target_routes"]["unique_references"] == ["route-one"]
    assert report["unknown_concept_references"]["source.classification.concept_ids"] == [
        "missing-source-concept"
    ]
    assert report["unknown_concept_references"]["item.candidate_destinations.concepts"] == [
        "missing-candidate-concept"
    ]
    assert report["unknown_concept_references"]["item.mapped_concepts"] == [
        "missing-mapped-concept"
    ]


def test_inventory_reports_filename_and_source_identity_exceptions(tmp_path: Path) -> None:
    _write_yaml(
        tmp_path / "data" / "sources.yml",
        {"sources": [{"id": "known-source"}]},
    )
    _write_yaml(tmp_path / "data" / "concepts.yml", {"concepts": []})
    _write_yaml(
        tmp_path / "data" / "extractions" / "wrong-filename.yml",
        {"source_id": "unknown-source", "items": []},
    )

    report = MODULE.build_report(tmp_path)

    assert report["counts"]["unknown_extraction_source_ids"] == 1
    assert report["counts"]["filename_source_id_mismatches"] == 1
    assert report["exceptions"]["unknown_extraction_source_ids"] == ["unknown-source"]
    assert report["exceptions"]["filename_source_id_mismatches"] == [
        "data/extractions/wrong-filename.yml"
    ]
