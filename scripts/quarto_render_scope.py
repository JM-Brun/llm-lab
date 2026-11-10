"""Classify Quarto pull-request changes for safe incremental rendering."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

MAX_INCREMENTAL_PAGES = 60
# Only inputs that can change rendered content belong here. Workflow
# orchestration and this classifier do not change the site itself. The browser
# audit script remains included because its checks require a freshly rendered
# site when the audit implementation changes.
GLOBAL_RENDER_INPUTS = {
    "pyproject.toml",
    "uv.lock",
    "scripts/site-browser-review.mjs",
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


def classify_changed_files(files: list[dict[str, Any]], config: str) -> dict[str, Any]:
    """Choose skip, incremental, or full rendering conservatively."""
    paths = [str(item.get("filename", "")) for item in files]
    site_relevant = any(
        path.startswith(("site/", "data/", "src/"))
        or path in GLOBAL_RENDER_INPUTS
        or (path.startswith("docs/requirements-") and path.endswith(".txt"))
        for path in paths
    )
    browser_relevant = any(
        path.startswith("site/") or path == "scripts/site-browser-review.mjs" for path in paths
    )

    render_inputs = [
        item
        for item in files
        if (
            str(item.get("filename", "")).startswith(("site/", "data/", "src/", "scripts/"))
            or str(item.get("filename", "")) in GLOBAL_RENDER_INPUTS
            or str(item.get("filename", "")).startswith("docs/requirements-")
            or str(item.get("filename", "")) in {"pyproject.toml", "uv.lock"}
        )
    ]

    targets: list[str] = []
    assets: list[str] = []
    safe = site_relevant and bool(render_inputs) and len(render_inputs) <= MAX_INCREMENTAL_PAGES
    configured_targets = _render_targets(config)

    for item in render_inputs:
        path = str(item.get("filename", ""))
        status = str(item.get("status", ""))
        if status != "modified":
            safe = False
            break

        if path.startswith("site/images/") and PurePosixPath(path).suffix.lower() == ".svg":
            assets.append(path)
            continue

        if not path.startswith("site/") or not path.endswith(".qmd"):
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
        "render_assets": sorted(set(assets)) if mode == "incremental" else [],
        "files": paths,
    }


def main() -> None:
    raw = os.environ.get("PR_CHANGED_FILES_JSON", "[]")
    files = json.loads(raw)
    if not isinstance(files, list):
        raise ValueError("PR_CHANGED_FILES_JSON must contain a JSON array")

    with Path("site/_quarto.yml").open(encoding="utf-8") as config_file:
        config = config_file.read()
    result = classify_changed_files(files, config)

    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        for key in ("site_relevant", "browser_relevant", "render_mode"):
            value = result[key]
            if isinstance(value, bool):
                value = str(value).lower()
            output.write(f"{key}={value}\n")
        for key in ("files", "render_targets", "render_assets"):
            output.write(f"{key}<<EOF\n")
            output.write("\n".join(result[key]))
            output.write("\nEOF\n")

    sys.stdout.write(
        f"Quarto scope: {result['render_mode']}; {len(result['render_targets'])} page(s) selected\n"
    )


if __name__ == "__main__":
    main()
