from __future__ import annotations

import json
import runpy
from dataclasses import replace
from pathlib import Path

import pytest

from cross_graph_query import query_concept
from project_index import ProjectIndex


ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def evidence_index() -> ProjectIndex:
    return ProjectIndex.build(ROOT, include_evidence=True)


def test_source_and_computation_loading_is_opt_in() -> None:
    index = ProjectIndex.build(ROOT)

    assert index.evidence_projection is None
    with pytest.raises(RuntimeError, match="include_evidence=True"):
        query_concept(index, "scaled-dot-product-attention")


def test_projection_loads_existing_source_and_computation_records(
    evidence_index: ProjectIndex,
) -> None:
    projection = evidence_index.evidence_projection
    assert projection is not None

    assert len(projection.sources_by_id) >= 10
    assert len(projection.extraction_items_by_id) >= 10
    assert len(projection.computational_nodes_by_id) >= 10
    assert projection.route_focus_groups
    assert projection.extraction_items_by_concept["scaled-dot-product-attention"]
    assert projection.extraction_items_by_concept["predictive-compression"]
    assert projection.extraction_items_by_concept["v-information"]
    assert projection.computational_nodes_by_page["fr/scaled-dot-product-attention"]


def test_five_pilot_concepts_resolve_typed_cross_graph_paths(
    evidence_index: ProjectIndex,
) -> None:
    cases = {
        "scaled-dot-product-attention": {
            "source-evidence",
            "computation-via-page",
            "computation-edge-via-page",
            "route-focus-computation",
        },
        "predictive-compression": {"source-evidence"},
        "v-information": {"source-evidence"},
        "mutual-information": {"source-evidence"},
        "joint-embedding-predictive-architecture": {"practice"},
    }

    for concept_id, expected_kinds in cases.items():
        result = query_concept(evidence_index, concept_id)
        actual_kinds = {path.kind for path in result.paths}
        assert expected_kinds <= actual_kinds, concept_id


def test_source_paths_keep_exact_locators_confidence_and_scan_status(
    evidence_index: ProjectIndex,
) -> None:
    v_information = query_concept(evidence_index, "v-information")
    source_paths = [path for path in v_information.paths if path.kind == "source-evidence"]

    assert source_paths
    assert any(
        path.steps[1].locator
        and path.steps[1].locator.get("label") == "Definition 3"
        and path.steps[1].confidence == "established"
        for path in source_paths
    )
    definition_path = next(
        path
        for path in source_paths
        if path.steps[1].locator
        and path.steps[1].locator.get("label") == "Definition 3"
    )
    item_step = definition_path.steps[1]
    assert item_step.assumptions
    assert item_step.limitations
    assert item_step.details is not None
    assert item_step.details["kind"] == "definition"
    assert item_step.details["disposition_rationale"]
    assert definition_path.links[0].basis == "classification.concept_ids"
    assert any(
        path.steps[2].details
        and path.steps[2].details.get("scan_status") == "partially-scanned"
        for path in source_paths
    )

    predictive_compression = query_concept(evidence_index, "predictive-compression")
    compression_paths = [
        path for path in predictive_compression.paths if path.kind == "source-evidence"
    ]
    source_ids = {path.steps[2].entity_id for path in compression_paths}
    assert any(source_id.startswith("shannon-") for source_id in source_ids)
    assert any(source_id.startswith("rissanen-") for source_id in source_ids)


def test_route_focus_path_preserves_pedagogical_roles(
    evidence_index: ProjectIndex,
) -> None:
    result = query_concept(evidence_index, "scaled-dot-product-attention")
    path = next(path for path in result.paths if path.kind == "route-focus-computation")
    focus_step = next(step for step in path.steps if step.entity_type == "route_focus")
    assert focus_step.details is not None
    references = focus_step.details["references"]

    assert any(
        reference["type"] == "concept"
        and reference["id"] == "scaled-dot-product-attention"
        and reference["role"] == "objects"
        for reference in references
    )
    assert any(
        reference["type"] == "node"
        and reference["role"] == "objects"
        for reference in references
    )
    assert any("stage-mediated" in caveat for caveat in path.caveats)


