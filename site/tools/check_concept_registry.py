#!/usr/bin/env python3
"""Validate the language-independent concept registry."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data" / "concepts.yml"
DOMAINS = ROOT / "data" / "domains.yml"
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
RELATION_FAMILIES = {
    "structural",
    "pedagogical",
    "representational",
    "constraint",
    "functional",
    "evaluative",
    "associative",
}


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
    """Detect cycles iteratively, including in long dependency chains."""
    active: set[str] = set()
    visited: set[str] = set()
    for root in edges:
        if root in visited:
            continue
        active.add(root)
        stack = [(root, iter(edges.get(root, [])))]
        while stack:
            node, targets = stack[-1]
            target = next(targets, None)
            if target is None:
                stack.pop()
                active.remove(node)
                visited.add(node)
            elif target in active:
                return True
            elif target not in visited:
                active.add(target)
                stack.append((target, iter(edges.get(target, []))))
    return False


def validate_domains(data: Any) -> tuple[set[str], list[str]]:
    """Validate the controlled bilingual domain registry."""
    errors: list[str] = []
    if (
        not isinstance(data, dict)
        or type(data.get("schema_version")) is not int
        or data.get("schema_version") != 1
    ):
        return set(), ["domains: expected mapping with schema_version: 1"]
    entries = data.get("domains")
    if not isinstance(entries, list) or not entries:
        return set(), ["domains: expected a non-empty list"]
    identifiers: set[str] = set()
    for index, domain in enumerate(entries):
        where = f"domains[{index}]"
        if not isinstance(domain, dict):
            errors.append(f"{where}: expected mapping")
            continue
        identifier = domain.get("id")
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
            errors.append(f"{where}.id: expected stable kebab-case identifier")
        elif identifier in identifiers:
            errors.append(f"{where}.id: duplicate identifier {identifier!r}")
        else:
            identifiers.add(identifier)
        for field in ("labels", "descriptions", "guiding_questions"):
            values = domain.get(field)
            if not isinstance(values, dict) or set(values) != {"fr", "en"}:
                errors.append(f"{where}.{field}: expected exactly fr and en")
            elif not all(isinstance(value, str) and value.strip() for value in values.values()):
                errors.append(f"{where}.{field}: values must be non-empty strings")
    expected = {
        "architectures-mechanisms",
        "text-tokenization",
        "mathematical-tools-geometry",
        "probabilistic-foundations-training",
        "inference-efficiency",
        "scale-research",
    }
    if identifiers != expected:
        errors.append(
            f"domains: expected the six controlled domain IDs; "
            f"missing={sorted(expected - identifiers)}, extra={sorted(identifiers - expected)}"
        )
    return identifiers, errors


def validate_registry(
    data: Any,
    published_pages: set[str] | None = None,
    domain_ids: set[str] | None = None,
) -> list[str]:
    """Return schema, bilingual, and referential-integrity errors."""
    errors: list[str] = []
    if (
        not isinstance(data, dict)
        or type(data.get("schema_version")) is not int
        or data.get("schema_version") != 2
    ):
        return ["registry: expected mapping with schema_version: 2"]

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

        importance = concept.get("importance")
        if importance not in {"core", "supporting", "specialized"}:
            errors.append(
                f"{where}.importance: expected one of core, supporting, specialized"
            )

        memberships = concept.get("domains")
        if not isinstance(memberships, list) or not memberships:
            errors.append(f"{where}.domains: expected a non-empty list of domain IDs")
        elif not all(isinstance(item, str) for item in memberships):
            errors.append(f"{where}.domains: values must be strings")
        else:
            if len(memberships) != len(set(memberships)):
                errors.append(f"{where}.domains: duplicate domain IDs")
            if domain_ids is not None:
                for domain_id in memberships:
                    if domain_id not in domain_ids:
                        errors.append(f"{where}.domains: unknown domain {domain_id!r}")

        resources = concept.get("resources")
        if not isinstance(resources, list) or not resources:
            errors.append(f"{where}.resources: expected a non-empty list of page IDs")
            continue
        if all(isinstance(item, str) for item in resources) and len(resources) != len(
            set(resources)
        ):
            errors.append(f"{where}.resources: duplicate resource IDs")
        resource_languages: set[str] = set()
        for page_id in resources:
            if not isinstance(page_id, str) or not PAGE_ID.fullmatch(page_id):
                errors.append(f"{where}.resources: invalid page ID {page_id!r}")
            else:
                resource_languages.add(page_id.split("/", maxsplit=1)[0])
                if published_pages is not None and page_id not in published_pages:
                    errors.append(f"{where}.resources: page {page_id!r} is not a published page")
        missing_languages = {"fr", "en"} - resource_languages
        if missing_languages:
            errors.append(
                f"{where}.resources: missing language(s) {', '.join(sorted(missing_languages))}"
            )

    relations = data.get("relations")
    if not isinstance(relations, list):
        errors.append("relations: expected a list")
        return errors

    seen: set[tuple[str, str, str]] = set()
    edges_by_type: dict[str, dict[str, list[str]]] = {}
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
                edges_by_type.setdefault(kind, {}).setdefault(source, []).append(target)

    relation_types = data.get("relation_types")
    used_types = {kind for _, kind, _ in seen}
    if not isinstance(relation_types, dict):
        errors.append("relation_types: expected a mapping")
    else:
        unknown_definitions = set(relation_types) - RELATION_TYPES
        missing_definitions = used_types - set(relation_types)
        if unknown_definitions:
            errors.append(f"relation_types: unsupported definitions {sorted(unknown_definitions)}")
        if missing_definitions:
            errors.append(
                f"relation_types: missing definitions for used types {sorted(missing_definitions)}"
            )
        for kind, definition in relation_types.items():
            where = f"relation_types.{kind}"
            if not isinstance(definition, dict):
                errors.append(f"{where}: expected mapping")
                continue
            if definition.get("direction") not in {"directed", "symmetric"}:
                errors.append(f"{where}.direction: expected directed or symmetric")
            if definition.get("family") not in RELATION_FAMILIES:
                errors.append(f"{where}.family: expected one of {sorted(RELATION_FAMILIES)}")
            for field in ("transitive", "acyclic", "learning_dependency"):
                if type(definition.get(field)) is not bool:
                    errors.append(f"{where}.{field}: expected a boolean")
            if "inverse" not in definition:
                errors.append(f"{where}.inverse: required field is missing")
            inverse = definition.get("inverse")
            if inverse is not None and (
                not isinstance(inverse, str) or inverse not in relation_types
            ):
                errors.append(f"{where}.inverse: expected null or a defined relation type")
            if definition.get("learning_dependency") is True:
                if definition.get("direction") != "directed":
                    errors.append(f"{where}.learning_dependency: must be directed")
                if definition.get("acyclic") is not True:
                    errors.append(f"{where}.learning_dependency: must be acyclic")
                if definition.get("family") != "pedagogical":
                    errors.append(f"{where}.learning_dependency: family must be pedagogical")
            for field in ("labels", "descriptions"):
                values = definition.get(field)
                if not isinstance(values, dict) or set(values) != {"fr", "en"}:
                    errors.append(f"{where}.{field}: expected exactly fr and en")
                elif not all(isinstance(value, str) and value.strip() for value in values.values()):
                    errors.append(f"{where}.{field}: values must be non-empty strings")
            if isinstance(inverse, str) and inverse in relation_types:
                inverse_definition = relation_types[inverse]
                if (
                    isinstance(inverse_definition, dict)
                    and inverse_definition.get("inverse") != kind
                ):
                    errors.append(
                        f"{where}.inverse: inverse relation {inverse!r} must point back to {kind!r}"
                    )

        for index, relation in enumerate(relations):
            if not isinstance(relation, dict):
                continue
            kind = relation.get("type")
            source = relation.get("from")
            target = relation.get("to")
            definition = relation_types.get(kind) if isinstance(kind, str) else None
            if (
                isinstance(definition, dict)
                and definition.get("direction") == "symmetric"
                and isinstance(source, str)
                and isinstance(target, str)
                and source >= target
            ):
                errors.append(
                    f"relations[{index}]: {kind} must use canonical lexical order "
                    "(from < to) because it is symmetric"
                )

        for kind, definition in relation_types.items():
            if (
                isinstance(definition, dict)
                and definition.get("acyclic") is True
                and _has_cycle(edges_by_type.get(kind, {}))
            ):
                errors.append(f"relations: {kind} graph must be acyclic")
            if isinstance(definition, dict) and definition.get("learning_dependency") is True:
                for index, relation in enumerate(relations):
                    if isinstance(relation, dict) and relation.get("type") == kind:
                        rationale = relation.get("rationale")
                        if (
                            not isinstance(rationale, dict)
                            or set(rationale) != {"fr", "en"}
                            or not all(
                                isinstance(value, str) and value.strip()
                                for value in rationale.values()
                            )
                        ):
                            errors.append(
                                f"relations[{index}].rationale: expected non-empty fr and en"
                            )
    return errors


def main() -> int:
    """Validate the checked-in concept and domain registries."""
    try:
        data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
        domain_data = yaml.safe_load(DOMAINS.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        sys.stderr.write(f"Cannot read concept/domain registry: {exc}\n")
        return 1
    domain_ids, domain_errors = validate_domains(domain_data)
    errors = [*domain_errors, *validate_registry(data, _published_page_ids(), domain_ids)]
    if errors:
        sys.stderr.write("\n".join(errors) + "\n")
        return 1
    sys.stdout.write(
        f"Validated {len(domain_ids)} domains, {len(data['concepts'])} concepts, "
        f"and {len(data['relations'])} relations.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
