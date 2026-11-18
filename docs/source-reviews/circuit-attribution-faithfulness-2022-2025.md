# Circuit discovery, attribution and faithfulness: methodological review (2022–2025)

**Review date:** 2026-11-18  
**Status:** first-pass source-backed methodological review; source-catalogue records and source-scoped extractions remain to be added  
**Related work:** [interpretability concept audit](interpretability-concept-audit-2026-11.md), [SAE research review](sparse-autoencoder-research-2023-2025.md), [issue #1232](https://github.com/JM-Brun/llm-lab/issues/1232)

## 1. Executive synthesis

Circuit research contains several operations that are often collapsed under the vague phrase “finding what matters”:

1. **Define a behavior and its measurement.** Choose a model/checkpoint, task, input distribution, clean/corrupted or baseline inputs, and a scalar target metric.
2. **Localize candidate components.** Direct activation patching tests selected substitutions; gradient attribution methods estimate many patching effects cheaply.
3. **Select a candidate subgraph.** A discovery algorithm ranks or prunes nodes/edges according to a metric, baseline and threshold.
4. **State a mechanistic hypothesis.** Explain how the selected components and paths are claimed to implement the bounded behavior.
5. **Validate the hypothesis.** Intervene on the proposed circuit and its complement, use resampling or counterfactual tests, and measure whether the predicted behavior is preserved or disrupted.
6. **Represent the result.** A graph drawing, feature label or dashboard is a visualization/interpretation layer, not the computational object and not validation evidence by itself.

The central distinction is therefore:

> **Attribution estimates where to look; interventions test what changes; discovery selects a candidate; validation tests whether the candidate explains the behavior.**

These stages can be composed, but none implies the next automatically.

## 2. Method comparison

| Method | Operation and output | Main advantage | Main limitation / correct interpretation |
|---|---|---|---|
| Activation patching | Replace a chosen activation (or edge contribution) with a value from a baseline/corrupted run; measure the change in a specified target metric | Direct intervention on the chosen computational variable | Costly when swept over many components/edges; result depends on patch site, replacement, baseline, metric and input distribution |
| ACDC | Iteratively prunes edges in a computational graph using activation-patching-based tests and a threshold; returns a candidate subgraph | Automates edge selection in a defined graph and task | Discovery procedure, not a standalone causal theory; depends on graph abstraction, metric, threshold, data and patching assumptions |
| Attribution patching / EAP | Uses gradients and activation differences to approximate patching effects, often ranking edges from a small number of forward/backward passes | Cheap pre-filter over many candidate edges | Local/linear approximation can miss effects; attribution score is not itself an intervention or universal causal importance |
| AtP* | Modifies AtP to address two reported false-negative classes and estimates/bounds residual false-negative risk | More reliable scalable pre-filter under the studied setup | Still an approximation and a filter; a bound is conditional on its assumptions and does not turn all selected edges into validated causes |
| EAP-IG | Integrates gradients along an interpolation between clean and baseline activations to improve edge attribution | Addresses cases where a local gradient at one endpoint is misleading | Improved ranking/faithfulness is empirical and task-scoped; integrated attribution remains a selection estimate, not the intervention used to establish causal effect |
| Causal scrubbing | Formalizes a mechanistic hypothesis as equivalence classes/resampling rules; replaces activations with those from inputs predicted equivalent by the hypothesis and checks behavior | Tests whether the hypothesized information flow predicts behavior under controlled resampling | A failed test rejects/refines the hypothesis under that test; a pass is conditional on the equivalence relation, resampling distribution, tested behavior and implementation |
| Sparse feature circuits | Extends graph analysis to SAE feature nodes and SAE reconstruction-error nodes, with estimated indirect effects and subsequent feature-level interventions/edits | More fine-grained candidate units than polysemantic heads/neurons; supports feature-level analysis | Depends on SAE quality, feature coverage, error-node accounting, graph construction and thresholds; a human feature label is not the feature's causal role |

### 2.1 Activation patching is the intervention, not the score

Activation patching is an intervention on a specified internal variable. A result is interpretable only when the protocol names:

- model and exact checkpoint;
- hook/site, layer, position and tensor/component being patched;
- source and replacement activations (clean, corrupted, mean, resampled, zero, etc.);
- task, examples and sampling procedure;
- target metric and direction of improvement;
- whether the test is single-component, edge-level, joint or complement ablation.

A change in a metric after patching supports a causal claim about that particular intervention in that setup. It does not prove that the component is uniquely necessary, sufficient, or the only implementation of the behavior. Redundancy, distributed representations and interactions can make single-edge effects misleading.

### 2.2 Attribution patching is an approximation

Attribution patching estimates the effect of a patch using a gradient-based approximation. In edge attribution patching, the estimate concerns a connection in a chosen computational graph, not an intrinsic property of a model component independent of graph and target.

The approximation is attractive because exhaustive edge patching is expensive. But a small estimated effect can be a false negative: nonlinearities, saturation, endpoint gradients and interactions can hide an effect. Therefore:

- use attribution to prioritize or pre-filter candidate interventions;
- retain a recall-oriented strategy when false negatives are costly;
- verify selected and strategically sampled rejected candidates with actual patching;
- report the baseline, gradient point/path, target metric and threshold;
- never describe an attribution-only edge as “causally validated”.

Syed et al. (BlackboxNLP 2024) report that their linear edge attribution method outperforms earlier automated discovery baselines on average AUC across their evaluated tasks, at a cost of two forward passes and one backward pass. This is a benchmark-specific comparison, not a theorem that attribution dominates direct interventions or works equally well on all models/tasks.

Kramár et al. study AtP as a pre-filter and identify two false-negative failure classes. AtP* changes the approximation to address them and proposes an estimate of residual false-negative risk. Its advantage is improved scalable localization under the evaluated settings; it does not remove the need for intervention-based verification.

### 2.3 Discovery is not validation

ACDC automates a step in circuit extraction: finding connections between units in a computational graph. Its reported GPT-2 Small Greater-Than result (68 selected edges out of 32,000 and recovery of the manually identified component types) is evidence about that benchmark and graph setup. It should not be generalized into “ACDC finds the true circuit” without qualification.

A discovered subgraph is a candidate produced by a selection rule. To support a mechanistic explanation, the study must separately test whether:

- the candidate is behaviorally sufficient under a defined complement-ablation test;
- its components/paths are necessary under defined interventions, where that claim is made;
- its internal dependencies match the proposed information flow;
- the behavior survives resampling/counterfactual tests predicted by the hypothesis;
- relevant alternative paths, redundant components and edge cases have been examined.

### 2.4 Faithfulness is not overlap

Hanna, Pezzelle and Belinkov (COLM 2024) distinguish circuit overlap from faithfulness. They define faithfulness in terms of ablating all model edges outside the proposed circuit without changing the task behavior. Their experiments show EAP-IG circuits can be more faithful than EAP circuits even when both have high node overlap with intervention-derived reference circuits. In their IOI analysis, a circuit with substantial overlap can nevertheless have zero measured faithfulness under the paper's test.

This yields an important evaluation rule:

- **Overlap** asks whether two procedures select similar nodes/edges.
- **Faithfulness** asks whether the selected circuit preserves the target behavior when the rest of the model is ablated.
- **Necessity/sufficiency** are distinct causal claims and require explicitly defined interventions and metrics.

Do not use overlap as a substitute for behavioral validation. Also do not treat a faithfulness score as universal: it is conditional on the task, data, target metric, ablation protocol and normalization.

### 2.5 Causal scrubbing tests a hypothesis, not a graph aesthetic

Causal scrubbing turns a proposed mechanistic explanation into resampling rules: activations are replaced with activations from inputs that the hypothesis treats as equivalent. If behavior changes where the hypothesis predicts invariance, the hypothesis is falsified or requires refinement for that test.

The crucial object is the **hypothesis plus its equivalence/resampling rules**, not the resulting diagram. The procedure can be demanding: equivalence classes must be specified carefully, resampling must preserve the intended controls, and a pass only supports the tested hypothesis on the tested distribution. It does not establish completeness for all prompts or behaviors.

### 2.6 Sparse feature circuits add nodes, not automatic semantic truth

Marks et al. (ICLR 2025) construct computational graphs containing SAE feature nodes and SAE error nodes, estimate indirect effects, and filter nodes/edges. Their feature-level approach makes some mechanisms more interpretable and supports SHIFT, which manually removes features judged irrelevant to a classifier's intended task.

For the ontology, preserve at least these distinctions:

- target-model component/activation;
- SAE encoder and decoder parameters;
- SAE feature (latent index with encoder-side detector and decoder-side reconstruction direction);
- per-example feature activation;
- SAE reconstruction-error node/term;
- computational graph node or edge in a specified abstraction;
- indirect-effect / attribution estimate;
- intervention/ablation applied to a feature or edge;
- human-authored feature description;
- graph visualization and grouped feature display.

A feature name or natural-language explanation is not a causal role. A feature circuit may be causally implicated under a particular protocol without proving that the feature is a universal semantic atom.

## 3. Evidence and scope matrix

| Source | Version / venue | What this review uses | Scope caveat |
|---|---|---|---|
| Conmy et al., *Towards Automated Circuit Discovery for Mechanistic Interpretability* | NeurIPS 2023; arXiv:2304.14997 | ACDC workflow, graph pruning, benchmark framing | GPT-2 Small tasks and the authors' graph/metric setup |
| Syed, Rager & Conmy, *Attribution Patching Outperforms Automated Circuit Discovery* | BlackboxNLP 2024; arXiv:2310.10348 | Linear approximation to edge patching, efficiency and comparative AUC | Reported benchmark average does not imply universal superiority |
| Kramár et al., *AtP*: Efficient and Scalable Methods for Localizing LLM Behaviour to Components | arXiv:2403.00745 (2024) | AtP pre-filter, two false-negative classes, AtP* and residual-risk estimate | Preprint; claims remain conditional on study assumptions and evaluations |
| Hanna, Pezzelle & Belinkov, *Have Faith in Faithfulness* | COLM 2024; arXiv:2403.17806 | EAP-IG and separation of overlap from faithfulness | Faithfulness is operationalized for specified tasks/metrics and ablation protocols |
| Chan et al., *Causal Scrubbing* | AI Alignment Forum research report (2022) | Hypothesis-driven resampling test | Research report; original protocol and limitations require a dedicated extraction |
| Marks et al., *Sparse Feature Circuits* | ICLR 2025; arXiv:2403.19647 | SAE feature/error graph, indirect effects, SHIFT | Depends on learned SAE features and graph/threshold choices |

## 4. Proposed typed distinctions — not yet canonical IDs

The existing concept registry and relation vocabulary must be audited before promotion. This review therefore does **not** add IDs or invent new relation types.

Candidate object categories to map onto the existing ontology:

- **model object:** activation, component, computational edge;
- **analysis model object:** SAE, feature, reconstruction error;
- **measurement:** activation-patching effect, attribution estimate, indirect-effect estimate, faithfulness score;
- **procedure:** intervention, attribution method, discovery algorithm, resampling validation;
- **hypothesis:** bounded circuit/mechanistic explanation;
- **representation:** graph visualization, feature description, pedagogical analogy.

Candidate relation semantics to check against the existing relation vocabulary (not proposed as new schema values yet):

- a method *estimates* a quantity;
- an intervention *modifies/replaces* a model state;
- an algorithm *selects/prunes* graph elements;
- a hypothesis *predicts* dependencies or invariances;
- a validation procedure *tests* a hypothesis;
- a visualization *represents* a graph/result;
- a description *interprets* an analysis object.

Do not encode “causes” merely because an attribution edge is drawn or ranked highly. A causal relation must carry its experimental scope and evidence provenance, either as explicit metadata or as a linked claim/evidence record.

## 5. Minimum evidence contract for a circuit claim

Every published or project-authored circuit claim should record:

1. **Behavior:** task definition and target metric (including baseline and direction).
2. **Model:** architecture, checkpoint/revision, layer/site and relevant hook semantics.
3. **Inputs:** dataset, sampling, clean/corrupted pairs, distribution and sample count.
4. **Graph:** node/edge definitions, abstraction level, omitted components and SAE/error-node treatment.
5. **Selection:** method/version, gradient baseline or path, thresholds, ranking and stopping rule.
6. **Interventions:** exact patching/ablation/resampling operations, controls and order.
7. **Evaluation:** recovery/overlap, faithfulness, necessity/sufficiency where tested, uncertainty and robustness.
8. **Limitations:** false negatives, nonlinear interactions, redundancy, threshold sensitivity, distribution shift and untested behaviors.
9. **Provenance:** source/version, section/figure/table locator, code/checkpoint where available, and whether LLM Lab independently reproduced anything.

A claim missing these fields should be labelled exploratory or under-specified, not presented as a validated mechanism.

## 6. Synthesis and next decisions

The papers form a methodological sequence rather than competing definitions of one object:

- ACDC automates graph-edge discovery using intervention-based tests.
- Attribution patching and AtP/AtP* reduce the cost of localization by estimating patch effects, with explicit false-negative risks.
- EAP-IG improves the attribution path to better preserve behavioral faithfulness in the evaluated settings.
- Causal scrubbing tests whether a mechanistic hypothesis predicts behavior under structured resampling.
- Sparse Feature Circuits move the graph's units to SAE features and reconstruction-error terms, then use attribution and interventions for downstream analysis.

The next integration step is to register each source independently, create source-scoped extractions with method/evidence/limitation locators, then audit the canonical relation vocabulary and bilingual concept pages. No experiment has been run by LLM Lab in this review; no external result is represented as independently reproduced.


## 7. Audit of the existing canonical relation vocabulary

The current data/concepts.yml already defines 12 bilingual relation types: represented-by, prerequisite, part-of, constrains, contributes-to, applies-to, mapped-by, produces, normalized-by, contrasts-with, evaluated-by and approximates. This review does not require a new relation type for every method distinction.

| Intended statement | Existing relation candidate | Guardrail |
|---|---|---|
| A method estimates an effect of a direct patching operation | approximates | The estimate is not the intervention; preserve the target quantity and approximation assumptions in evidence metadata |
| A circuit candidate is selected by a discovery algorithm | produces | Record the algorithm, graph, metric, threshold and data; “produces” does not imply correctness |
| A validation method is applied to a circuit hypothesis | applies-to | This records method scope, not a successful validation result |
| A circuit/hypothesis is assessed with a faithfulness or recovery metric | evaluated-by | Store the metric definition and intervention protocol; score is not a universal property |
| A graph or plot depicts a candidate computational graph | represented-by | The representation is not the underlying model graph or proof |
| An SAE feature/error term is a node in a particular feature-circuit abstraction | part-of | Keep this scoped to the represented graph; do not claim the SAE feature is a native Transformer component |
| Attribution and intervention are distinct procedures | contrasts-with | Use to prevent conceptual conflation, not as an ontological claim that they are opposites |

### Relation-vocabulary finding

The existing vocabulary is adequate for broad pedagogical and representational links, but it is **not sufficient by itself to encode a rigorous causal claim**. In particular, contributes-to should not be used as a shortcut for “causes”, and produces should not be interpreted as proof that an algorithm's output is valid. The registry currently has no dedicated relation whose semantics explicitly state an experimentally supported causal effect with scope and evidence.

For now, retain causal claims in source-scoped evidence records or structured claim metadata, including intervention, metric, model, inputs and scope. Do not add a generic causal edge to the concept graph until the project has decided how evidence, confidence, scope and counterevidence are represented. This avoids both false precision and a proliferation of weakly typed edges.

One schema hygiene point should also be checked in the implementation: the approximates relation definition appears after a large blank separator in the YAML. Its placement is syntactically valid if it remains inside relation_types, but validators and generated graph projections should confirm it is parsed as a relation type and not silently ignored.
