"""Tests for the canonical computational graph registry."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import yaml

MODULE_PATH = (
    Path(__file__).resolve().parents[2] / "site" / "tools" / "check_computational_graph.py"
)
MODULE: dict[str, Any] = runpy.run_path(str(MODULE_PATH), run_name="computational_graph_test")
validate_graph = MODULE["validate_graph"]


def _bilingual(label: str) -> dict[str, str]:
    return {"fr": label, "en": label}


def _valid_graph() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "branches": [
            {
                "id": "shared",
                "labels": _bilingual("Shared"),
                "descriptions": _bilingual("Shared computation."),
            }
        ],
        "nodes": [
            {
                "id": "context",
                "kind": "data",
                "role": "state",
                "labels": _bilingual("Context"),
                "descriptions": _bilingual("Input context."),
                "branches": ["shared"],
                "resources": ["fr/text-data", "en/text-data"],
            },
            {
                "id": "forward",
                "kind": "operation",
                "role": "model",
                "labels": _bilingual("Forward"),
                "descriptions": _bilingual("Model computation."),
                "branches": ["shared"],
                "resources": ["fr/generation", "en/generation"],
            },
        ],
        "relation_types": {
            "consumes": {
                "id": "consumes",
                "labels": _bilingual("Consumes"),
                "descriptions": _bilingual("Consumes input."),
            }
        },
        "edges": [
            {
                "id": "context-forward",
                "from": "context",
                "type": "consumes",
                "to": "forward",
            }
        ],
        "views": [
            {
                "id": "spine",
                "branch": "shared",
                "labels": _bilingual("Spine"),
                "descriptions": _bilingual("Shared view."),
                "nodes": ["context", "forward"],
                "edges": ["context-forward"],
            }
        ],
    }


def test_checked_in_computational_graph_is_valid() -> None:
    registry_path = Path(__file__).resolve().parents[2] / "data" / "computational-graph.yml"
    data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))

    errors = validate_graph(data, MODULE["published_page_ids"]())

    assert errors == []


def test_graph_rejects_duplicate_ids_and_unknown_edge_endpoints() -> None:
    data = _valid_graph()
    data["nodes"].append(data["nodes"][0].copy())
    data["edges"].append(
        {
            "id": "unknown-endpoint",
            "from": "missing",
            "type": "consumes",
            "to": "forward",
        }
    )

    errors = validate_graph(data)

    assert any("duplicate identifier" in error for error in errors)
    assert any(".from: unknown node" in error for error in errors)


def test_graph_requires_bilingual_metadata_and_published_resources() -> None:
    data = _valid_graph()
    data["nodes"][0]["descriptions"].pop("en")
    data["nodes"][1]["resources"] = ["fr/not-published", "en/generation"]

    errors = validate_graph(data, {"fr/text-data", "en/text-data", "en/generation"})

    assert any("descriptions: expected exactly fr and en" in error for error in errors)
    assert any("page 'fr/not-published' is not published" in error for error in errors)


def test_graph_rejects_unknown_branch_and_branchless_edge() -> None:
    data = _valid_graph()
    data["nodes"][0]["branches"] = ["missing"]

    errors = validate_graph(data)

    assert any("unknown branch" in error for error in errors)
    assert any("no shared branch membership" in error for error in errors)


def test_unmarked_cycles_are_rejected_and_feedback_cycles_are_allowed() -> None:
    data = _valid_graph()
    data["edges"].append(
        {
            "id": "forward-context",
            "from": "forward",
            "type": "consumes",
            "to": "context",
        }
    )

    errors = validate_graph(data)
    assert any("cycle exists outside" in error for error in errors)

    data["edges"][1]["type"] = "feeds-back"
    data["edges"][1]["feedback"] = True
    data["relation_types"]["feeds-back"] = {
        "id": "feeds-back",
        "labels": _bilingual("Feeds back"),
        "descriptions": _bilingual("Feedback loop."),
    }
    assert validate_graph(data) == []


def test_feedback_and_repeated_flags_are_restricted_to_their_edge_types() -> None:
    data = _valid_graph()
    data["edges"][0]["feedback"] = True

    errors = validate_graph(data)

    assert any("reserved for feeds-back" in error for error in errors)


def test_views_must_resolve_nodes_edges_and_branch_membership() -> None:
    data = _valid_graph()
    data["views"][0]["nodes"] = ["context"]
    data["views"][0]["edges"] = ["context-forward"]

    errors = validate_graph(data)

    assert any("endpoint outside the view" in error for error in errors)
