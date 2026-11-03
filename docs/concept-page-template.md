# Concept-page quick start

Use this file when creating or substantially revising a concept page. It is a **lightweight starting point**, not a required outline.

The authoritative guidance is the [flexible page-template system](page-template-system.md); choose a more specific [page pattern](page-patterns.md) when the subject is primarily an algorithm, mathematical or physical concept, architecture, technology, method, or overview.

## Start with the question

Before choosing headings, write down:

- **Question:** what should the reader understand?
- **Context:** where does this concept matter in an LLM?
- **Core idea:** what is the shortest accurate mental model?
- **Boundary:** what important detail belongs elsewhere?

Then select only the sections that support that outcome. A compact page may need just an intuition, definition, example, and limitation. A more technical page may need derivations, implementation details, or several examples. Do not add a heading merely because it appears in a suggested list.

## Possible ingredients

Use, combine, reorder, or omit as appropriate:

1. Motivation and intuition.
2. Definition, notation, assumptions, and conventions.
3. Mechanism or formal derivation.
4. Worked example or visual explanation.
5. Application in an LLM.
6. Properties, variants, and comparisons.
7. Misconceptions, counterexamples, and limitations.
8. Implementation, tests, or experiments when they exist.
9. Exercises or a short self-check.
10. Contextual connections and references.

Keep essential assumptions and caveats visible. Put genuinely optional derivations, extended examples, and answer keys behind the existing accessible disclosure pattern.

## Compact skeleton

Adapt this skeleton; do not paste it over a mature page without review.

```markdown
<!-- State the specific question and scope in the opening. -->

## Intuition

## Definition and mechanism

## Example

## Application in LLMs

## Limitations and common misconceptions

## Verify your understanding

## References
```

The headings above are suggestions, not mandatory sections. Delete, rename, merge, or add sections whenever the reader's question calls for it.

## Before publishing

- Keep the page self-contained for its LLM-specific learning objective.
- Use consistent notation and define symbols, dimensions, axes, and conventions.
- Link to canonical neighbouring pages; do not duplicate their full explanations.
- Maintain the `LLM-LAB-PAGE-MAP` comment and controlled tags from [page-metadata-schema.md](page-metadata-schema.md).
- Reuse existing callouts and visual styles from [design-system.md](design-system.md).
- Check the rendered page and its French/English counterpart.
