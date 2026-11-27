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
from dataclasses import dataclass
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


class ConceptualFocus(StrictModel):
    """Objects studied during one visit to a published lesson."""

    objects: list[str] = Field(min_length=1)
    outcome: LocalizedCopy
    mobilizes: list[str] = Field(default_factory=list)
    visit: Literal["study", "preview", "revisit"] = "study"

    @field_validator("objects", "mobilizes")
    @classmethod
    def distinct_objects(cls, values: list[str]) -> list[str]:
        if len(values) != len(set(values)):
            raise ValueError("a visit must list distinct conceptual objects")
        return values


class PredictionUse(StrictModel):
    """Where an operation sits relative to prediction and what it changes."""

    phase: Literal["input", "output", "training"]
    context: LocalizedCopy
    parameters: Literal["fixed", "updated"]
    action: LocalizedCopy


class StageOverview(StrictModel):
    """A plain-language question and answer with a formal reading of the same stage."""

    question: LocalizedCopy
    result: LocalizedCopy
    signature: str = Field(min_length=1)
    criterion: LocalizedCopy


class GuidedRouteStage(StrictModel):
    """One conceptual stage with bilingual copy and page references."""

    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    title: LocalizedCopy
    objective: LocalizedCopy
    overview: StageOverview | None = None
    pages: LocalizedPageIds
    optional_pages: OptionalLocalizedPageIds = Field(default_factory=OptionalLocalizedPageIds)
    conceptual_focus: dict[str, ConceptualFocus] = Field(default_factory=dict)
    compact_title: LocalizedCopy | None = None
    prediction_use: PredictionUse | None = None

    @model_validator(mode="after")
    def core_and_optional_pages_are_disjoint(self) -> GuidedRouteStage:
        for language in ("fr", "en"):
            overlap = set(getattr(self.pages, language)) & set(
                getattr(self.optional_pages, language)
            )
            if overlap:
                raise ValueError(f"{language} core and optional pages overlap: {sorted(overlap)}")
        return self


class LessonContract(StrictModel):
    """Logical topic references shared by both versions of a core lesson."""

    synthesis: str
    requires: list[str] = Field(default_factory=list)
    stage: str | None = None


class BoundaryExplanation(StrictModel):
    """Core lesson and concept IDs for one side of a conceptual boundary."""

    concept_ids: list[str] = Field(min_length=1)
    pages: LocalizedCopy


class BoundaryExercise(StrictModel):
    """A bilingual exercise and its shared explicit Quarto anchor."""

    pages: LocalizedCopy
    anchor: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    label: LocalizedCopy


class LearningBoundary(StrictModel):
    """Editorial evidence connecting two or more stages with an exercise."""

    criterion: str = Field(min_length=1)
    explanations: dict[str, BoundaryExplanation] = Field(min_length=2)
    transfer: BoundaryExercise


class GuidedRouteDocument(StrictModel):
    """Versioned source document for the reader-facing conceptual route."""

    schema_version: Literal[1]
    stages: list[GuidedRouteStage] = Field(min_length=1)
    # Detailed transition validation lives in guided_route_transitions.py so
    # this document accepts the canonical top-level field while keeping the
    # stage model and its membership projection independent.
    transitions: list[GuidedRouteTransition] = Field(default_factory=list)
    lesson_contracts: dict[str, LessonContract] | None = None
    boundaries: dict[str, LearningBoundary] = Field(default_factory=dict)

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
    overview: StageOverview | None = None
    pages: list[ResolvedPage]
    optional_pages: list[ResolvedPage] = Field(default_factory=list)
    conceptual_focus: dict[str, ConceptualFocus] = Field(default_factory=dict)
    compact_title: str | None = None
    prediction_use: PredictionUse | None = None


class ResolvedLessonContract(StrictModel):
    """A core lesson, its knowledge dependencies and its primary revision page."""

    scope: str
    outcome: str
    stage: str
    requires: list[ResolvedPage]
    synthesis: ResolvedPage
    revision_scope: str


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
    """Remove Quarto heading IDs and lightweight Markdown markup."""
    value = re.sub(r"\s+\{#[^}]+\}\s*$", "", value)
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
                "summary": metadata.get("summary", ""),
                "purpose": str(metadata.get("purpose", "")),
                **(
                    {"revision_of": metadata.get("revision_of", [])}
                    if metadata.get("revision_role") == "synthesis"
                    else {}
                ),
                "covered_stages": metadata.get("covered_stages", []),
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
                overview=stage.overview,
                pages=resolve_pages(getattr(stage.pages, language), stage.id, "core"),
                optional_pages=resolve_pages(
                    getattr(stage.optional_pages, language), stage.id, "optional"
                ),
                conceptual_focus=stage.conceptual_focus,
                compact_title=getattr(stage.compact_title, language)
                if stage.compact_title
                else None,
                prediction_use=stage.prediction_use,
            )
        )
    return resolved


