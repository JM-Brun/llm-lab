"""Regression tests for the canonical bilingual Understand running example."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

CORE_EXAMPLE_PAGES = (
    "llm-overview",
    "generation",
    "text-data",
    "embedding-space",
    "positional-encoding",
    "contextualized-representations",
)

FRENCH_EXAMPLE_FRAGMENTS = {
    "llm-overview": (
        "C'est une bonne situation, ça, scribe ?",
        "Vous savez, moi je ne crois pas",
    ),
    "generation": (
        "C'est une bonne situation, ça, scribe ?",
        "Vous savez, moi je ne crois pas",
    ),
    "text-data": (
        "C'est une bonne situation, ça, scribe ?",
        "Vous savez, moi je ne crois pas",
    ),
    "embedding-space": (
        "C'est une bonne situation, ça, scribe ?",
        "Vous savez, moi je ne crois pas",
    ),
    "positional-encoding": (
        "C'est une bonne situation, ça, scribe ?",
        "Vous savez, moi",
    ),
    "contextualized-representations": (
        "une bonne situation, ça, scribe ?",
        "de bonne ou de mauvaise situation",
        "moi je ne crois pas",
    ),
    "vraisemblance": (
        "C'est une bonne situation, ça, scribe ?",
        "Vous savez",
    ),
    "loss": ("Vous savez",),
    "exercises/contextualized-representations": (
        "une bonne situation, ça, scribe ?",
        "de bonne ou de mauvaise situation",
        "moi je ne crois pas",
    ),
}

ENGLISH_CONTINUATION = "They built roads between distant towns."


@pytest.mark.parametrize("page_id", tuple(FRENCH_EXAMPLE_FRAGMENTS))
def test_french_pages_reuse_relevant_fragments_naturally(page_id: str) -> None:
    source = (ROOT / "site" / "fr" / f"{page_id}.qmd").read_text(encoding="utf-8")
    for fragment in FRENCH_EXAMPLE_FRAGMENTS[page_id]:
        assert fragment in source, f"fr/{page_id} is missing {fragment!r}"


@pytest.mark.parametrize("page_id", CORE_EXAMPLE_PAGES)
def test_english_understand_pages_keep_their_own_running_example(page_id: str) -> None:
    source = (ROOT / "site" / "en" / f"{page_id}.qmd").read_text(encoding="utf-8")
    assert ENGLISH_CONTINUATION in source, f"en/{page_id} diverges from its running example"
