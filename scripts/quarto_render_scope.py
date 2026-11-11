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
# orchestration and browser-audit code do not change the generated site.
GLOBAL_RENDER_INPUTS = {
    "pyproject.toml",
    "uv.lock",
    # Renderer changes trigger an incremental CLI smoke test against the cached site.
    "scripts/quarto_render_batch.py",
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


def _is_static_image_asset(path: str) -> bool:
    """Return whether a path is a supported image under the copied asset directory."""
    relative_path = PurePosixPath(path.removeprefix("site/"))
    return (
        path.startswith("site/images/")
        and len(relative_path.parts) > 1
        and not relative_path.is_absolute()
        and ".." not in relative_path.parts
        and relative_path.suffix.lower() in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}
    )


def generator_scope(paths: list[str]) -> dict[str, bool]:
    """Select generated fragments from the authored inputs they actually depend on.

    History links include titles read from Quarto pages; the learning map projects
    published-page metadata, headings, navigation and the concept/route registries.
    Computational diagrams are independent and depend on their dedicated registry.
    """
    qmd_changed = any(path.startswith("site/") and path.endswith(".qmd") for path in paths)
    return {
        "generate_history": (
            qmd_changed
            or "data/history-pilot.yml" in paths
            or "site/tools/render_history_pilot.py" in paths
        ),
        "generate_learning_map": (
            qmd_changed
            or any(
                path
                in {
                    "site/_quarto.yml",
                    "site/en/_metadata.yml",
                    "site/fr/_metadata.yml",
                    "site/en/_sidebar.yml",
                    "site/fr/_sidebar.yml",
                    "data/concepts.yml",
                    "data/domains.yml",
                    "data/resources.yml",
                    "data/guided-route.yml",
                    "site/tools/build_learning_map.py",
                    "site/tools/learning_map_renderers.py",
                    "site/tools/page_index.py",
                    "site/tools/export_knowledge_graph.py",
                    "site/tools/artifact_writer.py",
                    "site/tools/strict_yaml.py",
                }
                for path in paths
            )
        ),
        "generate_computational_graph": (
            "data/computational-graph.yml" in paths
            or "site/tools/render_computational_graph.py" in paths
        ),
    }


def classify_changed_files(files: list[dict[str, Any]], config: str) -> dict[str, Any]:
    """Choose skip, incremental, or full rendering conservatively."""
    paths = [str(item.get("filename", "")) for item in files]
    generators = generator_scope(paths)
    site_relevant = any(
        path.startswith(("site/", "data/", "src/"))
        or path in GLOBAL_RENDER_INPUTS
        or (path.startswith("docs/requirements-") and path.endswith(".txt"))
        for path in paths
    )
    # Static image bytes do not change page structure, styles, or interactions.
    # Link/output checks still run for site changes, but the generic browser matrix
    # has no image-specific assertions and is not useful for image-only updates.
    browser_relevant = any(
        (path.startswith("site/") and not _is_static_image_asset(path))
        or path == "scripts/site-browser-review.mjs"
        for path in paths
    )

    render_inputs = [
        item
        for item in files
        if (
            str(item.get("filename", ""))
            not in {
                "scripts/quarto_render_batch.py",
                "scripts/quarto_render_scope.py",
                "scripts/site-browser-review.mjs",
                "site/tools/build_learning_map.py",
            }
            and (
                str(item.get("filename", "")).startswith(("site/", "data/", "src/", "scripts/"))
                or str(item.get("filename", "")) in GLOBAL_RENDER_INPUTS
                or str(item.get("filename", "")).startswith("docs/requirements-")
                or str(item.get("filename", "")) in {"pyproject.toml", "uv.lock"}
            )
        )
    ]

    targets: list[str] = []
    assets: list[str] = []
    renderer_items = [
        item for item in files if item.get("filename") == "scripts/quarto_render_batch.py"
    ]
    renderer_changed = bool(renderer_items)
    renderer_safe = all(item.get("status") in {"added", "modified"} for item in renderer_items)
    renderer_smoke_test = renderer_changed and renderer_safe
    map_generator_items = [
        item for item in files if item.get("filename") == "site/tools/build_learning_map.py"
    ]
    map_generator_changed = bool(map_generator_items)
    map_generator_safe = all(
        item.get("status") in {"added", "modified"} for item in map_generator_items
    )
    safe = (
        site_relevant
        and renderer_safe
        and map_generator_safe
        and len(render_inputs) <= MAX_INCREMENTAL_PAGES
    )
    configured_targets = _render_targets(config)

    for item in render_inputs:
        path = str(item.get("filename", ""))
        status = str(item.get("status", ""))
        if status != "modified":
            safe = False
            break

        if _is_static_image_asset(path):
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

    if map_generator_changed:
        map_targets = ["site/fr/learning-map.qmd", "site/en/learning-map.qmd"]
        if all(target.removeprefix("site/") in configured_targets for target in map_targets):
            targets.extend(map_targets)
        else:
            safe = False

    mode = "skip" if not site_relevant else "full"
    browser_audit_only = paths == ["scripts/site-browser-review.mjs"] and browser_relevant
    if browser_audit_only:
        mode = "skip"
    elif safe and (targets or assets or renderer_changed):
        mode = "incremental"

    return {
        "site_relevant": site_relevant,
        "browser_relevant": browser_relevant,
        **generators,
        "renderer_smoke_test": renderer_smoke_test,
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
        for key in (
            "site_relevant",
            "browser_relevant",
            "renderer_smoke_test",
            "render_mode",
            "generate_history",
            "generate_learning_map",
            "generate_computational_graph",
        ):
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
