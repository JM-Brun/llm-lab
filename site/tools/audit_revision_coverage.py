#!/usr/bin/env python3
"""Generate a deterministic inventory of published Understand and Build pages."""

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
        records.append(
            {
                "id": page_id,
                "language": page["language"],
                "destination": destination,
                "topic": page.get("topic"),
                "level": page.get("level"),
                "type": page.get("type"),
                "title": page.get("title"),
                "href": page.get("href"),
                "route_memberships": memberships,
                "route_status": route_status,
                "parents": sorted(page.get("parents", [])),
                "children": sorted(page.get("children", [])),
                "related": sorted(page.get("related", [])),
                "concept_ids": sorted(concept_ids_by_page.get(page_id, [])),
                "implementation_resource_ids": sorted(implementation_ids_by_page.get(page_id, [])),
                "synthesis_status": "not_assessed",
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
            "synthesis_not_assessed": len(subset),
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
            missing_topic_pages.append(
                {"id": record["id"], "destination": record["destination"]}
            )
            continue
        if language in LANGUAGES:
            topic_language_counts[(record["destination"], topic)][language] += 1

    bilingual_parity: dict[str, list[dict[str, Any]]] = {}
    for destination in DESTINATIONS:
        topics = sorted(
            topic for dest, topic in topic_language_counts if dest == destination
        )
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
                    "duplicate_fr": fr_count > 1,
                    "duplicate_en": en_count > 1,
                }
            )

    return {
        "schema_version": 1,
        "source_of_truth": [
            "published Quarto page metadata",
            "data/guided-route.yml",
            "data/concepts.yml",
            "data/resources.yml",
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
    }


def render_markdown(inventory: dict[str, Any]) -> str:
    """Render a compact report while keeping unrouted pages visible."""
    lines = [
        "# Revision coverage inventory",
        "",
        "> Generated projection; do not edit by hand.",
        "> Synthesis status remains unassessed until its editorial contract is explicit.",
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
                "| Language | Page | Topic | Route | Concepts | Implementation resources |",
                "|---|---|---|---|---:|---:|",
            ]
        )
        for page in inventory["pages"]:
            if page["destination"] != destination:
                continue
            lines.append(
                f"| {page['language']} | [{page['title']}]({page['href']}) "
                f"({page['id']}) | {page['topic']} | {page['route_status']} | "
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
            "## Metadata diagnostics",
            "",
            f"- Pages without a non-empty topic: **{len(inventory['missing_topic_pages'])}**",
            f"- Pages with unexpected language values: **{len(inventory['unexpected_languages'])}**",
            "",
            "Pages without a topic are excluded from topic-parity aggregation and listed in the JSON report.",
            "",
            "## Interpretation",
            "",
            "- Topic parity compares page counts only; it does not establish semantic equivalence.",
            "- Duplicate pages within a topic/language are flagged in the JSON report.",
            "- Understand preserves every core/optional stage membership,",
            "  including multiple memberships.",
            "- Understand pages outside the guided route are explicitly marked unrouted.",
            "- Build is inventoried from the published destination tag;",
            "  no linear order is inferred.",
            "- Concept and implementation links come from explicit registry edges.",
            "- not_assessed does not mean a page lacks a synthesis;",
            "  no typed synthesis relation exists yet.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write JSON to this path (default: stdout)")
    parser.add_argument("--markdown", type=Path, help="Also write a Markdown report")
    args = parser.parse_args()
    inventory = build_revision_inventory(
        load_pages(),
        registry_entries(ROOT / "data/concepts.yml", "concepts"),
        registry_entries(ROOT / "data/resources.yml", "resources"),
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
