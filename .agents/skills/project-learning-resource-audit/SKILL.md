---
name: project-learning-resource-audit
description: Audit a coherent external LLM learning project (book, course, educational site, tutorial series, repository ecosystem or interactive environment) as a learning system; compare its pedagogy, concepts, visuals, practice and implementation with LLM Lab while reusing existing source records and reviews.
---

# Project-level learning resource audit

## Mission and boundary

Use this skill when the user asks to audit, compare, onboard or extract value from an **entire learning project or coherent resource family**, rather than one article or one concept collection.

The project is the unit of instructional analysis; constituent articles, papers, lessons, code, figures and exercises remain separate source components with their own provenance. This skill coordinates their evidence but does not replace source-extraction, source-to-learning-integration, knowledge-and-learning-integration, or canonical schemas.

Normative procedure: [Project-level learning resource audit workflow](../../../docs/workflows/project-learning-resource-audit.md). Use its [project audit template](../../../docs/workflows/templates/project-learning-resource-audit-template.md).

## 1. Reconcile existing work first

Before scanning or creating anything:
1. Inspect coordinator issue #756 and identify the single project owner issue.
2. Search issues, PRs, data/sources.yml, data/extractions/, docs/source-reviews/ and existing comparisons for prior evidence.
3. Reuse narrower work (for example #86, #95, #114, #147, #458, #472, #742 and project-specific owners) without claiming it covers the whole project.
4. Preserve the distinction between a focused topic contribution and a broader project audit.
5. If no owner exists, create one project-specific issue linked to #756; otherwise update the existing owner. Never create a duplicate issue for the same project family.

Do not create a parallel project catalogue or manually maintained ownership registry. The owner issue and canonical source records are sufficient.

## 2. Select a proportionate audit depth

Choose and state one:
- **Architecture scan:** project promise, audience, curriculum map, major routes, practice and implementation boundaries; no claim of detailed lesson coverage.
- **Representative audit:** architecture scan plus selected lessons/modules/activities chosen to test the project's distinctive teaching approach.
- **Deep audit:** broad inspection of relevant components, including representative text, mathematics, visuals, practice, code and references.

A project audit is not complete merely because the home page, README or course index was inspected. Use a coverage table and name the selection bias. Do not silently expand scope until the work becomes unmaintainable.

## 3. Build the project-local model

Reconstruct only what inspected evidence supports:
- **Instructional architecture:** audience, prerequisites, outcomes, entry points, progression, required/optional routes, scaffolding and stopping points.
- **Conceptual/computational model:** concepts, representations, operations, data flow, equations, assumptions, simplifications and omissions.
- **Explanatory model:** learner questions, mental models, analogies, examples, counterexamples and misconceptions.
- **Visual/interactive model:** figures, animation, manipulation, observable state, hidden state, fidelity and accessibility.
- **Practice/implementation model:** exercises, feedback, notebooks, code, tests, datasets, reproducibility and implementation boundary.

Separate author-declared statements from reviewer inferences. A module order is not automatically a prerequisite graph. Do not claim that the external project provides a formal ontology, computational graph or curriculum map unless it does.

## 4. Compare with LLM Lab at equivalent levels

Inspect actual LLM Lab artifacts: canonical bilingual pages and page ownership; concept registry and typed relations; computational/data-flow architecture; conceptual route and optional depth; Build route, code and tests; Practice & experiment exercises; navigation, visuals, citations and existing source reviews.

Use a learner-question crosswalk rather than a keyword checklist. For each relevant external module, map:
1. learner question/capability;
2. external explanatory lens and learner action;
3. LLM Lab page/concept/route/activity;
4. differences in abstraction, assumptions, scope and evidence;
5. what LLM Lab already handles better;
6. genuine gap or complementarity and likely maintenance cost.

Keep source-local model, topic-level synthesis, project model and canonical LLM Lab graph/route distinct.

## 5. Required complementarity analysis

Do not reject a contribution because its topic already exists. Compare cognitive difficulty and learner question; mental model/explanatory lens; example phenomenon; abstraction level and prerequisite burden; teaching move and active learner behavior; caveats, assumptions and failure boundaries.

Likewise, do not integrate a contribution merely because it is novel. It must improve precision, intuition, transfer, accessibility, practice or implementation enough to justify complexity. Test at least one plausible contribution before declaring a pedagogical no-op.

Use canonical item_dispositions for extraction items. Do not create a separate project-level disposition enum, score, ranking or rubric vocabulary.

## 6. Cross-project comparison

When two or more project audits have comparable evidence:
- compare common learner questions and dimensions, not popularity or total topic counts;
- distinguish shared teaching patterns from independent technical corroboration;
- preserve contradictions and audience/scope differences;
- identify which project contributes which complementary perspective;
- compare with LLM Lab's existing treatment;
- propose one bounded synthesis experiment or justify none.

Reuse the existing multi-source comparison template as the matrix scaffold. Reuse and extend the dated [Raschka/Hugging Face/LLM Lab learning-path comparison](../../../docs/source-reviews/learning-path-comparison-2026-11-05.md). Do not create pairwise reports or a new portfolio registry. A single portfolio synthesis is justified only after evidence from multiple project owners exists.

## 7. Integration and validation

For accepted contributions, coordinate with source-to-learning-integration and knowledge-and-learning-integration. Prefer bounded improvements to existing pages/exercises; new pages, canonical concepts, graph relations, interactive tools and automation require a distinct learner outcome and evidence.

Keep Understand / Build / Deepen / Practice & experiment boundaries. Preserve existing content and visual assets; record unresolved rights rather than removing existing embeds. Maintain semantic FR/EN parity.

Report independently project inspection coverage; source extraction and technical evidence; project-model reconstruction; LLM Lab differential decisions; graph/page/route/Build changes; automated checks and rendered/accessibility review; learner evidence, only if actually collected.

Record actual CI against the final PR head. Do not treat a passing build, source count, issue update or completed audit checklist as evidence of learner mastery.

## Output

Produce the project audit dossier from the canonical template, link it from the existing project owner issue, and report audit depth and inspection boundary; existing work reused; project-local model and strengths/limitations; LLM Lab crosswalk and complementarity findings; item-level decisions and bounded integration; validation, unresolved gaps and revisit trigger.

Do not produce a cross-project ranking or portfolio synthesis before multiple comparable audits exist.
