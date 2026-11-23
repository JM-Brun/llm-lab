#!/usr/bin/env python3
"""Generate a deterministic inventory of Understand/Build pages and revision support."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from build_learning_map import (  # noqa: E402
    build_guided_route_memberships,
    load_guided_route,
    load_pages,
)
from project_index import ProjectIndex  # noqa: E402
from strict_yaml import load_yaml  # noqa: E402

DESTINATIONS = ("understand", "build")
LANGUAGES = ("fr", "en")


def registry_entries(path: Path, key: str) -> list[dict[str, Any]]:
    payload = load_yaml(path)
    entries = payload.get(key, []) if isinstance(payload, dict) else []
    if not isinstance(entries, list):
        raise ValueError(f"{path.relative_to(ROOT)}: expected a {key!r} list")
    return [entry for entry in entries if isinstance(entry, dict)]


def build_revision_inventory(
    pages: list[dict[str, Any]],
    concepts: list[dict[str, Any]],
    resources: list[dict[str, Any]],
    route_memberships: dict[str, list[dict[str, Any]]] | None = None,
    revision_support_by_page: dict[str, dict[str, Any]] | None = None,
    revision_aids_by_lesson: dict[str, list[dict[str, Any]]] | None = None,
    page_edges: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Project all published destination pages and their explicit relations."""
    concept_ids_by_page: dict[str, list[str]] = defaultdict(list)
    for concept in concepts:
        for page_id in concept.get("resources", []):
            if isinstance(page_id, str):
                concept_ids_by_page[page_id].append(str(concept.get("id")))

    implementation_ids_by_page: dict[str, list[str]] = defaultdict(list)
    for resource in resources:
        for page_id in resource.get("referenced_by", []):
            if isinstance(page_id, str):
                implementation_ids_by_page[page_id].append(str(resource.get("id")))

    if revision_support_by_page is None:
        revision_support_by_page = {}
    if revision_aids_by_lesson is None:
        revision_aids_by_lesson = {}
    page_by_id = {page["id"]: page for page in pages}

    if route_memberships is None:
        route_memberships = {}
        for language in LANGUAGES:
            language_pages = [p for p in pages if p["language"] in {language, "shared"}]
            stages = load_guided_route(language, language_pages)
            for page_id, entries in build_guided_route_memberships(stages).items():
                route_memberships[page_id] = [
                    {
                        "stage_id": item.stage_id,
                        "stage_index": item.stage_index,
                        "stage_title": item.stage_title,
                        "role": item.role,
                        "page_index": item.page_index,
                        "page_count": item.page_count,
                    }
                    for item in entries
                ]

    records: list[dict[str, Any]] = []
    for page in pages:
        destination = page.get("destination")
        if destination not in DESTINATIONS:
            continue
        page_id = page["id"]
        memberships = route_memberships.get(page_id, [])
        route_status = "not_applicable"
        if destination == "understand":
            if any(m["role"] == "core" for m in memberships):
                route_status = "core"
            elif memberships:
                route_status = "optional"
            else:
                route_status = "unrouted"
        revision_support = revision_support_by_page.get(
            page_id,
            {"status": "not_assessed", "evidence": [], "reason": None},
        )
        revision_aids: list[dict[str, Any]] = []
        for aid in revision_aids_by_lesson.get(page_id, []):
            aid_id = aid.get("id")
            aid_page = page_by_id.get(aid_id)
            if aid_page is None:
                raise ValueError(
                    f"revision aid {aid_id!r} for lesson {page_id!r} is not a published page"
                )
            revision_aids.append(
                {
                    "id": aid_id,
                    "role": aid.get("role"),
                    "title": aid_page.get("title"),
                    "href": aid_page.get("href"),
                }
            )
        records.append(
            {
                "id": page_id,
                "language": page["language"],
                "destination": destination,
                "topic": page.get("topic"),
                "level": page.get("level"),
                "type": page.get("type"),
                "domain": page.get("domain"),
                "covered_stages": page.get("covered_stages", []),
                "title": page.get("title"),
                "href": page.get("href"),
                "scope": page.get("scope"),
                "purpose": page.get("purpose"),
                "route_memberships": memberships,
                "route_status": route_status,
                "suggested_route": page.get("route", {}),
                "parents": sorted(page.get("parents", [])),
                "children": sorted(page.get("children", [])),
                "related": sorted(page.get("related", [])),
                "concept_ids": sorted(concept_ids_by_page.get(page_id, [])),
                "implementation_resource_ids": sorted(implementation_ids_by_page.get(page_id, [])),
                "revision_support": revision_support,
                "revision_aids": sorted(revision_aids, key=lambda aid: (aid["id"], aid["role"])),
            }
        )
    records.sort(key=lambda item: (item["destination"], item["language"], item["id"]))

    counts: dict[str, Any] = {}
    for destination in DESTINATIONS:
        subset = [p for p in records if p["destination"] == destination]
        counts[destination] = {
            "total": len(subset),
            "by_language": dict(Counter(p["language"] for p in subset)),
            "understand_route": (
                dict(Counter(p["route_status"] for p in subset))
                if destination == "understand"
                else None
            ),
            "revision_support_by_status": dict(
                sorted(Counter(page["revision_support"]["status"] for page in subset).items())
            ),
            "pages_with_revision_aids": sum(bool(page["revision_aids"]) for page in subset),
            "revision_aid_links": sum(len(page["revision_aids"]) for page in subset),
        }

    topic_language_counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    missing_topic_pages: list[dict[str, str]] = []
    unexpected_languages: list[dict[str, str]] = []
    for record in records:
        language = record["language"]
        topic = record["topic"]
        if language not in LANGUAGES:
            unexpected_languages.append({"id": record["id"], "language": str(language)})
        if not isinstance(topic, str) or not topic.strip():
            missing_topic_pages.append({"id": record["id"], "destination": record["destination"]})
            continue
        if language in LANGUAGES:
            topic_language_counts[(record["destination"], topic)][language] += 1

    bilingual_parity: dict[str, list[dict[str, Any]]] = {}
    for destination in DESTINATIONS:
        topics = sorted(topic for dest, topic in topic_language_counts if dest == destination)
        bilingual_parity[destination] = []
        for topic in topics:
            counts_for_topic = topic_language_counts[(destination, topic)]
            fr_count = counts_for_topic["fr"]
            en_count = counts_for_topic["en"]
            bilingual_parity[destination].append(
                {
                    "topic": topic,
                    "fr": fr_count,
                    "en": en_count,
                    "balanced": fr_count == en_count and fr_count > 0,
                    "multiple_fr": fr_count > 1,
                    "multiple_en": en_count > 1,
                }
            )

    affected_page_ids = {record["id"] for record in records}
    affected_page_edges = [
        edge
        for edge in (page_edges or [])
        if edge.get("source") in affected_page_ids or edge.get("target") in affected_page_ids
    ]
    affected_page_edges.sort(
        key=lambda edge: (edge["source"], edge["family"], edge["relation"], edge["target"])
    )

    associated_page_roles: dict[str, set[str]] = defaultdict(set)
    for lesson_page_id, aids in revision_aids_by_lesson.items():
        if lesson_page_id not in affected_page_ids:
            continue
        for aid in aids:
            associated_page_roles[aid["id"]].add(aid["role"])

    associated_page_ids = {
        page_id
        for edge in affected_page_edges
        for page_id in (edge["source"], edge["target"])
        if page_id not in affected_page_ids
    }
    associated_page_ids.update(associated_page_roles)
    associated_page_records: list[dict[str, Any]] = []
    missing_associated_page_ids: list[str] = []
    page_fields = (
        "id",
        "language",
        "destination",
        "topic",
        "level",
        "type",
        "domain",
        "title",
        "href",
        "scope",
        "purpose",
        "covered_stages",
        "route",
        "parents",
        "children",
        "related",
    )
    for page_id in sorted(associated_page_ids):
        page = page_by_id.get(page_id)
        if page is None:
            missing_associated_page_ids.append(page_id)
            continue
        associated_page_records.append(
            {
                **{field: page.get(field) for field in page_fields if field in page},
                "route_memberships": route_memberships.get(page_id, []),
                "concept_ids": sorted(concept_ids_by_page.get(page_id, [])),
                "implementation_resource_ids": sorted(
                    implementation_ids_by_page.get(page_id, [])
                ),
                "revision_roles": sorted(associated_page_roles.get(page_id, set())),
            }
        )

    associated_page_scope = affected_page_ids | {
        page["id"] for page in associated_page_records
    }
    associated_resource_ids = sorted(
        {
            resource_id
            for page_id in associated_page_scope
            for resource_id in implementation_ids_by_page.get(page_id, [])
        }
    )
    resource_by_id = {resource["id"]: resource for resource in resources}
    associated_resources = [
        resource_by_id[resource_id]
        for resource_id in associated_resource_ids
        if resource_id in resource_by_id
    ]
    missing_associated_resource_ids = sorted(
        set(associated_resource_ids) - set(resource_by_id)
    )
    associated_concept_ids = sorted(
        {
            concept_id
            for page_id in associated_page_scope
            for concept_id in concept_ids_by_page.get(page_id, [])
        }
    )

    return {
        "schema_version": 4,
        "source_of_truth": [
            "published Quarto page metadata",
            "data/guided-route.yml",
            "data/concepts.yml",
            "data/resources.yml",
            "LLM-LAB-PAGE-MAP revision_role/revision_of/revision_support",
            "site/tools/project_index.py",
        ],
        "counts": counts,
        "topic_language_counts": {
            f"{destination}:{topic}": dict(sorted(counts.items()))
            for (destination, topic), counts in sorted(topic_language_counts.items())
        },
        "bilingual_parity": bilingual_parity,
        "missing_topic_pages": missing_topic_pages,
        "unexpected_languages": unexpected_languages,
        "pages": records,
        "affected_page_edges": affected_page_edges,
        "associated_page_records": associated_page_records,
        "associated_resources": associated_resources,
        "associated_concept_ids": associated_concept_ids,
        "missing_associated_page_ids": missing_associated_page_ids,
        "missing_associated_resource_ids": missing_associated_resource_ids,
    }


