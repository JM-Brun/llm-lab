# Pedagogical breadcrumb and page-navigation contract

**Status:** proposed implementation contract  
**Scope:** reader-facing navigation across the bilingual LLM Lab site.  
**Coordination:** [#368 — consistent bilingual lesson-page template](https://github.com/JM-Brun/llm-lab/issues/368), [#225 — conceptual curriculum](https://github.com/JM-Brun/llm-lab/issues/225), [#415 — guided path vs resource graph](https://github.com/JM-Brun/llm-lab/issues/415), [#337 — rendered curriculum/navigation review](https://github.com/JM-Brun/llm-lab/issues/337).

This document specializes the existing [reader-experience and editorial method](reader-experience-and-editorial-method.md), [page-template guide](page-template-guide.md), and [page metadata schema](page-metadata-schema.md). It does not create a new page taxonomy, curriculum, concept registry, or metadata system.

## 1. Design objective

A reader should be able to determine, with little effort:

1. where the current page sits in the learning experience;
2. what question the page answers and why it matters;
3. what knowledge is genuinely needed before reading;
4. which material is core and which is optional;
5. what useful next action is available.

Consistency means stable cognitive and navigation cues, not identical page layouts or compulsory sections.

## 2. Keep navigation dimensions separate

| Dimension | Reader question | Existing source of truth | Must not be inferred from |
|---|---|---|---|
| Site/section navigation | Where is this page in the published site? | Quarto navigation and page destinations | Concept relations |
| Pedagogical breadcrumb | Which stage/context of the learning route am I viewing? | Existing curriculum stages and their page crosswalk | File path, sidebar nesting, concept hierarchy |
| Suggested reading transition | What is a useful page before/after this one? | `suggested_route.previous/next` | Strict prerequisite semantics |
| Conceptual hierarchy | Which concepts/pages contain or decompose this topic? | Typed page hierarchy | Reading order or processing order |
| Concept relations | How are the knowledge entities semantically related? | Typed concept graph | Visual proximity |
| Build dependencies | What must be implemented before this step? | Guided-build implementation sequence | Conceptual curriculum |
| Exploratory discovery | What else is connected and worth exploring? | Page/resource/concept graph views | A mandatory linear route |

These projections may link to one another, but their semantics remain distinct. In particular, **a pedagogical breadcrumb is not a concept-graph ancestry path**.

## 3. Breadcrumb behavior

### 3.1 Two complementary trails, not two competing curricula

When both add distinct orientation value, render two separate trails with explicit, localized labels:

1. **Site-location breadcrumb** — derived from the Quarto navigation hierarchy. It answers “Where am I in the published site?” It is a location aid, not a learning sequence.
2. **Pedagogical route context** — derived from the existing guided-route registry and its page crosswalk. It answers “Which learning route or stage gives this page its instructional context?” It is not a conceptual-parent chain and does not imply that every earlier stage is a strict prerequisite.

The two trails are separate projections of existing sources. Do not merge their items into one synthetic ancestry chain. Do not create a third breadcrumb from `hierarchy.parents`: that field describes conceptual containment/decomposition and can be multi-parent. Use it for contextual relationships, not automatically for reader-facing breadcrumb ancestry.

The pedagogical context component already piloted by PR #522 is a generated projection of `data/guided-route.yml`. Reuse and extend that component rather than adding page-specific breadcrumb markup or a parallel renderer. The Quarto sidebar remains the source for site location; its ancestry should not be copied into page metadata.

Render only the trails that provide distinct value. If both are shown, give them different accessible names (for example “Site location” / “Emplacement dans le site” and “Learning path” / “Parcours pédagogique”) and distinguish their visual hierarchy. Avoid duplicate adjacent links and avoid presenting the two trails as one continuous sequence.

### 3.2 Guided-route context

For pages assigned to a curriculum stage, show a compact breadcrumb using the existing stage names and page crosswalk. The breadcrumb should communicate the primary guided context, not claim that every item is a strict prerequisite.

Example (illustrative labels only):

`Understand → Data representations → Embeddings`

Use localized labels in French and English. Stable identifiers may be used internally but must never leak into visible labels.

### 3.3 Multiple entry points

A page may be reached from multiple stages, concepts, or companion lessons.

- Select one primary pedagogical context only when the curriculum explicitly establishes one.
- Offer other useful entry points as contextual links in the page body or a small related-navigation area.
- Do not fabricate a single parent merely to make the breadcrumb look tree-shaped.
- If no defensible primary route exists, omit the pedagogical breadcrumb rather than display a misleading one.
- A deep dive may show its destination/domain and its canonical concept owner without pretending to be a mandatory child of one lesson.

### 3.4 Breadcrumb semantics and accessibility

- Use semantic navigation markup with distinct accessible labels for the site-location and pedagogical trails when both are rendered; the pedagogical trail may use “Learning path” / “Parcours pédagogique”.
- Mark the current page as the current item; do not make it a self-link.
- Keep labels short, localized, and human-readable.
- Ensure keyboard focus, visible focus state, sufficient contrast, and a usable narrow-screen layout.
- Avoid truncating away the current page identity. On small screens, collapse ancestors progressively or provide an accessible compact representation.
- Do not use color alone to communicate the current position.

### 3.5 Do not duplicate navigation

The breadcrumb is an orientation aid, not a replacement for:
- the global site navigation;
- the page's meaningful previous/next route;
- contextual links at the point where a concept is discussed;
- the exploratory graph.

Avoid rendering two visually competing breadcrumbs or repeating the same route in multiple adjacent blocks.

## 4. Shared page contract and archetype-specific composition

All published learning pages should expose the relevant subset of these reader cues:

- **Identity:** meaningful title and, where useful, a specific learner question.
- **Role and scope:** what the page explains and what it deliberately leaves to another page.
- **Purpose/outcome:** what the reader should be able to explain, distinguish, calculate, trace, implement, or evaluate.
- **Prerequisites:** distinguish essential prerequisites from useful background.
- **Main explanation:** put the minimum correct mental model and essential caveats before optional depth.
- **Connections:** contextual links to canonical concepts, companion questions, implementation, tests, or evidence when they exist.
- **Closure:** a useful self-check, next step, or return route when appropriate.

These are cues, not mandatory headings. Omit inapplicable elements; never add empty callouts, boilerplate, or a section solely to satisfy a checklist.

| Page archetype | Stable cues to prioritize | Do not force |
|---|---|---|
| Orientation/system overview | System position, central question, map of major components, purposeful branches | Full prerequisite list or detailed derivations |
| Concept lesson | Definition, intuition, mechanism, notation/example, assumptions and misconception | Every possible related concept or a fixed number of sections |
| Concept bridge/question lesson | Question, concepts connected, why the relation matters, return links | A duplicate canonical definition |
| Guided build | Build milestone, expected artifact/state, technical prerequisites, verification | A theoretical curriculum breadcrumb that misstates implementation order |
| Deep dive | Specialized question, domain, canonical owner, essential background, return path | Mandatory placement in the core route |
| Practice/experiment | Question, hypothesis, controls, observations, interpretation, limitations | A generic lesson outline |
| Glossary/reference | Lookup category, concise definition, authoritative explanation link | Full exposition or forced previous/next sequence |

The existing page metadata `type` and archetype/template guides remain authoritative. Do not add an `archetype`, `breadcrumb`, `keywords`, or duplicate route field without first proving the existing model cannot express the requirement.

## 5. Placement within a page

For a substantive lesson, the preferred opening order is:

1. pedagogical breadcrumb, when a reliable guided context exists;
2. page title and specific learner question;
3. concise orientation paragraph establishing the central idea and scope;
4. learning outcomes, using the established collapsible convention when useful;
5. essential prerequisites and useful background, only when they materially help;
6. main explanation.

This is a default, not a rigid template. Landing pages, references, experiments, and build walkthroughs should use their archetype-specific opening. Do not repeat the chapter lead in a second introductory callout.

Within the body, place links beside the concept or question they resolve. At the end, provide a next step only when it is genuinely useful; avoid generic “continue your journey” language.

## 6. Bilingual contract

French and English counterparts must preserve equivalent:
- breadcrumb meaning and destination;
- learner question, scope, and outcome;
- distinction between essential and optional material;
- navigation intent and return paths;
- scientific caveats and implementation-status claims.

Natural wording and section-heading differences are acceptable. Stable page/topic identifiers are shared where the existing metadata contract requires them. Never expose internal IDs as user-facing labels.

## 7. Data and implementation rules

1. Reuse the existing curriculum stage definitions and page crosswalk; do not duplicate stage definitions in page front matter.
2. Reuse the generated guided-route context component introduced in PR #522; do not create a second pedagogical renderer.
3. Derive site-location ancestry from Quarto navigation, not from page-map hierarchy.
4. Keep `suggested_route`, `hierarchy`, `related`, concept relations, and build dependencies semantically separate.
5. Treat the pedagogical context as a **projection** of the existing guided-route registry.
6. Do not infer prerequisite edges from curriculum order, sidebar order, breadcrumb order, or graph layout.
7. Prefer deriving both trails from their existing sources at render/build time over hand-maintaining a second per-page route.
8. If the current data cannot express multiple route membership or a primary context, document the gap and propose the smallest extension before changing the schema.
9. Keep LLM Lab independently buildable; do not introduce a runtime dependency on Wiki Knowledge.
10. Do not create a workflow or GitHub Action per page or concept. Reuse the existing validation and site workflows.

## 8. Pilot and rollout

Use a small, representative pilot before site-wide changes:

- one core concept lesson (for example, embeddings);
- one system overview;
- one specialized/deep-dive page (for example, QKV/attention);
- one guided-build page;
- one practice/experiment or reference page.

For each pilot page, record:
- current rendered behavior and metadata;
- the intended primary learning context, or why no breadcrumb is appropriate;
- useful alternate entry points;
- archetype-specific cues that are present, missing, or intentionally inapplicable;
- FR/EN parity;
- desktop, mobile, keyboard, and screen-reader observations.

Implement in small reviewable PRs. Preserve all unique scientific content. Do not combine navigation work with broad content rewrites.

## 9. Validation and evidence

### Automated checks

Reuse and extend existing validators only where they can verify deterministic invariants:

- breadcrumb stage/page references resolve;
- localized labels exist for displayed items;
- the current page is represented correctly;
- no internal identifier leaks into visible navigation labels;
- route membership does not silently create prerequisite edges;
- FR/EN counterparts resolve to equivalent route contexts;
- existing page metadata, concept graph, local links, and Quarto render checks continue to pass.

A validator can establish structural consistency; it cannot establish that the breadcrumb helps a learner.

### Manual review

Review rendered pages on desktop and mobile, including keyboard navigation and accessible names. Record observations separately from CI results.

### Learner validation

Test with readers who have not authored the site. Ask them to locate their position, explain the page's purpose, identify what is optional, and choose a sensible next step. Do not claim improved comprehension from successful rendering or internal review alone.

## 10. Acceptance criteria

- [ ] The breadcrumb has one documented pedagogical meaning and does not conflate hierarchy, prerequisites, or site location.
- [ ] Existing curriculum and crosswalk data are reused; no competing curriculum is introduced.
- [ ] Pages without a defensible primary route are not given misleading breadcrumbs.
- [ ] Multiple entry points remain discoverable without inventing a tree.
- [ ] Shared reader cues are consistent while archetype-specific structures remain flexible.
- [ ] French and English pages have equivalent navigation intent and learning outcomes.
- [ ] The pilot covers representative page archetypes before generalization.
- [ ] Automated validation, rendered browser review, accessibility review, and learner evaluation are reported as separate evidence.
- [ ] No unique scientific content is lost and no per-concept workflow/action is introduced.

## 11. Pilot audit

The source-level baseline and unresolved implementation questions are recorded in the [pedagogical breadcrumb pilot audit](pedagogical-breadcrumb-pilot-audit.md). It distinguishes inspected source evidence from rendered, accessibility, bilingual-parity, and learner-validation evidence.

## 12. Related existing contracts

- [Reader experience and editorial method](reader-experience-and-editorial-method.md)
- [Page-template guide](page-template-guide.md)
- [Page metadata schema](page-metadata-schema.md)
- [Site page design system](site-page-design-system.md)
- [Full curriculum plan](full-curriculum-plan.md)
- [Learning path](learning-path.md)
- [Content section mapping](content-section-mapping.md)
