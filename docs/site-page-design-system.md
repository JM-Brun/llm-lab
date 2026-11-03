# LLM Lab page design system

## Purpose: a soft target, not a rigid standard

The goal is **controlled convergence**. Pages should feel related, be predictable to navigate, and remain easy to refactor together. They should not become identical: a mathematical derivation, a code walkthrough, and a historical timeline have different instructional needs.

Treat this document as a soft target:

- **Required contract:** stable page metadata, valid links, bilingual parity where a counterpart exists, and accessible disclosure behavior.
- **Recommended default:** page archetype, section hierarchy, opening orientation, callout roles, self-check placement, and navigation conventions.
- **Contextual choice:** diagrams, worked examples, code, exercises, historical notes, and the exact section order. Include them only when they serve the learning objective.

A page may depart from the default when the reason is clear. Prefer a documented exception over adding a new one-off convention.

## 1. Connect the existing taxonomy to page archetypes

The existing `LLM-LAB-PAGE-MAP v1` metadata remains the canonical inventory and learning graph. Do not introduce a second competing page registry. Its `type` tag determines the default archetype:

| Existing `type` | Default archetype | Template / guidance |
|---|---|---|
| `entry-point` | Orientation | Overview template, adapted for navigation |
| `system-overview` | Overview | [Overview template](overview-page-template.md) |
| `concept-lesson` | Explanation | [Concept template](concept-page-template.md) |
| `concept-bridge` | Explanation / bridge | Concept template; emphasize prerequisites and onward links |
| `deep-dive` | Explanation / deep dive | Concept template; formalism and derivations become central |
| `guided-build` | Procedural | [Guided-build template](guided-build-page-template.md) |
| `exercise-hub` | Practice | [Practice template](practice-page-template.md) |
| `experiment-guide` | Practice / experiment | Practice template; emphasize protocol and reproducibility |
| `glossary` | Reference | [Reference template](reference-page-template.md), concise entries |
| `historical-reference` | Reference / history | [Reference template](reference-page-template.md) |
| `bibliography` | Reference | Reference template; source roles and provenance |

The other metadata dimensions keep their existing roles:

- `destination`: what the learner is expected to do next (`orient`, `understand`, `build`, `deepen`, `practice`, `reference`).
- `level`: expected depth (`overview`, `core`, `applied`, `advanced`, `reference`).
- `topic`: stable bilingual topic identifier.
- `language` and `status`: language counterpart and publication state.
- `scope`, `purpose`, `suggested_route`, `hierarchy`, and `related`: the page's contract and position in the learning graph.

The page-map comment and front-matter `keywords` must continue to agree. The existing `scripts/check_page_metadata.py` and CI checks enforce the graph and bilingual consistency; templates should use these fields, not invent local navigation metadata.

## 2. Shared page anatomy

Not every page needs every part. This is the default reading order, not a checklist.

1. **Title and subtitle** — name the object and signal the scope or question.
2. **Opening orientation** — one concise paragraph or `.chapter-lead` giving the central idea and boundary.
3. **Learning outcomes** — optional, short, and collapsed by default when supplementary.
4. **Main learning sequence** — the smallest coherent set of sections that answers the page's question.
5. **Boundary / limitations** — explicit assumptions and non-claims where misunderstanding is likely.
6. **Self-check** — short questions embedded near the end or after a major unit; collapsed by default when supplementary, with answers individually hidden.
7. **Further study / references** — links to prerequisites, canonical deeper pages, implementation, experiments, and sources.
8. **Language switch** — use the established `.language-switch` pattern.

A page should not add a top-level section solely to host one short aside. Use a collapsed callout for optional historical context, caveats, implementation notes, or mathematical detail. Keep essential definitions and the main argument visible.

## 3. Shared Quarto presentation patterns

Use the site's existing classes and Quarto callouts rather than introducing page-specific HTML/CSS for common roles.

### Opening lead

