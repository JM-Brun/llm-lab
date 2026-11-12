"""Regression tests for process diagrams that are not navigation."""

from __future__ import annotations

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


def test_probability_meta_flow_is_not_a_navigation_landmark() -> None:
    pages = (
        (ROOT / "site" / "fr" / "probabilites.qmd", "Des logits au token sélectionné"),
        (ROOT / "site" / "en" / "probabilities.qmd", "From logits to the selected token"),
    )
    for path, label in pages:
        source = path.read_text(encoding="utf-8")
        group = (
            f'class="pipeline-stepper meta-flow" role="group" aria-label="{label}" '
            'aria-describedby="probability-flow-description"'
        )
        assert group in source
        assert '<p id="probability-flow-description" class="meta-flow__relation">' in source
        flow_start = source.index('class="pipeline-stepper meta-flow"')
        flow_end = source.index("</div>", flow_start)
        assert 'role="navigation"' not in source[flow_start:flow_end]


@pytest.mark.parametrize(
    "relative_path",
    [
        "fr/scaled-dot-product-attention.qmd",
        "en/scaled-dot-product-attention.qmd",
        "fr/causal-masking.qmd",
        "en/causal-masking.qmd",
        "fr/generation.qmd",
        "en/generation.qmd",
        "fr/transformer.qmd",
        "en/transformer.qmd",
    ],
)
def test_computation_diagrams_are_not_navigation_landmarks(relative_path: str) -> None:
    path = ROOT / "site" / relative_path
    source = path.read_text(encoding="utf-8")
    flow_start = source.index('class="pipeline-stepper"')
    flow_end = source.index("</div>", flow_start)
    assert 'role="group"' in source[flow_start:flow_end], path
    assert 'role="navigation"' not in source[flow_start:flow_end], path
