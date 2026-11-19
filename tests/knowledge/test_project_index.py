"""Tests for the deterministic project metadata query index."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
MODULE = runpy.run_path(
    str(ROOT / "site" / "tools" / "project_index.py"),
    run_name="project_index_test",
)
ProjectIndex = MODULE["ProjectIndex"]


def _write_page(
    site: Path,
    page_id: str,
    language: str,
    *,
    next_page: str | None = None,
    revision: dict[str, Any] | None = None,
    body: str = "",
) -> None:
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
    if revision is not None:
        metadata["revision"] = revision
    front = {"title": slug, "lang": language, "keywords": tags}
    content = (
        "---\n" + yaml.safe_dump(front, sort_keys=False) + "---\n\n"
        "<!--\nLLM-LAB-PAGE-MAP v1\n" + yaml.safe_dump(metadata, sort_keys=False) + "-->\n" + body
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
        (
            "resources.yml",
            {
                "schema_version": 1,
                "resources": [
                    {
                        "id": "attention-module",
                        "kind": "implementation",
                        "labels": {"fr": "Module attention", "en": "Attention module"},
                        "descriptions": {"fr": "Code.", "en": "Code."},
                        "language": "en",
                        "programming_language": "Python",
                        "status": "published",
                        "location": {"type": "local", "path": "src/attention.py"},
                        "referenced_by": ["fr/attention", "en/attention"],
                        "concepts": ["attention"],
                    }
                ],
            },
        ),
    ):
        (data / name).write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")

    source_dir = root / "src"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "attention.py").write_text("# test fixture\n", encoding="utf-8")


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


def test_concept_page_reference_must_exist(tmp_path: Path) -> None:
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en")
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)
    concepts_path = tmp_path / "data" / "concepts.yml"
    concepts = yaml.safe_load(concepts_path.read_text(encoding="utf-8"))
    concepts["concepts"][0]["resources"].append("fr/missing")
    concepts_path.write_text(yaml.safe_dump(concepts, sort_keys=False), encoding="utf-8")

    with pytest.raises(ValueError, match=r"data/concepts.yml.*attention.*fr/missing"):
        ProjectIndex.build(tmp_path)


def test_page_edge_target_must_exist(tmp_path: Path) -> None:
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en", next_page="en/missing")
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)

    with pytest.raises(ValueError, match=r"en/attention.qmd.*suggested_route.next.*en/missing"):
        ProjectIndex.build(tmp_path)


def test_non_page_resource_adapter_preserves_explicit_associations(tmp_path: Path) -> None:
    index = _index(tmp_path)

    resource = index.resources_by_id["attention-module"]
    assert resource.kind == "implementation"
    assert resource.language == "en"
    assert resource.referenced_by == ("fr/attention", "en/attention")
    assert resource.concepts == ("attention",)
    assert index.page_resource_associations == (
        MODULE["PageResourceAssociation"]("en/attention", "attention-module"),
        MODULE["PageResourceAssociation"]("fr/attention", "attention-module"),
    )
    assert index.concept_resource_associations == (
        MODULE["ConceptResourceAssociation"]("attention", "attention-module"),
    )


def test_non_page_resource_references_must_resolve(tmp_path: Path) -> None:
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en")
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)
    path = tmp_path / "data" / "resources.yml"
    resources = yaml.safe_load(path.read_text(encoding="utf-8"))
    resources["resources"][0]["referenced_by"].append("en/missing")
    path.write_text(yaml.safe_dump(resources, sort_keys=False), encoding="utf-8")

    with pytest.raises(ValueError, match=r"attention-module.*referenced_by.*en/missing"):
        ProjectIndex.build(tmp_path)


def test_non_page_resource_concept_reference_must_resolve(tmp_path: Path) -> None:
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en")
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)
    path = tmp_path / "data" / "resources.yml"
    resources = yaml.safe_load(path.read_text(encoding="utf-8"))
    resources["resources"][0]["concepts"].append("missing")
    path.write_text(yaml.safe_dump(resources, sort_keys=False), encoding="utf-8")

    with pytest.raises(ValueError, match=r"attention-module.*concepts.*missing"):
        ProjectIndex.build(tmp_path)


def test_revision_adapter_keeps_three_target_types_separate(tmp_path: Path) -> None:
    revision = {
        "status": "assessed",
        "resources": [
            {"role": "synthesis", "target": {"type": "section", "id": "revision-summary"}},
            {"role": "flashcards", "target": {"type": "page", "id": "en/query"}},
            {"role": "revision_sheet", "target": {"type": "resource", "id": "attention-module"}},
        ],
    }
    _write_page(
        tmp_path / "site",
        "fr/attention",
        "fr",
        body="\n## Revision summary {#revision-summary}\n",
    )
    _write_page(
        tmp_path / "site",
        "en/attention",
        "en",
        next_page="en/query",
        revision=revision,
        body="\n## Revision summary {#revision-summary}\n",
    )
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)

    index = ProjectIndex.build(tmp_path)

    assert index.revision_status_by_page["en/attention"] == "assessed"
    assert index.revision_status_by_page["fr/attention"] == "not_assessed"
    assert [
        (edge.source_page_id, edge.role, edge.target_type, edge.target_id)
        for edge in index.revision_edges
    ] == [
        ("en/attention", "flashcards", "page", "en/query"),
        ("en/attention", "revision_sheet", "resource", "attention-module"),
        ("en/attention", "synthesis", "section", "revision-summary"),
    ]
    assert all(edge.family != "revision" for edge in index.page_edges)
    assert [resource.resource_id for resource in index.resources_for_page("en/attention")] == [
        "attention-module"
    ]
    assert [page.page_id for page in index.pages_for_resource("attention-module")] == [
        "en/attention",
        "fr/attention",
    ]
    assert [resource.resource_id for resource in index.resources_for_concept("attention")] == [
        "attention-module"
    ]
    assert [concept["id"] for concept in index.concepts_for_resource("attention-module")] == [
        "attention"
    ]

    assert index.revision_targets_for_page("en/attention") == index.revision_edges
    synthesis_edges = index.revision_targets_for_page("en/attention", role="synthesis")
    assert synthesis_edges[0].target_type == "section"
    assert [page.page_id for page in index.pages_for_revision_target("page", "en/query")] == [
        "en/attention"
    ]
    assert [
        page.page_id for page in index.pages_for_revision_target("resource", "attention-module")
    ] == ["en/attention"]
    assert [
        page.page_id
        for page in index.pages_for_revision_target(
            "section", "revision-summary", section_page_id="en/attention"
        )
    ] == ["en/attention"]
    assert (
        index.pages_for_revision_target(
            "section", "revision-summary", section_page_id="fr/attention"
        )
        == ()
    )


def test_revision_section_requires_an_explicit_anchor(tmp_path: Path) -> None:
    revision = {
        "status": "assessed",
        "resources": [{"role": "synthesis", "target": {"type": "section", "id": "missing-anchor"}}],
    }
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en", revision=revision)
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)

    with pytest.raises(ValueError, match=r"revision section anchor.*missing-anchor"):
        ProjectIndex.build(tmp_path)


def test_revision_section_accepts_explicit_quarto_block_anchor(tmp_path: Path) -> None:
    revision = {
        "status": "assessed",
        "resources": [
            {"role": "revision_sheet", "target": {"type": "section", "id": "revision-block"}}
        ],
    }
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(
        tmp_path / "site",
        "en/attention",
        "en",
        revision=revision,
        body="\n::: {.callout-tip #revision-block}\nA concise recap.\n:::\n",
    )
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)

    index = ProjectIndex.build(tmp_path)

    assert index.revision_edges[0].target_type == "section"
    assert index.revision_edges[0].target_id == "revision-block"


def test_duplicate_revision_relationships_are_rejected(tmp_path: Path) -> None:
    relationship = {"role": "synthesis", "target": {"type": "page", "id": "en/query"}}
    revision = {"status": "assessed", "resources": [relationship, relationship]}
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en", revision=revision)
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)

    with pytest.raises(ValueError, match="duplicate revision relationship"):
        ProjectIndex.build(tmp_path)


def test_revision_page_target_must_be_published_and_language_compatible(tmp_path: Path) -> None:
    revision = {
        "status": "assessed",
        "resources": [{"role": "revision_sheet", "target": {"type": "page", "id": "fr/attention"}}],
    }
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en", revision=revision)
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)

    with pytest.raises(ValueError, match=r"revision page target language.*fr/attention"):
        ProjectIndex.build(tmp_path)


def test_revision_resource_target_must_be_published_and_language_compatible(tmp_path: Path) -> None:
    revision = {
        "status": "assessed",
        "resources": [
            {"role": "flashcards", "target": {"type": "resource", "id": "attention-module"}}
        ],
    }
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en", revision=revision)
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)
    path = tmp_path / "data" / "resources.yml"
    resources = yaml.safe_load(path.read_text(encoding="utf-8"))
    resources["resources"][0]["language"] = "fr"
    path.write_text(yaml.safe_dump(resources, sort_keys=False), encoding="utf-8")

    with pytest.raises(ValueError, match=r"revision resource target language.*attention-module"):
        ProjectIndex.build(tmp_path)


def test_revision_status_constraints_are_enforced(tmp_path: Path) -> None:
    revision = {"status": "not_applicable", "resources": []}
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en", revision=revision)
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)

    with pytest.raises(ValueError, match=r"not_applicable requires a non-empty reason"):
        ProjectIndex.build(tmp_path)


def test_inverse_queries_reject_unknown_entities_and_invalid_targets(tmp_path: Path) -> None:
    index = _index(tmp_path)

    with pytest.raises(KeyError, match="unknown published page"):
        index.resources_for_page("en/missing")
    with pytest.raises(KeyError, match="unknown resource"):
        index.pages_for_resource("missing-resource")
    with pytest.raises(KeyError, match="unknown concept"):
        index.resources_for_concept("missing-concept")
    with pytest.raises(KeyError, match="unknown resource"):
        index.concepts_for_resource("missing-resource")
    with pytest.raises(KeyError, match="unknown revision target page"):
        index.revision_edges_for_target("page", "en/missing")
    with pytest.raises(ValueError, match="section targets require"):
        index.revision_edges_for_target("section", "missing-anchor")
    with pytest.raises(ValueError, match="unknown revision target type"):
        index.revision_edges_for_target("concept", "attention")


def test_real_repository_resource_and_revision_inverse_queries() -> None:
    index = ProjectIndex.build(ROOT)

    expected_pages = {
        "gpt-config-module": ("en/gpt-config-walkthrough", "fr/gpt-config-walkthrough"),
        "gpt-generation-module": (
            "en/gpt-generation-walkthrough",
            "fr/gpt-generation-walkthrough",
        ),
        "gpt-model-module": ("en/gpt-model-walkthrough", "fr/gpt-model-walkthrough"),
        "gpt-ops-module": ("en/gpt-ops-walkthrough", "fr/gpt-ops-walkthrough"),
        "transformer-block-module": (
            "en/transformer-block-walkthrough",
            "fr/transformer-block-walkthrough",
        ),
    }
    assert set(expected_pages) == set(index.resources_by_id)
    assert sum(len(page_ids) for page_ids in expected_pages.values()) == 10
    for resource_id, expected_page_ids in expected_pages.items():
        assert tuple(
            page.page_id for page in index.pages_for_resource(resource_id)
        ) == expected_page_ids
        for page_id in expected_page_ids:
            assert [resource.resource_id for resource in index.resources_for_page(page_id)] == [
                resource_id
            ]
    assert [resource.resource_id for resource in index.resources_for_concept("self-attention")] == [
        "transformer-block-module"
    ]
    assert [
        concept["id"] for concept in index.concepts_for_resource("transformer-block-module")
    ] == [
        "attention-mask",
        "layer-normalization",
        "multi-head-attention",
        "residual-connections",
        "scaled-dot-product-attention",
        "self-attention",
    ]

    assert index.revision_targets_for_page("en/entropy") == ()
    assert index.pages_for_revision_target("page", "en/entropy") == ()
    assert index.pages_for_revision_target("resource", "gpt-config-module") == ()


def test_real_repository_index_has_referential_integrity() -> None:
    index = ProjectIndex.build(ROOT)

    assert index.pages_by_id
    assert index.concepts_by_id
    assert len(index.resources_by_id) == 5
    assert len(index.page_resource_associations) == 10
    assert index.revision_edges == ()
    assert set(index.revision_status_by_page.values()) == {"not_assessed"}
    assert all(edge.target in index.pages_by_id for edge in index.page_edges)
    assert index.stats() == ProjectIndex.build(ROOT).stats()
