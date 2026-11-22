# Cross-graph scientific pilot: attention, information theory and compression

**Initial inventory:** 2026-11-18  
**Follow-up review:** 2026-11-22  
**Status:** repository-grounded manual traversal review, with five deterministic regression tests covering the attention evidence path, KL/MI counterexample, FlashAttention IO scope, predictive-coding evidence and the V-information source-local boundary. This is not a general cross-graph query benchmark or a neural-LLM compression reproduction.  
**Parent tracking:** [#1233](https://github.com/JM-Brun/llm-lab/issues/1233) · [scientific pilot #1237](https://github.com/JM-Brun/llm-lab/issues/1237)

## Purpose and method

This pilot checks whether existing canonical structures can be traversed without flattening their semantics. It reuses the concept registry, computational graph, source catalogue, source extractions, bilingual page/resource associations, syntheses and experiment protocols. It does not create a graph, ontology, source record, concept or experiment.

The initial inventory was made against `main` on 2026-11-18. This follow-up rechecked the P4/P5 source extractions, source scan states, experiment code and tests on 2026-11-22. Exact locators below come from the repository's extraction records. Unit tests execute both coding CLI entry points through `main()` and check the deterministic finite-code report and exact round trip; no neural LLM experiment or natural-language corpus reproduction is claimed. A path described as a *manual join* is not evidence that a query engine or first-class cross-graph edge already exists.

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

**Path:** canonical concepts `cross-entropy` / `negative-log-likelihood` → `predictive-compression` → `entropy-coding` / `arithmetic-coding` → primary-source extraction items from Shannon and Rissanen → `experiments/predictive-compression/` → unit tests and exact decoder checks.

**What is supported:**
- For a specified autoregressive model and a fixed sequence, the ideal predictive cost in bits is the sum of token surprisals, `-log2 p(x_t | context)`. This is a model-dependent ideal length, not automatically the size of a finite file.
- Shannon's `noiseless-channel-coding-theorem` extraction records the asymptotic entropy-limited rate and a finite-block construction with integer code lengths. It does not claim that a finite implementation has exactly the real-valued sum of NLLs as its bit count.
- Rissanen's `probability-derived-ideal-length` extraction connects symbol ideal lengths to negative log-probabilities and accumulates the probability cost over a sequence. Its `finite-precision-and-decodability` item treats finite precision and unique inversion as separate construction constraints.
- The repository contains two deliberately distinct executable paths:
  - `run.py`: exact rational interval arithmetic, a finite dyadic code and exact reconstruction. The documented synthetic example reports 19.642 ideal bits, a 21-bit finite code and a successful round trip.
  - `quantized_coder.py`: positive integer frequencies summing to `2^12`, deterministic frame header and packed payload. The JSON report separates floating-point NLL, quantized ideal NLL, payload, padding, header and total serialized size. `tests/unit/test_quantized_predictive_coder.py::test_cli_runs_and_reports_distinct_coding_costs` executes the CLI entry point and checks exact reconstruction.

**Evidence locators:**
- `shannon-mathematical-theory-communication-1948:noiseless-channel-coding-theorem` — §9, pp. 16–17, Theorem 9 and second proof.
- `rissanen-langdon-arithmetic-coding-1979:probability-derived-ideal-length` — pp. 150–152, especially Eqs. (1)–(5).
- `rissanen-langdon-arithmetic-coding-1979:finite-precision-and-decodability` — pp. 151–152 and the decodability criteria, pp. 157–159.

**Limits:** the two experiments use a fixed synthetic four-symbol bigram source, not a neural network, LLM or natural-language corpus. The model, training sequence, alphabet and probability tables are shared out of band and excluded from the frame-size metric. The message length is carried in the header. The quantized coder still uses exact rational interval arithmetic; it is not a bounded-state production range coder. Shannon and Rissanen are both marked `partially-scanned`; their extraction locators and scope/limitations must travel with the claim. The Rissanen scan also records OCR/layout artefacts, so exact equation typography must be checked against the publisher copy before quotation.

### P5 — Predictive information → restricted model family → source-local theory

**Path:** canonical `mutual-information` / `v-information` concepts → source record `xu-et-al-usable-information-2020` → source-local pedagogical nodes `src-predictive-family`, `src-predictive-v-entropy`, `src-v-information`, `src-pac-estimation` → extraction items → bilingual information-theory experience guide.

**What is supported:** the paper defines predictive V-information relative to an explicitly specified family of probabilistic predictors and logarithmic loss. The no-input and conditional predictive V-entropies are compared; the relationship to Shannon mutual information depends on the unrestricted-family special case. The paper's PAC-style estimation result depends on bounded log-probabilities and a complexity condition for the selected predictive family.

**Evidence locators:**
- `xu-et-al-usable-information-2020:predictive-family-definition` — §2, Definition 1.
- `xu-et-al-usable-information-2020:v-information-definition` — §2, Definition 3.
- `xu-et-al-usable-information-2020:pac-estimation` — §4, Theorem 1.

**Limits:** the source record is `partially-scanned`, and the extraction's pedagogical reconstruction is explicitly `partial`; this is not a claim that the entire paper was exhaustively audited. The PAC statement requires the paper's bounded-log-probability and function-family complexity assumptions. The `src-*` nodes are source-local teaching nodes, not canonical concept IDs, and must not be promoted automatically. The project's XOR example is a finite exact population calculation, not a reproduction of the paper's high-dimensional experiments or PAC guarantee.

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

## Automated regression coverage

`tests/knowledge/test_cross_graph_scientific_pilot.py` now contains five focused checks: (1) attention computation to the Vaswani §3.2.1 locator; (2) the KL/MI negative control; (3) FlashAttention's IO-aware implementation scope; (4) the predictive-coding path to Shannon/Rissanen locators, with model-compression and runtime-memory boundaries; and (5) the V-information source-local graph, partial-scan state and exact Definition 1 / Definition 3 / Theorem 1 locators. These tests protect selected endpoints and semantic boundaries; they do not implement general graph traversal, evaluate arbitrary candidate edges, establish source completeness, or constitute a precision benchmark.

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

The source-to-extraction paths are now explicit for Vaswani, Dao, Shannon, Rissanen and Xu, with the partial-scan boundaries retained. The information-theory synthesis documents the Wayland notebook inspection, but the source-specific extraction filename remains unconfirmed; do not invent it or use it as a locator. The quantized-coder CLI is exercised by its unit test; no fresh neural-LLM experiment or reproduction of Huang et al. is claimed. These are explicit scope boundaries, not reasons to create substitute records.

## Decisions and next work

1. Keep the current canonical owners and graph vocabularies. No new schema or global bridge registry is justified by this pilot.
2. If a machine-readable traversal is implemented, derive its joins from existing IDs and relationships; retain edge category, source status, locator, assumptions and limitations in the returned path.
3. Extend `tests/knowledge/test_cross_graph_scientific_pilot.py` selectively: it currently protects three of the reviewed cases (attention-to-source locator, KL/MI negative control, FlashAttention IO scope). Add further assertions only where they test a distinct invariant; do not duplicate the existing manual candidate table or imply that all nine cases are automated.
4. Test bilingual rendered page parity separately from metadata/resource registration.
5. Confirm the exact CI run and head SHA that exercised `tests/knowledge/test_cross_graph_scientific_pilot.py`; separately re-run the existing experiment commands in CI or a controlled local environment, recording exact commit, interpreter/dependencies and outputs. Static inspection and a passing test are not a fresh experiment reproduction.
6. Extend the same protocol to compression/model deployment only after checkpoint size, predictive quality, peak runtime memory, HBM traffic, latency, throughput and bits/token are separately defined.

**No new canonical concepts, relations, source records or experiment claims are proposed by this report.**