def resolve_lesson_contracts(
    document: GuidedRouteDocument,
    stages: list[ResolvedGuidedRouteStage],
    pages: list[dict[str, Any]],
) -> dict[str, ResolvedLessonContract]:
    """Resolve shared topic IDs and verify prerequisites against the authored sequence."""
    page_by_id = {page["id"]: page for page in pages}
    occurrences: dict[str, list[tuple[str, int, ResolvedPage]]] = {}
    position = 0
    for stage in stages:
        for page in stage.pages:
            topic = page_by_id[page.id]["topic"]
            occurrences.setdefault(topic, []).append((stage.id, position, page))
            position += 1

    contracts = document.lesson_contracts or {}
    if contracts.keys() != occurrences.keys():
        raise ValueError(
            "guided lesson contracts must cover exactly the core topics: "
            f"missing={sorted(occurrences.keys() - contracts.keys())}, "
            f"extra={sorted(contracts.keys() - occurrences.keys())}"
        )
    acquisition: dict[str, tuple[str, int, ResolvedPage]] = {}
    for topic, visits in occurrences.items():
        stages_for_topic = {visit[0] for visit in visits}
        page_ids_for_topic = {visit[2].id for visit in visits}
        stage = contracts[topic].stage
        if len(page_ids_for_topic) != 1 or (len(visits) > 1 and stage is None):
            raise ValueError(f"guided lesson {topic!r}: ambiguous acquisition stage or page")
        if stage is not None and stage not in stages_for_topic:
            raise ValueError(f"guided lesson {topic!r}: acquisition stage {stage!r} is not core")
        acquisition[topic] = next(visit for visit in visits if stage in (None, visit[0]))

    by_page: dict[str, ResolvedLessonContract] = {}
    for topic, (stage, order, lesson) in acquisition.items():
        contract = contracts[topic]
        if len(set(contract.requires)) != len(contract.requires):
            raise ValueError(f"guided lesson {topic!r}: duplicate prerequisites")
        requires = []
        for prerequisite in contract.requires:
            previous = acquisition.get(prerequisite)
            if previous is None or previous[1] >= order:
                raise ValueError(
                    f"guided lesson {topic!r}: prerequisite {prerequisite!r} "
                    "must be acquired earlier in the core route"
                )
            requires.append(previous[2])
        candidates = [
            page
            for page in pages
            if page["topic"] == contract.synthesis
            and page["language"] == page_by_id[lesson.id]["language"]
            and lesson.id in page.get("revision_of", [])
        ]
        if len(candidates) != 1:
            raise ValueError(
                f"guided lesson {lesson.id!r}: expected one published synthesis "
                f"with topic {contract.synthesis!r} and a typed revision link"
            )
        synthesis = candidates[0]
        by_page[lesson.id] = ResolvedLessonContract(
            stage=stage,
            scope=page_by_id[lesson.id]["scope"],
            outcome=page_by_id[lesson.id]["purpose"],
            requires=requires,
            synthesis=ResolvedPage(**{key: synthesis[key] for key in ("id", "title", "href")}),
            revision_scope=synthesis["scope"],
        )
    return by_page


def resolve_boundary_exercises(
    document: GuidedRouteDocument,
    stages: list[ResolvedGuidedRouteStage],
    pages: list[dict[str, Any]],
    language: str,
) -> dict[str, list[ResolvedPage]]:
    """Index exercise links by each stage whose core lesson supplies an explanation."""
    core_ids_by_stage = {stage.id: {page.id for page in stage.pages} for stage in stages}
    page_by_id = {page["id"]: page for page in pages}
    by_stage: dict[str, list[ResolvedPage]] = {}
    for boundary_id, boundary in document.boundaries.items():
        exercise = boundary.transfer
        exercise_id = getattr(exercise.pages, language)
        target = page_by_id.get(exercise_id)
        if target is None or target["language"] != language or target["destination"] != "practice":
            raise ValueError(
                f"boundary {boundary_id!r}: expected a published {language} practice page "
                f"for {exercise_id!r}"
            )
        practice = ResolvedPage(
            id=exercise_id,
            title=getattr(exercise.label, language),
            href=f"{target['href']}#{exercise.anchor}",
        )
        for stage_id, explanation in boundary.explanations.items():
            lesson_id = getattr(explanation.pages, language)
            if lesson_id not in core_ids_by_stage.get(stage_id, set()):
                raise ValueError(
                    f"boundary {boundary_id!r}: {lesson_id!r} must be a core lesson of {stage_id!r}"
                )
            by_stage.setdefault(stage_id, []).append(practice)
    return by_stage


