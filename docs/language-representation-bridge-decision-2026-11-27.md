# Decision record — add a motivation page before text-data

**Date:** 2026-11-27  
**Status:** bilingual lesson drafted and added to the Understand route; awaiting CI and rendered-page review  
**Scope:** Understand route, bilingual page architecture, page metadata, concept graph, guided-route projection, and the boundary with the existing `text-data` lesson.

## 1. Decision to evaluate

The preferred direction is to add a short conceptual bridge immediately before `text-data`, rather than expanding `text-data` into a combined motivation-and-procedure lesson.

The two pages have distinct jobs:

- **Why represent language numerically?** explains the problem and motivation: why a neural model needs a numerical representation, why token IDs alone are insufficient, what learned vector representations make possible, and why context-dependent transformations matter.
- **Text and data (`text-data`)** explains the concrete input path and how it works: text, tokenizer, tokens, vocabulary, IDs, the tokenizer/model compatibility contract, and the transition to the initial embedding lookup.

This preserves the current `text-data` lesson's deliberately bounded scope and avoids duplicating the tokenization deep dives or the embedding-space lesson.

## 2. Recommended conceptual framing

The central teaching statement should be:

> **A language model needs a representation of language that its numerical machinery can compute with. Discrete symbols are first identified as tokens; their IDs provide stable indices, while learned vectors provide numerical representations that can be transformed and combined. Through these operations, the model learns and uses patterns and contextual relationships in language.**

A shorter recurring formulation for the course:

**Represent → compute → transform → learn → predict.**

This is a high-level explanatory lens, not a literal execution graph or a replacement for the canonical computational spine.

### Scientific precision to preserve

The new page must distinguish at least four things:

1. **Text and linguistic symbols:** human-readable strings and discrete units.
2. **Token IDs:** integer labels in a tokenizer-specific vocabulary. Their numerical magnitude, difference, or ordering has no inherent semantic meaning.
3. **Initial embeddings:** learned vectors selected using token IDs. Their geometry can encode useful statistical regularities, but is not a hand-written semantic ontology.
4. **Contextualized representations:** states produced by model computation. They depend on the occurrence's context and architecture, rather than being fixed properties stored in the tokenizer or a single embedding row.

Numerical representation makes mathematical operations possible; it does not mean that every linguistic relation is explicitly represented by one coordinate or that vector similarity is equivalent to understanding. Attention scores, weighted aggregation, projections, residual transformations and MLPs are operations over learned representations. The page may preview these ideas, but their mechanisms belong to the later canonical lessons.

### Suggested motivating example

Use a small contrast that can be revisited later:

- Show that arbitrary IDs assigned to *cat* and *dog* cannot be compared semantically by subtracting the IDs.
- Introduce the idea that an embedding table maps each ID to a learned vector.
- Preview that the model can transform and combine vectors, and that the representation of an occurrence can change with context.
- Use an ambiguous token such as *bank* only to motivate contextualization; do not claim that the embedding table stores a separate fixed vector for each sense.

The example should be explanatory, not a second worked tokenizer trace. Keep the existing localized GPT-2 trace in `text-data`.

## 3. Proposed page contract

| Dimension | Recommendation |
|---|---|
| French title | Pourquoi représenter le langage numériquement ? |
| English title | Why represent language numerically? |
| Stable page IDs | `fr/language-representation`, `en/language-representation` |
| Quarto sources | `site/fr/language-representation.qmd`, `site/en/language-representation.qmd` |
| Editorial type | `concept-lesson` (reuse the existing type; no new page archetype) |
| Destination | `understand` |
| Topic | `language-representation` (shared by both languages) |
| Level | `overview` |
| Status | `planned` until both pages are ready; then `published` |
| Suggested route | `llm-overview → language-representation → text-data → embedding-space` |

The page is concise and motivating, not a new technical chapter. It should answer:

