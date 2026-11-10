import importlib.util
from pathlib import Path

module_path = Path(__file__).resolve().parents[2] / "scripts" / "quarto_render_batch.py"
module_spec = importlib.util.spec_from_file_location("quarto_render_batch", module_path)
assert module_spec is not None and module_spec.loader is not None
module = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(module)
replace_project_render_targets = module.replace_project_render_targets


CONFIG = """project:
  type: website
  render:
    - fr/old.qmd
    - en/old.qmd

website:
  title: Example

format:
  html:
    toc: true
"""


def test_replaces_only_project_render_list_with_multiple_pages():
    result = replace_project_render_targets(
        CONFIG,
        ["site/fr/new.qmd", "site/en/new.qmd", "site/fr/new.qmd"],
    )

    assert result == CONFIG.replace(
        "    - fr/old.qmd\n    - en/old.qmd",
        '    - "fr/new.qmd"\n    - "en/new.qmd"',
    )
    assert "website:\n  title: Example" in result
    assert "format:\n  html:\n    toc: true" in result


def test_rejects_unsafe_or_empty_targets():
    for targets in ([], ["site/../outside.qmd"], ["site/styles.scss"], ["fr/page.qmd"]):
        try:
            replace_project_render_targets(CONFIG, targets)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected ValueError for {targets!r}")


def test_requires_existing_project_render_list():
    config = CONFIG.replace("  render:\n    - fr/old.qmd\n    - en/old.qmd\n", "")
    try:
        replace_project_render_targets(config, ["site/fr/new.qmd"])
    except ValueError as error:
        assert "project.render" in str(error)
    else:
        raise AssertionError("Expected a missing project.render list to fail")
