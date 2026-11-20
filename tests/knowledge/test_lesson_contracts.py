"""Protect the published core route and its revision navigation."""

from pathlib import Path

import pytest
from build_learning_map import (
    ROOT,
    SITE,
    GuidedRouteDocument,
    load_guided_route,
    load_pages,
    prepare_guided_page_context_fragments,
    render_lesson_contracts,
    resolve_lesson_contracts,
)
from strict_yaml import load_yaml


@pytest.fixture(scope="module")
def route_inputs():
    document = GuidedRouteDocument.model_validate(load_yaml(ROOT / "data/guided-route.yml"))
    all_pages = load_pages()
    inputs = {}
    for lang in ("fr", "en"):
        pages = [page for page in all_pages if page["language"] in {lang, "shared"}]
        inputs[lang] = load_guided_route(lang, pages), pages
    return document, inputs


def test_core_contracts_expose_objectives_and_link_bilingual_syntheses(
    route_inputs,
) -> None:
    document, inputs = route_inputs
    memberships = {}
    for lang, (stages, pages) in inputs.items():
        contracts = resolve_lesson_contracts(document, stages, pages)
        context = prepare_guided_page_context_fragments(lang, stages, lesson_contracts=contracts)
        plan = render_lesson_contracts(stages, contracts, lang)
        core_ids = {page.id for stage in stages for page in stage.pages}
        assert contracts.keys() == core_ids
        for page_id, contract in contracts.items():
            fragment = (
                SITE / "includes" / f"generated-guided-context-{page_id.replace('/', '-')}.qmd"
            )
            assert f"]({contract.synthesis.href})" in context[fragment]
            label = "Objectif de la leçon" if lang == "fr" else "Lesson objective"
            assert f"**{label}.** {contract.outcome}" in context[fragment]
            assert contract.outcome in plan
            assert plan.count(f"]({contract.synthesis.href})") == 1
            sheet = Path(SITE, lang, contract.synthesis.href).with_suffix(".qmd")
            source = sheet.read_text(encoding="utf-8")
            for anchor in ("revision-essentials", "revision-check"):
                assert f"{{#{anchor}}}" in source or f'id="{anchor}"' in source
            assert "<details>" in source
            assert "review-path.qmd" in source
        assert contracts[f"{lang}/generation"].stage == "inference"
        assert sum(page.id == f"{lang}/generation" for stage in stages for page in stage.pages) == 1
        topics = {page["id"]: page["topic"] for page in pages}
        memberships[lang] = [[topics[page.id] for page in stage.pages] for stage in stages]
    assert memberships["fr"] == memberships["en"]


@pytest.mark.parametrize("language", ["fr", "en"])
def test_review_plan_opens_with_plain_language_and_keeps_math_in_details(
    route_inputs, language: str
) -> None:
    document, inputs = route_inputs
    stages, pages = inputs[language]
    contracts = resolve_lesson_contracts(document, stages, pages)
    plan = render_lesson_contracts(stages, contracts, language)
    assert plan.count("<details>") == len(document.stages)

    for stage in document.stages:
        assert stage.overview is not None, stage.id
        overview = stage.overview
        section = plan.split(f"{{#{stage.id}}}", 1)[1].split("\n## ", 1)[0]
        introduction, disclosure = section.split("<details>", 1)
        formal, lessons = disclosure.split("</details>", 1)
        assert getattr(overview.question, language) in introduction
        assert getattr(overview.result, language) in introduction
        assert "$$" not in introduction
        assert f"$$\n{overview.signature}\n$$" in formal
        assert getattr(overview.criterion, language) in formal
        assert getattr(stage.objective, language) in formal
        assert "\n### " in lessons


@pytest.mark.parametrize("prerequisite", ["next-concept-modeling", "gradients", "text-data"])
def test_optional_future_and_self_dependencies_are_rejected(route_inputs, prerequisite) -> None:
    document, inputs = route_inputs
    invalid = document.model_copy(deep=True)
    assert invalid.lesson_contracts is not None
    invalid.lesson_contracts["text-data"].requires = [prerequisite]
    with pytest.raises(ValueError, match="must be acquired earlier in the core route"):
        resolve_lesson_contracts(invalid, *inputs["fr"])


def test_synthesis_requires_a_typed_revision_link(route_inputs) -> None:
    document, inputs = route_inputs
    stages, pages = inputs["fr"]
    broken = [
        dict(page, revision_of=[]) if page["id"] == "fr/revision-text-data" else page
        for page in pages
    ]
    with pytest.raises(ValueError, match=r"fr/text-data.*typed revision link"):
        resolve_lesson_contracts(document, stages, broken)