1. What makes raw text different from the numerical objects a neural network operates on?
2. Why are token IDs labels rather than meaningful coordinates?
3. What does a learned vector representation add?
4. What kinds of operations become possible over vectors?
5. Why must representations be transformed using context?
6. What will the next lessons explain concretely?

It should preview, but not teach in full: tokenization algorithms, embedding lookup implementation, vector geometry, attention, the Transformer block, logits, loss or optimization.

## 4. Alternatives considered

### A. Expand `text-data` with a long motivation introduction

**Advantages:** no new page or navigation node; direct continuity.

**Disadvantages:** weakens the existing page contract, mixes the problem ("why") with the procedure ("what/how"), makes an already detailed lesson longer, and risks duplicating embeddings and contextualization lessons.

**Assessment:** not preferred. A brief motivation paragraph may remain in `text-data`, but the full conceptual argument belongs before it.

### B. Add a separate page before `text-data` (preferred)

**Advantages:** clean separation of motivation and mechanism; explicit conceptual bridge from the LLM overview to the input representation chain; reusable page for the wider numerical-representation story.

**Costs:** bilingual content, route and navigation updates, page metadata, learning-map regeneration, and review of any lesson/revision/practice contracts triggered by core-route membership.

**Assessment:** best pedagogical fit, provided the page remains short and does not become an extra survey of embeddings or Transformer mathematics.

### C. Add a new guided-route stage

**Advantages:** the motivation becomes visible as a distinct stage in the route visualization.

**Disadvantages:** changes the current nine-stage route topology and stage-count assumptions for a page that is a bridge, not a new major computational phase. It could overstate the importance of the page and cause unnecessary changes to review-route projections and map layouts.

**Assessment:** not recommended initially. Put the bridge first in the existing `text-input` stage, before `text-data`. Reconsider a new stage only if learner evidence shows that numerical representation is a substantial independent learning milestone.

### D. Treat the page as a Deepen resource or optional reading

**Advantages:** lower impact on the core route.

**Disadvantages:** the motivation is foundational. Making it optional would leave the same conceptual gap for learners who follow the main path.

**Assessment:** not recommended. It belongs in Understand, with overview depth.

## 5. Impact on the existing metadata architecture

The current architecture already has the necessary distinct owners. No new registry, metadata field, relation vocabulary, domain, or graph family is justified by this change.

### 5.1 Page metadata and page graph

Add bilingual page-map records using the existing `LLM-LAB-PAGE-MAP v1` contract:

- Stable IDs: `fr/language-representation` and `en/language-representation`.
- Matching controlled tags: `type:concept-bridge`, `destination:understand`, `topic:language-representation`, `level:overview`, locale, and status.
- A concise `summary`, bounded `scope`, learner-centred `purpose`, and reciprocal `suggested_route` links.
- Keep `hierarchy.parents/children` empty unless the actual page content establishes conceptual containment. The fact that the new page precedes `text-data` is a route relation, not a parent-child relation.
- Use `related` for useful cross-links to `text-data`, `embedding-space`, and `contextualized-representations` where the page explains the connection.

Do not introduce `why`, `motivation`, `archetype`, or a new concept-list field into page metadata. The current `purpose` field already states the page's learning job; the page body carries the full motivation.

### 5.2 Concept registry: `data/concepts.yml`

The current registry already contains relevant canonical concepts, including `token`, `token-id`, `token-embedding`, and `contextualized-representation`. Reuse these IDs.

Do not create a concept for every word in the new page (e.g. "number", "vector", "calculation", "relationship"). Do not create a generic `numerical-representation` concept merely to mirror the page title: it risks becoming an overly broad bucket spanning IDs, embeddings, hidden states, logits and probabilities, which have different mathematical roles.

A new concept should be added only if source review and curriculum use establish a stable, reusable knowledge entity with a definition and typed relations that cannot be represented accurately by the existing concepts. If the page only motivates existing concepts, it need not own a new concept node.

