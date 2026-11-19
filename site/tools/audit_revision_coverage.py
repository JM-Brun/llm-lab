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

from build_learning_map import build_guided_route_memberships, load_guided_route, load_pages
from strict_yaml import load_yaml

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

    route_memberships: dict[str, list[dict[str, Any]]] = {}
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
            route_status = (
                "core" if any(m["role"] == "core" for m in memberships)
                else "optional" if memberships
                else "unrouted"
            )
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
                "implementation_resource_ids": sorted(
                    implementation_ids_by_page.get(page_id, [])
                ),
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
                if destination == "understand" else None
            ),
            "synthesis_not_assessed": len(subset),
        }
    topic_language_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"fr": 0, "en": 0}
    )
    for record in records:
        topic_language_counts[
            f"{record['destination']}:{record['topic']}"
        ][record["language"]] += 1

    return {
        "schema_version": 1,
        "source_of_truth": [
            "published Quarto page metadata",
            "data/guided-route.yml",
            "data/concepts.yml",
            "data/resources.yml",
        ],
        "counts": counts,
        "topic_language_counts": dict(sorted(topic_language_counts.items())),
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
        lines.extend([
            f"## {destination.title()}",
            "",
            f"- Published pages: **{summary['total']}**",
            f"- By language: {summary['by_language']}",
        ])
        if destination == "understand":
            lines.append(f"- Guided-route membership: {summary['understand_route']}")
        lines.extend([
            "",
            "| Language | Page | Topic | Route | Concepts | Implementation resources |",
            "|---|---|---|---|---:|---:|",
        ])
        for page in inventory["pages"]:
            if page["destination"] != destination:
                continue
            lines.append(
                f"| {page['language']} | [{page['title']}]({page['href']}) "
                f"({page['id']}) | {page['topic']} | {page['route_status']} | "
                f"{len(page['concept_ids'])} | {len(page['implementation_resource_ids'])} |"
            )
        lines.append("")
    lines.extend([
        "## Interpretation",
        "",
        "- Understand preserves every core/optional stage membership, including multiple memberships.",
        "- Understand pages outside the guided route are explicitly marked unrouted.",
        "- Build is inventoried from the published destination tag; no linear order is inferred.",
        "- Concept and implementation links come from explicit registry edges.",
        "- not_assessed does not mean a page lacks a synthesis; no typed synthesis relation exists yet.",
        "",
    ])
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
