"""Tests for the guided route's page-to-stage membership projection."""

from __future__ import annotations

import html
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
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    memberships = GENERATOR["build_guided_route_memberships"](stages)

    stage_ids = [stage.id for stage in stages]
    assert stage_ids[0] == "orientation"
    assert len(stage_ids) == len(set(stage_ids))
    assert all(stage.pages for stage in stages)

    generation = memberships[f"{language}/generation"]
    assert [(item.stage_id, item.role) for item in generation] == [
        ("inference", "core"),
    ]

    context_use = memberships[f"{language}/in-context-learning"]
    assert [(item.stage_id, item.role) for item in context_use] == [("context-use", "core")]
    context_engineering = memberships[f"{language}/context-engineering"]
    assert [(item.stage_id, item.role) for item in context_engineering] == [("context-use", "core")]

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

    # Deep dives are discoverable from the stage where their question arises,
    # but remain optional and do not become prerequisites.
    expected_deep_dive_stages = {
        "llm-evolution": [("orientation", "optional")],
        "next-concept-modeling": [("orientation", "optional")],
        "sinusoidal-positional-encoding": [("representations", "optional")],
        "contextualized-representations-advanced": [("representations", "optional")],
        "embeddings-deep-dive": [("representations", "optional")],
        "queries-keys-values-advanced": [("computation", "optional")],
        "cross-attention": [("computation", "optional")],
        "multimodal-architectures": [("computation", "optional")],
        "hybrid-llm-architectures": [("computation", "optional")],
        "decoding-strategies": [("inference", "optional")],
        "llm-computational-complexity": [("inference", "optional")],
        "rag-memory-boundaries": [("context-use", "optional")],
        "document-retrieval": [("context-use", "optional")],
        "language-modeling-math": [("scoring", "optional")],
        "mathematical-foundations": [
            ("scoring", "optional"),
            ("training", "optional"),
        ],
        "score-centering": [("training", "optional")],
    }
    for slug, expected in expected_deep_dive_stages.items():
        page_id = f"{language}/{slug}"
        assert [(item.stage_id, item.role) for item in memberships[page_id]] == expected

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


@pytest.mark.parametrize(
    ("language", "expected_labels", "expected_parts"),
    [
        (
            "fr",
            [
                "Vue d\u2019ensemble",
                "Encoder",
                "Représenter",
                "Contextualiser",
                "Prédire",
                "Générer",
                "Adapter le contexte",
                "Scorer",
                "Entraîner",
            ],
            ["Le modèle", "Prédire un token", "Utiliser et entraîner"],
        ),
        (
            "en",
            [
                "Overview",
                "Encode",
                "Represent",
                "Contextualize",
                "Predict",
                "Generate",
                "Shape context",
                "Score",
                "Train",
            ],
            ["The model", "Predict a token", "Use and train"],
        ),
    ],
)
def test_guided_rail_uses_compact_labels_and_preserves_full_accessible_titles(
    language: str,
    expected_labels: list[str],
    expected_parts: list[str],
) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    rendered = GENERATOR["render_guided_rail"](stages, language)
    route_markdown = GENERATOR["render_guided_route_markdown"](stages, language)

    assert [stage.compact_title for stage in stages] == expected_labels
    assert all(
        f'<span class="guided-rail__title">{label}</span>' in rendered for label in expected_labels
    )
    assert all(f">{part}</span>" in rendered for part in expected_parts)
    assert all(f"## {part} {{.guided-route-part" in route_markdown for part in expected_parts)
    # The nav landmark has its own aria-label in addition to the stage links.
    assert rendered.count('title="') == len(stages)
    for index, stage in enumerate(stages, start=1):
        full_label = html.escape(f"{index:02d} · {stage.title}", quote=True)
        assert f'aria-label="{full_label}"' in rendered
        assert f'href="#guided-stage-{stage.id}"' in rendered


@pytest.mark.parametrize(
    ("language", "section_title", "end_title", "expected_labels"),
    [
        (
            "fr",
            '        - section: "Comprendre les LLM"',
            '        - section: "Réviser"',
            {
                "llm-overview": "Panorama LLM",
                "text-data": "Texte et tokens",
                "embedding-space": "Embeddings",
                "positional-encoding": "Position des tokens",
                "contextualized-representations": "États contextualisés",
                "transformer": "Transformer",
                "queries-keys-values": "Requêtes, clés, valeurs",
                "scaled-dot-product-attention": "Calcul de l\u2019attention",
                "causal-masking": "Masque causal",
                "logits": "Logits",
                "probabilites": "Probabilités",
                "entropy": "Entropie",
                "generation": "Génération",
                "in-context-learning": "Apprentissage en contexte",
                "context-engineering": "Ingénierie du contexte",
                "vraisemblance": "Vraisemblance",
                "cross-entropy": "Entropie croisée",
                "loss": "Fonction de perte",
                "gradients": "Gradients",
                "training-loop": "Boucle d\u2019entraînement",
            },
        ),
        (
            "en",
            '        - section: "Understand LLMs"',
            '        - section: "Review"',
            {
                "llm-overview": "LLM overview",
                "text-data": "Text and tokens",
                "embedding-space": "Embeddings",
                "positional-encoding": "Token positions",
                "contextualized-representations": "Contextualized states",
                "transformer": "Transformer",
                "queries-keys-values": "Queries, keys, values",
                "scaled-dot-product-attention": "Attention computation",
                "causal-masking": "Causal mask",
                "logits": "Logits",
                "probabilities": "Probabilities",
                "entropy": "Entropy",
                "generation": "Generation",
                "in-context-learning": "In-context learning",
                "context-engineering": "Context engineering",
                "likelihood": "Likelihood",
                "cross-entropy": "Cross-entropy",
                "loss": "Loss function",
                "gradients": "Gradients",
                "training-loop": "Training loop",
            },
        ),
    ],
)
def test_main_sidebar_uses_compact_bilingual_labels(
    language: str,
    section_title: str,
    end_title: str,
    expected_labels: dict[str, str],
) -> None:
    config = (ROOT / "site/_quarto.yml").read_text(encoding="utf-8")
    start = config.index(section_title)
    end = config.index(end_title, start + len(section_title))
    section = config[start:end]

    for slug, label in expected_labels.items():
        entry = f'            - text: "{label}"\n              href: {language}/{slug}.qmd'
        assert entry in section
