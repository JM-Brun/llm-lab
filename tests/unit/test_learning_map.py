"""Unit tests for extracting and serializing the bilingual learning map."""

from __future__ import annotations

import json
import runpy
from pathlib import Path
from typing import Any

import pytest
import yaml

MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "build_learning_map.py"
MODULE: dict[str, Any] = runpy.run_path(str(MODULE_PATH), run_name="learning_map_test")

page_href = MODULE["page_href"]
clean_heading = MODULE["clean_heading"]
assign_route_rank = MODULE["assign_route_rank"]


def _write_page(
    site: Path,
    *,
    page_id: str,
    language: str,
    title: str,
    destination: str = "understand",
    topic: str = "attention",
    next_page: str | None = None,
    previous_page: str | None = None,
    children: list[str] | None = None,
    parents: list[str] | None = None,
    related: list[str] | None = None,
    domain: str | None = None,
    headings: tuple[str, ...] = ("## Core idea", "### Query, Key, Value"),
) -> None:
    """Create a minimal Quarto page carrying the repository page-map contract."""
    prefix, slug = page_id.split("/", maxsplit=1)
    path = site / (f"{slug}.qmd" if prefix == "reference" else f"{prefix}/{slug}.qmd")
    path.parent.mkdir(parents=True, exist_ok=True)
    tags = [
        "type:concept-lesson",
        f"destination:{destination}",
        f"topic:{topic}",
        "level:core",
        f"language:{language}",
        "status:published",
    ]
    front = {"title": title, "keywords": tags}
    metadata = {
        "id": page_id,
        "scope": "A concise scope.",
        "purpose": "A concise pedagogical purpose.",
        "suggested_route": {"previous": previous_page, "next": next_page},
        "hierarchy": {"parents": parents or [], "children": children or []},
        "related": related or [],
        "tags": tags,
    }
    if domain is not None:
        metadata["domain"] = domain
    front_yaml = yaml.safe_dump(front, allow_unicode=True, sort_keys=False).strip()
    metadata_yaml = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).strip()
    body = "\n".join(headings)
    page_content = "\n".join(
        [
            "---",
            front_yaml,
            "---",
            "",
            "<!--",
            "LLM-LAB-PAGE-MAP v1",
            metadata_yaml,
            "-->",
            "",
            body,
            "",
        ]
    )
    path.write_text(page_content, encoding="utf-8")


def _write_concept_registry(root: Path) -> None:
    """Write a minimal bilingual concept registry for generator tests."""
    data = {
        "schema_version": 1,
        "concepts": [
            {
                "id": "attention",
                "labels": {"fr": "Attention", "en": "Attention"},
                "definitions": {"fr": "Mécanisme.", "en": "Mechanism."},
                "resources": ["fr/attention", "en/attention"],
            },
            {
                "id": "query",
                "labels": {"fr": "Requête", "en": "Query"},
                "definitions": {"fr": "Projection.", "en": "Projection."},
                "resources": ["fr/attention", "en/attention"],
            },
        ],
        "relations": [{"from": "query", "type": "part-of", "to": "attention"}],
    }
    registry = root / "data" / "concepts.yml"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")


def _write_guided_route(
    root: Path,
    *,
    fr_core: list[str] | None = None,
    en_core: list[str] | None = None,
    fr_optional: list[str] | None = None,
    en_optional: list[str] | None = None,
) -> None:
    """Write a minimal versioned bilingual route source for generator tests."""
    source = {
        "schema_version": 1,
        "stages": [
            {
                "id": "orientation",
                "title": {"fr": "Situer le système", "en": "Orient yourself"},
                "objective": {"fr": "Observer le système.", "en": "Observe the system."},
                "pages": {
                    "fr": fr_core or ["fr/attention"],
                    "en": en_core or ["en/attention"],
                },
                "optional_pages": {
                    "fr": fr_optional or [],
                    "en": en_optional or [],
                },
            }
        ],
    }
    route = root / "data" / "guided-route.yml"
    route.parent.mkdir(parents=True, exist_ok=True)
    route.write_text(yaml.safe_dump(source, allow_unicode=True, sort_keys=False), encoding="utf-8")


