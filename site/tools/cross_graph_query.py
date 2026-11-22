"""Typed, read-only cross-graph paths over the ProjectIndex projection."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from cross_graph_evidence import (
    ComputationalNodeRecord,
    ExtractionItemRecord,
    RouteFocusGroup,
    SourceEvidenceRecord,
)
from project_index import ProjectIndex


@dataclass(frozen=True, slots=True)
class EvidencePathStep:
    ref: str
    entity_type: str
    entity_id: str
    label: str
    source_path: str | None = None
    status: str | None = None
    locator: dict[str, Any] | None = None
    confidence: str | None = None
    assumptions: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    details: dict[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class EvidencePathLink:
    source_ref: str
    target_ref: str
    relation: str
    basis: str
    source_path: str
    note: str | None = None


@dataclass(frozen=True, slots=True)
class EvidencePath:
    path_id: str
    kind: str
    concept_id: str
    steps: tuple[EvidencePathStep, ...]
    links: tuple[EvidencePathLink, ...]
    caveats: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class EvidenceGap:
    kind: str
    message: str
    source_id: str | None = None
    item_id: str | None = None
    source_path: str | None = None


@dataclass(frozen=True, slots=True)
class CrossGraphQueryResult:
    concept_id: str
    paths: tuple[EvidencePath, ...]
    gaps: tuple[EvidenceGap, ...]


def _label(labels: Any, language: str, fallback: str) -> str:
    if isinstance(labels, dict):
        value = labels.get(language) or labels.get("en") or labels.get("fr")
        if isinstance(value, str) and value.strip():
            return value
    return fallback


def _page_step(index: ProjectIndex, page_id: str) -> EvidencePathStep:
    page = index.pages_by_id[page_id]
    title = page.front.get("title")
    return EvidencePathStep(
        ref=f"page:{page_id}",
        entity_type="page",
        entity_id=page_id,
        label=title if isinstance(title, str) else page_id,
        source_path=page.path.as_posix(),
        status=page.tags.get("status"),
        details={"language": page.language, "destination": page.tags.get("destination")},
    )


def _concept_step(index: ProjectIndex, concept_id: str) -> EvidencePathStep:
    concept = index.concepts_by_id[concept_id]
    return EvidencePathStep(
        ref=f"concept:{concept_id}",
        entity_type="concept",
        entity_id=concept_id,
        label=_label(concept.get("labels"), "fr", concept_id),
        source_path="data/concepts.yml",
        details={"labels": concept.get("labels", {})},
    )


def _source_step(source: SourceEvidenceRecord) -> EvidencePathStep:
    status = source.scan_status
    return EvidencePathStep(
        ref=f"source:{source.source_id}",
        entity_type="source",
        entity_id=source.source_id,
        label=source.title,
        source_path=source.path,
        status=status,
        details={
            "canonical_url": source.canonical_url,
            "scan_status": source.scan_status,
            "integration_status": source.integration_status,
            "classification_concepts": source.classification_concepts,
            "related_concepts": source.related_concepts,
            "related_pages": source.related_pages,
        },
    )


def _extraction_step(item: ExtractionItemRecord, concept_id: str) -> EvidencePathStep:
    return EvidencePathStep(
        ref=f"extraction_item:{item.item_id}",
        entity_type="extraction_item",
        entity_id=item.item_id,
        label=item.claim,
        source_path=item.path,
        status=item.disposition,
        locator=item.locator,
        confidence=item.confidence,
        assumptions=item.assumptions,
        limitations=item.limitations,
        details={
            "source_id": item.source_id,
            "concept_mapping_basis": item.concept_mapping_basis.get(concept_id, ()),
            "candidate_pages": item.candidate_pages,
            "candidate_concepts": item.candidate_concepts,
        },
    )


def _node_step(node: ComputationalNodeRecord, language: str) -> EvidencePathStep:
    return EvidencePathStep(
        ref=f"computational_node:{node.node_id}",
        entity_type="computational_node",
        entity_id=node.node_id,
        label=_label(node.labels, language, node.node_id),
        source_path=node.path,
        details={
            "kind": node.kind,
            "role": node.role,
            "descriptions": node.descriptions,
            "resources": node.resources,
        },
    )


def _route_focus_step(group: RouteFocusGroup, page_title: str, language: str) -> EvidencePathStep:
    return EvidencePathStep(
        ref=f"route_focus:{group.stage_id}:{group.page_id}",
        entity_type="route_focus",
        entity_id=f"{group.stage_id}:{group.page_id}",
        label=f"{_label(group.stage_title, language, group.stage_id)} — {page_title}",
        source_path=group.path,
        details={
            "stage_id": group.stage_id,
            "page_id": group.page_id,
            "outcome": group.outcome,
            "references": tuple(
                {
                    "role": reference.role,
                    "type": reference.reference_type,
                    "id": reference.reference_id,
                }
                for reference in group.references
            ),
        },
    )


def _resource_label(resource: Any, language: str) -> str:
    return _label(resource.labels, language, resource.resource_id)


def query_concept(index: ProjectIndex, concept_id: str) -> CrossGraphQueryResult:
    """Return explicit source, computation, practice, and resource paths for a concept."""
    if concept_id not in index.concepts_by_id:
        raise KeyError(f"Unknown canonical concept: {concept_id}")
    projection = index.evidence_projection
    if projection is None:
        raise RuntimeError(
            "Cross-graph evidence is not loaded; build ProjectIndex with include_evidence=True"
        )

    concept_step = _concept_step(index, concept_id)
    paths: list[EvidencePath] = []
    gaps: list[EvidenceGap] = []
    item_sources: set[str] = set()

    # Item-level extraction mappings are the only source links treated as evidence paths.
    item_ids = projection.extraction_items_by_concept.get(concept_id, ())
    for item_id in item_ids:
        item = projection.extraction_items_by_id[item_id]
        source = projection.sources_by_id[item.source_id]
        item_sources.add(source.source_id)
        item_step = _extraction_step(item, concept_id)
        source_step = _source_step(source)
        caveats = list(item.limitations)
        if item.locator is None:
            caveats.append("No exact evidence locator is recorded for this extraction item.")
            gaps.append(
                EvidenceGap(
                    kind="missing-item-locator",
                    message="The item is mapped to the concept but has no exact locator.",
                    source_id=source.source_id,
                    item_id=item.item_id,
                    source_path=item.path,
                )
            )
        if source.scan_status != "scanned":
            caveats.append(f"Source scan status: {source.scan_status}.")
        if source.integration_status != "integrated":
            caveats.append(f"Source integration status: {source.integration_status}.")
        if item.disposition in {"defer", "reject"}:
            caveats.append(
                "Extraction disposition is "
                f"{item.disposition}; do not treat it as an accepted integration."
            )
        paths.append(
            EvidencePath(
                path_id=f"source-evidence:{concept_id}:{item.item_id}",
                kind="source-evidence",
                concept_id=concept_id,
                steps=(concept_step, item_step, source_step),
                links=(
                    EvidencePathLink(
                        source_ref=concept_step.ref,
                        target_ref=item_step.ref,
                        relation="mapped-to-concept",
                        basis="item.mapped_concepts or item.classification.concept_ids",
                        source_path=item.path,
                        note="Item-level mapping; source-level catalogue tags are not substituted.",
                    ),
                    EvidencePathLink(
                        source_ref=item_step.ref,
                        target_ref=source_step.ref,
                        relation="extracted-from",
                        basis="extraction_file.source_id",
                        source_path=item.path,
                    ),
                ),
                caveats=tuple(dict.fromkeys(caveats)),
            )
        )

    # Catalogue-level source associations are reported as gaps, never promoted to item evidence.
    for source_id, source_concepts in projection.source_level_concepts_by_id.items():
        if concept_id in source_concepts and source_id not in item_sources:
            source = projection.sources_by_id[source_id]
            gaps.append(
                EvidenceGap(
                    kind="source-catalogue-only",
                    message=(
                        "The source catalogue associates this source with the concept, "
                        "but no item-level extraction mapping resolves evidence."
                    ),
                    source_id=source_id,
                    source_path=source.path,
                )
            )

    # Candidate concept destinations are deliberately not traversed as accepted mappings.
    for item in projection.extraction_items_by_id.values():
        if concept_id in item.candidate_concepts and concept_id not in (
            *item.mapped_concepts,
            *item.classification_concepts,
        ):
            gaps.append(
                EvidenceGap(
                    kind="candidate-destination-not-promoted",
                    message=(
                        "The concept appears only as a candidate destination for this item; "
                        "no accepted item-level evidence path was created."
                    ),
                    source_id=item.source_id,
                    item_id=item.item_id,
                    source_path=item.path,
                )
            )

    # A page is an explicit mediator between a canonical concept and a computation node.
    computation_path_count = 0
    for page_id in sorted(index.pages_by_concept.get(concept_id, frozenset())):
        page_step = _page_step(index, page_id)
        for node_id in projection.computational_nodes_by_page.get(page_id, ()):
            node = projection.computational_nodes_by_id[node_id]
            node_step = _node_step(node, index.pages_by_id[page_id].language)
            paths.append(
                EvidencePath(
                    path_id=f"computation-via-page:{concept_id}:{page_id}:{node_id}",
                    kind="computation-via-page",
                    concept_id=concept_id,
                    steps=(concept_step, page_step, node_step),
                    links=(
                        EvidencePathLink(
                            source_ref=concept_step.ref,
                            target_ref=page_step.ref,
                            relation="has-concept-resource",
                            basis="concepts[].resources",
                            source_path="data/concepts.yml",
                        ),
                        EvidencePathLink(
                            source_ref=page_step.ref,
                            target_ref=node_step.ref,
                            relation="computational-resource-for",
                            basis="computational_graph.nodes[].resources",
                            source_path=node.path,
                        ),
                    ),
                    caveats=(
                        "Page-mediated association; this does not assert a direct "
                        "concept-to-node edge.",
                    ),
                )
            )
            computation_path_count += 1

    # Route focus is a separate, stage-mediated pedagogical relation.
    for group in projection.route_focus_groups:
        concept_refs = [
            reference
            for reference in group.references
            if reference.reference_type == "concept" and reference.reference_id == concept_id
        ]
        node_refs = [
            reference
            for reference in group.references
            if reference.reference_type == "node"
        ]
        if not concept_refs or not node_refs:
            continue
        page = index.pages_by_id[group.page_id]
        page_step = _page_step(index, group.page_id)
        focus_step = _route_focus_step(
            group,
            str(page.front.get("title", group.page_id)),
            page.language,
        )
        for concept_ref in concept_refs:
            for node_ref in node_refs:
                node = projection.computational_nodes_by_id[node_ref.reference_id]
                node_step = _node_step(node, page.language)
                paths.append(
                    EvidencePath(
                        path_id=(
                            f"route-focus:{concept_id}:{group.stage_id}:"
                            f"{group.page_id}:{node.node_id}"
                        ),
                        kind="route-focus-computation",
                        concept_id=concept_id,
                        steps=(concept_step, focus_step, node_step, page_step),
                        links=(
                            EvidencePathLink(
                                source_ref=concept_step.ref,
                                target_ref=focus_step.ref,
                                relation=f"route-focus-{concept_ref.role}",
                                basis=f"conceptual_focus.{concept_ref.role}",
                                source_path=group.path,
                            ),
                            EvidencePathLink(
                                source_ref=focus_step.ref,
                                target_ref=node_step.ref,
                                relation=f"route-focus-{node_ref.role}",
                                basis=f"conceptual_focus.{node_ref.role}",
                                source_path=group.path,
                            ),
                            EvidencePathLink(
                                source_ref=focus_step.ref,
                                target_ref=page_step.ref,
                                relation="focus-context-page",
                                basis="conceptual_focus page-slug key",
                                source_path=group.path,
                            ),
                        ),
                        caveats=(
                            "Stage-mediated pedagogical focus; not a direct canonical "
                            "concept-to-node relation.",
                        ),
                    )
                )
                computation_path_count += 1

    if computation_path_count == 0:
        gaps.append(
            EvidenceGap(
                kind="no-computation-path",
                message=(
                    "No explicit computation path was found through a concept page resource "
                    "or a guided-route conceptual-focus group."
                ),
            )
        )

    # Practice paths use only authored related edges to pages tagged destination:practice.
    practice_path_count = 0
    for page_id in sorted(index.pages_by_concept.get(concept_id, frozenset())):
        lesson_step = _page_step(index, page_id)
        for edge in index.pages_outgoing.get(page_id, ()):
            if edge.family != "related":
                continue
            practice_page = index.pages_by_id[edge.target]
            if practice_page.tags.get("destination") != "practice":
                continue
            practice_step = _page_step(index, edge.target)
            paths.append(
                EvidencePath(
                    path_id=f"practice:{concept_id}:{page_id}:{edge.target}",
                    kind="practice",
                    concept_id=concept_id,
                    steps=(concept_step, lesson_step, practice_step),
                    links=(
                        EvidencePathLink(
                            source_ref=concept_step.ref,
                            target_ref=lesson_step.ref,
                            relation="has-concept-resource",
                            basis="concepts[].resources",
                            source_path="data/concepts.yml",
                        ),
                        EvidencePathLink(
                            source_ref=lesson_step.ref,
                            target_ref=practice_step.ref,
                            relation="related-practice-page",
                            basis="page-map.related",
                            source_path=lesson_step.source_path or "",
                        ),
                    ),
                )
            )
            practice_path_count += 1
    if practice_path_count == 0:
        gaps.append(
            EvidenceGap(
                kind="no-practice-path",
                message="No authored related edge to a page tagged destination:practice was found.",
            )
        )

    # Non-page resources remain distinct from both source extractions and computation nodes.
    for association in index.concept_resource_associations:
        if association.concept_id != concept_id:
            continue
        resource = index.resources_by_id[association.resource_id]
        resource_step = EvidencePathStep(
            ref=f"resource:{resource.resource_id}",
            entity_type="resource",
            entity_id=resource.resource_id,
            label=_resource_label(resource, "fr"),
            source_path="data/resources.yml",
            status=resource.status,
            details={
                "kind": resource.kind,
                "language": resource.language,
                "location": resource.location,
                "referenced_by": resource.referenced_by,
                "programming_language": resource.programming_language,
                "provenance": resource.provenance,
            },
        )
        resource_links = (
            EvidencePathLink(
                source_ref=concept_step.ref,
                target_ref=resource_step.ref,
                relation="references-resource",
                basis="resources[].concepts",
                source_path="data/resources.yml",
            ),
        )
        paths.append(
            EvidencePath(
                path_id=f"resource:{concept_id}:{resource.resource_id}",
                kind="non-page-resource",
                concept_id=concept_id,
                steps=(concept_step, resource_step),
                links=resource_links,
            )
        )
        for page_id in resource.referenced_by:
            page_step = _page_step(index, page_id)
            paths.append(
                EvidencePath(
                    path_id=f"resource-page:{concept_id}:{resource.resource_id}:{page_id}",
                    kind="resource-page",
                    concept_id=concept_id,
                    steps=(concept_step, resource_step, page_step),
                    links=(
                        *resource_links,
                        EvidencePathLink(
                            source_ref=resource_step.ref,
                            target_ref=page_step.ref,
                            relation="referenced-by",
                            basis="resources.yml referenced_by",
                            source_path="data/resources.yml",
                        ),
                    ),
                )
            )

    if not item_ids:
        gaps.append(
            EvidenceGap(
                kind="no-item-level-evidence",
                message="No extraction item has an explicit item-level mapping to this concept.",
            )
        )

    return CrossGraphQueryResult(
        concept_id=concept_id,
        paths=tuple(sorted(paths, key=lambda path: path.path_id)),
        gaps=tuple(
            sorted(
                gaps,
                key=lambda gap: (
                    gap.kind,
                    gap.source_id or "",
                    gap.item_id or "",
                    gap.message,
                ),
            )
        ),
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root (defaults to the current checkout).",
    )
    parser.add_argument(
        "--concept",
        action="append",
        required=True,
        help="Canonical concept ID to query; may be supplied more than once.",
    )
    args = parser.parse_args(argv)
    index = ProjectIndex.build(args.root, include_evidence=True)
    results = [query_concept(index, concept_id) for concept_id in args.concept]
    print(json.dumps([asdict(result) for result in results], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
