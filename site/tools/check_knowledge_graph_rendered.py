#!/usr/bin/env python3
"""Validate that the generated JSON-LD graph is present in the rendered site."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

IMPORTANCE_LEVELS = {"essential", "important", "specialized"}
EXPORT_NAME = "knowledge-graph.jsonld"
EXPECTED_EXPORT_ID = "https://jm-brun.github.io/llm-lab/knowledge-graph.jsonld"
REQUIRED_TYPES = {
    "skos:ConceptScheme",
    "skos:Concept",
    "schema:LearningResource",
    "schema:SoftwareSourceCode",
    "prov:Entity",
}


def validate_graph(payload: dict[str, Any]) -> list[str]:
    """Check the rendered graph's minimum structure and internal references."""
    errors: list[str] = []
    graph = payload.get("@graph")
    if not isinstance(graph, list):
        return ["JSON-LD document has no @graph array"]

    context = payload.get("@context")
    if not isinstance(context, dict):
        errors.append("JSON-LD document has no explicit @context")
    else:
        for prefix in ("skos", "schema", "prov", "dcterms", "llmlab"):
            if prefix not in context:
                errors.append(f"JSON-LD context is missing the {prefix!r} prefix")

    nodes = [node for node in graph if isinstance(node, dict)]
    identifiers = {node["@id"] for node in nodes if isinstance(node.get("@id"), str)}
    types = {
        node_type
        for node in nodes
        for node_type in (
            node.get("@type") if isinstance(node.get("@type"), list) else [node.get("@type")]
        )
        if isinstance(node_type, str)
    }

    for required_type in sorted(REQUIRED_TYPES - types):
        errors.append(f"JSON-LD graph is missing required type {required_type!r}")

    if EXPECTED_EXPORT_ID not in identifiers:
        errors.append(f"JSON-LD graph is missing its export entity {EXPECTED_EXPORT_ID!r}")

    for node in nodes:
        node_id = node.get("@id")
        if isinstance(node_id, str) and "/id/concept/" in node_id:
            importance = node.get("llmlab:importance")
            if importance not in IMPORTANCE_LEVELS:
                errors.append(
                    f"Concept {node_id!r} has missing or invalid llmlab:importance {importance!r}"
                )

    for node in nodes:
        for predicate, value in node.items():
            if predicate.startswith("@"):
                continue
            values = value if isinstance(value, list) else [value]
            for item in values:
                if (
                    isinstance(item, dict)
                    and isinstance(item.get("@id"), str)
                    and item["@id"] not in identifiers
                ):
                    errors.append(
                        f"Unresolved graph reference {item['@id']!r} "
                        f"from {node.get('@id', '<anonymous>')!r} via {predicate!r}"
                    )

    return errors


def check_rendered_export(site_root: Path) -> list[str]:
    """Check the generated JSON-LD file in the rendered Quarto output."""
    export_path = site_root / EXPORT_NAME
    if not export_path.is_file():
        return [f"Rendered JSON-LD export is missing: {export_path}"]

    try:
        payload = json.loads(export_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"Cannot read rendered JSON-LD export {export_path}: {error}"]

    if not isinstance(payload, dict):
        return ["Rendered JSON-LD export must contain a JSON object"]
    return validate_graph(payload)


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: check_knowledge_graph_rendered.py <rendered-site-directory>\n")
        return 2

    site_root = Path(sys.argv[1])
    errors = check_rendered_export(site_root)
    if errors:
        sys.stdout.write("Rendered knowledge-graph check failed:\n")
        for error in errors:
            sys.stdout.write(f"- {error}\n")
        return 1

    sys.stdout.write(f"Rendered JSON-LD graph check passed for {site_root}.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
