# Annotated references

> **Catalogue boundary:** this page is the reader-maintained annotated bibliography. It is not a scan inventory. The canonical machine-readable source records, classification, scan scope/status and provenance live in [the source catalogue](../data/sources.yml), governed by [the source catalogue schema](source-catalogue-schema.md). A reference listed here is not automatically a source that has been scanned.


The repository is an independent learning and experimentation project. These sources are used for study and comparison; their code, text, datasets, figures, and model weights retain their own licenses and terms. An accessible URL does not automatically grant permission to copy or redistribute content.

## Visual explanations of GPT and Transformers

1. **Jay Alammar — The Illustrated GPT-2**
   - Article: https://jalammar.github.io/illustrated-gpt2/
   - Decoder-stack figure embedded by remote URL: https://jalammar.github.io/images/gpt2/gpt2-transformer-block-vectors-2.png
   - Causal training-window figure embedded by remote URL: https://jalammar.github.io/images/gpt2/transformer-decoder-attention-mask-dataset.png
   - **Use for:** visualizing decoder-only Transformer blocks, token embeddings, autoregressive generation, Q/K/V, and causal masking.
   - **Attribution and reuse:** the Quarto pages credit Jay Alammar directly below each figure and link to the original article. The files are not copied into this repository. Check the author's terms or request permission before separate redistribution or modification.

2. **Sara Ravi — GPT-2 Architecture Demystified: A Step-by-Step Breakdown**
   - Article: https://sararavi14.medium.com/gpt-2-architecture-demystified-a-step-by-step-breakdown-74b1c5c80d17
   - **Use for:** a second step-by-step explanation of the GPT-2 architecture.
   - **Attribution and reuse:** linked as a source rather than copying its illustrations. Verify the rights for individual figures before reuse.

3. **3Blue1Brown — Transformers, the tech behind LLMs**
   - Lesson: https://www.3blue1brown.com/lessons/gpt/
   - Content and reuse guidance: https://www.3blue1brown.com/about/
   - **Use for:** animated intuition for embeddings, attention, and Transformer language models.
   - **Attribution and reuse:** this repository links to the original lesson and does not republish its video or screenshots. Follow the creator's stated conditions for any still images or excerpts, including visible attribution and applicable duration limits.

## Main from-scratch path

4. **Sebastian Raschka — LLMs from Scratch**
   - Repository: https://github.com/rasbt/LLMs-from-scratch
   - Companion guide: https://sebastianraschka.com/llms-from-scratch/
   - Book: https://www.manning.com/books/build-a-large-language-model-from-scratch
   - **Use for:** a coherent end-to-end implementation path from tokenization and attention through GPT pre-training and fine-tuning.
   - **How this lab complements it:** stronger emphasis on numerical tests, controlled comparisons, reproducibility, failure analysis, and compute-aware trade-offs. Do not copy code without preserving attribution and checking its license.

5. **Build a Large Language Model (From Scratch), French-language resources**
   - Interactive learning site: https://www.llmdezero.com/
   - Companion repository: https://github.com/kevindegila/construire-un-llm-de-zero
   - Book overview: https://ayinedjimi-consultants.fr/ouvrages/construire-llm-from-scratch-fr
   - **Use for:** a second explanation in French and visual intuition. Treat implementation details as claims to verify against primary papers, framework documentation, and tests.

## Positional encodings

- **Sebastian Raschka — Understanding Positional Embeddings in Modern LLMs** (15 November 2026): https://magazine.sebastianraschka.com/p/understanding-positional-embeddings
  - **Use for:** visual and mathematical walkthrough from learned absolute and sinusoidal vectors to RoPE, including PyTorch conventions, partial RoPE, NoPE and learned relative-position bias.
  - **How this lab uses it:** as an advanced companion to the existing bilingual positional-encoding and RoPE lessons. See [the source review](source-reviews/raschka-positional-embeddings-2026-11.md). Figures and code remain link-only.


- **Vaswani et al. — Attention Is All You Need** (2017), section 3.5: https://arxiv.org/abs/1706.03762
  - **Use for:** primary formulation of sinusoidal positional encodings, frequency schedule, wavelength range, and fixed-offset motivation.
- **Jay Alammar — The Illustrated Transformer**: https://jalammar.github.io/illustrated-transformer/
  - **Use for:** visual intuition for positional vectors and the position-by-dimension matrix. Its July 2020 clarification distinguishes the earlier concatenated illustration from the interleaved formula in the original paper.
- **Harvard NLP — The Annotated Transformer**: https://nlp.seas.harvard.edu/annotated-transformer/
  - **Use for:** annotated PyTorch implementation connecting the equations to a precomputed buffer and input addition.
- **Stanford EE269 — Transformers for Signal Prediction**: https://web.stanford.edu/class/ee269/Lecture_Transformers.pdf
  - **Use for:** a signal-processing interpretation of angular frequency, wavelength, and logarithmically spaced positional scales.

See the [source review and pedagogical synthesis](source-reviews/sinusoidal-positional-encoding-2026-11.md) for inspection scope, technical reconciliation, and reuse limits. The machine-readable scan records remain in [the source catalogue](../data/sources.yml).

- **Khan et al. — Fractional Rotation, Full Potential? Investigating Performance and Convergence of Partial RoPE** (arXiv:2603.11611, v2, 15 October 2026): https://arxiv.org/abs/2603.11611
  - **Use for:** experimental evidence on partial-RoPE fractions, training convergence, NoPE instability and the memory footprint of precomputed RoPE tables.
  - **Qualification:** the up-to-10× saving concerns the RoPE sine/cosine cache, not the KV cache; results are bounded to the paper's 1B/8B configurations, data, sequence lengths and evaluation suite. See [the source review](source-reviews/partial-rope-fractional-rotation-2026-11.md).

## Q/K/V and attention perspectives

