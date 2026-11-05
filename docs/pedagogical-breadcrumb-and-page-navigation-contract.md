# Pedagogical breadcrumb and page-navigation contract

**Status:** canonical contract; guided-route context pilot implemented; site-location breadcrumb still under investigation  
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

## 3. Breadcrumb and nested page context

### 3.1 Three distinct navigation dimensions

The page opening may expose three related but non-interchangeable cues:

1. **Site location** — the native Quarto breadcrumb, rendered as `.quarto-title-breadcrumbs` from the active sidebar hierarchy. It answers “Where am I in the published site?”
2. **Pedagogical context** — the generated `.guided-page-context` projection of `data/guided-route.yml`. It answers “Which learning stage does this page serve?”
3. **Local process or representation stepper** — a page-authored `.pipeline-stepper`, when useful. It answers “What are the steps of the process or representation described here?”

These cues can be nested in one page header, but they must not be concatenated into one synthetic ancestry chain. A curriculum stage is not a Quarto sidebar ancestor, and a process sequence is not a curriculum.

### 3.2 One site breadcrumb: Quarto is canonical

- Keep the native Quarto `.quarto-title-breadcrumbs` as the single site-location breadcrumb.
- Do not inject a second breadcrumb from JavaScript or reconstruct the same sidebar ancestry in a parallel component.
- The custom `.llm-breadcrumb` implementation is retired; the language-switch script must not create site-location navigation.
- Preserve the Quarto breadcrumb's hierarchy and current-page indication. Style it for legibility and responsive wrapping without creating a second visual trail.
- Do not remove or rename sidebar sections to manipulate the breadcrumb; the Quarto sidebar remains the source of site hierarchy.

### 3.3 Pedagogical context is nested, not merged

For a page with exactly one guided-route membership, show the localized stage as a compact, linked context cue directly below the title/subtitle block and before the chapter lead. It is a subordinate context for the current page, not another breadcrumb path.

For a page with multiple memberships, retain all valid stage contexts and their objectives in a clearly labelled contextual section. Do not choose an arbitrary primary stage or render the memberships as one linear path.

The context is generated from `data/guided-route.yml`; reuse the existing generated partials. Do not derive it from `hierarchy.parents`, which describes conceptual containment and may be multi-parent.

### 3.4 Local steppers describe content, not location

A `.pipeline-stepper` is optional and page-specific. Retain it only when it accurately describes a process or representation sequence. Place it after the chapter lead and the short “idea to retain” explanation, so it supports the explanation rather than competing with the title and location cues.

Its accessible label must identify the process it describes (for example, “Étapes de l’entrée du modèle” or “Étapes du calcul de l’attention”). Do not label a local process stepper “learning path” / “parcours pédagogique”.

### 3.5 Multiple entry points

A page may be reached from multiple stages, concepts, or companion lessons.

- Preserve all explicit guided-route memberships and their core/optional status.
- Offer other useful entry points as contextual links in the page body or a small related-navigation area.
- Do not fabricate a single parent merely to make a breadcrumb look tree-shaped.
- If no defensible guided-route membership exists, omit the pedagogical context rather than display a misleading one.
- A deep dive may show its destination/domain and canonical concept owner without pretending to be a mandatory child of one lesson.

### 3.6 Semantics, accessibility, and duplication

- Use the native Quarto breadcrumb for site location and a separately labelled semantic `nav` for a single guided-route context.
- Keep labels short, localized, and human-readable; stable identifiers must never leak into visible text.
- Ensure keyboard focus, visible focus state, sufficient contrast, and a usable narrow-screen layout.
- Do not use color alone to communicate current position.
- A page may show one site breadcrumb, one pedagogical context, and one local process stepper when all three add distinct information. Never render duplicate instances of the same dimension.

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

For a substantive concept lesson, the preferred opening order is:

1. native Quarto site breadcrumb;
2. page title and subtitle;
3. pedagogical stage context, when the page has a reliable guided-route membership;
4. compact epistemic or status metadata, when useful;
5. concise chapter lead establishing the central idea and scope;
6. a short “idea to retain” or first-pass explanation, when it adds information rather than repeating the lead;
7. a local process/representation stepper, only when it materially helps and only after the initial explanation;
8. main explanation.

Quarto renders the site breadcrumb in the title block; the generated pedagogical context belongs immediately after that title block. These are separate dimensions in one coherent header, not two breadcrumb trails. The local stepper belongs to the content flow, not to the breadcrumb hierarchy.

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
