#!/usr/bin/env python3
"""Produce a review-oriented report from the bilingual page metadata graph.

This audit emits candidates for human review; it does not fail builds or infer
that lexical similarity proves duplicated teaching content.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_page_metadata import _load_page

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"[^\W\d_]{3,}", re.UNICODE)
STOPWORDS = {
    "avec",
    "dans",
    "des",
    "est",
    "les",
    "par",
    "pour",
    "que",
    "qui",
    "sur",
    "the",
    "and",
    "for",
    "from",
    "into",
    "that",
    "this",
    "with",
    "what",
}


def lexical_overlap(left: str, right: str) -> float:
    """Return Jaccard overlap of informative word tokens."""
    a = {word for word in TOKEN.findall(left.casefold()) if word not in STOPWORDS}
    b = {word for word in TOKEN.findall(right.casefold()) if word not in STOPWORDS}
    if len(a) < 4 or len(b) < 4:
        return 0.0
    return len(a & b) / len(a | b)


def audit_pages(pages: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Summarize graph structure and flag conservative editorial review candidates."""
    incoming: dict[str, set[str]] = defaultdict(set)
    for page_id, page in pages.items():
        targets = [
            page["route"].get("next"),
            *page["parents"],
            *page["children"],
            *page["related"],
        ]
        for target in targets:
            if target in pages:
                incoming[target].add(page_id)

    isolated = []
    for page_id, page in pages.items():
        outgoing = any(
            (
                page["route"].get("previous"),
                page["route"].get("next"),
                page["parents"],
                page["children"],
                page["related"],
            )
        )
        if not outgoing and not incoming[page_id]:
            isolated.append(page_id)

    candidates: list[dict[str, Any]] = []
    by_language: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for page_id, page in pages.items():
        language = page["tags"].get("language")
        if language in {"fr", "en"}:
            by_language[language].append((page_id, page))

    for language, language_pages in by_language.items():
        for index, (left_id, left) in enumerate(language_pages):
            for right_id, right in language_pages[index + 1 :]:
                for field in ("scope", "purpose"):
                    score = lexical_overlap(left.get(field, ""), right.get(field, ""))
                    if score >= 0.6:
                        candidates.append(
                            {
                                "language": language,
                                "field": field,
                                "score": round(score, 3),
                                "pages": [left_id, right_id],
                            }
                        )

    candidates.sort(key=lambda item: (-item["score"], item["pages"], item["field"]))
    return {
        "page_count": len(pages),
        "isolated_pages": sorted(isolated),
        "editorial_candidates": candidates[:30],
    }


def render_report(result: dict[str, Any]) -> str:
    """Render a concise Markdown report with explicit interpretation limits."""
    lines = [
        "# Page metadata audit",
        "",
        f"- Published pages analyzed: **{result['page_count']}**",
        f"- Pages with no graph relations: **{len(result['isolated_pages'])}**",
        f"- Lexical overlap candidates (capped at 30): **{len(result['editorial_candidates'])}**",
        "",
        "## Structural review candidates",
        "",
    ]
    if result["isolated_pages"]:
        lines.extend(f"- `{page_id}`" for page_id in result["isolated_pages"])
    else:
        lines.append("No isolated pages detected.")
    lines.extend(
        [
            "",
            "A page with no graph relations is not necessarily misplaced: independent entry points",
            "reference resources, and optional branches may be intentionally weakly connected.",
            "",
            "## Possible scope or purpose overlap",
            "",
            "These pairs share at least 0.60 Jaccard overlap among informative word tokens.",
            "This is a lexical triage signal only; it does not establish duplicate explanations,",
            "shared learning objectives, or a need to merge pages.",
            "",
        ]
    )
    if result["editorial_candidates"]:
        for item in result["editorial_candidates"]:
            left, right = item["pages"]
            field = item["field"]
            score = item["score"]
            lines.append(f"- `{left}` ↔ `{right}` — {field} (overlap {score:.3f})")
    else:
        lines.append("No pairs crossed the conservative lexical-overlap threshold.")
    lines.extend(
        [
            "",
            "## Method and limits",
            "",
            "- Only published pages represented in the rendered page metadata graph are analyzed.",
            "- French and English pages are compared separately; "
            "translated counterparts are not compared lexically.",
            "- Graph isolation checks all declared route, hierarchy, and related edges.",
            "- The report does not infer prerequisites, semantic equivalence, "
            "or pedagogical redundancy.",
            "- Review candidates require inspection of page objectives and actual body content.",
            "",
        ]
    )
    return "\n".join(lines)


def load_pages(site_dir: Path) -> dict[str, dict[str, Any]]:
    """Load valid page records from the explicit Quarto render list."""
    config = yaml.safe_load((site_dir / "_quarto.yml").read_text(encoding="utf-8"))
    render_list = config["project"]["render"]
    pages: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for entry in render_list:
        page = _load_page(site_dir / entry, site_dir, errors)
        if page is not None:
            pages[page["id"]] = page
    if errors:
        raise ValueError("Metadata errors prevent audit:\n" + "\n".join(errors))
    return pages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=ROOT / "site")
    parser.add_argument("--output", type=Path, help="Write Markdown report to this path")
    args = parser.parse_args()
    try:
        report = render_report(audit_pages(load_pages(args.site_dir)))
    except (OSError, KeyError, TypeError, ValueError, yaml.YAMLError) as exc:
        sys.stderr.write(f"Cannot audit page metadata: {exc}\n")
        return 1
    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