- **Neha KK — Understanding Queries, Keys and Values in Transformers** (Medium, 31 December 2025): https://medium.com/@nkk18072004/understanding-queries-keys-and-values-in-transformers-149ed07c9f8b
  - **Use for:** a concise introductory database-search analogy, an explicit motivation for separating Q/K matching from V payload, and a pronoun-context illustration.
  - **Review status:** text reconstructed from an indexed search result; direct page HTML, four in-body image slots, comments and figure rights remain unverified. See [the source review](source-reviews/qkv-neha-kk-medium-2026-11.md). The figures are not reused.
- **Nishanthan K — How Query, Key, and Value (QKV) Work in Transformers**: https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a
  - **Use for:** a complementary Q/K/V explanation and source comparison; see [the QKV synthesis dossier](source-reviews/qkv-learning-graph-comparison-2026-11.md).

## Practical model training

6. **Hugging Face LLM Course**
   - French course: https://huggingface.co/learn/llm-course/fr
   - English course: https://huggingface.co/learn/llm-course/en
   - **Use for:** tokenizers, datasets, Transformers, model fine-tuning, and the practical Hugging Face ecosystem. Course chapters and library APIs evolve; check the current docs for version-specific behavior.

7. **PyTorch Transformer building blocks**
   - Tutorial: https://docs.pytorch.org/tutorials/intermediate/transformer_building_blocks.html
   - Scaled dot-product attention tutorial: https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial
   - **Use for:** comparing readable reference implementations with framework primitives and optimized attention paths. Benchmark on the target hardware rather than assuming a kernel is faster in every configuration.

8. **EleutherAI Language Model Evaluation Harness**
   - Repository: https://github.com/EleutherAI/lm-evaluation-harness
   - **Use for:** understanding standardized evaluation tasks and reproducible benchmark execution. Benchmark scores still depend on task versions, prompts, model/tokenizer details, and evaluation configuration.

9. **Cameron R. Wolfe — Language Model Training and Inference: From Concept to Code** (Deep (Learning) Focus, 4 September 2023): https://cameronrwolfe.substack.com/p/language-model-training-and-inference
   - **Use for:** a conceptual-to-code walkthrough connecting causal next-token prediction in pretraining and autoregressive inference, plus a NanoGPT/PyTorch example of forward passes, cross-entropy, and practical training infrastructure.
   - **Limitations:** GPT-2/NanoGPT-specific and dated implementation context; not a current training recipe or evidence of LLM Lab implementation. See the [source comparison dossier](source-reviews/language-model-training-inference-cameron-wolfe-2026-11.md). Figures and code are linked only; reuse rights were not established.

## Additional perspectives

9. **Giles Thomas — LLM from scratch**
   - https://www.gilesthomas.com/llm-from-scratch
   - **Use for:** an additional implementation-oriented walkthrough; cross-check assumptions and code against maintained libraries.

10. **AlgoMonster — LLM course introduction**
    - https://algo.monster/courses/llm/llm_course_introduction
    - **Use for:** a structured overview and a potential supplement to the main path. Confirm current coverage and access requirements before relying on it as a primary resource.

11. **LocalLLaMA community discussion**
    - https://www.reddit.com/r/LocalLLaMA/comments/1mq5qw5/learn_how_to_build_an_llm_from_scratch_step_by/
    - **Use for:** practical questions and community perspectives, not as the sole authority for implementation or scientific claims.

12. **Medium walkthrough**
    - https://medium.com/@raufpokemon00/building-a-large-language-model-llm-from-scratch-61fed0570ea5
    - **Use for:** an alternative explanation. Validate technical claims and code against primary sources and runnable tests.

13. **Design principles for LLM-based systems with zero trust**
    - https://cyber.sites.beta.gouv.fr/nous-connaitre/publications/publications-internationales/design-principles-for-llm-based-systems-with-zero-trust/
    - **Use for:** a security perspective for later system-level experiments. Model construction and application security are related but distinct topics.


## Embedding primers and visual explorations

- **Hesam Sheikh Hessani — LLM Embeddings Explained: A Visual and Intuitive Guide** (Hugging Face Space, 2025): https://huggingface.co/spaces/hesamation/primer-llm-embedding
  - **Use for:** an introductory visual tour from TF-IDF and Word2Vec to BERT and modern LLM input embeddings, with an interactive nearest-token atlas for the input embedding table of DeepSeek-R1-Distill-Qwen-1.5B. The author's companion code is in [LLM Mechanics](https://github.com/hesamsheikh/llm-mechanics).
  - **Relationship to LLM Lab:** the token-ID lookup and initial-versus-contextualized distinction are already covered in the bilingual [embedding-space lessons](../site/fr/embedding-space.qmd) / [English version](../site/en/embedding-space.qmd). Treat the atlas as an optional real-model visual companion, not a duplicate explanation or a sentence-embedding benchmark.
  - **Review status:** complete article text inspected on 10 November 2026; interactive runtime, companion code, image assets and reuse rights not audited. The TF-IDF dimensionality and embedding-dimension claims need qualification. See the [source review](source-reviews/hesam-sheikh-hessani-llm-embeddings-explained-2026-11.md).

## Research notes on embedding geometry

These papers underpin the bilingual critical notes in the Quarto site. Treat each conclusion within its stated assumptions, models, tasks, and evaluation protocol.

