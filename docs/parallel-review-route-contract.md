# Parallel learning and review routes

**Status:** architectural contract and implementation plan  
**Date:** 2026-11-23  
**Canonical route source:** `data/guided-route.yml`  
**Current reader-facing projections:** `site/<lang>/learning-map.qmd` and `site/<lang>/review-path.qmd`

## 1. Decision

LLM Lab has two equivalent routes through the same curriculum:

1. **Learning route** — the primary route, using canonical lesson pages to build understanding.
2. **Review route** — an alternative route through the synthesis/revision pages and retrieval aids corresponding to those same lessons.

The review route is not a resource directory, an appendix, or a list of optional revision materials. It is a complete alternative traversal of the curriculum. A reader must be able to follow it from the first stage to the last without having to reconstruct the order from individual lesson pages.

Both routes are projections of one canonical pedagogical model. They must not have independently maintained stage lists, lesson order, prerequisite chains, or conceptual groupings.

\[
P_{learn}=\Pi_{learn}(G),\qquad
P_{review}=\Pi_{review}(G)
\]

Here, \(G\) is the canonical curriculum model. The projections differ in the learning artifact presented, not in the concepts, stage topology, or intended progression.

## 2. What must remain equivalent

For each language, the following properties are invariants:

| Property | Learning route | Review route |
|---|---|---|
| Stage identity and order | From `guided-route.yml` | Same IDs and order |
| Stage title and objective | Canonical stage metadata | Same meaning and language parity |
| Core lesson membership | `stage.pages` | One corresponding revision destination per core lesson |
| Lesson order within a stage | Canonical page order | Same order |
| Prerequisites / prior learning | Canonical lesson contract | Same dependencies, expressed for revision |
| Optional material | `stage.optional_pages` | Remains optional; never promoted to a core prerequisite |
| Bilingual structure | FR/EN route projections | Same stage and lesson identities across languages |
| Conceptual transitions | Canonical route and typed relations | Same transitions, expressed through revision aids |

Equivalence is structural and semantic, not a requirement that both routes have identical page counts or identical prose.

## 3. Canonical ownership and projection

### 3.1 One curriculum source

`data/guided-route.yml` owns stage IDs, stage order, core and optional page membership, objectives, overviews and conceptual focus.

`lesson_contracts` in that same file owns the mapping from each core lesson ID to its synthesis page and the lesson-level revision contract (including prerequisites, scope and outcome).

The review route must be generated from these structures. Do not introduce a second YAML file containing a manually copied sequence of review pages.

### 3.2 Core lesson mapping

For every core page in every stage:

- resolve exactly one primary synthesis/revision destination through its lesson contract;
- preserve the lesson's position within its stage;
- show the canonical lesson as a secondary link for readers who need a deeper explanation;
- carry the same prerequisite relationships and learning outcome into the revision presentation;
- validate that the revision destination exists in the same language projection.

The current contract uses one primary synthesis destination per core lesson. If the editorial model later permits several aids for a lesson, the primary route destination must remain unambiguous; additional aids can be presented as supporting material within that lesson's review stop.

A shared synthesis may support several lessons only where the canonical contract explicitly says so. Do not duplicate a shared aid merely to create artificial one-to-one ownership.

### 3.3 Optional pages

Optional lesson pages remain optional in the review route. They may link to an existing revision aid when one is explicitly registered, but absence of such an aid must not silently turn the optional lesson into a core stop.

The first implementation should expose optional revision support honestly and distinguish:
- an optional lesson with a corresponding revision aid;
- an optional lesson without a dedicated revision aid;
- an optional resource that is contextual/reference material rather than a lesson to revise.

Do not infer these distinctions from filenames, topic similarity, sidebar position or generic `related` links.

## 4. Role of synthesis sheets and flashcards

The review route has a stable stop for each core lesson. Different revision formats belong inside or alongside that stop:

- **Synthesis sheet:** reconstructs the central question, mechanism, essential distinctions, limits and key takeaways.
- **Flashcards:** support active retrieval of definitions, relationships, equations, distinctions and consequences.
- **Visual recall prompt:** asks the learner to reconstruct or interpret a diagram before revealing a concise correction.

Flashcards are not a second curriculum and must not create new stages. They are revision instruments attached to the corresponding lesson/revision stop. A lesson may have several decks or cards; a deck may cover several lessons only when its coverage is explicit.

The review route must not claim that every lesson has flashcards until an explicit inventory and coverage check establish that fact. Existing visual recall links on `review-path.qmd` are a small manually curated set, not evidence of complete flashcard coverage.

Exercises and implementation experiments remain in **Practice & experiment**. The review route may link to them as a separate next step, but must not embed exercise collections in the review sequence or conflate flashcards with worked exercises.

## 5. Reader experience

The review route should provide:

