"""Deterministic, read-only queries over LLM Lab's canonical project metadata.

This module composes existing readers. It is an in-memory projection, not a
new registry or source of truth. Page, concept, and route relations stay distinct.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from page_index import PublishedPage, load_published_pages
from strict_yaml import load_yaml


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
    """In-memory indexes over published pages and canonical concept/route YAML."""

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

    @classmethod
    def build(cls, root: Path) -> "ProjectIndex":
        """Build a deterministic snapshot from the repository root."""
        root = Path(root)
        published = load_published_pages(root / "site")
        pages = {page.page_id: page for page in published}

        concept_data = load_yaml(root / "data" / "concepts.yml")
        domain_data = load_yaml(root / "data" / "domains.yml")
        route_data = load_yaml(root / "data" / "guided-route.yml")
        concepts = {item["id"]: item for item in concept_data["concepts"]}
        domains = {item["id"]: item for item in domain_data["domains"]}

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
                if page_id in pages:
                    concept_to_pages[concept_id].add(page_id)
                    page_to_concepts[page_id].add(concept_id)

        concept_to_domains: dict[str, set[str]] = defaultdict(set)
        for concept_id, concept in concepts.items():
            for domain_id in concept.get("domains", []):
                concept_to_domains[domain_id].add(concept_id)

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
                        membership = RouteMembership(
                            stage["id"], language, role, page_id, position
                        )
                        memberships.append(membership)
                        route_page_lists[(stage["id"], language, role)].append(page_id)

        return cls(
            pages_by_id=pages,
            concepts_by_id=concepts,
            domains_by_id=domains,
            page_edges=tuple(edges),
            route_memberships=tuple(memberships),
            pages_by_tag={key: frozenset(value) for key, value in tag_index.items()},
            pages_by_concept={
                key: frozenset(value) for key, value in concept_to_pages.items()
            },
            concepts_by_page={
                key: frozenset(value) for key, value in page_to_concepts.items()
            },
            pages_by_domain={
                key: frozenset(value) for key, value in page_domain_index.items()
            },
            pages_incoming={
                key: tuple(sorted(value, key=lambda edge: (edge.source, edge.family, edge.relation)))
                for key, value in incoming.items()
            },
            pages_outgoing={
                key: tuple(sorted(value, key=lambda edge: (edge.target, edge.family, edge.relation)))
                for key, value in outgoing.items()
            },
            route_pages={key: tuple(value) for key, value in route_page_lists.items()},
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
        return tuple(self.pages_by_id[key] for key in sorted(self.pages_by_concept.get(concept_id, ())))

    def concepts_for_page(self, page_id: str) -> tuple[dict[str, Any], ...]:
        """Return concepts explicitly associated with a page in concepts.yml."""
        if page_id not in self.pages_by_id:
            raise KeyError(f"unknown published page: {page_id}")
        return tuple(
            self.concepts_by_id[key] for key in sorted(self.concepts_by_page.get(page_id, ()))
        )

    def incoming_pages(
        self, page_id: str, *, family: str | None = None, relation: str | None = None
    ) -> tuple[PageEdge, ...]:
        """Return authored page edges targeting page_id, optionally filtered."""
        if page_id not in self.pages_by_id:
            raise KeyError(f"unknown published page: {page_id}")
        return tuple(
            edge for edge in self.pages_incoming.get(page_id, ())
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
            edge for edge in self.pages_outgoing.get(page_id, ())
            if (family is None or edge.family == family)
            and (relation is None or edge.relation == relation)
        )

    def route_stage(self, stage_id: str, language: str, role: str = "core") -> tuple[PublishedPage, ...]:
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
                    1 for concept in self.concepts_by_id.values()
                    if concept.get("importance") == importance
                )
                for importance in ("core", "supporting", "specialized")
            },
            "concepts_by_domain": {
                domain_id: sum(
                    1 for concept in self.concepts_by_id.values()
                    if domain_id in concept.get("domains", [])
                )
                for domain_id in sorted(self.domains_by_id)
            },
        }
