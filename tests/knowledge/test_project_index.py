"""Tests for the deterministic project metadata query index."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from project_index import ProjectIndex


def _write_page(site: Path, page_id: str, language: str, *, next_page: str | None = None) -> None:
    _, slug = page_id.split("/", 1)
    path = site / language / f"{slug}.qmd"
    path.parent.mkdir(parents=True, exist_ok=True)
    tags = [
        "type:concept-lesson",
        "destination:understand",
        f"topic:{slug}",
        "level:core",
        f"language:{language}",
        "status:published",
    ]
    metadata = {
        "id": page_id,
        "suggested_route": {"previous": None, "next": next_page},
        "hierarchy": {"parents": [], "children": []},
        "related": [],
        "tags": tags,
    }
    front = {"title": slug, "lang": language, "keywords": tags}
    content = (
        "---\n" + yaml.safe_dump(front, sort_keys=False) + "---\n\n"
        "<!--\nLLM-LAB-PAGE-MAP v1\n" + yaml.safe_dump(metadata, sort_keys=False) + "-->\n"
    )
    path.write_text(content, encoding="utf-8")


def _write_sources(root: Path) -> None:
    data = root / "data"
    data.mkdir(parents=True, exist_ok=True)
    concepts = {
        "schema_version": 2,
        "concepts": [
            {
                "id": "attention",
                "importance": "core",
                "labels": {"fr": "Attention", "en": "Attention"},
                "definitions": {"fr": "Mécanisme.", "en": "Mechanism."},
                "domains": ["architectures-mechanisms"],
                "resources": ["fr/attention", "en/attention"],
            },
            {
                "id": "query",
                "importance": "supporting",
                "labels": {"fr": "Requête", "en": "Query"},
                "definitions": {"fr": "Projection.", "en": "Projection."},
                "domains": ["architectures-mechanisms"],
                "resources": ["fr/attention"],
            },
        ],
        "relations": [],
        "relation_types": {},
    }
    domains = {
        "schema_version": 1,
        "domains": [
            {
                "id": "architectures-mechanisms",
                "labels": {"fr": "Architectures", "en": "Architectures"},
            }
        ],
    }
    route = {
        "schema_version": 1,
        "stages": [
            {
                "id": "orientation",
                "title": {"fr": "Orientation", "en": "Orientation"},
                "objective": {"fr": "Observer.", "en": "Observe."},
                "pages": {"fr": ["fr/attention"], "en": ["en/attention"]},
                "optional_pages": {"fr": [], "en": ["en/query"]},
            }
        ],
        "transitions": [],
    }
    for name, value in (
        ("concepts.yml", concepts),
        ("domains.yml", domains),
        ("guided-route.yml", route),
    ):
        (data / name).write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def _index(tmp_path: Path) -> ProjectIndex:
    _write_page(tmp_path / "site", "fr/attention", "fr", next_page=None)
    _write_page(tmp_path / "site", "en/attention", "en", next_page="en/query")
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)
    return ProjectIndex.build(tmp_path)


def test_counts_distinguish_page_records_concepts_and_route_memberships(tmp_path: Path) -> None:
    stats = _index(tmp_path).stats()
    assert stats["published_page_records"] == 3
    assert stats["concepts"] == 2
    assert stats["route_memberships"] == 3
    assert stats["pages_by_tag"]["language"] == {"en": 2, "fr": 1}


def test_concept_page_associations_are_explicit_and_bidirectional(tmp_path: Path) -> None:
    index = _index(tmp_path)
    assert [page.page_id for page in index.pages_for_concept("attention")] == [
        "en/attention",
        "fr/attention",
    ]
    assert [concept["id"] for concept in index.concepts_for_page("fr/attention")] == [
        "attention",
        "query",
    ]


def test_page_relations_keep_family_and_direction(tmp_path: Path) -> None:
    index = _index(tmp_path)
    incoming = index.incoming_pages("en/query")
    assert [(edge.source, edge.family, edge.relation) for edge in incoming] == [
        ("en/attention", "suggested_route", "next")
    ]
    assert index.outgoing_pages("en/attention", family="suggested_route")[0].target == "en/query"


def test_route_core_and_optional_membership_are_distinct(tmp_path: Path) -> None:
    index = _index(tmp_path)
    assert [page.page_id for page in index.route_stage("orientation", "en", "core")] == [
        "en/attention"
    ]
    assert [page.page_id for page in index.route_stage("orientation", "en", "optional")] == [
        "en/query"
    ]


def test_unknown_ids_fail_clearly(tmp_path: Path) -> None:
    index = _index(tmp_path)
    with pytest.raises(KeyError, match="unknown concept"):
        index.pages_for_concept("missing")
    with pytest.raises(KeyError, match="unknown published page"):
        index.concepts_for_page("missing")
