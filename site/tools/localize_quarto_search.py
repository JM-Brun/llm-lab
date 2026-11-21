"""Keep Quarto's search UI and scope its local index to the current page language."""

import os
from pathlib import Path

SEARCH_ASSET = Path("site_libs/quarto-search/quarto-search.js")
QUARTO_LOOP = """        searchDocs.forEach(function (searchDoc) {
          fuse.add(searchDoc);
        });"""
LOCALIZED_LOOP = """        // LLM Lab: scope the documents before Fuse ranks or limits the results.
        const lang = document.documentElement.lang.toLowerCase().split("-")[0];
        searchDocs.forEach(function (searchDoc) {
          const path = searchDoc.href.split(/[?#]/, 1)[0];
          // The two indexed pages outside fr/ and en/ declare lang: fr.
          const frenchRootPage = path === "index.html" || path === "references.html";
          if ((lang !== "fr" && lang !== "en") || path.startsWith(`${lang}/`) ||
              (lang === "fr" && frenchRootPage)) {
            fuse.add(searchDoc);
          }
        });"""


def localize_search_asset(output_dir: Path) -> None:
    asset = output_dir / SEARCH_ASSET
    source = asset.read_text(encoding="utf-8")
    if LOCALIZED_LOOP in source:
        return
    # Quarto 1.x does not expose an index-language filter in website.search.
    # Fail on an upstream change rather than publishing mixed results again.
    if source.count(QUARTO_LOOP) != 1:
        raise ValueError(f"Unexpected Quarto search index loader in {asset}")
    asset.write_text(source.replace(QUARTO_LOOP, LOCALIZED_LOOP, 1), encoding="utf-8")


if __name__ == "__main__":
    localize_search_asset(Path(os.environ["QUARTO_PROJECT_OUTPUT_DIR"]))
