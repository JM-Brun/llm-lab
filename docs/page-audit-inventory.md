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
| `site/en/transformer.qmd` + `site/fr/transformer.qmd` | **System overview.** How does a decoder-only GPT turn a context into a next-token distribution, and how do the major components fit together? | Both pages explain token-to-representation flow, Transformer blocks, attention, logits/probabilities, and the difference between training and generation. Both distinguish the original encoder–decoder Transformer from GPT and warn against treating attention weights as a complete explanation. The further-reading lists have been reorganized by purpose in PR #60. | **Updated in merged PR #60; Quarto render and rendered local-link check passed on that PR head.** Visual browser review remains open; ensure the architecture comparison remains concise and optional details do not become prerequisites. Check whether a compact encoder-only / encoder–decoder / decoder-only comparison adds real value before adding it. |
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

## Third slice: text/data and training-example resource curation

This pass inspected the bilingual source sections and page structure, not every claim in the full lessons and not the rendered site.

| Page pair | What the source inspection found | Remaining work |
|---|---|---|
| `text-data.qmd` (FR/EN) | Both pages separate intuition, interactive visualizations, educational code, technical references/alternatives, and a suggested reading order. The resource set covers Karpathy's tokenizer walkthrough, Raschka, Hugging Face, BPE visualizers, `tiktoken` educational code, `minbpe`, SentencePiece, and the historical BPE paper. Both versions warn that teaching demonstrations and historical descriptions do not fully specify production tokenizer behavior. | Verify links and dates/versions; check the factual distinctions between BPE, WordPiece, SentencePiece, and production tokenizers; review the multilingual/equity claims and mini-lab instructions; inspect figures and responsive layout. |
| `training-examples.qmd` (FR/EN) | Both pages cover input-target shift, windows/stride, document boundaries/packing, padding/loss masks, tensor shapes, and a debugging checklist. Resource roles are explicit: worked examples, objective interpretation, educational code, batching API, visual model overview, and attention explanation. The pages avoid prescribing one universal packing or cross-document masking policy. | Verify local links to math/attention concepts; check all examples and masks; make sure packing, attention masks, and loss masks remain distinct; inspect rendered Mermaid diagrams and bilingual parity. |

The text/data resource library is already more than a list of links: it tells readers what each resource is useful for, what it does not establish, and how to progress from intuition to code to technical references. Preserve this pattern when curating other modules; do not add more sources unless they contribute a distinct role or resolve a gap.


## Fourth slice: attention arithmetic, causal-mask conventions, and training-example alignment

This source-level pass checked the stated numerical example and compared the English/French explanations side by side. The Quarto workflow completed successfully on the merged PR head, including its rendered local-link check; that does not replace a visual browser review or a full independent scientific audit.

| Area | Check performed | Result | Remaining work |
|---|---|---|---|
| Scaled dot-product attention numerical example | For scores `(1/√2, 0)`, the softmax is approximately `(0.6698, 0.3302)`. Applying these weights to `(10, 0)` and `(0, 20)` gives approximately `(6.698, 6.604)`, consistent with the displayed `(6.7, 6.6)`. | Arithmetic is consistent to the stated rounding. The explanation explicitly defines row-wise softmax and separates scores, weights, and output. | Independently inspect rendered math and the two SVG diagrams; no executable regression test currently verifies this example. |
| Attention dimensions and mask | Q,K ∈ R^(T×d_k), V ∈ R^(T×d_v), scores T×T, output T×d_v; additive mask uses 0 for allowed and −∞ for blocked positions. | Dimensions and convention are internally consistent for self-attention. Both language versions mention that a fully masked row needs explicit handling. | Verify diagrams and ensure future implementation tests include fully masked rows and the exact API convention. |
| Boolean-mask polarity | The pages distinguish PyTorch scaled_dot_product_attention (True = allowed) from MultiheadAttention attn_mask (True = blocked). | Important API-specific distinction is present in both languages. | Recheck against the API version used when an implementation is introduced; do not assume conventions are stable across every library/API. |
| Autoregressive shift | Input [t0,t1,t2,t3] maps to target [t1,t2,t3,t4]; the causal mask allows the diagonal because the input at position i contains x_i, while the target is x_(i+1). | The explanation is aligned with next-token prediction. The boundary convention for beginning/end tokens is noted. | Add an executable example only after the prerequisite concept gate; test final-token handling and padding/loss-mask alignment. |
| Windows, document packing, and masks | Reviewed distinctions among stride, context length, packing, separators, cross-document attention, attention masks, and loss masks. | Both language versions correctly avoid presenting one packing or cross-document policy as universal. A separator token alone is not described as blocking attention. | Validate all diagrams after render and later add tests that demonstrate intended boundary and loss-mask behavior in a concrete pipeline. |

