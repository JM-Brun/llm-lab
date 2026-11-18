# Cross-graph scientific pilot: attention, information theory and compression

**Date:** 2026-11-18  
**Status:** repository-grounded inventory and manual traversal review; not yet an automated cross-graph benchmark or a fresh execution of the experiments.  
**Parent tracking:** [#1233](https://github.com/JM-Brun/llm-lab/issues/1233) · [scientific pilot #1237](https://github.com/JM-Brun/llm-lab/issues/1237)

## Purpose and method

This pilot checks whether existing canonical structures can be traversed without flattening their semantics. It reuses the concept registry, computational graph, source catalogue, source extractions, bilingual page/resource associations, syntheses and experiment protocols. It does not create a graph, ontology, source record, concept or experiment.

The review is a static inspection of the current `main` content on 2026-11-18. Exact locators below are taken from the source extraction/review records. Experiment outputs are cited as repository-documented outputs; they were not rerun in this pass. A path described as a *manual join* is not evidence that a query engine or first-class cross-graph edge already exists.

## Canonical owners and real endpoints

| Structure | Canonical owner | Relevant real IDs / records | What it owns |
|---|---|---|---|
| Concept graph | `data/concepts.yml` | `query`, `key`, `value`, `self-attention`, `attention-score`, `attention-weight`, `scaled-dot-product-attention`, `softmax`, `entropy`, `cross-entropy`, `kl-divergence`, `mutual-information`, `predictive-compression`, `entropy-coding`, `arithmetic-coding`, `model-compression`, `quantization` | Bilingual concept definitions, domains, resources and typed concept relations |
| Computational graph | `data/computational-graph.yml` | `query-projection`, `queries`, `key-projection`, `keys`, `value-projection`, `values`, `attention-score-computation`, `attention-scores`, `masked-attention-scores`, `attention-softmax`, `attention-weights`, `value-aggregation`, `attention-output`, `token-nll`, `sequence-log-likelihood`, `kv-cache` | Computation/dataflow and operational dependencies; not scientific claims |
| Source catalogue | `data/sources.yml` | `vaswani-et-al-attention-is-all-you-need-2017`, `dao-et-al-flashattention-2022`, `xu-et-al-usable-information-2020`, `wayland-zhang-information-theory-llm-2026` | Bibliographic identity, scan/integration state, related pages/concepts and audit references |
| Source evidence | `data/extractions/<source-id>.yml` | `vaswani-et-al-attention-is-all-you-need-2017:scaled-dot-product-attention`; `dao-et-al-flashattention-2022:exact-io-aware-attention`, `:online-softmax-tiling`, `:io-complexity`, `:block-sparse-extension`; Xu source-local nodes and items | Source-located claims/definitions and source-local pedagogical reconstruction |
| Pedagogical pages | `site/fr/*.qmd`, `site/en/*.qmd` via source `related.pages` and concept `resources` | `fr/scaled-dot-product-attention`, `en/scaled-dot-product-attention`, `fr/entropy`, `en/entropy`, `fr/cross-entropy`, `en/cross-entropy`, `fr/compression-revision`, `en/compression-revision` | Learner-facing explanations; not evidence owners |
| Experiments | `experiments/**` | `attention_kl_vs_mutual_information.py`, `run.py`, `compression.py`, `experiments/predictive-compression/` | Reproducible computational checks; not primary-source evidence |
| Synthesis/reviews | `docs/source-syntheses/**`, `docs/source-reviews/**` | Information-theory, two meanings of compression, model-compression, Vaswani and FlashAttention reviews | Editorial synthesis and scoped interpretation; not replacements for sources |

### Important source-state caveat

The Vaswani record is still `partially-scanned`; its 2026-11-18 scan explicitly covers §3.2.1 and Equation (1), not the entire paper. The FlashAttention record is also `partially-scanned`; its scan covers the abstract and selected sections 2.2, 3.1–3.3 and selected Section 4 claims. Those limits must travel with any evidence path.

## Five manually reviewed traversal cases

### P1 — Attention concept → computation → primary mathematical definition

**Path:** `scaled-dot-product-attention` / `attention-weight` → computational nodes `attention-score-computation` → `attention-softmax` → `attention-weights` → extraction item `vaswani-et-al-attention-is-all-you-need-2017:scaled-dot-product-attention` → §3.2.1, Equation (1).

**What is supported:** scaled dot-product attention computes (QK^T/\sqrt{d_k}), applies softmax across keys for each query, and uses the resulting weights to aggregate values. For a fixed query and finite admissible key set, the softmax row is a normalized non-negative distribution. Shannon entropy can be computed on that row as a scoped derived statistic.

**Limits:** this source item does not define mutual information, semantic relevance, causal importance or a compression code. The exact source review says so explicitly. The canonical concept and computational node are not evidence in themselves; the extraction item and paper locator are.

**Evidence:** `data/extractions/vaswani-et-al-attention-is-all-you-need-2017.yml`, item `...:scaled-dot-product-attention`, locator §3.2.1; `docs/source-reviews/vaswani-attention-formulation-2026-11.md`.

### P2 — Mathematical attention → IO-aware implementation

**Path:** `scaled-dot-product-attention` → computational attention operations → source `dao-et-al-flashattention-2022` → extraction `exact-io-aware-attention` / `online-softmax-tiling` → Abstract and §§3.1–3.2, Algorithm 1, Theorems 1–2 and Proposition 3.

**What is supported:** FlashAttention is an IO-aware tiled algorithm for exact dense attention. Online softmax statistics and weighted-value accumulators are merged across blocks. The paper's IO complexity concerns HBM accesses under a two-level memory model; exactness does not imply bitwise-identical floating-point results.

**Limits:** exact dense FlashAttention retains (O(N^2d)) arithmetic FLOPs. The paper's block-sparse extension is a separate approximate algorithm (§3.3, Proposition 4). HBM traffic, peak memory, latency and throughput are separate quantities. “Memory-efficient” here is not Shannon source coding.

**Evidence:** `data/extractions/dao-et-al-flashattention-2022.yml`, items `exact-io-aware-attention`, `online-softmax-tiling`, `io-complexity`, `block-sparse-extension`; `docs/source-reviews/flashattention-primary-paper-2022.md`.

### P3 — Attention-weight statistics → information theory, with a negative control

**Path:** `attention-weight` / `softmax` → entropy and KL concepts → `experiments/information-theory/attention_kl_vs_mutual_information.py` → information-theory synthesis → bilingual attention/entropy resources.

**What is supported:** row-wise KL to a uniform reference and mutual information are different quantities. Mutual information requires a joint distribution and its marginals. The repository experiment constructs an explicit joint distribution for MI and contrasts it with row-to-uniform KL; the synthesis records a concrete counterexample and the interpretive boundary.

**Limits:** attention weights are not automatically calibrated conditional probabilities over random variables. An attention row alone does not supply a joint distribution. No semantic or causal interpretation follows from concentration alone.

**Evidence:** `docs/source-syntheses/information-theory-and-llms-2026-11.md` (especially its inspection caveat and “Attention et information mutuelle” section); `experiments/information-theory/attention_kl_vs_mutual_information.py`; `experiments/information-theory-llm/README.fr.md`. The source synthesis reports the linked notebook was statically inspected but not executed.

### P4 — Predictive log-loss → ideal code length → finite exact coding

**Path:** `cross-entropy` / `negative-log-likelihood` → `predictive-compression` → `entropy-coding` / `arithmetic-coding` → `experiments/predictive-compression/` → documented exact decode check.

**What is supported:** for a specified model assigning conditional probabilities to a sequence, the ideal predictive cost is the sum of (-\log_2 p(x_t\mid context)). The existing bigram experiment turns those probabilities into arithmetic-coding intervals and decodes the finite message exactly. The README documents a 19.642-bit ideal cost, 21-bit finite code and exact reconstruction for its fixed synthetic example.

**Limits:** this is a synthetic bigram example, not a neural network or LLM benchmark. The decoder is assumed to share the model, message length and conventions; model-training and metadata costs are excluded. The example does not prove that prompting or generation is lossless decompression.

**Evidence:** `experiments/predictive-compression/README.fr.md` (documented output and limits); `docs/source-syntheses/compression-two-meanings-2026-11.md`; concepts in `data/concepts.yml`.

### P5 — Predictive information → restricted model family → canonical concepts

**Path:** `mutual-information` / `cross-entropy` → source `xu-et-al-usable-information-2020` → source-local definitions `src-predictive-family`, `src-predictive-v-entropy`, `src-v-information` → extraction item `predictive-family-definition` and subsequent V-information items → bilingual experiment guide.

**What is supported:** predictive V-information is relative to an explicitly specified predictive family and logarithmic loss. Its relationship to Shannon mutual information depends on the unrestricted-family special case; it is not a universal synonym. The extraction keeps its source-local teaching model distinct from the canonical concept graph.

**Limits:** the source-local `src-` nodes are not canonical concept IDs and must not be promoted automatically. The project XOR example is a finite exact population calculation, not a reproduction of the paper's high-dimensional experiments or PAC guarantee.

**Evidence:** `data/extractions/xu-et-al-usable-information-2020.yml`, source-local graph and item locators (Definitions 1–3, Theorem 1); `data/sources.yml` source record; `experiments/information-theory-llm/README.fr.md`.

## Negative and ambiguous bridge benchmark

| Candidate | Decision | Reason |
|---|---|---|
| Attention-row entropy → entropy of that specified normalized row | Accept, scoped mathematical derivation | Requires fixed query/head/layer/input/mask/key support |
| Attention-row entropy → mutual information | Reject as equivalence | No joint distribution and marginals are supplied by a row |
| Row-to-uniform KL → mutual information | Reject | Different reference distributions and mathematical objects; existing experiment is a counterexample |
| FlashAttention → IO-aware exact dense implementation | Accept, implementation mapping | Primary paper and exact algorithm/complexity locators exist |
| FlashAttention → information-theoretic compression | Reject | HBM traffic/intermediate storage is not a lossless source code |
| Autoregressive NLL → ideal predictive code length | Accept under coding assumptions | Requires specified conditional model, log base, shared decoder/model and protocol |
| Quantized checkpoint → compressed input corpus | Reject as category error | Model representation and source data are different objects |
| KV cache → checkpoint compression | Reject as category error | Runtime state and persistent model weights are distinct |
| Concentrated attention → semantic relevance / causal importance | Unresolved; do not assert | Requires separate operational definition and causal/behavioral evidence |

This is a reviewed hand-curated candidate set, not a precision benchmark for an automated discovery system. No automated recommendations are being advertised.

## Coverage and missing links

| Acceptance check | Current result |
|---|---|
| Five real cross-structure paths | Five manually traced paths above; not yet machine-queryable |
| Exact evidence locators | Present for Vaswani, Dao and Xu; experiment README/script locations for reproducible examples |
| At least three rejected bridges | More than three explicitly rejected above |
| Bilingual learner-facing endpoints | FR/EN attention, entropy, cross-entropy and compression revision resources are registered |
| Independent corroboration | Not counted from duplicated pages/syntheses; primary source roles are stated |
| Automated deterministic traversal | Not implemented or tested by this pilot |
| Selective invalidation | Not tested |
| Fresh experiment execution in this pass | Not performed |
| Rendered page parity | Resource registrations are bilingual; rendered FR/EN narrative parity has not been re-audited here |

The source-to-extraction path is strongest for Vaswani and Dao. The information-theory synthesis documents the Wayland notebook inspection, but the source-specific extraction filename was not confirmed in this pass; do not invent it or use it as a locator. The experiment path for predictive compression has a documented exact output, but no new run was performed. These are explicit gaps, not reasons to create substitute records.

## Decisions and next work

1. Keep the current canonical owners and graph vocabularies. No new schema or global bridge registry is justified by this pilot.
2. If a machine-readable traversal is implemented, derive its joins from existing IDs and relationships; retain edge category, source status, locator, assumptions and limitations in the returned path.
3. Add a small deterministic test fixture for the nine candidates above only after choosing the existing validator/test owner. Include accepted, rejected and unresolved cases.
4. Test bilingual rendered page parity separately from metadata/resource registration.
5. Re-run the existing experiment commands and tests in CI or a controlled local environment, recording exact commit, interpreter/dependencies and outputs.
6. Extend the same protocol to compression/model deployment only after checkpoint size, predictive quality, peak runtime memory, HBM traffic, latency, throughput and bits/token are separately defined.

**No new canonical concepts, relations, source records or experiment claims are proposed by this report.**
