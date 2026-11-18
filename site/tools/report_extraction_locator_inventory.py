#!/usr/bin/env python3
"""Inventory extraction locator shapes without imposing new validation rules."""

from __future__ import annotations

import argparse
import json
import re
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
    if re.match(r"^(?:p(?:age)?\s*)?\d+(?:\s*[-–]\s*\d+)?$", text, re.IGNORECASE):
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
    examples: dict[str, list[str]] = defaultdict(list)
    missing = 0
    malformed = 0
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
            locator = item.get("locator") if isinstance(item, dict) else None
            if not isinstance(locator, dict):
                missing += 1
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
                examples[f"{locator_type}::{shape}"].append(
                    f"{path.name}:items[{index}]"
                )

    return {
        "inventory": "extraction-locator-shapes",
        "scope": "data/extractions/*.yml",
        "files_seen": len(files),
        "items_seen": items_count,
        "items_without_locator_mapping": missing,
        "locators_with_missing_or_invalid_required_fields": malformed,
        "yaml_or_record_errors": yaml_errors,
        "locator_types": dict(sorted(types.items())),
        "locator_key_shapes": dict(sorted(key_shapes.items())),
        "value_shapes_by_type": dict(sorted(shapes.items())),
        "representative_record_paths": dict(sorted(examples.items())),
        "interpretation": (
            "Observed shape inventory only. It does not assert that a locator resolves, "
            "that its source was inspected, or that a type-specific grammar is correct."
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
    print(rendered, end="")
    return 1 if report["yaml_or_record_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
