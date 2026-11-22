"""Regression tests for reader-facing Quarto metadata visibility."""

from __future__ import annotations

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


def test_overview_questions_live_on_dedicated_practice_pages_in_both_languages() -> None:
    import re

    for language in ("fr", "en"):
        lesson = (SITE / language / "llm-overview.qmd").read_text(encoding="utf-8")
        practice_path = SITE / language / "exercises" / "llm-overview.qmd"
        practice = practice_path.read_text(encoding="utf-8")

        # The lesson explains the model; comprehension questions belong to its
        # dedicated companion page. Keep one visible, direct link in each language.
        assert "::: {.self-check}" not in lesson
        assert "<!-- self-check-coverage: enforced -->" not in lesson
        lesson_links = re.findall(
            r"(?m)^\[[^\]]+\]\(exercises/llm-overview\.qmd\)\s*$", lesson
        )
        assert len(lesson_links) == 1, f"{language}: expected one visible companion link"
        assert practice_path.is_file()
        assert re.search(r"(?m)^\[.*?\]\(\.\./llm-overview\.qmd\)", practice)

        questions = re.findall(r"(?m)^\d+\. \*\*", practice)
        assert len(questions) == 9, f"{language}: expected nine preserved overview questions"
