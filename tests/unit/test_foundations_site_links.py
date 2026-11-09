"""Docstring links from the reference code to the published site must resolve.

The published site is the rendered Quarto project: ``site/<path>.qmd`` is
served at ``https://jm-brun.github.io/llm-lab/<path>.html``, and a directory
URL is only served when ``site/<path>/index.qmd`` exists. The rendered-site
link checker does not read Python source, so this test guards the links that
learners follow from ``src/llm_lab`` to the walkthrough and concept pages.
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
SITE_URL = re.compile(r"https://jm-brun\.github\.io/llm-lab/([^\s)>\"'`]*)")


def _source_page(url_path: str) -> pathlib.Path:
    """Return the Quarto source that the published URL path is rendered from."""
    if url_path == "" or url_path.endswith("/"):
        return SITE / url_path / "index.qmd"
    if url_path.endswith(".html"):
        return SITE / f"{url_path.removesuffix('.html')}.qmd"
    return SITE / url_path


def _site_links() -> list[tuple[str, str]]:
    links = []
    for path in sorted((ROOT / "src" / "llm_lab").rglob("*.py")):
        for match in SITE_URL.finditer(path.read_text(encoding="utf-8")):
            links.append((str(path.relative_to(ROOT)), match.group(1)))
    return links


def test_reference_code_links_to_site_pages() -> None:
    assert _site_links(), "expected docstring links from src/llm_lab to the site"


def test_reference_code_site_links_resolve_to_published_pages() -> None:
    broken = [
        f"{source}: {url_path}"
        for source, url_path in _site_links()
        if not _source_page(url_path).is_file()
    ]

    assert not broken, "site links without a published page:\n" + "\n".join(broken)