def test_page_href_is_relative_to_language_map() -> None:
    assert page_href("fr/index", "fr") == "../index.html"
    assert page_href("fr/text-data", "fr") == "text-data.html"
    assert page_href("en/text-data", "fr") == "../text-data.html"
    assert page_href("reference/references", "en") == "../references.html"


def test_clean_heading_removes_lightweight_markdown() -> None:
    assert clean_heading("**Query**, _Key_ and `Value`") == "Query, Key and `Value`"
    assert clean_heading("  Attention mechanisms:  ") == "Attention mechanisms"


def test_load_pages_extracts_published_pages_and_section_headings(tmp_path: Path) -> None:
    site = tmp_path / "site"
    _write_page(
        site,
        page_id="fr/attention",
        language="fr",
        title="Attention",
        headings=(
            "## Intuition",
            "### **Query**, Key and Value",
            "## Objectifs d'apprentissage",
            "## Calcul des scores",
            "## Normalisation",
            "## Agrégation",
            "## Masqué",
            "## Additional heading is beyond the limit",
        ),
    )
    _write_page(
        site,
        page_id="en/attention",
        language="en",
        title="Attention",
        headings=("## Intuition", "## Query, Key and Value"),
    )

    MODULE["load_pages"].__globals__["SITE"] = site
    pages = MODULE["load_pages"]()

    assert [page["id"] for page in pages] == ["en/attention", "fr/attention"]
    french = next(page for page in pages if page["language"] == "fr")
    assert french["title"] == "Attention"
    assert french["href"] == "attention.html"
    assert french["scope"] == "A concise scope."
    assert french["purpose"] == "A concise pedagogical purpose."
    assert french["section_headings"] == [
        "Intuition",
        "Query, Key and Value",
        "Calcul des scores",
        "Normalisation",
        "Agrégation",
        "Masqué",
    ]


def test_assign_route_rank_follows_suggested_route_and_hierarchy() -> None:
    pages = [
        {
            "id": "fr/index",
            "route": {"next": "fr/text-data"},
            "children": ["fr/overview"],
        },
        {"id": "fr/text-data", "route": {"next": "fr/tokenization"}, "children": []},
        {"id": "fr/tokenization", "route": {"next": None}, "children": []},
        {"id": "fr/overview", "route": {"next": None}, "children": []},
        {"id": "fr/unlinked", "route": {"next": None}, "children": []},
    ]

    assign_route_rank(pages, "fr")

    ranks = {page["id"]: page["rank"] for page in pages}
    assert ranks == {
        "fr/index": 0,
        "fr/text-data": 1,
        "fr/overview": 2,
        "fr/tokenization": 3,
        "fr/unlinked": 4,
    }


def test_load_guided_route_resolves_language_specific_page_links(tmp_path: Path) -> None:
    route = tmp_path / "data" / "guided-route.yml"
    route.parent.mkdir(parents=True)
    route.write_text(
        """schema_version: 1
stages:
  - id: orientation
    title: {fr: "Situer le système", en: "Orient yourself"}
    objective: {fr: "Observer le système.", en: "Observe the system."}
    pages:
      fr: [fr/overview, fr/generation]
      en: [en/overview, en/generation]
    optional_pages:
      fr: [fr/tensors]
      en: [en/tensors]
""",
        encoding="utf-8",
    )
    MODULE["load_guided_route"].__globals__["ROOT"] = tmp_path
    pages = [
        {"id": "fr/overview", "title": "Panorama", "href": "overview.html"},
        {"id": "fr/generation", "title": "Génération", "href": "generation.html"},
        {"id": "fr/tensors", "title": "Tenseurs", "href": "tensors.html"},
    ]
    french = MODULE["load_guided_route"]("fr", pages)
    english = MODULE["load_guided_route"](
        "en",
        [
            {"id": "en/overview", "title": "Overview", "href": "overview.html"},
            {"id": "en/generation", "title": "Generation", "href": "generation.html"},
            {"id": "en/tensors", "title": "Tensors", "href": "tensors.html"},
        ],
    )

    assert french[0].id == "orientation"
    assert french[0].title == "Situer le système"
    assert [page.href for page in french[0].pages] == ["overview.html", "generation.html"]
    assert french[0].optional_pages[0].title == "Tenseurs"
    assert english[0].title == "Orient yourself"
    assert english[0].pages[0].href == "overview.html"
    assert english[0].optional_pages[0].title == "Tensors"


