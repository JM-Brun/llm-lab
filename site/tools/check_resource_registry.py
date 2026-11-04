#!/usr/bin/env python3
"""Validate first-class non-page learning-resource records."""

from __future__ import annotations

import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data" / "resources.yml"
CONCEPTS = ROOT / "data" / "concepts.yml"
IDENTIFIER = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
BCP47 = re.compile(
    r"(?i)(?:(?:[a-z]{2,3}(?:-[a-z]{3}){0,3}|[a-z]{4}|[a-z]{5,8})"
    r"(?:-[a-z]{4})?(?:-(?:[a-z]{2}|[0-9]{3}))?"
    r"(?:-(?:[a-z0-9]{5,8}|[0-9][a-z0-9]{3}))*"
    r"(?:-[0-9a-wy-z](?:-[a-z0-9]{2,8})+)*"
    r"(?:-x(?:-[a-z0-9]{1,8})+)?|x(?:-[a-z0-9]{1,8})+)"
)
KINDS = {"implementation"}
STATUSES = {"published", "draft", "deprecated", "retired"}
PROVENANCE_FIELDS = {"creator", "publisher", "source_url", "license"}


def _published_page_ids(root: Path) -> set[str]:
    """Return stable IDs of published French and English Quarto pages."""
    published: set[str] = set()
    for language in ("fr", "en"):
        for path in (root / "site" / language).glob("*.qmd"):
            source = path.read_text(encoding="utf-8")
            match = re.search(
                r"<!--\s*\nLLM-LAB-PAGE-MAP v1\n(.*?)\n-->",
                source,
                re.DOTALL,
            )
            if match is None:
                continue
            try:
                metadata = yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                continue
            if not isinstance(metadata, dict):
                continue
            tags = {
                key: value
                for item in metadata.get("tags", [])
                if isinstance(item, str) and ":" in item
                for key, value in [item.split(":", maxsplit=1)]
            }
            page_id = metadata.get("id")
            if tags.get("status") == "published" and isinstance(page_id, str):
                published.add(page_id)
    return published


