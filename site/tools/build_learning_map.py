#!/usr/bin/env python3
"""Build bilingual, reader-facing learning-map data from Quarto page metadata.

The generated page rank is a deterministic display-order heuristic only. It
combines suggested-route and hierarchy edges to arrange the exploratory graph;
it is not a curriculum sequence or a prerequisite/topological ordering.

Structure (pages, navigation areas, concepts) is derived from authored sources;
presentation artifacts are rendered by ``learning_map_renderers`` and written
next to the JSON payloads, so the two layers evolve independently.
"""

from __future__ import annotations

import json
import posixpath
import re
import sys
import unicodedata
from collections import deque
from collections.abc import Sequence
from html import escape
from pathlib import Path
from typing import Any, Literal

from artifact_writer import write_artifacts
from guided_route_transitions import GuidedRouteTransition, validate_guided_route_transitions
from learning_map_renderers import (
    REPRESENTATIONS,
    escape_markdown_text,
    render_inline_map_data,
    render_map_script,
)
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from strict_yaml import load_yaml

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
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


class StrictModel(BaseModel):
    """Base model for repository-authored, strictly typed metadata."""

    model_config = ConfigDict(extra="forbid", strict=True)


class LocalizedCopy(StrictModel):
    """Required French and English copy for a guided-route field."""

    fr: str = Field(min_length=1)
    en: str = Field(min_length=1)

    @field_validator("fr", "en")
    @classmethod
    def reject_blank_copy(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("localized copy must not be blank")
        return value


class LocalizedPageIds(StrictModel):
    """Non-empty, language-specific list of core page identifiers."""

    fr: list[str] = Field(min_length=1)
    en: list[str] = Field(min_length=1)

    @field_validator("fr", "en")
    @classmethod
    def validate_page_ids(cls, value: list[str]) -> list[str]:
        if any(not page_id.strip() for page_id in value):
            raise ValueError("page identifiers must not be blank")
        if len(value) != len(set(value)):
            raise ValueError("page identifiers must be unique within a language")
        return value


class OptionalLocalizedPageIds(StrictModel):
    """Optional, language-specific deep-dive page identifiers."""

    fr: list[str] = Field(default_factory=list)
    en: list[str] = Field(default_factory=list)

    @field_validator("fr", "en")
    @classmethod
    def validate_page_ids(cls, value: list[str]) -> list[str]:
        if any(not page_id.strip() for page_id in value):
            raise ValueError("page identifiers must not be blank")
        if len(value) != len(set(value)):
            raise ValueError("page identifiers must be unique within a language")
        return value


class GuidedRouteStage(StrictModel):
    """One conceptual stage with bilingual copy and page references."""

    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    title: LocalizedCopy
    objective: LocalizedCopy
    pages: LocalizedPageIds
    optional_pages: OptionalLocalizedPageIds = Field(default_factory=OptionalLocalizedPageIds)

    @model_validator(mode="after")
    def core_and_optional_pages_are_disjoint(self) -> GuidedRouteStage:
        for language in ("fr", "en"):
            overlap = set(getattr(self.pages, language)) & set(
                getattr(self.optional_pages, language)
            )
            if overlap:
                raise ValueError(f"{language} core and optional pages overlap: {sorted(overlap)}")
        return self


class GuidedRouteDocument(StrictModel):
    """Versioned source document for the reader-facing conceptual route."""

    schema_version: Literal[1]
    stages: list[GuidedRouteStage] = Field(min_length=1)
    # Detailed transition validation lives in guided_route_transitions.py so
    # this document accepts the canonical top-level field while keeping the
    # stage model and its membership projection independent.
    transitions: list[GuidedRouteTransition] = Field(default_factory=list)

    @model_validator(mode="after")
    def stage_ids_are_unique(self) -> GuidedRouteDocument:
        ids = [stage.id for stage in self.stages]
        if len(ids) != len(set(ids)):
            raise ValueError("guided-route stage identifiers must be unique")
        return self


class ResolvedPage(StrictModel):
    """Published page link resolved from the canonical page metadata."""

    id: str
    title: str
    href: str


class ResolvedGuidedRouteStage(StrictModel):
    """A validated stage ready for rendering into Quarto Markdown."""

    id: str
    title: str
    objective: str
    pages: list[ResolvedPage]
    optional_pages: list[ResolvedPage] = Field(default_factory=list)


class ResolvedGuidedRouteTransition(StrictModel):
    """A localized transition resolved to reader-facing stage and page data."""

    id: str
    from_stage_id: str
    from_stage_title: str
    to_stage_id: str
    to_stage_title: str
    direction: Literal["directed", "symmetric"]
    purpose: str
    pages: list[ResolvedPage]


def page_href(page_id: str, language: str, source_path: Path | None = None) -> str:
    """Return the actual rendered path relative to a language-specific map page."""
    if source_path is not None:
        output_path = source_path.relative_to(SITE).with_suffix(".html").as_posix()
        return posixpath.relpath(output_path, start=language)
    if page_id == f"{language}/index":
        # The French landing page is the site root; the English landing page
        # lives in site/en/, the same directory as the pages linking to it.
        return "index.html" if language == "en" else "../index.html"
    if page_id == "reference/references":
        return "../references.html"
    prefix, slug = page_id.split("/", maxsplit=1)
    return f"{slug}.html" if prefix == language else f"../{slug}.html"


def clean_heading(value: str) -> str:
    """Remove lightweight Markdown markup from a section heading."""
    return re.sub(r"\s+", " ", INLINE_MARKUP.sub("", value)).strip(" :-")


def load_pages() -> list[dict[str, Any]]:
    """Project the shared published-page index into learning-map records."""
    from page_index import load_published_pages

    config_path = SITE / "_quarto.yml"
    rendered_sources: set[str] | None = None
    if config_path.is_file():
        config = load_yaml(config_path) or {}
        project = config.get("project") or {}
        render_entries = project.get("render") if isinstance(project, dict) else None
        if render_entries is not None:
            if not isinstance(render_entries, list) or not all(
                isinstance(entry, str) for entry in render_entries
            ):
                raise ValueError(
                    "site/_quarto.yml project.render must be an explicit list of paths"
                )
            rendered_sources = set(render_entries)

    pages: list[dict[str, Any]] = []
    for page in load_published_pages(SITE):
        source_path = page.path.relative_to(SITE).as_posix()
        # A page can be authored and marked published without being part of
        # Quarto's explicit build. Never advertise a destination the site won't emit.
        if rendered_sources is not None and source_path not in rendered_sources:
            continue
        page_id, language = page.page_id, page.language
        if page_id.endswith("/learning-map"):
            continue
        if language == "shared" and page_id != "reference/references":
            continue
        source, front, metadata, tags = page.source, page.front, page.metadata, page.tags

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
                "href": page_href(page_id, "fr" if language == "shared" else language, page.path),
                "language": language,
                "destination": tags.get("destination", "reference"),
                "level": tags.get("level", "reference"),
                "type": tags.get("type", "concept-lesson"),
                "topic": tags.get("topic", "misc"),
                "domain": metadata.get("domain"),
                "scope": str(metadata.get("scope", "")),
                "summary": str(metadata.get("summary", "")),
                "purpose": str(metadata.get("purpose", "")),
                "section_headings": section_headings,
                "route": metadata.get("suggested_route", {}),
                "parents": metadata.get("hierarchy", {}).get("parents", []),
                "children": metadata.get("hierarchy", {}).get("children", []),
                "related": metadata.get("related", []),
            }
        )
    return pages


