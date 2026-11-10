"""Render a safe batch of Quarto pages in one project invocation."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath


def replace_project_render_targets(config: str, targets: list[str]) -> str:
    """Replace only project.render while preserving the rest of the YAML verbatim."""
    normalized: list[str] = []
    for target in targets:
        path = PurePosixPath(target)
        if (
            not target.startswith("site/")
            or path.suffix != ".qmd"
            or path.is_absolute()
            or ".." in path.parts
        ):
            raise ValueError(f"Unsafe Quarto render target: {target!r}")
        relative = path.as_posix().removeprefix("site/")
        if relative not in normalized:
            normalized.append(relative)

    if not normalized:
        raise ValueError("At least one Quarto render target is required")

    lines = config.splitlines(keepends=True)
    project_start = next(
        (index for index, line in enumerate(lines) if line.rstrip("\n") == "project:"),
        None,
    )
    if project_start is None:
        raise ValueError("Could not find the top-level project section in site/_quarto.yml")

    project_end = next(
        (
            index
            for index in range(project_start + 1, len(lines))
            if lines[index].strip() and not lines[index].startswith((" ", "#"))
        ),
        len(lines),
    )
    render_start = next(
        (
            index
            for index in range(project_start + 1, project_end)
            if lines[index].rstrip("\n") == "  render:"
        ),
        None,
    )
    if render_start is None:
        raise ValueError("Could not find project.render in site/_quarto.yml")

    render_end = next(
        (
            index
            for index in range(render_start + 1, project_end)
            if lines[index].strip() and len(lines[index]) - len(lines[index].lstrip(" ")) <= 2
        ),
        project_end,
    )
    replacement = ["  render:\n", *(f"    - {json.dumps(path)}\n" for path in normalized)]
    return "".join(lines[:render_start] + replacement + lines[render_end:])


def main() -> None:
    targets = [
        line.strip() for line in os.environ.get("RENDER_TARGETS", "").splitlines() if line.strip()
    ]
    config_path = Path("site/_quarto.yml")
    original_config = config_path.read_text(encoding="utf-8")
    incremental_config = replace_project_render_targets(original_config, targets)

    try:
        config_path.write_text(incremental_config, encoding="utf-8")
        sys.stdout.write(f"Rendering {len(targets)} changed page(s) in one Quarto invocation\n")
        subprocess.run(["quarto", "render", "site", "--no-clean"], check=True)
    finally:
        config_path.write_text(original_config, encoding="utf-8")


if __name__ == "__main__":
    main()
