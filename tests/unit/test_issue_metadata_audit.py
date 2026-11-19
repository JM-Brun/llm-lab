from scripts.issue_metadata_audit import classify, render_report


def test_valid_issue_metadata_passes() -> None:
    labels = {"P2", "area:governance", "type:audit"}
    issues = [
        {
            "number": 12,
            "title": "[P2] Review governance",
            "state": "open",
            "labels": [{"name": label} for label in labels],
        }
    ]

    errors, counts, audited = classify(issues, labels)

    assert errors == []
    assert counts == {"P2": 1}
    assert audited == 1


def test_missing_multiple_and_unknown_labels_are_reported() -> None:
    known = {"P1", "P2", "area:governance", "type:audit"}
    issues = [
        {
            "number": 21,
            "title": "[P1] Conflicting priority",
            "state": "open",
            "labels": [
                {"name": "P2"},
                {"name": "P1"},
                {"name": "area:unknown"},
                {"name": "type:audit"},
                {"name": "type:feature"},
            ],
        }
    ]

    errors, counts, audited = classify(issues, known)

    assert audited == 1
    assert counts == {}
    assert any("expected exactly one priority" in error for error in errors)
    assert any("expected exactly one area" in error for error in errors)
    assert any("expected exactly one type" in error for error in errors)
    assert any("not in the repository taxonomy" in error for error in errors)
    assert any("multiple priorities" in error for error in errors)


def test_title_and_priority_label_must_agree() -> None:
    known = {"P3", "area:governance", "type:documentation"}
    issues = [
        {
            "number": 34,
            "title": "[P1] Optional cleanup",
            "state": "open",
            "labels": [{"name": label} for label in known],
        }
    ]

    errors, _, _ = classify(issues, known)

    assert any("title says P1 but label is P3" in error for error in errors)


def test_pull_requests_and_closed_issues_are_excluded() -> None:
    known = {"P2", "area:governance", "type:audit"}
    issues = [
        {"number": 1, "pull_request": {}, "labels": []},
        {"number": 2, "state": "closed", "labels": []},
    ]

    errors, counts, audited = classify(issues, known)

    assert errors == []
    assert counts == {}
    assert audited == 0


def test_report_states_structural_scope_and_limitations() -> None:
    report = render_report("JM-Brun/llm-lab", [], {"P2": 3}, 3)

    assert "Issues audited: **3**" in report
    assert "semantic priority" in report
    assert "No structural classification errors" in report
