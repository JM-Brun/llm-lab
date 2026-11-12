from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_probability_meta_flow_is_not_a_navigation_landmark() -> None:
    pages = (
        (ROOT / "site" / "fr" / "probabilites.qmd", "Des logits au token sélectionné"),
        (ROOT / "site" / "en" / "probabilities.qmd", "From logits to the selected token"),
    )
    for path, label in pages:
        source = path.read_text(encoding="utf-8")
        assert f'class="pipeline-stepper meta-flow" role="group" aria-label="{label}" aria-describedby="probability-flow-description"' in source
        assert '<p id="probability-flow-description" class="meta-flow__relation">' in source
        assert 'role="navigation"' not in source[source.index('class="pipeline-stepper meta-flow"'):source.index("</div>", source.index('class="pipeline-stepper meta-flow"'))]
