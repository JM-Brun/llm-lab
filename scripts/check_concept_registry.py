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
    "prerequisite",
    "part-of",
    "generalizes",
    "contrasts-with",
    "analogy",
    "implemented-by",
    "applies-to",
    "constrains",
    "produces",
    "normalized-by",
    "evaluated-by",
    "represented-by",
    "contributes-to",
    "mapped-by",
}
PAGE_ID = re.compile(r"(?:fr|en)/[a-z0-9]+(?:-[a-z0-9]+)*")


def _published_page_ids() -> set[str]:
    """Return stable IDs of published FR/EN Quarto pages."""
    published: set[str] = set()
    for language in ("fr", "en"):
        for path in (ROOT / "site" / language).glob("*.qmd"):
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
            if tags.get("status") == "published":
                page_id = metadata.get("id")
                if isinstance(page_id, str):
                    published.add(page_id)
    return published


def _has_cycle(edges: dict[str, list[str]]) -> bool:
    """Return whether a directed adjacency list contains a cycle."""
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(target) for target in edges.get(node, [])):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in edges)


def validate_registry(data: Any, published_pages: set[str] | None = None) -> list[str]:
    """Return schema, bilingual, and referential-integrity errors."""
    errors: list[str] = []
    if (
        not isinstance(data, dict)
        or type(data.get("schema_version")) is not int
        or data.get("schema_version") != 1
    ):
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

        for field in ("labels", "definitions"):
            values = concept.get(field)
            if not isinstance(values, dict) or set(values) != {"fr", "en"}:
                errors.append(f"{where}.{field}: expected exactly fr and en")
            elif not all(isinstance(value, str) and value.strip() for value in values.values()):
                errors.append(f"{where}.{field}: values must be non-empty strings")

        resources = concept.get("resources")
        if not isinstance(resources, list) or not resources:
            errors.append(f"{where}.resources: expected a non-empty list of page IDs")
            continue
        if all(isinstance(item, str) for item in resources) and len(resources) != len(
            set(resources)
        ):
            errors.append(f"{where}.resources: duplicate resource IDs")
        for page_id in resources:
            if not isinstance(page_id, str) or not PAGE_ID.fullmatch(page_id):
                errors.append(f"{where}.resources: invalid page ID {page_id!r}")
            elif published_pages is not None and page_id not in published_pages:
                errors.append(
                    f"{where}.resources: page {page_id!r} is not a published page"
                )

    relations = data.get("relations")
    if not isinstance(relations, list):
        errors.append("relations: expected a list")
        return errors

    seen: set[tuple[str, str, str]] = set()
    prerequisite_edges: dict[str, list[str]] = {}
    generalization_edges: dict[str, list[str]] = {}
    for index, relation in enumerate(relations):
        where = f"relations[{index}]"
        if not isinstance(relation, dict):
            errors.append(f"{where}: expected mapping")
            continue
        source, kind, target = (relation.get(key) for key in ("from", "type", "to"))
        if not isinstance(source, str) or source not in identifiers:
            errors.append(f"{where}.from: unknown concept {source!r}")
        if not isinstance(target, str) or target not in identifiers:
            errors.append(f"{where}.to: unknown concept {target!r}")
        if not isinstance(kind, str) or kind not in RELATION_TYPES:
            errors.append(f"{where}.type: unsupported relation {kind!r}")
        if isinstance(source, str) and isinstance(target, str) and source == target:
            errors.append(f"{where}: self-relations are not allowed")
        if all(isinstance(value, str) for value in (source, kind, target)):
            key = (source, kind, target)
            if key in seen:
                errors.append(f"{where}: duplicate relation {key!r}")
            seen.add(key)
            if source in identifiers and target in identifiers:
                if kind == "prerequisite":
                    prerequisite_edges.setdefault(source, []).append(target)
                elif kind == "generalizes":
                    generalization_edges.setdefault(source, []).append(target)

    if _has_cycle(prerequisite_edges):
        errors.append("relations: prerequisite graph must be acyclic")
    if _has_cycle(generalization_edges):
        errors.append("relations: generalization graph must be acyclic")
    return errors


def main() -> int:
    """Validate the checked-in registry."""
    try:
        data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        sys.stderr.write(f"Cannot read concept registry: {exc}\n")
        return 1
    errors = validate_registry(data, _published_page_ids())
    if errors:
        sys.stderr.write("\n".join(errors) + "\n")
        return 1
    sys.stdout.write(f"Validated {len(data['concepts'])} concepts and {len(data['relations'])} relations.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
