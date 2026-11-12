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


def test_rendered_site_cache_is_not_indexed_as_authored_pages(tmp_path: Path) -> None:
    _write_page(tmp_path, "en/build-path.qmd", "en/build-path", "en", content_language="en")
    _write_page(
        tmp_path,
        "_site/en/build-path.qmd",
        "en/build-path",
        "en",
        content_language="en",
    )

    pages = load_published_pages(tmp_path)

    assert [(page.page_id, page.path.relative_to(tmp_path).as_posix()) for page in pages] == [
        ("en/build-path", "en/build-path.qmd")
    ]


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


def test_probability_meta_flow_is_not_a_navigation_landmark() -> None:
    root = Path(__file__).resolve().parents[2]
    pages = (
        (root / "site" / "fr" / "probabilites.qmd", "Des logits au token sélectionné"),
        (root / "site" / "en" / "probabilities.qmd", "From logits to the selected token"),
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
        "fr/positional-encoding.qmd",
        "en/positional-encoding.qmd",
        "fr/queries-keys-values.qmd",
        "en/queries-keys-values.qmd",
        "fr/training-loop.qmd",
        "en/training-loop.qmd",
        "fr/contextualized-representations.qmd",
        "en/contextualized-representations.qmd",
        "fr/cross-entropy.qmd",
        "en/cross-entropy.qmd",
        "fr/loss.qmd",
        "en/loss.qmd",
        "fr/gradients.qmd",
        "en/gradients.qmd",
        "fr/vraisemblance.qmd",
        "en/likelihood.qmd",
        "fr/entropy.qmd",
        "en/entropy.qmd",
        "fr/logits.qmd",
        "en/logits.qmd",
    ],
)
def test_computation_diagrams_do_not_mark_a_current_step(relative_path: str) -> None:
    root = Path(__file__).resolve().parents[2]
    source = (root / "site" / relative_path).read_text(encoding="utf-8")
    flow_start = source.index("pipeline-stepper")
    div_end = source.find("\n</div>", flow_start)
    fence_end = source.find("\n::::", flow_start)
    flow_ends = [end for end in (div_end, fence_end) if end >= 0]
    flow_end = min(flow_ends)
    flow = source[flow_start:flow_end]
    assert 'role="group"' in flow
    assert 'role="navigation"' not in flow
    assert 'aria-current="step"' not in flow


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
        "fr/text-data.qmd",
        "en/text-data.qmd",
    ],
)
def test_computation_diagrams_are_not_navigation_landmarks(relative_path: str) -> None:
    root = Path(__file__).resolve().parents[2]
    path = root / "site" / relative_path
    source = path.read_text(encoding="utf-8")
    flow_start = source.index('class="pipeline-stepper"')
    flow_end = source.index("</div>", flow_start)
    assert 'role="group"' in source[flow_start:flow_end], path
    assert 'role="navigation"' not in source[flow_start:flow_end], path
    assert 'aria-current="step"' not in source[flow_start:flow_end], path