def prepare_exercise_review_fragments(
    stages: list[ResolvedGuidedRouteStage],
    boundary_exercises: dict[str, list[ResolvedPage]],
    language: str,
) -> dict[Path, str]:
    """Invert the plan's practice links into a partial for each exercise."""
    stages_by_exercise: dict[tuple[str, str], list[ResolvedGuidedRouteStage]] = {}
    for stage in stages:
        for exercise in boundary_exercises.get(stage.id, []):
            linked_stages = stages_by_exercise.setdefault((exercise.id, exercise.href), [])
            if stage not in linked_stages:
                linked_stages.append(stage)

    label = "Reprendre la révision" if language == "fr" else "Return to the review plan"
    artifacts: dict[Path, str] = {}
    for (exercise_id, exercise_href), linked_stages in stages_by_exercise.items():
        page_href, anchor = exercise_href.split("#", 1)
        plan_href = posixpath.relpath("review-path.html", posixpath.dirname(page_href) or ".")
        links = [
            f"[{escape_markdown_text(stage.title)}]({plan_href}#{stage.id})"
            for stage in linked_stages
        ]
        filename = f"generated-exercise-review-{exercise_id.replace('/', '-')}-{anchor}.qmd"
        artifacts[SITE / "includes" / filename] = f"**{label}** · " + " · ".join(links) + "\n"
    return artifacts


def render_lesson_contracts(
    stages: list[ResolvedGuidedRouteStage],
    contracts: dict[str, ResolvedLessonContract],
    language: str,
    boundary_exercises: dict[str, list[ResolvedPage]] | None = None,
) -> str:
    """Render the stage plan from the same lesson metadata used by the map."""
    fr = language == "fr"

    def link(page: ResolvedPage) -> str:
        return f"[{escape_markdown_text(page.title)}]({page.href})"

    lines: list[str] = []
    practice_by_stage = boundary_exercises or {}
    if any(stage.prediction_use for stage in stages):
        comparison_title = "Comparer les usages" if fr else "Compare uses"
        lines.extend(
            [
                f"## {comparison_title} {{#compare-prediction-uses .unlisted}}",
                "",
                render_prediction_use_comparison(stages, language),
                "",
            ]
        )
    for stage in stages:
        lines.extend([f"## {escape_markdown_text(stage.title)} {{#{stage.id}}}", ""])
        if overview := stage.overview:
            question = escape_markdown_text(getattr(overview.question, language))
            result = escape_markdown_text(getattr(overview.result, language))
            formal_label = "Écriture formelle" if fr else "Formal view"
            objective_label = "Objectif de l'étape" if fr else "Stage objective"
            lines.extend(
                [
                    f"**{question}** {result}",
                    "",
                    "<details>",
                    f"<summary>{formal_label}</summary>",
                    "",
                    "$$",
                    overview.signature,
                    "$$",
                    "",
                    getattr(overview.criterion, language),
                    "",
                    f"**{objective_label}.** {escape_markdown_text(stage.objective)}",
                    "",
                    "</details>",
                    "",
                ]
            )
        else:
            lines.extend([escape_markdown_text(stage.objective), ""])
        for practice in practice_by_stage.get(stage.id, []):
            lines.extend([link(practice), ""])
        for lesson in stage.pages:
            contract = contracts[lesson.id]
            lines.extend([f"### {escape_markdown_text(lesson.title)}", ""])
            if stage.id != contract.stage:
                acquired = next(item for item in stages if item.id == contract.stage)
                label = "Acquis visé à l'étape" if fr else "Outcome expected in"
                lines.extend([f"{link(lesson)} · {label} [{acquired.title}](#{acquired.id}).", ""])
                continue
            lines.extend([f"{link(lesson)} · {link(contract.synthesis)}", ""])
            if contract.requires:
                label = "Acquis mobilisés" if fr else "Prior learning"
                lines.append(f"- **{label}** — " + ", ".join(map(link, contract.requires)))
            revision_label = "À retrouver dans la fiche" if fr else "What the sheet covers"
            for label, value in (
                ("Périmètre" if fr else "Scope", contract.scope),
                ("Acquis visé" if fr else "Learning outcome", contract.outcome),
                (revision_label, contract.revision_scope),
            ):
                lines.append(f"- **{label}** — {escape_markdown_text(value)}")
            lines.append("")
    return "\n".join(lines)


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


