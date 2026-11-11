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
        "project:\n  render:\n"
        + "".join(f"    - fr/page-{index}.qmd\n" for index in range(60))
        + "\nwebsite:\n  title: Example\n"
    )
    files = [{"filename": f"site/fr/page-{index}.qmd", "status": "modified"} for index in range(49)]

    result = classify_changed_files(files, config)

    assert result["render_mode"] == "incremental"
    assert len(result["render_targets"]) == 49


def test_modified_static_images_can_be_copied_with_incremental_page_render():
    result = classify_changed_files(
        [
            {"filename": "site/fr/example.qmd", "status": "modified"},
            {"filename": "site/images/diagram.svg", "status": "modified"},
        ],
        CONFIG,
    )

    assert result["render_mode"] == "incremental"
    assert result["render_targets"] == ["site/fr/example.qmd"]
    assert result["render_assets"] == ["site/images/diagram.svg"]


def test_supported_static_image_extensions_are_incremental():
    for extension in (".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"):
        result = classify_changed_files(
            [{"filename": f"site/images/diagram{extension}", "status": "modified"}],
            CONFIG,
        )
        assert result["render_mode"] == "incremental"
        assert result["render_assets"] == [f"site/images/diagram{extension}"]


def test_multiple_modified_static_images_are_deduplicated_and_sorted():
    result = classify_changed_files(
        [
            {"filename": "site/en/example.qmd", "status": "modified"},
            {"filename": "site/images/z.svg", "status": "modified"},
            {"filename": "site/images/a.svg", "status": "modified"},
            {"filename": "site/images/z.svg", "status": "modified"},
        ],
        CONFIG,
    )

    assert result["render_mode"] == "incremental"
    assert result["render_assets"] == ["site/images/a.svg", "site/images/z.svg"]


def test_unsupported_assets_force_full_render():
    for path in (
        "site/images/diagram.css",
        "site/assets/diagram.svg",
    ):
        result = classify_changed_files(
            [
                {"filename": "site/fr/example.qmd", "status": "modified"},
                {"filename": path, "status": "modified"},
            ],
            CONFIG,
        )
        assert result["render_mode"] == "full"


def test_historical_four_page_two_svg_change_set_is_incremental():
    repository_root = Path(__file__).resolve().parents[2]
    config = (repository_root / "site" / "_quarto.yml").read_text(encoding="utf-8")
    changed_files = [
        {"filename": f"site/{language}/{page}.qmd", "status": "modified"}
        for language in ("en", "fr")
        for page in ("generation", "llm-overview")
    ] + [
        {
            "filename": f"site/images/llm-generation-process-{language}.svg",
            "status": "modified",
        }
        for language in ("en", "fr")
    ]

    result = classify_changed_files(changed_files, config)

    assert result["render_mode"] == "incremental"
    assert len(result["render_targets"]) == 4
    assert len(result["render_assets"]) == 2


def test_static_image_only_change_uses_copy_only_incremental_mode():
    result = classify_changed_files(
        [{"filename": "site/images/diagram.webp", "status": "modified"}],
        CONFIG,
    )

    assert result["render_mode"] == "incremental"
    assert result["render_targets"] == []
    assert result["render_assets"] == ["site/images/diagram.webp"]
    assert result["browser_relevant"] is False


def test_image_change_with_page_change_keeps_browser_audit_enabled():
    result = classify_changed_files(
        [
            {"filename": "site/fr/example.qmd", "status": "modified"},
            {"filename": "site/images/diagram.svg", "status": "modified"},
        ],
        CONFIG,
    )

    assert result["render_mode"] == "incremental"
    assert result["browser_relevant"] is True


def test_non_image_static_asset_keeps_browser_audit_enabled():
    result = classify_changed_files(
        [{"filename": "site/images/diagram.css", "status": "modified"}],
        CONFIG,
    )

    assert result["render_mode"] == "full"
    assert result["browser_relevant"] is True


def test_static_asset_paths_cannot_escape_the_images_directory():
    result = classify_changed_files(
        [
            {"filename": "site/fr/example.qmd", "status": "modified"},
            {"filename": "site/images/../../outside.svg", "status": "modified"},
        ],
        CONFIG,
    )

    assert result["render_mode"] == "full"
    assert result["render_assets"] == []


def test_added_or_deleted_static_image_forces_full_render():
    for status in ("added", "removed", "renamed"):
        result = classify_changed_files(
            [
                {"filename": "site/fr/example.qmd", "status": "modified"},
                {"filename": "site/images/diagram.svg", "status": status},
            ],
            CONFIG,
        )
        assert result["render_mode"] == "full"


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


def test_browser_audit_script_only_skips_quarto_render_but_keeps_browser_audit():
    result = classify_changed_files(
        [{"filename": "scripts/site-browser-review.mjs", "status": "modified"}], CONFIG
    )

    assert result["render_mode"] == "skip"
    assert result["site_relevant"] is False
    assert result["browser_relevant"] is True
    assert result["render_targets"] == []
    assert result["render_assets"] == []


def test_browser_audit_change_with_page_change_keeps_incremental_render_and_audit():
    result = classify_changed_files(
        [
            {"filename": "scripts/site-browser-review.mjs", "status": "modified"},
            {"filename": "site/en/learning/example.qmd", "status": "modified"},
        ],
        CONFIG,
    )

    assert result["render_mode"] == "incremental"
    assert result["site_relevant"] is True
    assert result["browser_relevant"] is True
    assert "site/en/learning/example.qmd" in result["render_targets"]