1. a short explanation that this is an alternative route through the same curriculum;
2. a complete stage navigator, in the same order and with the same stage grouping as the learning route;
3. for each stage, its question/overview and objective;
4. for each core lesson, the corresponding synthesis/revision page as the primary action;
5. concise prerequisite context and the expected knowledge outcome;
6. flashcards or visual-recall links attached to the relevant lesson, when registered;
7. links back to the canonical lesson and separately to relevant practice material;
8. clear progress through the same stage IDs (for example, stage 4 of 9).

The learning route should in turn expose a clear route switch to the review route. The review route should link back to the learning route. These are peer experiences, not a primary page plus a hidden appendix.

The route switch must remain discreet enough not to compete with the lesson content, but visible at the entry points and at useful transition points.

## 6. Current implementation: what exists and what is missing

The repository already has important foundations:

- `data/guided-route.yml` defines the ordered stages and their core/optional pages.
- `lesson_contracts` maps the 20 core lesson IDs to synthesis destinations and records prerequisites.
- `build_learning_map.py` resolves the bilingual route and renders generated lesson contracts.
- `site/fr/review-path.qmd` and `site/en/review-path.qmd` include the generated lesson-contract plan.
- `tests/knowledge/test_lesson_contracts.py` verifies core lesson coverage, synthesis links, objective rendering, language parity and selected prerequisite constraints.

However, the current review page is still titled and introduced as a **plan of the route and sheets**. It presents stage-grouped lesson contracts, but it is not yet validated as a full peer route. In particular:

- the route-level equivalence invariant is not asserted as one explicit contract;
- optional page membership is not yet projected as optional revision destinations;
- the three visual recall links on the review page are manually curated and not attached through a complete card/deck coverage model;
- the review entry point and route switch need a deliberate peer-navigation treatment;
- tests do not yet state in one place that both projections have exactly the same stage topology and core lesson order.

This is a gap in the projection and its validation, not a reason to create another curriculum registry.

## 7. Validation requirements

Add tests that derive both route projections from the same `GuidedRouteDocument` and assert:

1. identical ordered stage IDs;
2. identical stage titles and objectives by language;
3. identical ordered core lesson IDs in every stage;
4. exactly one resolvable primary synthesis destination for every core lesson;
5. no missing, duplicate or reordered core lesson destination;
6. preservation of optional membership and optional status;
7. equivalent prerequisite relationships and learning outcomes;
8. French/English semantic structure parity (same stage IDs and lesson IDs, with language-specific targets);
9. every registered flashcard/deck resolves to at least one valid lesson/revision stop;
10. no exercise-only page is mistaken for a synthesis or flashcard aid.

Tests should compare structured projections, not scrape rendered prose as the sole source of truth. Separate rendering tests should verify that the reader-facing pages expose the complete route, route switch, links, language destinations and accessible labels.

A coverage report should distinguish **missing**, **not assessed**, **present**, and **sufficiently reviewed**. A link existing is not evidence that a synthesis or deck is pedagogically sufficient.

## 8. Implementation sequence

1. **Lock the invariant:** adopt this contract and link it from the existing learning-path documentation.
2. **Build a structured review projection:** derive stage and lesson nodes from `guided-route.yml` plus `lesson_contracts`; do not duplicate route data.
3. **Represent revision formats:** reuse the existing typed revision-resource relationship contract and project synthesis sheets, flashcards and visual-recall aids into their lesson stops. Do not introduce a competing registry.
4. **Preserve optionality:** decide how optional pages with and without revision aids appear, based on explicit metadata.
5. **Render the peer route:** generate both language versions from the same projection logic and add route-switch links from both entry points.
6. **Add structural and rendered tests:** prove stage/lesson parity, language parity, link integrity and accessibility.
7. **Migrate incrementally:** validate a representative stage first, then the complete route. Do not mass-create flashcards or sheets to satisfy a count.

## 9. Boundaries with adjacent work

- [#1109](https://github.com/JM-Brun/llm-lab/issues/1109) owns the editorial quality and bilingual pilot of synthesis sheets.
- [#575](https://github.com/JM-Brun/llm-lab/issues/575) owns the canonical computational spine and the distinction between computation, knowledge relationships and pedagogical progression.
- The revision-resource relationship contract owns typed aid-to-lesson links and revision-support assessment.
- This contract owns the equivalence of the two reader-facing curriculum routes.

These responsibilities must coordinate through existing canonical registries; none should create a competing stage, concept, page or resource inventory.

## 10. Acceptance criteria

- [ ] The learning and review routes are explicitly presented as peer routes through the same curriculum.
- [ ] Both are generated from the same canonical stage and lesson model.
- [ ] Every core lesson has one primary revision destination in each language.
- [ ] Stage order, lesson order, objectives, prerequisites and outcomes are structurally equivalent.
- [ ] Optional material remains optional in both routes.
- [ ] Flashcards and visual-recall aids are attached to relevant lesson stops through explicit relationships.
- [ ] Exercises remain a separate Practice & experiment experience.
- [ ] FR/EN route structure and destinations are validated.
- [ ] Automated tests fail on missing, duplicated, reordered or incorrectly promoted core/optional memberships.
- [ ] No parallel curriculum registry or mass-generated low-value revision content is introduced.
