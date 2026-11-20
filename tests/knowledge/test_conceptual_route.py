"""Validate the learner-facing projection of canonical concepts and compute objects."""

import re
from html import escape

import pytest
from build_learning_map import (
    ROOT,
    SITE,
    load_concept_graph,
    load_guided_route,
    load_pages,
    prepare_build,
    render_conceptual_route,
)
from strict_yaml import load_yaml


@pytest.mark.parametrize(
    ("language", "preview", "revisit"),
    [("fr", "aperçu", "reprise"), ("en", "preview", "revisit")],
)
def test_conceptual_route_follows_core_visits_and_links_to_lessons_and_graph(
    language: str, preview: str, revisit: str
) -> None:
    path = SITE / "includes" / f"generated-conceptual-route-{language}.qmd"
    artifacts = prepare_build(language)
    projection = artifacts[path]
    stages = load_guided_route(language, load_pages())

    assert len(stages) == projection.count("<details>")
    start = projection.index(f" ({preview})](generation.html)")
    end = projection.index(f" ({revisit})](generation.html)")
    assert start < projection.index("](text-data.html)") < end
    assert end < projection.index("](context-engineering.html)")
    assert projection.count("](generation.html)") == 4
    assert "learning-map.html#mode=concepts&concept=autoregressive-generation" in projection
    assert "learning-map.html#mode=concepts&concept=prefill" in projection
    assert "learning-map.html#mode=concepts&concept=kv-cache" not in projection
    map_shell = artifacts[SITE / "includes" / f"generated-map-territories-{language}.qmd"]
    for fragment in re.findall(
        r"learning-map\.html#(mode=concepts&concept=[a-z0-9-]+)", projection
    ):
        assert f'id="{escape(fragment, quote=True)}"' in map_shell
    source = (SITE / language / "learning-map.qmd").read_text(encoding="utf-8")
    assert f"{{{{< include ../includes/{path.name} >}}}}" in source


@pytest.mark.parametrize(
    ("reference", "message"),
    [
        ("node:missing-object", "unknown conceptual object"),
        ("concept:token", "does not list 'fr/llm-overview' as a resource"),
    ],
)
def test_conceptual_route_checks_the_reference_and_its_supporting_page(
    reference: str, message: str
) -> None:
    pages = load_pages()
    stages = load_guided_route("fr", pages)
    concepts = load_concept_graph("fr", pages)["concepts"]
    nodes = load_yaml(ROOT / "data" / "computational-graph.yml")["nodes"]
    stages[0].conceptual_focus["llm-overview"].objects = [reference]
    with pytest.raises(ValueError, match=message):
        render_conceptual_route(stages, pages, concepts, nodes, "fr")
