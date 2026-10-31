#!/usr/bin/env python3
"""Validate the bilingual history pilot dataset against its editorial contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "history-pilot.yml"
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
DATE_PATTERNS = {
    "day": re.compile(r"\d{4}-\d{2}-\d{2}"),
    "month": re.compile(r"\d{4}-\d{2}"),
    "year": re.compile(r"\d{4}"),
}
EVENT_TYPES = {"research", "model_release", "ecosystem"}
DATE_KINDS = {
    "proposal",
    "submission",
    "publication",
    "announcement",
    "release",
    "adoption",
    "other",
}
SOURCE_KINDS = {
    "primary_paper",
    "technical_report",
    "official_announcement",
    "standard",
    "secondary_review",
}
CONFIDENCE = {"high", "medium", "provisional"}


def validate() -> list[str]:
    errors: list[str] = []
    try:
        data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"Cannot parse {DATA.relative_to(ROOT)}: {exc}"]
    if not isinstance(data, dict):
        return ["root: expected a mapping"]

    selection = data.get("selection", {})
    events = data.get("events")
    sources = data.get("sources")
    if not isinstance(selection, dict):
        return ["selection: expected a mapping"]
    if not isinstance(events, list) or not isinstance(sources, list):
        return ["events and sources must both be lists"]
    if selection.get("core_milestone_count") != 16 or selection.get("event_record_count") != 17:
        errors.append("selection: expected 16 core milestones and 17 event records")
    if len(events) != 17:
        errors.append(f"events: expected 17 records, found {len(events)}")

    source_map: dict[str, dict] = {}
    for i, source in enumerate(sources):
        where = f"sources[{i}]"
        if not isinstance(source, dict):
            errors.append(f"{where}: expected mapping")
            continue
        sid = source.get("id")
        if not isinstance(sid, str) or not ID.fullmatch(sid):
            errors.append(f"{where}: invalid stable source id")
            continue
        if sid in source_map:
            errors.append(f"{where}: duplicate source id {sid!r}")
        source_map[sid] = source
        if source.get("kind") not in SOURCE_KINDS:
            errors.append(f"{where}: unsupported source kind")
        for field in ("title", "authors_or_organization", "date", "url"):
            if not isinstance(source.get(field), str) or not source[field].strip():
                errors.append(f"{where}: missing non-empty {field}")
        parsed = urlsplit(source.get("url", "") if isinstance(source.get("url"), str) else "")
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{where}: source URL must be absolute HTTPS")
        if not isinstance(source.get("supports"), list) or not source["supports"]:
            errors.append(f"{where}: supports must be a non-empty list")

    event_ids: set[str] = set()
    for i, event in enumerate(events):
        where = f"events[{i}]"
        if not isinstance(event, dict):
            errors.append(f"{where}: expected mapping")
            continue
        eid = event.get("id")
        if not isinstance(eid, str) or not ID.fullmatch(eid):
            errors.append(f"{where}: invalid stable event id")
        elif eid in event_ids:
            errors.append(f"{where}: duplicate event id {eid!r}")
        else:
            event_ids.add(eid)
        if event.get("type") not in EVENT_TYPES:
            errors.append(f"{where}: unsupported event type {event.get('type')!r}")

        date = event.get("date")
        if not isinstance(date, dict):
            errors.append(f"{where}.date: expected mapping")
        else:
            precision, value = date.get("precision"), date.get("value")
            pattern = DATE_PATTERNS.get(precision)
            if not isinstance(value, str) or pattern is None or not pattern.fullmatch(value):
                errors.append(f"{where}.date: value does not match declared precision")
            if date.get("kind") not in DATE_KINDS:
                errors.append(f"{where}.date.kind: unsupported value {date.get('kind')!r}")

        for field in ("title", "summary"):
            translations = event.get(field)
            if not isinstance(translations, dict):
                errors.append(f"{where}.{field}: expected bilingual mapping")
            else:
                for lang in ("fr", "en"):
                    if (
                        not isinstance(translations.get(lang), str)
                        or not translations[lang].strip()
                    ):
                        errors.append(f"{where}.{field}.{lang}: missing translation")
        if not isinstance(event.get("era"), str) or not event["era"].strip():
            errors.append(f"{where}: missing era")
        if not isinstance(event.get("significance"), list) or not event["significance"]:
            errors.append(f"{where}: significance must be a non-empty list")
        if not isinstance(event.get("concept_ids"), list):
            errors.append(f"{where}: concept_ids must be a list")
        refs = event.get("source_ids")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{where}: source_ids must be a non-empty list")
        else:
            for ref in refs:
                if ref not in source_map:
                    # Checked again after all source IDs have been collected.
                    pass
        confidence = event.get("confidence")
        if confidence not in CONFIDENCE:
            errors.append(f"{where}: unsupported confidence {confidence!r}")
        elif confidence != "high" and not event.get("editorial_note"):
            errors.append(f"{where}: non-high confidence requires an editorial_note")

        links = event.get("internal_links", {})
        if not isinstance(links, dict):
            errors.append(f"{where}.internal_links: expected mapping")
        else:
            for lang in ("fr", "en"):
                destinations = links.get(lang, [])
                if not isinstance(destinations, list):
                    errors.append(f"{where}.internal_links.{lang}: expected list")
                    continue
                for destination in destinations:
                    if not isinstance(destination, str) or not (ROOT / destination).is_file():
                        errors.append(
                            f"{where}.internal_links.{lang}: missing destination {destination!r}"
                        )

    for i, event in enumerate(events):
        if isinstance(event, dict):
            for ref in event.get("source_ids", []):
                if ref not in source_map:
                    errors.append(f"events[{i}]: unresolved source id {ref!r}")
    if len(event_ids) != 17:
        errors.append(f"events: expected 17 unique IDs, found {len(event_ids)}")
    if len(source_map) != len(sources):
        errors.append("sources: IDs must all be valid and unique")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        sys.stdout.write("History pilot validation failed:\n")
        for error in errors:
            sys.stdout.write(f"- {error}\n")
        return 1
    sys.stdout.write(
        "History pilot validation passed: "
        "counts, schema, bilingual fields, dates, sources and internal links.\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
