"""Verify the runnable examples published on the bilingual Build pages."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("language", ["en", "fr"])
def test_build_example_runs_and_reports_its_claimed_results(language: str) -> None:
    page = (ROOT / "site" / language / "build-path.qmd").read_text(encoding="utf-8")
    examples = re.findall(r"```python\n(.*?)\n```", page, flags=re.DOTALL)
    assert len(examples) == 1, f"{language}: expected one runnable Build example"

    result = subprocess.run(
        [sys.executable, "-c", examples[0]],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    lines = result.stdout.strip().splitlines()
    assert len(lines) == 3
    assert lines[0].endswith("21426")
    for line in lines[1:]:
        ids = [int(token) for token in line.split(":", 1)[1].strip().strip("[]").split()]
        assert ids[:3] == [1, 2, 3]
        assert len(ids) == 11
        assert all(0 <= token < 50 for token in ids)