def render_markdown(inventory: dict[str, Any]) -> str:
    """Render a compact report while keeping unrouted pages visible."""
    lines = [
        "# Revision coverage inventory",
        "",
        "> Generated projection; do not edit by hand.",
        (
            "> Revision support status is an explicit editorial assessment; "
            "missing status remains not_assessed."
        ),
        "",
    ]
    for destination in DESTINATIONS:
        summary = inventory["counts"][destination]
        lines.extend(
            [
                f"## {destination.title()}",
                "",
                f"- Published pages: **{summary['total']}**",
                f"- By language: {summary['by_language']}",
            ]
        )
        if destination == "understand":
            lines.append(f"- Guided-route membership: {summary['understand_route']}")
        lines.extend(
            [
                "",
                (
                    "| Language | Page | Topic | Route | Suggested previous / next | "
                    "Revision support | Revision aids | Concepts | Implementation resources |"
                ),
                "|---|---|---|---|---|---|---:|---:|---:|",
            ]
        )
        for page in inventory["pages"]:
            if page["destination"] != destination:
                continue
            lines.append(
                f"| {page['language']} | [{page['title']}]({page['href']}) "
                f"({page['id']}) | {page['topic']} | {page['route_status']} | "
                f"{page['suggested_route'].get('previous') or '—'} / "
                f"{page['suggested_route'].get('next') or '—'} | "
                f"{page['revision_support']['status']} | {len(page['revision_aids'])} | "
                f"{len(page['concept_ids'])} | {len(page['implementation_resource_ids'])} |"
            )
        lines.append("")
        lines.extend(
            [
                "### Bilingual topic parity",
                "",
                "| Topic | FR pages | EN pages | Status |",
                "|---|---:|---:|---|",
            ]
        )
        for item in inventory["bilingual_parity"][destination]:
            status = "balanced" if item["balanced"] else "mismatch"
            lines.append(f"| {item['topic']} | {item['fr']} | {item['en']} | {status} |")
        lines.append("")
    lines.extend(
        [
            "## Page-graph edges incident to Understand/Build pages",
            "",
            "| Source | Family | Relation | Target |",
            "|---|---|---|---|",
        ]
    )
    for edge in inventory["affected_page_edges"]:
        lines.append(
            f"| {edge['source']} | {edge['family']} | {edge['relation']} | {edge['target']} |"
        )
    lines.extend(
        [
            "",
            "## Direct resource closure",
            "",
            f"- Associated page records: **{len(inventory['associated_page_records'])}**",
            f"- Associated non-page resources: **{len(inventory['associated_resources'])}**",
            f"- Associated concept IDs: **{len(inventory['associated_concept_ids'])}**",
            f"- Missing associated page IDs: **{len(inventory['missing_associated_page_ids'])}**",
            f"- Missing associated resource IDs: "
            f"**{len(inventory['missing_associated_resource_ids'])}**",
        ]
    )
    lines.append("")
    lines.extend(
        [
            "## Metadata diagnostics",
            "",
            f"- Pages without a non-empty topic: **{len(inventory['missing_topic_pages'])}**",
            f"- Pages with unexpected language values: "
            f"**{len(inventory['unexpected_languages'])}**",
            "",
            "Pages without a topic are excluded from topic-parity aggregation "
            "and listed in the JSON report.",
            "",
            "## Interpretation",
            "",
            "- Topic parity compares page counts only; it does not establish semantic equivalence.",
            "- Multiple pages within a topic/language are counted explicitly; "
            "this is not a duplicate-page judgment.",
            "- Understand preserves every core/optional stage membership,",
            "  including multiple memberships.",
            "- Understand pages outside the guided route are explicitly marked unrouted.",
            "- Build is inventoried from the published destination tag;",
            "  no linear order is inferred.",
            "- Concept and implementation links come from explicit registry edges.",
            "- JSON inventory preserves all page-graph edges incident to Understand/Build pages,",
            "  including route, hierarchy and related links; revision-aid edges are separate.",
            "- not_assessed means no editorial revision-support assessment is recorded;",
            "  it does not mean a page lacks a synthesis or revision aid.",
            "- Revision-aid links and revision-support assessments are independent:",
            "  a linked aid does not imply sufficient coverage, and integrated support",
            "  is anchored to an explicit section or callout in the source page.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write JSON to this path (default: stdout)")
    parser.add_argument("--markdown", type=Path, help="Also write a Markdown report")
    args = parser.parse_args()
    project_index = ProjectIndex.build(ROOT)
    revision_aids_by_lesson: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in project_index.revision_edges:
        revision_aids_by_lesson[edge.source_page_id].append(
            {"id": edge.aid_page_id, "role": edge.role}
        )
    inventory = build_revision_inventory(
        load_pages(),
        registry_entries(ROOT / "data/concepts.yml", "concepts"),
        registry_entries(ROOT / "data/resources.yml", "resources"),
        revision_support_by_page=project_index.revision_support_by_page,
        revision_aids_by_lesson=revision_aids_by_lesson,
        page_edges=[
            {
                "source": edge.source,
                "target": edge.target,
                "family": edge.family,
                "relation": edge.relation,
            }
            for edge in project_index.page_edges
        ],
    )
    payload = json.dumps(inventory, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(render_markdown(inventory), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
