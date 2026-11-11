"""Read the published Quarto page metadata shared by site projections.

This is an input index, not another registry or a substitute for the full page
metadata validator. Authored page IDs and their source files remain authoritative.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]
from strict_yaml import parse_yaml

_MARKER = "LLM-LAB-PAGE-MAP v1"
_COMMENT = re.compile(r"<!--\s*\nLLM-LAB-PAGE-MAP v1\n(.*?)\n-->", re.DOTALL)
_FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


@dataclass(frozen=True, slots=True)
class PublishedPage:
    """One authored published page and the metadata needed by projections."""

    path: Path
    page_id: str
    language: str
    source: str
    front: dict[str, Any]
    metadata: dict[str, Any]
    tags: dict[str, str]


def load_published_pages(site: Path) -> list[PublishedPage]:
    """Build a deterministic index, failing on ambiguous or malformed page maps."""
    pages: list[PublishedPage] = []
    paths_by_id: dict[str, Path] = {}
    for path in sorted(site.rglob("*.qmd")):
        relative = path.relative_to(site)
        # A restored Quarto output tree can coexist with authored sources while
        # generators run before rendering. Never index rendered/cache artifacts
        # as authored pages: their copied source files would duplicate page IDs.
        if "_site" in relative.parts:
            continue
        source = path.read_text(encoding="utf-8")
        if _COMMENT.search(source) is None:
            # Not a page: generated includes may quote the marker inside data.
            continue
        front_match = _FRONT_MATTER.match(source)
        comments = _COMMENT.findall(source)
        if front_match is None or len(comments) != 1 or source.count(_MARKER) != 1:
            raise ValueError(f"{relative}: expected front matter and exactly one page-map block")
        try:
            front = parse_yaml(front_match.group(1), source=f"{relative} (front matter)")
            metadata = parse_yaml(comments[0], source=f"{relative} (page map)")
        except yaml.YAMLError as exc:
            raise ValueError(f"{relative}: invalid page metadata YAML: {exc}") from exc
        if not isinstance(front, dict) or not isinstance(metadata, dict):
            raise ValueError(f"{relative}: front matter and page metadata must be mappings")
        raw_tags = metadata.get("tags")
        if not isinstance(raw_tags, list) or not all(isinstance(tag, str) for tag in raw_tags):
            raise ValueError(f"{relative}: page-map tags must be a list of strings")
        tags: dict[str, str] = {}
        for tag in raw_tags:
            if ":" not in tag:
                raise ValueError(f"{relative}: invalid page-map tag {tag!r}")
            key, value = tag.split(":", maxsplit=1)
            if key in tags:
                raise ValueError(f"{relative}: duplicate page-map tag {key!r}")
            tags[key] = value
        status = tags.get("status")
        if status not in {"published", "planned", "retired"}:
            raise ValueError(f"{relative}: invalid page status {status!r}")
        if status != "published":
            continue
        page_id, language = metadata.get("id"), tags.get("language")
        if not isinstance(page_id, str) or "/" not in page_id:
            raise ValueError(f"{relative}: invalid page ID {page_id!r}")
        if language not in {"fr", "en", "shared"}:
            raise ValueError(f"{relative}: invalid page language {language!r}")
        if page_id in paths_by_id:
            raise ValueError(
                f"{relative}: duplicate page ID {page_id!r} (also {paths_by_id[page_id]})"
            )
        paths_by_id[page_id] = relative
        pages.append(PublishedPage(path, page_id, language, source, front, metadata, tags))
    return pages
