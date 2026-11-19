from __future__ import annotations

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_issue_metadata.py"
SPEC = importlib.util.spec_from_file_location("audit_issue_metadata", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_audit_counts_open_issues_and_excludes_pull_requests() -> None:
    report = MODULE.audit_issues(
        [
            {
                "number": 1,
                "title": "[P1 · architecture] Build a graph",
                "labels": [
                    {"name": "P1"},
                    {"name": "area:architecture"},
                    {"name": "type:feature"},
                ],
            },
            {"number": 2, "title": "A pull request", "pull_request": {}},
        ]
    )
    assert report["issue_count"] == 1
    assert report["priority_counts"]["P1"] == 1
    assert report["defects"] == []


def test_audit_reports_missing_and_multiple_labels() -> None:
    report = MODULE.audit_issues(
        [
            {
                "number": 7,
                "title": "[P1 · source] Review evidence",
                "labels": [
                    {"name": "P2"},
                    {"name": "P3"},
                    {"name": "area:sources"},
                    {"name": "area:architecture"},
                ],
            },
            {"number": 8, "title": "Unclassified task", "labels": [{"name": "documentation"}]},
        ]
    )
    assert report["issue_count"] == 2
    assert report["priority_counts"]["unclassified"] == 2
    assert report["defects"][0]["problems"] == [
        "multiple priority labels", "multiple area labels"
    ]
    assert report["defects"][1]["problems"] == [
        "missing priority", "missing area", "missing type"
    ]


def test_audit_detects_title_priority_disagreement() -> None:
    report = MODULE.audit_issues(
        [
            {
                "number": 9,
                "title": "[P1 · source] Review evidence",
                "labels": [
                    {"name": "P2"},
                    {"name": "area:sources"},
                    {"name": "type:audit"},
                ],
            }
        ]
    )
    assert report["defects"][0]["problems"] == [
        "title says P1 but label is P2"
    ]
