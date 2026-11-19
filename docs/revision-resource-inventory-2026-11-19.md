# Inventory of existing Understand and Build revision support

**Date:** 2026-11-19  
**Status:** read-only inventory; no revision content created or migrated.  
**Historical snapshot:** current revision-aid links and assessments are maintained in [revision-aid-inventory-2026-11-19.md](revision-aid-inventory-2026-11-19.md); the normative proposed relation model is in [revision-resource-contract.md](revision-resource-contract.md). This earlier document predates the typed page-aid pilot and must not be used as the current relationship inventory.  
**Repository:** `JM-Brun/llm-lab`  
**Current main inspected:** `8fc0b80cbcb7333720a42211e9119bbf0528763e`  
**Inventory implementation:** `site/tools/audit_revision_coverage.py`, introduced in PR [#1379](https://github.com/JM-Brun/llm-lab/pull/1379).  
**Machine-readable snapshot inspected:** CI run [#5888](https://github.com/JM-Brun/llm-lab/actions/runs/44567812323), artifact `revision-coverage-inventory-0e98372c76a6bf1e4b00f731a9e9654ce3fb06d9`, generated from commit `817048ecda141fbf256e42237dc1a4f34bf44a88`.

This document inventories existing material. It does not decide that every page needs a new sheet, and it does not claim that existing summaries are pedagogically sufficient. The proposed relationship model is documented in the [revision-resource contract](revision-resource-contract.md); its integrated-section target correction is under review in [PR #1391](https://github.com/JM-Brun/llm-lab/pull/1391).

## 1. Scope and snapshot validity

The CI inventory covers every published page whose canonical page metadata declares `destination:understand` or `destination:build`. It uses the published page index, `data/guided-route.yml`, `data/concepts.yml`, and `data/resources.yml`; it does not infer page identity or semantic relationships from filenames.

The report was generated on PR #1379's head commit. A comparison from that snapshot to the inspected current `main` shows subsequent changes to the two `score-centering` pages, which are outside the Understand/Build destination set; the route, concept, resource registries and the 62 in-scope page files were not changed in that comparison. The 62-page counts below therefore remain applicable to the inspected main snapshot. The report itself remains pinned to its source commit and must not be described as a freshly generated artifact for current main.

## 2. Published page population

| Destination | Total | French | English | Route membership |
|---|---:|---:|---:|---|
| Understand | 46 | 23 | 23 | 40 core memberships, 6 optional memberships |
| Build | 16 | 8 | 8 | No Understand route membership is inferred |
| **Total** | **62** | **31** | **31** | — |

All 46 Understand pages have a route membership in the snapshot: none is reported as unrouted. Membership counts are not page counts; the inventory retains multiple memberships if a page occurs in more than one stage.

Bilingual topic-count parity is structurally complete in this snapshot: 23 Understand topic groups and 8 Build topic groups each have one French and one English page. This says nothing by itself about semantic equivalence, translation quality or equivalent learning outcomes.

## 3. Existing material inside the 62 pages

### 3.1 Explicit integrated revision sheets in Build

Four page instances (two bilingual topic pairs) contain an explicitly labelled, structured revision-sheet callout:

| Topic | French page | English page | Existing content |
|---|---|---|---|
| Corpus preparation | `fr/corpus-preparation` | `en/corpus-preparation` | Provenance, traceable transformations, split design, tokenizer leakage, and handoff contract |
| Training examples | `fr/training-examples` | `en/training-examples` | Shifted input/target alignment, teacher forcing, windows/stride, causal vs loss masks, and tensor shapes |

These are **integrated page sections**, not separate Quarto pages or records in `data/resources.yml`. Their French and English versions are present. The Build walkthrough pages also contain worked answers, test explanations, exercises and collapsible details; those are useful learning material but were not counted as revision sheets merely because they use HTML `<details>/<summary>` elements.

No other Build page in the 16-page population was found to have an explicitly labelled revision-sheet callout in this scan.

### 3.2 Integrated recaps and retrieval prompts in Understand

A source scan of the 46 Understand page bodies identified:

- **35 pages** with an explicit one-minute mental-model recap callout (18 English and 17 French);
- **6 additional pages** with a distinct `Takeaway`, `Key takeaways`, `Key points` or `À retenir` section, beyond the recap pages;
- **20 pages** with a `self-check` block (10 English and 10 French).

These are three separate observations and may overlap. A recap is an integrated synthesis element; a self-check is retrieval practice; neither is automatically a complete companion revision sheet. The page bodies and their actual claims must be reviewed before these elements are classified as sufficient.

The six additional takeaway-section pages are the French and English counterparts of:
- `context-engineering`;
- `in-context-learning`;
- `queries-keys-values`.

The 35 recap callouts occur on the following page IDs:

**English (18):**
`en/causal-masking`, `en/contextualized-representations`, `en/cross-entropy`, `en/entropy`, `en/generation`, `en/gradients`, `en/likelihood`, `en/llm-limits`, `en/llm-overview`, `en/logits`, `en/loss`, `en/positional-encoding`, `en/post-training`, `en/probabilities`, `en/scaled-dot-product-attention`, `en/text-data`, `en/training-loop`, `en/transformer-architectures`.

**French (17):**
`fr/causal-masking`, `fr/contextualized-representations`, `fr/cross-entropy`, `fr/entropy`, `fr/generation`, `fr/gradients`, `fr/llm-limits`, `fr/logits`, `fr/loss`, `fr/positional-encoding`, `fr/post-training`, `fr/probabilites`, `fr/scaled-dot-product-attention`, `fr/text-data`, `fr/training-loop`, `fr/transformer-architectures`, `fr/vraisemblance`.

The count is based on explicit page-body callout/heading markers, not a semantic quality score. Pages without those markers may still contain concise explanations, worked examples, or practice material.

### 3.3 Existing dedicated revision-sheet pages outside the 62-page population

Two bilingual page pairs already exist elsewhere in the published site. They are not counted as Understand/Build pages because their page metadata assigns them to other destinations:

| Page pair | Destination / type | Content and current relationship evidence |
|---|---|---|
| `fr/revision-information-theory`, `en/revision-information-theory` | Practice / `exercise-collection` | Revises surprisal, entropy, cross-entropy, KL divergence and predictive coding. Its `related` metadata points to entropy, cross-entropy and experience-information-theory pages. |
| `fr/compression-revision`, `en/compression-revision` | Deepen / `concept-bridge` | Visual synthesis of predictive coding, entropy, model compression, runtime memory, empirical evidence and self-check. It is explicitly linked in the body of the French/English entropy and LLM-overview pages (six link occurrences across four source pages). |

These are existing revision resources worth retaining and reviewing. Their current `related` edges or body links are **not** typed revision-ownership relations. Do not count a generic related edge as proof that the page is the canonical revision companion for a lesson.

## 4. Existing concept and non-page resource associations

The generated inventory reports **162 explicit concept-to-page associations**:

| Destination | Associations | Pages with at least one concept |
|---|---:|---:|
| Understand | 144 | 46 / 46 |
| Build | 18 | 6 / 16 |
| **Total** | **162** | **52 / 62** |

These are concept links, not revision links. A concept association does not establish that a page has a synthesis, flashcards or a revision sheet.

The inventory also reports **10 page-to-implementation-resource associations** on Build pages. They correspond to five shared non-page resource IDs, each referenced by its French and English walkthrough:

- `gpt-config-module`;
- `gpt-ops-module`;
- `transformer-block-module`;
- `gpt-model-module`;
- `gpt-generation-module`.

These are implementation modules, not revision aids. The current `data/resources.yml` registry contains these five `kind: implementation` records only. The current resource validator does not admit a revision-resource kind, and no standalone flashcard set was identified in this registry or in the inspected page content.

## 5. Typed revision coverage: what is and is not known

The generated report marks all **46 Understand and 16 Build pages** as `synthesis_status: not_assessed`. This status is hard-coded by the current inventory generator because no typed source-page → revision-artifact relationship is implemented.

It must be interpreted as **the relationship has not been assessed under a typed contract**, not as:
- no summary exists;
- no revision material exists;
- the page is deficient;
- a new sheet must be created.

The source scan above finds integrated summaries, self-checks and existing companion pages that the current typed inventory cannot represent. Conversely, the presence of a recap or a self-check does not prove that the page has sufficient revision support.

No flashcard resource was identified in the canonical non-page resource registry or in the scanned page markers. This is an inventory finding, not proof that no informal or unindexed flashcards exist elsewhere.

## 6. Decisions for the next implementation stages

1. Preserve the current Understand/Build page identities, route memberships, concept links and implementation-resource links.
2. Treat integrated page sections, companion Quarto pages and non-page resources as distinct target forms in the revision contract.
3. Keep the two existing bilingual revision-sheet pairs visible as candidates; do not duplicate them by creating new pages.
4. Assess the four existing Build callouts against the editorial contract before deciding whether they are sufficient.
5. Review the 35 recap callouts, 6 additional takeaway sections and 20 self-check blocks as separate evidence categories; do not equate any marker with quality.
6. Do not create flashcards or new synthesis pages in bulk. First validate the contract and decide the appropriate lightest format page by page.
7. Keep `not_assessed`, `assessed` and `not_applicable` semantically distinct in all future reports.

## 7. Reproducibility and limits

The page counts, route memberships, concept associations and implementation-resource associations come from the JSON artifact produced by `site/tools/audit_revision_coverage.py` in CI run #5888. The page-body recap, takeaway, self-check and revision-sheet observations come from a read-only scan of the corresponding Quarto source files on the inspected current main snapshot.

This is a structural inventory, not a complete editorial evaluation. It does not judge the correctness, sufficiency, accessibility, freshness or learner effectiveness of any recap or sheet. It does not introduce a new registry, schema, validator rule, page field, graph edge or generated UI.
