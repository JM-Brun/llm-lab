---
name: source-extraction
description: Inspect external articles, papers, documentation, repositories, datasets, experiments and visual sources; extract traceable structured claims, ideas, analogies and artifacts into the LLM Lab source catalogue without editing site pages or the canonical knowledge graph.
---

# Source extraction

## Mission and phase boundary

Produce a durable, machine-readable record of what a source actually contains and what may be useful to LLM Lab. This is **Phase A: extraction only**. Do not edit published pages, create pages, mutate `data/concepts.yml`, change graph relations, or regenerate graph projections. Candidate concepts and destinations are proposals for Phase B.

A scanned source may yield many independent items—or none worth integrating. Extraction is not endorsement or publication.

## Inspect repository conventions

Read the current graph standards and implementation audit, `docs/source-catalogue-schema.md`, `data/source-taxonomy.yml`, `data/domains.yml`, `data/sources.yml`, source/reference inventories, the pedagogical resource library, visual-asset register, existing source audits, validators and related skills. Use `data/sources.yml` as the canonical source catalogue and `data/extractions/<source-id>.yml` for atomic extraction records. Do not create a parallel catalogue, overload implementation-oriented `data/resources.yml`, create another concept registry, or hand-maintain JSON-LD. Keep records compact; link large artifacts to canonical files.

## 1. Identify and register each source
### Classification contract: themes, tags and metadata

Use the canonical contract in `docs/source-catalogue-schema.md` and controlled values in `data/source-taxonomy.yml`.

Every selected source must have one `classification.primary_theme` from `data/domains.yml`; add `secondary_themes` only for materially covered domains. A discovered but not yet classified source may leave the primary theme null. Do not create another domain taxonomy.

Keep these dimensions distinct:
- `tags`: sparse, namespaced retrieval facets (topic, method, modality, application, ecosystem), not concepts or scientific assertions;
- `concept_ids`: references to existing canonical concepts in `data/concepts.yml`;
- typed metadata: `source_type`, BCP 47 `language`, `technical_level`, `contribution_types`, `audiences`, scan/integration statuses, dates, versions and rights.

Do not add a generic `meta_tags` field or encode typed metadata as tags. Do not duplicate domain IDs or concept IDs in tags. Item-level classification may refine source classification but must not silently rewrite it. Avoid copying inherited source tags into every extraction item.


Record a stable language-independent ID and, where known:
- title, author/creator/organization, source type;
- canonical URL, DOI, repository identifier, publisher/venue;
- publication date, update date, access date, language;
- version, release, commit or archived edition;
- licence and separate text/figure/code/data reuse status (unknown is valid);
- scan status: `discovered`, `selected`, `scanned`, `partially-scanned`, `inaccessible`, `superseded`, `rejected` (or established equivalent);
- exact scope inspected: pages, sections, PDF pages, figures, appendices, code paths, commits, notebooks, supplementary files;
- access limitations, quality/evidence assessment, primary/secondary status and last verification;
- links to audit notes, PRs, issues and related existing concept/page/resource IDs.

A homepage visit does not mean the whole site was scanned. Register exact pages examined. Deduplicate by DOI, normalized canonical URL, or repository plus pinned revision—not title alone. Preserve mirrors, aliases, distinct editions and rescans; do not overwrite scan history.

## 2. Inspect and verify

Read beyond the abstract, introduction, README or conclusion. Inspect relevant equations, tables, figures, appendices, supplementary material, linked primary sources, code and tests.

Record the retrieval channel for each inspected artifact: direct canonical page, publisher API/feed, author-controlled mirror, repository source, or search index. Search-index text is useful for discovery and partial extraction, but it is not direct page retrieval; label it explicitly, retain the index/mirror limitations, and do not promote a source to `scanned` when intended content or media remains uninspected. If a mirror or profile snapshot conflicts with current indexed metadata, record the discrepancy and prefer neither silently.

Assess according to source type:
- research: methods, assumptions, data, supplementary material, replication and later critique;
- APIs/implementation: official documentation and pinned source;
- empirical claims: protocol, dataset, baselines, metrics, uncertainty and reproducibility;
- educational material: correctness, scope, clarity and supporting references.

