# Knowledge-change workflow

**Status:** normative workflow · **Version:** 1.0 · **Scope:** adding knowledge, integrating sources, creating or restructuring learning pages, and updating the canonical knowledge graph.

**Related canonical workflows:** [Source-to-learning system integration](source-to-learning-system-integration.md), [Source-to-knowledge validation](source-to-knowledge-validation.md), [Project-level learning resource audit](project-learning-resource-audit.md), [Page metadata schema](../page-metadata-schema.md), [Information architecture](../information-architecture.md).

## 1. Purpose

This workflow makes every knowledge change an explicit, traceable change to the existing LLM Lab learning system. It is an entry point and decision protocol, not a replacement for the specialist workflows, registries, schemas, templates or validators.

The desired outcome is not a larger corpus. It is a more coherent bilingual knowledge system in which:
- each durable concept has a clear definition, owner and meaningful typed relations;
- each page answers a distinct learner question at an appropriate depth;
- each source's contribution can be traced to the claims or teaching choices it informs;
- connections across domains are discoverable without being mistaken for prerequisites;
- new material improves existing explanations where possible, rather than multiplying near-duplicate pages;
- every change preserves useful prior knowledge and can be validated independently.

## 2. Choose the change mode

Start by identifying what is being added. A single request may combine modes, but each mode keeps its own evidence and completion state.

| Change mode | Typical input | Primary workflow / skill | Output |
|---|---|---|---|
| External source intake | Article, paper, book, course, repository, video, dataset | `source-to-learning-integration` (coordinates `source-extraction` then `knowledge-and-learning-integration`) | Source record, extraction, item decisions, justified project changes or explicit no-op |
| New project knowledge | A derived insight, corrected explanation, new relation, cross-domain synthesis | `knowledge-change-workflow` + `knowledge-and-learning-integration` | Evidence-backed page/graph/resource delta and provenance |
| New learning page | A durable learner question not served adequately by current pages | `new-learning-page` + `knowledge-and-learning-integration` when graph/source integration is involved | Page contract, bilingual page(s), metadata/navigation, links and tests |
| Existing page improvement | Missing explanation, better example, correction, scope/ownership issue | `page-content-audit` or `editorial-boundary-audit`, then integration | Bounded content change and preservation record |
| Cross-page or graph evolution | New concept, relation, domain impact, metadata/projection change | `knowledge-architecture-audit` | Canonical registry/metadata changes and regenerated projections |
| External learning project | Coherent course/site/book/repository ecosystem | `project-learning-resource-audit` first | Project model, source map, comparative integration decisions |

Do not invoke every skill. Use the smallest combination that covers distinct decisions. The [skill routing matrix](../../.agents/skills/audit-skill-routing/SKILL.md) is the operational index.

## 3. Gate 0 — establish the current baseline

Before editing:

1. Identify the repository, current base/head branch and commit. Work on a focused branch.
2. Search open and recently closed issues/PRs, existing source reviews, extractions, pages and graph records. Reuse the existing owner; do not create duplicate tracking work.
3. Read `AGENTS.md`, `CONTRIBUTING.md`, and the canonical documentation relevant to the change.
4. Locate the authoritative source, schema, generator, consumer and validator for every field or artifact to be changed.
5. Record what is observed, what is inferred and what remains unknown. Old audit reports and prior agent summaries are discovery aids, not current-state evidence.

**Pass condition:** the change has one clear owner and does not create a competing registry, graph, taxonomy, template contract or learning route.

## 4. Gate 1 — state the learner problem before choosing an artifact

Write one concise statement:

> A learner/researcher needs to [observable capability or resolve a precise question] because [specific difficulty or gap]; current LLM Lab coverage at [exact page/section/concept] does not yet do this adequately because [evidence].

Then test the smallest candidate intervention, in this order:

1. correct or clarify an existing claim;
2. improve an existing section, worked example, diagram, exercise or experiment;
3. add a complementary perspective or bounded subsection;
4. add a contextual link or optional reference;
5. create a new page only when the learner question is distinct, durable and cannot be served cleanly by an existing owner.

A different source, label, analogy or topic tag is not by itself a new learner question. A graph concept is not automatically a page. A new page is not automatically a new route step.

**Pass condition:** the proposed artifact is justified by a concrete learner benefit and its maintenance cost is understood.

## 5. Gate 2 — resolve ownership and model boundaries

