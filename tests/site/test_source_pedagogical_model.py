"""Tests for reconstructed source-local pedagogical models."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "site" / "tools"))

from check_source_catalogue import _validate_pedagogical_model  # noqa: E402


def test_qkv_source_pedagogical_model_is_structurally_valid() -> None:
    extraction_path = (
        ROOT / "data" / "extractions" / "nishanthan-k-qkv-transformers-devto.yml"
    )
    extraction = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    _validate_pedagogical_model(
        extraction["pedagogical_model"],
        "pedagogical_model",
        errors,
    )

    assert errors == []


def test_source_graph_rejects_edges_to_unknown_local_nodes() -> None:
    model = {
        "reconstruction": {
            "status": "partial",
            "basis": ["Indexed article body"],
            "inferred_elements": ["Learning outcomes"],
        },
        "source_graph": {
            "nodes": [
                {
                    "id": "query",
                    "kind": "representation",
                    "description": "A query vector.",
                    "locator": "Section 1",
                }
            ],
            "edges": [{"from": "query", "type": "compared-with", "to": "missing"}],
            "interpretation": "A source-local reconstruction.",
        },
        "learning_outcomes": [
            {"status": "inferred", "outcome": "Explain queries.", "basis": "Section 1"}
        ],
        "assumed_prerequisites": [
            {"status": "inferred", "topic": "Vectors.", "basis": "Notation in section 1"}
        ],
        "teaching_route": [
            {"order": 1, "section": "Introduction", "function": "motivate", "moves": ["Analogy"]}
        ],
        "pedagogical_strengths": ["Concise."],
        "pedagogical_limits": ["No exercises."],
        "comparison": {
            "dossier": "docs/source-reviews/example.md",
            "canonical_graph": "data/concepts.yml",
            "canonical_routes": ["data/guided-route.yml"],
            "decision": "No route change.",
            "structures_kept_separate": ["source-graph", "learning-route"],
        },
    }
    errors: list[str] = []

    _validate_pedagogical_model(model, "pedagogical_model", errors)

    assert any("source_graph.edges[0].to" in error for error in errors)


def test_source_learning_route_requires_contiguous_order() -> None:
    extraction_path = (
        ROOT / "data" / "extractions" / "nishanthan-k-qkv-transformers-devto.yml"
    )
    extraction = yaml.safe_load(extraction_path.read_text(encoding="utf-8"))
    model = extraction["pedagogical_model"]
    model["teaching_route"][1]["order"] = 4
    errors: list[str] = []

    _validate_pedagogical_model(model, "pedagogical_model", errors)

    assert any("order values must be unique and contiguous" in error for error in errors)
