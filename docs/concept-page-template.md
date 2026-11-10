# Concept-page quick start

Use this pattern when the reader needs to understand one concept, quantity, mathematical object, or mechanism and interpret it correctly in context. It is a **thinking aid**, not a mandatory layout. The [flexible page-template system](page-template-system.md) is the canonical composition guide; choose a more specific [scientific pattern](page-patterns.md) when it helps.

## Questions worth answering

Select the ones that support the page's actual purpose:

- What question or problem makes this concept useful?
- What is the most accurate intuitive model, and where does that intuition stop?
- What exactly is being defined? Which symbols, domains, dimensions, units, and conventions matter?
- What example makes the definition or mechanism concrete?
- How is the concept used in an LLM, and which properties are essential rather than implementation-specific?
- Which tempting interpretation, false equivalence, or boundary case should be challenged?
- What assumptions and limitations materially affect the conclusion?
- Is there a useful connection to maintained code, tests, or a deeper derivation?

## Possible composition

A compact concept page may need only a clear opening, a precise definition, one example, and a meaningful limitation. A mathematically demanding concept may need a derivation, alternative formulation, or several examples. Do not include all of them by default.

~~~markdown
<!-- State the question, object, and scope. -->

## Intuition

## Definition and interpretation

## Example
~~~

The headings are illustrative. Merge the intuition into the opening, move a caveat beside the claim it qualifies, or omit a section when it adds no explanatory value.

## Scientific and editorial safeguards

- Distinguish intuition and analogy from formal definitions, mathematical results, implementation conventions, and empirical observations.
- State material assumptions and theorem conditions; define notation before relying on it.
- Use counterexamples to expose the limits of an intuition or a common overgeneralization.
- Do not imply that cosine similarity is semantic similarity, that attention weights alone explain model reasoning, or that a low-dimensional projection preserves all original geometry.
- Keep the public explanation self-contained. Links add context or depth; they do not replace definitions needed to follow the argument.
- Put implementation walkthroughs and numerical verification in code-facing material; link them from the concept rather than duplicating a second implementation.
- Add a self-check only when a meaningful question tests the intended reasoning. Keep the answer collapsed by default and explain the reasoning, not only the result.
- Cite sources for the claims they actually support and check the rendered French/English counterparts.

For an algorithm, mathematical object, physical law, or method, consult the corresponding prompts in [page patterns](page-patterns.md).
