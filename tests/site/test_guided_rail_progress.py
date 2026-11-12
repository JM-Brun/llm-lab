from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_guided_progress_is_loaded_after_the_static_learning_map() -> None:
    quarto = (ROOT / "site" / "_quarto.yml").read_text(encoding="utf-8")
    includes = quarto.split("include-after-body:", 1)[1].split("\n    toc:", 1)[0]
    assert includes.index("includes/learning-map.html") < includes.index(
        "includes/guided-rail-progress.html"
    )


def test_guided_progress_uses_only_browser_local_storage() -> None:
    script = (ROOT / "site" / "includes" / "guided-rail-progress.html").read_text(encoding="utf-8")
    assert 'llm-lab:guided-progress:v1' in script
    assert "window.localStorage.getItem" in script
    assert "window.localStorage.setItem" in script
    assert "window.localStorage.removeItem" in script
    assert "fetch(" not in script
    assert "XMLHttpRequest" not in script


def test_guided_progress_handles_storage_failures_and_reset() -> None:
    script = (ROOT / "site" / "includes" / "guided-rail-progress.html").read_text(encoding="utf-8")
    assert "catch (error)" in script
    assert "if (progress === null || !writeProgress(progress)) return" in script
    assert "data-reset-label" in script
    assert "progress = []" in script


def test_guided_progress_styles_preserve_static_navigation_and_print() -> None:
    styles = (ROOT / "site" / "styles.scss").read_text(encoding="utf-8")
    assert ".guided-rail__stage" in styles
    assert ".guided-rail__progress[hidden]" in styles
    assert "@media print" in styles
    assert ".guided-rail__progress { display: none !important; }" in styles
