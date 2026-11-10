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

- **Vaswani et al. — Attention Is All You Need** (2017), section 3.5: https://arxiv.org/abs/1706.03762
  - **Use for:** primary formulation of sinusoidal positional encodings, frequency schedule, wavelength range, and fixed-offset motivation.
- **Jay Alammar — The Illustrated Transformer**: https://jalammar.github.io/illustrated-transformer/
  - **Use for:** visual intuition for positional vectors and the position-by-dimension matrix. Its July 2020 clarification distinguishes the earlier concatenated illustration from the interleaved formula in the original paper.
- **Harvard NLP — The Annotated Transformer**: https://nlp.seas.harvard.edu/annotated-transformer/
  - **Use for:** annotated PyTorch implementation connecting the equations to a precomputed buffer and input addition.
- **Stanford EE269 — Transformers for Signal Prediction**: https://web.stanford.edu/class/ee269/Lecture_Transformers.pdf
  - **Use for:** a signal-processing interpretation of angular frequency, wavelength, and logarithmically spaced positional scales.

See the [source review and pedagogical synthesis](source-reviews/sinusoidal-positional-encoding-2026-11.md) for inspection scope, technical reconciliation, and reuse limits. The machine-readable scan records remain in [the source catalogue](../data/sources.yml).

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



## Inference performance and generation systems

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