The concept registry's `resources` field associates concepts with pages; it is not a prerequisite list or a claim of exclusive ownership. Add the new page to a concept's resources only where it substantively explains that concept, not merely because it mentions it. In particular, do not automatically attach the bridge to every concept it previews.

If a real semantic relation is missing, use only the relation vocabulary already documented in the concept registry. Do not add `motivates`, `enables`, `solves`, `encodes` or other proposed generic edges as a quick fix: the concept graph has a controlled typed vocabulary, and pedagogical motivation is not necessarily a scientific relation between two concepts.

### 5.3 Guided route: `data/guided-route.yml`

Keep the existing nine stages initially. In the existing `text-input` stage:

- Order the core pages as `fr/language-representation` then `fr/text-data`, and likewise for English.
- Update the stage title/objective/question/result so the stage first motivates numerical representation and then traces the concrete text-to-ID input path.
- Give the new page its own `conceptual_focus` entry keyed by `language-representation`. It should mobilize existing concepts that it genuinely uses and state an observable outcome; do not invent computational nodes for conceptual motivations.
- Keep `text-data`'s focus on the concrete text → tokens → IDs trace.
- Do not add a `lesson_contracts` entry automatically. First check whether the route generator treats every page in a stage as a core lesson requiring a synthesis/revision artifact. If so, satisfy that existing contract deliberately; otherwise keep the bridge outside the lesson-contract mechanism rather than creating a dummy revision page.
- Keep the Build path independent. The bridge explains why representations are needed; it does not introduce corpus preparation or tokenizer-training steps as Understand prerequisites.

The stage remains a group of complementary resources, not a hard prerequisite DAG. The ordered list is the suggested study sequence.

### 5.4 Computational graph: `data/computational-graph.yml`

No new computational operation is needed. The new page explains the motivation for existing operations; it does not add a new execution step.

Reuse the existing computational nodes for token IDs, embedding lookup, initial hidden states and Transformer computation in its conceptual preview only where the reader benefits. Do not add nodes such as "understand language", "represent meaning" or "discover relationships". Those are explanatory outcomes, not executable operations.

Keep the graph's existing operational edge vocabulary (`consumes`, `produces`, `combines`, etc.) separate from page navigation, pedagogical dependencies and concept semantics.

### 5.5 Learning map, navigation and generated artifacts

Expected downstream updates once the pages exist:

- Add both source files to the Quarto render configuration and the correct Understand navigation section.
- Regenerate, never hand-edit, `learning-map-data-fr.json`, `learning-map-data-en.json`, and any other generated route/page-map artifacts.
- Confirm the page graph shows the suggested route without a false hierarchy edge.
- Confirm the concept graph only shows genuine concept-resource associations and typed relations.
- Check the route skeleton, stage labels, page counters and generated guided-context includes for assumptions about one page per stage.
- Update the bilingual language switch and the links from the bridge to `text-data`; update `text-data`'s previous-page link to the bridge.
- Inspect mobile and desktop rendering, keyboard navigation, breadcrumbs and the Understand sidebar.

### 5.6 Revision and Practice

The bridge should not duplicate the existing `text-data` revision sheet or tokenizer exercises. It needs a small set of transfer checks only if it creates a distinct learning outcome, for example:

- Explain why token IDs cannot be treated as coordinates.
- Explain what an embedding adds beyond an ID.
- Distinguish an initial embedding from a contextualized representation.

Keep exercises on the separate Practice surface in accordance with the project's page-specific exercise convention. Whether a dedicated exercise hub is warranted should depend on the number and quality of useful activities, not on creating a page mechanically.

## 6. Boundary with `text-data` and downstream lessons

The new page owns the motivation and conceptual distinctions. The existing lesson remains the authoritative concrete walkthrough.

