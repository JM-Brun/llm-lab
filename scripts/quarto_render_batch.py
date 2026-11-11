"""Render changed Quarto pages in one isolated project invocation.

The temporary output directory is kept outside the Quarto project and is
overlaid onto the published site only after Quarto succeeds. This prevents
the previous output tree from being copied into the new render and preserves
shared assets still referenced by untouched pages.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath


def replace_project_render_targets(config: str, targets: list[str]) -> str:
    """Replace only project.render while preserving the rest of the YAML."""
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
        raise ValueError("Could not find top-level project section in site/_quarto.yml")

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
    while render_end > render_start + 1 and not lines[render_end - 1].strip():
        render_end -= 1

    replacement = [
        "  render:\n",
        *(f"    - {json.dumps(path)}\n" for path in normalized),
    ]
    return "".join(lines[:render_start] + replacement + lines[render_end:])


def main() -> None:
    """Render the selected pages separately, then safely overlay their outputs."""
    targets = [
        line.strip() for line in os.environ.get("RENDER_TARGETS", "").splitlines() if line.strip()
    ]
    project_dir = Path("site")
    config_path = project_dir / "_quarto.yml"
    original_config = config_path.read_text(encoding="utf-8")
    incremental_config = replace_project_render_targets(original_config, targets)
    output_dir = project_dir / "_site"

    # Keep both the old published output and the temporary output outside the
    # project root: Quarto must not discover either as an input resource.
    with tempfile.TemporaryDirectory(
        prefix="_quarto_incremental_",
        dir=project_dir.parent,
    ) as temp_name:
        temp_output = Path(temp_name)
        relative_output = os.path.relpath(temp_output.resolve(), project_dir.resolve())

        try:
            # Override project.output-dir itself. Passing --output-dir too
            # would combine the two paths for website projects.
            isolated_config = incremental_config.replace(
                "  output-dir: _site\n",
                f"  output-dir: {json.dumps(relative_output)}\n",
                1,
            )
            if isolated_config == incremental_config:
                raise ValueError("Could not find the expected project.output-dir: _site")
            config_path.write_text(isolated_config, encoding="utf-8")
            sys.stdout.write(
                f"Rendering {len(targets)} changed page(s) into isolated output {relative_output}\n"
            )
            subprocess.run(
                ["quarto", "render", "site", "--no-clean"],
                check=True,
            )
        finally:
            config_path.write_text(original_config, encoding="utf-8")

        if not temp_output.is_dir() or not any(temp_output.iterdir()):
            raise RuntimeError("Quarto succeeded but produced no isolated output")
        if (temp_output / "_site").exists():
            raise RuntimeError("Isolated render unexpectedly copied the previous _site output")

        # Overlay generated files only. Never delete from the existing site:
        # untouched pages may still depend on shared Quarto assets.
        shutil.copytree(temp_output, output_dir, dirs_exist_ok=True)
        sys.stdout.write(
            f"Overlaid isolated render output into {output_dir}; "
            "existing shared assets were preserved\n"
        )


if __name__ == "__main__":
    main()
