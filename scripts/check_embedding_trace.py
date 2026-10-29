"""Execute the bilingual text-to-embedding example directly from the Quarto sources."""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_HEADING = "One reproducible trace: text → token IDs → embedding rows"
FR_HEADING = "Une trace reproductible : texte → IDs → lignes d'embedding"


def extract_python_example(path: Path, heading: str) -> str:
    """Return the first Python fenced block following the target heading."""
    text = path.read_text(encoding="utf-8")
    start = text.find(heading)
    if start < 0:
        raise AssertionError(f"Missing expected heading in {path}: {heading}")
    section = text[start + len(heading) :]
    match = re.search(r"\n\s*```python\s*\n(.*?)\n```", section, flags=re.DOTALL)
    if match is None:
        raise AssertionError(f"Missing Python block after {heading!r} in {path}")
    return match.group(1)


def main() -> None:
    examples = {
        "en": extract_python_example(ROOT / "site/en/embedding-space.qmd", EN_HEADING),
        "fr": extract_python_example(ROOT / "site/fr/embedding-space.qmd", FR_HEADING),
    }
    # Comments may be translated; executable statements must stay in sync.
    trees = {
        language: ast.dump(ast.parse(code), include_attributes=False)
        for language, code in examples.items()
    }
    if trees["en"] != trees["fr"]:
        raise AssertionError("The English and French tokenizer examples have diverged.")

    # Execute the actual documentation source, not a copied test fixture.
    for language, code in examples.items():
        namespace: dict[str, object] = {"__name__": f"embedding_trace_{language}"}
        exec(compile(code, f"<{language}-embedding-trace>", "exec"), namespace)


if __name__ == "__main__":
    main()