def render_cross_cutting_coverage_markdown(
    page: dict[str, Any], stages: Sequence[ResolvedGuidedRouteStage], language: str
) -> str:
    """Render explicit thematic coverage as a set, not as a route or menu."""
    if language not in {"fr", "en"}:
        raise ValueError(f"unsupported coverage language: {language!r}")
    stage_ids = page.get("covered_stages", [])
    if not isinstance(stage_ids, list) or any(not isinstance(item, str) for item in stage_ids):
        raise ValueError(f"invalid covered_stages metadata for {page['id']!r}")
    if len(stage_ids) != len(set(stage_ids)):
        raise ValueError(f"duplicate covered stage for {page['id']!r}")
    stage_by_id = {stage.id: stage for stage in stages}
    missing = [stage_id for stage_id in stage_ids if stage_id not in stage_by_id]
    if missing:
        raise ValueError(f"unknown covered stages for {page['id']!r}: {missing}")
    if not stage_ids:
        return ""
    heading = (
        "Étapes du parcours abordées dans ce panorama"
        if language == "fr"
        else "Learning stages covered by this overview"
    )
    heading_id = f"guided-coverage-{escape(page['id'].replace('/', '-'), quote=True)}"
    lines = [
        f'<section class="guided-page-coverage" aria-labelledby="{heading_id}">',
        f'  <h2 class="guided-page-coverage__heading" id="{heading_id}">{heading}</h2>',
        '  <ul class="guided-page-coverage__list">',
    ]
    for stage_id in stage_ids:
        stage = stage_by_id[stage_id]
        lines.append(
            f'    <li><a href="learning-map.html#guided-stage-{escape(stage.id, quote=True)}">'
            f"{escape(stage.title)}</a></li>"
        )
    lines.extend(["  </ul>", "</section>", ""])
    return "\n".join(lines)


def prepare_cross_cutting_coverage_fragments(
    language: str, pages: list[dict[str, Any]], stages: Sequence[ResolvedGuidedRouteStage]
) -> dict[Path, str]:
    """Generate coverage partials without changing curriculum membership."""
    outputs: dict[Path, str] = {}
    includes = SITE / "includes"
    for page in pages:
        if page.get("covered_stages") and page["language"] == language:
            output = includes / f"generated-guided-coverage-{page['id'].replace('/', '-')}.qmd"
            outputs[output] = render_cross_cutting_coverage_markdown(page, stages, language)
    return outputs


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
        source_title = escape(transition.from_stage_title)
        target_title = escape(transition.to_stage_title)
        summary = f"{source_title} {arrow} {target_title}"
        stage_links = (
            f'<p class="guided-page-transitions__stages">'
            f'<a href="{source_href}">{source_title}</a> '
            f'{arrow} <a href="{target_href}">{target_title}</a></p>'
        )
        lines.extend(
            [
                '  <details class="guided-page-transitions__item">',
                f"    <summary>{summary}</summary>",
                f"    {stage_links}",
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
        "Le modèle",
        "The model",
    ),
    (
        "prediction",
        "text-input",
        "Prédire un token",
        "Predict a token",
    ),
    (
        "usages",
        "inference",
        "Utiliser et entraîner",
        "Use and train",
    ),
)
ROUTE_PART_BY_FIRST_STAGE: dict[str, tuple[str, str, str]] = {
    first_stage_id: (part_id, title_fr, title_en)
    for part_id, first_stage_id, title_fr, title_en in ROUTE_PARTS
}


def validate_route_projection(stages: list[ResolvedGuidedRouteStage]) -> None:
    """Guard the reader-facing three-part projection of the canonical route.

    The nine-stage registry (data/guided-route.yml) remains the canonical
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
        compact_title = stage.compact_title or stage.title
        full_label = f"{index:02d} · {stage.title}"
        lines.append(
            f'  <a class="guided-rail__stage" href="#guided-stage-{escape(stage.id)}" '
            f'title="{escape(stage.title, quote=True)}" '
            f'aria-label="{escape(full_label, quote=True)}" '
            f'data-stage-id="{escape(stage.id)}" data-stage-index="{index}">'
            f'<span class="guided-rail__number">{index:02d}</span>'
            f'<span class="guided-rail__title">{escape(compact_title)}</span></a>'
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


def concept_fragment(concept_id: str) -> str:
    """Use the map's existing concept selection state as a native link target."""
    return f"mode=concepts&concept={concept_id}"


@dataclass(frozen=True)
class ConceptualVisit:
    """The same short learning unit shown on the map and on its lesson."""

    page: ResolvedPage
    stage_id: str
    objects: tuple[str, ...]
    mobilizes: tuple[str, ...]
    outcome: str
    visit_label: str


