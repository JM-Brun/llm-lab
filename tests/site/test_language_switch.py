"""Regression tests for the bilingual site's page-aware language switch."""

import pathlib  # noqa: I001
import re
from urllib.parse import unquote, urlsplit


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


def test_optional_local_language_switch_blocks_are_consistent() -> None:
    """Validate local shortcuts when authored; the global navbar remains sufficient."""
    block_pattern = re.compile(
        r"(?ms)^:{3,}\s*\{\.language-switch\}\s*\n"
        r"(.*?)^:{3,}\s*$"
    )
    link_pattern = re.compile(r"\[([^]]+)\]\(([^)]+)\)")

    pages = sorted(
        path
        for language in ("fr", "en")
        for path in (SITE / language).rglob("*.qmd")
    )
    for page in pages:
        source = page.read_text(encoding="utf-8")
        blocks = list(block_pattern.finditer(source))
        assert source.count("{.language-switch}") == len(blocks), (
            f"{page.relative_to(SITE)}: every local language-switch block must use "
            "the canonical fenced-div wrapper"
        )
        for index, block in enumerate(blocks, start=1):
            where = f"{page.relative_to(SITE)} language-switch block {index}"
            body = block.group(1)
            links = link_pattern.findall(body)
            labels = [label.strip().casefold() for label, _ in links]

            assert set(labels) == {"français", "english"} and len(labels) == 2, (
                f"{where}: expected exactly one Français and one English link"
            )
            assert re.search(
                r"\*\*\s*(?:Langue|Language)\s*:\s*\*\*",
                body,
                flags=re.IGNORECASE,
            ), f"{where}: expected a localized Langue:/Language: label"

            for label, target in links:
                parsed = urlsplit(target.strip())
                assert not parsed.scheme and not parsed.netloc, (
                    f"{where}: language links must be relative source links"
                )
                target_path = (page.parent / unquote(parsed.path)).resolve()
                assert target_path.suffix == ".qmd" and target_path.is_file(), (
                    f"{where}: {label!r} target does not resolve to a Quarto source: {target!r}"
                )
                relative_target = target_path.relative_to(SITE.resolve())
                expected_language = "fr" if label.strip().casefold() == "français" else "en"
                assert relative_target.parts[0] == expected_language, (
                    f"{where}: {label!r} points to the wrong language tree: {target!r}"
                )
