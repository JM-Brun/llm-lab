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
    destination: str = "understand",
    page_type: str = "concept-lesson",
    revision_role: str | None = None,
    revision_of: list[str] | None = None,
    revision_support: dict[str, Any] | None = None,
    body: str = "",
) -> None:
    _, slug = page_id.split("/", 1)
    path = site / language / f"{slug}.qmd"
    path.parent.mkdir(parents=True, exist_ok=True)
    tags = [
        f"type:{page_type}",
        f"destination:{destination}",
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
    if revision_role is not None:
        metadata["revision_role"] = revision_role
    if revision_of is not None:
        metadata["revision_of"] = revision_of
    if revision_support is not None:
        metadata["revision_support"] = revision_support
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


def test_page_revision_aid_builds_bidirectional_queries_and_assessment(tmp_path: Path) -> None:
    support = {
        "status": "partial",
        "evidence": [
            {
                "aid": "en/revision-sheet",
                "note": "Core identities are covered; the lesson-specific mask contract remains.",
            }
        ],
    }
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(
        tmp_path / "site",
        "en/attention",
        "en",
        revision_support=support,
    )
    _write_page(tmp_path / "site", "en/query", "en")
    _write_page(
        tmp_path / "site",
        "en/revision-sheet",
        "en",
        destination="practice",
        page_type="exercise-collection",
        revision_role="revision_sheet",
        revision_of=["en/attention"],
    )
    _write_sources(tmp_path)

    index = ProjectIndex.build(tmp_path)

    edge = MODULE["RevisionEdge"]("en/revision-sheet", "revision_sheet", "en/attention")
    assert index.revision_aids_for_lesson("en/attention") == (edge,)
    assert index.revision_aids_for_lesson("en/attention", role="flashcards") == ()
    assert [page.page_id for page in index.lessons_for_revision_aid("en/revision-sheet")] == [
        "en/attention"
    ]
    assert index.revision_support_for_lesson("en/attention")["status"] == "partial"
    assert index.revision_support_for_lesson("fr/attention")["status"] == "not_assessed"
    assert all(edge.family != "revision" for edge in index.page_edges)


def test_revision_aid_must_target_a_published_understand_or_build_lesson(tmp_path: Path) -> None:
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en")
    _write_page(tmp_path / "site", "en/query", "en")
    _write_page(
        tmp_path / "site",
        "en/revision-sheet",
        "en",
        destination="practice",
        page_type="exercise-collection",
        revision_role="revision_sheet",
        revision_of=["en/other-practice"],
    )
    _write_page(
        tmp_path / "site",
        "en/other-practice",
        "en",
        destination="practice",
        page_type="exercise-collection",
    )
    _write_sources(tmp_path)
    with pytest.raises(ValueError, match=r"revision_of \(eligible lesson\).*en/other-practice"):
        ProjectIndex.build(tmp_path)


def test_revision_aid_rejects_duplicate_targets(tmp_path: Path) -> None:
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en")
    _write_page(
        tmp_path / "site",
        "en/revision-sheet",
        "en",
        destination="practice",
        page_type="exercise-collection",
        revision_role="revision_sheet",
        revision_of=["en/attention", "en/attention"],
    )
    _write_sources(tmp_path)

    with pytest.raises(ValueError, match="duplicate page IDs"):
        ProjectIndex.build(tmp_path)


def test_revision_aid_rejects_wrong_language_targets(tmp_path: Path) -> None:
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en")
    _write_page(
        tmp_path / "site",
        "en/revision-sheet",
        "en",
        destination="practice",
        page_type="exercise-collection",
        revision_role="revision_sheet",
        revision_of=["fr/attention"],
    )
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)

    with pytest.raises(ValueError, match=r"revision_of language.*fr/attention"):
        ProjectIndex.build(tmp_path)


def test_revision_support_requires_valid_page_aid_evidence(tmp_path: Path) -> None:
    support = {
        "status": "companion_sufficient",
        "evidence": [{"aid": "en/missing-aid", "note": "A claimed aid."}],
    }
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en", revision_support=support)
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)

    with pytest.raises(ValueError, match=r"revision evidence aid.*en/missing-aid"):
        ProjectIndex.build(tmp_path)


