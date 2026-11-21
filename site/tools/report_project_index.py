"""Report the canonical project index and structural FR/EN review findings."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from project_coverage import (
    UNREGISTERED_DIMENSIONS,
    bilingual_association_findings,
    build_concept_coverage,
)
from project_index import ProjectIndex

UNITS = {
    "published_page_records": "published page ID",
    "declared_topics": "distinct topic tag on a published page",
    "bilingual_topics": "topic with one published FR page and one published EN page",
    "concepts": "canonical concept ID",
    "domains": "canonical domain ID",
    "page_edges": "stored directed page-relation occurrence",
    "route_memberships": "explicit stage/language/role/page occurrence",
    "unique_route_pages": "unique page ID with at least one Understand membership",
    "revision_edges": "stored directed revision-aid/role/lesson association",
    "revision_support_by_status": "in-scope lesson page ID per assessment status",
    "pages_by_tag": "published page ID per tag value",
    "concepts_by_importance": "concept ID per importance level",
    "concepts_by_domain": "concept ID per explicit domain membership",
}


def checkout_provenance(root: Path) -> dict[str, str | bool | None]:
    """Identify HEAD and whether the report read inputs beyond that commit."""
    if not (root / ".git").exists():
        return {"commit": None, "inputs_modified": None}
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True)
        changes = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=normal", "--", "site", "data"],
            cwd=root,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "inputs_modified": None}
    return {"commit": commit.strip(), "inputs_modified": bool(changes.strip())}


def build_report(root: Path, page_filters: dict[str, str]) -> dict[str, Any]:
    index = ProjectIndex.build(root)
    coverage = build_concept_coverage(index)
    selected_ids = [page.page_id for page in index.select_pages(**page_filters)]
    return {
        "schema_version": 1,
        "source": checkout_provenance(root),
        "inputs": [
            "site/**/*.qmd",
            "data/concepts.yml",
            "data/domains.yml",
            "data/guided-route.yml",
            "data/resources.yml",
        ],
        "exclusions": ["planned and retired pages", "rendered and generated site artifacts"],
        "unregistered_coverage_dimensions": UNREGISTERED_DIMENSIONS,
        "units": UNITS,
        "project_counts": index.stats(),
        "page_selection": {
            "filters": dict(sorted(page_filters.items())),
            "unit": UNITS["published_page_records"],
            "count": len(selected_ids),
            "ids": selected_ids,
        },
        "coverage_unit": coverage["unit"],
        "coverage_state_counts": coverage["state_counts"],
        "review_findings": bilingual_association_findings(coverage),
    }


def render_markdown(report: dict[str, Any]) -> str:
    source = report["source"]
    selection = report["page_selection"]
    filters = ", ".join(f"{key}={value}" for key, value in selection["filters"].items())
    lines = [
        "# Project metadata index",
        "",
        f"- Source commit: `{source['commit'] or 'unavailable'}`",
        f"- Modified site/data paths: {source['inputs_modified']}",
        f"- Exclusions: {', '.join(report['exclusions'])}",
        f"- Page selection: **{selection['count']}** page records ({filters or 'no filters'})",
        "",
        "## Whole-project counts",
        "",
        "| Count | Unit | Total |",
        "| --- | --- | ---: |",
    ]
    lines.extend(
        f"| `{key}` | {report['units'][key]} | {value} |"
        for key, value in report["project_counts"].items()
        if isinstance(value, int)
    )
    if selection["filters"] and selection["ids"]:
        lines.extend(["", "## Selected pages", ""])
        lines.extend(f"- `{page_id}`" for page_id in selection["ids"])
    lines.extend(["", "## Structural bilingual findings", ""])
    for finding in report["review_findings"]:
        lines.append(
            f"- `{finding['entity_ids']['concept']}` → `{finding['evidence']['path']}`. "
            f"{finding['suggested_review_action']}"
        )
    if not report["review_findings"]:
        lines.append("No missing association for a uniquely paired published counterpart.")
    lines.extend(["", "## Unregistered coverage dimensions", ""])
    lines.extend(f"- **{key}** — {value}" for key, value in UNREGISTERED_DIMENSIONS.items())
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    for key in ("language", "destination", "type", "topic", "domain"):
        parser.add_argument(f"--{key}", help=f"Exact {key} filter for the page selection")
    args = parser.parse_args()
    filters = {
        key: value
        for key, value in vars(args).items()
        if key not in {"root", "format"} and value is not None
    }
    report = build_report(args.root.resolve(), filters)
    output = (
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
        if args.format == "json"
        else render_markdown(report)
    )
    sys.stdout.write(output + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