def test_load_guided_route_rejects_missing_published_page(tmp_path: Path) -> None:
    _write_guided_route(
        tmp_path,
        fr_core=["fr/not-published"],
        en_core=["en/not-published"],
    )
    MODULE["load_guided_route"].__globals__["ROOT"] = tmp_path

    with pytest.raises(ValueError, match="unpublished or missing core page"):
        MODULE["load_guided_route"]("fr", [])


def test_guided_route_schema_rejects_duplicate_or_unknown_fields() -> None:
    model = MODULE["GuidedRouteDocument"]
    valid_stage = {
        "id": "orientation",
        "title": {"fr": "Situer", "en": "Orient"},
        "objective": {"fr": "Observer.", "en": "Observe."},
        "pages": {"fr": ["fr/a"], "en": ["en/a"]},
    }
    with pytest.raises(ValueError, match="identifiers must be unique"):
        model.model_validate({"schema_version": 1, "stages": [valid_stage, valid_stage]})
    with pytest.raises(ValueError):
        model.model_validate({"schema_version": 1, "stages": [valid_stage], "unexpected": True})


def test_render_guided_route_markdown_uses_native_quarto_blocks() -> None:
    stage_model = MODULE["ResolvedGuidedRouteStage"]
    page_model = MODULE["ResolvedPage"]
    stage = stage_model(
        id="orientation",
        title="Situer le système",
        objective="Observer une génération.",
        pages=[page_model(id="fr/overview", title="Panorama", href="overview.html")],
        optional_pages=[page_model(id="fr/tensors", title="Tenseurs", href="tensors.html")],
    )

    markdown = MODULE["render_guided_route_markdown"]([stage], "fr")

    assert ":::: {.guided-route-grid}" in markdown
    assert "::: {.guided-route-stage}" in markdown
    assert "[Panorama](overview.html)" in markdown
    assert "**Approfondissements facultatifs**" in markdown
    assert "<ol" not in markdown
    assert "<a " not in markdown


def test_repository_guided_route_resolves_against_published_pages(monkeypatch) -> None:
    repository_root = MODULE_PATH.parents[1]
    monkeypatch.setitem(MODULE["load_pages"].__globals__, "SITE", repository_root / "site")
    monkeypatch.setitem(MODULE["load_guided_route"].__globals__, "ROOT", repository_root)
    published_pages = MODULE["load_pages"]()
    published_ids = {page["id"] for page in published_pages}

    for language in ("fr", "en"):
        stages = MODULE["load_guided_route"](language, published_pages)
        assert stages
        assert len({stage.id for stage in stages}) == len(stages)
        for stage in stages:
            assert stage.title and stage.objective
            assert all(page.id in published_ids for page in stage.pages)
            assert all(page.id in published_ids for page in stage.optional_pages)