def slugify_area_id(title: str) -> str:
    """Return an ASCII slug used as a stable, language-scoped area identifier."""
    folded = unicodedata.normalize("NFKD", title).encode("ascii", "ignore")
    return re.sub(r"[^a-z0-9]+", "-", folded.decode("ascii").lower()).strip("-")


def sidebar_page_id(entry: object, language: str) -> str | None:
    """Resolve one Quarto sidebar entry to a published page identifier.

    An entry is either a page path or a ``{text, href}`` item whose ``text``
    relabels the page in the sidebar and breadcrumbs without changing its id.
    """
    if isinstance(entry, dict) and "section" not in entry:
        entry = entry.get("href")
    if not isinstance(entry, str) or not entry.endswith(".qmd"):
        return None
    slug = entry.removesuffix(".qmd")
    if "/" not in slug:
        if slug == "references":
            return "reference/references"
        return f"{language}/{slug}"
    return slug


def load_sidebar_page_neighbors(language: str) -> dict[str, dict[str, str]]:
    """Return native Quarto previous/next page IDs in sidebar reading order.

    This is deliberately separate from the suggested pedagogical route: the
    two sequences can differ, and only identical destinations are redundant.
    """
    if language not in {"fr", "en"}:
        raise ValueError(f"unsupported sidebar language: {language!r}")
    config_path = SITE / "_quarto.yml"
    if not config_path.is_file():
        return {}
    config = load_yaml(config_path)
    sidebars = (config or {}).get("website", {}).get("sidebar", [])
    sidebar = next((entry for entry in sidebars if entry.get("id") == language), None)
    if sidebar is None:
        raise ValueError(f"missing Quarto sidebar for language: {language!r}")

    ordered: list[str] = []

    def visit(entries: list[object]) -> None:
        for entry in entries:
            if isinstance(entry, dict) and "section" in entry:
                href = entry.get("href")
                page_id = sidebar_page_id(href, language)
                if page_id is not None:
                    ordered.append(page_id)
                visit(entry.get("contents", []))
            else:
                page_id = sidebar_page_id(entry, language)
                if page_id is not None:
                    ordered.append(page_id)

    visit(sidebar.get("contents", []))
    # A linked section can also be listed by its parent. Keep its first
    # occurrence, matching the resource-map projection's no-duplicate rule.
    ordered = list(dict.fromkeys(ordered))
    return {
        page_id: {
            direction: ordered[index + offset]
            for direction, offset in (("previous", -1), ("next", 1))
            if 0 <= index + offset < len(ordered)
        }
        for index, page_id in enumerate(ordered)
    }


