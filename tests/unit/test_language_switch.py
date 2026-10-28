"""Regression tests for the bilingual site's page-aware language switch."""

from __future__ import annotations

import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
SWITCH = SITE / "includes" / "language-switch.html"


def language_mapping() -> dict[str, str]:
    """Read the French-to-English page mapping from the switch script."""
    source = SWITCH.read_text(encoding="utf-8")
    block = re.search(
        r"const frenchToEnglish = \{(?P<body>.*?)\n  \};",
        source,
        flags=re.DOTALL,
    )
    assert block is not None, "Language switch mapping was not found"

    pairs = re.findall(
        r'^\s*"([^"]+)":\s*"([^"]+)",?\s*$',
        block.group("body"),
        flags=re.MULTILINE,
    )
    mapping = dict(pairs)
    assert len(mapping) == len(pairs), "Duplicate French slugs in language mapping"
    return mapping


def test_language_mapping_covers_all_french_pages() -> None:
    mapping = language_mapping()
    french_slugs = {page.stem for page in (SITE / "fr").glob("*.qmd")}

    assert set(mapping) == french_slugs, (
        "Every French page must have an explicit language-switch mapping. "
        f"Missing: {sorted(french_slugs - set(mapping))}; "
        f"stale: {sorted(set(mapping) - french_slugs)}"
    )


def test_language_mapping_covers_all_english_pages_except_homepage() -> None:
    mapping = language_mapping()
    english_slugs = {page.stem for page in (SITE / "en").glob("*.qmd") if page.stem != "index"}

    assert set(mapping.values()) == english_slugs, (
        "Every English content page must have exactly one French counterpart. "
        f"Missing: {sorted(english_slugs - set(mapping.values()))}; "
        f"stale: {sorted(set(mapping.values()) - english_slugs)}"
    )


def test_language_switch_targets_are_bijective_and_existing() -> None:
    mapping = language_mapping()

    assert len(set(mapping.values())) == len(mapping), (
        "Two French pages must not map to the same English page"
    )
    for french_slug, english_slug in mapping.items():
        assert (SITE / "fr" / f"{french_slug}.qmd").is_file()
        assert (SITE / "en" / f"{english_slug}.qmd").is_file()
