# Tokenization and embeddings — source-to-knowledge transferability pilot

**Date:** 2026-11-05  
**Workflow:** `docs/workflows/source-to-knowledge-validation.md` v0.1  
**Owning issue:** [#496](https://github.com/JM-Brun/llm-lab/issues/496)  
**Calibration case:** Q/K/V, completed in #492 / PR #494  
**New incremental source:** [TokCollate (Variš, Stephen & Libovický, ACL 2026)](https://aclanthology.org/2026.acl-demo.41/)  
**Source ID:** `varis-stephen-libovicky-tokcollate-2026`

## Executive result

The source-to-knowledge workflow transfers to this second concept collection **with adaptations but without a new registry, concept graph, learning route or skill**. The pilot discovered and inspected a genuinely new source, registered it, extracted six atomic contributions, compared them against the existing canonical bilingual tokenizer-evaluation pages and collection, and made item-level integration decisions.

The source's main incremental value is an operational example of a multi-stage evaluation system: it accepts already-tokenized files, computes intrinsic metrics, serializes results, and supports a separate interactive visualizer. It does not itself execute tokenizer inference in the paper's described version. This is complementary to the project's existing explanations of tokenizer metrics, but it does not justify a new page or implementation.

**Decision:** register and cite as an optional advanced reference; defer learner-facing changes and hands-on integration until the repository and live visualizer have been inspected. This is a completed source-to-knowledge pilot, not a completed software audit or learner study.

## 1. Scope and baseline reconstruction

The declared learner question is:

> How can tokenizers be compared across languages without collapsing compression, vocabulary overlap, intrinsic metrics, and downstream model quality into one score?

The existing canonical route remains:

`text and corpus → tokenizer → token IDs → embedding lookup → positional information → contextualized hidden states`.

Pages inspected directly:
- `site/en/tokenizer-design-evaluation.qmd` and `site/fr/tokenizer-design-evaluation.qmd`;
- `site/en/tokenization-strategies.qmd` and `site/fr/tokenization-strategies.qmd`.

The advanced bilingual page already distinguishes representation length, system cost and downstream quality; introduces reproducible comparison requirements; discusses multilingual tokenization metrics and TokLens; and explicitly warns that intrinsic metrics do not establish downstream quality. The core tokenization pages already distinguish tokenization stages and avoid treating fewer tokens as proof of better model quality.

Baseline evidence reused, not rescanned:
- #114 — tokenization and embedding source audit;
- #147 — Vizuara/ByteByteGo pedagogical assessment;
- #82 — text → token IDs → embeddings → contextualized states;
- #96 — Raschka Chapter 2 audit;
- #458 and #460/#463 — source registration and structured extraction migration;
- the existing source collection and migration map.

The pre-pilot `main` catalogue was counted directly at **47 source records** (four Q/K/V/KV-cache plus 43 tokenization/embeddings records). The pilot branch contains **48** after registering TokCollate. The collection dossier was reconciled to this current branch snapshot; neither count is treated as a completeness target.

## 2. Discovery and source inspection

### Discovery decision

The new source was identified through the ACL Anthology 2026 System Demonstrations proceedings as a tool-oriented contribution within the already-covered subdomain of multilingual tokenizer evaluation. It is not an alias or mirror of an existing source record. DOI and Anthology ID provide stable identity.

### Directly inspected scope

- ACL Anthology metadata page: title, authors, publication venue/date, pages, DOI and licence statement.
- Publisher-hosted proceedings PDF: all ten pages, including system architecture, input/output contract, metric definitions, language metadata, visualizer, use cases, case study, related work, limitations and configuration appendix.
- The paper screenshots/captions were inspected as part of the PDF text/context, but no source asset was copied or adapted.

### Explicitly not inspected

- GitHub implementation, dependencies, tests, sample data and release history;
- live visualizer interaction, keyboard/mobile behavior and accessibility;
- independent reproduction of metric outputs or the paper's case study;
- provenance and validity of all language metadata sources.

Therefore the source is **partially scanned**, despite full-text PDF inspection. The paper's statement that the code is MIT-licensed is not independently verified; the ACL Anthology states that the proceedings paper is CC BY 4.0. Paper and software rights are kept separate.

## 3. Extraction and evidence

Structured extraction: `data/extractions/varis-stephen-libovicky-tokcollate-2026.yml`.

Six atomic items were retained:

| Item | Contribution | Evidence boundary |
|---|---|---|
| Two-stage evaluation architecture | Pre-tokenized inputs → Python scoring → structured result files → separate visualizer | Paper-described architecture; implementation not run |
| Metric families | Monolingual and cross-lingual intrinsic measures | Tool inventory, not universal quality taxonomy |
| Cross-lingual metric distinction | Vocabulary overlap vs distribution divergence vs alignment and length ratios | Metrics answer different questions and require different data |
| Language metadata provenance | FLORES+, ISO codes, Glottolog, Wikidata, Joshi taxonomy, manual typology, FineWeb2 proxy | Composite lineage; some metadata manually reconciled |
| Intrinsic/extrinsic boundary | Tool implements intrinsic metrics and warns against treating them as downstream-quality predictors | Explicit limitation; does not invalidate every intrinsic metric |
| Educator use case | Interactive filtering, tables, correlations and tokenized-text comparison | Author-stated use case, not measured learning evidence |

Extraction preserves the source's claims, scope and limitations. It does not promote the paper's case study into a project benchmark or treat an author-stated educator use case as evidence of learning efficacy.

## 4. Cross-source comparison and item-level decisions

| Contribution | Existing canonical treatment | Decision | Rationale |
|---|---|---|---|
| Separate tokenizer execution from evaluation and visualization | Reproducible evaluation protocol exists, but this concrete tool architecture is not currently central | integrate-by-reference | Useful operational example; no second pipeline or implementation |
| Inventory of monolingual metrics | Advanced page already explains token count, fertility, compression and their limits | already-covered | A second catalogue would add length, not understanding |
| Distinguish cross-lingual overlap, distribution and alignment metrics | Existing multilingual metric discussion and TokLens reference | integrate-by-reference | Adds a useful methodological comparison for advanced readers; no new core section |
| Language metadata provenance and grouping | Not a prerequisite to the core learner route | defer | Too implementation-specific until a practical lab needs it |
| Intrinsic metrics do not guarantee downstream quality | Explicitly covered in the bilingual advanced page | already-covered | Reinforces a key caveat without changing it |
| Interactive educator use case | Existing optional visualizer references, but no independent usability test of TokCollate | link | Candidate for optional resource list only after live tool inspection |

**Best-of-sources finding:** TokCollate is not a stronger explanation of what tokenization is. It contributes a distinct *research workflow* perspective: input contracts, metric computation, data lineage, and interactive result exploration. This is complementary to the canonical explanatory route, not a reason to extend the beginner path.

## 5. Project integration decision

No canonical page, concept, route, exercise, figure or implementation was changed in this pilot.

- **Source catalogue:** one new stable record.
- **Extraction:** one source-scoped YAML file with six atomic items.
- **Concept graph:** no changes; existing `token` concept is sufficient.
- **Source graph:** no new concept graph; this is a system paper, not a tutorial with a learner sequence requiring a reconstructed pedagogical model.
- **Learning route:** no changes; tool usage is optional advanced practice, not a prerequisite.
- **Bilingual pages:** no changes; the comparison confirmed that the core distinction is already present in both languages.
- **Assets:** no copied figures; no rights inference from the software licence statement.

The integration choice is deliberately small: preserve the source as a traceable optional reference. A later page link is conditional on a separate implementation/live-interface check and a clear learner task.

## 6. Validation gates

| Gate | Result | Evidence / limitation |
|---|---|---|
| Source identity and provenance | pass | ACL Anthology metadata and DOI |
| Source inspection | partial | All ten PDF pages inspected; repository and live demo not inspected |
| Extraction fidelity | pass at paper-text scope | Six located items with evidence kinds, confidence, scope and caveats |
| Cross-source synthesis | pass | Compared against four bilingual canonical pages and the existing collection |
| Integration decision | pass | Item-level decisions; no-op justified against exact existing treatment |
| Schema and catalogue validation | pass | CI validator accepted the new catalogue and extraction records; branch catalogue count is 48 |
| Python CI | pass | Run 2094 succeeded, including pytest, Ruff, mypy and catalogue/extraction checks |
| Quarto site | pending at report cut-off | Run 2088 was still rendering; final status must be confirmed before merge |
| Rendered browser/accessibility review | not run | Not required for a no-page-change pilot; remains owned by #156 / #320/#329 for existing assets/pages |
| Independent learner validation | not run | No learning-effectiveness claim; use existing #447 only if a future learner-facing change warrants it |

## 7. Workflow scalability and effort

### What transferred cleanly

- Existing catalogue, taxonomy, extraction schema and stable-ID policy were sufficient.
- Existing extraction and integration skills covered the work without a new skill.
- The source could be added incrementally without rescanning the 43-source historical collection.
- The workflow correctly separated source inspection, extraction, synthesis, integration and learner evidence.
- A no-page-change outcome was possible without treating the source as useless.

### Friction and defects observed

1. **Snapshot drift:** the collection dossier and issue #458 report different catalogue totals. Counts must be generated from the validated tree and timestamped; narrative snapshots should not be maintained manually.
2. **Source-type nuance:** the source is a software/system demonstration paper, not a tutorial. The current schema supports it without forcing a pedagogical graph or learner route.
3. **Evidence-lineage gap:** the extraction schema can store corroborating sources, but this source's own metric descriptions cite other work. The pilot does not independently validate all those cited works; future synthesis must not count citation chains as independent corroboration.
4. **Operational effort is not yet measured:** the repository contains no trustworthy elapsed-time or active-human-time log for discovery, PDF inspection, extraction, comparison and validation. The PR provides a reproducible task boundary, but not a defensible hours estimate. Do not invent one.
5. **No execution-based validation:** because the tool repository was not inspected/run, the workflow has tested source-to-knowledge processing, not tool reproducibility.

### Effort measurement for the next source

Record active time by stage (discovery, source inspection, extraction, comparison, integration decision, validation), number of human review interventions, blocked/retry events, and automated checks. Exclude waiting time for CI unless it requires human intervention. Record actual values in the next pilot; do not infer them from file counts or number of tool calls.

## 8. Pedagogical quality: what this pilot can and cannot establish

This source's pedagogical contribution is an educator-facing interactive use case, but no learner sequence, task outcome or independent usability observation was collected. The pilot therefore evaluates *potential pedagogical affordance*, not effectiveness.

The contribution becomes testable only after a concrete activity is designed, for example:
- compare token count/fertility for the same fixed parallel text across two tokenizers;
- explain why vocabulary overlap and Jensen–Shannon divergence are not interchangeable;
- identify which metric requires parallel sentence pairs;
- explain why a good intrinsic score cannot alone establish downstream model quality.

A future formative check should score the learner's reasoning and transfer, not just correct recall of metric names. The existing #447 learner pilot is Q/K/V-specific and should not be repurposed without a deliberate scope decision; do not open a duplicate pilot.

## 9. Next actions

1. Confirm the running Quarto site workflow and post-render checks on the PR head; repair any failure before merge.
2. Reconcile the catalogue count only when further sources are registered; the current baseline (47) and pilot branch (48) are now recorded.
3. Inspect the TokCollate repository at a pinned commit and verify code licence, dependencies, metric implementation, sample data and tests before considering a practical link.
4. Open the live visualizer and inspect keyboard, mobile and accessibility behavior before recommending it as a learner tool.
5. If the tool is adopted for an activity, design a small task and test comprehension/transfer separately; no efficacy claim from the paper's educator use case.
6. Reconcile this report after #458 backfill closes; do not repeat the prior source scans.

## 10. Reproducibility

- New source: https://aclanthology.org/2026.acl-demo.41/
- DOI: https://doi.org/10.18653/v1/2026.acl-demo.41
- Paper-stated repository: https://github.com/ufal/TokCollate
- Canonical pages inspected: `site/en/tokenizer-design-evaluation.qmd`, `site/fr/tokenizer-design-evaluation.qmd`, `site/en/tokenization-strategies.qmd`, `site/fr/tokenization-strategies.qmd`.
- Existing method: `docs/workflows/source-to-knowledge-validation.md` v0.1.
