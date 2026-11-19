#!/usr/bin/env python3
"""Audit required metadata on all open GitHub issues in a repository."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from typing import Any

PRIORITY = re.compile(r"P[0-3]")
TITLE_PRIORITY = re.compile(r"^\s*\[?(P[0-3])(?:\b|\s*[·:])", re.IGNORECASE)


def audit_issues(issues: list[dict[str, Any]]) -> dict[str, Any]:
    """Return deterministic metadata defects and priority counts."""
    defects: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for issue in issues:
        if "pull_request" in issue:
            continue
        labels = [
            label.get("name", "")
            for label in issue.get("labels", [])
            if isinstance(label, dict)
        ]
        priorities = [label for label in labels if PRIORITY.fullmatch(label)]
        areas = [label for label in labels if label.startswith("area:")]
        types = [label for label in labels if label.startswith("type:")]
        counts[priorities[0] if len(priorities) == 1 else "unclassified"] += 1
        problems: list[str] = []
        for name, values in (("priority", priorities), ("area", areas), ("type", types)):
            if not values:
                problems.append(f"missing {name}")
            elif len(values) > 1:
                problems.append(f"multiple {name} labels")
        match = TITLE_PRIORITY.match(issue.get("title", ""))
        if match and len(priorities) == 1 and match.group(1).upper() != priorities[0]:
            problems.append(
                f"title says {match.group(1).upper()} but label is {priorities[0]}"
            )
        if problems:
            defects.append(
                {
                    "number": issue.get("number"),
                    "title": issue.get("title", ""),
                    "problems": problems,
                }
            )
    return {
        "issue_count": sum(counts.values()),
        "priority_counts": {
            key: counts.get(key, 0)
            for key in ("P0", "P1", "P2", "P3", "unclassified")
        },
        "defects": defects,
    }


def fetch_open_issues(repository: str) -> list[dict[str, Any]]:
    """Fetch every page through the authenticated GitHub CLI."""
    result = subprocess.run(
        [
            "gh", "api", "--paginate", "--slurp",
            f"repos/{repository}/issues?state=open&per_page=100",
        ],
        check=True, capture_output=True, text=True,
    )
    pages = json.loads(result.stdout)
    return [issue for page in pages for issue in page]


def main() -> int:
    repository = sys.argv[1] if len(sys.argv) > 1 else "JM-Brun/llm-lab"
    try:
        issues = fetch_open_issues(repository)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"Could not fetch issues for {repository}: {exc}", file=sys.stderr)
        return 2
    report = audit_issues(issues)
    print(f"Repository: {repository}")
    print(f"Open issues: {report['issue_count']}")
    for priority, count in report["priority_counts"].items():
        print(f"  {priority}: {count}")
    if report["defects"]:
        for defect in report["defects"]:
            print(
                f"  #{defect['number']} {defect['title']}: "
                + "; ".join(defect["problems"])
            )
        return 1
    print("Required metadata is complete and title priorities are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
