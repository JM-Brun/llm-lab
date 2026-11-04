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

### Analogies and mental models

For each useful analogy, record source domain, target concept, mapped entities/relations, mechanism illuminated, valid scope, where the mapping breaks, likely misconception, suitable teaching location and source locator. An analogy never replaces a formal or computational definition.

### Figures and visual assets

Inspect the visual itself. Record creator, original URL, locator, caption/context, visual encoding, assumptions, omissions, accessibility, licence, permission and reuse status. Candidate actions: link original, embed with verified rights, create an independently authored explanation, or omit with rationale. Never trace or cosmetically alter protected figures. Phase B decides whether to update the site and asset register.

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
- Each retained item is atomic, traceable and scoped.
- Analogies, visuals, experiments, datasets and code have relevant metadata and rights/reproducibility status.
- Scanned, partial, linked-only, inaccessible and rejected sources are distinguished.
- Historical sources are reconciled when initialization is in scope.
- No pages or canonical graph structures were changed.
- The Phase B hand-off and unresolved questions are explicit.
