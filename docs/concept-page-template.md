# Reusable concept-page template

Use this as a **thinking scaffold**, not a mandatory page layout. Keep sections that serve the learner's question; omit or combine the rest. A short page with a clear scope is better than a long page padded to match a template.

## Suggested learning path

1. **Question and motivation** — What problem does the concept solve? Why should an LLM learner care?
2. **Intuition** — Give a mental model or concrete example, and state where the intuition stops being reliable.
3. **Definition and notation** — Define the object precisely; introduce symbols, domains, dimensions, axes, and conventions before using them.
4. **Worked example** — Trace a small example numerically or symbolically, showing intermediate steps.
5. **Application in LLMs** — Explain where and why the concept is used; distinguish essential properties from common implementation choices.
6. **Misconceptions and counterexamples** — Name common false beliefs or false equivalences, then demonstrate the limits with a counterexample or boundary case.
7. **Implementation and verification** — Link to maintained code and tests where they exist. Explain tensor shapes, masks, numerical stability, invariants, and important edge cases. If not meaningfully executable, provide an algorithm or derivation and say why.
8. **Exercises** — Ask questions that require recall, calculation, interpretation, or transfer. Hide answers by default using an accessible disclosure element; reveal a worked explanation, not only the final answer.
9. **Limitations and open questions** — State assumptions, known failure modes, unresolved debates, and what the page does not establish.
10. **Connections and next steps** — Link to prerequisites, related concepts, overview/synthesis pages, implementation, tests, and experiments in both directions where practical.
11. **References and provenance** — Cite primary/official sources for claims, pedagogical sources for teaching approaches, and verified licences/attribution for reused assets.

## Compact authoring skeleton

Adapt this structure to the site's existing Quarto conventions and page metadata; do not paste it blindly over a mature page.

```markdown
## The question

## Intuition

## Definition and notation

## Worked example

## Where it appears in LLMs

## Common misconceptions and counterexamples

## Implementation and tests

## Exercises

<details>
<summary>Show answer and reasoning</summary>

Explain the reasoning, assumptions, and any edge cases here.

</details>

## Limitations

## Connections

- Prerequisites:
- Related concepts:
- Implementation:
- Tests or experiments:
- Glossary terms:

## References
```

## Editorial rules

- State the learner question and intended outcome near the top.
- Separate formal claims from intuition, analogy, implementation conventions, and empirical findings.
- Use one consistent notation throughout the page and across linked pages; explain any deliberate difference.
- Prefer an original, legible visual when it reveals a structure that prose cannot show efficiently. Add captions, meaningful alt text, units/labels, provenance, and checked reuse rights.
- Do not assert that cosine similarity is semantic similarity, that attention weights alone explain model reasoning, or that a projected embedding plot faithfully preserves the original geometry. Treat these as prompts to investigate assumptions, not slogans to repeat.
- Use bidirectional links so readers can travel from explanation to canonical concept, code, tests, and back.
- Consider glossary additions for stable technical terms, especially terms with multiple translations or overloaded meanings. The glossary should define briefly and point to the full explanation rather than duplicate it.
- Keep the public page self-contained; links are for navigation and deeper study, not substitutes for necessary definitions or derivations.
- Check the rendered page and the other language version, not just the source.

## Acceptance question

Can a reader explain the concept in their own words, use its notation correctly, work through a small example, identify at least one important limitation or misconception, and find the corresponding implementation or verification evidence when it exists?
