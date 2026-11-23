"""Regression tests for the bilingual Q/K/V practice activity pilot."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
QKV_ACTIVITY_ANCHORS = {
    "ex-attention-scores-to-output",
    "ex-attention-manual-aggregation",
    "ex-attention-weighted-mixture-vs-selection",
    "ex-attention-project-qkv",
    "ex-attention-calculate-qkv-isolate-values",
    "ex-attention-predict-projection-change",
    "ex-attention-connect-projections-learning",
    "ex-attention-cross-attention-transfer",
}


def _source(language: str, relative_path: str) -> str:
    return (ROOT / "site" / language / relative_path).read_text(encoding="utf-8")


def _page_map(source: str) -> dict[str, Any]:
    match = re.search(
        r"<!--\s*LLM-LAB-PAGE-MAP v1\s*(.*?)\s*-->",
        source,
        re.DOTALL,
    )
    assert match is not None, "page must declare LLM-LAB-PAGE-MAP v1"
    payload = yaml.safe_load(match.group(1))
    assert isinstance(payload, dict)
    return payload


def _body_without_page_map(source: str) -> str:
    return re.sub(
        r"<!--\s*LLM-LAB-PAGE-MAP v1.*?-->",
        "",
        source,
        flags=re.DOTALL,
    )


def _markdown_targets(source: str) -> list[str]:
    return re.findall(r"\]\(([^)]+)\)", _body_without_page_map(source))


def _heading_anchors(source: str) -> list[str]:
    return re.findall(r"^#{2,6}\s+.*?\{#([^}]+)\}\s*$", source, re.MULTILINE)


def test_qkv_activity_anchors_are_stable_and_bilingual() -> None:
    french = _source("fr", "exercises-attention.qmd")
    english = _source("en", "exercises-attention.qmd")

    french_anchors = _heading_anchors(french)
    english_anchors = _heading_anchors(english)

    assert french_anchors == english_anchors
    assert len(french_anchors) == len(set(french_anchors))
    assert QKV_ACTIVITY_ANCHORS <= set(french_anchors)


def test_qkv_lesson_links_only_to_its_dedicated_practice_hub() -> None:
    for language in ("fr", "en"):
        lesson = _source(language, "queries-keys-values.qmd")
        targets = _markdown_targets(lesson)

        hub_links = [target for target in targets if target.endswith("exercises/queries-keys-values.qmd")]
        shared_collection_links = [
            target for target in targets if "exercises-attention.qmd" in target
        ]

        assert len(hub_links) == 1
        assert shared_collection_links == []


def test_qkv_practice_hub_is_the_boundary_to_the_shared_collection() -> None:
    for language in ("fr", "en"):
        lesson_id = f"{language}/queries-keys-values"
        hub_id = f"{language}/queries-keys-values-exercises"
        collection_id = f"{language}/exercises-attention"

        lesson = _page_map(_source(language, "queries-keys-values.qmd"))
        hub = _page_map(_source(language, "exercises/queries-keys-values.qmd"))
        collection = _page_map(_source(language, "exercises-attention.qmd"))

        assert hub_id in lesson["related"]
        assert collection_id not in lesson["related"]
        assert {lesson_id, collection_id} <= set(hub["related"])

        expected_collection_neighborhood = {
            lesson_id,
            f"{language}/scaled-dot-product-attention",
            f"{language}/causal-masking",
            f"{language}/attention-score-scaling",
            f"{language}/cross-attention",
            f"{language}/transformer-block-walkthrough",
        }
        assert expected_collection_neighborhood <= set(collection["related"])

        hub_targets = _markdown_targets(_source(language, "exercises/queries-keys-values.qmd"))
        assert any("exercises-attention.qmd#attention" in target for target in hub_targets)
