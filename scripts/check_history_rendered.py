#!/usr/bin/env python3
"""Check the rendered bilingual timeline's event parity and semantic structure."""

from __future__ import annotations

import sys
from collections import Counter
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
        self.timeline_text: list[str] = []
        self.has_labelled_timeline = False
        # Track nesting depth for the root tag: Pandoc may wrap headings in nested
        # <section> elements, so the first matching closing tag is not necessarily
        # the end of the timeline container.
        self.timeline_roots: list[tuple[str, int]] = []
        self.timeline_root_tags_seen: Counter[str] = Counter()
        self.tag_counts: Counter[str] = Counter()
        self.time_tags: list[tuple[str | None, str | None]] = []
        self.anchor_tags: list[tuple[str | None, str | None]] = []

    @property
    def in_timeline(self) -> bool:
        return bool(self.timeline_roots)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tag_counts[tag] += 1
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()

        # Quarto/Pandoc may preserve raw HTML containers or wrap them differently.
        # Identify the timeline by its semantic class, not by assuming <section>.
        if "history-timeline" in classes:
            self.timeline_roots.append((tag, 1))
            self.timeline_root_tags_seen[tag] += 1
            self.has_labelled_timeline = self.has_labelled_timeline or bool(
                attributes.get("aria-label")
            )
        elif self.timeline_roots and self.timeline_roots[-1][0] == tag:
            root_tag, depth = self.timeline_roots[-1]
            self.timeline_roots[-1] = (root_tag, depth + 1)

        if tag == "li" and "history-timeline__item" in classes and self.in_timeline:
            event_id = attributes.get("data-event-id") or ""
            event_type = attributes.get("data-event-type") or ""
            self.events.append((event_id, event_type))

        if tag == "time":
            datetime_value = attributes.get("datetime")
            self.time_tags.append((datetime_value, attributes.get("class")))
            if self.in_timeline:
                self.times.append(datetime_value or "")

        if tag == "a":
            href = attributes.get("href")
            self.anchor_tags.append((href, attributes.get("class")))
            if href and self.in_timeline:
                self.links.append(href)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if self.timeline_roots and self.timeline_roots[-1][0] == tag:
            root_tag, depth = self.timeline_roots[-1]
            if depth == 1:
                self.timeline_roots.pop()
            else:
                self.timeline_roots[-1] = (root_tag, depth - 1)

    def handle_data(self, data: str) -> None:
        if data.strip():
            text = data.strip()
            self.text.append(text)
            if self.in_timeline:
                self.timeline_text.append(text)


def inspect_page(path: Path, lang: str) -> tuple[list[tuple[str, str]], list[str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Rendered history page is missing: {path}")
    rendered_html = path.read_text(encoding="utf-8")
    parser = TimelineParser()
    parser.feed(rendered_html)
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
    if any(not value for value in parser.times):
        errors.append(f"{lang}: a semantic time element is missing its datetime attribute")
    if not parser.has_labelled_timeline:
        errors.append(f"{lang}: timeline container is missing its accessible label")

    visible_text = " ".join(parser.timeline_text)
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

    if errors:
        timeline_marker = rendered_html.find("history-timeline")
        timeline_snippet = (
            rendered_html[max(0, timeline_marker - 300) : timeline_marker + 2400]
            if timeline_marker >= 0
            else "<history-timeline marker absent>"
        )
        sys.stdout.write(
            f"{lang}: HTML diagnostics: tags={dict(parser.tag_counts)}, "
            f"timeline_root_tags_seen={dict(parser.timeline_root_tags_seen)}, "
            f"all_time_tags={parser.time_tags[:8]}, "
            f"all_anchors={parser.anchor_tags[:12]}, "
            f"timeline_times={len(parser.times)}, timeline_links={len(parser.links)}\\n"
            f"{lang}: timeline HTML excerpt: {timeline_snippet}\\n"
        )
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
