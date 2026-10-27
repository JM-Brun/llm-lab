# Editorial boundary audit: general foundations vs LLM applications

**Status:** first-pass inventory, reviewed 2026-10-27. This is an editorial audit, not a claim that all pages have already been rewritten or that the private wiki content has been verified. The passage-level record for the current four-concept slice is in the [knowledge-preservation ledger](knowledge-preservation-ledger.md). No model implementation or experiment is authorized by this document.

## Decision rule

- `wiki-knowledge` is the canonical location for general mathematical definitions, derivations, proofs, and reusable examples.
- `llm-lab` explains the consequences of those concepts for token prediction, Transformer computation, training, generation, and evaluation.
- Public lessons must remain independently understandable because the canonical wiki is private. Keep and teach all definitions, assumptions, derivations, examples, caveats, and exercises needed for the LLM learning objective; cite public sources. Do not publish private Wiki URLs or concept IDs in reader-facing content; maintainers may record cross-repository traceability in private notes.
- Keep a page when it explains an LLM-specific mechanism, even if it uses mathematics. Refactor it when most of its explanatory value is a general mathematical treatment.
- Page ownership is conceptual, not one-to-one: one applied page can use several wiki concepts and one concept can support many applied pages.

## Inventory and disposition

| Existing public page | First-pass classification | Recommended action |
|---|---|---|
| `site/fr/mathematical-foundations.qmd`, `site/en/mathematical-foundations.qmd` | Applied overview already connects logits → probabilities → likelihood/loss → gradients | Keep the chain, but rename the reader-facing title and framing to “The mathematical chain of LLM training”. Keep the equations as a compact map, not a general foundations course. |
| `site/fr/logits.qmd`, `site/en/logits.qmd` | LLM-specific application with a small generic definition | Keep; prioritize vocabulary-sized output vectors, shift/position/batch dimensions, invariances, and what logits do not mean. Avoid expanding into a general treatment of score parameterizations. |
| `site/fr/probabilites.qmd`, `site/en/probabilities.qmd` | Mixed: general softmax/probability plus next-token interpretation | Keep as an application page; focus on categorical next-token distributions, conditional context, temperature as a decoding transform, and the distinction between normalized probabilities and calibration/truth. Link to public general references. |
| `site/fr/entropy.qmd`, `site/en/entropy.qmd` | Predominantly general information theory (joint/conditional entropy, mutual information, coding, continuous variables, statistical-physics comparison) | Highest-priority refactor. Reduce to the entropy of a model's next-token distribution, conditional entropy/perplexity where relevant, and interpretation limits. Classify general derivations individually. The Wiki may hold a deeper cross-domain treatment, but retain the mathematical definitions and derivations needed by the public LLM lesson. Do not call anything “moved” until the disposition is verified. |
| `site/fr/cross-entropy.qmd`, `site/en/cross-entropy.qmd` | Mixed, with substantial general derivation (KL direction, coding, arbitrary target distributions) and some LLM application | Refocus on token-level negative log-likelihood, one-hot versus soft targets only as needed, reduction/masking, token averaging, and perplexity. Keep only the mathematical identities needed to make the LLM objective understandable. |
| `site/fr/vraisemblance.qmd`, `site/en/likelihood.qmd` | Strong LLM-specific application: autoregressive factorization and observed tokens | Keep; make explicit sequence likelihood, conditional factorization, teacher forcing, summed versus mean token NLL, padding/target masks, and the relationship to cross-entropy. Record the general MLE concept relation internally; the public page must derive the needed LLM-specific result and cite accessible public sources. |
| `site/fr/loss.qmd`, `site/en/loss.qmd` | Strong LLM-specific application: target shifting, masking, batch reduction, diagnostics | Keep; ensure each implementation claim corresponds to an actual implementation/test or is labelled planned. Avoid duplicating a general loss-function taxonomy. |
| `site/fr/gradients.qmd`, `site/en/gradients.qmd` | Mixed: general chain rule/gradient descent plus cross-entropy derivative and numerical checks | Refocus on gradient flow from token loss through logits and model parameters, what autodiff computes, finite-difference checks, and failure modes. Retain the chain-rule explanation needed locally; record any Wiki relation in private maintainer notes only. |
| `site/fr/tensors.qmd`, `site/en/tensors.qmd` | LLM-specific representation/shapes, with general tensor prerequisites | Keep Transformer-specific shapes plus enough local explanation of arrays, axes, rank, and projection semantics for a standalone reader. The Wiki may contain a deeper general treatment; do not remove local prerequisites just to avoid overlap. |
| `site/fr/embedding-space.qmd`, `site/fr/positional-encoding.qmd` (no English counterparts in the current tree) | LLM/Transformer-specific applications, but incomplete bilingual parity | Keep in scope; track English counterparts as an editorial gap, not as permission to duplicate general linear algebra. |
| `site/fr/transformer.qmd`, `site/en/transformer.qmd`; Q/K/V, scaled attention, causal masking | Applied architecture and computation | Keep. Link equations to model behavior, tensor dimensions, causal invariants, implementation status, and tests. |
| `site/fr/cosine-similarity.qmd`, `site/en/cosine-similarity.qmd`; embedding-linearity pages | Critical application/research notes | Keep as cross-cutting case studies, not as substitutes for the implementation path or general vector-space foundations. |
| `site/fr/evaluation-experimentale.qmd`, `site/en/experimental-evaluation.qmd` | Evaluation-method application | Keep separate from general statistics; identify the exact LLM evaluation decision and limits being illustrated. |
| Glossary, history, exercises, references | Navigation and learning support | Keep; glossary definitions should be concise and point to applied pages, not grow into a competing textbook. |

