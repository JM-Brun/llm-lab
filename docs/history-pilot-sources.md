# LLM history pilot: source-checked candidate milestones

**Status:** research shortlist, 2026-10-31  
**Owner:** [issue #197](https://github.com/JM-Brun/llm-lab/issues/197)  
**Related model:** [history-data-model.md](history-data-model.md)

This is a candidate set for a first historical pilot, not the final public chronology. Dates below identify the cited event convention (submission, publication, or conference publication), not a claim of absolute invention priority. The source links are primary papers or official publication records wherever possible.

## Candidate milestones

| Approx. date | Candidate event | Stream | Why it belongs | Primary evidence | Editorial caution |
|---|---|---|---|---|---|
| 2003 | Neural probabilistic language model | research | Connects neural networks, distributed word representations and probabilistic language modelling; an important bridge from n-gram methods. | [Bengio et al., JMLR (2003)](https://jmlr.org/papers/v3/bengio03a.html) | Do not claim this is the first neural language model without a dedicated priority review. |
| 2013 | Efficient word representations (word2vec) | research | Makes continuous word representations practical at large corpus scale and popularizes reusable embedding spaces. | [Mikolov et al., arXiv:1301.3781](https://arxiv.org/abs/1301.3781) · [Google Research publication record](https://research.google/pubs/efficient-estimation-of-word-representations-in-vector-space/) | Word2vec is not itself a contextual language model; distinguish static word vectors from contextual representations. |
| 2014 | Sequence-to-sequence learning with LSTMs | research | Establishes a general neural encoder-decoder approach for sequence transduction. | [Sutskever et al., arXiv:1409.3215](https://arxiv.org/abs/1409.3215) · [NeurIPS/Google Research record](https://research.google/pubs/sequence-to-sequence-learning-with-neural-networks/) | Keep separate from attention; the fixed-length encoder representation is a limitation addressed by later work. |
| 2014 | Learned attention for neural machine translation | research | Relaxes the fixed-length-vector bottleneck by allowing the decoder to focus on relevant source positions. | [Bahdanau, Cho & Bengio, arXiv:1409.0473](https://arxiv.org/abs/1409.0473) | A precursor to Transformer attention, not the same mechanism or architecture. |
| 2017 | Transformer architecture | research | Proposes an encoder-decoder sequence-transduction architecture based on attention, without recurrence or convolution in its central computation. | [Vaswani et al., arXiv:1706.03762](https://arxiv.org/abs/1706.03762) | The arXiv v1 submission is 12 June 2017; distinguish submission from conference publication. Do not describe the paper as inventing attention. |
| 2018 | ELMo contextualized representations | research | Uses deep bidirectional language-model states to create context-dependent word representations. | [Peters et al., NAACL 2018](https://aclanthology.org/N18-1202/) · [arXiv:1802.05365](https://arxiv.org/abs/1802.05365) | ELMo is based on a bidirectional LSTM language model, not a Transformer. It is a parallel pretraining path. |
| 2018 | BERT pretraining | research | Demonstrates deep bidirectional Transformer encoder pretraining with masked language modelling and task adaptation. | [Devlin et al., arXiv:1810.04805](https://arxiv.org/abs/1810.04805) | arXiv v1 was submitted 11 October 2018; conference publication followed in 2019. BERT is not an autoregressive text generator. |
| 2019 | T5 text-to-text transfer framework | research | Unifies a broad range of NLP tasks under a text-to-text formulation and systematically compares transfer-learning choices. | [Raffel et al., arXiv:1910.10683](https://arxiv.org/abs/1910.10683) · [Google Research record](https://research.google/pubs/exploring-the-limits-of-transfer-learning-with-a-unified-text-to-text-transformer/) | T5 is an encoder-decoder model; do not fold it into the decoder-only GPT lineage. |
| 2020 | Empirical scaling laws for neural language models | research | Quantifies relationships between loss, model size, data and compute, making resource allocation a central research question. | [Kaplan et al., arXiv:2001.08361](https://arxiv.org/abs/2001.08361) · [OpenAI paper page](https://openai.com/index/scaling-laws-for-neural-language-models/) | Later compute-optimal work revised practical implications; avoid presenting the original allocation conclusion as timeless consensus. |
| 2020 | GPT-3 and few-shot in-context learning | research | Shows strong task-agnostic few-shot performance from a large autoregressive model without gradient updates at evaluation time. | [Brown et al., arXiv:2005.14165](https://arxiv.org/abs/2005.14165) | Distinguish in-context learning from parameter fine-tuning; avoid implying that scale alone explains all capabilities. |
| 2022 | InstructGPT and RLHF | research | Studies instruction following through supervised demonstrations, preference rankings, reward modelling and reinforcement learning. | [Ouyang et al., arXiv:2203.02155](https://arxiv.org/abs/2203.02155) | Separate the research contribution from the ChatGPT product launch. The paper itself reports remaining errors and limitations. |
| 2022 | FlashAttention | research | Shows how IO-aware tiling can compute exact attention more efficiently on GPU memory hierarchies. | [Dao et al., arXiv:2205.14135](https://arxiv.org/abs/2205.14135) · [NeurIPS 2022 proceedings](https://papers.nips.cc/paper_files/paper/2022/hash/67d57c32e20fd0a7a302cb81d36e40d5-Abstract-Conference.html) | It improves implementation efficiency; it does not change the mathematical definition of standard attention. Performance depends on hardware and workload. |
| 2023 | Direct Preference Optimization (DPO) | research | Recasts preference-based alignment as a direct optimization objective, avoiding a separately trained reward model in the proposed formulation. | [Rafailov et al., arXiv:2305.18290](https://arxiv.org/abs/2305.18290) · [NeurIPS 2023 proceedings](https://papers.neurips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html) | Do not describe DPO as eliminating preference data or all alignment complexity; it changes the optimization formulation. |
| 2023 | Mamba selective state-space model | research | Presents input-dependent selective state spaces as an alternative sequence-model backbone with linear sequence-length scaling in its formulation. | [Gu & Dao, arXiv:2312.00752](https://arxiv.org/abs/2312.00752) | Present as an alternative research line, not as a demonstrated universal replacement for Transformers. |

## Separate stream: ecosystem and product events

These events may appear on the same timeline but must be visibly distinguished from research contributions:

| Date | Event | Stream | Evidence | Boundary |
|---|---|---|---|---|
| 2022-11-30 | ChatGPT public launch | ecosystem | [OpenAI announcement](https://openai.com/index/chatgpt/) | A major product/distribution milestone; not the invention of the Transformer or RLHF. |

## Initial concept and relation candidates

Relations below are hypotheses to encode only after source-by-source review. They are not all direct influence claims.

| From | To | Candidate relation | Rationale to verify |
|---|---|---|---|
| Neural probabilistic language modelling (2003) | Word representations (2013) | precursor_to / extends | Both use distributed representations, but the specific technical lineage and scope need careful wording. |
| Seq2Seq LSTM (2014) | Bahdanau attention (2014) | precursor_to | Attention addresses the fixed-length context bottleneck in encoder-decoder NMT. |
| Bahdanau attention (2014) | Transformer (2017) | precursor_to | Attention mechanisms predate Transformer; do not claim the Transformer simply reuses Bahdanau's exact mechanism. |
| Transformer (2017) | BERT (2018) | applied_in | BERT uses a Transformer encoder with a different pretraining objective. |
| Transformer (2017) | T5 (2019) | applied_in | T5 uses an encoder-decoder Transformer and text-to-text transfer. |
| Scaling laws (2020) | GPT-3 (2020) | parallel_to / contextualizes | Both belong to the scaling-era discussion; do not imply that the paper alone caused GPT-3. |
| InstructGPT (2022) | DPO (2023) | contextual relation; possible extends | DPO addresses preference optimization in a different formulation; direct methodological lineage should be documented before using influenced/extends. |
| Transformer (2017) | FlashAttention (2022) | applied_in / optimizes | FlashAttention optimizes attention computation used in Transformer workloads; it does not replace the architecture. |
| Transformer (2017) | Mamba (2023) | alternative_to | Mamba is presented as an alternative sequence-model backbone motivated partly by Transformer efficiency limits. |

## Gaps deliberately left open

The pilot is not yet balanced across all relevant histories. Further source work is needed for:

- statistical n-gram language modelling and perplexity before neural language models;
- recurrent language models, LSTM origins, and neural machine translation context;
- subword tokenization and byte-pair encoding in NLP;
- GPT-1 and the generative-pretraining line, with a stable primary source and clear date convention;
- compute-optimal scaling (including Chinchilla) and the relationship to Kaplan et al.;
- LoRA/QLoRA, mixture-of-experts, grouped-query attention and KV caching;
- multimodal pretraining, retrieval-augmented generation, tool use and reasoning-time compute;
- non-English and non-Western research contributions.

Do not fill these gaps with model-release catalogues alone. Each candidate needs an original source and a clear pedagogical reason to appear.

## Verification status

- **Source discovery:** completed for the candidate rows above using original papers, proceedings or official institutional records.
- **Bibliographic audit:** partial. Conference publication dates, arXiv submission dates and release dates still need consistent normalization.
- **Relation audit:** provisional. The relation table is a review queue, not an approved graph.
- **Bilingual descriptions:** not yet drafted.
- **Internal concept links:** not yet checked against the current EN/FR page inventory.
- **Publication decision:** not yet made. Keep the existing page until the pilot has been reviewed and rendered.