Use the existing canonical ownership model. Do not infer ownership from filenames or headings.

| Information | Canonical owner / rule |
|---|---|
| Source identity and bibliographic metadata | `data/sources.yml` and its documented source model |
| Atomic source evidence and item dispositions | `data/extractions/<source-id>.yml`, controlled by `data/source-taxonomy.yml` |
| Stable concepts and typed semantic relations | `data/concepts.yml` |
| Controlled knowledge domains | `data/domains.yml` |
| Non-page implementation resources | `data/resources.yml` |
| Page identity, editorial role, destination, tags, hierarchy, related and suggested navigation | `LLM-LAB-PAGE-MAP` metadata in page source |
| Sequential Understand route | `data/guided-route.yml` only |
| Build route and deliverables | Existing Build route definitions and docs |
| Source-to-project synthesis and provenance | Existing `docs/source-reviews/`, `docs/source-syntheses/`, extraction records and references |
| Generated graph, map, route and navigation projections | Existing generators; never hand-edit generated outputs |

Keep these structures distinct:
- concept graph relations are semantic, not reading instructions;
- page hierarchy expresses containment/organization, not necessarily prerequisites;
- `related` expresses useful discovery links, not a route;
- `suggested_route` is page-level local navigation, not a second global curriculum;
- domain membership is classification, not causality or dependency;
- source citations are provenance, not proof that sources independently corroborate one another.

Use only existing controlled values. Propose a schema, relation type, tag namespace or domain change only when several real cases require it; document migration and validator implications before adoption.

## 6. Gate 3 — evidence and synthesis

For source-backed changes, complete Phase A extraction before Phase B integration unless a trustworthy, current extraction already exists. Follow the canonical source-to-knowledge protocol.

For project-derived knowledge that is not tied to one external source:
- record the derivation, implementation/test, dataset or observation that supports it;
- separate established facts, project-specific results, hypotheses and design choices;
- include assumptions, scope, uncertainty, counterexamples and failure conditions;
- cite the exact primary/official source or local artifact where the claim depends on it;
- do not create a synthetic citation or imply independent corroboration from derivative sources.

For each candidate contribution, compare its learner question, explanatory lens, mental model, example phenomenon, teaching move, abstraction level, evidence and caveats with the exact existing coverage. Assess novelty and complementarity separately. A low-novelty complementary perspective can be valuable; a novel detail can still be noise.

Use only item dispositions defined by `data/source-taxonomy.yml`. Keep source scan status, extraction completeness, synthesis, integration and validation as independent states.

**Pass condition:** each accepted contribution has a precise evidence boundary, a decision and a canonical destination. Useful rejected/deferred material remains traceable where appropriate.

## 7. Gate 4 — create or update the learning artifact

### Existing page
- Preserve its declared purpose and canonical scope, or document why that contract must change.
- Add only the explanation needed for the learner question.
- Link to the canonical owner for details rather than duplicating a second full explanation.
- Keep examples, figures, equations, exercises and references consistent with the updated text.
- Record a source-to-destination conservation map for every move, merge, shortening or replacement.

### New page
Use [New learning page skill](../../.agents/skills/new-learning-page/SKILL.md) and the existing [page-template guide](../page-template-guide.md), page archetype and metadata schema. Before implementation, define:
- one durable learner question and observable outcome;
- intended audience, prerequisites, scope and exclusions;
- canonical concepts and source evidence;
- why existing pages cannot own the material;
- destination (Understand, Build, Deepen, Practice & experiment or reference);
- language counterparts and any justified exception;
- links and graph/navigation implications;
- preservation, validation and maintenance plan.

Do not invent a new Understand route. If the sequential route genuinely needs changing, update `data/guided-route.yml` and its documentation/tests as a separate, explicit curriculum decision. Optional Deepen pages remain optional and must not acquire implied order from sibling links or hierarchy.

### Graph update
Add a concept only if it is stable, reusable, clearly distinguishable and useful beyond one page/source. Reuse existing IDs and relations. Every new relation must have a precise meaning, direction and evidence. Do not turn examples, transient claims, section headings, tools or source-local nodes into canonical concepts automatically.

A new concept should have bilingual labels/definitions and useful page-resource associations. Update the concept registry and its validator fixtures/tests; regenerate graph projections through their canonical generator.

## 8. Gate 5 — connect the knowledge, not just the files

