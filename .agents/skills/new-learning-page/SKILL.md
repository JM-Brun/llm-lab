---
name: new-learning-page
description: Design and create a new bilingual LLM Lab learning page only when a distinct, durable learner question cannot be served cleanly by existing pages; integrate metadata, concepts, sources, navigation and validation without creating a competing curriculum.
---

# New learning page

## Mission

Create a page that earns its place in the existing LLM Lab learning system. The goal is not to publish every interesting topic or source as a page; it is to give a distinct learner question a clear, durable owner at the right depth.

Use the normative [knowledge-change workflow](../../../docs/workflows/knowledge-change-workflow.md), the canonical [page-template guide](../../../docs/page-template-guide.md), and its [pre-draft learning-page blueprint](../../../docs/page-template-system.md#4-design-before-drafting-the-learning-page-blueprint). When invoked by `knowledge-change-workflow` or source integration, execute the page-necessity gate and page contract, then return the decision; do not route the same request back to the dispatcher. This skill owns the page-creation decision and page contract; it does not replace source extraction, concept-graph governance, technical review or rendered-site validation.

## When to use

Use when a new reader-facing page is explicitly proposed or when an existing page cannot own a distinct learner question without losing clarity, scope or maintainability.

Do not use merely because:
- a new source has been ingested;
- a new concept candidate has been extracted;
- a topic has many references;
- an existing page is long (first test section-level refactoring and existing owners);
- a new domain, route step or sidebar entry seems convenient.

For a source-backed proposal, use `source-to-learning-integration` for extraction and evidence, then `knowledge-and-learning-integration` for accepted content/graph decisions. For graph-only work, use `knowledge-architecture-audit`. For a refactor of several existing pages, use `page-group-audit` and `editorial-boundary-audit`.

## Gate 0 — establish the baseline

Inspect the current branch/commit and existing issues/PRs. Read:
- `AGENTS.md` and `CONTRIBUTING.md`;
- `docs/content-section-mapping.md`, `docs/learning-path.md`, `docs/page-metadata-schema.md`;
- `docs/page-template-guide.md` and the matching archetype/template;
- `docs/information-architecture.md` and `docs/knowledge-graph-standards.md` when graph implications exist;
- relevant page pairs, neighboring pages, indexes, sidebars, render lists, route registry and generated projections;
- existing issues, source reviews, source records, extraction dossiers and relevant graph concepts.

The current repository state is authoritative. Previous plans and audits are leads, not proof.

## Gate 1 — prove the page is needed

Write the learner contract:

> After this page, [audience] can [observable capability] in order to [meaningful task]. The current canonical owner [page/section] is insufficient because [specific gap], and extending it would [specific scope or coherence cost].

Compare at least:
1. extending an existing page;
2. adding a bounded subsection, example, figure or exercise;
3. linking to an existing resource;
4. creating a new page.

Create the page only if it has a distinct, reusable learner question and a stable scope. Record what is out of scope and which page owns adjacent details.

**No-page outcome is valid:** integrate a section/link/experiment or document why no change is justified.

## Gate 2 — define the page contract before writing

Record:

| Field | Required decision |
|---|---|
| Learner question | One precise question, not a broad subject label |
| Outcome | Observable verb: explain, distinguish, derive, calculate, implement, inspect, compare, evaluate or decide |
| Audience/prerequisites | Declared separately from reviewer inference |
| Scope | Concepts and mechanisms the page owns |
| Non-goals | Adjacent concepts explicitly owned elsewhere |
| Editorial role | Overview, core lesson, Build, Deepen, Practice/experiment, synthesis or reference |
| Destination | Existing Understand / Build / Deepen / Practice & experiment structure |
| Evidence | Sources, locators, assumptions, confidence and unresolved claims |
| Canonical concepts | Existing concept IDs or a justified proposal for stable new concepts |
| Neighbors | Prerequisite/previous/next, hierarchy and related links with distinct semantics |
| Language plan | FR and EN counterparts or an explicit, justified language exception |
| Validation | Relevant schema, graph, route, bilingual, render, link, accessibility and learner checks |

Do not use a page's editorial role, destination, primary Deepen domain, concept-domain memberships and guided-route stage as interchangeable metadata.

Before drafting, complete the applicable [learning-page blueprint](../../../docs/page-template-system.md#4-design-before-drafting-the-learning-page-blueprint). It must make the learner problem, value to LLM understanding, observable outcome, scope/ownership, prerequisites, curriculum position, explanatory sequence, mathematical contract, source synthesis, misconceptions and validation evidence explicit. Decide whether a worked thread genuinely helps; do not force a single running example onto subjects better taught by contrasting cases. For a revision, update only the affected blueprint decisions rather than creating a duplicate planning document.

## Gate 3 — choose the correct place and depth

Keep the existing four destinations distinct:
- **Understand:** core conceptual progression, ordered only by `data/guided-route.yml`.
- **Build:** implementation and construction milestones, using the existing Build route.
- **Deepen:** optional, independently useful extensions. Sibling deep dives do not imply order or prerequisites.
- **Practice & experiment:** transversal exercises, experiments and learner actions; not a second conceptual course.

A new Understand page requires an explicit curriculum decision: update `data/guided-route.yml`, its generated projections, tests and `docs/learning-path.md` consistently. Do not encode a new global sequence in page metadata, sidebars, hierarchy or a page-local chain.

Understand and Build are independent learning paths: the former orders conceptual understanding; the latter orders implementation by executable dependencies. A link from one to the other is a contextual reference, not an automatic prerequisite or a requirement to create paired pages. A lesson may inform several Build milestones, and a Build milestone may use several canonical Understand explanations.

A new Deepen page should have a bounded purpose, correct existing primary domain, `type:deep-dive` and `destination:deepen` metadata as specified by the schema, and no invented previous/next chain. Use `related` for genuinely useful cross-links. Confirm how the current Deepen index is generated before adding manual navigation.

## Gate 4 — build the page from canonical templates

1. Select the existing archetype and page template. Templates are soft guidance; include only sections that serve the learner contract.
2. Create stable page identity and metadata according to `docs/page-metadata-schema.md`. IDs are durable and language-aware as the schema requires; do not derive them from mutable titles.
3. Draft the explanation in original project language, following the approved blueprint. Define terms before use; state assumptions; distinguish mechanism, interpretation and analogy; bound analogies.
4. If a worked thread is used, keep inputs, conventions and intermediate results consistent and checkable; add contrasting examples when they teach a distinct property.
5. Use one canonical owner for each substantial explanation. Other pages may recap briefly and link.
6. Include examples, equations, figures, code or experiments only when they serve the declared outcome. Verify the actual asset and rights before reuse; never infer licence from attribution.
7. Add claim-level citations/links and preserve source locators in the relevant dossier. A bibliography alone does not establish provenance for individual claims.
8. Add a summary or revision aid only when it materially supports the outcome. Keep learner questions, exercises and learner-directed experiments on the dedicated companion Practice page, following the shared editorial contract and [issue #1512](https://github.com/JM-Brun/llm-lab/issues/1512).
9. Provide contextual links to adjacent pages that name the actual unresolved question, not a generic “read next” paragraph.

## Gate 5 — integrate metadata, graph and navigation

- Add the page to the correct Quarto render list and language-matched sidebar/index only after confirming the repository's current navigation model.
- Add a language switch to its true counterpart; never point to the language homepage as a substitute for a missing translation without stating the exception.
- Update page hierarchy only for genuine containment. Use `suggested_route` only for the page's local navigation semantics.
- Update `related` links only when the destination answers a specific adjacent question.
- Add concept-resource associations only for concepts the page actually teaches or meaningfully explains.
- Add stable concepts to `data/concepts.yml` only if they are reusable beyond this page and satisfy the concept schema. Use existing typed relations and domains; do not add a new relation/domain casually.
- Regenerate generated projections using canonical generators. Never hand-edit generated map data, route fragments, JSON-LD or generated includes.

## Gate 6 — bilingual editorial parity

Unless the page is explicitly and justifiably language-specific, create both French and English counterparts in the same change.

Parity means equivalent:
- learner question, outcomes and scope;
- definitions, claims, equations and assumptions;
- examples and their intended teaching function;
- caveats, counterexamples and uncertainty;
- exercises, references and navigation.

Natural phrasing, examples and narrative may differ by language. Preserve intentional language-specific storylines, cultural cues and editorial choices; do not force identical prose or examples. Ensure links and assets are language-matched.

## Gate 7 — validation and release readiness

Run relevant checks based on the touched files:
- page metadata and schema validators;
- concept/domain/resource registry validators and graph endpoint/relation checks;
- route membership, reciprocity and generated-projection freshness when relevant;
- Quarto render and rendered local-link validation;
- bilingual structural and semantic comparison;
- browser inspection at desktop and narrow widths for changed pages;
- keyboard/accessibility and interaction checks for affected components;
- learner task or formative review only when actually conducted.

Record exact commands, commit SHA, CI run and result. Distinguish source review, automated tests, render, browser/accessibility and learner evidence. A passing build is not proof of correctness, accessibility or comprehension.

## Required page-creation report

1. Learner contract and evidence that a new page was necessary.
2. Alternatives considered and why rejected.
3. Canonical owner and explicit non-goals.
4. Page IDs, paths, metadata, destination and language counterparts.
5. Sources and claim provenance.
6. Concept graph and page-navigation changes, or explicit no-change decisions.
7. Preservation/relocation map for any reused material.
8. Render, tests, browser/accessibility and learner-validation status.
9. Maintenance owner, known gaps and revisit triggers.

## Non-regression rules

- Do not delete useful content before its destination exists and is checked.
- Do not create a parallel route, duplicate concept definition or shadow registry.
- Do not turn related pages into a clique or a linear chain.
- Do not present Deepen as a prerequisite.
- Do not claim a language counterpart or validation that does not exist.
- Do not merge a PR without explicit authorization.