def test_integrated_revision_support_requires_explicit_section_anchor(tmp_path: Path) -> None:
    support = {
        "status": "integrated_sufficient",
        "evidence": [{"anchor": "missing-summary", "note": "Integrated recap."}],
    }
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(tmp_path / "site", "en/attention", "en", revision_support=support)
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)

    with pytest.raises(ValueError, match=r"revision evidence anchor.*missing-summary"):
        ProjectIndex.build(tmp_path)


def test_integrated_revision_support_accepts_explicit_heading_anchor(tmp_path: Path) -> None:
    support = {
        "status": "integrated_sufficient",
        "evidence": [{"anchor": "revision-summary", "note": "Integrated recap."}],
    }
    _write_page(tmp_path / "site", "fr/attention", "fr")
    _write_page(
        tmp_path / "site",
        "en/attention",
        "en",
        revision_support=support,
        body="\n## Revision summary {#revision-summary}\n",
    )
    _write_page(tmp_path / "site", "en/query", "en")
    _write_sources(tmp_path)

    index = ProjectIndex.build(tmp_path)

    assert index.revision_support_for_lesson("en/attention")["status"] == "integrated_sufficient"


def test_real_repository_index_has_referential_integrity() -> None:
    index = ProjectIndex.build(ROOT)

    assert index.pages_by_id
    assert index.concepts_by_id
    assert len(index.resources_by_id) == 5
    assert len(index.page_resource_associations) == 10
    assert len(index.revision_edges) == 4
    assert {
        (edge.aid_page_id, edge.role, edge.source_page_id) for edge in index.revision_edges
    } == {
        ("fr/revision-information-theory", "revision_sheet", "fr/entropy"),
        ("fr/revision-information-theory", "revision_sheet", "fr/cross-entropy"),
        ("en/revision-information-theory", "revision_sheet", "en/entropy"),
        ("en/revision-information-theory", "revision_sheet", "en/cross-entropy"),
    }
    assert {
        page.page_id for page in index.lessons_for_revision_aid("fr/revision-information-theory")
    } == {"fr/entropy", "fr/cross-entropy"}
    assert {edge.aid_page_id for edge in index.revision_aids_for_lesson("en/cross-entropy")} == {
        "en/revision-information-theory"
    }
    assert all(
        index.revision_support_for_lesson(page_id)["status"] == "partial"
        for page_id in ("fr/entropy", "en/entropy", "fr/cross-entropy", "en/cross-entropy")
    )
    integrated_pages = {
        "fr/corpus-preparation",
        "en/corpus-preparation",
        "fr/training-examples",
        "en/training-examples",
        "fr/causal-masking",
        "en/causal-masking",
        "fr/transformer-architectures",
        "en/transformer-architectures",
        "fr/llm-overview",
        "en/llm-overview",
        "fr/generation",
        "en/generation",
        "fr/post-training",
        "en/post-training",
        "fr/context-engineering",
        "en/context-engineering",
        "fr/llm-limits",
        "en/llm-limits",
        "fr/text-data",
        "en/text-data",
        "fr/logits",
        "en/logits",
        "fr/probabilites",
        "en/probabilities",
        "fr/loss",
        "en/loss",
        "fr/gradients",
        "en/gradients",
        "fr/positional-encoding",
        "en/positional-encoding",
        "fr/contextualized-representations",
        "en/contextualized-representations",
        "fr/embedding-space",
        "en/embedding-space",
        "fr/in-context-learning",
        "en/in-context-learning",
        "fr/queries-keys-values",
        "en/queries-keys-values",
        "fr/scaled-dot-product-attention",
        "en/scaled-dot-product-attention",
        "fr/training-loop",
        "en/training-loop",
        "fr/transformer",
        "en/transformer",
        "fr/vraisemblance",
        "en/likelihood",
    }
    assert {
        page_id
        for page_id, assessment in index.revision_support_by_page.items()
        if assessment["status"] == "integrated_sufficient"
    } == integrated_pages
    assert (
        sum(item["status"] == "not_assessed" for item in index.revision_support_by_page.values())
        == len(index.revision_support_by_page) - 50
    )
    assert all(edge.target in index.pages_by_id for edge in index.page_edges)
    assert index.stats() == ProjectIndex.build(ROOT).stats()
