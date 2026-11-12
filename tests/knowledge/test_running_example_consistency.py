"""Regression tests for the canonical bilingual Understand running example."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

CANONICAL_CONTINUATIONS = {
    "fr": "Être scribe, c'est relier des histoires.",
    "en": "They built roads between distant towns.",
}
CORE_EXAMPLE_PAGES = (
    "llm-overview",
    "generation",
    "text-data",
    "embedding-space",
    "positional-encoding",
    "contextualized-representations",
)


@pytest.mark.parametrize(
    ("language", "continuation"),
    [
        ("fr", CANONICAL_CONTINUATIONS["fr"]),
        ("en", CANONICAL_CONTINUATIONS["en"]),
    ],
)
def test_understand_pages_reuse_one_canonical_continuation(
    language: str, continuation: str
) -> None:
    for page_id in CORE_EXAMPLE_PAGES:
        source = (ROOT / "site" / language / f"{page_id}.qmd").read_text(
            encoding="utf-8"
        )
        assert continuation in source, (
            f"{language}/{page_id} diverges from the running example"
        )


@pytest.mark.parametrize(
    "page_id",
    [
        "text-data",
        "embedding-space",
        "positional-encoding",
        "contextualized-representations",
    ],
)
def test_french_mechanism_pages_do_not_use_the_film_quote_as_the_target(
    page_id: str,
) -> None:
    source = (ROOT / "site" / "fr" / f"{page_id}.qmd").read_text(encoding="utf-8")
    assert "Vous savez, moi je ne crois pas" not in source
