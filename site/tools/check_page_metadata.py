#!/usr/bin/env python3
"""Validate Quarto page metadata and the bilingual learning graph."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
MARKER = "LLM-LAB-PAGE-MAP v1"
COMMENT = re.compile(r"<!--\s*\nLLM-LAB-PAGE-MAP v1\n(.*?)\n-->", re.DOTALL)
FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
ID_PATTERN = re.compile(r"(?:fr|en)/[a-z0-9]+(?:-[a-z0-9]+)*|reference/references")
TOPIC_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
TAG_TYPES = {
    "entry-point",
    "system-overview",
    "concept-lesson",
    "concept-bridge",
    "guided-build",
    "deep-dive",
    "exercise-hub",
    "experiment-guide",
    "glossary",
    "historical-reference",
    "bibliography",
}
DESTINATIONS = {"orient", "understand", "build", "deepen", "practice", "reference"}
LEVELS = {"overview", "core", "applied", "advanced", "reference"}
LANGUAGES = {"fr", "en", "shared"}
STATUSES = {"published", "planned", "retired"}
LIST_FIELDS = ("parents", "children", "related")
RELATION_FIELDS = ("previous", "next", "parents", "children", "related")


def _page_id_for_path(path: Path, site_dir: Path) -> str | None:
    """Return the stable ID expected for a rendered source path."""
    relative = path.relative_to(site_dir).as_posix()
    if relative == "index.qmd":
        return "fr/index"
    if relative == "references.qmd":
        return "reference/references"
    match = re.fullmatch(r"(fr|en)/([a-z0-9]+(?:-[a-z0-9]+)*)\.qmd", relative)
    return f"{match.group(1)}/{match.group(2)}" if match else None


def _tag_map(tags: Any, where: str, errors: list[str]) -> dict[str, str]:
    """Validate tag syntax and return one value per controlled dimension."""
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        errors.append(f"{where}.tags: expected a list of strings")
        return {}

    dimensions: dict[str, str] = {}
    for tag in tags:
        dimension, separator, value = tag.partition(":")
        if not separator or not value:
            errors.append(f"{where}.tags: malformed tag {tag!r}")
            continue
        if dimension in dimensions:
            errors.append(f"{where}.tags: duplicate dimension {dimension!r}")
        dimensions[dimension] = value

    expected = {"type", "destination", "topic", "level", "language", "status"}
    if set(dimensions) != expected:
        errors.append(
            f"{where}.tags: expected exactly {sorted(expected)}, found {sorted(dimensions)}"
        )
    if dimensions.get("type") not in TAG_TYPES:
        errors.append(f"{where}.tags: unsupported type {dimensions.get('type')!r}")
    if dimensions.get("destination") not in DESTINATIONS:
        errors.append(f"{where}.tags: unsupported destination {dimensions.get('destination')!r}")
    if not TOPIC_PATTERN.fullmatch(dimensions.get("topic", "")):
        errors.append(f"{where}.tags: topic must be a stable kebab-case identifier")
    if dimensions.get("level") not in LEVELS:
        errors.append(f"{where}.tags: unsupported level {dimensions.get('level')!r}")
    if dimensions.get("language") not in LANGUAGES:
        errors.append(f"{where}.tags: unsupported language {dimensions.get('language')!r}")
    if dimensions.get("status") not in STATUSES:
        errors.append(f"{where}.tags: unsupported status {dimensions.get('status')!r}")
    return dimensions


def _load_page(path: Path, site_dir: Path, errors: list[str]) -> dict[str, Any] | None:
    relative = path.relative_to(site_dir).as_posix()
    source = path.read_text(encoding="utf-8")
    front_match = FRONT_MATTER.match(source)
    if front_match is None:
        errors.append(f"{relative}: missing or malformed YAML front matter")
        return None
    try:
        front = yaml.safe_load(front_match.group(1))
    except yaml.YAMLError as exc:
        errors.append(f"{relative}: invalid front matter YAML: {exc}")
        return None
    if not isinstance(front, dict):
        errors.append(f"{relative}: front matter must be a mapping")

    comments = COMMENT.findall(source)
    marker_count = source.count(MARKER)
    metadata_follows_front_matter = (
        re.match(r"\s*<!--\s*\nLLM-LAB-PAGE-MAP v1\n", source[front_match.end() :]) is not None
    )
    if not metadata_follows_front_matter:
        errors.append(f"{relative}: page-map comment must immediately follow front matter")
    if len(comments) != 1 or marker_count != 1:
        errors.append(
            f"{relative}: expected exactly one {MARKER!r} comment, "
            f"found {len(comments)} valid block(s) and {marker_count} marker(s)"
        )
        return None
    try:
        metadata = yaml.safe_load(comments[0])
    except yaml.YAMLError as exc:
        errors.append(f"{relative}: invalid page-map YAML: {exc}")
        return None
    if not isinstance(metadata, dict):
        errors.append(f"{relative}: page-map block must be a YAML mapping")
        return None

    required = {"id", "scope", "purpose", "suggested_route", "hierarchy", "related", "tags"}
    missing = required - set(metadata)
    if missing:
        errors.append(f"{relative}: missing page-map fields {sorted(missing)}")

    page_id = metadata.get("id")
    if not isinstance(page_id, str) or not ID_PATTERN.fullmatch(page_id):
        errors.append(f"{relative}.id: invalid stable page ID {page_id!r}")
    else:
        expected_id = _page_id_for_path(path, site_dir)
        if expected_id is None or page_id != expected_id:
            errors.append(
                f"{relative}.id: expected {expected_id!r} from source path, found {page_id!r}"
            )
    if not isinstance(page_id, str) or not ID_PATTERN.fullmatch(page_id):
        return None

    for field in ("scope", "purpose"):
        if not isinstance(metadata.get(field), str) or not metadata[field].strip():
            errors.append(f"{relative}.{field}: expected a non-empty string")

    route = metadata.get("suggested_route")
    if not isinstance(route, dict):
        errors.append(f"{relative}.suggested_route: expected a mapping")
        route = {}
    for field in ("previous", "next"):
        if field not in route:
            errors.append(f"{relative}.suggested_route.{field}: required field is missing")
    for field in ("previous", "next"):
        target = route.get(field)
        if target is not None and not isinstance(target, str):
            errors.append(f"{relative}.suggested_route.{field}: expected a page ID or null")

    hierarchy = metadata.get("hierarchy")
    if not isinstance(hierarchy, dict):
        errors.append(f"{relative}.hierarchy: expected a mapping")
        hierarchy = {}
    for field in LIST_FIELDS[:2]:
        if field not in hierarchy:
            errors.append(f"{relative}.hierarchy.{field}: required field is missing")
    relations: dict[str, Any] = {
        "previous": route.get("previous"),
        "next": route.get("next"),
        "parents": hierarchy.get("parents"),
        "children": hierarchy.get("children"),
        "related": metadata.get("related"),
    }
    for field in LIST_FIELDS:
        values = relations[field]
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
            errors.append(f"{relative}.{field}: expected a list of page IDs")
            relations[field] = []
        elif len(values) != len(set(values)):
            errors.append(f"{relative}.{field}: duplicate relation targets")
        if page_id in values:
            errors.append(f"{relative}.{field}: a page cannot reference itself")

    tags = _tag_map(metadata.get("tags"), relative, errors)
    keywords = front.get("keywords") if isinstance(front, dict) else None
    if not isinstance(keywords, list) or not all(isinstance(tag, str) for tag in keywords):
        errors.append(f"{relative}.keywords: expected a YAML list of strings")
    elif keywords != metadata.get("tags"):
        errors.append(f"{relative}.keywords: must exactly match page-map tags and ordering")

    language = tags.get("language")
    if page_id == "reference/references":
        if language != "shared":
            errors.append(f"{relative}.tags: shared reference page must use language:shared")
    elif page_id and language != page_id.split("/", maxsplit=1)[0]:
        errors.append(f"{relative}.tags: language tag does not match page ID")

    if tags.get("status") == "planned":
        errors.append(f"{relative}.tags: a page in the Quarto render list cannot be status:planned")

    return {
        "path": relative,
        "id": page_id,
        "route": {"previous": relations["previous"], "next": relations["next"]},
        "parents": relations["parents"],
        "children": relations["children"],
        "related": relations["related"],
        "tags": tags,
    }


def _validate_relations(pages: dict[str, dict[str, Any]], errors: list[str]) -> None:
    """Validate relation targets, reciprocal edges, and hierarchy acyclicity."""
    for page_id, page in pages.items():
        relations = {
            "previous": [page["route"]["previous"]] if page["route"]["previous"] else [],
            "next": [page["route"]["next"]] if page["route"]["next"] else [],
            "parents": page["parents"],
            "children": page["children"],
            "related": page["related"],
        }
        for field, targets in relations.items():
            for target in targets:
                if target not in pages:
                    errors.append(f"{page_id}.{field}: unknown page ID {target!r}")
                elif pages[target]["tags"].get("status") != "published":
                    errors.append(f"{page_id}.{field}: target {target!r} is not published")

        for child in page["children"]:
            if child in pages and page_id not in pages[child]["parents"]:
                errors.append(f"{page_id}.children: {child!r} does not list {page_id!r} as parent")
        for parent in page["parents"]:
            if parent in pages and page_id not in pages[parent]["children"]:
                errors.append(f"{page_id}.parents: {parent!r} does not list {page_id!r} as child")
        if set(page["related"]) & (set(page["parents"]) | set(page["children"])):
            errors.append(f"{page_id}.related: related targets cannot also be parent/child")

        previous = page["route"]["previous"]
        following = page["route"]["next"]
        if previous in pages and pages[previous]["route"]["next"] != page_id:
            errors.append(f"{page_id}.previous: {previous!r} does not point next to this page")
        if following in pages and pages[following]["route"]["previous"] != page_id:
            errors.append(f"{page_id}.next: {following!r} does not point back to this page")

    # Parent -> child edges must form a directed acyclic graph.
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(page_id: str, trail: list[str]) -> None:
        if page_id in visiting:
            cycle = " -> ".join([*trail, page_id])
            errors.append(f"hierarchy: cycle detected: {cycle}")
            return
        if page_id in visited:
            return
        visiting.add(page_id)
        for child in pages[page_id]["children"]:
            if child in pages:
                visit(child, [*trail, page_id])
        visiting.remove(page_id)
        visited.add(page_id)

    for page_id in pages:
        visit(page_id, [])


def _validate_bilingual_parity(pages: dict[str, dict[str, Any]], errors: list[str]) -> None:
    """Compare French and English pages by canonical topic rather than slug."""
    by_topic: dict[str, dict[str, str]] = defaultdict(dict)
    for page_id, page in pages.items():
        tags = page["tags"]
        language = tags.get("language")
        topic = tags.get("topic")
        if language in {"fr", "en"} and topic:
            if language in by_topic[topic]:
                errors.append(f"topic {topic!r}: more than one {language} page")
            by_topic[topic][language] = page_id

    for topic, counterparts in by_topic.items():
        if set(counterparts) != {"fr", "en"}:
            errors.append(f"topic {topic!r}: expected French and English counterparts")
            continue
        fr_id, en_id = counterparts["fr"], counterparts["en"]
        fr, en = pages[fr_id], pages[en_id]
        for dimension in ("type", "destination", "level", "status"):
            if fr["tags"].get(dimension) != en["tags"].get(dimension):
                errors.append(f"topic {topic!r}: FR/EN {dimension} tags differ")

        for field in ("previous", "next"):
            fr_target = fr["route"][field]
            en_target = en["route"][field]
            fr_topic = pages.get(fr_target, {}).get("tags", {}).get("topic") if fr_target else None
            en_topic = pages.get(en_target, {}).get("tags", {}).get("topic") if en_target else None
            if fr_topic != en_topic:
                errors.append(f"topic {topic!r}: FR/EN suggested-route {field} differs")

        for field in ("parents", "children", "related"):
            fr_topics = sorted(
                pages[target]["tags"].get("topic", target)
                for target in fr[field]
                if target in pages
            )
            en_topics = sorted(
                pages[target]["tags"].get("topic", target)
                for target in en[field]
                if target in pages
            )
            if fr_topics != en_topics:
                errors.append(f"topic {topic!r}: FR/EN {field} relations differ")


def validate(site_dir: Path) -> list[str]:
    """Return all page metadata contract violations under a Quarto site directory."""
    config_path = site_dir / "_quarto.yml"
    if not config_path.is_file():
        return [f"Missing Quarto configuration: {config_path}"]
    try:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"Cannot parse {config_path}: {exc}"]
    render_list = config.get("project", {}).get("render") if isinstance(config, dict) else None
    if not isinstance(render_list, list) or not render_list:
        return [f"{config_path.relative_to(ROOT)}: project.render must be a non-empty list"]

    errors: list[str] = []
    pages: dict[str, dict[str, Any]] = {}
    seen_paths: set[str] = set()
    for entry in render_list:
        if not isinstance(entry, str):
            errors.append(f"project.render: expected a source path string, found {entry!r}")
            continue
        if entry in seen_paths:
            errors.append(f"project.render: duplicate source path {entry!r}")
            continue
        seen_paths.add(entry)
        path = site_dir / entry
        if not path.is_file():
            errors.append(f"project.render: missing source file {entry!r}")
            continue
        page = _load_page(path, site_dir, errors)
        if page is None:
            continue
        page_id = page["id"]
        if page_id in pages:
            errors.append(f"{entry}.id: duplicate page ID {page_id!r}")
        else:
            pages[page_id] = page

    _validate_relations(pages, errors)
    _validate_bilingual_parity(pages, errors)
    return errors


def main() -> int:
    site_dir = Path(sys.argv[1]) if len(sys.argv) == 2 else ROOT / "site"
    if len(sys.argv) > 2:
        sys.stderr.write("Usage: check_page_metadata.py [site-directory]\n")
        return 2
    errors = validate(site_dir)
    if errors:
        sys.stderr.write("Page metadata validation failed:\n")
        for error in errors:
            sys.stderr.write(f"- {error}\n")
        return 1
    sys.stdout.write("Page metadata validation passed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
