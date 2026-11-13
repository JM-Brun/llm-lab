# Flexible page-template system

**Status:** editorial guidance for new and revised pages.  
**Purpose:** provide reusable starting points, improve coherence between pages, and make later refactoring inexpensive—without turning a template into a publication checklist.

This is the canonical entry point for page composition. It connects the [reader-experience method](reader-experience-and-editorial-method.md), [visual design system](design-system.md), [page metadata contract](page-metadata-schema.md), [content-section map](content-section-mapping.md), and [contributor principles](contributor-guiding-principles.md). It complements these documents; it does not create a parallel editorial or visual system. The cross-cutting rollout, shared page anatomy, navigation boundaries, and rendered-validation sequence are consolidated in the [page harmonization plan](page-harmonization-plan.md).

## 1. The target is convergence, not uniformity

A template is a **soft target**: a starting hypothesis about the clearest way to teach a subject. It is not a required sequence, completeness score, or reason to add empty headings.

Pages should converge on a shared reader experience: readers can identify the question and main idea; intuition is distinguishable from precise claims; notation, examples, figures, and caveats appear when useful; optional depth does not obstruct the central explanation; links expose meaningful relationships; and recurring visual patterns behave consistently.

Convergence does **not** mean identical sections, length, callouts, or visual density. Pages should look related because they share design and editorial principles—not because they repeat an outline.

Before adding a section, ask: **what reader question does it answer, and what would be lost if it were omitted?** If there is no specific answer, omit it, merge it with another section, or move it to a more suitable page.

## 2. Compose from three layers

### A. Shared orientation

Most explanatory pages benefit from a little orientation. These are prompts, not mandatory headings:

- **Identity:** a precise title and a concise opening that places the subject in context.
- **Question / purpose:** the problem, phenomenon, or design choice being explained.
- **Core mental model:** the central idea in a few sentences or a useful figure.
- **Scope:** only where a boundary prevents a likely misunderstanding.
- **Learning outcomes:** only when they help; use the existing `.callout-note.learning-outcomes` component and keep outcomes specific.

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
| Exercises | Can I recall, calculate, interpret, or transfer? | Dedicated per-lesson practice page linked from the lesson; answers collapsed |
| Connections | Which neighbouring concepts clarify or use it? | Contextual links in relevant paragraphs |
| References | Which sources support the claims? | Primary / official and pedagogical sources |

A module is not automatically a heading. A definition may fit in the opening; a limitation may belong beside the claim it qualifies; an implementation link may be one sentence inside the mechanism section.

### C. Optional depth

Use progressive disclosure for genuinely secondary material: extended derivations, long examples, implementation details, historical notes, alternative formulations, answer keys, or research debates.

Do **not** collapse information needed to interpret the main claim. Assumptions, units, scope restrictions, and caveats that change the conclusion must remain visible. Do not make readers open several nested disclosures to find the basic mechanism.

## 3. Choose a pattern by the dominant learner question

Page families are starting points, not exclusive categories. A page may combine patterns; choose the one that best describes its **main teaching job**. See the [page-pattern guide](page-patterns.md) for prompts and [implementation-page patterns](implementation-page-patterns.md) for code-facing material.

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

Do not create a new pattern for every topic. Split or add a family only when its learner question or explanatory structure is materially different.

### Stable exercise references

A collection page has its own bilingual page identity in the `LLM-LAB-PAGE-MAP` block. An exercise embedded in that collection is identified by a **named heading anchor**, not by a numbered position or a short opaque code.

Use this pattern for each exercise heading:

```markdown
### Calculate an embedding lookup {#ex-text-data-embedding-lookup}
```

- Use `ex-<collection>-<concept-or-skill>-<action>`: lowercase kebab-case, descriptive, and independent of the display title.
- Reuse the exact same anchor in the French and English counterpart. The identifier is language-neutral; translate only the heading text.
- Do not encode order (`1`, `A`, `B`), language (`fr`, `en`), or a temporary section name in the identifier. Reordering, inserting, or removing another exercise must not rename existing anchors.
- A link to an in-page exercise combines the collection page URL with the anchor. If an exercise moves to another page, preserve the old fragment as an alias where practical and update the canonical link.
- If an exercise becomes a standalone page, give that page its normal stable page ID through `LLM-LAB-PAGE-MAP`; do not create a parallel exercise registry for headings embedded in pages.

