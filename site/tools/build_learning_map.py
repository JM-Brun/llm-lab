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
from html import escape
from pathlib import Path
from typing import Any, Literal

import yaml
from learning_map_renderers import REPRESENTATIONS, escape_markdown_text, render_map_script
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ROOT = Path(__file__).resolve().parents[2]
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


def slugify_area_id(title: str) -> str:
    """Return an ASCII slug used as a stable, language-scoped area identifier."""
    folded = unicodedata.normalize("NFKD", title).encode("ascii", "ignore")
    return re.sub(r"[^a-z0-9]+", "-", folded.decode("ascii").lower()).strip("-")


def sidebar_page_id(entry: object, language: str) -> str | None:
    """Resolve one Quarto sidebar entry to a published page identifier."""
    if not isinstance(entry, str) or not entry.endswith(".qmd"):
        return None
    slug = entry.removesuffix(".qmd")
    if "/" not in slug:
        if slug == "references":
            return "reference/references"
        return f"{language}/{slug}"
    return slug


def load_navigation(language: str, pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Derive the drill-down area structure from the authored Quarto sidebar.

    The sidebar is the only authored source of reader-facing grouping. Entries
    that do not resolve to a published page identifier are ignored, and empty
    groups are dropped, so the progressive map never shows a dead end.
    """
    config = yaml.safe_load((SITE / "_quarto.yml").read_text(encoding="utf-8"))
    sidebars = (config or {}).get("website", {}).get("sidebar", [])
    sidebar = next((entry for entry in sidebars if entry.get("id") == language), None)
    if sidebar is None:
        raise ValueError(f"missing Quarto sidebar for language: {language!r}")
    published = {page["id"] for page in pages}

    def collect(entries: list[object]) -> list[str]:
        """Keep only sidebar entries that resolve to published pages."""
        identifiers = (sidebar_page_id(entry, language) for entry in entries)
        return [value for value in identifiers if value in published]

    areas: list[dict[str, Any]] = []
    for entry in sidebar.get("contents", []):
        if not isinstance(entry, dict) or "section" not in entry:
            continue
        sections = [
            {"title": str(item["section"]), "pages": collect(item.get("contents", []))}
            for item in entry.get("contents", [])
            if isinstance(item, dict) and "section" in item
        ]
        sections = [section for section in sections if section["pages"]]
        area_pages = collect(entry.get("contents", []))
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
    payload = yaml.safe_load(source_path.read_text(encoding="utf-8"))
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
                f'{membership.stage_id}">{membership.stage_index:02d} · {escape(membership.stage_title)}</a>'
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
                    f'{membership.stage_id}">{membership.stage_index:02d} · {escape(membership.stage_title)}</a>'
                ),
                f'      <span class="guided-page-context__role">{role_label}</span>',
                f"      <p>{escape(membership.stage_objective)}</p>",
                "    </li>",
            ]
        )
    lines.extend(["  </ul>", "</section>", ""])
    return "\n".join(lines)


def render_guided_route_markdown(stages: list[ResolvedGuidedRouteStage], language: str) -> str:
    """Render the route as native Quarto Markdown; no browser-side route renderer."""
    if language not in {"fr", "en"}:
        raise ValueError(f"unsupported guided-route language: {language!r}")
    core_label = "Pages centrales" if language == "fr" else "Core pages"
    optional_label = "Ressources facultatives" if language == "fr" else "Optional resources"
    lines = [":::: {.guided-route-grid}", ""]
    for index, stage in enumerate(stages, start=1):
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
        lines.extend(f"- [{escape_markdown_text(page.title)}]({page.href})" for page in stage.pages)
        if stage.optional_pages:
            lines.extend(["", f"**{optional_label}**", ""])
            lines.extend(
                f"- [{escape_markdown_text(page.title)}]({page.href})"
                for page in stage.optional_pages
            )
        lines.extend(["", ":::", ""])
    lines.extend(["::::", ""])
    return "\n".join(lines)


def write_guided_page_context_fragments(
    language: str, stages: list[ResolvedGuidedRouteStage]
) -> list[Path]:
    """Write generated context partials for every page in the guided route."""
    memberships = build_guided_route_memberships(stages)
    page_by_id = {
        page.id: page for stage in stages for page in [*stage.pages, *stage.optional_pages]
    }
    includes = SITE / "includes"
    includes.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for page_id, page_memberships in memberships.items():
        page = page_by_id[page_id]
        output = includes / f"generated-guided-context-{page_id.replace('/', '-')}.qmd"
        output.write_text(
            render_guided_page_context_markdown(page, page_memberships, language),
            encoding="utf-8",
        )
        outputs.append(output)
    return outputs


def write_guided_route_fragment(language: str, stages: list[ResolvedGuidedRouteStage]) -> Path:
    """Write a generated Quarto Markdown partial for the requested language."""
    output = SITE / "includes" / f"generated-guided-route-{language}.qmd"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_guided_route_markdown(stages, language), encoding="utf-8")
    return output


def write_map_fragments(
    language: str, navigation: list[dict[str, Any]], pages: list[dict[str, Any]]
) -> None:
    """Write every generated presentation artifact for one language."""
    page_by_id = {page["id"]: page for page in pages}
    includes = SITE / "includes"
    includes.mkdir(parents=True, exist_ok=True)
    (includes / "learning-map.html").write_text(render_map_script(), encoding="utf-8")
    for representation in REPRESENTATIONS.values():
        fragment = includes / f"generated-{representation.artifact}-{language}.qmd"
        fragment.write_text(
            representation.render(language, navigation, page_by_id),
            encoding="utf-8",
        )


def load_domain_labels(language: str) -> dict[str, str] | None:
    """Return localized domain labels, or None when the domain registry is absent."""
    path = ROOT / "data" / "domains.yml"
    if not path.is_file():
        return None
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {
        str(domain["id"]): str(domain["labels"][language]) for domain in payload.get("domains", [])
    }


def load_concept_graph(
    language: str, pages: list[dict[str, Any]]
) -> dict[str, list[dict[str, Any]]]:
    """Load the reviewed concept registry and resolve language-specific page links."""
    registry_path = ROOT / "data" / "concepts.yml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
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


def build(language: str) -> Path:
    """Write the published page graph and every generated presentation artifact."""
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
    write_guided_route_fragment(language, guided_route)
    write_guided_page_context_fragments(language, guided_route)
    write_map_fragments(language, navigation, pages)
    output.write_text(
        json.dumps(
            {
                "language": language,
                "source": "LLM-LAB-PAGE-MAP v1 + data/guided-route.yml + data/concepts.yml",
                "pages": pages,
                "navigation": navigation,
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
