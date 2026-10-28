# Public page audit inventory

**Status:** first-pass audit, not a certification of all claims or a rendered-site review.  
**Started:** 2026-10-28  
**Scope of this pass:** Transformer overview and its direct concept chain.  
**Method:** [Reader experience and editorial method](reader-experience-and-editorial-method.md).

This file records what was actually reviewed and what remains to be checked. A page is not marked complete because it exists, is linked, or has a green CI run. Scientific review, French/English parity, rendered-page review, implementation evidence, and learner mastery are separate checks.

## Status vocabulary

- **Reviewed — follow-up open:** source content inspected; concrete remaining checks are recorded.
- **Updated in PR:** source edits proposed in an open pull request; not yet merged or rendered.
- **Not reviewed:** no claim of content review.
- **Not applicable:** criterion does not apply to this page type.

## First vertical slice: Transformer → attention → position

| Page / language pair | Role and reader question | What this pass confirmed in source | Remaining work |
|---|---|---|---|
| `site/en/transformer.qmd` + `site/fr/transformer.qmd` | **System overview.** How does a decoder-only GPT turn a context into a next-token distribution, and how do the major components fit together? | Both pages explain token-to-representation flow, Transformer blocks, attention, logits/probabilities, and the difference between training and generation. Both distinguish the original encoder–decoder Transformer from GPT and warn against treating attention weights as a complete explanation. The further-reading lists have been reorganized by purpose in PR #60. | **Updated in PR #60; render pending.** Visually inspect both languages; verify every local link; ensure the architecture comparison remains concise and optional details do not become prerequisites. Check whether a compact encoder-only / encoder–decoder / decoder-only comparison adds real value before adding it. |
| `site/en/queries-keys-values.qmd` + `site/fr/queries-keys-values.qmd` | **Concept.** What are Q, K, and V, and how do learned projections participate in attention? | Both pages explain learned projections, distinguish learned coordinates from human-readable semantic labels, give dimensions, connect to scaled attention and causal masking, and cite Bahdanau et al. (2014) and Vaswani et al. (2017). Both distinguish conceptual contracts from the absence of a reusable implementation. | Recheck equations and tensor dimensions side by side; verify that `d_k` and `d_v` are distinguished consistently; inspect the English intuition versus French diagram for equivalent learning value. Verify local links and rendered equations. |
| `site/en/scaled-dot-product-attention.qmd` + `site/fr/scaled-dot-product-attention.qmd` | **Concept / worked derivation.** How do Q/K scores become weights that aggregate V, and why is the score scaled? | Both pages give the four operations, a numerical worked example, a variance-based explanation of (1/\sqrt{d_k}), a primary-paper link, misconceptions, and implementation status. The opening explicitly says softmax does not establish semantic relevance or causality. | Recheck the worked example numerically in both languages; verify the softmax axis, mask placement, and shapes in the rendered equations; ensure the explanation distinguishes row-wise normalization from any claim of semantic or causal interpretation. |
| `site/en/causal-masking.qmd` + `site/fr/causal-masking.qmd` | **Concept / correctness invariant.** How is access to future tokens prevented, and how would leakage be detected? | Both pages define allowed positions, connect masking to autoregressive factorization, include misconceptions and a future-token perturbation test, and explicitly state that the reusable end-to-end implementation/test is not yet present. | Confirm mask convention (boolean versus additive, allowed versus blocked) stays explicit in both languages; inspect edge cases and rendering. Keep the perturbation test as a proposed acceptance criterion, not a claim that it already runs. |
| `site/en/positional-encoding.qmd` + `site/fr/positional-encoding.qmd` | **Concept / optional deep dive.** Why does attention need positional information, and how does RoPE introduce it? | Both pages distinguish multiple positional approaches, explain RoPE rotations, discuss what RoPE does and does not guarantee, include misconceptions, and link to Vaswani et al. (2017), Su et al. (2021), and Hugging Face documentation. The overview now explicitly lets readers skip the derivation on a first pass. | Recheck the mathematical derivation and any relative-position claim against Su et al.; distinguish paper-level properties from architecture-specific implementation details; inspect the figures and equations in both languages. |

## Source roles used in this slice