def test_source_level_and_candidate_links_are_not_promoted_to_item_evidence(
    evidence_index: ProjectIndex,
) -> None:
    projection = evidence_index.evidence_projection
    assert projection is not None

    source_id = "vaswani-et-al-attention-is-all-you-need-2017"
    source_levels = dict(projection.source_level_concepts_by_id)
    source_levels[source_id] = tuple(
        sorted(set(source_levels.get(source_id, ())) | {"mutual-information"})
    )
    sources = dict(projection.sources_by_id)
    sources[source_id] = replace(
        sources[source_id],
        related_concepts=tuple(
            sorted(set(sources[source_id].related_concepts) | {"mutual-information"})
        ),
    )
    candidate_item = next(iter(projection.extraction_items_by_id.values()))
    updated_item = replace(
        candidate_item,
        mapped_concepts=(),
        classification_concepts=(),
        concept_mapping_basis={},
        candidate_concepts=("mutual-information",),
    )
    items = dict(projection.extraction_items_by_id)
    items[candidate_item.item_id] = updated_item
    item_mappings = {
        concept_id: tuple(
            item_id for item_id in item_ids if item_id != candidate_item.item_id
        )
        for concept_id, item_ids in projection.extraction_items_by_concept.items()
    }
    updated_projection = replace(
        projection,
        source_level_concepts_by_id=source_levels,
        sources_by_id=sources,
        extraction_items_by_id=items,
        extraction_items_by_concept=item_mappings,
    )
    updated_index = replace(evidence_index, evidence_projection=updated_projection)

    result = query_concept(updated_index, "mutual-information")
    source_gap = next(
        gap
        for gap in result.gaps
        if gap.kind == "source-catalogue-only" and gap.source_id == source_id
    )
    assert source_gap.basis == ("related.concepts",)
    candidate_gap = next(
        gap
        for gap in result.gaps
        if gap.kind == "candidate-destination-not-promoted"
        and gap.item_id == candidate_item.item_id
    )
    assert candidate_gap.basis == ("candidate_destinations.concepts",)
    assert not any(
        step.entity_type == "extraction_item" and step.entity_id == candidate_item.item_id
        for path in result.paths
        for step in path.steps
    )


def test_missing_item_locator_is_reported_as_a_gap(
    evidence_index: ProjectIndex,
) -> None:
    projection = evidence_index.evidence_projection
    assert projection is not None
    item_id = projection.extraction_items_by_concept["v-information"][0]
    item = projection.extraction_items_by_id[item_id]
    items = dict(projection.extraction_items_by_id)
    items[item_id] = replace(item, locator=None)
    updated_index = replace(
        evidence_index,
        evidence_projection=replace(projection, extraction_items_by_id=items),
    )

    result = query_concept(updated_index, "v-information")
    missing_locator_gap = next(
        gap
        for gap in result.gaps
        if gap.kind == "missing-item-locator" and gap.item_id == item_id
    )
    assert missing_locator_gap.basis == ("item.locator",)
    path = next(
        path
        for path in result.paths
        if path.kind == "source-evidence" and path.steps[1].entity_id == item_id
    )
    assert path.steps[1].locator is None


def test_cross_graph_query_cli_emits_json(capsys: pytest.CaptureFixture[str]) -> None:
    module = runpy.run_path(str(ROOT / "site" / "tools" / "cross_graph_query.py"))
    module["main"](
        [
            "--root",
            str(ROOT),
            "--concept",
            "scaled-dot-product-attention",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["concept_id"] == "scaled-dot-product-attention"
    assert any(path["kind"] == "source-evidence" for path in payload[0]["paths"])
