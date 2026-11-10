"""Tests for the display-math delimiter checker."""

import pathlib  # noqa: I001
import subprocess
import sys


TOOLS = pathlib.Path(__file__).resolve().parents[2] / "site" / "tools"
SCRIPT = TOOLS / "check_math_delimiters.py"


def run_checker(site: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(site)],
        capture_output=True,
        check=False,
        text=True,
    )


def write_page(site: pathlib.Path, body: str) -> None:
    page = site / "fr" / "attention.qmd"
    page.parent.mkdir(parents=True)
    page.write_text(body, encoding="utf-8")


def test_accepts_double_dollar_blocks_and_inline_math(tmp_path: pathlib.Path) -> None:
    write_page(tmp_path, "Inline $x$ math stays allowed.\n\n$$\nQ = XW_Q.\n$$\n")

    result = run_checker(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "passed" in result.stdout


def test_reports_lone_single_dollar_delimiter_lines(tmp_path: pathlib.Path) -> None:
    write_page(tmp_path, "$\nQ = XW_Q.\n$\n")

    result = run_checker(tmp_path)

    assert result.returncode == 1
    assert "lone '$' line(s)" in result.stdout


def test_ignores_dollar_lines_inside_code_fences(tmp_path: pathlib.Path) -> None:
    write_page(tmp_path, "```bash\n$\nexit\n```\n\n$$\nQ = XW_Q.\n$$\n")

    result = run_checker(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