def _valid_http_url(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip() or any(char.isspace() for char in value):
        return False
    try:
        parsed = urlsplit(value)
        # Accessing .port is required: urlsplit alone accepts malformed and
        # out-of-range ports without raising.
        port = parsed.port
        return (
            parsed.scheme in {"http", "https"}
            and (port is None or 0 <= port <= 65535)
            and bool(parsed.netloc)
            and parsed.hostname is not None
            and parsed.username is None
            and parsed.password is None
        )
    except ValueError:
        return False


def _valid_bcp47(value: Any) -> bool:
    """Check BCP 47 structure offline, including extension singleton uniqueness."""
    if not isinstance(value, str) or not BCP47.fullmatch(value):
        return False
    subtags = value.lower().split("-")[1:]
    if "x" in subtags:
        subtags = subtags[: subtags.index("x")]
    singletons = [subtag for subtag in subtags if len(subtag) == 1]
    return len(singletons) == len(set(singletons))


def _validate_location(location: Any, root: Path, where: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(location, dict):
        return [f"{where}: expected a location mapping"]
    location_type = location.get("type")
    if location_type == "local":
        if set(location) != {"type", "path"}:
            return [f"{where}: local location must contain exactly type and path"]
        value = location.get("path")
        if not isinstance(value, str) or not value or "\\" in value:
            return [f"{where}.path: expected a repository-relative POSIX path"]
        pure_path = PurePosixPath(value)
        if pure_path.is_absolute():
            return [f"{where}.path: absolute paths are not allowed"]
        raw_segments = value.split("/")
        if any(part in {"", ".", ".."} for part in raw_segments):
            return [f"{where}.path: empty, dot, and parent segments are not allowed"]
        try:
            resolved_root = root.resolve(strict=True)
            resolved_path = (root / Path(*pure_path.parts)).resolve(strict=True)
            resolved_path.relative_to(resolved_root)
        except (OSError, ValueError):
            return [
                f"{where}.path: path must exist inside the repository "
                "(including symlink resolution)"
            ]
        if not resolved_path.is_file():
            errors.append(f"{where}.path: local resource must resolve to a file")
    elif location_type == "external":
        if set(location) != {"type", "url"}:
            return [f"{where}: external location must contain exactly type and url"]
        if not _valid_http_url(location.get("url")):
            errors.append(f"{where}.url: expected an absolute HTTP(S) URL")
    else:
        errors.append(f"{where}.type: expected 'local' or 'external'")
    return errors


def validate_resource_registry(
    data: Any,
    root: Path,
    published_pages: set[str],
    concept_ids: set[str],
) -> list[str]:
    """Return structural, vocabulary, location, and referential-integrity errors."""
    errors: list[str] = []
    if (
        not isinstance(data, dict)
        or type(data.get("schema_version")) is not int
        or data.get("schema_version") != 1
    ):
        return ["resources: expected mapping with schema_version: 1"]
    entries = data.get("resources")
    if not isinstance(entries, list) or not entries:
        return ["resources: expected a non-empty list"]

    identifiers: set[str] = set()
    allowed_fields = {
        "id",
        "kind",
        "labels",
        "descriptions",
        "language",
        "programming_language",
        "status",
        "location",
        "referenced_by",
        "concepts",
        "provenance",
    }
    for index, resource in enumerate(entries):
        where = f"resources[{index}]"
        if not isinstance(resource, dict):
            errors.append(f"{where}: expected mapping")
            continue
        unknown = set(resource) - allowed_fields
        if unknown:
            errors.append(f"{where}: unknown field(s) {', '.join(sorted(unknown))}")

        identifier = resource.get("id")
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
            errors.append(f"{where}.id: expected stable kebab-case identifier")
        elif identifier in identifiers:
            errors.append(f"{where}.id: duplicate identifier {identifier!r}")
        else:
            identifiers.add(identifier)

        kind = resource.get("kind")
        if not isinstance(kind, str) or kind not in KINDS:
            errors.append(f"{where}.kind: unsupported resource kind {kind!r}")

        for field in ("labels", "descriptions"):
            values = resource.get(field)
            if not isinstance(values, dict) or set(values) != {"fr", "en"}:
                errors.append(f"{where}.{field}: expected exactly fr and en")
            elif not all(isinstance(value, str) and value.strip() for value in values.values()):
                errors.append(f"{where}.{field}: values must be non-empty strings")

        language = resource.get("language")
        if not _valid_bcp47(language):
            errors.append(f"{where}.language: expected a valid BCP 47 language tag")

        programming_language = resource.get("programming_language")
        if programming_language is not None and (
            not isinstance(programming_language, str) or not programming_language.strip()
        ):
            errors.append(f"{where}.programming_language: expected a non-empty string when present")

        status = resource.get("status")
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f"{where}.status: unsupported lifecycle status {status!r}")

        errors.extend(_validate_location(resource.get("location"), root, f"{where}.location"))

        referenced_by = resource.get("referenced_by")
        if not isinstance(referenced_by, list):
            errors.append(f"{where}.referenced_by: expected a list of published page IDs")
        elif not all(isinstance(page_id, str) for page_id in referenced_by):
            errors.append(f"{where}.referenced_by: values must be strings")
        else:
            if len(referenced_by) != len(set(referenced_by)):
                errors.append(f"{where}.referenced_by: duplicate page IDs")
            for page_id in referenced_by:
                if page_id not in published_pages:
                    errors.append(f"{where}.referenced_by: page {page_id!r} is not published")
            if (status == "published" or status == "deprecated") and not referenced_by:
                errors.append(
                    f"{where}.referenced_by: published/deprecated resources "
                    "need a published page reference"
                )
            if (status == "draft" or status == "retired") and referenced_by:
                errors.append(
                    f"{where}.referenced_by: draft/retired resources "
                    "cannot be linked from published pages"
                )

        concepts = resource.get("concepts")
        if not isinstance(concepts, list):
            errors.append(f"{where}.concepts: expected a list of concept IDs (possibly empty)")
        elif not all(isinstance(item, str) for item in concepts):
            errors.append(f"{where}.concepts: values must be strings")
        else:
            if len(concepts) != len(set(concepts)):
                errors.append(f"{where}.concepts: duplicate concept IDs")
            for concept_id in concepts:
                if concept_id not in concept_ids:
                    errors.append(f"{where}.concepts: unknown concept {concept_id!r}")

        provenance = resource.get("provenance")
        if provenance is not None:
            if not isinstance(provenance, dict):
                errors.append(f"{where}.provenance: expected a mapping")
            else:
                unknown_provenance = set(provenance) - PROVENANCE_FIELDS
                if unknown_provenance:
                    errors.append(
                        f"{where}.provenance: unknown field(s) "
                        f"{', '.join(sorted(unknown_provenance))}"
                    )
                for field, value in provenance.items():
                    if not isinstance(value, str) or not value.strip():
                        errors.append(f"{where}.provenance.{field}: expected a non-empty string")
                    elif field == "source_url" and not _valid_http_url(value):
                        errors.append(
                            f"{where}.provenance.source_url: expected an absolute HTTP(S) URL"
                        )

    return errors


def main() -> int:
    """Validate resources against the repository's published pages and concepts."""
    try:
        data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
        concepts_data = yaml.safe_load(CONCEPTS.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        sys.stderr.write(f"Cannot read resource/concept registry: {exc}\n")
        return 1
    concept_ids = {
        item["id"]
        for item in concepts_data.get("concepts", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    errors = validate_resource_registry(data, ROOT, _published_page_ids(ROOT), concept_ids)
    if errors:
        sys.stderr.write("\n".join(errors) + "\n")
        return 1
    sys.stdout.write(f"Validated {len(data['resources'])} first-class learning resources.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
