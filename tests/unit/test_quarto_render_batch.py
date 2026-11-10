from pathlib import Path
import importlib.util
module_path = Path(__file__).resolve().parents[2] / "scripts" / "quarto_render_batch.py"
spec = importlib.util.spec_from_file_location("quarto_render_batch", module_path)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
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
def test_replaces_only_project_render_list():
    result = module.replace_project_render_targets(CONFIG, ["site/fr/new.qmd", "site/en/new.qmd", "site/fr/new.qmd"])
    assert result == CONFIG.replace("    - fr/old.qmd\n    - en/old.qmd", '    - "fr/new.qmd"\n    - "en/new.qmd"')
    assert "website:\n  title: Example" in result
    assert "format:\n  html:\n    toc: true" in result
def test_rejects_unsafe_or_empty_targets():
    for targets in ([], ["site/../outside.qmd"], ["site/styles.scss"], ["fr/page.qmd"]):
        try:
            module.replace_project_render_targets(CONFIG, targets)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected ValueError for {targets!r}")
def test_requires_existing_project_render_list():
    config = CONFIG.replace("  render:\n    - fr/old.qmd\n    - en/old.qmd\n", "")
    try:
        module.replace_project_render_targets(config, ["site/fr/new.qmd"])
    except ValueError as error:
        assert "project.render" in str(error)
    else:
        raise AssertionError("Expected missing project.render to fail")

def test_renderer_implementation_change_forces_full_site_validation():
    scope_path = Path(__file__).resolve().parents[2] / "scripts" / "quarto_render_scope.py"
    scope_spec = importlib.util.spec_from_file_location("quarto_render_scope", scope_path)
    assert scope_spec is not None and scope_spec.loader is not None
    scope = importlib.util.module_from_spec(scope_spec)
    scope_spec.loader.exec_module(scope)

    result = scope.classify_changed_files(
        [{"filename": "scripts/quarto_render_batch.py", "status": "modified"}],
        CONFIG,
    )
    assert result["site_relevant"] is True
    assert result["render_mode"] == "full"
