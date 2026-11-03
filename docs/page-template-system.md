# Flexible page-template system

**Status:** editorial guidance for new and revised pages.  
**Purpose:** provide reusable starting points, improve coherence between pages, and make later refactoring inexpensive—without turning a template into a publication checklist.

This is the canonical entry point for page composition. It connects the [reader-experience method](reader-experience-and-editorial-method.md), [visual design system](design-system.md), [page metadata contract](page-metadata-schema.md), [content-section map](content-section-mapping.md), and [contributor principles](contributor-guiding-principles.md). It complements these documents; it does not create a parallel editorial or visual system.

## 1. The target is convergence, not uniformity

A template is a **soft target**: a starting hypothesis about the clearest way to teach a subject. It is not a required sequence, completeness score, or reason to add empty headings.

Pages should converge on a shared reader experience: readers can identify the question and main idea; intuition is distinguishable from precise claims; notation, examples, figures, and caveats appear when useful; optional depth does not obstruct the central explanation; links expose meaningful relationships; and recurring visual patterns behave consistently.

Convergence does **not** mean identical sections, length, callouts, or visual density. Pages should look related because they share design and editorial principles—not because they repeat an outline.

Before adding a section, ask: **what reader question does it answer, and what would be lost if it were omitted?** If there is no specific answer, omit it, merge it with another section, or move it to a more suitable page.

### Choose the documentation job before the subject pattern

A page's **documentation job** and its **scientific subject pattern** are different dimensions.

Use the reader's need to identify the broad form:

- **Tutorial:** guide a learner through a learning experience or build.
- **How-to:** help someone complete a specific task.
- **Reference:** make precise facts, conventions, parameters, or comparisons easy to consult.
- **Explanation:** build understanding of a concept, mechanism, context, or design choice.

These are the four Diátaxis documentation genres. They are a useful editorial taxonomy, not an empirical learning standard and not a mandatory metadata field. A page may deliberately combine genres, but should have one dominant job.

Then choose the scientific pattern that best fits the subject: algorithm, mathematical object, physical concept, architecture, technology, research approach, overview, and so on. For example, an attention page may be an explanation whose subject pattern is an algorithmic mechanism; a GPT build page may be a tutorial whose subject pattern is an architecture plus implementation technique.

Keep the repository's existing metadata contract authoritative: the controlled type tag describes the site's stable editorial role. Do not introduce a second archetype or Diátaxis metadata field unless a concrete tooling need is demonstrated. The documentation genre is an authoring decision that can be recorded in prose or review notes when useful.

The existing overview, concept, guided-build, practice, and reference templates remain focused supplements for their respective page jobs. They should reuse this composition model rather than define a competing universal outline.

## 2. Compose from three layers

### A. Shared orientation

Most explanatory pages benefit from a little orientation. These are prompts, not mandatory headings:

- **Identity:** a precise title and a concise opening that places the subject in context.
- **Question / purpose:** the problem, phenomenon, or design choice being explained.
- **Core mental model:** the central idea in a few sentences or a useful figure.
- **Scope:** only where a boundary prevents a likely misunderstanding.
- **Learning outcomes:** only when they help; use the existing learning-outcomes callout and keep outcomes specific.

Combine these elements in the opening when that reads better. Do not create a separate section for each by default.

### B. Explanatory modules

Select, combine, and reorder only the modules that serve the subject.

| Module | Reader question | Typical treatment |
|---|---|---|
| Motivation | Why was this idea needed? | Opening or first section |
| Intuition | What mental model predicts its behaviour? | Prose, analogy with limits, or figure |
| Definition | What exactly is the object or term? | Precise prose and canonical terminology |
| Mechanism | What happens, and in what order? | Steps, data flow, pseudocode, diagram |
| Mathematics | What is the formal statement or derivation? | Essential equations inline; longer derivation optional |
| Worked example | Can I trace a concrete case? | Small, checkable numerical or symbolic example |
| Physical interpretation | What does it mean physically? | Units, dimensions, assumptions, limiting cases |
| Implementation | How is it represented or computed? | Maintained code, shapes, conventions |
| Properties | What follows under which assumptions? | Guarantees, invariants, complexity, empirical behaviour |
| Comparison / variants | What changes between alternatives? | Explicit comparison dimensions |
| Limitations | Where does the explanation stop applying? | Material caveats kept visible |
| Misconceptions | Which plausible interpretation is wrong? | Counterexample or boundary case |
| History / provenance | Who introduced it, and what supports the account? | Optional, sourced historical context |
| Exercises | Can I recall, calculate, interpret, or transfer? | Existing self-check pattern; answers collapsed |
| Connections | Which neighbouring concepts clarify or use it? | Contextual links in relevant paragraphs |
| References | Which sources support the claims? | Primary / official and pedagogical sources |

A module is not automatically a heading. A definition may fit in the opening; a limitation may belong beside the claim it qualifies; an implementation link may be one sentence inside the mechanism section.

### C. Optional depth

Use progressive disclosure for genuinely secondary material: extended derivations, long examples, implementation details, historical notes, alternative formulations, answer keys, or research debates.

