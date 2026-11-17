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


def test_generation_candidate_probabilities_form_a_distribution() -> None:
    source = (ROOT / "site" / "fr" / "generation.qmd").read_text(encoding="utf-8")
    assert "« savez » 0,5 · « êtes » 0,3 · « voyez » 0,2" in source
    assert "« savez » 0,6 · « êtes » 0,2 · « voyez » 0,2" not in source


def test_vraisemblance_reuses_generation_probabilities_and_product() -> None:
    source = (ROOT / "site" / "fr" / "vraisemblance.qmd").read_text(encoding="utf-8")
    assert "$0{,}6$ à « Vous »" in source
    assert "$0{,}5$ à « savez »" in source
    assert "$0{,}8$ à la virgule" in source
    assert "=0{,}6\\times0{,}5\\times0{,}8=0{,}24." in source


def test_loss_reuses_generation_probabilities_and_nll_values() -> None:
    source = (ROOT / "site" / "fr" / "loss.qmd").read_text(encoding="utf-8")
    assert "$0{,}6$, $0{,}5$ et $0{,}8$" in source
    assert r"\\ell_2=-\\ln(0{,}5)\\approx0{,}693" in source
    assert r"\\mathcal L=\\frac{0{,}511+0{,}693+0{,}223}{3}\\approx0{,}476" in source


@pytest.mark.parametrize("page_id", tuple(FRENCH_EXAMPLE_FRAGMENTS))
def test_french_pages_reuse_relevant_fragments_naturally(page_id: str) -> None:
    source = (ROOT / "site" / "fr" / f"{page_id}.qmd").read_text(encoding="utf-8")
    for fragment in FRENCH_EXAMPLE_FRAGMENTS[page_id]:
        assert fragment in source, f"fr/{page_id} is missing {fragment!r}"


@pytest.mark.parametrize("page_id", CORE_EXAMPLE_PAGES)
def test_english_understand_pages_keep_their_own_running_example(page_id: str) -> None:
    source = (ROOT / "site" / "en" / f"{page_id}.qmd").read_text(encoding="utf-8")
    assert ENGLISH_CONTINUATION in source, f"en/{page_id} diverges from its running example"
