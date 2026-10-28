"""Tests for the rendered-site local link checker."""

import sys
from pathlib import Path
from subprocess import CompletedProcess, run


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_site_links.py"


def run_checker(site: pathlib.Path) -> CompletedProcess[str]:
    return run(
        [sys.executable, str(SCRIPT), str(site)],
        capture_output=True,
        check=False,
        text=True,
    )


def test_accepts_existing_files_fragments_and_external_links(tmp_path: pathlib.Path) -> None:
    (tmp_path / "index.html").write_text(
        '<a href="guide.html#intro">Guide</a><a href="https://example.com/docs">External</a>',
        encoding="utf-8",
    )
    (tmp_path / "guide.html").write_text(
        '<h1 id="intro">Introduction</h1>',
        encoding="utf-8",
    )

    result = run_checker(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "passed" in result.stdout


def test_reports_missing_local_file(tmp_path: pathlib.Path) -> None:
    (tmp_path / "index.html").write_text(
        '<a href="missing.html">Missing</a>',
        encoding="utf-8",
    )

    result = run_checker(tmp_path)

    assert result.returncode == 1
    assert "missing target" in result.stdout


def test_reports_missing_fragment(tmp_path: pathlib.Path) -> None:
    (tmp_path / "index.html").write_text(
        '<a href="guide.html#absent">Guide</a>',
        encoding="utf-8",
    )
    (tmp_path / "guide.html").write_text(
        '<h1 id="present">Guide</h1>',
        encoding="utf-8",
    )

    result = run_checker(tmp_path)

    assert result.returncode == 1
    assert "missing fragment" in result.stdout
