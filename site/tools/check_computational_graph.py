#!/usr/bin/env python3
"""Validate the canonical computational graph registry."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data" / "computational-graph.yml"
IDENTIFIER = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
PAGE_ID = re.compile(r"(?:fr|en)/[a-z0-9]+(?:-[a-z0-9]+)*")
NODE_KINDS = {"data", "operation", "control", "policy"}
EDGE_TYPES = {
    "consumes",
    "produces",
    "combines",
    "constrains",
    "applies",
    "selects",
    "scores",
    "aggregates",
    "differentiates",
    "updates",
    "feeds-back",
    "conditions",
    "uses-optional",
}


def published_page_ids() -> set[str]:
    """Return stable IDs of published bilingual Quarto pages."""
    published: set[str] = set()
    for language in ("fr", "en"):
        for path in (ROOT / "site" / language).glob("*.qmd"):
            source = path.read_text(encoding="utf-8")
            match = re.search(
                r"<!--\\s*\\nLLM-LAB-PAGE-MAP v1\\n(.*?)\\n-->",
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


def _bilingual_strings(value: Any, where: str, errors: list[str]) -> None:
    """Require non-empty French and English strings."""
    if not isinstance(value, dict) or set(value) != {"fr", "en"}:
        errors.append(f"{where}: expected exactly fr and en")
        return
    if not all(isinstance(item, str) and item.strip() for item in value.values()):
        errors.append(f"{where}: values must be non-empty strings")


def _unique_records(
    records: Any, collection: str, errors: list[str]
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    """Index records by stable ID while reporting malformed and duplicate IDs."""
    indexed: dict[str, dict[str, Any]] = {}
    if not isinstance(records, list) or not records:
        errors.append(f"{collection}: expected a non-empty list")
        return indexed, set()
    for index, record in enumerate(records):
        where = f"{collection}[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{where}: expected mapping")
            continue
        identifier = record.get("id")
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
            errors.append(f"{where}.id: expected stable kebab-case identifier")
            continue
        if identifier in indexed:
            errors.append(f"{where}.id: duplicate identifier {identifier!r}")
            continue
        indexed[identifier] = record
        _bilingual_strings(record.get("labels"), f"{where}.labels", errors)
        _bilingual_strings(record.get("descriptions"), f"{where}.descriptions", errors)
    return indexed, set(indexed)


def _has_cycle(edges: dict[str, list[str]]) -> bool:
    """Detect directed cycles iteratively."""
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


def validate_graph(
    data: Any, published_pages: set[str] | None = None
) -> list[str]:
    """Return schema, bilingual, reference, and graph-structure errors."""
    errors: list[str] = []
    if (
        not isinstance(data, dict)
        or type(data.get("schema_version")) is not int
        or data.get("schema_version") != 1
    ):
        return ["registry: expected mapping with schema_version: 1"]

    branches, branch_ids = _unique_records(data.get("branches"), "branches", errors)
    nodes, node_ids = _unique_records(data.get("nodes"), "nodes", errors)
    relation_types, relation_type_ids = _unique_records(
        [
            {"id": key, **value}
            for key, value in data.get("relation_types", {}).items()
            if isinstance(key, str) and isinstance(value, dict)
        ]
        if isinstance(data.get("relation_types"), dict)
        else data.get("relation_types"),
        "relation_types",
        errors,
    )
    if not isinstance(data.get("relation_types"), dict):
        errors.append("relation_types: expected mapping")

    for identifier, node in nodes.items():
        where = f"nodes.{identifier}"
        if node.get("kind") not in NODE_KINDS:
            errors.append(f"{where}.kind: expected one of {sorted(NODE_KINDS)}")
        memberships = node.get("branches")
        if not isinstance(memberships, list) or not memberships:
            errors.append(f"{where}.branches: expected a non-empty list")
        elif not all(isinstance(branch_id, str) for branch_id in memberships):
            errors.append(f"{where}.branches: values must be strings")
        else:
            if len(memberships) != len(set(memberships)):
                errors.append(f"{where}.branches: duplicate branch IDs")
            for branch_id in memberships:
                if branch_id not in branch_ids:
                    errors.append(f"{where}.branches: unknown branch {branch_id!r}")

        resources = node.get("resources")
        if not isinstance(resources, list) or not resources:
            errors.append(f"{where}.resources: expected a non-empty list of page IDs")
            continue
        languages: set[str] = set()
        if all(isinstance(page_id, str) for page_id in resources):
            if len(resources) != len(set(resources)):
                errors.append(f"{where}.resources: duplicate page IDs")
        for page_id in resources:
            if not isinstance(page_id, str) or not PAGE_ID.fullmatch(page_id):
                errors.append(f"{where}.resources: invalid page ID {page_id!r}")
                continue
            languages.add(page_id.split("/", maxsplit=1)[0])
            if published_pages is not None and page_id not in published_pages:
                errors.append(f"{where}.resources: page {page_id!r} is not published")
        missing_languages = {"fr", "en"} - languages
        if missing_languages:
            errors.append(
                f"{where}.resources: missing language(s) {', '.join(sorted(missing_languages))}"
            )

    edges = data.get("edges")
    if not isinstance(edges, list) or not edges:
        errors.append("edges: expected a non-empty list")
        edges = []
    edge_ids: set[str] = set()
    acyclic_edges: dict[str, list[str]] = {}
    for index, edge in enumerate(edges):
        where = f"edges[{index}]"
        if not isinstance(edge, dict):
            errors.append(f"{where}: expected mapping")
            continue
        edge_id = edge.get("id")
        if not isinstance(edge_id, str) or not IDENTIFIER.fullmatch(edge_id):
            errors.append(f"{where}.id: expected stable kebab-case identifier")
        elif edge_id in edge_ids:
            errors.append(f"{where}.id: duplicate identifier {edge_id!r}")
        else:
            edge_ids.add(edge_id)

        source, kind, target = (edge.get(key) for key in ("from", "type", "to"))
        if not isinstance(source, str) or source not in node_ids:
            errors.append(f"{where}.from: unknown node {source!r}")
        if not isinstance(target, str) or target not in node_ids:
            errors.append(f"{where}.to: unknown node {target!r}")
        if not isinstance(kind, str) or kind not in relation_type_ids or kind not in EDGE_TYPES:
            errors.append(f"{where}.type: unsupported relation {kind!r}")

        feedback = edge.get("feedback", False)
        repeated = edge.get("repeated", False)
        optional = edge.get("optional", False)
        for field, value in (
            ("feedback", feedback),
            ("repeated", repeated),
            ("optional", optional),
        ):
            if type(value) is not bool:
                errors.append(f"{where}.{field}: expected boolean when present")
        if kind == "feeds-back" and feedback is not True:
            errors.append(f"{where}: feeds-back edges must declare feedback: true")
        if feedback is True and kind != "feeds-back":
            errors.append(f"{where}: feedback: true is reserved for feeds-back edges")
        if repeated is True and kind != "produces":
            errors.append(f"{where}: repeated: true is reserved for produces edges")
        if optional is True and (
            not isinstance(kind, str) or kind not in {"produces", "uses-optional"}
        ):
            errors.append(f"{where}: optional: true requires produces or uses-optional")

        if isinstance(source, str) and source in nodes and isinstance(target, str) and target in nodes:
            shared_branches = set(nodes[source].get("branches", [])) & set(
                nodes[target].get("branches", [])
            )
            if not shared_branches:
                errors.append(
                    f"{where}: endpoints have no shared branch membership"
                )
            if feedback is not True and repeated is not True:
                acyclic_edges.setdefault(source, []).append(target)

    if _has_cycle(acyclic_edges):
        errors.append(
            "edges: a directed cycle exists outside explicitly marked feedback/repeated edges"
        )

    views, view_ids = _unique_records(data.get("views"), "views", errors)
    for identifier, view in views.items():
        where = f"views.{identifier}"
        branch_id = view.get("branch")
        if not isinstance(branch_id, str) or branch_id not in branch_ids:
            errors.append(f"{where}.branch: unknown branch {branch_id!r}")
        view_nodes = view.get("nodes")
        view_edges = view.get("edges")
        if not isinstance(view_nodes, list) or not view_nodes:
            errors.append(f"{where}.nodes: expected a non-empty list")
            view_nodes = []
        if not isinstance(view_edges, list):
            errors.append(f"{where}.edges: expected a list")
            view_edges = []
        if all(isinstance(node_id, str) for node_id in view_nodes):
            if len(view_nodes) != len(set(view_nodes)):
                errors.append(f"{where}.nodes: duplicate node IDs")
        else:
            errors.append(f"{where}.nodes: values must be strings")
        if all(isinstance(edge_id, str) for edge_id in view_edges):
            if len(view_edges) != len(set(view_edges)):
                errors.append(f"{where}.edges: duplicate edge IDs")
        else:
            errors.append(f"{where}.edges: values must be strings")
        for node_id in view_nodes:
            if not isinstance(node_id, str) or node_id not in node_ids:
                errors.append(f"{where}.nodes: unknown node {node_id!r}")
            elif branch_id not in nodes[node_id].get("branches", []):
                errors.append(
                    f"{where}.nodes: node {node_id!r} is not a member of branch {branch_id!r}"
                )
        edge_index = {
            edge.get("id"): edge
            for edge in edges
            if isinstance(edge, dict) and isinstance(edge.get("id"), str)
        }
        for edge_id in view_edges:
            edge = edge_index.get(edge_id) if isinstance(edge_id, str) else None
            if edge is None:
                errors.append(f"{where}.edges: unknown edge {edge_id!r}")
                continue
            if edge.get("from") not in view_nodes or edge.get("to") not in view_nodes:
                errors.append(
                    f"{where}.edges: edge {edge_id!r} has an endpoint outside the view"
                )

    return errors


def main() -> int:
    """Validate the checked-in computational graph."""
    try:
        data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        sys.stderr.write(f"Cannot read computational graph registry: {exc}\n")
        return 1

    errors = validate_graph(data, published_page_ids())
    if errors:
        sys.stderr.write("\n".join(errors) + "\n")
        return 1

    sys.stdout.write(
        f"Validated {len(data['branches'])} branches, {len(data['nodes'])} nodes, "
        f"{len(data['edges'])} edges, and {len(data['views'])} views.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
