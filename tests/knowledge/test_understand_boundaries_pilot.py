"""Check stable evidence links for two reviewed Understand boundaries."""

from pathlib import Path

import pytest
from build_learning_map import load_guided_route, load_pages
from page_index import load_published_pages
from project_index import _has_explicit_anchor
from strict_yaml import load_yaml

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"


@pytest.mark.parametrize("language", ["fr", "en"])
def test_boundary_evidence_resolves_to_core_and_published_practice(language: str) -> None:
    pilot = load_yaml(ROOT / "docs/meta/understand-boundaries-pilot.yml")
    concepts = load_yaml(ROOT / "data/concepts.yml")
    concept_ids = {concept["id"] for concept in concepts["concepts"]}
    pages = {page["id"]: page for page in load_pages() if page["language"] == language}
    site_pages = {page.page_id: page for page in load_published_pages(SITE)}
    stages = load_guided_route(language, list(pages.values()))
    core_ids_by_stage = {stage.id: {page.id for page in stage.pages} for stage in stages}

    for boundary_id, boundary in pilot["boundaries"].items():
        for stage_id, explanation in boundary["explanations"].items():
            lesson_id = explanation["pages"][language]
            assert lesson_id in core_ids_by_stage[stage_id], (boundary_id, lesson_id)
            assert set(explanation["concept_ids"]) <= concept_ids, boundary_id

        transfer = boundary["transfer"]
        exercise_id = transfer["pages"][language]
        assert pages[exercise_id]["destination"] == "practice", boundary_id
        assert _has_explicit_anchor(site_pages[exercise_id].source, transfer["anchor"]), (
            boundary_id,
            exercise_id,
        )