def resolve_conceptual_visits(
    stages: list[ResolvedGuidedRouteStage],
    pages: list[dict[str, Any]],
    concepts: list[dict[str, Any]],
    computational_nodes: list[dict[str, Any]],
    language: str,
) -> list[ConceptualVisit]:
    """Resolve the objects studied and the ideas mobilized by each core visit."""
    page_by_id = {page["id"]: page for page in pages}
    objects = {
        f"concept:{concept['id']}": (
            concept["label"],
            {resource["id"] for resource in concept["resources"]},
            f"learning-map.html#{concept_fragment(concept['id'])}",
        )
        for concept in concepts
    }
    objects.update(
        {
            f"node:{node['id']}": (node["labels"][language], set(node.get("resources", [])), None)
            for node in computational_nodes
        }
    )
    fr = language == "fr"
    visit_labels = {
        "study": "",
        "preview": " (aperçu)" if fr else " (preview)",
        "revisit": " (reprise)" if fr else " (revisit)",
    }

    def resolve(reference: str, where: str, resource_id: str | None = None) -> str:
        if reference not in objects:
            raise ValueError(f"{where}: unknown conceptual object {reference!r}")
        label, resources, href = objects[reference]
        if resource_id is not None and resource_id not in resources:
            raise ValueError(f"{where}: {reference!r} does not list {resource_id!r} as a resource")
        label = escape_markdown_text(label)
        return f"[{label}]({href})" if href else label

    seen_objects: set[str] = set()
    visits: list[ConceptualVisit] = []
    for stage in stages:
        core_topics = [page_by_id[page.id]["topic"] for page in stage.pages]
        if (
            len(core_topics) != len(set(core_topics))
            or set(core_topics) != stage.conceptual_focus.keys()
        ):
            raise ValueError(
                f"{stage.id} ({language}): conceptual_focus must match the core topics "
                f"{core_topics!r}, found {sorted(stage.conceptual_focus)!r}"
            )
        for page, topic in zip(stage.pages, core_topics, strict=True):
            focus = stage.conceptual_focus[topic]
            if focus.visit == "revisit" and seen_objects.isdisjoint(focus.objects):
                raise ValueError(f"{stage.id}: revisited topic {topic!r} needs an earlier object")
            seen_objects.update(focus.objects)
            where = f"{stage.id}/{topic}"
            visits.append(
                ConceptualVisit(
                    page=page,
                    stage_id=stage.id,
                    objects=tuple(resolve(ref, where, page.id) for ref in focus.objects),
                    mobilizes=tuple(resolve(ref, where) for ref in focus.mobilizes),
                    outcome=escape_markdown_text(getattr(focus.outcome, language)),
                    visit_label=visit_labels[focus.visit],
                )
            )
    return visits


def render_conceptual_visit(visit: ConceptualVisit, *, link_lesson: bool) -> str:
    """Render mobilized concepts, studied objects and the learning outcome."""
    studied = " + ".join(visit.objects) + visit.visit_label
    mobilized = " + ".join(visit.mobilizes)
    chain = f"{mobilized} → {studied}" if mobilized else studied
    outcome = f"[{visit.outcome}]({visit.page.href})" if link_lesson else visit.outcome
    return f"{chain} · {outcome}"


def render_prediction_use_comparison(
    stages: Sequence[ResolvedGuidedRouteStage], language: str, *, stage_anchor_prefix: str = ""
) -> str:
    """Compare the treatment of context, parameters and predictions at each use."""
    fr = language == "fr"
    header = (
        "| Étape | Contexte $c$ | Paramètres $\\theta$ | Opération |"
        if fr
        else "| Stage | Context $c$ | Parameters $\\theta$ | Operation |"
    )
    parameter_labels = (
        {"fixed": "Fixés", "updated": "Mis à jour"}
        if fr
        else {"fixed": "Fixed", "updated": "Updated"}
    )
    phase_labels = (
        {"input": "Entrée", "output": "Sortie", "training": "Entraînement"}
        if fr
        else {"input": "Input", "output": "Output", "training": "Training"}
    )
    lines = [header, "|---|---|---|---|"]
    for stage in stages:
        if use := stage.prediction_use:
            title = escape_markdown_text(stage.compact_title or stage.title)
            link = f"[{title}](#{stage_anchor_prefix}{stage.id})"
            context = escape_markdown_text(getattr(use.context, language)).replace("|", r"\|")
            action = escape_markdown_text(getattr(use.action, language)).replace("|", r"\|")
            parameters = parameter_labels[use.parameters]
            phase = phase_labels[use.phase]
            lines.append(f"| {link} | {context} | {parameters} | **{phase}** · {action} |")
    upstream_note = (
        "Composer le contexte agit en amont. Les trois autres opérations utilisent "
        "la distribution produite. L'entraînement agrège les pénalités calculées sur les cibles "
        "observées, propage le gradient et applique une mise à jour."
        if fr
        else "Context design shapes the input. The other three operations use the distribution. "
        "Training aggregates penalties on observed targets, backpropagates the gradient, "
        "and applies an update."
    )
    return "\n".join([*lines, "", upstream_note, ""])


