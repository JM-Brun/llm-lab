# Page-template guide

This guide helps contributors choose a useful explanatory approach without turning page design into a fixed schema. Templates are **soft targets**: prompts to consider, not sections to reproduce. A page is complete when it serves its reader's question—not when it matches an outline.

## Start with three different questions

Do not collapse these dimensions into one taxonomy:

1. **What is the reader trying to do?** Use the documentation-genre lens: learn through a tutorial, accomplish a task with a how-to, look up precise information in a reference, or understand a concept through an explanation. A page can mix these needs, but identify its dominant job.
2. **What is the page's stable editorial role in this repository?** Keep the existing LLM-LAB-PAGE-MAP and controlled type tags. They support the learning graph and site organization; do not add a parallel archetype or diataxis metadata field.
3. **What kind of subject is being explained?** Choose a scientific pattern—concept, algorithm, mathematical object, physical law, architecture, technology, method, or overview—according to the explanatory problem. These patterns are not metadata categories and are not mutually exclusive.

The [page archetype implementation map](site-page-design-system.md) connects existing metadata types to their usual page roles. The [flexible page-template system](page-template-system.md) is the canonical guide to composing a page; [page patterns](page-patterns.md) and [implementation-page patterns](implementation-page-patterns.md) provide subject-specific prompts.

## Choose only what helps

1. State the concrete question the page should answer.
2. Identify the dominant reader task and existing metadata type.
3. Choose one primary scientific or implementation pattern; borrow from another only when it resolves a real explanatory need.
4. Select the few modules that make the explanation accurate and understandable.
5. Decide which details belong in the main flow and which are genuinely optional.
6. Check the rendered page and its language counterpart.

Do not create a section because a template names it. A definition may fit in the opening; a caveat may belong beside the claim it qualifies; an implementation link may need only one sentence. Combine, rename, reorder, or omit freely.

## Existing quick starts

These files offer focused prompts for recurring page jobs. They complement the canonical composition guide; they are not separate standards or competing outlines.

- [Overview](overview-page-template.md): orient the reader and explain relationships across a system or topic.
- [Concept](concept-page-template.md): explain one object, quantity, or mechanism precisely.
- [Reference](reference-page-template.md): support lookup, comparison, chronology, or source consultation.
- [Guided build](guided-build-page-template.md): help the reader construct and verify a working artifact.
- [Practice and experiment](practice-page-template.md): support sustained problem-solving or a reproducible investigation.
- [Scientific page patterns](page-patterns.md): adapt the explanation to the subject.
- [Implementation page patterns](implementation-page-patterns.md): choose a code-facing workflow such as walkthrough, verification, benchmark, integration, or debugging.

## Shared reader-experience principles

- Keep the question, essential explanation, definitions, and caveats that change the conclusion visible.
- Use progressive disclosure for genuinely supplementary derivations, extended examples, historical context, and answer keys—not to hide prerequisites or essential reasoning.
- Keep short in-page comprehension checks distinct from full exercise collections and experiments. When a check is included, use the shared presentation convention and keep solutions collapsed by default.
- Use diagrams, code, and interactive elements only when they answer a concrete reader question better than prose alone.
- Reuse the [visual design system](design-system.md); a new content pattern does not justify a new visual component by itself.
- Preserve substantive French/English parity, while allowing natural differences in wording and sectioning.

## Review aid—not a gate

Ask only the questions that apply:

- Can a reader tell what question this page answers and what it does not cover?
- Is the main idea understandable before optional depth?
- Are formal claims, intuition, implementation choices, and empirical evidence distinguishable?
- Are notation, units, dimensions, assumptions, and conditions defined where needed?
- Does each example, figure, or exercise contribute something specific?
- Are links placed where the relevant concept appears, rather than collected into a redundant navigation section?
- Are source claims, reuse rights, and implementation status represented honestly?
- Has the rendered experience and the other language version been checked?

A justified deviation is not a defect. If a prompt does not fit the page, mark it not applicable or omit it; do not add content to satisfy the guide.
