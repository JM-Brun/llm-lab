#!/usr/bin/env python3
r"""Check math delimiters in Quarto sources.

Quarto renders math only when it is written with $...$ (inline) or
$$...$$ (display). LaTeX-style delimiters such as \(...\) or \[...\],
and their double-escaped variants, render as literal text in .qmd sources.
This linter reports:

- lines whose only content is a lone ```$``` (legacy marker for broken
  display math);
- raw \(, \), \[ and \] sequences outside code, including double-escaped
  variants such as \\).

Fenced code blocks (``` or ~~~) and inline code spans are ignored.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# One or two backslashes immediately followed by (, ), [ or ].
_PAREN_DELIMS = re.compile(r"[\\]{1,2}[()\\[\\]]")
# A LaTeX line break with an explicit length argument (e.g. \\[2ex]) is
# legitimate LaTeX, not a math delimiter.
_LINE_BREAK_LENGTH = re.compile(r"[\\]{2}\[\s*\d+(?:\.\d+)?\s*(?:pt|mm|cm|in|ex|em|bp|sp|mu)\s*\]")


def _is_fence(stripped: str) -> bool:
    """Return True when a stripped line opens or closes a code fence."""
    return stripped.startswith("```") or stripped.startswith("~~~")


def mask_inline_code(line: str) -> str:
    """Replace inline code spans with spaces so their content is not scanned."""
    parts = line.split("`")
    masked = [part if index % 2 == 0 else " " * len(part) for index, part in enumerate(parts)]
    return "`".join(masked)


def lone_delimiter_lines(text: str) -> list[int]:
    """Return numbers of lines whose only content is a single ```$``` outside fences."""
    offenders: list[int] = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if _is_fence(stripped):
            in_fence = not in_fence
            continue
        if not in_fence and stripped == "$":
            offenders.append(number)
    return offenders


def raw_delimiter_hits(text: str) -> list[tuple[int, str]]:
    """Return (line number, matched text) for raw LaTeX delimiters outside code."""
    offenders: list[tuple[int, str]] = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if _is_fence(stripped):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        masked = _LINE_BREAK_LENGTH.sub(
            lambda match: " " * len(match.group(0)), mask_inline_code(line)
        )
        for match in _PAREN_DELIMS.finditer(masked):
            offenders.append((number, match.group(0)))
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
        text = page.read_text(encoding="utf-8")
        numbers = lone_delimiter_lines(text)
        if numbers:
            locations = ", ".join(str(number) for number in numbers)
            errors.append(f"{page.relative_to(root)}: lone '$' line(s) {locations}")
        hits = raw_delimiter_hits(text)
        if hits:
            locations = ", ".join(f"{number} ('{token}')" for number, token in hits)
            errors.append(f"{page.relative_to(root)}: raw LaTeX delimiter(s) at {locations}")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: check_math_delimiters.py <site-source-directory>\n")
        return 2

    errors = check_site(Path(sys.argv[1]))
    if errors:
        sys.stdout.write("Math delimiter check failed:\n")
        sys.stdout.write(
            "Math must use $...$ and $$...$$; lone '$' lines and raw "
            "\\(...\\) / \\[...\\] delimiters do not render in Quarto.\n"
        )
        for error in errors:
            sys.stdout.write(f"- {error}\n")
        return 1

    sys.stdout.write("Math delimiter check passed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
