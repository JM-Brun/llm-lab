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
import re
import sys
import unicodedata
from collections import deque
from collections.abc import Sequence
from html import escape
from pathlib import Path
from typing import Any, Literal

from artifact_writer import write_artifacts
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


def page_href(page_id: str, language: str) -> str:
    """Return a path relative to a language-specific learning-map page."""
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

    pages: list[dict[str, Any]] = []
    for page in load_published_pages(SITE):
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
                "href": page_href(page_id, "fr" if language == "shared" else language),
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


class GuidedRouteMembership(StrictModel):
    """One page's explicit membership in a guided-route stage."""

    stage_id: str
    stage_index: int
    stage_title: str
    stage_objective: str
    role: Literal["core", "optional"]


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
        for page in stage.pages:
            memberships.setdefault(page.id, []).append(
                GuidedRouteMembership(
                    stage_id=stage.id,
                    stage_index=stage_index,
                    stage_title=stage.title,
                    stage_objective=stage.objective,
                    role="core",
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
                )
            )
    return memberships


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
        if membership.role == "optional":
            lines.append(f'  <span class="guided-page-context__role">{role_label}</span>')
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
        "  <ul>",
    ]
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
                f"      <p>{escape(membership.stage_objective)}</p>",
                "    </li>",
            ]
        )
    lines.extend(["  </ul>", "</section>", ""])
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
    language: str, stages: list[ResolvedGuidedRouteStage]
) -> dict[Path, str]:
    """Render generated context partials for every page in the guided route."""
    memberships = build_guided_route_memberships(stages)
    page_by_id = {
        page.id: page for stage in stages for page in [*stage.pages, *stage.optional_pages]
    }
    includes = SITE / "includes"
    outputs: dict[Path, str] = {}
    for page_id, page_memberships in memberships.items():
        page = page_by_id[page_id]
        output = includes / f"generated-guided-context-{page_id.replace('/', '-')}.qmd"
        outputs[output] = render_guided_page_context_markdown(page, page_memberships, language)
    return outputs


def write_guided_page_context_fragments(
    language: str, stages: list[ResolvedGuidedRouteStage]
) -> list[Path]:
    """Write generated context partials for every page in the guided route."""
    artifacts = prepare_guided_page_context_fragments(language, stages)
    write_artifacts(artifacts)
    return list(artifacts)


ROUTE_COMPLETION_COPY: dict[str, dict[str, Any]] = {
    "en": {
        "kicker": "Theory path — Understand",
        "title": "You have reached the end of the path",
        "summary": (
            "You followed one prediction from text to a probability distribution, "
            "saw how an observed target is scored, and how a gradient points to a "
            "parameter update. Choose what to do with it:"
        ),
        "exits": (
            (
                "build-path.qmd",
                "Build",
                "read and run the small GPT that implements these stages",
            ),
            (
                "exercises.qmd",
                "Practice",
                "check that you can redo the calculations without the page",
            ),
            (
                "deepen.qmd",
                "Deepen",
                "follow the derivations and variants that the path left aside",
            ),
            (
                "learning-map.qmd",
                "Review",
                "see the eight stages again and return to any of them",
            ),
        ),
    },
    "fr": {
        "kicker": "Parcours Théorie — Comprendre",
        "title": "Vous êtes arrivé au bout du parcours",
        "summary": (
            "Vous avez suivi une prédiction du texte à une distribution de "
            "probabilité, vu comment une cible observée est évaluée et comment "
            "un gradient indique une mise à jour des paramètres. À vous de "
            "choisir la suite :"
        ),
        "exits": (
            (
                "build-path.qmd",
                "Construire",
                "lire et exécuter le petit GPT qui implémente ces étapes",
            ),
            (
                "exercises.qmd",
                "Pratiquer",
                "vérifier que vous savez refaire les calculs sans la page",
            ),
            (
                "deepen.qmd",
                "Approfondir",
                "suivre les dérivations et variantes laissées de côté",
            ),
            (
                "learning-map.qmd",
                "Revoir",
                "retrouver les huit étapes et revenir à l'une d'elles",
            ),
        ),
    },
}


def render_route_completion_markdown(language: str) -> str:
    """Render the closing block shown on the last core page of the guided route.

    Without it the route ends on a page whose only onward link points
    backwards, so a reader who finishes has nowhere to go.
    """
    if language not in ROUTE_COMPLETION_COPY:
        raise ValueError(f"unsupported suggested-route language: {language!r}")
    copy = ROUTE_COMPLETION_COPY[language]
    lines = [
        # A div, not <aside>: Quarto moves <aside> elements into the page margin.
        '<div class="route-complete" role="region" aria-labelledby="route-complete-title">',
        f'  <p class="route-complete__kicker">{escape(copy["kicker"])}</p>',
        f'  <p class="route-complete__title" id="route-complete-title">{escape(copy["title"])}</p>',
        f"  <p>{escape(copy['summary'])}</p>",
        '  <ul class="route-complete__exits">',
    ]
    for href, label, description in copy["exits"]:
        lines.append(
            f'    <li><a href="{escape(href, quote=True)}"><strong>{escape(label)}</strong></a>'
            f" — {escape(description)}</li>"
        )
    lines.extend(["  </ul>", "</div>", ""])
    return "\n".join(lines)


