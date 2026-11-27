# Language-representation bridge — remaining work

**Updated:** 2026-11-27  
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

### Validation status at this update

| Check on the latest PR #1762 head at this update | Status |
|---|---|
| Python quality and domain checks | Passed on head `a1f9fbd` |
| Full test suite | Passed: 839 passed, 1 skipped, 1 warning |
| Full Quarto render | Passed |
| Current-head browser audit | Passed: FR/EN desktop and mobile, no overflow, no unrendered math, no Axe violations on desktop; report has no failures |
| Secret scanning | Passed |

The browser audit from PR #1754 must not be treated as final validation for PR #1762: the page text, examples, learning outcomes, and visual content have changed.

## 2. Remaining work — ordered by priority

### P0 — Complete validation of the current content

- [x] Full test suite on the current PR head: 839 passed, 1 skipped, 1 warning.
- [x] Full Quarto render completed successfully.
- [x] Browser audit completed for French and English at desktop (1440 px) and mobile (390 px) widths.
- [x] Inspected the four rendered lesson screenshots: hierarchy, lead, tables, diagram, callouts, language switch, breadcrumbs, and previous/next links render correctly; no visible clipping or layout defect was found.
- [x] Browser report confirms no horizontal overflow on the lesson and review pages; desktop lesson pages have 0 Axe violations and all four lesson views render 4 math spans with 0 unrendered math.
- [x] Generated map freshness tests pass; the canonical generator output matches the tracked map data. No hand-edits to generated artifacts were used.
- [x] The lookup equation is retained as a concise bridge from ID to learned vector, not as a detailed implementation lesson.

**Resolved CI defects:** an earlier head (`9bc83e5`) had stale FR/EN section-heading inventories; a later head (`f4ba645`) exposed stale `purpose` values for the two review sheets. The canonical learning-map generator was rerun and its outputs committed. On head `a1f9fbd`, both bilingual freshness tests pass as part of the 839-passed test suite.

**Acceptance:** current PR head has successful CI and Quarto/browser checks, with any remaining warnings identified and judged. A successful render alone is not a substitute for inspecting the page in the browser.

### P1 — Align the learning contract with the revised explanation

The content has shifted from a mostly representational distinction toward a motivation grounded in mathematical modelling and distributional learning. Some supporting metadata and revision material still reflect the earlier emphasis.

- [x] Revisit the bilingual page-map `purpose`, `summary`, and `scope` for alignment with the revised opening and learning outcomes.
- [x] Update the `language-representation` outcome in `data/guided-route.yml` to cover learned vectors, network transformations, linguistic regularities, prediction, and the distinction between IDs, initial embeddings, and contextualized states.
- [x] Update the bilingual `revision-language-representation` sheets so their recall question and answer cover the motivation for learnable numerical representations and the role of the prediction objective.
- [x] Recheck the bilingual `revision_support` evidence and review-sheet `scope`/`purpose`; preserve the existing typed `revision_of` relation and synthesis contract.
- [x] Confirm that the main lesson and review sheets remain aligned in French and English.

**Acceptance:** a learner reviewing the sheet can reconstruct the *why* (learnable numerical representations and linguistic regularities), not only the *what/how* (ID → embedding → contextualized state).

### P1 — Tighten scientific precision in the examples

- [x] Clarify that the integer table using *chat/chien/voiture* and *cat/dog/car* is a simplified illustration. Real tokenizers assign IDs to tokens, which may be words, subwords, punctuation, or other units; a written word is not necessarily one token.
- [x] Confirm that the distributional example (*chat/félin*, *cat/feline*) illustrates evidence from usage and context, not a guarantee that every next-token model places synonyms near one another in its embedding table.
- [x] Keep the distinction between an embedding's learned parameters and an explicit dictionary definition; vectors are not human-readable dictionary entries.
- [x] Preserve the qualification that contextualization depends on the architecture and accessible context. The same token ID gives the same initial embedding at fixed parameters, but later states may differ by occurrence.
- [x] Explain briefly that gradients update embedding parameters and later network parameters through the training objective; discrete token IDs are not differentiable parameters. The derivation remains in the dedicated training lessons.

**Acceptance:** no claim equates token IDs with semantic coordinates, vector proximity with synonymy or understanding, or a token's initial embedding with its contextualized state.

### P2 — Validate the pedagogical transfer

Automated tests establish structural consistency and rendering, not whether the learner has acquired the intended mental model.

- [ ] Ask a reader who has not studied the later embedding/attention lessons to explain, in their own words:
  1. why assigning an integer to a word/token does not create a useful semantic geometry;
  2. what learned vectors make possible that an arbitrary ID does not;
  3. how prediction from usage can encourage useful representations without a hand-written dictionary of meanings;
  4. why an initial embedding is not yet a contextualized representation.
- [ ] Record any misconception or point of friction and make the smallest targeted revision.
- [ ] Recheck that the page remains an overview and does not duplicate the concrete tokenizer trace in `text-data`, embedding lookup in `embedding-space`, or Transformer computation in later lessons.

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

1. [x] Finish CI and full-site rendering.
2. [x] Complete and inspect the current-head desktop/mobile browser review.
3. [x] Align the bilingual lesson, metadata, route outcome, revision sheets, and scientific qualifications.
4. [x] Regenerate affected map projections and pass their freshness validators.
5. [x] Run the full tests and browser audit on the final code head `a1f9fbd`.
6. [ ] Conduct the short learner transfer check (P2).
7. Keep PR #1762 open until the user decides whether to merge; the automated and rendered-site checks are green.

## 5. Completion record

Update this section when work is performed:

| Item | Result | Evidence |
|---|---|---|
| PR #1762 CI | Passed — 839 passed, 1 skipped, 1 warning | [CI run 8227](https://github.com/JM-Brun/llm-lab/actions/runs/46033531255) |
| Full Quarto render | Passed | [Quarto run 7573](https://github.com/JM-Brun/llm-lab/actions/runs/46033531298) |
| Current-head browser audit | Passed — FR/EN desktop and mobile, no overflow, 0 Axe violations on desktop, no audit failures | [Browser-review artifact](https://github.com/JM-Brun/llm-lab/actions/runs/46033531298) |
| Review-sheet and route-outcome alignment | Completed | [PR #1762](https://github.com/JM-Brun/llm-lab/pull/1762) |
| Learner transfer check | Open — requires an independent reader | Record reader feedback and resulting changes |
