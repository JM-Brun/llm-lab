"""Concept-centred coverage matrix over explicit ProjectIndex relations.

The matrix is a read-only projection. It never infers semantic associations and
keeps unregistered or unassessed dimensions distinct from missing evidence.
"""

from __future__ import annotations

from collections import Counter
from pathlib import PurePosixPath
from typing import Any

REGISTRY_VERSION = 1
MATRIX_SCHEMA_VERSION = 1

UNREGISTERED_DIMENSIONS = {
    "build": "No reviewed machine-readable Build milestone/evidence crosswalk exists.",
    "computation": "No canonical concept-to-computational-node bridge exists.",
    "sources": "Source/extraction adapters and a reviewed concept-evidence bridge are pending.",
    "practice": "No complete canonical exercise/test/experiment mapping exists.",
}


def _page_path(page: Any) -> str:
    """Return a stable repository-relative path without leaking the checkout root."""
    parts = PurePosixPath(page.path.as_posix()).parts
    try:
        site_index = parts.index("site")
    except ValueError:
        return page.path.name
    return PurePosixPath(*parts[site_index:]).as_posix()


def _cell(state: str, evidence: list[dict[str, str]], reason: str) -> dict[str, Any]:
    return {"state": state, "evidence": evidence, "reason": reason}


def build_concept_coverage(index: Any) -> dict[str, Any]:
    """Build a deterministic concept-centred matrix from a validated ProjectIndex."""
    rows: list[dict[str, Any]] = []

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
        page_evidence = [
            {
                "id": page.page_id,
                "path": _page_path(page),
                "language": page.language,
            }
            for page in pages
        ]

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

        revision_states = [
            index.revision_support_by_page.get(page_id, {}).get("status", "not_assessed")
            for page_id in page_ids
        ]
        revision_edges = [
            edge for page_id in page_ids for edge in index.revision_aids_for_lesson(page_id)
        ]
        if not page_ids:
            revision_state = "needs_review"
            revision_reason = "No associated teaching page is available for revision assessment."
        elif all(state == "not_applicable" for state in revision_states):
            revision_state = "not_applicable"
            revision_reason = "All associated pages are explicitly outside revision-support scope."
        elif all(state == "not_assessed" for state in revision_states):
            revision_state = "not_assessed"
            revision_reason = (
                "No editorial revision-support assessment is recorded for the associated pages."
            )
        elif all(
            state in {"integrated_sufficient", "companion_sufficient"} for state in revision_states
        ):
            revision_state = "present"
            revision_reason = (
                "All associated teaching pages have sufficient assessed revision support."
            )
        else:
            revision_state = "needs_review"
            revision_reason = (
                "At least one associated page has partial, missing, or "
                "mixed revision-support status."
            )
        revision_evidence = [
            {
                "id": page_id,
                "path": _page_path(index.pages_by_id[page_id]),
                "status": index.revision_support_by_page.get(page_id, {}).get(
                    "status", "not_assessed"
                ),
            }
            for page_id in page_ids
        ]
        revision_evidence.extend(
            {
                "id": f"{edge.aid_page_id}:{edge.role}:{edge.source_page_id}",
                "path": _page_path(index.pages_by_id[edge.aid_page_id]),
                "role": edge.role,
                "target_id": edge.source_page_id,
            }
            for edge in revision_edges
        )
        revision_cell = _cell(revision_state, revision_evidence, revision_reason)

        languages = sorted({page.language for page in pages if page.language in {"fr", "en"}})
        bilingual_cell = _cell(
            "needs_review",
            page_evidence,
            (
                "FR and EN page records both exist, but semantic parity requires editorial review."
                if languages == ["en", "fr"]
                else "Expected bilingual counterparts need an explicit reviewed pairing rule."
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
            "revision_support": revision_cell,
            "bilingual_parity": bilingual_cell,
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
