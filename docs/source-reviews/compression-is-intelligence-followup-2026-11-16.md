# Follow-up audit — “Compression Is Intelligence” (16 November 2026)

## Scope and status

This follow-up closes part of the evidence gap identified in the source extraction for Sourav Mukherjee's article, while keeping unverified parts explicitly open.

- Article: [Medium canonical page](https://medium.com/bongquisitive-tech/compression-is-intelligence-the-information-theory-behind-llms-70022356dad8)
- Retrieval route recorded by the project: [Freedium mirror](https://freedium-mirror.cfd/https://medium.com/bongquisitive-tech/compression-is-intelligence-the-information-theory-behind-llms-70022356dad8)
- Existing extraction: `data/extractions/sourav-mukherjee-compression-intelligence-2026.yml`
- Existing source review: `docs/source-reviews/compression-is-intelligence-mukherjee-2026-11.md`
- Experimental follow-up: [issue #1136](https://github.com/JM-Brun/llm-lab/issues/1136)

This is a literature and experimental-design follow-up, not a claim that the proposed experiment has been run.

## 1. Main technical clarification: three different inference problems

The article's section on entropy-guided pruning brings together several ideas that must be separated before they are taught or experimentally compared.

| Method family | Signal | Object changed | What it does **not** establish |
|---|---|---|---|
| Layer-wise entropy-guided KV allocation (Kim & Jung, 2025) | Entropy of attention-weight distributions, averaged across heads in each layer | Per-layer KV-cache budget and selected cached positions | That low-surprisal generated reasoning tokens can be deleted |
| Attention-guided KV eviction (SAGE-KV, 2025) | Attention-derived token/head importance | Existing KV entries after prefill | That entropy is the signal, or that reasoning text can be pruned |
| Decoded-token entropy cache refresh (EntropyCache, 2026) | Maximum entropy of newly decoded token distributions | Whether cached states in a diffusion LLM should be recomputed | That autoregressive chain-of-thought tokens are dispensable |
| Reasoning-token deletion (open hypothesis) | Predictive entropy and/or realized surprisal, as candidate selection signals | The generated context itself, followed by regeneration | Anything until task utility is measured under controlled interventions |

### 1.1 Kim & Jung: attention entropy allocates memory across layers

Kim and Jung calculate the entropy of attention weights for each head, average these values within a Transformer layer, and allocate a larger KV-cache budget to layers with broader attention distributions. They then select a common set of cache positions per layer and combine it with recent and sink tokens.

The signal is **attention-weight entropy**, not the model's next-token predictive entropy and not the realized surprisal of a generated token. The intervention changes the retained KV state, not the textual reasoning sequence.

The publisher reports, for its evaluated configurations, 4.18% lower memory use on Qwen3 4B while preserving ROUGE, and 46.6% lower decoding time on Mistral 0.1v 7B. These are paper-reported, configuration-specific results; they are not universal guarantees and do not validate reasoning-token deletion.

Primary source: [Kim & Jung (2025), Mathematics 13(15), 2366](https://doi.org/10.3390/math13152366) · [full text and figures](https://www.mdpi.com/2227-7390/13/15/2366).

### 1.2 SAGE-KV: attention-guided eviction is not an entropy method

SAGE-KV performs a one-time top-k selection at token and head levels after prefill, using self-attention information to evict KV entries for long-context inference. The paper reports evaluations on LongBench and three long-context model configurations.

It is a useful comparator for cache eviction, but it should not be classified as proof of entropy-guided reasoning-token pruning. Its decision signal and intervention target differ.

Primary source: [Wang et al. (2025), arXiv:2503.08879](https://arxiv.org/abs/2503.08879).

### 1.3 EntropyCache: entropy predicts cache drift in diffusion LMs

EntropyCache uses the maximum entropy of newly decoded token distributions as a low-overhead signal for deciding whether to skip or recompute cached states. Its motivating empirical observation is a correlation between decoded-token entropy and KV-cache drift in diffusion-based LMs. The paper evaluates LLaDA-8B-Instruct and Dream-7B-Instruct and reports large speedups on its benchmarks.

This is an important bridge between entropy and inference efficiency, but its scope is **diffusion language models and cache refresh**. It is not a general result about deleting low-entropy reasoning tokens from autoregressive LLM traces.

Primary source: [Cheong et al. (2026), EntropyCache, arXiv:2603.18489](https://arxiv.org/abs/2603.18489) · [authors' code repository](https://github.com/mscheong01/EntropyCache).

## 2. Signal glossary: keep the variables distinct

For a context (c_t), predictive distribution (p(\cdot\mid c_t)), and actually emitted token (x_t):

- **Predictive entropy:** (H_t=-\sum_x p(x\mid c_t)\log p(x\mid c_t)). It describes uncertainty over possible next tokens before observing the selected token.
- **Realized surprisal:** (s_t=-\log p(x_t\mid c_t)). It describes the probability assigned to the token that was actually emitted.
- **Attention-weight entropy:** entropy of a normalized attention-weight vector over context positions, for a specified layer/head/query.
- **KV-cache drift:** a discrepancy between retained cached states and states obtained by recomputing under the updated context/model procedure. It requires a method-specific definition and measurement.
- **Token utility:** the causal contribution of a token to a task outcome under a specified intervention. None of the four signals above is, by definition, token utility.

The entropy and surprisal values depend on the logarithm base (bits for base 2, nats for natural logarithms). Comparisons must use consistent conventions.

A token can have low surprisal and still carry essential grammatical, referential or algorithmic information. Conversely, a high-surprisal token may be an error or irrelevant detail. The hypothesis to test is therefore not “low entropy means redundant”, but whether a particular signal predicts the **marginal task-quality cost of a defined deletion intervention**.

## 3. A feasible first experiment for issue #1136

### 3.1 Experimental question

For a fixed open autoregressive model and a fixed task suite, do predictive entropy or realized surprisal identify generated tokens whose deletion from the continuing context causes less task-quality degradation than random deletion at the same budget?

This first experiment should not mix KV eviction, cache recomputation and textual context deletion. It studies only textual context deletion followed by regeneration.

### 3.2 Intervention definition

1. Run a no-pruning baseline and save the prompt, generated trace, per-step next-token distribution summaries, final answer, model revision, tokenizer revision, decoding settings and seed.
2. At each eligible generated position, record predictive entropy and realized surprisal under the exact distribution that produced the token.
3. Select a fixed deletion budget using one signal at a time. Pre-register the direction and threshold/ranking rule; do not tune it on the test set.
4. Remove the selected token(s) from the context and **regenerate the continuation** from the altered context. Do not simply delete a token while retaining later tokens that were generated conditionally on the original trace.
5. Score the regenerated final answer with task-specific exact-match or accuracy metrics and retain the failure trace.

### 3.3 Minimum comparison groups

- No deletion.
- Predictive-entropy-ranked deletion.
- Realized-surprisal-ranked deletion.
- Random deletion with matched count and eligible positions.
- Recency-matched deletion (remove the same number of tokens from comparable regions).
- Optional attention-based control only if its exact signal and extraction point are specified and implemented.

The random and recency controls are essential: a method must beat simple deletion policies, not merely the no-pruning baseline.

### 3.4 Tasks and metrics

Use a small, public, deterministic reasoning suite with answer keys and at least two task types (for example, arithmetic word problems and symbolic/multi-step tasks). Keep prompt templates fixed and avoid training or threshold selection on the evaluation set.

Report:

- exact match / task accuracy and paired quality difference from baseline;
- failure categories and examples, not only aggregate scores;
- deleted-token count and fraction, by position and token type;
- generated output length and total tokens processed;
- end-to-end latency, throughput and peak memory;
- pruning/scoring overhead separately from generation time;
- multiple seeds and paired confidence intervals.

A token-deletion policy is not an efficiency win if computing its signal costs more than the saved generation work. Quality and cost must be reported together.

### 3.5 Reproducibility gates

Before interpreting results, pin the model and tokenizer revisions, software stack, hardware, prompts, decoding parameters, seeds, selection rule and evaluation code. Store raw per-example outcomes and the full configuration. Start with a pilot to verify that token-level predictive distributions can be recorded consistently; do not claim the experiment is implemented or run until artifacts exist.

### 3.6 Interpretation limits

- A positive result applies only to the tested model, tasks, prompts, deletion budget and decoding setup.
- A low-entropy signal that correlates with deletion tolerance is not automatically causal or transferable.
- A result on visible generated rationales does not establish that hidden internal reasoning states can be pruned.
- Text-context deletion is not KV-cache eviction and does not measure cache drift.
- If random deletion performs similarly, the entropy signal has not demonstrated added value.

## 4. Visual-asset audit: still open for the source article

The current source extraction explicitly records `figures_media.status: not-inspected`. The canonical Medium page is member-only and the Freedium mirror could not be retrieved by the current inspection channel in this follow-up. Therefore:

- the number and identity of figures in the article have **not** been independently re-verified here;
- no article figure is described as inspected;
- no figure has been copied, redrawn or reused;
- no reuse licence or permission for article figures has been established.

Do not mark the article's media scan complete on the strength of the text extraction. To close this item, retrieve the exact article page and each embedded asset, record exact URLs and captions, inspect the actual image bytes, and assess provenance, rights, accessibility and pedagogical value separately. If the images remain inaccessible, keep the status partial and link to the original rather than reconstructing unseen visuals.

The figures in Kim & Jung's publisher article are separate primary-research assets; their existence does not close the Medium article's visual audit.

## 5. Source-to-project decisions

| Contribution | Project destination | Decision |
|---|---|---|
| Attention entropy as layer-wise cache-allocation signal | Existing compression revision sheet and inference-efficiency synthesis | Explain as a distinct cache-allocation method |
| SAGE-KV attention-based eviction | This research note / issue #1136 related work | Comparator only; not an entropy result |
| EntropyCache decoded-token entropy | This research note / issue #1136 related work | Scope explicitly to diffusion-LM cache refresh |
| Predictive entropy vs realized surprisal | Canonical entropy lesson and bilingual revision sheet | Preserve definitions and units |
| Reasoning-token deletion | Issue #1136 | Experimental hypothesis; no claim of validation |
| Original Medium article figures | Source extraction and visual-asset audit | Still uninspected; no reuse authorized |

## 6. References

1. Kim, H. & Jung, Y. (2025). [Entropy-Guided KV Caching for Efficient LLM Inference](https://doi.org/10.3390/math13152366). *Mathematics*, 13(15), 2366.
2. Wang, G. et al. (2025). [LLMs Know What to Drop: Self-Attention Guided KV Cache Eviction for Efficient Long-Context Inference](https://arxiv.org/abs/2503.08879). arXiv:2503.08879.
3. Cheong, M. et al. (2026). [EntropyCache: Decoded Token Entropy Guided KV Caching for Diffusion Language Models](https://arxiv.org/abs/2603.18489). arXiv:2603.18489.
4. Mukherjee, S. (2026). [Compression Is Intelligence: The Information Theory Behind LLMs](https://medium.com/bongquisitive-tech/compression-is-intelligence-the-information-theory-behind-llms-70022356dad8). *Medium*, 20 July 2026. Retrieved by the project through the Freedium mirror; article figures remain uninspected.

## Completion state

- Textual article extraction: complete according to the existing extraction record.
- Critical distinction between cache methods and reasoning-token deletion: clarified in this follow-up.
- Primary literature triage: three relevant methods compared at signal/intervention/scope level.
- Real autoregressive token-deletion experiment: specified, not implemented or run.
- Article figure/media inspection: open.
- Article figure reuse rights: unknown; no new use authorized.