def render_conceptual_route(
    stages: list[ResolvedGuidedRouteStage],
    visits: list[ConceptualVisit],
    language: str,
    lesson_contracts: dict[str, ResolvedLessonContract],
) -> str:
    """Render three global moves, with the full visit skeleton on demand."""
    validate_route_projection(stages)
    stage_order = [stage.id for stage in stages]
    starts = [stage_order.index(stage_id) for _, stage_id, _, _ in ROUTE_PARTS]
    fr = language == "fr"
    lines: list[str] = []
    for (part_id, _, french, english), first, end in zip(
        ROUTE_PARTS, starts, [*starts[1:], len(stages)], strict=True
    ):
        stage_links: list[str] = []
        for stage in stages[first:end]:
            title = escape_markdown_text(stage.compact_title or stage.title)
            link = f"[{title}](#guided-stage-{stage.id})"
            stage_links.append(link)
            if (stage.prediction_use is not None) != (part_id == "usages"):
                raise ValueError(f"{stage.id}: prediction_use must match membership in uses")
        separator = " · " if part_id == "usages" else " → "
        parts = separator.join(stage_links)
        lines.append(f"- **{french if fr else english}** · {parts}")

    summary = "Comparer les usages" if fr else "Compare uses"
    lines.extend(
        [
            "",
            "<details>",
            f"<summary>{summary}</summary>",
            "",
            render_prediction_use_comparison(stages, language, stage_anchor_prefix="guided-stage-"),
            "</details>",
        ]
    )

    count = len({visit.page.id for visit in visits})
    label = f"Squelette des {count} leçons" if fr else f"Skeleton of the {count} lessons"
    lines.extend(["", "<details>", f"<summary>{label}</summary>", ""])
    review_label = "Fiche de révision" if fr else "Review sheet"
    for stage in stages:
        lines.extend([f"**{escape_markdown_text(stage.title)}**", ""])
        for visit in visits:
            if visit.stage_id != stage.id:
                continue
            line = "- " + render_conceptual_visit(visit, link_lesson=True)
            if contract := lesson_contracts.get(visit.page.id):
                line += f" · [{review_label}]({contract.synthesis.href})"
            lines.append(line)
        lines.append("")
    return "\n".join([*lines, "</details>", ""])


def render_lesson_skeleton(visits: list[ConceptualVisit], language: str) -> str:
    """Expose the map's local unit next to the lesson's route navigation."""
    fr = language == "fr"
    label = "Squelette de la leçon" if fr else "Lesson skeleton"
    map_label = "Voir le parcours" if fr else "See the path"
    lines = ["", "<details>", f"<summary>{label}</summary>", ""]
    lines.extend("- " + render_conceptual_visit(visit, link_lesson=False) for visit in visits)
    return "\n".join(
        [*lines, "", f"[{map_label}](learning-map.html#conceptual-route)", "", "</details>", ""]
    )


def prepare_guided_page_context_fragments(
    language: str,
    stages: list[ResolvedGuidedRouteStage],
    transitions: list[ResolvedGuidedRouteTransition] | None = None,
    lesson_contracts: dict[str, ResolvedLessonContract] | None = None,
    conceptual_visits: Sequence[ConceptualVisit] = (),
) -> dict[Path, str]:
    """Render membership, the lesson skeleton and transition context for route pages."""
    memberships = build_guided_route_memberships(stages)
    page_by_id = {
        page.id: page for stage in stages for page in [*stage.pages, *stage.optional_pages]
    }
    transition_index = build_guided_route_transition_index(transitions or [])
    visits_by_page: dict[str, list[ConceptualVisit]] = {}
    for visit in conceptual_visits:
        visits_by_page.setdefault(visit.page.id, []).append(visit)
    includes = SITE / "includes"
    outputs: dict[Path, str] = {}
    for page_id, page_memberships in memberships.items():
        page = page_by_id[page_id]
        output = includes / f"generated-guided-context-{page_id.replace('/', '-')}.qmd"
        membership = render_guided_page_context_markdown(page, page_memberships, language)
        transition_context = render_guided_page_transitions(
            transition_index.get(page_id, []), language
        )
        visits = visits_by_page.get(page_id)
        skeleton = render_lesson_skeleton(visits, language) if visits else ""
        review_link = ""
        if lesson_contracts and page_id in lesson_contracts:
            outcome_label = "Objectif de la leçon" if language == "fr" else "Lesson objective"
            label = "Réviser cette leçon" if language == "fr" else "Review this lesson"
            contract = lesson_contracts[page_id]
            outcome = escape_markdown_text(contract.outcome)
            href = contract.synthesis.href
            membership += f"\n**{outcome_label}.** {outcome}\n\n"
            review_link = f"\n[{label}]({href})\n\n"
        outputs[output] = membership + skeleton + transition_context + review_link
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
    "fr": "Parcours terminé · voie complémentaire : construire un GPT →",
    "en": "Path complete · optional companion path: build a GPT →",
}


def final_core_page_id(stages: Sequence[ResolvedGuidedRouteStage]) -> str | None:
    """Return the last core page of the guided route, where the route ends."""
    for stage in reversed(stages):
        if stage.pages:
            return stage.pages[-1].id
    return None


