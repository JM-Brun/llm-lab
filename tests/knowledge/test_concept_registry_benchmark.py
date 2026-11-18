"""Tests for deterministic synthetic concept-registry benchmark fixtures."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
MODULE: dict[str, Any] = runpy.run_path(
    str(ROOT / "site" / "tools" / "benchmark_concept_registry.py"),
    run_name="concept_registry_benchmark_test",
)
build_synthetic_registry = MODULE["build_synthetic_registry"]
validate_registry = MODULE["validate_registry"]


def test_synthetic_registry_fixture_is_valid_and_has_expected_scale() -> None:
    base = yaml.safe_load((ROOT / "data" / "concepts.yml").read_text(encoding="utf-8"))
    domains = yaml.safe_load((ROOT / "data" / "domains.yml").read_text(encoding="utf-8"))
    domain_ids = {item["id"] for item in domains["domains"]}
    from page_index import load_published_pages

    published_pages = {page.page_id for page in load_published_pages(ROOT / "site")}
    target_size = len(base["concepts"]) + 12

    original = yaml.safe_dump(base, sort_keys=True)
    fixture = build_synthetic_registry(base, target_size)
    repeated = build_synthetic_registry(base, target_size)

    assert yaml.safe_dump(base, sort_keys=True) == original
    assert fixture == repeated
    assert len(fixture["concepts"]) == target_size
    assert len(fixture["relations"]) == len(base["relations"]) + 11
    assert validate_registry(fixture, published_pages, domain_ids) == []


def test_synthetic_registry_rejects_target_below_baseline() -> None:
    base = {"concepts": [{"id": "one"}], "relations": [], "relation_types": {}}

    try:
        build_synthetic_registry(base, 0)
    except ValueError as error:
        assert "smaller than baseline" in str(error)
    else:
        raise AssertionError("expected target below baseline to fail")
