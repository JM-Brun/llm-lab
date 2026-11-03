# Page archetype implementation map

**Purpose:** connect the reusable page templates to the existing LLM Lab editorial, visual, and metadata contracts. This file is an index and mapping layer, not a second design system.

## Sources of truth

Use the existing documents according to their responsibility:

| Concern | Canonical document |
|---|---|
| Visual identity, colors, typography, responsive behavior, accessibility | [Visual design system](design-system.md) |
| Reader experience, progressive disclosure, page roles, editorial economy | [Reader experience and editorial method](reader-experience-and-editorial-method.md) |
| Page metadata, controlled taxonomy, learning graph, bilingual parity | [Page metadata contract](page-metadata-schema.md) |
| Page inventory, ownership boundaries, destination and content placement | [Content-section mapping](content-section-mapping.md) |
| Contributor rules and scientific/pedagogical acceptance | [Contributor guiding principles](contributor-guiding-principles.md) |
| Reusable section patterns and starter skeletons | [Page-template guide](page-template-guide.md) |

If guidance conflicts, preserve the canonical document above; update this map and the relevant template rather than creating a parallel rule.

## Map the existing metadata taxonomy to templates

The existing `LLM-LAB-PAGE-MAP v1` metadata remains the canonical page inventory. Its `type` tag selects a default template:

| Existing `type` | Default archetype | Template / adaptation |
|---|---|---|
| `entry-point` | Orientation | Overview template, adapted for route selection |
| `system-overview` | Overview | [Overview](overview-page-template.md) |
| `concept-lesson` | Explanation | [Concept](concept-page-template.md) |
| `concept-bridge` | Explanation / bridge | Concept; emphasize prerequisite and destination links |
| `deep-dive` | Explanation / deep dive | Concept; formalism and derivation become central |
| `guided-build` | Procedural | [Guided build](guided-build-page-template.md) |
| `exercise-hub` | Practice | [Practice and experiment](practice-page-template.md) |
| `experiment-guide` | Practice / experiment | Practice; emphasize protocol and reproducibility |
| `glossary` | Reference | [Reference](reference-page-template.md); concise entries |
| `historical-reference` | Reference / history | Reference; provenance and historiographical caveats |
| `bibliography` | Reference | Reference; source roles and provenance |

This is a default, not a new required metadata field. A page may use a different archetype if its actual learning task justifies it.

## How to use the templates

1. Read the page's current `LLM-LAB-PAGE-MAP` scope, purpose, type, and learning-graph relations.
2. Select the default archetype from the table above.
3. Start from the matching template, but retain only sections that perform a real learning job.
4. Reuse the existing Quarto classes and site components; do not invent local styling for a recurring pattern.
5. Check the French/English counterpart and rendered output.
6. When a pattern recurs and needs changing, update its canonical rule/template first, then migrate pages incrementally.

## Shared patterns already present in the site

| Pattern | Existing implementation | Default use |
|---|---|---|
| Opening orientation | `.chapter-lead` in `site/styles.scss` | One concise scope and central idea |
| Supplementary outcomes | Quarto `.callout-note.learning-outcomes` | Two to four observable outcomes; collapsed when supplementary |
| Key intuition | Quarto `.callout-tip` | One non-redundant mental model |
| Optional context | Quarto `.callout-note` with `collapse="true"` | History, caveats, or side detail not needed for the main argument |
| Self-check | Collapsible Quarto callout with individual `<details>` answers | A few questions testing reasoning or transfer |
| Language navigation | `.language-switch` in `site/styles.scss` | Equivalent FR/EN navigation |

These patterns are already used unevenly across published pages. The objective is gradual convergence, not a mass rewrite or a new CSS component for every page.
