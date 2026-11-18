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


def test_inventory_separates_missing_scalar_and_mapping_locators(tmp_path: Path) -> None:
    _write(
        tmp_path / "data" / "extractions" / "sample.yml",
        {
            "schema_version": 1,
            "source_id": "sample-source",
            "items": [
                {"locator": {"type": "url", "value": "https://example.org/paper"}},
                {"locator": {"type": "timestamp", "value": "01:23:45"}},
                {"locator": {"type": "page", "value": "12-14"}},
                {"locator": {"type": "page", "value": "12\u201314"}},
                {"locator": {"type": "section", "value": "Section 2.1"}},
                {"locator": {"type": "custom", "value": "opaque"}},
                {"locator": {"type": "url", "value": ""}},
                {"locator": "Section 3.2: method and results"},
                {"locator": "01:23:45"},
                {"summary": "No locator"},
                {"locator": None},
                {"locator": ["unexpected", "shape"]},
                {"locator": 42},
                "not-an-extraction-record",
            ],
        },
    )

    report = MODULE.collect_inventory(tmp_path)

    assert report["files_seen"] == 1
    assert report["items_seen"] == 14
    assert report["items_without_locator"] == 2
    assert report["items_with_scalar_locator"] == 2
    assert report["items_with_unsupported_locator_shape"] == 2
    assert report["unsupported_locator_shapes"] == {
        "int::non-string:int": 1,
        "list::non-string:list": 1,
    }
    assert report["items_with_non_mapping_extraction_record"] == 1
    assert report["items_without_locator_mapping"] == 6
    assert report["locators_with_missing_or_invalid_required_fields"] == 1
    assert report["locator_types"]["url"] == 2
    assert report["mapping_value_shapes_by_type"]["url::http-url"] == 1
    assert report["mapping_value_shapes_by_type"]["timestamp::timestamp-like"] == 1
    assert report["mapping_value_shapes_by_type"]["page::page-number-like"] == 2
    assert report["mapping_value_shapes_by_type"]["section::section-like"] == 1
    assert report["scalar_locator_value_shapes"]["section-like"] == 1
    assert report["scalar_locator_value_shapes"]["timestamp-like"] == 1
    assert "https://example.org/paper" not in str(report)
    assert "Section 3.2: method and results" not in str(report)


def test_value_shape_recognizes_timestamp_ranges() -> None:
    assert MODULE._value_shape("01:23:45") == "timestamp-like"
    assert MODULE._value_shape("05:41\u201310:22") == "timestamp-like"
    assert MODULE._value_shape("00:01:00-03:21:46") == "timestamp-like"
    assert MODULE._value_shape("00:01:00 \u2014 03:21:46") == "timestamp-like"
    assert MODULE._value_shape("00:00\u201303:02 and 12:59\u201314:55") == "timestamp-like"
    assert MODULE._value_shape("1:28:42\u20131:49:58 onward") == "timestamp-like"
    assert MODULE._value_shape("Chapter 2: 05:41\u201310:22") == "opaque-text"
