# Reusable overview-page template

Use this archetype when a reader needs a **map of a topic**, not a complete technical treatment. An overview should establish the central mental model, distinguish nearby concepts, and route readers to dedicated pages for depth.

## Suggested structure

1. **Scope and orientation** — What is covered, what is not, and why the topic matters.
2. **Learning outcomes** — A short list of capabilities the reader should gain. Keep this supplementary block collapsed by default.
3. **Central question or problem** — Introduce the problem in concrete, non-technical terms.
4. **Core mental model** — One diagram or compact explanation that organizes the topic.
5. **Essential distinctions** — A small number of distinctions needed to avoid category errors.
6. **How the pieces connect** — A concise process, taxonomy, or map. Link each substantial phase or concept to its dedicated page.
7. **Applications and boundaries** — What the topic helps explain, and what it does not establish.
8. **Self-check** — A few transfer-oriented questions, collapsed by default; hide answers individually.
9. **Further study** — Prerequisites, deeper explanations, implementation, experiments, and references.

## Compact authoring skeleton

Adapt numbering and labels to the actual page. Do not retain empty sections.

```markdown
::: {.chapter-lead}
A concise statement of the topic, its central idea, and its scope.
:::

::: {.callout-note .learning-outcomes collapse="true" title="Learning outcomes"}
By the end of this page, you should be able to:
- ...
:::

## The central question

## A mental model

## Essential distinctions

## How the pieces connect

Link each substantial concept to its dedicated page.

## Applications and boundaries

::: {.callout-note collapse="true" title="Check your understanding"}
A small number of questions that test interpretation and transfer.

<details>
<summary>Show the reasoning</summary>

A worked explanation, including assumptions and limits.

</details>
:::

## Further study

- Prerequisites:
- Deeper explanations:
- Implementation or experiments:
- References:
```

## Editorial rules

- Do not turn an overview into a miniature version of every child page. Define terms briefly and link out for derivations, algorithms, and implementation.
- Keep the main narrative linear. Use collapsed callouts for historical context, optional formalization, and caveats that do not change the central mental model.
- A diagram should clarify relationships or process, not merely repeat adjacent prose.
- Avoid calling a partial conceptual sequence a complete lifecycle or pipeline. State omitted stages when that distinction matters.
- Prefer a small number of well-chosen links placed on the relevant concept, not a paragraph announcing that a deeper page exists.