| Source | Role | Do not use it as |
|---|---|---|
| Vaswani et al. (2017), [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762) | Primary source for the original encoder–decoder Transformer and scaled dot-product attention. | A specification for every later decoder-only GPT or modern Transformer variant. |
| Bahdanau et al. (2014), [*Neural Machine Translation by Jointly Learning to Align and Translate*](https://arxiv.org/abs/1409.0473) | Historical grounding for attention in neural encoder–decoder models. | Evidence that all attention variants have identical mechanics. |
| Su et al. (2021), [*RoFormer: Enhanced Transformer with Rotary Position Embedding*](https://arxiv.org/abs/2104.09864) | Primary source for RoPE's formulation and stated properties. | A guarantee that every implementation or long-context extension behaves identically. |
| 3Blue1Brown, [Transformer overview](https://www.3blue1brown.com/lessons/gpt/) and [attention lesson](https://www.3blue1brown.com/lessons/attention/) | Visual intuition and a first mental model. | A substitute for formal assumptions, exact conventions, or implementation tests. |
| Jay Alammar, [*The Illustrated Transformer*](https://jalammar.github.io/illustrated-transformer/) and [*The Illustrated GPT-2*](https://jalammar.github.io/illustrated-gpt2/) | Visual comparison of the original architecture and GPT-2. | One universal diagram of all current LLMs. |
| Harvard NLP, [*The Annotated Transformer*](https://nlp.seas.harvard.edu/annotated-transformer/) | Connect the original paper's equations to an executable implementation. | A current universal GPT implementation; its architecture follows the original encoder–decoder design. |
| PyTorch, [scaled dot-product attention API](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html) | Clarify a specific library API contract and conventions. | A general proof of correctness or a full Transformer tutorial. |
| DeepLearning.AI, [*How Transformer LLMs Work*](https://www.deeplearning.ai/courses/how-transformer-llms-work) | Compact video course for a modern, system-level explanation. | The only source of truth for mathematics or an obligatory dependency for the course. |

## Second slice: mathematical-chain source coverage (source pass only)

This pass inspected the bilingual page structure and existing reference links; it did **not** independently verify every derivation or render every equation.

| Page pair | Source coverage found | Change in PR #60 | Still to verify |
|---|---|---|---|
| `logits.qmd` (FR/EN) | Clear definitions, tensor/vocabulary shapes, two-class example, invariance property, and self-check; no external reference was listed. | Added the official PyTorch `CrossEntropyLoss` API as an implementation reference for unnormalized logits, explicitly not as the mathematical definition. | Check numerical example, shapes, softmax invariance, and rendered equations. |
| `likelihood.qmd` / `vraisemblance.qmd` | Both explain autoregressive factorization, likelihood-to-loss, and an example; no external reference was listed. | Added Goodfellow, Bengio, and Courville's *Deep Learning* §5.5 on maximum-likelihood estimation, distinguishing the general framework from its autoregressive application. | Check sequence factorization, log-likelihood sign, and equivalence to the stated objective. |
| `loss.qmd` (FR/EN) | Both distinguish per-token penalty, reduction, target masks, and aggregate training metrics; no external reference was listed. | Added PyTorch `CrossEntropyLoss` documentation for ignored targets and reduction conventions. | Verify all examples and make sure training-loss comparisons state compatible reduction and masking conventions. |
| `gradients.qmd` (FR/EN) | Both explain gradients, chain rule, gradient-descent update, and finite-difference verification; no external reference was listed. | Added PyTorch autograd mechanics and `gradcheck` documentation. | Verify derivative examples, finite-difference tolerances, and the distinction between mathematical gradients and library autodiff behavior. |
| `probabilities.qmd` / `probabilites.qmd`, `entropy.qmd`, `cross-entropy.qmd` | Existing source links include relevant PyTorch API documentation and/or information-theory references. | No source-list change in this pass. | Review the actual claims and equations; the existence of a reference list does not establish completeness or correctness. |
| `mathematical-foundations.qmd` (FR/EN) | Both provide a high-level chain and common notation; the page links to PyTorch's cross-entropy API. | Used as the entry point for the chain, not rewritten. | Check that every linked concept's notation and loss conventions agree and that the overview remains readable without opening every derivation. |

The new references were selected for a specific role: official API docs specify implementation conventions; Goodfellow et al. provide the general mathematical foundation for maximum likelihood. Neither type replaces the local explanation.

## Next audit steps

1. Finish source and rendered-page review of this vertical slice; check local links and bilingual meaning, not just literal wording.
2. Finish the mathematical-chain audit: verify equations, worked examples, notation consistency, rendering, and bilingual meaning; the source-coverage pass above is not a full scientific review.
3. Review text and data: tokenization, corpus boundaries, context windows, shifted targets, packing, padding, and loss masks.
4. Review the remaining pages (tensors, embedding space, evaluation, critical notes, glossary, history, references, exercises) and record missing counterparts or artifacts explicitly.
5. Prioritize concrete defects by reader impact. Do not bulk-rewrite pages that already satisfy the contract.
6. Do not add implementations or experiments until their prerequisites pass the existing knowledge-validation gate.

## What this inventory does not claim

- It is not a complete audit of every page in the repository.
- Source inspection is not a rendered Quarto review.
- A cited source is not proof that every sentence on the page is correct.
- A planned test is not an executed test.
- Publication, CI, or completing an exercise does not by itself demonstrate learner mastery.
