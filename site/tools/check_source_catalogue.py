#!/usr/bin/env python3
"""Validate the source catalogue and atomic extraction records."""

from __future__ import annotations

import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = ROOT / "data" / "sources.yml"
TAXONOMY_FILE = ROOT / "data" / "source-taxonomy.yml"
DOMAIN_FILE = ROOT / "data" / "domains.yml"
CONCEPT_FILE = ROOT / "data" / "concepts.yml"
EXTRACTION_DIR = ROOT / "data" / "extractions"
ID_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
TAG_PATTERN = re.compile(
    r"(?:topic|method|modality|application|ecosystem):[a-z0-9]+(?:-[a-z0-9]+)*"
)
CONFIDENCE_LEVELS = {
    "established",
    "well-supported",
    "context-dependent",
    "disputed",
    "speculative",
    "unverified",
}
COMMUNITY_VOICES = {
    "primary-author",
    "reader-comment",
    "editorial-note",
    "maintainer",
    "other",
}
VERIFICATION_STATUSES = {"unverified", "corroborated", "contradicted", "not-assessed"}


def _load_yaml(path: Path, root: Path, errors: list[str]) -> Any:
    """Load YAML and collect a contextual error instead of raising."""
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"{path.relative_to(root)}: cannot load YAML ({exc})")
        return None


def _is_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return True
        except ValueError:
            return False


def _strings(value: Any, where: str, errors: list[str]) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"{where}: expected a list of strings")
        return []
    return value


def _validate_tags(value: Any, where: str, errors: list[str]) -> None:
    tags = _strings(value, where, errors)
    if len(tags) != len(set(tags)):
        errors.append(f"{where}: duplicate tags")
    for tag in tags:
        if not TAG_PATTERN.fullmatch(tag):
            errors.append(f"{where}: invalid namespaced tag {tag!r}")


def _page_ids(root: Path) -> set[str]:
    """Collect stable page IDs from bilingual page-map comments."""
    page_ids: set[str] = set()
    pattern = re.compile(r"^id:\s*['\"]?((?:fr|en)/[a-z0-9-]+)", re.MULTILINE)
    for language in ("fr", "en"):
        for path in (root / "site" / language).glob("*.qmd"):
            source = path.read_text(encoding="utf-8")
            match = re.search(
                r"<!--\s*\nLLM-LAB-PAGE-MAP v1\n(.*?)\n-->",
                source,
                re.DOTALL,
            )
            if match:
                page_ids.update(pattern.findall(match.group(1)))
    return page_ids