def build_suggested_route_contexts(
    stages: Sequence[ResolvedGuidedRouteStage],
) -> dict[str, list[dict[str, ResolvedPage | str | None]]]:
    """Project ordered stage membership into contextual previous/next neighbors.

    Stage order and page order are the canonical route. A page in several stages
    receives one neighbor pair per membership instead of an arbitrary global pair.
    Boundaries connect the last core page of one stage to the first core page of
    the adjacent stage; explanatory transitions remain a separate concept.
    """
    contexts: dict[str, list[dict[str, ResolvedPage | str | None]]] = {}
    for stage_index, stage in enumerate(stages):
        for page_index, page in enumerate(stage.pages):
            previous, previous_stage_title = (
                (stage.pages[page_index - 1], stage.title)
                if page_index > 0
                else (stages[stage_index - 1].pages[-1], stages[stage_index - 1].title)
                if stage_index > 0 and stages[stage_index - 1].pages
                else (None, None)
            )
            following, next_stage_title = (
                (stage.pages[page_index + 1], stage.title)
                if page_index + 1 < len(stage.pages)
                else (stages[stage_index + 1].pages[0], stages[stage_index + 1].title)
                if stage_index + 1 < len(stages) and stages[stage_index + 1].pages
                else (None, None)
            )
            contexts.setdefault(page.id, []).append(
                {
                    "stage_id": stage.id,
                    "stage_title": stage.title,
                    "previous": previous,
                    "previous_stage_title": previous_stage_title,
                    "next": following,
                    "next_stage_title": next_stage_title,
                }
            )
    return contexts


