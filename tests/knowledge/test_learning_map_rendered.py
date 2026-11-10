"""Checks for the rendered map shell, including escaped-markup regressions."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "site/tools/check_learning_map_rendered.py"
SPEC = importlib.util.spec_from_file_location("check_learning_map_rendered", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


@pytest.mark.parametrize("language", ["en", "fr"])
def test_valid_map_has_real_localized_controls(tmp_path: Path, language: str) -> None:
    page = tmp_path / f"{language}.html"
    page.write_text(
        f'''<main><div data-learning-map data-language="{language}"
        data-source="../learning-map-data-{language}.json">
        <select data-map-mode><option value="pages">Pages</option>
        <option value="concepts">Concepts</option></select>
        <input type="search" data-map-search>
        <select data-map-relation-type></select>
        <button type="button" data-map-reset>Reset</button>
        <div data-map-viewport></div><div data-map-detail-panel></div>
        <p data-map-status></p></div></main>''',
        encoding="utf-8",
    )

    assert MODULE.inspect_page(page, language) == []


def test_escaped_inner_html_does_not_count_as_a_map(tmp_path: Path) -> None:
    page = tmp_path / "en.html"
    page.write_text(
        """<div data-learning-map data-language="en"
        data-source="../learning-map-data-en.json">
        <pre><code>&lt;select data-map-mode&gt;&lt;/select&gt;
        &lt;div data-map-viewport&gt;&lt;/div&gt;</code></pre></div>""",
        encoding="utf-8",
    )

    errors = MODULE.inspect_page(page, "en")
    assert any("data-map-mode" in error for error in errors)
    assert any("data-map-viewport" in error for error in errors)
