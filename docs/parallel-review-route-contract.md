# Parallel learning and review routes

**Status:** core bilingual Review route implemented; optional revision formats and complete visual-recall coverage remain partial.  
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

## 6. Current implementation and remaining gaps — 2026-11-23

### 6.1 Implemented core route

The core learning/review projections are now implemented and tested:

- `data/guided-route.yml` remains the single owner of the nine stages, core/optional memberships, transitions and conceptual focus.
- `lesson_contracts` maps the 20 core lesson IDs to their primary synthesis destinations and records prerequisites, scope and outcomes.
- `build_learning_map.py` resolves the bilingual route and renders the stage-grouped review plan.
- `site/fr/review-path.qmd` and `site/en/review-path.qmd` expose that generated plan and link back to the learning route.
- PR [#1549](https://github.com/JM-Brun/llm-lab/pull/1549) makes the Understand and Review sidebars flat, peer projections: 20 core lessons in canonical order, followed by the review index, 20 primary synthesis pages and two shared cross-lesson review aids.
- The same PR moves optional route companions out of the core Understand sidebar and keeps them discoverable in Deepen. The numerical information-theory experiment remains in Practice.
- `tests/knowledge/test_lesson_contracts.py` checks core lesson coverage, synthesis links, objectives, prerequisites, stage grouping and FR/EN parity.
- `tests/knowledge/test_flat_curriculum_sidebar.py` derives both sidebar sequences from the canonical route and lesson contracts, then asserts exact order, one-level navigation, optional-page placement and Practice separation.
- `ProjectIndex` validates the current page-based `revision_role`, `revision_of` and `revision_support` metadata and derives both aid→lesson and lesson→aid queries. See the updated [revision-resource contract](revision-resource-contract.md).

The core route therefore no longer needs a second curriculum registry or a manually maintained list of synthesis pages.

### 6.2 Remaining gaps

1. **Optional revision support:** optional learning pages remain optional and discoverable in Deepen. They are not currently projected as optional stops in the Review sidebar. Add an optional revision link only where a genuine aid is explicitly registered; do not create aids merely to mirror page counts.
2. **Visual recall and flashcards:** the review index currently links three manually curated visual-recall sections. This is not a complete flashcard/deck inventory and must not be presented as one.
3. **Learner-facing wording:** the review index still uses the title “Plan du parcours et fiches de révision” / “Learning path plan and review sheets”. Consider a concise title that makes the peer-route role clearer, but preserve its current function and avoid adding another navigation level.
4. **Rendered validation:** structural tests and successful rendering do not replace a visual and keyboard review of the Review sidebar, route switch, stage disclosures and synthesis pages at desktop and mobile widths.
5. **Pedagogical sufficiency:** the existence of a synthesis page or typed revision edge does not establish that the aid is sufficiently complete, accurate or effective. Keep editorial quality review separate from link integrity.

The core route is implemented; these remaining points concern optional coverage, presentation and learner validation, not missing core curriculum identities.

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

- [x] The learning and review routes are presented as peer routes through the same curriculum.
- [x] Both core routes are generated from the same canonical stage and lesson model.
- [x] Every core lesson has one primary revision destination in each language.
- [x] Core stage order, lesson order, objectives, prerequisites and outcomes are structurally checked.
- [x] Optional learning pages remain outside the core route and are discoverable in Deepen; optional revision stops are not fabricated.
- [ ] Flashcards and visual-recall aids have a complete, explicit coverage inventory. The current three visual-recall links are only a manually curated subset.
- [x] Exercises remain a separate Practice & experiment experience.
- [x] FR/EN core route structure and destinations are validated.
- [x] Automated tests protect core order, exact review destinations, optional-page placement and Practice separation.
- [x] No parallel curriculum registry or mass-generated low-value revision content is introduced.
- [ ] Desktop/mobile rendered review, keyboard navigation and learner-level validation are recorded.

## 11. Lesson size and editorial rhythm

The curriculum is made of **lessons**, not arbitrarily long topic pages. Except for orientation/overview pages, a core lesson should normally represent **10–15 minutes of focused reading**. This is a target band, not a quota: conceptual completeness and a coherent learning outcome take precedence over an exact word count.

### 11.1 Estimate reading time honestly

Reading time must account for more than prose word count. The editorial audit should record:
- prose and explanatory text;
- equations and mathematical derivations;
- diagrams that require interpretation;
- code walkthroughs or worked examples;
- optional/revealed material, counted separately from the main reading path.

Use a consistent estimation method and expose the estimate as editorial metadata or audit output, not as a prominent decorative badge. Do not count hidden details, exercises, references or optional deep dives as mandatory reading. Flag lessons substantially outside the target band for editorial review.

### 11.2 Split by conceptual boundary, not by length alone

When a lesson is too long, split it only where each resulting lesson can have:
- one clear question or problem;
- one coherent conceptual scope;
- a meaningful learning outcome;
- prerequisites available earlier in the canonical route;
- a complete explanation without requiring the reader to consult its revision page.

Do not split a derivation, mechanism or causal explanation merely to hit a duration. Conversely, do not combine independent concepts just to reduce page count. Update the single canonical route and lesson contracts when a split or merge is justified; never maintain a parallel list of lesson fragments.

### 11.3 Shared lesson template

Core lessons should use a stable visual and pedagogical pattern:

1. **Compact opening:** route breadcrumb/progress, one central question or key idea, and the lesson objective. Avoid stacking several metadata banners.
2. **Main explanation:** a continuous narrative, with consistent heading hierarchy; definitions, notation, equations and diagrams appear where they are needed in the argument.
3. **One integrated example or interpretation:** selected to make the mechanism operational, not as a detached decorative aside.
4. **Short conclusion:** the result established and the transition to the next lesson.
5. **Quiet navigation:** a link to the corresponding review page and the next canonical lesson.

The template is a rhythm, not a rigid checklist. A section may be omitted when it adds no value; it must not be filled with generic boilerplate.

### 11.4 Keep the main route readable

The main lesson should prioritize the explanatory argument. As a default, keep only:
- at the opening: the route context and one concise statement of the central idea/objective;
- at the end: one concise takeaway or transition, plus the review-page link.

Avoid interrupting the argument with repeated callouts, editorial notes, multiple analogies, resource boxes, long caveats, exercise lists, recap panels and optional digressions. Move these to the corresponding review page or to an explicitly optional deep-dive page when they are not needed to follow the core explanation.

**Do not remove scientific qualifications that change the meaning of a claim.** A limitation, assumption, distinction or warning required to interpret an equation, diagram or conclusion correctly stays adjacent to that explanation. Only extended discussion, secondary examples and supplementary remarks move out of the main flow.

### 11.5 One review companion per lesson

Each core lesson has a corresponding review destination. The review companion is the consolidation workspace for that lesson and may contain, where available and explicitly linked:
- a compact conceptual skeleton / reconstruction outline;
- the synthesis sheet and key equations;
- definitions and essential distinctions;
- flashcards and active-recall prompts;
- short comprehension questions with answers or feedback;
- remarks, caveats, alternative intuitions and common confusions;
- links to relevant exercises, experiments and optional deep dives.

These elements are not all required to exist before a lesson can be published. Missing formats must be reported honestly; do not fabricate flashcard coverage or duplicate content to fill a template. A review page must remain understandable as a revision artifact, but it does not replace the complete explanation in the main lesson.

Questions that test recall or conceptual discrimination belong in review. Multi-step problem solving, calculation practice, coding tasks and experiments remain in **Practice & experiment** and are linked rather than copied into the review page.

### 11.6 Migration protocol

Refactor incrementally by canonical stage:
1. measure all core lessons using the same reading-time method;
2. classify each interruption/box as essential-to-understand, useful-to-revise, optional-deepening or practice;
3. select one representative lesson and its revision companion as the template pilot;
4. compare the two pages for completeness, flow, visual rhythm and bilingual parity;
5. only then migrate the remaining lessons in bounded stage-sized batches.

No bulk deletion or movement is acceptable without checking that the explanation remains complete and that the moved material has a valid destination. Preserve source citations and provenance during moves.

