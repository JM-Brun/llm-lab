"""Check stable evidence links for reviewed Understand boundaries."""

from os.path import relpath
from pathlib import Path, PurePosixPath

import pytest
from build_learning_map import GuidedRouteDocument, load_guided_route, load_pages, prepare_build
from learning_map_renderers import escape_markdown_text
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
    artifacts = prepare_build(language)
    plan = artifacts[fragment]
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

        exercise_fragment = (
            SITE
            / "includes"
            / (f"generated-exercise-review-{exercise_id.replace('/', '-')}-{transfer.anchor}.qmd")
        )
        exercise_path = PurePosixPath(pages[exercise_id]["href"])
        review_href = ("../" * len(exercise_path.parent.parts)) + "review-path.html"
        stages_in_review_order = [stage for stage in stages if stage.id in boundary.explanations]
        return_links = " · ".join(
            f"[{escape_markdown_text(stage.title)}]({review_href}#{stage.id})"
            for stage in stages_in_review_order
        )
        label = "Reprendre la révision" if language == "fr" else "Return to the review plan"
        assert artifacts[exercise_fragment] == f"**{label}** · {return_links}\n"

        exercise = site_pages[exercise_id]
        include_path = relpath(exercise_fragment, exercise.path.parent)
        shortcode = "{{< include " + include_path + " >}}"
        assert exercise.source.count(shortcode) == 1, exercise_id
        exercise_body = exercise.source.split(f"{{#{transfer.anchor}}}", 1)[1]
        exercise_body = exercise_body.split("\n##", 1)[0]
        solution, closed, after_solution = exercise_body.partition("</details>")
        assert closed and shortcode in after_solution and shortcode not in solution, exercise_id

        for stage_id, explanation in boundary.explanations.items():
            lesson_id = getattr(explanation.pages, language)
            assert lesson_id in core_ids_by_stage[stage_id], (boundary_id, lesson_id)
            assert set(explanation.concept_ids) <= concept_ids, boundary_id
            section = plan.split(f"{{#{stage_id}}}", 1)[1].split("\n## ", 1)[0]
            before_lessons = section.split("\n### ", 1)[0]
            after_formula = before_lessons.partition("</details>")[2]
            assert f"[{getattr(transfer.label, language)}]({href})" in after_formula
