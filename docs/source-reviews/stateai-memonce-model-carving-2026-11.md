# State of AI — Model Carving and MemOnce: source audit

**Date:** 2026-11-27  
**Newsletter:** [State of AI, 23 November 2026](https://stateai.substack.com/p/self-pruning-transformers-memonce-memory-cache)  
**Inbox alias:** [Substack inbox item 226235776](https://substack.com/inbox/post/226235776) (same newsletter, not a separate source)  
**Primary papers:** [Model Carving, arXiv:2611.27962v1](https://arxiv.org/abs/2611.27962) · [MemOnce, arXiv:2611.27973v1](https://arxiv.org/abs/2611.27973)

## Inspection status

The indexed newsletter result exposed the title, introduction, headline summary and contents list naming 15 research items. Direct retrieval of the Substack page returned a cache miss. The two headline papers were inspected from their full v1 text, including equations, architecture figures, experimental sections, appendices and author-stated limitations. This is a primary-source audit of those two papers, **not a complete scan of the newsletter**.

The other 13 entries remain discovered references only. Their titles/topics must not be treated as reviewed evidence or silently extracted from the table of contents.

## 1. MemOnce — technical reconstruction

The paper contrasts standard Transformer layer-wise, token-level KV caches (O(LND) state and quadratic full-attention prefill), fixed-state recurrent/linear architectures (bounded state but possible loss of fine detail), cross-layer sharing such as YOCO (removes depth factor but remains sequence-length dependent), and external memory stores.

It formalizes continual generation as:
[
pi_	heta(y_tmid x_t,x_{1:t-1}) =
pi_	heta(y_tmid x_t,M_t),quad
M_t=f_	heta(x_t,x_{1:t-1}).
]
This is the authors' unifying formulation, not proof that all memory systems implement the same mechanism.

The implementation has three operations:
[
G_t=g_	heta(x_{1:t-1}),qquad
M_t=i_	heta(x_t,G_t),qquad
C_t=u_	heta(M_t).
]
The encoder writes compact states to a persistent bank; indexing retrieves the active subset; the decoder materializes per-layer KV caches.

### Memory encoder-decoder

For each processed segment, the model produces final-layer hidden states. It retains the trailing 1/r fraction (example r=8) and concatenates them into one global bank. Layer-specific lightweight MLP projections reconstruct each attention layer's keys and values:
[
K^l=K^l_{mathrm{Proj}}(M_t),quad
V^l=V^l_{mathrm{Proj}}(M_t).
]
This avoids storing separate historical KV tensors at every layer and avoids forcing every layer to share identical K/V representations.

### Memory sparse attention

The persistent bank is split into a recent short-term window and a long-term pool. The query representation is projected and L2-normalized; cosine similarity selects top-K long-term entries. Those entries are concatenated with the short-term window. Retrieval happens once per continual input and the selected memory is reused across attention layers and subsequent decoding steps.

The active subset is bounded by C, so active state is O(CD), independent of context length and depth under the fixed-budget assumption. The persistent bank G_t remains expandable and may be offloaded to CPU or SSD. **Constant active GPU state is not constant total storage.**

### Backbone and optimization

The default backbone is hybrid: each stage interleaves three linear blocks (e.g. GDN) with one Memory Sparse Attention block. During pretraining, backbone and memory encoder-decoder are jointly optimized. During post-training adaptation, the backbone is frozen; indexing/decoding projections and LoRA adapters used during memory encoding are optimized.

### Evaluation and results

Evaluation includes WikiText/LAMBADA perplexity, zero-shot tasks, memory benchmarks (MemBench, LoCoMo, LongMemEval, PersonaMem), general-capability retention (MMLU, GSM8K, GPQA), and representation transfer.

For Qwen3.5-4B at one-million-token context, the paper reports 25 MB memory-state cache versus 144 GB for standard Transformer in Figure 1, 6.9× lower prefill latency, 3.5× throughput, and 60.07% overall memory benchmark performance versus 54.30% for the full-context baseline. These figures are specific to the authors' setup. The cache metric is not total system memory or the entire persistent bank.

Additional reported results: overall Recall@10 69.21 and NDCG@10 53.06 across eight retrieval/reranking datasets. Ablations report less than 0.3% accuracy loss from r=1 to r=8, K=64 as the best tested balance, and single-shot indexing 12× faster than M+ and 17× faster than RAG-Rewrite. These results have not been independently reproduced.

## 2. Model Carving — technical reconstruction

Model Carving jointly trains weights, scalar nonnegative gates on sublayer outputs, and learned residual connections. The initial network is overparameterized. A compute-aware pressure estimates the loss reduction that saved FLOPs could buy as additional training tokens under a fixed training-compute budget.

The training objective adds a pressure term for each active sublayer. Pressure is estimated online from the learning curve. A logarithmic gate penalty compares a sublayer's quality contribution with the compute value; a gate reaching zero is clipped to zero. The trainer periodically compiles a smaller graph without zero-gated sublayers and switches to it later.

The final inference model is a **static heterogeneous Transformer**. There is no per-token routing or dynamic gate decision at inference. Retained attention applications still use ordinary KV caches.

### Reported experiments

- Standard Transformers: 140M–2.7B parameters.
- Looped Transformers: 140M–1.3B.
- At equal training compute, carved models reportedly reach validation loss that full-depth baselines need up to 1.7× compute to match.
- Up to 34% fewer inference FLOPs per token.
- Up to 1.61× decode throughput in largest-batch H100 measurements at 4,096-token context.
- Downstream comparisons include CORE-22 and five generative tasks; equal-inference comparisons allow more samples from the carved model.

These are study-specific maxima and comparisons, not general expected speedups.

### Limitations acknowledged by authors

- Scale limited to 2.7B standard and 1.3B looped models.
- Pruning pressure does not model learning-rate cooldown; authors report 10–16% less gain from cooldown than dense models.
- Most pruning happens in the first 20% of training and relies on the prior.
- Gate initialization and ln(20) margin are fixed hyperparameters.
- Larger scales, longer training, other data, uncertainty-aware predictors and dynamic reinsertion remain future work.

## 3. Cross-paper distinction

| Dimension | Model Carving | MemOnce |
|---|---|---|
| Lifecycle | Training | Continual inference, plus adaptation |
| Object changed | Network topology | Historical memory representation and access |
| Mechanism | Compute-aware sublayer gates | Compact state encoder, retrieval, KV decoder |
| Runtime | Static graph | Query-conditioned retrieval |
| KV cache | Retained for active attention | Reconstructed on demand for retrieved memory |
| Objective | Quality under training-compute budget | Recall and inference scalability over long histories |

Do not merge these under a generic pruning/compression concept. Their optimization targets, lifecycle and execution behavior differ.

## 4. LLM Lab placement

- **MemOnce:** extend existing KV-cache / inference / long-context material only after comparison with YOCO, LastKV, linear attention, RAG and persistent-memory concepts. The key distinction is persistent bank vs bounded active state vs decoded layer KV cache.
- **Model Carving:** connect model compression and pruning to architecture search and compute-aware training. Explain the pressure derivation only if the training-optimization pathway supports the mathematics.
- **No new canonical concept IDs yet:** existing concepts cover the current mapping; concept additions require a separate ontology review.
- **No learner-facing page edits in this ingestion PR:** this PR records sources and evidence. A page integration should be a subsequent scoped change after the existing lessons and graphs are audited.

## 5. Remaining work

- [ ] Retrieve and inspect the complete newsletter body and all 15 linked items; record each as reviewed, deferred or rejected.
- [ ] Inspect official project/code repositories for both papers, implementation availability, licences and reproducibility instructions.
- [ ] Independently verify benchmark arithmetic, hardware, memory accounting and model configurations.
- [ ] Compare MemOnce against existing lessons on KV cache, YOCO/cross-layer sharing, linear attention, retrieval and persistent memory.
- [ ] Compare Model Carving against existing pruning, architecture-search and model-compression material.
- [ ] Decide whether new concepts are justified only after canonical concept and graph review.
- [ ] Run source catalogue/extraction validators and open a separate integration PR if warranted.

## Evidence boundary

Primary evidence: arXiv v1 PDFs, inspected 2026-11-27. Newsletter: indexed search extract; canonical page inaccessible to direct retrieval. No code was run and no experimental result independently reproduced. Figures are described, not copied. Reuse rights remain unknown.


## 6. Official MemOnce implementation inspection

The authors' [official GitHub repository](https://github.com/Clare-Nie/MemOnce) was inspected after the paper audit. It declares Apache-2.0 for the repository code and provides pretraining and post-training implementations, evaluation scripts, a released checkpoint, and a Qwen3.5 inference path.

The post-training inference implementation makes the write/read cycle concrete:

- Historical turns are tokenized and split into segments of at most 4,096 tokens.
- The default post-training configuration writes one 64-token memory block per segment.
- A FIFO short state holds up to 1,024 tokens (16 blocks at 64 tokens each).
- Retrieval keys are computed for memory blocks; the answer path retrieves up to 64 long-term blocks and combines them with the short state.
- The retrieved representation is decoded into memory KV caches before generation.
- The released checkpoint README describes approximately 71M trained parameters (LoRA write adapter, KV readout projections and mem_to_emb), loaded alongside the Qwen3.5-4B base model.

The repository README's own 1M-context table reports:
- Qwen3.5-4B full-context baseline: 32.05 GB active GPU cache;
- MemOnce: 25.0 MB active GPU cache plus a 640.0 MB offloaded pool;
- MemOnce prefill: 41.36 seconds; decoding: 29.3 tokens/second.

This clarifies the operational meaning of the headline: **1,313× is the active GPU cache reduction against the 32.05 GB Qwen3.5-4B baseline, while the 640 MB offloaded pool remains part of memory accounting.** The 144 GB standard-Transformer point shown in the paper's architecture comparison is a separate baseline/measurement and should not be substituted into this ratio.

The repository's Apache-2.0 licence applies to the repository code. It does not automatically grant rights to the Qwen base model, downloaded checkpoint, datasets, benchmark assets or third-party dependencies. No checkpoint was downloaded, no environment installed, and no inference or benchmark was run; implementation inspection is not independent reproduction.

The implementation source and its extraction are registered separately as `clare-nie-memonce-implementation` and `data/extractions/clare-nie-memonce-implementation.yml`.
