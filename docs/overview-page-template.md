# Overview-page quick start

Use this pattern when the reader needs a **map of a topic or system**: what the main parts are, how they relate, and where a deeper explanation is useful. It is a prompt, not a required outline. The [flexible page-template system](page-template-system.md) defines the shared composition principles.

## Questions worth answering

Select only those that matter for this overview:

- What problem, system, or family of ideas is in scope?
- What is the smallest mental model that makes the whole intelligible?
- Which distinctions prevent likely category errors?
- How do the main components or stages relate? What flows between them?
- Which details belong to dedicated concept, algorithm, or implementation pages?
- What does this overview deliberately leave unresolved?

A diagram is useful when it exposes structure, flow, or relationships that are difficult to see in prose. It should not merely repeat the adjacent paragraphs.

## Possible composition

An overview often combines a concise opening, a system-level model, a few essential distinctions, and contextual links placed where the concepts appear. A compact self-check can help when there is a meaningful system-level inference to test. None of these needs to become a separate heading.

~~~markdown
<!-- State the system, central question, and scope concisely. -->

## A mental model

## How the main parts relate

## Important distinctions
~~~

Treat this as an illustration only. Delete it when the page reads better without these headings; add a section only when it performs a distinct job.

## Boundaries

- Explain enough to orient the reader; do not reproduce every child page.
- Do not remove a definition needed to understand the overview merely because a dedicated page exists.
- Distinguish a conceptual system map from a chronological history or an implementation pipeline.
- Do not call a partial sequence a complete lifecycle; state omitted stages when that affects interpretation.
- Put links on the concepts they clarify. Avoid generic “further study” or “pour continuer” lists that duplicate site navigation.
- Keep the main system-level claim and its necessary qualifications visible. Collapse only genuinely supplementary context or answer reasoning.

For implementation walkthroughs, experiments, and benchmarks, use the focused [implementation-page patterns](implementation-page-patterns.md).
