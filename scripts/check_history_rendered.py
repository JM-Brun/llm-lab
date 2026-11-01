#!/usr/bin/env python3
"""Check the rendered bilingual timeline's event parity and semantic structure."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "fr": ROOT / "site" / "_site" / "fr" / "transformer-history.html",
    "en": ROOT / "site" / "_site" / "en" / "transformer-history.html",
}
EXPECTED_EVENT_COUNT = 17
EXPECTED_STREAMS = {"research", "model_release", "ecosystem"}


class TimelineParser(HTMLParser):
    """Collect timeline event metadata, dates, links and visible text."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.events: list[tuple[str, str]] = []
        self.times: list[str] = []
        self.links: list[str] = []
        self.text: list[str] = []
        self.has_labelled_timeline = False
        self.timeline_depth = 0
        # Quarto may wrap headings in nested <section> elements. Track each
        # section independently so closing a nested section cannot close the
        # outer history-timeline scope.
        self.section_stack: list[bool] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()

        if tag == "section":
            is_timeline = "history-timeline" in classes
            self.section_stack.append(is_timeline)
            if is_timeline:
                self.has_labelled_timeline = bool(attributes.get("aria-label"))
                self.timeline_depth += 1

        if tag == "li" and "history-timeline__item" in classes and self.timeline_depth > 0:
            event_id = attributes.get("data-event-id") or ""
            event_type = attributes.get("data-event-type") or ""
            self.events.append((event_id, event_type))

        if tag == "time" and self.timeline_depth > 0:
            self.times.append(attributes.get("datetime") or "")

        href = attributes.get("href")
        if href and self.timeline_depth > 0:
            self.links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self.section_stack:
            was_timeline = self.section_stack.pop()
            if was_timeline:
                self.timeline_depth -= 1

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.text.append(data.strip())


def inspect_page(path: Path, lang: str) -> tuple[list[tuple[str, str]], list[str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Rendered history page is missing: {path}")
    parser = TimelineParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()

    errors: list[str] = []
    ids = [event_id for event_id, _ in parser.events]
    streams = {event_type for _, event_type in parser.events}
    if len(parser.events) != EXPECTED_EVENT_COUNT:
        errors.append(f"{lang}: expected 17 rendered events, found {len(parser.events)}")
    if len(set(ids)) != len(ids):
        errors.append(f"{lang}: duplicate rendered event IDs")
    if any(not event_id for event_id in ids):
        errors.append(f"{lang}: an event is missing its stable ID")
    if streams != EXPECTED_STREAMS:
        errors.append(f"{lang}: expected all three event streams, found {sorted(streams)}")
    if len(parser.times) != EXPECTED_EVENT_COUNT:
        errors.append(f"{lang}: expected 17 semantic time elements, found {len(parser.times)}")
    if not parser.has_labelled_timeline:
        errors.append(f"{lang}: timeline section is missing its accessible label")

    visible_text = " ".join(parser.text)
    if lang == "fr":
        if "Aucune page de notion dédiée" not in visible_text:
            errors.append("fr: missing explicit no-internal-page fallback")
        if "février 2019" not in visible_text or "novembre 2019" not in visible_text:
            errors.append("fr: GPT-2 staged release interval is not visible")
    else:
        if "No dedicated LLM Lab concept page yet" not in visible_text:
            errors.append("en: missing explicit no-internal-page fallback")
        if "February 2019" not in visible_text or "November 2019" not in visible_text:
            errors.append("en: GPT-2 staged release interval is not visible")

    if len(parser.links) < EXPECTED_EVENT_COUNT:
        errors.append(f"{lang}: expected at least one source link per event")
    if any("TODO" in href or href == "#" for href in parser.links):
        errors.append(f"{lang}: placeholder link found")
    return parser.events, errors


def main() -> int:
    results: dict[str, list[tuple[str, str]]] = {}
    errors: list[str] = []
    for lang, path in PAGES.items():
        try:
            events, page_errors = inspect_page(path, lang)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
            continue
        results[lang] = events
        errors.extend(page_errors)

    if "fr" in results and "en" in results and results["fr"] != results["en"]:
        errors.append("FR/EN rendered event IDs or event-stream order differ")

    if errors:
        sys.stdout.write("Rendered history validation failed:\n")
        for error in errors:
            sys.stdout.write(f"- {error}\n")
        return 1

    sys.stdout.write(
        "Rendered history validation passed: 17 events, three streams, date ranges, "
        "source links, accessible labels and FR/EN parity.\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
