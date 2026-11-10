"""Stable, language-neutral anchors for in-page exercise references."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

SITE = Path(__file__).resolve().parents[2] / "site"
COLLECTIONS = ("attention", "foundations", "generation", "text-data", "transformer")


@pytest.mark.parametrize("collection", COLLECTIONS)
def test_exercise_anchor_ids_are_stable_and_bilingual(collection: str) -> None:
    """Exercise anchors are descriptive, collection-scoped, and shared by FR/EN."""
    identifiers: dict[str, list[str]] = {}
    for language in ("fr", "en"):
        path = SITE / language / f"exercises-{collection}.qmd"
        source = path.read_text(encoding="utf-8")
        exercise_ids = [
            match.group(1) or match.group(2)
            for match in re.finditer(
                r"^#{3} .+?\{#([^}]+)\}\s*$|<a id=\"(ex-[^\"]+)\"></a>",
                source,
                flags=re.MULTILINE,
            )
        ]
        exercise_ids = [
            identifier for identifier in exercise_ids if identifier.startswith(f"ex-{collection}-")
        ]
        exercise_headings = re.findall(r"^#{3} (.+)$", source, flags=re.MULTILINE)
        assert all(
            not re.search(r"\b(?:TR-[A-Z]|CA-A|AT-[ABC]|GE-[A-E]|TF-[ABC])\b", title)
            for title in exercise_headings
        )
        assert exercise_ids, f"{path.relative_to(SITE)}: no explicit exercise anchors"
        assert all(identifier.startswith(f"ex-{collection}-") for identifier in exercise_ids)
        assert len(exercise_ids) == len(set(exercise_ids)), (
            f"{path.relative_to(SITE)}: duplicate IDs"
        )
        identifiers[language] = exercise_ids

    assert identifiers["fr"] == identifiers["en"], (
        f"{collection}: French and English exercise anchors must match in the same order"
    )
