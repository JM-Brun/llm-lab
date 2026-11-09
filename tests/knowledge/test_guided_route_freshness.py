"""Keep the tracked guided routes synchronized with their canonical inputs."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
GENERATOR: dict[str, Any] = runpy.run_path(
    str(ROOT / "site/tools/build_learning_map.py"), run_name="guided_route_freshness_test"
)


@pytest.mark.parametrize("language", ["fr", "en"])
def test_tracked_guided_route_matches_canonical_sources(language: str) -> None:
    pages = [page for page in GENERATOR["load_pages"]() if page["language"] in {language, "shared"}]
    stages = GENERATOR["load_guided_route"](language, pages)
    expected = GENERATOR["render_guided_route_markdown"](stages, language)
    fragment = ROOT / "site" / "includes" / f"generated-guided-route-{language}.qmd"

    assert fragment.is_file(), f"Missing tracked guided route: {fragment}"
    assert fragment.read_text(encoding="utf-8") == expected, (
        f"Stale guided route: {fragment}. Regenerate with "
        "uv run --no-project --with-requirements docs/requirements-history-validation.txt "
        "--python 3.12 python site/tools/build_learning_map.py"
    )
