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

## 5. Remaining work — staged plan

The two headline papers and their official repositories have now been inspected, and four atomic extraction records have been created. The remaining work is no longer a generic “read more” list: it is split into distinct closure, validation, comparison and integration gates. Do not reopen completed research tasks unless a later audit finds a concrete discrepancy.

### Gate A — close the newsletter scan (source completeness)

**Status: blocked by source access; highest remaining ingestion priority.**

- [ ] Retry the canonical Substack article and the inbox alias through an authenticated/alternate retrieval path, without treating the alias as a second source.
- [ ] If the full newsletter remains inaccessible, record that limitation as final for this scan and use the contents list only as a discovery queue.
- [ ] Triage the 13 discovered references individually before creating source records: DICE speculative decoding; ScopeAct; hierarchical task planning; UniEvo-VL; NoiseRater; MemLife; EMA Policy Gradient; Mixture of Latent Recursions; scientific-discovery/monofact analysis; massive activations in hybrid linear-attention LLMs; StereoVLM; Generalist Action Critic; La-JEPA.
- [ ] For each candidate, record a decision (ingest / defer / reject), a canonical primary-source URL, relevance to LLM Lab, and a short rationale. Ingest only those with a clear project fit; do not turn the newsletter table of contents into 13 automatic ingestion obligations.
- [ ] Update the newsletter's `scan_status` only when the actual inspection scope supports the change. The two headline papers being fully reviewed does not make the newsletter fully scanned.

**Acceptance:** every item visible in the newsletter contents has an explicit disposition; any uninspected item remains clearly marked as discovered/deferred, never as reviewed.

### Gate B — validate the ingestion artefacts (technical integrity)

**Status: latest commit-associated CI, Quarto site and secret-scanning runs are successful; catalogue-specific semantics still deserve a targeted check.**

- [ ] Run the repository's existing source-catalogue and extraction validators against `data/sources.yml` and the four new extraction files; do not create a new workflow just for this ingestion.
- [ ] Check controlled vocabularies, required fields, unique source IDs, canonical URLs/aliases, extraction item IDs, source locators, and consistency between each source's `related.audit_records` and the files that exist.
- [ ] Confirm that `method`/contribution tags and source types use the repository's current allowed values; do not silently broaden the schema to accommodate one source.
- [ ] Verify that the 1,313× statement is consistently scoped to 32.05 GB active GPU cache versus 25.0 MB active cache in the Qwen3.5-4B 1M-context repository table, while retaining the 640 MB offloaded pool. Keep the paper's separate 144 GB comparison distinct.
- [ ] Confirm that licence statements are scoped to the two repositories' code only, not automatically to checkpoints, base models, datasets, benchmark assets or dependencies.

**Acceptance:** existing validators pass; source/extraction references resolve; no unsupported status or licence claim is introduced. CI success is recorded separately from semantic catalogue validation.

### Gate C — compare against the existing LLM Lab knowledge model (no page edits yet)

**Status: not started as a systematic page-by-page audit.**

