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

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = (
    SCRIPT_DIR.parents[1]
    if SCRIPT_DIR.name == "tools" and SCRIPT_DIR.parent.name == "site"
    else SCRIPT_DIR.parent
)
for tools_dir in (SCRIPT_DIR, ROOT / "site" / "tools"):
    if (tools_dir / "check_page_metadata.py").is_file():
        sys.path.insert(0, str(tools_dir))
        break

from check_page_metadata import _load_page, validate as validate_page_metadata
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


def route_topology(pages: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Describe route and hierarchy topology without inferring prerequisites.

    Suggested-route chains use only the route next field. Hierarchy relations
    are reported separately because they have a different meaning and must not
    be merged into the learning sequence.
    """
    topology: dict[str, dict[str, Any]] = {}
    for language in ("fr", "en"):
        language_pages = {
            page_id: page
            for page_id, page in pages.items()
            if page.get("tags", {}).get("language") == language
        }
        incoming_next: dict[str, list[str]] = defaultdict(list)
        route_edges: list[tuple[str, str]] = []
        for page_id, page in language_pages.items():
            next_id = page.get("route", {}).get("next")
            if next_id in language_pages:
                route_edges.append((page_id, next_id))
                incoming_next[next_id].append(page_id)

        starts = sorted(
            page_id
            for page_id, page in language_pages.items()
            if page.get("route", {}).get("previous") is None
            and page.get("route", {}).get("next") is not None
        )
        ends = sorted(
            page_id
            for page_id, page in language_pages.items()
            if page.get("route", {}).get("next") is None
            and page.get("route", {}).get("previous") is not None
        )
        outside_route = sorted(
            page_id
            for page_id, page in language_pages.items()
            if page.get("route", {}).get("previous") is None
            and page.get("route", {}).get("next") is None
        )

        chains: list[list[str]] = []
        covered: set[str] = set()
        for start_id in starts:
            chain: list[str] = []
            seen_in_chain: set[str] = set()
            current = start_id
            while current in language_pages and current not in seen_in_chain:
                chain.append(current)
                covered.add(current)
                seen_in_chain.add(current)
                next_id = language_pages[current].get("route", {}).get("next")
                if next_id not in language_pages:
                    break
                current = next_id
            chains.append(chain)

        route_participants = {
            page_id
            for page_id, page in language_pages.items()
            if page.get("route", {}).get("previous") is not None
            or page.get("route", {}).get("next") is not None
        }
        unrooted = sorted(route_participants - covered)
        outside_by_destination: dict[str, list[str]] = defaultdict(list)
        for page_id in outside_route:
            destination = language_pages[page_id].get("tags", {}).get(
                "destination", "unclassified"
            )
            outside_by_destination[str(destination)].append(page_id)

        hierarchy_fan_out = [
            {"page": page_id, "children": sorted(page.get("children", []))}
            for page_id, page in sorted(language_pages.items())
            if len(page.get("children", [])) > 1
        ]
        hierarchy_multi_parent = [
            {"page": page_id, "parents": sorted(page.get("parents", []))}
            for page_id, page in sorted(language_pages.items())
            if len(page.get("parents", [])) > 1
        ]
        route_merges = [
            {"page": page_id, "incoming_from": sorted(sources)}
            for page_id, sources in sorted(incoming_next.items())
            if len(sources) > 1
        ]

        topology[language] = {
            "page_count": len(language_pages),
            "route_edge_count": len(route_edges),
            "route_participant_count": len(route_participants),
            "route_starts": starts,
            "route_ends": ends,
            "outside_suggested_route": outside_route,
            "outside_suggested_route_by_destination": {
                destination: sorted(ids)
                for destination, ids in sorted(outside_by_destination.items())
            },
            "chains": chains,
            "unrooted_route_pages": unrooted,
            "route_merges": route_merges,
            "hierarchy_fan_out": hierarchy_fan_out,
            "hierarchy_multi_parent": hierarchy_multi_parent,
        }
    return topology


def audit_pages(
    pages: dict[str, dict[str, Any]],
    metadata_validation_errors: list[str] | None = None,
) -> dict[str, Any]:
    """Summarize graph topology and flag conservative editorial review candidates."""
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
        "route_topology": route_topology(pages),
        "metadata_validation_checked": metadata_validation_errors is not None,
        "metadata_validation_errors": metadata_validation_errors or [],
    }


def render_report(result: dict[str, Any]) -> str:
    """Render a concise Markdown report with explicit interpretation limits."""
    tick = chr(96)
    lines = [
        "# Page metadata audit",
        "",
        f"- Published pages analyzed: **{result['page_count']}**",
        f"- Pages with no graph relations: **{len(result['isolated_pages'])}**",
        f"- Lexical overlap candidates (capped at 30): **{len(result['editorial_candidates'])}**",
        "",
        "## Suggested-route and hierarchy topology",
        "",
        "The suggested route is derived only from " + tick + "suggested_route.next" + tick + ".",
        "Hierarchy (parents / children) and related links are reported separately; they are",
        "not interpreted as learning prerequisites or merged into a global route.",
        "",
    ]
    for language, label in (("fr", "French"), ("en", "English")):
        topology = result["route_topology"].get(language)
        if topology is None:
            continue
        lines.extend(
            [
                f"### {label} (" + tick + language + tick + ")",
                "",
                f"- Published language pages: **{topology['page_count']}**",
                f"- Suggested-route edges: **{topology['route_edge_count']}**",
                f"- Pages participating in a suggested route: **{topology['route_participant_count']}**",
                f"- Route starts: **{len(topology['route_starts'])}**",
                f"- Route ends: **{len(topology['route_ends'])}**",
                f"- Pages outside the suggested route: **{len(topology['outside_suggested_route'])}**",
                f"- Unrooted route participants: **{len(topology['unrooted_route_pages'])}**",
                "",
                "**Starts**",
                "",
            ]
        )
        lines.extend(f"- {tick}{page_id}{tick}" for page_id in topology["route_starts"])
        if not topology["route_starts"]:
            lines.append("- None")
        lines.extend(["", "**Ends**", ""])
        lines.extend(f"- {tick}{page_id}{tick}" for page_id in topology["route_ends"])
        if not topology["route_ends"]:
            lines.append("- None")
        lines.extend(["", "**Suggested-route chains**", ""])
        if topology["chains"]:
            for chain in topology["chains"]:
                lines.append(" → ".join(f"{tick}{page_id}{tick}" for page_id in chain))
        else:
            lines.append("No rooted multi-page route chain detected.")
        lines.extend(["", "**Pages outside the suggested route, by destination**", ""])
        if topology["outside_suggested_route_by_destination"]:
            for destination, page_ids in topology[
                "outside_suggested_route_by_destination"
            ].items():
                sample = ", ".join(f"{tick}{page_id}{tick}" for page_id in page_ids[:8])
                remainder = len(page_ids) - min(len(page_ids), 8)
                suffix = f" (+{remainder} more)" if remainder else ""
                lines.append(
                    f"- {tick}{destination}{tick}: **{len(page_ids)}** — {sample}{suffix}"
                )
        else:
            lines.append("- None")
        for key, heading, relation_label in (
            ("route_merges", "Route convergence points", "incoming route links"),
            ("hierarchy_fan_out", "Hierarchy fan-out hubs", "children"),
            ("hierarchy_multi_parent", "Hierarchy multi-parent nodes", "parents"),
        ):
            lines.extend(["", f"**{heading}**", ""])
            records = topology[key]
            if records:
                for record in records:
                    related = record.get("incoming_from", record.get(relation_label, []))
                    lines.append(
                        f"- {tick}{record['page']}{tick} — {len(related)} {relation_label}: "
                        + ", ".join(f"{tick}{item}{tick}" for item in related)
                    )
            else:
                lines.append("- None")
        lines.extend(["", "**Unrooted route participants**", ""])
        if topology["unrooted_route_pages"]:
            lines.extend(
                f"- {tick}{page_id}{tick}" for page_id in topology["unrooted_route_pages"]
            )
        else:
            lines.append("- None")
        lines.append("")

    lines.extend(
        [
            "A page outside the suggested route is not necessarily orphaned: optional",
            "deep dives, practice pages, reference resources and parallel Build branches",
            "may intentionally have null route links. Hierarchy fan-out is not a route",
            "branch; it describes a different relation type. Convergence and unrooted",
            "components are diagnostic signals, not automatic correction instructions.",
            "",
            "## Structural metadata validator",
            "",
        ]
    )
    if not result["metadata_validation_checked"]:
        lines.append("The existing structural validator was not run for this report.")
    elif result["metadata_validation_errors"]:
        lines.extend(
            f"- {error}" for error in result["metadata_validation_errors"]
        )
    else:
        lines.append(
            "The existing page-metadata validator reported no structural errors, "
            "including route-reference, cycle, reciprocity and FR/EN parity checks."
        )
    lines.extend(
        [
            "",
            "## Structural review candidates",
            "",
        ]
    )
    if result["isolated_pages"]:
        lines.extend(f"- {tick}{page_id}{tick}" for page_id in result["isolated_pages"])
    else:
        lines.append("No isolated pages detected.")
    lines.extend(
        [
            "",
            "A page with no graph relations is not necessarily misplaced: independent entry points,",
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
            lines.append(f"- {tick}{left}{tick} ↔ {tick}{right}{tick} — {field} (overlap {score:.3f})")
    else:
        lines.append("No pairs crossed the conservative lexical-overlap threshold.")
    lines.extend(
        [
            "",
            "## Method and limits",
            "",
            "- Only published pages represented in the explicit Quarto render list are analyzed.",
            "- French and English route graphs are described separately; structural parity is delegated to the existing validator.",
            "- Suggested-route chains use only " + tick + "suggested_route.next" + tick + "; hierarchy and related links are not used to rank or order the route.",
            "- Route-free pages are reported by destination and must not be called orphans without editorial review.",
            "- The report does not infer prerequisites, semantic equivalence, or pedagogical redundancy.",
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
        validation_errors = validate_page_metadata(args.site_dir)
        report = render_report(
            audit_pages(load_pages(args.site_dir), validation_errors)
        )
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
