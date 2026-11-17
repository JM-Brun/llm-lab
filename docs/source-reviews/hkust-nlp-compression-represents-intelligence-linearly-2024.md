# Source review — Compression Represents Intelligence Linearly

**Accessed:** 17 November 2026  
**Repository:** https://github.com/hkust-nlp/llm-compression-intelligence  
**Paper:** Yuzhen Huang, Jinghan Zhang, Zifei Shan and Junxian He, “Compression Represents Intelligence Linearly”, COLM 2024, https://arxiv.org/abs/2404.09937  
**Dataset:** https://huggingface.co/datasets/hkust-nlp/llm-compression

## Executive assessment

This is a strong empirical bridge between predictive language modelling and selected downstream capabilities. It is not proof that compression is a universal definition of intelligence. The paper operationalizes “intelligence” through averages over 12 benchmarks in three domains, then measures predictive compression on external domain-specific corpora.

**Recommendation:** retain it as an empirical case study in the existing compression material and use it to motivate a reproducible domain-matched BPC experiment. Do not create a duplicate foundational lesson or a new canonical “intelligence” concept.

## What is measured

The paper studies 31 public language models and three task families:

| Domain | External corpus | Downstream benchmark examples |
|---|---|---|
| Knowledge / commonsense | Common Crawl | Natural Questions, TriviaQA, ARC-C, HellaSwag, MMLU |
| Coding | GitHub Python | HumanEval, MBPP, DS-1000 |
| Mathematics | ArXiv mathematics | GSM8K, MATH, SAT-Math, MMLU-Math |

The “intelligence” variable is an aggregate benchmark score for selected tasks, not a direct measure of general intelligence, agency, reliability or understanding.

Reported Pearson correlations between benchmark average and bits per character (BPC):

| Domain | Pearson r |
|---|---:|
| Knowledge / commonsense | -0.935 |
| Coding | -0.937 |
| Mathematics | -0.953 |
| Overall | -0.931 |

The paper reports an overall RMSE of 3.1% for its linear fit. Lower BPC means the model assigns higher probability to the held-out text under this protocol; this is associated with higher benchmark scores in the studied model sample. These are strong associations, not causal effects. Scale, training data, compute and training quality may influence both variables.

## Metric: bits per character

For a character sequence X:

[
\mathrm{BPC}(X)=\frac{-\sum_{i=1}^{N}\log_2 p(x_i\mid x_{<i})}{T}
]

where T is the number of characters. When the implementation accumulates cross-entropy in nats:

[
\mathrm{BPC}=\frac{\mathrm{total\_loss\ (nats)}}{T\ln 2}.
]

Character normalization offers a common external unit across tokenizers. It does not eliminate all preprocessing or corpus-composition differences. The information-theoretic interpretation is ideal code length: a symbol assigned probability p costs -log₂(p) bits under an ideal arithmetic coder. Practical coding also has model-availability, framing and coder overhead.

## Domain alignment

BPC is distribution-dependent. A model may compress text from a domain represented in its training distribution better than text from a mismatched domain. The paper reports weaker alignment under mismatched corpus/task combinations. For program-aided mathematical reasoning, combining Python and mathematics corpora can be more informative than either alone.

Do not report a single “compression score” without naming the corpus, preprocessing, context length and intended capability. A score on Common Crawl is not automatically a measure of coding or mathematical competence.

## Contamination and scope

The authors use MIN-K% PROB as a benchmark-contamination diagnostic and treat suspicious Qwen mathematical results as outliers in the regression. This is screening, not proof that remaining models are uncontaminated. Excluding points also changes the fitted relationship and should be transparent.

Scope is bounded: public base models, 12 benchmarks, three domains, a short/medium context setup (1,900-token context; sliding windows with stride 512), and a 2024-era model/corpus snapshot. The authors identify fine-tuned models, long contexts, weaker models and automatic corpus selection as future work.

## Repository implementation notes

The evaluation entry point loads a causal model and tokenizer, accumulates token cross-entropy, then divides by character count times ln(2). The packed dataset concatenates tokenized content and builds sliding windows.

A portability concern: the dataset advances mutable begin/previous-end offsets as items are requested. This is compatible with the current sequential, non-shuffled DataLoader path, but fragile under random access, shuffling or multiple workers. This is a static code-review observation, not a demonstrated failure in the intended setup.

A project reproduction should use stateless index-based access, document treatment of document boundaries and separators, pin model/tokenizer revisions and dependencies, record precision/device settings, and test character counting and normalization.

## Relationship to existing LLM Lab material

Relevant existing resources already cover the foundations:
- entropy and surprisal lessons;
- cross-entropy and negative log likelihood;
- compression revision and predictive-compression concepts;
- the toy arithmetic coder and synthetic domain-shift experiment;
- experimental evaluation, benchmark validity and contamination.

The distinct contribution is the bridge from a toy mechanism to a multi-model empirical association, plus the evidence that corpus/task alignment matters.

## Bounded integration proposal

1. Add a compact empirical case-study panel to the bilingual compression revision pages: three domains, four headline correlations, BPC equation and non-causal caveat.
2. Link to cross-entropy and experimental-evaluation lessons rather than restating them.
3. Extend the existing predictive-compression experiment plan with a real-corpus, multi-domain protocol. Begin with accessible models and legally usable corpora.
4. Make corpus mismatch and contamination explicit controls. Do not present this as a current model leaderboard.
5. Keep the loader concern in the research note unless the code is adapted; do not import the upstream loader unchanged.

## Quality, rights and verdict

The paper is a peer-reviewed COLM 2024 contribution; the repository and dataset improve inspectability. Neither the reported correlations nor the implementation have been independently reproduced in this review. The README reports MIT for code and CC BY-NC-SA 4.0 for the dataset, subject to underlying source-corpus licences and restrictions. Do not assume the dataset can be redistributed wholesale. Paper text and figures remain link-only.

**Verdict: high value, high complementarity, bounded generality.** Integrate as an empirical case study and experimental-design reference. Do not claim intelligence is identical to compression, that BPC measures every capability, or that correlation establishes causation.