def render_suggested_route_markdown(
    page: dict[str, Any],
    page_by_id: dict[str, dict[str, Any]],
    language: str,
    *,
    completes_route: bool = False,
    sidebar_neighbors: dict[str, str] | None = None,
    preserve_pedagogical_cards: bool = False,
    stage_routes: Sequence[dict[str, ResolvedPage | str | None]] | None = None,
) -> str:
    """Render local previous/next links from the page's canonical suggested route.

    ``completes_route`` marks the last core page of the guided route. Its
    suggested route has no next page, so the reader would be left with a
    single backward link; it gets one optional companion-path card to Build.
    This cross-link does not make Build a required continuation of Understand.
    """
    if language not in {"fr", "en"}:
        raise ValueError(f"unsupported suggested-route language: {language!r}")

    route = page.get("route") or {}
    if stage_routes:
        cards: list[str] = []
        for context in stage_routes:
            for direction in ("previous", "next"):
                target = context.get(direction)
                if target is None:
                    continue
                stage_title = str(context[f"{direction}_stage_title"])
                if not isinstance(target, ResolvedPage):
                    raise ValueError(
                        f"invalid {direction} stage route for {page['id']!r}: {target!r}"
                    )
                if direction == "previous":
                    label = (
                        f"← Étape précédente · {stage_title}"
                        if language == "fr"
                        else f"← Previous · {stage_title}"
                    )
                else:
                    label = (
                        f"Continuer {stage_title} →"
                        if language == "fr"
                        else f"Continue {stage_title} →"
                    )
                href = str(target.href)
                if not href.endswith(".html"):
                    raise ValueError(f"route target has no published HTML href: {target.id!r}")
                source_href = f"{href[:-5]}.qmd"
                cards.extend(
                    [
                        f'  <a class="route-nav-card" href="{escape(source_href, quote=True)}">',
                        f'    <span class="nav-direction">{escape(label)}</span>',
                        f'    <span class="nav-title">{escape(str(target.title))}</span>',
                        "  </a>",
                    ]
                )
        if completes_route and page.get("route", {}).get("next") is None:
            companion_id = f"{language}/{ROUTE_CONTINUATION_PAGE}"
            companion = page_by_id.get(companion_id)
            if companion is not None:
                label = ROUTE_CONTINUATION_LABEL[language]
                href = str(companion.get("href", ""))
                if not href.endswith(".html"):
                    raise ValueError(f"route target has no published HTML href: {companion_id!r}")
                source_href = f"{href[:-5]}.qmd"
                cards.extend(
                    [
                        f'  <a class="route-nav-card" href="{escape(source_href, quote=True)}">',
                        f'    <span class="nav-direction">{escape(label)}</span>',
                        f'    <span class="nav-title">{escape(str(companion["title"]))}</span>',
                        "  </a>",
                    ]
                )
        if not cards:
            return ""
        return "\n".join(['<div class="route-nav-cards">', *cards, "</div>", ""])

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
        # Understand's guided route is an explicit pedagogical layer. Keep its
        # cards even when Quarto exposes the same destination in its footer:
        # the two navigation systems serve different purposes.
        if not preserve_pedagogical_cards and target_id == (sidebar_neighbors or {}).get(direction):
            continue
        target = page_by_id.get(target_id)
        if target is None:
            raise ValueError(f"unresolved {direction} route for {page['id']!r}: {target_id!r}")
        display_label = label
        if direction == "previous" and target_id == f"{language}/build-path":
            display_label = (
                "← Retour au parcours Build" if language == "fr" else "← Back to the Build path"
            )
        href = str(target.get("href", ""))
        if not href.endswith(".html"):
            raise ValueError(f"route target has no published HTML href: {target_id!r}")
        source_href = f"{href[:-5]}.qmd"
        cards.extend(
            [
                f'  <a class="route-nav-card" href="{escape(source_href, quote=True)}">',
                f'    <span class="nav-direction">{escape(display_label)}</span>',
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
    core_page_ids = {page.id for stage in stages for page in stage.pages}
    continuation_id = f"{language}/{ROUTE_CONTINUATION_PAGE}"
    sidebar_neighbors_by_page = load_sidebar_page_neighbors(language)
    stage_routes_by_page = build_suggested_route_contexts(stages)
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
            preserve_pedagogical_cards=page["id"] in core_page_ids,
            stage_routes=stage_routes_by_page.get(page["id"]),
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
    resource_registry_path = ROOT / "data" / "resources.yml"
    resource_registry = (
        load_yaml(resource_registry_path) if resource_registry_path.is_file() else {}
    )
    code_resources_by_concept: dict[str, list[dict[str, str]]] = {}
    for resource in resource_registry.get("resources", []):
        if resource.get("status") != "published":
            continue
        location = resource["location"]
        href = (
            f"https://github.com/JM-Brun/llm-lab/blob/main/{location['path']}"
            if location["type"] == "local"
            else location["url"]
        )
        for concept_id in resource.get("concepts", []):
            code_resources_by_concept.setdefault(concept_id, []).append(
                {
                    "id": resource["id"],
                    "label": resource["labels"][language],
                    "description": resource["descriptions"][language],
                    "href": href,
                    "programming_language": resource.get("programming_language", ""),
                }
            )
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
                "code_resources": code_resources_by_concept.get(item["id"], []),
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
    route_document = GuidedRouteDocument.model_validate(load_yaml(ROOT / "data/guided-route.yml"))
    lesson_contracts = (
        resolve_lesson_contracts(route_document, guided_route, pages)
        if route_document.lesson_contracts is not None
        else {}
    )
    navigation = load_navigation(language, pages)
    artifacts = prepare_guided_route_fragment(language, guided_route)
    visits: list[ConceptualVisit] = []
    if any(stage.conceptual_focus for stage in guided_route):
        computation = load_yaml(ROOT / "data" / "computational-graph.yml")
        visits = resolve_conceptual_visits(
            guided_route, pages, concept_graph["concepts"], computation["nodes"], language
        )
        artifacts[SITE / "includes" / f"generated-conceptual-route-{language}.qmd"] = (
            render_conceptual_route(guided_route, visits, language, lesson_contracts)
        )
    artifacts.update(
        prepare_guided_page_context_fragments(
            language, guided_route, guided_transitions, lesson_contracts, visits
        )
    )
    if lesson_contracts:
        boundary_exercises = resolve_boundary_exercises(
            route_document, guided_route, pages, language
        )
        artifacts[SITE / "includes" / f"generated-lesson-contracts-{language}.qmd"] = (
            render_lesson_contracts(guided_route, lesson_contracts, language, boundary_exercises)
        )
        artifacts.update(
            prepare_exercise_review_fragments(guided_route, boundary_exercises, language)
        )
    artifacts.update(prepare_cross_cutting_coverage_fragments(language, pages, guided_route))
    artifacts.update(prepare_suggested_route_fragments(language, pages, guided_route))
    payload = {
        "language": language,
        "source": "LLM-LAB-PAGE-MAP v1 + data/guided-route.yml + data/concepts.yml",
        "pages": pages,
        "navigation": navigation,
        **concept_graph,
    }
    artifacts.update(prepare_map_fragments(language, navigation, pages, payload))
    focus_concept_ids = {
        reference.removeprefix("concept:")
        for stage in guided_route
        for focus in stage.conceptual_focus.values()
        for reference in (*focus.objects, *focus.mobilizes)
        if reference.startswith("concept:")
    }
    if focus_concept_ids:
        # Place the link targets above the interactive map so native fragment
        # navigation scrolls to the graph along with setting its selection.
        anchor_ids = (
            escape(concept_fragment(item), quote=True) for item in sorted(focus_concept_ids)
        )
        anchors = "\n".join(f'<span id="{item}" aria-hidden="true"></span>' for item in anchor_ids)
        territory = SITE / "includes" / f"generated-map-territories-{language}.qmd"
        artifacts[territory] = f"```{{=html}}\n{anchors}\n```\n\n" + artifacts[territory]
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
