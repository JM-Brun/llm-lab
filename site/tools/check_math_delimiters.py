#!/usr/bin/env python3
"""Check that display math in Quarto sources uses $$ blocks, not lone $ lines."""

from __future__ import annotations

import sys
from pathlib import Path


def lone_delimiter_lines(text: str) -> list[int]:
    """Return numbers of lines whose only content is a single ``$`` outside fences."""
    offenders: list[int] = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and stripped == "$":
            offenders.append(number)
    return offenders


def check_site(site_root: Path) -> list[str]:
    """Return human-readable delimiter errors for the Quarto sources of a site."""
    root = site_root.resolve()
    if not root.is_dir():
        return [f"Site source directory does not exist: {root}"]

    pages = sorted(root.rglob("*.qmd"))
    if not pages:
        return [f"No Quarto sources found in site directory: {root}"]

    errors: list[str] = []
    for page in pages:
        numbers = lone_delimiter_lines(page.read_text(encoding="utf-8"))
        if numbers:
            locations = ", ".join(str(number) for number in numbers)
            errors.append(f"{page.relative_to(root)}: lone '$' line(s) {locations}")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: check_math_delimiters.py <site-source-directory>\n")
        return 2

    errors = check_site(Path(sys.argv[1]))
    if errors:
        sys.stdout.write("Math delimiter check failed:\n")
        sys.stdout.write("Display math must use $$ blocks; a lone '$' line breaks rendering.\n")
        for error in errors:
            sys.stdout.write(f"- {error}\n")
        return 1

    sys.stdout.write("Math delimiter check passed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
