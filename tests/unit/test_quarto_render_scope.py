import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.quarto_render_scope import classify_changed_files


CONFIG = """project:
  type: website
  render:
    - fr/example.qmd
    - en/example.qmd
    - references.qmd

website:
  title: Example
"""


def test_modified_page_uses_incremental_render():
    result = classify_changed_files(
        [{"filename": "site/fr/example.qmd", "status": "modified"}], CONFIG
    )

    assert result["render_mode"] == "incremental"
    assert result["render_targets"] == ["site/fr/example.qmd"]
    assert result["browser_relevant"] is True


def test_multiple_modified_pages_are_rendered_incrementally():
    result = classify_changed_files(
        [
            {"filename": "site/fr/example.qmd", "status": "modified"},
            {"filename": "site/en/example.qmd", "status": "modified"},
        ],
        CONFIG,
    )

    assert result["render_mode"] == "incremental"
    assert len(result["render_targets"]) == 2


def test_deleted_or_added_page_forces_full_render():
    for status in ("added", "removed", "renamed"):
        result = classify_changed_files(
            [{"filename": "site/fr/example.qmd", "status": status}], CONFIG
        )
        assert result["render_mode"] == "full"


def test_global_configuration_and_shared_references_force_full_render():
    for path in (
        "site/_quarto.yml",
        "site/references.qmd",
        "site/styles.scss",
        ".github/workflows/publish-quarto.yml",
    ):
        result = classify_changed_files([{"filename": path, "status": "modified"}], CONFIG)
        assert result["render_mode"] == "full"


def test_unlisted_page_forces_full_render():
    result = classify_changed_files(
        [{"filename": "site/fr/not-listed.qmd", "status": "modified"}], CONFIG
    )
    assert result["render_mode"] == "full"


def test_more_than_twenty_pages_force_full_render():
    config = (
        "project:\n  render:\n"
        + "".join(f"    - fr/page-{index}.qmd\n" for index in range(21))
        + "\nwebsite:\n  title: Example\n"
    )
    files = [{"filename": f"site/fr/page-{index}.qmd", "status": "modified"} for index in range(21)]

    result = classify_changed_files(files, config)

    assert result["render_mode"] == "full"


def test_unrelated_changes_skip_site_render():
    result = classify_changed_files([{"filename": "README.md", "status": "modified"}], CONFIG)

    assert result["render_mode"] == "skip"
    assert result["site_relevant"] is False
