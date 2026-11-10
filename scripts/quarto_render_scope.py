"""Classify Quarto pull-request changes for safe incremental rendering."""

from __future__ import annotations

import json
import os
import re
from pathlib import PurePosixPath
from typing import Any

MAX_INCREMENTAL_PAGES = 20
GLOBAL_RENDER_INPUTS = {
    ".github/workflows/quarto.yml",
    "pyproject.toml",
    "uv.lock",
    "scripts/site-browser-review.mjs",
    "scripts/quarto_render_scope.py",
}


def _render_targets(config: str) -> set[str]:
    """Return the explicit project.render targets from site/_quarto.yml."""
    match = re.search(r"(?ms)^  render:\n(.*?)(?=^website:)", config)
    if match is None:
        return set()
    return {
        line.strip()[2:].strip()
        for line in match.group(1).splitlines()
        if line.strip().startswith("- ")
    }


def classify_changed_files(
    files: list[dict[str, Any]], config: str
) -> dict[str, Any]:
    """Choose skip, incremental, or full rendering conservatively."""
    paths = [str(item.get("filename", "")) for item in files]
    site_relevant = any(
        path.startswith(("site/", "data/", "src/"))
        or path in GLOBAL_RENDER_INPUTS
        or (path.startswith("docs/requirements-") and path.endswith(".txt"))
        for path in paths
    )
    browser_relevant = any(
        path.startswith("site/") or path == "scripts/site-browser-review.mjs"
        for path in paths
    )

    render_inputs = [
        item
        for item in files
        if (
            str(item.get("filename", "")).startswith(
                ("site/", "data/", "src/", "scripts/")
            )
            or str(item.get("filename", "")) in GLOBAL_RENDER_INPUTS
            or str(item.get("filename", "")).startswith("docs/requirements-")
            or str(item.get("filename", "")) in {"pyproject.toml", "uv.lock"}
        )
    ]

    targets: list[str] = []
    safe = site_relevant and bool(render_inputs) and len(render_inputs) <= MAX_INCREMENTAL_PAGES
    configured_targets = _render_targets(config)

    for item in render_inputs:
        path = str(item.get("filename", ""))
        status = str(item.get("status", ""))
        if (
            not path.startswith("site/")
            or not path.endswith(".qmd")
            or status != "modified"
        ):
            safe = False
            break

        relative = path.removeprefix("site/")
        relative_path = PurePosixPath(relative)
        if (
            relative == "references.qmd"
            or relative_path.is_absolute()
            or ".." in relative_path.parts
            or relative not in configured_targets
        ):
            safe = False
            break
        targets.append(path)

    mode = "skip" if not site_relevant else "full"
    if safe and targets:
        mode = "incremental"

    return {
        "site_relevant": site_relevant,
        "browser_relevant": browser_relevant,
        "render_mode": mode,
        "render_targets": sorted(set(targets)) if mode == "incremental" else [],
        "files": paths,
    }


def main() -> None:
    raw = os.environ.get("PR_CHANGED_FILES_JSON", "[]")
    files = json.loads(raw)
    if not isinstance(files, list):
        raise ValueError("PR_CHANGED_FILES_JSON must contain a JSON array")

    config = open("site/_quarto.yml", encoding="utf-8").read()
    result = classify_changed_files(files, config)

    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        for key in ("site_relevant", "browser_relevant", "render_mode"):
            output.write(f"{key}={str(result[key]).lower() if isinstance(result[key], bool) else result[key]}\n")
        for key in ("files", "render_targets"):
            output.write(f"{key}<<EOF\n")
            output.write("\n".join(result[key]))
            output.write("\nEOF\n")

    print(
        f"Quarto scope: {result['render_mode']}; "
        f"{len(result['render_targets'])} page(s) selected"
    )


if __name__ == "__main__":
    main()
