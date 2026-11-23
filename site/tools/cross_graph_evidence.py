"""Optional read-only projection of source evidence and computational relations."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from page_index import PublishedPage
from project_index_errors import ProjectIndexIntegrityError
from strict_yaml import load_yaml


@dataclass(frozen=True, slots=True)
class SourceEvidenceRecord:
    source_id: str
    title: str
    canonical_url: str | None
    scan_status: str | None
    integration_status: str | None
    classification_concepts: tuple[str, ...]
    related_concepts: tuple[str, ...]
    related_pages: tuple[str, ...]
    path: str


@dataclass(frozen=True, slots=True)
class ExtractionItemRecord:
    item_id: str
    source_id: str
    kind: str
    claim: str
    locator: dict[str, Any] | None
    confidence: str | None
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    mapped_concepts: tuple[str, ...]
    classification_concepts: tuple[str, ...]
    concept_mapping_basis: dict[str, tuple[str, ...]]
    disposition: str | None
    disposition_rationale: str | None
    candidate_pages: tuple[str, ...]
    candidate_concepts: tuple[str, ...]
    path: str


@dataclass(frozen=True, slots=True)
class ComputationalNodeRecord:
    node_id: str
    kind: str
    role: str
    labels: dict[str, Any]
    descriptions: dict[str, Any]
    resources: tuple[str, ...]
    path: str


@dataclass(frozen=True, slots=True)
class ComputationalEdgeRecord:
    edge_id: str
    source_node_id: str
    target_node_id: str
    relation_type: str
    path: str


@dataclass(frozen=True, slots=True)
class RouteFocusReference:
    role: str
    reference_type: str
    reference_id: str


@dataclass(frozen=True, slots=True)
class RouteFocusGroup:
    stage_id: str
    page_id: str
    stage_title: dict[str, Any]
    outcome: dict[str, Any]
    references: tuple[RouteFocusReference, ...]
    path: str


@dataclass(frozen=True, slots=True)
class CrossGraphEvidenceProjection:
    sources_by_id: dict[str, SourceEvidenceRecord]
    extraction_items_by_id: dict[str, ExtractionItemRecord]
    extraction_items_by_concept: dict[str, tuple[str, ...]]
    source_level_concepts_by_id: dict[str, tuple[str, ...]]
    computational_nodes_by_id: dict[str, ComputationalNodeRecord]
    computational_nodes_by_page: dict[str, tuple[str, ...]]
    computational_edges: tuple[ComputationalEdgeRecord, ...]
    route_focus_groups: tuple[RouteFocusGroup, ...]
    route_focus_by_page: dict[str, tuple[RouteFocusGroup, ...]]
    unresolved_route_focus: tuple[str, ...]


def _string_tuple(value: Any, *, source: str, record_id: str, relation: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list):
        values = value
    else:
        raise ProjectIndexIntegrityError(
            source=source,
            record_id=record_id,
            relation=relation,
            target=type(value).__name__,
        )
    if any(not isinstance(item, str) or not item.strip() for item in values):
        raise ProjectIndexIntegrityError(
            source=source,
            record_id=record_id,
            relation=relation,
            target=repr(values),
        )
    return tuple(dict.fromkeys(values))


def _optional_text(value: Any) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def load_cross_graph_evidence_projection(
    root: Path,
    pages: dict[str, PublishedPage],
    concepts: dict[str, dict[str, Any]],
    route_data: dict[str, Any],
) -> CrossGraphEvidenceProjection:
    source_path = root / "data" / "sources.yml"
    source_data = load_yaml(source_path)
    if (
        not isinstance(source_data, dict)
        or type(source_data.get("schema_version")) is not int
        or source_data.get("schema_version") != 1
    ):
        raise ValueError("data/sources.yml: expected mapping with schema_version: 1")
    source_entries = source_data.get("sources")
    if not isinstance(source_entries, list):
        raise ValueError("data/sources.yml must define a sources list")

    sources_by_id: dict[str, SourceEvidenceRecord] = {}
    source_level_concepts_by_id: dict[str, tuple[str, ...]] = {}
    for source_entry in source_entries:
        if not isinstance(source_entry, dict):
            raise ValueError("Every source catalogue entry must be a mapping")
        source_id = source_entry.get("id")
        if not isinstance(source_id, str) or not source_id:
            raise ValueError("Every source catalogue entry must have a non-empty id")
        if source_id in sources_by_id:
            raise ProjectIndexIntegrityError(
                source="data/sources.yml",
                record_id=source_id,
                relation="unique source id",
                target=source_id,
            )
        classification = source_entry.get("classification") or {}
        related = source_entry.get("related") or {}
        if not isinstance(classification, dict) or not isinstance(related, dict):
            raise ProjectIndexIntegrityError(
                source="data/sources.yml",
                record_id=source_id,
                relation="classification and related mappings",
                target="non-mapping value",
            )
        classification_concepts = _string_tuple(
            classification.get("concept_ids"),
            source="data/sources.yml",
            record_id=source_id,
            relation="classification.concept_ids",
        )
        related_concepts = _string_tuple(
            related.get("concepts"),
            source="data/sources.yml",
            record_id=source_id,
            relation="related.concepts",
        )
        related_pages = _string_tuple(
            related.get("pages"),
            source="data/sources.yml",
            record_id=source_id,
            relation="related.pages",
        )
        for concept_id in (*classification_concepts, *related_concepts):
            if concept_id not in concepts:
                raise ProjectIndexIntegrityError(
                    source="data/sources.yml",
                    record_id=source_id,
                    relation="source-level concept association",
                    target=concept_id,
                )
        for page_id in related_pages:
            if page_id not in pages:
                raise ProjectIndexIntegrityError(
                    source="data/sources.yml",
                    record_id=source_id,
                    relation="related.pages",
                    target=page_id,
                )
        source_level_concepts_by_id[source_id] = tuple(
            sorted(set(classification_concepts) | set(related_concepts))
        )
        sources_by_id[source_id] = SourceEvidenceRecord(
            source_id=source_id,
            title=_optional_text(source_entry.get("title")) or source_id,
            canonical_url=_optional_text(source_entry.get("canonical_url")),
            scan_status=_optional_text(source_entry.get("scan_status")),
            integration_status=_optional_text(source_entry.get("integration_status")),
            classification_concepts=classification_concepts,
            related_concepts=related_concepts,
            related_pages=related_pages,
            path="data/sources.yml",
        )

    extraction_items_by_id: dict[str, ExtractionItemRecord] = {}
    extraction_items_by_concept: dict[str, list[str]] = defaultdict(list)
    extraction_root = root / "data" / "extractions"
    extraction_paths = sorted((*extraction_root.glob("*.yml"), *extraction_root.glob("*.yaml")))
    for extraction_path in extraction_paths:
        extraction_data = load_yaml(extraction_path)
        if not isinstance(extraction_data, dict):
            raise ValueError(f"{extraction_path.relative_to(root).as_posix()}: expected a mapping")
        source_id = extraction_data.get("source_id")
        if not isinstance(source_id, str) or source_id not in sources_by_id:
            raise ProjectIndexIntegrityError(
                source=extraction_path.relative_to(root).as_posix(),
                record_id=str(source_id),
                relation="source_id",
                target=str(source_id),
            )
        items = extraction_data.get("items", [])
        if not isinstance(items, list):
            raise ProjectIndexIntegrityError(
                source=extraction_path.relative_to(root).as_posix(),
                record_id=source_id,
                relation="items",
                target=type(items).__name__,
            )
        item_path = extraction_path.relative_to(root).as_posix()
        for item in items:
            if not isinstance(item, dict):
                raise ProjectIndexIntegrityError(
                    source=item_path,
                    record_id=source_id,
                    relation="items entry",
                    target=type(item).__name__,
                )
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id:
                raise ProjectIndexIntegrityError(
                    source=item_path,
                    record_id=source_id,
                    relation="item.id",
                    target=repr(item_id),
                )
            if item_id in extraction_items_by_id:
                raise ProjectIndexIntegrityError(
                    source=item_path,
                    record_id=item_id,
                    relation="unique extraction item id",
                    target=item_id,
                )
            classification = item.get("classification") or {}
            evidence = item.get("evidence") or {}
            if not isinstance(classification, dict):
                classification = {}
            if not isinstance(evidence, dict):
                evidence = {}
            mapped_concepts = _string_tuple(
                item.get("mapped_concepts"),
                source=item_path,
                record_id=item_id,
                relation="mapped_concepts",
            )
            classification_concepts = _string_tuple(
                classification.get("concept_ids"),
                source=item_path,
                record_id=item_id,
                relation="classification.concept_ids",
            )
            mapping_basis: dict[str, list[str]] = defaultdict(list)
            for concept_id in mapped_concepts:
                mapping_basis[concept_id].append("mapped_concepts")
            for concept_id in classification_concepts:
                mapping_basis[concept_id].append("classification.concept_ids")
            for concept_id in mapping_basis:
                if concept_id not in concepts:
                    raise ProjectIndexIntegrityError(
                        source=item_path,
                        record_id=item_id,
                        relation="item-level concept mapping",
                        target=concept_id,
                    )
                extraction_items_by_concept[concept_id].append(item_id)

            locator_value = item.get("locator")
            if locator_value is None:
                locator = None
            elif isinstance(locator_value, dict):
                locator = dict(locator_value)
            elif isinstance(locator_value, str):
                locator = {"value": locator_value}
            else:
                raise ProjectIndexIntegrityError(
                    source=item_path,
                    record_id=item_id,
                    relation="locator",
                    target=type(locator_value).__name__,
                )
            candidate_destinations = item.get("candidate_destinations") or {}
            if not isinstance(candidate_destinations, dict):
                candidate_destinations = {}
            candidate_pages = _string_tuple(
                candidate_destinations.get("pages"),
                source=item_path,
                record_id=item_id,
                relation="candidate_destinations.pages",
            )
            candidate_concepts = _string_tuple(
                candidate_destinations.get("concepts"),
                source=item_path,
                record_id=item_id,
                relation="candidate_destinations.concepts",
            )
            assumptions = _string_tuple(
                evidence.get("assumptions", item.get("assumptions")),
                source=item_path,
                record_id=item_id,
                relation="evidence.assumptions",
            )
            limitations = _string_tuple(
                evidence.get("limitations", item.get("limitations")),
                source=item_path,
                record_id=item_id,
                relation="evidence.limitations",
            )
            claim = (
                _optional_text(item.get("claim"))
                or _optional_text(item.get("summary"))
                or _optional_text(item.get("title"))
                or item_id
            )
            extraction_items_by_id[item_id] = ExtractionItemRecord(
                item_id=item_id,
                source_id=source_id,
                kind=_optional_text(item.get("kind")) or "unspecified",
                claim=claim,
                locator=locator,
                confidence=_optional_text(evidence.get("confidence"))
                or _optional_text(item.get("confidence")),
                assumptions=assumptions,
                limitations=limitations,
                mapped_concepts=mapped_concepts,
                classification_concepts=classification_concepts,
                concept_mapping_basis={
                    key: tuple(sorted(set(value))) for key, value in mapping_basis.items()
                },
                disposition=_optional_text(classification.get("disposition"))
                or _optional_text(item.get("disposition")),
                disposition_rationale=_optional_text(item.get("disposition_rationale")),
                candidate_pages=candidate_pages,
                candidate_concepts=candidate_concepts,
                path=item_path,
            )

    graph_path = root / "data" / "computational-graph.yml"
    graph_data = load_yaml(graph_path)
    if (
        not isinstance(graph_data, dict)
        or type(graph_data.get("schema_version")) is not int
        or graph_data.get("schema_version") != 1
    ):
        raise ValueError("data/computational-graph.yml: expected mapping with schema_version: 1")
    graph_nodes = graph_data.get("nodes")
    graph_edges = graph_data.get("edges", [])
    if not isinstance(graph_nodes, list) or not isinstance(graph_edges, list):
        raise ValueError("data/computational-graph.yml must define nodes and edges lists")
    computational_nodes_by_id: dict[str, ComputationalNodeRecord] = {}
    computational_nodes_by_page: dict[str, list[str]] = defaultdict(list)
    for node in graph_nodes:
        if not isinstance(node, dict):
            raise ValueError("Every computational graph node must be a mapping")
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id:
            raise ValueError("Every computational graph node must have a non-empty id")
        if node_id in computational_nodes_by_id:
            raise ProjectIndexIntegrityError(
                source="data/computational-graph.yml",
                record_id=node_id,
                relation="unique computational node id",
                target=node_id,
            )
        resources = _string_tuple(
            node.get("resources"),
            source="data/computational-graph.yml",
            record_id=node_id,
            relation="resources",
        )
        for page_id in resources:
            if page_id not in pages:
                raise ProjectIndexIntegrityError(
                    source="data/computational-graph.yml",
                    record_id=node_id,
                    relation="resources",
                    target=page_id,
                )
            computational_nodes_by_page[page_id].append(node_id)
        labels = node.get("labels") or {}
        descriptions = node.get("descriptions") or {}
        computational_nodes_by_id[node_id] = ComputationalNodeRecord(
            node_id=node_id,
            kind=_optional_text(node.get("kind")) or "unspecified",
            role=_optional_text(node.get("role")) or "unspecified",
            labels=dict(labels) if isinstance(labels, dict) else {},
            descriptions=dict(descriptions) if isinstance(descriptions, dict) else {},
            resources=resources,
            path="data/computational-graph.yml",
        )

    computational_edges: list[ComputationalEdgeRecord] = []
    for position, edge in enumerate(graph_edges):
        if not isinstance(edge, dict):
            raise ProjectIndexIntegrityError(
                source="data/computational-graph.yml",
                record_id=str(position),
                relation="edge",
                target=type(edge).__name__,
            )
        source_node_id = edge.get("from")
        target_node_id = edge.get("to")
        relation_type = edge.get("type")
        for relation, node_id in (
            ("from", source_node_id),
            ("to", target_node_id),
        ):
            if not isinstance(node_id, str) or node_id not in computational_nodes_by_id:
                raise ProjectIndexIntegrityError(
                    source="data/computational-graph.yml",
                    record_id=str(edge.get("id", position)),
                    relation=relation,
                    target=str(node_id),
                )
        if not isinstance(source_node_id, str) or not isinstance(target_node_id, str):
            raise ProjectIndexIntegrityError(
                source="data/computational-graph.yml",
                record_id=str(edge.get("id", position)),
                relation="endpoints",
                target=f"{source_node_id!r} -> {target_node_id!r}",
            )
        if not isinstance(relation_type, str) or not relation_type:
            raise ProjectIndexIntegrityError(
                source="data/computational-graph.yml",
                record_id=str(edge.get("id", position)),
                relation="type",
                target=str(relation_type),
            )
        computational_edges.append(
            ComputationalEdgeRecord(
                edge_id=_optional_text(edge.get("id"))
                or f"{source_node_id}:{relation_type}:{target_node_id}",
                source_node_id=source_node_id,
                target_node_id=target_node_id,
                relation_type=relation_type,
                path="data/computational-graph.yml",
            )
        )

    route_focus_groups: list[RouteFocusGroup] = []
    unresolved_route_focus: list[str] = []
    for stage in route_data.get("stages", []):
        if not isinstance(stage, dict):
            raise ValueError("Every guided-route stage must be a mapping")
        stage_id = stage.get("id")
        if not isinstance(stage_id, str) or not stage_id.strip():
            raise ValueError("data/guided-route.yml: every stage needs a non-empty string ID")
        stage_pages_data = stage.get("pages") or {}
        if not isinstance(stage_pages_data, dict):
            raise ProjectIndexIntegrityError(
                source="data/guided-route.yml",
                record_id=str(stage_id),
                relation="pages",
                target=type(stage_pages_data).__name__,
            )
        stage_pages = [
            page_id for language in ("fr", "en") for page_id in stage_pages_data.get(language, [])
        ]
        focus_map = stage.get("conceptual_focus") or {}
        if not isinstance(focus_map, dict):
            continue
        stage_title = stage.get("title") or {}
        outcome_default = stage.get("outcome") or {}
        for page_slug, focus in focus_map.items():
            matching_pages = [
                page_id for page_id in stage_pages if page_id.rsplit("/", 1)[-1] == page_slug
            ]
            if not matching_pages:
                unresolved_route_focus.append(f"{stage_id}:{page_slug}")
                continue
            if not isinstance(focus, dict):
                continue
            outcome = focus.get("outcome") or outcome_default
            references: list[RouteFocusReference] = []
            for role in ("objects", "mobilizes"):
                raw_references = _string_tuple(
                    focus.get(role),
                    source="data/guided-route.yml",
                    record_id=f"{stage_id}:{page_slug}",
                    relation=f"conceptual_focus.{role}",
                )
                for raw_reference in raw_references:
                    if ":" not in raw_reference:
                        raise ProjectIndexIntegrityError(
                            source="data/guided-route.yml",
                            record_id=f"{stage_id}:{page_slug}",
                            relation=f"conceptual_focus.{role}",
                            target=raw_reference,
                        )
                    reference_type, reference_id = raw_reference.split(":", 1)
                    registry = (
                        concepts
                        if reference_type == "concept"
                        else computational_nodes_by_id
                        if reference_type == "node"
                        else None
                    )
                    if registry is None or reference_id not in registry:
                        raise ProjectIndexIntegrityError(
                            source="data/guided-route.yml",
                            record_id=f"{stage_id}:{page_slug}",
                            relation=f"conceptual_focus.{role}",
                            target=raw_reference,
                        )
                    references.append(RouteFocusReference(role, reference_type, reference_id))
            if not references:
                continue
            for page_id in matching_pages:
                route_focus_groups.append(
                    RouteFocusGroup(
                        stage_id=stage_id,
                        page_id=page_id,
                        stage_title=dict(stage_title) if isinstance(stage_title, dict) else {},
                        outcome=dict(outcome) if isinstance(outcome, dict) else {},
                        references=tuple(references),
                        path="data/guided-route.yml",
                    )
                )

    route_focus_by_page: dict[str, list[RouteFocusGroup]] = defaultdict(list)
    for group in route_focus_groups:
        route_focus_by_page[group.page_id].append(group)

    return CrossGraphEvidenceProjection(
        sources_by_id=sources_by_id,
        extraction_items_by_id=extraction_items_by_id,
        extraction_items_by_concept={
            key: tuple(sorted(value)) for key, value in extraction_items_by_concept.items()
        },
        source_level_concepts_by_id=source_level_concepts_by_id,
        computational_nodes_by_id=computational_nodes_by_id,
        computational_nodes_by_page={
            key: tuple(sorted(value)) for key, value in computational_nodes_by_page.items()
        },
        computational_edges=tuple(
            sorted(
                computational_edges,
                key=lambda edge: (edge.source_node_id, edge.relation_type, edge.target_node_id),
            )
        ),
        route_focus_groups=tuple(
            sorted(route_focus_groups, key=lambda group: (group.stage_id, group.page_id))
        ),
        route_focus_by_page={
            key: tuple(sorted(value, key=lambda group: group.stage_id))
            for key, value in route_focus_by_page.items()
        },
        unresolved_route_focus=tuple(sorted(unresolved_route_focus)),
    )
