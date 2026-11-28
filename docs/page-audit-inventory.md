# Public page audit evidence log

**Status:** cumulative record of bounded, dated audits. It is neither a complete site-wide certification nor a live operational status board.  
**Started:** 2026-10-28  
**Latest entry in this file:** 2026-11-24. Later Raschka chapter and appendix audits are recorded in [the full curriculum plan](full-curriculum-plan.md).  
**Scope:** selected bilingual pages, page groups, source contributions, scientific claims, implementation evidence, and rendered/visual observations. Each entry states its own scope and evidence boundary.  
**Method:** [Reader experience and editorial method](reader-experience-and-editorial-method.md).

Use the [content-section mapping](content-section-mapping.md) for the current reader-facing destination and ownership of every FR/EN page (Understand, Build, Deepen, or Practice & experiment). This evidence log does not replace that page inventory.

This file preserves what a particular audit actually inspected and what remained uncertain at that time. Its historical statements such as “remaining work” are not automatically current: consult the linked GitHub issue/PR and any later dated reconciliation before acting. A page is not considered validated merely because it exists, is linked, or has a green CI run.

## Status vocabulary

- **Reviewed — follow-up open:** source content inspected; concrete remaining checks are recorded in that dated audit.
- **Updated in PR:** source edits were proposed in the referenced pull request; this does not imply merge, render, or browser validation.
- **Not reviewed:** no claim of content review.
- **Not applicable:** criterion does not apply to this page type.

## First vertical slice: LLM panorama → GPT/Transformer → attention → position

| Page / language pair | Role and reader question | What this pass confirmed in source | Remaining work |
|---|---|---|---|
| `site/en/llm-overview.qmd` + `site/fr/llm-overview.qmd` | **System panorama.** What is an LLM, and how do architecture, parameter learning/adaptation, and inference differ? | Both pages define the scope of LLM/NLP/AI, compare encoder-only / encoder–decoder / decoder-only Transformer families, distinguish inference with fixed parameters from training, and discuss adaptation and limitations. This PR adds an explicit three-dimension comparison and narrows the subtitle/scope from an unqualified lifecycle to the path from pretraining to use. | **Updated in this PR.** Check whether the table gives a sufficiently precise mental model without duplicating the GPT computation page; verify bilingual semantic parity, rendered table/diagram and first-screen/navigation. |
| `site/en/transformer.qmd` + `site/fr/transformer.qmd` | **System overview.** How does a decoder-only GPT turn a context into a next-token distribution, and how do the major components fit together? | Both pages explain token-to-representation flow, Transformer blocks, attention, logits/probabilities, and distinguish a forward pass from the autoregressive decoding loop. The RoPE description now locates the Q/K rotation before the attention score product. Interactive experiments and source-level audit have been moved to a separate Practice page to avoid overloading the system explanation. | **Updated in this PR.** Verify bilingual rendering, local links, equation placement and the first-screen/navigation in the built site. Browser/responsive/keyboard review remains separate from CI. |
| `site/en/transformer-explainer.qmd` + `site/fr/transformer-explainer.qmd` | **Practice / experiment.** What can an interactive GPT-2 visualization show, how can its behavior be tested, and what implementation limitations must not be generalized? | The activity preserves the interactive explorer, four-part observation guide, controlled experiments, source-code trace from UI to ONNX/PyTorch computation, and critical audit of top-p truncation and attention/embedding interpretation. It distinguishes the external demo from LLM Lab's own implementation. | **Added in this PR.** Verify that the embedded explorer loads or its fallback link works; check table/math rendering, FR/EN parity and navigation. The external service and pinned source snapshot may change independently. |
| `site/en/queries-keys-values.qmd` + `site/fr/queries-keys-values.qmd` | **Concept.** What are Q, K, and V, and how do learned projections participate in attention? | Both pages explain learned projections, distinguish routing (Q/K) from transmitted content (V), give essential dimensions, and link to the advanced Q/K/V deep dive for per-position equations, geometry, gradients and architectural variants. | Keep the core page intuitive and qualitative; inspect the advanced page for mathematical correctness and bilingual parity. Verify local links, generated page context, rendered equations and sidebar placement. |
| `site/en/scaled-dot-product-attention.qmd` + `site/fr/scaled-dot-product-attention.qmd` | **Concept / worked derivation.** How do Q/K scores become weights that aggregate V, and why is the score scaled? | Both pages give the four operations, a numerical worked example, a variance-based explanation of (1/\sqrt{d_k}), a primary-paper link, misconceptions, and implementation status. The opening explicitly says softmax does not establish semantic relevance or causality. | Recheck the worked example numerically in both languages; verify the softmax axis, mask placement, and shapes in the rendered equations; ensure the explanation distinguishes row-wise normalization from any claim of semantic or causal interpretation. |
| `site/en/causal-masking.qmd` + `site/fr/causal-masking.qmd` | **Concept / correctness invariant.** How is access to future tokens prevented, and how would leakage be detected? | Both pages define allowed positions, connect masking to autoregressive factorization, include misconceptions and a future-token perturbation test, and explicitly state that the reusable end-to-end implementation/test is not yet present. | Confirm mask convention (boolean versus additive, allowed versus blocked) stays explicit in both languages; inspect edge cases and rendering. Keep the perturbation test as a proposed acceptance criterion, not a claim that it already runs. |
| `site/en/positional-encoding.qmd` + `site/fr/positional-encoding.qmd` | **Understand — core concept.** Why does a Transformer need positional information, and where do the main mechanism families enter the computation? | Both pages introduce absolute, relative, and rotary approaches at a conceptual level, distinguish their broad insertion points, and link to the dedicated advanced RoPE page. The core lesson no longer contains the RoPE derivation or implementation checklist. | Review the conceptual comparison and verify that the page does not imply all architectures use the same positional mechanism; inspect the bilingual diagrams and links. |

| `site/en/tensors.qmd` + `site/fr/tensors.qmd` | **Concept / implementation invariant.** How do tensor shapes and axes encode the semantics of LLM operations? | Both pages show common shapes, projection dimensions, a wrong-axis softmax counterexample, and bilingual SVG figures. The current change adds a minimal executable PyTorch example with shape and normalization assertions. | Review the rendered code and figure in both languages; execute the snippet in the locked environment or a dedicated test; consider extracting reusable operations into `src/llm_lab` only when there is a stable API need. The broader concept-page audit must check implementation sections across the remaining LLM topics; this single row does not certify the whole site. |

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
| `post-training.qmd` (FR/EN) | New 2026-11-11. Compares pretraining, SFT, preference methods, parameter-efficient adaptation and context-only methods by data, loss tokens and parameters changed. Sources: Ouyang et al. 2022, Wei et al. 2021, Rafailov et al. 2023, Hu et al. 2021, Lewis et al. 2020. | Source claims not yet independently reviewed. | Verify against the primary papers: SFT loss-on-response convention is typical practice and not universal; the KL-penalty statement for RLHF; the LoRA description; and the table's “typical” qualifiers. Rendered desktop and mobile review pending. |
| `training-loop.qmd` (FR/EN) | New 2026-11-10. Conceptual loop, optimizer role, train/validation loss and overfitting, with a NumPy example built on `llm_lab.foundations.losses`; sources are Kingma and Ba, Loshchilov and Hutter, Goodfellow et al. ch. 5.2, Karpathy and the PyTorch AdamW documentation. | Source claims and the example output not yet independently reviewed. | Verify the example against the current `losses.py`, the quoted numbers (loss 2.485 to 1.147, validation minimum 2.006 at step 100, final 2.162), and the scope statements about Adam/AdamW; review rendered desktop and mobile layout. |
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


## Fifth slice: numerical and algebraic checks for the mathematical chain

This is a bounded source-level check of representative identities and worked examples in the EN/FR pages. Calculations were independently checked; this is not a full derivation-by-derivation review, and no new code tests were executed in this pass.

| Concept | Independent check | Result | Remaining work |
|---|---|---|---|
| Logits → softmax | For z = (0, ln 3), softmax gives (1/(1+3), 3/(1+3)) = (0.25, 0.75). Adding the same constant to all logits preserves the distribution; a logit difference ln 2 gives a probability ratio of 2. | Examples and stated invariances in the EN/FR logits/probability pages are consistent. | Inspect rendered equations; add automated examples only if they add coverage beyond the existing loss unit tests. |
| Entropy | H(0.5, 0.5) = ln 2 nats = 1 bit. H(0.9, 0.1) = −0.9 ln 0.9 − 0.1 ln 0.1 ≈ 0.32508 nats ≈ 0.468996 bits. | Both language versions' rounded values (0.325 nats, 0.469 bit) are consistent. The stated 0 ≤ H ≤ ln V bound assumes a normalized discrete distribution over a finite vocabulary, as noted. | Verify rendered units and equations; review whether the distinction between predictive entropy and observed-token surprisal is consistently used across all linked pages. |
| Sequence likelihood → NLL | 0.5 × 0.25 × 0.8 = 0.1; −ln(0.1) ≈ 2.302585, and log-likelihood is the negative of NLL. | EN/FR example is arithmetically consistent. The text correctly attributes factorization to conditional probability/chain rule, not independence among tokens. | Verify the exact scope of the independent-sequences statement and the averaging conventions used when comparing corpus results. |
| Cross-entropy and KL | H(q,p) = H(q) + D_KL(q∥p) follows by expanding definitions for normalized q,p, with the usual zero-mass conventions. For q=(1,0), p=(0.9,0.1), D_KL(q∥p)=−ln 0.9≈0.10536 nats, while D_KL(p∥q)=∞. | The example and directionality caveat are consistent in both languages. | Inspect full derivation rendering and check terminology parity for “cross-entropy”, “entropie croisée”, and “divergence KL”. |
| Cross-entropy gradient | For one-hot target y and p=softmax(z), ∂ℓ/∂z_i = p_i − 1[i=y]. This is a derivative with respect to logits, not directly with respect to network parameters. | The gradients pages state the correct scoped identity and distinguish the later chain-rule step. | Check tensor/Jacobian notation in rendered equations; the existing NumPy reference tests have a deliberately limited row-wise scope and do not test sequence masks or target shifting. |
| Perplexity convention | If mean NLL uses natural logarithms, PPL = exp(mean NLL); if using log base 2, PPL = 2^(mean NLL). | The EN/FR loss pages correctly state the logarithm-base dependence and note tokenizer/reduction comparability limits. | Ensure future benchmark/report templates record tokenizer, evaluated tokens, ignored targets, and reduction protocol. |

The checked examples are mutually consistent across the relevant pages at source level. This does **not** imply all equations, diagrams, external links, or rendered math have been reviewed. The text pages already describe the reference NumPy loss tests and their limits; this audit did not rerun those tests.

## Sixth slice: text/data and training-window alignment (source review)

This pass compared the English and French source pages and checked the worked input-target example, stride table, conceptual diagrams, mask distinctions, and mini-lab parity. It did not verify every external URL or inspect rendered pages in a browser.

| Area | Check performed | Result | Remaining work |
|---|---|---|---|
| Text → token → ID → embedding | Checked that the pipeline separates Unicode text, UTF-8 bytes, tokenization, IDs, and learned embeddings; both languages explicitly call diagrams conceptual and segmentation examples hypothetical. | Core distinctions and limitations are aligned across languages. | Verify external links and inspect rendered diagrams and mobile layout. |
| BPE and tokenizer claims | Checked the distinction between tokenizer training and encoding, and the qualification that byte-level base units are not a property of every BPE tokenizer. | Wording avoids treating all BPE tokenizers as interchangeable or as morphological analyzers. | Independently validate the cited research claims and current resource availability; this source pass did not open every paper. |
| Multilingual comparison mini-lab | Compared test cases for whitespace, casing, numbers, composed/decomposed Unicode, language variation, and code. | The EN/FR pages contain equivalent test categories and warn that token count alone is not a quality metric. | Run the mini-lab with named tokenizer versions before reporting empirical outcomes. |
| Input-target shift | Checked the worked input/target example and confirmed that stride examples are input windows. | Alignment is consistent, but the original stride table could be read as describing complete training examples. This PR labels the table as input-window-only and explains the required successor/tail convention in both languages. | Later add a small executable example only after the prerequisite knowledge gate; test tail handling and padding/loss-mask alignment. |
| Document boundaries, padding, masks, shapes | Compared the EN/FR descriptions and diagrams for packing, separators, cross-document attention, loss masks, and `[B,L,V]` logits. | The pages distinguish these concepts and do not claim that a separator token blocks attention by itself. | Validate Mermaid rendering and eventually test a concrete pipeline's mask semantics. |

The edits in this slice are intentionally narrow: clarify the scope of the stride table and connect it to next-token target alignment. No model implementation was added. No Quarto render, external-link sweep, executable test, or visual browser review was performed for this slice.


## Seventh slice: tensor shapes, embedding geometry, and evaluation exercises (source review)

This pass compared English and French source pages for tensors, embedding space, and experimental evaluation. It checked stated shapes, axis semantics, embedding-type distinctions, cosine caveats, projection limitations, and the evaluation exercise's target population, grouping, selection bias, AP baseline, calibration, and uncertainty discussion. It did not verify every cited source or inspect rendered pages in a browser.

| Area | Result | Remaining work |
|---|---|---|
| Tensor shapes and axes | Common shapes are qualified as conventions rather than universal API contracts. The projection example is dimensionally consistent: `(B,T,D) × (D,D') → (B,T,D')`; vocabulary logits have shape `(B,T,V)`. EN/FR explanations are substantively aligned. | Inspect both SVGs and rendered equations; later verify against concrete APIs when implementation examples are introduced. |
| Embedding types and similarity | Both languages distinguish initial token embeddings, contextualized representations, and sentence/document embeddings. Both caution that cosine proximity does not prove equivalence or answer correctness and that 2D projections distort geometry. | Independently check cited papers and review the linked linearity pages in a dedicated pass. |
| Coordinate transformation statement | The original sentence could overgeneralize by saying a coordinate-mixing transformation preserves useful relationships without specifying conditions. This PR replaces it with the precise orthogonal-change-of-coordinates example, which preserves dot products, distances, and cosine similarities while changing axis interpretation. | Inspect rendered bilingual wording and keep the example scoped to orthogonal transformations; arbitrary transformations need not preserve these quantities. |
| Evaluation exercise | The case states its deployment target (unseen papers), explains paper-level grouping, raises unseen-query dependence, warns about selecting the best of 40 configurations, and distinguishes AP from calibration. The random-ranking baseline is explicitly approximate, not a finite-sample identity. | Independently verify metric references and ensure future revisions keep the estimand aligned with the split and uncertainty unit. |

This is a bounded source-level review, not a complete scientific certification. No model implementation or experiment was added. Rendered equations/figures and external-link validity remain separate checks.


## Eighth slice: version-sensitive claim in the linearity / SAE reading list

A targeted source check compared the paper's published PMLR page with the authors' later arXiv v2, which includes a corrigendum. The published PMLR abstract attributes the reported compositional generalization failures to an amortization gap; the later arXiv v2 states that dictionary learning, not the inference procedure alone, is the binding constraint, and that replacing the encoder with per-example iterative inference on the same SAE-learned dictionary does not close the gap. This is a material version difference, not a cosmetic citation update.

| Area | Finding | Change | Remaining work |
|---|---|---|---|
| EN/FR discussion of Barin-Pacela et al. (2026) | The previous prose treated limitations of amortized inference as a stable conclusion without noting the later corrigendum. | Both language pages now preserve the shared conclusion (linear representation does not imply linear accessibility) while explicitly distinguishing the PMLR proceedings abstract from the author-updated arXiv v2. | Re-read the corrigendum and paper details before any deeper technical summary; do not collapse the two versions into one claim. |
| Bibliographic links | PMLR page is the published proceedings record; arXiv v2 is linked separately as the author-updated version. | Version provenance is visible beside the claim and in the reference list. | Confirm rendered links and the wording after Quarto render; this audit did not establish which version the authors intend readers to treat as definitive beyond the stated corrigendum. |

