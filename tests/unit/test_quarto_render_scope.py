import importlib.util
from pathlib import Path

module_path = Path(__file__).resolve().parents[2] / "scripts" / "quarto_render_scope.py"
module_spec = importlib.util.spec_from_file_location("quarto_render_scope", module_path)
assert module_spec is not None and module_spec.loader is not None
module = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(module)
classify_changed_files = module.classify_changed_files


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


def test_large_safe_batch_stays_incremental():
    config = (
        "project:\\n  render:\\n"
        + "".join(f"    - fr/page-{index}.qmd\\n" for index in range(60))
        + "\\nwebsite:\\n  title: Example\\n"
    )
    files = [
        {"filename": f"site/fr/page-{index}.qmd", "status": "modified"}
        for index in range(49)
    ]

    result = classify_changed_files(files, config)

    assert result["render_mode"] == "incremental"
    assert len(result["render_targets"]) == 49


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
        "pyproject.toml",
        "uv.lock",
        "scripts/site-browser-review.mjs",
    ):
        result = classify_changed_files([{"filename": path, "status": "modified"}], CONFIG)
        assert result["render_mode"] == "full"


def test_unlisted_page_forces_full_render():
    result = classify_changed_files(
        [{"filename": "site/fr/not-listed.qmd", "status": "modified"}], CONFIG
    )
    assert result["render_mode"] == "full"


def test_more_than_sixty_pages_force_full_render():
    config = (
        "project:\n  render:\n"
        + "".join(f"    - fr/page-{index}.qmd\n" for index in range(61))
        + "\nwebsite:\n  title: Example\n"
    )
    files = [{"filename": f"site/fr/page-{index}.qmd", "status": "modified"} for index in range(61)]

    result = classify_changed_files(files, config)

    assert result["render_mode"] == "full"


def test_unrelated_changes_skip_site_render():
    result = classify_changed_files([{"filename": "README.md", "status": "modified"}], CONFIG)

    assert result["render_mode"] == "skip"
    assert result["site_relevant"] is False


def test_workflow_orchestration_and_scope_classifier_edits_skip_site_render():
    for path in (
        ".github/workflows/quarto.yml",
        ".github/workflows/publish-quarto.yml",
        "scripts/quarto_render_scope.py",
    ):
        result = classify_changed_files([{"filename": path, "status": "modified"}], CONFIG)
        assert result["render_mode"] == "skip"
        assert result["site_relevant"] is False
        assert result["browser_relevant"] is False