```markdown
::: {.chapter-lead}
State the central idea, the scope, and the most important boundary in a few sentences.
:::
```

### Learning outcomes

```markdown
::: {.callout-note .learning-outcomes collapse="true" title="Learning outcomes"}
By the end of this page, you should be able to:
- explain ...
- distinguish ...
- apply ...
:::
```

Use the natural French equivalent for the title. Outcomes should be observable actions, not a copy of the table of contents.

### Key intuition

```markdown
::: {.callout-tip title="The key idea"}
Give one compact mental model and state where it stops being reliable.
:::
```

Do not repeat the opening lead verbatim. Use this only when the page benefits from a second, more operational summary.

### Self-check

```markdown
::: {.callout-note collapse="true" title="Check your understanding"}
1. Ask a question requiring explanation, calculation, interpretation, or transfer.

<details>
<summary>Show the reasoning</summary>

Explain the reasoning, assumptions, and an important boundary case.

</details>
:::
```

Use the existing `.self-check` class only where legacy styling or page-specific behavior requires it. Prefer one canonical Quarto callout pattern for new work. Avoid nesting several disclosure layers without a clear reason.

### Optional side note

```markdown
::: {.callout-note collapse="true" title="Historical context"}
Keep supplementary context here. Link to a dedicated page when the topic needs more than a short note.
:::
```

### Language switch

```markdown
::: {.language-switch}
**Language:** [Français](page.qmd) · [English](../en/page.qmd)
:::
```

Keep the established class so the switch remains visually consistent.

## 4. Visual design contract

The shared visual language is already implemented in `site/styles.scss`. Reuse its semantic classes and tokens:

| Role | Existing class / token | Use |
|---|---|---|
| Opening statement | `.chapter-lead` | Scope and central idea |
| Main site identity | `.hero-intro` | Entry-point hero only, not ordinary lesson sections |
| Key idea | `.callout-tip` | One useful intuition |
| Supplementary content | `.callout-note` | Optional detail, caveat, historical note |
| Learning outcomes | `.learning-outcomes` | Short outcomes block |
| Language navigation | `.language-switch` | Bilingual page switch |
| Reading surfaces | `--llm-paper`, `--llm-line`, `--llm-ink` | Neutral, consistent surfaces |

Avoid adding new colors, radii, shadows, or card patterns for an individual page when an existing semantic class already expresses the role. If a recurring need cannot be met by the current system, add one reusable class/token in `site/styles.scss` and document it here.

Prefer native Markdown and Quarto components. Custom HTML should be reserved for cases where semantic Quarto/Markdown cannot express the needed structure accessibly.

## 5. Convergence rules

- **One concept, one canonical destination.** Overview pages orient and link out; they should not reproduce the full derivation or implementation.
- **Consistent section semantics.** A heading should represent a substantial learning unit, not a decorative label or a single caveat.
- **Predictable disclosures.** Optional outcomes, self-checks, answers, and side notes are collapsed by default. Essential content is not hidden.
- **Bidirectional learning graph.** Use the metadata graph for structural relations and prose links for meaningful navigation. Do not add a link just to satisfy a quota.
- **Bilingual structural parity.** French and English pages should share purpose, conceptual sequence, disclosure behavior, and equivalent links, while using idiomatic language.
- **No forced uniformity.** A page may omit a suggested section or change order when the learning task requires it.
- **Refactor shared patterns centrally.** When a recurring design or content pattern changes, update the relevant template and this contract; then migrate affected pages incrementally.

## 6. Practical review checklist

- Does the page's metadata type map to the archetype actually used?
- Does the opening explain scope and purpose without duplicating the subtitle?
- Is the main learning sequence visible and coherent?
- Are optional content and self-checks collapsed by default?
- Are headings substantive and correctly nested?
- Are substantial topics linked to canonical destination pages?
- Does the bilingual counterpart have the same learning intent and disclosure behavior?
- Does the page reuse existing classes before adding custom CSS?
- Has the rendered page been checked at desktop and mobile widths?