- [ ] For MemOnce, inspect the existing bilingual material and graph around KV cache, long context, YOCO/cross-layer sharing, linear attention, recurrent state, RAG/retrieval and persistent memory. Reuse the relevant work already tracked in #765, #1237 and the canonical computational spine #575.
- [ ] Compare the three memory quantities explicitly in the conceptual model: expandable persistent/offloaded bank; bounded active retrieved state; layer-specific KV tensors materialized for attention. Check whether current pages distinguish them or collapse them under “KV cache”.
- [ ] For Model Carving, inspect the existing material on model compression, structured pruning, layer dropping, architecture search, distillation and compute-aware training. Keep it distinct from token pruning (#1136), unstructured weight sparsity and inference-time dynamic routing.
- [ ] Use the project's semantic concept IDs and relation conventions. Do not create placeholder IDs, duplicate existing concepts, or force either paper into the #575 computational spine if it is only a neighbouring architectural concern.
- [ ] Produce a compact comparison matrix: existing page/concept → supported overlap → genuinely new distinction → evidence locator → proposed action (reuse / clarify / cross-link / new concept / no change).

**Acceptance:** every proposed addition is justified by a demonstrated gap in the current knowledge model; “paper introduces a term” is not sufficient justification.

### Gate D — decide and implement learner-facing integration (separate change)

**Status: deliberately deferred from this ingestion PR.**

- [ ] Make an explicit editorial decision for each paper after Gate C. Prefer extending an existing lesson over creating a new page.
- [ ] If MemOnce adds a useful learning contribution, integrate the lifecycle and memory-accounting distinctions into the appropriate inference/long-context/KV-cache material, with a precise comparison to existing approaches.
- [ ] If Model Carving adds a useful learning contribution, place it with training-time architecture optimization/model compression; explain the compute-budget objective and static resulting topology without implying dynamic inference routing.
- [ ] Update FR and EN counterparts together, then update the knowledge graph, learning map and relevant routes only where the new relationships are pedagogically meaningful.
- [ ] Keep exercises and questions in the separate “Practice & experiment” area rather than expanding the main explanatory pages with a growing exercise bank.
- [ ] Preserve source attribution and figure/code reuse boundaries. Link to figures when rights are unknown; do not copy assets by default.

**Acceptance:** a separate, reviewable PR contains only justified learner-facing changes, with bilingual parity, correct graph relations and working navigation.

### Gate E — optional reproducibility follow-up (not a prerequisite for source ingestion)

- [ ] If a concrete implementation-learning objective emerges, create a small, isolated smoke-test plan for each repository using its documented environment; do not download large checkpoints or datasets by default.
- [ ] For MemOnce, distinguish inference-path smoke testing from reproducing 1M-context memory/latency/throughput claims.
- [ ] For Model Carving, distinguish code-path validation from reproducing long training runs and hardware throughput claims.
- [ ] Record hardware, software versions, model/checkpoint provenance, dataset licences, memory accounting and deviations. Never relabel author-reported results as independently reproduced.

**Acceptance:** any experiment is reproducible and narrowly scoped; otherwise the work remains explicitly paper/code inspection only.

### Recommended execution order

1. **B first:** validate the artefacts already committed, since this can close the ingestion PR without waiting for Substack access.
2. **A in parallel as source discovery:** recover the newsletter if possible; otherwise disposition the 13 references and close the access limitation honestly.
3. **C next:** perform the comparative audit against existing pages and the canonical knowledge graph.
4. **D only after C:** open a separate integration PR if a real pedagogical gap remains.
5. **E only on demand:** do not make reproduction a hidden prerequisite for documenting the papers.

The ingestion PR should not absorb Gates C–E. Its scope is source registration, evidence extraction and a trustworthy audit trail; learner-facing architecture changes belong in a subsequent, smaller change.

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


## 7. Official Model Carving implementation inspection

The authors' [official GitHub repository](https://github.com/KadenZheng/model-carving) was inspected. Its README specifies Python 3.11 with JAX 0.9.0.1, Flax 0.12.2 and Optax 0.2.7; the repository declares an MIT licence (including attribution to the MIT-licensed Theseus portions). It provides standard and looped configurations matching the paper's stated scale ranges and uses one training entry point with a dense baseline mode and a --carving mode.

Implementation details inspected:
- carving/carver.py computes each sublayer's FLOP share, estimates pressure from the remaining token budget and fitted end-of-run learning rate, applies gate updates, and schedules graph removal;
- carving/gates.py implements Adam gate moments, the logarithmic pressure slope using ln(20), and clipping at zero;
- carving/budget.py accounts for attention, MLP, readout and learned-connection FLOPs;
- carving/residual.py implements gated residual writes and learned cross-layer/loop connections;
- carving/rate.py implements the learning-rate snapshots and power-law fit.

A useful nuance from the code: a gate reaching zero schedules removal; the graph is changed at the scheduled removal point. A pending removal can be cancelled if the gate reopens before that point. The topology is frozen for cooldown. This is more precise than describing every zero crossing as immediate permanent deletion.

No environment was installed and no training or benchmark was run. The code inspection therefore supports implementation traceability, not independent reproduction. The repository and extraction are registered as `kaden-zheng-model-carving-implementation` and `data/extractions/kaden-zheng-model-carving-implementation.yml`.
