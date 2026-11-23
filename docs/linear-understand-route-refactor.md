# Refactor the Understand route into a simple linear course

**Status:** architectural proposal based on repository inspection; no reader-facing pages or curriculum content have been moved yet.  
**Scope:** Understand / Comprendre route, its bilingual review counterpart, and the navigation that exposes them.  
**Related work:** [parallel review-route contract](parallel-review-route-contract.md), [lesson sizing and editorial rhythm](parallel-review-route-contract.md#11-lesson-size-and-editorial-rhythm), [issue #1541](https://github.com/JM-Brun/llm-lab/issues/1541), [canonical computational spine #575](https://github.com/JM-Brun/llm-lab/issues/575).

## 1. Decision to make

The current route is difficult to follow and maintain because the learner encounters several overlapping structures:

1. the conceptual stages and ordered core pages in `data/guided-route.yml`;
2. nested sections in the Quarto sidebar;
3. page hierarchy and suggested transitions in page metadata;
4. the exploratory learning map derived from the sidebar and page metadata;
5. the review plan, which repeats the stage groupings but is not yet a complete alternative traversal.

These structures serve different purposes, but the reader is exposed to too much of their hierarchy at once. The proposed simplification is:

> **One visible, linear sequence of core lessons, one corresponding review page per lesson, and no nested navigation levels inside the Understand course.**

The course remains conceptually grouped. Its nine stages become labels and orientation summaries in the course overview, not expandable navigation containers. Optional deep dives, Build, Practice & experiment, and reference material remain distinct destinations.

This is a navigation and editorial simplification, not a reduction of the knowledge model.

## 2. Repository facts observed

### 2.1 Canonical route

`data/guided-route.yml` currently defines nine ordered stages and bilingual core-page membership:

| Order | Stage ID | FR title | Core pages |
|---:|---|---|---:|
| 1 | `orientation` | Fonctionnement d’un LLM | 1 |
| 2 | `text-input` | Du texte aux tokens | 1 |
| 3 | `representations` | Des identifiants aux représentations | 3 |
| 4 | `computation` | Comprendre le calcul du Transformer | 4 |
| 5 | `prediction` | Des états à la distribution prédictive | 3 |
| 6 | `inference` | Exécuter l’inférence et générer du texte | 1 |
| 7 | `context-use` | Exploiter et concevoir le contexte | 2 |
| 8 | `scoring` | Attribuer un score aux tokens observés | 2 |
| 9 | `training` | Apprendre et mettre à jour les paramètres | 3 |
| | **Total** | | **20** |

The route also stores stage objectives, overviews, conceptual focus, optional pages, and cross-stage transitions. `lesson_contracts` maps the core lessons to their primary revision destinations and prerequisite references. This is valuable canonical information and should be preserved.

The nine stages are not all strict prerequisite chains. In particular, inference/generation, observed-target scoring, and training are distinct uses of the shared predictive distribution. A linear reader-facing order is a pedagogical itinerary, not a claim that every preceding lesson is a formal prerequisite for every later lesson.

### 2.2 Navigation

The French Quarto sidebar currently nests Understand content several levels deep. For example, the text/data entry contains nested groups for representations, Transformer computation and scores/probabilities; other groups separately expose generation/context, scoring, loss/gradients, and architectures/limits. This does not exactly mirror the nine canonical stages.

The English sidebar follows the same general nested-navigation model. The learning-map generator deliberately reads and preserves this recursive sidebar structure. Therefore, simply changing the route YAML would not simplify the reader-facing navigation: the sidebar and the generated exploratory map would still expose nested groupings.

Revision pages are published and linked from core lessons and the review-path index, but are not currently a flat, complete peer route in the sidebar.

### 2.3 Existing documentation drift

Some older reconciliation prose still describes an eight-stage route and older page memberships, while the current canonical YAML has nine stages and twenty core pages. This is a documentation drift risk. The refactor must treat the current validated YAML and lesson contracts as the source of truth, then reconcile older narrative audits rather than copying their obsolete counts or sequences.

## 3. Proposed reader-facing architecture

### 3.1 Understand overview: one entry point

The overview page is the only place where the complete course structure is introduced. It should contain:

- a short explanation of the learning objective and how to use the course;
- one compact linear list of the core lessons, numbered in reading order;
- a short stage label for each lesson (the existing nine groups);
- a direct link to each lesson;
- a direct link to the corresponding review route;
- a concise indication of what is optional and what belongs to Build or Practice.

The overview may preserve the nine stage summaries as a compact grouping or as a secondary "course structure" section. It must not require readers to navigate through nested pages or collapsible levels to discover the next lesson.

### 3.2 Main route: one flat sequence

All twenty core lessons are presented as one ordered sequence. Each lesson page has:

1. one compact opening with course position, central question/key idea and objective;
2. the continuous explanatory narrative;
3. definitions, notation, equations, figures and worked reasoning exactly where they are needed;
4. a short conclusion and transition;
5. one quiet link to its review companion and one next-lesson link.

The course navigation exposes the twenty core lessons at one level beneath the Understand entry point. No stage contains nested lesson sub-sections. The stage name can appear as a small contextual label in the lesson header and overview, but is not a navigation level.

A single linear order must not falsely turn every relationship into a prerequisite. The lesson contracts retain the actual `requires` information; the overview can describe sibling branches where useful without interrupting the main route.

### 3.3 Review route: same twenty stops, different artifacts

The review route uses the same ordered lesson identities and stage labels. It is not a separate curriculum registry.

Each stop links to exactly one corresponding review page and can expose the available revision resources:

- reconstruction skeleton / conceptual outline;
- synthesis and key equations;
- definitions and distinctions;
- flashcards and active recall;
- comprehension questions with answers or feedback;
- remarks, limitations, alternative intuitions and common confusions;
- links to relevant practice and optional deep dives.

The review route should be navigable linearly in the same order as the main route. Each review page offers a return to its main lesson, a previous/next review link, and a route switch to the corresponding main lesson. Missing resource types must remain visible as coverage gaps in internal audits, not be filled with invented content.

### 3.4 Other content destinations

The simplified course must not absorb every page into the linear sequence:

- **Deepen:** optional technical and historical details, advanced architectures, mathematical extensions and alternative approaches. They remain discoverable through the Deepen landing page and contextual links.
- **Practice & experiment:** exercises, calculations, coding, controlled experiments and evaluation tasks. These remain separate from both lesson and review sequences.
- **Build:** a distinct implementation route with its own milestones and dependency structure.
- **Reference:** glossary, sources, history and other lookup material.

A core lesson may link to any of these where contextually useful. Such links do not create extra mandatory stops in the Understand sequence.

## 4. Navigation changes

### 4.1 Quarto sidebar

Replace the nested Understand sidebar tree in both languages with a single flat list of core lessons, in the exact order generated from the canonical route. Keep the Understand overview / learning-map entry visible as the route's entry point.

Do not hand-maintain the twenty-link sequence in two sidebars. Generate or validate the flat list from the canonical route, or introduce a small generator that emits the Quarto sidebar fragment from `data/guided-route.yml`. If Quarto configuration cannot include generated fragments directly, use a generated file and a test that verifies exact parity with the canonical route.

Optional pages must not be interleaved with the twenty core lesson links. They remain in Deepen or in explicitly optional contextual links. Existing Build, Practice and Reference navigation can retain their own organization; this proposal does not require flattening every part of the website.

### 4.2 Learning map

The learning map remains useful for exploration, discovery and conceptual relationships, but it should not be the only way to follow the course. Its route view should show the same flat sequence as the overview and sidebar.

The exploratory map can continue to expose territories, concepts, relations and page metadata. However, nested sidebar sections should no longer be interpreted as the course's conceptual hierarchy. If the map still needs grouping, derive stage labels from the canonical route, not from nested navigation.

### 4.3 Previous / next

Native previous/next navigation should follow the canonical core sequence for core lessons. It must not unexpectedly enter optional pages, exercises, revision pages, Build pages or reference pages.

The review sequence has its own previous/next links over the same lesson identities and review destinations. Cross-route links should pair the same lesson ID. The overview and optional pages should not be accidentally inserted into the sequence.

### 4.4 Stage groups retained without nested navigation

The nine current groups remain useful for:
- communicating the conceptual progression;
- explaining the broad phases of the model's computation and uses;
- providing a compact progress indicator;
- grouping the overview list visually;
- supporting internal audits and curriculum coverage.

They should not be represented as additional nested page levels. A reader should be able to see the next lesson without expanding a parent section.

## 5. Content refactor and knowledge preservation

Flattening navigation alone will not make the course coherent. The twenty core lessons need a coordinated editorial review.

For each lesson, record before editing:

- canonical lesson ID and stage;
- current FR/EN source paths;
- primary synthesis/review destination;
- prerequisite references and learning outcome;
- estimated reading time, including equations, diagrams and code;
- current headings, figures, equations, examples, caveats, callouts, links and citations;
- material that belongs in the main explanation;
- material that can move to the review page;
- material that belongs in Deepen or Practice;
- proposed destination for every moved item.

Classify each content block into four categories:

| Classification | Destination | Rule |
|---|---|---|
| Essential explanation | Main lesson | Required to understand the claim, mechanism, derivation or example |
| Consolidation / retrieval | Review companion | Synthesis, reconstruction, flashcards, recall questions, secondary intuition, common confusions |
| Optional extension | Deepen or a clearly optional disclosure | Valuable but not required for the core outcome |
| Practice | Practice & experiment | Multi-step problem solving, calculations, coding and experiments |

A scientific qualification stays next to the claim it qualifies when removing it would make the explanation misleading. Do not move an assumption, limitation or boundary condition merely because it currently appears in a callout.

Every move must preserve source attribution, figure attribution/licence information, equation definitions, anchors where externally referenced, and useful cross-links. No content is deleted solely to reduce page length or visual density.

### 5.1 Lesson duration and scope

Except for the overview, target 10–15 minutes of focused reading per core lesson. The estimate must account for prose, mathematical reasoning, diagrams and code, not only word count.

Split an oversized lesson only at a genuine conceptual boundary where each resulting lesson has a coherent question, outcome, prerequisites and self-contained explanation. Merge undersized lessons only when they form one coherent learning objective. Do not force the duration target by padding or arbitrary splitting.

### 5.2 Shared visual template

Use one stable lesson rhythm in FR and EN:
- compact opening;
- continuous explanatory body;
- integrated example;
- concise conclusion;
- unobtrusive review and next-lesson links.

The main lesson should normally retain only the opening context/central idea and a short ending. Remove redundant metadata banners, repeated summary panels, secondary resource boxes, editorial asides and revision aids from the main narrative when they can be moved without loss.

The review page uses a complementary template with a conceptual skeleton, synthesis, recall resources and supplementary notes. It should not reproduce the main lesson verbatim.

## 6. Canonical data model and implementation boundaries

Keep `data/guided-route.yml` as the single source for:
- the nine stage identities and order;
- the twenty core lesson identities and order;
- stage objectives and overviews;
- optional page membership;
- conceptual focus and cross-stage transitions;
- existing lesson contracts, primary synthesis destinations and prerequisites.

Keep the concept model invariant:
- `data/concepts.yml`: concept identities, definitions, domains and typed semantic relations;
- `data/computational-graph.yml`: computational nodes, operations and typed data-flow relations.

Neither registry is to be rewritten to make the page navigation linear. The shared predictive distribution and its generation, scoring and learning branches remain exactly the conceptual/computational model described in the canonical computational-spine work.

The affected layer is the **page/resource model**:
- published page identities and `LLM-LAB-PAGE-MAP v1` metadata;
- page-to-page `hierarchy`, `suggested_route` and `related` relations;
- page-to-concept associations and first-class non-page resource associations;
- typed revision-aid relations and support assessments;
- reader-facing navigation projections in Quarto and the learning map.

Use the existing read-only `ProjectIndex` as the joined query model. It composes page metadata, page edges, route memberships, concept associations, domains, resources, revision edges and support assessments. It is not a second registry. Extend existing audits when their output omits a relation; do not create a parallel inventory or curriculum list.

Keep relation semantics distinct:
- `hierarchy.parents/children`: genuine page containment or decomposition, not a prerequisite or reading order;
- `suggested_route.previous/next`: an authored reading transition, not a formal prerequisite and not necessarily the twenty-lesson course;
- `related`: useful cross-links that are neither containment nor route order;
- `revision_of`: a typed revision-aid-to-lesson relation, separate from ordinary page links;
- concept-to-page and resource-to-page associations: explicit links to the stable concept/resource registries.

The canonical learner-facing sequence is projected from `guided-route.yml` and resolved `lesson_contracts`, not inferred from sidebar indentation, `hierarchy` or `suggested_route`. The concept graph, computational graph and page/resource graph communicate through explicit associations but must not become interchangeable.

Do not flatten or delete page relations merely because the reader-facing sidebar becomes linear. Review each affected edge according to its own semantics and preserve all useful incoming/outgoing links.

## 7. Migration sequence

Perform the refactor in small, reversible stages.

### Lot A — Baseline from existing metadata and graph tooling
1. Run the existing deterministic page/revision inventory and page-metadata audits against the same commit; do not hand-build a second inventory.
2. Use `ProjectIndex.build(root)` as the read-only joined projection of page metadata, page edges, guided-route memberships, concept associations, non-page resources, typed revision relations and support assessments.
3. Use `site/tools/audit_revision_coverage.py` for the bilingual Understand/Build inventory. Its JSON is the machine-readable migration baseline; its Markdown output is the human-readable coverage view.
4. Preserve all incoming and outgoing page-graph edges incident to affected pages, including `suggested_route`, `hierarchy` and `related`; keep typed revision edges and concept associations separately identifiable.
5. Distinguish page-level facts from content-block inspection. Only the latter requires a bounded editorial review of figures, equations, examples, citations, anchors and moved passages; do not maintain it as a second page registry.
6. Record the source commit and inventory schema/tool versions. Historical snapshots are evidence for their recorded commit, not a substitute for rerunning current canonical inputs.
7. Identify stale documentation that still describes eight stages or older memberships, then record current sidebar nesting and rendered previous/next behavior.

### Lot B — Navigation projection
1. Generate the flat twenty-lesson sequence from the canonical route.
2. Flatten the Understand sidebar in FR and EN without changing page content.
3. Align the overview and learning-map route view to the same order.
4. Verify previous/next links do not enter optional or unrelated destinations.
5. Keep Deepen, Build, Practice and Reference separate.

### Lot C — One bilingual lesson/review pilot
1. Use Q/K/V as the first pilot pair, as already audited in issue #1541.
2. Establish the shared main-lesson and review-page templates.
3. Strengthen the review page before moving secondary content out of the lesson.
4. Preserve all essential explanation, mathematical definitions, scientific caveats and provenance.
5. Measure reading time and inspect visual density at desktop and mobile widths.
6. Review both languages before accepting the pattern.

### Lot D — Stage-by-stage content refactor
Apply the validated template in bounded batches, keeping the existing stage IDs as editorial labels. After each batch:
- compare source content and destination content;
- check all figures, equations, citations, anchors and links;
- run the bilingual render and structural tests;
- review reading time and visual rhythm;
- update the review-resource coverage audit.

### Lot E — Retire redundant navigation, not knowledge
Once the flat route is validated:
- remove obsolete nested Understand sidebar sections;
- remove redundant duplicated route descriptions from overview pages;
- keep the nine-stage conceptual explanation in one authoritative orientation page;
- retain historical audits as dated evidence, but mark obsolete counts and decisions clearly;
- keep the exploratory map and knowledge graph available as secondary discovery tools.

## 8. Required validation

### Structural tests
- exactly nine canonical stages and twenty core lesson identities until an explicit curriculum change is approved;
- FR/EN have identical lesson identities, order and stage membership;
- every core lesson has one resolvable primary review destination per language;
- every review destination maps back to exactly one core lesson;
- optional pages never appear as mandatory core stops;
- the generated sidebar order equals the canonical core route;
- previous/next navigation follows only the corresponding route;
- the main route and review route have identical lesson identity/order;
- all moved resources retain explicit typed ownership and valid destinations.

### Editorial tests
- non-overview core lessons target 10–15 minutes, with documented exceptions;
- each lesson has one clear question and outcome;
- main explanations are complete without opening the review page;
- review pages contain revision artifacts rather than duplicate lesson prose;
- essential scientific caveats remain beside the claims they qualify;
- exercises remain in Practice & experiment;
- no figures, citations, examples, equations or useful anchors are lost during moves.

### Rendered experience
- FR and EN render correctly;
- desktop, mobile, keyboard and touch navigation work;
- the reader can identify the current lesson, previous/next lesson and paired review page without expanding nested navigation;
- route switching preserves the corresponding lesson;
- overview and review index do not become excessively long or visually noisy;
- a learner walkthrough confirms that the simplified order is understandable and does not imply false prerequisite dependencies.

## 9. Explicit non-goals

- Do not flatten Build into the Understand course.
- Do not turn Practice into a final mandatory stage.
- Do not remove optional deep dives or historical context.
- Do not discard the nine-stage conceptual model or the knowledge/computational graphs.
- Do not split all lessons mechanically to equal word counts.
- Do not migrate every current callout without classification.
- Do not merge PRs or remove pages merely to make the sidebar shorter.
- Do not claim learner validation based only on CI or static source checks.

## 10. Acceptance criteria

- [ ] The Understand route has one flat, canonical sequence of core lessons in FR and EN.
- [ ] The sequence is generated from or strictly validated against `data/guided-route.yml`.
- [ ] No nested page levels are needed to navigate the core course.
- [ ] The overview explains the nine conceptual groups without making them navigation barriers.
- [ ] Each main lesson has exactly one corresponding review destination.
- [ ] The review route is a complete peer traversal with the same lesson order.
- [ ] The review page carries revision aids and supplementary content; the main page remains a self-contained explanation.
- [ ] Main lessons target 10–15 minutes except overview pages, with justified exceptions.
- [ ] Deepen, Build, Practice and Reference remain distinct.
- [ ] No knowledge, scientific qualification, source, figure, equation, example or useful link is lost.
- [ ] The learning map distinguishes pedagogical sequence from exploratory page/concept relationships.
- [ ] Bilingual structural, rendered, accessibility and learner checks pass.

## 11. Open decisions to resolve during the pilot

1. Whether the overview is a dedicated short route page or whether the current learning-map page remains the entry point with the linear route at its top. Avoid maintaining two competing overviews.
2. Whether review navigation should be a dedicated full page with twenty stops, or whether the review route page should itself become a sequence of lesson companion entries. The preferred option is a concise index plus twenty dedicated companion pages, not one enormous revision document.
3. Whether a compact stage marker appears in lesson headers. It should orient the learner without recreating nested navigation.
4. Which existing optional pages are truly Deepen resources versus legacy core material that deserves promotion. Decide from learning outcomes and evidence, not sidebar location alone.

These decisions should be settled on the Q/K/V bilingual pilot and then applied consistently.