Existing public fragments should be retained as aliases when replacing opaque or automatically generated heading IDs. The page metadata remains the authority for page identity; heading anchors identify only the exercise within that page.

## 4. A practical starting sequence

1. Write one sentence stating the question the page answers.
2. State what the reader should understand after the core explanation.
3. Choose the dominant pattern.
4. Select only the modules needed to meet that outcome.
5. Decide what belongs in the main flow and what can be optional depth.
6. Identify useful diagrams, examples, or comparisons—if any.
7. Connect the page to canonical neighbours using the metadata relation semantics.
8. Add references that support the actual claims.
9. Review the rendered page and its language counterpart.

If a page becomes too long, check for duplicated explanations, unclear scope, or material that belongs on an existing canonical page. Do not split it merely to meet a target length.

## 5. Reuse the shared visual language

The [visual design system](design-system.md) is the authority for colours, typography, spacing, accessibility, responsive behaviour, and interaction. Templates should reuse its patterns rather than define page-specific styling.

- Reuse existing Quarto callout classes and shared styles.
- Use a callout only when its semantic role is clear.
- Use accessible `details` disclosures for optional depth and answer keys.
- Use figures when they explain structure, geometry, data flow, comparison, or change; provide captions and meaningful alt text.
- Keep status labels (implemented, tested, illustrative, planned) consistent.
- Prefer a shared component or SCSS rule when a presentation pattern genuinely recurs.

A new page pattern does not justify a new visual component by itself. Establish the semantic role and reusability first.

## 6. Preserve the existing knowledge architecture

Templates guide content; they do not replace page metadata or the learning graph.

