# Sparse autoencoder research: source review and concept implications (2023–2025)

**Review date:** 2026-11-18  
**Review depth:** full-paper sections audited for Cunningham et al., Gao et al., Chanin et al. and Shu et al.; metadata/overview-level review only for Bricken et al.; full audit still pending  
**Purpose:** ground the proposed SAE and mechanistic-interpretability concepts in distinct primary sources and keep evidence, method and interpretation layers separate.

## 1. Scope and status

Five scientific sources are registered separately in `data/sources.yml`. Their catalogue records deliberately remain `scan_status: partially-scanned` and `integration_status: partially-integrated`. Official publisher/proceedings metadata and abstracts were checked for all five; the full published papers of Cunningham et al., Gao et al., Chanin et al. and Shu et al. were inspected for their main methods, evaluation protocols and limitations. Bricken et al. remains overview-level because the original long-form page could not be fully retrieved in this pass. Code and checkpoints were not run, and not every appendix or cited work has been audited.

No source in this review is treated as independently reproduced. The sources provide reported findings and technical framing, not direct measurements made by LLM Lab.

## 2. Source-by-source findings

### 2.1 Cunningham et al. — Sparse Autoencoders Find Highly Interpretable Features in Language Models (ICLR 2024)

- **Version and identity:** arXiv:2309.08600 (first posted 2023); published ICLR 2024 proceedings version. Published author order: Robert Huben, Hoagy Cunningham, Logan Smith, Aidan Ewart and Lee Sharkey.
- **Abstract-level contribution:** uses sparse autoencoders to reconstruct language-model internal activations and identify an overcomplete set of sparsely activating directions/features. The paper reports greater interpretability under automated measures than comparison directions, and a feature-level causal analysis on counterfactual indirect-object-identification behavior.
- **Concept implication:** a learned SAE feature is a dictionary direction in an activation space, not automatically a native neuron. A feature's interpretation and causal role are separate claims.
- **Scope/limitation:** the reported causal result is tied to the studied task, model and experimental setup; it does not license a universal claim that SAE features are always causal or monosemantic. The full paper and methods have not yet been audited here.
- **Primary record:** [ICLR 2024 proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/1fa1ab11f4bd5f94b2ec20e794dbfa3b-Abstract-Conference.html) · [arXiv](https://arxiv.org/abs/2309.08600)

### 2.2 Bricken et al. — Towards Monosemanticity: Decomposing Language Models With Dictionary Learning (2023 research report)

- **Version and identity:** Transformer Circuits Thread research report published 2023-10-04; Anthropic authorship; not a peer-reviewed proceedings paper.
- **Abstract/overview-level contribution:** applies sparse dictionary learning to a one-layer Transformer and reports a large set of interpretable features, including an overcomplete feature basis relative to the model's neuron count.
- **Concept implication:** feature directions can be distributed combinations of neuron activations; interpreting only native neurons may miss useful directions in activation space.
- **Scope/limitation:** the studied one-layer model and report-specific feature examples must not be generalized to all architectures, layers or modern LLMs. The complete technical report and figure reuse status remain unaudited.
- **Primary record:** [Transformer Circuits Thread](https://transformer-circuits.pub/2023/monosemantic-features/index.html)

### 2.3 Gao et al. — Scaling and Evaluating Sparse Autoencoders (ICLR 2025)

- **Version and identity:** arXiv:2406.04093 (first posted 2024); published ICLR 2025 proceedings version. Authors: Leo Gao, Tom Dupré la Tour, Henk Tillman, Gabriel Goh, Rajan Troll, Alec Radford, Ilya Sutskever, Jan Leike and Jeffrey Wu.
- **Abstract-level contribution:** studies the scaling of SAE dictionaries and the reconstruction/sparsity trade-off; proposes k-sparse autoencoders to control sparsity, modifications aimed at reducing dead latents, scaling analyses and several feature-quality metrics.
- **Concept implication:** "feature quality" is multidimensional. Reconstruction, sparsity, dead latents, recovery of hypothesized features, explanation of activation patterns and downstream effects are not interchangeable measures.
- **Scope/limitation:** reported scaling trends and metrics are tied to the paper's training setups, models and evaluation definitions. A larger dictionary or a higher score does not by itself establish semantic truth or causal completeness.
- **Primary record:** [ICLR 2025 proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/42ef3308c230942d223c411adf182c88-Abstract-Conference.html) · [arXiv](https://arxiv.org/abs/2406.04093)

### 2.4 Chanin et al. — A is for Absorption: Studying Feature Splitting and Absorption in Sparse Autoencoders (NeurIPS 2025)

- **Version and identity:** arXiv:2409.14507 (first posted 2024); published NeurIPS 2025 proceedings version, DOI 10.52202/085713-2755. Published paper authors: David Chanin, James Wilken-Smith, Tomáš Dulka, Hardik Bhatnagar, Satvik Golechha and Joseph Bloom.
- **Abstract-level contribution:** studies feature splitting as dictionary size increases and identifies feature absorption: apparently coherent latents may fail to activate on cases where they should, with activation absorbed by finer child features in hierarchical feature settings. The paper reports evaluation across hundreds of SAEs.
- **Concept implication:** a feature description that fits selected positive examples can still have poor coverage. Counterexample search must include expected-positive cases where the feature fails to activate, not only false-positive examples.
- **Scope/limitation:** the reported mechanism and metric are those of the paper's hierarchy assumptions, tasks and SAE evaluations. The full paper/supplement has not yet been audited or reproduced. This is a 2025 proceedings paper, not a 2024 publication merely because its preprint appeared in 2024.
- **Primary record:** [NeurIPS 2025 proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/hash/764ff7477b8e24dbe01531f6791e8bdf-Abstract-Conference.html) · [arXiv](https://arxiv.org/abs/2409.14507)

### 2.5 Shu et al. — A Survey on Sparse Autoencoders: Interpreting the Internal Mechanisms of Large Language Models (Findings of EMNLP 2025)

- **Version and identity:** arXiv:2503.05613; published Findings of EMNLP 2025, DOI 10.18653/v1/2025.findings-emnlp.89. Authors: Dong Shu, Xuansheng Wu, Haiyan Zhao, Daking Rai, Ziyu Yao, Ninghao Liu and Mengnan Du. The ACL Anthology page states that post-2016 materials use CC BY 4.0.
- **Abstract-level contribution:** surveys SAE architectures and training, input- and output-based feature explanation methods, structural and functional evaluation metrics, and applications.
- **Concept implication:** use this source as a map of the field and its taxonomies, not as primary evidence for each underlying empirical result.
- **Scope/limitation:** claims in the survey must be traced to the cited primary studies before being promoted to source-grounded claims in the knowledge graph. Full sections and references have not yet been audited.
- **Primary record:** [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.89/) · [arXiv](https://arxiv.org/abs/2503.05613)


### 2.6 Full-paper cross-check: what the methods actually distinguish

The full papers make several ontology boundaries more precise than their abstracts alone:

- **Target activation site:** Cunningham et al. explicitly sample activations from residual-stream, MLP-sublayer or attention-head-sublayer locations. The activation vector is therefore always site-scoped; an SAE dictionary trained on one site is not automatically transferable to another.
- **Encoder coefficient vs decoder direction:** the SAE encoder computes a latent coefficient for a given input, while the decoder direction contributes to reconstruction. The latent index links these parameters, but they are not definitionally the same vector. The Chanin analysis shows why this distinction matters: encoder and decoder directions can become asymmetric under absorption. Do not use "feature activation", "feature direction" and "reconstruction contribution" interchangeably.
- **Cunningham's reported feature score:** their automated interpretation procedure asks GPT-4 to produce a human-readable description from activating examples, then predicts feature activations on other examples; correlation with actual activations forms the score. This is predictive agreement under that protocol, not a proof that the description is semantically true or exhaustive.
- **Cunningham's causal evidence:** the paper uses activation patching along selected dictionary-feature directions in an indirect-object-identification task, compares with PCA, and applies ACDC while treating features as a flat computational graph with independent effects. The test set is 50 IOI examples. This is a specific intervention result, not a universal validation of SAE features or of arbitrary attribution graphs.
- **Cunningham's coverage caveat:** even a feature described as an apostrophe detector does not fire on every apostrophe; other context-specific features activate. A convincing top-activating-example panel is not evidence of complete recall.
- **Gao's quality measures:** the paper distinguishes normalized reconstruction MSE and sparsity (L0), dead-latent rate, recovery of hypothesized features, sparse downstream effects, and explanation precision/recall. It studies both a ReLU/L1 baseline and TopK variants; TopK directly constrains the number of active latents rather than applying the same L1 penalty. These are separate metrics and training choices, not one scalar notion of interpretability.
- **Gao's scope:** the published experiments include GPT-2 small and GPT-4 residual-stream activations, with specific layer selection, context length and normalization. The 16M-latent result is tied to the authors' GPT-4 setup. Scaling trends should not be promoted to model-independent laws without preserving those conditions.
- **Chanin's absorption mechanism:** when a dense parent feature always co-occurs with a sparse child feature, an SAE can lower its sparsity cost by folding the parent direction into the child decoder direction and suppressing the parent encoder on child-positive examples. This creates an encoder recall hole even when reconstruction remains good.
- **Chanin's experimental protocol:** the paper tests first-letter information with Gemma-2-2B and Gemma Scope 16k/65k SAEs, plus selected SAEs trained on Qwen2 0.5B and Llama 3.2 1B. Its absorption metric combines probe alignment with ablation effects on a defined output-logit measure; thresholds were selected by manual inspection. This is a source-specific metric, not a universal diagnostic.
- **Chanin's limitations:** the causal-ablation metric cannot be applied beyond layer 17 in its Gemma-2-2B spelling setup because attention has already moved the relevant information to the final token. The metric is conservative and likely underestimates absorption: it misses multiple absorbing latents and weakly firing main latents. The authors also lack multiple seeds for the released SAEs, so their own training runs are used to establish non-zero absorption rather than universal rates.

The resulting practical rule is stronger than "inspect counterexamples": test both **precision** (what else activates?) and **recall** (what expected cases fail to activate?), then use a method-specific intervention only when a causal claim is needed. Record the model, layer/hook, token position, preprocessing, SAE architecture, latent index, encoder/decoder directions, evaluation metric and intervention protocol.



### 2.7 Full-survey cross-check: explanation methods and evaluation are separate taxonomies

The full Shu et al. survey is useful as a field map, but its taxonomies should not be mistaken for a single agreed ontology:

- **Input-based explanations:** MaxAct selects highly activating text spans; PruningMaxAct removes context while attempting to retain activation. The survey reports a precision/recall trade-off for pruning, drawing on Gao et al. These are procedures for generating evidence/examples, not the feature itself.
- **Output-based explanations:** VocabProj projects a decoder feature direction onto output embeddings; MutInfo adds a mutual-information formulation to reduce frequency/norm-driven ambiguity. These methods depend on model architecture and embedding geometry; they are not universal feature semantics.
- **Structural evaluation:** reconstruction MSE/cosine similarity, FVU/explained variance, KL or cross-entropy shifts, delta language-model loss, activation-magnitude preservation, L0 sparsity, latent firing frequency, feature-density statistics and sparsity/fidelity trade-offs.
- **Functional evaluation:** feature-description/monosemanticity scoring, sparse probing, targeted probe perturbation, input/output description faithfulness, feature absorption, feature-geometry redundancy and out-of-distribution generalization.
- **No ground-truth shortcut:** the survey explicitly notes that SAE evaluation lacks general ground-truth labels. Different metrics operationalize different questions; a high score in one family does not establish correctness across the others.
- **Survey limitation:** the paper focuses on SAE developments in the LLM era and does not comprehensively cover the history of related ideas in distributed representations, disentangled representation learning or sparse coding. Use it to navigate and classify the literature, then follow its references to primary sources.

This taxonomy reinforces a key modelling decision: **feature explanation method**, **evidence sample**, **evaluation metric**, **feature latent** and **causal intervention** should remain distinct categories. A MaxAct panel or VocabProj token list is not a concept node; it is output from a method applied to a feature under a defined model and dataset.


## 3. Cross-source synthesis: what the evidence supports

1. **SAEs are auxiliary analysis models.** They learn a sparse representation of activations from a selected target-model site. The SAE is not itself a Transformer layer or a native component of the target model.
2. **A feature is a learned latent/dictionary direction.** It is scoped to the target model/checkpoint, layer or hook, activation preprocessing, SAE training run and dictionary. A feature index is not globally portable.
3. **A feature activation is a per-example coefficient.** It is not the direction/dictionary feature itself, and it depends on the input and the exact activation site.
4. **Interpretability is not one metric.** Reconstruction fidelity, sparsity, dead-latent rate, feature recovery, explanation quality, coverage and downstream effects answer different questions.
5. **Positive examples are insufficient.** Feature splitting and absorption make expected-positive misses and hierarchical counterexamples especially important. A feature may have a clear set of top activations yet poor recall on cases its description predicts.
6. **Descriptions and causal claims are different.** A human-readable or model-generated label is a hypothesis; a causal claim requires a defined intervention and suitable controls. Cunningham's activation-patching result and Chanin's ablation-based absorption metric each depend on their own task, layer and metric; neither validates every feature or circuit.
7. **Surveys are navigation aids.** The Shu et al. survey distinguishes input-based and output-based explanation methods, structural and functional metrics, and application areas. Its categories are useful for navigation, but source-level empirical claims must point to the primary paper that establishes them.

## 4. Implications for the canonical concept graph

The five papers support further review of these candidates, but do not justify creating nodes from every term:

- **Sparse autoencoder:** a learned encoder/decoder system applied to target-model activations.
- **SAE latent feature:** a learned dictionary coordinate/direction, scoped to a particular SAE and target activation site.
- **Feature activation:** the per-input value/coefficient of a particular latent.
- **Feature evaluation:** a family of distinct measurements (reconstruction, sparsity, dead latents, feature recovery, explanation/coverage and downstream effects), not a single scalar concept.
- **Feature explanation:** a hypothesis/representation, often model-generated; keep its provenance and evidence separate from the feature.
- **Feature splitting / absorption:** empirical phenomena and limitations of dictionary learning, not synonyms for a feature hierarchy.
- **Attribution method / circuit hypothesis / causal intervention:** related but distinct categories; the SAE papers in this first pass do not provide a complete survey of attribution methods or circuit validation. Additional primary sources are required before defining these concepts canonically.

Do not add `activation` as a generic node without resolving its overlap with `contextualized-representation`. A hidden state, an activation tensor at a hook, a scalar SAE coefficient and a UI activation score are not interchangeable.

## 5. What remains to scan

- Full Cunningham et al. and Gao et al. methods, objectives, metrics, ablations and limitations.
- Bricken report sections describing the exact model, SAE training setup, feature examples and interventions.
- Chanin et al. methods, hierarchy assumptions, absorption metric, datasets/SAEs, controls and supplementary analyses.
- Shu et al. survey taxonomy and bibliography, then trace important claims to primary sources.
- Additional primary sources for attribution methods, activation patching, causal scrubbing, circuit validation and steering controls.
- Any reuse licences for figures, datasets and code separately from article access.

## 6. Explicit non-claims

This first pass is based on official publisher/proceedings pages, abstracts and report overviews. It does not claim that LLM Lab has trained or run an SAE, independently inspected the Gemma Scope feature, recomputed its activations, reproduced any attribution method, or validated a complete causal circuit. All five catalogue entries remain partially scanned.
