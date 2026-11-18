# Cross-domain bridge pilot — baseline audit / Audit initial du pilote de passerelles transversales

**Date:** 2026-11-18  
**Status:** inventory and semantic review; no canonical graph edges changed  
**Tracking:** [#1237](https://github.com/JM-Brun/llm-lab/issues/1237), parent architecture [#1233](https://github.com/JM-Brun/llm-lab/issues/1233)

## Executive summary / Résumé exécutif

The repository already contains the scientific material needed for a first pilot. The main gap is not missing subject graphs: it is the lack of a reviewed, evidence-bearing traversal contract connecting existing concept, computational, source-local and experiment structures.

Le dépôt contient déjà les matériaux scientifiques nécessaires. Le manque principal n'est pas un graphe thématique supplémentaire : c'est un protocole de traversée vérifiable, avec preuves, entre les structures conceptuelles, computationnelles, documentaires et expérimentales existantes.

**Decision:** do not add a new graph, canonical concept, generic relation type or duplicate experiment in this first pass. First validate the existing records and their evidence paths. Treat derived quantities such as attention-weight entropy as scoped experimental measurements unless a genuine reusable concept is justified.

**Décision :** ne pas ajouter de graphe, de concept canonique, de type générique de relation ni d'expérience redondante à ce stade. Valider d'abord les enregistrements et leurs chemins de preuve. Traiter les quantités dérivées comme l'entropie des poids d'attention comme des mesures expérimentales contextualisées, sauf justification d'un concept réutilisable.

## 1. Existing structures and canonical endpoints / Structures et points d'ancrage existants

### Concept registry

The canonical registry is `data/concepts.yml` (schema version 2). It already contains, among others:

- Attention: `query`, `key`, `value`, `attention-score`, `attention-weight`, `softmax`, `scaled-dot-product-attention`, `self-attention`, `multi-head-attention`, `causal-mask`.
- Probability and learning: `conditional-distribution`, `entropy`, `surprisal`, `cross-entropy`, `kl-divergence`, `mutual-information`, `v-information`, `sequence-likelihood`, `negative-log-likelihood`.
- Coding and compression: `predictive-compression`, `minimum-description-length`, `entropy-coding`, `arithmetic-coding`, `model-compression`, `pruning`, `quantization`, `knowledge-distillation`.
- Runtime: `kv-cache` and inference-computation concepts.

IDs are language-independent and definitions/resources are bilingual. Existing concepts already point to learning pages; do not create translated duplicates.

### Existing typed concept relations relevant to the pilot

The current registry already expresses these useful edges:

- `attention-score --normalized-by--> softmax`
- `softmax --produces--> attention-weight`
- `attention-weight --part-of--> scaled-dot-product-attention`
- `attention-weight --contrasts-with--> mutual-information`
- `entropy --prerequisite--> cross-entropy`
- `kl-divergence --prerequisite--> cross-entropy`
- `mutual-information --contrasts-with--> v-information`
- `predictive-compression --applies-to--> conditional-distribution`
- `predictive-compression --contributes-to--> entropy-coding`
- `surprisal --contributes-to--> predictive-compression`
- `arithmetic-coding --part-of--> entropy-coding`
- `model-compression --contrasts-with--> predictive-compression`
- `quantization --part-of--> model-compression`
- `kv-cache --contributes-to--> decode-step`

These edges are concept-level semantics, not proof records. In particular, the existing contrast between attention weights and mutual information is a valuable guardrail, but it does not establish a positive mathematical bridge from attention weights to the entropy of a specified distribution.

The current vocabulary includes typed relations such as `part-of`, `contributes-to`, `applies-to`, `normalized-by`, `produces`, `contrasts-with`, `approximates`, `prerequisite` and `represented-by`. It does not currently make every edge a claim object with its own source locator, assumptions, epistemic status and falsification conditions. Do not overload a relation label to imply those missing semantics.

### Separate structures that must remain separate

- `data/computational-graph.yml`: computational operations, intermediate data and execution branches.
- Source-local pedagogical models in `data/extractions/*.yml`: reconstructions of a source's own teaching model, explicitly scoped to the accessible source.
- Source catalogue, source extractions and synthesis documents: source identity, claims, evidence and editorial decisions.
- Experiment code and tests: operationalized quantities and reproducible observations.
- Page graph / learning route: navigation and pedagogical sequence, not scientific causality.

The concept relation review (`docs/audits/concept-relation-edge-review.md`) explicitly says the concept map is not a complete execution DAG and that high-level relations such as `contributes-to` are not strict data-flow or causal-completeness claims. The knowledge-graph standards profile likewise treats JSON-LD as a deterministic projection, not a new authoring store.

## 2. Audited source and experiment material / Matériaux documentaires et expérimentaux audités

### Information theory

`docs/source-syntheses/information-theory-and-llms-2026-11.md` already records the key distinction:

- Attention does not calculate mutual information.
- Attention weights are not bits and are not an estimator of mutual information by themselves.
- MI requires a joint distribution.
- The reviewed attention/MI notebook used row-wise KL to a uniform distribution and mislabeled it as an approximation of MI; the synthesis explicitly rejects that interpretation.
- V-information is predictor-family-relative and remains distinct from Shannon MI.

The synthesis also audits the primary V-information paper (Xu et al., 2020) and records that author experiments were not reproduced. Preserve this source-role distinction.

### Predictive compression versus model/runtime compression

`docs/source-syntheses/compression-two-meanings-2026-11.md` and `model-compression-2026-11.md` already distinguish:

1. Predictive/source coding of a data sequence using conditional probabilities.
2. Compression of model parameters/structure (quantization, pruning, distillation).
3. Temporary runtime memory and IO (KV cache, activations, buffers).

They explicitly state that better checkpoint compression does not guarantee better predictive coding; KV-cache quantization affects runtime memory rather than directly shrinking model-weight files; and actual deployment benefits depend on hardware, kernels and workload.

### Existing experiments

- `experiments/information-theory/attention_kl_vs_mutual_information.py`: constructs joint distributions from context probabilities and conditional rows. It demonstrates that a non-uniform attention-like row can have positive KL to uniform while repeated identical rows make context and key independent, with MI equal to zero. It also computes weighted conditional KL to the marginal and states the joint-distribution assumptions.
- `experiments/information-theory/compression.py`: compares constant, IID-uniform and symmetric first-order Markov sources with fixed seeds; reports marginal entropy, source entropy rate and finite zlib size including container overhead. It explicitly warns that the finite compressor result is not a proof of the asymptotic coding theorem.
- `experiments/information-theory/run.py`: verifies entropy/cross-entropy/KL and idealized code-length identities for a finite categorical example.
- Existing unit tests in `tests/unit/test_information_theory.py` cover the cross-entropy decomposition, bit/nat conventions, MI for independent/perfectly correlated variables, invalid joint tables and the identity between MI and expected conditional KL to the marginal.
- Additional existing experiments cover V-information, predictive compression, sequence compression and compression strategy spectra. Reconcile their outputs and definitions before creating anything new.

### Attention implementation

`data/computational-graph.yml` already contains attention-specific nodes for Q/K/V, score computation, masked scores, attention softmax, attention weights, weighted value aggregation and output. This gives a computational path to reuse.

The source-local FlashAttention reconstruction explicitly distinguishes the mathematical attention function from its GPU kernel and distinguishes exact tiled attention from sparse attention. It notes that some technical details are cross-checked against the primary paper and official documentation because the full secondary article is not accessible. Keep this source-access limitation visible.

Primary implementation references to verify at claim level:
- Vaswani et al. (2017), https://arxiv.org/abs/1706.03762
- Dao et al. (2022), https://arxiv.org/abs/2205.14135
- Dao (2023), https://arxiv.org/abs/2307.08691

## 3. Candidate bridges and current disposition / Passerelles candidates et statut

| Candidate | Correct relation class | Current disposition | Reason / evidence boundary |
|---|---|---|---|
| Softmax over the visible keys for one fixed query produces non-negative weights summing to one | Mathematical property / scoped equivalence | **Supported for the specified operation; formalize in pilot** | Follows from softmax normalization; masking defines the admissible support. Do not generalize to arbitrary attention variants without checking their normalization. |
| Entropy of a fixed attention-weight row | Mathematical application of Shannon entropy to a specified distribution | **Supported as a derived measure; no new canonical concept yet** | The row is a normalized distribution over visible keys. The value measures concentration/dispersion of that row, not semantic information or causal importance. |
| Attention-weight entropy equals mutual information | Mathematical equivalence | **Rejected** | Entropy is a property of one distribution; MI requires a joint distribution and its marginals. Existing synthesis and KL-vs-MI experiment provide a counterexample. |
| Row-wise KL to uniform equals mutual information | Mathematical equivalence | **Rejected** | The reference distribution is uniform, not the marginal distribution induced by a specified joint. Repeated identical non-uniform rows yield positive KL-to-uniform and zero MI. |
| FlashAttention implements exact dense attention with IO-aware tiling/online softmax | Implementation mapping; mathematical equivalence under stated numerical assumptions | **Candidate supported by primary paper; benchmark exactness separately** | Separate algorithmic function, floating-point deviations, HBM traffic and runtime measurements. |
| FlashAttention is information-theoretic compression | Analogy at most; not an established equivalence | **Rejected as stated** | It reduces IO / intermediate materialization; it does not encode the input sequence into a shorter lossless code. |
| Autoregressive NLL / cross-entropy and ideal predictive code length | Mathematical relation under shared probability model, tokenization, log base and coding protocol | **Supported with assumptions; test finite coder separately** | Expected ideal code length under model mismatch is cross-entropy; a real lossless coder additionally needs a compatible encoder/decoder and protocol. |
| Markov marginal entropy and entropy rate | Mathematical distinction | **Supported and experimentally represented** | The Markov experiment demonstrates dependencies lower entropy rate while stationary marginal entropy can remain high. |
| Model quantization and source coding of the input corpus | Equivalence | **Rejected as category error** | Quantization changes model representation; source coding encodes data. A quantized model may later be evaluated as a predictor/coder, which is a separate experiment. |
| KV-cache quantization and reduced runtime memory | Implementation/empirical relation | **Supported as a scoped hypothesis; workload/backend measurement required** | It concerns runtime state, not checkpoint size or source-code length. |
| Attention as an information bottleneck | Theoretical mechanism / optimization claim | **Unresolved; do not add** | Requires explicit random variables, objective, assumptions and evidence. Weighted aggregation alone is insufficient. |

## 4. First reviewed negative benchmark / Premier benchmark négatif

The first reproducible negative case should be the existing KL-versus-MI experiment, not a newly invented toy. Required assertions:

1. Two contexts have equal probability.
2. Both conditional rows are the same non-uniform vector, e.g. `[0.9, 0.1]`.
3. Mean row-wise KL to uniform is strictly positive.
4. The constructed joint makes context and key independent, so MI is zero.
5. The weighted conditional KL to the marginal equals MI (zero in this case).
6. The output labels the quantities and units distinctly and does not call row-wise KL an MI estimate.

The contrasting-row case (e.g. `[0.9, 0.1]` and `[0.1, 0.9]`) is useful, but its numerical equality between KL-to-uniform and MI in a symmetric binary example is incidental. A test must not infer general equivalence from that coincidence.

## 5. Evidence path contract for the pilot / Contrat de preuve

A scientific bridge must be traceable through existing structures:

`canonical concept IDs → typed concept relation (if already justified) → computational node or source-local node (when relevant) → source ID + extraction item + exact locator → synthesis decision → experiment/test (if empirical or executable)`

At each step preserve the distinction between:

- primary-source statement or theorem;
- formal derivation by the project;
- source author's pedagogical analogy;
- implementation documentation;
- secondary-source interpretation;
- project experiment and its measured result.

A source citation is not itself a proof. A page's topical association is not a relation. Repeated secondary sources may all derive from one primary source and are not independent corroboration. An experiment supports only the tested setup and assumptions.

For the pilot, if the current extraction schema cannot attach evidence to a cross-structure relation without inventing an incompatible edge format, keep the reviewed claim in the synthesis/benchmark artifact and report the schema gap to #1233. Do not silently encode epistemic status into an unrelated concept relation field.

## 6. Work sequence / Suite du travail

1. Run existing experiment scripts and their unit tests in the repository's locked environment; capture outputs and versions.
2. Inspect the exact primary-paper passages and current source extraction IDs/locators for attention and FlashAttention. Repair source-local references only when the evidence warrants it.
3. Produce a small bilingual benchmark with positive, negative and unresolved candidates; include exact inputs, expected outputs and reasons for rejection.
4. Trace at least five paths through more than one existing structure. Mark missing evidence paths as gaps, not as supported edges.
5. Only then decide whether existing concept relations need a narrowly scoped addition or whether an evidence-bearing bridge belongs in an existing provenance/synthesis projection.
6. Validate deterministic output, negative-case rejection and FR/EN parity. No automated candidate becomes established knowledge merely because it is traversable.

## 7. Acceptance checklist / Critères d'acceptation

- [ ] Existing concept IDs and source/experiment records reused; no duplicates.
- [ ] Five cross-structure paths audited, with exact locators or explicit gaps.
- [ ] At least three false or underspecified bridges rejected with reasons.
- [ ] KL-to-uniform versus MI negative case reproduced and tested.
- [ ] Mathematical identity, implementation mapping, analogy and causal claim remain distinct.
- [ ] Entropy rate versus marginal entropy and ideal code length versus finite coder size remain distinct.
- [ ] Checkpoint compression, predictive/source coding and runtime memory remain distinct.
- [ ] Evidence, assumptions, limitations and source independence are recorded.
- [ ] Bilingual synthesis and benchmark preserve meaning without forcing identical teaching narratives.
- [ ] Existing tests pass; new tests are deterministic and scoped.

## 8. Repository references / Références internes

- `data/concepts.yml`
- `data/computational-graph.yml`
- `docs/audits/concept-relation-edge-review.md`
- `docs/knowledge-graph-standards.md`
- `docs/source-syntheses/information-theory-and-llms-2026-11.md`
- `docs/source-syntheses/compression-two-meanings-2026-11.md`
- `docs/source-syntheses/model-compression-2026-11.md`
- `experiments/information-theory/attention_kl_vs_mutual_information.py`
- `experiments/information-theory/compression.py`
- `experiments/information-theory/run.py`
- `tests/unit/test_information_theory.py`

## 9. Five concrete cross-structure paths / Cinq chemins transversaux concrets

This path inventory was completed after the initial baseline. It reuses the current canonical IDs and source-local records. A path is not automatically a new concept relation: the table marks where the canonical graph is already connected and where only a source/provenance traversal currently exists.

| Path | Existing evidence path | What the traversal establishes | Remaining boundary |
|---|---|---|---|
| **P1 — Mathematical attention** | Source `vaswani-et-al-attention-is-all-you-need-2017` → extraction `...:scaled-dot-product-attention` (§3.2.1, Eq. 1) → canonical Q/K/V, score, weight, softmax and scaled-dot-product concepts → computational nodes `attention-score-computation → attention-scores → attention-softmax → attention-weights → value-aggregation → attention-output`. | The primary equation is connected to the existing implementation-level computation without duplicating either graph. | The formula itself does not establish an information-theoretic or causal interpretation. |
| **P2 — Attention versus mutual information** | Wayland source → extraction `wayland-zhang-information-theory-llm-2026:attention-mutual-information` (section “Attention as Mutual Information”) → canonical `attention-weight` / `mutual-information` contrast → `experiments/information-theory/attention_kl_vs_mutual_information.py` → information-theory synthesis. | The source's analogy is preserved as an analogy/contrast, and the experiment supplies a negative case against identifying row-wise KL-to-uniform with MI. | No positive equivalence between attention weights and MI is supported. A single attention row does not define the required joint distribution. |
| **P3 — Shannon MI versus predictive V-information** | Xu et al. source → `xu-et-al-usable-information-2020:predictive-family-definition` (Definition 1) and `:v-information-definition` (Definition 3) → canonical `v-information`, `mutual-information`, `cross-entropy` → bilingual finite-family experiment. | The primary formal definition and optional-ignorance condition ground a family-relative predictive quantity; the paper's unrestricted-family special case is kept distinct from restricted predictive families. | The project's toy example is an exact finite-distribution illustration, not a reproduction of the paper's PAC theorem or high-dimensional experiments. |
| **P4 — Predictive loss and source coding** | Wayland source → `:cross-entropy-kl-decomposition` and `:compression-intelligence` → canonical `cross-entropy`, `negative-log-likelihood`, `surprisal`, `predictive-compression`, `entropy-coding` → `experiments/information-theory/run.py` (ideal lengths) and `compression.py` (finite zlib and entropy-rate comparison). | The expected ideal code-length interpretation of log loss is distinguished from a finite compressor's actual byte count and framing overhead. | The zlib experiment does not use the LLM's conditional distribution. The canonical concept graph has no explicit reviewed edge yet connecting cross-entropy/NLL to predictive compression; retain this as a candidate relation, not an implicit path. |
| **P5 — Attention function and IO-aware implementation** | Vaswani primary attention extraction → computational attention nodes → Dao et al. source `dao-et-al-flashattention-2022` and extraction items `:exact-io-aware-attention`, `:online-softmax-tiling`, `:io-complexity`, `:block-sparse-extension` → source review → existing FlashAttention benchmark protocol. | The mathematical attention operation, exact dense IO-aware implementation, online-softmax mechanism, asymptotic HBM bounds and separate block-sparse approximation can be followed through distinct structures. | No new FlashAttention concept node is warranted. A benchmark result must still record actual hardware/backend, shapes, dtype, masks, correctness tolerance and workload; the paper's results are not universal runtime guarantees. |

### Explicit relation candidates held back

1. **Cross-entropy / NLL ↔ predictive compression:** mathematically justified under a specified target distribution, model distribution, tokenization, logarithm base and coding protocol. The existing `cross-entropy-kl-decomposition` extraction and `run.py` experiment are evidence anchors. Do not add an edge until its direction and relation label are reviewed against the current relation vocabulary.
2. **Attention-weight row ↔ Shannon entropy:** valid as applying a standard functional to a normalized row for a fixed query/head/layer/input/mask. This can remain an experiment-derived metric; it does not require a new canonical concept.
3. **FlashAttention ↔ scaled-dot-product attention:** an implementation mapping, not a taxonomy or causal relation. The primary Dao extraction supports it; do not claim that IO optimization is information-theoretic source compression.
4. **Attention ↔ information bottleneck:** unresolved. No relation is added without explicit random variables, objective, assumptions and a source-backed theorem or empirical test.

### Numerical negative-case oracle

For equally likely contexts and repeated conditional rows `[0.9, 0.1]`:

- Mean row-wise KL to the uniform distribution: **0.5310044064 bits**.
- Context–key mutual information: **0 bits**, because the conditional row is identical for both contexts and the variables are independent.

For contrasting rows `[0.9, 0.1]` and `[0.1, 0.9]`:

- Mean row-wise KL to uniform: **0.5310044064 bits** (unchanged).
- Context–key mutual information: **0.5310044064 bits**.

The equality in the second case is incidental: the contrasting rows induce a uniform marginal. The first case is the decisive counterexample. A regression test for this distinction is merged in the existing information-theory unit tests.

### Verification status

- [x] Primary-source extraction for Vaswani §3.2.1 / Equation (1) merged.
- [x] Primary-source extraction for Dao et al. (2022), including theorem and block-sparse boundaries, merged.
- [x] Existing Wayland and Xu extraction items identified and reused.
- [x] Negative KL-to-uniform versus MI regression test merged.
- [ ] Execute the repository's locked test suite and validators; no CI status was reported for the documentation/source/test PRs during this pass.
- [ ] Review the candidate cross-entropy/NLL → predictive-compression relation before any canonical edge change.
- [ ] Add a machine-readable benchmark only if an existing experiment/test format cannot express these reviewed cases without creating a second graph.