- Keep `LLM-LAB-PAGE-MAP` and controlled `keywords` aligned with [page-metadata-schema.md](page-metadata-schema.md).
- Distinguish conceptual parent/child relations from suggested reading order and merely related concepts.
- Link to canonical explanations rather than duplicating substantial material.
- Keep each public page self-contained for its LLM-specific learning objective; a link is not a substitute for a necessary definition or derivation.
- Add implementation, tests, exercises, or experiments only when they exist; label planned work honestly.
- Keep editorial tags machine-readable and out of the visible reading flow; see the [page metadata visibility contract](page-metadata-schema.md#21-reader-facing-visibility-contract).
- Highlight only a small number of important scientific terms in context, preferably linking their first useful occurrence to a canonical explanation. Do not add keyword clouds or a repeated list of page tags.
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


## 9. Synthesis sheets: a fast, trustworthy entry point

A **synthesis sheet** is a deliberately edited orientation layer for a substantial subject. It helps a reader answer “what is this, how does it fit, and what should I remember?” quickly, then routes them to canonical explanations, evidence, code, tests, and practice. It is not a compressed copy of a lesson, a decorative infographic, or a replacement for the underlying material.

This is a use of the existing **Overview / synthesis** pattern, not a new page archetype or learning stage. Apply the same metadata contract, page ownership, bilingual identity, design system, and content-section boundaries as any other page. The sheet may be a dedicated page when it has a distinct reader task; otherwise, a clearly bounded synthesis section in an existing canonical overview may be better.

### 9.1 Decide whether a separate sheet earns its place

Create or maintain a distinct sheet only when it adds a useful reader outcome that is not already served well by the canonical page opening or overview. Good reasons include:

- several concepts must be connected or contrasted to prevent a common misunderstanding;
- a system, algorithm, or data flow benefits from one coherent visual overview;
- readers need a compact decision aid or reference they can revisit;
- the subject is substantial enough to merit an independent entry point and meaningful links to deeper material.

Do **not** create a separate sheet when it would merely repeat a concise existing explanation, when the subject is too narrow to benefit from a separate entry point, or when the visual would add decoration rather than explanatory value. Record the decision through the existing page map / review workflow; do not introduce a second sheet registry.

### 9.2 Flexible editorial anatomy

Select only the elements that serve the sheet's central question. The order is a useful default, not a required checklist.

| Element | Reader need | Editorial guidance |
|---|---|---|
| Question and short answer | “What am I looking at?” | State the central question and answer it precisely in a few sentences. |
| Mental model | “How should I picture it?” | Offer one useful intuition and state where the analogy or simplification stops. |
| Primary visual | “How do the parts or ideas relate?” | Prefer one original, legible diagram, trace, timeline, or comparison that carries real explanatory work. |
| Mechanism / example | “Can I follow it?” | Show a small sequence, worked example, or concrete case that can be checked. |
| Key distinctions | “What should I not confuse?” | Compare only along explicit, relevant dimensions; avoid false binaries. |
| Practical significance | “When does this matter?” | Explain use, design consequences, costs, or trade-offs in context. |
| Limits and misconceptions | “What does this not establish?” | Keep consequential assumptions, failure modes, uncertainty, and omitted details visible. |
| Takeaways | “What should remain?” | End with a small number of precise, non-redundant conclusions. |
| Go deeper | “Where can I verify or learn more?” | Link to canonical concept pages, derivations, implementation, tests, experiments, and exercises that actually exist. |
| Evidence | “Why should I trust this?” | Cite primary / official sources for factual claims; identify pedagogical sources as such. |

Topic-specific sheets may take another form: architecture map, algorithm trace, mathematical reference, historical synthesis, or decision matrix. Do not force every subject into the same infographic layout.

### 9.3 Visual and evidence rules

- A visual must make a structure, relationship, transformation, comparison, or quantitative pattern easier to understand than prose alone. If it does not, omit it.
- Prefer original diagrams built from the project's own explanation. Record third-party asset provenance and licence in the existing [visual asset register](visual-assets-register.md); never assume that public availability grants reuse rights.
- Every meaningful diagram needs a descriptive caption and useful alternative text. Its meaning must remain available without colour, hover, animation, or JavaScript.
- Label boundaries, direction, units, tensor shapes, assumptions, and legend entries where they affect interpretation. Avoid visual precision that the evidence does not support.
- Distinguish established facts, simplified mental models, measured empirical findings, active disagreements, and open questions. A polished diagram does not turn an assumption into a fact.
- Comparisons must name their dimensions and context. Benchmark numbers need their workload, model / hardware / software conditions, metric, provenance, and date or version when relevant.
- Use primary papers, official documentation, and reproducible project evidence for technical claims. Use secondary teaching resources to inspire explanation, not as sole support for contested or quantitative claims.
- Do not reproduce third-party diagrams or copy their prose. References such as ByteByteGo, Distill, Jay Alammar, and Hugging Face are useful for studying pedagogical techniques; their assets and wording are not project assets.

### 9.4 Bilingual and navigational contract

- French and English counterparts must preserve the same substantive claims, caveats, examples, evidence quality, and useful links. Wording and layout may differ naturally by language.
- Use the existing stable page IDs and LLM-LAB-PAGE-MAP semantics. Keep language-neutral anchors stable across counterparts where the page system requires them.
- Link to canonical pages at the point where a reader is likely to want more detail. Do not create generic link dumps or imply that optional deep dives are prerequisites.
- Identify the intended audience / level and prerequisites only when they materially help a reader choose the sheet. Do not render internal metadata keys as reader-facing badges.
- State the last substantive review date where freshness matters; do not imply that a date alone guarantees currency.

### 9.5 Lightweight quality review

Before publishing or revising a sheet, ask:

- [ ] Does it answer one identifiable reader question that is not already answered as well elsewhere?
- [ ] Can a reader state the central idea after a quick scan without mistaking the simplification for the full theory?
- [ ] Does the visual explain something specific, and can it be understood accessibly without colour or interaction?
- [ ] Is there at least one concrete example, trace, or comparison when the subject needs one?
- [ ] Are consequential assumptions, limitations, disagreements, and uncertainty visible?
- [ ] Are factual and quantitative claims traceable to suitable sources?
- [ ] Do links lead to canonical deeper resources that exist, rather than duplicated material or planned work presented as available?
- [ ] Is the French / English counterpart substantively equivalent?
- [ ] Has the rendered result been checked at narrow and wide widths, with keyboard navigation and meaningful alternative text?
- [ ] Does the sheet complement the learning path rather than create a new mandatory stage?

A review is evidence of editorial care, not proof of improved learning outcomes. Claims about learner impact require learner-facing evaluation.
