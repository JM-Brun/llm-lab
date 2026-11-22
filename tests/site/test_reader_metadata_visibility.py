"""Regression tests for reader-facing Quarto metadata visibility."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"


def test_editorial_keywords_remain_machine_readable_but_are_not_in_title_block() -> None:
    config = yaml.safe_load((SITE / "_quarto.yml").read_text(encoding="utf-8"))
    partials = config["format"]["html"]["template-partials"]

    assert "includes/title-metadata.html" in partials

    partial = (SITE / "includes" / "title-metadata.html").read_text(encoding="utf-8")
    assert "$if(keywords)$" not in partial
    assert 'class="keywords"' not in partial


def test_page_classification_tags_are_preserved_in_source_metadata() -> None:
    page = (SITE / "fr" / "learning-map.qmd").read_text(encoding="utf-8")

    assert '"type:entry-point"' in page
    assert '"destination:orient"' in page
    assert '"topic:learning-map"' in page
    assert '"level:overview"' in page
    assert '"language:fr"' in page
    assert '"status:published"' in page


def test_overview_questions_are_collected_on_the_dedicated_practice_pages() -> None:
    heading = re.compile(r"^## .+?\s+\{#([a-z0-9-]+)\}\s*$", re.MULTILINE)
    marker = re.compile(r"<!-- self-check-covers: ([^>]+) -->")
    for language in ("fr", "en"):
        lesson = (SITE / language / "llm-overview.qmd").read_text(encoding="utf-8")
        practice = (SITE / language / "exercises" / "llm-overview.qmd").read_text(encoding="utf-8")

        assert "::: {.self-check}" not in lesson
        assert "exercises/llm-overview.qmd" in lesson
        assert "<!-- self-check-coverage: enforced -->" in practice
        assert "::: {.self-check}" in practice
        major_headings = re.findall(r"^## (.+?)\\s*$", lesson, re.MULTILINE)
        sections = set(heading.findall(lesson))
        covered = {item for group in marker.findall(practice) for item in group.split()}
        assert major_headings
        assert len(sections) == len(major_headings), f"{language}: every major section needs an ID"
        assert sections == covered
