# Language-representation bridge — remaining work

**Updated:** 2026-11-27 (after successful validation of PR head `a1f9fbdbbf2188d48a4ae8df64daeb2dc4aa28cd`)  
**Scope:** follow-up to the bilingual `language-representation` bridge and its current content refinement.  
**Current pull request:** [#1762 — explain why language needs mathematical representations](https://github.com/JM-Brun/llm-lab/pull/1762).

This is an implementation handoff, not a proposal to redesign the learning path. The nine-stage route, existing concept vocabulary, page archetypes, and canonical computational graph remain unchanged.

## 1. Current state

### Already implemented

The structural integration was merged in [PR #1754](https://github.com/JM-Brun/llm-lab/pull/1754) (merge commit `1138ad13ae34afd25178dadc177191b1155f7848`):

- bilingual `language-representation` pages in the Understand path, before `text-data`;
- bilingual review sheets under Practice/Review;
- existing `concept-bridge` metadata, `language-representation` topic, and `overview` level;
- links to the existing `token`, `token-id`, `token-embedding`, and `contextualized-representation` concepts;
- route, navigation, lesson-contract, and generated learning-map integration;
- no new concept, relation type, metadata field, domain, computational node, or route stage.

PR #1754 also passed a full test run at its validated head (832 passed, 1 skipped) and a bilingual desktop/mobile browser audit. Those results validate that earlier content revision, not the current copy in PR #1762.

### Current content refinement

PR #1762 is open. The current refinement changes the bilingual lesson, its two review sheets, the text-input outcome in `data/guided-route.yml`, and the corresponding generated learning-map data. It also updates this handoff and the architecture decision record.

Its pedagogical correction is important: the page's primary job is to explain **why language must be represented mathematically so a neural network can learn and exploit linguistic regularities**. The distinction between an ID, an initial embedding, and a contextualized state remains necessary, but it supports the broader explanation.

The current refinement also:
- clarifies that tokenizer units are not necessarily whole words;
- connects the embedding matrix to the learned vector and explains that backpropagation updates embedding parameters, not discrete token IDs;
- uses a distributional example to explain how usage contexts provide statistical evidence, without treating vector proximity as a complete definition of meaning;
- updates the bilingual review sheets so learners reconstruct the motivation and the role of the prediction objective, not merely recall that ID subtraction is meaningless;
- aligns the guided-route outcome with learned representations, linguistic regularities, prediction, and contextualization.

### Validation status — current PR head

**Validated head:** `a1f9fbdbbf2188d48a4ae8df64daeb2dc4aa28cd`  
**CI run:** [46033531255](https://github.com/JM-Brun/llm-lab/actions/runs/46033531255)  
**Quarto/browser run:** [46033531298](https://github.com/JM-Brun/llm-lab/actions/runs/46033531298)  
**Secret scan:** [46033531196](https://github.com/JM-Brun/llm-lab/actions/runs/46033531196)

| Check | Result |
|---|---|
| Python quality and domain checks | Passed |
| Full test suite | **841 passed, 1 skipped** |
| Python coverage | **98.27%** (required threshold: 90%) |
| Full Quarto render | Passed |
| Learning-map generation and controls | Passed |
| Knowledge-graph export | Passed |
| History timeline parity | Passed |
| Local links in rendered site | Passed |
| Browser review of bilingual lesson and review pages | Passed |
| Secret scanning | Passed |

The browser audit covered the FR/EN lesson and review sheets at desktop (1440×1000) and mobile (390×844) viewports. All four target pages returned HTTP 200; no horizontal overflow or unrendered math was reported. Each lesson rendered four math spans. Desktop Axe checks reported zero violations; all measured focus targets were visibly focusable. The browser report recorded `failures: []`.

Screenshots and the audit report are retained in workflow artifact `site-browser-review-8c0f10cfa450429585d7a5c8e305d2ed95e1198b` (artifact ID `15216131326`, expires 2026-12-27). These automated browser/accessibility results do not replace a learner transfer check with someone who has not studied the later lessons.

The earlier generated-map freshness failures on heads `9bc83e5` and `f4ba645` were corrected by synchronizing the FR/EN section inventories and review-sheet purpose values. The current generator, Quarto render, and full test suite pass on the validated head. Those historical failures are not open defects.

**P0 acceptance is met on the validated head.** If the branch changes again, rerun relevant checks on the new head before merging.

## 2. Remaining work — ordered by priority

### P0 — Complete validation of the current content

**Completed on validated head.**

- [x] Full Python quality/domain checks and test suite passed.
- [x] Full Quarto site render completed successfully.
- [x] Generated learning-map data, knowledge-graph export, timeline parity, and local-link checks passed.
- [x] Browser audit completed for both languages at desktop and mobile widths.
- [x] Both lesson pages and both review sheets returned HTTP 200, with no horizontal overflow or unrendered mathematical notation.
- [x] Desktop Axe checks reported zero violations; measured focus targets were visibly focusable.
- [x] Screenshots and browser audit report were saved as a workflow artifact.

**Evidence:** CI run `46033531255`; Quarto/browser run `46033531298`; secret scan `46033531196`. Exact metrics and artifact ID are recorded above.

### P1 — Align the learning contract and scientific precision

**Completed on validated head.**

- [x] Bilingual page-map `purpose`, `summary`, and `scope` match the revised opening and learning outcomes.
- [x] The `language-representation` outcome in `data/guided-route.yml` covers learned vectors, network transformations, linguistic regularities, prediction, and the distinction between IDs, initial embeddings, and contextualized states.
- [x] Bilingual review sheets ask learners to reconstruct the motivation for learnable numerical representations and the role of the prediction objective.
- [x] The lesson's `revision_support` evidence points to the existing `revision-summary` anchor; the FR/EN review-sheet `scope` and `purpose` are aligned.
- [x] The main lesson and review sheet preserve the same conceptual emphasis in French and English, with language-appropriate examples.
- [x] The integer table is explicitly simplified. Real tokenizer units may be words, word fragments, characters, or punctuation; a written word is not necessarily one token.
- [x] The distributional examples (`chat/félin`, `cat/feline`) are framed as evidence from comparable usage contexts, not as a guarantee that every next-token model places synonyms near one another.
- [x] The lesson rejects interpreting an embedding as a dictionary definition or its individual coordinates as readable semantic properties.
- [x] The contextualization example distinguishes a shared initial embedding from occurrence-specific contextualized states. The causal-model qualification limits accessible context to the prefix and current position.
- [x] The parameter-learning bridge states that gradients from the loss can update embedding-matrix rows and other network parameters; token IDs remain discrete indices and are not updated.

**Acceptance:** met. The lesson does not equate token IDs with semantic coordinates, vector proximity with synonymy or understanding, or an initial embedding with a contextualized state.

### P2 — Validate the pedagogical transfer

**Remaining work.** Automated tests establish structural consistency and rendering, not whether a learner has acquired the intended mental model. This is the only substantive pedagogical validation still open.

- [ ] Ask a reader who has not studied the later embedding/attention lessons to explain, in their own words:
  1. why assigning an integer to a word/token does not create a useful semantic geometry;
  2. what learned vectors make possible that an arbitrary ID does not;
  3. how prediction from usage can encourage useful representations without a hand-written dictionary of meanings;
  4. why an initial embedding is not yet a contextualized representation.
- [ ] Record misconceptions, ambiguities, or points of friction. Distinguish a genuine conceptual gap from unfamiliar terminology that belongs in a later lesson.
- [ ] Make only targeted revisions. Preserve the overview boundary and avoid adding technical detail already covered by `text-data`, `embedding-space`, or later Transformer lessons.
- [ ] If the lesson changes, keep the FR/EN versions, review sheets, metadata, route outcome, and generated map projections synchronized; rerun validation on the new PR head.

**Acceptance:** a learner can explain the motivation and the conceptual handoff to `text-data` without needing the technical detail reserved for later pages.

## 3. Explicitly out of scope

Do not use this follow-up to:

- add a tenth guided-route stage;
- create a generic `numerical-representation` concept or new concept relations;
- modify the canonical computational graph to represent pedagogical explanations;
- move tokenizer algorithms, embedding lookup implementation, attention, or Transformer mechanics into this bridge;
- merge the main lesson and its review sheet;
- create a new page archetype, metadata field, or parallel registry.

These would expand the architecture without being required to complete the current task.

## 4. Recommended execution sequence

1. Do not repeat the already-passing P0 work unless the branch changes. The current validated head is `a1f9fbdbbf2188d48a4ae8df64daeb2dc4aa28cd`.
2. Perform the short learner transfer check (P2) with someone unfamiliar with the embedding/attention lessons.
3. Record the reader's answers and misconceptions; make the smallest targeted changes, if any.
4. If changes are made, regenerate affected map projections and rerun tests, full render, and browser audit on the new head.
5. Review the final diff and workflow artifact, then make the merge decision. This handoff does not authorize an automatic merge.

## 5. Completion record

| Item | Result | Evidence |
|---|---|---|
| PR #1762 automated CI | Passed: 841 passed, 1 skipped; 98.27% coverage | [CI run 46033531255](https://github.com/JM-Brun/llm-lab/actions/runs/46033531255) |
| Full Quarto render and generated projections | Passed | [Quarto run 46033531298](https://github.com/JM-Brun/llm-lab/actions/runs/46033531298) |
| FR/EN desktop/mobile browser audit | Passed; no overflow, no unrendered math, zero desktop Axe violations, no reported failures | [Quarto run 46033531298](https://github.com/JM-Brun/llm-lab/actions/runs/46033531298), artifact `15216131326` |
| Secret scanning | Passed | [Secret scan 46033531196](https://github.com/JM-Brun/llm-lab/actions/runs/46033531196) |
| Learning contract and scientific precision | Completed | PR #1762 current diff |
| Learner transfer check | **Open** | Record reader feedback here |
| PR merge decision | Open; PR not merged at this update | [PR #1762](https://github.com/JM-Brun/llm-lab/pull/1762) |
