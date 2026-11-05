"""Tests for the controlled source-extraction lifecycle vocabulary."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "site" / "tools"))

from check_source_catalogue import _validate_item_controlled_values  # noqa: E402


def _taxonomy() -> dict:
    return yaml.safe_load((ROOT / "data" / "source-taxonomy.yml").read_text(encoding="utf-8"))


def test_taxonomy_defines_distinct_evidence_and_editorial_vocabularies() -> None:
    taxonomy = _taxonomy()

    assert set(taxonomy["evidence_confidence_levels"]) == {
        "established",
        "well-supported",
        "context-dependent",
        "disputed",
        "speculative",
        "unverified",
    }
    assert set(taxonomy["assessment_levels"]) == {"low", "moderate", "high", "uncertain"}
    assert set(taxonomy["item_dispositions"]) >= {
        "integrate",
        "correct",
        "clarify",
        "link",
        "cite",
        "case-study",
        "experiment",
        "integrate-by-reference",
        "already-covered",
        "defer",
        "reject",
    }


def test_item_controlled_values_accept_taxonomy_values() -> None:
    taxonomy = _taxonomy()
    for disposition in taxonomy["item_dispositions"]:
        errors: list[str] = []
        _validate_item_controlled_values(
            {
                "evidence": {"confidence": "well-supported"},
                "disposition": disposition,
            },
            "item",
            set(taxonomy["evidence_confidence_levels"]),
            set(taxonomy["item_dispositions"]),
            errors,
        )
        assert errors == []


def test_item_controlled_values_reject_unknown_values() -> None:
    taxonomy = _taxonomy()
    errors: list[str] = []

    _validate_item_controlled_values(
        {
            "evidence": {"confidence": "high"},
            "disposition": "already-integrated",
        },
        "item",
        set(taxonomy["evidence_confidence_levels"]),
        set(taxonomy["item_dispositions"]),
        errors,
    )

    assert any("evidence.confidence: unsupported value 'high'" in error for error in errors)
    assert any("disposition: unsupported value 'already-integrated'" in error for error in errors)
