# Annotated references

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
