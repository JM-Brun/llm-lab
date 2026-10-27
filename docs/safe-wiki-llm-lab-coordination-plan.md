# Safe, staged coordination plan: private wiki and public LLM Lab

**Status:** Phase 0 — planning and inventory.  
**Applies to:** `JM-Brun/wiki-knowledge` (private canonical knowledge base) and `JM-Brun/llm-lab` (public bilingual learning book).  
**Non-negotiable constraint:** the public `llm-lab` site must remain understandable and usable without access to the private wiki.

## 1. Editorial contract

The two repositories have different audiences and delivery constraints.

- **`wiki-knowledge`** is the canonical, cross-domain home for reusable foundations: general definitions, assumptions, derivations, edge cases, proof sketches, and relations between concepts.
- **`llm-lab`** is the public, bilingual application book. It explains what those foundations mean in language modelling and Transformers, with LLM-specific notation, examples, shapes, implementation implications, diagnostics, references, and limitations.
- **A concept may legitimately appear in both repositories.** Reuse is not a mandate to delete. General theory can live in the wiki while a compact, self-contained explanation of the needed theory remains in LLM Lab.
- **No public page may require a private link to be understood.** A wiki link may be a supplementary “deeper foundation” link only. The public page must retain enough definitions, assumptions, equations and references to stand alone.
- **No knowledge is deleted merely to reduce duplication.** First inventory it, classify it, identify its destination, and verify that the destination retains it. When in doubt, keep the content in the public page until reviewed.
- **No mandatory chapter mapping.** The course structure is determined by learner prerequisites and the goal of implementing, training, generating with, testing, and evaluating a small decoder-only LLM. Raschka is a coverage reference, not the table of contents.
- **Do not add new model implementations or experiments until their prerequisites have been reviewed/acquired in the private career-learning inventory.**

## 2. Safe content classes

Classify each passage, equation, diagram, reference, example, caveat, exercise, and test separately where needed. A whole page may contain multiple classes.

| Class | Examples | Required treatment in public `llm-lab` | Wiki treatment |
|---|---|---|---|
| A. General foundation | Entropy definition, KL support conditions, chain rule, vector-space definition | Keep a concise standalone explanation when required to understand the LLM lesson; cite public references. | May host the deeper canonical treatment. |
| B. LLM application | Next-token distribution, causal shift, logits-to-softmax flow, token loss, Transformer axes | Keep and develop here. | Link from wiki only where useful; do not force application details into the foundation page. |
| C. Shared bridge | Softmax derivative, relation between NLL and likelihood, meaning of entropy for decoding | Keep the LLM interpretation and any assumptions needed locally; cross-link the general derivation. | Keep general derivation and cross-domain connections. |
| D. Evidence and validation | Code examples, numerical checks, tests, benchmark results, shape diagrams | Keep or link to public code/tests; do not replace with a private-only reference. | Store general evidence only if it serves the wiki's own policy and scope. |
| E. Learning support | Misconceptions, counterexamples, self-check questions, glossary terms | Keep the material needed for the public reader; duplication is acceptable when pedagogically useful. | Keep general exercises or concept relations where appropriate. |
| F. Provenance | Citations, attribution, source notes, caveats | Preserve in the repository where the claim or asset is used; links must be publicly accessible. | Preserve source provenance for canonical claims. |

## 3. Phased workflow and gates

### Phase 0 — Freeze and inventory (current phase)

1. Treat the existing `llm-lab` PR #17 as a reviewable proposal, not as permission to remove content from the public book.
2. Capture the current `main` version and proposed branch version of every affected public page.
3. Build a passage-level preservation ledger: source file/section; concept or claim; equations; assumptions; examples; caveats; references; exercises; links; proposed treatment; destination; reviewer/status.
4. Compare the new wiki concepts with both the public page on `main` and the proposed PR version.
5. Mark each item **keep public**, **keep in both**, **move only after verified replacement**, **rewrite**, or **unresolved**. “Move” never means silently delete.

**Gate 0:** no further removals or page-scope reductions until the ledger exists and the public-self-containment review is complete.

### Phase 1 — Validate the private canonical concepts

