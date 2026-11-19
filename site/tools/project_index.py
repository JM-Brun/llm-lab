"""Deterministic, read-only queries over LLM Lab's canonical project metadata.

This module composes existing readers. It is an in-memory projection, not a
new registry or source of truth. Page, concept, route, resource and revision relations
stay distinct.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from page_index import PublishedPage, load_published_pages
from strict_yaml import load_yaml


class ProjectIndexIntegrityError(ValueError):
    """A canonical project relation points to a missing or invalid record."""

    def __init__(self, *, source: str, record_id: str, relation: str, target: object) -> None:
        self.source = source
        self.record_id = record_id
        self.relation = relation
        self.target = target
        super().__init__(
            f"{source}: record {record_id!r} has invalid {relation} reference {target!r}"
        )


@dataclass(frozen=True, slots=True)
class ResourceRecord:
    """One first-class non-page resource, retaining its canonical metadata."""

    resource_id: str
    kind: str
    language: str
    status: str
    labels: dict[str, str]
    descriptions: dict[str, str]
    location: dict[str, Any]
    referenced_by: tuple[str, ...]
    concepts: tuple[str, ...]
    programming_language: str | None = None
    provenance: dict[str, str] | None = None


@dataclass(frozen=True, slots=True)
class PageResourceAssociation:
    """A page explicitly listed by a non-page resource's referenced_by field."""

    page_id: str
    resource_id: str


@dataclass(frozen=True, slots=True)
class ConceptResourceAssociation:
    """A non-page resource explicitly associated with a canonical concept."""

    concept_id: str
    resource_id: str


@dataclass(frozen=True, slots=True)
class RevisionEdge:
    """A typed page-to-revision-support relation, separate from page graph edges."""

    source_page_id: str
    role: str
    target_type: str
    target_id: str


REVISION_STATUSES = {"not_assessed", "assessed", "not_applicable"}
REVISION_ROLES = {"synthesis", "flashcards", "revision_sheet"}
REVISION_TARGET_TYPES = {"section", "page", "resource"}
STABLE_ANCHOR = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def _language_matches(source: str, target: str) -> bool:
    """Allow exact language matches, regional variants, and language-neutral targets."""
    source_tag, target_tag = source.lower(), target.lower()
    if target_tag == "shared":
        return True
    if source_tag == "shared":
        return target_tag == "shared"
    return target_tag == source_tag or target_tag.startswith(source_tag + "-")


def _has_explicit_anchor(source: str, anchor: str) -> bool:
    """Find an explicit Quarto heading/div or HTML ID; never infer a slug from text."""
    escaped = re.escape(anchor)
    patterns = (
        r"^#{1,6}\s+.*\{[^}\n]*#" + escaped + r"(?=\s|\})[^}\n]*\}\s*$",
        r"^:::\s+\{[^}\n]*#" + escaped + r"(?=\s|\})[^}\n]*\}\s*$",
        r'\bid=["\']' + escaped + r'["\']',
    )
    return any(re.search(pattern, source, re.MULTILINE) for pattern in patterns)