def load_navigation(language: str, pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Derive the drill-down area structure recursively from the Quarto sidebar.

    The sidebar is the only authored source of reader-facing grouping. Nested
    sections are preserved so the learning map and its static fallback reflect
    the same hierarchy as the native Quarto navigation.
    """
    config = load_yaml(SITE / "_quarto.yml")
    sidebars = (config or {}).get("website", {}).get("sidebar", [])
    sidebar = next((entry for entry in sidebars if entry.get("id") == language), None)
    if sidebar is None:
        raise ValueError(f"missing Quarto sidebar for language: {language!r}")
    published = {page["id"] for page in pages}

    def collect(entries: list[object]) -> list[str]:
        """Keep only sidebar entries that resolve to published page identifiers."""
        identifiers = (sidebar_page_id(entry, language) for entry in entries)
        return [value for value in identifiers if value in published]

    def collect_section(entry: dict[str, Any]) -> dict[str, Any] | None:
        """Preserve one sidebar section and all of its nested sections."""
        contents = entry.get("contents", [])
        # A linked Quarto section has its own canonical entry page in addition
        # to its expandable child lessons. Include that page in the resource-map
        # projection exactly once, before the remaining section contents.
        page_entries = [entry.get("href"), *contents] if entry.get("href") else contents
        pages_in_section = collect(page_entries)
        nested = [
            section
            for item in contents
            if isinstance(item, dict) and "section" in item
            if (section := collect_section(item)) is not None
        ]
        if not pages_in_section and not nested:
            return None
        section: dict[str, Any] = {
            "title": str(entry["section"]),
            "pages": pages_in_section,
        }
        if nested:
            section["sections"] = nested
        return section

    areas: list[dict[str, Any]] = []
    for entry in sidebar.get("contents", []):
        if not isinstance(entry, dict) or "section" not in entry:
            continue
        contents = entry.get("contents", [])
        sections = [
            section
            for item in contents
            if isinstance(item, dict) and "section" in item
            if (section := collect_section(item)) is not None
        ]
        area_pages = collect(contents)
        if not area_pages and not sections:
            continue
        areas.append(
            {
                "id": slugify_area_id(str(entry["section"])),
                "title": str(entry["section"]),
                "pages": area_pages,
                "sections": sections,
            }
        )
    return areas


def load_guided_route(language: str, pages: list[dict[str, Any]]) -> list[ResolvedGuidedRouteStage]:
    """Validate the route source and resolve every reference to a published page."""
    if language not in {"fr", "en"}:
        raise ValueError(f"unsupported guided-route language: {language!r}")

    source_path = ROOT / "data" / "guided-route.yml"
    payload = load_yaml(source_path)
    document = GuidedRouteDocument.model_validate(payload)
    # Validate bilingual transitions against the complete published-page index.
    # This is intentionally separate from membership projection and does not
    # alter core/optional roles or infer prerequisite edges.
    validate_guided_route_transitions(payload, {page["id"] for page in load_pages()})
    page_by_id = {page["id"]: page for page in pages}
    resolved: list[ResolvedGuidedRouteStage] = []

    def resolve_pages(page_ids: list[str], stage_id: str, role: str) -> list[ResolvedPage]:
        resources: list[ResolvedPage] = []
        for page_id in page_ids:
            page = page_by_id.get(page_id)
            if page is None:
                raise ValueError(
                    f"guided-route stage {stage_id!r} references unpublished or "
                    f"missing {role} page {page_id!r}"
                )
            resources.append(ResolvedPage(id=page_id, title=page["title"], href=page["href"]))
        return resources

    for stage in document.stages:
        resolved.append(
            ResolvedGuidedRouteStage(
                id=stage.id,
                title=getattr(stage.title, language),
                objective=getattr(stage.objective, language),
                pages=resolve_pages(getattr(stage.pages, language), stage.id, "core"),
                optional_pages=resolve_pages(
                    getattr(stage.optional_pages, language), stage.id, "optional"
                ),
            )
        )
    return resolved


def load_guided_route_transitions(
    language: str, pages: list[dict[str, Any]]
) -> list[ResolvedGuidedRouteTransition]:
    """Resolve canonical transitions without changing stage membership."""
    if language not in {"fr", "en"}:
        raise ValueError(f"unsupported guided-route language: {language!r}")
    payload = load_yaml(ROOT / "data" / "guided-route.yml")
    published = {page["id"] for page in load_pages()}
    transitions = validate_guided_route_transitions(payload, published)
    stages = {stage.id: stage for stage in GuidedRouteDocument.model_validate(payload).stages}
    page_by_id = {page["id"]: page for page in pages}
    resolved = []
    for transition in transitions:
        page_refs = getattr(transition.pages, language)
        missing = [page_id for page_id in page_refs if page_id not in page_by_id]
        if missing:
            raise ValueError(
                f"transition {transition.id!r} references pages unavailable in "
                f"the {language} projection: {missing}"
            )
        source = stages[transition.from_stage]
        target = stages[transition.to_stage]
        resolved.append(
            ResolvedGuidedRouteTransition(
                id=transition.id,
                from_stage_id=source.id,
                from_stage_title=getattr(source.title, language),
                to_stage_id=target.id,
                to_stage_title=getattr(target.title, language),
                direction=transition.direction,
                purpose=getattr(transition.purpose, language),
                pages=[
                    ResolvedPage(
                        id=page_id,
                        title=page_by_id[page_id]["title"],
                        href=page_by_id[page_id]["href"],
                    )
                    for page_id in page_refs
                ],
            )
        )
    return resolved


class GuidedRouteMembership(StrictModel):
    """One page's explicit membership in a guided-route stage."""

    stage_id: str
    stage_index: int
    stage_title: str
    stage_objective: str
    role: Literal["core", "optional"]
    # Position data is optional so that a membership can be built without the
    # whole route; the page context omits what it does not know.
    stage_count: int | None = None
    page_index: int | None = None
    page_count: int | None = None


def build_guided_route_memberships(
    stages: list[ResolvedGuidedRouteStage],
) -> dict[str, list[GuidedRouteMembership]]:
    """Index every route membership without inventing a unique parent.

    A page can occur in several stages and can be core in one context while
    optional in another. Preserve stage order and membership role exactly as
    authored in the canonical route registry.
    """
    memberships: dict[str, list[GuidedRouteMembership]] = {}
    for stage_index, stage in enumerate(stages, start=1):
        for page_index, page in enumerate(stage.pages, start=1):
            memberships.setdefault(page.id, []).append(
                GuidedRouteMembership(
                    stage_id=stage.id,
                    stage_index=stage_index,
                    stage_title=stage.title,
                    stage_objective=stage.objective,
                    role="core",
                    stage_count=len(stages),
                    page_index=page_index,
                    page_count=len(stage.pages),
                )
            )
        for page in stage.optional_pages:
            memberships.setdefault(page.id, []).append(
                GuidedRouteMembership(
                    stage_id=stage.id,
                    stage_index=stage_index,
                    stage_title=stage.title,
                    stage_objective=stage.objective,
                    role="optional",
                    stage_count=len(stages),
                )
            )
    return memberships


def render_stage_badge(membership: GuidedRouteMembership, language: str) -> str:
    """Render the localized stage counter and stable hooks for future local progress."""
    if membership.stage_count is None:
        return ""
    label = "Étape" if language == "fr" else "Stage"
    return (
        f'<span class="guided-page-context__badge" '
        f'data-stage-id="{escape(membership.stage_id)}" '
        f'data-stage-index="{membership.stage_index}" '
        f'data-stage-total="{membership.stage_count}">'
        f"{label} {membership.stage_index}/{membership.stage_count}</span>"
    )


def render_membership_position(membership: GuidedRouteMembership, language: str) -> str:
    """Say where a core page sits: stage out of stages, page out of the stage's pages.

    An optional resource has no rank, and its stage number is already in the
    stage cue, so it gets no position text.
    """
    if (
        membership.stage_count is None
        or membership.page_index is None
        or membership.page_count is None
    ):
        return ""
    of = "sur" if language == "fr" else "of"
    stage_word = "Étape" if language == "fr" else "Stage"
    return (
        f"{stage_word} {membership.stage_index} {of} {membership.stage_count}"
        f" · page {membership.page_index} {of} {membership.page_count}"
    )


def render_guided_page_context_markdown(
    page: ResolvedPage,
    memberships: list[GuidedRouteMembership],
    language: str,
) -> str:
    """Render honest route context without inventing a unique parent stage."""
    if language not in {"fr", "en"}:
        raise ValueError(f"unsupported guided-route language: {language!r}")
    if not memberships:
        return ""

    if len(memberships) == 1:
        membership = memberships[0]
        aria_label = (
            "Contexte du parcours pédagogique" if language == "fr" else "Learning path context"
        )
        role_label = "Ressource facultative" if language == "fr" else "Optional resource"
        lines = [
            f'<nav class="guided-page-context" aria-label="{aria_label}">',
            '  <span class="guided-page-context__label">'
            + ("Parcours pédagogique" if language == "fr" else "Learning path")
            + "</span>",
            (
                '  <a class="guided-page-context__stage" href="learning-map.html#guided-stage-'
                f'{membership.stage_id}">{membership.stage_index:02d} · '
                f"{escape(membership.stage_title)}</a>"
            ),
        ]
        if badge := render_stage_badge(membership, language):
            lines.append(f"  {badge}")
        if membership.role == "optional":
            lines.append(f'  <span class="guided-page-context__role">{role_label}</span>')
        position = render_membership_position(membership, language)
        if position:
            lines.append(f'  <span class="guided-page-context__position">{position}</span>')
        lines.extend(["</nav>", ""])
        return "\n".join(lines)

    heading = (
        "Cette page intervient à plusieurs moments du parcours"
        if language == "fr"
        else "This page appears at more than one point in the learning path"
    )
    lines = [
        '<section class="guided-page-context guided-page-context--multiple"',
        '         aria-labelledby="guided-page-context-heading">',
        f'  <p id="guided-page-context-heading">{heading} : '
        f"<strong>{escape(page.title)}</strong>.</p>",
    ]
    lines.append("  <ul>")
    for membership in memberships:
        role_label = (
            ("Facultatif" if language == "fr" else "Optional")
            if membership.role == "optional"
            else ("Étape centrale" if language == "fr" else "Core stage")
        )
        lines.extend(
            [
                "    <li>",
                (
                    '      <a href="learning-map.html#guided-stage-'
                    f'{membership.stage_id}">{membership.stage_index:02d} · '
                    f"{escape(membership.stage_title)}</a>"
                ),
                f'      <span class="guided-page-context__role">{role_label}</span>',
                *(
                    [f"      {badge}"]
                    if (badge := render_stage_badge(membership, language))
                    else []
                ),
                *(
                    [f'      <span class="guided-page-context__position">{position}</span>']
                    if (position := render_membership_position(membership, language))
                    else []
                ),
                f"      <p>{escape(membership.stage_objective)}</p>",
                "    </li>",
            ]
        )
    lines.extend(["  </ul>", "</section>", ""])
    return "\n".join(lines)


def build_guided_route_transition_index(
    transitions: list[ResolvedGuidedRouteTransition],
) -> dict[str, list[ResolvedGuidedRouteTransition]]:
    """Index explicit transition explanations by page, preserving source order."""
    index: dict[str, list[ResolvedGuidedRouteTransition]] = {}
    for transition in transitions:
        for page in transition.pages:
            index.setdefault(page.id, []).append(transition)
    return index


def render_guided_page_transitions(
    transitions: list[ResolvedGuidedRouteTransition], language: str
) -> str:
    """Render progressive, non-prerequisite transition context without raw IDs."""
    if language not in {"fr", "en"}:
        raise ValueError(f"unsupported language: {language!r}")
    if not transitions:
        return ""
    label = (
        "Liens entre étapes expliqués sur cette page"
        if language == "fr"
        else "Stage connections explained on this page"
    )
    lines = [
        '<section class="guided-page-transitions" aria-label="' + label + '">',
        f'  <p class="guided-page-transitions__label">{label}</p>',
    ]
    for transition in transitions:
        arrow = "→" if transition.direction == "directed" else "↔"
        source_href = "learning-map.html#guided-stage-" + escape(
            transition.from_stage_id, quote=True
        )
        target_href = "learning-map.html#guided-stage-" + escape(transition.to_stage_id, quote=True)
        summary = (
            f'<a href="{source_href}">{escape(transition.from_stage_title)}</a> '
            f'{arrow} <a href="{target_href}">{escape(transition.to_stage_title)}</a>'
        )
        lines.extend(
            [
                '  <details class="guided-page-transitions__item">',
                f"    <summary>{summary}</summary>",
                f"    <p>{escape(transition.purpose)}</p>",
                "  </details>",
            ]
        )
    lines.extend(["</section>", ""])
    return "\n".join(lines)


ROUTE_PARTS: tuple[tuple[str, str, str, str], ...] = (
    (
        "discover",
        "orientation",
        "Découvrir le système",
        "Discover the system",
    ),
    (
        "prediction",
        "text-input",
        "Comprendre une prédiction",
        "Understand how a prediction is computed",
    ),
    (
        "usages",
        "inference",
        "Comprendre les usages de la prédiction",
        "Understand the uses of a prediction",
    ),
)
ROUTE_PART_BY_FIRST_STAGE: dict[str, tuple[str, str, str]] = {
    first_stage_id: (part_id, title_fr, title_en)
    for part_id, first_stage_id, title_fr, title_en in ROUTE_PARTS
}


def validate_route_projection(stages: list[ResolvedGuidedRouteStage]) -> None:
    """Guard the reader-facing three-part projection of the canonical route.

    The eight-stage registry (data/guided-route.yml) remains the canonical
    curriculum model; the three parts are the orientation projection
    recommended by docs/understand-llms-route-audit-2026-11-09.md. Renaming
    or reordering a boundary stage must update ROUTE_PARTS, not silently
    drop or shuffle a part heading.
    """
    known_stage_ids = {stage.id for stage in stages}
    missing = [
        first_stage_id
        for _, first_stage_id, _, _ in ROUTE_PARTS
        if first_stage_id not in known_stage_ids
    ]
    opening_order = [stage.id for stage in stages if stage.id in ROUTE_PART_BY_FIRST_STAGE]
    expected_order = [first_stage_id for _, first_stage_id, _, _ in ROUTE_PARTS]
    if missing or opening_order != expected_order:
        raise ValueError(
            "guided-route three-part projection is out of sync with "
            f"data/guided-route.yml: missing={sorted(missing)}, order={opening_order}"
        )


GUIDED_RAIL_LABELS: dict[str, dict[str, str]] = {
    "fr": {
        "aria": "Progression dans le parcours pédagogique",
        "progress": "Progression consultée · stockée uniquement dans ce navigateur",
        "reset": "Effacer la progression consultée",
    },
    "en": {
        "aria": "Learning path progress",
        "progress": "Viewed progress · stored only in this browser",
        "reset": "Clear viewed progress",
    },
}


def render_guided_rail(stages: list[ResolvedGuidedRouteStage], language: str) -> str:
    """Render a static, linked overview of route stages with an optional JS progress slot."""
    if language not in GUIDED_RAIL_LABELS:
        raise ValueError(f"unsupported guided-route language: {language!r}")
    labels = GUIDED_RAIL_LABELS[language]
    lines = [
        f'<nav class="guided-rail" aria-label="{labels["aria"]}" '
        f'data-guided-rail data-total="{len(stages)}">',
    ]
    for index, stage in enumerate(stages, start=1):
        part = ROUTE_PART_BY_FIRST_STAGE.get(stage.id)
        if part is not None:
            part_id, title_fr, title_en = part
            part_title = title_fr if language == "fr" else title_en
            lines.append(
                f'  <span class="guided-rail__part" data-part="{part_id}">'
                f"{escape(part_title)}</span>"
            )
        lines.append(
            f'  <a class="guided-rail__stage" href="#guided-stage-{escape(stage.id)}" '
            f'data-stage-id="{escape(stage.id)}" data-stage-index="{index}">'
            f'<span class="guided-rail__number">{index:02d}</span>'
            f'<span class="guided-rail__title">{escape(stage.title)}</span></a>'
        )
    lines.extend(
        [
            f'  <p class="guided-rail__progress" data-guided-rail-progress hidden '
            f'data-reset-label="{labels["reset"]}">{labels["progress"]}</p>',
            "</nav>",
            "",
        ]
    )
    return "\n".join(lines)


def render_guided_route_markdown(stages: list[ResolvedGuidedRouteStage], language: str) -> str:
    """Render the route as native Quarto Markdown; no browser-side route renderer."""
    if language not in {"fr", "en"}:
        raise ValueError(f"unsupported guided-route language: {language!r}")
    core_label = "Pages centrales" if language == "fr" else "Core pages"
    optional_label = "Ressources facultatives" if language == "fr" else "Optional resources"
    recap_label = "rappel" if language == "fr" else "recap"
    seen_page_ids: set[str] = set()

    def page_line(page: ResolvedPage) -> str:
        """Mark pages already listed in an earlier stage as a recap."""
        marker = f" *({recap_label})*" if page.id in seen_page_ids else ""
        seen_page_ids.add(page.id)
        return f"- [{escape_markdown_text(page.title)}]({page.href}){marker}"

    lines: list[str] = []
    grid_open = False
    for index, stage in enumerate(stages, start=1):
        part = ROUTE_PART_BY_FIRST_STAGE.get(stage.id)
        if part is not None:
            part_id, part_title_fr, part_title_en = part
            part_title = part_title_fr if language == "fr" else part_title_en
            if grid_open:
                lines.extend(["::::", ""])
                grid_open = False
            lines.extend(
                [
                    f"## {part_title} {{.guided-route-part #guided-part-{part_id}}}",
                    "",
                ]
            )
        if not grid_open:
            lines.extend([":::: {.guided-route-grid}", ""])
            grid_open = True
        lines.extend(
            [
                f"::: {{.guided-route-stage #guided-stage-{stage.id}}}",
                "",
                f"### {index:02d} · {escape_markdown_text(stage.title)}",
                "",
                escape_markdown_text(stage.objective),
                "",
                f"**{core_label}**",
                "",
            ]
        )
        lines.extend(page_line(page) for page in stage.pages)
        if stage.optional_pages:
            lines.extend(["", f"**{optional_label}**", ""])
            lines.extend(page_line(page) for page in stage.optional_pages)
        lines.extend(["", ":::", ""])
    if grid_open:
        lines.extend(["::::", ""])
    return "\n".join(lines)


def prepare_guided_page_context_fragments(
    language: str,
    stages: list[ResolvedGuidedRouteStage],
    transitions: list[ResolvedGuidedRouteTransition] | None = None,
) -> dict[Path, str]:
    """Render membership and explicit transition context for route pages."""
    memberships = build_guided_route_memberships(stages)
    page_by_id = {
        page.id: page for stage in stages for page in [*stage.pages, *stage.optional_pages]
    }
    transition_index = build_guided_route_transition_index(transitions or [])
    includes = SITE / "includes"
    outputs: dict[Path, str] = {}
    for page_id, page_memberships in memberships.items():
        page = page_by_id[page_id]
        output = includes / f"generated-guided-context-{page_id.replace('/', '-')}.qmd"
        membership = render_guided_page_context_markdown(page, page_memberships, language)
        transition_context = render_guided_page_transitions(
            transition_index.get(page_id, []), language
        )
        outputs[output] = membership + transition_context
    return outputs


def write_guided_page_context_fragments(
    language: str, stages: list[ResolvedGuidedRouteStage]
) -> list[Path]:
    """Write generated context partials for every page in the guided route."""
    artifacts = prepare_guided_page_context_fragments(language, stages)
    write_artifacts(artifacts)
    return list(artifacts)


ROUTE_CONTINUATION_PAGE = "build-path"
ROUTE_CONTINUATION_LABEL = {
    "fr": "Parcours terminé · ensuite : construire →",
    "en": "Path complete · next: build →",
}


def final_core_page_id(stages: Sequence[ResolvedGuidedRouteStage]) -> str | None:
    """Return the last core page of the guided route, where the route ends."""
    for stage in reversed(stages):
        if stage.pages:
            return stage.pages[-1].id
    return None


def render_suggested_route_markdown(
    page: dict[str, Any],
    page_by_id: dict[str, dict[str, Any]],
    language: str,
    *,
    completes_route: bool = False,
    sidebar_neighbors: dict[str, str] | None = None,
) -> str:
    """Render local previous/next links from the page's canonical suggested route.

    ``completes_route`` marks the last core page of the guided route. Its
    suggested route has no next page, so the reader would be left with a
    single backward link; it gets one forward card to the Build path instead.
    That is one concrete next step, not a list repeating the site menu.
    """
    if language not in {"fr", "en"}:
        raise ValueError(f"unsupported suggested-route language: {language!r}")

    route = page.get("route") or {}
    directions = (
        (
            "previous",
            "← Étape précédente" if language == "fr" else "← Previous step",
        ),
        (
            "next",
            "Étape suivante →" if language == "fr" else "Next step →",
        ),
    )
    targets: list[tuple[str, str, object]] = [
        (direction, label, route.get(direction)) for direction, label in directions
    ]
    if completes_route and route.get("next") is None:
        targets.append(
            (
                "continuation",
                ROUTE_CONTINUATION_LABEL[language],
                f"{language}/{ROUTE_CONTINUATION_PAGE}",
            )
        )
    cards: list[str] = []
    for direction, label, target_id in targets:
        if target_id is None:
            continue
        if not isinstance(target_id, str):
            raise ValueError(f"invalid {direction} route for {page['id']!r}: {target_id!r}")
        # Keep pedagogical transitions only when they add a destination that
        # the native Quarto footer navigation does not already expose.
        if target_id == (sidebar_neighbors or {}).get(direction):
            continue
        target = page_by_id.get(target_id)
        if target is None:
            raise ValueError(f"unresolved {direction} route for {page['id']!r}: {target_id!r}")
        href = str(target.get("href", ""))
        if not href.endswith(".html"):
            raise ValueError(f"route target has no published HTML href: {target_id!r}")
        source_href = f"{href[:-5]}.qmd"
        cards.extend(
            [
                f'  <a class="route-nav-card" href="{escape(source_href, quote=True)}">',
                f'    <span class="nav-direction">{escape(label)}</span>',
                f'    <span class="nav-title">{escape(str(target["title"]))}</span>',
                "  </a>",
            ]
        )

    if not cards:
        return ""
    return "\n".join(['<div class="route-nav-cards">', *cards, "</div>", ""])


def prepare_suggested_route_fragments(
    language: str,
    pages: list[dict[str, Any]],
    stages: Sequence[ResolvedGuidedRouteStage] = (),
) -> dict[Path, str]:
    """Render generated local-navigation partials for pages with route metadata.

    ``stages`` identifies the last core page of the guided route, which gets a
    forward card to the Build path.
    """
    page_by_id = {page["id"]: page for page in pages}
    final_page_id = final_core_page_id(stages)
    continuation_id = f"{language}/{ROUTE_CONTINUATION_PAGE}"
    sidebar_neighbors_by_page = load_sidebar_page_neighbors(language)
    includes = SITE / "includes"
    outputs: dict[Path, str] = {}
    for page in pages:
        rendered = render_suggested_route_markdown(
            page,
            page_by_id,
            language,
            # A site without a Build path (test fixtures) keeps its plain ending;
            # the published route is guarded by its own test.
            completes_route=page["id"] == final_page_id and continuation_id in page_by_id,
            sidebar_neighbors=sidebar_neighbors_by_page.get(page["id"], {}),
        )
        output = includes / (f"generated-suggested-route-{page['id'].replace('/', '-')}.qmd")
        outputs[output] = rendered
    return outputs


def write_suggested_route_fragments(
    language: str,
    pages: list[dict[str, Any]],
    stages: Sequence[ResolvedGuidedRouteStage] = (),
) -> list[Path]:
    """Write generated local-navigation partials for pages with route metadata."""
    artifacts = prepare_suggested_route_fragments(language, pages, stages)
    write_artifacts(artifacts)
    return list(artifacts)


def prepare_guided_route_fragment(
    language: str, stages: list[ResolvedGuidedRouteStage]
) -> dict[Path, str]:
    """Render a generated Quarto Markdown partial for the requested language."""
    output = SITE / "includes" / f"generated-guided-route-{language}.qmd"
    rail = render_guided_rail(stages, language)
    return {output: rail + "\n" + render_guided_route_markdown(stages, language)}


def write_guided_route_fragment(language: str, stages: list[ResolvedGuidedRouteStage]) -> Path:
    """Write a generated Quarto Markdown partial for the requested language."""
    artifacts = prepare_guided_route_fragment(language, stages)
    write_artifacts(artifacts)
    return next(iter(artifacts))


def prepare_map_fragments(
    language: str,
    navigation: list[dict[str, Any]],
    pages: list[dict[str, Any]],
    payload: dict[str, Any],
) -> dict[Path, str]:
    """Render every generated presentation artifact for one language."""
    page_by_id = {page["id"]: page for page in pages}
    includes = SITE / "includes"
    artifacts = {includes / "learning-map.html": render_map_script()}
    for representation in REPRESENTATIONS.values():
        fragment = includes / f"generated-{representation.artifact}-{language}.qmd"
        artifacts[fragment] = representation.render(language, navigation, page_by_id)
    artifacts[includes / f"generated-map-data-{language}.qmd"] = render_inline_map_data(payload)
    return artifacts


def write_map_fragments(
    language: str,
    navigation: list[dict[str, Any]],
    pages: list[dict[str, Any]],
    payload: dict[str, Any],
) -> None:
    """Write every generated presentation artifact for one language."""
    write_artifacts(prepare_map_fragments(language, navigation, pages, payload))


def load_domain_labels(language: str) -> dict[str, str] | None:
    """Return localized domain labels, or None when the domain registry is absent."""
    path = ROOT / "data" / "domains.yml"
    if not path.is_file():
        return None
    payload = load_yaml(path) or {}
    return {
        str(domain["id"]): str(domain["labels"][language]) for domain in payload.get("domains", [])
    }


def load_concept_graph(
    language: str, pages: list[dict[str, Any]]
) -> dict[str, list[dict[str, Any]]]:
    """Load the reviewed concept registry and resolve language-specific page links."""
    registry_path = ROOT / "data" / "concepts.yml"
    registry = load_yaml(registry_path)
    domain_labels = load_domain_labels(language)
    page_by_id = {page["id"]: page for page in pages}
    concepts = []
    concept_ids = set()
    referenced_domains: list[str] = []
    for item in registry["concepts"]:
        resources = []
        for page_id in item["resources"]:
            page = page_by_id.get(page_id)
            if page is not None:
                resources.append({"id": page_id, "title": page["title"], "href": page["href"]})
        domains = [value for value in item.get("domains", []) if isinstance(value, str)]
        for domain_id in domains:
            if domain_id not in referenced_domains:
                referenced_domains.append(domain_id)
        concepts.append(
            {
                "id": item["id"],
                "label": item["labels"][language],
                "definition": item["definitions"][language],
                "importance": item["importance"],
                "domains": domains,
                "resources": resources,
            }
        )
        concept_ids.add(item["id"])
    relations = []
    for edge in registry["relations"]:
        if edge["from"] not in concept_ids or edge["to"] not in concept_ids:
            continue
        relation = {"from": edge["from"], "type": edge["type"], "to": edge["to"]}
        rationale = edge.get("rationale")
        if isinstance(rationale, dict) and isinstance(rationale.get(language), str):
            relation["rationale"] = rationale[language]
        relations.append(relation)
    relation_types = {
        kind: {
            "direction": definition["direction"],
            "family": definition["family"],
            "transitive": definition["transitive"],
            "acyclic": definition["acyclic"],
            "learning_dependency": definition["learning_dependency"],
            "inverse": definition["inverse"],
            "label": definition["labels"][language],
            "description": definition["descriptions"][language],
        }
        for kind, definition in registry["relation_types"].items()
        if any(edge["type"] == kind for edge in relations)
    }
    if domain_labels is None:
        concept_domains = [
            {"id": domain_id, "label": domain_id} for domain_id in referenced_domains
        ]
    else:
        ordered = [domain_id for domain_id in domain_labels if domain_id in referenced_domains]
        ordered += [domain_id for domain_id in referenced_domains if domain_id not in domain_labels]
        concept_domains = [
            {"id": domain_id, "label": domain_labels.get(domain_id, domain_id)}
            for domain_id in ordered
        ]
    return {
        "concepts": concepts,
        "concept_domains": concept_domains,
        "concept_relations": relations,
        "concept_relation_types": relation_types,
    }


def assign_route_rank(pages: list[dict[str, Any]], language: str) -> None:
    """Assign a display rank using route and hierarchy edges, not a learning order."""
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


def prepare_build(language: str) -> dict[Path, str]:
    """Render the published page graph and every presentation artifact without writing."""
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
    guided_route = load_guided_route(language, pages)
    guided_transitions = load_guided_route_transitions(language, pages)
    navigation = load_navigation(language, pages)
    artifacts = prepare_guided_route_fragment(language, guided_route)
    artifacts.update(
        prepare_guided_page_context_fragments(language, guided_route, guided_transitions)
    )
    artifacts.update(prepare_suggested_route_fragments(language, pages, guided_route))
    payload = {
        "language": language,
        "source": "LLM-LAB-PAGE-MAP v1 + data/guided-route.yml + data/concepts.yml",
        "pages": pages,
        "navigation": navigation,
        **concept_graph,
    }
    artifacts.update(prepare_map_fragments(language, navigation, pages, payload))
    artifacts[output] = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    return artifacts


def build(language: str) -> Path:
    """Write the published page graph and every generated presentation artifact."""
    write_artifacts(prepare_build(language))
    return SITE / f"learning-map-data-{language}.json"


def main() -> None:
    """Generate bilingual learning maps and the linked-data export."""
    from export_knowledge_graph import build_graph, serialize_graph

    # Render every output before replacing any, so an invalid route, concept or
    # graph in one language cannot leave the other language half-updated.
    artifacts: dict[Path, str] = {}
    outputs = [SITE / f"learning-map-data-{language}.json" for language in ("fr", "en")]
    for language in ("fr", "en"):
        artifacts.update(prepare_build(language))
    export = SITE / "knowledge-graph.jsonld"
    artifacts[export] = serialize_graph(build_graph())
    write_artifacts(artifacts)
    for output in [*outputs, export]:
        sys.stdout.write(f"Generated {output.relative_to(ROOT)}\n")


if __name__ == "__main__":
    main()