Sources checked: [PMLR proceedings version](https://proceedings.mlr.press/v337/barin-pacela26a.html) and [arXiv v2 including corrigendum](https://arxiv.org/abs/2603.28744v2). No implementation or experiment was added. Rendered review and external-link validation remain open.


## Ninth slice: reproducibility status of the SMDS research repository

A targeted README review of the linked project repository found that it describes itself as experimental software. The repository provides code and scripts relevant to inspecting the method, but the source review did not execute the code, download and validate the data, or reproduce the paper's results.

| Area | Finding | Change | Remaining work |
|---|---|---|---|
| SMDS project resource link (EN/FR linearity pages) | Repository README describes the software as experimental. Linking to the repository is not evidence of independent reproduction. | PR #67 adds this caveat in both languages and explicitly limits the link's purpose to inspection and attempting a reproduction. | Render both pages, check link validity and bilingual parity; any actual reproduction must have a separately documented environment, data provenance, commands, outputs, and deviations. |

Source inspected: [official project repository README](https://github.com/UKPLab/tmlr2026-manifold-analysis). This is a repository-metadata/source inspection only, not an execution or reproduction audit.

## Tenth slice: primary-source check of multidimensional-feature and probe-selectivity claims

A targeted check compared the wording in the EN/FR linearity pages with the ICLR 2025 paper on multidimensional features and the ACL Anthology record for Hewitt & Liang's control-task paper. The source abstracts support the claims below; this was not a full reproduction or a line-by-line review of either paper.

| Claim area | Primary-source support | Result and scope |
|---|---|---|
| Multidimensional features and circular representations | Engels et al., [ICLR 2025 proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/d3221cdb27e49d9c1cd35ad254feccfe-Abstract-Conference.html) describe irreducible multidimensional features, circular day/month representations, modular-arithmetic tasks, and interventions on Mistral 7B and Llama 3 8B. | The page's summary is supported. Keep model names and task scope explicit; do not generalize to all features or models. |
| Probe control tasks and selectivity | Hewitt & Liang, [ACL Anthology record](https://aclanthology.org/D19-1275/) describes random-label control tasks that probe models can learn independently of the linguistic structure, and defines selectivity to contextualize task accuracy. | The page's recommendation to use control tasks and avoid interpreting probe accuracy in isolation is supported. The paper's experiments concern specific linguistic tasks and ELMo representations, so the general methodological lesson should not be presented as a universal empirical result for every probe family. |
| SMDS scope | The TMLR paper's abstract identifies temporal reasoning as the case study and reports lines, circles, and clusters; the official repository describes itself as experimental software. | The page appropriately limits generalization and labels the repository caveat. No code or dataset was executed. |

**Remaining validation:** inspect rendered EN/FR equations, figures, and navigation; verify all external links from the complete page; and review the detailed methods/results before making stronger claims about causal interventions or generalization across model families.

## Eleventh slice: SMDS figure-link accuracy in the bilingual linearity pages

A targeted inspection of the linked arXiv HTML source found that the existing “Figure 2” link was described as an example of a discovered circular feature, but Figure 2 is the method-comparison overview. Figure 3 presents the recovered feature geometries and is the appropriate target for the explanation mentioning circles.

| Area | Finding | Change | Remaining work |
|---|---|---|---|
| SMDS figure links in EN/FR | The source HTML caption identifies Figure 2 as “Feature Manifold Discovery and the Limitations of Previous Methods”; Figure 3 presents retrieved feature manifolds. | Updated both language pages to point to Figure 3 and revised the link label to describe the broader set of feature geometries rather than implying Figure 2 itself is a circular-feature example. | Confirm the anchor in the rendered browser and continue the full external-link sweep; this was a targeted link/content check, not a full visual audit. |

Source inspected: [arXiv HTML v1](https://arxiv.org/html/2510.01025v1). The official SMDS repository still labels its software experimental; no code or data were executed and no reproduction is claimed.


## Twelfth slice: update the supplementary probe-control resource link

A targeted external-link sweep found that the supplementary “Designing and Interpreting Probes with Control Tasks” link used an older Stanford-hosted path that could not be verified. The author's current page on the same topic is available at Columbia and explains probing, the probe-confounder problem, control tasks, and selectivity. The authoritative ACL Anthology paper link remains in the reference list.

| Area | Finding | Change | Remaining work |
|---|---|---|---|
| Supplementary probe-control resource (EN/FR) | The old `nlp.stanford.edu/~johnhew/probe-control/` URL could not be verified in this check. The author's current `Designing and Interpreting Probes` explainer is available at Columbia. | Replaced the supplementary link in both language pages with the current author-hosted explainer. The ACL Anthology paper remains the primary bibliographic reference. | Check the updated link in rendered pages; continue checking other external links. A failed retrieval from one tool is not, by itself, proof that the old URL is universally unavailable. |
| Other sources checked in this pass | The ICLR proceedings record, ACL Anthology record, relevant arXiv abstract pages, PMLR proceedings page, SMDS repository, and Transformer Circuits framework resource resolve or have searchable records matching their cited works. The arXiv v2 corrigendum page was not directly retrievable by the browser tool, but search results for arXiv:2603.28744v2 expose the updated abstract and corrigendum note. | No additional citation changes made in this pass. | This is a targeted availability/identity check, not a comprehensive automated HTTP status sweep. |

Sources checked: [author's current probing explainer](https://www.cs.columbia.edu/~johnhew/interpreting-probes.html), [ACL Anthology paper](https://aclanthology.org/D19-1275/), [ICLR 2025 paper](https://proceedings.iclr.cc/paper_files/paper/2025/hash/d3221cdb27e49d9c1cd35ad254feccfe-Abstract-Conference.html), [SMDS paper HTML](https://arxiv.org/html/2510.01025v1), and [official SMDS repository](https://github.com/UKPLab/tmlr2026-manifold-analysis).
## Thirteenth slice: apply the pedagogical-resource method to Q/K/V

This is a targeted source-level review of the bilingual Q/K/V concept pair, chosen because it already has a custom diagram and an established visual-explanation lineage. The purpose is to use external resources as design references—not to reproduce their prose or figures.

| Resource consulted as a design reference | What it can contribute | Guardrail for this page |
|---|---|---|
| [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) | Stepwise visual separation of the attention operations and data flow. | Keep the diagram's roles precise; do not let the analogy imply literal symbolic search. |
| [3Blue1Brown — Transformers](https://www.3blue1brown.com/lessons/gpt/) | Visual pacing and the distinction between scores, weights, and information flow. | Do not infer semantic meaning or causal explanation from attention weights alone. |
| [Distill](https://distill.pub/) | How a carefully scoped interactive explanation can expose a mechanism. | No interactive widget is needed unless it answers a concrete question better than a static example. |
| [Vaswani et al. (2017)](https://arxiv.org/abs/1706.03762) | Primary technical grounding for scaled dot-product attention. | Use the paper to check the mechanism and equations, not as evidence for every later implementation detail. |

| Area | Finding | Change made | Remaining validation |
|---|---|---|---|
| French/English pedagogical parity | The English page had a card-index analogy while the French page did not; neither page had a small numerical example isolating weights from values. | Added the equivalent card-index analogy to French and a matched toy calculation in both languages: scores \((0,\ln 3)\), softmax weights \((0.25,0.75)\), values \((2,10)\), output \(8\). Explicitly labels scalar values as a toy simplification. | Render both pages; verify the math and decimal notation display correctly. |
| Visual interpretation | Both pages already contain original diagrams. The current task did not justify replacing them with copied external assets or adding an animation. | Preserve the original diagrams and add a worked example to complement, not duplicate, the visual flow. | Inspect both SVGs at desktop/mobile widths; verify labels, contrast, alt text, and the diagram's distinction between score computation and value aggregation. |
| Source provenance | The existing references page does not clearly catalogue the Q/K/V diagrams as original project assets. | Record the bilingual Q/K/V diagrams in the visual-provenance page. | Confirm the relative image paths and the rendered references page. |

**Scope of this pass:** source-level review and proposed text changes only. No Quarto render, browser-based responsive review, or numerical test has been run in this step. Do not mark the page pair fully audited until those checks pass.

## Fourteenth slice: add a complementary visual perspective to cross-entropy

**Learner problem:** readers can manipulate the formula \(-\log p(y)\) without developing an intuition for how strongly the loss reacts to a lower probability assigned to the observed token.

**Resources and roles**
- [3Blue1Brown — But what is cross-entropy?](https://www.youtube.com/watch?v=GlYgs6v2YfU): visual intuition and narrative pacing.
- [PyTorch CrossEntropyLoss documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html): implementation-specific behavior; not a substitute for the mathematical definition.
- Shannon (1948) and Cover & Thomas: information-theoretic context for entropy and cross-entropy.

| Area | Finding | Change made | Remaining validation |
|---|---|---|---|
| Intuition | The existing page derived the loss and mentioned confident errors, but did not give a visual comparison for the same target under different predicted probabilities. | Added separate original English and French SVGs comparing \(p(y)=0.9\) and \(p(y)=0.1\), with losses about 0.105 and 2.303 nats, to the matching language pages. | Verify the numerical labels, visual scaling, and responsive rendering. |
| Complementary angle | Cross-entropy is not the entropy of the model distribution and does not tell us whether a target is factually true. It scores the probability assigned to a target distribution/token. | The text says explicitly that the figure concerns one token with a one-hot target and does not depict the full vocabulary distribution, valid-token reduction, or full training objective. | Check the text does not duplicate or contradict the separate entropy page; add a contextual cross-link if useful. |
| Provenance | An external video provides teaching inspiration but the diagram is authored for this repository. | Recorded the original SVG and its intended scope in the references page. | Check the relative path and the generated HTML figure. |

**Validation status:** source-level review only. No Quarto render, screenshot review, or automated SVG accessibility check has been run for this change.

## How to use this evidence log

1. **Find the dated audit that matches the page, source, or claim.** Its scope is limited to the objects and checks it explicitly names; do not generalize a sample to the whole site.
2. **Resolve current page ownership and destination** in [content-section-mapping.md](content-section-mapping.md), not by inferring them from an old audit row.
3. **Apply the shared review method** in [reader-experience-and-editorial-method.md](reader-experience-and-editorial-method.md) and the relevant page archetype guidance in [page-template-guide.md](page-template-guide.md).
4. **Resolve current work and status in GitHub.** The principal owners are:
   - [#130](https://github.com/JM-Brun/llm-lab/issues/130): high-level learning-design coordination;
   - [#280](https://github.com/JM-Brun/llm-lab/issues/280): incremental page-archetype convergence;
   - [#78](https://github.com/JM-Brun/llm-lab/issues/78): Build sequence and implementation evidence;
   - [#1512](https://github.com/JM-Brun/llm-lab/issues/1512): separation of learning and practice pages;
   - [#756](https://github.com/JM-Brun/llm-lab/issues/756): external learning-source portfolio;
   - [#584](https://github.com/JM-Brun/llm-lab/issues/584) and [#988](https://github.com/JM-Brun/llm-lab/issues/988): reader-facing rendering/accessibility and navigation contracts;
   - [#447](https://github.com/JM-Brun/llm-lab/issues/447): independent learner evidence.
5. **Keep evidence types separate:** source inspection, scientific/numerical verification, code and unit tests, Quarto/rendered-link checks, browser/responsive/accessibility review, and learner observation answer different questions. A result in one category does not certify another.
6. **Turn only confirmed defects into work.** Update the existing owning issue where possible. Do not create a second page inventory, opportunity register, generic checklist, workflow, or issue merely to restate a finding.

When new evidence supersedes an older observation, preserve the historical record and add a concise dated reconciliation with a link to the current owner/evidence. Do not silently rewrite an old audit as though the newer check had been performed at the time.

## What this evidence log does not claim

- It is not a complete audit of every page in the repository.
- Source inspection is not a rendered Quarto review.
- A cited source is not proof that every sentence on the page is correct.
- A planned test is not an executed test.
- Publication, CI, or completing an exercise does not by itself demonstrate learner mastery.




## Tensor axes and cross-domain semantics

| Page / language pair | Role and reader question | What this pass changed | Remaining work |
|---|---|---|---|
| `site/fr/tensors.qmd` + `site/en/tensors.qmd` | **Foundations / debugging invariant.** How can a tensor operation be shape-compatible but semantically wrong? | Proposed in branch `docs/tensor-axis-semantics-cross-domain`: a bilingual counterexample for softmax over vocabulary versus sequence positions; a concrete invariant (probabilities sum to one over the vocabulary axis per batch-position); optional bridges to signal processing, tabular schemas, mathematical tensors in physics/geometry, and probability/information theory. The cross-domain section explicitly marks these as optional and keeps LLM Lab self-contained. | Verify numerical statements and bilingual parity; run Quarto render and local-link checks; inspect rendered code/math and responsive behavior. Check the external NumPy link. No CI or rendered-site validation is claimed by this source edit alone. |

**Editorial rule reinforced by this change:** cross-domain links should explain a transferable idea and its limits, not just name an adjacent discipline. Candidate deeper concepts can later be developed as independent knowledge pages; public LLM Lab should not depend on private notes or on those future pages.


## Chapter 3 source pass: attention mechanisms (2026-10-29)

| Page / pair | Confirmed in source | Remaining work |
|---|---|---|
| `site/en/queries-keys-values.qmd` + FR counterpart | Learned Q/K/V projections and the match-versus-aggregate distinction; implementation status is not overstated. Multi-head behavior is mentioned as a future contract, not as an existing implementation. | Validate exact shape conventions and gradient behavior when the prerequisite-gated implementation work begins; route architecture-level multi-head reshaping to #98. |
| `site/en/scaled-dot-product-attention.qmd` + FR counterpart | Four-step computation, (QK^T), scaling by (sqrt{d_k}), row-wise softmax, additive mask convention, weighted aggregation, numerical example and implementation-status caveat. | Recheck rendered equations and diagrams; #80 owns tested invariants and any implementation. |
| `site/en/causal-masking.qmd` + FR counterpart | Autoregressive access constraint, additive mask, API-specific boolean polarity and explicit statement that the page is not an end-to-end causal proof. | #81 owns future-token perturbation and boundary/broadcasting tests; keep causal, padding and loss masks distinct. |
| `site/en/tensors.qmd` + FR counterpart | Batch/sequence/feature and vocabulary shapes, head dimension notation, axis pitfalls. | Add no duplicate general tensor lesson. The multi-head reshape/transpose contract belongs in #98 or #80 once scope is agreed. |

**Upstream scope checked:** Raschka Chapter 3 README and main notebook; the bonus folders for efficient multi-head variants and PyTorch buffers were also inspected. No dedicated multi-head or dropout page was found among the candidate paths checked. This is a bounded source audit, not a full browser/render review. The Quarto workflow for merged PR #110 passed both site rendering and rendered local-link checks; visual/mobile review remains separate.

## Chapter 4 source pass: GPT model architecture (2026-10-29)

| Page / pair | Confirmed in source | Remaining work |
|---|---|---|
| site/en/transformer.qmd + FR counterpart | System-level GPT data flow, block roles, residual paths/MLP at overview level, logits and autoregressive generation. | Keep as a concise canonical overview. Improve links to focused concepts; do not expand it into an implementation manual. |
| Q/K/V, scaled attention and causal masking pages + FR counterparts | Single-head attention mechanics and causal access constraints are explained conceptually. | Architecture-level multi-head split/transpose/concatenate/output projection remains partial and is owned by #98; single-head invariants and leakage tests remain #80/#81. |
| Embedding-space and positional-encoding pages + FR counterparts | Learned representations and positional mechanisms are discussed as concepts. | Explicit GPT-style token-embedding plus learned absolute-position-embedding shape contract remains partial; #82 owns the concept-level treatment. |
| site/en/tensors.qmd + FR counterpart | General batch, sequence, feature and vocabulary axis literacy. | No full GPT forward-pass trace or parameter-count derivation found in the checked pages. Avoid repeating general tensor material. |
| Architecture configuration, parameter tying, dropout/train-eval semantics | Upstream Chapter 4 notebook includes these topics; no complete tested public contract found in the candidate pages. | Record as gaps for a future prerequisite-gated implementation. Distinguish dropout from masking and architecture-specific choices from universal Transformer properties. |

**Upstream scope checked:** [Raschka Chapter 4](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04), its [main-code folder](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/01_main-chapter-code), and [main notebook](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch04/01_main-chapter-code/ch04.ipynb). This is a bounded source audit, not a browser/render review or evidence of learner mastery. Optional KV cache, performance comparisons, MoE, GQA and MLA remain outside the baseline path.


## Active text-to-embedding slice: PR #118 and #120 validation

**Scope:** [#82](https://github.com/JM-Brun/llm-lab/issues/82), coordinated by [roadmap #78](https://github.com/JM-Brun/llm-lab/issues/78). This remains the active slice; later attention, model and training implementations remain deferred.

| Check | Evidence | Status / limitation |
|---|---|---|
| One consistent input across text, tokenizer IDs and embedding lookup | [PR #118](https://github.com/JM-Brun/llm-lab/pull/118), merged at `50734b1f74bc1778431ec255861489223be4c2d0`; EN and FR embedding-space pages trace `hello world` through UTF-8, GPT-2 `tiktoken` IDs `[31373, 995]`, token byte fragments, synthetic embedding rows and illustrative absolute-position addition. | Source content present. Real tokenizer IDs are distinguished from synthetic embedding/position values; no claim is made that the example loads GPT-2 weights or computes contextual states. |
| Exact bilingual snippet execution | [PR #120](https://github.com/JM-Brun/llm-lab/pull/120), merged at `28ae31a075f8318705933e262bf6bbd944e9a6d9`. `scripts/check_embedding_trace.py` extracts the real fenced Python blocks from both Quarto sources, compares their executable ASTs (allowing translated comments), and executes both. | **Passed** in [Python CI run 40899831246](https://github.com/JM-Brun/llm-lab/actions/runs/40899831246), using the docs-only pin `tiktoken==0.14.0`. No runtime dependency was added. |
| Python quality checks | [Run 40899831246](https://github.com/JM-Brun/llm-lab/actions/runs/40899831246). | Passed: documentation dependency installation, execution of both examples, formatting, lint, type checking and tests; the complete job concluded successfully. |
| Quarto render and local links | [Run 40899831524](https://github.com/JM-Brun/llm-lab/actions/runs/40899831524). | **Passed**: bilingual site render and rendered local-link check. This is not a browser-based visual/responsive review. |
| Exact tokenizer behavior and assumptions | The example executes against the pinned `tiktoken` release; expected IDs/fragments were also cross-checked against the official [tiktoken encoding tests](https://github.com/openai/tiktoken/blob/main/tests/test_encoding.py). | The code proves the documented GPT-2 encoding for this exact input in the pinned environment. It does not validate every tokenizer family, Unicode normalization policy, or model embedding weights. |
| Browser / responsive review | Attempts to retrieve the deployed EN/FR pages through the available browser route were not successful. | **Not verified.** Inspect both languages and figures at desktop and mobile widths when browser access is available. |
| External-reference audit | Checked the identity and relevance of the five listed papers/documentation references (Mikolov et al. 2013; Ethayarajh 2019; Li et al. 2020; Steck et al. 2024; Sentence Transformers STS docs). The `hello world` IDs are confirmed by the official `tiktoken==0.14.0` test file; both EN/FR links now target that version tag rather than `main`. | Targeted reference spot-check passed. The suggested video remains explicitly unverified; browser-based page/figure review remains open. |
| Learner mastery | No learner diagnostic has been administered for this slice. | Not assessed; do not infer mastery from content, CI or publication. |

### Remaining checks before closing #82

- [ ] Inspect deployed EN/FR pages and figures at desktop/mobile widths.
- [ ] Finish a targeted external-reference and version-claim audit for tokenizer/Unicode/embedding material.
- [ ] Keep technical correctness, code execution, CI/render, browser review and learner mastery as separate statuses.

The successful #120 runs supersede earlier comments that said the embedded example had not been executed. Do not mark browser review or learner mastery complete based on these runs, and do not advance later curriculum slices until the active chain has been reviewed and its remaining acceptance criteria are met.


## Tokenization-to-embedding source audit — first pass (2026-10-29)

**Scope:** source-level checks for claims supporting the active [text → token IDs → embeddings issue #82](https://github.com/JM-Brun/llm-lab/issues/82) and the tokenizer evaluation/resource scope in [#114](https://github.com/JM-Brun/llm-lab/issues/114). The external pages below were opened and their relevant sections checked on 2026-10-29. This is a bounded first pass, not completion of the larger source inventory in [#114](https://github.com/JM-Brun/llm-lab/issues/114).

| Source | Concepts actually supported by the source | LLM Lab mapping and disposition | Status / caveat |
|---|---|---|---|
| OpenAI, [tiktoken encoding tests](https://github.com/openai/tiktoken/blob/main/tests/test_encoding.py) | The public GPT-2 encoding test asserts that encoding “hello world” gives IDs [31373, 995] and decoding returns the original text. | Keep the exact IDs in the bilingual worked trace; use the pinned tiktoken 0.14.0 execution check to catch drift in the installed version. | **Checked.** The GitHub main URL is mutable, so CI execution of the pinned package is the reproducible check; the upstream test is corroborating evidence, not a version pin. |
| Hugging Face LLM Course, [Byte-Pair Encoding tokenization](https://huggingface.co/learn/llm-course/en/chapter6/5) | Explains BPE merge learning, the distinction between tokenizer training and applying a trained tokenizer, and byte-level BPE's use of bytes to cover arbitrary text. | Keep BPE training and encoding distinct in the text-data lesson; use this as an accessible complementary explanation, not as the source for exact GPT-2 IDs. | **Opened and relevant.** This is the BPE lesson; the full normalization/pre-tokenization and tokenizer-family lessons need their own pass. |
| PyTorch, [torch.nn.Embedding API](https://docs.pytorch.org/docs/2.15/generated/torch.nn.Embedding.html) | Defines an embedding as a lookup table mapping integer indices to rows and documents input/output shapes. | Supports the claim that token IDs index embedding rows; it does not support synthetic numeric values or imply that lookup contextualizes tokens. | **Opened and relevant.** The stable URL redirected to versioned documentation; the versioned page was accessible. The public example remains NumPy-only and does not need PyTorch as a dependency. |
| Su et al., [RoFormer / RoPE](https://arxiv.org/abs/2104.09864) | The primary paper describes rotary position embedding: absolute positions are represented through rotations, with relative-position dependence incorporated into self-attention. | Supports the distinction between adding learned absolute position vectors to token embeddings and applying RoPE to query/key vectors inside attention. | **Primary source checked.** The current page gives a conceptual contrast; a detailed derivation is intentionally deferred. |
| Ethayarajh (2019), [How Contextual are Contextualized Word Representations?](https://arxiv.org/abs/1909.00512) | Empirically studies contextualized representations in ELMo, BERT, and GPT-2; reports context dependence and non-isotropy in the examined models/layers. | Supports the distinction between a static token embedding and context-dependent hidden representations. The bank SVG is an original conceptual illustration, not data reproduced from the paper. | **Primary paper checked.** Do not attribute the illustration's specific example or vectors to the paper; its evidence is empirical and model-/layer-scoped. |
| Ahia et al. (2023), [Do All Languages Cost the Same?](https://aclanthology.org/2023.emnlp-main.614/) | Studies token-count variation and API cost/utility across 22 languages and reports that some language communities face higher token usage and poorer results in the evaluated commercial APIs. | Supports the page's motivation to measure multilingual tokenization costs and utility separately. | **ACL abstract checked.** Findings concern the evaluated models, APIs, languages and benchmarks; don't present them as a universal or current price comparison for every provider. |
| Ali et al. (2024), [Tokenizer Choice For LLM Training: Negligible or Crucial?](https://aclanthology.org/2024.findings-naacl.247/) | Reports experiments training 24 mono-/multilingual LLMs at 2.6B parameters and finds tokenizer choices can affect downstream performance and training cost; fertility/parity do not always predict downstream quality. | Supports the warning that intrinsic metrics and token counts are not substitutes for task evaluation. | **ACL abstract checked.** Preserve the experiment's scale and setup when describing results; do not generalize its numerical cost claims to every model size or training recipe. |
| Wegmann et al. (2025), [Tokenization is Sensitive to Language Variation](https://aclanthology.org/2025.findings-acl.572/) | Studies BPE design choices (training corpus, pre-tokenizer, vocabulary size) and distinguishes tasks that should be robust to linguistic variation from tasks where surface variation matters. | Supports examples involving spelling variants and the statement that tokenizer settings can affect downstream behavior, not merely sequence length. | **ACL abstract checked.** The finding that pre-tokenization had the largest overall impact is specific to the study's BERT-base experiments and evaluated tasks. |
| Arnett et al. (2025), [Explaining and Mitigating Crosslingual Tokenizer Inequities](https://papers.nips.cc/paper_files/paper/2025/hash/5b91cefbfa52340af2f16f249572dc76-Abstract-Conference.html) | Studies token premiums across roughly 7,000 monolingual tokenizers and 97 languages; reports effects associated with vocabulary size and pre-tokenization, and evaluates superword tokenizers. | Supports discussion of cross-lingual fragmentation and the need to measure language-specific costs; complements API-focused work with tokenizer-design experiments. | **NeurIPS abstract checked.** Results are tied to the paper's tokenizer experiments and definitions; do not collapse token premium, model quality, and commercial price into one metric. |
| Chiu (2026), [TokLens: A Multilingual Lens on Tokenizer Quality for LLMs](https://aclanthology.org/2026.acl-srw.18/) and [toolkit repository](https://github.com/guan404ming/toklens) | Introduces six intrinsic metrics and studies 24 tokenizers across 15 languages; its abstract reports different relationships between intrinsic metrics and English versus multilingual benchmark results. | Supports the page's caution that no single intrinsic metric is a universal quality proxy, while providing a candidate tool for future controlled comparisons. | **ACL-SRW abstract and repository summary checked.** Reported relationships include correlations and may be confounded by pretraining data; do not infer causality or generalize a headline token-ratio to every tokenizer/version. |
| Li et al. (2020), [On the Sentence Embeddings from Pre-trained Language Models](https://aclanthology.org/2020.emnlp-main.733/) | The ACL Anthology abstract discusses sentence embeddings from pretrained BERT, their anisotropic geometry, and their performance on semantic-textual-similarity tasks. | Retain as context for the distinction between token-level and sentence/document embeddings, and for why a pretrained contextual model's raw sentence representations may not be ready-made semantic sentence vectors. | **Abstract and bibliographic metadata checked.** The paper is specifically about BERT sentence embeddings and BERT-flow; do not generalize its empirical finding to every model or all token-level embeddings. |
| Steck, Ekanadham & Kallus (2024), [Is Cosine-Similarity of Embeddings Really About Similarity?](https://arxiv.org/abs/2403.05440) | Analyzes when cosine similarity on embeddings can be misleading in regularized linear models and cautions against assuming it always measures semantic similarity. | Supports caution against treating cosine similarity as universal semantic truth. Keep the scope caveat: the paper's formal analysis is not a proof that every embedding model behaves identically. | **Primary paper checked.** It motivates caution, not a universal ranking of cosine, dot product and Euclidean distance. |
| Sentence Transformers, [Semantic Textual Similarity](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html) | Shows encoding sentence pairs and computing similarity; documents cosine, dot product, Euclidean and Manhattan options and notes the equivalence between dot product and cosine for normalized vectors. | Supports the distinction between task-trained sentence embeddings and internal token representations, and the need to choose metrics based on model/task conventions. | **Official documentation checked.** Its examples concern Sentence Transformers; do not generalize their scores to GPT-2 hidden states. |
| OpenAI, [tiktoken repository README](https://github.com/openai/tiktoken) | Describes the library as a BPE tokenizer for OpenAI models and documents API entry points for named encodings and model-to-encoding selection. Its README performance comparison explicitly names older package versions. | Supports using tiktoken as the named GPT-2 encoding source in the worked trace; avoid repeating performance claims without reproducing the benchmark under current versions. | **README checked.** No third-party code or performance figure is copied. The exact behavior used in LLM Lab is covered by PR #120's pinned execution. |
| Karpathy, [minbpe educational implementation](https://github.com/karpathy/minbpe) | README distinguishes training, encoding and decoding and points to minimal byte-level BPE implementations; repository includes an MIT license. | Good optional code-reading resource if a learner later needs to inspect BPE training/encoding internals. It is not needed to understand the current text-to-embedding example. | **README and MIT license checked; implementation not executed or line-by-line reviewed.** Link rather than copy code in this pass. |
| Hugging Face, [Tokenizers library](https://github.com/huggingface/tokenizers) | Official library for fast tokenizer implementations, with a public README and API/documentation links; repository includes an Apache 2.0 license. | Supports the practical learning path for normalization, pre-tokenization, tokenizer training and encoding pipelines. | **README and license checked; detailed API/source review deferred.** The library's own speed claims are not independent comparative evidence and are not repeated in LLM Lab. |
| Google, [SentencePiece](https://github.com/google/sentencepiece) | Repository describes SentencePiece as a tokenizer that can train from raw text and supports BPE and Unigram-style models; repository includes an Apache 2.0 license. | Supports the page's caveat that SentencePiece is a tokenizer library/framework and is not synonymous with the Unigram algorithm. | **README and license checked.** No code or images copied; model-specific configuration still matters. |
| Sennrich, Haddow & Birch (2016), [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) | Primary paper for using BPE-derived subword units in neural machine translation to address rare and unknown words; it is not a specification of GPT-2's byte-level tokenizer. | Supports the historical bridge from compression BPE to subword segmentation in NLP, while keeping GPT-2 byte-level details sourced to its own implementation/tests. | **arXiv abstract checked.** Do not cite this paper alone for byte-level BPE, current LLM tokenizer conventions, or universal performance claims. |
| Gage (1994), [A New Algorithm for Data Compression](https://dl.acm.org/doi/10.5555/177910.177914) | Historical primary source for byte-pair encoding as a general-purpose byte-compression algorithm. The accessible [reconstructed PDF copy](https://www.derczynski.com/papers/archive/BPE_Gage.pdf) states that frequent adjacent byte pairs are replaced with unused byte values and discusses compression/expansion tables and implementation constraints. | Supports historical provenance and the distinction between compression BPE and later subword-tokenizer adaptations. It does **not** specify GPT-2's byte-level BPE tokenizer or modern text pre-tokenization rules. | **Full text reviewed via a reconstructed PDF copy**, which notes it was reconstructed from the original C Users Journal HTML in 2020; the publisher page itself still returned 403. Treat detailed historical claims as grounded in this copy, not as direct verification of the publisher-hosted original. |
| Karpathy, [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) | The video metadata and chapter list identify a practical walkthrough covering Unicode/UTF-8, BPE training, pair counting and merging, GPT-2 regex pre-tokenization, encoding/decoding and special tokens. A [third-party transcript generated from public captions](https://youtube2text.diguardia.org/v/let-s-build-the-gpt-tokenizer-zduSFxRajkE) was inspected at the relevant timestamped sections. | Useful as an optional practical companion, especially for the sequence from text/bytes to tokens and the difference between training BPE merges and applying a trained tokenizer. Treat broad statements about tokenization causing model failures as the presenter's framing, not as universal causal evidence. | **Metadata, chapter list and relevant transcript sections checked; the video itself was not watched end-to-end.** Transcript is third-party caption-derived, so transcription errors are possible. Keep optional; cite exact timestamps only after checking the video directly if a page makes a precise claim. |
| Raschka, [Chapter 2 code notebook](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch02/01_main-chapter-code/ch02.ipynb) | Targeted cell-level review of the current Chapter 2 notebook: §§2.2–2.5 / cells 12–77 cover a didactic regex tokenizer, vocabulary-to-ID mapping, special/unknown tokens and the GPT-2 `tiktoken` encoding; §§2.7–2.8 / cells 103–137 demonstrate `torch.nn.Embedding`, row lookup, batch tensor shapes, and learned absolute position embeddings added to token embeddings. | Useful as a practical cross-reference for the active chain. The simple regex tokenizer is a teaching scaffold, not a GPT-2-compatible tokenizer; the `tiktoken` GPT-2 encoding is a distinct implementation. The notebook's positional example uses learned absolute position embeddings, not RoPE, and stops before contextualization by Transformer blocks. The LLM Lab synthetic lookup example is not a port of this notebook. | **Targeted cell mapping reviewed from source (notebook cells 12–77 and 103–137); notebook was not executed end-to-end.** No copied code or figures. No detailed mapping was done for §§2.6/2.9 or later training topics because those are outside the current #82 scope. |
| Hugging Face community article, [Visualize the encoding process in a BPE tokenizer](https://huggingface.co/blog/SauravP97/bpe-tokenizer-visualize) | Describes a Graphviz-based visualization of how a pretrained GPT-2 tokenizer encodes text, reports the same “hello world” IDs, and requires a separate community package plus Transformers/Graphviz dependencies. | Could complement the BPE-training visualizer by showing an encoding trace from a trained tokenizer, but is not needed for the already-executable compact example. | **Article opened; community code not executed or dependency-audited.** Keep as an optional reference only; do not copy its figure or claim reproducibility without testing the package/version and dependency chain. |
| Hugging Face, [Tokenization algorithms](https://huggingface.co/docs/transformers/main/en/tokenizer_summary) | Summarizes BPE, WordPiece and SentencePiece/Unigram; explicitly distinguishes the pair-frequency criterion of BPE from WordPiece's likelihood-derived merge score, and describes SentencePiece's treatment of raw text and whitespace markers. | Use as the cross-family reference for the tokenization-strategy page; keep the simplified algorithm descriptions scoped to each family. | **Opened and relevant.** The page is broad and should complement, not replace, each algorithm's primary/official documentation. |
| Müller & Steinbach, [BPE Explainer](https://philipmueller.dev/bpe-visualization/) and [source repository](https://github.com/muelphil/bpe-explainer) | Interactive, step-by-step BPE training visualization with token merges, pair frequencies, vocabulary growth, and a switch between original compression BPE and an LLM-adapted variant. | Best candidate among the two named visualizers for a linked optional activity focused on BPE training mechanics. Keep it external; do not duplicate its visualization in LLM Lab. | **Live page and repository inspected.** No root LICENSE file was found in the checked repository paths; treat reuse rights as unverified and link externally rather than copying its assets/code. Its training visualization is not a substitute for demonstrating a particular pretrained tokenizer's encoding output. |
| Cornell CS4782, [Interactive Tokenization Visualizer](https://www.cs.cornell.edu/courses/cs4782/2026sp/demos/bytepair/) | Offers a step-by-step BPE/WordPiece comparison, current vocabulary, candidate merges, and tokenization of new input. | Potentially useful for comparing the algorithms, but not the first-choice recommendation until its displayed state is reliable. | **Page reachable; quality caveat observed and surfaced in both EN/FR public resource lists:** the current page snapshot displays “Frequency: undefined” for the highlighted merge while listing frequencies in the candidate-pair panel. A dated caveat was added to the text-data and tokenization-strategies pages in both languages. Recheck the live tool later and remove the caveat only when the discrepancy is confirmed fixed. |

### Visuals and reuse decision

- The Unicode/UTF-8, BPE trace, embedding-space and contextualized-embedding figures in LLM Lab are project-authored SVGs. Their alt text describes the intended lesson and identifies illustrative rather than measured content where relevant.
- The English tokenization-strategies page previously linked to the French Hugging Face BPE lesson. It now links to the English lesson; the French page continues to link to the French counterpart. This is a language-navigation correction, not a change to the technical explanation.
- The external sources above are linked for learning and attribution; this pass did **not** copy external diagrams or code assets into the site.
- The Müller–Steinbach BPE Explainer and Cornell CS4782 visualizer have now been inspected at the content/output level. Prefer the BPE Explainer as an external optional resource for BPE training mechanics; link only because reuse rights were not verified. Treat Cornell's visualizer as provisional because the displayed merge frequency is inconsistent in the current page snapshot. Neither inspection is a responsive-browser review.
- A live link being reachable is not the same as confirming its scientific support for every nearby sentence. The rows above explicitly separate those statuses.

### Remaining work for this source audit

1. Gage (1994), relevant Karpathy tokenizer transcript sections, and Raschka Chapter 2 cells 12–77 and 103–137 are now reviewed within the limits recorded in their rows above. Do not describe the Karpathy video as watched end-to-end, the reconstructed Gage PDF as the publisher-hosted original, or the Raschka notebook as executed end-to-end. Remaining source work is limited to assessing the Hugging Face community visualizer's package provenance/dependencies if it is to be promoted beyond an optional link.
2. Inspect the published EN/FR embedding-space pages and SVGs at desktop and mobile widths. Text extraction and a successful Quarto build do not establish responsive visual quality.
3. The Li et al. sentence-embedding abstract is checked. Targeted Raschka cell mapping is now recorded above; do not expand into later notebook sections unless an active-page claim requires it.
4. If the HF community visualization is considered for recommendation, check its package provenance, versioning, dependency chain and current execution before promoting it beyond an optional link.
5. Keep browser review and learner mastery open in #82; do not close it based on source review or CI alone.


## Fourth slice: Hugging Face LLM Course — tokenizer chapters (source-by-source review)

**Scope reviewed:** the official Hugging Face course pages for BPE, WordPiece, Unigram, and building a tokenizer block by block, compared with the current English and French tokenization-strategies.qmd pages. This is a source/content comparison, not a claim that every code cell in the course was executed.

| Source section | Concepts actually covered by the source | LLM Lab coverage (EN/FR) | Assessment / remaining gap |
|---|---|---|---|
| [BPE training and encoding](https://huggingface.co/docs/course/chapter6/5) | Initial alphabet after normalization/pre-tokenization; corpus word frequencies; frequency-weighted adjacent-pair counts; iterative merges and vocabulary growth; merge-order encoding; unknown-symbol behaviour; byte-level BPE's 256-byte base; tie-breaking differences between a didactic implementation and the library. | The worked low / lower / lowest trace explains pair counting, merging, vocabulary growth and a tie. The page explicitly marks its example as word-level with an end-of-word marker and distinguishes it from byte-level production tokenizers. It explains byte-level coverage, OOV implications, merge order and implementation-specific tie-breaking. The BPE training/encoding distinction is also explicit. | **Explained with a deliberate simplification.** The local worked example gives each word one occurrence, so it does not demonstrate weighting pair counts by corpus word frequencies. The source's weighted example and code are not reproduced. This is acceptable for the conceptual page, but the source audit should preserve the distinction and not claim a full reproduction of the HF implementation. A future implementation exercise can cover weighted counts and tie-breaking after the prerequisite concept is acquired. |
| [WordPiece](https://huggingface.co/docs/course/chapter6/6) | Word-initial versus continuation symbols; ## convention; likelihood-related pair score; explicit uncertainty because Google's original trainer is not open; final-vocabulary encoding by greedy longest-match-first; whole-word [UNK] fallback in the described implementation. | The page gives the score formula, explains its interpretation relative to BPE frequency, explicitly caveats that the original Google training procedure is not publicly specified and HF's account is a reconstruction, then explains greedy longest-match-first, ##, and a BERT-style whole-word [UNK] fallback. | **Explained with appropriate caveats.** The site does not reproduce the full training implementation, but it does not present the reconstructed formula as a universal or definitive specification. No correction currently justified. |
| [Unigram](https://huggingface.co/docs/course/chapter6/7) | Candidate vocabulary built from substrings or a large initial BPE vocabulary; token probabilities; probability of a complete segmentation; Viterbi search; loss as negative log-likelihood over corpus words; iterative vocabulary pruning by the effect of removing candidates; SentencePiece's more efficient approximations and initial-vocabulary construction. | The page describes a probabilistic candidate-subword model, vocabulary pruning by the smallest increase in loss, Viterbi decoding, and the distinction from ranked BPE merges and WordPiece greedy matching. | **Core algorithm explained; training details selectively covered.** The page does not reproduce HF's worked probability calculations, corpus-level NLL example, or the approximation used by SentencePiece to score token removal. These are implementation-depth details rather than a conceptual error. Keep them as a possible later practical extension, not as a reason to enlarge the introductory explanation now. |
| [Building a tokenizer, block by block](https://huggingface.co/docs/course/chapter6/8) | Construction of a Tokenizer from a model plus configurable normalizer, pre-tokenizer, post-processor and decoder; concrete code for configuring components and training. | The site defines these pipeline components in a table, explains their separate roles, shows outputs from different configurations, and discusses offsets and special-token handling. It does not yet provide a full from-scratch construction of a Hugging Face Tokenizer object. | **Conceptual pipeline explained; construction implementation not covered.** This is a real boundary in current coverage, not a missing definition. Keep it visible in the learning map; defer an implementation exercise until the prerequisite component concepts are acquired. |
| [SentencePiece / Unigram discussion](https://huggingface.co/docs/course/chapter6/7) | SentencePiece accepts raw input streams rather than requiring whitespace-delimited words; whitespace can be represented in the vocabulary (visible ▁ convention in examples); Unigram is one supported model family, not the whole library. | The site correctly says SentencePiece can train BPE or Unigram and distinguishes it from an algorithm. The examples explain ▁ as a visible boundary marker and compare tokenizer outputs. | **Mostly explained; one nuance should remain explicit.** Avoid implying that SentencePiece is synonymous with Unigram or that all SentencePiece configurations use the same whitespace conventions. Current wording does not make that mistake. The precise raw-stream/whitespace handling is not yet developed as a standalone concept. |

### Visual and reuse decision for this source

The Hugging Face course's tokenizer-pipeline illustration is already embedded remotely in both language versions of tokenization-strategies.qmd. Its exact asset path is recorded in upstream dataset commit [07e86fc](https://huggingface.co/datasets/huggingface-course/documentation-images/commit/07e86fc4f13286402333e65c52b7d9e8ea1293ea), attributed by the dataset UI to mishig (Hugging Face Staff); the dataset declares Apache-2.0. The course contribution instructions direct course authors to place chapter images in this repository. The exact upstream history and repository-level licence evidence are documented in the visual-assets register.

**Decision:** keep the existing remote illustration and attribution unchanged. It adds a pipeline-level visual not duplicated by the project's algorithm-specific worked examples. Repository-level Apache-2.0 evidence is strong, but the original illustrator and any third-party components have not been independently established. Do not copy or modify the figure locally as part of this audit.

### Overall finding

The current EN/FR tokenization guide covers the core conceptual distinctions in the four Hugging Face course sections. The main differences are deliberate depth boundaries: weighted BPE training counts, detailed Unigram loss/pruning calculations, and an executable library-level tokenizer construction are not fully reproduced. These should be treated as deferred practical extensions, not silently described as already implemented. No scientific correction to the current pages is required by this comparison alone.

**Validation boundary:** source files and the cited Hugging Face course pages were inspected; this pass did not execute the Hugging Face notebooks, perform a browser-based visual review, or validate desktop/mobile rendering.

## Focused source audit — Transformer Explainer integration (2026-10-30)

**Scope:** the integration and source-reading section in the French and English Transformer overview pages, checked against upstream commit [`bfe50af`](https://github.com/poloclub/transformer-explainer/commit/bfe50afba10b9b560b84143ee1107d977defa74f). This is a source-level review, not a browser-render or accessibility certification.

| Finding | Evidence inspected | Correction / remaining boundary |
|---|---|---|
| UI components were described as if they performed the model calculations. | `Embedding.svelte`, `QKV.svelte`, `AttentionMatrix.svelte`, `Mlp.svelte`, and `LinearSoftmax.svelte` render or expose the visual interface. | The bilingual overview now separates the visual component from the computation/data path. Q/K/V projections, attention, MLP, and embeddings are implemented in the PyTorch reference model (`model.py`); browser inference and tokenization are orchestrated through `data.ts` and ONNX Runtime Web. |
| The top-p caveat described an impossible condition for the restricted distribution. | `topPSampling` in `src/utils/data.ts` sorts logits, slices to 50, applies temperature, softmaxes those 50 values, computes cumulative probabilities, truncates, and renormalizes. | The explanation now states that top-p is computed over a distribution already restricted to 50 candidates. The omitted vocabulary tail cannot enter the selected nucleus; exact full-vocabulary top-p can therefore differ when its nucleus extends beyond those 50 candidates. |
| Upstream source links used the mutable `main` branch. | Upstream tree and relevant files were inspected at commit `bfe50afba10b9b560b84143ee1107d977defa74f`. | The source map now pins links to that commit so readers can reproduce the audit. Re-audit before relying on those implementation details after upstream changes. |

**Confirmed:** the repository has a PyTorch reference model, while the browser path uses an ONNX session; the two should not be conflated. **Not checked:** a fresh browser interaction, model download behavior, mobile layout, keyboard accessibility, or whether the upstream demo's runtime behavior still matches the pinned source snapshot.

**Numerical counterexample for the top-p limitation:** if the top 50 candidates contain 0.80 of the full-vocabulary probability mass and the requested threshold is 0.90, exact full-vocabulary nucleus sampling must include candidates beyond rank 50. The audited implementation renormalizes the top-50 subset to 1.00 first, so its cumulative threshold can be reached without considering the omitted 0.20 tail.


## Coverage reconciliation against the current sidebar — 2026-11-02

The existing [content-section mapping](content-section-mapping.md) classifies the reader-facing role of the site pages. That classification is useful for navigation design, but it is **not** evidence that each page has received the detailed source, language-parity, rendered, and responsive review required by this inventory.

A mechanical comparison of the two current sidebars in `site/_quarto.yml` against the detailed page entries above found **23 sidebar page entries not yet represented by a page-specific row in this audit inventory** (11 bilingual pairs plus the English landing page counterpart; the French landing page is the root `index.qmd`). These are recorded as **Not reviewed** below. This is a coverage gap, not a finding that the pages are defective.

| Canonical page pair / entry | Primary role from content map | Detailed audit status | Next bounded review |
|---|---|---|---|
| `index.qmd` / `en/index.qmd` | Entry point | Source-reviewed 2026-11-12; rendered/browser review pending | FR/EN route selection, status honesty, and entry affordances align; the interactive SVG figure is symmetric and keyboard-activatable in both languages. No substantive source-level correction identified. Three cosmetic observations recorded in the entry-point audit section (2026-11-12). Still inspect the published pages, the SVG interactions, and responsive behavior. |
| `site/fr/llm-overview.qmd` / `site/en/llm-overview.qmd` | Understand — system orientation | Source-reviewed 2026-11-02; rendered/browser review pending | FR/EN sections and learning checks align. The page distinguishes architecture from objective, model families from model scale, prompting/RAG from weight updates, and observed task competence from stronger claims about understanding. Sources have differentiated roles. No substantive source-level correction identified. Still inspect the published pages, Mermaid diagrams, links and responsive layout; verify #108 acceptance separately. |
| `site/fr/unicode-text.qmd` / `site/en/unicode-text.qmd` | Understand — supporting concept | Source-reviewed in opening-slice and optional-page audits (2026-11-02/03); rendered/code-example review pending | Existing audits confirm that this is an optional Deepen page, not a core prerequisite, and that it distinguishes code points, UTF-8 bytes and normalization without duplicating tokenization or embedding lessons. Reuse the recorded source evidence; remaining checks are return-link and rendered code-point/byte examples. |
| `site/fr/embedding-space.qmd` / `site/en/embedding-space.qmd` | Understand — concept | Source-reviewed 2026-11-02; rendered/browser review pending | FR/EN outlines, worked lookup, terminology and references align. The page correctly separates token IDs, initial token embeddings, contextualized states and sentence/document embeddings; synthetic values are labelled illustrative, and the real GPT-2 tokenizer trace is separately evidenced by PRs #118/#120. The 2D projection and similarity caveats avoid treating geometry as universal semantics. No substantive source-level correction identified. Still inspect equations, SVGs and responsive rendering; #82 remains the active content gate. |
| `site/fr/contextualized-representations.qmd` / `site/en/contextualized-representations.qmd` | Understand — concept bridge | Source-reviewed 2026-11-02; rendered/browser review pending | FR/EN explanations and equations align. The same-ID assumption is explicit; learned absolute position embeddings are distinguished from RoPE; the causal-decoder expression is scoped to preceding context and labelled conceptual. The external Rushang Chauhan figure's asset-level reuse review remains pending in #156 and is transparently disclosed on both pages. Still inspect SVG and external figure rendering, responsive behavior and links. |
| `site/fr/build-path.qmd` / `site/en/build-path.qmd` | Build — guided implementation route | Source-reviewed 2026-11-06; crosswalk updated in merged PR #598; G0–G9 evidence audit merged in PR #600 | The bilingual hub retains the tested NumPy inference reference and the G0–G9 implementation milestones. PR #598 clarifies the three sibling uses of the shared predictor, separates G9 reference verification from E1 task evaluation, and states that G8 validation uses fixed parameters. PR #600 reconciles milestone claims against source and tests. The implementation boundary remains unchanged: no complete training loop, optimizer, validation runner or checkpoint is claimed. |
| `site/fr/cosine-similarity.qmd` / `site/en/cosine-similarity.qmd` | Deepen — critical case study | Source-reviewed 2026-11-11; rendered/browser review pending | See the “Deepen case-study source audit” section (2026-11-11): geometric and semantic claims are kept distinct. Remaining work: rendered review and independent verification of the recent citations. |
| `site/fr/linearite-embeddings.qmd` / `site/en/embedding-linearity.qmd` | Deepen — research-oriented case study | Source-reviewed 2026-11-11; rendered/browser review pending | See the “Deepen case-study source audit” section (2026-11-11): representation, decodability and functional use stay distinct. Remaining work: rendered review and independent verification of the 2026 citations. |
| `site/fr/evaluation-experimentale.qmd` / `site/en/experimental-evaluation.qmd` | Practice & experiment — method | Source-reviewed 2026-11-12; targeted clarification proposed in PR | The exercise correctly distinguishes ranking from calibration, leakage-safe selection, paper-level grouping, winner's-curse bias and uncertainty limits. A material ambiguity was found in query-level AP aggregation (macro vs micro), the corresponding random baseline, and crossed paper/query dependence; see the dedicated audit entry below. Rendered review and independent execution of any proposed protocol remain open. |
| `site/fr/exercises.qmd` / `site/en/exercises.qmd` | Practice & experiment | Source-reviewed 2026-11-12; rendered/browser review pending | Honest catalogue hub with exact FR/EN parity: 33 per-lesson entries counted identically in both languages, published collections state counts and remaining work symmetrically, planned collections are not presented as published, and the Raschka no-copy contract is present in both. No claimed interactivity on the page itself. No substantive source-level correction identified; minor observations in the exercise-hub audit section (2026-11-12). Rendered review, link checks, and per-collection audits remain open. |
| `site/fr/glossary.qmd` / `site/en/glossary.qmd` | Reference | Source-reviewed 2026-11-12; rendered/browser review pending | Concise reference index with exact FR/EN parity: 61 entries in both languages (4/11/9/10/27 across the five thematic groups), no duplicate definitions, explicit disambiguations (decoding vs decoder vs incremental decode; the embedding family; width vs d_ff/d_head), correctly scoped claims (GRPO reward source left unspecified; reward model as learned proxy), and links to canonical pages on substantive entries. No substantive source-level correction identified; minor observations in the reference-pages audit section (2026-11-12). Rendered review and link checks remain open. |
| `site/fr/transformer-history.qmd` / `site/en/transformer-history.qmd` | Reference — optional history | Source-reviewed 2026-11-12; rendered/browser review pending | Chronology audited at the data layer (`data/history-pilot.yml`): 17 event records for 16 milestones, dates and attributions consistent with the cited primary sources, and per-event editorial notes that scope every claim (GPT-2 report not peer-reviewed; ChatGPT distinct from InstructGPT; no DPO lineage claim; Chinchilla not a universal ratio; FlashAttention keeps quadratic complexity). The page disclaims a single causal chain and is not presented as a prerequisite path (`suggested_route.next` null). The timeline include is a build-time generated artifact validated by `check_history_pilot.py` and `check_history_rendered.py`. No substantive correction identified; minor observations in the reference-pages audit section (2026-11-12). |

### Review protocol for these entries

- Review FR and EN as separate rendered pages, then compare the learning objective and claims side by side.
- Record source inspection, scientific verification, link/build checks, browser rendering, responsive behavior, and accessibility observations separately.
- Do not mark a page complete solely because its counterpart exists, the page appears in the sidebar, or Quarto CI passes.
- Prioritize the overview, build path, and embedding/contextualization bridge after the active #82 browser gate; then review optional deep dives and references.
- Keep this table as a gap register. Add a page-specific findings row only when the corresponding review has actually been performed.


### Source-level review notes — panorama, build path and representations (2026-11-02)

This pass reviewed the source files in both languages and cross-checked the build route against `docs/learning-path.md`, the editorial contract, and existing implementation/evidence references. It did **not** inspect the published pages in a browser.

| Page pair | Review result | Evidence boundary / remaining action |
|---|---|---|
| LLM panorama | The mental model is appropriately system-level. Architecture and training objective are separate axes; encoder-only, encoder–decoder and decoder-only families are examples rather than a quality ranking; prompting/RAG are distinguished from parameter adaptation; test-set leakage and limits of next-token prediction are stated. The EN/FR section structure and learning checks correspond. | Source-level review only. The panorama is published on `main` via merged PR #213. #108 acceptance and browser inspection remain open. |
| Guided build path | The route teaches only the mathematical operations needed at each point and clearly marks absent implementation evidence. Inference and learning are not conflated. The EN/FR milestone sequence and status claims align. | The causal perturbation criterion now explicitly requires evaluation mode / disabled dropout so stochastic dropout does not confound the comparison. This is a wording/acceptance-criterion correction, not evidence that the test has been implemented. |
| Embedding space | The worked lookup distinguishes row indices from learned vectors; synthetic matrices are not passed off as model weights. The page separates token embeddings, contextualized hidden states and sentence/document embeddings, and cautions against semantic overinterpretation of vector geometry. | Existing real-tokenizer trace and bilingual snippet execution are separately evidenced by PRs #118 and #120. No full GPT embedding stack is claimed. Browser inspection of equations and figures remains open. |
| Contextualized representations | The same-token-ID premise is explicit; positional embeddings and RoPE are not conflated; the causal-context equation is explicitly scoped and conceptual. The bilingual explanations are aligned. | The overview figure's asset-level permission review remains pending in #156. Do not treat publication or attribution as permission clearance. Browser review remains open. |

**Cross-document status correction:** `docs/learning-path.md` previously described the bilingual panorama as being on Draft PR #213. PR #213 was merged on 2026-11-02; the roadmap now records publication on `main` while keeping #108 acceptance and browser review pending. This is a status correction, not a closure of #108.

### Review-implementation pass — panorama, Transformer, Transformer Explainer, llm-limits (2026-11-03)

This pass applied the 2026-11-02 external review of the panorama and Transformer pages, merged via PR #248. It is a source-level change record; it is not a browser-render, accessibility, or acceptance certification.

| Page pair | What changed | Evidence boundary / remaining action |
|---|---|---|
| LLM panorama | Rewritten around the context → distribution → token loop: affirmative definition opens the page, single central Mermaid loop with edges, three-phase lifecycle, architecture families moved to a "for orientation" callout after the loop, numbered sections 1–10 with the expected-outcome callout and final checkpoint of #245/#246 integrated, quiz refocused, caveats grouped at the end. | Source-level and CI validation only. Rendered review of the Mermaid diagrams, nested-sets figure, table and callouts in both languages remains open, as does #108 acceptance. |
| New page `llm-limits.qmd` / `en/llm-limits.qmd` | Short critical companion of the panorama: what the next-token objective does not guarantee — truth of outputs, calibration, the meaning of "understanding", so-called emergent abilities, the role of scale. Sources verified: Wei et al. 2022 (arXiv:2206.07682), Schaeffer et al. 2023 (arXiv:2304.15004). | Source-level review only. Rendered review, sidebar placement and language-switch behavior to check on the published site. |
| Transformer overview | Diagram first, merged "first reading" callout, two-link continue section, Markdown defects fixed (fused list after the top-p formula, glued language-switch block in FR, four-colon fence in EN), entry-outcome callout and final checkpoint of #245/#246 integrated. | Source-level. Rendered figure, callout and checkpoint review remains open. |
| Transformer Explainer | The top-p audit is reframed as a documented design choice: upstream commit bfe50af truncates to 50 with an explicit display rationale, and top-k (Hugging Face default 50) then top-p composition is standard filtering. The page now states precisely what the composition computes instead of reporting a nonexistent defect. | Reframing verified against the pinned upstream commit. The external service and snapshot may change independently; browser review remains open. |

**Scope note:** the review's sidebar-reduction recommendation (30+ entries) is an editorial navigation decision, recorded here as open, not applied in #248.

### Review-implementation record — build-path rework in PR #285 (2026-11-03)

**Scope:** the bilingual build-path hub (`site/fr/build-path.qmd`, `site/en/build-path.qmd`) and its cross-document links, reworked in open PR #285. Source-level record; not a rendered-site, browser, or learner-mastery review.

| Area | Change in PR #285 | Evidence boundary / remaining action |
|---|---|---|
| Duplication with the concept section | Redundant generation/learning recaps replaced by a short “generate first, train later” section with contextual links; the former separate verification and milestone tables merged into a single milestone table. | Concept material is linked, not restated. Inspect rendered tables and callouts in both languages, including mobile widths. |
| Reference-code integration | New construction-order module list and executable quickstart (`uv sync --dev`; `GPTConfig` → `GPT` → greedy and sampled `generate`; `uv run pytest` with test files listed in reading order); pure-NumPy (float64), inference-only scope stated explicitly. | The snippet mirrors the tested `src/llm_lab/foundations/` API; it is not an executed CI example. Keep it in sync if the reference API changes. |
| Milestone alignment | The milestone table uses the G0–G9 identifiers of `docs/learning-path.md`, with G2 flagged as a parallel branch; the causal-attention acceptance test keeps the evaluation-mode/dropout condition from the 2026-11-02 pass. | Status claims stay bounded: the inference reference is tested; the data pipeline, training loop and evaluation are not yet built. Recheck against the canonical learning path after merge. |
| Cross-document traceability | `README.md` (site entry bullet, refreshed Status paragraph) and `docs/content-section-mapping.md` (inventory rows, renumbered milestone table, refreshed evidence) updated in the same PR. | Re-verify all three documents against the canonical learning path after merge. |


### Deepen knowledge-map and taxonomy pass — 2026-11-04

**Scope:** organize the advanced destination without turning it into a second mandatory route. The bilingual map pages (`site/fr/deepen.qmd`, `site/en/deepen.qmd`) introduce six question-led domains: architectures/mechanisms; text/tokenization; mathematical tools/geometry; probabilistic foundations/training; inference/efficiency; and scale/research questions.

| Area | Change | Evidence boundary / remaining action |
|---|---|---|
| Reader discovery | Added bilingual landing maps with entry points by learner question, concise descriptions of each deep dive, and a classification rule for future topics. | Source-level content review; inspect rendered tables, anchors, language switch, and navigation after CI. |
| Sidebar taxonomy | Replaced the previous uneven groups with six stable domains and placed the map at the top of the Deepen section in both languages. | Sidebar source updated; verify rendered Quarto navigation and mobile behavior. |
| Editorial governance | Added an admission/placement contract to the content map and contributor principles: one primary category, canonical ownership, precise graph-edge semantics, and a threshold for creating categories. | Future additions must update map, navigation, render list, inventory, and bilingual metadata. |
| RoPE integration | PR #387 is now merged; the RoPE deep dive is included under Architectures and mechanisms in both languages and in the bilingual map. | Rendered navigation, anchors, language switching, and mobile behavior remain to be inspected on the published site. |

This is a source-level organizational change, not evidence that readers have tested or validated the new information architecture.


### Knowledge graph: machine-readable Deepen domains — 2026-11-04

**Scope:** add a stable taxonomy field to the existing generated page graph, rather than creating a second graph implementation.

| Area | Change | Validation boundary |
|---|---|---|
| Metadata model | Added one controlled top-level `domain` field to each of the 15 bilingual Deepen content-page pairs. The specific `topic` and broad `destination` fields retain their separate meanings. | Validator requires one of six domain identifiers for Deepen content pages, exempts entry points, and rejects the field on other destinations. |
| Data generation | The existing `build_learning_map.py` now exports `domain` to the bilingual JSON payload. | Existing graph data-generation tests extended to cover domain preservation and serialization. |
| Interactive discovery | Added a domain filter to the existing FR/EN interactive map. Selecting a domain scopes the view to Deepen; changing destination away from Deepen clears the domain filter. Node labels use short forms; the details panel retains full category names. | Browser interaction, responsive layout, and keyboard use still require rendered review. |
| Editorial contract | Documented the six controlled IDs and clarified that each page has one primary domain; cross-domain links remain `related` edges. | Future additions must update FR/EN counterparts, metadata, and the map's controlled vocabulary together. |

The graph still distinguishes suggested reading route, conceptual hierarchy, and cross-links. Domain is a classification attribute, not a new edge type or prerequisite relation.


### Advanced LLM evolution synthesis — 2026-11-06

**Scope:** add the bilingual advanced synthesis `site/fr/llm-evolution.qmd` / `site/en/llm-evolution.qmd`, linked from the existing Deepen map under Scale and research questions. This is a cross-cutting synthesis, not a new mandatory route or a new architecture specification.

| Area | Change | Evidence boundary / remaining action |
|---|---|---|
| Historical comparison | Compare GPT-2 through GPT-6 across documented public milestones while explicitly stating that this is not a controlled comparison. | GPT-2 and GPT-3 claims are grounded in the original public materials; GPT-4 and GPT-5 claims in OpenAI's release/system-card materials; GPT-6 API behavior in current developer documentation. Internal architecture, training data, and recipes remain unknown where not disclosed. |
| Conceptual organization | Separate scale/data, training and post-training, modality, architecture/efficiency, inference-time compute, and system integration. | The axes are an editorial synthesis, not a claim that every generation follows the same sequence or uses every technique. |
| Scientific qualification | Correct the oversimplification that GPT-2 only continued text and had no task-transfer behavior; distinguish few-shot prompting from parameter updates; distinguish tool calling from tool execution. | Claims are bounded by cited sources. The ByteByteGo article is retained as a pedagogical starting point, not treated as the sole technical authority. |
| Knowledge graph | Add bilingual concepts for pretraining, in-context learning, post-training, instruction tuning, RLHF, DPO, inference-time compute, reasoning models, tool calling, and agentic systems; add only typed relations whose semantics are explicit. | The concept registry now includes project-relative `importance` metadata (`core`, `supporting`, `specialized`). New advanced concepts are classified as supporting or specialized; this annotation does not imply guided-route membership or prerequisite status. |
| Navigation | Add both language versions to Quarto rendering, the existing Deepen sidebar taxonomy, and the bilingual Deepen map. | Source-level validation only until CI and rendered/browser checks complete. |

The new pages are intentionally outside the guided route: they are advanced synthesis pages, not prerequisites. Therefore they do not include generated guided-route context fragments.


### Training/inference concept repair — 2026-11-06

**Scope:** source-level inspection of the bilingual generation, training-example and glossary pages, cross-checked against the concept registry, computational graph, and reference implementation. This is not a rendered-browser or full scientific peer review.

| Page pair / artifact | Review result | Evidence boundary / remaining action |
|---|---|---|
| `site/fr/generation.qmd` / `site/en/generation.qmd` | The canonical generation lesson now distinguishes prompt **prefill**, iterative **decode**, token-selection **decoding**, and the full autoregressive generation loop. It states that the local NumPy reference recomputes the current context and has no KV cache or optimized incremental-decode function. | Source change in PR #601. Render both languages; inspect the new subsection, equations/terminology, links and responsive layout. Do not infer that the implementation has a KV cache. |
| `site/fr/training-examples.qmd` / `site/en/training-examples.qmd` | The canonical training-example lesson now explains teacher forcing immediately after shifted input/target alignment. It states the causal-mask constraint and distinguishes conditioning from objective, loss and optimizer. | Source change in PR #601. The reference `training_examples.py` only constructs windows/targets; it does not execute teacher-forced model training. Render both languages and check the section transition. |
| `site/fr/glossary.qmd` / `site/en/glossary.qmd` | Added concise entries for teacher forcing, prefill, incremental decode and KV cache, each linked to its canonical lesson where applicable. | Source change in PR #601. Verify links and bilingual terminology in the rendered site. |
| `data/concepts.yml` / `data/computational-graph.yml` | The relevant concept nodes, domains, importance values and typed relations already existed. No graph schema, relation or route change was needed for this content repair. | Registry source inspected; graph/registry validation remains part of CI. Concept edges are not pedagogical prerequisites. |
| `data/sources.yml` | The previous training/inference audit claimed that five source records had been added, but the current registry did not contain those identifiers. The corrected audit no longer claims source-catalogue ingestion. | Source ingestion remains a separate task; add records only after bibliographic metadata, locators and scan status are verified. |
| `site/fr/evaluation-experimentale.qmd` / `site/en/experimental-evaluation.qmd` | The page pair is an applied protocol-design exercise for a scientific-passage ranker, not a canonical LLM evaluation chapter or benchmark. Its FR/EN metadata and stated scope correspond. | This limited scope check does not complete the page's scientific, example, link or rendered audit. Keep it in Practice; broader evaluation coverage remains open. |

**Audit correction:** the prior `training-inference-concepts-2026-11-06.md` incorrectly reported the three lesson explanations as already present and reported source records absent from the current source catalogue as integrated. PR #601 adds the missing lesson content and corrects the audit. Exposure bias remains deferred; it is not claimed as covered by the current lesson or glossary.



### Scoring, training and evaluation page-group source audit — 2026-11-06

**Scope:** FR/EN source-level review of likelihood, cross-entropy, loss, gradients, training examples and the experimental-evaluation exercise. Page frontmatter, page-map contracts, route role, core mathematical distinctions, implementation caveats and local transitions were compared. This pass did not render pages or independently re-derive every equation.

| Page pair | Source-level finding | Remaining boundary |
|---|---|---|
| `vraisemblance.qmd` / `likelihood.qmd` | The pair aligns on autoregressive chain-rule factorization, product-to-sum log-likelihood, NLL sign, sum-versus-mean distinction, and the need to report tokenizer/data conventions. It correctly separates conditional token probabilities from an independence assumption across separate dataset sequences. | No executable sequence-scoring implementation is evidenced by this pair. Recheck equations and source links in rendered FR/EN output. |
| `cross-entropy.qmd` (FR/EN) | Both distinguish general target-distribution cross-entropy from the one-hot negative log-probability case, entropy from cross-entropy, and token-level penalty from sequence/batch aggregation. Both state that logits/labels must be shifted consistently and that ignored positions affect both numerator and denominator. | The NumPy reference is deliberately row-wise `(B,C)`, unweighted mean, with gradient only w.r.t. logits. It does not implement sequence alignment, masks, ignore-index, soft targets, class weights or perplexity. The pages state this limitation; no full LLM training loss is claimed. |
| `loss.qmd` (FR/EN) | Both distinguish per-token penalty, valid-position masking, reduction conventions, perplexity and task metrics. Both warn that reported loss values are comparable only under compatible tokenizer, data, masks, lengths and reduction. | No complete token-sequence loss/masking implementation or training loop is evidenced. Preserve the distinction between the scalar objective and its derivative. |
| `gradients.qmd` (FR/EN) | Both explain the logit derivative, chain rule from logits to parameters, local sensitivity, elementary SGD and numerical finite-difference checks. The two language versions have corresponding section structure and caveats. | The reference tests finite-difference agreement for the loss derivative w.r.t. logits; they do not verify backpropagation through GPT parameters. No autograd/backward pass or optimizer update is implemented in the NumPy GPT. |
| `training-examples.qmd` (FR/EN) | Both explain shifted inputs/targets, stride, document boundaries, packing, padding, attention masks and loss masks. The implementation section accurately restricts `training_examples.py` to complete sliding windows and one-token-shifted targets. PR #601 adds the missing teacher-forcing explanation without implying that the helper executes model training. | Corpus ingestion, tokenization, packing, padding, masks, batching and train/validation splits remain unimplemented in the reference helper. Render the added teacher-forcing subsection in both languages. |
| `evaluation-experimentale.qmd` / `experimental-evaluation.qmd` | Both pages define a transfer exercise for a scientific-passage ranker, with an explicit deployment target, grouped dependence, leakage, selection bias, AP, calibration and uncertainty. The page metadata correctly places it in Practice, not as a canonical LLM-evaluation lesson. | This is a protocol-design exercise, not a model implementation or benchmark. A dedicated LLM evaluation chapter/harness remains a separate gap; do not use this exercise as evidence of one. |

**Cross-page path:** observed target → likelihood/log-likelihood → one-hot cross-entropy → batch loss/reduction → gradient → (future) optimizer update. This is a conceptual/mathematical relation, not a claim that the current code executes the full path. Training-example construction supplies shifted targets; evaluation applies scoring/metrics with fixed parameters and remains distinct from optimization.

**Metadata result:** the inspected FR/EN pairs use corresponding `type`, `destination`, `topic`, `level`, `language` and `status` tags. Page-level `domain` is not required here because these are not Deepen domain pages. Training examples remain a Build page and an optional training-stage companion; the evaluation exercise remains Practice. No page tag or route change is warranted by this source pass.

**Status:** source-level review only. No claim of rendered parity, accessibility, learner comprehension or complete scientific peer review.

### Status refresh — computational-spine page-group audit (2026-11-06)

The source-level page-group review recorded above is now integrated with the canonical lessons:

- PR #600 merged the G0–G9 implementation-evidence corrections; the build-path row above reflects that status.
- PR #601 merged the bilingual teacher-forcing and prefill/decode lesson corrections and glossary entries.
- PR #604 merged the observed-prefix explanation in the likelihood pages, distinguishing known-target scoring from generation and parameter-updating training.
- The scoring/training/evaluation group audit in this inventory remains a **source-level review**. It does not certify every derivation independently, rendered FR/EN parity, screen-reader usability, or learner comprehension.

The remaining #584 checks must therefore stay separate: complete the shared-core page audit; inspect rendered pages where evidence is still missing; and perform manual screen-reader and native-breadcrumb checks. Automated Quarto, Playwright and axe results are not substitutes for those manual checks.


## Fifteenth slice: precise softmax wording in the attention overview

A targeted FR/EN comparison of the scaled dot-product attention openings found a small but meaningful terminology mismatch. The French page said that softmax normalizes the weights, while the English page said that it “normalizes scores”. Strictly, softmax exponentiates the input scores and normalizes the resulting positive values; the output is the attention-weight vector. The English sentence now states this operation explicitly and retains the qualification that normalization is over accessible positions after optional masking.

| Area | Finding | Change | Remaining work |
|---|---|---|---|
| Softmax terminology (site/en/scaled-dot-product-attention.qmd) | “Normalizes scores” compresses two operations and can suggest that softmax merely rescales the raw scores. | Reworded the English opening to say that softmax exponentiates and normalizes the scaled, optionally masked scores into weights. The French formulation already described normalization of the weights and was retained. | Verify rendered FR/EN equations and opening paragraphs; no mathematical code or behavior changed. |

This is a narrow source-level correction, not a full audit of the attention lesson or its rendered presentation.


## Sixteenth slice: shared attention core, observed-target scoring, and training boundary (2026-11-07)

**Scope:** bounded source-level audit of the bilingual Q/K/V → scaled dot-product attention → causal masking chain, followed by observed-prefix likelihood scoring, cross-entropy/loss, training-example alignment, gradients, and the held-out evaluation boundary. This pass compared FR/EN source pages and independently checked representative equations and numerical examples. It is not a full derivation-by-derivation certification, rendered browser review, external-link sweep, or learner-mastery test.

### A. Q/K/V → attention → causal masking

| Page pair | Scientific/editorial finding | Status and remaining validation |
|---|---|---|
| `queries-keys-values.qmd` (FR/EN) | The common input is the current attention-submodule input $X$, not necessarily a raw token embedding: first-block input may include positional information; later blocks receive hidden states. $Q=XW_Q$, $K=XW_K$, $V=XW_V$, with $Q,K\in\mathbb R^{T\times d_k}$ and $V\in\mathbb R^{T\times d_v}$. Q/K determine routing weights; V supplies content. Projection parameters are separate but jointly optimized. The displayed weight-gradient identities are correctly scoped to linear projections without bias and fixed $X$. Cross-attention and MQA/GQA are explicitly marked as variants. | **Source review passed for the checked claims.** FR/EN purpose, page-map scope, tags and route agree. Preserve the diagrams and source-specific perspectives. Still inspect both SVGs and rendered equations at desktop/mobile widths; verify local route links in the built site. |
| `scaled-dot-product-attention.qmd` (FR/EN) | The single-head equations are dimensionally consistent: $S=QK^\top\in\mathbb R^{T\times T}$, $A=\operatorname{softmax}(S/\sqrt{d_k}+M)$ row-wise, and $O=AV\in\mathbb R^{T\times d_v}$. The additive hard-mask convention is explicit. The worked example uses scaled scores $(1/\sqrt2,0)$, weights approximately $(0.6698,0.3302)$, and output approximately $(6.698,6.604)$, matching the rounded $(6.7,6.6)$. The convex-combination statement is correctly limited to the pre-output-projection/pre-residual aggregation. | **Source review passed for the checked claims.** FR/EN calculation, interpretation and scope align. Still inspect both attention-flow SVGs and rendered math; add an executable regression only if it gives coverage beyond `tests/unit/test_attention.py`. |
| `attention-score-scaling.qmd` (FR/EN) | Under independent, zero-mean, unit-variance components, $\operatorname{Var}(q^\top k)=d_k$, so the standard deviation is $\sqrt{d_k}$; division by $\sqrt{d_k}$ returns variance to one in this simplified model. The page correctly avoids claiming that learned projections must exhibit this exact distribution or that scaling guarantees unsaturated softmax. | **Source review passed for the stated assumptions.** The FR micro-workbench has an empirical check; verify EN parity and rendered code/math, and confirm the cited source/version. |
| `causal-masking.qmd` (FR/EN) | The lower-triangular convention $j\le i$, additive values $0$ and $-\infty$, and application before softmax are internally consistent with next-token targets shifted by one. The diagonal is allowed because position $i$ contains input $x_i$, while its target is $x_{i+1}$. API-specific boolean-mask polarity is correctly distinguished. Fully masked rows and the limitations of a single-head perturbation test are disclosed. | **Source review passed for the checked claims.** Preserve the distinction among causal, padding and loss masks. Still inspect both SVGs and rendered code blocks; re-run the existing unit tests and confirm that the bilingual page links resolve. |
| `tensors.qmd` (FR/EN) | The existing audit records compatible batch/sequence/feature/vocabulary axes and projection shapes. The attention equations above are consistent with those contracts. | **Not re-audited line by line in this slice.** Keep its prior status; verify the rendered shape examples alongside the attention pages rather than duplicating a tensor lesson. |

### B. Scoring: observed prefix → target probability → sequence likelihood → NLL

| Page pair | Scientific/editorial finding | Status and remaining validation |
|---|---|---|
| `vraisemblance.qmd` / `likelihood.qmd` | Sequence factorization is the chain rule, not a token-independence assumption. For fixed parameters, observed-prefix scoring evaluates target probabilities without sampling, feedback of generated tokens, gradients or parameter updates. Log-likelihood converts products into sums; maximizing it is equivalent to minimizing NLL for the same observations and included positions. The example $0.5\times0.25\times0.8=0.1$, $-\ln(0.1)\approx2.303$ nats, and mean NLL $\approx0.768$ nat/token is consistent. | **One precision improvement applied in this slice:** qualify the one-forward-pass claim to sequences fitting within the context window and state that longer sequences require an explicit window/stride and target-counting convention. Re-render and inspect FR/EN parity. |
| `cross-entropy.qmd` (FR/EN) | The one-hot identity $-\log p_\theta(x_t\mid x_{<t})$, logit form $-z_y+\log\sum_j e^{z_j}$, and distinction between predictive entropy and observed-target cross-entropy are consistent. The page correctly scopes the NumPy reference implementation to $(B,C)$ logits and one target per row; it does not claim sequence shifting, token masks or a complete LLM training loss. | **Source review passed for the checked claims.** Recheck rendered derivation and confirm API-specific claims against the pinned/current PyTorch documentation when implementation work resumes. |
| `loss.qmd` (FR/EN) | The mean over valid target positions correctly excludes ignored positions from numerator and denominator. Sum, per-sequence mean and weighted mean are distinguished as different objectives/scales. $\mathrm{PPL}=\exp(\mathrm{NLL}_{mean})$ is correctly qualified for natural logarithms; the bit-based form and tokenizer/evaluation comparability caveats are present. | **Source review passed for the checked claims.** Keep reduction, tokenizer, target mask and evaluated corpus explicit in future benchmark reports. |
| `gradients.qmd` (FR/EN) | For one-hot cross-entropy, $\partial\ell/\partial z_i=p_i-\mathbb1[i=y]$ is correctly scoped to logits. The chain-rule expression uses the Jacobian of the full logit vector and correctly distinguishes gradient computation from the optimizer update. The SGD update is correctly presented as an elementary example, not a universal optimizer. | **Source review passed for the checked claims.** Rendered Jacobian notation and numerical gradient-check examples remain to inspect; current reference tests do not establish a full GPT backward pass. |

### C. Training and evaluation boundary

| Page pair / area | Finding | Remaining work |
|---|---|---|
| `training-examples.qmd` (FR/EN) | The input/target shift, teacher forcing as observed-prefix conditioning, causal visibility, stride, packing, padding, attention masks and loss masks are kept distinct. The page explicitly says its reference window builder does not execute a trainable forward pass, teacher forcing, or parameter updates. | Recheck full FR/EN parity and the corpus-tail/window examples; render Mermaid and code blocks. Preserve this as Build/data preparation, not as a prerequisite that replaces the conceptual scoring or loss lessons. |
| Training branch | The conceptual chain remains observed prefixes + targets → forward computation → target log-probability/NLL → reduction → objective → gradients → optimizer update. Teacher forcing is a conditioning strategy, not the objective or optimizer. The relation-type correction from PR #615 is consistent with this distinction. | The repository still does not provide end-to-end autograd through GPT weights, optimizer training, checkpointing, or a reproducible trained checkpoint. Do not imply otherwise. Keep implementation gaps with #78. |
| Held-out evaluation | Scoring on held-out data uses fixed parameters and does not update them; evaluation aggregates observed-target scores/metrics. This is distinct from training loss and from generation. | Keep the applied scientific-passage ranking exercise (`evaluation-experimentale.qmd` / `experimental-evaluation.qmd`) clearly identified as an evaluation-design case study, not as an implementation or benchmark of LLM language-model perplexity. Review metric estimands and uncertainty in its own scope. |

### D. Cross-cutting editorial assessment

- These pages are not one linear sequence of execution steps: Q/K/V, attention and causal masking are nested operations within a Transformer block; scoring and training are sibling uses of the shared forward computation.
- FR/EN page-map scope, purpose, topic identifiers, destination and level metadata are aligned for the inspected page pairs. French and English use different filenames for likelihood (`vraisemblance.qmd` and `likelihood.qmd`) but link to each other correctly.
- The distinction between Understand concept lessons and the Build-oriented training-example bridge is appropriate. Keep optional implementation detail collapsible and avoid duplicating the canonical tensor, code or history pages.
- Existing sources are complementary rather than interchangeable: Vaswani et al. grounds the attention formulation; PyTorch documents API conventions; Goodfellow et al. grounds maximum likelihood; visual explainers support intuition but do not establish mathematical correctness.

### E. Validation status — do not overclaim

**Completed in this pass:** repository source inspection of the listed FR/EN page pairs; independent arithmetic/dimension checks described above; targeted correction of the context-window qualification in the likelihood pair.

**Not completed:** Quarto render for this change; rendered FR/EN equation and SVG inspection; page-level browser/responsive/keyboard review; full external-link validation; manual breadcrumb and screen-reader review; end-to-end model scoring/training execution; learner testing.

The browser review is conditional in `.github/workflows/quarto.yml`: it runs for selected branch prefixes (including `ux/`), not for every pull request. The successful render on the original `docs/` branch therefore did not execute Chromium, keyboard, Axe, screenshot or responsive-page checks. Do not report those as passed until the targeted browser run completes.


## Seventeenth slice: positional information and tensor-shape notation (2026-11-07)

**Scope:** bounded source-level review of the bilingual positional-encoding introduction and its RoPE deep dive, plus the FR/EN tensor-shape reference and its softmax-axis worked example. This pass checks conceptual distinctions, notation, representative dimensions and arithmetic; it is not a complete review of every positional-encoding architecture or every implementation API.

### A. Positional information versus causal visibility

| Page pair | Finding | Decision and remaining validation |
|---|---|---|
| positional-encoding.qmd (FR/EN) | The previous opening risked implying that a causal decoder has no order signal unless an explicit positional encoding is added. That is too broad: content-only attention does not itself represent position, but a causal mask imposes an ordering constraint by restricting position i to its prefix (j ≤ i). The mask does not explicitly encode absolute positions or relative offsets. | **Clarified in both languages.** The opening now distinguishes content-based attention, causal visibility and explicit positional mechanisms. The diagram is explicitly scoped to absolute input encoding and RoPE; it does not depict the causal mask. |
| Absolute and relative mechanisms | Absolute encodings add position-specific vectors to token representations. Relative mechanisms can encode offsets through attention-score biases or relative representations. RoPE applies position-dependent rotations to Q/K after projection and before QK-transpose; its dot product depends on the relative offset. | **Taxonomy clarified.** RoPE is identified as a rotary relative-position mechanism, not as a category disjoint from all relative methods. It remains separately described because its insertion point and geometry differ from additive relative biases. |
| rope.qmd (FR/EN) | For one coordinate pair and one frequency, qₘ = R(mθ)q and kₙ = R(nθ)k. The rotation identities R(α)ᵀ = R(−α) and R(α)R(β) = R(α+β) imply qₘᵀkₙ = qᵀR((n−m)θ)k. The page correctly scopes the derivation to a pair/frequency and states that standard RoPE rotates Q/K, not V. | **Source check passed for the displayed derivation and scope.** No derivation or variant catalogue was copied into the introductory page. Rendered equations and diagrams still require the browser/render pass. |

The existing concept graph already distinguishes the roles: causal-mask constrains self-attention, while positional-encoding contributes to self-attention. No duplicate relation or new relation type was added. The concept registry already classifies positional encoding as core and associates it with the architecture/mechanisms and mathematical-tools/geometry domains.

### B. Tensor shapes, axes and numerical examples

| Area | Finding | Decision |
|---|---|---|
| Vocabulary notation | The tensor reference used V for vocabulary size in the same conceptual area as the value tensor V in Q/K/V. Both usages are conventional, but the overload was avoidable. | **Disambiguated in FR/EN:** vocabulary size is now N_vocab, including shapes, equations, code-oriented labels and both softmax comparison SVGs. The attention value notation remains V. |
| Shape contracts | Hidden activations (B,T,D), logits (B,T,N_vocab), and common multi-head activations (B,H,T,d_h) are correctly identified as common rather than universal. D = H d_h is appropriately qualified with “often”. The projection X with shape (B,T,D) and W with shape (D,D′) gives XW with shape (B,T,D′). | **Source check passed.** The page preserves the warning that shape compatibility does not establish axis semantics or computational correctness. |
| Softmax counterexample | For logits [2,1,0] and [0,1,2], softmax over the vocabulary axis gives approximately [0.665,0.245,0.090] and [0.090,0.245,0.665]. Softmax over the two-position axis gives [0.881,0.500,0.119] and [0.119,0.500,0.881]; the sums over the vocabulary axis are 1.5, not 1. | **Numerical example independently checked.** The PyTorch assertions test both normalizations and make the intended probability invariant explicit. |
| Embedding-table cost | N_vocab = 50,000 and d = 768 gives 38,400,000 parameters. At four bytes per parameter, the weights occupy 153.6 MB decimal, or about 146.5 MiB. A separate output projection may add d × N_vocab weights; weight tying changes that count. | **Arithmetic checked.** The page correctly excludes gradients, optimizer states and unrelated model parameters from the estimate. |

### C. Bilingual and editorial reconciliation

- FR/EN positional lessons now distinguish the causal visibility constraint from explicit positional mechanisms, use the same absolute/relative taxonomy, and retain the existing localized diagrams and links.
- FR/EN tensor lessons use the same N_vocab notation and corresponding worked examples. The English-only learning-path callout was removed; its useful guidance about introducing PyTorch operations in context and keeping general tensor theory optional is now a concise paragraph in both languages.
- No page was moved between Understand and Deepen: positional encoding remains a core concept lesson; tensor shapes remain an optional advanced reference.
- No changes were needed in data/concepts.yml: its existing typed relations already represent causal masking and positional encoding as distinct contributions to self-attention.

### D. Validation status and limits

**Completed in this source pass:** FR/EN source comparison; correction of the causal-mask/position distinction; clarification that RoPE belongs to the relative-position family; check of the RoPE pairwise derivation; vocabulary-symbol disambiguation; independent checks of the tensor shapes, softmax values and parameter-memory estimate.

**Rendered/browser evidence (workflow 42366358835, commit a3f44dd):** the Quarto site rendered successfully and the Chromium review completed with 232 cases and zero reported failures. For the three audited page pairs (positional encoding, RoPE, tensors), the report records HTTP 200, zero console/page errors, zero horizontal overflow, zero unrendered math delimiters, zero Axe violations on the full desktop-light cases, and working localized previous/next controls. FR/EN desktop-light reports each record exactly one native breadcrumb and zero custom duplicates; the breadcrumb ancestry is visible in the rendered pages. The guided-route context is a single labelled navigation landmark with one resolvable stage link. Keyboard review completed its tab cycle and reported visible focus for every sampled focus target (33 on positional encoding, 33 on RoPE, 40 on tensors, per language). The tensor SVGs loaded at desktop and mobile widths; the softmax comparison illustration remains legible in the reviewed desktop capture. FR desktop captures of positional encoding, RoPE and tensors were visually inspected; the mobile tensor capture was checked for layout and overflow.

**Still not established:** external-link freshness; manual screen-reader behaviour in FR/EN; complete manual verification of breadcrumb semantics and navigation ancestry beyond the automated DOM/text checks; learner understanding. Axe and keyboard focus checks are not a screen-reader test, and source/render checks do not certify every mathematical claim.

## External-link and API-claim check: cross-entropy pair (2026-11-07)

**Scope:** bounded verification for `site/en/cross-entropy.qmd` + `site/fr/cross-entropy.qmd` of the two source items left open for this pair: external-link freshness, and confirmation of the API-specific claims against the current PyTorch documentation. This is not a rendered-page review, an external-content certification, or a learner check.

### Numerical spot checks (independent computation)

- $-\ln 0.9 \approx 0.10536$ nats and $-\ln 0.1 \approx 2.30259$ nats match the figure and text values in both languages (0.105 / 2.303); the "nearly 22 times larger" statement matches (ratio $\approx 21.85$).
- The logit form $\ell(z,y)=-z_y+\log\sum_j e^{z_j}$ equals $-\log\operatorname{softmax}(z)_y$ to machine precision on a random four-vocabulary example.
- The gradient claim $\partial\ell/\partial z_i = p_i-\mathbb{1}[i=y]$ was confirmed against centered finite differences (agreement below $10^{-4}$).

### External links

| Link | Check result (2026-11-07) |
|---|---|
| PyTorch CrossEntropyLoss documentation (`docs.pytorch.org/docs/stable`) | Resolves; titled "CrossEntropyLoss — PyTorch 2.15 documentation" at check time. The API detail on the site pages is confirmed: the criterion computes cross entropy **between input logits and target**, and "the input is expected to contain the unnormalized logits for each class (which do not need to be positive or sum to 1)". The signature `ignore_index=-100, reduction='mean', label_smoothing=0.0` and the input/target shape contracts `(N,C,d_1,\dots,d_K)` / `(N,d_1,\dots,d_K)` confirm the pages' advice to check shapes, `ignore_index`, targets and reduction. The "CrossEntropyLoss expects probabilities" misconception is correctly marked false in FR/EN. |
| Shannon (1948), A Mathematical Theory of Communication (Harvard-hosted PDF) | Resolves; the document is the Bell System Technical Journal reprint by C. E. Shannon. |
| Cover & Thomas, Elements of Information Theory (Wiley, DOI 10.1002/047174882X) | The DOI resolves, but the publisher page is behind a bot-protection wall; the content could not be re-verified from this check. Keep the bibliographic citation; no freshness or content claim is made. |
| 3Blue1Brown — But what is cross-entropy? (YouTube) | Resolves; the title matches the citation ("But what is cross-entropy? | Compression is Intelligence Part 2", 3Blue1Brown). |

### Result

- **API-specific claims confirmed against the current stable PyTorch documentation** (2026-11-07). The earlier remaining item "confirm API-specific claims against the pinned/current PyTorch documentation" is discharged for the checked claims; the site links to the rolling `stable` documentation rather than a pinned version, so this confirmation is dated, not permanent.
- No external link is dead. The Wiley DOI is reachable only behind bot protection; its content freshness remains unverified.
- The FR/EN reference lists are identical in content and intent, including the "API behaviour, not the general mathematical definition" annotation.
- **Still not established for this pair:** rendered inspection of the derivation, equations and the target-probability SVG at desktop/mobile widths; a PyTorch version-pinning policy; screen-reader behaviour; learner understanding. Link checks do not certify the videos' or books' full content.

## External-link and API-claim check: loss and gradients pairs (2026-11-07)

**Scope:** the same bounded verification as the cross-entropy slice above, applied to `site/en/loss.qmd` + `site/fr/loss.qmd` and `site/en/gradients.qmd` + `site/fr/gradients.qmd` (scoring/training branch of #584). Not a rendered-page review, screen-reader or learner check.

### Numerical spot checks (independent computation)

- **Chain rule** $\nabla_\theta\mathcal{L}=(\partial z/\partial\theta)^\top\nabla_z\mathcal{L}$: verified on a linear logit map $z=W\theta$ (4 logits, 3 parameters, one-hot cross-entropy). The analytic gradient $W^\top(p-\mathbb{1}[i=y])$ matches centered finite differences to below $10^{-5}$.
- **Centered-difference formula** $(f(\theta_i+\epsilon)-f(\theta_i-\epsilon))/(2\epsilon)$: sanity check on $f(x)=x^2$ at $x=3$ returns 6 to numerical precision.
- **SGD direction:** one step $\theta-\eta\nabla_\theta\mathcal{L}$ with $\eta=0.05$ reduces the loss on the example (2.1164 → 2.0839), consistent with the "steepest local decrease" statement.
- **Perplexity:** $\exp(0.768)\approx 2.156$, consistent with the likelihood-page example's mean NLL and the $\operatorname{PPL}=\exp(\operatorname{NLL}_{\mathrm{mean}})$ convention (nats).
- The masking claim that ignored positions contribute to neither numerator nor denominator of a mean over valid targets matches the PyTorch behaviour documented for `ignore_index` (loss averaged over non-ignored targets).

### External links

| Link | Check result (2026-11-07) |
|---|---|
| PyTorch CrossEntropyLoss documentation (loss pair, FR/EN) | Already verified the same day in the cross-entropy slice above; the loss pages' annotations (unnormalized logits, ignored targets, class weights, reduction modes) are confirmed by the same documentation. |
| PyTorch — Autograd mechanics notes (gradients pair, FR/EN) | Resolves; "Autograd mechanics — PyTorch 2.15 documentation" at check time. The annotation (reverse-mode automatic differentiation and the computation graph) matches the page's subject. |
| PyTorch — `gradcheck` API documentation (gradients pair, FR/EN) | Resolves; the page states "Check gradients computed via small finite differences against analytical gradients", confirming the pages' annotation about numerical checking of analytical gradients against finite differences. |

### Deployed-page spot check

The published FR/EN pages resolve with the expected localized titles: "Loss: from per-token penalty to training objective", "Loss : de la perte par token à l'objectif", "Gradients: connecting loss to parameters", "Gradients : relier la perte aux paramètres". This is an availability and title check, not a rendered-mathematics or responsive review.

### Result

- **API-specific claims confirmed** for both pairs against the current stable PyTorch documentation (dated 2026-11-07; the site links the rolling `stable` docs).
- No external link is dead; no FR/EN divergence found in reference lists, misconceptions, callouts or self-check structure. The loss pair's cross-language links to the likelihood pair (`likelihood.qmd` / `vraisemblance.qmd`) are correctly localized.
- **Still not established for these pairs:** rendered inspection of equations at desktop/mobile widths, manual screen-reader behaviour, and learner understanding.


## Eighteenth slice: opening learner route — orientation → generation preview → text and representations

**Review date:** 2026-11-08  
**Scope:** source-level pass over the opening stages of `data/guided-route.yml`, including the optional Unicode deep dive. This pass inspected page metadata, declared purpose/scope, section hierarchy, opening explanations and route links. It is **not** a complete scientific audit, a rendered browser review, or evidence of learner mastery.

The route deliberately starts with a black-box generation experience before explaining the input and internal computation. This is pedagogically coherent if the learner is told that the first pass is an observable system-level preview and that the same generation page is revisited later as the detailed inference stage.

| Page pair | Role and route position | What this pass confirmed | Remaining check / decision |
|---|---|---|---|
| `llm-overview.qmd` (FR/EN) | System overview; orientation entry point | Both versions establish vocabulary, frame next-token continuation as the problem, introduce GPT computation, show the shared prediction spine, distinguish architecture / parameter learning / use, and situate inference in the lifecycle. The page points to generation as the next step. | Review the rendered first screen and diagram hierarchy. Check that the vocabulary list is sufficient but does not become an implicit prerequisite checklist; verify that the three dimensions remain distinct from chronological lifecycle stages. |
| `generation.qmd` (FR/EN) | Core concept lesson; orientation preview and later inference stage | Both versions define the fixed-parameter autoregressive loop and explicitly distinguish prefill, incremental decode, token-selection decoding, and generation. The declared scope excludes Transformer internals and parameter learning; the next route step is text/data. | **Intentional repeated membership:** this one canonical page occurs in both orientation and the later inference stage. Verify the rendered route context makes the first reading a preview and the later membership a return/deepening, rather than suggesting that the learner must reread an unchanged page. Check overlap with the temperature/sampling material on the probabilities page. |
| `text-data.qmd` (FR/EN) | Core concept lesson; text-input stage | Both versions connect preprocessing, tokenization, IDs and embedding lookup; distinguish prompt encoding from training-corpus preparation; and delegate Unicode and algorithm details to specialist pages. The route continues to tokenization strategies, with links to Unicode and embedding space. | Verify that the embedding lookup is introduced only as a preview here and that the later representation stage adds the necessary detail. Check that “preprocessing”, tokenizer behavior and corpus preparation remain distinct rather than being read as one universal pipeline. |
| `tokenization-strategies.qmd` (FR/EN) | Core concept lesson; text-input stage | Both versions cover granularity, tokenizer pipeline components, special tokens, BPE/WordPiece/unigram, a worked BPE example, and the distinction between tokenizer training and encoding at inference. The declared next destination is embedding space. | Check the rendered BPE example and terminology parity. Explicitly verify that “training the tokenizer” cannot be mistaken for pretraining the language model; keep tokenizer-specific claims scoped to the stated algorithm and pipeline. |
| `unicode-text.qmd` (FR/EN) | Optional advanced deep dive; not on the required core sequence | Both versions explicitly state that the page is optional, distinguish Unicode code points, UTF-8 bytes and normalization, and provide a return link to the main route. Its page metadata marks it as Deepen/advanced rather than a core Understand lesson. | Verify the return link and rendered code-point/byte examples. No reason to promote it into the core route: it is useful when representation differences matter, but not required for the first conceptual pass. |
| `embedding-space.qmd` (FR/EN) | Core concept lesson; representations stage | Both versions distinguish static historical word vectors from learned token embeddings, demonstrate ID-indexed lookup, label the numerical embedding/position weights as synthetic rather than GPT-2 parameters, and transition from initial embeddings to contextualized representations. | Recheck the complete worked trace and its assertions in both languages; verify the referenced tokenizer version and rendered code. Keep the synthetic values and illustrative positional vectors visibly distinct from actual pretrained GPT-2 weights. |
| `positional-encoding.qmd` (FR/EN) | Core concept lesson; representations stage | Both versions are intentionally concise: why order is needed, three approaches, misconceptions and references. The existing #643/#646 audit work already covers the source/rendered distinction between positional encoding, causal masking, RoPE classification and tensor notation. | Reuse #646 evidence rather than repeat its source audit. Confirm its final-head browser evidence remains the evidence associated with the merged content; keep RoPE derivations in the optional deep-dive page. |
| `contextualized-representations.qmd` (FR/EN) | Core concept lesson; representations stage | Both versions explain why repeated occurrences share an initial embedding but can produce different contextualized hidden states; distinguish the objects and locate the transformation in Transformer layers. | Check that this page's transition into the Transformer overview is explicit in the rendered route. Preserve the distinction between token identity, position, initial embedding and contextualized state. |

### Opening-route synthesis

- The high-level sequence is coherent: **orient → observe generation → unpack text input → inspect tokenization → build representations → contextualize them**.
- The first generation page is a deliberate black-box preview, not a claim that a useful model can generate coherent language before training. Keep the parameter-quality caveat visible in the overview and the generation lesson.
- The route has a useful distinction between required core pages and the optional Unicode deep dive. Do not turn every useful technical prerequisite into a mandatory detour.
- The text/data overview necessarily previews embedding lookup; the representations stage must deepen it rather than repeat the same explanation.
- The most important unresolved reader-experience question in this slice is the **second appearance of the generation page** in the guided route. Its pedagogical intent is sound, but the interface must communicate the return/revisit.
- No substantive content deletion or new page is justified by this source pass. Follow-up changes should be driven by the rendered review or a reproducible learning obstacle.

### Evidence boundary

This review is based on the current `main` source files and route registry. It does not certify every equation, external resource, figure, code example, or rendered layout. The previous #646 evidence is referenced only for the positional-encoding/tensor slice and is not generalized to the other pages. Learner comprehension still requires the separate pilot protocol; route coherence alone is not outcome evidence.


## Nineteenth slice: Transformer computation → prediction → inference, scoring and training

**Review date:** 2026-11-08  
**Scope:** source-level pass over the remaining required stages in `data/guided-route.yml`, plus the directly linked Build bridge and optional decoding deep dive. The review compared FR/EN metadata, declared purpose/scope, section hierarchy, key conceptual distinctions, route placement and exercise discoverability. It did not independently re-derive every equation, execute every snippet, inspect every rendered page, or test learner outcomes.

| Page pair | Role and route position | What this pass confirmed | Remaining check / decision |
|---|---|---|---|
| `transformer.qmd` (FR/EN) | System overview; computation stage | Both pages explain one forward pass from token IDs to logits, the repeated Transformer block, depth versus width, and the distinction between a forward pass and autoregressive generation. The practice section links to a separate GPT-2 exploration and explicitly says it is not required to follow the main explanation. The short training/inference comparison links to training examples and computational complexity rather than embedding an implementation tutorial. | Keep the system-level explanation as the overview. During rendered review, verify that the practice link and training/inference comparison read as optional context, not as a second Build tutorial. Reuse the existing architecture-history and block-walkthrough pages for deeper material. |
| `queries-keys-values.qmd` (FR/EN) | Core concept lesson; computation stage | Both versions distinguish Q/K projections (which determine attention weights) from V (which supplies aggregated content), derive the projections, state dimensions, and provide a self-check. | No additional core exercise is required based on this pass: the bilingual exercise hub already includes Q/K/V projection, parameter-intervention, gradient-learning and cross-attention transfer exercises. Verify their rendered answer disclosures and code blocks as part of the exercise review. |
| `scaled-dot-product-attention.qmd` (FR/EN) | Core concept lesson / worked derivation; computation stage | Both pages organize the calculation into four steps, include a numerical worked example, explain scaling, distinguish scores/weights/output, and address misconceptions before a self-check. | Reuse the prior #638 numerical/source audit and existing deterministic fixtures rather than repeating arithmetic. Rendered equation/diagram review remains separate. |
| `causal-masking.qmd` (FR/EN) | Core concept lesson / correctness invariant; computation stage | Both versions define allowed versus blocked positions, distinguish causal, padding and loss masks, connect the constraint to autoregressive factorization, and include a future-token perturbation example. The lesson treats causal masking as a correctness condition, not merely a decoding option. | The page is relatively dense because it combines definition, mask distinctions and a multi-step adversarial example. Check progressive disclosure and figure/code rendering before deciding whether any material should move to an optional deep dive; do not remove the invariant or imply a separator token alone prevents cross-document attention. |
| `logits.qmd` (FR/EN) | Core concept lesson; prediction stage | Both pages define vocabulary-sized unnormalized scores and distinguish ranking from a normalized probability distribution. Their short structure is appropriate for this single conceptual transition. | Verify the output projection link and ensure notation for vocabulary size and final sequence position agrees with the Transformer and probabilities pages. |
| `probabilites.qmd` / `probabilities.qmd` | Core concept lesson with interactive exploration; prediction stage | Both pages explain categorical next-token distributions, conditional probabilities, temperature, calibration and the distinction from factual truth. The numerical example and interactive temperature exploration support interpretation rather than treating softmax as a truth detector. | There is deliberate topic overlap with the generation lesson (temperature/sampling) and the advanced decoding deep dive (temperature/top-k/top-p). Preserve distinct roles: probability normalization and calibration here; a compact operational introduction in generation; full decoding algorithms and trade-offs in the optional deep dive. Check that the interactive experiment is not required to understand the mathematical explanation. |
| `entropy.qmd` (FR/EN) | Core concept lesson; prediction stage | Both versions distinguish predictive entropy of the distribution from the surprisal of a particular observed token, include numerical examples and bounds, and warn against interpreting entropy as factual uncertainty or correctness. | Verify consistent use of entropy, surprisal and nats/bits across the probabilities and likelihood pages. Do not conflate predictive entropy with target-token NLL. |
| `likelihood.qmd` / `vraisemblance.qmd` | Core concept lesson; scoring stage | Both versions introduce autoregressive factorization, score a known sequence from observed prefixes, convert products to summed log-probabilities, and connect log-likelihood maximization to NLL minimization for fixed observations. | Keep this as the canonical explanation of sequence likelihood. Verify that the observed-prefix framing remains distinct from generated-token feedback and from a parameter update; reuse #604's observed-prefix audit. |
| `cross-entropy.qmd` (FR/EN) | Core concept bridge; scoring stage and optional training reference | Both versions derive the target-distribution objective, recover NLL for a one-hot target, and connect multiple positions to shifted targets, valid-target masks, perplexity and gradients. This makes it a useful bridge between observed-target scoring and training rather than a separate model operation. | Inspect overlap with `loss.qmd` and `gradients.qmd`: retain the per-token objective and mathematical identities here, while batch reduction belongs to loss and parameter differentiation belongs to gradients. Avoid duplicating full derivations across pages. |
| `loss.qmd` (FR/EN) | Core concept lesson; training stage | Both versions move from per-token penalty to batch objective, explain target masking and sum/mean/weighted reduction, and distinguish training loss from evaluation metrics. | Verify denominator/mask conventions and reduction labels against the Build implementation. Keep perplexity's log-base and tokenization caveats consistent with cross-entropy. |
| `gradients.qmd` (FR/EN) | Core concept lesson; training stage | Both pages start with gradients with respect to logits, apply the chain rule to parameters, show a gradient-descent update and include a numerical verification path. They explicitly avoid claiming that a gradient alone defines an optimizer or guarantees global improvement. | Keep the scope distinction explicit: gradient is a derivative of the objective; optimizer/scheduler behavior is a separate update policy. Reuse the existing finite-difference and autograd references, and inspect code/math rendering. |
| `training-examples.qmd` (FR/EN) | Concept bridge; Build destination, optional from the conceptual route | Both versions explain input-target shifting, teacher forcing on observed prefixes, windows/stride, document boundaries/packing, padding/loss masks, tensor shapes and alignment debugging. Its page type and destination correctly separate data construction from the Understand concept sequence. | The conceptual training stage links it as optional/Build rather than making it an inference prerequisite. Verify that loss masks, attention masks and document-boundary policies remain distinct and that the examples' target shift is consistent with the causal-mask page. |
| `build-path.qmd` (FR/EN) | Guided implementation route; Build destination | Both pages describe the construction order, reference modules, guided tours and milestones, and explicitly present generation, scoring and training as three uses of the shared computation. They also preserve the caveat that random initialization demonstrates mechanics, not useful language quality. | Keep this path distinct from the conceptual route. Check each milestone against actual code/tests and preserve explicit implementation gaps; a route link or lesson is not evidence that the corresponding model feature exists. |
| `decoding-strategies.qmd` (FR/EN) | Optional advanced deep dive; Deepen destination | Both versions distinguish distribution transformations from sequence search, cover temperature/top-k/top-p, greedy/beam/contrastive decoding and quality-diversity evaluation, and call for reproducible comparison protocols. | Keep it optional. The core route should explain the next-token selection problem without requiring beam search, contrastive decoding or open-ended generation research. |

### Exercise and transfer audit — Q/K/V

The bilingual exercise hub already contains the requested Q/K/V transfer sequence; this is not a missing-content issue:

- distinguish weighted aggregation from hard selection;
- project a sequence into Q, K and V and infer their shapes before running NumPy;
- predict which quantities can change under isolated changes to (W_Q), (W_K) or (W_V);
- explain how the projections are learned indirectly through the final prediction loss and where their gradients flow;
- transfer the provenance of Q, K and V to cross-attention, then distinguish MQA/GQA sharing from the functional roles of the projections.

These tasks are distinct from the stable AT-A/AT-B/AT-C exercises, which focus on multi-head calculation, shapes, and intervention diagnosis. Do not replace the Q/K/V tasks with the multi-head collection or create a duplicate exercise series. The exercise hub is explicit about these competencies in both languages; the rendered answer/code disclosures remain part of #329's browser review.

### End-to-end route synthesis

The complete eight-stage route is conceptually coherent at source level:

1. **Orientation:** understand the system and see generation as a black-box behavior.
2. **Text input:** unpack text, tokens, tokenizer and IDs.
3. **Representations:** follow lookup, positional information and contextualized states.
4. **Computation:** inspect a Transformer pass and the operations inside its blocks.
5. **Prediction:** interpret logits, probabilities and predictive entropy.
6. **Inference:** revisit generation with prefill, incremental decode and token-selection policies.
7. **Scoring:** evaluate probabilities assigned to observed targets and sequence likelihood.
8. **Training:** connect token-level objectives to batch loss and gradients; use the Build branch for teacher forcing, shifted examples and implementation detail.

This order does not imply that the model executes these eight stages as one linear runtime. In particular, scoring and training are sibling uses of the shared prediction computation; teacher forcing is a context policy for observed prefixes, not a prerequisite for inference; and prefill/decode are inference execution phases, not training operations.

### Priority findings

- **No major sequence inversion found** in the required pages reviewed. The route progresses from a system-level mental model to input, representations, internal computation, output distribution and the distinct operational uses.
- **The most important overlap to manage** is temperature/sampling across generation, probabilities and advanced decoding. Their scopes should remain complementary, with one canonical home for each level of detail.
- **The strongest existing practice asset** is the Q/K/V exercise sequence. It already tests causal reasoning about projections, parameter interventions, learning and transfer; do not add redundant exercises.
- **The most important conceptual boundary** is between the shared forward prediction, observed-target scoring, and training updates. Keep the distinctions visible across likelihood, cross-entropy, loss, gradients and Build.
- **The largest remaining evidence gap** is not route structure but rendered and learner-facing validation: equation/figure inspection for the remaining pages, manual screen-reader/touch review where applicable, and an independent learner pilot. Automated CI or a page inventory cannot establish comprehension.

### Evidence boundary

This is a structured source-level audit of the current bilingual route and linked pages. It does not claim a full scientific certification of every statement or a complete visual inspection. Existing #638/#604/#646 evidence is reused only for their exact audited scopes. The rendered exercise-hub review remains owned by #329/#710; Q/K/V rendered/media provenance remains under #483; independent learner validation remains under #447.


## Twentieth slice: optional branches and the practical Build route

**Review date:** 2026-11-08  
**Scope:** source-level review of every optional page declared by the eight stages in `data/guided-route.yml`, plus the French and English Build-path pages. Compared declared purpose/scope, metadata level/destination, section hierarchy, relation to the main sequence, Build dependencies and explicit implementation-status claims. This is not a complete audit of every linked Practice activity or every code tour.

### A. Optional branches

| Optional page pair | Declared pedagogical role | Finding | Remaining check / decision |
|---|---|---|---|
| `transformer-architectures.qmd` (FR/EN) | Optional core-level Understand comparison from orientation | The page has a distinct role from the GPT computation overview: compare encoder-only, encoder–decoder and decoder-only configurations, information visibility, architecture/objective/task, and classification limits. The comparison is a useful optional branch before committing to the lab's decoder-only scope. | Keep optional: it broadens the learner's model-family map without becoming a prerequisite to understanding the chosen GPT. Rendered comparison diagram and cross-attention links still need review. |
| `llm-limits.qmd` (FR/EN) | Optional overview-level critical companion | Its scope is deliberately limited to what next-token training does and does not guarantee, meanings of “understanding”, emergent-ability claims and scale effects. It does not compete with the experimental-evaluation lesson. | Keep adjacent to orientation as a critical perspective. Check that “objective guarantee”, calibration, factuality and measured capability remain distinct in the final examples. |
| `unicode-text.qmd` (FR/EN) | Optional advanced text representation | Already reviewed in the opening slice. It distinguishes code points, bytes and normalization without burdening the core tokenization sequence. | Keep optional; reuse the previous slice's return-link/render check. |
| `tokenizer-design-evaluation.qmd` (FR/EN) | Advanced Deepen branch from tokenization | The scope progresses from tokenizer-family mechanisms to vocabulary/budget choices, reproducibility, evaluation metrics and multilingual disparities. It is genuinely deeper than the core BPE/WordPiece/Unigram introduction. | Keep optional and advanced. Its protocol and empirical claims need their own source/freshness and rendered code/figure audit; do not move it into the required sequence. |
| `tensors.qmd` (FR/EN) | Advanced technical reference | It provides shape/axis reasoning, projection dimensions, softmax-axis counterexample and parameter-cost calculation. It explicitly says it is not a prerequisite course for Build. | Keep as a just-in-time reference. Ensure concept pages link to the exact relevant sections instead of making the whole page compulsory. Existing #646 numerical/render evidence is reusable for its audited scope. |
| `rope.qmd` (FR/EN) | Advanced mathematical deep dive | It derives relative-offset dependence for a coordinate pair, locates rotations in Q/K and discusses implementation/extrapolation limits without repeating the general position lesson. | Keep optional. Reuse the existing positional/RoPE derivation evidence; rendered equations and implementation details remain subject to the exact prior audit scope. |
| `cross-attention.qmd` (FR/EN) | Advanced architecture/mechanism deep dive | It explicitly establishes the distinct provenance of Q versus K/V, dimensions, masks and placement in encoder–decoder and multimodal models. It supports Q/K/V transfer rather than extending the decoder-only core into an unnecessary prerequisite. | Keep optional. Its connection to the Transformer-architecture comparison and Q/K/V exercise should be navigable, but it should not be required to understand decoder-only self-attention. |
| `attention-score-scaling.qmd` (FR/EN) | Advanced mathematical deep dive | It isolates the variance argument for (1/\sqrt{d_k}), states the Gaussian assumptions and their limits, and avoids repeating the full attention calculation or causal masking. | Keep optional. The distinction between an explanatory independent-Gaussian model and learned projected Q/K must remain visible in both languages. |
| `decoding-strategies.qmd` (FR/EN) | Advanced inference deep dive | It progresses from distribution transforms (temperature/top-k/top-p) to sequence search (greedy/beam/contrastive) and reproducible quality-diversity comparisons. This is a distinct outcome from the short generation and probability explanations. | Keep optional. Preserve the explicit division of depth already identified in the main-route slice; inspect the rendered protocol/figures before changing the page. |
| `scaling-laws.qmd` (FR/EN) | Advanced research-oriented Deepen branch | It explains empirical relations between parameters, data, compute and loss, while explicitly rejecting a universal parameter-count threshold for LLMs. This complements rather than replaces the small-GPT Build route. | Keep optional. It should not be framed as a required prerequisite to training mechanics or as a universal model taxonomy. |

### B. Build path: sequence, dependency and evidence

Both `build-path.qmd` versions explicitly distinguish three things that must remain separate:

1. the order in which the code tours are presented;
2. the implementation dependencies/imports;
3. the learner's conceptual route through Understand pages.

The code-tour order is configuration → numerical operations → Transformer block → model assembly → generation. The page explicitly warns that this is a useful reading order, not a complete dependency graph: the block imports attention operations and generation imports optional decoding filters. The minimal inference path is not yet separated from those extensions.

The build milestones preserve the important split:
- G0/G1/G3–G7 construct and inspect the inference path, with random initialization clearly qualified.
- G1b/G2 form a parallel corpus/tokenizer/training-example branch; they are required before training, not before generation.
- G8 covers loss, parameter gradients, updates and fixed-parameter validation as the intended outcome, while the implementation is explicitly partial.
- G9 is a parity criterion, not a claim that an independent reference comparison already exists.
- E1 is cross-cutting task evaluation, not another sequential model-construction stage.

This is pedagogically sound and consistent with the conceptual eight-stage route. The Build route should not be forced into the same page order: a reader can learn the generation loop before building the training-data pipeline.

### C. Important implementation-status precision

The current Build page states that the training implementation is partial and names `losses.py` functions `cross_entropy_from_logits` and `cross_entropy_gradient`, while also stating that there is no complete training loop, optimizer, automated validation runner or checkpoint. This is an important distinction to preserve: a gradient of the loss with respect to logits is not yet backpropagation of gradients through all model parameters, and neither is a parameter-update/optimizer implementation.

The Build page also correctly distinguishes:
- a conceptual lesson from implemented code;
- a worked example from a test;
- a passing test from a complete proof of a property;
- a validation score at fixed parameters from an optimizer step;
- token IDs from readable generated text (which requires a compatible tokenizer).

No evidence in this source pass justifies claiming that end-to-end training, checkpoint loading, EOS stopping, KV cache, corpus provenance/deduplication, full padding/packing/masking, or independent implementation parity is already available.

### D. Bilingual and editorial assessment

- Optional-page metadata is consistent across FR/EN in type, destination, level and declared purpose for all pairs reviewed.
- Optional does not mean pedagogically unimportant: the architecture comparison and LLM-limits companion are overview-level resources; tokenizer design, tensors, RoPE, cross-attention, attention scaling, decoding and scaling laws are genuinely advanced.
- The advanced pages have distinct stated outcomes; no page split/merge is justified from this source pass.
- The Build page has matching milestone identifiers and substantive claims in both languages. The English and French route links point to localized concept pages.
- No new page, registry, route, workflow or exercise collection is justified.

### E. Follow-up priorities

1. Render the Build route and its milestone table at desktop/mobile widths; inspect table overflow and code-example legibility.
2. Verify the route context around optional links: the reader should understand why a branch is optional and where to return.
3. Audit the actual guided code tours (configuration, operations, block, model, generation) against their code and tests; the Build landing page is not a substitute for those page reviews.
4. Review Practice activities for observable learning outcomes, feedback quality, answer disclosure, and alignment with the corresponding concept and Build milestone.
5. Keep independent learner validation under #447; neither page metadata nor test coverage demonstrates transfer.

### Evidence boundary

This pass inspected source-level page contracts and the two Build landing pages. It did not certify every advanced derivation, reference, interactive widget, code tour, generated route UI or rendered layout. It does not constitute the complete Practice activity audit or learner validation. Reuse existing #646 and earlier exact-scope evidence rather than repeating those checks.


## Twenty-first slice: five guided code tours, from configuration to generation

**Review date:** 2026-11-08  
**Scope:** source-level comparison of the five guided Build tour pairs (FR/EN), including metadata, page contract, learning outcomes, previous/next links, declared exclusions, exercise/test sections and relation to the Build landing page. This is not a line-by-line audit of the Python source or an execution of every code sample/test.

| Tour pair | Distinct learning outcome and place in Build sequence | What this pass confirmed | Remaining check / decision |
|---|---|---|---|
| `gpt-config-walkthrough.qmd` (FR/EN) | 1/5: understand model configuration before operations exist | Both pages focus on `GPTConfig`, seven named dimensions, immutability and construction-time validation. They explicitly exclude model computation, the Transformer block and generation. Learning outcomes connect configuration fields to tensor shapes and early validation. | Keep first. The first page has no previous tour and links forward to operations. Verify each claimed field and validation case against the source/tests in the code audit. |
| `gpt-ops-walkthrough.qmd` (FR/EN) | 2/5: understand independently testable numerical primitives | Both pages cover initialization, linear projection, per-position layer normalization and approximate GELU; they explicitly exclude block/model assembly. They connect output-shape prediction to the `axis=-1` convention and tests. | Keep second. Check that initialization claims are scoped to this educational implementation and that the GELU approximation explanation does not imply exact equivalence. |
| `transformer-block-walkthrough.qmd` (FR/EN) | 3/5: trace a pre-LN block, residual branches, attention heads and MLP | Both pages focus on the repeated block, pre-LN residual order, residual-weight initialization, explicit attention loops, head slicing and position-wise MLP. They exclude embeddings, output head and generation. The links to Q/K/V, attention, causal masking and contextualized states are relevant rather than a duplicate concept course. | Keep third. The block imports attention operations that have no separate tour; the Build landing page already calls out this dependency. Verify the actual call graph and that loop-based code is presented as an inspectable reference implementation, not as the only/fastest implementation. |
| `gpt-model-walkthrough.qmd` (FR/EN) | 4/5: assemble the forward pass from token IDs to vocabulary logits | Both pages cover token/position embedding tables, stacked blocks, final normalization, untied output head and parameter counting. They explicitly exclude generation. The shape contract is ((B,T)\to(B,T,V)), and the page links back to the conceptual representation/logit lessons. | Keep fourth. The causal evidence is a prefix-invariance test, not a universal proof over all possible inputs; preserve that qualification. Verify broadcasting and parameter accounting against the source/tests. |
| `gpt-generation-walkthrough.qmd` (FR/EN) | 5/5: unroll the autoregressive loop after model assembly | Both pages explain prompt validation, sliding context, last-position logits, greedy or temperature-sampled selection and deliberate absence of KV cache/early stopping. They explicitly exclude the forward-pass computation and assume the model tour has been read. | Keep fifth. The page has no next tour by design and links back to the conceptual generation/logits/probabilities lessons. Verify that “generated text” language remains qualified where the current implementation actually returns token IDs and has no compatible tokenizer/checkpoint loader. |

### Build-tour sequence and pedagogical boundary

The five tours provide a coherent implementation-facing progression:

**configuration → numerical operations → Transformer block → GPT assembly/forward pass → autoregressive generation.**

This is intentionally different from the conceptual learning route. The latter introduces generation as a black-box behavior before internal mechanisms; Build constructs the mechanism before running it. The two paths are complementary, not contradictory.

Each tour has a distinct declared scope and learning outcomes. The tour sequence uses reciprocal previous/next metadata and a shared Build parent; the last tour correctly has no next item. The FR/EN pairs have matching stage numbers, conceptual exclusions, exercise/test sections and link intent.

### Specific pedagogical cautions

- The numerical operations tour is a set of reusable primitives, not a separate mathematical prerequisite course.
- The block tour's explicit loops are a deliberate inspectability choice; do not imply that they are the preferred optimized production implementation.
- The model tour's prefix-invariance test supports a specific causal property under the tested extension; it is not a general formal proof.
- The generation tour returns token IDs in the current reference implementation. Readable text requires a compatible tokenizer; useful language output requires trained or pretrained parameters.
- The implementation currently recomputes the context on each generation step and deliberately omits KV caching and an EOS/early-stopping rule. This is a useful baseline for understanding the loop, not an inference-performance implementation.
- An operation's unit test, a model-level test and a learner's ability to explain/modify the code are different forms of evidence.

### Decision

Keep all five tours as separate Build pages. Their outcomes and file boundaries are distinct, and merging them would collapse the inspectable progression from configuration through numerical operations and architecture to sequence generation. No new tour or extra prerequisite page is justified.

### Remaining evidence

The next code-focused pass should compare each tour's code excerpts and stated test claims with the current source and unit tests, execute the examples, and inspect the rendered exercises/answer disclosures. This source pass did not certify code correctness, numerical examples, responsive layout, keyboard/screen-reader behavior or learner transfer. Reuse the existing Build-path status matrix and do not create a second implementation-status catalogue.


## Twenty-second slice: Practice catalogue and formative exercise progression

**Review date:** 2026-11-08  
**Scope:** source-level FR/EN comparison of the exercise hub, availability/status table, learning purpose and current collection coverage. Also checked the collection headings and declared maturity against the conceptual/Build route. This is not a complete correctness audit of every answer, rendered disclosure or interactive activity.

### A. Exercise hub contract

The FR/EN exercise hubs have matching roles and status claims:
- They are a registry/navigation point for extended exercises and transfer tasks, not another lesson.
- They explicitly distinguish short lesson-level self-checks from longer, multi-step formative collections.
- They ask learners to attempt problems before opening collapsed solutions and explain assumptions/limits; a correct numerical result alone is not treated as mastery.
- The availability table distinguishes published exercises from collections that are only planned.

This is a useful and pedagogically important contract. Preserve it; do not present all collection headings as available activities.

### B. Current exercise coverage

| Collection | Current published material | Main gap explicitly acknowledged by the hub |
|---|---|---|
| Mathematical foundations | Seven progressive exercises: logits/softmax/NLL; loss masking and denominator; logit-to-parameter chain rule; soft targets/KL; batch shapes; stable log-sum-exp/log-softmax; NLL-to-perplexity | Finite-difference gradient verification and further topics |
| Text data | TR-A representation pipeline reconstruction; TR-B embedding lookup and tensor shapes; TR-C identity/position/context distinctions | Dedicated BPE, windows, shifted targets and leakage exercises |
| Attention | Weighted aggregation; Q/K/V projection reconstruction; isolated projection interventions; gradient-learning path; cross-attention transfer; AT-A–AT-C multi-head exercises | Causal-mask and invariance exercises |
| Transformer | TF-A pre-LN block/shape trace; TF-B block parameter count; TF-C diagnosis and interventions | Architecture-variant exercises |
| Pretraining | Prerequisite and focus outline only | Collection not yet authored |
| Generation | Prerequisite and focus outline only | Collection not yet authored |
| Fine-tuning | Prerequisite and focus outline only | Collection not yet authored |
| Evaluation | Prerequisite and focus outline only | Collection not yet authored |
| Efficiency | Prerequisite and focus outline only | Collection not yet authored |
| Advanced topics | Prerequisite and focus outline only | Collection not yet authored |

The English and French hubs match in the collection names, published counts/identifiers, prerequisite framing and explicit not-yet-authored status. The first four collections align with the concepts currently taught and with the transfer expectations from the route. The later collections are honest roadmaps, not falsely advertised exercises.

### C. Pedagogical implications

- **Do not create duplicate Q/K/V exercises.** The existing attention collection already covers role recognition, reconstructing projections, predicting the effect of parameter interventions, explaining learning through gradients and transfer to cross-attention. AT-A/B/C cover a separate multi-head outcome.
- **Prioritize the causal-mask/invariance gap next.** It is a central correctness invariant used in the conceptual route and Build G4. A formative task should make the learner predict which earlier-position outputs can or cannot change when future tokens are appended, then distinguish this invariant from padding and loss masks.
- **Complete the text-data transfer gap after that.** TR-A/B/C establish representations, but BPE merge tracing, shifted windows and leakage/boundary handling are explicitly listed as not yet covered by extended exercises. They are good candidates for a single coherent sequence rather than unrelated one-off exercises.
- **Do not author all planned collections at once.** Pretraining, generation, fine-tuning, evaluation and efficiency need the corresponding model/data/code milestones to become sufficiently concrete. Add them when the core implementation and lessons can support realistic tasks.
- **Keep feedback formative.** For each new task, require a prediction or explanation before code/calculation, expose the worked solution after an attempt, and include at least one transfer or counterexample question where the concept warrants it.

### D. Priority decision

The next exercise-development work should be:

1. Causal masking and prefix invariance (one connected task with a prediction, a small counterexample and a test interpretation).
2. Tokenization/BPE and text-window alignment (a progression from merge trace to shifted targets and leakage detection).
3. Only then consider pretraining/generation collections, based on the state of the actual training and inference code.

This is a priority recommendation, not a claim that the new exercises already exist. It should be coordinated with #220 (text-to-representation formative sequence), #329 (rendered review) and #447 (learner validation), rather than creating a parallel exercise project.

### Evidence boundary

This is a source-level catalogue and coverage review. It does not independently certify all seven mathematical solutions, all TR/AT/TF answers, disclosure accessibility, or learner mastery. The next pass should verify representative calculations and code-backed claims, then review all answer disclosures in the rendered bilingual site. Reuse the existing exercise hub; no new registry is warranted.


### E. Independent arithmetic spot-check — seven mathematical exercises

A separate arithmetic pass on the seven published mathematical exercises found no numerical or algebraic discrepancy in the stated answers:

- Exercise 1: softmax ((1/9,1/3,5/9)), target NLL (ln 3), gradient ((1/9,-2/3,5/9)).
- Exercise 2: valid-target mean (2\ln 2=\ln 4\approx1.3863); incorrect denominator-four result (1.5\ln2\approx1.0397).
- Exercise 3: (J^\top g=(0.3,-0.5)).
- Exercise 4: (H(q,p)=\ln2\approx0.6931), (H(q)\approx0.5623), and (D_{KL}(q\Vert p)\approx0.1308).
- Exercise 5: logits shape ((2,4,10)), targets/losses by position ((2,4)), six valid positions, vocabulary softmax on the last axis.
- Exercise 6: stable log-sum-exp (\approx1001.4076) and target NLL (\approx0.4076).
- Exercise 7: (\exp(1.2)\approx3.3201).

This was an independent calculation/identity check of the displayed values, not execution of every code block or validation of all pedagogical wording. The finite-difference gradient-check exercise remains explicitly unfinished in the hub.

## Eighteenth slice: guided-route card harmonization across the core chain (2026-11-08)

**Scope:** source-level, file-by-file review of the suggested-reading cards (the generated `route-nav-cards` fragments) along the 18-page core guided chain, FR and EN: index → llm-overview → generation → text-data → tokenization-strategies → embedding-space → positional-encoding → contextualized-representations → transformer → queries-keys-values → scaled-dot-product-attention → causal-masking → logits → probabilites → entropy → vraisemblance → cross-entropy → loss → gradients. This slice serves the reader-side navigation spine of #584 and informs the open card/stepper harmonization decision of #337. It records source evidence only; rendered, screen-reader and learner evidence are not claimed.

### Findings

- The `suggested_route` metadata chain is exact across the 36 FR/EN page files: every previous/next anchor resolves to a published page, the FR and EN chains mirror each other, and gradients terminates with `next: null`.
- Card coverage was asymmetric: only 8 of 18 core pages included the generated fragment (queries-keys-values, scaled-dot-product-attention, causal-masking, logits, probabilites, vraisemblance, cross-entropy, loss). Nine chain pages carried no card at all (llm-overview, generation, tokenization-strategies, embedding-space, positional-encoding, contextualized-representations, transformer, entropy, gradients), so the probabilites → entropy and loss → gradients transitions were one-way: a neighbour's card pointed at a page without a reciprocal card.
- text-data (FR/EN) hand-maintained a `route-nav-cards` div duplicating the generator output, contrary to the derive-at-build rule (contract §7.7), with an effective divergence: the EN hand cards used « ← Previous Step » / « Next Step → » where the generator emits « ← Previous step » / « Next step → ».
- logits (FR/EN) placed the generated include inside the `.self-check` div; contextualized-representations (FR/EN) nested the `.language-switch` block inside the `.self-check` div.
- The embedding-space pair mislabelled its input-chain link: FR « pour l’étape précédente » and EN "for the preceding tokenizer stage" pointed at text-data, which is two steps back in the route; the immediately preceding page is tokenization-strategies.
- `build_learning_map.py` `page_href` resolved both `fr/index` and `en/index` to `../index.html`. This is correct for FR (the French landing page is the site root) but wrong for EN consumers: from pages under `site/en/`, `../index.html` is the French homepage, not `site/en/index.qmd`. The defect was latent (no EN page included an index-targeted card) and becomes reader-visible as soon as en/llm-overview includes its previous-step card.

### Changes made in this slice

- Added the generated suggested-route include to the ten pages above (FR and EN), immediately before the language-switch block, matching the placement convention of the eight already-carded pages.
- Replaced the hand-written text-data cards with the generated fragment; targets are unchanged, labels now follow the generator in both languages.
- Moved the logits include after the self-check closing fence; closed the contextualized-representations self-check div before its language-switch block.
- Corrected the embedding-space pair to name both input-chain predecessors (text-data and tokenization-strategies).
- Fixed `page_href`: `en/index` now resolves to `index.html` for pages under `site/en/`, mirroring the FR root landing case.
- Deliberately retained: the generation end-of-page next-step callout (contract §4/§5) and the page-specific `pipeline-stepper` on text-data (contract §3.4).

### Validation status and limits

**Completed in this source pass:** comparison of include statements, div nesting and route metadata across the 36 page files; reading of `write_suggested_route_fragments`, `render_suggested_route_markdown` and `page_href` in `build_learning_map.py` to confirm fragment naming, `next: null` handling, label vocabulary and index href resolution.

**Delegated to the Quarto workflow on the accompanying pull request:** fragment resolution at render time, `check_site_links` over the rendered site, the rendered learning-map and knowledge-graph checks, and the targeted rendered browser review. This slice claims no rendered evidence.

**Still not established:** manual screen-reader behaviour; learner validation (#447); the broader rendered navigation review (#337) and the remaining #584 items.

## 2026-11-09: guided-route page-by-page structural audit

**Scope and method.** Inspected the bilingual page-map metadata, stated scope/purpose, headings and route placement for the 21 core page pairs in the eight stages of `data/guided-route.yml`. Read targeted body excerpts for the system panorama, generation, Transformer overview and output-probability lessons to check the most important cross-page boundaries. This is a route-structure and editorial-contract audit, **not** a line-by-line scientific certification of all 42 files, a rendered review, or learner testing.

### Stage-to-page review

| Guided stage | Core page pairs inspected | Pedagogical role and result |
|---|---|---|
| Orientation | `llm-overview`, `generation` | Starts with the problem and a black-box generation loop. The early generation membership is intentional: it previews inference before requiring knowledge of tokenization or Transformer internals. |
| Text input | `text-data`, `tokenization-strategies` | Moves from raw text to tokens and IDs, then explains segmentation strategies. Unicode and tokenizer design/evaluation remain optional depth rather than gates. |
| Representations | `embedding-space`, `positional-encoding`, `contextualized-representations` | Separates ID lookup, positional information and context-dependent hidden states. Tensor algebra and RoPE derivations remain optional. |
| Computation | `transformer`, `queries-keys-values`, `scaled-dot-product-attention`, `causal-masking` | The overview locates the block; Q/K/V are projections from each block's input states; attention computes scores and aggregates values; causal masking constrains visibility. The order does not imply that Q/K/V follow the final contextualized states. |
| Prediction | `logits`, `probabilities`, `entropy` | Separates unnormalized vocabulary scores, the normalized next-token distribution and uncertainty of that distribution. |
| Inference | `generation` (second membership) | Returns to the canonical generation lesson for prefill/decode, token selection, context feedback and stopping. It is the same page as the early preview, not a second generation lesson. |
| Scoring | `likelihood`, `cross-entropy` | Moves from an observed target's conditional probability to sequence likelihood/log-likelihood and the token-level target-distribution penalty. Parameters remain fixed. |
| Training | `loss`, `gradients` | Aggregates valid per-token penalties into an objective, then differentiates it and discusses parameter updates. Training-example construction remains an optional Build bridge, not an inference prerequisite. |

The route is consistent with the narrative separation in `docs/learning-path.md`: first understand what the model computes and how inference works; then study scoring and learning; follow corpus preparation and shifted training examples through the separate Build branch.

### Cross-page boundaries checked

- **Generation versus training:** the generation lesson defines prefill and incremental decode as inference execution phases and explicitly distinguishes them from teacher forcing. The latter is explained in `training-examples`, where observed-prefix conditioning and shifted targets belong.
- **Input versus training data:** `text-data` owns prompt encoding at inference; `corpus-preparation` owns provenance, filtering, deduplication, held-out splits and tokenizer fitting; `training-examples` owns windows, shifted targets, document boundaries, padding and masks.
- **Representations versus block computation:** initial embeddings, positional information and contextualized states have separate concept pages. Q/K/V are internal projections in each Transformer block, not a stage after final contextualization.
- **Attention versus prediction:** Q/K/V, score/weight/value aggregation and causal visibility have separate explanations; the Transformer overview stops at logits, and the generation loop owns selection and feedback.
- **Probability versus scoring:** predictive entropy concerns the distribution before observing a target; likelihood scores an observed sequence; cross-entropy compares a target distribution with the prediction; batch loss adds explicit masking/reduction; gradients describe sensitivity and the route to parameter updates.
- **Evaluation scope:** the linked experimental-evaluation page is explicitly a protocol-design exercise for a scientific-passage ranker. It is not represented as a benchmark of a locally trained language model.
- **Optional depth:** architecture comparison, Unicode, tokenizer design/evaluation, tensor details, RoPE, cross-attention and advanced attention/decode mechanisms remain optional resources; they do not become prerequisites for the core route.

### Targeted correction: make the two generation readings explicit

The route deliberately places the canonical `generation` page in both Orientation and Inference. Before this pass, the source explained the mechanism but did not tell a first-time reader how to handle this repeated membership. Added a short bilingual instruction to the existing one-minute summary:

- At **Orientation**, read the loop as a black-box preview and retain the fixed-parameter distinction.
- At **Inference**, return to the same page for prefill, incremental decode and selection strategies.

This clarifies the route without creating a duplicate page, a second route registry, or another visual component.

### Remaining validation and limits

- This pass checked the source-level route and page contracts; it did not independently recompute every equation or execute every code block.
- The browser reviews remain separate: #320 (text-to-representations), #337 (global map/navigation), #347 (data → loss → generation and Build crosswalk), and #329 (exercise hub). Use their existing workflows and evidence; do not add another browser workflow.
- Manual screen-reader evidence and native breadcrumb verification remain open under #584. Automated Axe/browser results do not replace them.
- Learner comprehension and transfer have not been measured; retain the pilot under #447.
- No content was removed or merged. The next scientific pass should inspect complete page bodies in small vertical slices, beginning with the probability → entropy → likelihood → cross-entropy → loss chain, then the Build data branch, and record only reproducible or evidence-backed corrections.

## 2026-11-09: mathematical spot-check of prediction → scoring → loss → gradients

**Scope.** Checked the bilingual source equations and worked examples for `probabilities`, `entropy`, `likelihood`, `cross-entropy`, `loss` and `gradients`. Recomputed the small numerical examples independently. This is a bounded equation/example check, not a full proof review of every statement or an execution of the code.

| Page pair | Check | Result |
|---|---|---|
| Probabilities | `softmax(0, ln 3) = (0.25, 0.75)`; temperature scaling preserves logit order for positive temperature while changing concentration. | Correct in the inspected FR/EN text. The page distinguishes normalized probability from calibration and factual truth. |
| Entropy | `H(0.5, 0.5) = ln 2 = 1 bit`; `H(0.9, 0.1) ≈ 0.325 nat ≈ 0.469 bit`; finite-vocabulary bounds are `0 ≤ H ≤ ln V` nats. | Values and units are consistent. Predictive entropy is distinguished from the surprisal of the observed target. |
| Likelihood | `0.5 × 0.25 × 0.8 = 0.1`; total NLL is `−ln(0.1) ≈ 2.303` nats; mean NLL over three targets is about `0.768` nat. | Correct in both languages. The context-window qualification is explicit: one forward pass scores all positions only when the sequence fits the window; longer sequences need an explicit window/stride and target-counting convention. |
| Cross-entropy | One-hot target gives `−ln p(y)`; general target gives `H(q,p) = −Σ qᵢ ln pᵢ`; perplexity is `exp(mean NLL)` in nats and `2^(mean NLL)` in bits. | Formulae and stated units are consistent. The page distinguishes target-distribution cross-entropy from predictive entropy and batch-level loss. |
| Loss | Per-token penalty is `−ln pᵧ`; mean over valid positions divides by `|M|`; ignored positions are excluded from numerator and denominator. | Formula and prose agree in both languages. The page also states that the reference NumPy function covers row-wise classification loss, not sequence shifting, token masks or a complete LLM training objective. |
| Gradients | For one-hot cross-entropy, `∂ℓ/∂zᵢ = pᵢ − 1[i=y]`; chain rule carries this to parameters; gradient descent subtracts the learning-rate-scaled gradient. | The inspected equations and interpretation are consistent in FR/EN. The text does not conflate a gradient with a complete optimizer or guarantee of global improvement. |

### Pedagogical consequence

The progression is mathematically coherent when each question remains distinct:

1. **Before observing a target:** what distribution does the model predict, and how spread out is it? (probabilities, entropy)
2. **After a target is known:** how much probability did the model assign to it, and to the observed sequence? (target probability, likelihood/log-likelihood)
3. **For a target distribution:** what penalty does the prediction incur? (cross-entropy)
4. **Across a batch:** which valid target positions are aggregated, and with what denominator? (loss)
5. **For learning:** how does that objective vary with logits and parameters? (gradients, then optimizer update)

No mathematical correction was justified by this spot-check. The implementation boundary remains important: the conceptual pages describe sequence-level alignment and masking, while the current NumPy loss primitive is intentionally narrower and does not implement a complete sequence training loop.

## 2026-11-09: Build data branch audit — corpus → tokenizer → training examples

**Scope.** Compared the FR/EN `corpus-preparation` and `training-examples` pages, including the worked input-target examples, teacher-forcing explanation, split/tokenizer protocol, windowing contract, document-boundary discussion, mask distinctions and stated implementation limits.

| Area | Source-level check | Result |
|---|---|---|
| Corpus preparation | The page separates source eligibility/provenance, parsing, filtering, deduplication, evaluation splitting, tokenizer fitting/freezing and encoding. | The sequence is presented as a set of decisions, not a universal fixed recipe. It explicitly allows deduplication before splitting or group-aware splitting followed by cross-partition near-duplicate checks, depending on the generalization claim. |
| Held-out protocol | For a conventional held-out experiment, tokenizer fitting uses the training partition only; the tokenizer is then frozen before validation/test encoding. | Correctly scoped as a conventional protocol, not claimed to describe every industrial pretraining pipeline. |
| Input-target shift | For `[t0,t1,t2,t3,t4]` with input length 4, the page pairs `[t0,t1,t2,t3]` with `[t1,t2,t3,t4]`. | Alignment is correct: each input position predicts its next token; the final input token is not its own target. |
| Stride example | For stream `[8,3,3,9,2,7]`, length 3 and stride 1, the first two pairs are `[8,3,3] → [3,3,9]` and `[3,3,9] → [3,9,2]`. | Both FR/EN examples are correct. The prose distinguishes input-window length from stride and states that the last input token needs a successor. |
| Teacher forcing | Reference tokens form the observed prefix; the causal mask restricts each position to its available prefix; the shifted targets provide the next-token labels. | The page distinguishes this conditioning strategy from the objective, loss, optimizer and inference-time generated-token feedback. |
| Document boundaries | Packing, boundary markers and cross-document attention masking are listed as separate decisions. | The important caveat is explicit: an end-of-document token does not by itself block attention. Cross-document masking is implementation- and objective-dependent. |
| Padding and masks | Padding, attention visibility and loss inclusion are treated separately. | The page states that ignored targets should not contribute to the loss, and that flattening/reduction must preserve logits-target-mask alignment. |
| Implementation evidence | `sliding_input_target_pairs` builds complete sliding windows and shifted targets; incomplete corpus tails are dropped. | Scope is not overstated: tokenizer/corpus loading, packing, padding, masks, batching, train/validation splitting and a training loop are not implemented by this helper. |

### Pedagogical hand-off

The Build branch has a coherent responsibility split:

`corpus-preparation → frozen tokenizer / token stream → training-examples → model forward pass → cross-entropy / loss → gradients`.

This is a **construction dependency**, not a prerequisite chain for the conceptual inference route. The short `text-data` lesson remains the prompt-to-token-IDs entry point; the Build pages own corpus governance and training-example construction.

### Findings and next action

No scientific or bilingual correction was justified by this pass. The worked examples, key distinctions and implementation boundaries agree in the inspected FR/EN sources. Continue with the remaining page groups and rendered evidence under the existing #347/#320/#337 reviews; do not create a second data pipeline or duplicate the Build implementation.

## 2026-11-09: practice catalogue and exercise-prerequisite audit

**Scope.** Compared the FR/EN exercise-hub headings, collection-status tables, stable exercise IDs and preparation guidance with the guided route and the canonical lesson ownership. This is a source-level audit of catalogue structure and prerequisites, not a complete solution-by-solution mathematical review or a rendered exercise-hub review.

### Coherence confirmed

- The hub distinguishes short lesson self-checks from longer Practice & experiment exercises; it does not present the hub itself as a lesson or claim every planned collection is complete.
- Text-data exercises progress from representation reconstruction and embedding lookup (TR-A–TR-C), to shifted windows (TR-D), BPE merge counting (TR-E), and split/tokenizer leakage diagnosis (TR-F).
- Q/K/V practice progresses from weighted aggregation and projection reconstruction to parameter-change reasoning, learning, and transfer to cross-attention. CA-A introduces causal masking and prefix invariance independently; AT-A–AT-C then cover multi-head calculation, shapes, and intervention reasoning.
- Transformer exercises TF-A–TF-C use the reference Pre-LN block: shape/normalization tracing, parameter counting, then claim diagnosis and controlled interventions.
- The hub keeps unfinished pretraining, generation, fine-tuning, evaluation, efficiency and advanced collections explicitly marked as planned or incomplete.

### Correction: do not overstate collection-wide prerequisites

The Text data collection's former summary line listed `training-examples` as a prerequisite for the entire collection, although TR-A–TR-C can be started from the text/embedding lessons and only TR-D requires the training-example construction page. TR-E and TR-F have their own distinct preparation pages.

Updated the FR/EN collection introduction to state that the first exercises can start from text/data and embeddings, while each exercise's preparation line is authoritative for additional prerequisites. This avoids making the Build training-data branch look like a prerequisite for the earlier representation exercises.

### Limits

The exercise IDs and prerequisite descriptions are aligned in the inspected FR/EN source. The contents and numerical solutions of every exercise have not been independently re-derived in this pass. The existing #329 browser review remains responsible for rendered desktop/mobile, keyboard and disclosure checks; no new test suite or workflow was added.

## 2026-11-09: optional-resource boundary audit

**Scope.** Inspected the FR/EN metadata and section structure of the ten optional page pairs linked from the guided route: `llm-limits`, `transformer-architectures`, `unicode-text`, `tokenizer-design-evaluation`, `tensors`, `rope`, `cross-attention`, `attention-score-scaling`, `decoding-strategies` and `scaling-laws`.

| Optional resource | Boundary checked |
|---|---|
| LLM limits | Critical reading of the next-token objective, truth, understanding and emergence; does not replace the evaluation-protocol lesson. |
| Transformer architectures | Compares encoder-only, encoder–decoder and decoder-only information flow; keeps architecture, objective and task distinct. Hands-on comparison is linked to Practice rather than becoming a code prerequisite. |
| Unicode text | Covers code points, UTF-8 bytes and normalization before tokenization; does not duplicate tokenization algorithms or embeddings. |
| Tokenizer design/evaluation | Deepens BPE/WordPiece/Unigram mechanisms, budgets, metrics and multilingual trade-offs beyond the core strategy comparison. |
| Tensors | Optional reference for shapes and axes, including the warning that shape compatibility does not prove semantic correctness; explicitly not a prerequisite for the Build path. |
| RoPE | Derives relative-offset dependence and locates rotations in Q/K; does not repeat the general positional-information introduction. |
| Cross-attention | Explains distinct Q versus K/V provenance across representation streams and encoder–decoder/multimodal contexts; remains outside the core self-attention prerequisite path. |
| Attention score scaling | Develops the Gaussian variance argument and its assumptions; does not repeat the four-step attention lesson or become a prerequisite for it. |
| Advanced decoding | Separates distribution transformations from sequence search and discusses reproducibility and quality/diversity; remains optional after core generation. |
| Scaling laws | Treats empirical parameter/data/compute/loss relationships without defining a universal LLM threshold; remains optional rather than a prerequisite to training mechanics. |

The inspected page scopes and headings support their optional/deepening roles in both languages. No optional resource needs to be inserted into the core guided route as a mandatory step. This check does not certify every external citation, equation, figure or rendered layout on these pages; those require their own bounded content/render reviews.

## 2026-11-09: Transformer block and attention — scientific and exercise spot-check

**Scope.** Read the FR/EN source bodies for the Transformer overview, Q/K/V, scaled dot-product attention, causal masking, and the reference pre-LN block walkthrough. Re-derived the displayed one-head attention example, the Q/K/V projection-gradient identities, and the published multi-head exercise calculations AT-A–AT-C. Checked the causal-mask workbench logic against its stated invariant. This remains a bounded source/math audit, not a full certification of every Transformer variant or a rendered accessibility review.

### Conceptual dependency chain

The inspected pages support a coherent division of responsibilities:

1. **Transformer overview:** locates attention, the position-wise MLP, residual paths, normalization, depth/width and the output logits inside the GPT computation. It deliberately does not reteach tokenization or decoding.
2. **Q/K/V:** starts from the current attention input (X), which is not necessarily a raw embedding: it is the hidden state at that block. It defines learned projections and distinguishes routing (Q/K) from transmitted content (V).
3. **Scaled dot-product attention:** calculates (QK^T), scales by the key width, applies an optional additive mask before softmax, and aggregates V. It keeps scores, normalized weights and output vectors distinct.
4. **Causal masking:** specializes the allowed-position relation to (j\leq i), explains why the diagonal is valid under shifted next-token targets, and distinguishes causal, padding, document-boundary and loss masks.
5. **Reference block walkthrough:** makes one concrete GPT-2-like pre-LN implementation inspectable without presenting it as a universal Transformer specification.

The page sequence is pedagogically defensible: Q/K/V establishes the inputs and their provenance; the attention page performs the calculation with a generic optional mask; the causal-mask page then explains the autoregressive restriction. The attention equation already includes (M), so the next page is a specialization of that slot, not a new operation appended after softmax.

### Numerical and algebraic checks

- **Single-head worked example:** (q=(1,0)), (k_1=(1,0)), (k_2=(0,1)), (d_k=2) gives scaled scores ((1/\sqrt2,0)), weights approximately ((0.6698,0.3302)), and output approximately ((6.698,6.604)). The displayed rounded values ((0.67,0.33)) and ((6.7,6.6)) are consistent.
- **Attention self-check:** scores ((2,0)) with (d_k=4) become ((1,0)), giving softmax approximately ((0.731,0.269)). Correct.
- **Projection gradients:** for (Q=XW_Q), (K=XW_K), (V=XW_V), with fixed (X), no bias and the stated matrix orientation, (partial\mathcal L/\partial W_Q=X^T\partial\mathcal L/\partial Q), and analogously for K and V. The page correctly qualifies this as a local linear-projection identity inside the full network.
- **AT-A:** the two head softmaxes are ((3/4,1/4)) and ((1/4,3/4)); their outputs and concatenated vector are correct. (W_O=I) is correctly identified as a special case that does not mix head channels.
- **AT-B:** all batch/sequence/head shapes and the (1/\sqrt{d_{head}}) scale are consistent with the reference implementation, where the combined (d\times d) projections are sliced into heads.
- **AT-C:** the claim classifications and three controlled interventions are consistent with that same reference parameterization. In particular, changing (H) while keeping the packed projection matrices fixed changes the slice width and scaling, not the parameter count or reassembled ((B,T,d)) shape.
- **Causal-mask workbench:** for each query row the diagonal remains allowed, so the row maximum used by the stable softmax is finite. Modifying future K/V positions cannot affect earlier outputs in the isolated head calculation. The page correctly says this is a test of the example, not a proof that a complete model has no other leakage path.

### Targeted editorial corrections

1. The Build walkthrough described pre-LN as simply “more stable” than post-LN when stacking many blocks. Replaced that categorical comparison in FR/EN with a scoped statement: Xiong et al. (2020) analyze better-behaved gradients at initialization for pre-LN in their theoretical/experimental setting, which can reduce warm-up dependence; this is not a universal guarantee. Added the primary PMLR citation.
2. The Q/K/V page said the gradient to Q/K passes through “their normalization”. Replaced this ambiguous phrase in FR/EN with “the softmax that normalizes them”, making clear that it means score normalization rather than LayerNorm.

### Remaining checks

- This pass does not certify the full implementation against every modern attention family (MQA/GQA, grouped or latent attention, sliding-window, sparse, multi-latent, etc.); those remain architecture-specific deep dives.
- The full multi-head causal-mask interaction and padding-query behavior deserve a dedicated bounded exercise/test review before being treated as covered.
- The main conceptual pages and the Build walkthrough have distinct purposes and should remain distinct. Do not fold code-level initialization details into the core learning route.
- Rendered diagrams, equation layout, keyboard behavior and screen-reader output still require the existing browser/manual review workflow. No new workflow or registry was added.

### Implementation-contract clarification: fully masked query rows

The source review also compared the causal-mask lesson with `src/llm_lab/foundations/attention.py` and `tests/unit/test_attention.py`. The primitive explicitly handles a fully masked row by returning zero weights and a zero output; its unit test verifies that this avoids invalid floating-point operations. Such weights are **not** a probability distribution, because they sum to zero. The ordinary causal lower-triangular mask avoids this case by retaining the diagonal.

Added this precise implementation contract to the FR/EN causal-masking pages, while retaining the warning that other APIs/implementations may choose a different convention. This connects the mathematical edge case to the reference implementation without presenting its convention as universal.

The CA-A exercise already distinguishes the causal, padding, loss and document-boundary masks and points to both the isolated attention primitive test and the complete-GPT prefix-invariance test. The reference GPT test compares prefix logits with the corresponding logits from a longer sequence; it does not claim to test arbitrary padding or packed-document policies.

## 2026-11-09: output distribution, scoring and inference — page-pair audit

**Scope.** Reviewed the FR/EN source bodies and route metadata for `logits`, `probabilities`, `entropy`, `likelihood`, `cross-entropy` and `generation`. Compared generation statements with `src/llm_lab/foundations/gpt.py` and `src/llm_lab/foundations/generate.py`. This is a bounded source-level and arithmetic review; it is not a rendered review or a certification of every decoding algorithm.

### Coherence of the conceptual chain

- **Logits → probabilities:** logits are correctly presented as unnormalized vocabulary scores; softmax creates a conditional categorical distribution. The distinction between score ranking, probability, calibration and factual truth is preserved.
- **Probabilities → entropy:** entropy describes the spread of the predictive distribution before observing the next token. The page distinguishes it from the surprisal of the realized target.
- **Observed token → likelihood:** the chain-rule factorization scores the observed sequence using reference prefixes and fixed parameters. The explanation correctly avoids assuming independence between tokens.
- **Likelihood → cross-entropy:** for one-hot targets, token NLL is the corresponding cross-entropy term. The pages distinguish total sequence NLL, mean per-token NLL and batch loss with explicit masking/reduction.
- **Inference loop:** generation repeats context processing, next-token selection, appending and stopping. Prefill and incremental decode are execution phases; decoding is the token-selection/transformation procedure. The page explicitly separates prefill from teacher forcing.

The FR/EN route metadata and the inspected conceptual distinctions align. The canonical sequence does not imply that entropy, likelihood and cross-entropy are interchangeable: they answer different questions about a distribution, an observed sequence and a target distribution.

### Arithmetic and source-contract checks

- The two-logit example ((0,\log 3)) gives probabilities ((0.25,0.75)).
- The probability example's initial temperature explorer uses logits ((3,1.5,1,0.2)); the displayed initial percentages (about 70.5%, 15.7%, 9.5%, 4.3%) are consistent with softmax at temperature 1.
- The entropy examples ((0.5,0.5)) and ((0.9,0.1)) give (\log 2) nats (1 bit) and about 0.325 nats (0.469 bit), respectively.
- The likelihood example ((0.5,0.25,0.8)) gives sequence likelihood (0.1), total NLL about 2.303 nats and mean NLL about 0.768 nat per token.
- The one-hot cross-entropy formula (-z_y+\log\sum_j e^{z_j}), its gradient (p_i-\mathbf 1[i=y]), and perplexity (\exp(\text{mean NLL in nats})) are consistent with the stated conventions.
- The reference `generate.py` reprocesses the full available context window at each step; it has no KV cache, optimized incremental decode, or EOS early-stop. It stops after the requested `max_new_tokens`. The page already documented the first two limitations; added the missing stopping detail in FR/EN so the generic conceptual stop criteria are not mistaken for the current code contract.

### Targeted correction: finite temperature is not uniform

The interactive temperature explainer described every (T>1) as producing a “uniform distribution”. For a finite temperature, the distribution becomes flatter relative to (T=1), but is not generally uniform; uniformity is approached as temperature tends to infinity (for finite logits). Reworded the FR/EN explanatory text to say “flatter” and “approaches uniformity as temperature increases”. The surrounding mathematical explanation was already correct.

### Remaining checks

- This pass did not audit top-k/top-p or beam-search algorithms in full; they remain in the optional decoding-strategies lesson.
- No learner study was conducted to determine whether the distinction between decode, decoding and generation is retained by first-time readers; the wording is now explicit but transfer still needs testing.
- The interactive temperature component's runtime behavior, keyboard operation and responsive layout remain part of the existing rendered/browser review.
- The source implementation intentionally differs from a production inference engine. Preserve this distinction rather than adding cache or serving complexity to the pedagogical reference implementation.

### Scope clarification for causal-mask tests and padding

A final cross-check of the reference implementation confirmed that the full-GPT prefix-invariance test exercises causal self-attention only. `GPT.forward` accepts token IDs and the Transformer block constructs its causal mask internally; the reference model does not expose a padding-mask argument or implement packed-document boundary masking. The exercise had already distinguished those mask types conceptually, but its test evidence could be misread as validating them. Added this implementation boundary in FR/EN immediately after the two test descriptions. The test claims now match the actual code surface.

## 2026-11-09: training-example implementation and test-quality check

**Scope.** Compared `training-examples.qmd` and `corpus-preparation.qmd` with `sliding_input_target_pairs` and its unit tests. The implementation's window-count formula, input/target offset, stride semantics and incomplete-tail handling agree with the lesson's examples. The helper intentionally does not implement corpus loading, tokenization, packing, padding, masks or an optimizer/training loop.

**Test defect found and corrected.** `test_every_target_is_the_next_token_in_the_stream` used `np.arange` token IDs and checked the final target with `stream[inputs[:, -1] + 1]`. Because token IDs happened to equal their source positions, this assertion accidentally treated an ID as a position. It would not be valid for an arbitrary token stream and did not independently express the window-offset invariant.

Changed the fixture to non-monotonic token IDs unrelated to positions, then computed each final target's source position from the window start, stride and context length. The within-window shift assertion remains separate. This makes the test verify the actual contract: targets are the next source token at the corresponding position, not the token ID plus one.

The corrected expected final targets for the fixture are `[3, 14]` at source positions 4 and 7. The Python CI run for the updated PR head is required to confirm the change; no local test execution is claimed.

## 2026-11-09: loss-to-gradient aggregation bridge

**Scope.** Compared the FR/EN `loss` and `gradients` pages with `cross_entropy_from_logits`, `cross_entropy_gradient` and their tests.

The reference NumPy loss computes an unweighted mean across batch rows; its gradient correspondingly divides each row's (p-y) vector by the batch size. The lesson on gradients displayed the correct local, one-position derivative (p_i-\mathbf 1[i=y]), then moved to a vector of all batch logits without explicitly showing how the mean-over-valid-positions convention changes that derivative. The preceding loss page defined the denominator, but the hand-off between pages was implicit.

Added the explicit FR/EN formula for the unweighted mean over valid target positions:
- valid position: ((p_{b,t,i}-\mathbf 1[i=y_{b,t}])/|\mathcal M|);
- ignored position: zero derivative with respect to that position's logits for this objective.

The text states that sum, weighting and other reductions change the corresponding factor. This connects the local cross-entropy derivative to the actual batch objective without claiming that the reference classification primitive implements sequence masks or a complete LLM loss.

### Checks

For a batch of (B) rows, the implementation returns ((p-y)/B); its unit tests compare this gradient with central finite differences, verify row sums of zero, check invariance to row-wise constant shifts and reject invalid inputs. The conceptual page remains broader than this primitive and keeps sequence shifting/masking outside the implementation's scope.


## 2026-11-09: loss masking versus attention visibility — gradient-flow clarification

**Scope.** Cross-checked the FR/EN loss and gradients lessons against training-examples.qmd, causal-masking.qmd, and the stated batch objective. This is a conceptual dependency review; the small NumPy classification-loss primitive is not a sequence-loss or masking implementation.

### Finding and correction

The loss pages correctly define the valid target-position set and exclude ignored targets from both numerator and denominator. The gradient pages correctly state that the derivative with respect to logits at an ignored position is zero for this objective. However, those statements could be misread as saying that a loss mask also prevents the corresponding token representation from influencing valid predictions, or that all gradients associated with that position must vanish.

That inference is not generally valid. A loss mask selects supervised target positions. An attention mask controls which positions may influence other position representations. If an ignored position's representation is used in computing a valid-position logit (for example, as an allowed key/value), gradients from that valid loss can still propagate through the dependency. The exact behavior depends on causal direction, padding side, mask semantics and the architecture.

Added a concise explanation and links to the canonical training-example and causal-masking lessons in both loss pages. Added a collapsed advanced note in both gradients pages to distinguish a zero derivative with respect to an ignored position's logits from the possible gradient flow through that position's representation when it contributes to valid logits.

### Boundary retained

- No claim that the current reference GPT implements padding or packed-document masks; its forward interface still exposes only token IDs and internal causal masking.
- No sequence-loss API, padding policy, or training loop was added to the NumPy foundations.
- The page prose distinguishes these roles, but the concept registry previously contained only the causal-mask concept and the computational graph represented the loss mask only generically inside loss reduction. Added explicit concepts for attention, padding, document-boundary and loss masks to the existing concept registry, with bilingual definitions, domains, importance and canonical page resources. The computational graph remains unchanged: its documented scope deliberately excludes batching, padding and training-window sampling, and no concrete implementation currently justifies adding those dataflow nodes.

### Validation limits

The correction is bilingual and source-level. The Quarto render and existing metadata/link checks should validate the edited pages; a rendered browser review and an executable padded/packed batch example remain separate work. No new workflow or test harness is introduced.

## 2026-11-09: greedy decoding versus sequence-level maximum — deterministic counterexample

**Scope.** Extended the FR/EN decoding-strategies lesson in response to issue #84. The example is a fixed-horizon, two-step conditional tree; it is a mathematical toy, not a model benchmark.

Used first-step probabilities P(A)=0.60 and P(B)=0.40, followed by P(x|A)=0.51, P(y|A)=0.49, P(z|B)=0.99 and P(w|B)=0.01. Greedy decoding returns A x with probability 0.306, while exhaustive enumeration identifies B z with probability 0.396. The distinction is between locally maximizing each next-token probability and maximizing the product of conditional probabilities over a complete fixed-length sequence.

Added a runnable NumPy snippet in both languages. It uses log-probabilities as logits so that softmax recovers the stated conditional distributions, enumerates the four complete sequences, and prints the greedy and sequence-MAP outcomes. No randomness, external model, download, or training is involved.

Explicitly bounded the conclusion: exhaustive enumeration is feasible here only because the tree is tiny and the horizon fixed. Longer horizons and larger vocabularies make it expensive; beam search is an approximate search over prefixes. Variable-length stopping and length normalization change the comparison objective.

### Validation still required

- Execute the snippet in CI or an equivalent checked environment; verify the four sequence scores and bilingual parity.
- Quarto render, local-link checks and targeted browser review on the PR head.
- This example satisfies the issue's greedy-versus-sequence-MAP challenge; it does not claim to implement beam search or establish a general decoding-quality ranking.

### Evaluation metrics: likelihood is not task quality

Extended the evaluation section with explicit bilingual links and a bounded example: likelihood/NLL (and derived perplexity) scores observed tokens on a corpus; it does not directly measure factuality, instruction following or user utility. Task metrics only measure the operationalized property and protocol. The existing experimental-evaluation exercise's Average Precision measures ranking quality, not probability calibration. This reuses existing lessons rather than introducing a new metric or page.

The user-supplied YouTube URL in issue #84 could not be verified through the available source retrieval: the direct page fetch returned a cache miss and exact video-ID search returned no result. It is therefore not cited or incorporated; its title/transcript and timestamps remain unverified.

## 2026-11-09: targeted browser review — decoding strategies (PR #728)

**Scope.** Reviewed the rendered English and French `decoding-strategies.html` pages on the PR head `c3324c1` using the existing targeted Playwright browser-review job. This is evidence for the changed page pair only, not a site-wide visual certification.

- Both pages returned HTTP 200 at a 1440 × 1000 desktop viewport in the light theme.
- No horizontal overflow was detected; no unrendered math was detected (15 math spans per page).
- The learning-path context was present, its navigation landmark and accessible label were exposed, and its stage anchor resolved.
- All 34 focus targets on each page were reported focus-visible; axe reported zero accessibility violations for these runs.
- The job generated screenshots and a machine-readable audit report in artifact `site-browser-review-921a135ecf610af84ed4c814c3e140ed1a8e79f0` (run [42599137931](https://github.com/JM-Brun/llm-lab/actions/runs/42599137931)).

**Limit.** This targeted profile selected the two changed language variants at desktop size only. It does not establish mobile layout, dark-theme behavior, screen-reader usability, or learner comprehension. Those remain separate checks; do not describe this as a full manual review.

The YouTube resource supplied in issue #84 remains unverified: direct retrieval previously returned a cache miss and an exact video-ID web search on 2026-11-09 returned no result. No title, transcript, timestamps, or claims are inferred from the URL.


## 2026-11-09: ranking quality versus probability calibration

**Scope.** Added a deterministic binary-ranking counterexample to the FR/EN decoding-strategies lessons, extending the existing distinction between Average Precision (AP) and calibration. No new page, concept-registry entry, dependency, model benchmark or evaluation framework was added.

The four labels are `[1, 0, 1, 0]`. Score set A is `[0.65, 0.55, 0.45, 0.35]`; score set B is `[0.99, 0.89, 0.11, 0.01]`. B is a strictly increasing transformation of A, so both produce the same ranking and AP = 5/6 ≈ 0.833. With the explicitly fixed bins [0, 0.5) and [0.5, 1], both bins have observed positive frequency 0.5. The weighted ECE is 0.10 for A and 0.44 for B.

A standard-library Python snippet in each language page computes AP and this two-bin ECE and asserts the expected values. The text states that ECE depends on binning and that the four-observation example is illustrative, not a reliable calibration estimate or an empirical LLM evaluation.

**Validation still required:** execute both snippets, verify FR/EN semantic parity, run Python CI and Quarto render/local-link checks, then inspect the exact rendered changes. Mobile layout is intentionally not a gate for this source/content slice and remains a later release-review task.

## 2026-11-09: execution of decoding/evaluation teaching examples

**Scope.** Executed the exact Python code blocks from the FR and EN `decoding-strategies.qmd` pages for the greedy-versus-sequence-MAP counterexample and the AP-versus-ECE calibration counterexample. The corresponding FR/EN code blocks were compared and are identical.

**Results.**
- Greedy counterexample: `('A', 'x')`, sequence probability 0.306; exhaustive fixed-horizon MAP sequence `('B', 'z')`, probability 0.396.
- Calibration counterexample: AP = 0.833 for both strictly rank-preserving score sets; two-bin size-weighted ECE = 0.10 and 0.44, respectively. The source assertions passed.

**Rendered/build evidence.** The AP/ECE lesson changes are integrated through PR #740; its final-head Python CI and Quarto site workflows both succeeded. The targeted responsive browser evidence for the FR/EN page pair is separately recorded above from PR #736. It covers desktop/mobile at 390 × 844 and 1440 × 1000 in the light theme; it does not establish dark-theme, screen-reader or learner-comprehension behavior.

**Limits.** The greedy snippet prints its expected values but does not contain assertions; this pass verified the outputs manually. The examples are deterministic teaching counterexamples, not model benchmarks or reliable calibration estimates. This execution does not audit the complete top-k/top-p/beam-search implementations or establish learner transfer.

## 2026-11-09: contrastive decoding versus contrastive search

**Scope.** Audited the terminology used in the FR/EN decoding-strategies lesson against the original methods and the versioned Transformers guide.

- Li et al. (ACL 2023) contrastive decoding contrasts expert/amateur model log-likelihoods under an expert plausibility constraint.
- Su et al. (NeurIPS 2022, §3.2) contrastive search uses one model, a top-k candidate set, model confidence and a maximum cosine-similarity degeneration penalty over contextual token representations.
- The candidate-set (k) in contrastive search is not top-k sampling: one selects a candidate by a penalized objective; the other truncates a distribution and samples.
- The FR/EN lesson now distinguishes the methods and gives the original contrastive-search objective. It explicitly states that the teaching GPT does not implement this method.

**Sources.** Li et al., https://aclanthology.org/2023.acl-long.687/ ; Su et al., https://papers.nips.cc/paper_files/paper/2022/file/871cae8f599cb8bbfcb0f58fe1af95ad-Paper-Conference.pdf ; version-specific Transformers 4.46 guide, https://huggingface.co/docs/transformers/v4.46.0/en/generation_strategies.

**Boundary.** The Transformers reference is explicitly versioned; no claim is made that the same parameterization is present in the current release. This is a conceptual clarification, not a new implementation, concept node, page or dependency.


## 2026-11-09: beam-search score and stopping-policy qualification

**Scope.** Completed the bounded source audit of the beam-search explanation in the FR/EN decoding-strategies lessons against the current Hugging Face generation API and implementation documentation, while rechecking the existing local top-k/top-p reference implementation and tests.

**Findings.**
- The local `top_k_filter` keeps exactly the requested number of highest-probability entries (stable ties by original index), then renormalizes. `top_p_filter` keeps the smallest descending-probability prefix whose cumulative mass reaches or exceeds the threshold, including the crossing token, then renormalizes. The unit tests cover these contracts, ties, threshold boundaries, distribution-shape dependence, temperature-before-filtering behavior, determinism, input immutability and invalid inputs.
- The teaching generation path applies temperature, then top-k, then top-p before sampling. This is a deliberately bounded pedagogical contract, not a universal ordering. The reference does not implement beam search, configurable logits processors, contrastive decoding or penalties.
- Beam search accumulates token log-probability scores, but practical implementations may apply length normalization and distinct early-stopping policies. The current Transformers documentation describes `length_penalty` and `early_stopping` options; these affect hypothesis ranking and termination. The existing fixed-horizon A/B counterexample is correctly scoped as unnormalized sequence-MAP, not a complete production beam-search specification.
- The current Transformers source assembles multiple logits processors/warpers in an implementation-specific sequence; its ordering is not a cross-library standard. Parameter names alone therefore do not define an experiment.

**Change.** Added a concise FR/EN qualification after the beam-search definition, explicitly separating fixed-length sequence probability from length-penalized beam scores and early-stopping behavior. Added the official generation API reference. No new implementation, dependency, concept node, page or workflow was added.

**Sources.**
- Transformers generation API: https://huggingface.co/docs/transformers/main_classes/text_generation
- Transformers generation configuration: https://github.com/huggingface/transformers/blob/main/src/transformers/generation/configuration_utils.py
- Transformers generation processor construction: https://github.com/huggingface/transformers/blob/main/src/transformers/generation/utils.py
- Local implementation: `src/llm_lab/foundations/decoding_filters.py`; tests: `tests/unit/test_decoding_filters.py`.

**Validation boundary.** The top-k/top-p code and tests were inspected at source level in this pass; no new local test run is claimed. PR CI and Quarto render are required for this documentation change. This does not close the outstanding mobile/dark-theme, screen-reader or independent learner-evidence tasks in #84/#584/#447.


## 2026-11-09: PyTorch cross-entropy API example (FR/EN)

**Scope.** Add one bounded, self-contained PyTorch example to the bilingual cross-entropy lessons, complementing rather than replacing the project's NumPy reference.

**Teaching contract.** The snippet uses logits `(B,T,V)` and integer targets `(B,T)` already aligned to the prediction positions; it flattens `(B,T)` to the batch axis required by `CrossEntropyLoss`. It shows per-position losses with `reduction='none'`, a valid-target mean with `ignore_index=-100`, agreement with an explicit `log_softmax`/gather calculation, and the numerical change caused by incorrectly applying softmax before the loss API. It explicitly does not implement autoregressive shifting, attention masks, or a training loop.

**Execution.** The exact example was executed locally with PyTorch 2.10.0+cpu. Per-token losses were `[0.169846..., 1.551444..., 0.0]`; mean loss and manual calculation both equalled `0.860645...`; applying softmax first yielded `0.946560...`. All `torch.testing.assert_close` assertions and the negative-control assertion passed.

**Boundaries.** This is a documentation example, not a new runtime dependency or package implementation. The existing maintained NumPy reference remains limited to `(B,C)` row-wise mean loss; the PyTorch snippet demonstrates sequence-shaped API adaptation and ignored targets. It assumes the caller has already aligned labels and logits.

**Sources.** PyTorch `CrossEntropyLoss` API: https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html ; PyTorch `LogSoftmax`: https://docs.pytorch.org/docs/stable/generated/torch.nn.LogSoftmax.html.


### Source-to-claim mapping — cross-entropy API example

| Claim in the bilingual example | Source | Scope/qualification |
|---|---|---|
| `CrossEntropyLoss` consumes unnormalized class logits; class-index targets, `ignore_index` and `reduction` determine the per-target and aggregated loss. | [PyTorch 2.14 CrossEntropyLoss documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) | Official API contract. The example uses unweighted class-index targets and the default `ignore_index=-100`; it does not cover probability targets, class weights or label smoothing. |
| `LogSoftmax` computes log-softmax as one operation with better numerical properties than separate softmax then log. | [PyTorch 2.14 LogSoftmax documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.LogSoftmax.html) | API/numerical guidance used for the manual cross-check; not a new mathematical definition. |
| The common language-model logits shape `(B,T,V)` must be rearranged to place classes at dimension 1 for the flattened `(B*T,V)` class-index call. | CrossEntropyLoss input-shape contract above; executable example in FR/EN lesson. | This example flattens positions into the sample dimension. It assumes targets are already aligned and does not implement the causal shift. |
| The ignored target does not contribute to the mean reduction. | CrossEntropyLoss `ignore_index`/`reduction='mean'` documentation above. | Valid for this unweighted class-index example; weighted-mean semantics differ and are not demonstrated. |

The source table covers the newly added PyTorch API example only. It does not close the wider source-to-claim audit for the complete logits → probabilities → likelihood → cross-entropy → loss page group.


## Focused source-to-claim audit: logits → probabilities → likelihood → cross-entropy → loss

**Scope.** This mapping records which external sources support which claims in the bilingual mathematical chain. It does not certify every equation, diagram, link, or rendered page. Mathematical identities derived directly in the lessons remain the responsibility of the local derivation and numerical examples; API documentation is not treated as a mathematical authority.

| Claim used in the lesson group | Source and exact role | Boundary / verification note |
|---|---|---|
| Logits are unnormalized real-valued class scores; class-index targets and ignored targets have defined shape/range and reduction semantics in the framework API. | [PyTorch `CrossEntropyLoss`](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html): API contract, including logits input, class-index targets, `ignore_index`, and `none` / `sum` / `mean` reductions. | Supports implementation behavior, not the definition of logits or the mathematical derivation of cross-entropy. The sequence example must explicitly place classes on the vocabulary axis and align targets before flattening. |
| The cross-entropy implementation for class-index targets is equivalent to log-softmax followed by negative log-likelihood; logits should be passed directly rather than softmax-normalized first. | [PyTorch `CrossEntropyLoss`](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html): explicitly documents the log-softmax + NLL equivalence. | The bilingual lesson's manual `log_softmax`/gather calculation is a local numerical cross-check. It is not a separate implementation of the framework API. |
| Maximum likelihood for observed data, including conditional likelihood, becomes a sum of log probabilities; maximizing it is equivalent to minimizing negative log-likelihood and, in the categorical empirical-target setting, cross-entropy. | Goodfellow, Bengio & Courville, [*Deep Learning*, §5.5 and §5.5.1](https://www.deeplearningbook.org/contents/mlp.html): general MLE and conditional log-likelihood framework. | The book supplies the statistical framework. The autoregressive factorization over token positions is the LLM-specific application explained locally; do not attribute the Transformer-specific sequence construction to this chapter. |
| Entropy is the expected information content of a discrete distribution, with logarithm base determining bits versus nats. | Shannon (1948), [*A Mathematical Theory of Communication*](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x): foundational definition of discrete-source entropy and logarithm-base interpretation. | Shannon's paper is historical foundation, not a source for PyTorch conventions or the full modern neural-network cross-entropy API. The identity between cross-entropy, entropy and KL divergence is derived in the lesson and separately checked algebraically. |
| The cross-entropy gradient for one-hot targets is $p_i-\mathbf{1}[i=y]$, and this is a derivative with respect to logits rather than model parameters. | Local derivation in the bilingual cross-entropy/gradients lessons; the framework references above establish the implemented objective, not this derivative as a pedagogical proof. | Keep the boundary explicit: obtaining parameter gradients requires the chain rule through the network. The maintained NumPy helper currently covers row-wise $(B,C)$ loss and logits gradient only, not full sequence masking or GPT-weight backpropagation. |
| For $(B,T,V)$ sequence logits, softmax must normalize over $V$ at each $(B,T)$ position; a wrong axis changes the modeled distribution. | Local invariant and adversarial counterexample in the bilingual lesson, integrated by [PR #809](https://github.com/JM-Brun/llm-lab/pull/809). | This is a tensor-semantics claim verified by the lesson's numerical assertion, not by the PyTorch API citation alone. |
| Stable log-softmax/cross-entropy avoids the underflow failure of explicitly computing softmax probabilities and then taking their logarithm. | [PyTorch `CrossEntropyLoss`](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) documents the log-softmax + NLL composition; [PyTorch `functional.log_softmax`](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.log_softmax.html) explicitly states that separate softmax then log is numerically unstable; the extreme-logit example in [PR #809](https://github.com/JM-Brun/llm-lab/pull/809) demonstrates the failure mode. | The example demonstrates one finite-precision case; it is not a general benchmark of all kernels, dtypes, or devices. |

**Audit outcome.** The source roles are now explicit: Goodfellow supports the MLE/NLL statistical bridge; Shannon supports the entropy foundation; PyTorch specifies framework/API behavior; local derivations and executable counterexamples support the LLM-specific tensor, axis, masking, and gradient claims. No source should be cited as proving claims outside its stated role.

**Remaining validation.** This source map does not replace a fresh bilingual rendered review of the full page group. The recent #809 browser evidence covers its changed cross-entropy pages on its tested head, not every page in the logits → probabilities → likelihood → cross-entropy → loss chain.


## Transformer boundary audit — 2026-11-10

This source-level review resumes the first Transformer slice and focuses on the boundary between the conceptual mechanism, the reference implementation, and the assembled GPT. It does not claim a fresh rendered-page or learner-comprehension review.

| Layer | Canonical ownership | Evidence inspected | Boundary to preserve |
|---|---|---|---|
| Conceptual mechanism | `site/fr/transformer.qmd` / `site/en/transformer.qmd`, with component lessons for Q/K/V, scaled attention and causal masking | The overview explains attention versus position-wise MLP, residual paths, normalization, depth/width and the path to logits. | Explain the block's input/output contract and distinguish attention sublayer, complete block and GPT assembly. Do not teach implementation details here. |
| One block implementation | `site/fr/transformer-block-walkthrough.qmd` / `site/en/transformer-block-walkthrough.qmd` | The walkthrough follows the pre-LN `TransformerBlock` implementation: Q/K/V/O, head slicing, causal attention, residual paths, LayerNorm and GELU MLP. | Keep it code-first: parameter initialization, concrete tensor shapes, source lines and tests. It implements one selected architecture, not every Transformer variant. |
| GPT integration | `site/fr/gpt-model-walkthrough.qmd` / `site/en/gpt-model-walkthrough.qmd` | The walkthrough traces token/position embeddings, repeated blocks, final normalization and the vocabulary projection from `(B,T)` to `(B,T,V)`. | Do not re-explain block internals; explain repetition, interfaces, output logits and model-level invariants. |
| Build crosswalk | `site/fr/build-path.qmd` / `site/en/build-path.qmd`; `docs/learning-path.md` | The G4 attention primitive spans `attention.py` and the attention sublayer in `transformer_block.py`; G5 owns full block composition and GPT assembly. | A source file may serve more than one milestone at different scopes. Do not split modules solely to make the curriculum labels look one-to-one. |

### Findings and corrections

- The conceptual overview already had the right high-level ingredients, but did not state the three scales as an explicit contract. A short bilingual section now distinguishes attention sublayer → Transformer block → assembled GPT and gives the block's `(B,T,d)` input/output contract.
- The Build table previously linked the entire block walkthrough from both G4 and G5 without explaining the different scopes. G4 now points to the attention section and owns the single-head primitive plus its multi-head integration; G5 owns the complete pre-LN block and GPT assembly.
- The model walkthrough now explicitly starts where the block walkthrough ends: it follows repeated blocks and the model-level input/output interfaces rather than re-teaching the block.
- No new registry, page, Python module, workflow or diagram framework is introduced. The existing conceptual route, Build milestones and bilingual canonical pages remain the sources of truth.

### Validation still required

This change is a source-level editorial correction. Run the existing Python CI and Quarto render/static checks, then inspect the changed FR/EN pages at desktop and mobile widths. Verify the new section anchors, math rendering and the G4/G5 links in the built site. This source review does not establish screen-reader usability or learner mastery.


## Q/K/V reader-experience audit — 2026-11-10

A focused source-level audit compared the bilingual Q/K/V concept lesson with the preceding Transformer overview, the following scaled dot-product attention lesson, and Nishanthan K's [DEV Community article](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a). The review follows the repository's Understand Path Audit skill. It found a sound conceptual boundary and strong scientific content, but identified two high-impact teaching gaps: no worked numerical example of the projections, and no concrete motivating problem near the opening. The existing two-path SVG was retained and its alt text clarified; the coreference example was moved to the opening and the lexical-ambiguity example remains as one optional note.

The bilingual concept pages now include observable conceptual learning outcomes and an early qualified coreference example, while keeping numerical matrix calculations out of the conceptual route. The two-dimensional Q/K/V calculation and W_V-only intervention have been moved into the matching French and English Attention exercise collections with collapsed worked solutions. The complete audit, route analysis, arithmetic, preservation decisions, and validation limits are recorded in [Q/K/V pedagogical audit and revision](audits/qkv-pedagogical-audit.md).

**Status:** Updated in PR/branch; source-level checks completed. Quarto render, published-page browser review, and learner task testing remain open. This is not a rendered-site or learner-outcome certification.


**Q/K/V reading-flow follow-up — 2026-11-10:** the bilingual concept pages now open with the contextual problem before introducing terminology, define Q/K/V in parallel, place the existing two-path diagram immediately after the definitions, and transition from that diagram to the shared-input projection equations. Repeated summaries and competing illustration/history detours were removed from the core reading path; geometry, training, architecture variants, and lexical ambiguity remain optional. Numerical calculations remain exclusively in the Attention exercises. See [the focused Q/K/V pedagogical audit](audits/qkv-pedagogical-audit.md).


**Q/K/V content-preservation follow-up — 2026-11-10:** a before/after content audit distinguished equivalent reformulations from genuinely omitted nuances. The routing-versus-content distinction (including the fact that K and V need not encode the same feature), the warning against nearest-value selection, the historical and external visual references, and an explicit hand-off to existing projection/intervention/gradient/cross-attention/GQA-MQA exercises were restored or made discoverable. The per-position equations and summary table remain intentionally consolidated into equivalent matrix notation and the new narrative. See [the Q/K/V pedagogical audit](audits/qkv-pedagogical-audit.md).


## Q/K/V advanced deep dive — 2026-11-10

A dedicated bilingual Deepen page now owns the material previously scattered across collapsed callouts or compressed out of the core reading flow: individual per-position equations, batched tensor shapes, dot-product geometry, routing/content nuance and the nearest-value caveat, local gradient paths through a standard attention head, multi-head projection layout, MQA/GQA, projection-parameter tying, lexical ambiguity and limits of attention-map interpretation, and supplementary resources. The core Q/K/V lesson retains the essential distinction and links to this page. Cross-attention remains owned by its existing dedicated page; numerical hand calculations remain in the Attention exercises.

**Validation boundary:** source-level editing only at this stage. Quarto render, generated metadata/context validation, link checks, bilingual rendered review, and CI remain pending.


## Representations and embedding-lookup audit — 2026-11-10

A source-level pedagogical audit reviewed the bilingual Understand lessons on token embeddings (`embedding-space.qmd`) and contextualized representations (`contextualized-representations.qmd`), together with their transitions from the text-data stage and towards the Transformer overview. The review follows the repository's Understand Path Audit skill and page design guidelines. It identified four high-value teaching enhancements: collapsible learning outcomes, interactive pipeline steppers and epistemic badges, executable NumPy micro-workbenches with shape and equality invariants, and folded active-recall refutations of common fallacies (consecutive integer ID proximity and polysemy ID requirements).

Both French and English pages now incorporate these interactive pedagogical components while strictly preserving existing SVGs, asset reuse reviews, and reproducible tokenizer traces. The self-check sections now cross-link directly to the matching exercises in the catalogue (`Exercise TR-B` for embedding lookup and `Exercise TR-C` for context differentiation). The full methodology and preservation checks are recorded in [Representations and embedding-lookup audit](audits/representations-pedagogical-audit.md).

**Status:** Updated in PR/branch; source-level checks completed. Quarto render, published-page browser review, and learner task testing remain open. This is not a rendered-site or learner-outcome certification.

## Deepen case-study source audit — cosine similarity and embedding linearity (2026-11-11)

**Scope:** FR/EN source-level review of the two Deepen case studies recorded as "Not reviewed" in the coverage reconciliation table: `cosine-similarity.qmd` and `linearite-embeddings.qmd` / `embedding-linearity.qmd`. This pass inspected frontmatter, page-map blocks, route metadata, section structure, the evidence boundary of each scientific claim, and FR/EN parity. It did not render pages in a browser, run the proposed experiments, or independently re-verify the cited 2025–2026 papers.

| Page pair | Review result | Evidence boundary / remaining action |
|---|---|---|
| `site/fr/cosine-similarity.qmd` / `site/en/cosine-similarity.qmd` | Both pages separate geometric similarity from semantic equivalence consistently. The Steck et al. result is scoped to some regularized linear model families and explicitly not generalized to all modern encoders; the Li et al. (EMNLP 2020) anisotropy findings are scoped to "their experiments"; hubness and anisotropy are presented as measurable diagnostics, not automatic explanations of retrieval errors. The metric-choice guidance (cosine vs dot product, normalization contract) matches the cited Sentence Transformers documentation. The section-4 experiment is labelled as an experiment to add to the repository, not an implemented one; the Python snippet documents its input assumptions and numerical limits. FR and EN sections, misconception blocks, counterexamples and resource lists correspond. | Rendered/browser review, link checks, and independent verification of the recent citations (Steck et al. WWW 2024; Nastase & Merlo 2025; Nielsen & Hansen 2024) remain open. A cited source is not proof of every sentence. |
| `site/fr/linearite-embeddings.qmd` / `site/en/embedding-linearity.qmd` | Both pages distinguish linear representation, linear accessibility/decodability and functional use, and never claim that a successful probe establishes causal use. The XOR counterexample and the product-feature transformation are mathematically correct and used only to illustrate representation dependence. Superposition (Elhage et al. 2022) and multidimensional features (Engels et al. 2025; Tiblias et al. 2026) are reported with their scope limits; the Barin-Pacela PMLR-versus-arXiv-v2 version note (dictionary learning as the binding constraint, corrigendum) is present in both languages and warns against the over-general summary. Experiments A and B are proposals with explicit expected-result caveats, not executed tests. | Rendered review, any future implementation of the proposed experiments, and independent verification of the 2026 citations (Garg et al.; Barin-Pacela et al.; Tiblias et al.) remain open. Do not cite this row as evidence that the experiments run. |

**Minor source observations (cosmetic, not blocking):**

1. In the learning-resources blocks of both pairs, a first `####` sub-heading ("Lectures critiques" / "Critical reading" on cosine-similarity; "Lectures scientifiques et techniques" / "Research and technical reading" on linearity) is immediately followed by the next sub-heading with no content, which renders an empty heading in both languages.
2. The EN linearity page keeps the French-style section number "3 bis", which is not idiomatic English; renumbering (e.g. "3a" or a renumbered list) is a cosmetic localization fix for a future pass.
3. The local `language-switch` block is present on both FR pages (canonical wrapper per #958/#962) and absent on both EN pages. The contract makes the block optional, so this is a documented asymmetry rather than a violation; confirm the intended direction with the owner before changing anything.
4. The takeaway placement differs slightly: the FR linearity page opens its conclusion with the embedding-space link while the EN page closes with a "Canonical lesson" sentence. Semantically equivalent.
5. Neither pair carries `description-meta:` because its page-map block has no `summary:` field; per the merged T1 rule (#961) these pages keep the subtitle fallback for the meta description. Consistent, not a defect.

**Validation status:** source-level review only. No Quarto render, browser inspection, or independent re-derivation of the cited results was run for this entry.

## Entry-point source audit — FR/EN landing pages (2026-11-12)

**Scope:** FR/EN source-level review of the site entry points recorded as "Not reviewed" in the coverage reconciliation table: `index.qmd` (root, FR) and `en/index.qmd` (EN landing). Per the protocol, the entry point is reviewed first among the remaining rows. This pass inspected frontmatter, page-map blocks, route selection, status honesty, equivalent FR/EN entry affordances, the interactive SVG process figure, and cross-language and bibliography links. It did not render pages in a browser, run an assistive-technology pass, or test touch or keyboard behavior beyond source inspection.

| Page pair | Review result | Evidence boundary / remaining action |
|---|---|---|
| `index.qmd` (FR) / `en/index.qmd` | Route selection is honest and symmetric: two independent primary paths (Understand / Build) plus Deepen and always-available practice affordances; both languages state that neither path is a required continuation of the other, and both state the theory-path prerequisites. Status honesty holds: the Build entry says reference inference is tested and complete training remains to be implemented, identically in FR and EN. Entry affordances (hero actions, three-card grid, practice block, three epistemic badges, the clickable SVG figure, the "three sibling uses" callout, explore-further links, language switch) are present in both languages with matching content. The SVG figure uses language-suffixed ids and labels, `role="link"`/`tabindex`/Enter activation in both languages, and `.html` `data-href` targets, so the incremental-render source-link defect (#983, fixed by #993) does not apply to it. Page-map parity is exact: the same seven children and the same `suggested_route.next` to llm-overview, matching guided-route step 01. | Rendered/browser review, link checks, and a keyboard/screen-reader pass on the SVG interactions remain open. |

**Minor source observations (cosmetic, not blocking):**

1. The EN "Run locally" badge adds an explicit clarification ("Copy them into a local Python environment; the code blocks do not execute in this page.") that the FR "Micro-code exécutable" badge lacks; the FR label alone could suggest the code runs on the page. Candidate alignment for a future editorial pass.
2. FR frontmatter declares `sidebar: fr` while the EN page has no `sidebar` key. `site/_quarto.yml` defines two sidebars (`id: fr`, `id: en`); the EN page resolves its sidebar by content matching (`en/index.qmd` is listed in the `en` sidebar), so the FR key is defensive rather than load-bearing. Justified asymmetry, not a defect.
3. Both pages link their bibliography label to the same shared page `references.qmd` (declared `language:shared`, French title "Références et provenance des illustrations"). EN readers therefore land on a French-titled page; keeping a single shared page versus adding an EN-facing label or redirect is an owner decision.
4. Neither page-map has a `summary:` field, so no `description-meta:` was inserted; per the merged T1 rule (#961) both keep the subtitle fallback for the meta description. Consistent, not a defect.

**Validation status:** source-level review only. No Quarto render, browser inspection, or assistive-technology testing was run for this entry.

## Exercise-hub source audit — FR/EN exercise catalogue (2026-11-12)

**Scope:** FR/EN source-level review of the practice hub recorded as "Not reviewed" in the coverage reconciliation table: `site/fr/exercises.qmd` and `site/en/exercises.qmd`. This pass inspected frontmatter, page-map blocks, the per-lesson exercise list, the collection and planned-collection status tables, references, and FR/EN parity. It did not render pages in a browser, execute any exercise, or review the linked collection pages themselves (each has, or will get, its own row).

| Page pair | Review result | Evidence boundary / remaining action |
|---|---|---|
| `site/fr/exercises.qmd` / `site/en/exercises.qmd` | Both pages are honest catalogues with exact FR/EN parity. The collapsed per-lesson list has 33 entries in both languages (19 Understand, 7 Build, 7 Deepen), matching the claimed count. The five published collections state their exercise counts and explicitly list what remains to be developed (finite-difference gradient checking, advanced attention variants, architecture variants, temperature/top-k/top-p), identically in FR and EN. Planned collections (pretraining, fine-tuning, evaluation, efficiency, advanced topics) are explicitly not presented as published. The Raschka reference carries the no-copy contract ("use as a topic index; do not copy exercise statements or solutions") in both languages. Page-map parity is exact: the same five children and a `suggested_route.next` to the evaluation page in each language. The hub itself claims no interactivity, so the "claimed interactivity" check reduces to the linked collection pages, outside this pass. | Rendered/browser review, link checks, and per-collection content audits remain open. |

**Minor source observations (cosmetic, not blocking):**

1. FR typo in the Génération collection row: "boucle autoregressive" is missing its accent (cf. "Génération autorégressive" correctly written earlier on the same page); candidate one-word fix for a future editorial pass.
2. The EN section headings inside the collapsed callout carry bilingual labels ("Understand / Comprendre", "Build / Construire", "Deepen / Approfondir") while the FR page uses French-only labels. Documented asymmetry, consistent with giving EN readers a bridge to the French sidebar naming; the direction choice belongs to the owner.
3. Both pages keep five bare HTML anchors (`<a id="...">`) named after the five collections, mirroring an earlier in-page layout; collections now live on separate pages, so these anchors look vestigial. Symmetric FR/EN and harmless, but they could be removed in a future cleanup if nothing targets them.
4. The page links to exercise pages with `.qmd` source hrefs; the incremental-render rewrite (#993) and the CI link check cover this pattern, so it is a dependency, not a defect.
5. Neither page-map has a `summary:` field, so no `description-meta:` was inserted; per the merged T1 rule (#961) the subtitle fallback applies. The `language-switch` block is present on both pages. Consistent, not a defect.

**Validation status:** source-level review only. No Quarto render, browser inspection, or execution of any exercise was run for this entry.


## Experimental-evaluation page audit — 2026-11-12

**Scope:** source-level review of `site/fr/evaluation-experimentale.qmd` and `site/en/experimental-evaluation.qmd`, including FR/EN parity, the stated retrieval estimand, AP interpretation, leakage-safe model selection, and uncertainty. No ranking system or evaluation pipeline was executed.

**What is sound:** the exercise gives a concrete deployment target (unseen papers), distinguishes passage-level leakage from paper-level grouping, identifies selection optimism from choosing among 40 configurations, separates AP from calibration, and warns that few independent clusters make uncertainty estimates unstable. Its scope is appropriately a protocol-design exercise rather than a benchmark claim.

**Material gap and targeted correction:** the page did not define how AP is aggregated across research questions. For per-query rankings, macro-AP (compute AP per query, then average under a stated query weighting) and micro-AP (pool query–passage pairs before computing AP) are different estimands. The 5% prevalence example is not enough to define a macro-AP random baseline: per-query prevalence and query weighting matter. The text now asks learners to state the aggregation, scopes the approximate 0.05 baseline to the prevalence of the evaluation unit, and explains why global passage prevalence does not determine the macro baseline.

The uncertainty guidance now makes the crossed-dependence consequence explicit: when the same queries recur across papers, a paper-only bootstrap is conditional on the observed queries. Generalization over both papers and queries requires a sampling design and uncertainty method that reflect both dimensions (for example, multiway or hierarchical resampling). FR and EN changes are semantically aligned.

**Validation boundary:** source review only. Quarto rendering, local-link checks, and a rendered bilingual review remain pending; no empirical protocol or bootstrap implementation was run.

## Reference-pages source audit — FR/EN glossary and Transformer history (2026-11-12)

**Scope:** FR/EN source-level review of the last two rows recorded as "Not reviewed" in the coverage reconciliation table: the reference glossary (`site/fr/glossary.qmd` / `site/en/glossary.qmd`) and the optional-history reference (`site/fr/transformer-history.qmd` / `site/en/transformer-history.qmd`). For the history page, the chronology lives in a data-driven timeline, so the audit covered the page sources plus the canonical dataset `data/history-pilot.yml` and its CI checkers (`check_history_pilot.py`, `check_history_rendered.py`). This pass did not render pages in a browser, and event dates were checked against general knowledge of the cited primary sources, not by re-fetching each source.

| Page pair | Review result | Evidence boundary / remaining action |
|---|---|---|
| `site/fr/glossary.qmd` / `site/en/glossary.qmd` | Exact FR/EN parity: 61 entries in both languages, distributed identically across the five thematic groups (language models 4, text and data 11, representations and geometry 9, probability and learning 10, Transformer architecture 27), with entry-for-entry correspondence. Definitions are short, operational, and correctly scoped: the decoding/decoder/incremental-decode triad is explicitly disambiguated; the embedding family (initial token, contextualized, sentence/document, space) is separated; width is warned against conflation with `d_ff`/`d_head`; GRPO's reward source is explicitly left unspecified; the reward model is called a learned proxy, not an objective measure. Duplicate definitions were not found. Substantive entries link to their canonical pages; unlinked entries (anisotropy, hubness, calibration, multi-head attention, parameter, fine-tuning, SFT, and a few others) are consistent with the page's stated first-pass-definition contract. | Rendered/browser review and link checks remain open. Definitions were checked for internal consistency and scope, not re-derived from the primary literature; the canonical pages remain the authority. |
| `site/fr/transformer-history.qmd` / `site/en/transformer-history.qmd` | The page structure is 1:1 across languages (classification section with a mermaid figure, timeline via include, four reading cautions, single primary source). The chronology itself lives in `data/history-pilot.yml`: 16 selected milestones represented by 17 event records (the GPT-2 research announcement and the staged checkpoint releases are distinct), each with `kind` (submission/announcement/release), a bilingual summary and an editorial note. All event dates and attributions checked correct: Bahdanau 2014-09-01, Vaswani 2017-06-12, GPT announcement 2018-06-11, BERT 2018-10-11 (NAACL 2019), GPT-2 announcement 2019-02-14, staged releases 2019-02 to 2019-11 with the documented month-attribution conflict kept at `confidence: medium`, T5 2019-10-23, Kaplan 2020-01-23, RAG 2020-05-22, GPT-3 2020-05-28, LoRA 2021-06-17, InstructGPT 2022-03-04, Chinchilla 2022-03-29, FlashAttention 2022-05-27, ChatGPT 2022-11-30, DPO 2023-05-29, Mamba 2023-12-01. Historical nuance is strong throughout (attention predates the Transformer; Transformer is not an autoregressive LLM; scale does not explain everything; a publication date is not absolute priority), and the page is not presented as a prerequisite learning path. | Rendered/browser review of the generated timeline remains open (covered by `check_history_rendered.py` in CI at the structural level). Dates were verified against general knowledge, not by fetching each cited URL; the dataset's own source records remain the attribution authority. |

**Minor source observations (cosmetic, not blocking):**

1. Glossary: "Voir aussi" / "Related pages" contains two adjacent unlabeled lists (3 links, then 4 links) with no subheadings; renders as two consecutive bullet lists. Symmetric FR/EN; a labeled split would be a cosmetic improvement.
2. Glossary: the sentence pointing to the "parcours Géométrie et interprétabilité des représentations" (EN: representation geometry and interpretability path) links to `embedding-space.qmd`, a lesson page hosting that path; the wording could suggest a dedicated page. Symmetric FR/EN, harmless.
3. Glossary: neither page-map has a `summary:` field, so no `description-meta:`; per the merged T1 rule (#961) the subtitle fallback applies (the glossary was in the documented T1 no-summary skips). Consistent, not a defect. EN spelling is consistently British ("favours", "neighbours").
4. History: the FR page closes its `language-switch` block with a 3-colon fence while the EN page uses 4 colons; both are valid Quarto fences, cosmetic inconsistency only.
5. History: the includes `_history-timeline-{fr,en}.qmd` are absent from the repository. They are build-time generated artifacts, inferred from the data-driven pipeline (`data/history-pilot.yml` + the two history checkers) and from CI passing on main; the generator script itself was not located in this session. Recorded here so future auditors do not flag the include as broken.

**Validation status:** source-level review only. No Quarto render, browser inspection, or fetch of the cited URLs was run for this entry.


## Visual pedagogy audit: canonical Understand route (2026-11-16)

**Scope and evidence.** Source-level inspection of the 9 stages in `data/guided-route.yml`, covering 20 bilingual core page pairs (40 Quarto sources): orientation/generation, text-data, embedding-space, positional-encoding, contextualized-representations, transformer, Q/K/V, scaled attention, causal masking, logits, probabilities, entropy, in-context learning, context engineering, likelihood, cross-entropy, loss, gradients and training-loop. This records source-declared figures, stepper/Mermaid/interactive elements and their pedagogical role. It is **not** a browser screenshot audit, SVG visual inspection, assistive-technology test, or learner study. “No dedicated figure found” means none was declared in the inspected page source; it does not mean the page is visually empty.

### Page-level inventory

| Route stage / page pair | Visual elements found in source | Pedagogical value already present | Gap / next decision |
|---|---|---|---|
| 1 — `llm-overview` (FR/EN) | Full autoregressive generation SVG; three-use predictive-distribution SVG with dedicated mobile variant. | Strong system map; distinguishes generation, observed-target scoring and training. | **Keep.** Check that the same running example and terminology persist into the later pages; verify desktop/mobile visual hierarchy in browser. |
| 1 & 6 — `generation` (FR/EN) | Accessible generation-loop stepper; a three-turn worked table with contexts, probability excerpts and selected tokens; explicit prefill, incremental decode and KV-cache prose. No dedicated image/SVG or Mermaid diagram found in source. | The page already provides a strong numerical/narrative trace and correctly distinguishes decode (execution phase) from decoding (selection rule). | **Improve by visualizing existing content, not adding a second explanation.** Convert the three-turn table into a compact time-sequence figure showing prefill, distribution, selection, append, incremental decode and stop. Keep KV-cache as an optional efficiency overlay; parameters remain fixed. |
| 2 — `text-data` (FR/EN) | Pipeline stepper and Mermaid flow diagram. | Good conceptual path from text to discrete model input; distinguishes prompt encoding from corpus preparation. | **Improve selectively.** Add a small worked tokenizer trace with actual output, named tokenizer/version and visible token strings/IDs. Keep corpus construction out of this page. Avoid a second generic pipeline figure. |
| 3 — `embedding-space` (FR/EN) | Dedicated embedding-lookup SVG and explanatory caption. | Explicitly separates token ID/address from the vector stored in the selected row. | **Keep.** Connect the same token/ID to the contextualization example; ensure the geometric view is not mistaken for a literal 2D representation of the full embedding space. |
| 3 — `positional-encoding` (FR/EN) | Stepper branches between common approaches; SVG shows absolute input addition versus RoPE rotation of Q/K after projection and before QK. | Strong comparison of insertion points; makes an architecture-specific distinction visible. | **Keep and verify.** Test that the branch does not imply these are the only positional methods or that all models use RoPE. |
| 3 — `contextualized-representations` (FR/EN) | Pipeline SVG plus same-token/different-context SVG. | Excellent continuity: same lookup, different accessible context, potentially different hidden states. | **Keep.** Consider one synchronized small numerical/trace example only if authentic intermediate states can be sourced; do not add decorative vectors. |
| 4 — `transformer` (FR/EN) | Whole GPT + expanded pre-LN block SVG; end-to-end data-flow SVG; Mermaid residual/block flow; attention-versus-MLP comparison SVG. | Strong macro-to-micro progression, distinguishes attention mixing across positions from position-wise MLP processing, and locates logits. | **Keep.** Avoid another architecture infographic. A tensor-shape overlay or trace is a better candidate than a fifth static architecture picture, provided it stays readable and links to Build. |
| 4 — `queries-keys-values` (FR/EN) | Main Q/K/V flow SVG with responsive mobile source; separate score, attention-weight and output matrix SVG, also responsive. | Very good separation of routing projections, content values, raw scores, normalized weights and output shapes. | **Keep; extend as a guided worked trace.** Reuse one tiny input sequence through Q/K/V and the attention page; prediction-before-reveal is more valuable than another static figure. |
| 4 — `scaled-dot-product-attention` (FR/EN) | Calculation-flow SVG; three optional FlashAttention figures (tiling, online softmax, dense versus sparse); accessible stepper. | Core figure correctly distinguishes Q/K score production, pre-softmax mask, row-wise normalization and V aggregation. Advanced figures explain IO-aware tiling and distinguish dense exact attention from sparse connectivity. | **Keep.** Make the core worked example traceable across the Q/K/V page and causal-mask page. Preserve FlashAttention as optional deepening, not a prerequisite. |
| 4 — `causal-masking` (FR/EN) | Lower-triangular four-position mask SVG; stepper. | A compact, correct visual for the allowed-prefix invariant; the text separately distinguishes causal, padding, document and loss masks. | **Improve.** Add a tiny before/after score matrix showing a future score blocked before softmax, then a prefix-invariance test result. Avoid a larger generic Transformer diagram. |
| 5 — `logits` (FR/EN) | SVG counterexample: common shift of logits leaves softmax distribution unchanged; stepper. | Strong counterexample rather than a decorative definition. | **Keep.** Link the same numerical logits directly to the probability and entropy examples so the three pages share one trace. |
| 5 — `probabilities` / `probabilites` (EN/FR) | Logits → temperature → softmax → optional filters → selection SVG; actual temperature slider and bars in both languages. | The route distinguishes score transform, distribution, filtering and selection; the interactive control supports causal exploration. | **Keep and improve the experiment.** Add a learner prediction prompt, expose exact numeric values, and make reset/keyboard/screen-reader behavior explicit. Verify that the same example is used on the logits page. |
| 5 — `entropy` (FR/EN) | SVG comparing concentrated, example and uniform distributions, with entropy values. | Good visual distinction between token probabilities and a whole-distribution summary. | **Keep.** Connect the plotted distributions to the probability page's numerical example; ensure units (nats/bits) remain explicit. |
| 7 — `in-context-learning` (FR/EN) | Mermaid diagram found in both sources. | A diagrammatic explanation exists; source does not establish that it is interactive. | **Review/possibly improve.** Ensure it contrasts zero-/few-shot context examples with parameter updates and does not imply ICL always means a particular internal learning mechanism. |
| 7 — `context-engineering` (FR/EN) | No dedicated image, SVG, Mermaid or interactive visualization found in inspected source; however, the page already has a three-level context comparison table, neighboring-concept comparison table, an eight-operation list and a design example. | The conceptual distinctions are already unusually explicit; the gap is a spatial/system-level representation, not missing definitions. | **Candidate for one original system-boundary diagram only if useful in browser/learner review.** Show application-stored information versus the subset selected/retrieved/structured for a particular model call, then the supplied context and model parameters as separate things. Include trust boundaries. Do not duplicate the two existing comparison tables. |
| 8 — `likelihood` / `vraisemblance` (EN/FR) | Accessible scoring stepper; no dedicated diagram found. | The mathematical chain and target-scoring objective are explicit in prose/equations. | **Candidate for a compact sequence-scoring figure.** Show a known sequence, shifted conditional probabilities and multiplication/sum of log probabilities. Do not depict token selection or parameter updates here. |
| 8 — `cross-entropy` (FR/EN) | Figure comparing target probability 0.9 versus 0.1 and resulting −ln p(y) loss. | Strong intuitive link between probability assigned to the observed target and penalty. | **Keep.** Reuse the target token and probability from the likelihood example; distinguish single-token NLL from batch/sequence reduction. |
| 9 — `loss` (FR/EN) | Training-loss stepper; no dedicated diagram found. | Describes aggregation, target alignment and masking in text. | **High-priority candidate.** Show token-level losses → target/loss mask → reduction (sum/mean with denominator stated) → scalar objective. Keep attention mask and loss mask visually distinct. |
| 9 — `gradients` (FR/EN) | Parameter-update stepper; no dedicated diagram found. | The chain-rule/update explanation exists in text and equations. | **High-priority candidate.** Use a tiny scalar or two-parameter example: loss surface, gradient direction, learning-rate-scaled update, before/after parameter. Do not use an ungrounded neural-network stock diagram. |
| 9 — `training-loop` (FR/EN) | One-training-step stepper; no dedicated diagram found. The page already contains a concrete running numerical example (target probability 0.6, local loss about 0.511 nats, logit gradient and parameter-update explanation). | The numerical trace is strong source material for a figure; the conceptual separation between steps 1–3 and the parameter update is explicit. | **High-priority candidate.** Visualize the existing numerical example and the loop, rather than inventing new values: forward pass → target loss → gradient → optimizer update → recomputation. Add a separate validation branch that measures but never updates parameters. |

### Cross-page findings

1. **Strongest existing visual sequence:** Transformer → Q/K/V → scaled attention → causal mask. It already contains architecture, projections, matrices, operation order and causal constraint. Improve continuity with a single small worked example; do not add more independent overviews.
2. **Strongest counterexample/interactive teaching:** logits common-shift invariance and the probability temperature explorer. Reuse one consistent numerical example across logits → probabilities → entropy → scoring.
3. **Weakest visual coverage in the core route:** context engineering, sequence likelihood, loss aggregation, gradient update and the repeated training loop. Their current prose/stepper can orient the learner but does not yet visually expose the transformation being taught.
4. **Responsive treatment is uneven by design:** some complex figures have explicit mobile variants (predictive-distribution and Q/K/V); other pages rely on width scaling. Browser review must check legibility, not just that an SVG loads.
5. **Bilingual source parity is visible for the inspected examples:** corresponding FR/EN figures and alt text exist for the main route. This source check does not prove semantic equivalence of every caption, rendered layout or keyboard interaction.

### Priority decisions (avoid a figure-per-page rule)

- **P0 — cross-page numerical continuity:** choose one small, explicitly synthetic worked sequence and carry it through token IDs → embeddings → Q/K/V → scores/mask/softmax/output → logits/probabilities/entropy. Label synthetic values clearly; never present them as a real model trace.
- **P1 — training mechanism:** add only three complementary visuals: (a) token loss and reduction/mask, (b) gradient/update on a tiny parameter example, (c) repeated training/validation loop. Reuse the same target/loss convention across FR and EN.
- **P1 — generation:** add a time-sequence for prefill/decode/append/stop; show KV-cache only as a clearly labelled optional efficiency overlay.
- **P1 — context engineering:** one boundary/system diagram if user testing confirms that retrieval, prompt assembly, parameters and external memory are currently conflated.
- **P2 — causal mask:** add a score-before/after-softmax micro-example tied to the existing triangular matrix.
- **P2 — likelihood:** only add a sequence probability diagram if it can reuse the same target probabilities as cross-entropy; otherwise keep the equation and stepper.

### Acceptance checklist for any visual change

- [ ] State the learner question the visual answers and the intended learner action (locate, trace, predict, compare, calculate, manipulate or reconstruct).
- [ ] Check scientific conventions, shapes, axes, mask polarity, units, and all displayed numbers independently.
- [ ] Label illustrative/synthetic data and distinguish them from authentic model traces.
- [ ] Reuse the same notation, token identity, example and semantic colour roles across connected pages.
- [ ] Provide FR/EN equivalent content, informative alt text/caption and a textual/no-JavaScript path.
- [ ] Check keyboard, focus, touch target, reduced-motion, responsive and screen-reader behavior for interactive figures.
- [ ] Link to the matching exercise and, where available, implementation/test; do not claim evidence that does not exist.
- [ ] Record provenance and asset-level rights for every external visual; do not copy reference-project figures.
- [ ] Evaluate rendering/accessibility separately from learner comprehension. Use a small prediction/transfer task before claiming a learning benefit.

**Next bounded work:** browser-review the P0/P1 pages at desktop and mobile; then prototype one end-to-end shared numerical trace and one training-loop figure in FR/EN. Do not launch a site-wide illustration campaign or introduce a new visualization framework before those pilots are evaluated.


## 2026-11-16: 3Blue1Brown — cross-entropy, Part 2

**Scope.** Source-level pedagogical and mathematical audit of *But what is cross-entropy? | Compression is Intelligence Part 2* (16 July 2026), compared with the existing bilingual cross-entropy, language-modeling-math, loss and LLM-evolution lessons, the predictive-compression material, and the concept graph.

| Part 2 idea | Existing coverage | Decision |
|---|---|---|
| Cross-entropy as the average cost of using a code optimized for another distribution | The general formula and KL decomposition existed, but the operational codebook interpretation and a numerical distribution-shift example were not prominent in the learner path. | Add the code-mismatch interpretation and the 2.625-bit example to the advanced bilingual math page. |
| Direction and notation of target/model distributions | The project consistently uses target (q), prediction (p); the video uses (P) for observed data and (Q) for the code/model. | Add an explicit notation map to prevent a silent argument swap. |
| Language-tree / gzip application | No dedicated case study in the core path. | Record as an optional application; explicitly state that gzip co-compression is only an empirical analogy/estimate, not exact cross-entropy or ideal Shannon coding. |
| Why negative logarithm? | The pages derived NLL and the cross-entropy/KL identity, but did not show the optional constrained-optimization argument for the logarithmic form. | Add a bounded Lagrange-multiplier derivation with assumptions and a warning against universalizing the result. |
| Pretraining as average information per observed token | Already covered by token-level NLL, likelihood, cross-entropy, loss reduction and perplexity. | Keep canonical pages; no duplicate derivation. |
| Distillation with a teacher's full output distribution | Soft targets and the teacher-model example were mentioned, but not explained as a contrast with one-hot next-token supervision. | Add the teacher/student distribution interpretation and its limits; connect the existing knowledge-distillation concept to the advanced page and graph. |
| KL as excess coding cost | The identity and directionality were already covered. | Retain the canonical derivation; add the concrete excess-bits example and coding interpretation. |

### Scientific and pedagogical qualifications

- The video's notation differs from the project's notation. Project (q) is the data/target distribution and (p) is the model distribution; the video labels those roles (P) and (Q), respectively.
- In the four-symbol example, the old code lengths are ((1,2,3,3)) bits. Under the shifted data distribution ((1/8,1/8,1/4,1/2)), the average is (2.625) bits; source entropy is (1.75) bits and excess cost is (0.875) bit/symbol.
- The gzip language-tree example is not exactly cross-entropy: gzip is a practical dictionary/repetition compressor, and the cited cross-compression distance has additional details. It is an instructive analogy, not a calibrated probability model or ideal entropy coder.
- The log-loss derivation is conditional on an additive separable event loss, normalized predictions, differentiability, and requiring the data distribution to minimize expected loss for every interior data distribution. Other tasks can justify other objectives.
- Teacher distributions are soft supervision, not ground truth. Distillation can transmit the teacher's errors and biases; it is model compression, not predictive data compression.
- Lower held-out cross-entropy measures better probabilistic prediction under the chosen data/tokenizer/evaluation protocol; it does not alone establish truth, intelligence, or broad task quality.

### Changes

- Added bilingual advanced derivations and a worked mismatched-code example to `site/fr/language-modeling-math.qmd` and `site/en/language-modeling-math.qmd`.
- Registered Part 2 and its provenance/scan limitations in `data/sources.yml` and a structured extraction.
- Added a cross-source synthesis and updated the source index/references.
- Connected the existing knowledge-distillation concept to the advanced math pages and added a prerequisite edge from cross-entropy to knowledge distillation.

### Validation still required

Quarto rendering, bilingual link checks, YAML/schema and graph validation, Python/domain checks, and CI must pass on the final PR head. No rendered visual audit or learner study is claimed.

## Probability and decoding ownership update — 2026-11-24

A bilingual refactor now separates the core predictive-distribution lesson from optional decoding policy details. The earlier visual-pedagogy inventory above is retained as a dated snapshot; its ownership notes for the probability page are superseded as follows:

- `probabilities` / `probabilites` remains the core lesson for logits, softmax, the conditional next-token distribution, normalization, calibration, and the distinction between model probability and factual truth. It keeps a short conceptual bridge to generation, observed-target scoring, and training.
- The detailed temperature treatment and interactive explorer, its worked numerical comparison, the decoding-flow visual, NumPy workbench, and comparison table now belong to the existing optional `decoding-strategies` Deepen page. The page owns the `#temperature` anchor; generation and other cross-links point there.
- Questions and worked answers for the probability lesson now live in a dedicated bilingual Practice companion. The main lesson links to it rather than embedding a growing question bank. Existing shared Foundations exercises remain the canonical location for softmax/NLL calculations; temperature and top-k/top-p practice remains in the Generation exercise collection.
- The bilingual revision pages now describe temperature and top-k/top-p as optional decoding transformations, not as part of the base predictive distribution. Entropy, Generation, and the Transformer Explainer link to the canonical decoding owner where relevant.
- The Deepen page links to its existing dedicated decoding-strategies comprehension page; the more computational temperature and top-k/top-p calculations remain in the Generation exercise collection. This preserves a per-page question destination without duplicating calculation exercises.

The transfer was checked against the prior bilingual probability and decoding pages: the core page is shorter, while the decoding page gains the moved explanations and interactive material; the moved numerical examples, filters, comparison and implementation details remain represented. This is an ownership/sequence correction, not a deletion of those concepts.

**Validation boundary:** source-level ownership, bilingual links, page metadata and generated map projections have been reconciled. Final-head Quarto/Chromium and Python CI results are tracked by PR #1584; no learner-outcome or manual screen-reader claim is made here.


## 2026-11-24: route and Practice audit — predictive distribution → scoring → loss

**Scope.** Bounded reader-continuity and exercise-ownership audit of the FR/EN path from the predictive distribution through observed-target scoring, cross-entropy and batch loss. This pass reuses the prior source-level mathematical audits recorded above; it does not re-derive or re-certify their equations. It checks page roles, transitions, bilingual destinations and the separation between Understand and Practice.

| Page pair | Existing reader contract and Practice destination | Audit finding |
|---|---|---|
| `probabilities.qmd` / `probabilites.qmd` | Core Understand page for logits → softmax → conditional distribution; dedicated FR/EN Practice companions. Temperature and filtering are delegated to the existing Deepen/Generation owners. | **Keep.** The page owns the predictive distribution and does not absorb scoring or decoding policy. Its companion checks prefix dependence, normalization, calibration and truth, and links temperature work to the canonical decoding destination. |
| `likelihood.qmd` / `vraisemblance.qmd` | Core scoring page; dedicated FR/EN Practice companions. The page states that the prefix and target are observed, parameters are fixed, and no generated token is fed back. | **Keep.** This is the correct reader-facing destination for the prediction → scoring transition. The exercise “Generate or score from the same prefix” makes the distinction operational: generation follows its own greedy prefix, while scoring follows the observed continuation. In the worked example, the observed continuation has likelihood 0.27 versus 0.24 for the greedy continuation; greedy selection is not sequence-level likelihood maximization. |
| `cross-entropy.qmd` (FR/EN) | Core page for the local penalty; dedicated FR/EN Practice companions. It connects one-hot targets to token NLL and delegates soft-target/KL derivation to Deepen. | **Keep the ownership boundary.** The Practice companion contains concise checks on zero loss, masked-token denominators and the limits of perplexity. The actual soft-target/KL calculation already exists in the shared Foundations exercise (`ex-foundations-soft-targets-kl`); do not duplicate it here. |
| `loss.qmd` (FR/EN) | Core page for aggregation, target masking and reduction; dedicated FR/EN Practice companions. | **Keep.** The page follows naturally after cross-entropy and leads to gradients. Its exercises cover visible inputs versus ignored targets and validation-loss comparison. |

### Cross-page findings and decisions

1. The conceptual path is coherent: predictive distribution → observed-target likelihood → local cross-entropy penalty → masked/reduced batch loss → gradients. The new prediction → scoring edge is explanatory and cross-cutting; it does not insert scoring into the linear inference sequence or make scoring a prerequisite for generation.
2. The likelihood Practice exercise is a strong transfer task because it contrasts two prefixes and exposes why greedy decoding does not maximize sequence likelihood. Retain it as the principal exercise supporting the new transition.
3. All four core lessons have dedicated bilingual Practice destinations. Their links return to the corresponding lesson, and their question banks remain outside the Understand pages.
4. One bilingual link-parity gap was found: the French likelihood Practice page linked to both cross-entropy and loss, while the English page linked only to loss. **Corrected in the accompanying audit PR** by adding the cross-entropy link to the English page.
5. The cross-entropy Practice page is intentionally concise. Do not add a second soft-target/KL calculation: the shared Foundations collection already owns that exercise and the cross-entropy lesson links to the relevant deeper treatment.
6. The probability Practice page correctly delegates temperature and top-k/top-p exercises to the Generation collection rather than duplicating decoding-policy work.

### Evidence boundary

This is a source/metadata/link and exercise-ownership audit. It is not a new mathematical derivation review, a final rendered visual audit, a manual screen-reader test, or an independent learner study. The existing inventory entries for logits/probabilities/likelihood/cross-entropy/loss remain the source of prior mathematical-review evidence. Final-head CI, rendered-link/browser review for the small bilingual link correction, manual accessibility and learner validation remain separate checks.


## 2026-11-24: gradient and training-loop audit — source, numerical trace and Practice boundary

**Scope.** Bounded FR/EN source and executable-example audit of the final core training path: loss gradient → parameter gradient → optimizer update → repeated training and held-out validation. This completes the specific open example checks noted in the earlier mathematical-chain inventory. It does not certify a full Transformer backward pass, checkpointing, distributed training or the unfinished end-to-end Build milestone.

| Page pair | Source and numerical evidence | Decision |
|---|---|---|
| \`gradients.qmd\` (FR/EN) | The one-hot cross-entropy derivative is consistently stated as \(p_i-\mathbb{1}[i=y]\); its components sum to zero. The batch-mean form correctly adds \(1/|\mathcal{M}|\) over valid target positions and zero derivative for ignored logits. The text distinguishes this local logit derivative from parameter gradients and explains the flattened-logit/Jacobian view used by backpropagation. | **Keep.** The conceptual progression from local logit gradient to parameter gradient and optimizer update is explicit. The caveat that an ignored logit's zero derivative does not necessarily cut every gradient path through a hidden representation is important and correctly scoped. |
| Gradient worked example | For \(p=(0.6,0.2,0.1,0.1)\) and target class 0, \(g_z=(-0.4,0.2,0.1,0.1)\), whose sum is zero. With \(h=(1,-1)\) and \(\eta=0.1\), the updated logits are \(z-0.2g_z\), giving changes \((+0.08,-0.04,-0.02,-0.02)\). A fresh softmax gives target probability \(0.626075\), consistent with the page's \(0.626\). | **Numerically verified.** The FR example uses the localized target token “Vous”; the EN example uses “They”. The same probabilities and gradient are preserved. |
| Finite-difference check | A central difference with \(\epsilon=10^{-6}\) on the four-logit cross-entropy example was compared with the analytical gradient using the repository's documented loss convention. Maximum absolute discrepancy: approximately \(2.34\times10^{-10}\). | **Targeted check passed.** This validates this deterministic example only; it is not a general \`gradcheck\` of the full GPT backward pass. |
| Gradient Practice companion | FR/EN companions ask about the \(p-y\) derivative, interpretation of finite-difference disagreement and step-size choice. The applied exercise compares two distributions with equal target loss but different non-target probabilities, then computes distinct parameter updates and next-token probabilities. The worked values \(0.537\) and \(0.540\) were independently recomputed. | **Keep.** It tests transfer from equal scalar loss to different gradient vectors and updates, rather than repeating the lesson's derivation. |
| \`training-loop.qmd\` (FR/EN) | The runnable example uses the maintained \`cross_entropy_from_logits\` and \`cross_entropy_gradient\` functions in \`src/llm_lab/foundations/losses.py\`. It trains a 12-state lookup table with full-batch SGD on 60 sampled transitions and measures 400 held-out transitions. | **Numerically verified.** The same code and seed reproduce the bilingual narrative. |
| Training-loop numerical output | Under NumPy 2.3.5 and seed 0, training loss is 2.485 at step 0 and 1.147 at step 300. Validation loss is minimized at step 100 (2.006), then reaches 2.162 at step 300. This matches the rounded FR/EN claims (2.485 → 1.15; 2.01 minimum; 2.16 final). | **Keep with current qualification.** The code asserts the qualitative pattern, not exact values; the prose correctly says exact values depend on seed/library version. |
| Training-loop Practice companion | FR/EN pages cover optimizer versus gradient, overfitting, validation versus test, one SGD step, and an end-to-end transfer through representations, generation, observed-target scoring, loss, gradients and validation. | **Keep.** The transfer task explicitly uses the generated prefix for generation and the observed prefix for scoring, preserving the distinction established in the earlier route audit. |

### Pedagogical boundary and remaining checks

- The training-loop code is inside a collapsed **Further exploration → Implementation** section. It is a deliberately small Markov lookup-table experiment, not a Transformer implementation; the page explicitly states that limitation and keeps the full from-scratch training milestone in Build. Retain this as an optional experiment for now rather than moving it and losing its explanatory role.
- The optimizer section correctly distinguishes the gradient, optimizer and learning rate. Adam/AdamW are described as adaptive first-order methods; the second moment is not confused with a Hessian or Newton update.
- The code measures validation with fixed parameters; it does not update on validation data. The page distinguishes validation-based selection from final test-set assessment.
- The earlier visual inventory still identifies the training loop as a candidate for one compact visual using this same numerical example. That is a separate rendered-pedagogy decision; do not add a generic training diagram or duplicate the code trace.
- Rendered desktop/mobile inspection, manual screen-reader review and independent learner comprehension remain separate evidence. This source/code pass does not claim any of them.


## 2026-11-24: inference → context-use boundary audit

**Scope.** Reader-facing route, page ownership and Practice-link audit for the transition from free-running inference to application-level context use. This pass reuses the existing generation, prefill/decode and context-engineering source/visual inventory entries; it does not repeat their mathematical or source reviews.

| Page / stage | Existing contract | Audit finding |
|---|---|---|
| Generation — inference stage | One canonical FR/EN page owns the autoregressive loop, prompt prefill, iterative decode, token-selection decoding, feedback and stopping. Its Practice companion has self-check questions and links to the extended Generation collection. | **Keep.** The page explicitly separates prefill/decode from teacher forcing, and its Practice page asks learners to distinguish the two. No separate prefill lesson is needed. |
| In-context learning — first page in context-use | Explains zero-shot/one-shot/few-shot adaptation from prompt examples while parameters remain fixed. It follows generation and leads to context engineering in both languages. | **Keep.** The route transition is pedagogically sound: the learner moves from how a continuation is generated to how demonstrations in the supplied prompt can affect that continuation without changing parameters. |
| Context engineering — second page in context-use | Explains application-side selection, organization, updating and security of the context; distinguishes ICL, RAG, memory and model parameters. It follows ICL and closes the context-use stage. | **Keep.** The page's three-level comparison, neighboring-concept table, design example and eight operations already provide the needed distinctions. A system-boundary diagram remains a conditional visual candidate from the earlier visual inventory, not a missing definition or a reason to add another page. |
| Generation Practice companion | Four self-check questions include prefill versus teacher forcing; extended Generation exercises cover the autoregressive loop, KV cache and selection. | **Keep.** This is the correct owner for inference mechanics and selection exercises. |
| In-context-learning Practice companion | Dedicated FR/EN page with answered transfer questions and an experiment on few-shot generalization, irrelevant/reordered/contradictory examples and held-out cases. It links to the shared exercise space rather than a separate one-to-one collection page. | **Keep.** The companion is self-contained enough; do not create a redundant topic-specific exercise collection merely to satisfy a filename convention. |
| Context-engineering Practice companion | Dedicated FR/EN applied page with design, evaluation, neighboring-concept and two-call context-tracing exercises. The final exercise explicitly separates information retained by the application, information sent on each call, and tokens fed back within a single generation. | **Keep.** The two-call exercise is a strong transfer task for distinguishing application context from model parameters and within-call autoregressive feedback. It does not need a second extended collection. |

### Cross-boundary decisions

1. The route order is coherent: generation → in-context learning → context engineering. The nine-stage route places generation in inference and the two context-use lessons in the following context-use stage; the pages' suggested-route metadata agrees in FR/EN.
2. No new computational edge or prerequisite is justified. The stage transition is an application-level extension of inference, not a change to the model's forward computation.
3. Keep the ownership distinction: ICL describes how prompt demonstrations affect behavior at fixed parameters; context engineering describes how the application chooses and assembles the context that reaches the model. RAG and external memory remain system-side mechanisms, not hidden model state.
4. No new prefill/decode page is needed. The canonical generation lesson and its Practice companion already own those execution phases and explicitly distinguish them from teacher forcing.
5. The browser-review contract should not require every Practice companion to link to a separate extended collection. Some companions (notably ICL and context engineering) are intentionally self-contained. PR #1604 generalizes the existing check: require the collection link only when a shared collection is explicitly mapped or a matching published collection exists; still require a visible return link, a learner-facing self-check section and native collapsed answer disclosures.

### Evidence boundary

This is a source, metadata, route and exercise-ownership audit. It is not a new review of the ICL mechanism, RAG implementation, generation math, rendered screenshots, screen-reader output or learner performance. The previously recorded visual inventory remains authoritative for the conditional context-engineering diagram and generation timeline.


## 2026-11-24: text-input → representations boundary audit

**Scope.** Reader continuity, page ownership and Practice placement for text/data → token IDs → embedding lookup → positional information → contextualized representations. Existing source and mathematical audits for these pages are reused; this pass does not re-derive tokenizer, embedding, positional-encoding or Transformer equations.

| Page | Existing role and companion | Audit finding |
|---|---|---|
| Text and data | Sole core page in the text-input stage; next page is embedding space. Dedicated FR/EN companion has three self-check questions and two applied tasks; the broad Text data collection owns the longer tokenizer, tensor-shape, training-window and leakage exercises. | **Mostly keep; one migration needed.** The core page already has a link-only Practice section, but its collapsed supplementary panel still contains the distinct “Encode the prefix and continuation” task. That task is absent from the dedicated companion and should move there. The remaining diagram, explanation of the two tokenizer uses and further-reading links are explanatory depth, not exercises; retain them under a separate Further exploration heading. |
| Embedding space | First page in the representations stage; follows text/data and precedes positional encoding. Dedicated FR/EN companion includes ID/row checks, a small lookup table and the Embedding Atlas. | **Keep; normalize navigation.** The main page links to its companion but does not give that link a dedicated Practice heading. Add the standard link-only section; retain the explanatory “where do table values come from?” material in supplementary resources and the cross-link to the text-data lookup exercise. |
| Positional encoding | Follows embedding space and precedes contextualized representations. Dedicated FR/EN companion contains four checks covering order, RoPE, causal masking and extrapolation; it links to the shared Transformer exercise collection. | **Keep; clarify section ownership.** The core page's Practice section is already link-only. Its collapsed panel contains a permutation-equivariance explanation, optional sinusoidal geometry and references—not learner questions. Move that panel under an explicit Further exploration heading and remove wording that describes it as practice. Do not move the mathematical explanation into the exercise bank. |
| Contextualized representations | Final page in the representations stage; next page is the Transformer. Dedicated FR/EN companion includes a causal-boundary question and an SAE investigation. | **Keep; normalize navigation and remove empty UI.** The main page links to the companion inline but has no Practice heading. Move the link into the standard link-only Practice section and remove the empty supplementary-resources disclosure. Keep the existing five-step pipeline and absolute-position/RoPE comparison in Understand. |

### Cross-page decisions

1. The stage order and page metadata are coherent in both languages: text/data → embedding space → positional encoding → contextualized representations → Transformer. The route objective correctly distinguishes the project's learned absolute position vector added before the first block from RoPE rotations applied to Q/K inside attention.
2. No new page, concept, stage or graph edge is needed. The hand-off is already represented in the guided route and the page-level previous/next metadata.
3. Keep the broad Text data collection as the owner of extended tokenizer, tensor-shape, BPE, windowing and leakage exercises. The dedicated Text and data companion owns short checks and the moved prefix/continuation task; do not duplicate the practical tokenizer trace.
4. Keep the positional-equivariance proof and sinusoidal geometry on the core page as optional Further exploration. They are explanatory/deepening material, not questions; the companion already owns the four learner checks.
5. Harmonize Practice as a link-only section on all four core lessons. The companion pages remain the sole location for their questions and exercises. Supplementary explanations and optional mathematical depth stay in clearly labelled Further exploration sections.
6. The existing browser review must accept self-contained companions and companions linked to a shared collection rather than requiring a non-existent topic-specific collection. This is covered by the generalized browser-contract correction in #1604.

### Follow-up

A focused content PR should move the prefix/continuation task to the Text and data companion, add consistent Practice headings to Embedding space and Contextualized representations, move optional panels outside Practice on Text and data and Positional encoding, and remove the empty Contextualized representations panel. Preserve every explanatory paragraph, diagram, citation and existing anchor.



## 2026-11-25: representations → Transformer → Q/K/V → attention boundary audit

**Scope.** Audit the reader hand-off from contextualized representations into the Transformer computation, and normalize the boundary between core Understand lessons and their dedicated Practice companions. Reuse the existing scientific audits for Transformer blocks, Q/K/V, scaled dot-product attention and causal masking; do not repeat derivations or alter validated equations.

| Page | Existing role and companion | Audit finding and action |
|---|---|---|
| Transformer | Synthesis of the decoder-only GPT network and its forward flow; dedicated FR/EN companion at `exercises/transformer.qmd`. | **Normalize Practice ownership.** The lesson had a bare exercise link rather than a dedicated section. Move it into a link-only Practice section. Keep the GPT-2 interactive workshop optional: it is an observation/experiment resource, not a replacement for the growing question bank. Place it under Further exploration and describe its optional scope explicitly. |
| Queries, keys and values | Explains the three learned projections and their complementary roles; dedicated FR/EN companion at `exercises/queries-keys-values.qmd`. | **Clarify section hierarchy.** The Practice link was already correct and link-only. Its mathematical/architectural deep dive was inside the supplementary panel immediately following Practice, but had no explicit parent section. Add Further exploration above that panel; preserve the equations, architecture comparisons and implementation links. |
| Scaled dot-product attention | Owns the scores → scaling → optional mask → softmax → value aggregation calculation; dedicated FR/EN companion at `exercises/scaled-dot-product-attention.qmd`. | **Separate learning modes.** The Practice link was already correct. The optional Transformer-block walkthrough (Build) and FlashAttention material (hardware/algorithmic deepening) were structurally under Practice. Move the supplementary panel under Further exploration; do not move its content into the exercise bank or the main computation sequence. |
| Causal masking | Defines the autoregressive information constraint and its relation to attention; dedicated FR/EN companion at `exercises/causal-masking.qmd`. | **Normalize navigation.** The companion link appeared near the chapter lead rather than in a Practice section. Move it to a link-only Practice section after the conceptual explanation. Keep API-specific boolean-mask conventions and reference implementation/tests under Further exploration. |

### Cross-page decisions

1. The reader hand-off remains: contextualized representations → Transformer block → Q/K/V projections → scaled dot-product attention → causal masking. The Transformer lesson locates the stack and the input to its first block; Q/K/V explains the projections from a common block input; attention and masking explain how the resulting scores are normalized and constrained.
2. Keep the distinction between the representation entering a block and Q/K/V as learned projections internal to each block. Do not imply that Q/K/V are computed once after the final contextualized representation or that they form a separate post-Transformer stage.
3. No new lesson, concept, stage, prerequisite or knowledge-graph edge is justified. Existing Q/K/V, attention and mask source reviews remain authoritative.
4. Each core lesson now has a single link-only Practice section. Its dedicated companion remains the owner of self-check questions, worked answers and applied tasks.
5. Further exploration owns optional architecture/math depth, implementation conventions, Build-path walkthroughs and hardware optimization. These remain accessible without being presented as required stages or as questions in the main lesson.
6. Keep the GPT-2 interactive workshop as an optional exploration resource. It is a controlled-observation lab with its own purpose and should not be duplicated into the companion question bank.
7. Preserve all existing explanatory text, equations, figures, citations, links and stable anchors. FR/EN structure and meaning should match; language-specific prose and anchors remain localized.

### Validation boundary

This is an article-level source and navigation audit. The change is structural and does not re-derive or claim new validation of Transformer, Q/K/V, attention, FlashAttention or causal-mask mathematics. Final Quarto render, local-link checks, browser review at desktop/mobile sizes and native disclosure keyboard checks are required on the final PR head. These do not replace manual screen-reader review or learner validation.

### Follow-up

After this migration is validated, continue the remaining unverified route boundaries from the existing inventory. Do not reopen the already audited scoring/loss, gradient/training-loop, inference/context-use or text-input/representations groups unless a concrete regression is found.


## 2026-11-25: Build tour contract audit — GPT configuration

**Scope.** First bounded source-to-page audit of the five guided Build code tours. This entry covers only the first tour pair (`gpt-config-walkthrough.qmd`), its Practice companions, `gpt_config.py` and `test_gpt_config.py`. The remaining four tours are not yet certified by this pass.

### Contract comparison

| Claim / learning outcome | Page and exercise evidence | Implementation and test evidence | Result |
|---|---|---|---|
| Six architecture dimensions are positive integers; `embedding_dim` is divisible by `num_heads`. | The FR/EN tour explains the six dimensions, divisibility and early failure. The exercise checks an incompatible and a compatible head split. | `GPTConfig.__post_init__` originally checked only `value <= 0` and divisibility. `test_gpt_config.py` covered zero dimensions and divisibility, but not runtime types. | **Gap found:** positive floats such as `embedding_dim=16.0` passed construction because Python type annotations are not runtime checks. The failure could then occur later when NumPy needs integer dimensions. The original “positive integer” promise was stronger than the actual validator. |
| `seed` controls initialization values, not model shapes; default is zero. | Both tours and their exercises describe the seed as an initialization control with a default of zero. | `GPT` passes `config.seed` to `np.random.default_rng`; the configuration originally did not validate seed type or non-negativity. | **Gap found:** a negative or non-integer seed was not rejected by `GPTConfig` itself; it failed later when the RNG was constructed. |
| Configuration is immutable. | Both tours state that the object is frozen. | `@dataclass(frozen=True)` and `test_config_is_immutable` confirm this contract. | **Confirmed.** |
| Field-to-shape mapping. | The interactive dimension map and table connect V, T, d, H, L and MLP width to model arrays and operations. | `GPTConfig`, `TransformerBlock` and `GPT` use the corresponding dimensions; the block slices d into H heads and the model constructs `(V,d)` and `(T,d)` embeddings. | **Confirmed for the inspected contracts.** |

### Correction applied in the focused branch

- `GPTConfig` now validates all six dimensions as positive integral values at construction, explicitly rejecting booleans and floats (including `16.0`). The runtime check uses exact Python `int` values, matching the declared field types; booleans and NumPy scalar types are not silently coerced.
- `seed` is now validated as a non-negative integral value, excluding booleans, before it reaches `default_rng`.
- Unit tests cover positive floats, booleans, negative/non-integer seeds, and accepted NumPy integer scalars.
- FR/EN tour excerpts, explanations, test descriptions and dedicated Practice companions now state and exercise the same runtime contract.

### Evidence boundary and next action

This is a code/page/test contract audit, not a full audit of the remaining Build tours or a rendered browser review. The correction must pass the existing Python quality/test suite and full Quarto/browser workflow on its final PR head. Continue with `gpt_ops.py` and its tests next, then the block, assembled GPT and generation tours; reuse this same claim → page → implementation → test method. Do not treat the remaining tour pages as audited merely because they link to tested modules.


## 2026-11-25: Build tour contract audit — operations, Transformer block and assembled GPT

**Scope.** Second bounded source-to-page pass covering the FR/EN tours and Practice companions for `gpt_ops.py`, `transformer_block.py` and `gpt.py`, their implementation modules and unit tests. It reuses the scientific architecture audits already validated; it checks only that the implementation, tests, worked answers and stated evidence agree.

### Findings and corrections

| Area | Finding | Correction / evidence |
|---|---|---|
| Layer normalization | With epsilon inside the square root, the normalized variance is `variance / (variance + eps)`, slightly below 1. For a constant row, the centered numerator is zero, so the affine output is exactly `beta`, not the input mean. The walkthrough and one Practice answer were imprecise. | FR/EN explanation and worked answer corrected. Existing tests confirm epsilon is added to the variance and constant rows normalize to zero before affine parameters. |
| GELU approximation | The prose described an error of order `1e-4`, while the test only allowed `1e-3` on its grid. | The claim is now scoped to the actual grid `[-3, 3]` with maximum absolute error about `4.73 × 10⁻⁴`; the test asserts `< 5 × 10⁻⁴`. |
| GPT parameter count | The worked solution for `V=50, T=16, d=16, H=2, L=2, hidden=32` double-counted one `4d` normalization term in its intermediate sum. | FR/EN solution corrected: 2,224 parameters per block; 4,448 across two blocks; 6,386 total. The unit test now cross-checks the worked example's fixed total as well as the independently derived formula. |
| Prefix-invariance test | An additional assertion compared logits at two different positions, which is not a causal invariant. The lesson's French wording also overstated a single fixture as a proof. | The irrelevant assertion was removed. The lesson now describes the test as targeted empirical evidence for the tested prefix/configuration, not a universal proof; the Practice answer already stated this limitation. |
| Transformer-block Practice | The second exercise group restarted numbering at 3, duplicating the earlier Q/K/V question. | FR/EN numbering is continuous from 1 to 5. |
| Practice companion contract | The browser review requires an explicit learner-facing self-check heading, not merely a generic “Exercises/Exercices” heading. | Touched FR/EN companions now use “Check your understanding” / “Vérifier sa compréhension”; generated learning-map projections were refreshed to match. |

### Evidence boundary and next action

The source/test checks for the operations, block and assembled-model tours are complete. The fifth tour, `generate.py`, was audited and corrected separately in merged PR #1617. Together with the configuration correction in merged PR #1614, all five guided Build tours have now been compared against their implementation, tests, FR/EN explanations and Practice companions. PR #1618 consolidates the operations/block/model corrections and is awaiting its final Quarto/browser review. After that integration, the source-to-page audit of the five-tour Build route is complete. Manual screen-reader/native-breadcrumb review and the learner pilot remain separate evidence.


## 2026-11-25: Build tour contract audit — generation

**Scope.** Fifth and final guided Build tour: FR/EN generation walkthrough and Practice companion, `generate.py`, `test_generate.py`, and the top-k/top-p filters.

### Findings and corrections

- The `top_k` validation compared the supplied value with 1 before checking its type. A string such as `"3"` therefore raised an incidental `TypeError` instead of the documented `ValueError`.
- Temperature validation passed booleans as numeric values and allowed text values to fail inside `np.isfinite`, rather than returning the named validation error.
- PR #1617 moved both checks before the generation loop, rejects boolean/non-real temperatures and non-boolean/non-integer `top_k`, and preserves Python/NumPy integer support.
- Regression tests cover string/list `top_k`, boolean/text temperatures, zero temperature in greedy mode, and non-finite temperatures in both decoding modes. The FR/EN walkthrough and source docstring now state the same contract.
- PR #1617 merged after Python quality/type checks, the full test suite and the Quarto/browser workflow passed.

### Evidence boundary

This completes the source → claim → implementation → test comparison for all five guided Build tours. It does not close the independent screen-reader/native-breadcrumb review, full accessibility review, or learner pilot under #447.


## 2026-11-25: text-data transfer exercises and training-example Practice gap

**Scope.** Continue the earlier exercise-catalogue recommendation after the causal-mask work. Inspect the current FR/EN text-data extended collection, the training-examples concept bridge and its dedicated Practice companions, plus the narrow NumPy window-construction reference and tests. Do not repeat the already audited TR-A–TR-C representation tasks, the tokenization/BPE scientific review, or the source-level corpus-preparation review.

### Status correction to the earlier catalogue recommendation

The earlier 2026-11-09 recommendation described BPE merge tracing, shifted windows and leakage handling as not yet authored. That is now stale: the published bilingual Text data collection already contains six progressive exercises. The inventory's TR-A–TR-F labels are shorthand; the source pages use stable descriptive anchors:

- TR-A: `ex-text-data-representation-pipeline`
- TR-B: `ex-text-data-embedding-lookup`
- TR-C: `ex-text-data-representation-context`
- TR-D: `ex-text-data-training-windows`
- TR-E: `ex-text-data-bpe-merges`
- TR-F: `ex-text-data-data-leakage`

### Checks completed

- TR-D's matrices, shapes, valid start positions, corpus-tail reasoning and window-count formula were independently checked. For (N=7,L=3), the counts are 4, 2 and 2 for strides 1, 2 and 3 respectively. The target-copy bug is correctly distinguished from a shape-only check.
- TR-E's occurrence counts and two successive merges were independently checked. (o+w) occurs 4 times, (l+o) 3 times; after the first merge (l+ow) occurs 3 times. Applying the learned merges to `lowest` yields `low · e · s · t · </w>`. The exercise clearly labels its word-level convention as pedagogical, not production byte-level BPE.
- TR-F correctly distinguishes overlapping-window leakage, near-duplicate cross-partition leakage and an explicitly defined temporal-continuation protocol. The train-only tokenizer-fitting recommendation is correctly scoped to a conventional held-out experiment.
- The three exercises' prompts, solutions, equations, limitations and success criteria match in substance in FR/EN. No correction is justified; do not rewrite them.
- The training-examples lessons correctly separate teacher forcing from objective/loss/optimizer; packing from boundary-marker insertion and cross-document masking; padding from attention masks and loss masks; and shape compatibility from semantic alignment.
- The illustrative valid-token mean is (2/3\approx0.667); the naive mean over all five positions is (1.8). The warning that attention masking alone does not ensure PAD targets are excluded from loss is explicit.
- `sliding_input_target_pairs` and its tests cover the declared narrow window/shift contract. They intentionally do not implement corpus loading, packing, padding, collators or loss masks. No implementation expansion is warranted without a separately specified pipeline contract.

### Remaining work

The dedicated FR/EN training-examples Practice companions contain four short checks (shift, teacher forcing/causality, attention versus loss masks, logits axes). They do not yet contain a complete transfer scenario for document boundaries/packing or padded-batch loss reduction. Add a small number of progressive tasks to these existing companions: (1) two documents packed with an EOS/boundary marker, making the cross-document visibility policy explicit; (2) unequal-length examples with separate attention and loss masks and a stated valid-token denominator; (3) optionally, a target-alignment bug introduced by padding. Reuse the lesson's existing examples and keep the tasks conceptual unless a concrete packer/collator implementation exists. Do not duplicate TR-D's window arithmetic or TR-F's split-leakage cases.

The detailed findings, checked arithmetic and acceptance boundary are in [the training-example Practice gap audit](audits/training-example-practice-gaps-2026-11-25.md).

**Validation boundary:** this is a source-level and arithmetic audit, not rendered-page, assistive-technology or learner validation. Use the existing Quarto/browser workflow after any content changes; no new workflow is needed. Manual keyboard/touch/screen-reader checks remain under #483, and learner validation remains gated under #447.


## 2026-11-25: causal-masking exercise ownership and prefix-invariance evidence

**Scope.** Reconcile the published CA-A exercise with the lesson-specific Practice companion, the shared Attention collection, the current NumPy implementation/tests and the roadmap. Reuse the completed technical audit in #81; do not add another mask implementation, duplicate test, or workflow.

### Findings

- The causal-masking lesson already linked to a dedicated companion page, but that companion contained only one short softmax check. The substantive CA-A exercise (mask construction, shifted targets, prefix invariance and mask-type distinctions) lived in the shared Attention collection. The lesson also linked directly to that collection from a supplementary callout. This split ownership did not match the project convention that the lesson points to its own expandable Practice page.
- The full exercise is already technically supported. `tests/unit/test_attention.py::test_scaled_dot_product_attention_causal_invariance` perturbs future keys/values and checks earlier outputs at the single-head primitive level. `tests/unit/test_gpt.py::test_prefix_invariance_future_tokens_do_not_change_earlier_logits` compares prefix logits with the corresponding logits from a longer input under the same GPT. These are complementary targeted regression tests, not formal proofs for all architectures.
- The Further exploration text on both causal lessons incorrectly said that the tests did not cover a complete GPT. It now distinguishes the primitive-level test from the full-GPT logits test and links to both.
- The roadmap's deferred causal-attention section understated the current implementation. It now records the NumPy reference, additive 2D mask contract, local and full-model invariance tests, bilingual lesson links, and the one direct comparison still deferred: numerical parity of the primitive against PyTorch SDPA. The existing Hugging Face GPT-2 eager parity test is not described as an SDPA primitive-parity test.

### Changes in merged PR #1622 and focused PR #1626

- Move the full CA-A task and its worked solution from the shared Attention collection to the dedicated FR/EN causal-masking Practice companions.
- Add two progressive hints, an explicit test-interpretation prompt, and a compact self-check criterion while preserving the existing worked matrices, mask distinctions, command and optional standalone code.
- Keep both previous collection anchors as link-only aliases to the dedicated page, so existing inbound links do not break. Update the collection overview to describe CA-A as owned by the causal-masking companion.
- Keep the core prefix-invariance explanation in the concept page, remove the inline link to CA-A from the conceptual explanation, and expose one prominent link to the dedicated Practice companion near the beginning of the lesson.
- Refresh the generated bilingual learning-map section-heading projections for the newly added CA-A heading.

### Evidence boundary and next action

The move does not change implementation or scientific claims. Run the existing Python suite and full Quarto/browser workflow on the final head of PR #1626; verify the companion pages at desktop/mobile widths and confirm both legacy anchors resolve. Manual screen-reader/touch review remains under #483, and learner evidence remains under #447. The next exercise-development gap from the 2026-11-08 catalogue audit is the text-data transfer sequence (BPE merge tracing, shifted windows and leakage/boundary handling); inspect the current TR-A/B/C and training-example pages before adding anything, to avoid duplication.

### Quarto anchor rendering detail

When a legacy HTML `<a id="…"></a>` alias is immediately followed by a Markdown heading, the heading can be absorbed into the raw HTML block and its explicit heading ID will not appear in the rendered page. Keep a blank line between the alias and the heading, then verify the fragment against the rendered HTML. The CA-A transfer preserves both old fragments and the new canonical `#ca-a-prefix-invariance` target.


## 2026-11-25: Q/K/V, attention and causal-masking Practice audit

**Scope.** Source-level review of the FR/EN Q/K/V exercise collection and the dedicated scaled-dot-product-attention and causal-masking Practice companions. This extends the earlier Q/K/V lesson/source audit without repeating the three-source ingestion or the already completed causal-mask implementation audit. It checks exercise claims, worked arithmetic, prerequisite visibility and the lesson-to-Practice handoff; it is not learner-effectiveness evidence.

### Findings

- The Q/K/V exercise sequence covers the declared competencies: distinguish the roles of Q/K/V; reconstruct projections and tensor shapes; predict which quantities can change under a parameter intervention; explain indirect learning from the model loss; and transfer the provenance distinction to cross-attention. Separate tasks calculate weighted aggregation and distinguish a multi-head concatenation from an attention-weighted sum.
- The worked calculations were checked: the scaled scores $(1,0)/\sqrt{2}$ give weights approximately $(0.67,0.33)$ and output approximately $(6.7,6.6)$ for the stated values; the small matrix products in the projection intervention exercise give $q=(1,2)$, $k=(2,1)$, $v=(1,3)$ and $v'=(2,2)$. The stated invariants under a change to $W_V$ alone are correct.
- The parameter-intervention answers correctly distinguish “can change” from “must change”: changing $W_Q$ or $W_K$ can alter scores and weights; changing $W_V$ alone leaves Q/K-derived weights fixed but can alter the aggregated content. The cross-attention equations correctly source Q from the querying stream and K/V from the queried stream.
- The gradient-path exercise is scientifically consistent with the derivation in the optional Q/K/V deep dive. However, the collection's general preparation note did not expose that dependency: a learner could encounter a matrix-gradient question without being directed to the derivation. The FR/EN collection now links that specific question to the deep-dive section on gradient paths, while keeping the derivation optional for the other projection exercises.
- The scaled-attention companion's numerical softmax, weighted-mixture counterexample and limiting one-hot explanation are correct. The causal-masking companion correctly handles the lower-triangular allowed relation, the shifted-target/diagonal convention, prefix invariance, and the distinct roles of causal, padding, loss and document-boundary masks. Its standalone NumPy check renormalizes only over allowed positions and its stated limitations match the described tests.
- The FR/EN collections use corresponding stable exercise anchors and the same progression. No additional flashcards, new concepts, or new workflow are justified by this audit.

### Change and boundary

A targeted preparation link was added immediately before the Q/K/V gradient-path exercise in both languages. No scientific formula or worked answer required correction in this slice. This is a source-level exercise audit only: it does not establish that learners can transfer the reasoning, does not certify every attention exercise or every Practice collection, and does not replace the independent learner pilot. Advanced multi-head masking variants and broader invariants remain outside this bounded pass.


## 2026-11-25: observed-target scoring and loss Practice audit

**Scope.** Source-level review of the FR/EN Practice companions for likelihood, cross-entropy and loss, plus the shared mathematical-foundations exercises they reference. The pass checks probability factorization, numerical answers, target alignment, masking, aggregation and the distinction between generation and scoring. It does not re-audit the underlying implementation or establish learner effectiveness.

### Findings

- The likelihood exercises correctly apply the chain rule: the running continuation has likelihood $0.6\times0.5=0.3$, log-likelihood approximately $-1.204$ nats and NLL approximately $1.204$ nats. The explanation explicitly avoids an independence assumption between successive tokens. The transfer task correctly distinguishes an observed path with likelihood $0.30\times0.90=0.27$ from the greedy path with likelihood $0.60\times0.40=0.24$: greedy decoding maximizes each local conditional choice, not necessarily the probability of the resulting multi-token sequence.
- The cross-entropy lesson's core one-hot calculation is correctly expressed as $-\log p(y)$; the numerical loss and logit-gradient exercises already exist in the shared Foundations collection. Its soft-target task correctly uses $H(q,p)=H(q)+D_{\mathrm{KL}}(q\Vert p)$ with the order of the KL arguments preserved. The dedicated cross-entropy companion's short conceptual checks are therefore complemented by existing numerical tasks; duplicating those tasks would be unnecessary.
- The loss exercise correctly distinguishes a token visible as an input from the same token's earlier target being excluded from the loss. Its row-2 query can see the observed prefix $(A,B)$ but not the future input $C$. Changing the future token can change the observed target's probability and loss without changing that row's prediction distribution.
- The shared Foundations masking exercise's valid-target reduction arithmetic is correct: with losses $\ln2,\ln4,\ln8$, the mean over three valid positions is $2\ln2\approx1.386$ nats. In the dedicated loss companion, the two included targets contribute $\ln2$ and $\ln4$, giving a mean of $\tfrac32\ln2\approx1.040$ nats; restoring the excluded first target gives $2\ln2\approx1.386$ nats over three targets. Including the ignored position in the denominator would change the objective. The checkpoint exercise also correctly distinguishes a global valid-token mean (X: 1.0; Y: 1.4) from an unweighted mean of batch means (X: 1.75; Y: 1.25), which can reverse the ranking when batch sizes differ.
- The corresponding FR/EN exercise anchors and intended reasoning are aligned. No correction to the mathematical answers was found in this bounded group.

### Change and boundary

The cross-entropy Practice companions now link directly to the existing shared exercises for (1) logits → softmax → one-hot NLL and (2) soft targets → cross-entropy/KL. The broader Foundations collection remains the owner of those calculations; no duplicate exercise was added. This is a source-level and arithmetic audit, not a learner study or a complete audit of every scoring/training resource.


## 2026-11-25: prefill, teacher forcing and free-running generation audit

**Scope.** Bounded FR/EN review of the generation lesson, its Practice hub and GE-D prefill/decode exercise, alongside the Build G2 training-examples lesson and the text-data Practice collection. The purpose was to verify that three related but non-equivalent ideas are not collapsed: inference prefill, teacher-forced conditioning on observed/reference tokens, and free-running autoregressive feedback.

### Findings

- The generation collection contains **eight** formative exercises (GE-A–GE-H), including a prefill/decode trace and a later prefix-caching/continuous-batching exercise. No additional generic prefill exercise is needed.
- The Build G2 lesson correctly defines shifted pairs $x=[t_0,\ldots,t_{L-1}]$ and $y=[t_1,\ldots,t_L]$, explains the causal restriction at each position, and explicitly says teacher forcing is a conditioning strategy rather than the objective, loss or optimizer. It correctly distinguishes the reference window-builder from an actual trainable forward pass.
- The existing GE-D exercise's answer was too compressed: it described teacher forcing as conditioning on an observed prefix (also used for scoring) but did not make explicit the key training distinction—reference tokens remain inputs even when the model would have predicted something else, and training compares position-wise logits with shifted targets. This could leave the conceptual difference from prefill underspecified.
- The generation lesson's previous phrase “prefill resembles teacher forcing” was directionally useful but risked implying equivalence. Both can process known tokens under a causal mask; however, prefill is an inference execution phase that obtains the first next-token distribution and may populate a KV cache, while teacher forcing is a conditioning regime using reference tokens (with shifted targets and loss in training). Scoring may also condition on an observed prefix with fixed parameters. Free-running generation instead feeds back selected tokens.
- The text-data Practice collection already exercises the construction of shifted windows, complete-target boundaries, window counts and alignment bugs. It did not explicitly test whether learners understand that teacher forcing does not feed back the model's own predictions. A targeted fourth stage now tests that counterfactual and contrasts it with free-running generation, then points to the existing prefill/decode exercise.
- The FR/EN generation lesson, GE-D answer, self-check answer and new Practice stage now use the same three-way distinction and cross-link the complementary material. No training implementation is introduced; the existing prerequisite gate on G8 remains untouched.

### Changes and boundary

The bilingual generation lesson now states the limited similarity and the operational distinction. GE-D and the generation self-check give a more precise explanation. The text-data Practice collection gains one targeted teacher-forcing-versus-free-running exercise, and GE-D links to it. This is a source-level pedagogical correction; it does not validate learner mastery, implement pretraining, or replace the separate G8 prerequisite review.

## 2026-11-25: gradient-to-parameter-update audit

**Scope.** Bounded FR/EN source review of the loss, gradients and training-loop lessons; the dedicated gradient and training-loop Practice pages; the maintained NumPy cross-entropy implementation; and the numerical training-loop example. The pass checks representative derivatives, tensor/parameter relationships, update arithmetic, optimizer terminology and exercise coverage. It does not certify every backward operation in a Transformer, run a framework-level autodiff suite, or clear the G8 implementation gate.

### Findings

- For a one-hot target, the derivative of softmax cross-entropy with respect to logits is correctly stated as p − y. Its components sum to zero, consistently with softmax invariance to a common logit shift. For the unweighted mean over valid target positions, the additional factor 1/|M| and zero direct derivative at ignored logit positions are correctly included.
- The lesson correctly distinguishes a zero derivative at an ignored position's logits from a zero gradient throughout the computation graph: that position's representation may still influence valid logits through allowed attention dependencies. The loss mask and attention mask are not interchangeable.
- The chain-rule expression ∇θL = (∂z/∂θ)ᵀ ∇zL is dimensionally coherent when z is the flattened collection of logits involved in the objective. The explanation correctly notes that reverse-mode backpropagation applies the transposed Jacobian without materializing the full Jacobian.
- For an affine output head z = Wh + b, the outer-product derivative ∂ℓ/∂W = g_z hᵀ is correct. The worked SGD step with h = (1,−1), η = 0.1 and p = (0.6,0.2,0.1,0.1) yields a new target probability of approximately 0.6261, consistent with the displayed 0.626.
- The paired equal-loss exercise is arithmetically correct: both distributions assign probability 1/2 to the observed target and therefore have loss ln 2, but their non-target bias gradients differ. Recomputed target probabilities after the update are approximately 0.53743 and 0.54048, consistent with the rounded answers.
- The NumPy cross-entropy-gradient implementation returns the gradient of the batch-mean cross-entropy. The training example correctly accumulates repeated input-token row contributions with np.add.at; the resulting parameter gradient is the chain rule through the lookup of a row of W.
- Re-executing the documented deterministic NumPy example with seed 0 reproduces the reported qualitative behavior and rounded values: training loss 2.4849 at initialization and 1.1467 at step 300; validation loss reaches its lowest recorded value, 2.0059, at step 100 and rises to 2.1621 at step 300.
- **Terminology correction:** the micro-example uses all 60 training examples for every update. It is full-batch gradient descent, not stochastic/mini-batch SGD. The general explanation of stochastic gradient descent remains valid for sampled mini-batches, but the example and its code comment were too loosely labelled. The bilingual lesson now distinguishes these cases explicitly.
- **Optimizer precision:** the prior wording that Adam and AdamW differ only in their update rule was too compressed for AdamW. The bilingual lesson now states that AdamW adds decoupled weight decay to the update, separate from the gradient of the data loss. Its second moment remains distinct from a Hessian or a curvature estimate.
- The dedicated FR/EN gradient exercises cover the cross-entropy logit derivative, finite-difference diagnosis, learning-rate overshoot, and a parameter-level update. The training-loop exercises cover the distinction between gradient and update, validation without parameter mutation, checkpoint choice, and end-to-end transfer. No additional duplicate exercise is justified by this pass.

### Changes and boundary

The FR/EN training-loop lessons now distinguish sampled mini-batch SGD from full-batch gradient descent, accurately label the deterministic 60-example implementation, and qualify the AdamW weight-decay contribution. The existing exercises and numerical examples were retained; no duplicate tasks or training implementation were added.

### Remaining work

- Independently verify the finite-difference guidance against a concrete deterministic function and documented tolerances; this pass inspected the explanation but did not run PyTorch gradcheck.
- Audit gradients through at least one earlier Transformer operation (for example, a Q/K/V projection and attention aggregation), not only the final affine output head. Include shape checks and distinguish shared-parameter accumulation across positions/batch items.
- Verify the repository's actual autodiff/backward tests and the implementation evidence claimed by the Build milestones. The small NumPy example is not a Transformer backward pass.
- Keep the end-to-end training loop, optimizer integration, gradient clearing/accumulation semantics, checkpointing and validation executor behind the existing G8 prerequisite gate. This audit does not clear that gate.
- Learner transfer remains unmeasured: source correctness and arithmetic checks do not establish that readers can independently derive or debug parameter gradients.

### Attention-gradient continuation — 2026-11-25

The bilingual Q/K/V deep dive now makes the row-wise softmax backward rule explicit: $(G_S)_{ij}=A_{ij}((G_A)_{ij}-\sum_r A_{ir}(G_A)_{ir})$. The fixed additive mask is not differentiated; forbidden positions have zero softmax weight and therefore zero score gradient, provided the row has at least one accessible key.

The existing Q/K/V learning exercise asked learners to identify gradient paths and projection-gradient forms, but did not require a numerical reverse-mode calculation through attention. The bilingual Practice collection now adds optional exercise AT-E: one query, two keys and values, a scalar upstream objective, and a worked calculation of $G_V$, $G_A$, $G_S$, $G_Q$ and $G_K$. Its arithmetic was independently checked. This is a local single-row exercise; it does not validate batched/multi-head backward code or establish learner mastery.

Still open: finite-difference verification of the full attention path; shared-parameter accumulation across positions/batch items and heads; backward tests for the full Transformer block; and the gated G8 training loop in issue #656. Do not start G8 implementation before its separate prerequisite review.


## 2026-11-26: main Understand route — text, representations and Transformer hand-off

**Scope.** Bounded FR/EN source audit of the first main-route segment: `text-data`, `embedding-space`, `positional-encoding`, `contextualized-representations`, and the hand-off into `transformer` / `queries-keys-values`. Cross-checked page-map metadata, bilingual counterparts, `data/guided-route.yml`, and the canonical computational graph in `data/computational-graph.yml`. This is a source/architecture audit, not a rendered browser review, a complete mathematical re-derivation, or learner-effectiveness evidence.

### Findings

- **The route sequence is coherent in source.** The page-map links and the `representations` guided-route stage agree on `text-data → embedding-space → positional-encoding → contextualized-representations`; the next page-map transition is `contextualized-representations → transformer → queries-keys-values`. The guided route then moves into the `computation` stage. No route-registry change is justified by this pass.
- **Text → IDs → lookup is explained with useful concrete evidence.** The FR/EN lessons distinguish token boundaries, tokenizer-local IDs and learned vectors; compare two tokenizers on the same exact arithmetic string; explain the tokenizer/checkpoint contract, special tokens, context-budget implications, and separate prompt encoding from corpus/tokenizer preparation. The FR lesson links to a reproducible tokenizer/lookup trace and a dedicated Practice page. The EN page preserves the same conceptual coverage. The different running prompts in FR and EN are not by themselves a parity defect; their token traces are language-specific.
- **The embedding page has a clear and appropriately bounded role.** It treats an ID as a row address, not a numerical coordinate or semantic distance, and distinguishes the initial lookup from later contextual states. Its Build and Deepen destinations are separated from the core explanation; the exercises have a dedicated companion.
- **The positional page distinguishes two independent questions.** It separates the signal that represents position/relative offset from the causal constraint that determines which keys a query may access. It correctly places RoPE on projected Q/K before the attention score product, classifies it as a relative mechanism, and reserves derivations for Deepen. The guided-route criterion explicitly scopes the additive learned-position equation to the project's GPT rather than every architecture.
- **The contextualization page makes the critical fixed-variable comparison.** It states the same-ID/same-lookup assumption, distinguishes initial embeddings from layer hidden states, and compares past versus future perturbations at a fixed position in a causal GPT. It does not claim that contextualization guarantees a human-interpretable semantic geometry.
- **The architectural hand-off is directionally correct.** The contextualization lesson says that Transformer blocks produce contextualized states; the Transformer overview owns the repeated block stack and the forward path to logits; Q/K/V are introduced as operations inside a block. This matches the canonical computational graph, where `transformer-block-input` feeds Q/K/V projections. It avoids the incorrect sequence “final contextualized representations, then Q/K/V”.
- **FR/EN page-map contracts and the visible route are aligned for the four audited pages.** Their `previous/next` metadata and the eight-stage route agree. All four pages currently declare `revision_support.status: integrated_sufficient`; that metadata is evidence of a recorded revision pass, not independent proof that rendered explanations, examples and accessibility are fully validated.

### Status decision

| Page pair | Source status | Remaining validation |
|---|---|---|
| `text-data` | **Ready for the main route** | Render the exact tokenizer tables/math and verify exercise/revision links in FR/EN; do not expand the core lesson into a BPE algorithm tutorial. |
| `embedding-space` | **Ready for the main route** | Render the matrix/lookup examples and verify the Practice/Build/Deepen hand-off. |
| `positional-encoding` | **Ready for the main route** | Verify bilingual diagrams and rendered equations; retain the distinction between positional signal and causal visibility. |
| `contextualized-representations` | **Ready for the main route, with a boundary check at the next page** | Verify the past/future comparison and diagram; ensure the Transformer overview immediately explains how block operations produce the contextual states. |
| `transformer` → `queries-keys-values` | **Next audit target; not certified by this slice** | Audit the full block computation and its boundary with the preceding contextualization page. |

No content rewrite or metadata change is warranted for the four first-segment pages based on this source pass. In particular, do not change the guided route, introduce a second graph, or add per-page orientation configuration merely to restate links that already work in the source model.

### Remaining work for subsequent sessions

1. **Continue the source audit at the hand-off, not by reopening the four pages indiscriminately.** Inspect FR/EN `transformer`, `queries-keys-values`, `scaled-dot-product-attention` and `causal-masking` as one group. Check that each block receives its input hidden states; Q/K/V are projected from that block input; attention output, residual path, normalization and MLP are located in the correct order for the architecture actually taught; repeated blocks produce the final states; and the output head produces logits. Record architectural variants explicitly rather than implying one universal block.
2. **Check tensor contracts across the group.** Reconcile batch, sequence, model, head and head-dimension symbols; matrix orientations; Q/K/V shapes; attention-score and mask shapes; softmax axis; and the location of the causal mask. Recompute worked numerical examples rather than relying on existing `revision_support` notes.
3. **Check the shared-core boundary into prediction.** Audit `logits`, `probabilites` / `probabilities`, and `entropy` together. Verify that the output projection consumes the final hidden state at each position and that vocabulary softmax is not confused with attention softmax.
4. **Then audit the three sibling uses, without forcing them into one sequence:** generation (including prefill, incremental decode and optional KV cache); observed-target scoring/evaluation (likelihood and held-out aggregation, fixed parameters); training (shifted targets, teacher forcing, loss, gradients and parameter update). Reuse the existing audits and evidence in this file and issues #584/#656; do not duplicate completed scoring, prefill/teacher-forcing or gradient exercises.
5. **Rendered validation remains separate.** For each bounded group, verify FR/EN Quarto output, links/anchors, math, diagrams, code blocks, responsive layout, keyboard operation and accessibility. Manual screen-reader evidence and native breadcrumb ancestry/labels remain open in #584; axe success does not close them.
6. **Reconcile the route and implementation crosswalk only when a concrete mismatch is found.** Keep `data/concepts.yml`, `data/computational-graph.yml`, `data/guided-route.yml` and the Build milestones as four distinct representations. Do not create another registry, workflow per concept, or speculative per-page JavaScript.

### Recommended next session entry point

Start with the FR/EN `transformer.qmd` pair, then follow the existing route into Q/K/V, scaled attention and causal masking. Use the current source audit in the first vertical slice above as a closed baseline; reopen those pages only if the block-level audit identifies a specific upstream contradiction. Update this inventory with dated evidence and exact residual checks after each bounded group.


## 2026-11-26: main Understand route — Transformer block, Q/K/V and causal attention

**Scope.** Bounded FR/EN source review of `transformer`, `queries-keys-values`, `scaled-dot-product-attention` and `causal-masking`. Cross-checked page-map navigation, the computation-stage sequence in `data/guided-route.yml`, and the corresponding nodes/edges/resources in `data/computational-graph.yml`. This pass inspected the lesson explanations and representative equations; it did not render the pages, re-derive every optional advanced equation, or repeat the Practice arithmetic audit recorded on 2026-11-25.

### Findings

- **The Transformer overview is fit for the main route.** FR/EN versions describe a decoder-only GPT, distinguish the network forward pass from downstream softmax/token selection, and show both the full stack and a pre-LN block. They locate attention, the position-wise MLP, residual stream, normalization, final normalization and vocabulary projection. The text explicitly scopes pre-LN as the illustrated arrangement and notes architectural variation. It also separates parallel masked training computation from sequential autoregressive generation.
- **The Q/K/V lesson correctly starts inside a block.** It says the shared input is the current block state, not the final contextualized output of the entire network. For the reference pre-LN GPT it writes the normalized projection input as $X=\operatorname{LN}_1(H_{\mathrm{in}})$ while the residual path receives $H_{\mathrm{in}}$. It also explains that in later blocks the input already contains contextualized states. RoPE is located after Q/K projection and before score computation; the lesson explicitly says its projection equations precede the rotation.
- **The Q/K/V tensor contracts are internally consistent.** For one self-attention head, $X\in\mathbb{R}^{T\times d_{model}}$, $W_Q,W_K\in\mathbb{R}^{d_{model}\times d_k}$, and $W_V\in\mathbb{R}^{d_{model}\times d_v}$ give $Q,K\in\mathbb{R}^{T\times d_k}$ and $V\in\mathbb{R}^{T\times d_v}$. The page keeps self-attention provenance distinct from cross-attention, where Q and K/V come from different streams.
- **The attention page has the correct operation order and axes.** It presents $S=QK^\top$, scaling by $\sqrt{d_k}$, optional additive masking, row-wise softmax over accessible key positions, then $O=AV$. Shapes are $T\times T$ for scores/mask/weights and $T\times d_v$ for the output. It distinguishes this positional softmax from the later vocabulary softmax and warns against interpreting weights as semantic relevance or causal attribution.
- **The causal-mask lesson is consistent with the attention formula.** It defines allowed $j\le i$ / blocked $j>i$, applies the additive mask before softmax, explains why the diagonal is allowed under shifted next-token targets, and separates causal, padding, document-boundary and loss masks. It also records API-specific boolean-mask polarity and the exact limitations of the repository's reference implementation.
- **The graph and route match the page explanations.** The computation-stage order is Transformer overview → Q/K/V → scaled attention → causal masking. The computational graph represents Q/K/V projections as operations from `transformer-block-input`, and the causal mask as a control on the attention-score path. This is consistent with the four separate project representations; no route or graph change is warranted.
- **FR/EN semantic parity is strong for the inspected core explanations.** Page titles, scopes, objectives, equations, major diagrams and transition links correspond. The running narrative differs between languages, which is appropriate for the language-specific examples and does not alter the underlying mechanism.

### Status decision

| Page pair | Source status | Remaining validation |
|---|---|---|
| `transformer` | **Ready for the main route** | Render both architecture diagrams; inspect first-screen legibility, equations, and the hand-off to Q/K/V and logits. |
| `queries-keys-values` | **Ready for the main route** | Render projection equations and responsive diagrams; verify that the pre-LN input notation is legible to a first-time reader and that the one-head scope is explicit. |
| `scaled-dot-product-attention` | **Ready for the main route** | Render formula and attention-flow diagrams; independently recompute the lesson's worked example if changed. |
| `causal-masking` | **Ready for the main route** | Render the triangular mask and verify links/anchors; keep implementation/API detail in its supplementary section. |

No source-level mathematical or architectural correction was identified in this bounded pass. The existing Practice audit of Q/K/V, scaled attention and causal masking is recorded above (2026-11-25); it should not be repeated without a specific changed source or a failed validation.

### Remaining work after this slice

1. Complete rendered FR/EN review of these four pages: responsive diagrams (especially the Q/K/V and attention matrices), math rendering, page transitions, Practice links, keyboard/focus behavior and accessibility.
2. Audit the next prediction group: `logits` → `probabilites` / `probabilities` → `entropy`. Explicitly distinguish the final hidden state, output projection, vocabulary softmax and attention softmax.
3. Audit the branch point from the conditional distribution into generation, observed-target scoring/evaluation and training. Reuse the dated scoring, prefill/teacher-forcing and gradient audits already in this inventory; do not rebuild the same evidence.
4. Keep manual FR/EN screen-reader and native breadcrumb ancestry/label checks tracked in #584. Automated axe results do not close them.


## 2026-11-26: main Understand route — logits, probabilities and predictive entropy

**Scope.** Bounded FR/EN source review of `logits`, `probabilites` / `probabilities`, and `entropy`; cross-checked the prediction stage and its outgoing transitions in `data/guided-route.yml`, plus the corresponding final-hidden-state, vocabulary-projection, logits, softmax and sibling-use nodes in `data/computational-graph.yml`. The pass checked the representative running examples and mathematical definitions. It did not render the pages or independently audit downstream generation/scoring/training lessons.

### Findings

- **The logits lesson correctly closes the network forward pass.** It takes the final hidden state at a prediction position, applies the vocabulary projection, and obtains one score per vocabulary token. The FR/EN pages distinguish score, probability and truth; state the $(B,T,V)$ batch/sequence/vocabulary axes; and explain common-shift invariance and why the raw maximum is not a confidence measure. The training note correctly says a stable cross-entropy implementation can consume logits directly without an explicit prior softmax.
- **The probabilities lesson correctly defines the shared conditional-distribution boundary.** It applies vocabulary softmax to logits at one position, distinguishes normalization from calibration and factual truth, and differentiates attention softmax (over accessible positions) from vocabulary softmax (over candidate tokens). It also separates optional decoding policy operations—temperature, top-k and top-p—from the base predictive distribution, and notes that library ordering can vary.
- **The same four-token running example is numerically consistent across the output projection, probability and entropy pages.** The illustrative probability vector $(0.6,0.2,0.1,0.1)$ has entropy $-\sum_i p_i\ln p_i\approx1.089$ nats; the maximum for four outcomes is $\ln4\approx1.386$ nats, so the stated ratio is about 79%. The FR and EN token labels differ with their respective narrative examples, while the numerical distribution and mathematical reasoning agree.
- **The entropy lesson distinguishes three different objects.** Predictive entropy is the expected surprisal over the full distribution before the next token is observed; the surprisal $-\log p(x_t\mid x_{<t})$ belongs to one observed token; and cross-entropy compares a target distribution with the model distribution. It correctly avoids treating low entropy as factual correctness or empirical calibration.
- **The branch semantics are explicit at the distribution page and in the canonical registries.** The probability lesson names generation, observed-target scoring and learning as three uses. The guided route declares prediction → inference, prediction → observed scoring, and prediction → training transitions; the computational graph likewise keeps generated-token feedback, observed-target scoring/evaluation and parameter-updating training as distinct branches.
- **The global suggested-route chain and the guided-route branch navigation serve different purposes.** The page-map validator and regression test require the legacy scoring sequence `entropy → vraisemblance / likelihood → cross-entropy`; the test explicitly preserves `likelihood.previous = entropy` while contextual transition cards provide the additional inference/generation branch from prediction. Do not rewrite this global route edge to `entropy → generation`: doing so breaks reciprocal metadata validation and the guided-route projection contract. The generation stage remains a sibling use of the shared conditional distribution in `data/guided-route.yml` and `data/computational-graph.yml`; its contextual navigation is the correct place to expose that branch. This PR restores the tested reciprocal scoring metadata and leaves the canonical graph unchanged.
- **FR/EN content parity is strong for the audited concepts.** The formulas, definitions, example probabilities, temperature semantics, calibration caveats and links to the next lessons correspond. The running token labels are localized rather than forced to be identical.

### Status decision

| Page pair | Source status | Remaining validation |
|---|---|---|
| `logits` | **Ready for the main route** | Render the output-projection example, $(B,T,V)$ notation and common-shift figure; verify the link to probabilities. |
| `probabilites` / `probabilities` | **Ready for the main route** | Render the softmax example and three-use branch explanation; inspect the transition cues against the guided route. |
| `entropy` | **Ready for the main route** | Render the entropy calculation and figure; verify the legacy scoring next-step cue and the separate contextual inference transition in FR/EN. |

No mathematical correction was identified in this bounded pass. The downstream pages for generation, likelihood, cross-entropy, loss and gradients have their own dated audits in this inventory; those checks are not repeated here.

### Remaining work after this slice

1. Render the prediction group in FR/EN and inspect the equation, numerical table, entropy chart, accessibility text and links at desktop/mobile sizes.
2. Verify in the rendered FR/EN pages that the global entropy → likelihood scoring cue remains reciprocal and that the contextual guided-route transition separately exposes prediction → inference/generation. Do not conflate the page-map suggested-route chain with the guided-route stage graph.
3. Continue with a cross-branch audit of generation, observed-target scoring/evaluation and training. Use the existing 2026-11-25 audit entries for prefill, teacher forcing, likelihood, cross-entropy, loss and gradients; inspect only gaps or contradictions, not already checked arithmetic.
4. Record manual screen-reader and native breadcrumb evidence under #584; automated browser/Axe checks remain a separate evidence class.


## Issue #1739 — Understand representation lessons (2026-11-27)

A source-grounded page-by-page audit of the bilingual **Positional encoding** and **Contextualized representations** lessons, their revision sheets, Practice companions and existing Deepen destinations is recorded in [the representation contribution audit](source-syntheses/understand-representations-intellectual-contributions-audit-2026-11.md).

This batch confirms that both lessons already have several substantial contributions: positional insertion-point distinctions and the separation of positional information from causal visibility; shared embedding lookup versus context-dependent hidden states, causal dependency boundaries, and limits on semantic interpretation. The source-derived empirical measurements for contextuality remain in Deepen. No new page metadata field, contribution registry, concept node or route step is justified.

The audit is source-only. It does not claim rendered visual, accessibility or learner validation. The next #1739 batch should continue in canonical Understand route order and reuse the existing Q/K/V pilot rather than repeat it.


## Issue #1739 — branches génération, scoring et apprentissage (2026-11-27)

Audit source page par page des leçons Understand FR/EN `generation`, `vraisemblance` / `likelihood`, `loss`, `gradients` et `training-loop`. Le pilote cross-entropy #1739 est réutilisé sans duplication. La matrice détaillée et les décisions de conservation sont dans [le dossier des contributions génération/scoring/apprentissage](source-syntheses/understand-generation-scoring-training-contributions-audit-2026-11.md).

### Résultats

- Les trois usages de la distribution prédictive restent distincts : génération libre (token sélectionné puis réinjecté), scoring (token de référence observé) et apprentissage (cible observée, loss, gradient puis mise à jour).
- La génération distingue forward pass, sélection/décodage et boucle complète ; le choix local change le préfixe et peut changer toute la suite, sans optimiser la vraisemblance globale.
- Le scoring factorise la probabilité d'une séquence selon les préfixes de référence ; il ne sélectionne pas les tokens. La perplexité dépend du tokenizer, du corpus et de la convention d'agrégation.
- La loss explicite l'alignement logits-position cible et le risque d'un décalage silencieux. Teacher forcing est un régime de conditionnement, pas une loss ni un optimiseur.
- Le masque de loss n'est pas un masque d'attention. Une position exclue comme cible peut rester visible en entrée ; sa représentation peut recevoir un gradient indirect via une position supervisée qui l'utilise comme clé ou valeur.
- Le gradient n'est pas l'update. Seule l'étape de l'optimiseur modifie les paramètres ; la validation mesure le modèle à paramètres fixes.

### Décision

Aucune modification des leçons n'est justifiée par cette inspection : les apports sont déjà présents et les audits Practice/numériques du 25 novembre les ont en partie vérifiés. Aucun nouveau concept, champ de métadonnées ou registre n'est requis. Les distinctions ci-dessus deviennent des invariants de conservation pour les futures refontes.

### Limites et suite

Ce lot est un audit de contenu source, pas une validation de rendu ou d'accessibilité. La vérification Quarto/browser, mobile, navigation, clavier et lecteur d'écran reste à effectuer. Continuer l'inventaire exhaustif à partir des registres canoniques, sans réauditer les pages déjà couvertes par les pilotes et audits datés.


## Issue #1739 — apprentissage en contexte et ingénierie du contexte (2026-11-27)

Audit source FR/EN des leçons Understand `in-context-learning` et `context-engineering`, avec leurs exercices Practice dédiés. Voir [le dossier des contributions autour du contexte](source-syntheses/understand-context-use-intellectual-contributions-audit-2026-11.md).

### Résultats

- ICL décrit l'utilisation d'instructions et de démonstrations présentes dans le prompt à paramètres fixes ; context engineering décrit le travail du système pour sélectionner, organiser, actualiser et sécuriser les informations transmises.
- La leçon ICL distingue zero-shot/one-shot/few-shot, fine-tuning et RAG ; elle explicite que la reproduction d'un format ne prouve pas la généralisation et que les induction heads ne sont qu'une hypothèse mécaniste partielle.
- Context engineering formalise trois niveaux : contexte disponible dans le système, séquence effectivement transmise dans la fenêtre, positions accessibles à une requête selon le masque et l'architecture.
- Le contenu stocké ou récupéré n'est pas automatiquement transmis. La page relie cette frontière à la provenance, à la fraîcheur et aux risques d'injection indirecte.
- Les exercices Practice couvrent généralisation, sélection, transmission, accès causal, provenance, sécurité et évolution du contexte entre appels.

### Décision et limites

Les deux pages disposent déjà d'apports distinctifs suffisants ; aucune modification de leçon, nouveau concept ou extension des métadonnées n'est justifié. Le lot est source-only : rendu des diagrammes FR/EN, mobile, navigation, clavier et accessibilité manuelle restent à vérifier.


## Issue #1739 — panorama et entrée texte (2026-11-27)

Audit source FR/EN des premières leçons Understand `llm-overview` et `text-data`, ainsi que de la page Practice dédiée à `text-data`. Le pilote `embedding-space` est réutilisé sans répétition. Voir [le dossier panorama et entrée texte](source-syntheses/understand-overview-text-input-intellectual-contributions-audit-2026-11.md).

### Résultats

- Le panorama définit une distribution conditionnelle du prochain token et distingue génération, scoring et apprentissage comme trois usages, pas comme étapes d'une seule exécution.
- Il sépare architecture, apprentissage et utilisation, et distingue LLM (catégorie), Transformer (famille d'architectures) et GPT (famille decoder-only).
- Il distingue paramètres appris, contexte transmis et informations externes récupérées ; les poids ne sont pas une base documentaire consultable.
- `text-data` suit une occurrence de texte jusqu'aux tokens, IDs et vecteurs ; les IDs sont locaux à un vocabulaire et ne sont pas des quantités sémantiques.
- Le tokenizer fait partie du contrat du checkpoint : vocabulaire et conventions doivent rester associés aux poids, qui indexent les embeddings d'entrée et les logits de sortie.
- Les conséquences du nombre de tokens sur le budget et le coût sont présentées avec des limites explicites ; un découpage plus court ne prouve ni meilleure qualité ni meilleure maîtrise linguistique.

### Décision et limites

Les deux pages disposent déjà d'apports distinctifs suffisants ; aucune modification, nouveau concept ou extension des métadonnées n'est justifié. Les rendus FR/EN, figures, blocs d'exemple, affichage mobile et accessibilité restent à vérifier.


## Issue #1739 — matrice consolidée du parcours Understand (2026-11-27)

La [matrice consolidée des contributions](source-syntheses/understand-route-intellectual-contributions-index-2026-11.md) rassemble une ligne par leçon canonique bilingue de `data/guided-route.yml`, avec les apports distinctifs à préserver et les dossiers/pilotes qui constituent les preuves détaillées.

Elle confirme la couverture source de toutes les leçons Understand du parcours principal. Elle ne certifie pas leur rendu visuel ni leur accessibilité. Le contrat de modélisation retient les structures existantes — catalogue/extractions, dossiers de synthèse, concepts, graphe computationnel, parcours et page-map — sans ajouter de champ `intellectual_contributions` ou de registre exécutable parallèle. La maintenance doit mettre à jour la matrice et les dossiers de preuve lors de toute refonte.


## 2026-11-28: concept bridge `language-representation` — shared Practice destination

**Scope.** Source-level FR/EN audit of the published `language-representation` concept bridge in the `text-input` stage, its hand-off to `text-data`, and the existing bilingual `exercises/text-data.qmd` companion hub. Cross-checked `data/guided-route.yml`, inline PAGE-MAP metadata, the companion's questions and the generated learning-map payloads. This is a bounded source/metadata audit; it is not a rendered-browser, screen-reader or learner-validation result.

### Findings

- **Route identity and denominator.** The `text-input` stage contains two core destinations: `language-representation` (type `concept-bridge`) and `text-data` (type `concept-lesson`). The bridge is a published Understand page and must be represented in route-wide page inventories, but it is not one of the 20 canonical concept lessons counted by the #1739 intellectual-contribution matrix. Keep the two denominators explicit: 20 canonical lessons, plus this separate bridge page.
- **Distinct role.** `language-representation` motivates why neural networks use learnable numerical representations. It distinguishes symbolic units, arbitrary vocabulary IDs, learned vectors, distributional regularities, and occurrence-specific contextualized states. It deliberately leaves concrete tokenization, detailed lookup, vector geometry and Transformer mechanisms to their dedicated pages.
- **The shared Practice hub already assesses the bridge's core distinctions.** Its bilingual checks ask whether repeated occurrences of one ID select the same initial vector, whether an ID encodes meaning, and whether IDs from different tokenizers can be compared. Its applied exercises trace text → IDs → embedding rows and the first-block input, then distinguish lookup invariants from positional/contextual transformations. The broader text-data collection supplies the extended tokenizer, lookup and windowing tasks.
- **A separate bridge-only exercise page would duplicate existing assessment.** The existing `exercises/text-data.qmd` hub is a coherent group destination for the bridge and the following `text-data` lesson: both occupy the same route stage and share the ID → initial-vector → contextualized-state distinctions. The `embedding-space` lesson retains its own dedicated companion; its cross-cutting links to the text-data collection are not reclassified as part of this group.
- **A real navigation omission was present.** Neither language version of `language-representation` exposed a Practice section or companion link, and the shared hub did not link back to the bridge. The source pages now expose a short link-only Practice section; the hub names the shared group and provides return links to both lessons.
- **Example continuity.** The French overview, bridge and text-data lesson use the Otis exchange. The English overview and text-data lesson use the Romans question, but the English bridge previously claimed to follow the same running example while using Otis. Its lead now identifies Otis as a separate contrastive example and explicitly names the Romans question as the English running prompt. The underlying semantic contrast and tokenizer claims are unchanged.
- **Metadata and generated projections.** The bridge and shared hub now have reciprocal PAGE-MAP `related` references. The tracked FR/EN learning-map JSON and inline map-data payloads match the source metadata and current content headings. The link-only `Exercices` / `Practice` section is intentionally excluded from generated content headings; the companion association is represented by the `related` references. No guided-route stage, concept, computational edge, metadata field or navigation system was added.

### Decision

Retain `language-representation` as a concept bridge, not as a new canonical concept lesson. Reuse the existing `text-data` Practice hub as an explicitly justified shared companion for the two pages in the text-input stage. Do not create another exercise page or duplicate the current ID/lookup/context questions. Keep the extended tokenizer and windowing tasks in the existing Text data collection.

### Validation boundary and follow-up

Source links and reciprocal page-map references were checked against the exact bilingual file paths. The map payload changes mirror the generator's serialization contract, but the official map-generation command and freshness tests have not been run locally in this pass. Require the existing CI freshness checks, full Quarto render and browser review on the final PR head. Manual screen-reader and learner checks remain separate and are not claimed here.