def _load_non_page_resources(
    root: Path,
    pages: dict[str, PublishedPage],
    concepts: dict[str, dict[str, Any]],
) -> tuple[
    dict[str, ResourceRecord],
    tuple[PageResourceAssociation, ...],
    tuple[ConceptResourceAssociation, ...],
]:
    """Adapt data/resources.yml without conflating it with concept page IDs."""
    path = root / "data" / "resources.yml"
    data = load_yaml(path)
    if (
        not isinstance(data, dict)
        or type(data.get("schema_version")) is not int
        or data.get("schema_version") != 1
    ):
        raise ValueError("data/resources.yml: expected mapping with schema_version: 1")
    entries = data.get("resources")
    if not isinstance(entries, list) or not entries:
        raise ValueError("data/resources.yml: resources must be a non-empty list")

    records: dict[str, ResourceRecord] = {}
    page_associations: list[PageResourceAssociation] = []
    concept_associations: list[ConceptResourceAssociation] = []
    for index, item in enumerate(entries):
        where = f"data/resources.yml: resources[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where}: expected a mapping")
        resource_id = item.get("id")
        if not isinstance(resource_id, str) or not resource_id.strip():
            raise ValueError(f"{where}.id: expected a non-empty stable ID")
        if resource_id in records:
            raise ProjectIndexIntegrityError(
                source="data/resources.yml",
                record_id=resource_id,
                relation="duplicate resource ID",
                target=resource_id,
            )

        kind, language, status = item.get("kind"), item.get("language"), item.get("status")
        if not all(isinstance(value, str) and value for value in (kind, language, status)):
            raise ValueError(f"{where}: kind, language and status must be non-empty strings")
        labels, descriptions, location = (
            item.get("labels"),
            item.get("descriptions"),
            item.get("location"),
        )
        if not isinstance(labels, dict) or not isinstance(descriptions, dict):
            raise ValueError(f"{where}: labels and descriptions must be mappings")
        if not isinstance(location, dict):
            raise ValueError(f"{where}.location: expected a mapping")

        referenced_by = item.get("referenced_by")
        resource_concepts = item.get("concepts")
        if not isinstance(referenced_by, list) or not all(
            isinstance(value, str) for value in referenced_by
        ):
            raise ValueError(f"{where}.referenced_by: expected a list of page IDs")
        if not isinstance(resource_concepts, list) or not all(
            isinstance(value, str) for value in resource_concepts
        ):
            raise ValueError(f"{where}.concepts: expected a list of concept IDs")
        if len(referenced_by) != len(set(referenced_by)):
            raise ValueError(f"{where}.referenced_by: duplicate page IDs")
        if len(resource_concepts) != len(set(resource_concepts)):
            raise ValueError(f"{where}.concepts: duplicate concept IDs")

        for page_id in referenced_by:
            if page_id not in pages:
                raise ProjectIndexIntegrityError(
                    source="data/resources.yml",
                    record_id=resource_id,
                    relation="referenced_by (page ID)",
                    target=page_id,
                )
            page_associations.append(PageResourceAssociation(page_id, resource_id))
        for concept_id in resource_concepts:
            if concept_id not in concepts:
                raise ProjectIndexIntegrityError(
                    source="data/resources.yml",
                    record_id=resource_id,
                    relation="concepts (concept ID)",
                    target=concept_id,
                )
            concept_associations.append(ConceptResourceAssociation(concept_id, resource_id))

        programming_language = item.get("programming_language")
        if programming_language is not None and not isinstance(programming_language, str):
            raise ValueError(f"{where}.programming_language: expected a string when present")
        provenance = item.get("provenance")
        if provenance is not None and not isinstance(provenance, dict):
            raise ValueError(f"{where}.provenance: expected a mapping when present")
        records[resource_id] = ResourceRecord(
            resource_id=resource_id,
            kind=kind,
            language=language,
            status=status,
            labels=dict(labels),
            descriptions=dict(descriptions),
            location=dict(location),
            referenced_by=tuple(referenced_by),
            concepts=tuple(resource_concepts),
            programming_language=programming_language,
            provenance=dict(provenance) if provenance is not None else None,
        )

    return (
        records,
        tuple(sorted(page_associations, key=lambda edge: (edge.page_id, edge.resource_id))),
        tuple(sorted(concept_associations, key=lambda edge: (edge.concept_id, edge.resource_id))),
    )


