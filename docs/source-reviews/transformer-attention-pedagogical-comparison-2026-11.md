# Comparative pedagogical audit: attention and Transformer explanations

**Review date:** 2026-11-09  
**Coordinator:** [LLM Lab #756](https://github.com/JM-Brun/llm-lab/issues/756)  
**Project owners:** [Jay Alammar #758](https://github.com/JM-Brun/llm-lab/issues/758), [3Blue1Brown #759](https://github.com/JM-Brun/llm-lab/issues/759), [Polo Club #762](https://github.com/JM-Brun/llm-lab/issues/762)

## 1. Purpose and review protocol

This review compares complementary teaching approaches for attention and Transformer models. It does not rank the projects globally. It distinguishes source-derived observations, code/paper inspection, and uncompleted validation.

Review depth is deliberately explicit:

| Work | Material inspected | Not yet inspected |
|---|---|---|
| Jay Alammar, *The Illustrated Transformer* | Full article text | Fresh asset-level rights review |
| Jay Alammar, *The Illustrated GPT-2* | Full article text via indexed page content | Fresh asset-level rights review |
| Jay Alammar / Maarten Grootendorst, *How Transformer LLMs Work* (2025) | Official course outline and course announcement | Full videos, code examples and quiz |
| 3Blue1Brown, *Attention in Transformers, step by step* (lesson by Grant Sanderson; text adaptation by Justin Sun) | Full text adaptation, lesson structure, embedded questions, YouTube description and timestamps | Independent audiovisual viewing and animation timing review |
| Polo Club, *Transformer Explainer* | CHI 2026 paper, README, MIT licence, selected Svelte components, sampling/data code and model metadata | Live browser testing, keyboard/mobile checks and numerical parity run |

A text adaptation is not equivalent to watching a video. Static source inspection is not equivalent to executing the deployed interactive tool.

## 2. Findings by pedagogical approach

### 2.1 Jay Alammar: visual decomposition and architecture bridge

**The Illustrated Transformer** provides a progressive visual zoom from the system architecture to token representations, attention and matrix operations. Its word/vector-to-matrix transition is useful for connecting a per-token explanation to tensor computation. The article primarily presents the original encoder–decoder translation architecture.

**The Illustrated GPT-2** is the more direct bridge to decoder-only autoregressive language modeling. Its walkthrough makes causal masking, head splitting, weighted value aggregation, concatenation, output projection, training/inference distinctions and key/value reuse visible.

Useful teaching patterns:
- show one-token/vector and whole-sequence/matrix views of the same operation;
- make architecture family and objective explicit before discussing a block;
- distinguish parallel training over positions from token-by-token autoregressive inference;
- disclose diagram simplifications and model-specific dimensions.

Qualifications:
- The original Transformer article is not a generic GPT architecture diagram. Its six layers, eight heads and dimensions are historical example values.
- GPT-2-era descriptions should not be silently generalized to current architectures.
- The article's cache explanation is an intuition, not a complete prefill/decode or per-layer cache specification.
- Do not reproduce the illustrations without asset-specific permission. Prefer original LLM Lab diagrams with explicit axes, tensor shapes and causal constraints.

### 2.2 3Blue1Brown: contextual intuition, matrix conventions and staged retrieval

The lesson begins with contextual ambiguity (the token “mole”) to motivate why an initial token embedding is insufficient. It frames attention as information transfer that updates a token's contextual representation, then progressively introduces Q, K, dot products, softmax, masking, V, multi-head attention and the output projection.

Distinctive contributions:
- contextual ambiguity before equations;
- geometric intuition for query-key dot products;
- staged explanation of attention scores, normalized weights and weighted value aggregation;
- embedded prediction/recall questions at conceptual transitions;
- a concrete bridge from the value map to a down/up factorization and shared multi-head output matrix;
- an explanation that one training sequence supplies next-token predictions for multiple prefix positions, motivating causal masking and parallel training.

The lesson uses a **column-vector convention**: Q/K vectors are columns and softmax is column-wise. This is explicitly contrasted with the row-vector convention used in the original paper and common implementations. LLM Lab uses row-wise softmax for Q/K matrices whose rows correspond to query positions. These are compatible conventions, not a contradiction; any cross-reference should show the transpose and normalization axis explicitly.

The public animation source repository contains a scene script for this lesson, `_2024/transformers/attention.py`. Static inspection of its scene classes reveals a deliberate visual sequence: contextualized token updates and a mystery-novel example; geometric Q/K projections into a smaller space; construction of the dot-product attention matrix and scaled-softmax equation; parallel next-token predictions and causal masking; context-size scaling; value aggregation and low-rank value-map factorization; cross-attention; multi-head attention; the shared output matrix; and GPU parallelizability. This code-level inspection clarifies the intended visual progression, but it does not replace watching the rendered video: pacing, animation legibility and the exact visual emphasis remain unreviewed.

Scientific qualifications:
- The noun/adjective attention-head example is explicitly hypothetical, not an interpretation of a trained head.
- The intuitive description of adding value vectors to embeddings is later refined by the factorized value map and shared output projection. Do not imply raw head output is simply added to the residual stream.
- GPT-3 parameter counts and head counts are model-specific historical examples.
- The lesson's training explanation is adjacent to teacher forcing and shifted targets, but it does not formally define teacher forcing, target shifting, loss reduction or parameter updates. LLM Lab should provide those definitions separately.

### 2.3 Polo Club: token-centric flow and interactive computation

The CHI 2026 paper describes a token-centric, Sankey-inspired flow visualization, consistent visual encoding, progressive expansion from overview to mathematical detail, learner-provided prompts, live GPT-2 inference, sampling controls and embedded guided-learning cards. The paper states a CC BY 4.0 licence; this does not remove the need to check any separately credited third-party asset. The repository software has a separate MIT licence.

The paper reports a 90-participant between-subjects study of motivated non-experts. Participants studied for up to 45 minutes and completed an immediate seven-question multiple-choice quiz aligned with six learning objectives. The baselines were Jay Alammar's *The Illustrated GPT-2* blog and the 3Blue1Brown video *But what is a GPT?* (not the specific attention lesson reviewed in §2.2).

Reported mean quiz accuracy was 73.3% for Transformer Explainer, 59.5% for the blog and 61.9% for the video. The paper reports pairwise advantages over both baselines (p = 0.021). The question-level improvement for attention was marginal (p = 0.056); architecture overview and output probabilities showed clearer advantages. MLP was the weakest learning objective and did not have a dedicated interactive feature.

The evidence is promising but bounded:
- one short controlled study with 90 non-expert participants;
- immediate post-study quiz, not long-term retention or transfer;
- seven multiple-choice questions;
- no detailed test of mathematical mechanism mastery;
- one blog and one video baseline;
- no advanced learner or from-scratch implementation-course comparison.

Selected code inspection found model metadata for GPT-2 small (default), medium and large; block/head navigation; QKV and attention matrix views; masked and softmaxed attention values; hoverable numerical cells; logits/probabilities; temperature and top-k/top-p controls; and an MLP view. These are static source observations, not confirmation of live deployment behavior.

### 2.4 Existing LLM Lab integration

LLM Lab already has a substantial bilingual Practice & experiment page:
- `site/fr/transformer-explainer.qmd`
- `site/en/transformer-explainer.qmd`

It already links the three architecture families to a live GPT-2 small experiment; includes controlled tests for causal-prefix invariance and temperature; distinguishes observation from computational evidence; maps interface components to the PyTorch reference model and ONNX execution path; and documents the demonstrator's top-p behavior over a 50-candidate truncated set.

The page pins repository commit `bfe50afba10b9b560b84143ee1107d977defa74f` (2026-06-06), which exists. The pinned source is useful for reproducible citations. Current-main code was sampled as a cross-check, but no live browser session was run in this review.

**Decision:** do not create another explainer page, duplicate experiments or add another visualization framework. The existing bilingual page is the integration destination. The CHI paper can be cited there with a short description of its study design and limitations, but learner benefit for LLM Lab itself must not be inferred from the external study.

### 2.5 Jay Alammar / Maarten Grootendorst: 2025 course

The official DeepLearning.AI outline describes 13 video lessons (~1h34), two code examples and a quiz. The sequence moves from bag-of-words and embeddings through attention, Transformer architecture, tokenizers, block/self-attention, a Hugging Face model example, recent improvements (KV cache, MQA, GQA, sparse attention) and MoE.

This is a concise intuition-to-current-architecture route, not a from-scratch implementation route. Its most distinctive candidate contributions are the current-architecture overview, modern attention/inference variants, and compact code-backed inspection of a recent Hugging Face model.

Only the outline and announcement were inspected. No claim is made about the correctness or depth of the individual videos or code examples.

### 2.6 3Blue1Brown: *But what is a GPT?* (Deep Learning Chapter 5)

This is the preceding lesson to the attention chapter and, importantly, the video used as the video baseline in the Polo Club CHI 2026 study. Its text adaptation was inspected, and the public animation source scripts for generation, embeddings, autoregression and machine-learning basics were sampled.

Its source-local progression is unusually relevant to LLM Lab's overall computational spine:
1. Predict, sample and repeat: input text produces a next-token distribution, a token is sampled, appended and the cycle repeats.
2. Tokens and embeddings: text is segmented into tokens and mapped to vectors.
3. Neural-network premise: learned weights, matrix operations, nonlinearities and data flow.
4. Embedding geometry: vector directions, dot products, nearest neighbors and illustrative semantic directions.
5. Contextualization: the same initial token representation is refined by context through repeated attention and MLP blocks.
6. Unembedding: the final sequence representation is projected to vocabulary logits.
7. Softmax and temperature: logits become a distribution used for sampling.
8. Parallel training intuition: every position can provide a next-token prediction during training, even though generation consumes the final position and then feeds the sampled token back.

The public scene scripts reinforce this structure:
- generation/autoregression scenes animate the predict → distribution → sample → append → repeat loop, including temperature examples and parallel next-token predictions;
- embedding scenes visualize token segmentation, embedding matrices, vector spaces, dot products and contextual updates;
- machine-learning scenes visualize weights versus data, matrix computations, softmax and the neural-network premise.

This offers a clear big-picture mental model and a useful bridge between the model's forward computation and autoregressive decoding. It is complementary to Chapter 6: Chapter 5 explains the end-to-end system; Chapter 6 opens the internal attention mechanism.

Qualifications:
- The vector arithmetic/nearest-neighbor examples are illustrative. The animation code uses a separate GloVe/word-vector model for some geometric demonstrations; these are not measurements of GPT-3 token embeddings.
- The lesson sometimes describes token embeddings as also carrying positional information. LLM Lab should distinguish the token-embedding lookup from positional embeddings/encodings and the combined input representation.
- GPT-3 parameter counts, vocabulary size and context length are historical model-specific examples.
- Temperature zero is best understood as the limit as temperature approaches zero from above; the formula is not evaluated by dividing by literal zero.
- The parallel next-token explanation motivates shifted targets and teacher-forced training, but does not fully define teacher forcing, target alignment, loss masking or gradient updates.

The text adaptation and scene source provide a substantial structural review, but the rendered video has not yet been independently watched. Pacing, animation timing, visual legibility and the exact transitions remain open.

## 3. Cross-project synthesis

These resources serve different learning needs:

| Learning need | Distinctive source contribution | LLM Lab destination |
|---|---|---|
| Motivate contextualization | 3Blue1Brown | Contextualized representations and attention introduction |
| Move from token vectors to matrix computation | Jay Alammar | Q/K/V and scaled dot-product attention |
| Make conventions and tensor shapes explicit | 3Blue1Brown's convention note, paired with LLM Lab's row-wise formulation | Q/K/V and scaled attention; only add a convention bridge if it resolves a demonstrated learner confusion |
| See architecture and information flow at multiple scales | Polo Club | Existing bilingual Transformer Explainer experiment page |
| Understand autoregressive generation and cache intuition | Illustrated GPT-2 and 2025 course | Generation, prefill/decode, KV-cache and inference-efficiency work |
| Explore contemporary attention variants | 2025 course outline | Coordinate with existing inference-efficiency and Hugging Face owners before deciding page placement |
| Practice retrieval and transfer | Embedded checks in 3Blue1Brown; guided learning in Polo Club | Existing Understand route and Practice & experiment activities |

The conceptual knowledge graph, computational dependencies and pedagogical sequence must remain separate but cross-linked. These resources do not justify forcing all attention-related concepts into one linear route.

## 4. Candidate concepts and existing ownership

The 2025 course names KV cache, MQA, GQA, sparse attention and MoE. The current learner-facing site tree inspected for this review does not show dedicated pages for these topics. That is a coverage signal, not yet a decision to create five pages.

Reuse existing owners:
- KV-cache/inference-efficiency source curation: [#266](https://github.com/JM-Brun/llm-lab/issues/266).
- Hugging Face implementation and documentation: [#765](https://github.com/JM-Brun/llm-lab/issues/765).
- Computational spine and prefill/teacher-forcing distinction: [#584](https://github.com/JM-Brun/llm-lab/issues/584) and [#576](https://github.com/JM-Brun/llm-lab/issues/576).
- Historical orientation: [#197](https://github.com/JM-Brun/llm-lab/issues/197).

MQA/GQA and sparse attention should first be compared as architectural variants within the existing attention material or a bounded Deepen destination. MoE needs a separate source-based scope decision; the course outline alone is insufficient evidence to write a lesson.

## 5. Decisions and remaining work

### Accepted
- Retain Jay Alammar, 3Blue1Brown and Polo Club as complementary references, each attached to a specific learning need.
- Adopt progressive visual zoom, a stable visual language, and short prediction checkpoints as reusable teaching patterns.
- Use the 2025 course as a candidate source for modern architecture extensions, subject to lesson/code inspection.
- Preserve original tensor conventions and explicit assumptions in LLM Lab.

### Deferred
- Full audiovisual review of the selected 3Blue1Brown lesson.
- Full review of Jay Alammar's 2025 course videos and code examples.
- Live browser, keyboard and mobile testing of Polo Club.
- Numerical parity checks against its pinned PyTorch/ONNX model path.
- Asset-specific rights review before any external illustration or screenshot reuse.
- Final placement decisions for MQA, GQA, sparse attention and MoE.

### Rejected for now
- Recreating a full Transformer Explainer in LLM Lab.
- Creating separate pages for every modern attention variant based solely on a course outline.
- Treating illustrative attention-head interpretations as factual descriptions of learned heads.
- Treating the Polo Club user study as evidence that LLM Lab's own pages improve learning outcomes.

## 6. Source and evidence references

- [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
- [Jay Alammar — The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/)
- [DeepLearning.AI — How Transformer LLMs Work](https://www.deeplearning.ai/courses/how-transformer-llms-work)
- [Jay Alammar — 2025 course announcement](https://newsletter.languagemodels.co/p/how-transformer-llms-work-free-course)
- [3Blue1Brown — But what is a GPT?](https://www.3blue1brown.com/lessons/gpt/)
- [3Blue1Brown — Attention in Transformers, step by step](https://www.3blue1brown.com/lessons/attention/)
- [3Blue1Brown — video and timestamps](https://www.youtube.com/watch?v=eMlx5fFNoYc)
- [3Blue1Brown — animation source code for Chapter 5](https://github.com/3b1b/videos/tree/master/_2024/transformers)
- [3Blue1Brown — animation source code for Chapter 6](https://github.com/3b1b/videos/blob/master/_2024/transformers/attention.py)
- [Polo Club — Transformer Explainer repository](https://github.com/poloclub/transformer-explainer)
- [Polo Club — CHI 2026 paper](https://doi.org/10.1145/3772318.3791725)
- [LLM Lab — existing bilingual experiment guide](../../site/fr/transformer-explainer.qmd)