def test_build_writes_language_specific_json(tmp_path: Path) -> None:
    site = tmp_path / "site"
    _write_page(site, page_id="fr/index", language="fr", title="Accueil", topic="overview")
    _write_page(site, page_id="fr/attention", language="fr", title="Attention")
    _write_page(site, page_id="en/index", language="en", title="Home", topic="overview")
    _write_page(site, page_id="en/attention", language="en", title="Attention")
    _write_guided_route(tmp_path)

    MODULE["build"].__globals__["SITE"] = site
    MODULE["build"].__globals__["ROOT"] = tmp_path
    _write_concept_registry(tmp_path)
    output = MODULE["build"]("fr")
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert output.name == "learning-map-data-fr.json"
    assert payload["language"] == "fr"
    assert payload["source"] == "LLM-LAB-PAGE-MAP v1 + data/guided-route.yml + data/concepts.yml"
    assert "guided_route" not in payload
    assert {page["id"] for page in payload["pages"]} == {"fr/index", "fr/attention"}
    assert all(page["href"] for page in payload["pages"])
    assert all(isinstance(page["section_headings"], list) for page in payload["pages"])
    fragment = site / "includes" / "generated-guided-route-fr.qmd"
    assert fragment.exists()
    assert "[Attention](attention.html)" in fragment.read_text(encoding="utf-8")
    assert payload["concepts"] == [
        {
            "id": "attention",
            "label": "Attention",
            "definition": "Mécanisme.",
            "resources": [{"id": "fr/attention", "title": "Attention", "href": "attention.html"}],
        },
        {
            "id": "query",
            "label": "Requête",
            "definition": "Projection.",
            "resources": [{"id": "fr/attention", "title": "Attention", "href": "attention.html"}],
        },
    ]
    assert payload["concept_relations"] == [{"from": "query", "type": "part-of", "to": "attention"}]


def test_load_pages_preserves_primary_deepen_domain(tmp_path: Path) -> None:
    site = tmp_path / "site"
    _write_page(
        site,
        page_id="fr/rope",
        language="fr",
        title="RoPE",
        destination="deepen",
        topic="rope",
        domain="architectures-mechanisms",
    )
    MODULE["load_pages"].__globals__["SITE"] = site

    pages = MODULE["load_pages"]()

    assert len(pages) == 1
    assert pages[0]["domain"] == "architectures-mechanisms"


def test_build_serializes_deepen_domain(tmp_path: Path) -> None:
    site = tmp_path / "site"
    _write_page(
        site,
        page_id="fr/index",
        language="fr",
        title="Accueil",
        topic="overview",
    )
    _write_page(
        site,
        page_id="fr/rope",
        language="fr",
        title="RoPE",
        destination="deepen",
        topic="rope",
        domain="architectures-mechanisms",
    )
    _write_page(site, page_id="en/index", language="en", title="Home", topic="overview")
    _write_guided_route(tmp_path, fr_core=["fr/rope"], en_core=["en/index"])
    MODULE["build"].__globals__["SITE"] = site
    MODULE["build"].__globals__["ROOT"] = tmp_path
    _write_concept_registry(tmp_path)

    output = MODULE["build"]("fr")
    payload = json.loads(output.read_text(encoding="utf-8"))
    rope = next(page for page in payload["pages"] if page["id"] == "fr/rope")

    assert rope["domain"] == "architectures-mechanisms"


def test_learning_map_browser_script_has_valid_javascript_and_fallback_target() -> None:
    """Catch syntax errors that would prevent the browser map from initializing."""
    import shutil
    import subprocess

    import pytest

    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is required for the inline browser-script syntax check.")

    script_path = MODULE_PATH.parents[1] / "site" / "includes" / "learning-map.html"
    source = script_path.read_text(encoding="utf-8")
    assert source.count("<script>") == 1
    script = source.split("<script>", maxsplit=1)[1].split("</script>", maxsplit=1)[0]
    result = subprocess.run(
        [node, "--check", "-"], input=script, text=True, capture_output=True, check=False
    )
    assert result.returncode == 0, result.stderr
    assert "conceptList.appendChild" not in script
    assert "sectionHeadingList.appendChild(item)" in script