## Structural findings

1. The Quarto sidebar now labels the sequence as maths applied to LLMs in both languages. This aligns the navigation with the intended ownership boundary; the content refactor is tracked separately.
2. The entropy pages are the clearest substantive duplication risk: they cover broad information theory, coding, continuous variables, and a comparison with statistical physics, much of which is reusable outside LLMs.
3. The cross-entropy and gradients pages also contain general derivations that should be shortened in favour of the training objective and gradient flow in an autoregressive model.
4. The likelihood and loss pages are comparatively well aligned with the desired scope because they already discuss autoregressive factorization, target shifts, masking, and aggregation.
5. General concepts were added in [wiki-knowledge PR #23](https://github.com/JM-Brun/wiki-knowledge/pull/23), but their pages remain draft and need scientific/registry follow-up. Their existence is not a completed migration and does not authorize reducing the public explanations.
5. The tensor lesson now has an English counterpart and a translated diagram. English counterparts for embedding space and positional encoding remain gaps; do not silently describe every concept page as fully bilingual.
6. The README and home pages should describe the public course as an LLM application lab, not as a second canonical mathematics wiki.
7. A private Wiki URL is never sufficient support for public readers. Each applied page must teach the prerequisites needed for independent comprehension, including definitions, assumptions, derivations and examples as required, plus accessible public references.

## Current implementation status — 2026-10-27

The entropy and cross-entropy pages have already been refocused in `main`; do not treat them as unstarted refactors. The current versions retain the LLM-specific definitions and caveats identified in the inventory above. A textual bilingual pass found no correction that could be justified from the current source alone. Browser-rendered MathJax/layout and live external-reference checks remain open; see the [knowledge-preservation ledger](knowledge-preservation-ledger.md).

The next content-review slice is **logits and probabilities**, followed by **likelihood and loss**, then **gradients**. Review these as connected parts of the autoregressive objective rather than independent rewrite projects. Preserve current scope and only edit where a specific claim, mismatch, missing assumption, broken link, or pedagogical defect is demonstrated.

## Ordered work

### P0 — Clarify the public information architecture
- Rename the visible mathematical section as “Mathématiques appliquées aux LLM / Maths applied to LLMs”.
- Reframe the mathematical-chain overview as an application map, not a general-foundations syllabus.
- Align README and home-page wording with the wiki/course division.
- Keep all existing URLs stable while changing titles and navigation.

### P1 — Refactor the highest-duplication pages
1. **Logits/probabilities:** audit the paired pages for exact meaning of logits, vocabulary dimension, conditional distributions, temperature, calibration versus truth, and bilingual parity.
2. **Likelihood/loss:** validate sequence factorization, target shift, padding/ignored positions, reduction, and perplexity conventions across the paired pages.
3. **Gradients:** audit the loss-to-logits-to-parameters path, assumptions behind derivatives, and numerical-verification claims.
4. **Entropy/cross-entropy:** the first-pass refactor is already in `main`; retain the current focused scope and resolve only the outstanding browser/external-reference checks or defects found by later evidence.

### P2 — Validate and connect
- Compare French and English claims, caveats, examples, and references page by page.
- Add links from each applied mechanism to code/tests only when those artefacts exist.
- Check all internal links and render the full Quarto site.
- Verify canonical wiki destinations privately before asserting that general content has been migrated; never expose private page content on the public site.
- Keep the mastery registry private and do not infer mastery from page edits or passing CI.

## Acceptance criteria

- The visible information architecture no longer presents LLM Lab as the canonical home of general mathematics.
- Every retained mathematics page answers a concrete LLM question and includes its assumptions, an LLM-specific example, limits, and public references.
- General mathematical treatments are owned by `wiki-knowledge`; no claim of migration is made without checking the destination.
- The public site remains understandable and renderable without private-repository access.
- French/English parity gaps are explicitly tracked.
- No implementation or experiment is added before its prerequisite knowledge is validated.
