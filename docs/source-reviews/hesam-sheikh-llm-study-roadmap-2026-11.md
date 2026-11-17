# Source review — Hesam Sheikh, “How I Studied LLMs in Two Weeks: A Comprehensive Roadmap”

**Source ID:** hesam-sheikh-llm-study-roadmap-2024  
**Author:** Hesam Sheikh (also credited as Hesam Sheikh Hassani in the publisher's social post)  
**Publisher:** Towards Data Science / TDS Archive  
**Canonical URL:** https://towardsdatascience.com/how-i-studied-llms-in-two-weeks-a-comprehensive-roadmap-e8ac19667a31/  
**Review date:** 2026-11-17  
**Publication date:** 2024-10-18  
**Source type:** practitioner learning roadmap  
**Language:** English

## 1. Inspection scope and provenance

The canonical Towards Data Science URL blocks automated retrieval. The article body was reconstructed from the accessible TDS Archive/Medium friend-link page, a full text mirror on Indie Hackers, and the author's linked public GitHub repository. The publisher archive confirms the title, author, and date; the Indie Hackers copy exposes the article body and three named study stages.

| Component | Status | Evidence / limitation |
|---|---|---|
| Article text | Inspected via accessible mirror | Full body, headings, three stages, prerequisites and study advice visible |
| Canonical page | Inaccessible | TDS robots policy blocked retrieval; mirror used for text |
| Author attribution | Corroborated | Article byline and author's linked GitHub repository |
| Study-note PDFs | Identified, not inspected | Repository links to LLM-from-scratch, hallucination and edge-technique PDFs |
| Day-based study notes | Inspected | Repository README and daily READMEs for Days 003–016 inspected; embedded images and linked PDFs remain unaudited |
| Article images | Not visually inspected | Cover and embedded note illustrations were visible as image slots, but bytes were not retrieved |
| Comments | Partial | A small sample on mirrors; not treated as author claims |
| Rights | Unknown | Link-only; no licence or permission established |

The “two weeks” is a report of the author's personal study duration, not a validated estimate for beginners. The author says prior ML/LLM familiarity helped and that the same work could take more than a month. The article body presents three thematic stages; its linked repository supplies a more granular Day 003–016 study-note sequence. All daily README files for Days 003–016 were inspected; their sequence and stated durations are summarized below. Embedded images and linked PDFs remain outside the visual/content audit.

## 2. Reconstructed learning structure

The article groups the study into three stages:

1. **Build an LLM from scratch:** token and positional embeddings, self-attention, Transformer architecture, the original *Attention Is All You Need* paper, and basic fine-tuning. The author singles out understanding self-attention and the roles of Q, K and V as the main conceptual difficulty. Sebastian Raschka's *Build a Large Language Model (From Scratch)* is the central resource.
2. **Study hallucination:** positional bias, exposure bias, and contributions from data, training and inference. The author recommends studying mitigation as well as causes.
3. **Study techniques beyond basic attention:** pause tokens, Infini-attention, RoPE, KV cache and Mixture of Experts, then consolidate by reading Meta Llama's architecture and code.

The linked ML Retreat README maps LLM study notes across Day 003 through Day 016. I inspected the README for every day in that range. The resulting sequence is: Day 003 token and positional embeddings (7.5 h); Day 004 attention (duration unspecified); Day 005 attention/multi-head attention (3 h); Day 006 GPT and fine-tuning (5 h); Day 007 classification and instruction fine-tuning (4 h); Day 008 language modelling and an introduction to hallucination (6.5 h); Day 009 knowledge distillation (2 h); Day 010 hallucination, locality bias and exposure bias (5.5 h); Day 011 pause tokens, Infini-attention and bidirectional LMs (4.5 h); Day 012 RoPE and KV cache (4 h); Day 013 KV cache, MoE and Llama (6.5 h); Day 014 Vision Transformers (6 h); Day 015 LLMs and natural-language understanding (6 h); and Day 016 multimodal language models (7 h). These are author-reported estimates, not independently measured study times. The Day 003 README records Raschka Chapters 1–2, a Mistral tokenizer guide, a positional-encoding tutorial and explanatory videos. Across the daily notes, the author repeatedly warns that most images are from Raschka's book; no image assets are copied.

The resource strategy is plural: original research papers, survey papers, explanatory videos (especially Andrej Karpathy's language-model playlist), and a personal repository of notes. The prerequisites listed are linear algebra; probability/statistics and MLE; calculus and gradients; optimization including SGD and Adam; Python/NumPy/Pandas; a deep-learning framework; neural-network layers, activations, backpropagation and loss functions. CNNs are explicitly optional.

The study advice is more reusable than the two-week framing: adapt the route to prior knowledge and goals; do not treat a resource as mandatory cover-to-cover reading; formulate a question before reading and search for the relevant answer; enjoy the process rather than optimizing for a deadline.

## 3. Technical assessment and qualifications

1. **Self-attention and Q/K/V:** the source correctly identifies these as a conceptual bottleneck. Retain the mathematical account of projections, compatibility scores, normalization, weighted value aggregation, causal masking and tensor shapes. Q/K/V are not literal database fields or conscious token decisions.
2. **Hallucination is multi-causal:** data, training and inference are useful investigation dimensions, not an exhaustive causal taxonomy. Positional effects such as “lost in the middle” are task- and setup-dependent; they do not establish a universal rule that models simply prefer nearby tokens. Exposure bias concerns train/inference prefix-distribution mismatch and error propagation; it is not a complete explanation for factual hallucination. Distinguish factual errors, unsupported generation, prompt/context failures, retrieval failures and evaluation artefacts.
3. **Pause tokens:** describe the particular mechanism and training setup rather than saying a token inherently gives a model more thinking time. Extra computation depends on architecture, objective and inference procedure.
4. **Infini-attention:** it is a specific long-context mechanism combining local attention with compressive memory, not a generic explanation of million-token context windows. A provider's advertised context length does not establish use of Infini-attention.
5. **RoPE:** describe the rotary transformation of query/key representations that encodes relative-position information in attention scores; keep variants and context-extension methods distinct.
6. **KV cache:** cache reuse avoids recomputing prior keys/values during autoregressive decoding, trading memory for reduced repeated computation. Size and benefit depend on layers, heads, dimensions, sequence length, batch and cache strategy.
7. **MoE:** experts are sub-networks within a sparse model, selected by routing; this is not simply “several smaller LLMs” combined. Keep total parameters, active parameters per token, routing, communication and load balancing distinct. The article's Mistral/Llama comparison is historical and task-specific, not a general guarantee.
8. **Llama as consolidation:** inspecting a concrete implementation is a good synthesis activity, but one model family cannot represent all Transformer/LLM designs. Pin the model/version and distinguish architecture from implementation choices.

## 4. Relationship to LLM Lab

The source is a **complementary study-design reference**, not a replacement curriculum. LLM Lab deliberately separates Understand (conceptual progression), Build (implementation dependency order), Deepen (optional detail), and Practice & experiment (activities and evidence). The article's broad “build from scratch” theme must not collapse these into one linear curriculum.

Its broad prerequisites should not become a blanket gate: LLM Lab introduces mathematics and tensor conventions where needed and keeps advanced depth optional. A learner can start with the inference mental model without first mastering all optimization mathematics or a deep-learning framework.

| Article topic | Existing LLM Lab destination |
|---|---|
| Tokens and embeddings | text-data, tokenization-strategies, embedding-space |
| Positional embeddings and RoPE | positional-encoding and Deepen material |
| Self-attention, Q/K/V and Transformer | queries-keys-values, scaled-dot-product-attention, causal-masking, transformer |
| Fine-tuning | post-training; Build adaptation branch for implementation |
| Hallucination and context failures | generation, context engineering, RAG/memory boundaries, evaluation/error analysis |
| KV cache and inference efficiency | generation and inference-efficiency deep dives |
| MoE and Infini-attention | optional architecture deepening; no core lesson without a defined learner outcome |
| Llama code study | optional comparative reading, not the project's reference implementation |

The source adds a useful **meta-learning practice**: question-led, selective reading and adaptive pacing. This can inform learner guidance, but it does not justify a new canonical route node or duplicate lesson.

## 5. Disposition

**Decision: integrate by reference as a roadmap and study-method resource; do not import its sequence as the LLM Lab curriculum.**

- Preserve the three-stage outline and topics in the source-local extraction.
- Link to the article and author's ml-retreat repository as optional further study.
- Keep the two independent Understand and Build pathways and their evidence gates.
- Do not present the sequence as a validated 14-day curriculum; Days 003–016 have now been inspected, but the author's prior experience and self-reported durations make the schedule non-generalizable.
- Do not reproduce the article's diagrams or linked PDF notes. Day 003 explicitly attributes most of its images to Raschka's book; inspect assets and rights separately before visual integration.
- Revisit the remaining daily notes and three study-note PDFs; they may add concrete explanations or diagrams beyond the article.


## 6. Inspection of the linked Day 003–016 study journal

The daily READMEs add important content that the article's three-stage summary compresses or omits:

| Day | Topic and inspected resource trail | Estimated time |
|---|---|---:|
| 003 | Tokens and positional embeddings; Raschka Chapters 1–2, Mistral tokenizer guide, positional-encoding tutorial and videos | 7.5 h |
| 004 | Attention; start of Raschka Chapter 3, *Attention Is All You Need*, visual Transformer/attention videos | Not stated |
| 005 | Attention; finish Chapter 3, start Chapter 4, multi-head attention video | 3 h |
| 006 | GPT and fine-tuning; Raschka Chapters 4–5, start Chapter 6 | 5 h |
| 007 | Classification and instruction fine-tuning; finish Raschka Chapters 6–7 | 4 h |
| 008 | Language modelling and hallucination introduction; Karpathy's makemore videos and *Hallucination is Inevitable* | 6.5 h |
| 009 | Knowledge distillation; survey of LLM knowledge distillation | 2 h |
| 010 | Hallucination; survey, locality bias, softmax bottleneck and exposure bias | 5.5 h |
| 011 | Pause tokens, Infini-attention and bidirectional LMs; pause-token and Infini-attention papers, *Meet in the Middle* | 4.5 h |
| 012 | RoPE and KV cache; original RoFormer paper and explanatory videos | 4 h |
| 013 | KV cache, MoE and Llama; Mixtral resources and Llama architecture walkthrough | 6.5 h |
| 014 | Vision Transformers; original ViT paper, explanations and PyTorch implementation resource | 6 h |
| 015 | LLM and natural-language understanding; world-model probing, arguments about form/meaning and Chinese Room | 6 h |
| 016 | Multimodal LMs; multimodality survey resources and GPT-2 reproduction video | 7 h |

The sum of the 13 stated estimates (excluding Day 004) is 67 hours. This is arithmetic over the author's estimates, not a verified workload or proof that the sequence can be completed in two weeks. It also does not include unreported time for exercises, breaks or implementation.

### 6.1 Additional topics worth retaining

- **Knowledge distillation:** this is a distinct compression/transfer learning topic, not merely another fine-tuning variant. The daily note points to the 2024 survey *A Survey on Knowledge Distillation of Large Language Models* (arXiv:2402.13116). LLM Lab should cross-link to its existing compression and post-training coverage rather than create a new core lesson solely from this roadmap.
- **Locality bias and softmax bottleneck:** Day 010 broadens the hallucination study beyond the article's brief positional/exposure-bias labels. Keep these as separate mechanisms/questions; do not collapse locality bias into the “lost in the middle” phenomenon or treat any one as a universal hallucination cause.
- **Pause tokens and bidirectional LMs:** Day 011 includes *Think before you speak: Training Language Models With Pause Tokens*, *Meet in the Middle: A New Pre-training Paradigm*, and the Infini-attention paper. These represent different research questions (extra computation, bidirectional pretraining, and long-context memory) and should not be grouped as one technique.
- **RoPE and KV cache:** Day 012 connects position representation with inference memory. They interact in deployed decoder architectures but solve different problems; the cache is not a positional encoding.
- **Natural-language understanding and grounding:** Day 015 juxtaposes a synthetic world-model probing paper, a critical form-versus-meaning paper, and the Chinese Room argument. These are research and philosophical perspectives, not a settled empirical demonstration that LLMs either do or do not understand language. Separate operational capabilities, grounded reference, semantic generalization and philosophical criteria.
- **Vision and multimodality:** Days 014–016 widen the route beyond text-only LLMs. ViT is a Transformer applied to image patches; multimodal language models add modality-specific encoders/token pathways and alignment or fusion mechanisms. Do not imply all multimodal models use the same architecture.

### 6.2 Selected primary and survey resources linked by the author

- Vaswani et al., *Attention Is All You Need*: https://arxiv.org/abs/1706.03762
- *A Survey on Knowledge Distillation of Large Language Models*: https://arxiv.org/abs/2402.13116
- *Hallucination is Inevitable: An Innate Limitation of Large Language Models*: https://arxiv.org/abs/2401.11817
- *A Survey on Hallucination in Large Language Models*: https://arxiv.org/abs/2311.05232
- *Think before you speak: Training Language Models With Pause Tokens*: https://arxiv.org/abs/2310.02226
- *Meet in the Middle: A New Pre-training Paradigm*: https://arxiv.org/abs/2303.07295
- *Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention*: https://arxiv.org/abs/2404.07143
- *RoFormer: Enhanced Transformer with Rotary Position Embedding*: https://arxiv.org/abs/2104.09864
- *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*: https://arxiv.org/abs/2010.11929
- *Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task*: https://arxiv.org/abs/2210.13382
- *Climbing towards NLU: On Meaning, Form, and Understanding in the Age of Data*: https://aclanthology.org/2020.acl-main.463/
- *Provable Limitations of Acquiring Meaning from Ungrounded Form*: https://arxiv.org/abs/2104.10809

### 6.3 Scope and visual-asset boundary

The daily README files were read, but their referenced JPG/PNG assets were not retrieved as bytes and were not visually inspected. The three overview PDFs in the repository root were identified but not downloaded or parsed. The daily notes repeatedly attribute most illustrations to Sebastian Raschka's book; Day 004 and Day 005 say this explicitly. The article/repository's image slots therefore remain **not visually audited**, and no image is reused or redrawn from an unseen asset. The next visual pass must inspect exact image bytes and distinguish original author-created annotations from book-derived figures before considering a new project-owned flashcard or diagram.
