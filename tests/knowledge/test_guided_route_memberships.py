"""Validate the explicit page-to-stage membership projection."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
GENERATOR: dict[str, Any] = runpy.run_path(
    str(ROOT / "site/tools/build_learning_map.py"),
    run_name="guided_route_membership_test",
)



@pytest.mark.parametrize("language", ["fr", "en"])
def test_membership_projection_preserves_core_optional_and_multiple_contexts(
    language: str,
) -> None:
    pages = [
        page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}
    ]
    stages = GENERATOR["load_guided_route"](language, pages)
    memberships = GENERATOR["build_guided_route_memberships"](stages)

    assert [stage.id for stage in stages] == [
        "orientation",
        "text-input",
        "representations",
        "computation",
        "prediction",
        "inference",
        "scoring",
        "training",
    ]

    generation = memberships[f"{language}/generation"]
    assert [(item.stage_id, item.role) for item in generation] == [
        ("orientation", "core"),
        ("inference", "core"),
    ]

    text_input = memberships[f"{language}/text-data"]
    assert [(item.stage_id, item.role) for item in text_input] == [("text-input", "core")]

    tokenization = memberships[f"{language}/tokenization-strategies"]
    assert [(item.stage_id, item.role) for item in tokenization] == [("text-input", "optional")]

    entropy = memberships[f"{language}/entropy"]
    assert [(item.stage_id, item.role) for item in entropy] == [("prediction", "core")]

    likelihood = (
        memberships[f"{language}/vraisemblance"]
        if language == "fr"
        else memberships[f"{language}/likelihood"]
    )
    assert [(item.stage_id, item.role) for item in likelihood] == [("scoring", "core")]

    cross_entropy = memberships[f"{language}/cross-entropy"]
    assert [(item.stage_id, item.role) for item in cross_entropy] == [
        ("scoring", "core"),
        ("training", "optional"),
    ]

    # Training-example construction belongs to the independent Build path,
    # not to the conceptual Theory route.
    assert f"{language}/training-examples" not in memberships

    optional_page = f"{language}/transformer-architectures"
    assert [(item.stage_id, item.role) for item in memberships[optional_page]] == [
        ("orientation", "optional")
    ]

    core_page = f"{language}/embedding-space"
    assert [(item.stage_id, item.role) for item in memberships[core_page]] == [
        ("representations", "core")
    ]

    optional_attention_depth = f"{language}/attention-score-scaling"
    assert [(item.stage_id, item.role) for item in memberships[optional_attention_depth]] == [
        ("computation", "optional")
    ]

    assert f"{language}/build-path" not in memberships
    practice_page = (
        f"{language}/evaluation-experimentale"
        if language == "fr"
        else f"{language}/experimental-evaluation"
    )
    assert practice_page not in memberships


def test_membership_projection_keeps_empty_membership_absent() -> None:
    stages = [
        GENERATOR["ResolvedGuidedRouteStage"](
            id="one",
            title="Stage one",
            objective="An objective",
            pages=[GENERATOR["ResolvedPage"](id="en/core", title="Core", href="core.html")],
            optional_pages=[
                GENERATOR["ResolvedPage"](id="en/optional", title="Optional", href="optional.html")
            ],
        )
    ]

    memberships = GENERATOR["build_guided_route_memberships"](stages)

    assert set(memberships) == {"en/core", "en/optional"}
    assert memberships["en/core"][0].role == "core"
    assert memberships["en/optional"][0].role == "optional"
    assert "en/unassigned" not in memberships


@pytest.mark.parametrize("language", ["fr", "en"])
def test_guided_route_stage_anchors_are_stable(language: str) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    rendered = GENERATOR["render_guided_route_markdown"](stages, language)

    for stage in stages:
        assert f"#guided-stage-{stage.id}" in rendered


@pytest.mark.parametrize("language", ["fr", "en"])
def test_route_projection_parts_match_the_canonical_route(language: str) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)

    GENERATOR["validate_route_projection"](stages)

    rendered = GENERATOR["render_guided_route_markdown"](stages, language)
    for part_id in ("discover", "prediction", "usages"):
        assert f"#guided-part-{part_id}" in rendered


def test_single_membership_renders_as_context_not_as_a_parent_claim() -> None:
    membership = GENERATOR["GuidedRouteMembership"](
        stage_id="representations",
        stage_index=3,
        stage_title="From IDs to representations",
        stage_objective="Trace embedding lookup and contextualization.",
        role="optional",
    )
    page = GENERATOR["ResolvedPage"](
        id="en/rope", title="Rotary Position Embeddings", href="rope.html"
    )

    rendered = GENERATOR["render_guided_page_context_markdown"](page, [membership], "en")

    assert '<nav class="guided-page-context"' in rendered
    assert 'href="learning-map.html#guided-stage-representations"' in rendered
    assert "Rotary Position Embeddings" not in rendered
    assert 'class="guided-page-context__label">Learning path</span>' in rendered
    assert (
        'class="guided-page-context__stage" '
        'href="learning-map.html#guided-stage-representations"' in rendered
    )
    assert "03 · From IDs to representations" in rendered
    assert "Optional resource" in rendered


def test_multiple_memberships_are_all_rendered_with_their_purposes() -> None:
    memberships = [
        GENERATOR["GuidedRouteMembership"](
            stage_id="orientation",
            stage_index=1,
            stage_title="Orient yourself",
            stage_objective="Observe a complete generation loop.",
            role="core",
        ),
        GENERATOR["GuidedRouteMembership"](
            stage_id="prediction",
            stage_index=5,
            stage_title="From hidden states to predictions",
            stage_objective="Connect logits, probabilities and next-token selection.",
            role="core",
        ),
    ]
    page = GENERATOR["ResolvedPage"](
        id="en/generation", title="Text generation", href="generation.html"
    )

    rendered = GENERATOR["render_guided_page_context_markdown"](page, memberships, "en")

    assert "guided-page-context--multiple" in rendered
    assert "guided-stage-orientation" in rendered
    assert "guided-stage-prediction" in rendered
    assert "01 · Orient yourself" in rendered
    assert "05 · From hidden states to predictions" in rendered
    assert "Observe a complete generation loop." in rendered
    assert "Connect logits, probabilities and next-token selection." in rendered
    assert "Core stage" in rendered


def test_page_without_route_membership_has_no_context_fragment() -> None:
    page = GENERATOR["ResolvedPage"](
        id="en/build-path", title="Build a small GPT", href="build-path.html"
    )

    assert GENERATOR["render_guided_page_context_markdown"](page, [], "en") == ""


@pytest.mark.parametrize("language", ["fr", "en"])
def test_writer_generates_page_contexts_for_every_route_member(
    language: str, tmp_path: Path
) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    memberships = GENERATOR["build_guided_route_memberships"](stages)
    page_by_id = {
        page.id: page for stage in stages for page in [*stage.pages, *stage.optional_pages]
    }

    original_site = GENERATOR["SITE"]
    GENERATOR["SITE"] = tmp_path
    try:
        outputs = GENERATOR["write_guided_page_context_fragments"](language, stages)
    finally:
        GENERATOR["SITE"] = original_site

    assert len(outputs) == len(memberships)
    overview_id = f"{language}/llm-overview"
    generation_id = f"{language}/generation"
    output_by_name = {path.name: path for path in outputs}

    overview_filename = f"generated-guided-context-{overview_id.replace('/', '-')}.qmd"
    overview_file = output_by_name[overview_filename]
    generation_file = output_by_name[
        f"generated-guided-context-{generation_id.replace('/', '-')}.qmd"
    ]
    render_context = GENERATOR["render_guided_page_context_markdown"]
    assert overview_file.read_text(encoding="utf-8") == render_context(
        page_by_id[overview_id], memberships[overview_id], language
    )
    assert generation_file.read_text(encoding="utf-8") == render_context(
        page_by_id[generation_id], memberships[generation_id], language
    )


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Stage 4 of 8 · page 2 of 4"),
        ("fr", "Étape 4 sur 8 · page 2 sur 4"),
    ],
)
def test_core_page_context_states_position(language: str, expected: str) -> None:
    membership = GENERATOR["GuidedRouteMembership"](
        stage_id="computation",
        stage_index=4,
        stage_title="Computation",
        stage_objective="objective",
        role="core",
        stage_count=8,
        page_index=2,
        page_count=4,
    )
    page = GENERATOR["ResolvedPage"](id=f"{language}/qkv", title="QKV", href="qkv.html")

    rendered = GENERATOR["render_guided_page_context_markdown"](page, [membership], language)

    assert f'<span class="guided-page-context__position">{expected}</span>' in rendered


def test_optional_page_context_adds_no_position() -> None:
    membership = GENERATOR["GuidedRouteMembership"](
        stage_id="representations",
        stage_index=3,
        stage_title="Representations",
        stage_objective="objective",
        role="optional",
        stage_count=8,
    )
    page = GENERATOR["ResolvedPage"](id="en/rope", title="RoPE", href="rope.html")

    rendered = GENERATOR["render_guided_page_context_markdown"](page, [membership], "en")

    # The stage number is already in the stage cue; an optional page has no rank.
    assert "guided-page-context__position" not in rendered


def test_page_context_omits_position_it_does_not_know() -> None:
    membership = GENERATOR["GuidedRouteMembership"](
        stage_id="representations",
        stage_index=3,
        stage_title="Representations",
        stage_objective="objective",
        role="core",
    )
    page = GENERATOR["ResolvedPage"](id="en/x", title="X", href="x.html")

    rendered = GENERATOR["render_guided_page_context_markdown"](page, [membership], "en")

    assert "guided-page-context__position" not in rendered


@pytest.mark.parametrize("language", ["fr", "en"])
def test_real_route_positions_are_complete_and_consistent(language: str) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    memberships = GENERATOR["build_guided_route_memberships"](stages)

    for stage_index, stage in enumerate(stages, start=1):
        ranks = [
            membership.page_index
            for page in stage.pages
            for membership in memberships[page.id]
            if membership.role == "core" and membership.stage_index == stage_index
        ]
        assert ranks == list(range(1, len(stage.pages) + 1))
    for page_memberships in memberships.values():
        for membership in page_memberships:
            assert membership.stage_count == len(stages)
            assert (membership.page_count is None) == (membership.role == "optional")

    core_ids = {page.id for stage in stages for page in stage.pages}
    fragments = GENERATOR["prepare_guided_page_context_fragments"](language, stages)
    for path, text in fragments.items():
        page_id = path.name.removeprefix("generated-guided-context-").removesuffix(".qmd")
        page_id = page_id.replace("-", "/", 1)
        assert ("guided-page-context__position" in text) == (page_id in core_ids), path.name


@pytest.mark.parametrize("language", ["fr", "en"])
def test_guided_rail_links_every_stage_in_registry_order(language: str) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    rendered = GENERATOR["render_guided_rail"](stages, language)

    positions = [rendered.index(f'href="#guided-stage-{stage.id}"') for stage in stages]
    assert positions == sorted(positions)
    assert rendered.count('class="guided-rail__part"') == len(GENERATOR["ROUTE_PARTS"])
    assert "\\n" not in rendered
    assert 'data-guided-rail data-total="8"' in rendered
    assert 'data-guided-rail-progress hidden' in rendered
    part_positions = [
        rendered.index(f'data-part="{part_id}"') for part_id in ("discover", "prediction", "usages")
    ]
    assert part_positions == sorted(part_positions)
    disclaimer = (
        "stockée uniquement dans ce navigateur"
        if language == "fr"
        else "stored only in this browser"
    )
    assert disclaimer in rendered


def test_guided_rail_rejects_unknown_language() -> None:
    with pytest.raises(ValueError, match="unsupported guided-route language"):
        GENERATOR["render_guided_rail"]([], "de")


def test_guided_rail_escapes_stage_titles() -> None:
    stage = GENERATOR["ResolvedGuidedRouteStage"](
        id="safe-stage",
        title='<script>alert("x")</script>',
        objective="objective",
        pages=[],
    )
    rendered = GENERATOR["render_guided_rail"]([stage], "en")
    assert "&lt;script&gt;" in rendered
    assert "<script>" not in rendered


@pytest.mark.parametrize("language", ["fr", "en"])
def test_guided_route_fragment_places_rail_before_stage_anchors(
    language: str, tmp_path: Path
) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    original_site = GENERATOR["SITE"]
    GENERATOR["SITE"] = tmp_path
    try:
        artifacts = GENERATOR["prepare_guided_route_fragment"](language, stages)
    finally:
        GENERATOR["SITE"] = original_site
    rendered = next(iter(artifacts.values()))
    assert rendered.index('class="guided-rail"') < rendered.index("#guided-stage-orientation")
    assert "\\n" not in rendered


@pytest.mark.parametrize(("language", "label"), [("fr", "Étape 3/8"), ("en", "Stage 3/8")])
def test_page_context_renders_stage_badge_and_tracking_attributes(language: str, label: str) -> None:
    membership = GENERATOR["GuidedRouteMembership"](
        stage_id="representations",
        stage_index=3,
        stage_title="Representations",
        stage_objective="objective",
        role="core",
        stage_count=8,
        page_index=1,
        page_count=4,
    )
    page = GENERATOR["ResolvedPage"](
        id=f"{language}/embeddings", title="Embeddings", href="embeddings.html"
    )
    rendered = GENERATOR["render_guided_page_context_markdown"](page, [membership], language)

    assert label in rendered
    assert 'data-stage-id="representations"' in rendered
    assert 'data-stage-index="3"' in rendered
    assert 'data-stage-total="8"' in rendered


@pytest.mark.parametrize("language", ["fr", "en"])
def test_rail_and_page_context_use_identical_stage_ids(language: str) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    rail = GENERATOR["render_guided_rail"](stages, language)
    context = GENERATOR["render_guided_page_context_markdown"](
        stages[0].pages[0],
        GENERATOR["build_guided_route_memberships"](stages)[stages[0].pages[0].id],
        language,
    )

    assert 'href="#guided-stage-' + stages[0].id + '"' in rail
    assert 'data-stage-id="' + stages[0].id + '"' in context
