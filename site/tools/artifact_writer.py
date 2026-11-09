"""Stage generated files before publishing them with per-file atomic replacement.

Staging failure leaves existing files untouched. Replacement of several files is
not a transaction: a later replacement can fail after an earlier one succeeds.
"""

from __future__ import annotations

import os
import secrets
import stat
from collections.abc import Mapping
from pathlib import Path


def _stage_artifact(target: Path, content: str) -> Path:
    """Write one temporary sibling using the destination's permissions."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not target.is_file():
        raise IsADirectoryError(f"Generated artifact is not a regular file: {target}")

    for _ in range(10):
        temporary = target.with_name(f".{target.name}.{secrets.token_hex(8)}.tmp")
        try:
            descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
        except FileExistsError:
            continue
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                descriptor = -1
                if target.exists():
                    os.chmod(temporary, stat.S_IMODE(target.stat().st_mode))
                stream.write(content)
        except BaseException:
            if descriptor != -1:
                os.close(descriptor)
            temporary.unlink(missing_ok=True)
            raise
        return temporary
    raise FileExistsError(f"Cannot allocate temporary file for {target}")


def write_artifacts(artifacts: Mapping[Path, str]) -> None:
    """Stage all outputs first, then replace each target atomically.

    Resolve symbolic links before staging, matching ordinary file writes, and
    reject multiple output paths that would overwrite the same physical target.
    """
    targets: dict[Path, str] = {}
    for path, content in artifacts.items():
        target = path.resolve()
        if target in targets:
            raise ValueError(f"Multiple generated artifacts resolve to {target}")
        targets[target] = content

    staged: list[tuple[Path, Path]] = []
    try:
        for target, content in targets.items():
            staged.append((target, _stage_artifact(target, content)))
        for published, (target, temporary) in enumerate(staged):
            try:
                os.replace(temporary, target)
            except OSError as exc:
                exc.add_note(
                    f"Cannot publish {target} after replacing {published} of {len(staged)} "
                    "artifacts; rerun generation."
                )
                raise
    finally:
        for _, temporary in staged:
            temporary.unlink(missing_ok=True)
