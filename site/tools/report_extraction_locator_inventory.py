#!/usr/bin/env python3
"""Inventory extraction locator shapes without imposing new validation rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _value_shape(value: Any) -> str:
    if not isinstance(value, str):
        return f"non-string:{type(value).__name__}"
    text = value.strip()
    if not text:
        return "empty"
    if re.match(r"^https?://", text, re.IGNORECASE):
        return "http-url"
    if re.match(r"^(?:\d{1,2}:)?\d{1,2}:\d{2}(?:\.\d+)?$", text):
        return "timestamp-like"
    if re.match(r"^(?:p(?:age)?\s*)?\d+(?:\s*[-\u2013]\s*\d+)?$", text, re.IGNORECASE):
        return "page-number-like"
    if re.search(r"(?:^|\b)(?:line|lines|l\.)\s*\d+", text, re.IGNORECASE):
        return "line-reference-like"
    if re.search(r"\b(?:section|chapter|part|appendix)\b", text, re.IGNORECASE):
        return "section-like"
    return "opaque-text"


def collect_inventory(root: Path = ROOT) -> dict[str, Any]:
    extraction_dir = root / "data" / "extractions"
    files = sorted(extraction_dir.glob("*.yml"))
    types: Counter[str] = Counter()
    shapes: Counter[str] = Counter()
    key_shapes: Counter[str] = Counter()
    non_mapping_shapes: Counter[str] = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    non_mapping_examples: dict[str, list[str]] = defaultdict(list)
    missing = 0
    non_mapping = 0
    malformed = 0
    malformed_items = 0
    items_count = 0
    yaml_errors: list[dict[str, str]] = []

    for path in files:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            yaml_errors.append({"file": path.name, "error": str(exc)})
            continue
        if not isinstance(data, dict) or not isinstance(data.get("items"), list):
            yaml_errors.append({"file": path.name, "error": "expected mapping with items list"})
            continue
        for index, item in enumerate(data["items"]):
            items_count += 1
            record_path = f"{path.name}:items[{index}]"
            if not isinstance(item, dict):
                malformed_items += 1
                continue
            if "locator" not in item or item["locator"] is None:
                missing += 1
                continue
            locator = item["locator"]
            if not isinstance(locator, dict):
                non_mapping += 1
                shape = f"{type(locator).__name__}::{_value_shape(locator)}"
                non_mapping_shapes[shape] += 1
                if len(non_mapping_examples[shape]) < 3:
                    non_mapping_examples[shape].append(record_path)
                continue
            key_shapes[",".join(sorted(str(key) for key in locator))] += 1
            locator_type = locator.get("type")
            if not isinstance(locator_type, str) or not locator_type.strip():
                malformed += 1
                locator_type = "<missing-or-invalid-type>"
            types[locator_type] += 1
            value = locator.get("value")
            if value is None or (isinstance(value, str) and not value.strip()):
                malformed += 1
            shape = _value_shape(value)
            shapes[f"{locator_type}::{shape}"] += 1
            if len(examples[f"{locator_type}::{shape}"]) < 3:
                examples[f"{locator_type}::{shape}"].append(record_path)

    return {
        "inventory": "extraction-locator-shapes",
        "scope": "data/extractions/*.yml",
        "files_seen": len(files),
        "items_seen": items_count,
        "items_without_locator": missing,
        "items_with_non_mapping_locator": non_mapping,
        "items_with_non_mapping_locator_by_shape": dict(sorted(non_mapping_shapes.items())),
        "non_mapping_locator_examples": dict(sorted(non_mapping_examples.items())),
        "items_with_non_mapping_extraction_record": malformed_items,
        "locators_with_missing_or_invalid_required_fields": malformed,
        "yaml_or_record_errors": yaml_errors,
        "locator_types": dict(sorted(types.items())),
        "locator_key_shapes": dict(sorted(key_shapes.items())),
        "value_shapes_by_type": dict(sorted(shapes.items())),
        "representative_record_paths": dict(sorted(examples.items())),
        "interpretation": (
            "Observed shape inventory only. Missing locators, scalar/non-mapping locators, "
            "malformed mappings and mapping value shapes are counted separately. It does not "
            "assert that a locator resolves, that its source was inspected, or that a "
            "type-specific grammar is correct."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = collect_inventory(args.root)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 1 if report["yaml_or_record_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
