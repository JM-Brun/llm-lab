"""Check stable evidence links for two reviewed Understand boundaries."""

from pathlib import Path

import pytest
from build_learning_map import GuidedRouteDocument, load_guided_route, load_pages, prepare_build
from page_index import load_published_pages
from project_index import _has_explicit_anchor
from strict_yaml import load_yaml

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"


@pytest.mark.parametrize("language", ["fr", "en"])
def test_boundary_evidence_resolves_to_core_and_published_practice(language: str) -> None:
    document = GuidedRouteDocument.model_validate(load_yaml(ROOT / "data/guided-route.yml"))
    concepts = load_yaml(ROOT / "data/concepts.yml")
    concept_ids = {concept["id"] for concept in concepts["concepts"]}
    pages = {page["id"]: page for page in load_pages() if page["language"] == language}
    site_pages = {page.page_id: page for page in load_published_pages(SITE)}
    stages = load_guided_route(language, list(pages.values()))
    core_ids_by_stage = {stage.id: {page.id for page in stage.pages} for stage in stages}
    fragment = SITE / "includes" / f"generated-lesson-contracts-{language}.qmd"
    plan = prepare_build(language)[fragment]
    assert document.boundaries

    for boundary_id, boundary in document.boundaries.items():
        transfer = boundary.transfer
        exercise_id = getattr(transfer.pages, language)
        assert pages[exercise_id]["destination"] == "practice", boundary_id
        assert _has_explicit_anchor(site_pages[exercise_id].source, transfer.anchor), (
            boundary_id,
            exercise_id,
        )
        href = f"{pages[exercise_id]['href']}#{transfer.anchor}"
        assert plan.count(f"]({href})") == len(boundary.explanations)

        for stage_id, explanation in boundary.explanations.items():
            lesson_id = getattr(explanation.pages, language)
            assert lesson_id in core_ids_by_stage[stage_id], (boundary_id, lesson_id)
            assert set(explanation.concept_ids) <= concept_ids, boundary_id
            section = plan.split(f"{{#{stage_id}}}", 1)[1].split("\n## ", 1)[0]
            before_lessons = section.split("\n### ", 1)[0]
            after_formula = before_lessons.partition("</details>")[2]
            assert f"[{getattr(transfer.label, language)}]({href})" in after_formula
