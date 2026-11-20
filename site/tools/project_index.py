"""Deterministic, read-only queries over LLM Lab's canonical project metadata.

This module composes existing readers. It is an in-memory projection, not a
new registry or source of truth. Page, concept, route, resource and revision relations
stay distinct.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
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
    """A typed revision-aid → source-lesson relation, separate from page graph edges."""

    aid_page_id: str
    role: str
    source_page_id: str


REVISION_ROLES = {"synthesis", "flashcards", "revision_sheet"}
REVISION_SUPPORT_STATUSES = {
    "not_assessed",
    "integrated_sufficient",
    "companion_sufficient",
    "partial",
    "missing",
    "not_applicable",
}
ELIGIBLE_LESSON_DESTINATIONS = {"understand", "build"}
STABLE_ANCHOR = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def _language_matches(aid_language: str, lesson_language: str) -> bool:
    """Require same-language aids; allow a genuinely multilingual resource."""
    aid_tag, lesson_tag = aid_language.lower(), lesson_language.lower()
    if aid_tag == "mul":
        return lesson_tag in {"fr", "en"}
    if aid_tag == "shared":
        return lesson_tag == "shared"
    return lesson_tag == aid_tag or lesson_tag.startswith(aid_tag + "-")


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
        if (
            not isinstance(kind, str)
            or not isinstance(language, str)
            or not isinstance(status, str)
            or not all((kind, language, status))
        ):
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
) -> tuple[dict[str, dict[str, Any]], tuple[RevisionEdge, ...]]:
    """Load aid → lesson relations and evidence-backed lesson assessments."""
    edges: list[RevisionEdge] = []
    for page_id, aid in pages.items():
        role = aid.metadata.get("revision_role")
        raw_targets = aid.metadata.get("revision_of")
        if role is None and raw_targets is None:
            continue
        where = f"{aid.path.as_posix()}.revision"
        if not isinstance(role, str) or role not in REVISION_ROLES:
            raise ValueError(f"{where}.revision_role: unsupported revision role {role!r}")
        if (
            not isinstance(raw_targets, list)
            or not raw_targets
            or not all(isinstance(target, str) and target.strip() for target in raw_targets)
        ):
            raise ValueError(f"{where}.revision_of: expected a non-empty list of page IDs")
        if len(raw_targets) != len(set(raw_targets)):
            raise ValueError(f"{where}.revision_of: duplicate page IDs")
        if aid.tags.get("destination") in ELIGIBLE_LESSON_DESTINATIONS:
            raise ValueError(f"{where}: a source lesson cannot also be declared as a revision aid")
        for target_id in raw_targets:
            target = pages.get(target_id)
            if target is None:
                raise ProjectIndexIntegrityError(
                    source=where,
                    record_id=page_id,
                    relation="revision_of (published page)",
                    target=target_id,
                )
            if target.tags.get("destination") not in ELIGIBLE_LESSON_DESTINATIONS:
                raise ProjectIndexIntegrityError(
                    source=where,
                    record_id=page_id,
                    relation="revision_of (eligible lesson)",
                    target=target_id,
                )
            if not _language_matches(aid.language, target.language):
                raise ProjectIndexIntegrityError(
                    source=where,
                    record_id=page_id,
                    relation="revision_of language",
                    target=target_id,
                )
            edges.append(RevisionEdge(page_id, role, target_id))

    edge_keys = {(edge.aid_page_id, edge.source_page_id) for edge in edges}
    assessments: dict[str, dict[str, Any]] = {}
    for page_id, page in pages.items():
        if page.tags.get("destination") not in ELIGIBLE_LESSON_DESTINATIONS:
            if "revision_support" in page.metadata:
                raise ValueError(
                    f"{page.path.as_posix()}.revision_support: "
                    "only Understand/Build lessons may be assessed"
                )
            continue
        raw_support = page.metadata.get("revision_support")
        if raw_support is None:
            assessments[page_id] = {"status": "not_assessed", "evidence": (), "reason": None}
            continue
        where = f"{page.path.as_posix()}.revision_support"
        if not isinstance(raw_support, dict) or set(raw_support) - {"status", "evidence", "reason"}:
            raise ValueError(f"{where}: expected mapping with status, evidence and optional reason")
        status = raw_support.get("status")
        if not isinstance(status, str) or status not in REVISION_SUPPORT_STATUSES:
            raise ValueError(f"{where}.status: unsupported revision support status {status!r}")
        raw_evidence = raw_support.get("evidence", [])
        if not isinstance(raw_evidence, list):
            raise ValueError(f"{where}.evidence: expected a list")
        reason = raw_support.get("reason")
        if reason is not None and (not isinstance(reason, str) or not reason.strip()):
            raise ValueError(f"{where}.reason: expected a non-empty string when present")
        evidence: list[dict[str, str]] = []
        has_aid = False
        has_anchor = False
        for index, item in enumerate(raw_evidence):
            evidence_where = f"{where}.evidence[{index}]"
            if not isinstance(item, dict) or set(item) not in ({"aid", "note"}, {"anchor", "note"}):
                raise ValueError(f"{evidence_where}: expected exactly aid/anchor and note")
            note = item.get("note")
            if not isinstance(note, str) or not note.strip():
                raise ValueError(f"{evidence_where}.note: expected a non-empty string")
            if "anchor" in item:
                anchor = item["anchor"]
                if not isinstance(anchor, str) or not STABLE_ANCHOR.fullmatch(anchor):
                    raise ValueError(f"{evidence_where}.anchor: expected a stable section anchor")
                if not _has_explicit_anchor(page.source, anchor):
                    raise ProjectIndexIntegrityError(
                        source=where,
                        record_id=page_id,
                        relation="revision evidence anchor",
                        target=anchor,
                    )
                has_anchor = True
                evidence.append({"anchor": anchor, "note": note})
            else:
                aid_id = item["aid"]
                if not isinstance(aid_id, str) or not aid_id.strip():
                    raise ValueError(f"{evidence_where}.aid: expected a non-empty aid ID")
                if (
                    aid_id not in pages
                    or pages[aid_id].metadata.get("revision_role") not in REVISION_ROLES
                ):
                    raise ProjectIndexIntegrityError(
                        source=where,
                        record_id=page_id,
                        relation="revision evidence aid",
                        target=aid_id,
                    )
                if (aid_id, page_id) not in edge_keys:
                    raise ProjectIndexIntegrityError(
                        source=where,
                        record_id=page_id,
                        relation="revision evidence aid does not target lesson",
                        target=aid_id,
                    )
                has_aid = True
                evidence.append({"aid": aid_id, "note": note})
        if status == "not_assessed" and (evidence or reason):
            raise ValueError(f"{where}: not_assessed cannot contain evidence or reason")
        if status == "integrated_sufficient" and not has_anchor:
            raise ValueError(f"{where}: integrated_sufficient requires anchor evidence")
        if status == "companion_sufficient" and not has_aid:
            raise ValueError(f"{where}: companion_sufficient requires linked aid evidence")
        if status == "partial" and not (evidence or reason):
            raise ValueError(f"{where}: partial requires evidence or a reason")
        if status in {"missing", "not_applicable"} and not reason:
            raise ValueError(f"{where}.reason: {status} requires a non-empty reason")
        if status in {"missing", "not_applicable"} and evidence:
            raise ValueError(
                f"{where}.evidence: {status} cannot claim revision aids or integrated support"
            )
        assessments[page_id] = {
            "status": status,
            "evidence": tuple(evidence),
            "reason": reason,
        }

    return assessments, tuple(
        sorted(edges, key=lambda edge: (edge.source_page_id, edge.aid_page_id, edge.role))
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
    revision_support_by_page: dict[str, dict[str, Any]]
    revision_edges: tuple[RevisionEdge, ...]
    revision_aids_by_lesson: dict[str, tuple[RevisionEdge, ...]]
    revision_lessons_by_aid: dict[str, tuple[RevisionEdge, ...]]

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
        revision_support_by_page, revision_edges = _load_revision_relations(pages)
        aids_by_lesson: dict[str, list[RevisionEdge]] = defaultdict(list)
        lessons_by_aid: dict[str, list[RevisionEdge]] = defaultdict(list)
        for revision_edge in revision_edges:
            aids_by_lesson[revision_edge.source_page_id].append(revision_edge)
            lessons_by_aid[revision_edge.aid_page_id].append(revision_edge)

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
            revision_support_by_page=revision_support_by_page,
            revision_edges=revision_edges,
            revision_aids_by_lesson={
                key: tuple(sorted(value, key=lambda edge: (edge.aid_page_id, edge.role)))
                for key, value in aids_by_lesson.items()
            },
            revision_lessons_by_aid={
                key: tuple(sorted(value, key=lambda edge: edge.source_page_id))
                for key, value in lessons_by_aid.items()
            },
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
        """Return non-page resources explicitly associated with one published page."""
        if page_id not in self.pages_by_id:
            raise KeyError(f"unknown published page: {page_id}")
        resource_ids = sorted(
            edge.resource_id for edge in self.page_resource_associations if edge.page_id == page_id
        )
        return tuple(self.resources_by_id[key] for key in resource_ids)

    def pages_for_resource(self, resource_id: str) -> tuple[PublishedPage, ...]:
        """Return published pages explicitly referencing one non-page resource."""
        if resource_id not in self.resources_by_id:
            raise KeyError(f"unknown non-page resource: {resource_id}")
        page_ids = sorted(
            edge.page_id
            for edge in self.page_resource_associations
            if edge.resource_id == resource_id
        )
        return tuple(self.pages_by_id[key] for key in page_ids)

    def resources_for_concept(self, concept_id: str) -> tuple[ResourceRecord, ...]:
        """Return non-page resources explicitly associated with one concept."""
        if concept_id not in self.concepts_by_id:
            raise KeyError(f"unknown concept: {concept_id}")
        resource_ids = sorted(
            edge.resource_id
            for edge in self.concept_resource_associations
            if edge.concept_id == concept_id
        )
        return tuple(self.resources_by_id[key] for key in resource_ids)

    def concepts_for_resource(self, resource_id: str) -> tuple[dict[str, Any], ...]:
        """Return concepts explicitly associated with one non-page resource."""
        if resource_id not in self.resources_by_id:
            raise KeyError(f"unknown non-page resource: {resource_id}")
        concept_ids = sorted(
            edge.concept_id
            for edge in self.concept_resource_associations
            if edge.resource_id == resource_id
        )
        return tuple(self.concepts_by_id[key] for key in concept_ids)

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

    def revision_aids_for_lesson(
        self, page_id: str, *, role: str | None = None
    ) -> tuple[RevisionEdge, ...]:
        """Return published revision aids explicitly linked to one lesson."""
        if page_id not in self.pages_by_id:
            raise KeyError(f"unknown published page: {page_id}")
        return tuple(
            edge
            for edge in self.revision_aids_by_lesson.get(page_id, ())
            if role is None or edge.role == role
        )

    def lessons_for_revision_aid(self, aid_page_id: str) -> tuple[PublishedPage, ...]:
        """Return source lessons targeted by one published Quarto revision aid."""
        aid = self.pages_by_id.get(aid_page_id)
        if aid is None or aid.metadata.get("revision_role") not in REVISION_ROLES:
            raise KeyError(f"unknown published revision-aid page: {aid_page_id}")
        return tuple(
            self.pages_by_id[edge.source_page_id]
            for edge in self.revision_lessons_by_aid.get(aid_page_id, ())
        )

    def revision_support_for_lesson(self, page_id: str) -> dict[str, Any]:
        """Return the independent editorial assessment for one Understand/Build lesson."""
        if page_id not in self.pages_by_id:
            raise KeyError(f"unknown published page: {page_id}")
        if page_id not in self.revision_support_by_page:
            raise ValueError(f"page is not an Understand/Build lesson: {page_id}")
        return self.revision_support_by_page[page_id]

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
            "revision_edges": len(self.revision_edges),
            "revision_support_by_status": dict(
                sorted(
                    Counter(
                        item["status"] for item in self.revision_support_by_page.values()
                    ).items()
                )
            ),
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