def _load_revision_relations(
    pages: dict[str, PublishedPage],
    resources: dict[str, ResourceRecord],
) -> tuple[dict[str, str], tuple[RevisionEdge, ...]]:
    """Adapt the proposed page-map revision object without changing the page validator."""
    statuses: dict[str, str] = {}
    edges: list[RevisionEdge] = []
    for page_id, page in pages.items():
        if "revision" not in page.metadata:
            statuses[page_id] = "not_assessed"
            continue

        revision = page.metadata["revision"]
        where = f"{page.path.as_posix()}.revision"
        if not isinstance(revision, dict):
            raise ProjectIndexIntegrityError(
                source=where, record_id=page_id, relation="revision object", target=revision
            )
        unknown_fields = set(revision) - {"status", "resources", "reason"}
        if unknown_fields:
            names = ", ".join(sorted(map(str, unknown_fields)))
            raise ValueError(f"{where}: unknown field(s) {names}")
        status = revision.get("status")
        if not isinstance(status, str) or status not in REVISION_STATUSES:
            raise ValueError(f"{where}.status: unsupported revision status {status!r}")
        raw_edges = revision.get("resources", [])
        if not isinstance(raw_edges, list):
            raise ValueError(f"{where}.resources: expected a list")
        reason = revision.get("reason")
        if status == "not_applicable":
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError(f"{where}.reason: not_applicable requires a non-empty reason")
        elif reason is not None:
            raise ValueError(f"{where}.reason: only not_applicable may declare a reason")
        if status != "assessed" and raw_edges:
            raise ValueError(f"{where}.resources: {status} cannot contain revision relations")

        seen: set[tuple[str, str, str]] = set()
        for index, item in enumerate(raw_edges):
            relation_where = f"{where}.resources[{index}]"
            if not isinstance(item, dict) or set(item) != {"role", "target"}:
                raise ValueError(f"{relation_where}: expected exactly role and target")
            role, target = item.get("role"), item.get("target")
            if not isinstance(role, str) or role not in REVISION_ROLES:
                raise ValueError(f"{relation_where}.role: unsupported revision role {role!r}")
            if not isinstance(target, dict) or set(target) != {"type", "id"}:
                raise ValueError(f"{relation_where}.target: expected exactly type and id")
            target_type, target_id = target.get("type"), target.get("id")
            if not isinstance(target_type, str) or target_type not in REVISION_TARGET_TYPES:
                raise ValueError(
                    f"{relation_where}.target.type: unsupported target type {target_type!r}"
                )
            if not isinstance(target_id, str) or not target_id.strip():
                raise ValueError(f"{relation_where}.target.id: expected a non-empty string")
            key = (role, target_type, target_id)
            if key in seen:
                raise ValueError(f"{relation_where}: duplicate revision relationship {key!r}")
            seen.add(key)

            if target_type == "section":
                if not STABLE_ANCHOR.fullmatch(target_id):
                    raise ValueError(f"{relation_where}.target.id: invalid section anchor")
                if not _has_explicit_anchor(page.source, target_id):
                    raise ProjectIndexIntegrityError(
                        source=where,
                        record_id=page_id,
                        relation="revision section anchor",
                        target=target_id,
                    )
            elif target_type == "page":
                target_page = pages.get(target_id)
                if target_page is None or target_id == page_id:
                    raise ProjectIndexIntegrityError(
                        source=where,
                        record_id=page_id,
                        relation="revision page target",
                        target=target_id,
                    )
                if not _language_matches(page.language, target_page.language):
                    raise ProjectIndexIntegrityError(
                        source=where,
                        record_id=page_id,
                        relation="revision page target language",
                        target=target_id,
                    )
            else:
                target_resource = resources.get(target_id)
                if target_resource is None or target_resource.status != "published":
                    raise ProjectIndexIntegrityError(
                        source=where,
                        record_id=page_id,
                        relation="revision resource target",
                        target=target_id,
                    )
                if not _language_matches(page.language, target_resource.language):
                    raise ProjectIndexIntegrityError(
                        source=where,
                        record_id=page_id,
                        relation="revision resource target language",
                        target=target_id,
                    )
            edges.append(RevisionEdge(page_id, role, target_type, target_id))
        statuses[page_id] = status

    return statuses, tuple(
        sorted(
            edges,
            key=lambda edge: (
                edge.source_page_id,
                edge.role,
                edge.target_type,
                edge.target_id,
            ),
        )
    )


@dataclass(frozen=True, slots=True)
class PageEdge:
    """One authored page relation, preserving its relation family and direction."""

    source: str
    target: str
    family: str
    relation: str


@dataclass(frozen=True, slots=True)
class RouteMembership:
    """A page's explicit membership in one guided-route stage."""

    stage_id: str
    language: str
    role: str
    page_id: str
    position: int


