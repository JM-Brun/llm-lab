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

| 2019-02-14 | GPT-2 research announcement and technical report | research | Extends the GPT autoregressive language-model line and studies zero-shot transfer across several NLP tasks using a larger Transformer trained on WebText. | [OpenAI announcement and linked technical report (14 February 2019)](https://openai.com/index/better-language-models/) · [OpenAI-hosted paper PDF](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) | Treat 14 February as the announcement date; the report is an OpenAI technical report, not a peer-reviewed conference paper. Describe reported zero-shot results with the paper's task/benchmark limits, not as general task mastery. |
| 2019-02 to 2019-11 | GPT-2 staged model releases | model_release | Makes the GPT-2 family available in stages: 124M (February), 355M (May), 774M (August), and 1.5B (November). | [OpenAI GPT-2 release report (PDF)](https://cdn.openai.com/GPT_2_August_Report.pdf) · [OpenAI six-month update (20 August 2019)](https://openai.com/index/gpt-2-6-month-follow-up/) · [OpenAI 1.5B release (5 November 2019)](https://openai.com/index/gpt-2-1-5b-release/) · [Official GPT-2 model card](https://github.com/openai/gpt-2/blob/master/model_card.md) | Keep this separate from the research announcement. Use the released-checkpoint counts (124M, 355M, 774M, 1.5B), not the erroneous original paper/blog counts (117M, 345M, 762M, 1542M); OpenAI's archived repository explicitly acknowledges the original count error. Prefer May for the 355M release: the technical report and May interim update support it, although the August follow-up's detailed timeline says April. The same follow-up's timeline says January for the 124M release, while its prose and technical report say February; retain month-level precision and record this inconsistency. |
| 2019 | T5 text-to-text transfer framework | research | Unifies a broad range of NLP tasks under a text-to-text formulation and systematically compares transfer-learning choices. | [Raffel et al., arXiv:1910.10683](https://arxiv.org/abs/1910.10683) · [Google Research record](https://research.google/pubs/exploring-the-limits-of-transfer-learning-with-a-unified-text-to-text-transformer/) | T5 is an encoder-decoder model; do not fold it into the decoder-only GPT lineage. |
| 2020 | Empirical scaling laws for neural language models | research | Quantifies relationships between loss, model size, data and compute, making resource allocation a central research question. | [Kaplan et al., arXiv:2001.08361](https://arxiv.org/abs/2001.08361) · [OpenAI paper page](https://openai.com/index/scaling-laws-for-neural-language-models/) | Later compute-optimal work revised practical implications; avoid presenting the original allocation conclusion as timeless consensus. |
| 2020 | GPT-3 and few-shot in-context learning | research | Shows strong task-agnostic few-shot performance from a large autoregressive model without gradient updates at evaluation time. | [Brown et al., arXiv:2005.14165](https://arxiv.org/abs/2005.14165) | Distinguish in-context learning from parameter fine-tuning; avoid implying that scale alone explains all capabilities. |
| 2022 | InstructGPT and RLHF | research | Studies instruction following through supervised demonstrations, preference rankings, reward modelling and reinforcement learning. | [Ouyang et al., arXiv:2203.02155](https://arxiv.org/abs/2203.02155) | Separate the research contribution from the ChatGPT product launch. The paper itself reports remaining errors and limitations. |
| 2022 | FlashAttention | research | Shows how IO-aware tiling can compute exact attention more efficiently on GPU memory hierarchies. | [Dao et al., arXiv:2205.14135](https://arxiv.org/abs/2205.14135) · [NeurIPS 2022 proceedings](https://papers.nips.cc/paper_files/paper/2022/hash/67d57c32e20fd0a7a302cb81d36e40d5-Abstract-Conference.html) | It improves implementation efficiency; it does not change the mathematical definition of standard attention. Performance depends on hardware and workload. |
| 2023 | Direct Preference Optimization (DPO) | research | Recasts preference-based alignment as a direct optimization objective, avoiding a separately trained reward model in the proposed formulation. | [Rafailov et al., arXiv:2305.18290](https://arxiv.org/abs/2305.18290) · [NeurIPS 2023 proceedings](https://papers.neurips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html) | Do not describe DPO as eliminating preference data or all alignment complexity; it changes the optimization formulation. |
| 2023 | Mamba selective state-space model | research | Presents input-dependent selective state spaces as an alternative sequence-model backbone with linear sequence-length scaling in its formulation. | [Gu & Dao, arXiv:2312.00752](https://arxiv.org/abs/2312.00752) | Present as an alternative research line, not as a demonstrated universal replacement for Transformers. |

### GPT-2: date and parameter-count audit

The official record contains internal inconsistencies, so the chronology should not imply more precision than the evidence supports:

- **Research announcement/report:** use **14 February 2019**, the date displayed on the original OpenAI announcement. The August follow-up's retrospective timeline instead places the announcement and small-model release in January. Keep the announcement date tied to the dated original page, and do not silently harmonize the retrospective discrepancy.
- **124M checkpoint:** use **February 2019** at month precision. The August follow-up's prose and its technical report say February, while its detailed retrospective timeline says January.
- **355M checkpoint:** use **May 2019** at month precision. The technical report and the May interim update support May; the August follow-up's detailed timeline says April. The same OpenAI announcement page is itself updated with a May 2019 interim release note.
- **774M checkpoint:** use **20 August 2019**, the dated OpenAI six-month update.
- **1.5B checkpoint:** use **5 November 2019**, the dated final release announcement.
- **Parameter counts:** the original GPT-2 paper and first announcement used 117M, 345M, 762M and 1542M. OpenAI's archived [repository README](https://github.com/openai/gpt-2#readme) explicitly says the original counts were wrong; the later official [model card](https://github.com/openai/gpt-2/blob/master/model_card.md) gives 124M, 355M, 774M and 1.5B. Use the corrected released-checkpoint counts and, if historical precision matters, note the original error rather than presenting both sets as competing valid conventions.

This audit distinguishes source publication date from retrospective event dating. It does not establish the exact day on which the January/February or April/May checkpoint transitions occurred.

### Core research-event date audit (arXiv v1 convention)

For consistency, the following dates are **first arXiv submission dates**, not invention dates, acceptance dates, or necessarily first public discussion. This convention applies only where an arXiv record exists. The timeline may display year-level precision for readability, but the underlying source record should retain the full date and `kind: submission`.

| Candidate | First-submission date | Source | Date decision / boundary |
|---|---:|---|---|
| Bahdanau et al., learned attention | 2014-09-01 | [arXiv:1409.0473](https://arxiv.org/abs/1409.0473) | First arXiv version; do not conflate with later conference/publication history. |
| Transformer | 2017-06-12 | [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) | The paper proposes the Transformer; it explicitly describes prior attention mechanisms in existing encoder-decoder systems. |
| ELMo | 2018-02-15 | [arXiv:1802.05365](https://arxiv.org/abs/1802.05365) | First arXiv version; the method uses deep bidirectional language-model states, not a Transformer. |
| BERT | 2018-10-11 | [arXiv:1810.04805](https://arxiv.org/abs/1810.04805) | First arXiv version; conference publication is a separate 2019 bibliographic event. |
| T5 | 2019-10-23 | [arXiv:1910.10683](https://arxiv.org/abs/1910.10683) | First arXiv version; encoder-decoder text-to-text transfer framework. |
| Kaplan et al. scaling laws | 2020-01-23 | [arXiv:2001.08361](https://arxiv.org/abs/2001.08361) | First arXiv version; empirical scaling relationships, not timeless universal laws. |
| GPT-3 | 2020-05-28 | [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) | First arXiv version; describe few-shot evaluation without gradient updates, not as proof that scale alone explains capabilities. |
| RAG | 2020-05-22 | [arXiv:2005.11401](https://arxiv.org/abs/2005.11401) | First arXiv version; original formulation combines parametric generation with a non-parametric retrieved memory. |
| LoRA | 2021-06-17 | [arXiv:2106.09685](https://arxiv.org/abs/2106.09685) | First arXiv version; parameter-efficient adaptation, not a new base architecture. |
| Chinchilla | 2022-03-29 | [arXiv:2203.15556](https://arxiv.org/abs/2203.15556) | First arXiv version; use its compute-optimal training claim with the study's compute/data/model assumptions, not as a universal token/parameter law. |
| InstructGPT | 2022-03-04 | [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) | First arXiv version; the abstract and method describe demonstrations, preference rankings, reward modelling and RLHF. |
| FlashAttention | 2022-05-27 | [arXiv:2205.14135](https://arxiv.org/abs/2205.14135) | First arXiv version; exact IO-aware attention algorithm using tiling. Do not claim it changes the quadratic arithmetic complexity of standard attention. |
| DPO | 2023-05-29 | [arXiv:2305.18290](https://arxiv.org/abs/2305.18290) | First arXiv version; direct preference objective in the paper's formulation. It still uses preference data. |
| Mamba | 2023-12-01 | [arXiv:2312.00752](https://arxiv.org/abs/2312.00752) | First arXiv version; selective state-space sequence model, not evidence of universal Transformer replacement. |

Two 2018–2019 cases require a different treatment:

- **GPT (GPT-1):** use **11 June 2018** as the date of OpenAI's [official research announcement](https://openai.com/index/language-unsupervised/), which links the paper. The original work was circulated as an OpenAI technical report/preprint, not a conventional arXiv submission in this inventory. The paper's contribution is generative language-model pretraining followed by discriminative task-specific fine-tuning; do not frame it as the first use of pretraining or transfer learning in NLP.
- **GPT-2:** use **14 February 2019** for the dated official announcement, as detailed in the GPT-2 audit above. This is not a peer-reviewed conference publication date.

**Evidence scope:** this pass checked arXiv first-version metadata and abstracts for the listed papers, plus the official OpenAI GPT announcement. It validates date conventions and high-level descriptions only. It does **not** satisfy the separate full-text review gate for every technical claim or relation. Keep that gate open until each complete paper is reviewed.

## Separate stream: ecosystem and product events

These events may appear on the same timeline but must be visibly distinguished from research contributions:

| Date | Event | Stream | Evidence | Boundary |
|---|---|---|---|---|
| 2022-11-30 | ChatGPT public launch | ecosystem | [OpenAI announcement](https://openai.com/index/chatgpt/) | A major product/distribution milestone; not the invention of the Transformer or RLHF. |

## Initial concept and relation candidates

The initial hypotheses have been reviewed in [history-relation-audit.md](history-relation-audit.md). They must not be encoded as a dense directed graph. The conservative pilot decisions are:

| Candidate pair | Decision | Editorial constraint |
|---|---|---|
| Neural probabilistic language modelling (2003) → word2vec (2013) | No edge yet | Shared use of distributed representations does not establish direct influence. |
| Seq2Seq LSTM (2014) ↔ Bahdanau attention (2014) | No directed edge | Explain the shared encoder–decoder problem context without imposing an unsupported chronology or lineage. |
| Bahdanau attention (2014) → Transformer (2017) | precursor_to | Relevant antecedent; not the same architecture or necessarily the same attention formulation. |
| Transformer (2017) → BERT (2018) | applied_in | Architectural application; masked-language-model pretraining is a distinct contribution. |
| Transformer (2017) → T5 (2019) | applied_in | Encoder–decoder Transformer; not part of the decoder-only GPT lineage. |
| Scaling laws (2020) and GPT-3 (2020) | Same era; no directed edge | Contemporaneous contributions do not establish a causal relationship. |
| InstructGPT (2022) and DPO (2023) | Shared preference-alignment concept | Do not claim direct lineage without additional primary-source evidence. |
| FlashAttention (2022) | Attach to attention/efficiency concept | IO-aware exact attention implementation; not a new architecture or a reduction of the pairwise attention computation's quadratic sequence-length complexity. |
| Transformer (2017) ↔ Mamba (2023) | alternative_to | Compare sequence-model backbones; do not imply universal replacement or direct succession. |

The audit is a first-pass editorial decision record, not final publication approval. Full-paper review, coverage expansion, and bilingual source-backed event records remain outstanding.

## Coverage expansion: additional source-backed candidates

These candidates address gaps identified in the first pass. They are not all selected for the first visual release. Their role, date convention, and relation to the existing events must be reviewed before inclusion.

### Earlier statistical and recurrent language modelling

| Approx. date | Candidate event | Stream | Why it belongs | Primary evidence | Editorial caution |
|---|---|---|---|---|---|
| 1992 | Class-based n-gram language models | research | Representative account of statistical language modelling with word classes and n-gram probabilities before neural LMs became dominant. | [Brown et al., Computational Linguistics (1992)](https://aclanthology.org/J92-4003/) | Not the origin of n-gram modelling. Use as a documented milestone, not as the beginning of statistical language modelling. A deeper historical survey is still needed for Shannon, Markov models, smoothing and perplexity. |
| 1997 | Long short-term memory (LSTM) | research | Introduces a gated recurrent architecture designed to preserve error flow over long time intervals. | [Hochreiter & Schmidhuber, Neural Computation (1997)](https://doi.org/10.1162/neco.1997.9.8.1735) | The article history records receipt in 1995 and publication in 1997. Choose and label publication date for the chronology; do not imply LSTM was invented specifically for language modelling. |

### Generative pretraining and tokenization

| Approx. date | Candidate event | Stream | Why it belongs | Primary evidence | Editorial caution |
|---|---|---|---|---|---|
| 2018-06 | GPT / generative pretraining for language understanding | research | Combines a Transformer-based autoregressive language model pretraining stage with task-specific discriminative fine-tuning, establishing a prominent GPT research line. | [OpenAI research announcement and paper link (11 June 2018)](https://openai.com/index/language-unsupervised/) · [Original paper PDF](https://abaj.ai/doc/papers/radford2018improving.pdf) | The paper was distributed as a technical report rather than a conventional peer-reviewed conference paper. Distinguish the research announcement from later GPT-2/GPT-3 model releases. |
| 2016 | Subword units for neural machine translation | research | Shows how subword segmentation based on byte-pair encoding can address rare and open-vocabulary words in neural MT. | [Sennrich, Haddow & Birch, ACL 2016](https://aclanthology.org/P16-1162/) | BPE predates this NLP application as a compression algorithm. Credit this work for a prominent NLP adaptation, not invention of BPE itself. Distinguish tokenization from model architecture. |

### Scaling, adaptation and conditional computation

| Approx. date | Candidate event | Stream | Why it belongs | Primary evidence | Editorial caution |
|---|---|---|---|---|---|
| 2017 | Sparsely-gated Mixture-of-Experts | research | Demonstrates conditional computation with a gating network selecting a sparse subset of expert subnetworks, including language-modelling applications. | [Shazeer et al., ICLR 2017](https://arxiv.org/abs/1701.06538) · [Google Research record](https://research.google/pubs/outrageously-large-neural-networks-the-sparsely-gated-mixture-of-experts-layer/) | This is not the first theoretical proposal of mixture-of-experts. Explain sparse conditional computation and distinguish parameter count from active compute. The paper's model is recurrent/convolutional-era, not a Transformer MoE. |
| 2022-03 | Chinchilla and compute-optimal training | research | Reassesses the allocation of a fixed training-compute budget between parameter count and training tokens. | [Hoffmann et al., arXiv:2203.15556](https://arxiv.org/abs/2203.15556) · [NeurIPS 2022 proceedings](https://proceedings.neurips.cc/paper_files/paper/2022/hash/c1e2faff6f588870935f114ebe04a3e5-Abstract.html) | Do not summarize as a universal fixed parameter/token ratio. The conclusion depends on the study's training setup and compute assumptions; compare explicitly with Kaplan et al. |
| 2021-06 | LoRA: low-rank adaptation | research | Introduces a parameter-efficient adaptation method that freezes pretrained weights and learns low-rank updates. | [Hu et al., arXiv:2106.09685](https://arxiv.org/abs/2106.09685) | LoRA is an adaptation technique, not a new base architecture. QLoRA is a later distinct extension and needs its own source and event if included. |

### Retrieval, multimodality, prompting and tools

| Approx. date | Candidate event | Stream | Why it belongs | Primary evidence | Editorial caution |
|---|---|---|---|---|---|
| 2020-05 | Retrieval-Augmented Generation (RAG) | research | Combines parametric sequence-to-sequence generation with a retrieved non-parametric document index for knowledge-intensive tasks. | [Lewis et al., arXiv:2005.11401](https://arxiv.org/abs/2005.11401) · [NeurIPS 2020 proceedings](https://papers.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html) | The paper's specific architecture is not identical to every modern system called RAG. Do not imply retrieval eliminates hallucination or guarantees provenance. |
| 2022-04 | Flamingo visual-language model | research | Demonstrates few-shot visual-language learning over interleaved image, video and text inputs by connecting pretrained vision and language models. | [Alayrac et al., arXiv:2204.14198](https://arxiv.org/abs/2204.14198) · [NeurIPS 2022 proceedings](https://papers.neurips.cc/paper_files/paper/2022/hash/960a172bc7fbf0177ccccbb411a7d800-Abstract-Conference.html) | A representative multimodal research milestone, not the origin of vision-language learning or multimodality. Include other modalities and research groups in a balanced account. |
| 2022-01 | Chain-of-thought prompting | research | Studies whether prompting with intermediate reasoning examples improves performance on multi-step tasks. | [Wei et al., arXiv:2201.11903](https://arxiv.org/abs/2201.11903) · [NeurIPS 2022 proceedings](https://papers.neurips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html) | This is a prompting/evaluation method, not evidence that generated rationales faithfully expose internal reasoning. Avoid claims that reasoning abilities simply “emerged” as a settled causal explanation. |
| 2023-02 | Toolformer | research | Explores training language models to decide when and how to call external APIs and incorporate returned results. | [Schick et al., arXiv:2302.04761](https://arxiv.org/abs/2302.04761) · [NeurIPS 2023 proceedings](https://proceedings.neurips.cc/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html) | This is one research approach to tool use, not the origin of all tool-augmented systems. Distinguish tool calling from retrieval-only RAG and from product-level agent systems. |

### Remaining research gaps

The source discovery is broader now, but still incomplete. A balanced history still needs:

- earlier statistical foundations: Shannon's information-theoretic language modelling, Markov assumptions, smoothing, perplexity, and the transition from count-based to neural models;
- the pre-2016 history of subword segmentation, byte-pair encoding, WordPiece and SentencePiece, with their distinct origins and uses;
- the broader progression of decoder-only pretrained language models beyond the GPT-2 source-checked announcement and staged-release record;
- QLoRA and later parameter-efficient adaptation methods;
- grouped-query attention, multi-query attention, KV caching, speculative decoding and inference-time systems;
- further multimodal lines (speech, audio, video, image-text pretraining) and contributions beyond Flamingo;
- tool use, external memory, planning, test-time compute and reasoning approaches beyond the single CoT and Toolformer examples;
- non-English, multilingual and non-Western contributions, deliberately sourced rather than appended as token examples.

Do not fill these gaps with model-release catalogues alone. Each candidate needs a primary or authoritative source, an accurate date convention, and a clear pedagogical reason to appear.

## First-release selection

The candidate inventory is now assessed in [history-milestone-selection.md](history-milestone-selection.md). That matrix proposes a focused core chronology, separates context/supplementary items, records ordinal decision criteria, and maps only to existing bilingual concept pages. GPT-2 now has separate source-backed research-announcement and staged-release records; its exact date semantics and careful capability wording still need final editorial review.

## Verification status

- **Source discovery:** completed for the candidate rows above using original papers, proceedings or official institutional records.
- **Bibliographic audit:** partial. Conference publication dates, arXiv submission dates and release dates still need consistent normalization.
- **Relation audit:** provisional but documented in [history-relation-audit.md](history-relation-audit.md).
- **First-release selection:** proposed in [history-milestone-selection.md](history-milestone-selection.md); not yet approved as final content.
- **Bilingual descriptions:** not yet drafted.
- **Internal concept links:** current EN/FR Quarto page inventory checked on the working branch; only existing destinations are proposed in the selection matrix.
- **Coverage balance:** incomplete, notably early statistical foundations, efficient inference, multimodal speech/audio/video, and multilingual/non-Western contributions.
- **Publication decision:** not yet made. Keep the existing page until the pilot has been reviewed and rendered.