For each newly added wiki concept, check definitions, domains, assumptions, boundary cases, notation, derivations, source quality, cross-links, and registry consistency. Confirm its lifecycle/status accurately reflects the level of review. The fact that a concept page exists or automated checks pass is not scientific validation.

**Gate 1:** any concept still draft or scientifically unreviewed may be linked as supplementary reading, but it cannot justify removing the public explanation.

### Phase 2 — Audit the proposed public edits

Review each changed public page against its original content and the preservation ledger. Verify that:
- the public page defines all notation it uses;
- necessary equations and assumptions remain present;
- the LLM-specific explanation is more precise, not merely shorter;
- references are public and sufficient;
- links resolve within the public site;
- French and English versions have equivalent technical coverage;
- figures, alt text, and attribution remain intact;
- examples and self-checks still teach the intended concept.

**Gate 2:** every removed or condensed item has a verified disposition, and a reader without wiki access can follow the page.

### Phase 3 — Validate the public build and navigation

Run the Quarto render/CI checks; inspect the rendered site in both languages; check local links, anchors, navigation, figures, accessibility basics, and bilingual parity. Automated success is necessary but does not replace content review.

**Gate 3:** public build and content review pass. No merge based solely on green CI.

### Phase 4 — Merge in safe order

The wiki foundation PR may be merged independently only after its own scientific and repository-policy review. The public PR can then be reviewed against the merged concepts, but must remain self-contained. If wiki validation is delayed or a concept is rejected, retain or restore the relevant explanation in `llm-lab`; do not block the public book on private content being perfect.

**Gate 4:** explicitly confirm the final public diff and the preservation ledger before merging `llm-lab` PR #17.

### Phase 5 — Continue the course, one bounded slice at a time

Only after the current math-page slice is closed, select the next bounded slice based on prerequisites and the implementation objective. For each slice: inventory → propose → review science → update FR/EN → run checks → inspect rendered output → update the curriculum and next-session handoff. Do not refactor the entire course in one PR.

## 4. Immediate scope: the current mathematical-page slice

The current PR concerns entropy, probabilities/softmax, cross-entropy, and tensor shapes; gradients and likelihood links are adjacent dependencies. Before merging:

- Compare the original public versions with PR #17 line by line.
- Verify that general information-theory explanations removed from public pages are not needed to understand the retained LLM material.
- Preserve the complete explanation locally: all definitions, assumptions, derivations, examples, caveats, and exercises needed for the LLM learning objective. A deeper general treatment in the private Wiki is supplementary and never justifies shortening the public lesson.
- Check the probability page for numerical stability and the distinction between logits, probabilities, confidence, calibration, and truth.
- Check cross-entropy for target alignment, ignored positions, reduction, and the exact conditions linking token NLL and perplexity.
- Check tensors for shape/axis semantics, framework-array terminology, masking/broadcasting pitfalls, and both-language parity.
- Check entropy for the distinction between distribution entropy and observed-token surprisal, and do not imply that low entropy establishes factual correctness.
- Check gradients and likelihood links for consistent notation and loss aggregation; avoid claiming finite-difference agreement proves the intended model is correct.
- Retain all existing public references, figures, exercises, caveats, and useful examples unless a reviewed ledger explicitly records their replacement.

## 5. Acceptance criteria for every future PR in this workstream

- [ ] Scope is bounded and stated.
- [ ] Original public content has been inventoried before edits.
- [ ] No knowledge has been silently dropped; each removed/condensed item has a recorded disposition.
- [ ] Public pages are self-contained without private repository access.
- [ ] Canonical wiki links are supplementary, not required for comprehension or rendering.
- [ ] Technical claims state assumptions and link to public sources, proofs, tests, or code as appropriate.
- [ ] FR/EN technical coverage is equivalent, or remaining gaps are explicitly tracked.
- [ ] Relevant rendered pages, navigation, figures, and links have been inspected.
- [ ] CI status is reported accurately; a green build is not presented as scientific validation.
- [ ] Curriculum and next-session handoff are updated.

## 6. Immediate next action

Do **not** start another broad rewrite. First create and review the preservation ledger for the four affected concepts (entropy, probabilities/softmax, cross-entropy, tensors), using `llm-lab/main`, the current PR branch, and the merged wiki concepts as the three comparison points. Resolve any uncertain item by retaining it publicly. Only then make targeted corrections to PR #17.
