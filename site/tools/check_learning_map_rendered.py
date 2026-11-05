"""Check that each rendered learning map contains its interactive DOM shell."""

from __future__ import annotations

import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

VOID_ELEMENTS = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)


class MapParser(HTMLParser):
    """Collect real elements inside a map, not markup escaped inside code blocks."""

    def __init__(self, language: str) -> None:
        super().__init__(convert_charrefs=True)
        self.language = language
        self.stack: list[tuple[str, bool, bool]] = []
        self.roots = 0
        self.valid_roots = 0
        self.found: Counter[str] = Counter()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        inside_map = bool(self.stack and self.stack[-1][1])
        inside_mode = bool(self.stack and self.stack[-1][2])
        if tag == "div" and "data-learning-map" in attributes:
            self.roots += 1
            inside_map = True
            if (
                attributes.get("data-language") == self.language
                and attributes.get("data-source") == f"../learning-map-data-{self.language}.json"
            ):
                self.valid_roots += 1
        if inside_map:
            for name, expected_tag in (
                ("data-map-mode", "select"),
                ("data-map-search", "input"),
                ("data-map-relation-type", "select"),
                ("data-map-reset", "button"),
                ("data-map-viewport", "div"),
                ("data-map-detail-panel", "div"),
                ("data-map-status", "p"),
            ):
                if tag == expected_tag and name in attributes:
                    self.found[name] += 1
            if tag == "option" and inside_mode and attributes.get("value") in {"pages", "concepts"}:
                self.found[f"option:{attributes['value']}"] += 1
        if tag not in VOID_ELEMENTS:
            is_mode = inside_mode or (inside_map and "data-map-mode" in attributes)
            self.stack.append((tag, inside_map, is_mode))

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


def inspect_page(path: Path, language: str) -> list[str]:
    """Return actionable errors for a localized rendered map."""
    if not path.is_file():
        return [f"{path}: rendered page is missing"]
    parser = MapParser(language)
    parser.feed(path.read_text(encoding="utf-8"))
    errors = []
    if parser.roots != 1 or parser.valid_roots != 1:
        errors.append(f"{path}: expected one {language} map with its localized data source")
    for name in (
        "data-map-mode",
        "option:pages",
        "option:concepts",
        "data-map-search",
        "data-map-relation-type",
        "data-map-reset",
        "data-map-viewport",
        "data-map-detail-panel",
        "data-map-status",
    ):
        if parser.found[name] != 1:
            errors.append(f"{path}: expected one real {name} element; found {parser.found[name]}")
    return errors


def main() -> int:
    site = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("site/_site")
    errors = [
        error
        for lang in ("fr", "en")
        for error in inspect_page(site / lang / "learning-map.html", lang)
    ]
    if errors:
        sys.stderr.write("Rendered learning-map validation failed:\n")
        for error in errors:
            sys.stderr.write(f"- {error}\n")
        return 1
    sys.stdout.write("Rendered learning-map shells passed for FR and EN.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