def validate_source_catalogue(root: Path = ROOT) -> list[str]:
    """Return structural and referential-integrity errors for sources and extractions."""
    source_file = root / "data" / "sources.yml"
    taxonomy_file = root / "data" / "source-taxonomy.yml"
    domain_file = root / "data" / "domains.yml"
    concept_file = root / "data" / "concepts.yml"
    extraction_dir = root / "data" / "extractions"

    errors: list[str] = []
    taxonomy = _load_yaml(taxonomy_file, root, errors)
    domains = _load_yaml(domain_file, root, errors)
    concepts = _load_yaml(concept_file, root, errors)
    sources_data = _load_yaml(source_file, root, errors)
    if errors:
        return errors

    if not isinstance(taxonomy, dict) or taxonomy.get("schema_version") != 1:
        return ["data/source-taxonomy.yml: expected schema_version: 1"]
    if not isinstance(domains, dict) or domains.get("schema_version") != 1:
        return ["data/domains.yml: expected schema_version: 1"]
    if not isinstance(concepts, dict) or concepts.get("schema_version") != 1:
        return ["data/concepts.yml: expected schema_version: 1"]
    if not isinstance(sources_data, dict) or sources_data.get("schema_version") != 1:
        return ["data/sources.yml: expected schema_version: 1"]

    source_types = set(taxonomy.get("source_types", []))
    scan_statuses = set(taxonomy.get("scan_statuses", []))
    integration_statuses = set(taxonomy.get("integration_statuses", []))
    extraction_kinds = set(taxonomy.get("extraction_kinds", []))
    domain_ids = {
        item.get("id")
        for item in domains.get("domains", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    concept_ids = {
        item.get("id")
        for item in concepts.get("concepts", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    pages = _page_ids(root)

    source_entries = sources_data.get("sources")
    if not isinstance(source_entries, list):
        return ["data/sources.yml: expected a sources list"]

    source_ids: set[str] = set()
    for index, source in enumerate(source_entries):
        where = f"data/sources.yml:sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{where}: expected a mapping")
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not ID_PATTERN.fullmatch(source_id):
            errors.append(f"{where}.id: expected a stable kebab-case ID")
        elif source_id in source_ids:
            errors.append(f"{where}.id: duplicate source ID {source_id!r}")
        else:
            source_ids.add(source_id)

        if source.get("source_type") not in source_types:
            errors.append(f"{where}.source_type: unsupported value {source.get('source_type')!r}")
        if source.get("scan_status") not in scan_statuses:
            errors.append(f"{where}.scan_status: unsupported value {source.get('scan_status')!r}")
        if source.get("integration_status") not in integration_statuses:
            errors.append(
                f"{where}.integration_status: unsupported value "
                f"{source.get('integration_status')!r}"
            )

        classification = source.get("classification", {})
        if not isinstance(classification, dict):
            errors.append(f"{where}.classification: expected a mapping")
            classification = {}
        primary = classification.get("primary_theme")
        if primary is not None and primary not in domain_ids:
            errors.append(f"{where}.classification.primary_theme: unknown domain {primary!r}")
        secondary = _strings(
            classification.get("secondary_themes"),
            f"{where}.classification.secondary_themes",
            errors,
        )
        if len(secondary) != len(set(secondary)) or primary in secondary:
            errors.append(f"{where}.classification: duplicate or overlapping themes")
        for domain_id in secondary:
            if domain_id not in domain_ids:
                errors.append(f"{where}.classification.secondary_themes: unknown domain {domain_id!r}")
        _validate_tags(classification.get("tags"), f"{where}.classification.tags", errors)
        for concept_id in _strings(
            classification.get("concept_ids"),
            f"{where}.classification.concept_ids",
            errors,
        ):
            if concept_id not in concept_ids:
                errors.append(f"{where}.classification.concept_ids: unknown concept {concept_id!r}")

        history = source.get("scan_history")
        if not isinstance(history, list) or not history:
            errors.append(f"{where}.scan_history: expected at least one inspection event")
        else:
            for event_index, event in enumerate(history):
                event_where = f"{where}.scan_history[{event_index}]"
                if not isinstance(event, dict):
                    errors.append(f"{event_where}: expected a mapping")
                    continue
                if not _is_date(event.get("accessed_at")):
                    errors.append(f"{event_where}.accessed_at: expected ISO 8601 date or datetime")
                if event.get("status") not in scan_statuses:
                    errors.append(f"{event_where}.status: unsupported value {event.get('status')!r}")
                _strings(event.get("inspected_scope"), f"{event_where}.inspected_scope", errors)
                _strings(event.get("limitations"), f"{event_where}.limitations", errors)

        related = source.get("related", {})
        if isinstance(related, dict):
            for page_id in _strings(related.get("pages"), f"{where}.related.pages", errors):
                if page_id not in pages:
                    errors.append(f"{where}.related.pages: unknown page {page_id!r}")
            for concept_id in _strings(related.get("concepts"), f"{where}.related.concepts", errors):
                if concept_id not in concept_ids:
                    errors.append(f"{where}.related.concepts: unknown concept {concept_id!r}")
        else:
            errors.append(f"{where}.related: expected a mapping")

    item_ids: set[str] = set()
    extraction_files = sorted(extraction_dir.glob("*.yml"))
    for path in extraction_files:
        where = str(path.relative_to(ROOT))
        data = _load_yaml(path, root, errors)
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            errors.append(f"{where}: expected schema_version: 1")
            continue
        source_id = data.get("source_id")
        if source_id not in source_ids:
            errors.append(f"{where}.source_id: unknown source {source_id!r}")
        items = data.get("items")
        if not isinstance(items, list):
            errors.append(f"{where}.items: expected a list")
            continue

        for index, item in enumerate(items):
            item_where = f"{where}:items[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{item_where}: expected a mapping")
                continue
            item_id = item.get("id")
            if (
                not isinstance(item_id, str)
                or not item_id.startswith(f"{source_id}:")
                or item_id in item_ids
            ):
                errors.append(f"{item_where}.id: expected unique ID prefixed by source_id")
            else:
                item_ids.add(item_id)
            if item.get("kind") not in extraction_kinds:
                errors.append(f"{item_where}.kind: unsupported value {item.get('kind')!r}")
            if not isinstance(item.get("summary"), str) or not item["summary"].strip():
                errors.append(f"{item_where}.summary: expected non-empty paraphrase")
            locator = item.get("locator")
            if not isinstance(locator, dict) or not locator.get("type") or not locator.get("value"):
                errors.append(f"{item_where}.locator: expected type and value")
            evidence = item.get("evidence")
            if not isinstance(evidence, dict):
                errors.append(f"{item_where}.evidence: expected a mapping")
            elif evidence.get("confidence") not in CONFIDENCE_LEVELS:
                errors.append(f"{item_where}.evidence.confidence: unsupported value")

            classification = item.get("classification", {})
            if classification is not None and not isinstance(classification, dict):
                errors.append(f"{item_where}.classification: expected a mapping")
                classification = {}
            if isinstance(classification, dict):
                primary = classification.get("primary_theme")
                if primary is not None and primary not in domain_ids:
                    errors.append(f"{item_where}.classification.primary_theme: unknown domain")
                _validate_tags(classification.get("tags"), f"{item_where}.classification.tags", errors)
                for concept_id in _strings(
                    classification.get("concept_ids"),
                    f"{item_where}.classification.concept_ids",
                    errors,
                ):
                    if concept_id not in concept_ids:
                        errors.append(f"{item_where}.classification.concept_ids: unknown concept {concept_id!r}")

            provenance = item.get("provenance")
            if provenance is not None:
                if not isinstance(provenance, dict):
                    errors.append(f"{item_where}.provenance: expected a mapping")
                else:
                    if provenance.get("voice") not in COMMUNITY_VOICES:
                        errors.append(f"{item_where}.provenance.voice: unsupported voice")
                    if provenance.get("parent_source_id") not in source_ids:
                        errors.append(f"{item_where}.provenance.parent_source_id: unknown source")
                    if not isinstance(provenance.get("locator"), dict):
                        errors.append(f"{item_where}.provenance.locator: expected a mapping")
                    if not _is_date(provenance.get("captured_at")):
                        errors.append(f"{item_where}.provenance.captured_at: expected ISO 8601 date")

            verification = item.get("verification")
            if verification is not None:
                if not isinstance(verification, dict):
                    errors.append(f"{item_where}.verification: expected a mapping")
                else:
                    if verification.get("status") not in VERIFICATION_STATUSES:
                        errors.append(f"{item_where}.verification.status: unsupported status")
                    for reference in _strings(
                        verification.get("sources"),
                        f"{item_where}.verification.sources",
                        errors,
                    ):
                        if reference not in source_ids and not reference.startswith(("https://", "http://")):
                            errors.append(f"{item_where}.verification.sources: unknown source {reference!r}")

            destinations = item.get("candidate_destinations", {})
            if isinstance(destinations, dict):
                for page_id in _strings(
                    destinations.get("pages"),
                    f"{item_where}.candidate_destinations.pages",
                    errors,
                ):
                    if page_id not in pages:
                        errors.append(f"{item_where}.candidate_destinations.pages: unknown page {page_id!r}")

    return errors


def main() -> int:
    errors = validate_source_catalogue()
    if errors:
        sys.stderr.write("Source catalogue validation failed:\n")
        for error in errors:
            sys.stderr.write(f"- {error}\n")
        return 1
    sys.stdout.write("Source catalogue and extraction records are valid.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