For each accepted change, inspect relevant neighboring concepts and pages. Consider cross-domain relations when they reveal a real shared mechanism, causal link, analogy, constraint, application or contrast.

Use typed relations, not generic `related-to`. For example, distinguish:
- shared mechanism from superficial vocabulary overlap;
- causal contribution from correlation;
- analogy from identity;
- prerequisite from application;
- contradiction from mere difference;
- independent corroboration from shared citation lineage.

Cross-domain connections should help explain one subject through another without flattening either field. Keep separate definitions and evidence boundaries where disciplines use similar terms differently. Record the bridge's value and limits.

Update page `related` links only when they answer a useful next question. Do not create a complete clique among all related pages. Update concept-resource associations only where the page actually supports the concept.

**Pass condition:** a reader can understand why each important link exists and what question it helps answer.

## 9. Gate 6 — bilingual and preservation checks

For every published bilingual change:
- update the French and English counterparts substantively, not necessarily literally;
- preserve intentional language-specific narrative, examples, references and cultural cues;
- compare scope, learning outcomes, technical claims, equations, caveats, examples, exercises and navigation;
- use language-matched links and illustrations;
- record an explicit exception when no counterpart is appropriate.

For every move, split, merge or shortening, maintain a conservation ledger:

| Source block | Information/learner function | Decision | Destination/anchor | Verification |
|---|---|---|---|---|
| Exact source heading/anchor | Definition, derivation, caveat, example, figure, exercise, citation, link, etc. | keep / move / merge / summarize / retire with rationale | Exact path and target anchor | Present, rendered, tested |

Do not remove a source block until its replacement or destination exists and has been checked. Keep distinctive examples and caveats even when a general explanation is consolidated.

## 10. Gate 7 — validate at the right layers

Run checks proportionate to the changed system. Expand scope when shared schemas, registries, generators, templates or routes change.

| Layer | Examples | What it establishes (and does not) |
|---|---|---|
| Source/provenance | exact locators, scan scope, rights, external reference spot-check | Traceability; not scientific truth by itself |
| Technical | primary-source review, derivation, code tests, experiment reproduction | Scoped correctness; not pedagogical effectiveness |
| Data/schema | YAML/schema and source/concept/resource/page metadata validators | Structural contract; not semantic quality |
| Graph/navigation | concept endpoints/relations, page links, route membership, generated projection freshness | Structural coherence; not learner comprehension |
| Bilingual | FR/EN structure and semantic comparison | Parity; not independent translation review unless performed |
| Build/render | relevant unit tests, full Quarto render when applicable, rendered local-link check | Buildability and local link integrity; not accessibility |
| Rendered/accessibility | desktop/mobile, theme, keyboard, screen-reader/text alternative, interaction/error states | Observed usability for tested cases only |
| Learner | formative tasks, transfer questions, independent observation | Evidence for tested learners/tasks only; not broad efficacy |

Report each layer as **passed**, **failed**, **pending**, **not run** or **not applicable**, with the exact command/commit where possible. Do not imply a browser or learner check from a passing CI run.

## 11. Gate 8 — close the loop

The change is ready for review when:
- the issue/PR ownership is clear and linked;
- the problem statement and scope are explicit;
- source and knowledge decisions are traceable;
- all accepted material has one canonical owner;
- prior useful knowledge is preserved;
- graph/page/route semantics remain distinct;
- bilingual counterparts and language-specific editorial choices are respected;
- generated artifacts are regenerated, never hand-edited;
- relevant tests and renders are reported honestly;
- unresolved work is recorded in the existing issue rather than silently left in prose.

The completion report should include:
1. learner problem and change mode;
2. canonical files/artifacts changed;
3. sources and evidence boundaries;
4. concepts/relations/pages/resources added, changed or intentionally unchanged;
5. cross-domain links considered and why retained/rejected;
6. preservation map;
7. FR/EN parity and intentional differences;
8. validation matrix;
9. remaining risks and revisit triggers.

A task can be complete with an explicit no-change decision. It is not complete merely because a page, source record, graph node, issue or PR was created.

## 12. Maintenance and improvement

Update this workflow only when canonical ownership, gate semantics or validation responsibilities change. Keep detailed page composition in page templates, source procedures in source workflows, and graph semantics in information-architecture documentation. Do not copy their full checklists here.

When a repeated failure appears, add a targeted test or validator before adding another prose checklist. Review the workflow against real additions and page changes; record case-specific lessons in dated audits, not as permanent universal rules.
