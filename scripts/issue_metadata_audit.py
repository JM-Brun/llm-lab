#!/usr/bin/env python3
"""Read-only audit of GitHub issue classification metadata."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

PRIORITIES = {"P0", "P1", "P2", "P3"}
PRIORITY_PATTERN = re.compile(r"(?<![A-Za-z0-9])P[0-3](?![A-Za-z0-9])")


def fetch_pages(url: str, token: str | None) -> list[dict[str, Any]]:
    """Fetch every page from a GitHub REST collection."""
    items: list[dict[str, Any]] = []
    page = 1
    while True:
        request = Request(
            f"{url}{'&' if '?' in url else '?'}per_page=100&page={page}",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                **({"Authorization": f"Bearer {token}"} if token else {}),
            },
        )
        try:
            with urlopen(request, timeout=30) as response:
                batch = json.load(response)
        except (HTTPError, URLError, TimeoutError) as exc:
            raise RuntimeError(f"GitHub API request failed on page {page}: {exc}") from exc
        if not isinstance(batch, list):
            raise RuntimeError(f"Expected a JSON array from {url}")
        items.extend(item for item in batch if isinstance(item, dict))
        if len(batch) < 100:
            return items
        page += 1


def classify(
    issues: list[dict[str, Any]], known_labels: set[str]
) -> tuple[list[str], Counter[str], int]:
    """Return validation errors, priority counts and number of audited issues."""
    errors: list[str] = []
    counts: Counter[str] = Counter()
    audited = 0

    for issue in issues:
        if "pull_request" in issue or issue.get("state", "open") != "open":
            continue
        audited += 1
        number = issue.get("number", "?")
        title = str(issue.get("title", ""))
        labels = [
            str(label.get("name", ""))
            for label in issue.get("labels", [])
            if isinstance(label, dict)
        ]

        priorities = [label for label in labels if label in PRIORITIES]
        areas = [label for label in labels if label.startswith("area:")]
        types = [label for label in labels if label.startswith("type:")]

        for name, values in (
            ("priority", priorities),
            ("area", areas),
            ("type", types),
        ):
            if len(values) != 1:
                errors.append(
                    f"#{number}: expected exactly one {name} label; found "
                    f"{', '.join(values) if values else 'none'}"
                )

        for label in areas + types:
            if label not in known_labels:
                errors.append(f"#{number}: label {label!r} is not in the repository taxonomy")

        title_priorities = sorted(set(PRIORITY_PATTERN.findall(title)))
        if len(title_priorities) > 1:
            errors.append(
                f"#{number}: title contains multiple priorities ({', '.join(title_priorities)})"
            )
        elif (
            len(title_priorities) == 1
            and len(priorities) == 1
            and title_priorities[0] != priorities[0]
        ):
            errors.append(
                f"#{number}: title says {title_priorities[0]} but label is {priorities[0]}"
            )

        if len(priorities) == 1:
            counts[priorities[0]] += 1

    return errors, counts, audited


def render_report(repo: str, errors: list[str], counts: Counter[str], audited: int) -> str:
    total = sum(counts.values())
    lines = [
        "# Issue metadata audit",
        "",
        f"- Repository: `{repo}`",
        "- Scope: all open issues; pull requests excluded",
        f"- Issues audited: **{audited}**",
        f"- Issues with exactly one priority: **{total}**",
        f"- Classification errors: **{len(errors)}**",
        "",
        "| Priority | Issues |",
        "|---|---:|",
    ]
    lines.extend(f"| {priority} | {counts[priority]} |" for priority in sorted(PRIORITIES))
    lines.extend(["", "## Findings", ""])
    lines.extend(f"- {error}" for error in errors)
    if not errors:
        lines.append("No structural classification errors found.")
    lines.extend(
        [
            "",
            "> This is a read-only structural check. It does not assess semantic priority,",
            "> completion, issue dependencies, ownership or saved-search configuration.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="JM-Brun/llm-lab", help="GitHub owner/name")
    parser.add_argument("--input", help="Offline JSON fixture with issues and labels arrays")
    args = parser.parse_args()

    if args.input:
        with open(args.input, encoding="utf-8") as stream:
            fixture = json.load(stream)
        issues = fixture["issues"]
        known_labels = {
            str(label["name"]) for label in fixture["labels"] if isinstance(label, dict)
        }
    else:
        owner, separator, name = args.repo.partition("/")
        if not separator or not owner or not name:
            parser.error("--repo must use owner/name format")
        base = f"https://api.github.com/repos/{quote(owner)}/{quote(name)}"
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        labels = fetch_pages(f"{base}/labels", token)
        known_labels = {str(label.get("name", "")) for label in labels}
        issues = fetch_pages(f"{base}/issues?state=open", token)

    errors, counts, audited = classify(issues, known_labels)
    report = render_report(args.repo, errors, counts, audited)
    sys.stdout.write(report + "\\n")
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, json.JSONDecodeError, RuntimeError) as exc:
        sys.stderr.write(f"issue metadata audit: {exc}\\n")
        raise SystemExit(2) from exc