Distinguish proof, measurement, empirical association, illustrative example, design choice, opinion, hypothesis and undocumented assertion. Preserve disagreement and limitations. Do not infer behavior from names or README claims when source/tests are available.

## 3. Extract atomic structured items

Give every item a stable ID within its source and make it independently routable. Controlled kinds include:
- knowledge: `claim`, `definition`, `mechanism`, `derivation`, `assumption`, `result`, `limitation`, `counterexample`;
- pedagogy: `analogy`, `mental-model`, `teaching-sequence`, `question`, `misconception`;
- media: `figure`, `diagram`, `animation`, `visualization`;
- practice/engineering: `experiment`, `benchmark`, `dataset`, `code-example`, `implementation-pattern`;
- editorial proposals: `page-improvement`, `new-page-proposal`, `cross-link`, `open-question`.

Each item records, as applicable:
- concise original synthesis (not copied prose);
- precise locator: section, page, timestamp, equation, figure/table, code path plus commit, notebook cell or dataset ID;
- evidence kind, confidence (`established`, `well-supported`, `context-dependent`, `disputed`, `speculative`, `unverified`), scope and assumptions;
- limitations, caveats, counterevidence and what the source does not establish;
- learner difficulty addressed and potential pedagogical value;
- candidate concepts/pages/resources/experiments and proposed destination (proposal only);
- links to related extracted items;
- optional `pedagogical_assessment` with independent levels and rationales for novelty, complementarity, pedagogical value, applicability, redundancy and evidence quality (required for pedagogical contributions and proposed learning improvements; see `docs/source-catalogue-schema.md`).

Do not collapse a paper's observation into a universal fact. Do not copy substantial passages; synthesize and preserve technical terminology only where necessary.

## 3a. Compare value, not just topic novelty

A source can cover a concept already present and still improve the project through a different explanatory route. Do not use topical overlap as a proxy for redundancy, and do not decide that an item is uninteresting merely because its destination page already exists.

For each potentially useful item, assess these dimensions independently (qualitatively, with a short rationale; never collapse them into one score):

| Dimension | Question |
|---|---|
| novelty | Does it add a fact, distinction, derivation, caveat, result or implementation detail absent from the project? |
| complementarity | Does it offer a genuinely different mental model, analogy, sequence, example, perspective, framing or connection? |
| pedagogical_value | Does that difference address a learner difficulty, misconception, abstraction barrier or missing intuition? |
| applicability | Can it be used meaningfully in a page, route, glossary, visual, activity, experiment or implementation? |
| redundancy | How much does it repeat existing content or an existing explanation, rather than merely sharing its topic? |
| evidence_quality | How reliable, precise and inspectable is the source for this particular contribution? |

Use low, moderate, high or uncertain for each level and add a concise rationale. Uncertain is preferable to guessing. For factual claims, evidence quality concerns correctness/support; for analogies and examples, assess whether they are clearly presented and appropriately bounded.

When comparing with LLM Lab, identify the exact existing page/section and compare the explanatory function: learner question, mental model, example, sequence, level, caveats and likely misconceptions. A new analogy on an already-covered topic is not automatically redundant; nor is it automatically valuable. Record what it illuminates that the existing explanation does not, and where it may mislead.

Keep useful alternative perspectives in the extraction record even when Phase B decides not to publish them. Phase A should preserve options, not prematurely filter for novelty.

### Extract for compilation across sources

Assume most useful sources will overlap with the project's subject matter. The purpose of a source collection is to build a traceable compilation of complementary explanations, not to find one supposedly novel source and discard the rest. For each pedagogically relevant item, capture a compact pedagogical_profile in the extraction record when it is a candidate for later synthesis: learner_question, explanatory_lens, teaching_form, abstraction_level, prerequisites, distinctive_value and limitations (see docs/source-catalogue-schema.md). Also record the exact locator. Keep values source-grounded and concise; do not force unique labels. Do not force every source into a unique perspective. Record useful convergence and meaningful disagreement, but keep source-specific claims distinguishable. Phase A records ingredients and provenance; it does not merge them into an unattributed composite. Flag groups of items that may warrant cross-source synthesis.

