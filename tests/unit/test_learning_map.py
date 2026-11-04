"""Unit tests for extracting and serializing the bilingual learning map."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import runpy

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
    import yaml

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
    front_yaml = yaml.safe_dump(front, allow_unicode=True, sort_keys=False).strip()
    metadata_yaml = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).strip()
    body = "\n".join(headings)
    path.write_text(
        f"---\n{front_yaml}\n---\n\n<!--\nLLM-LAB-PAGE-MAP v1\n"
        f"{metadata_yaml}\n-->\n\n{body}\n",
        encoding="utf-8",
    )


def test_page_href_is_relative_to_language_map() -> None:
    assert page_href("fr/index", "fr") == "../index.html"
    assert page_href("fr/text-data", "fr") == "text-data.html"
    assert page_href("en/text-data", "fr") == "../text-data.html"
    assert page_href("reference/references", "en") == "../references.html"


def test_clean_heading_removes_lightweight_markdown() -> None:
    assert clean_heading("**Query**, _Key_ and `Value`") == "Query, Key and `Value`"
    assert clean_heading("  Attention mechanisms:  ") == "Attention mechanisms"


def test_load_pages_extracts_published_pages_and_heading_concepts(tmp_path: Path) -> None:
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

    MODULE["SITE"] = site
    pages = MODULE["load_pages"]()

    assert [page["id"] for page in pages] == ["en/attention", "fr/attention"]
    french = next(page for page in pages if page["language"] == "fr")
    assert french["title"] == "Attention"
    assert french["href"] == "attention.html"
    assert french["scope"] == "A concise scope."
    assert french["purpose"] == "A concise pedagogical purpose."
    assert french["concepts"] == [
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


def test_build_writes_language_specific_json(tmp_path: Path) -> None:
    site = tmp_path / "site"
    _write_page(site, page_id="fr/index", language="fr", title="Accueil", topic="overview")
    _write_page(site, page_id="fr/attention", language="fr", title="Attention")
    _write_page(site, page_id="en/index", language="en", title="Home", topic="overview")
    _write_page(site, page_id="en/attention", language="en", title="Attention")

    MODULE["SITE"] = site
    output = MODULE["build"]("fr")
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert output.name == "learning-map-data-fr.json"
    assert payload["language"] == "fr"
    assert payload["source"] == "LLM-LAB-PAGE-MAP v1"
    assert {page["id"] for page in payload["pages"]} == {"fr/index", "fr/attention"}
    assert all(page["href"] for page in payload["pages"])
    assert all(isinstance(page["concepts"], list) for page in payload["pages"])
