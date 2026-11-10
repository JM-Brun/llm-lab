# LLM history: relation audit and editorial decisions

**Status:** first-pass audit, 2026-10-31  
**Owner:** [issue #197](https://github.com/JM-Brun/llm-lab/issues/197)  
**Related documents:** [history data model](history-data-model.md) · [pilot sources](history-pilot-sources.md)

This audit converts the pilot's provisional relation hypotheses into conservative editorial decisions. It is not a claim that the history is complete. The goal is to prevent the visual genealogy from suggesting stronger causality, priority, or replacement than the evidence supports.

## 1. Relation decisions

| Candidate pair | Decision for the pilot | Rationale and required wording |
|---|---|---|
| Neural probabilistic language model (2003) → word2vec (2013) | **Do not draw an edge yet** | Both use distributed representations, but similarity of representation strategy is not enough to establish direct influence or a specific technical extension. Keep them in the same broad representation history, with no directed arrow until a primary-source lineage is documented. |
| Seq2Seq LSTM (2014) → Bahdanau attention (2014) | **Do not draw a directed edge** | Bahdanau et al. describe the fixed-length encoder–decoder vector as a bottleneck and introduce soft search over source positions. That is a problem/solution relationship in the encoder–decoder research context, but the two papers' 2014 dates are close and the current pilot does not establish a simple chronological parent-child relation. A neutral contextual link is safer. |
| Bahdanau attention (2014) → Transformer (2017) | **Keep as precursor_to, with a narrow rationale** | Learned attention for recurrent encoder–decoder translation is an important antecedent to later attention-based sequence modelling. It is not the same architecture or necessarily the same attention formulation as the Transformer. The edge must explicitly say “relevant antecedent”, not “invented Transformer attention” or “directly became the Transformer”. |
| Transformer (2017) → BERT (2018) | **Keep as applied_in** | BERT explicitly uses a bidirectional Transformer encoder. The event relation is an architectural application, while masked-language-model pretraining is a separate objective-level contribution. |
| Transformer (2017) → T5 (2019) | **Keep as applied_in** | T5 uses an encoder–decoder Transformer. Do not imply that it belongs to the decoder-only GPT lineage. |
| Scaling laws (2020) ↔ GPT-3 (2020) | **Use parallel_to only if useful; otherwise no edge** | The papers are contemporaneous contributions to the scaling-era discussion. The current evidence does not justify saying Kaplan et al. caused GPT-3 or that GPT-3 validates every allocation recommendation in the scaling-laws paper. |
| InstructGPT (2022) → DPO (2023) | **No direct edge in the first pilot** | DPO explicitly frames itself against RLHF workflows involving reward modelling and reinforcement learning, and proposes a different optimization formulation for preference data. That supports a shared problem-space or methodological comparison, but not by itself a direct lineage from the InstructGPT paper. Link both to the concept “preference-based alignment” instead. |
| Transformer (2017) → FlashAttention (2022) | **Use optimizes only if added to the vocabulary; otherwise applied_in is imprecise** | FlashAttention is an IO-aware exact attention algorithm designed for Transformer workloads. It changes the implementation and memory-traffic profile of attention, not the Transformer architecture or the mathematical definition of standard attention. Prefer a dedicated relation such as efficient_implementation_of if the vocabulary is deliberately extended; otherwise describe this in the event summary without a genealogy edge. |
| Transformer (2017) ↔ Mamba (2023) | **Keep alternative_to, but make the comparison scoped** | Mamba is presented as a selective state-space sequence-model architecture motivated partly by limitations of attention-based Transformers. It is an alternative backbone for sequence modelling, not a universal replacement and not a direct successor in a single lineage. |

## 2. Corrections to the pilot's chronology and labels

### Distinguish submission from publication

The pilot currently uses year-level dates for most papers. This is acceptable for the first display only if the date convention is visible and consistent. Before publishing day-level dates:

- store arXiv submission, conference publication, and public release as distinct date kinds;
- do not use an arXiv submission date as if it were the conference publication date;
- avoid ordering same-year contributions by guessed month/day;
- make the event detail panel expose the date kind and source.

The Bahdanau and Sutskever papers both belong to 2014, but the pilot should not infer a simple ordering from the year alone. Their relation is not required for understanding the later Transformer.

### Separate the technical layers

- **Architecture:** Transformer, BERT encoder, T5 encoder–decoder, Mamba state-space backbone.
- **Objective/training method:** masked language modelling, text-to-text denoising, RLHF, DPO.
- **Representation:** static word vectors, contextual representations.
- **Algorithm/implementation:** FlashAttention.
- **Empirical finding:** scaling laws.
- **Product/ecosystem:** ChatGPT public launch.

Do not place these in one undifferentiated “model evolution” chain. One event can touch multiple layers, but its primary type and significance tags must remain explicit.

### Avoid overstated claims

Replace or qualify the following formulations wherever they appear:

- “word2vec introduced embeddings” → it popularized efficient methods for learning static distributed word representations; distributed representations predate it.
- “Transformer introduced attention” → it proposed an attention-based architecture and removed recurrence/convolution from its central sequence computation.
- “BERT is a generative LLM” → BERT is an encoder-only bidirectional pretrained language model; its original objective is not left-to-right autoregressive generation.
- “FlashAttention reduces attention's quadratic complexity” → the original method computes exact attention and improves IO efficiency; the pairwise attention computation remains quadratic in sequence length.
- “DPO removes RLHF” → DPO is a preference-optimization formulation that avoids a separately trained reward model and an RL stage in its proposed procedure; it does not remove preference data or alignment trade-offs.
- “Mamba replaces Transformers” → Mamba is an alternative sequence-model backbone with different computational and representational trade-offs.

## 3. Relation vocabulary changes

Do not add a generic related_to edge: it has no explanatory value and makes the graph dense.

A possible efficient_implementation_of relation would clarify FlashAttention, but it should be added only if the project will also use it for other kernel/algorithm milestones. Otherwise keep the relation vocabulary stable and represent FlashAttention's connection in its summary and concept tags.

The current precursor_to definition should remain distinct from influenced:

- precursor_to: a technically relevant earlier formulation or component, without claiming documented direct influence;
- influenced: a direct lineage supported by citation, author statement, or other explicit evidence.

For parallel_to, require a rationale that identifies what is parallel (problem, objective, or research period), not merely that two dates are close.

## 4. Recommended pilot graph

The first release should be deliberately sparse:

1. Bahdanau attention → Transformer (precursor_to), with the caveat above.
2. Transformer → BERT (applied_in).
3. Transformer → T5 (applied_in).
4. Transformer ↔ Mamba (alternative_to), with the comparison scoped to sequence-model backbones.
5. Optionally show Kaplan scaling laws and GPT-3 in the same “scaling” era without a directed edge.
6. Optionally connect InstructGPT and DPO to a shared preference-alignment concept, not directly to each other.
7. Show FlashAttention as an implementation/efficiency milestone attached to the attention concept, not as a new architecture node.

A sparse, explainable graph is preferable to a visually impressive but historically misleading network.

## 5. Evidence checked in this pass

- Bahdanau et al., [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473): abstract describes the fixed-length encoder–decoder bottleneck and soft search over source positions.
- Sutskever et al., [Sequence to Sequence Learning with Neural Networks](https://research.google/pubs/sequence-to-sequence-learning-with-neural-networks/): describes an LSTM encoder mapping an input sequence to a fixed-dimensional vector and an LSTM decoder.
- Dao et al., [FlashAttention](https://arxiv.org/abs/2205.14135) and [NeurIPS proceedings record](https://papers.nips.cc/paper_files/paper/2022/hash/67d57c32e20fd0a7a302cb81d36e40d5-Abstract-Conference.html): characterize the method as IO-aware exact attention using tiling to reduce memory reads/writes.
- Rafailov et al., [Direct Preference Optimization](https://arxiv.org/abs/2305.18290) and [NeurIPS proceedings record](https://papers.nips.cc/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html): explicitly compare DPO with reward-model-plus-RL preference optimization.
- Mamba, [Selective State Spaces](https://arxiv.org/abs/2312.00752): primary paper required for final wording and exact relation rationale; this pass does not treat later survey claims as primary evidence.

## 6. Remaining verification before publication

- [ ] Read the full primary papers, not abstracts alone, for every relation retained in the final graph.
- [ ] Audit the GPT-1/GPT-2 generative-pretraining line and Chinchilla before claiming a balanced account of scaling and autoregressive LMs.
- [ ] Add pre-neural statistical language modelling, recurrent language modelling, and LSTM origins with primary sources.
- [ ] Add tokenizer/subword history, including BPE's NLP adoption, without confusing its earlier compression origins with its later NLP use.
- [ ] Audit LoRA/QLoRA, MoE, GQA/KV cache, multimodal models, RAG, tool use, and reasoning-time compute.
- [ ] Include a deliberate search for contributions outside the usual US/UK institutional and English-language publication narrative.
- [ ] Check every internal link against the actual bilingual page inventory.
- [ ] Only then encode a bilingual pilot dataset and render the chronology/genealogy prototype.

**Publication gate:** this audit is a conservative editorial decision record, not approval to publish the graph. The public view remains blocked on source-level verification, coverage balance, bilingual records, and rendered accessibility review.