| Topic | Motivation bridge | `text-data` | Later canonical lesson |
|---|---|---|---|
| Why numerical computation is needed | Explain | Brief reminder | Mathematical foundations as needed |
| Discrete symbols and token units | Introduce | Explain operationally | Tokenization deep dives |
| Token IDs are arbitrary labels | Motivate | Demonstrate and verify | Embedding-space |
| Embeddings as learned vectors | Preview purpose | Show the ID-to-lookup transition | `embedding-space` |
| Vector geometry and similarity | Explain why useful, with caveats | Link only | `embedding-space`, `cosine-similarity` |
| Contextual representations | Motivate | Mention transition | `contextualized-representations` |
| Attention and weighted aggregation | Preview the need for operations | Do not teach | Q/K/V and attention lessons |
| Tokenizer pipeline and segmentation | Do not detail | Explain the concrete pipeline | Tokenization strategies / Unicode |
| Corpus preparation and tokenizer fitting | Exclude | Explicitly distinguish | Build path |

The bridge should end with a precise handoff: the next page shows how a text string is converted into tokens and tokenizer-specific IDs; the later embedding lesson explains how an ID selects a learned vector.

## 7. Validation and acceptance criteria

The change is ready only when all of the following hold:

1. A learner can explain why a neural model needs numerical representations before being shown the tokenizer mechanics.
2. A learner can distinguish token IDs from learned embedding vectors and explain why arithmetic on IDs is meaningless.
3. The learner understands that useful geometric structure is learned and task-dependent, not an inherent semantic coordinate system.
4. The learner can explain why initial embeddings and contextualized states are different.
5. The new page is a concise bridge, not a duplicate of `text-data`, `embedding-space`, or the Transformer lessons.
6. FR and EN versions are conceptually equivalent and have matching page metadata and route structure.
7. The page graph, concept graph and computational graph retain their separate semantics.
8. The existing route and lesson-contract validators pass; all generated artifacts are reproducible.
9. The Understand navigation, language switch, breadcrumbs, mobile layout and links are checked in the rendered site.
10. Any revision or Practice artifact is justified by a distinct learning outcome and follows its existing contract.

A passing metadata validator proves structural consistency, not that the conceptual bridge teaches well. Record learner validation separately.

## 8. Implementation sequence

1. Confirm the page contract and the boundary with `text-data`.
2. Draft the FR/EN pages with one motivating example and no duplicated tokenizer trace.
3. Add the page-map metadata and reciprocal suggested-route links.
4. Insert both pages before `text-data` in the existing `text-input` stage; update its bilingual objective and conceptual focus.
5. Inspect the lesson-contract validator and decide whether the bridge needs a revision artifact; do not assume.
6. Update Quarto render/navigation and regenerate map artifacts.
7. Run page metadata, concept registry, guided-route, learning-map and Quarto validation.
8. Review page/concept/computational graph projections independently.
9. Conduct a short learner transfer check before considering the design complete.

## 9. Existing decisions and documents preserved

This proposal is consistent with:

- `docs/text-data-lesson-follow-up-2026-11-26.md`: `text-data` owns text → tokens → IDs → initial lookup and must not absorb tokenizer deep dives or Build concerns.
- `docs/page-metadata-schema.md`: route order, conceptual hierarchy, related links, page tags and concept identity have distinct meanings.
- `docs/learning-path.md` and `data/guided-route.yml`: the Understand route is a projection of the curriculum; the route is not the computational graph or a strict prerequisite DAG.
- `docs/canonical-computational-spine.md`: input representation, Transformer computation and prediction are distinct levels; Q/K/V are internal to Transformer blocks.
- `docs/information-architecture.md`: page graph, concept graph, computational graph, source catalogue and reader-facing routes have separate canonical ownership.

This record recommends an architectural direction. It does not claim that either bilingual page, route, registry or generated map has already been changed.


## 10. Implementation order: model the learning job before writing the lesson

The first implementation increment is deliberately metadata-only. It creates the bilingual page sources with their page-map contracts and associates the planned pages with the existing canonical concepts they will introduce or connect:

- `token` and `token-id`: discrete symbols and tokenizer-local identifiers;
- `token-embedding`: the learned vector selected from the model's embedding table;
- `contextualized-representation`: the state produced by subsequent context-dependent computation.

