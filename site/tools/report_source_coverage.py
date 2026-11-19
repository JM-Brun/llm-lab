#!/usr/bin/env python3
"""Report source-to-knowledge coverage without changing catalogue records.

This is a coverage diagnostic, not a replacement for check_source_catalogue.py.
Unknown metadata and missing pedagogical links are reported as review alerts;
only malformed or dangling references are reported as integrity errors.
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


def build_report(root: Path) -> dict[str, Any]:
    """Build deterministic source, extraction, concept, and destination metrics."""
    data_dir = root / "data"
    sources_doc = _load(data_dir / "sources.yml")
    concepts_doc = _load(data_dir / "concepts.yml")
    collections_doc = _load(data_dir / "source-collections.yml")
    sources = [item for item in sources_doc.get("sources", []) if isinstance(item, dict)]
    concepts = [item for item in concepts_doc.get("concepts", []) if isinstance(item, dict)]

    extraction_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    orphan_extractions: list[str] = []
    extraction_item_count = 0
    extraction_record_count = 0
    for path in sorted((data_dir / "extractions").glob("*.yml")):
        extraction_record_count += 1
        record = _load(path)
        source_id = record.get("source_id")
        items = record.get("items", [])
        if not isinstance(items, list):
            items = []
        extraction_item_count += len(items)
        if not isinstance(source_id, str) or not source_id:
            orphan_extractions.append(path.relative_to(root).as_posix())
        else:
            extraction_by_source[source_id].append(record)

    source_ids = {source.get("id") for source in sources if isinstance(source.get("id"), str)}
    known_concepts = {
        concept.get("id") for concept in concepts if isinstance(concept.get("id"), str)
    }
    unknown_extraction_sources = sorted(set(extraction_by_source) - source_ids)
    orphan_extractions.extend(unknown_extraction_sources)

    concept_sources: dict[str, set[str]] = defaultdict(set)
    unknown_concept_references: set[str] = set()
    source_without_concept: list[str] = []
    source_without_destination: list[str] = []
    sources_without_extraction: list[dict[str, Any]] = []
    unknown_dates: list[str] = []
    unknown_licences: list[str] = []
    scan_history_mismatches: list[str] = []
    source_status_counts: Counter[str] = Counter()
    integration_status_counts: Counter[str] = Counter()
    scan_status_counts: Counter[str] = Counter()

    for source in sources:
        source_id = str(source.get("id", "<missing-id>"))
        scan_status = str(source.get("scan_status", "missing"))
        integration_status = str(source.get("integration_status", "missing"))
        scan_status_counts[scan_status] += 1
        integration_status_counts[integration_status] += 1
        source_status_counts[f"{scan_status} / {integration_status}"] += 1

        if source.get("publication_date") in (None, ""):
            unknown_dates.append(source_id)
        licence = source.get("licence")
        if not isinstance(licence, dict) or licence.get("status") in (None, "", "unknown"):
            unknown_licences.append(source_id)

        history = source.get("scan_history", [])
        if isinstance(history, list) and history:
            last_status = history[-1].get("status") if isinstance(history[-1], dict) else None
            if last_status and last_status != scan_status:
                scan_history_mismatches.append(source_id)

        concept_ids: set[str] = set()
        classification = source.get("classification")
        if isinstance(classification, dict):
            concept_ids.update(
                value for value in classification.get("concept_ids", []) if isinstance(value, str)
            )
        related = source.get("related")
        pages: set[str] = set()
        audit_records: list[str] = []
        if isinstance(related, dict):
            concept_ids.update(
                value for value in related.get("concepts", []) if isinstance(value, str)
            )
            pages.update(value for value in related.get("pages", []) if isinstance(value, str))
            audit_records = [
                value for value in related.get("audit_records", []) if isinstance(value, str)
            ]

        records = extraction_by_source.get(source_id, [])
        for record in records:
            for item in record.get("items", []) if isinstance(record.get("items"), list) else []:
                if not isinstance(item, dict):
                    continue
                item_classification = item.get("classification")
                if isinstance(item_classification, dict):
                    concept_ids.update(
                        value
                        for value in item_classification.get("concept_ids", [])
                        if isinstance(value, str)
                    )

        unknown_concept_references.update(concept_ids - known_concepts)
        valid_concepts = concept_ids & known_concepts
        for concept_id in valid_concepts:
            concept_sources[concept_id].add(source_id)
        if not valid_concepts:
            source_without_concept.append(source_id)
        if not pages:
            source_without_destination.append(source_id)
        if not records:
            sources_without_extraction.append(
                {
                    "id": source_id,
                    "integration_status": integration_status,
                    "audit_records": audit_records,
                }
            )

    concepts_without_sources = sorted(
        concept_id for concept_id in known_concepts if not concept_sources.get(concept_id)
    )
    low_coverage_concepts = sorted(
        (
            {"id": concept_id, "source_count": len(concept_sources[concept_id])}
            for concept_id in known_concepts
            if 0 < len(concept_sources[concept_id]) < 2
        ),
        key=lambda item: (item["source_count"], item["id"]),
    )

    collection_entries = [
        item for item in collections_doc.get("collections", []) if isinstance(item, dict)
    ]
    collection_source_ids: dict[str, set[str]] = {
        str(item["id"]): set() for item in collection_entries if isinstance(item.get("id"), str)
    }
    collection_extraction_records: Counter[str] = Counter()
    collection_extraction_items: Counter[str] = Counter()
    explicit_collection_decisions: set[str] = set()
    explicit_unassigned_sources: set[str] = set()
    for source in sources:
        source_id = source.get("id")
        if not isinstance(source_id, str) or "collections" not in source:
            continue
        explicit_collection_decisions.add(source_id)
        memberships = source.get("collections")
        if not isinstance(memberships, list):
            continue  # Structural errors are reported by check_source_catalogue.py.
        if not memberships:
            explicit_unassigned_sources.add(source_id)
        for collection_id in memberships:
            if not isinstance(collection_id, str) or collection_id not in collection_source_ids:
                continue
            collection_source_ids[collection_id].add(source_id)
            records = extraction_by_source.get(source_id, [])
            collection_extraction_records[collection_id] += len(records)
            collection_extraction_items[collection_id] += sum(
                len(record.get("items", []))
                for record in records
                if isinstance(record.get("items"), list)
            )
    collection_coverage = {
        "counts": {
            "sources_with_explicit_decision": len(explicit_collection_decisions),
            "sources_explicitly_unassigned": len(explicit_unassigned_sources),
            "sources_without_explicit_decision": len(sources) - len(explicit_collection_decisions),
            "total_source_memberships": sum(
                len(values) for values in collection_source_ids.values()
            ),
        },
        "collections": {
            collection_id: {
                "source_records": len(source_ids_for_collection),
                "extraction_files": collection_extraction_records[collection_id],
                "atomic_items": collection_extraction_items[collection_id],
            }
            for collection_id, source_ids_for_collection in sorted(collection_source_ids.items())
        },
        "join_rule": "extraction.source_id -> source.id -> source.collections",
    }

    return {
        "schema_version": 1,
        "scope": {
            "sources_file": "data/sources.yml",
            "extraction_directory": "data/extractions/",
            "concepts_file": "data/concepts.yml",
            "matching_rule": "extraction.source_id (never filename matching)",
        },
        "counts": {
            "sources": len(sources),
            "extraction_records": extraction_record_count,
            "extraction_items": extraction_item_count,
            "concepts": len(known_concepts),
            "sources_without_extraction": len(sources_without_extraction),
            "integrated_sources_without_extraction": sum(
                item["integration_status"] == "integrated" for item in sources_without_extraction
            ),
            "sources_without_extraction_with_audit_record": sum(
                bool(item["audit_records"]) for item in sources_without_extraction
            ),
            "sources_without_extraction_without_audit_record": sum(
                not item["audit_records"] for item in sources_without_extraction
            ),
            "sources_without_concept_link": len(source_without_concept),
            "sources_without_page_destination": len(source_without_destination),
            "concepts_without_source": len(concepts_without_sources),
            "concepts_with_one_source": len(low_coverage_concepts),
            "publication_dates_unknown": len(unknown_dates),
            "licence_status_unknown": len(unknown_licences),
            "extraction_source_references_unknown": len(orphan_extractions),
            "concept_references_unknown": len(unknown_concept_references),
            "scan_history_status_mismatches": len(scan_history_mismatches),
        },
        "collection_coverage": collection_coverage,
        "status_distribution": {
            "scan": dict(sorted(scan_status_counts.items())),
            "integration": dict(sorted(integration_status_counts.items())),
            "combined": dict(sorted(source_status_counts.items())),
        },
        "review_queues": {
            "sources_without_extraction": sources_without_extraction,
            "integrated_sources_without_extraction": [
                item["id"]
                for item in sources_without_extraction
                if item["integration_status"] == "integrated"
            ],
            "sources_without_extraction_with_audit_record": [
                item["id"] for item in sources_without_extraction if item["audit_records"]
            ],
            "sources_without_extraction_without_audit_record": [
                item["id"] for item in sources_without_extraction if not item["audit_records"]
            ],
            "sources_without_concept_link": sorted(source_without_concept),
            "sources_without_page_destination": sorted(source_without_destination),
            "concepts_without_source": concepts_without_sources,
            "concepts_with_one_source": low_coverage_concepts,
            "publication_dates_unknown": sorted(unknown_dates),
            "licence_status_unknown": sorted(unknown_licences),
            "extraction_source_references_unknown": sorted(orphan_extractions),
            "concept_references_unknown": sorted(unknown_concept_references),
            "scan_history_status_mismatches": sorted(scan_history_mismatches),
        },
        "interpretation": {
            "sources_without_extraction": (
                "Review queue, not an error: record an explicit defer/reject/already-covered "
                "decision where appropriate; do not create empty extraction files."
            ),
            "audit_record_links": (
                "A related.audit_records link is a navigation aid, not proof that the audit "
                "contains a source-specific extraction decision or item-level evidence. "
                "Review the linked record before treating a source as already covered."
            ),
            "concepts_with_one_source": (
                "Coverage signal only. A single authoritative source may be sufficient; "
                "corroboration requires domain-specific human review."
            ),
            "unknown_metadata": (
                "Coverage alerts, not validation failures. Preserve unknown values until "
                "independently verified."
            ),
            "contradictions": (
                "Not inferred automatically. Compare claims, evidence, scope, dates, and "
                "methods during human source review."
            ),
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    counts = report["counts"]
    lines = [
        "# Source-to-knowledge coverage report",
        "",
        "Generated from the canonical source register, extraction records, and concept graph.",
        "This is a diagnostic snapshot; it does not modify source records.",
        "",
        "## Coverage",
        "",
        "| Metric | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    collection_coverage = report.get("collection_coverage", {})
    collection_counts = collection_coverage.get("counts", {})
    lines.extend(["", "## Explicit collection coverage", ""])
    lines.append(f"Join rule: `{collection_coverage.get('join_rule', 'not available')}`")
    lines.append("")
    lines.append("| Measure | Count |")
    lines.append("|---|---:|")
    for key, value in collection_counts.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "### Per collection", ""])
    lines.append("| Collection | Source records | Extraction files | Atomic items |")
    lines.append("|---|---:|---:|---:|")
    for collection_id, metrics in collection_coverage.get("collections", {}).items():
        lines.append(
            f"| {collection_id} | {metrics['source_records']} | "
            f"{metrics['extraction_files']} | {metrics['atomic_items']} |"
        )
    lines.extend(["", "## Status distribution", ""])
    for dimension, values in report["status_distribution"].items():
        lines.append(f"### {dimension}")
        lines.append("")
        for status, count in values.items():
            lines.append(f"- {status}: {count}")
        lines.append("")
    lines.extend(["## Review queues", ""])
    for queue, values in report["review_queues"].items():
        lines.append(f"### {queue.replace('_', ' ')} ({len(values)})")
        lines.append("")
        if not values:
            lines.append("- None")
        else:
            for value in values:
                if isinstance(value, dict):
                    lines.append(
                        f"- {value.get('id')}: integration status "
                        f"`{value.get('integration_status')}`; "
                        f"{len(value.get('audit_records', []))} linked audit record(s)"
                    )
                else:
                    lines.append(f"- {value}")
        lines.append("")
    lines.extend(["## Interpretation and limits", ""])
    for key, explanation in report["interpretation"].items():
        lines.append(f"- **{key.replace('_', ' ')}:** {explanation}")
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
        sys.stderr.write(f"Cannot build source coverage report: {exc}\n")
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