## Next audit steps

1. Finish source and rendered-page review of this vertical slice; check local links and bilingual meaning, not just literal wording.
2. Finish the mathematical-chain audit: verify equations, worked examples, notation consistency, rendering, and bilingual meaning; the source-coverage pass above is not a full scientific review.
3. Finish the text/data and training-example audit: verify external/local links, scientific claims, worked examples, masks, diagrams, and responsive rendering.
4. Review the remaining pages (tensors, embedding space, evaluation, critical notes, glossary, history, references, exercises) and record missing counterparts or artifacts explicitly.
5. Prioritize concrete defects by reader impact. Do not bulk-rewrite pages that already satisfy the contract.
6. Do not add implementations or experiments until their prerequisites pass the existing knowledge-validation gate.

## What this inventory does not claim

- It is not a complete audit of every page in the repository.
- Source inspection is not a rendered Quarto review.
- A cited source is not proof that every sentence on the page is correct.
- A planned test is not an executed test.
- Publication, CI, or completing an exercise does not by itself demonstrate learner mastery.


## Fifth slice: text/data and training-window alignment (source review)

This pass compared the English and French source pages and checked the worked input-target example, stride table, conceptual diagrams, mask distinctions, and mini-lab parity. It did not verify every external URL or inspect rendered pages in a browser.

| Area | Check performed | Result | Remaining work |
|---|---|---|---|
| Text → token → ID → embedding | Checked that the pipeline separates Unicode text, UTF-8 bytes, tokenization, IDs, and learned embeddings; both languages explicitly call diagrams conceptual and segmentation examples hypothetical. | Core distinctions and limitations are aligned across languages. | Verify external links and inspect rendered diagrams and mobile layout. |
| BPE and tokenizer claims | Checked the distinction between tokenizer training and encoding, and the qualification that byte-level base units are not a property of every BPE tokenizer. | Wording avoids treating all BPE tokenizers as interchangeable or as morphological analyzers. | Independently validate the cited research claims and current resource availability; this source pass did not open every paper. |
| Multilingual comparison mini-lab | Compared test cases for whitespace, casing, numbers, composed/decomposed Unicode, language variation, and code. | The EN/FR pages contain equivalent test categories and warn that token count alone is not a quality metric. | Run the mini-lab with named tokenizer versions before reporting empirical outcomes. |
| Input-target shift | Checked the worked input/target example and confirmed that stride examples are input windows. | Alignment is consistent, but the original stride table could be read as describing complete training examples. This PR labels the table as input-window-only and explains the required successor/tail convention in both languages. | Later add a small executable example only after the prerequisite knowledge gate; test tail handling and padding/loss-mask alignment. |
| Document boundaries, padding, masks, shapes | Compared the EN/FR descriptions and diagrams for packing, separators, cross-document attention, loss masks, and `[B,L,V]` logits. | The pages distinguish these concepts and do not claim that a separator token blocks attention by itself. | Validate Mermaid rendering and eventually test a concrete pipeline's mask semantics. |

The edits in this slice are intentionally narrow: clarify the scope of the stride table and connect it to next-token target alignment. No model implementation was added. No Quarto render, external-link sweep, executable test, or visual browser review was performed for this slice.
