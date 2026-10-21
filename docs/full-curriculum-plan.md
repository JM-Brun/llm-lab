# Full LLM curriculum and coverage plan

**Status:** planning only. This document defines scope, dependencies, page ownership, and acceptance criteria. It does not authorize drafting all lessons, adding model implementations, or running new experiments immediately.

**Primary baseline:** Sebastian Raschka, [*Build a Large Language Model (From Scratch)* source repository](https://github.com/rasbt/LLMs-from-scratch). The repository evolves; re-check its README and chapter folders before marking coverage complete.

**Complementary explanations:** [Jay Alammar, The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/), [The Illustrated Transformer From Scratch](https://idtjo.hosting.acm.org/wordpress/the-illustrated-transformer/), [Jay Alammar, The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/), and [3Blue1Brown's GPT lessons](https://www.3blue1brown.com/lessons/gpt/).

## 1. Editorial contract

- Keep the course bilingual (French and English) and the concept pages canonical: explain one concept deeply, then link to it instead of duplicating it.
- Separate overview pages, concept pages, exercises, implementations/tests, experiment reports, and private mastery evidence.
- Explain intuition, notation, tensor shapes, assumptions, numerical issues, misconceptions, counterexamples, failure modes, and limits—not just the happy path.
- Cite research papers and official documentation for technical claims. Attribute external diagrams and link to their original pages. Do not copy an illustration merely because it is publicly accessible.
- State clearly what exists, what has been validated, and what is only planned. A passing test, rendered page, low training loss, or completed exercise does not by itself demonstrate mastery.
- Do not add new implementations or experiments until their conceptual prerequisites are marked acquired in the private `career-knowledge` inventory.
- Use Raschka's book and repository as a **coverage baseline**, not as text, code, or exercise material to reproduce. Write original explanations and exercises; link to the source.
- The ACM-hosted article presents a useful modern-block perspective, but it is not a substitute for explaining the original encoder–decoder Transformer and why decoder-only GPT differs.

## 2. Target information architecture

### Public course
1. **Orientation and map** — what an LLM is, learning prerequisites, reading paths, scope and limitations.
2. **Mathematical and numerical foundations** — vectors/matrices/tensors, probability, logits/softmax, information theory, likelihood, losses, derivatives, optimization, numerical stability.
3. **Text and datasets** — Unicode, normalization, tokenization, vocabularies, BPE, special tokens, encoding/decoding, windows, batching, input-target shift, data leakage.
4. **Attention** — Q/K/V, score scaling, masking, softmax, weighted values, multi-head attention, tensor shapes, causal invariants.
5. **Transformer architecture** — embeddings, positional information, residual paths, normalization, MLP/FFN, block ordering, output head, parameter tying, decoder-only versus encoder/decoder and encoder-only.
6. **GPT implementation concepts** — configuration, parameter count, initialization, forward pass, loss, generation; code links only after prerequisites are validated.
7. **Pretraining** — autoregressive objective, data splits, batching, optimizer, schedules, clipping, validation, checkpointing, perplexity, reproducibility and resource costs.
8. **Inference and decoding** — greedy decoding, sampling, temperature, top-k/top-p, stopping, prompt/context limits, KV cache, latency/memory trade-offs.
9. **Fine-tuning** — classification fine-tuning, instruction formats, supervised fine-tuning (SFT), target masking, packing, dataset quality, overfitting and catastrophic forgetting.
10. **Evaluation** — task-specific metrics, baselines, held-out sets, contamination, leakage, uncertainty, error analysis, LLM-as-judge limitations, calibration when appropriate.
11. **Efficiency and architecture variants** — LoRA, quantization/QLoRA, memory accounting, efficient attention, GQA, MLA, sliding windows, MoE, KV sharing; mark advanced/optional.
12. **Preference optimization and alignment** — preference pairs, reward models at conceptual level, DPO, preference-data bias, evaluation and regressions; mark advanced/optional.
13. **Critical reading and research methods** — representation geometry, cosine similarity, linearity hypotheses, ablations, causal claims, reproducibility, evidence quality and limitations.
14. **Glossary, reference library and cross-cutting visual atlas**.

### Separate exercise space
Use a distinct `site/exercises/` area, with a bilingual landing page and one future exercise collection per module. Exercise IDs should remain stable across languages. Each course question links to the relevant collection or exercise anchor; the collection links back to the canonical concept page. Keep the answer key collapsed by default and do not put exercise solutions into lesson prose.

Planned collections (structure only; exercises are not written yet):
- `foundations`: vectors, tensor shapes, probability, softmax, entropy, cross-entropy, likelihood, gradients and numerical checks.
- `text-data`: tokenization, special tokens, windows, input-target alignment, batching and data-split hygiene.
- `attention`: Q/K/V roles, score scaling, masks, multi-head shapes and causal-invariance reasoning.
- `transformer`: block data flow, positional information, residuals, normalization, MLP and architecture comparison.
- `pretraining`: objective, training curves, validation, perplexity, checkpoints and reproducibility.
- `generation`: next-token distributions, decoding settings, stopping and KV-cache trade-offs.
- `fine-tuning`: classification, SFT, loss masking, split integrity, overfitting and error analysis.
- `evaluation`: baselines, leakage/contamination, uncertainty, metrics and limitations.
- `efficiency`: LoRA/QLoRA concepts, parameter/memory accounting and trade-offs.
- `advanced`: DPO, architecture variants, critical-reading and research-design prompts.

Every future exercise should declare: stable ID, language parity, prerequisites, target concept, format (conceptual / derivation / paper-and-pencil / code / debugging / experimental design), difficulty, expected evidence, hint(s), optional collapsed solution, and relevant references. Do not copy the book's exercise statements or solutions.

## 3. Coverage map against Raschka

This map follows the chapter and appendix structure advertised in the upstream repository README. It is a scope checklist, not a claim that LLM Lab already covers all details.

| Upstream topic | LLM Lab destination / planned destination | Current coverage status |
|---|---|---|
| Ch. 1 — Understanding LLMs | Orientation, Transformer overview, glossary, history | Partial: high-level GPT flow exists; broaden LLM families, training stages, limits and terminology after prerequisite review. |
| Ch. 2 — Working with text data | Text/data module; tokenization, BPE, special tokens, windows, dataloader | Gap: not yet a dedicated, comprehensive bilingual chapter. |
| Ch. 3 — Coding attention mechanisms | Q/K/V, scaled dot-product attention, causal masking, multi-head attention | Partial: conceptual pages exist; detailed shape contracts and implementation are not yet complete. |
| Ch. 4 — Implementing a GPT model | Transformer overview, block, GPT model, generation | Partial: overview exists; complete architecture/configuration/forward pass and code are not established. |
| Ch. 5 — Pretraining on unlabeled data | Pretraining, optimizer/training loop, validation, generation, checkpointing | Gap/partial: objective concepts exist; full reproducible pretraining account is not present. |
| Ch. 6 — Fine-tuning for text classification | Fine-tuning/classification | Gap: dedicated coverage and validated implementation not present. |
| Ch. 7 — Fine-tuning to follow instructions | SFT, instruction data, masking, evaluation | Partial elsewhere in the career learning programme, but no complete public bilingual course module yet. Map to existing canonical knowledge before writing. |
| Appendix A — PyTorch introduction | Tensor shapes, autograd, modules, datasets/dataloaders, device and reproducibility | Gap: only add the prerequisite depth actually needed; link official PyTorch docs. |
| Appendix B — References and further reading | Reference library | Partial: references exist; expand and categorize when the plan is reviewed. |
| Appendix C — Exercise solutions | Separate exercise area with hidden answer keys | Planned structure; no new exercises/solutions in this planning change. |
| Appendix D — Training-loop improvements | Training-loop diagnostics, scheduling, clipping, logging and checkpointing | Advanced/optional gap. |
| Appendix E — LoRA | Parameter-efficient fine-tuning, rank/alpha/target modules, memory and evaluation | Conceptual material exists in the private career track; public bilingual coverage needs a future mapped review. |
| Bonus — tokenizer variants, dataloaders, embedding vs linear layers | Text-data concepts and exercise collection | Gap; cover only after core text-data concepts are validated. |
| Bonus — optimized attention, buffers, KV cache, FLOPs | Attention/inference/efficiency modules | Gap; distinguish conceptual description from measured performance. |
| Bonus — GQA, MLA, sliding-window attention, DeltaNet, MoE, KV sharing | Advanced architecture variants | Not core parity for the first pass; add as optional comparative notes with current primary sources. |
| Bonus — other model families, e.g. Llama/Qwen/Gemma | Architecture comparison and reference loading | Optional extension; avoid claiming one GPT implementation represents all LLMs. |
| Bonus — dataset utilities, evaluation, DPO, UI | Data quality, evaluation and preference optimization | Partial/gap; keep UI building out of the core learning objective. |
| Related Reasoning From Scratch material — verifier-based evaluation, self-consistency/refinement, RLVR/GRPO | Advanced evaluation and inference-time reasoning | Beyond the book baseline; candidate extensions, not initial requirements. |

## 4. Complementary perspectives to incorporate

### Jay Alammar — The Illustrated Transformer / Illustrated GPT-2
Use for visual intuition about embeddings, positional information, encoder–decoder flow, residual paths, attention, decoder blocks and GPT-2 data flow. Explicitly distinguish the original encoder–decoder Transformer from decoder-only GPT. Link to the author's figures rather than copying them. Check the source page's current version before citing a particular detail.

### ACM — The Illustrated Transformer From Scratch
Use as a complementary modern-architecture explanation: self-attention as the operation that mixes information across sequence positions; position-wise MLP as a per-vector operation; residual connections and normalization; and a comparison of modern model families. Explain that this framing is an abstraction: convolutional, recurrent, cross-attention, or other interactions can exist in broader architectures, and details vary across implementations.

### Raschka's source repository
Use its chapter README files, notebooks, bonus folders, and code as a living index of topics, not as text to copy. At review time, distinguish:
- book core chapters and appendices;
- optional bonus implementations and architecture variants;
- newer material added after the book's original scope.
Pin links to the most specific upstream file where useful, and record the date reviewed.

### Visual policy
Prefer original SVG diagrams that clarify tensor flow, shapes, masking, train-vs-inference differences, or competing architecture choices. Each figure needs alt text and a nearby explanation of what it does **not** show. External images should be embedded only when reuse terms allow it; otherwise link to the original source. Keep a provenance entry for every external visual actually embedded.

## 5. Suggested sequencing and gates

1. **Inventory first:** map every existing page to the plan; identify duplicates, gaps, language asymmetry, and missing cross-links.
2. **Knowledge gate:** check prerequisites against `career-knowledge`. Do not create an implementation for a concept that has not been acquired.
3. **Improve existing pages:** correct claims, equations, terminology, counterexamples, references and figures before adding new pages.
4. **Plan review:** confirm scope and ordering; mark each planned module core or optional.
5. **Exercise framework:** create the navigation and link convention first; populate only after course concepts and prerequisite knowledge are validated.
6. **New concept pages:** add one canonical bilingual pair at a time, only for a real gap.
7. **Implementation and experiments:** only after the relevant knowledge gate, with explicit tests, baselines, provenance and limitations.

## 6. Definition of coverage

A topic is considered covered only when:
- a canonical explanation exists in French and English with equivalent claims and caveats;
- notation, tensor shapes and assumptions are explicit where relevant;
- at least one common misconception or discriminating counterexample is addressed where pedagogically useful;
- references support the claims and external visual provenance is clear;
- internal links and rendered math work;
- any implementation claim is backed by actual code/tests, not planned work;
- the learner can answer an unfamiliar transfer question and explain failure conditions, with mastery recorded privately in `career-knowledge`.

A topic is **not** covered merely because it appears in a heading, a diagram, a link, a checklist, or a roadmap.

## 7. Upstream references

- Raschka, [LLMs-from-scratch repository and chapter index](https://github.com/rasbt/LLMs-from-scratch).
- Raschka, [How to best read this book](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch01/reading-recommendations.md).
- Alammar, [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/).
- Alammar, [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/).
- [The Illustrated Transformer From Scratch (ACM-hosted article)](https://idtjo.hosting.acm.org/wordpress/the-illustrated-transformer/).
- [3Blue1Brown — Transformers, the tech behind LLMs](https://www.3blue1brown.com/lessons/gpt/).