- **Cosine similarity and embedding geometry:** Steck, Ekanadham & Kallus, [*Is Cosine-Similarity of Embeddings Really About Similarity?*](https://arxiv.org/abs/2403.05440); Ethayarajh, [*How Contextual are Contextualized Word Representations?*](https://arxiv.org/abs/1909.00512); Nastase & Merlo, [*Testing the assumptions about the geometry of sentence embedding spaces*](https://arxiv.org/abs/2509.01606); Zhelezniak et al., [*Correlation Coefficients and Semantic Textual Similarity*](https://arxiv.org/abs/1905.07790).
- **Linearity and multidimensional features:** Park, Choe & Veitch, [*The Linear Representation Hypothesis and the Geometry of Large Language Models*](https://arxiv.org/abs/2311.03658); Engels et al., [*Not All Language Model Features Are One-Dimensionally Linear*](https://arxiv.org/abs/2405.14860); Tiblias et al., [*Shape Happens*](https://arxiv.org/html/2510.01025v1); Elhage et al., [*Toy Models of Superposition*](https://transformer-circuits.pub/2022/toy_model/).
- **Probe evaluation:** Hewitt & Liang, [*Designing and Interpreting Probes with Control Tasks*](https://aclanthology.org/D19-1275/); Barin-Pacela et al., [*Stop Probing, Start Coding*](https://proceedings.mlr.press/v337/barin-pacela26a.html).

Read the corresponding [cosine-similarity note](../site/fr/cosine-similarity.qmd) and [linearity note](../site/fr/linearite-embeddings.qmd) for assumptions, counterexamples, and suggested reproducible tests. The bibliography is a starting point; a citation does not by itself establish that every claim has been independently reproduced in this repository.

## How references and illustrations should be used

- Prefer original papers, official framework documentation, and maintained source repositories for technical claims.
- For each external figure, credit the creator near the figure and provide a direct link to the original source and, where known, the licence.
- Embed from the creator's source rather than storing a copy when permission to redistribute is unclear; remote embedding is not a substitute for checking applicable terms.
- Record the date/version consulted when an API or benchmark can change.
- Cite upstream work in reports and notebook introductions.
- Do not treat a tutorial's results as independently reproduced until the experiment has been run and checked here.
- Review licenses before reusing code, figures, datasets, model weights, or substantial text.


## Chapter-by-chapter study resources for Raschka's book

Use these resources as complementary explanations and study aids, not as substitutes for the book's formal definitions, primary papers, official documentation, or tests. Their content may change; verify details before relying on them for a technical claim.

11. **Sebastian Raschka — reading and study method**
    - Article: https://sebastianraschka.com/blog/2025/reading-books.html
    - Book companion hub and chapter map: https://sebastianraschka.com/llms-from-scratch/
    - **Use for:** a reading-first workflow: read a chapter for context, use videos as a second explanation, work through the source code, then attempt the chapter exercises before checking solutions.

12. **Sebastian Raschka — Build a Large Language Model (From Scratch)**
    - Publisher/book page: https://www.manning.com/books/build-a-large-language-model-from-scratch
    - Official companion repository: https://github.com/rasbt/LLMs-from-scratch
    - Chapter-by-chapter video playlist: https://www.youtube.com/playlist?list=PLQRyiBCWmqp5twpd8Izmaxu5XRkxd5yC-
    - Additional video supplied for this course: https://www.youtube.com/watch?v=kPGTx4wcm_w
    - **Use for:** the primary chapter sequence (Chapters 1–7), source-code reference, and an optional second explanation. The book is the scope baseline, not text or exercises to reproduce. Confirm the exact title and topic of individual videos before citing them for specific claims.

13. **Solomon Eshun — Building LLMs From Scratch, Part 2: Tokenization**
    - Article: https://soloshun.medium.com/building-llms-from-scratch-part-2-tokenization-e0bf05d24094
    - **Use for:** an accessible secondary explanation of word-, character-, and subword-tokenization trade-offs, special tokens, BPE, and the use of a pretrained tokenizer. Cross-check BPE details and implementation behavior against the official tokenizer documentation and Raschka's chapter/repository; this article is pedagogical, not a primary specification.

14. **AlgoMonster — LLM course introduction**
    - Course page: https://algo.monster/courses/llm/llm_course_introduction
    - **Use for:** an optional alternative course structure or recap. Review current contents and access requirements before assigning it to a specific chapter; it does not define the canonical LLM Lab sequence.

15. **Third-party PDF mirror of the Raschka book — provenance not verified**
    - URL supplied for review: https://dl.tehrandata.org/book/Build-a-large-language-models.pdf
    - **Use policy:** do not treat this mirror as the canonical edition, redistribute it, or assume it is authorized. Prefer the publisher page and the author's official repository/video materials. This reference is recorded for provenance transparency only; no copied book text, figures, or exercises should enter LLM Lab.



## Visual learning tools and interactive references

These resources are curated for teaching design and guided experimentation. Inclusion here means they are useful candidates, not that every claim, figure, or licence has been fully audited. See the [focused review and integration map](source-reviews/visual-learning-resources-2026-11.md).

- **Polo Club — Transformer Explainer**: https://poloclub.github.io/transformer-explainer/ ; research: https://research.ibm.com/publications/transformer-explainer-learning-llm-transformers-with-interactive-visual-explanation-and-experimentation
  - Use for live GPT-2 inference, token-level input, attention/MLP flow, next-token probabilities, and sampling experiments. Boundary: a specific GPT-2 implementation, not a universal architecture.
- **Brendan Bycroft — LLM Visualization**: https://bbycroft.net/llm
  - Use for 3D inspection of components, layers, weights, activations, and tensor flow. Boundary: selected GPT-style models; diagram proportions are not universal.
- **3Blue1Brown — GPT and Attention**: https://www.3blue1brown.com/lessons/gpt/ ; https://www.3blue1brown.com/lessons/attention/
  - Use for visual intuition. Boundary: pair animations with formal notation and numerical checks.
- **TensorFlow Playground**: https://playground.tensorflow.org/
  - Use for small-network experiments on optimization, regularization and overfitting. Boundary: not a Transformer or LLM simulator.
- **Sebastian Raschka — A Visual Guide to Attention Variants**: https://magazine.sebastianraschka.com/p/visual-attention-variants
  - Use for MHA, MQA, GQA, MLA, sliding-window and sparse attention. Boundary: evolving survey, not a controlled benchmark.
- **Maarten Grootendorst — A Visual Guide to Mixture of Experts**: https://www.maartengrootendorst.com/blog/moe/
  - Use for experts, sparse layers, router selection, capacity and load balancing. Boundary: keep active versus total parameters distinct.
- **Modular — LLM Inference Handbook**: https://handbook.modular.com/
  - Use for request lifecycle, prefill/decode, KV cache, latency, batching, GPU memory and serving. Boundary: living engineering documentation; product/performance guidance is version-dependent.
- **Neuronpedia**: https://www.neuronpedia.org/ ; [SAE overview](https://docs.neuronpedia.org/sparse-autoencoders/overview), [feature dashboards](https://docs.neuronpedia.org/sparse-autoencoders/feature-dashboards), [auto-interpretability](https://docs.neuronpedia.org/sparse-autoencoders/auto-interp), [API](https://docs.neuronpedia.org/api/)
  - Use for inspecting feature activations, logits, density, model-generated explanations, custom-text tests and attribution tools. Boundary: explanations and scores are fallible; source/model/layer matter; activations and steering are not causal proof.
- **Apple — Embedding Atlas**: https://apple.github.io/embedding-atlas/ ; [overview](https://apple.github.io/embedding-atlas/overview.html), [CLI guide](https://apple.github.io/embedding-atlas/tool.html), [research paper](https://machinelearning.apple.com/research/embedding-atlas)
  - Use for large embedding projections, nearest-neighbour search, density-based clustering, labels and metadata cross-filtering. Boundary: projections and clustering can distort apparent structure; record dataset, model, metric and settings.

## Inference performance and generation systems

- **Sebastian Raschka — “From Full to Hybrid Attention in LLMs”** (LinkedIn post and author companion article, 10 November 2026):
  - Post: https://www.linkedin.com/posts/sebastianraschka_currently-working-towards-a-bigger-open-llm-share-7525958627799695361-Hprj/
  - Companion article: https://sebastianraschka.com/blog/2026/full-to-hybrid-attention.html
  - **Use for:** a dated snapshot of dense-global versus hybrid attention patterns in the author's selected open-model sample, and a taxonomy that distinguishes sparse/local attention from recurrent-state mechanisms.
  - **Interpretation and reuse:** the reported 50/50 split is sample-specific and has not been independently audited; it is not a market census or a performance benchmark. The article's figures are linked, not copied. See [the source review](source-reviews/raschka-full-to-hybrid-attention-2026-11.md).


- **Brij Pandey — “You ask LLM a question. It pauses. Then the answer starts appearing, piece by piece.”** (LinkedIn post, 10 November 2026): https://www.linkedin.com/posts/brijpandeyji_you-ask-llm-a-question-it-pauses-then-share-7525787285829804032-YNEl
  - **Use for:** a compact end-to-end inference diagram connecting tokenization, embeddings, decoder layers, KV caching, next-token selection, streaming, TTFT/ITL diagnostics, and speculative decoding.
  - **Integration:** used as a secondary pedagogical overview in the bilingual generation lesson to motivate prefill/decode latency, KV-cache memory growth, and the distinction between first-token latency and inter-token latency. Technical details are qualified against the model architecture and serving configuration; the LinkedIn figure is linked, not copied.
  - **Review status:** post text and supplied diagram inspected on 10 November 2026. This is a pedagogical secondary source, not an implementation specification or benchmark. See [the source review](source-reviews/linkedin-inference-generation-2026-11.md).

## Joint embeddings and cross-modal representation alignment

- **Mayank Kejriwal — Do AI models trained on different modalities converge to the same representation of the world?** (AI Scientist, 8 November 2026): https://aiscientist.substack.com/p/do-ai-models-trained-on-different
  - **Use for:** an accessible synthesis of the Platonic Representation Hypothesis, good-view versus bad-view JEPA training, the conditional convergence theorem, cross-modal alignment experiments, and their limitations.
  - **Primary research:** Balestriero & LeCun, [*Proving and Improving the Platonic Representation Hypothesis with JEPAs*](https://arxiv.org/abs/2610.39302), arXiv:2610.39302 (2026).
  - **Review status:** first-pass extraction recorded in `data/extractions/ai-scientist-platonic-representation-jepa-2026.yml` and `data/extractions/balestriero-lecun-platonic-representation-jepas-2026.yml`; the primary paper's proof appendices and experimental sections still require full audit. See [the source review](source-reviews/platonic-representation-jepa-2026-11.md). Treat reported alignment scores and sample-efficiency comparisons as author-reported, task-specific results, not independent reproductions or general-intelligence evidence.


- **Eleventh Hour Enthusiast — Proving and Improving the Platonic Representation Hypothesis with JEPAs** (Medium, full article inspected 10 November 2026): https://medium.com/@EleventhHourEnthusiast/proving-and-improving-the-platonic-representation-hypothesis-with-jepas-80a88aa3766d
  - **Use for:** a worked derivation from positive-pair probabilities to the graph Laplacian, normalized adjacency, whitened spectral optimization and eigengap condition. Its four-state cycle is particularly useful for teaching why a tied eigenvalue at the dimensionality boundary can yield different optimal geometries.
  - **Relationship to the other sources:** a pedagogical secondary explanation of arXiv:2610.39302, not an independent proof or independent experimental replication. The article explicitly distinguishes its second-order spectral proof from the LeJEPA/SIGReg experiments.
  - **Review status:** full body ingested in `data/extractions/eleventh-hour-enthusiast-platonic-representation-jepa-2026.yml`; figures were not downloaded and reuse rights are unknown.

- **Hugging Face Papers — arXiv:2610.39302 record:** https://huggingface.co/papers/2610.39302
  - **Use for:** an alternate discovery/access page for the same Balestriero–LeCun paper, including its abstract, author-submitted summary and discussion. This is not a separate research publication and is not counted as an additional independent source.
  - **Figure locator supplied for review:** https://huggingface.co/papers/2610.39302?image-viewer=7E717904F1535C836EA2DEC65DD6993C6356BA9A
  - **Reuse caution:** the viewer URL identifies a hosted figure asset, but asset provenance and reuse permission were not established. Link to it rather than copying it until rights are checked.

- **Randall Balestriero & Yann LeCun — Contrastive and Non-Contrastive Self-Supervised Learning Recover Global and Local Spectral Embedding Methods** (arXiv:2205.11508v3, 2022; also in the NeurIPS 2022 proceedings): https://arxiv.org/abs/2205.11508
  - **Use for:** the single-encoder spectral lineage behind the Platonic Representation Theorem's mechanism: VICReg's invariance term is the Dirichlet energy of the embedding on the pairwise-similarity graph, the constrained VICReg problem recovers (kernel) Laplacian Eigenmaps, the linear-network regime recovers Locality Preserving Projections and Linear Discriminant Analysis, and contrastive versus non-contrastive SSL corresponds to global versus local spectral embedding.
  - **Relationship to the other sources:** direct primary precedent for the spectral machinery of arXiv:2610.39302 (positive-pair kernel, eigenspace selection); the 2026 theorem extends this analysis to agreement between separately trained encoders. The Medium article's lineage sentence cites this paper.
  - **Review status:** first-pass extraction recorded in `data/extractions/balestriero-lecun-contrastive-non-contrastive-ssl-spectral-2022.yml`; the arXiv HTML was retrieved but read selectively, and the theorems' proofs and experiments remain unaudited. See [the source review](source-reviews/platonic-representation-jepa-2026-11.md).

- **YouTube video — video ID `j0O8Aq6ducw`:** https://www.youtube.com/watch?v=j0O8Aq6ducw
  - **Review status:** URL recorded at the user's request. YouTube watch-page and oEmbed metadata could not be retrieved in this pass; title, creator, transcript, date and contents remain unverified. Do not use it as evidence until inspected.


## Historical reading roadmaps

- **Sebastian Raschka — [Understanding Large Language Models: A Cross-Section of the Most Relevant Literature To Get Up to Speed](https://magazine.sebastianraschka.com/p/understanding-large-language-models)** (16 April 2023).
  - **Use for:** a curated historical route through foundational attention and Transformer papers, model-family objectives, scaling and efficiency, parameter-efficient fine-tuning, and early instruction-following/alignment literature.
  - **Scope:** this is a selective 2023 reading guide, not a systematic review or a current ranking. Its paper summaries are secondary pointers; consult the primary papers for technical claims and current sources for developments after April 2023.
  - **Project review:** [source review](source-reviews/raschka-understanding-large-language-models-2023.md); canonical scan and provenance are recorded in [the source catalogue](../data/sources.yml).

## Roadmap-oriented and practitioner-focused LLM courses

**Maxime Labonne — LLM Course**
- Repository: https://github.com/mlabonne/llm-course
- **Use for:** a broad, roadmap-oriented map of LLM foundations, model-scientist topics (architecture, pre-training, post-training, evaluation, quantization and merging), and LLM-engineering topics (running models, prompting, RAG, agents, optimization, deployment and security), with links to practical articles and notebooks.
- **How this lab complements it:** use the roadmap to discover practitioner topics and compare alternative learning progressions; keep LLM Lab's two independent Understand and Build paths, canonical concept ownership, bilingual parity, tested NumPy-first explanations and evidence gates. The course's breadth is a discovery aid, not a mandate to add every topic to the core curriculum.
- **Audit and reuse status:** README-level discovery recorded 2026-11-12; representative linked materials and current notebook compatibility still require inspection under [project audit #1049](https://github.com/JM-Brun/llm-lab/issues/1049). Link to original materials; do not assume notebook, text, figure, code or dataset reuse rights from repository visibility.


## LLM fundamentals and the transition to agents

- **Microsoft Learn — [LLM Fundamentals](https://learn.microsoft.com/en-us/agent-framework/journey/llm-fundamentals)** (Agent Framework learning journey; page updated 25 August 2026).
  - **Use for:** a developer-oriented bridge from core LLM mechanics to agent applications: tokenization and context windows; pretraining and post-training (SFT/RLHF); reasoning-oriented reinforcement learning; autoregressive inference, prefill/decode and KV-cache; chat message roles; temperature; strengths and limitations; structured tool calls and the external execution loop; and the additional layers agents provide (tools, sessions/memory and middleware).
  - **Relationship to LLM Lab:** use as a complementary application-oriented synthesis, not as the canonical scientific authority or as a reason to make Microsoft Agent Framework a project dependency. Integrate concepts into their existing canonical bilingual pages, preserving the separate Understand and Build paths and avoiding a new duplicate “LLM fundamentals” chapter.
  - **Qualification:** the page is framework-oriented and simplifies some topics. Cross-check scientific claims against primary papers and established technical references; distinguish model-generated tool-call requests from application-side execution; qualify statements about reasoning, determinism, memory and tool-use training by model/provider/runtime.
  - **Access and reuse:** the page currently displays an authorization notice in the retrieved view. Link to the original rather than copying its prose, examples or diagrams; no third-party assets are reused.

## Efficient attention and GPU execution

- **Damien Benveniste — “How FlashAttention Speeds Up LLM Attention”** (The AI Edge, 13 November 2026): https://newsletter.theaiedge.io/p/how-flashattention-speeds-up-llm-attention
  - **Use for:** an introduction to tiled exact attention, online normalization and the distinction between attention mathematics and GPU execution.
  - **Review status:** only the introductory courtesy excerpt and table of contents were accessible; the full newsletter is paid. Technical framing is cross-checked against primary papers and PyTorch documentation. No figures or full text are reused. See [the source review](source-reviews/flashattention-io-aware-2026-11.md).
- **Tri Dao et al. — “FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness”** (NeurIPS 2022): https://arxiv.org/abs/2205.14135
  - **Use for:** primary source for IO-aware tiling, exact attention, reduced HBM traffic and IO analysis.
- **Tri Dao — “FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning”** (ICLR 2024): https://arxiv.org/abs/2307.08691
  - **Use for:** follow-up improvements to work partitioning and GPU parallelism; benchmark claims remain hardware- and workload-specific.
- **Jay Shah et al. — “FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision”** (NeurIPS 2024): https://arxiv.org/abs/2407.08608
  - **Use for:** a hardware-specific follow-up exploiting Hopper GPU asynchrony, Tensor Memory Accelerator, warp specialization and low-precision FP8. Treat it as a distinct generation/implementation, not as an interchangeable synonym for the original FlashAttention kernel.
- **PyTorch — Scaled dot product attention API:** https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html
  - **Use for:** API contract and backend-dispatch constraints. Calling SDPA does not prove that a FlashAttention backend was selected.

## Information theory, entropy and predictive compression

- **Grant Sanderson / 3Blue1Brown — [Reinventing Entropy | Compression is Intelligence Part 1](https://www.youtube.com/watch?v=l6DKRf-fAAM)** (7 June 2026; approximately 32 minutes).
  - **Use for:** an intuitive derivation of surprisal from ideal code length, prefix-free codes and binary trees, Shannon entropy as expected information, and the transition from independent symbols to context-dependent language and entropy rate.
  - **AIhub relay:** [Reinventing Entropy | Compression is Intelligence Part 1](https://aihub.org/2026/07/16/reinventing-entropy-compression-is-intelligence-part-1/) (16 July 2026). This page embeds the same video; it is not an independent second source.
  - **Review status:** the full timestamped transcript was retrieved through a third-party caption mirror and reconciled with the existing bilingual entropy and compression lessons. The original video was not independently inspected frame by frame, and caption fidelity remains unverified. See the [critical synthesis](source-syntheses/reinventing-entropy-2026-11.md) and [structured extraction](../data/extractions/3blue1brown-reinventing-entropy-compression-intelligence-part-1-2026.yml).
  - **Reuse:** link to the original video only; no transcript, screenshots, animation or music are republished. The source's idealized “random-looking compressed stream” intuition must not be treated as a necessary-and-sufficient test for optimal compression.


## Information theory and language models

## Algorithmic information and universal agents

**Synthesis:** [Kolmogorov complexity, universal prediction and AIXI](source-syntheses/kolmogorov-aixi-computability-2026-11.md) connects the formal layers and their computability limits.

- **Marcus Hutter — [Universal Algorithmic Intelligence: A Mathematical Top-Down Approach](https://arxiv.org/abs/cs/0701125)** (2007; based on the IDSIA technical report).
  - **Use for:** the primary theoretical construction connecting Kolmogorov complexity, the universal Solomonoff mixture, sequential decision theory, AIXI and the resource-bounded AIXI(t,l) agent. Sections 3.2–3.4 and 6 are the key route.
  - **Critical qualifications:** K is upper semicomputable but not computable; the universal mixture is a semimeasure, not a normalized computable probability; AIXI's optimality is relative to formal assumptions. The detailed AIXI(t,l) construction gives $O(t\,2^l)$ per cycle, with large hidden constants. Do not flatten superscripts or confuse candidate-program bounds with environment-only bounds.
  - **Review status:** complete targeted inspection of the accessible report on 17 November 2026. See [advanced source review](source-reviews/aixi-kolmogorov-computability-2026-11.md) and [Hutter extraction](../data/extractions/hutter-universal-algorithmic-intelligence-2007.yml), [Leike & Hutter extraction](../data/extractions/leike-hutter-computability-aixi-2015.yml), and [2024 textbook extraction](../data/extractions/hutter-quarel-catt-universal-ai-2024.yml).

- **Jan Leike & Marcus Hutter — [On the Computability of AIXI](https://arxiv.org/abs/1510.05572)** (UAI 2015).
  - **Use for:** formulation-sensitive computability results. Standard/iterative exact AIXI is not limit computable because of exact action ties and the iterative discounted infinite-horizon value definition; ε-optimality plus a recursive value function yields a limit-computable infinite-horizon policy, with a computable tolerance that can decrease toward zero. The paper models environments as lower semicomputable chronological conditional semimeasures (LSCCCSs).
  - **Scope:** abstract, introduction, relevant computability results and discussion (including Corollary 22) inspected; technical proofs were not audited line by line. Do not paraphrase the result as ruling out every useful approximation to restricted aspects of AIXI.

- **Marcus Hutter, David Quarel & Elliot Catt — [An Introduction to Universal Artificial Intelligence](https://hutter1.net/publ/uaibook2.pdf)** (24 December 2024).
  - **Use for:** a current textbook-level treatment of Kolmogorov complexity and universal prediction, plus the explicit AIXI(t,l) algorithm, proof-length parameter (l_P), setup complexity and per-cycle theorem. See Section 13.2, Algorithm 13.1 and Theorem 13.2.3.
  - **Review status:** targeted inspection of the relevant background and AIXI(t,l) section; no code or algorithm was executed. Asymptotic complexity is not a practical runtime benchmark.


- **Wayland Zhang — Information Theory Is All You Need (to Understand LLMs)** (17 February 2026): https://waylandz.com/blog/information-theory-and-llm/
  - **Use for:** a unifying introductory thread connecting Shannon information, entropy, next-token prediction, cross-entropy, KL divergence, attention, compression and model capacity.
  - **Critical qualifications:** attention weights are not mutual information; Landauer's erasure bound does not establish a general information ceiling for learning from a dataset; compression performance is not equivalent to intelligence; V-information depends on a specified predictive/model class and operational setup.
  - **Companion material:** the author links an English and Chinese notebook in https://github.com/waylandzhang/information-theory-and-language-models. The English notebook received a static 18-cell audit; it was not executed. See the [notebook audit](source-reviews/wayland-notebook-audit-2026-11.md).
  - **Review status:** article text inspected and notebook source cells plus saved text outputs statically audited on 16 November 2026; notebook execution and figure reuse were not verified. See the [article source review](source-reviews/information-theory-wayland-zhang-2026-11.md). Text, figures and code are link-only; no reuse licence was established.

- **Yilun Xu, Shengjia Zhao, Jiaming Song, Russell Stewart and Stefano Ermon — “A Theory of Usable Information under Computational Constraints”** (ICLR 2020): https://arxiv.org/abs/2002.10689
  - **Use for:** primary formal source for predictive \\(\\mathcal V\\)-information, predictive families, optional ignorance, predictive conditional \\(\\mathcal V\\)-entropy and the relation to Shannon mutual information.
  - **Critical qualifications:** the quantity is relative to an explicitly specified predictive family and loss; it is asymmetric and is not a synonym for Shannon mutual information. The paper's estimation guarantees depend on bounded log-probabilities and complexity assumptions; an overly expressive class can overfit and an overly restrictive class can miss useful structure.
  - **LLM Lab integration:** use the finite-family exact example in the bilingual information-theory experiment guide as a first operational illustration, not as evidence comparing Transformer attention with bag-of-words. See [the source review](source-reviews/predictive-v-information-xu-2020.md).


- **Grant Sanderson / 3Blue1Brown — [But what is cross-entropy? | Compression is Intelligence Part 2](https://www.youtube.com/watch?v=GlYgs6v2YfU)** (16 July 2026; approximately 34 minutes).
  - **Official lesson:** [3Blue1Brown lesson page](https://www.3blue1brown.com/?lesson=cross-entropy&topic=neural-networks); [creator's Substack article](https://3blue1brown.substack.com/p/but-what-is-cross-entropy).
  - **Review status:** creator-published captions reviewed through a third-party transcript mirror; relevant upstream Manim source scripts inspected statically, not executed. No frame-by-frame audiovisual audit. See the [critical synthesis](source-syntheses/cross-entropy-compression-distillation-2026-11.md) and [structured extraction](../data/extractions/3blue1brown-cross-entropy-compression-intelligence-part-2-2026.yml).
  - **Use for:** the operational meaning of cross-entropy as the average cost of a code optimized for a different distribution; the link to next-token pretraining, the assumptions behind the logarithmic loss, soft-target distillation, and KL divergence.

- **Notion — [Intelligence = Compression](https://jealous-speedwell-b32.notion.site/Intelligence-Compression-4c8d01d16ebf4dc98c5c5cb85ea825c8)** (author and date not identified).
  - **Use for:** a compact cross-cutting prompt to connect predictive coding, the Hutter Prize, algorithmic information theory and cognitive architectures.
  - **Critical qualification:** “intelligence = compression” is a hypothesis/slogan, not an established equivalence. The claimed equivalence between text compression and passing the Turing test is not demonstrated; compression does not automatically reduce end-to-end compute because coding/decoding overhead and downstream costs matter. The page is unsourced and contains a malformed enwik9 size expression; the official benchmark defines enwik9 as 10^9 bytes. Existing entropy, cross-entropy and predictive-compression lessons remain the authoritative teaching destinations.
  - **Review status:** all public page text inspected on 17 November 2026; Hutter Prize details checked against the official competition page. Author, date, revision, figures and reuse rights remain unknown. See [critical source review](source-reviews/notion-intelligence-compression-2026-11.md) and [structured extraction](../data/extractions/notion-intelligence-compression-summary.yml). Text and figures are link-only.

## Remote GPU training and managed execution

- **YouTube — “GPU-POOR? NO PROBLEM!... thanks to 🤗 Jobs”**: https://www.youtube.com/watch?v=7Yx_7byZiFU
  - **Use for:** an operational illustration of moving a NanoGPT-like training command from constrained local hardware to managed Hugging Face Jobs through a shell launcher.
  - **Review status:** partial, transcript-assisted for the audiovisual source; the full linked [NanoGPT Jobs repository](https://github.com/scienceetonnante/nanogpt-jobs) was subsequently inspected statically (README, `train.py`, `run_on_hf.sh`, requirements and sampler). The code confirms a ~51M-parameter GPT trained on TinyStories and a private Storage Bucket staging/persistence workflow. No job was executed and no billed run was independently verified. The code has no held-out validation/test evaluation. See the [source review](source-reviews/huggingface-jobs-nanogpt-video-2026-11.md) and [French](../experiments/huggingface-jobs/README.fr.md)/[English](../experiments/huggingface-jobs/README.md) operational recipes.
  - **Relationship to LLM Lab:** optional remote-execution recipe after a working training loop, not a core prerequisite or evidence that the project currently trains NanoGPT.
- **Hugging Face — [Run and manage Jobs](https://huggingface.co/docs/huggingface_hub/en/guides/jobs), [configuration](https://huggingface.co/docs/hub/en/jobs-configuration), and [pricing](https://huggingface.co/docs/hub/en/jobs-pricing)**
  - **Use for:** current CLI/Python job execution, hardware flavors, timeouts, secrets and billing. Check the living documentation before launching paid compute.

## Sentence embeddings and information retrieval

- **Reimers & Gurevych (2019).** [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://aclanthology.org/D19-1410/). Primary source for the Siamese sentence-embedding architecture; weight tying is a property of this design, not a universal requirement for bi-encoders.
- **Khattab & Zaharia (2020).** [ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832). Introduces contextualized late interaction and MaxSim.
- **Santhanam et al. (2022).** [ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction](https://aclanthology.org/2022.naacl-main.272/). Residual compression and denoised supervision for late-interaction retrieval.
- **Formal, Piwowarski & Clinchant (2021).** [SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking](https://arxiv.org/abs/2107.05720). Learned sparse term-weight retrieval.
- **Thakur et al. (2021).** [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663). Heterogeneous comparison of lexical, sparse, dense, late-interaction and reranking systems.

- **Chawla (2025).** [Visual Guide to Bi-encoders, Cross-encoders and ColBERT](https://blog.dailydoseofds.com/p/visual-guide-to-bi-encoders-cross). A compact visual overview; consult primary ColBERT papers for the formal architecture and performance claims.
- **Faysse et al. (2025).** [ColPali: Efficient Document Retrieval with Vision Language Models](https://proceedings.iclr.cc/paper_files/paper/2025/hash/99e9e141aafc314f76b0ca3dd66898b3-Abstract-Conference.html). Extends late interaction to visual page retrieval; includes ViDoRe, architecture comparisons and query-to-patch visualizations.

## Learning-roadmap case studies

- **Hesam Sheikh — How I Studied LLMs in Two Weeks: A Comprehensive Roadmap** (Towards Data Science, 18 October 2024): https://towardsdatascience.com/how-i-studied-llms-in-two-weeks-a-comprehensive-roadmap-e8ac19667a31/
  - **Companion study journal:** https://github.com/hesamsheikh/ml-retreat (Days 003–016 cover tokenization, attention, GPT/fine-tuning, hallucination, knowledge distillation, pause tokens, Infini-attention, RoPE, KV cache, MoE, ViT, natural-language understanding and multimodal LMs).
  - **Use for:** a practitioner case study of question-led learning, selective resource use and a broad progression from core Transformers to advanced and multimodal topics. Treat the two-week duration and daily time estimates as one learner's report, not a general workload promise.
  - **Review status:** article and daily README text inspected; linked PDF notes and embedded images not inspected. Day notes repeatedly attribute many images to Sebastian Raschka's book; no images are reproduced. See [source review](source-reviews/hesam-sheikh-llm-study-roadmap-2026-11.md) and [structured extraction](../data/extractions/hesam-sheikh-llm-study-roadmap-2024.yml).

## Introductory LLM explainers

- **Jose Parreño Garcia — [LLMs explained (Part 1): The 3-layer framework behind chatGPT & friends](https://joseparreogarcia.substack.com/p/how-llms-work-part-1-the-3-essential-layers)** (5 April 2025).
  - **Use for:** an accessible analogy between classical predictive modelling and three broad stages of LLM construction: corpus collection, base-model training and fine-tuning.
  - **Critical caveat:** next-token training is not a truth objective; fine-tuning does not guarantee factuality; the article's categorical claims about reasoning and understanding are not established by its explanation. The Llama 3 8B / DeepSeek R1 14B comparison is anecdotal and confounded.
  - **Review status:** full visible article body and both embedded images inspected; video and outbound resources not systematically audited. Images and text remain link-only. See [source review](source-reviews/jose-parreno-garcia-how-llms-work-three-layers-2026-11.md) and [structured extraction](../data/extractions/jose-parreno-garcia-how-llms-work-three-layers-2025.yml).


## End-to-end LLM lifecycle and mental models

- **Andrej Karpathy — Deep Dive into LLMs like ChatGPT** (5 February 2025): https://www.youtube.com/watch?v=7xTGNNLPyMI
  - **Use for:** an accessible, end-to-end overview of pretraining data, tokenization, Transformer computation, inference, base models, post-training, hallucinations, tool use, context, reasoning and reinforcement learning. Particularly useful as a lifecycle-level companion to the canonical lessons rather than a replacement for them.
  - **How this lab uses it:** optional overview linked to the LLM panorama, post-training, in-context learning and limits material. The source's teaching route is reconstructed separately from the canonical concept graph and learning paths. See [the source review](source-reviews/karpathy-deep-dive-llms-2026-11.md) and [learning-graph comparison](source-reviews/karpathy-deep-dive-learning-graph-2026-11.md).
  - **Review status:** partially scanned on 18 November 2026 using the YouTube description, 24 public chapter markers and a third-party timestamped transcript index. The audiovisual recording was not watched end-to-end; transcript accuracy, demonstrations, slides and visual assets remain unverified. Figures, transcript and code are not copied. The video description's educational-use statement is not treated as blanket redistribution permission.

- **Jose Parreño Garcia — [Understanding Transformers (Part 4): Attention is just a few matrices](https://joseparreogarcia.substack.com/p/understanding-transformers-part-4)** (20 June 2026).
  - **Use for:** an introductory walkthrough of Q/K/V, scaled dot-product attention, row-wise softmax, weighted Value aggregation and multi-head attention; especially the distinction between relevance scoring and information aggregation.
  - **Critical qualifications:** softmax is a fixed normalization, not a learned interaction mechanism; attention logits are not semantic similarity; causal masks also matter at autoregressive inference; parallel sequence computation does not remove sequential token generation; standard multi-head attention includes an output projection W_O.
  - **Review status:** complete visible article text inspected on 19 November 2026. Embedded figures, linked series parts and the original paper were not inspected; no code was executed. Text and figures are link-only. See the [critical source review](source-reviews/jose-parreno-garcia-understanding-transformers-part-4-2026-11.md) and [structured extraction](../data/extractions/jose-parreno-garcia-understanding-transformers-part-4-2026.yml).

## Pre-training progress and evaluation

- **Sebastian Raschka — Pre-training is (still) not plateauing** (22 November 2026): https://sebastianraschka.com/blog/2026/pretraining-is-still-not-plateauing.html
  - LinkedIn post: https://www.linkedin.com/posts/sebastianraschka_pre-training-is-still-not-plateauing-finally-share-7530419578179502080-e0tU/
  - **Use for:** an accessible reading of recent base-model log-perplexity progress and the distinction between pre-training, post-training and the harness that applies model capabilities.
  - **Qualification:** the author's note interprets an OpenAI chart; the chart image has not been independently inspected in this review. See [the source review](source-reviews/raschka-pretraining-not-plateauing-2026-11.md).

- **Jakub Pachocki / OpenAI — Perplexity and Intelligence** (22 November 2026): https://openai.com/index/perplexity-and-intelligence/
  - **Use for:** the primary explanation of OpenAI's reported held-out base-model perplexity measurements, the relation between log-perplexity and cross-entropy, and the limitations of perplexity as a cross-lab or downstream-capability metric.
  - **Qualification:** reported measurements concern a fixed internal code dataset; the underlying dataset and evaluation pipeline are not public in the article. The chart is linked, not reproduced.


## Misconceptions and deployed-system models

- **Zhicheng Lin — [Six misconceptions about large language models: A minimal model and diagnostic taxonomy](https://doi.org/10.1093/pnasnexus/pgag236)**, *PNAS Nexus*, 5(7), pgag236, 8 July 2026 (corrected and typeset 17 July 2026).
  - **Use for:** the distinction between the pretraining objective and deployed-system capability; learned distributions and sampled outputs; parametric, contextual and external memory; and task competence versus agency.
  - **Qualification:** this is a Perspective proposing a diagnostic framework, not a consensus taxonomy. Its empirical examples and cited primary studies were not independently verified in this source pass. The article is open access under CC BY 4.0; no figures are reused.
  - **Review and extraction:** [source review](source-reviews/lin-2026-six-llm-misconceptions-source-review.md) and [structured extraction](../data/extractions/lin-2026-six-llm-misconceptions.yml).
