"""Tests for the first-class non-page resource registry."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "check_resource_registry.py"
MODULE: dict[str, Any] = runpy.run_path(str(MODULE_PATH), run_name="resource_registry_test")
validate_resource_registry = MODULE["validate_resource_registry"]


def _valid_resource() -> dict[str, Any]:
    return {
        "id": "shared-transformer-code",
        "kind": "implementation",
        "labels": {"fr": "Code Transformer", "en": "Transformer code"},
        "descriptions": {"fr": "Description française.", "en": "English description."},
        "language": "en",
        "programming_language": "Python",
        "status": "published",
        "location": {"type": "local", "path": "src/example.py"},
        "referenced_by": ["fr/build-path", "en/build-path"],
        "concepts": ["attention", "masking"],
    }


def _validate(tmp_path: Path, resource: dict[str, Any]) -> list[str]:
    (tmp_path / "src").mkdir(exist_ok=True)
    (tmp_path / "src" / "example.py").write_text("value = 1\n", encoding="utf-8")
    return validate_resource_registry(
        {"schema_version": 1, "resources": [resource]},
        tmp_path,
        {"fr/build-path", "en/build-path"},
        {"attention", "masking"},
    )


def test_accepts_one_resource_shared_by_bilingual_pages_and_multiple_concepts(
    tmp_path: Path,
) -> None:
    errors = _validate(tmp_path, _valid_resource())
    assert errors == []


def test_rejects_duplicate_resource_ids_and_duplicate_concept_links(tmp_path: Path) -> None:
    resource = _valid_resource()
    duplicate = _valid_resource()
    duplicate["concepts"] = ["attention", "attention"]
    errors = validate_resource_registry(
        {"schema_version": 1, "resources": [resource, duplicate]},
        tmp_path,
        {"fr/build-path", "en/build-path"},
        {"attention", "masking"},
    )
    assert any("duplicate identifier" in error for error in errors)
    assert any("duplicate concept IDs" in error for error in errors)


def test_rejects_unknown_concepts_and_unpublished_page_references(tmp_path: Path) -> None:
    resource = _valid_resource()
    resource["concepts"] = ["not-a-concept"]
    resource["referenced_by"] = ["fr/not-published"]
    errors = _validate(tmp_path, resource)
    assert any("unknown concept" in error for error in errors)
    assert any("not published" in error for error in errors)


def test_rejects_path_traversal_and_absolute_paths(tmp_path: Path) -> None:
    resource = _valid_resource()
    resource["location"] = {"type": "local", "path": "../outside.py"}
    errors = _validate(tmp_path, resource)
    assert any("parent segments" in error for error in errors)
    resource["location"] = {"type": "local", "path": "/etc/passwd"}
    errors = _validate(tmp_path, resource)
    assert any("absolute" in error for error in errors)


def test_rejects_symlink_escape(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside-resource.py"
    outside.write_text("secret = True\n", encoding="utf-8")
    (tmp_path / "src").mkdir(exist_ok=True)
    (tmp_path / "src" / "escape.py").symlink_to(outside)
    resource = _valid_resource()
    resource["location"] = {"type": "local", "path": "src/escape.py"}
    errors = _validate(tmp_path, resource)
    assert any("inside the repository" in error for error in errors)


def test_rejects_invalid_external_urls_without_network_access(tmp_path: Path) -> None:
    resource = _valid_resource()
    resource["location"] = {"type": "external", "url": "file:///tmp/example"}
    errors = _validate(tmp_path, resource)
    assert any("absolute HTTP(S) URL" in error for error in errors)
    resource["location"] = {"type": "external", "url": "https://example.org/resource"}
    assert _validate(tmp_path, resource) == []


def test_rejects_unknown_status_and_invalid_language_tag(tmp_path: Path) -> None:
    resource = _valid_resource()
    resource["status"] = "available"
    resource["language"] = "english"
    errors = _validate(tmp_path, resource)
    assert any("lifecycle status" in error for error in errors)
    assert any("BCP 47" in error for error in errors)


def test_concept_to_resource_links_are_many_to_many(tmp_path: Path) -> None:
    first = _valid_resource()
    second = _valid_resource()
    second["id"] = "second-transformer-code"
    second["location"] = {"type": "local", "path": "src/second.py"}
    (tmp_path / "src").mkdir(exist_ok=True)
    (tmp_path / "src" / "second.py").write_text("value = 2\n", encoding="utf-8")
    errors = validate_resource_registry(
        {"schema_version": 1, "resources": [first, second]},
        tmp_path,
        {"fr/build-path", "en/build-path"},
        {"attention", "masking"},
    )
    assert errors == []


def test_accepts_each_documented_lifecycle_status(tmp_path: Path) -> None:
    resource = _valid_resource()
    for status in ("published", "draft", "deprecated", "retired"):
        resource["status"] = status
        assert _validate(tmp_path, resource) == []


def test_rejects_missing_local_files_and_malformed_location_variants(
    tmp_path: Path,
) -> None:
    resource = _valid_resource()
    resource["location"] = {"type": "local", "path": "src/missing.py"}
    errors = _validate(tmp_path, resource)
    assert any("must exist inside the repository" in error for error in errors)

    resource["location"] = {
        "type": "external",
        "url": "https://example.org/resource",
        "path": "unexpected.py",
    }
    errors = _validate(tmp_path, resource)
    assert any("exactly type and url" in error for error in errors)


def test_rejects_invalid_optional_provenance_without_inventing_defaults(
    tmp_path: Path,
) -> None:
    resource = _valid_resource()
    assert "provenance" not in resource
    resource["provenance"] = {
        "creator": " ",
        "source_url": "javascript:alert(1)",
    }
    errors = _validate(tmp_path, resource)
    assert any("non-empty string" in error for error in errors)
    assert any("absolute HTTP(S) URL" in error for error in errors)
