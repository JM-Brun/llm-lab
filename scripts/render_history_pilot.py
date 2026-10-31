#!/usr/bin/env python3
"""Render the canonical bilingual history dataset as accessible Quarto timeline fragments."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "history-pilot.yml"
OUTPUTS = {
    "fr": ROOT / "site" / "fr" / "_history-timeline-generated.qmd",
    "en": ROOT / "site" / "en" / "_history-timeline-generated.qmd",
}
ERA_LABELS = {
    "neural-sequence-modelling-and-attention": {
        "fr": "Attention et modélisation de séquences",
        "en": "Attention and sequence modelling",
    },
    "transformer-and-pretraining": {
        "fr": "Transformers et pré-entraînement",
        "en": "Transformers and pretraining",
    },
    "scaling-and-post-training": {
        "fr": "Mise à l'échelle et post-entraînement",
        "en": "Scaling and post-training",
    },
    "efficiency-and-alternative-architectures": {
        "fr": "Efficacité et architectures alternatives",
        "en": "Efficiency and alternative architectures",
    },
    "multimodal-reasoning-and-ecosystem": {
        "fr": "Raisonnement, multimodalité et écosystème",
        "en": "Reasoning, multimodality and ecosystem",
    },
}
STREAM_LABELS = {
    "research": {"fr": "Recherche", "en": "Research"},
    "model_release": {"fr": "Diffusion de modèle", "en": "Model release"},
    "ecosystem": {"fr": "Écosystème", "en": "Ecosystem"},
}
DATE_KIND_LABELS = {
    "proposal": {"fr": "Proposition", "en": "Proposal"},
    "submission": {"fr": "Soumission arXiv", "en": "arXiv submission"},
    "publication": {"fr": "Publication", "en": "Publication"},
    "announcement": {"fr": "Annonce officielle", "en": "Official announcement"},
    "release": {"fr": "Mise à disposition", "en": "Release"},
    "adoption": {"fr": "Adoption", "en": "Adoption"},
    "other": {"fr": "Autre date documentée", "en": "Other documented date"},
}
MONTHS = {
    "fr": [
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "août",
        "septembre",
        "octobre",
        "novembre",
        "décembre",
    ],
    "en": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def display_date(value: str, precision: str, lang: str) -> str:
    if precision == "year":
        return value
    year, month, *day = value.split("-")
    month_name = MONTHS[lang][int(month) - 1]
    if precision == "month":
        return f"{month_name} {year}"
    return f"{int(day[0])} {month_name} {year}"


def page_title(path: str) -> str:
    source = ROOT / path
    try:
        content = source.read_text(encoding="utf-8")
    except OSError:
        return Path(path).stem.replace("-", " ").title()
    match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
    return match.group(1) if match else Path(path).stem.replace("-", " ").title()


def editorial_note(event: dict[str, Any], lang: str) -> str | None:
    note = event.get("editorial_note")
    if isinstance(note, dict):
        value = note.get(lang)
        return value if isinstance(value, str) and value.strip() else None
    if isinstance(note, str) and lang == "fr":
        return note
    return None


def render_event(event: dict[str, Any], sources: dict[str, dict[str, Any]], lang: str) -> str:
    date = event["date"]
    date_value = date["value"]
    date_text = display_date(date_value, date["precision"], lang)
    if date.get("end_value"):
        date_text += " " + chr(0x2013) + " " + display_date(date["end_value"], date["precision"], lang)
    stream = STREAM_LABELS[event["type"]][lang]
    date_kind = DATE_KIND_LABELS[date["kind"]][lang]
    title = esc(event["title"][lang])
    summary = esc(event["summary"][lang])

    output = [
        f'<li class="history-timeline__item history-timeline__item--{esc(event["type"])}">',
        '  <div class="history-timeline__meta">',
        f'    <time datetime="{esc(date_value)}">{esc(date_text)}</time>',
        f'    <span class="history-timeline__kind">{esc(date_kind)}</span>',
        f'    <span class="history-timeline__stream">{esc(stream)}</span>',
        "  </div>",
        '  <div class="history-timeline__content">',
        f"    <h4>{title}</h4>",
        f"    <p>{summary}</p>",
    ]

    internal_links = event.get("internal_links", {}).get(lang, [])
    if internal_links:
        label = "Approfondir" if lang == "fr" else "Explore the concept"
        links = [
            f'<a href="{esc(Path(path).name)}">{esc(page_title(path))}</a>'
            for path in internal_links
        ]
        output.append(
            f'    <p class="history-timeline__concepts"><strong>{label} :</strong> '
            + " · ".join(links)
            + "</p>"
        )
    else:
        missing_label = (
            "Aucune page de notion dédiée dans LLM Lab pour le moment."
            if lang == "fr"
            else "No dedicated LLM Lab concept page yet."
        )
        output.append(f'    <p class="history-timeline__missing">{missing_label}</p>')

    source_links = []
    for source_id in event["source_ids"]:
        source = sources[source_id]
        source_links.append(
            f'<a href="{esc(source["url"])}" rel="external">{esc(source["title"])}</a>'
        )
    source_label = "Sources"
    output.append(
        f'    <p class="history-timeline__sources"><strong>{source_label} :</strong> '
        + " · ".join(source_links)
        + "</p>"
    )

    note = editorial_note(event, lang)
    if note:
        note_label = "Précaution" if lang == "fr" else "Editorial note"
        output.append(
            f'    <p class="history-timeline__note"><strong>{note_label} :</strong> {esc(note)}</p>'
        )

    output.extend(["  </div>", "</li>"])
    return "\n".join(output)


def render(data: dict[str, Any], lang: str) -> str:
    sources = {source["id"]: source for source in data["sources"]}
    events = sorted(data["events"], key=lambda event: (event["date"]["value"], event["id"]))
    title = "Chronologie historique" if lang == "fr" else "Historical timeline"
    output = [f'<section class="history-timeline" aria-label="{title}">']
    current_era: str | None = None
    for index, event in enumerate(events):
        era = event["era"]
        if era != current_era:
            if era not in ERA_LABELS:
                raise ValueError(f"Unknown era {era!r}")
            output.append(f'<h3 class="history-timeline__era">{esc(ERA_LABELS[era][lang])}</h3>')
            output.append('<ol class="history-timeline__list">')
            current_era = era
        output.append(render_event(event, sources, lang))
        next_index = index + 1
        if next_index == len(events) or events[next_index]["era"] != current_era:
            output.append("</ol>")
    output.append("</section>")
    return "\n".join(output) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="Fail if generated fragments are stale."
    )
    args = parser.parse_args()

    try:
        data = yaml.safe_load(DATA_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("History dataset root must be a mapping.")
        rendered = {lang: render(data, lang) for lang in ("fr", "en")}
    except (OSError, yaml.YAMLError, KeyError, TypeError, ValueError) as exc:
        sys.stderr.write(f"History timeline generation failed: {exc}\n")
        return 1

    if args.check:
        stale = [
            str(path.relative_to(ROOT))
            for lang, path in OUTPUTS.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != rendered[lang]
        ]
        if stale:
            sys.stderr.write("Generated history fragments are stale: " + ", ".join(stale) + "\n")
            return 1
        sys.stdout.write("Generated bilingual history fragments are up to date.\n")
        return 0

    for lang, path in OUTPUTS.items():
        path.write_text(rendered[lang], encoding="utf-8")
    sys.stdout.write("Generated French and English history timeline fragments.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
