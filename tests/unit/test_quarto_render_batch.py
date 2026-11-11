from pathlib import Path

root = Path(__file__).resolve().parents[2]
batch = __import__("runpy").run_path(str(root / "scripts" / "quarto_render_batch.py"))
scope = __import__("runpy").run_path(str(root / "scripts" / "quarto_render_scope.py"))

CONFIG = """project:
  type: website
  render:
    - fr/old.qmd
    - en/old.qmd
    - fr/learning-map.qmd
    - en/learning-map.qmd

website:
  title: Example

format:
  html:
    toc: true
"""


def test_replaces_only_project_render_list():
    result = batch["replace_project_render_targets"](
        CONFIG,
        ["site/fr/new.qmd", "site/en/new.qmd", "site/fr/new.qmd"],
    )
    assert result == CONFIG.replace(
        "    - fr/old.qmd\n    - en/old.qmd\n    - fr/learning-map.qmd\n    - en/learning-map.qmd",
        '    - "fr/new.qmd"\n    - "en/new.qmd"',
    )
    assert "website:\n  title: Example" in result
    assert "format:\n  html:\n    toc: true" in result


def test_rejects_unsafe_or_empty_targets():
    targets = ([], ["site/../outside.qmd"], ["site/styles.scss"], ["fr/page.qmd"])
    for invalid_targets in targets:
        try:
            batch["replace_project_render_targets"](CONFIG, invalid_targets)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected ValueError for {invalid_targets!r}")


def test_requires_existing_project_render_list():
    config = CONFIG.replace(
        "  render:\n    - fr/old.qmd\n    - en/old.qmd\n"
        "    - fr/learning-map.qmd\n    - en/learning-map.qmd\n",
        "",
    )
    try:
        batch["replace_project_render_targets"](config, ["site/fr/new.qmd"])
    except ValueError as error:
        assert "project.render" in str(error)
    else:
        raise AssertionError("Expected missing project.render to fail")


def test_renderer_implementation_change_uses_cached_site_smoke_test():
    for status in ("added", "modified"):
        result = scope["classify_changed_files"](
            [{"filename": "scripts/quarto_render_batch.py", "status": status}],
            CONFIG,
        )
        assert result["site_relevant"] is True
        assert result["renderer_smoke_test"] is True
        assert result["render_mode"] == "incremental"
        assert result["render_targets"] == []


def test_renderer_change_keeps_safe_page_changes_incremental():
    result = scope["classify_changed_files"](
        [
            {"filename": "scripts/quarto_render_batch.py", "status": "modified"},
            {"filename": "scripts/quarto_render_scope.py", "status": "modified"},
            {"filename": "site/fr/old.qmd", "status": "modified"},
        ],
        CONFIG,
    )
    assert result["render_mode"] == "incremental"
    assert result["render_targets"] == ["site/fr/old.qmd"]


def test_renderer_file_deletion_or_rename_requires_full_validation():
    for status in ("removed", "renamed"):
        result = scope["classify_changed_files"](
            [{"filename": "scripts/quarto_render_batch.py", "status": status}],
            CONFIG,
        )
        assert result["render_mode"] == "full"
        assert result["renderer_smoke_test"] is False


def test_learning_map_generator_change_renders_all_consumers():
    result = scope["classify_changed_files"](
        [{"filename": "site/tools/build_learning_map.py", "status": "modified"}],
        CONFIG,
    )
    assert result["render_mode"] == "full"
    assert result["render_targets"] == []
    assert result["generate_learning_map"] is True
    assert result["browser_relevant"] is True


def test_learning_map_generator_removal_requires_full_validation():
    result = scope["classify_changed_files"](
        [{"filename": "site/tools/build_learning_map.py", "status": "removed"}],
        CONFIG,
    )
    assert result["render_mode"] == "full"


def test_rewrites_only_local_quarto_source_page_hrefs() -> None:
    document = (
        '<a href="deepen.qmd#transformer-resources">Local</a>'
        '<a href="../fr/exercises.qmd?mode=full#fondations">Relative</a>'
        '<a href="https://example.com/guide.qmd#external">External</a>'
        '<a href="#local-anchor">Fragment</a>'
        '<div data-href="untouched.qmd">Data attribute</div>'
        '<a href="document.pdf">Other file</a>'
    )

    rewritten = batch["rewrite_quarto_source_links"](document)

    assert 'href="deepen.html#transformer-resources"' in rewritten
    assert 'href="../fr/exercises.html?mode=full#fondations"' in rewritten
    assert 'href="https://example.com/guide.qmd#external"' in rewritten
    assert 'href="#local-anchor"' in rewritten
    assert 'data-href="untouched.qmd"' in rewritten
    assert 'href="document.pdf"' in rewritten


def test_rewrites_rendered_html_pages_before_overlay(tmp_path: Path) -> None:
    page = tmp_path / "fr" / "transformer.html"
    page.parent.mkdir()
    page.write_text(
        '<a href="deepen.qmd#transformer-resources">Resources</a>',
        encoding="utf-8",
    )
    non_html = tmp_path / "fr" / "source.txt"
    non_html.write_text('<a href="deepen.qmd">Not rendered HTML</a>', encoding="utf-8")

    changed_pages = batch["rewrite_rendered_html_links"](tmp_path)

    assert changed_pages == 1
    assert 'href="deepen.html#transformer-resources"' in page.read_text(encoding="utf-8")
    assert 'href="deepen.qmd"' in non_html.read_text(encoding="utf-8")