Do **not** collapse information needed to interpret the main claim. Assumptions, units, scope restrictions, and caveats that change the conclusion must remain visible. Do not make readers open several nested disclosures to find the basic mechanism.

## 3. Choose a pattern by the dominant learner question

The patterns in the [page-pattern guide](page-patterns.md) are **subject-specific explanatory patterns**, not documentation genres and not metadata types. A page may combine patterns; choose the one that best describes its **main teaching job**. Do not create a new pattern for every topic.

| Pattern | Dominant question | Usually emphasise |
|---|---|---|
| Concept / quantity | What does this mean, and how should I interpret it? | Intuition, definition, notation, example, assumptions |
| Algorithm / method | What problem does it solve, and how does it produce an answer? | Objective, mechanism, worked trace, properties, complexity, failure modes |
| Mathematical concept | What is the formal object, and what follows from its definition? | Definitions, notation, derivation, geometric or algebraic intuition |
| Physical concept / law | What phenomenon is described, and under which conditions? | Physical interpretation, units, governing relation, assumptions, validity |
| Architecture / system | What are the components, and how does information or control flow? | System diagram, component roles, data flow, interfaces, trade-offs |
| Technology / technique | What changes in the system, and what trade-off follows? | Mechanism, constraints, quality/performance/cost, use cases, limits |
| Research approach | What question does this approach ask, and how does it differ? | Problem framing, assumptions, workflow, evidence, limitations |
| Overview / synthesis | How do several ideas fit together? | Organising principles, relationships, boundaries, routes to canonical pages |

Split or add a family only when its learner question or explanatory structure is materially different.

## 4. A practical starting sequence

1. Identify the reader's documentation need (tutorial, how-to, reference, explanation, or a deliberate hybrid).
2. Write one sentence stating the question the page answers.
3. State what the reader should understand after the core explanation.
4. Choose the dominant scientific pattern.
5. Select only the modules needed to meet that outcome.
6. Decide what belongs in the main flow and what can be optional depth.
7. Identify useful diagrams, examples, or comparisons—if any.
8. Connect the page to canonical neighbours using the metadata relation semantics.
9. Add references that support the actual claims.
10. Review the rendered page and its language counterpart.

If a page becomes too long, check for duplicated explanations, unclear scope, or material that belongs on an existing canonical page. Do not split it merely to meet a target length.

## 5. Reuse the shared visual language

The [visual design system](design-system.md) is the authority for colours, typography, spacing, accessibility, responsive behaviour, and interaction. Templates should reuse its patterns rather than define page-specific styling.

- Reuse existing Quarto callout classes and shared styles.
- Use a callout only when its semantic role is clear.
- Use accessible details disclosures for optional depth and answer keys.
- Use figures when they explain structure, geometry, data flow, comparison, or change; provide captions and meaningful alt text.
- Keep status labels (implemented, tested, illustrative, planned) consistent.
- Prefer a shared component or SCSS rule when a presentation pattern genuinely recurs.

A new page pattern does not justify a new visual component by itself. Establish the semantic role and reusability first.

## 6. Preserve the existing knowledge architecture

Templates guide content; they do not replace page metadata or the learning graph.

- Keep the LLM-LAB-PAGE-MAP marker and controlled keywords aligned with the [page-metadata-schema](page-metadata-schema.md).
- Distinguish conceptual parent/child relations from suggested reading order and merely related concepts.
- Link to canonical explanations rather than duplicating substantial material.
- Keep each public page self-contained for its LLM-specific learning objective; a link is not a substitute for a necessary definition or derivation.
- Add implementation, tests, exercises, or experiments only when they exist; label planned work honestly.
- Maintain substantive French/English parity.

The [content-section map](content-section-mapping.md) remains the inventory of page roles and content boundaries. If a template conflicts with a canonical page's scope, the content map and reader-experience method take precedence.

## 7. Refactoring and maintenance

- Keep semantic patterns stable and styling centralised.
- Avoid copying large boilerplate blocks into every page.
- Abstract recurring presentation, not one-off content.
- When a shared pattern changes, update its guidance and representative pages together.
- Revise templates when rendered reviews expose friction.
- Do not mass-convert pages solely to make headings identical. Refactor when it improves comprehension, consistency, accessibility, or maintainability.

Start selectively: compare representative pages against the soft target, record justified deviations, and only then decide whether broader refactoring is worthwhile.

## 8. Review aid—not a gate

- [ ] The page answers a specific learner question and has a clear scope.
- [ ] The opening gives a useful mental model without burying the reader in detail.
- [ ] Intuition is distinguishable from formal or empirical claims.
- [ ] Terms, symbols, units, dimensions, and assumptions are defined before use.
- [ ] Examples or figures clarify something that prose alone would make harder to see.
- [ ] Optional depth is discoverable; essential caveats remain visible.
- [ ] Likely misconceptions are challenged when relevant.
- [ ] Links express real conceptual or learning-graph relationships.
- [ ] References support the claims.
- [ ] Existing design patterns are reused; accessibility and responsive rendering are checked.
- [ ] The counterpart language is substantively equivalent.

Mark items not applicable when the page does not need them. The purpose is to notice missing support for the page's learning objective, not to maximise checked boxes.