## 4. Capture teaching contributions

### Reconstruct the source's pedagogical graph and route

For a tutorial, article, course, chapter or other instructional source, do not stop at extracting isolated claims. Reconstruct its **local learning model** as a review artifact:

1. Identify the source's nodes: durable concepts, computational objects, operations, intermediate representations, examples, learner questions, activities and outcomes. Distinguish technical entities from pedagogical anchors.
2. Identify typed relationships: transforms, produces, uses, aggregates, constrains, is part of, motivates, illustrates, contrasts with, and any genuine prerequisite. Do not turn section order or an illustrative analogy into a semantic dependency.
3. Reconstruct the teaching route: section order, explicit and inferred learning outcomes, assumed prerequisites, transitions, worked examples, checks/practice, optional depth and omitted topics. Label inferred outcomes and edges as inferred, not author-declared.
4. Persist the reconstruction in a top-level `pedagogical_model` block in the source's extraction YAML: source-local graph nodes/typed edges, ordered teaching route, declared versus inferred outcomes/prerequisites, strengths, limits and comparison-dossier pointer. Use Mermaid in the review dossier as a human-readable view of that structured record; do not create a second canonical concept registry or a parallel graph database.
5. Keep the source model separate from the LLM Lab model. Phase A records the source's own structure and proposes candidate concepts/relations/destinations; Phase B compares it with the current canonical graph and route.
6. Record source-specific strengths and limits: what the route makes easy to understand, what it assumes, what it compresses, and what it does not teach.

The comparison must distinguish three structures:
- **semantic knowledge graph**: what entities/concepts exist and how they relate;
- **pedagogical route**: the sequence and scaffolding used to learn;
- **site navigation/hierarchy**: how readers discover and move between resources.

These structures can inform one another but are not interchangeable. A source may reveal missing graph nodes without warranting a route change, or offer a better local explanation without changing either canonical structure.


### Analogies and mental models

For each useful analogy, record source domain, target concept, mapped entities/relations, mechanism illuminated, valid scope, where the mapping breaks, likely misconception, suitable teaching location and source locator. An analogy never replaces a formal or computational definition.

### Figures and visual assets

Inspect the visual itself—not only its surrounding prose or an indexed text extract. Record creator, original URL, exact locator, caption/context, visual encoding, assumptions, omissions, accessibility, licence, permission and reuse status. Candidate actions: link original, embed with verified rights, create an independently authored explanation, or omit with rationale. Never trace or cosmetically alter protected figures. Phase B decides whether to update the site and asset register.

#### Visual-first inspection checkpoint

For every article, tutorial, course page or paper with a visual component, perform a separate media pass after the textual pass:

1. Enumerate the cover/hero image and every in-body image, diagram, chart, animation, video and linked visual. Distinguish a decorative thumbnail from an explanatory figure; do not assume the cover image is the figure the author discusses.
2. Resolve each asset to its original media URL and record its exact article locator (caption, section, figure number, or DOM order). Preserve redirects and mirrors as provenance, not as proof of authorship.
   - Use a retrieval ladder when the page renderer is inaccessible: canonical article HTML/metadata, the publisher's documented API or RSS/JSON endpoint, then a confirmed author-controlled mirror. Record which route yielded each asset. A mirror's cover thumbnail, search-result thumbnail, or repeated alt text is not proof that it is the in-body figure; compare article identity and figure placement before treating assets as equivalent.
3. Open the actual media at readable resolution. Inspect labels, arrows, grouping, reading order, visual hierarchy, mathematical notation, dimensions, colour dependence, cropping and mobile legibility. If the media cannot be retrieved or rendered, mark it **not visually inspected**; do not infer its content from alt text, a filename, a thumbnail, or the surrounding paragraph.
4. Evaluate the figure as a teaching artifact independently of the article: which learner question does it answer, what representation or relationship does it make visible, what prerequisite does it assume, what does it omit, and what misconception could it create? Compare that explanatory function with the exact current LLM Lab figure/page, not just the topic.
5. Record creator/rights-holder, source URL, licence evidence, permission and reuse conditions separately. A public image, an accessible CDN URL, attribution, or a permissive licence for article text does not automatically establish figure reuse rights. Unknown rights mean link-only or independently authored alternatives pending review—not automatic removal of existing material.
6. Keep the decision explicit: retain as a linked reference, embed unchanged only when rights are verified, commission/create an independently authored visual without tracing, or omit with a reason. For a promising but inaccessible visual, preserve a follow-up question and keep the source scan partial.