The existing typed concept relations already express the important conceptual transitions: a token is represented by an ID and by an embedding; the ID is a prerequisite for the initial embedding; the initial embedding is a prerequisite for the contextualized representation. **Do not add a generic “numerical representation” concept or new relation type merely to name the motivation.** The bridge is a pedagogical explanation connecting existing scientific concepts, not necessarily a new ontology entity.

The page records use the existing `concept-bridge` type, `understand` destination, and `overview` level. This is more precise than `concept-lesson`: the page's editorial job is to connect the symbolic input to the numerical representations unpacked by the following lessons. `language-representation` is a page topic, not a new scientific domain. The page sources remain `status:planned`; they are therefore excluded from the published-page index and learning-map projection. They are not yet added to `site/_quarto.yml`, the active `suggested_route` edges of published pages, or `data/guided-route.yml`.

Only after the bilingual explanation is authored and reviewed should the next increment:
1. change the two page statuses to `published` and add both sources to Quarto's explicit render list;
2. connect `llm-overview → language-representation → text-data` in the published page-map routes and update reciprocal navigation where appropriate;
3. place the page before `text-data` inside the existing `text-input` stage, without creating a tenth stage, and update that stage's question/objective/result only if its new scope genuinely requires it;
4. regenerate and validate the learning-map projections, breadcrumbs, sidebars and bilingual navigation.

This staging prevents a planned page from becoming a broken published route or a partially visible graph node. It also keeps the canonical computational graph unchanged: the bridge explains why the existing numerical operations are useful; it does not add a computational operation or alter dataflow.


## 11. Current implementation and review state

The bilingual pages have now been authored and activated:

- `site/fr/language-representation.qmd`
- `site/en/language-representation.qmd`

Both use the existing `concept-bridge` type, `understand` destination, `language-representation` topic, `overview` level and `published` status. The type follows the page design system's definition: connect a concept to its prerequisites or applications. No new metadata vocabulary or schema field was introduced.

The page content follows the intended conceptual boundary:
- why neural computation uses numerical tensors;
- why token IDs are vocabulary-local addresses rather than semantic coordinates;
- how a learned embedding vector differs from its ID;
- why learned vector geometry should not be treated as an explicit semantic ontology;
- why contextualized states require later model computation.

The existing Understand stage `text-input` now includes the bridge before `text-data`. Its objective and overview question explicitly cover both motivation and input encoding. The stage count and topology are unchanged. The published page routes are now:

`llm-overview → language-representation → text-data → embedding-space`

The bilingual Quarto render list and Understand sidebars include the new pages. The reciprocal `suggested_route` links on the overview and text-data pages were updated. The canonical concept registry associations were retained and reused; no computational graph nodes or edges were added.

The existing core-route contract requires one synthesis companion for every core lesson. A dedicated bilingual recall sheet was therefore added at `revision-language-representation`, with a single retrieval question and a typed `revision_of` link. The new lesson contract requires `llm-overview`; `text-data` retains its existing `llm-overview` prerequisite. The suggested reading route places the bridge before `text-data`, but that order is not itself encoded as a hard prerequisite: the two concepts remain independently understandable. This preserves the distinction between route order and learning dependency, as well as the separation between main explanations and Practice/Review material.

### Remaining validation before merge

- Confirm the page metadata validator accepts both new records and the shared topic.
- Run the guided-route and learning-map generators; confirm the new focus references resolve to concepts whose resource lists include the bridge pages.
- Render both languages and inspect mathematical notation, the flow sketch, links, mobile layout, and Quarto previous/next navigation.
- Confirm the generated learning-map JSON and graph projections are reproducible; do not hand-edit generated artifacts.
- Check that the page remains an overview and does not duplicate the technical explanation in `text-data`, `embedding-space`, or `contextualized-representations`.

No CI success is claimed until those checks have actually run.