@dataclass(slots=True)
class ProjectIndex:
    """In-memory projection of canonical page, concept, route and resource records."""

    pages_by_id: dict[str, PublishedPage]
    concepts_by_id: dict[str, dict[str, Any]]
    domains_by_id: dict[str, dict[str, Any]]
    page_edges: tuple[PageEdge, ...]
    route_memberships: tuple[RouteMembership, ...]
    pages_by_tag: dict[tuple[str, str], frozenset[str]]
    pages_by_concept: dict[str, frozenset[str]]
    concepts_by_page: dict[str, frozenset[str]]
    pages_by_domain: dict[str, frozenset[str]]
    pages_incoming: dict[str, tuple[PageEdge, ...]]
    pages_outgoing: dict[str, tuple[PageEdge, ...]]
    route_pages: dict[tuple[str, str, str], tuple[str, ...]]
    resources_by_id: dict[str, ResourceRecord]
    page_resource_associations: tuple[PageResourceAssociation, ...]
    concept_resource_associations: tuple[ConceptResourceAssociation, ...]
    resource_ids_by_page: dict[str, tuple[str, ...]]
    page_ids_by_resource: dict[str, tuple[str, ...]]
    resource_ids_by_concept: dict[str, tuple[str, ...]]
    concept_ids_by_resource: dict[str, tuple[str, ...]]
    revision_status_by_page: dict[str, str]
    revision_edges: tuple[RevisionEdge, ...]
    revision_edges_by_page: dict[str, tuple[RevisionEdge, ...]]
    revision_sources_by_page: dict[str, tuple[RevisionEdge, ...]]
    revision_sources_by_resource: dict[str, tuple[RevisionEdge, ...]]
    revision_sources_by_section: dict[tuple[str, str], tuple[RevisionEdge, ...]]

    @classmethod
    def build(cls, root: Path) -> ProjectIndex:
        """Build a deterministic snapshot from the repository root."""
        root = Path(root)
        published = load_published_pages(root / "site")
        pages = {page.page_id: page for page in published}

        concept_data = load_yaml(root / "data" / "concepts.yml")
        domain_data = load_yaml(root / "data" / "domains.yml")
        route_data = load_yaml(root / "data" / "guided-route.yml")
        concepts = {item["id"]: item for item in concept_data["concepts"]}
        domains = {item["id"]: item for item in domain_data["domains"]}
        resources, page_resource_associations, concept_resource_associations = (
            _load_non_page_resources(root, pages, concepts)
        )
        revision_status_by_page, revision_edges = _load_revision_relations(pages, resources)

        resource_ids_by_page: dict[str, set[str]] = defaultdict(set)
        page_ids_by_resource: dict[str, set[str]] = defaultdict(set)
        resource_ids_by_concept: dict[str, set[str]] = defaultdict(set)
        concept_ids_by_resource: dict[str, set[str]] = defaultdict(set)
        for association in page_resource_associations:
            resource_ids_by_page[association.page_id].add(association.resource_id)
            page_ids_by_resource[association.resource_id].add(association.page_id)
        for association in concept_resource_associations:
            resource_ids_by_concept[association.concept_id].add(association.resource_id)
            concept_ids_by_resource[association.resource_id].add(association.concept_id)

        revision_by_page: dict[str, list[RevisionEdge]] = defaultdict(list)
        revision_by_target_page: dict[str, list[RevisionEdge]] = defaultdict(list)
        revision_by_target_resource: dict[str, list[RevisionEdge]] = defaultdict(list)
        revision_by_target_section: dict[tuple[str, str], list[RevisionEdge]] = defaultdict(list)
        for edge in revision_edges:
            revision_by_page[edge.source_page_id].append(edge)
            if edge.target_type == "page":
                revision_by_target_page[edge.target_id].append(edge)
            elif edge.target_type == "resource":
                revision_by_target_resource[edge.target_id].append(edge)
            else:
                revision_by_target_section[(edge.source_page_id, edge.target_id)].append(edge)

        def freeze_ids(index: dict[str, set[str]]) -> dict[str, tuple[str, ...]]:
            return {key: tuple(sorted(value)) for key, value in index.items()}

        def sort_revision_edges(edges: list[RevisionEdge]) -> tuple[RevisionEdge, ...]:
            return tuple(
                sorted(
                    edges,
                    key=lambda edge: (
                        edge.source_page_id,
                        edge.role,
                        edge.target_type,
                        edge.target_id,
                    ),
                )
            )

        def freeze_revision_by_page(
            index: dict[str, list[RevisionEdge]],
        ) -> dict[str, tuple[RevisionEdge, ...]]:
            return {key: sort_revision_edges(value) for key, value in index.items()}

        def freeze_revision_by_section(
            index: dict[tuple[str, str], list[RevisionEdge]],
        ) -> dict[tuple[str, str], tuple[RevisionEdge, ...]]:
            return {key: sort_revision_edges(value) for key, value in index.items()}

        tag_index: dict[tuple[str, str], set[str]] = defaultdict(set)
        for page in published:
            for dimension, value in page.tags.items():
                tag_index[(dimension, value)].add(page.page_id)

        page_to_concepts: dict[str, set[str]] = defaultdict(set)
        concept_to_pages: dict[str, set[str]] = defaultdict(set)
        for concept_id, concept in concepts.items():
            # In schema v2, concepts[].resources contains page IDs. It is not
            # data/resources.yml and must not be counted as a non-page resource.
            for page_id in concept.get("resources", []):
                if not isinstance(page_id, str) or page_id not in pages:
                    raise ProjectIndexIntegrityError(
                        source="data/concepts.yml",
                        record_id=concept_id,
                        relation="resources (page ID)",
                        target=page_id,
                    )
                concept_to_pages[concept_id].add(page_id)
                page_to_concepts[page_id].add(concept_id)

        page_domain_index: dict[str, set[str]] = defaultdict(set)
        for page in published:
            domain = page.metadata.get("domain")
            if isinstance(domain, str) and domain:
                page_domain_index[domain].add(page.page_id)

        edges: list[PageEdge] = []
        for page in published:
            metadata = page.metadata
            suggested = metadata.get("suggested_route", {})
            if isinstance(suggested, dict):
                for relation in ("previous", "next"):
                    target = suggested.get(relation)
                    if isinstance(target, str) and target:
                        edges.append(PageEdge(page.page_id, target, "suggested_route", relation))
            hierarchy = metadata.get("hierarchy", {})
            if isinstance(hierarchy, dict):
                for relation in ("parents", "children"):
                    for target in hierarchy.get(relation, []):
                        edges.append(PageEdge(page.page_id, target, "hierarchy", relation))
            for target in metadata.get("related", []):
                edges.append(PageEdge(page.page_id, target, "related", "related"))

        for edge in edges:
            if edge.target not in pages:
                source_page = pages[edge.source]
                raise ProjectIndexIntegrityError(
                    source=source_page.path.relative_to(root).as_posix(),
                    record_id=edge.source,
                    relation=f"{edge.family}.{edge.relation}",
                    target=edge.target,
                )

        incoming: dict[str, list[PageEdge]] = defaultdict(list)
        outgoing: dict[str, list[PageEdge]] = defaultdict(list)
        for edge in edges:
            outgoing[edge.source].append(edge)
            incoming[edge.target].append(edge)

        memberships: list[RouteMembership] = []
        route_page_lists: dict[tuple[str, str, str], list[str]] = defaultdict(list)
        for stage in route_data["stages"]:
            for language in ("fr", "en"):
                for role, field in (("core", "pages"), ("optional", "optional_pages")):
                    for position, page_id in enumerate(stage.get(field, {}).get(language, [])):
                        if page_id not in pages:
                            raise ValueError(
                                f"guided-route stage {stage['id']!r} references "
                                f"unpublished or unknown page {page_id!r}"
                            )
                        membership = RouteMembership(stage["id"], language, role, page_id, position)
                        memberships.append(membership)
                        route_page_lists[(stage["id"], language, role)].append(page_id)

        return cls(
            pages_by_id=pages,
            concepts_by_id=concepts,
            domains_by_id=domains,
            page_edges=tuple(edges),
            route_memberships=tuple(memberships),
            pages_by_tag={key: frozenset(value) for key, value in tag_index.items()},
            pages_by_concept={key: frozenset(value) for key, value in concept_to_pages.items()},
            concepts_by_page={key: frozenset(value) for key, value in page_to_concepts.items()},
            pages_by_domain={key: frozenset(value) for key, value in page_domain_index.items()},
            pages_incoming={
                key: tuple(
                    sorted(value, key=lambda edge: (edge.source, edge.family, edge.relation))
                )
                for key, value in incoming.items()
            },
            pages_outgoing={
                key: tuple(
                    sorted(value, key=lambda edge: (edge.target, edge.family, edge.relation))
                )
                for key, value in outgoing.items()
            },
            route_pages={key: tuple(value) for key, value in route_page_lists.items()},
            resources_by_id=resources,
            page_resource_associations=page_resource_associations,
            concept_resource_associations=concept_resource_associations,
            resource_ids_by_page=freeze_ids(resource_ids_by_page),
            page_ids_by_resource=freeze_ids(page_ids_by_resource),
            resource_ids_by_concept=freeze_ids(resource_ids_by_concept),
            concept_ids_by_resource=freeze_ids(concept_ids_by_resource),
            revision_status_by_page=revision_status_by_page,
            revision_edges=revision_edges,
            revision_edges_by_page=freeze_revision_by_page(revision_by_page),
            revision_sources_by_page=freeze_revision_by_page(revision_by_target_page),
            revision_sources_by_resource=freeze_revision_by_page(revision_by_target_resource),
            revision_sources_by_section=freeze_revision_by_section(revision_by_target_section),
        )

    def select_pages(self, **filters: str) -> tuple[PublishedPage, ...]:
        """Select pages by exact tag dimensions (type, destination, topic, etc.)."""
        candidates: set[str] | None = None
        for dimension, value in filters.items():
            matches = set(self.pages_by_tag.get((dimension, value), frozenset()))
            candidates = matches if candidates is None else candidates & matches
        ids = candidates if candidates is not None else set(self.pages_by_id)
        return tuple(self.pages_by_id[key] for key in sorted(ids))

    def pages_for_concept(self, concept_id: str) -> tuple[PublishedPage, ...]:
        """Return pages explicitly listed by a canonical concept record."""
        if concept_id not in self.concepts_by_id:
            raise KeyError(f"unknown concept: {concept_id}")
        return tuple(
            self.pages_by_id[key] for key in sorted(self.pages_by_concept.get(concept_id, ()))
        )

    def concepts_for_page(self, page_id: str) -> tuple[dict[str, Any], ...]:
        """Return concepts explicitly associated with a page in concepts.yml."""
        if page_id not in self.pages_by_id:
            raise KeyError(f"unknown published page: {page_id}")
        return tuple(
            self.concepts_by_id[key] for key in sorted(self.concepts_by_page.get(page_id, ()))
        )

    def resources_for_page(self, page_id: str) -> tuple[ResourceRecord, ...]:
        """Return non-page resources explicitly referenced by a published page."""
        if page_id not in self.pages_by_id:
            raise KeyError(f"unknown published page: {page_id}")
        return tuple(
            self.resources_by_id[resource_id]
            for resource_id in self.resource_ids_by_page.get(page_id, ())
        )

    def pages_for_resource(self, resource_id: str) -> tuple[PublishedPage, ...]:
        """Return published pages listed by a non-page resource's referenced_by field."""
        if resource_id not in self.resources_by_id:
            raise KeyError(f"unknown resource: {resource_id}")
        return tuple(
            self.pages_by_id[page_id]
            for page_id in self.page_ids_by_resource.get(resource_id, ())
        )

    def resources_for_concept(self, concept_id: str) -> tuple[ResourceRecord, ...]:
        """Return non-page resources explicitly associated with a canonical concept."""
        if concept_id not in self.concepts_by_id:
            raise KeyError(f"unknown concept: {concept_id}")
        return tuple(
            self.resources_by_id[resource_id]
            for resource_id in self.resource_ids_by_concept.get(concept_id, ())
        )

    def concepts_for_resource(self, resource_id: str) -> tuple[dict[str, Any], ...]:
        """Return canonical concepts explicitly associated with a non-page resource."""
        if resource_id not in self.resources_by_id:
            raise KeyError(f"unknown resource: {resource_id}")
        return tuple(
            self.concepts_by_id[concept_id]
            for concept_id in self.concept_ids_by_resource.get(resource_id, ())
        )

    def revision_targets_for_page(
        self, page_id: str, *, role: str | None = None
    ) -> tuple[RevisionEdge, ...]:
        """Return typed revision targets declared by a source page."""
        if page_id not in self.pages_by_id:
            raise KeyError(f"unknown published page: {page_id}")
        if role is not None and (
            not isinstance(role, str) or role not in REVISION_ROLES
        ):
            raise ValueError(f"unknown revision role: {role}")
        return tuple(
            edge
            for edge in self.revision_edges_by_page.get(page_id, ())
            if role is None or edge.role == role
        )

    def revision_edges_for_target(
        self,
        target_type: str,
        target_id: str,
        *,
        section_page_id: str | None = None,
        role: str | None = None,
    ) -> tuple[RevisionEdge, ...]:
        """Return source→target revision edges using a page-local key for sections."""
        if role is not None and (
            not isinstance(role, str) or role not in REVISION_ROLES
        ):
            raise ValueError(f"unknown revision role: {role}")
        if not isinstance(target_id, str) or not target_id.strip():
            raise ValueError("target_id must be a non-empty string")
        if target_type == "page":
            if section_page_id is not None:
                raise ValueError("section_page_id is only valid for section targets")
            if target_id not in self.pages_by_id:
                raise KeyError(f"unknown revision target page: {target_id}")
            edges = self.revision_sources_by_page.get(target_id, ())
        elif target_type == "resource":
            if section_page_id is not None:
                raise ValueError("section_page_id is only valid for section targets")
            if target_id not in self.resources_by_id:
                raise KeyError(f"unknown revision target resource: {target_id}")
            edges = self.revision_sources_by_resource.get(target_id, ())
        elif target_type == "section":
            if not isinstance(section_page_id, str) or not section_page_id:
                raise ValueError("section targets require a non-empty section_page_id")
            page = self.pages_by_id.get(section_page_id)
            if page is None:
                raise KeyError(f"unknown section owner page: {section_page_id}")
            if not _has_explicit_anchor(page.source, target_id):
                raise KeyError(f"unknown explicit section anchor: {section_page_id}#{target_id}")
            edges = self.revision_sources_by_section.get((section_page_id, target_id), ())
        else:
            raise ValueError(f"unknown revision target type: {target_type}")
        return tuple(edge for edge in edges if role is None or edge.role == role)

    def pages_for_revision_target(
        self,
        target_type: str,
        target_id: str,
        *,
        section_page_id: str | None = None,
        role: str | None = None,
    ) -> tuple[PublishedPage, ...]:
        """Return unique source pages that point to a typed revision target."""
        edges = self.revision_edges_for_target(
            target_type,
            target_id,
            section_page_id=section_page_id,
            role=role,
        )
        source_ids = sorted({edge.source_page_id for edge in edges})
        return tuple(self.pages_by_id[page_id] for page_id in source_ids)

    def incoming_pages(
        self, page_id: str, *, family: str | None = None, relation: str | None = None
    ) -> tuple[PageEdge, ...]:
        """Return authored page edges targeting page_id, optionally filtered."""
        if page_id not in self.pages_by_id:
            raise KeyError(f"unknown published page: {page_id}")
        return tuple(
            edge
            for edge in self.pages_incoming.get(page_id, ())
            if (family is None or edge.family == family)
            and (relation is None or edge.relation == relation)
        )

    def outgoing_pages(
        self, page_id: str, *, family: str | None = None, relation: str | None = None
    ) -> tuple[PageEdge, ...]:
        """Return authored page edges originating at page_id, optionally filtered."""
        if page_id not in self.pages_by_id:
            raise KeyError(f"unknown published page: {page_id}")
        return tuple(
            edge
            for edge in self.pages_outgoing.get(page_id, ())
            if (family is None or edge.family == family)
            and (relation is None or edge.relation == relation)
        )

    def route_stage(
        self, stage_id: str, language: str, role: str = "core"
    ) -> tuple[PublishedPage, ...]:
        """Return explicitly ordered route members; role is core or optional."""
        if language not in {"fr", "en"} or role not in {"core", "optional"}:
            raise ValueError("language must be fr/en and role must be core/optional")
        key = (stage_id, language, role)
        if not any(m.stage_id == stage_id for m in self.route_memberships):
            raise KeyError(f"unknown route stage: {stage_id}")
        return tuple(self.pages_by_id[page_id] for page_id in self.route_pages.get(key, ()))

    def stats(self) -> dict[str, Any]:
        """Return counts with explicit units; route memberships are not page counts."""
        by_tag: dict[str, dict[str, int]] = defaultdict(dict)
        for (dimension, value), ids in sorted(self.pages_by_tag.items()):
            by_tag[dimension][value] = len(ids)
        return {
            "published_page_records": len(self.pages_by_id),
            "concepts": len(self.concepts_by_id),
            "domains": len(self.domains_by_id),
            "page_edges": len(self.page_edges),
            "route_memberships": len(self.route_memberships),
            "pages_by_tag": dict(by_tag),
            "concepts_by_importance": {
                importance: sum(
                    1
                    for concept in self.concepts_by_id.values()
                    if concept.get("importance") == importance
                )
                for importance in ("core", "supporting", "specialized")
            },
            "concepts_by_domain": {
                domain_id: sum(
                    1
                    for concept in self.concepts_by_id.values()
                    if domain_id in concept.get("domains", [])
                )
                for domain_id in sorted(self.domains_by_id)
            },
        }