def render_route_return_cards(
    memberships: Sequence[GuidedRouteMembership], language: str
) -> list[str]:
    """Render one way back to the path for each stage that lists the page as optional.

    The card targets the stage on the path page rather than one core page:
    the registry does not record which core page the reader came from.
    """
    label = "↩ Retour au parcours" if language == "fr" else "↩ Back to the learning path"
    cards: list[str] = []
    for membership in memberships:
        if membership.role != "optional":
            continue
        cards.extend(
            [
                '  <a class="route-nav-card route-nav-card--return" '
                f'href="learning-map.html#guided-stage-{membership.stage_id}">',
                f'    <span class="nav-direction">{escape(label)}</span>',
                f'    <span class="nav-title">{membership.stage_index:02d} · '
                f"{escape(membership.stage_title)}</span>",
                "  </a>",
            ]
        )
    return cards


def render_suggested_route_markdown(
    page: dict[str, Any],
    page_by_id: dict[str, dict[str, Any]],
    language: str,
    *,
    return_memberships: Sequence[GuidedRouteMembership] = (),
    completes_route: bool = False,
) -> str:
    """Render the local navigation shown at the bottom of a page.

    Previous/next cards come from the page's canonical suggested route.
    ``return_memberships`` adds a way back for pages that are only optional
    resources of the guided route; ``completes_route`` adds the closing block
    of its last core page.
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
    cards: list[str] = []
    for direction, label in directions:
        target_id = route.get(direction)
        if target_id is None or return_memberships:
            # An optional resource shows its way back to the path instead of
            # edges from another reading order that its page does not surface.
            continue
        if not isinstance(target_id, str):
            raise ValueError(f"invalid {direction} route for {page['id']!r}: {target_id!r}")
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

    cards.extend(render_route_return_cards(return_memberships, language))

    blocks: list[str] = []
    if cards:
        blocks.append("\n".join(['<div class="route-nav-cards">', *cards, "</div>", ""]))
    if completes_route:
        blocks.append(render_route_completion_markdown(language))
    return "\n".join(blocks)


def final_core_page_id(stages: Sequence[ResolvedGuidedRouteStage]) -> str | None:
    """Return the last core page of the guided route, where the route ends."""
    for stage in reversed(stages):
        if stage.pages:
            return stage.pages[-1].id
    return None


def prepare_suggested_route_fragments(
    language: str,
    pages: list[dict[str, Any]],
    stages: Sequence[ResolvedGuidedRouteStage] = (),
) -> dict[Path, str]:
    """Render generated local-navigation partials.

    A page gets a partial when it has suggested-route edges, when it is only an
    optional resource of the guided route (way back), or when it is the last
    core page of the route (closing block).
    """
    page_by_id = {page["id"]: page for page in pages}
    memberships = build_guided_route_memberships(list(stages))
    final_page_id = final_core_page_id(stages)
    includes = SITE / "includes"
    outputs: dict[Path, str] = {}
    for page in pages:
        page_memberships = memberships.get(page["id"], [])
        optional_only = bool(page_memberships) and all(
            membership.role == "optional" for membership in page_memberships
        )
        route = page.get("route") or {}
        rendered = render_suggested_route_markdown(
            page,
            page_by_id,
            language,
            return_memberships=page_memberships if optional_only else (),
            completes_route=page["id"] == final_page_id and route.get("next") is None,
        )
        if not rendered:
            continue
        output = includes / (f"generated-suggested-route-{page['id'].replace('/', '-')}.qmd")
        outputs[output] = rendered
    return outputs


def write_suggested_route_fragments(
    language: str,
    pages: list[dict[str, Any]],
    stages: Sequence[ResolvedGuidedRouteStage] = (),
) -> list[Path]:
    """Write generated local-navigation partials (see the prepare function)."""
    artifacts = prepare_suggested_route_fragments(language, pages, stages)
    write_artifacts(artifacts)
    return list(artifacts)


def prepare_guided_route_fragment(
    language: str, stages: list[ResolvedGuidedRouteStage]
) -> dict[Path, str]:
    """Render a generated Quarto Markdown partial for the requested language."""
    output = SITE / "includes" / f"generated-guided-route-{language}.qmd"
    return {output: render_guided_route_markdown(stages, language)}


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
    navigation = load_navigation(language, pages)
    artifacts = prepare_guided_route_fragment(language, guided_route)
    artifacts.update(prepare_guided_page_context_fragments(language, guided_route))
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
