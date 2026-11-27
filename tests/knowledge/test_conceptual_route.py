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
    resolve_conceptual_visits,
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

    overview, uses, details = projection.split("<details>")
    assert sum(line.startswith("- **") for line in overview.splitlines()) == 3
    assert (
        "](#guided-stage-inference) ·" in overview
        and "](#guided-stage-context-use) ·" in overview
        and "](#guided-stage-scoring) ·" in overview
    )
    rows = re.findall(
        r"^\| \[[^\n]+\]\(#guided-stage-([a-z-]+)\) \| .+? \| (.+?) \| \*\*(.+?)\*\*",
        uses,
        re.M,
    )
    fixed, updated = ("Fixés", "Mis à jour") if language == "fr" else ("Fixed", "Updated")
    entry, output, training = (
        ("Entrée", "Sortie", "Entraînement")
        if language == "fr"
        else ("Input", "Output", "Training")
    )
    assert rows == [
        ("inference", fixed, output),
        ("context-use", fixed, entry),
        ("scoring", fixed, output),
        ("training", updated, training),
    ]
    anchor = "compare-prediction-uses"
    plan = artifacts[SITE / "includes" / f"generated-lesson-contracts-{language}.qmd"]
    comparison = plan.split(f"{{#{anchor} .unlisted}}", 1)[1].split("\n## ", 1)[0].strip()
    map_table = uses.split("</summary>", 1)[1].split("</details>", 1)[0].strip()
    assert comparison == map_table.replace("](#guided-stage-", "](#")
    for stage_id, _, _ in rows:
        assert f"{{#{stage_id}}}" in plan

    overview_page = (SITE / language / "llm-overview.qmd").read_text(encoding="utf-8")
    choosing = overview_page.split("{#choosing-an-approach}", 1)[1].split("\n## ", 1)[0]
    assert f"](review-path.qmd#{anchor})" in choosing

    start = details.index(f" ({preview}) ·")
    end = details.index(f" ({revisit}) ·")
    assert start < details.index("](text-data.html)") < end
    assert end < details.index("](context-engineering.html)")
    assert details.count("](generation.html)") == 1
    assert details.count("](llm-overview.html)") == 1
    assert "learning-map.html#mode=concepts&concept=autoregressive-generation" in projection
    assert "learning-map.html#mode=concepts&concept=prefill" in projection
    assert "learning-map.html#mode=concepts&concept=kv-cache" not in projection
    map_shell = artifacts[SITE / "includes" / f"generated-map-territories-{language}.qmd"]
    for fragment in re.findall(
        r"learning-map\.html#(mode=concepts&concept=[a-z0-9-]+)", projection
    ):
        assert f'id="{escape(fragment, quote=True)}"' in map_shell
    rows = re.findall(
        r"^- (.+) · \[([^\n]+)\]\(([^/\n]+)\.html\) · \[[^\n]+\]\(([^/\n]+\.html)\)$",
        details,
        re.MULTILINE,
    )
    assert len(rows) == 21
    assert len({page_slug for _, _, page_slug, _ in rows}) == 21
    lesson_order = [page_slug for _, _, page_slug, _ in rows]
    assert lesson_order.index("language-representation") < lesson_order.index("text-data")
    assert next(sheet for _, _, lesson, sheet in rows if lesson == "entropy") == (
        "revision-entropy.html"
    )
    for chain, outcome, page_slug, synthesis in rows:
        fragment = SITE / "includes" / f"generated-guided-context-{language}-{page_slug}.qmd"
        local = artifacts[fragment]
        assert "(learning-map.html#conceptual-route)" in local
        assert f"{chain} · {outcome}" in local
        assert f"]({synthesis})" in local
    panorama = SITE / "includes" / f"generated-guided-context-{language}-llm-overview.qmd"
    generation = SITE / "includes" / f"generated-guided-context-{language}-generation.qmd"
    assert f" ({preview}) ·" in artifacts[panorama]
    assert f" ({revisit}) ·" in artifacts[generation]
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
        resolve_conceptual_visits(stages, pages, concepts, nodes, "fr")
