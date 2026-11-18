# ColBERT and ColBERTv2 — primary-source comparison

**Review date:** 2026-11-18  
**Owning issue:** [#1211](https://github.com/JM-Brun/llm-lab/issues/1211)

**Sources:** Khattab & Zaharia (SIGIR 2020), *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT* ([PDF](https://people.eecs.berkeley.edu/~matei/papers/2020/sigir_colbert.pdf), [DOI](https://doi.org/10.1145/3397271.3401075)); Santhanam et al. (NAACL-HLT 2022), *ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction* ([ACL Anthology](https://aclanthology.org/2022.naacl-main.272/), [PDF](https://aclanthology.org/2022.naacl-main.272.pdf), DOI 10.18653/v1/2022.naacl-main.272).

**Evidence boundary:** published PDFs and selected tables/figures were inspected. No code execution, checkpoint download, FAISS index construction, benchmark reproduction or repository audit is claimed.

## Executive synthesis

ColBERT occupies a useful middle ground between single-vector bi-encoders and cross-encoders. It independently encodes query and document into contextualized token vectors, stores document vectors offline, then compares the two sets at scoring time. For each query vector, MaxSim selects its maximum similarity to any document vector; the maxima are summed.

ColBERTv2 preserves this scoring architecture and improves two other parts: supervision (cross-encoder distillation and hard negatives) and storage (centroid plus quantized residual vectors). The reported storage gains are substantial but configuration-specific.

## 1. ColBERT (SIGIR 2020)

### Architecture and score

The paper contrasts representation-based single-vector scoring, interaction matrices, full cross-encoding and late interaction (§1, Figure 2). ColBERT independently encodes query and document into sets of contextualized token vectors. Its score is:

\[
S_{q,d}=\sum_{i=1}^{|E_q|}\max_{j=1}^{|E_d|} E_{q_i}\cdot E_{d_j}^{T}
\]

The output vectors are L2-normalized, so dot product equals cosine similarity. MaxSim selects the strongest document-token match for each query vector; summation aggregates query-side evidence.

The original implementation shares a BERT encoder between query and document inputs but uses distinct [Q] and [D] markers. Query augmentation pads short queries with mask tokens; document punctuation vectors are filtered. These are implementation decisions, not requirements for every late-interaction model.

### Indexing and retrieval

Document representations are computed and stored offline. The paper describes two deployment patterns:

1. **Reranking:** exhaustively compute MaxSim over a bounded candidate list, such as BM25's top 1,000.
2. **End-to-end retrieval:** index all document token vectors in FAISS, retrieve approximate nearest token vectors for each query vector, map them back to candidate documents, then refine the set with full MaxSim.

Thus ColBERT is not limited to reranking. Its token-level vector index can also generate first-stage candidates, but the first stage is approximate and depends on index/probe/candidate settings.

### MS MARCO results and measurement boundaries

On MS MARCO reranking (Table 1), ColBERT over BERT-base reports MRR@10 34.9 (dev/eval), 61 ms reranking latency and 7B FLOPs/query. The paper's BERT-base reference trained with its own pairwise loss reports MRR@10 36.0 on dev, 10,700 ms and 97T FLOPs/query.

For end-to-end retrieval (Table 2), ColBERT reports MRR@10 36.0 on dev and 36.7 on a local evaluation set, with 458 ms latency over the 8.8M-passage collection.

Do not collapse these into one speedup claim:
- reranking and end-to-end retrieval are different pipelines;
- baseline reranking latency excludes CPU preprocessing while ColBERT's stated reranking latency includes gathering/transferring document vectors and query processing;
- the local end-to-end evaluation set differs from the official reranking evaluation;
- measurements use 2020-era V100 / Titan V hardware.

## 2. ColBERTv2 (NAACL-HLT 2022)

### What changed

ColBERTv2 retains token-level late interaction and MaxSim (§3.1), but changes supervision and storage.

**Denoised supervision (§3.2).** An initial ColBERT model retrieves candidate passages. A 22M-parameter MiniLM cross-encoder teacher scores query-passage pairs. Training tuples contain 64 passages; KL-divergence distills teacher scores into ColBERTv2, with in-batch negatives and an index refresh. This is more than a compression-only revision: the supervision pipeline changes too. The authors note that hard-negative distillation increases training complexity and cost.

**Residual compression (§3.3).** Each token vector is represented by a nearest-centroid ID plus a quantized residual. For the paper's 128-dimensional setup, the stated encoding uses four bytes for the centroid ID and 16 or 32 bytes for a one- or two-bit-per-dimension residual, compared with 256 bytes for ColBERT's 16-bit vector representation. These are vector-payload figures, not a complete accounting of every index and serving resource.

**Retrieval (§3.4–3.5).** The index groups token-vector IDs by centroid. For each query vector, retrieval probes nearby centroids, decompresses nearby residual vectors and forms approximate MaxSim scores. Candidate passages are then loaded and rescored using all their vectors. Candidate generation is approximate; final scoring refines the candidate set.

### LoTTE and out-of-domain evaluation

The authors introduce LoTTE: 12 test sets across writing, recreation, science, technology and lifestyle. Each test set has 500–2,000 queries and 100k–2M passages. Search queries are derived from GooAQ and linked to StackExchange answer posts; forum queries are derived from StackExchange question titles and corresponding answers. The benchmark targets natural search queries over long-tail topics, complementing BEIR's heterogeneous but often semantic-relatedness-oriented tasks.

The paper evaluates models trained on MS MARCO on BEIR, Wikipedia Open QA and LoTTE. It reports ColBERTv2 highest on 22 of 28 out-of-domain tests. The BEIR comparison with SPLADEv2 is mixed: ColBERTv2 leads on six benchmarks, ties on two and trails on five. This argues against a simplistic claim that one retrieval family wins every task.

### Storage and limitations

On the MS MARCO index, the paper reports 154 GiB for ColBERT versus 16 GiB or 25 GiB for ColBERTv2 with one- or two-bit residuals, respectively, including 4.5 GiB for inverted lists. This is the reported 6–10× footprint reduction in that configuration. The paper gives query latency on the order of 50–250 ms in an appendix; this is not a universal serving guarantee.

The authors' own limitations:
- all benchmarks are English;
- out-of-domain models are trained on MS MARCO;
- IR judgments contain false negatives;
- annotation mechanisms differ between BEIR, LoTTE and Open-QA;
- cross-family comparisons may not be perfectly apples-to-apples because model families require different tuning;
- hard-negative distillation increases training complexity.

## 3. Comparison and integration decision

| Dimension | ColBERT (2020) | ColBERTv2 (2022) |
|---|---|---|
| Representation | Contextual token vectors | Same late-interaction representation |
| Scoring | Sum of query-token MaxSim | Same MaxSim principle |
| Index | Offline token vectors; FAISS IVFPQ retrieval | Centroid lists + quantized residuals |
| Candidate retrieval | Approximate token-vector search then full MaxSim refinement | Approximate centroid/residual generation then full MaxSim refinement |
| Supervision | Pairwise positive/negative training | Cross-encoder distillation, hard negatives, in-batch negatives |
| Main contribution | Late interaction between independently encoded token sets | Better supervision and smaller vector storage |
| Key caveat | Historical latency and index settings | English-only benchmarks, MS MARCO training domain, false negatives and configuration-specific compression |

Keep the existing single-vector / cross-encoder / late-interaction diagram and retrieval-family table. Add no new concept, route stage or registry. Ensure the lesson states:
- ColBERT vectors are contextualized token vectors, not one pooled sentence vector;
- MaxSim is the defining late-interaction aggregation;
- offline document encoding supports both first-stage retrieval and reranking;
- candidate generation can be approximate and final scoring refines the shortlist;
- ColBERTv2 changes supervision and compression, not the basic late-interaction principle;
- retrieval quality, recall, ranking metrics, index size, indexing cost and query latency are separate measurements.

## 4. Remaining work

- Audit released repositories and exact checkpoints only if reproducibility is needed; no implementation audit is claimed here.
- Audit complete ColBERTv2 benchmark appendices and compression ablations before using more granular comparisons.
- Continue with SPLADE and BEIR: contrast sparse vocabulary-level expansion with multi-vector late interaction, and inspect benchmark composition/metrics rather than cite aggregate rankings without context.
- Preserve both sources as partially-scanned until code/data/implementation dimensions are actually inspected.
