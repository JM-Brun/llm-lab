# Interpretability concept audit — 2026-11

**Status:** editorial and ontology audit; proposals only, not canonical concept records  
**Scope:** Neuronpedia, sparse autoencoders, feature-level evidence, attribution and mechanistic/circuit hypotheses  
**Related work:** [Neuronpedia integration dossier](embedding-atlas-neuronpedia-integration-2026-11.md), [extraction](../../data/extractions/neuronpedia-interpretability-platform-2026.yml), [issue #1220](https://github.com/JM-Brun/llm-lab/issues/1220)

## 1. Audit result

The current canonical registry contains **102 concepts**. It already represents the Transformer-side foundations needed to introduce interpretability without building a parallel ontology:

- `token-embedding` and `contextualized-representation` cover the initial token vector and context-dependent hidden state.
- `self-attention`, `query`, `key`, `value`, `attention-score`, `attention-weight`, `multi-head-attention`, `causal-mask` and related concepts cover the standard attention computation.
- `logits` and `output-projection` cover the output-score path.

The registry currently has **no canonical concepts** for sparse autoencoders, SAE latents/features, feature activation values, attribution methods, circuit hypotheses or causal interventions. The source record for Neuronpedia is integrated and tagged for these topics, but its `concept_ids` intentionally remain limited to `contextualized-representation` and `self-attention`. Those links are valid entry points, not a complete interpretability ontology.

The existing bilingual advanced pages already contain a learner-facing Neuronpedia protocol. In particular, they correctly state that feature identity is scoped to a model/source/release, that generated explanations are hypotheses, and that attribution/steering evidence does not automatically establish causality. The next concept work should connect and sharpen these pages rather than create a new chapter or duplicate learning route.

## 2. Ontology boundary: five different layers

| Layer | Technical meaning | Examples | Not to be mistaken for |
|---|---|---|---|
| Model state / computational object | A vector or tensor at a defined model, layer, hook, token position and computation stage | Residual-stream activation; MLP or attention output | A feature label or a plot |
| Learned analysis object | Parameters/directions learned by an auxiliary analysis model | SAE encoder, decoder, dictionary, latent feature | A native Transformer neuron or a universal semantic concept |
| Per-example measurement | A value obtained when a learned object is applied to a particular input/state | Feature activation coefficient at a position | The feature direction itself |
| Analysis / intervention method | A defined procedure that estimates, decomposes, modifies or tests a quantity | SAE encoding, attribution, ablation, activation patching, steering | A dashboard visualization |
| Interpretation / teaching representation | A human- or model-authored account of selected evidence | Auto-Interp label, feature description, attribution graph, analogy, exercise | The underlying model state, latent, or causal mechanism |

This is a conceptual separation, not a claim that every product dashboard exposes all five layers or that each should become a concept node.

## 3. Candidate concepts and decisions

The bilingual definitions below are editorial candidates for review. They are deliberately not assigned stable IDs yet.

| Candidate | Proposed French label | Proposed English label | Proposed definition boundary | Preliminary decision |
|---|---|---|---|---|
| Sparse autoencoder (SAE) | Autoencodeur parcimonieux (SAE) | Sparse autoencoder (SAE) | An auxiliary encoder/decoder model trained to map activations from a specified model site to a sparse latent code and reconstruct them | **Add candidate.** A method/model object; not a Transformer component |
| SAE latent feature | Feature latente de SAE | SAE latent feature | A learned coordinate/direction in a particular SAE dictionary, scoped to the model, checkpoint, activation site and SAE version | **Add candidate.** Keep distinct from a native neuron and from a human concept |
| Feature activation | Activation d'une feature | Feature activation | The coefficient/value of a particular SAE latent for a specified input, token position and activation site | **Add candidate.** A per-example measurement, not the latent itself |
| Model activation / activation vector | Activation du modèle / vecteur d'activation | Model activation / activation vector | A vector/tensor produced at a defined computation site; it requires explicit model, layer/hook and position scope | **Defer or merge carefully.** It overlaps with existing contextualized hidden states but is broader; do not add a vague generic node |
| Feature explanation | Explication d'une feature | Feature explanation | A human- or model-generated hypothesis describing observed activation patterns, with provenance and evaluation method | **Likely a representation/evidence annotation, not necessarily a canonical concept.** Avoid promoting every dashboard label |
| Attribution method | Méthode d'attribution | Attribution method | A method-specific estimate/decomposition relating model components or inputs to a defined target quantity | **Add candidate if the selected methods are specified.** Attribution is not intervention |
| Circuit hypothesis | Hypothèse de circuit | Circuit hypothesis | A proposed set of model components and computational relations intended to explain a bounded behavior | **Add candidate.** A hypothesis, not a graph UI or established mechanism by default |
| Causal intervention | Intervention causale | Causal intervention | A controlled modification of a specified internal state/component followed by measurement of a defined outcome | **Add candidate.** Requires controls and explicit intervention protocol |

### Terms that should remain non-concepts unless a concrete need is demonstrated

- A feature index such as `10956`: an identifier within a specific source/model/release namespace, never a global concept ID.
- An Auto-Interp score: a method-dependent evaluation result, not a universal measure of truth.
- Activation density, positive/negative examples and logits: measurements/evidence fields whose exact definitions belong in source- or method-level documentation.
- Highlighted tokens, heatmaps, dashboards and attribution-graph drawings: tool visualizations.
- Narrative examples, analogies and exercise prompts: pedagogical representations.
- "Neuronpedia feature": a platform-specific record/reference, not a separate scientific object category.

## 4. Proposed relationships to the existing graph

Use the current canonical graph vocabulary where it expresses a relationship accurately. Do not overload a relation just to force every edge into the graph.

| From | Existing relation candidate | To | Qualification |
|---|---|---|---|
| Sparse autoencoder | `applies-to` | Contextualized representation | The SAE is trained/applied to activations from a selected model site; document that this is a scoped use, not a universal relation to every contextualized state |
| SAE latent feature | `part-of` | Sparse autoencoder | The feature belongs to a particular learned dictionary |
| Sparse autoencoder | `produces` | Feature activation | Only if the node denotes the per-example encoded coefficient; the encoding is input- and site-dependent |
| Attribution method | `applies-to` | Contextualized representation | Only for methods whose target/input is explicitly defined |
| Causal intervention | `applies-to` | Contextualized representation | The intervention must name the modified quantity and measurement target |
| Circuit hypothesis | `evaluated-by` | Causal intervention | Only when the intervention actually tests a prediction of that hypothesis; an intervention does not validate an entire circuit automatically |

The current relation vocabulary includes `applies-to`, `part-of`, `produces`, `evaluated-by`, `represented-by`, `approximates`, `contributes-to`, `prerequisite`, `contrasts-with`, `constrains`, `normalized-by` and `mapped-by`. There are currently no dedicated relations such as `encodes`, `activates`, `describes`, `supports` or `tests`. If those distinctions become necessary, propose a typed vocabulary extension with definitions, inverse/compatibility rules and validation tests; do not silently invent edge types in `concepts.yml`.

## 5. Evidence ladder and claim calibration

| Evidence | What it can support | What it cannot establish alone |
|---|---|---|
| Activation examples / density | Where and how often a feature responds in the sampled/source-defined setting | Completeness, semantic uniqueness, necessity or causal importance |
| Auto-Interp description | A falsifiable verbal hypothesis about selected examples | Ground truth, exhaustive coverage or causal explanation |
| Logit view | The output-token quantity computed by that dashboard/method | Feature activation magnitude or causal contribution without method-specific derivation |
| Attribution | A method-specific estimate/decomposition under stated assumptions | A controlled intervention or proof of necessity |
| Ablation / patching / steering | Sensitivity to a specified intervention under a defined protocol | A complete circuit explanation without controls, baselines, counterfactuals and scope limits |
| Circuit analysis | A structured mechanistic hypothesis when nodes/edges have computational definitions | A validated causal graph merely because the result is drawn as a graph |

A learner-facing claim should state the exact model/checkpoint, source/release, layer/hook, token position, method and target quantity whenever relevant. Use "consistent with", "suggests" or "under this intervention" when evidence is limited. Reserve necessity/sufficiency or causal language for protocols that actually test those claims.

## 6. Mathematical anchor: a common SAE parameterization

For a common ReLU-SAE parameterization, an activation vector $x$ at a specified layer/hook is encoded as:

$$
z = \operatorname{ReLU}(W_{enc}(x-b_{pre})+b_{enc}),
$$

and reconstructed as:

$$
\hat{x}=W_{dec}z+b_{dec}.
$$

This notation is an anchor for one common family, not a universal implementation. Keep the following objects separate:

- $x$: the model activation vector at the selected site;
- $W_{enc}, W_{dec}$ and biases: learned SAE parameters;
- $z$: the sparse latent code for this input;
- $z_i$: one coordinate/value in this code;
- the $i$-th decoder direction: a learned dictionary direction;
- a natural-language label: an interpretation of observed examples, not a parameter.

A feature's identity is therefore scoped to the model/checkpoint, activation site, SAE training run/dictionary and release. Matching numeric indices across dictionaries do not imply matching features.

## 7. Existing learning-resource mapping

| Existing resource | Role in the interpretability learning sequence |
|---|---|
| `fr/contextualized-representations` / `en/contextualized-representations` | Understand shared initial lookup and context-dependent hidden states |
| `fr/contextualized-representations-advanced` / `en/contextualized-representations-advanced` | Formalize activation states, accessible context, attention and MLP transformations; host the advanced Neuronpedia investigation |
| `fr/exercises/contextualized-representations` / `en/exercises/contextualized-representations` | Test an SAE feature hypothesis against examples and counterexamples |
| `fr/queries-keys-values-advanced` / `en/queries-keys-values-advanced` | Prerequisite for understanding attention computations and the limits of head-level interpretations |
| Existing Transformer and attention pages | Locate the interpreted objects in the actual computation |

Do not create a parallel "interpretability" route at this stage. A future dedicated page is justified only if the concept audit demonstrates a coherent learning objective that cannot be served by the existing advanced route.

## 8. Source-ingestion gap

The source review currently cites the following primary or survey works, but the canonical source catalogue audit found no separate source records for them. The Neuronpedia platform record is not a substitute for these scientific sources.

1. Cunningham et al. (2023), [Sparse Autoencoders Find Highly Interpretable Features in Language Models](https://arxiv.org/abs/2309.08600).
2. Bricken et al. (2023), [Towards Monosemanticity: Decomposing Language Models With Dictionary Learning](https://transformer-circuits.pub/2023/monosemantic-features/index.html).
3. Gao et al. (2024), [Scaling and Evaluating Sparse Autoencoders](https://arxiv.org/abs/2406.04093).
4. Chanin et al. (2024), [A is for Absorption: Studying Feature Splitting and Absorption in Sparse Autoencoders](https://arxiv.org/abs/2409.14507).
5. Shu et al. (2025), [A Survey on Sparse Autoencoders: Interpreting the Internal Mechanisms of Large Language Models](https://aclanthology.org/2025.findings-emnlp.89/).

Next source pass: ingest the primary papers as distinct source records with identifiers, authors, dates, versions, licence/reuse status, scope, technical contributions, limitations, tags and candidate concept IDs only after the paper-level review. Record which claims each source supports; do not treat a survey as primary evidence for every claim.

## 9. Acceptance gates before canonical concept changes

- [ ] Ingest and review the primary papers; distinguish reproduced findings from reported findings.
- [ ] Confirm each candidate's technical definition and bilingual label against the papers.
- [ ] Decide whether model activation should reuse/refine `contextualized-representation` or become a separately scoped concept.
- [ ] Decide whether feature explanation belongs in the concept registry or only in source/evidence metadata.
- [ ] Validate candidate domain membership (primarily `architectures-mechanisms`, with `mathematical-tools-geometry` where the mathematical object warrants it).
- [ ] Validate each proposed relation against the current vocabulary; extend the vocabulary only with explicit contracts and tests.
- [ ] Add canonical IDs and update Neuronpedia's `concept_ids` only after the preceding gates pass.
- [ ] Update generated concept graph/projections and verify FR/EN resource resolution.
- [ ] Add tests for bilingual definitions, unique IDs, valid domains, valid relation types, and resolvable resources.
- [ ] Review the learner route and both language versions after rendering.

## 10. Explicit non-claims

This audit is a literature-informed ontology proposal. It does not claim that the project has trained an SAE, reproduced Neuronpedia's feature, independently computed its activations, reproduced attribution graphs, or validated a causal circuit. The source remains partially scanned until the relevant model-level evidence and methods have been inspected or reproduced.
