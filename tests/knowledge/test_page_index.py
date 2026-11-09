"""Tests for the shared published-page index and its projections."""

from __future__ import annotations

from pathlib import Path

import pytest
from export_knowledge_graph import BASE
from page_index import load_published_pages


def _write_page(
    site: Path, relative: str, page_id: str, language: str, *, content_language: str = "fr"
) -> None:
    path = site / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\ntitle: Example\nlang: {content_language}\n---\n\n"
        "<!--\nLLM-LAB-PAGE-MAP v1\n"
        f"id: {page_id}\ntags: ['language:{language}', 'status:published']\n-->\n",
        encoding="utf-8",
    )


def test_index_includes_root_and_shared_pages(tmp_path: Path) -> None:
    _write_page(tmp_path, "index.qmd", "fr/index", "fr")
    _write_page(tmp_path, "en/index.qmd", "en/index", "en", content_language="en")
    _write_page(tmp_path, "references.qmd", "reference/references", "shared")

    assert {page.page_id for page in load_published_pages(tmp_path)} == {
        "fr/index",
        "en/index",
        "reference/references",
    }


def test_export_urls_follow_source_paths(tmp_path: Path, monkeypatch) -> None:
    import export_knowledge_graph

    _write_page(tmp_path, "index.qmd", "fr/index", "fr")
    _write_page(tmp_path, "en/index.qmd", "en/index", "en", content_language="en")
    _write_page(tmp_path, "references.qmd", "reference/references", "shared")
    monkeypatch.setattr(export_knowledge_graph, "SITE", tmp_path)

    pages = export_knowledge_graph._page_records()

    assert pages["fr/index"]["url"] == f"{BASE}/index.html"
    assert pages["en/index"]["url"] == f"{BASE}/en/index.html"
    assert pages["reference/references"]["url"] == f"{BASE}/references.html"
    assert pages["reference/references"]["language"] == "fr"


def test_duplicate_published_ids_are_rejected(tmp_path: Path) -> None:
    _write_page(tmp_path, "first.qmd", "fr/example", "fr")
    _write_page(tmp_path, "second.qmd", "fr/example", "fr")

    with pytest.raises(ValueError, match="duplicate page ID 'fr/example'"):
        load_published_pages(tmp_path)


@pytest.mark.parametrize(
    "tags",
    [
        "['language:fr', 'status:publshed']",
        "['language:fr', 'status:published', 'status:retired']",
        "['language:fr', 'status:published', 'oops']",
    ],
)
def test_invalid_status_and_malformed_tags_are_rejected(tmp_path: Path, tags: str) -> None:
    (tmp_path / "example.qmd").write_text(
        "---\ntitle: Example\n---\n\n<!--\nLLM-LAB-PAGE-MAP v1\n"
        f"id: fr/example\ntags: {tags}\n-->\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=r"example\.qmd"):
        load_published_pages(tmp_path)


def test_duplicate_metadata_keys_are_rejected(tmp_path: Path) -> None:
    (tmp_path / "example.qmd").write_text(
        "---\ntitle: Example\n---\n\n<!--\nLLM-LAB-PAGE-MAP v1\n"
        "id: fr/first\nid: fr/example\n"
        "tags: ['language:fr', 'status:published']\n-->\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicate key 'id'") as error:
        load_published_pages(tmp_path)
    assert "example.qmd" in str(error.value)


def test_registry_validators_see_root_and_shared_pages(tmp_path: Path) -> None:
    import check_resource_registry

    _write_page(tmp_path / "site", "index.qmd", "fr/index", "fr")
    _write_page(tmp_path / "site", "references.qmd", "reference/references", "shared")

    assert check_resource_registry._published_page_ids(tmp_path) == {
        "fr/index",
        "reference/references",
    }


def test_files_quoting_the_marker_without_a_page_map_are_not_pages(tmp_path: Path) -> None:
    (tmp_path / "generated.qmd").write_text(
        '<script type="application/json">{"source":"LLM-LAB-PAGE-MAP v1 + data"}</script>\n',
        encoding="utf-8",
    )
    _write_page(tmp_path, "real.qmd", "fr/real", "fr")

    assert [page.page_id for page in load_published_pages(tmp_path)] == ["fr/real"]
