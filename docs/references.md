# Annotated references

The repository is an independent learning and experimentation project. These sources are used for study and comparison; their code, text, datasets, and model weights retain their own licenses and terms.

## Main from-scratch path

1. **Sebastian Raschka — LLMs from Scratch**
   - Repository: https://github.com/rasbt/LLMs-from-scratch
   - Companion guide: https://sebastianraschka.com/llms-from-scratch/
   - Book: https://www.manning.com/books/build-a-large-language-model-from-scratch
   - **Use for:** a coherent end-to-end implementation path from tokenization and attention through GPT pre-training and fine-tuning.
   - **How this lab complements it:** stronger emphasis on numerical tests, controlled comparisons, reproducibility, failure analysis, and compute-aware trade-offs. Do not copy code without preserving attribution and checking its license.

2. **Build a Large Language Model (From Scratch), French-language resources**
   - Interactive learning site: https://www.llmdezero.com/
   - Companion repository: https://github.com/kevindegila/construire-un-llm-de-zero
   - Book overview: https://ayinedjimi-consultants.fr/ouvrages/construire-llm-from-scratch-fr
   - **Use for:** a second explanation in French and visual intuition. Treat implementation details as claims to verify against primary papers, framework documentation, and tests.

## Practical model training

3. **Hugging Face LLM Course**
   - French course: https://huggingface.co/learn/llm-course/fr
   - English course: https://huggingface.co/learn/llm-course/en
   - **Use for:** tokenizers, datasets, Transformers, model fine-tuning, and the practical Hugging Face ecosystem. Course chapters and library APIs evolve; check the current docs for version-specific behavior.

4. **PyTorch Transformer building blocks**
   - Tutorial: https://docs.pytorch.org/tutorials/intermediate/transformer_building_blocks.html
   - Scaled dot-product attention tutorial: https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial
   - **Use for:** comparing readable reference implementations with framework primitives and optimized attention paths. Benchmark on the target hardware rather than assuming a kernel is faster in every configuration.

5. **EleutherAI Language Model Evaluation Harness**
   - Repository: https://github.com/EleutherAI/lm-evaluation-harness
   - **Use for:** understanding standardized evaluation tasks and reproducible benchmark execution. Benchmark scores still depend on task versions, prompts, model/tokenizer details, and evaluation configuration.

## Additional perspectives

6. **Giles Thomas — LLM from scratch**
   - https://www.gilesthomas.com/llm-from-scratch
   - **Use for:** an additional implementation-oriented walkthrough; cross-check assumptions and code against maintained libraries.

7. **AlgoMonster — LLM course introduction**
   - https://algo.monster/courses/llm/llm_course_introduction
   - **Use for:** a structured overview and a potential supplement to the main path. Confirm current coverage and access requirements before relying on it as a primary resource.

8. **LocalLLaMA community discussion**
   - https://www.reddit.com/r/LocalLLaMA/comments/1mq5qw5/learn_how_to_build_an_llm_from_scratch_step_by/
   - **Use for:** practical questions and community perspectives, not as the sole authority for implementation or scientific claims.

9. **Medium walkthrough**
   - https://medium.com/@raufpokemon00/building-a-large-language-model-llm-from-scratch-61fed0570ea5
   - **Use for:** an alternative explanation. Validate technical claims and code against primary sources and runnable tests.

10. **Design principles for LLM-based systems with zero trust**
    - https://cyber.sites.beta.gouv.fr/nous-connaitre/publications/publications-internationales/design-principles-for-llm-based-systems-with-zero-trust/
    - **Use for:** a security perspective for later system-level experiments. Model construction and application security are related but distinct topics.

## How references should be used

- Prefer original papers, official framework documentation, and maintained source repositories for technical claims.
- Record the date/version consulted when an API or benchmark can change.
- Cite upstream work in reports and notebook introductions.
- Do not treat a tutorial's results as independently reproduced until the experiment has been run and checked here.
- Review licenses before reusing code, datasets, model weights, or substantial text.
