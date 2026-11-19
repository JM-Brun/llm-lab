#!/usr/bin/env python3
"""Inventory historical extraction fields and destination references.

This read-only report separates source links, item classifications, candidate
destinations, legacy destination fields, and source-local teaching routes.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
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
    if not isinstance(value, list):
        return [], int(value is not None)
    refs = [entry for entry in value if isinstance(entry, str) and entry.strip()]
    return refs, len(value) - len(refs)


def _bucket() -> dict[str, Any]:
    return {
        "records_with_field": 0,
        "references": 0,
        "invalid_entries": 0,
        "_values": set(),
    }


def _add(bucket: dict[str, Any], value: Any) -> list[str]:
    refs, invalid = _strings(value)
    bucket["records_with_field"] += 1
    bucket["references"] += len(refs)
    bucket["invalid_entries"] += invalid
    bucket["_values"].update(refs)
    return refs


def _finalize(buckets: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        key: {
            "records_with_field": bucket["records_with_field"],
            "references": bucket["references"],
            "unique_references": sorted(bucket["_values"]),
            "unique_reference_count": len(bucket["_values"]),
            "invalid_entries": bucket["invalid_entries"],
        }
        for key, bucket in buckets.items()
    }


def build_report(root: Path) -> dict[str, Any]:
    data_dir = root / "data"
    sources_doc = _load(data_dir / "sources.yml")
    concepts_doc = _load(data_dir / "concepts.yml")
    sources = [item for item in sources_doc.get("sources", []) if isinstance(item, dict)]
    known_sources = {item["id"] for item in sources if isinstance(item.get("id"), str)}
    known_concepts = {
        item["id"]
        for item in concepts_doc.get("concepts", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    source_destinations = {
        key: _bucket()
        for key in (
            "related.pages",
            "related.concepts",
            "related.routes",
            "classification.concept_ids",
        )
    }
    item_destinations = {
        key: _bucket()
        for key in (
            "candidate_destinations.pages",
            "candidate_destinations.concepts",
            "candidate_destinations.routes",
            "candidate_destinations.resources",
            "classification.concept_ids",
            "mapped_concepts",
            "target_resources",
            "target_pages",
            "target_concepts",
            "target_routes",
        )
    }
    item_key_presence: Counter[str] = Counter()
    candidate_shapes: Counter[str] = Counter()
    unknown_concepts: dict[str, set[str]] = {
        key: set()
        for key in (
            "source.related.concepts",
            "source.classification.concept_ids",
            "item.candidate_destinations.concepts",
            "item.classification.concept_ids",
            "item.mapped_concepts",
        )
    }
    unknown_concept_occurrences: dict[str, dict[str, list[dict[str, Any]]]] = {
        key: defaultdict(list) for key in unknown_concepts
    }
    extraction_files = extraction_items = candidate_items = local_route_steps = 0
    malformed: list[str] = []
    filename_mismatches: list[str] = []
    unknown_sources: set[str] = set()

    for source in sources:
        related = source.get("related")
        if isinstance(related, dict):
            for field in ("pages", "concepts", "routes"):
                if field in related:
                    refs = _add(source_destinations[f"related.{field}"], related[field])
                    if field == "concepts":
                        unknown = set(refs) - known_concepts
                        unknown_concepts["source.related.concepts"].update(unknown)
                        for concept_id in unknown:
                            unknown_concept_occurrences["source.related.concepts"][concept_id].append(
                                {"source_id": source.get("id")}
                            )
        classification = source.get("classification")
        if isinstance(classification, dict) and "concept_ids" in classification:
            refs = _add(
                source_destinations["classification.concept_ids"], classification["concept_ids"]
            )
            unknown = set(refs) - known_concepts
            unknown_concepts["source.classification.concept_ids"].update(unknown)
            for concept_id in unknown:
                unknown_concept_occurrences["source.classification.concept_ids"][concept_id].append(
                    {"source_id": source.get("id")}
                )

    for path in sorted((data_dir / "extractions").glob("*.yml")):
        extraction_files += 1
        relative_path = path.relative_to(root).as_posix()
        record = _load(path)
        source_id = record.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            malformed.append(relative_path + ":missing-source-id")
        else:
            if source_id not in known_sources:
                unknown_sources.add(source_id)
            if path.stem != source_id:
                filename_mismatches.append(relative_path)

        model = record.get("pedagogical_model")
        if isinstance(model, dict) and isinstance(model.get("teaching_route"), list):
            local_route_steps += len(model["teaching_route"])

        items = record.get("items", [])
        if not isinstance(items, list):
            malformed.append(relative_path + ":items-not-list")
            continue
        for item in items:
            if not isinstance(item, dict):
                malformed.append(relative_path + ":non-mapping-item")
                continue
            extraction_items += 1
            item_key_presence.update(item.keys())

            classification = item.get("classification")
            if isinstance(classification, dict) and "concept_ids" in classification:
                refs = _add(
                    item_destinations["classification.concept_ids"], classification["concept_ids"]
                )
                unknown_concepts["item.classification.concept_ids"].update(
                    set(refs) - known_concepts
                )

            for field in (
                "mapped_concepts",
                "target_resources",
                "target_pages",
                "target_concepts",
                "target_routes",
            ):
                if field in item:
                    refs = _add(item_destinations[field], item[field])
                    if field == "mapped_concepts":
                        unknown = set(refs) - known_concepts
                        unknown_concepts["item.mapped_concepts"].update(unknown)
                        for concept_id in unknown:
                            unknown_concept_occurrences["item.mapped_concepts"][concept_id].append(
                                {"extraction_file": relative_path, "item_id": item.get("id")}
                            )

            candidate = item.get("candidate_destinations")
            if "candidate_destinations" in item:
                candidate_items += 1
                if not isinstance(candidate, dict):
                    candidate_shapes["non-mapping"] += 1
                else:
                    candidate_shapes["mapping"] += 1
                    for field in ("pages", "concepts", "routes", "resources"):
                        if field in candidate:
                            refs = _add(
                                item_destinations[f"candidate_destinations.{field}"],
                                candidate[field],
                            )
                            if field == "concepts":
                                unknown = set(refs) - known_concepts
                                unknown_concepts["item.candidate_destinations.concepts"].update(unknown)
                                for concept_id in unknown:
                                    unknown_concept_occurrences[
                                        "item.candidate_destinations.concepts"
                                    ][concept_id].append(
                                        {"extraction_file": relative_path, "item_id": item.get("id")}
                                    )

    return {
        "schema_version": 1,
        "scope": {
            "sources_file": "data/sources.yml",
            "concepts_file": "data/concepts.yml",
            "extraction_directory": "data/extractions/",
            "matching_rule": "extraction.source_id -> sources[].id; filename equality is a separate diagnostic",
        },
        "counts": {
            "sources": len(sources),
            "extraction_files": extraction_files,
            "extraction_items": extraction_items,
            "items_with_candidate_destinations": candidate_items,
            "unknown_extraction_source_ids": len(unknown_sources),
            "filename_source_id_mismatches": len(filename_mismatches),
            "malformed_records_or_items": len(malformed),
            "source_local_teaching_route_steps": local_route_steps,
        },
        "item_field_presence": dict(sorted(item_key_presence.items())),
        "candidate_destination_shapes": dict(sorted(candidate_shapes.items())),
        "source_destinations": _finalize(source_destinations),
        "item_destinations": _finalize(item_destinations),
        "unknown_concept_references": {
            key: sorted(values) for key, values in unknown_concepts.items()
        },
        "unknown_concept_reference_occurrences": {
            key: {concept_id: locations for concept_id, locations in sorted(values.items())}
            for key, values in unknown_concept_occurrences.items()
        },
        "exceptions": {
            "unknown_extraction_source_ids": sorted(unknown_sources),
            "filename_source_id_mismatches": sorted(filename_mismatches),
            "malformed_records_or_items": sorted(malformed),
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
        lines.extend(
            [
                "",
                f"## {section.replace('_', ' ').title()}",
                "",
                "| Field | Records with field | References | Unique | Invalid entries |",
                "|---|---:|---:|---:|---:|",
            ]
        )
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
