"""Concept-centred coverage matrix over explicit ProjectIndex relations.

The matrix is a read-only projection. It never infers semantic associations and
keeps unregistered or unassessed dimensions distinct from missing evidence.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import PurePosixPath
from typing import Any

from page_index import PublishedPage, group_bilingual_topics
from project_index import ProjectIndex

REGISTRY_VERSION = 2
MATRIX_SCHEMA_VERSION = 1

UNREGISTERED_DIMENSIONS = {
    "build": "No reviewed machine-readable Build milestone/evidence crosswalk exists.",
    "computation": "No canonical concept-to-computational-node bridge exists.",
    "sources": "Opt-in source adapter exists; complete concept-to-source/item mapping is not registered.",
    "practice": "No complete canonical exercise/test/experiment mapping exists.",
}


def _page_path(page: PublishedPage) -> str:
    """Return a stable repository-relative path without leaking the checkout root."""
    parts = PurePosixPath(page.path.as_posix()).parts
    try:
        site_index = parts.index("site")
    except ValueError:
        return page.path.name
    return PurePosixPath(*parts[site_index:]).as_posix()


def _cell(state: str, evidence: list[dict[str, str]], reason: str) -> dict[str, Any]:
    return {"state": state, "evidence": evidence, "reason": reason}


def _page_evidence(page: PublishedPage) -> dict[str, str]:
    return {"id": page.page_id, "path": _page_path(page), "language": page.language}


def _bilingual_coverage(
    pages_by_id: dict[str, PublishedPage],
    topics: dict[str, dict[str, list[str]]],
    pages: list[PublishedPage],
) -> dict[str, Any]:
    if not pages:
        return _cell("needs_review", [], "No explicit published teaching-page association.")

    linked_by_topic: dict[str, set[str]] = defaultdict(set)
    for page in pages:
        if page.language in {"fr", "en"}:
            linked_by_topic[page.tags.get("topic", "")].add(page.page_id)
    if not linked_by_topic:
        return _cell(
            "not_applicable",
            [dict(_page_evidence(page), association="linked") for page in pages],
            "All associated pages are language-neutral.",
        )

    evidence: list[dict[str, str]] = []
    unresolved = False
    missing = False
    for topic, linked_ids in sorted(linked_by_topic.items()):
        counterparts = topics.get(topic, {})
        unique_pair = set(counterparts) == {"fr", "en"} and all(
            len(ids) == 1 for ids in counterparts.values()
        )
        candidate_ids = {page_id for ids in counterparts.values() for page_id in ids}
        if not unique_pair:
            unresolved = True
        elif candidate_ids - linked_ids:
            missing = True
        for page_id in sorted(linked_ids | candidate_ids):
            association = "linked"
            if page_id not in linked_ids:
                association = "missing_counterpart" if unique_pair else "candidate"
            evidence.append(
                {
                    **_page_evidence(pages_by_id[page_id]),
                    "topic": topic,
                    "pair_status": "resolved" if unique_pair else "unresolved",
                    "association": association,
                }
            )

    if unresolved:
        return _cell("needs_review", evidence, "At least one topic lacks a unique published pair.")
    if missing:
        return _cell("missing", evidence, "At least one published counterpart is not associated.")
    return _cell("present", evidence, "Every associated topic links both published counterparts.")


def _revision_coverage(index: ProjectIndex, page_ids: list[str]) -> dict[str, Any]:
    if not page_ids:
        return _cell("needs_review", [], "No explicit published teaching-page association.")

    statuses: set[str] = set()
    evidence: list[dict[str, str]] = []
    for page_id in page_ids:
        assessment = index.revision_support_by_page.get(page_id)
        if assessment is None:
            continue
        page_path = _page_path(index.pages_by_id[page_id])
        status = assessment["status"]
        if status != "not_applicable":
            statuses.add(status)
        lesson_evidence = {"id": page_id, "path": page_path, "status": status}
        if assessment["reason"] is not None:
            lesson_evidence["reason"] = assessment["reason"]
        evidence.append(lesson_evidence)
        for item in assessment["evidence"]:
            if "anchor" in item:
                anchor = item["anchor"]
                evidence.append({"id": f"{page_id}#{anchor}", "path": f"{page_path}#{anchor}"})
        for edge in index.revision_aids_for_lesson(page_id):
            evidence.append(
                {
                    "id": f"{edge.aid_page_id}:{edge.role}:{edge.source_page_id}",
                    "path": _page_path(index.pages_by_id[edge.aid_page_id]),
                    "role": edge.role,
                    "target_id": edge.source_page_id,
                }
            )

    if not statuses:
        return _cell("not_applicable", evidence, "No associated lesson is in revision scope.")
    if statuses == {"not_assessed"}:
        return _cell("not_assessed", evidence, "Every in-scope lesson awaits assessment.")
    if statuses <= {"integrated_sufficient", "companion_sufficient"}:
        return _cell("present", evidence, "Every in-scope lesson has sufficient revision support.")
    if statuses == {"missing"}:
        return _cell("missing", evidence, "Every in-scope lesson was assessed as missing support.")
    return _cell("needs_review", evidence, "In-scope assessments are partial or have mixed states.")


def build_concept_coverage(index: ProjectIndex) -> dict[str, Any]:
    """Build a deterministic concept-centred matrix from a validated ProjectIndex."""
    rows: list[dict[str, Any]] = []
    bilingual_topics = group_bilingual_topics(
        {page_id: page.tags for page_id, page in index.pages_by_id.items()}
    )

    memberships_by_page: dict[str, list[Any]] = {}
    resource_ids_by_concept: dict[str, set[str]] = {}
    for association in index.concept_resource_associations:
        resource_ids_by_concept.setdefault(association.concept_id, set()).add(
            association.resource_id
        )
    for membership in index.route_memberships:
        memberships_by_page.setdefault(membership.page_id, []).append(membership)

    for concept_id in sorted(index.concepts_by_id):
        concept = index.concepts_by_id[concept_id]
        page_ids = sorted(index.pages_by_concept.get(concept_id, ()))
        pages = [index.pages_by_id[page_id] for page_id in page_ids]
        page_evidence = [_page_evidence(page) for page in pages]

        labels = concept.get("labels", {})
        definitions = concept.get("definitions", {})
        has_bilingual_definition = all(
            isinstance(values, dict)
            and isinstance(values.get(language), str)
            and bool(values[language].strip())
            for values in (labels, definitions)
            for language in ("fr", "en")
        )
        definition_cell = _cell(
            "present" if has_bilingual_definition else "needs_review",
            [{"id": concept_id, "path": f"data/concepts.yml#{concept_id}"}],
            (
                "Canonical FR/EN labels and definitions are present."
                if has_bilingual_definition
                else "Canonical bilingual labels or definitions need review."
            ),
        )

        teaching_cell = _cell(
            "present" if page_evidence else "needs_review",
            page_evidence,
            (
                "Explicit concept-to-page associations resolve to published pages."
                if page_evidence
                else "No explicit published teaching page; eligibility is not defined."
            ),
        )

        route_evidence: list[dict[str, str]] = []
        for page in pages:
            for membership in memberships_by_page.get(page.page_id, []):
                route_evidence.append(
                    {
                        "id": f"{membership.stage_id}:{membership.role}:{membership.page_id}",
                        "page_id": membership.page_id,
                        "stage_id": membership.stage_id,
                        "role": membership.role,
                        "path": "data/guided-route.yml",
                    }
                )
        route_evidence.sort(key=lambda item: (item["stage_id"], item["role"], item["page_id"]))
        understand_cell = _cell(
            "present" if route_evidence else "needs_review",
            route_evidence,
            (
                "At least one associated teaching page has explicit Understand-route membership."
                if route_evidence
                else "No associated page has route membership; this is not automatically a defect."
            ),
        )

        resource_ids = sorted(resource_ids_by_concept.get(concept_id, ()))
        resource_evidence = [
            {"id": resource_id, "path": f"data/resources.yml#{resource_id}"}
            for resource_id in resource_ids
        ]
        resources_cell = _cell(
            "present" if resource_evidence else "needs_review",
            resource_evidence,
            (
                "Explicit first-class non-page resource associations exist."
                if resource_evidence
                else "No non-page resource association; no universal requirement is assumed."
            ),
        )

        dimensions = {
            "definition": definition_cell,
            "teaching_pages": teaching_cell,
            "understand": understand_cell,
            "build": _cell(
                "not_registered",
                [],
                UNREGISTERED_DIMENSIONS["build"],
            ),
            "computation": _cell(
                "not_registered",
                [],
                UNREGISTERED_DIMENSIONS["computation"],
            ),
            "resources": resources_cell,
            "sources": _cell(
                "not_registered",
                [],
                UNREGISTERED_DIMENSIONS["sources"],
            ),
            "practice": _cell(
                "not_registered",
                [],
                UNREGISTERED_DIMENSIONS["practice"],
            ),
            "revision_support": _revision_coverage(index, page_ids),
            "bilingual_parity": _bilingual_coverage(index.pages_by_id, bilingual_topics, pages),
        }
        rows.append(
            {
                "concept_id": concept_id,
                "importance": concept.get("importance"),
                "domain_ids": sorted(concept.get("domains", [])),
                "dimensions": dimensions,
            }
        )

    state_counts: dict[str, dict[str, int]] = {}
    dimension_ids = tuple(rows[0]["dimensions"]) if rows else ()
    for dimension_id in dimension_ids:
        counts = Counter(row["dimensions"][dimension_id]["state"] for row in rows)
        state_counts[dimension_id] = dict(sorted(counts.items()))

    return {
        "schema_version": MATRIX_SCHEMA_VERSION,
        "registry_version": REGISTRY_VERSION,
        "unit": "canonical concept ID",
        "row_count": len(rows),
        "state_counts": state_counts,
        "rows": rows,
    }


def bilingual_association_findings(coverage: dict[str, Any]) -> list[dict[str, Any]]:
    """Flag unlinked published counterparts only where the declared pairing is unique."""
    findings = []
    for row in coverage["rows"]:
        for page in row["dimensions"]["bilingual_parity"]["evidence"]:
            if page.get("association") != "missing_counterpart":
                continue
            findings.append(
                {
                    "rule_id": "missing-bilingual-concept-association",
                    "severity": "review",
                    "source_path": "data/concepts.yml",
                    "entity_ids": {"concept": row["concept_id"], "page": page["id"]},
                    "evidence": page,
                    "suggested_review_action": (
                        "Check whether the published counterpart teaches the same concept "
                        "before changing its explicit resource links."
                    ),
                }
            )
    return findings
