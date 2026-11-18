"""Tests for the read-only extraction locator shape inventory."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "site" / "tools" / "report_extraction_locator_inventory.py"
SPEC = importlib.util.spec_from_file_location("locator_inventory", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def test_inventory_counts_locator_types_and_shapes_without_exposing_values(tmp_path: Path) -> None:
    _write(
        tmp_path / "data" / "extractions" / "sample.yml",
        {
            "schema_version": 1,
            "source_id": "sample-source",
            "items": [
                {"locator": {"type": "url", "value": "https://example.org/paper"}},
                {"locator": {"type": "timestamp", "value": "01:23:45"}},
                {"locator": {"type": "page", "value": "12-14"}},
                {"locator": {"type": "page", "value": "12\\u201314"}},
                {"locator": {"type": "section", "value": "Section 2.1"}},
                {"locator": {"type": "custom", "value": "opaque"}},
                {"locator": {"type": "url", "value": ""}},
                {"summary": "No locator"},
            ],
        },
    )

    report = MODULE.collect_inventory(tmp_path)

    assert report["files_seen"] == 1
    assert report["items_seen"] == 8
    assert report["items_without_locator_mapping"] == 1
    assert report["locators_with_missing_or_invalid_required_fields"] == 1
    assert report["locator_types"]["url"] == 2
    assert report["value_shapes_by_type"]["url::http-url"] == 1
    assert report["value_shapes_by_type"]["timestamp::timestamp-like"] == 1
    assert report["value_shapes_by_type"]["page::page-number-like"] == 2
    assert report["value_shapes_by_type"]["section::section-like"] == 1
    assert "https://example.org/paper" not in str(report)
