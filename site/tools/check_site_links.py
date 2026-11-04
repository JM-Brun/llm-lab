#!/usr/bin/env python3
"""Check local file and fragment links in a rendered Quarto HTML site."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class LinkParser(HTMLParser):
    """Collect links and anchors from one HTML document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        href = attributes.get("href")
        if href is not None:
            self.links.append(href)
        anchor_id = attributes.get("id")
        if anchor_id:
            self.anchors.add(anchor_id)
        name = attributes.get("name")
        if tag == "a" and name:
            self.anchors.add(name)


def parse_html(path: Path) -> LinkParser:
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def resolve_target(site_root: Path, source: Path, href: str) -> Path | None:
    """Resolve a local href to a rendered file; return None for non-file URLs."""
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None

    path = unquote(parsed.path)
    if not path:
        return source

    target = (site_root / path.lstrip("/")) if path.startswith("/") else (source.parent / path)
    target = target.resolve()

    if target.is_dir():
        target = target / "index.html"
    if target.is_file():
        return target

    if not target.suffix:
        html_target = target.with_suffix(".html")
        if html_target.is_file():
            return html_target
        index_target = target / "index.html"
        if index_target.is_file():
            return index_target
    return target


def check_site(site_root: Path) -> list[str]:
    """Return human-readable local link errors for a rendered site."""
    root = site_root.resolve()
    if not root.is_dir():
        return [f"Rendered site directory does not exist: {root}"]

    html_files = sorted(root.rglob("*.html"))
    if not html_files:
        return [f"No HTML files found in rendered site: {root}"]

    parsed_pages = {path: parse_html(path) for path in html_files}
    errors: list[str] = []

    for source, page in parsed_pages.items():
        for href in page.links:
            parsed = urlsplit(href)
            target = resolve_target(root, source, href)
            if target is None:
                continue
            if not target.is_file():
                errors.append(f"{source.relative_to(root)}: missing target for {href!r}")
                continue
            fragment = unquote(parsed.fragment)
            if fragment and target.suffix.lower() == ".html":
                target_page = parsed_pages.get(target)
                if target_page is None:
                    target_page = parse_html(target)
                if fragment not in target_page.anchors:
                    errors.append(
                        f"{source.relative_to(root)}: missing fragment "
                        f"#{fragment} in {target.relative_to(root)} (href {href!r})"
                    )
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: check_site_links.py <rendered-site-directory>\n")
        return 2

    site_root = Path(sys.argv[1])
    errors = check_site(site_root)
    if errors:
        sys.stdout.write("Rendered-site link check failed:\n")
        for error in errors:
            sys.stdout.write(f"- {error}\n")
        return 1

    sys.stdout.write(f"Rendered-site link check passed for {site_root}.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
