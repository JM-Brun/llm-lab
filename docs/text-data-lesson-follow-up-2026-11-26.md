# Text-data lesson — implementation follow-up and remaining work

**Date:** 2026-11-26  
**Scope:** `site/{fr,en}/text-data.qmd`, its revision sheets, Practice links, generated learning-map artifacts, and the tokenization/embedding source corpus.  
**Related:** [PR #1713](https://github.com/JM-Brun/llm-lab/pull/1713), [issue #1492](https://github.com/JM-Brun/llm-lab/issues/1492), [issue #1319](https://github.com/JM-Brun/llm-lab/issues/1319), [issue #584](https://github.com/JM-Brun/llm-lab/issues/584).

## 1. Purpose and editorial contract

The lesson is the Understand entry point for the representation chain:

`text → tokens → vocabulary entries / IDs → initial embedding lookup`.

It should let a learner explain what the model receives, distinguish a token from its ID and its initial vector, compare tokenizers on a fixed input, and understand why the tokenizer must match the model weights.

The lesson is not the place to teach every segmentation algorithm, corpus preparation, training-window construction, or the full empirical evaluation of tokenizers. Those responsibilities remain separate:

| Learning space | Canonical responsibility |
|---|---|
| Understand | `text-data`: text → tokens → IDs → initial lookup |
| Deepen | `tokenization-and-tokenizers` hub, then Unicode, segmentation strategies, tokenizer design/evaluation |
| Build | corpus preparation, tokenizer fitting, training examples and targets |
| Practice | dedicated `exercises-text-data` collection |
| Revision | concise retrieval and conceptual checks in `revision-text-data` |

The hub and specialized pages are the canonical destinations for detailed explanations. Avoid reintroducing a second, collapsed explanation of Build in the main lesson.

## 2. Work completed in PR #1713

The PR makes the following bilingual changes:

- Removes a repeated “two uses, two paths” paragraph from the supplementary section while preserving its historical anchor.
- Strengthens both revision sheets with three explicit checks: same-ID initial lookup, prompt encoding versus tokenizer fitting, and the interpretation limits of token count.
- Adds direct links from the revision sheets to the lesson, Practice collection and Deepen hub.
- Corrects Practice destinations to the actual `exercises-text-data.qmd` page (the former `exercises/text-data.qmd` path did not resolve).
- Refreshes the French and English generated learning-map data to include the new revision headings.

The revision checks state the necessary conditions: same ID retrieves the same embedding row at fixed parameters; later contextualized states may differ; prompt encoding uses an already fixed tokenizer; token count alone does not establish downstream quality.

No new source ingestion, concept taxonomy, page family, CI workflow or parallel registry is introduced.

## 3. Source and knowledge base — current evidence boundary

The living dossier is [Tokenization and embeddings — cross-source synthesis](source-reviews/tokenization-embeddings-source-collection.md). Its 2026-11-26 snapshot records 32 explicit collection memberships, 12 extraction files and 45 atomic items, joined through `extraction.source_id → source.id → source.collections`. The repository-wide snapshot records 150 source records, 112 extraction files, 552 atomic items and 125 canonical concepts.

These are inventory counts, not measures of completeness, evidence strength or learning outcomes. Do not revive the superseded 2026-11-19 counts or infer source membership from tags, filenames, citations or topic similarity.

The existing synthesis distinguishes instructional resources, implementations, documentation and empirical research. Preserve its boundaries: source inspection may be partial; a cited source is not automatically proof for every page claim; experimental token efficiency is not equivalent to downstream quality.

## 4. Remaining work — ordered and testable

### P0 — close PR #1713 safely

- [ ] Confirm all required CI checks pass on the final PR head. The initial failure was stale generated map data for the new revision headings; the two locale artifacts have now been refreshed.
- [ ] Confirm the Quarto/browser audit validates all internal links, especially the Practice destination and the FR/EN lesson ↔ revision ↔ Deepen navigation.
- [ ] Review the rendered pages at desktop and mobile widths. Check heading hierarchy, supplementary-section behavior, language switch and the visual density of the revision sheet.
- [ ] Verify the GPT-2 examples and the transition to `embedding-space`: French final ID `5633`, English final ID `30`; ensure each is interpreted only with the matching tokenizer and vocabulary.
- [ ] Confirm generated learning-map artifacts are reproducible from the authored pages; do not hand-edit generated output again after this refresh.

### P1 — validate pedagogical adequacy

- [ ] Run a short learner pilot without coaching. Ask the learner to reconstruct text → tokens → IDs → lookup and explain what changes when the tokenizer changes.
- [ ] Check transfer questions: why an ID is not a magnitude or coordinate; why the same ID has the same initial lookup but can yield different contextual states; why fewer tokens do not prove better quality.
- [ ] Compare the FR and EN pages side by side for conceptual equivalence, not literal translation. Verify examples, IDs, claims, anchors and destinations.
- [ ] Recheck the `revision_support` metadata against the actual revision sheet and its stable anchors. Update only if the evidence no longer supports `integrated_sufficient`.
- [ ] Verify every claim that was strengthened in the revision sheet against the existing source dossier and canonical embedding pages. Add claim-level provenance only where a real evidence gap is found.

### P1 — source and concept traceability (broader #1319 work)

- [ ] Audit the 12 extraction files / 45 items currently assigned to this collection for source lineage, locator quality, idea types, limitations and integration disposition. This is a source-by-source triage, not a target count.
- [ ] Reconcile candidate tokenizer concepts against `data/concepts.yml`: decide whether each candidate is a concept, a specialization, a computation operation, an attribute or merely terminology. Do not create one concept per technical term.
- [ ] Validate the typed subgraph and the actual FR/EN page coverage. Keep semantic relations, computational operations and pedagogical prerequisites in their respective canonical models.
- [ ] Update the locator/provenance audit to the current extraction inventory; the older report does not validate the newer 12/45 snapshot.

### P2 — optional extensions, only when justified

- [ ] Add a reproducible byte-level worked example only if it clarifies a gap not already covered by the Unicode and tokenizer-strategy pages.
- [ ] Add tokenizer implementation comparisons only where a behavioral difference matters to the learner; pin package/model revisions and preserve exact input/output evidence.
- [ ] Extend flashcards or exercises only after learner-pilot results identify a concrete retrieval or transfer gap.

## 5. Acceptance criteria

The work is complete when:

1. The core lesson remains concise and teaches the representation contract without duplicating Deepen or Build.
2. The bilingual revision sheets reinforce the essential distinctions and link to the correct Practice and Deepen destinations.
3. The generated learning-map artifacts are fresh and all required CI checks pass.
4. The GPT-2 example transitions are verified against the matching tokenizer and embedding vocabulary.
5. A learner can reconstruct and explain the chain without relying on memorized terminology alone.
6. The source, claim, concept, page and exercise links remain traceable without inferring evidence or prerequisites from proximity.

A green CI is necessary for the repository changes, but it does not demonstrate learner understanding. Record technical validation and learner validation separately.

## 6. Handoff for the next session

Start with PR #1713 and its latest checks. Do not repeat source ingestion or rebuild the tokenization hub. After merge, continue with the P1 learner pilot and the targeted provenance/concept audit under #1319. Treat the broader corpus backlog as separate from closing the lesson PR.
