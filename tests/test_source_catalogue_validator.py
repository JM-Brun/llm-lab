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
    _write_yaml(
        root / "data" / "source-collections.yml",
        {"schema_version": 1, "collections": []},
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


def test_locator_type_and_value_must_be_non_empty_strings(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    data["items"][0]["locator"] = {"type": ["section"], "value": {"heading": "Abstract"}}
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("items[0].locator.type: expected non-empty text" in error for error in errors)
    assert any("items[0].locator.value: expected non-empty text" in error for error in errors)


def test_provenance_locator_and_optional_speaker_are_structurally_validated(
    tmp_path: Path,
) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    data["items"][0]["provenance"] = {
        "voice": "reader-comment",
        "parent_source_id": "example-source",
        "locator": {"type": "comment", "value": "  "},
        "captured_at": "2026-11-18T12:00:00Z",
        "speaker": "",
    }
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("provenance.locator.value: expected non-empty text" in error for error in errors)
    assert any("provenance.speaker: expected non-empty text" in error for error in errors)


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


def test_duplicate_source_ids_are_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path)
    source_path = tmp_path / "data" / "sources.yml"
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    data["sources"].append(data["sources"][0].copy())
    _write_yaml(source_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("duplicate source ID 'example-source'" in error for error in errors)


def test_duplicate_extraction_item_ids_are_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    data["items"].append(data["items"][0].copy())
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("items[1].id: expected unique ID prefixed by source_id" in error for error in errors)


def test_extraction_item_id_must_use_its_source_prefix(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    data["items"][0]["id"] = "another-source:item-1"
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("items[0].id: expected unique ID prefixed by source_id" in error for error in errors)


def test_unknown_source_domain_concept_and_page_references_are_rejected(
    tmp_path: Path,
) -> None:
    _corpus(tmp_path)
    source_path = tmp_path / "data" / "sources.yml"
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    source = data["sources"][0]
    source["classification"]["primary_theme"] = "unknown-domain"
    source["classification"]["concept_ids"] = ["unknown-concept"]
    source["related"] = {
        "pages": ["en/unknown-page"],
        "concepts": ["unknown-concept"],
    }
    _write_yaml(source_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("primary_theme: unknown domain" in error for error in errors)
    assert any("classification.concept_ids: unknown concept" in error for error in errors)
    assert any("related.pages: unknown page" in error for error in errors)
    assert any("related.concepts: unknown concept" in error for error in errors)


def test_duplicate_source_tags_are_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path)
    source_path = tmp_path / "data" / "sources.yml"
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    data["sources"][0]["classification"]["tags"] = ["topic:attention", "topic:attention"]
    _write_yaml(source_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("classification.tags: duplicate tags" in error for error in errors)


def test_malformed_namespaced_source_tag_is_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path)
    source_path = tmp_path / "data" / "sources.yml"
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    data["sources"][0]["classification"]["tags"] = ["subject:attention"]
    _write_yaml(source_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("invalid namespaced tag" in error for error in errors)


def test_valid_extraction_disposition_and_assessment_are_accepted(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    item = data["items"][0]
    item["disposition"] = "defer"
    item["pedagogical_assessment"] = {
        "novelty": {"level": "moderate", "rationale": "Adds a scoped example."},
        "evidence_quality": {
            "level": "high",
            "rationale": "The source states the result directly.",
        },
    }
    _write_yaml(extraction_path, data)

    assert MODULE.validate_source_catalogue(tmp_path) == []


def test_unknown_extraction_disposition_is_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    data["items"][0]["disposition"] = "maybe"
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("disposition: unsupported value 'maybe'" in error for error in errors)


def test_invalid_pedagogical_assessment_level_is_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    data["items"][0]["pedagogical_assessment"] = {
        "novelty": {"level": "excellent", "rationale": "A reason."}
    }
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any(
        "pedagogical_assessment.novelty.level: unsupported value 'excellent'" in error
        for error in errors
    )


def test_empty_pedagogical_assessment_rationale_is_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    data["items"][0]["pedagogical_assessment"] = {
        "novelty": {"level": "moderate", "rationale": "  "}
    }
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any(
        "pedagogical_assessment.novelty.rationale: expected non-empty text" in error
        for error in errors
    )


def test_extraction_tag_namespace_and_duplicates_are_checked(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    data["items"][0]["classification"] = {"tags": ["topic:attention", "topic:attention"]}
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("classification.tags: duplicate tags" in error for error in errors)


def test_valid_community_provenance_and_verification_are_accepted(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    item = data["items"][0]
    item["provenance"] = {
        "voice": "reader-comment",
        "parent_source_id": "example-source",
        "locator": {"type": "comment", "value": "Comment 42"},
        "captured_at": "2026-11-18T12:00:00Z",
    }
    item["verification"] = {
        "status": "corroborated",
        "sources": ["example-source", "https://example.org/independent-note"],
    }
    _write_yaml(extraction_path, data)

    assert MODULE.validate_source_catalogue(tmp_path) == []


def test_invalid_community_provenance_and_verification_are_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    item = data["items"][0]
    item["provenance"] = {
        "voice": "anonymous-crowd",
        "parent_source_id": "missing-source",
        "locator": "Comment 42",
        "captured_at": "not-a-date",
    }
    item["verification"] = {
        "status": "probably-true",
        "sources": ["missing-source"],
    }
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("provenance.voice: unsupported voice" in error for error in errors)
    assert any("provenance.parent_source_id: unknown source" in error for error in errors)
    assert any("provenance.locator: expected a mapping" in error for error in errors)
    assert any("provenance.captured_at: expected ISO 8601 date" in error for error in errors)
    assert any("verification.status: unsupported status" in error for error in errors)
    assert any("verification.sources: unknown source 'missing-source'" in error for error in errors)


def test_non_mapping_candidate_destinations_are_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    data["items"][0]["candidate_destinations"] = ["en/attention"]
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("candidate_destinations: expected a mapping" in error for error in errors)


def test_source_collection_membership_is_optional_during_backfill(tmp_path: Path) -> None:
    _corpus(tmp_path)

    assert MODULE.validate_source_catalogue(tmp_path) == []


def test_valid_single_and_multiple_collection_memberships_are_accepted(tmp_path: Path) -> None:
    _corpus(tmp_path)
    _write_yaml(
        tmp_path / "docs" / "collections" / "one.md",
        {"title": "Collection one"},
    )
    _write_yaml(
        tmp_path / "docs" / "collections" / "two.md",
        {"title": "Collection two"},
    )
    _write_yaml(
        tmp_path / "data" / "source-collections.yml",
        {
            "schema_version": 1,
            "collections": [
                {
                    "id": "collection-one",
                    "title": "Collection one",
                    "dossier_path": "docs/collections/one.md",
                    "status": "active",
                },
                {
                    "id": "collection-two",
                    "title": "Collection two",
                    "dossier_path": "docs/collections/two.md",
                    "status": "archived",
                },
            ],
        },
    )
    source_path = tmp_path / "data" / "sources.yml"
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    data["sources"][0]["collections"] = ["collection-one", "collection-two"]
    _write_yaml(source_path, data)

    assert MODULE.validate_source_catalogue(tmp_path) == []


def test_unknown_and_duplicate_collection_memberships_are_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path)
    _write_yaml(
        tmp_path / "data" / "source-collections.yml",
        {
            "schema_version": 1,
            "collections": [
                {
                    "id": "known-collection",
                    "title": "Known collection",
                    "dossier_path": "docs/collections/missing.md",
                    "status": "active",
                }
            ],
        },
    )
    source_path = tmp_path / "data" / "sources.yml"
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    data["sources"][0]["collections"] = [
        "unknown-collection",
        "known-collection",
        "known-collection",
    ]
    _write_yaml(source_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("unknown collection ID 'unknown-collection'" in error for error in errors)
    assert any("duplicate collection IDs" in error for error in errors)
    assert any("dossier_path: file does not exist" in error for error in errors)


def test_duplicate_collection_registry_ids_are_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path)
    entry = {
        "id": "same-collection",
        "title": "Same collection",
        "dossier_path": "docs/collections/same.md",
        "status": "active",
    }
    _write_yaml(
        tmp_path / "data" / "source-collections.yml",
        {"schema_version": 1, "collections": [entry, entry]},
    )

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("duplicate collection ID 'same-collection'" in error for error in errors)


def test_explicit_null_collection_membership_is_rejected(tmp_path: Path) -> None:
    _corpus(tmp_path)
    source_path = tmp_path / "data" / "sources.yml"
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    data["sources"][0]["collections"] = None
    _write_yaml(source_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any(
        "sources[0].collections: expected a list of collection IDs" in error for error in errors
    )


def test_collection_registry_rejects_non_string_status_without_crashing(tmp_path: Path) -> None:
    _corpus(tmp_path)
    _write_yaml(
        tmp_path / "data" / "source-collections.yml",
        {
            "schema_version": 1,
            "collections": [
                {
                    "id": "invalid-status",
                    "title": "Invalid status",
                    "dossier_path": "docs/missing.md",
                    "status": ["active"],
                }
            ],
        },
    )

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any(".status: expected 'active' or 'archived'" in error for error in errors)


def test_extraction_cannot_duplicate_source_collection_membership(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    data["collections"] = ["qkv-attention"]
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("membership belongs on the canonical source record" in error for error in errors)


def test_extraction_filename_must_match_canonical_source_id(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_dir = tmp_path / "data" / "extractions"
    canonical = extraction_dir / "example-source.yml"
    noncanonical = extraction_dir / "renamed-extraction.yml"
    noncanonical.write_text(canonical.read_text(encoding="utf-8"), encoding="utf-8")

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any(
        "filename must be canonical (expected example-source.yml)" in error for error in errors
    )
    assert any("duplicate extraction for 'example-source'" in error for error in errors)


def test_extraction_source_id_must_be_a_string_and_not_a_collection(tmp_path: Path) -> None:
    _corpus(tmp_path, with_extraction=True)
    extraction_path = tmp_path / "data" / "extractions" / "example-source.yml"
    data = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    data["source_id"] = ["example-source"]
    _write_yaml(extraction_path, data)

    errors = MODULE.validate_source_catalogue(tmp_path)

    assert any("source_id: expected a stable kebab-case ID" in error for error in errors)
    assert any("source_id: unknown source" in error for error in errors)
