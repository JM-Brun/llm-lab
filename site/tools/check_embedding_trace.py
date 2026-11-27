"""Execute the bilingual text-to-embedding examples directly from Quarto sources."""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EN_HEADING = "Optional practical trace — from text to vectors"
FR_HEADING = "Trace pratique facultative — du texte aux vecteurs"

EXPECTED_PREFIXES = {
    "en": "What have the Romans ever done for us?",
    "fr": "C'est une bonne situation, ça, scribe ?",
}


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


def assigned_string(tree: ast.AST, name: str) -> str | None:
    """Return the literal string assigned to a named variable, if present."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if (
            any(isinstance(target, ast.Name) and target.id == name for target in node.targets)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            return node.value.value
    return None


class NormalizeLiteralValues(ast.NodeTransformer):
    """Preserve trace logic while allowing localized inputs and token-ID sequences."""

    def visit_Constant(self, node: ast.Constant) -> ast.Constant:
        return ast.copy_location(ast.Constant(value=type(node.value).__name__), node)

    def visit_Compare(self, node: ast.Compare) -> ast.Compare:
        self.generic_visit(node)
        if (
            isinstance(node.left, ast.Name)
            and node.left.id == "token_ids"
            and len(node.comparators) == 1
            and isinstance(node.comparators[0], ast.List)
        ):
            # The localized prompts have different token counts, so their
            # expected ID lists differ in length while the assertion is the same.
            node.comparators[0] = ast.copy_location(
                ast.List(elts=[ast.Constant(value="token-id-sequence")], ctx=ast.Load()),
                node.comparators[0],
            )
        return node


def main() -> None:
    examples = {
        "en": extract_python_example(ROOT / "site/en/exercises-text-data.qmd", EN_HEADING),
        "fr": extract_python_example(ROOT / "site/fr/exercises-text-data.qmd", FR_HEADING),
    }

    trees = {language: ast.parse(code) for language, code in examples.items()}
    for language, tree in trees.items():
        actual_prefix = assigned_string(tree, "prefix")
        if actual_prefix != EXPECTED_PREFIXES[language]:
            raise AssertionError(
                f"The {language} tokenizer example must use its canonical running-example prefix."
            )

    # The executable structure stays bilingual-equivalent; only localized
    # strings, byte fragments and expected tokenizer-specific values may differ.
    normalized = {
        language: ast.dump(
            NormalizeLiteralValues().visit(tree),
            include_attributes=False,
        )
        for language, tree in trees.items()
    }
    if normalized["en"] != normalized["fr"]:
        raise AssertionError("The English and French tokenizer trace logic has diverged.")

    # Execute the actual documentation source, not a copied test fixture.
    for language, code in examples.items():
        namespace: dict[str, object] = {"__name__": f"embedding_trace_{language}"}
        exec(compile(code, f"<{language}-embedding-trace>", "exec"), namespace)


if __name__ == "__main__":
    main()