Do not silently treat a visual pass as complete because the article body was retrieved. The scan record and review note must state separately whether textual content, visual assets, linked resources and rights were inspected.



### Community discussion and reader comments

Treat comments, replies, issue discussions and community annotations as **separate voices**, not as part of the primary author's source text.

- Record the speaker/role when available (author, reader, maintainer, reviewer), exact locator, date and thread context. Do not infer identity or expertise from a username.
- When the comment is embedded in another source, keep the parent article as the container but mark the item's `provenance.voice` as `reader-comment`; include `parent_source_id`, the exact comment locator, capture date and speaker only when explicit. Use the optional `verification` block for independent checks; do not place verifier conclusions in the comment's summary.
- Separate the primary work's claims from suggestions, corrections, questions and anecdotes introduced by commenters. An author's acknowledgement is not independent technical validation.
- Preserve potentially useful leads even when they are outside the article's scope. Mark them as community-derived and unverified until checked against an authoritative source, implementation or reproducible evidence.
- If a comment contains a substantive technical claim, assess it independently and, when it warrants extraction, give it a distinct item/provenance rather than attributing it to the article author. Register the underlying primary source separately if one is identified.
- Do not silently promote a comment into the article's extraction or use it to change the article's integration status. A comment may motivate a new research task without becoming evidence for the source's claims.
- When a comment compresses a mechanism, check for omitted steps and boundary conditions before reuse. Preserve the original statement as a lead, then record the technically precise interpretation separately.

### Experiments, benchmarks, datasets and code

For experiments, record question/hypothesis, independent/dependent/control variables, dataset, model/version, protocol, baseline, metrics, uncertainty, compute/hardware, expected interpretation and limitations. Use statuses: proposed, protocol implemented, run completed, independently reproduced. Never report source results as LLM Lab results.

For code, record repository, pinned commit/version, path, licence, dependencies, tests and whether executed. Distinguish intended, observed and test-guaranteed behavior.

## 5. Backfill historical scanned sources

When initializing the catalogue, search the repository for source audits, bibliographies, source inventories, page citations, figure registers, experiment reports, notebooks, datasets, code references and PR/issue discussions.

Classify each mention as demonstrably scanned, partially scanned, linked/cited only, discovered/recommended only, or unknown. Register every verifiably scanned source. Link audit notes instead of copying prose. Extract historical items only where evidence exists. A bare URL/title is not a completed scan.

Produce a reconciliation report: counts by status, duplicates/aliases, unlinked extractions, inaccessible sources and unresolved provenance/licence questions. Do not claim historical completeness until the repository-wide backfill has been counted.

## 6. Phase B hand-off

Provide:
1. source records with scope and scan status;
2. atomic extraction items with locators, evidence, confidence, scope and caveats;
3. candidate concepts, graph relations, pages, assets, experiments and cross-links;
4. rights/reproducibility constraints and unknowns;
5. a source-to-item index and summary.

Candidate graph nodes/edges must be marked as proposals. Reuse known IDs and relation semantics; do not mutate the canonical graph in Phase A.

## Definition of done

- Each scanned source has stable identity, provenance, scope, status and limitations.
- Items originating in comments or embedded community discussion preserve a distinct voice, parent-source locator and independent verification status; they are never silently attributed to the primary author.
- Each retained item is atomic, traceable and scoped.
- For instructional sources, the local concept/process graph and pedagogical route are reconstructed, or explicitly marked not applicable; inferred outcomes and edges are labelled.
- Analogies, visuals, experiments, datasets and code have relevant metadata and rights/reproducibility status.
- Scanned, partial, linked-only, inaccessible and rejected sources are distinguished.
- Historical sources are reconciled when initialization is in scope.
- No pages or canonical graph structures were changed.
- The Phase B hand-off and unresolved questions are explicit.
