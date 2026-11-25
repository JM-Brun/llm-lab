# Refactor the Understand route into a simple linear course

**Status (2026-11-25):** the flat bilingual sequence of 20 core lessons and its nine conceptual groups are implemented. The chapter/lesson proposal and first-pass source-level migration ledger are documented; bounded bilingual content and Practice-separation changes have since been merged (including [#1602](https://github.com/JM-Brun/llm-lab/pull/1602), [#1604](https://github.com/JM-Brun/llm-lab/pull/1604), [#1609](https://github.com/JM-Brun/llm-lab/pull/1609), [#1611](https://github.com/JM-Brun/llm-lab/pull/1611) and [#1613](https://github.com/JM-Brun/llm-lab/pull/1613)). The chapter model is still a proposal, not a second route registry. Remaining gates are rendered reading-time/first-screen review, complete bilingual desktop/mobile/keyboard validation, learner evidence, and any further content transfer justified by the migration ledger. See [the lesson migration ledger](lesson-migration-ledger.md) for current section ownership and evidence, and [issue #1541](https://github.com/JM-Brun/llm-lab/issues/1541) for the parallel Review route.  
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

The bilingual Understand sidebar is now a flat list of the twenty core lessons in canonical order. The Review sidebar is a peer projection: it follows the same lesson order, then exposes the review index, primary synthesis pages and shared review aids (PR [#1549](https://github.com/JM-Brun/llm-lab/pull/1549)). This removes nested navigation levels from the two main routes without deleting page hierarchy or exploratory map groupings.

The Review experience is not yet a complete peer traversal. The current review page still behaves primarily as a stage-grouped plan/sheet index; progress cues, complete route switching, optional-aid handling and learner-facing validation remain tracked by [issue #1541](https://github.com/JM-Brun/llm-lab/issues/1541). The learning map remains an exploratory projection and must not be mistaken for another mandatory route.

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

The flat bilingual Understand and Review sidebars are implemented by PR #1549. Keep the Understand overview / learning-map entry visible as the route's entry point. The twenty lesson identities and order must remain aligned with `data/guided-route.yml`; the sidebars are projections, not a second curriculum source.

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

### 6.1 Generated migration inventory

The existing `site/tools/audit_revision_coverage.py` is extended rather than replaced. Its machine-readable output combines:
- every published Understand/Build page record and its route membership;
- all incoming and outgoing page-graph edges incident to those pages, with relation family and direction;
- the direct associated-page closure, including revision aids, all pages with canonical route membership (regardless of destination), and pages in Deepen, Practice, Build or Reference;
- full records from `data/resources.yml` for non-page resources associated with the affected pages or their direct page neighbors;
- concept IDs associated with the same page neighborhood;
- missing associated page/resource IDs, which must remain empty in a valid migration baseline.

The inventory distinguishes the affected page set from its external associated pages. It records the complete guided-route membership counts separately from the narrower `understand_route` destination counts, so optional pages in Deepen are not silently omitted. It does not recursively crawl the whole website or duplicate the concept/resource registries: it records the direct, typed neighborhood needed to plan and validate a page refactor. The JSON output is the machine-readable migration ledger; the Markdown output summarizes the coverage and edge topology.

Run it from the repository root:

```bash
uv run --with-requirements docs/requirements-history-validation.txt \
  python site/tools/audit_revision_coverage.py \
  --json /tmp/understand-build-inventory.json \
  --markdown /tmp/understand-build-inventory.md

uv run --with-requirements docs/requirements-history-validation.txt \
  python site/tools/audit_page_metadata.py
```

Capture the source commit and inventory schema version with each artifact. Compare stable IDs and typed edges before and after each migration batch; aggregate counts alone are insufficient.

### 6.2 Generated baseline (2026-11-23, schema v5)

The CI artifact generated from commit `b90b37e5fa6a2bcf2ab9280764602f8a17b5b558` provides the initial migration baseline:

| Measure | Result |
|---|---:|
| Core lesson memberships | 40 (20 FR, 20 EN) |
| Optional route memberships | 56 across 54 unique pages (27 FR, 27 EN) |
| Published Understand pages | 46 (23 per language) |
| Published Build pages | 16 (8 per language) |
| Understand topics with exact FR/EN parity | 23 |
| Page-graph edges incident to Understand/Build pages | 760 |
| Direct associated page records outside those destinations | 184 |
| Typed revision-aid links to Understand pages | 50 across 40 pages |
| Associated non-page resources | 5 |
| Associated concept IDs in the direct page neighborhood | 102 |
| Missing associated page/resource IDs | 0 / 0 |

All 46 Understand pages and 16 Build pages have `integrated_sufficient` revision-support assessments. Forty Understand pages have explicit revision-aid links. The 50 links include shared aids, so link count and page count are not interchangeable.

**Important count distinction:** the older `understand_route.optional` field counts only optional pages whose editorial destination is `understand` (six bilingual page records). It is not the total optional curriculum. The full route projection now counts optional memberships across all destinations: 56 memberships over 54 unique optional pages. Many optional pages are correctly classified under Deepen and are included through the route-membership projection and direct associated-page closure.

The 760 page-graph edges are directed metadata records, not 760 independent semantic relations: reciprocal `parents/children` and `previous/next` declarations are explicit. The inventory keeps these edges separate from typed revision-aid relations, concept IDs and non-page resource records. The zero missing-ID counts confirm that the current direct neighborhood resolves against the published page and resource registries.

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

- [x] The Understand route has one flat, canonical sequence of core lessons in FR and EN (PR #1549).
- [ ] The sequence is generated from or strictly validated against `data/guided-route.yml`.
- [x] No nested page levels are needed to navigate the core course (PR #1549).
- [x] The overview explains the nine conceptual groups without making them navigation barriers.
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


## 12. Pedagogical target: short lessons grouped into chapters

The purpose of the refactor is not merely to flatten navigation. The reader-facing course must become a genuinely linear progression of **short, coherent lessons**, normally requiring 10–15 minutes of focused study each. Several lessons may be grouped into a chapter when they contribute to one larger learning objective. Chapters are orientation/grouping devices; lessons are the units the learner completes.

### 12.1 Information architecture

Use exactly three reader-facing levels:

1. **Course** — the complete path and its expected outcome.
2. **Chapter** — a meaningful conceptual phase, introduced by a short statement of what the learner will understand by its end.
3. **Lesson** — one question, one principal learning outcome, one bounded conceptual scope, and a target duration of 10–15 minutes maximum for the mandatory path.

A chapter may contain one lesson when that is pedagogically justified. Do not create artificial lessons to make chapter sizes uniform. Conversely, do not retain an oversized page merely because it currently occupies one route slot.

The linear path must make the progression explicit: what the learner already knows, what this lesson adds, what they should be able to explain or do afterwards, and why the next lesson follows. Optional deep dives, exercises, code labs and historical material are linked from the relevant lesson but do not count toward its mandatory duration.

### 12.2 Lesson-level acceptance contract

A lesson is ready for the main path only when it has:

- one central question, stated in learner-facing language;
- one observable learning outcome, expressed with an action verb;
- prerequisites supplied by earlier lessons or explicitly marked as optional;
- one continuous explanation that answers the question without requiring another page;
- one worked example, diagram or calculation that operationalizes the idea;
- a short conclusion that states the acquired idea and motivates the next step;
- a credible mandatory-path duration estimate, accounting for prose, equations, diagrams and worked examples separately from optional material;
- a corresponding review companion and a separate practice destination where exercises exist.

A lesson should normally teach one principal new idea. Closely coupled sub-steps of one mechanism may remain together (for example, score calculation, normalization and value aggregation in one attention computation). Independent questions should not be bundled merely because they share a topic label.

### 12.3 First-pass size audit of the current French route

The following counts are a structural screening, not final reading-time estimates. They exclude YAML/front matter, editorial HTML comments and fenced code blocks, but still include some practice and optional sections. Actual duration must be measured after the mandatory path is separated from those sections.

| Current lesson | Approx. words | First-pass editorial decision |
|---|---:|---|
| Panorama | 2,038 | Keep as a special orientation, not a standard lesson; reduce the mandatory path to the first prediction loop and defer architecture/history/system material. |
| Texte et tokens | 1,277 | Keep; move embedded exercises and optional Unicode/tokenizer detail to their dedicated destinations. |
| Plongements | 1,073 | Keep as a short lesson; remove unrelated forward-looking material from the core argument. |
| Position | 1,370 | Keep the reason for position and the core mechanism; move exercises and geometric derivations out of the mandatory path. |
| États contextualisés | 1,414 | Keep; ensure it compares initial and contextualized states without trying to teach the Transformer mechanism itself. |
| Transformer | 3,107 | Split or substantially narrow. Candidate boundary: (a) the Transformer block and its sublayers; (b) the forward pass and how a stack produces final states/logits. Historical 2017 architecture material remains a separate optional/history destination. Confirm the boundary against the actual explanations before moving content. |
| Q/K/V | 1,470 | Keep as one focused lesson on the three projection roles; move exercises and advanced variants out of the mandatory path. |
| Attention | 2,043 | Keep the single-query computation as one lesson; move exercises, Build material and FlashAttention out. Reassess whether the five calculation steps fit 15 minutes with the diagram. |
| Masque causal | 1,680 | Keep as one lesson if its mandatory path stays focused on visibility and the causal constraint; move comparisons of other masks to optional material. |
| Logits | 1,138 | Keep as a short lesson. |
| Probabilités | 1,597 | Keep logits-to-distribution and conditional interpretation; separate extended temperature exploration and additional examples from the mandatory path. |
| Entropie | 1,924 | Keep predictive entropy and its distinction from observed-token score; move compression and V-information to optional deep dives. |
| Génération | 2,858 | First transfer serving/scheduling, latency details, exercises and implementation links to their proper destinations. Keep the core autoregressive loop plus conceptual prefill/decode together if the rendered lesson then fits 15 minutes; split only if the remaining material still contains two independent learning outcomes or exceeds the limit. |
| In-context learning | 1,009 | Keep as a short lesson. |
| Ingénierie du contexte | 1,531 | Keep the design principles and one worked example; move extended RAG/memory material to linked lessons if it exceeds the time budget. |
| Vraisemblance | 1,088 | Keep as a short lesson on scoring an observed sequence and teacher forcing. |
| Entropie croisée | 2,463 | Narrow first: retain the per-token objective, one worked example and the observed-target distinction; merge the sequence-level perplexity explanation into the likelihood lesson, move the KL derivation to `language-modeling-math`, the gradient bridge to `gradients`, implementation details to Build/Deepen, and exercises to Practice. Split only if the remaining single outcome still exceeds 15 minutes. |
| Loss | 1,472 | Keep the aggregation over valid shifted targets and the distinction between attention and loss masks; keep teacher forcing only to the extent needed to explain the observed prefix. |
| Gradients | 1,581 | Keep as one lesson from local derivatives to a parameter update; move extended calculus/optimizer variants out. |
| Boucle d’entraînement | 2,627 | Narrow first: keep one coherent update, repeated batches and the train/validation distinction; move implementation/workflows to Build and detailed optimizer comparisons to Deepen. Reassess the rendered duration before deciding whether one-step and repeated-optimization explanations need separate lessons. |

**Baseline note:** the word counts in this first-pass table are a pre-migration snapshot, not a current inventory or a reading-time estimate. Use the section-level decisions and dated source audits in `lesson-migration-ledger.md` for the current state.

### 12.4 Candidate chapter structure

These are conceptual chapter groupings, not a commitment to preserve the current nine stage boundaries unchanged:

1. **Voir ce que prédit un LLM** — orientation/panorama.
2. **Transformer le texte en entrée** — texte, tokens et identifiants.
3. **Construire les représentations** — plongements, position, états contextualisés.
4. **Comprendre le calcul du Transformer** — architecture du bloc, passe avant, Q/K/V, attention, causalité.
5. **Produire une distribution prédictive** — logits, softmax/probabilités, entropie.
6. **Générer une continuation** — boucle autorégressive, puis prefill/decode et cache KV.
7. **Concevoir le contexte** — in-context learning et ingénierie du contexte.
8. **Évaluer une séquence observée** — vraisemblance, entropie croisée.
9. **Apprendre les paramètres** — loss, gradients, mise à jour et boucle d'entraînement.

The chapter order must reflect the intended first reading, not pretend that every chapter is a strict mathematical prerequisite of the next. Scoring and training are related uses of the predictive distribution; they should be explained as distinct branches, with a clear transition rather than a false dependency.

### 12.5 Required migration sequence

1. Measure the mandatory reading path of all current lessons in both languages using one documented method. Count optional sections, exercises, code walkthroughs and references separately.
2. Mark each section as core explanation, review aid, practice, optional deepening, implementation/Build, or history. Do not move material until its destination is explicit.
3. Approve the chapter/lesson map and the split/merge decisions before changing route IDs or navigation.
4. Pilot one oversized lesson (Transformer or Generation) in French and English. Validate that each resulting lesson stands alone and stays within 10–15 minutes.
5. Update `data/guided-route.yml`, lesson contracts, revision companions, practice links, metadata and both language sidebars from the same canonical decision. Do not create a second manually maintained route.
6. Check the complete learner experience: chapter introductions, lesson objectives, previous/next progression, review link, practice link, optional branches, responsive rendering and bilingual parity.

Do not treat a word-count threshold as an automatic split rule. Duration is an acceptance criterion; conceptual coherence determines the split boundary. Preserve all scientific qualifications, citations, diagrams and existing explanations through explicit moves or merges.


## 13. Knowledge-preserving migration ledger

The section-size audit and chapter proposal are now complemented by the section-level migration specification in [lesson-migration-ledger.md](lesson-migration-ledger.md). It records the 20-lesson/9-chapter target, first-pass dispositions for every core lesson, and detailed source-section decisions for the largest pages.

**Important refinement to the earlier split proposals:** transfer misplaced material first; split only after measuring the remaining coherent lesson. A large current page is not automatically two lessons. Conversely, do not compress two independent learning outcomes into one page merely to preserve the current page count.

The ledger now records three completed bilingual content pilots at source-text level. First, the full soft-target/KL derivation and its non-degenerate numerical example were consolidated in the existing language-modeling-math Deepen page, and the sequence-level perplexity definition was consolidated in the likelihood lesson. Second, the Transformer overview was narrowed to the forward pass; detailed block internals moved to contextualized-representations-advanced, architecture dimensions to tensors, and the 2017 diagram plus explanatory table to transformer-history. Its five guided-reading questions were moved to the existing Transformer Practice companion, with suggested answers. Third, the temperature equation, interactive explorer, worked calculations, decoding-flow figure and NumPy workbench were moved from the probability lesson to the existing decoding-strategies Deepen page. The probability lesson now focuses on the base conditional distribution; Generation and Entropy retain concise cross-links, and Practice points to the existing GE-F temperature exercise. The core cross-entropy lesson keeps the one-hot case and the mean cross-entropy/mean-NLL equivalence; the core Transformer lesson keeps the representations-to-logits path and concise block roles. Quarto rendering, local-link/anchor checks, learning-map/graph generation and automated Playwright desktop/mobile/keyboard review now pass for the three content pilots. Generated map-list, map-data and guided-route fragments have been refreshed; the CI freshness suite is being rerun. Rendered reading-time measurements and learner validation remain pending. Every other source section remains in place until its bilingual destination, exact anchor, contextual link and preservation checks have been verified. Exercises are transferred to Practice companions; implementation to Build; mathematical extensions and variants to Deepen; overlapping explanations to their canonical synthesis page. A destination must exist and be checked before the source is shortened.
