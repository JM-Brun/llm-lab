#!/usr/bin/env python3
"""Inventory historical extraction fields and destination references.

This report is observational: it separates canonical source links, item
classifications, candidate destinations, legacy destination fields, and
source-local teaching routes. It never promotes a proposal to an integration.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = yaml.safe_load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return value


def _strings(value: Any) -> tuple[list[str], int]:
    """Return non-empty strings and the number of non-string/empty entries."""
    if value is None:
        return [], 0
    if not isinstance(value, list):
        return [], 1
    refs = [entry for entry in value if isinstance(entry, str) and entry.strip()]
    return refs, len(value) - len(refs)


def _bucket() -> dict[str, Any]:
    return {"records_with_field": 0, "references": 0, "unique_references": [], "invalid_entries": 0}


def _add(bucket: dict[str, Any], value: Any) -> None:
    refs, invalid = _strings(value)
    bucket["records_with_field"] += 1
    bucket["references"] += len(refs)
    bucket["invalid_entries"] += invalid
    bucket["_values"].update(refs)


def build_report(root: Path) -> dict[str, Any]:
    data_dir = root / "data"
    sources_doc = _load(data_dir / "sources.yml")
    concepts_doc = _load(data_dir / "concepts.yml")
    sources = [item for item in sources_doc.get("sources", []) if isinstance(item, dict)]
    known_sources = {item.get("id") for item in sources if isinstance(item.get("id"), str)}
    known_concepts = {
        item.get("id")
        for item in concepts_doc.get("concepts", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    fields: Counter[str] = Counter()
    item_key_presence: Counter[str] = Counter()
    source_destinations = {
        "related.pages": _bucket(),
        "related.concepts": _bucket(),
        "classification.concept_ids": _bucket(),
        "related.routes": _bucket(),
    }
    item_destinations = {
        "candidate_destinations.pages": _bucket(),
        "candidate_destinations.concepts": _bucket(),
        "candidate_destinations.routes": _bucket(),
        "candidate_destinations.resources": _bucket(),
        "classification.concept_ids": _bucket(),
        "mapped_concepts": _bucket(),
        "target_resources": _bucket(),
        "target_pages": _bucket(),
        "target_concepts": _bucket(),
        "target_routes": _bucket(),
    }
    candidate_shape_counts: Counter[str] = Counter()
    local_teaching_routes = 0
    extraction_files = 0
    extraction_items = 0
    malformed_records: list[str] = []
    source_id_mismatches: list[str] = []
    unknown_source_ids: set[str] = set()
    extracted_source_ids: set[str] = set()
    unknown_concept_refs: dict[str, set[str]] = {
        key: set() for key in (
            "source.related.concepts",
            "source.classification.concept_ids",
            "item.candidate_destinations.concepts",
            "item.classification.concept_ids",
            "item.mapped_concepts",
        )
    }

    for source in sources:
        related = source.get("related")
        if isinstance(related, dict):
            for field in ("pages", "concepts", "routes"):
                key = f"related.{field}"
                if field in related:
                    _add(source_destinations[key], related[field])
                    refs, _ = _strings(related[field])
                    if field == "concepts":
                        unknown_concept_refs["source.related.concepts"].update(
                            set(refs) - known_concepts
                        )
        classification = source.get("classification")
        if isinstance(classification, dict) and "concept_ids" in classification:
            value = classification["concept_ids"]
            _add(source_destinations["classification.concept_ids"], value)
            refs, _ = _strings(value)
            unknown_concept_refs["source.classification.concept_ids"].update(
                set(refs) - known_concepts
            )

    for path in sorted((data_dir / "extractions").glob("*.yml")):
        extraction_files += 1
        record = _load(path)
        source_id = record.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            malformed_records.append(path.relative_to(root).as_posix())
        else:
            extracted_source_ids.add(source_id)
            if source_id not in known_sources:
                unknown_source_ids.add(source_id)
            if path.stem != source_id:
                source_id_mismatches.append(path.relative_to(root).as_posix())

        items = record.get("items", [])
        if not isinstance(items, list):
            malformed_records.append(path.relative_to(root).as_posix() + ":items-not-list")
            continue
        for item in items:
            if not isinstance(item, dict):
                malformed_records.append(path.relative_to(root).as_posix() + ":non-mapping-item")
                continue
            extraction_items += 1
            for key in item:
                item_key_presence[key] += 1
            for key in item_destinations:
                if key in item:
                    if key == "candidate_destinations":
                        continue
                    _add(item_destinations[key], item[key])
                    refs, _ = _strings(item[key])
                    if key == "classification.concept_ids":
                        unknown_concept_refs["item.classification.concept_ids"].update(
                            set(refs) - known_concepts
                        )
                    elif key == "mapped_concepts":
                        unknown_concept_refs["item.mapped_concepts"].update(
                            set(refs) - known_concepts
                        )
            candidate = item.get("candidate_destinations")
            if "candidate_destinations" in item:
                if not isinstance(candidate, dict):
                    candidate_shape_counts["non-mapping"] += 1
                else:
                    candidate_shape_counts["mapping"] += 1
                    for field in ("pages", "concepts", "routes", "resources"):
                        if field in candidate:
                            key = f"candidate_destinations.{field}"
                            _add(item_destinations[key], candidate[field])
                            refs, _ = _strings(candidate[field])
                            if field == "concepts":
                                unknown_concept_refs[
                                    "item.candidate_destinations.concepts"
                                ].update(set(refs) - known_concepts)
            model = record.get("pedagogical_model")
            if isinstance(model, dict):
                route = model.get("teaching_route")
                if isinstance(route, list):
                    local_teaching_routes += len(route)

    def finalize(buckets: dict[str, dict[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, bucket in buckets.items():
            result[key] = {
                "records_with_field": bucket["records_with_field"],
                "references": bucket["references"],
                "unique_references": sorted(bucket["_values"]),
                "unique_reference_count": len(bucket["_values"]),
                "invalid_entries": bucket["invalid_entries"],
            }
        return result

    for bucket in (*source_destinations.values(), *item_destinations.values()):
        bucket["_values"] = set()

    # The aggregation above uses a set for deterministic unique-reference output.
    # Rebuild it in a second pass because buckets are initialized after loading.
    # (The first pass is intentionally kept free of assumptions about field shapes.)
    # This second pass also guarantees that malformed legacy values stay visible.
    for source in sources:
        related = source.get("related")
        if isinstance(related, dict):
            for field in ("pages", "concepts", "routes"):
                if field in related:
                    refs, _ = _strings(related[field])
                    source_destinations[f"related.{field}"]["_values"].update(refs)
        classification = source.get("classification")
        if isinstance(classification, dict) and "concept_ids" in classification:
            refs, _ = _strings(classification["concept_ids"])
            source_destinations["classification.concept_ids"]["_values"].update(refs)

    for path in sorted((data_dir / "extractions").glob("*.yml")):
        record = _load(path)
        items = record.get("items", [])
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            for key in item_destinations:
                if key in item and key != "candidate_destinations":
                    refs, _ = _strings(item[key])
                    item_destinations[key]["_values"].update(refs)
            candidate = item.get("candidate_destinations")
            if isinstance(candidate, dict):
                for field in ("pages", "concepts", "routes", "resources"):
                    if field in candidate:
                        refs, _ = _strings(candidate[field])
                        item_destinations[f"candidate_destinations.{field}"]["_values"].update(refs)

    return {
        "schema_version": 1,
        "scope": {
            "sources_file": "data/sources.yml",
            "concepts_file": "data/concepts.yml",
            "extraction_directory": "data/extractions/",
            "matching_rule": "extraction.source_id -> sources[].id; filename equality reported separately",
        },
        "counts": {
            "sources": len(sources),
            "extraction_files": extraction_files,
            "extraction_items": extraction_items,
            "items_with_candidate_destinations": sum(
                1 for value in item_key_presence if value == "candidate_destinations"
            ),
            "unknown_extraction_source_ids": len(unknown_source_ids),
            "filename_source_id_mismatches": len(source_id_mismatches),
            "malformed_records_or_items": len(malformed_records),
            "local_teaching_route_steps": local_teaching_routes,
        },
        "item_field_presence": dict(sorted(item_key_presence.items())),
        "candidate_destination_shapes": dict(sorted(candidate_shape_counts.items())),
        "source_destinations": finalize(source_destinations),
        "item_destinations": finalize(item_destinations),
        "unknown_concept_references": {
            key: sorted(values) for key, values in unknown_concept_refs.items()
        },
        "exceptions": {
            "unknown_extraction_source_ids": sorted(unknown_source_ids),
            "filename_source_id_mismatches": sorted(source_id_mismatches),
            "malformed_records_or_items": sorted(malformed_records),
        },
        "interpretation": {
            "candidate_destinations": "Editorial proposals, not evidence of integration.",
            "mapped_concepts": "Legacy/authoring field counted separately from classification.concept_ids.",
            "target_resources": "Legacy/authoring resource references; not assumed to be page IDs or routes.",
            "teaching_route": "Source-local pedagogical sequence, not a canonical destination route.",
            "unknown_references": "Reported for review; not promoted to validation errors by this report.",
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Extraction destination and field inventory",
        "",
        "Read-only inventory. Proposals, classifications, resource references, and source-local teaching routes are kept separate.",
        "",
        "## Corpus",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in report["counts"].items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Item field presence", "", "| Field | Items |", "|---|---:|"])
    for key, value in report["item_field_presence"].items():
        lines.append(f"| `{key}` | {value} |")
    for section in ("source_destinations", "item_destinations"):
        lines.extend(["", f"## {section.replace('_', ' ').title()}", "", "| Field | Records with field | References | Unique | Invalid entries |", "|---|---:|---:|---:|---:|"])
        for key, value in report[section].items():
            lines.append(
                f"| `{key}` | {value['records_with_field']} | {value['references']} | "
                f"{value['unique_reference_count']} | {value['invalid_entries']} |"
            )
    lines.extend(["", "## Candidate destination shapes", ""])
    for key, value in report["candidate_destination_shapes"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Unknown concept references", ""])
    for key, values in report["unknown_concept_references"].items():
        lines.append(f"- **{key}:** {len(values)}")
        for value in values:
            lines.append(f"  - `{value}`")
    lines.extend(["", "## Interpretation", ""])
    for key, value in report["interpretation"].items():
        lines.append(f"- **{key}:** {value}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, help="Write the report to a file instead of stdout.")
    args = parser.parse_args()
    try:
        report = build_report(args.root.resolve())
    except (OSError, ValueError, yaml.YAMLError) as exc:
        sys.stderr.write(f"Cannot build extraction destination inventory: {exc}\n")
        return 2
    rendered = (
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.format == "json"
        else render_markdown(report)
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
