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


## Active text-to-embedding slice: PR #118 validation

**Scope:** [#82](https://github.com/JM-Brun/llm-lab/issues/82), coordinated by [roadmap #78](https://github.com/JM-Brun/llm-lab/issues/78). This is still the active slice; later attention, model and training implementations remain deferred.

| Check | Evidence | Status / limitation |
|---|---|---|
| One consistent input across text, tokenizer IDs and embedding lookup | [PR #118](https://github.com/JM-Brun/llm-lab/pull/118), merged at `50734b1f74bc1778431ec255861489223be4c2d0`; EN and FR embedding-space pages trace `hello world` through UTF-8, GPT-2 `tiktoken` IDs `[31373, 995]`, token byte fragments, synthetic embedding rows and illustrative absolute-position addition. | Source content present. Real tokenizer IDs are distinguished from synthetic embedding/position values; no claim is made that the example loads GPT-2 weights or computes contextual states. |
| Python CI on the merged revision | [Run 40897933771](https://github.com/JM-Brun/llm-lab/actions/runs/40897933771), on the merge commit. | Passed: dependency installation, formatting, lint, type check and tests. This does not execute the documentation's `tiktoken` snippet. |
| Quarto render and publication | [Run 40897934138](https://github.com/JM-Brun/llm-lab/actions/runs/40897934138), on the merge commit. The generated GitHub Pages artifact was inspected to confirm both `en/embedding-space.html` and `fr/embedding-space.html` contain the trace and pinned install instruction. | Render and deploy passed; artifact content checked. Artifact inspection is not a substitute for browser-based visual/responsive review. |
| Exact tokenizer behavior | Expected IDs and fragments were cross-checked against the official [tiktoken encoding tests](https://github.com/openai/tiktoken/blob/main/tests/test_encoding.py). NumPy lookup and position-value assertions were tested separately. | The complete example was **not** executed in an environment with `tiktoken==0.14.0`; this remains open. |
| Browser / responsive review | Attempts to open the deployed EN/FR pages were not accessible through the available browser retrieval. | **Not verified.** Inspect both languages at desktop and mobile widths when a browser session is available. |
| Mastery | No learner diagnostic has been administered for this slice. | Not assessed; do not infer mastery from content, CI or publication. |

### Remaining checks before closing #82

- [ ] Execute the complete embedded example with `tiktoken==0.14.0` in a reproducible Python environment, or explicitly disposition the example as documentation-only and explain why execution adds no distinct value.
- [ ] Inspect deployed EN/FR pages and figures at desktop/mobile widths.
- [ ] Spot-check the external tokenizer references and version-specific claims.
- [ ] Keep technical correctness, code execution, CI/render, browser review and learner mastery as separate statuses.

The latest merge-commit CI/render evidence supersedes earlier comments that said final-revision workflows were unconfirmed. This does not close #82 or authorize work on later curriculum slices.
