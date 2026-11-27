"""Fast editorial guardrails for the lessons in the canonical core route."""

from __future__ import annotations

import warnings
from pathlib import Path

import pytest
from lesson_duration import DURATION_EXCEPTIONS, estimate_lesson_duration
from strict_yaml import load_yaml

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
ROUTE_FILE = ROOT / "data" / "guided-route.yml"
TARGET_MINUTES = (10.0, 15.0)
HARD_LIMIT_MINUTES = 25.0


@pytest.fixture(scope="module")
def core_lessons() -> list[tuple[str, str, str]]:
    """Read only the bilingual page IDs listed as core lessons in guided-route.yml."""
    route = load_yaml(ROUTE_FILE)
    lessons: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    for stage in route["stages"]:
        for language in ("fr", "en"):
            for page_id in stage["pages"][language]:
                key = (language, page_id)
                if key in seen:
                    continue
                seen.add(key)
                source = SITE / f"{page_id}.qmd"
                assert source.is_file(), f"Missing core lesson source: {source}"
                lessons.append((language, page_id, source.read_text(encoding="utf-8")))
    return lessons


def test_estimator_counts_learning_content_but_excludes_non_core_sections() -> None:
    sample = """---
title: Example
---
<!-- page metadata -->
## Main idea

A sentence with an equation $x = y$.

```python
x = 1
y = 2
```

## Exercises

This should not contribute to the estimate.

## Deepen

Neither should this.
"""
    estimate = estimate_lesson_duration(sample)
    assert estimate.prose_words == 7
    assert estimate.code_lines == 2
    assert estimate.inline_equations == 1
    assert estimate.minutes == 0.5


def test_estimator_excludes_collapsed_optional_callouts_with_nested_divs() -> None:
    sample = """## Main idea

Visible content remains in the estimate.

::::: {.callout-note collapse="true" title="Optional deep dive"}
This outer content is optional.

::: {.callout-tip}
Nested content is optional too.
:::
:::::

More visible content remains in the estimate.
"""
    estimate = estimate_lesson_duration(sample)
    assert estimate.prose_words == 15


def test_estimator_counts_expanded_callouts() -> None:
    sample = """## Main idea

::: {.callout-note}
This expanded content is part of the reading path.
:::
"""
    estimate = estimate_lesson_duration(sample)
    assert estimate.prose_words == 11


def test_core_route_lessons_stay_within_the_editorial_duration_budget(
    core_lessons: list[tuple[str, str, str]],
) -> None:
    page_ids = {page_id for _, page_id, _ in core_lessons}
    assert set(DURATION_EXCEPTIONS) <= page_ids
    assert all(reason.strip() for reason in DURATION_EXCEPTIONS.values())

    out_of_target: list[str] = []
    over_hard_limit: list[str] = []
    for language, page_id, source in core_lessons:
        estimate = estimate_lesson_duration(source)
        label = f"{language}/{page_id.rsplit('/', maxsplit=1)[-1]}"
        if estimate.minutes > HARD_LIMIT_MINUTES:
            if page_id not in DURATION_EXCEPTIONS:
                over_hard_limit.append(f"{label}: {estimate.minutes:.1f} min")
        elif not TARGET_MINUTES[0] <= estimate.minutes <= TARGET_MINUTES[1]:
            out_of_target.append(f"{label}: {estimate.minutes:.1f} min")

    assert not over_hard_limit, (
        "Core lessons exceed 25 minutes without a documented pedagogical exception: "
        + ", ".join(over_hard_limit)
        + ". Split or refocus the lesson, or document a justified exception."
    )
    if out_of_target:
        warnings.warn(
            "Core lessons outside the 10-15 minute target (review for balance): "
            + ", ".join(out_of_target),
            UserWarning,
            stacklevel=1,
        )
