"""Keep the tracked learning-map artifacts synchronized with their canonical inputs."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
GENERATOR: dict[str, Any] = runpy.run_path(
    str(ROOT / "site/tools/build_learning_map.py"), run_name="map_artifacts_freshness_test"
)
RENDERERS: dict[str, Any] = runpy.run_path(
    str(ROOT / "site/tools/learning_map_renderers.py"), run_name="map_artifacts_freshness_test"
)


def _published_pages(language: str) -> list[dict[str, Any]]:
    return [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]


@pytest.mark.parametrize("language", ["fr", "en"])
def test_tracked_map_list_matches_canonical_sidebar(language: str) -> None:
    """The static map list reflects the authored Quarto sidebar, not a stale copy (LM-16)."""
    pages = _published_pages(language)
    navigation = GENERATOR["load_navigation"](language, pages)
    expected = RENDERERS["render_resource_list"](
        language, navigation, {page["id"]: page for page in pages}
    )
    fragment = ROOT / "site" / "includes" / f"generated-map-list-{language}.qmd"

    assert fragment.is_file(), f"Missing tracked map list: {fragment}"
    assert fragment.read_text(encoding="utf-8") == expected, (
        f"Stale map list: {fragment}. Regenerate with "
        "uv run --no-project --with-requirements docs/requirements-history-validation.txt "
        "--python 3.12 python site/tools/build_learning_map.py"
    )


@pytest.mark.parametrize("language", ["fr", "en"])
def test_tracked_map_territories_match_renderer(language: str) -> None:
    """The interactive map shell stays locked to the renderer output (LM-16)."""
    expected = RENDERERS["render_territory_map"](language, [], {})
    fragment = ROOT / "site" / "includes" / f"generated-map-territories-{language}.qmd"

    assert fragment.is_file(), f"Missing tracked map territories: {fragment}"
    assert fragment.read_text(encoding="utf-8") == expected, (
        f"Stale map territories: {fragment}. Regenerate with "
        "uv run --no-project --with-requirements docs/requirements-history-validation.txt "
        "--python 3.12 python site/tools/build_learning_map.py"
    )
