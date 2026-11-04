#!/usr/bin/env python3
"""Build bilingual, reader-facing learning-map data from Quarto page metadata."""

from __future__ import annotations

import json
import re
import sys
from collections import deque
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
COMMENT = re.compile(r"<!--\s*\nLLM-LAB-PAGE-MAP v1\n(.*?)\n-->", re.DOTALL)
FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
HEADING = re.compile(r"^#{2,3}\s+(.+?)\s*#*\s*$", re.MULTILINE)
INLINE_MARKUP = re.compile(r"[*_]|<[^>]+>")
EXCLUDED_HEADINGS = {
    "objectifs d'apprentissage",
    "learning objectives",
    "à retenir",
    "a retenir",
    "takeaways",
    "références",
    "references",
    "pour aller plus loin",
    "further reading",
}
COLUMN_ORDER = {
    "orient": 0,
    "understand": 0,
    "build": 1,
    "deepen": 2,
    "practice": 3,
    "reference": 3,
}


def page_href(page_id: str, language: str) -> str:
    """Return a path relative to a language-specific learning-map page."""
    if page_id == f"{language}/index":
        return "../index.html"
    if page_id == "reference/references":
        return "../references.html"
    prefix, slug = page_id.split("/", maxsplit=1)
    return f"{slug}.html" if prefix == language else f"../{slug}.html"


def clean_heading(value: str) -> str:
    """Remove lightweight Markdown markup from a section heading."""
    return re.sub(r"\s+", " ", INLINE_MARKUP.sub("", value)).strip(" :-")


def load_pages() -> list[dict[str, Any]]:
    """Read published page maps and extract editorial section headings."""
    pages: list[dict[str, Any]] = []
    for path in sorted(SITE.rglob("*.qmd")):
        source = path.read_text(encoding="utf-8")
        front_match = FRONT_MATTER.match(source)
        comments = COMMENT.findall(source)
        if front_match is None or len(comments) != 1:
            continue
        front = yaml.safe_load(front_match.group(1))
        metadata = yaml.safe_load(comments[0])
        if not isinstance(front, dict) or not isinstance(metadata, dict):
            continue
        tags = {
            key: value
            for tag in metadata.get("tags", [])
            if isinstance(tag, str) and ":" in tag
            for key, value in [tag.split(":", maxsplit=1)]
        }
        language = tags.get("language")
        if tags.get("status") != "published" or language not in {"fr", "en", "shared"}:
            continue
        page_id = metadata.get("id")
        if not isinstance(page_id, str) or page_id.endswith("/learning-map"):
            continue
        if language not in {"fr", "en"} and page_id != "reference/references":
            continue

        section_headings: list[str] = []
        for heading in HEADING.findall(source):
            heading_text = clean_heading(heading)
            if (
                heading_text
                and heading_text.casefold() not in EXCLUDED_HEADINGS
                and heading_text not in section_headings
            ):
                section_headings.append(heading_text)
            if len(section_headings) == 6:
                break

        title = str(front.get("title", page_id.rsplit("/", maxsplit=1)[-1]))
        pages.append(
            {
                "id": page_id,
                "title": title,
                "href": page_href(page_id, "fr" if language == "shared" else language),
                "language": language,
                "destination": tags.get("destination", "reference"),
                "level": tags.get("level", "reference"),
                "type": tags.get("type", "concept-lesson"),
                "topic": tags.get("topic", "misc"),
                "domain": metadata.get("domain"),
                "scope": str(metadata.get("scope", "")),
                "purpose": str(metadata.get("purpose", "")),
                "section_headings": section_headings,
                "route": metadata.get("suggested_route", {}),
                "parents": metadata.get("hierarchy", {}).get("parents", []),
                "children": metadata.get("hierarchy", {}).get("children", []),
                "related": metadata.get("related", []),
            }
        )
    return pages


def load_concept_graph(
    language: str, pages: list[dict[str, Any]]
) -> dict[str, list[dict[str, Any]]]:
    """Load the reviewed concept registry and resolve language-specific page links."""
    registry_path = ROOT / "data" / "concepts.yml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    page_by_id = {page["id"]: page for page in pages}
    concepts = []
    concept_ids = set()
    for item in registry["concepts"]:
        resources = []
        for page_id in item["resources"]:
            page = page_by_id.get(page_id)
            if page is not None:
                resources.append({"id": page_id, "title": page["title"], "href": page["href"]})
        concepts.append(
            {
                "id": item["id"],
                "label": item["labels"][language],
                "definition": item["definitions"][language],
                "resources": resources,
            }
        )
        concept_ids.add(item["id"])
    relations = [
        {"from": edge["from"], "type": edge["type"], "to": edge["to"]}
        for edge in registry["relations"]
        if edge["from"] in concept_ids and edge["to"] in concept_ids
    ]
    return {"concepts": concepts, "concept_relations": relations}


def assign_route_rank(pages: list[dict[str, Any]], language: str) -> None:
    """Rank pages by a breadth-first walk of the suggested route and hierarchy."""
    by_id = {page["id"]: page for page in pages}
    queue = deque([f"{language}/index"])
    seen: set[str] = set()
    rank = 0
    while queue:
        page_id = queue.popleft()
        if page_id in seen or page_id not in by_id:
            continue
        seen.add(page_id)
        by_id[page_id]["rank"] = rank
        rank += 1
        page = by_id[page_id]
        next_page = page.get("route", {}).get("next")
        if isinstance(next_page, str):
            queue.append(next_page)
        queue.extend(page.get("children", []))
    for page in pages:
        if page["id"] not in seen:
            page["rank"] = rank
            rank += 1


def build(language: str) -> Path:
    """Write the published page graph for one language."""
    all_pages = load_pages()
    pages = [
        page for page in all_pages if page["language"] == language or page["language"] == "shared"
    ]
    assign_route_rank(pages, language)
    pages.sort(
        key=lambda page: (
            COLUMN_ORDER.get(page["destination"], 3),
            page["rank"],
            page["title"].casefold(),
        )
    )
    output = SITE / f"learning-map-data-{language}.json"
    concept_graph = load_concept_graph(language, pages)
    output.write_text(
        json.dumps(
            {
                "language": language,
                "source": "LLM-LAB-PAGE-MAP v1 + data/concepts.yml",
                "pages": pages,
                **concept_graph,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return output


def main() -> None:
    """Generate bilingual learning maps and the linked-data export."""
    for language in ("fr", "en"):
        output = build(language)
        sys.stdout.write(f"Generated {output.relative_to(ROOT)}\n")
    from export_knowledge_graph import write_export

    export = write_export(SITE / "knowledge-graph.jsonld")
    sys.stdout.write(f"Generated {export.relative_to(ROOT)}\n")


if __name__ == "__main__":
    main()
