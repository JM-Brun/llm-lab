from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "site" / "tools" / "report_source_coverage.py"
SPEC = importlib.util.spec_from_file_location("report_source_coverage", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def test_collection_report_joins_extractions_by_source_id_and_counts_distinct_measures(
    tmp_path: Path,
) -> None:
    _write(
        tmp_path / "data" / "sources.yml",
        {
            "schema_version": 1,
            "sources": [
                {"id": "source-a", "collections": ["collection-one", "collection-two"]},
                {"id": "source-b", "collections": ["collection-two"]},
                {"id": "source-c"},
                {"id": "source-d", "collections": []},
            ],
        },
    )
    _write(
        tmp_path / "data" / "source-collections.yml",
        {
            "schema_version": 1,
            "collections": [
                {
                    "id": "collection-one",
                    "title": "Collection one",
                    "dossier_path": "docs/one.md",
                    "status": "active",
                },
                {
                    "id": "collection-two",
                    "title": "Collection two",
                    "dossier_path": "docs/two.md",
                    "status": "active",
                },
            ],
        },
    )
    _write(tmp_path / "data" / "concepts.yml", {"schema_version": 2, "concepts": []})
    _write(
        tmp_path / "data" / "extractions" / "source-a.yml",
        {
            "schema_version": 1,
            "source_id": "source-a",
            "items": [{"id": "a:1"}, {"id": "a:2"}],
        },
    )
    _write(
        tmp_path / "data" / "extractions" / "source-b.yml",
        {"schema_version": 1, "source_id": "source-b", "items": [{"id": "b:1"}]},
    )

    report = MODULE.build_report(tmp_path)

    assert report["collection_coverage"]["join_rule"] == (
        "extraction.source_id -> source.id -> source.collections"
    )
    assert report["collection_coverage"]["counts"] == {
        "sources_with_explicit_decision": 3,
        "sources_explicitly_unassigned": 1,
        "sources_without_explicit_decision": 1,
        "total_source_memberships": 3,
    }
    assert report["collection_coverage"]["collections"] == {
        "collection-one": {"source_records": 1, "extraction_files": 1, "atomic_items": 2},
        "collection-two": {"source_records": 2, "extraction_files": 2, "atomic_items": 3},
    }


def test_collection_report_markdown_labels_distinct_counts(tmp_path: Path) -> None:
    _write(
        tmp_path / "data" / "sources.yml",
        {"schema_version": 1, "sources": [{"id": "source-a", "collections": ["collection-one"]}]},
    )
    _write(
        tmp_path / "data" / "source-collections.yml",
        {
            "schema_version": 1,
            "collections": [
                {
                    "id": "collection-one",
                    "title": "Collection one",
                    "dossier_path": "docs/one.md",
                    "status": "active",
                }
            ],
        },
    )
    _write(tmp_path / "data" / "concepts.yml", {"schema_version": 2, "concepts": []})
    (tmp_path / "data" / "extractions").mkdir(parents=True, exist_ok=True)

    markdown = MODULE.render_markdown(MODULE.build_report(tmp_path))

    assert "## Explicit collection coverage" in markdown
    assert "| Collection | Source records | Extraction files | Atomic items |" in markdown
    assert "| collection-one | 1 | 0 | 0 |" in markdown
