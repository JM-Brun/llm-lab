# Page-template guide

These templates define three page archetypes for the LLM Lab knowledge base. They are **reusable starting points, not mandatory checklists**. Choose the archetype according to the reader's task, then remove sections that do not serve it.

## Choose the page type

| Archetype | Reader's task | Typical content | Avoid |
|---|---|---|---|
| **Overview / panorama** | Build a mental map and understand how ideas relate | Scope, learning outcomes, central model, a small number of distinctions, links to deeper pages | Full derivations, implementation detail, long historical digressions |
| **Concept** | Understand one technical idea and use it correctly | Motivation, intuition, formal definition, worked example, application, misconceptions, limitations | Repeating the whole overview or turning every page into a textbook chapter |
| **Reference / history** | Look up facts, compare items, or place developments in context | Scope and conventions, taxonomy or chronology, evidence and sources, caveats | Presenting a selective list as exhaustive or implying causation from chronology |

## Shared presentation rules

- **Visible by default:** the question, scope, essential explanation, main diagram, core definitions, and the links needed to continue learning.
- **Collapsed by default:** learning outcomes when they are supplementary, self-checks and exercises, worked solutions, historical side notes, optional mathematical detail, implementation notes, and extended caveats. Use descriptive titles so readers know what they will reveal.
- Do not hide content needed to understand the page's main argument. A callout is not a way to defer an essential definition.
- Prefer one meaningful hierarchy of headings. Do not create a numbered top-level section for a single caveat or a short aside.
- Use the same Quarto callout pattern for optional material:

```markdown
::: {.callout-note collapse="true" title="Optional detail"}
Supplementary explanation goes here.
:::
```

- Keep language versions structurally equivalent: same purpose, hierarchy, and disclosure behavior, while allowing natural wording.
- Link to a dedicated page when a topic needs more than a concise orientation. The overview should explain enough to orient the reader, not duplicate the destination page.

## Archetype templates

- [Overview / panorama page](overview-page-template.md)
- [Concept page](concept-page-template.md)
- [Reference / history page](reference-page-template.md)

## Review checklist

1. Is the page type clear from its purpose and content?
2. Does the opening state what the reader will understand or be able to do?
3. Are essential explanations visible without opening disclosures?
4. Are optional details and self-checks collapsed by default?
5. Does each substantial subtopic link to a canonical deeper page rather than being duplicated?
6. Are historical claims, empirical claims, and conceptual explanations distinguished?
7. Is the other language version aligned in structure and disclosure behavior?
8. Has the rendered page been checked for heading hierarchy, links, and accessible disclosure labels?
