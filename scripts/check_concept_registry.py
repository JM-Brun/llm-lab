#!/usr/bin/env python3
"""Validate the language-independent concept registry."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "concepts.yml"
IDENTIFIER = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
RELATION_TYPES = {
    "prerequisite", "part-of", "generalizes", "contrasts-with",
    "analogy", "implemented-by", "applies-to", "constrains",
    "produces", "normalized-by", "evaluated-by",
}
PAGE_ID = re.compile(r"(?:fr|en)/[a-z0-9]+(?:-[a-z0-9]+)*")


def validate_registry(data: Any) -> list[str]:
    """Return all schema and referential-integrity errors."""
    errors: list[str] = []
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return ["registry: expected mapping with schema_version: 1"]
    concepts = data.get("concepts")
    if not isinstance(concepts, list) or not concepts:
        return ["concepts: expected a non-empty list"]
    identifiers: set[str] = set()
    for index, concept in enumerate(concepts):
        where = f"concepts[{index}]"
        if not isinstance(concept, dict):
            errors.append(f"{where}: expected mapping")
            continue
        identifier = concept.get("id")
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
            errors.append(f"{where}.id: expected stable kebab-case identifier")
        elif identifier in identifiers:
            errors.append(f"{where}.id: duplicate identifier {identifier!r}")
        else:
            identifiers.add(identifier)
        labels = concept.get("labels")
        definitions = concept.get("definitions")
        for field, values in (("labels", labels), ("definitions", definitions)):
            if not isinstance(values, dict) or set(values) != {"fr", "en"}:
                errors.append(f"{where}.{field}: expected exactly fr and en")
            elif not all(isinstance(value, str) and value.strip() for value in values.values()):
                errors.append(f"{where}.{field}: values must be non-empty strings")
        resources = concept.get("resources")
        if not isinstance(resources, list):
            errors.append(f"{where}.resources: expected a list of page IDs")
        else:
            for page_id in resources:
                if not isinstance(page_id, str) or not PAGE_ID.fullmatch(page_id):
                    errors.append(f"{where}.resources: invalid page ID {page_id!r}")
    relations = data.get("relations")
    if not isinstance(relations, list):
        errors.append("relations: expected a list")
        return errors
    seen: set[tuple[str, str, str]] = set()
    for index, relation in enumerate(relations):
        where = f"relations[{index}]"
        if not isinstance(relation, dict):
            errors.append(f"{where}: expected mapping")
            continue
        source, kind, target = (relation.get(key) for key in ("from", "type", "to"))
        if source not in identifiers:
            errors.append(f"{where}.from: unknown concept {source!r}")
        if target not in identifiers:
            errors.append(f"{where}.to: unknown concept {target!r}")
        if source == target:
            errors.append(f"{where}: self-relations are not allowed")
        if kind not in RELATION_TYPES:
            errors.append(f"{where}.type: unsupported relation {kind!r}")
        key = (source, kind, target)
        if key in seen:
            errors.append(f"{where}: duplicate relation {key!r}")
        seen.add(key)
    return errors


def main() -> int:
    """Validate the checked-in registry."""
    try:
        data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        sys.stderr.write(f"Cannot read concept registry: {exc}\n")
        return 1
    errors = validate_registry(data)
    if errors:
        sys.stderr.write("\n".join(errors) + "\n")
        return 1
    sys.stdout.write(f"Validated {len(data['concepts'])} concepts and {len(data['relations'])} relations.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
