# Concept relation edge review

**Date:** 2026-11-05  
**Status:** source-semantic review covers all 122 current retained assertions (66 initial + 54 subsequent review + 2 audited on 2026-11-25). Rendered graph usability, browser/accessibility, and learner validation remain open  
**Canonical data:** [`data/concepts.yml`](../data/concepts.yml)  
**Tracking:** [LLM Lab #416](https://github.com/JM-Brun/llm-lab/issues/416), [merged validator PR #520](https://github.com/JM-Brun/llm-lab/pull/520)

## Scope and method

The initial inventory below records the 10 declared relation types and 26 edges present when this review began; the dated follow-up sections record subsequent registry changes and reviews. It checks the intended reading, direction, relation family, and whether the edge should influence learning order. It is a conceptual review, not a proof that the graph is a complete execution graph or a rendered-UX evaluation.

All current edge endpoints are canonical concept IDs. No domain-specific source/target restriction is imposed: concepts can belong to multiple domains and legitimate relations cross domain boundaries. Cardinality constraints are not currently justified; the registry is many-to-many.

## Relation type inventory

| Type | Family | Direction | Transitive | Acyclic | Learning dependency | Review |
|---|---|---|---:|---:|---:|---|
| `represented-by` | representational | directed | no | no | no | Appropriate for token → embedding lookup representation |
| `prerequisite` | pedagogical | directed | no | yes | yes | Only type allowed to drive a learning dependency; each edge requires bilingual rationale |
| `part-of` | structural | directed | yes | yes | no | Used for internal components/intermediates of attention mechanisms |
| `constrains` | constraint | directed | no | no | no | Appropriate for causal mask → attention mechanism |
| `contributes-to` | functional | directed | no | no | no | Captures a contribution, not necessarily a direct data-flow edge |
| `applies-to` | functional | directed | no | no | no | Expresses mechanism applicability; not a prerequisite |
| `mapped-by` | representational | directed | no | no | no | Expresses a representation transformed by a projection |
| `produces` | functional | directed | no | no | no | Expresses output production |
| `normalized-by` | functional | directed | no | no | no | Expresses score-vector normalization; does not encode every preceding scale/mask operation |
| `evaluated-by` | evaluative | directed | no | no | no | High-level relation to a loss; does not by itself encode target/label input |

All ten types are used by the current graph. Every current type is directed; the validator supports symmetric types when explicitly declared in metadata. No inverse relation is currently declared. The `transitive` flag records declared semantics; it does not cause inferred edges to be materialized.

## Edge inventory and review

| # | Edge | Assessment |
|---:|---|---|
| 1 | `token → represented-by → token-embedding` | **Accept.** The token ID selects an initial embedding vector. The label reads source → target correctly. |
| 2 | `token-embedding → prerequisite → contextualized-representation` | **Accept with pedagogical scope.** This is a learner prerequisite, not merely a computational dependency. Its bilingual rationale is recorded in the edge. |
| 3 | `query → part-of → self-attention` | **Accept.** Query projections are an internal component of the mechanism. |
| 4 | `key → part-of → self-attention` | **Accept.** Key projections are an internal component of the mechanism. |
| 5 | `value → part-of → self-attention` | **Accept.** Value projections are an internal component of the mechanism. |
| 6 | `query → part-of → scaled-dot-product-attention` | **Accept.** Query vectors are an input component of scaled dot-product attention. |
| 7 | `key → part-of → scaled-dot-product-attention` | **Accept.** Key vectors are an input component of scaled dot-product attention. |
| 8 | `value → part-of → scaled-dot-product-attention` | **Accept.** Value vectors are an input component of scaled dot-product attention. |
| 9 | `query → contributes-to → attention-score` | **Accept.** Query contributes to the compatibility score. |
| 10 | `key → contributes-to → attention-score` | **Accept.** Key contributes to the compatibility score. |
| 11 | `attention-score → part-of → scaled-dot-product-attention` | **Accept.** Scores are an intermediate result in the mechanism. |
| 12 | `attention-weight → part-of → scaled-dot-product-attention` | **Accept.** Normalized weights are an intermediate result in the mechanism. |
| 13 | `attention-score → normalized-by → softmax` | **Accept with scope note.** Softmax normalizes the score vector; the graph does not separately represent scaling and masking before normalization. |
| 14 | `softmax → produces → attention-weight` | **Accept.** Softmax produces normalized attention weights. |
| 15 | `causal-mask → constrains → scaled-dot-product-attention` | **Accept.** The mask restricts allowed attention positions. |
| 16 | `scaled-dot-product-attention → applies-to → self-attention` | **Accept.** The scaled dot-product formulation is used by self-attention. |
| 17 | `scaled-dot-product-attention → part-of → multi-head-attention` | **Accept.** Multi-head attention composes multiple attention heads. |
| 18 | `multi-head-attention → contributes-to → contextualized-representation` | **Accept.** Attention output contributes to a contextualized state; the edge is not an assertion that attention alone produces the final state. |
| 19 | `causal-mask → constrains → self-attention` | **Accept.** A direct high-level relation is useful in addition to the lower-level mechanism edge; it is not a route dependency. |
| 20 | `positional-encoding → contributes-to → self-attention` | **Accept with scope note.** Positional information enters the representations used by attention; the relation is indirect at this abstraction level. |
| 21 | `self-attention → contributes-to → contextualized-representation` | **Accept.** Self-attention contributes to context-dependent representations. |
| 22 | `contextualized-representation → mapped-by → output-projection` | **Accept.** The final representation is transformed by the output projection. |
| 23 | `output-projection → produces → logits` | **Accept.** The vocabulary projection produces logits. |
| 24 | `logits → normalized-by → softmax` | **Accept with scope note.** Softmax converts logits to a probability distribution; implementations may use numerically stable log-softmax/cross-entropy paths without materializing probabilities. |
| 25 | `softmax → evaluated-by → cross-entropy` | **Accept with scope note.** The predicted distribution is an input to cross-entropy; the target distribution/label is not represented by this edge. |
| 26 | `training-objective → evaluated-by → cross-entropy` | **Accept with scope note.** This expresses the training objective's loss criterion at a high level; it does not equate the task objective with the loss function. |

## Findings and limits

1. No edge in the current inventory requires an immediate direction reversal based on its declared verbal reading.
2. `prerequisite` is the only relation allowed to influence a learner route. Its edge rationale must be bilingual and explicit. No route is inferred from graph layout or page order.
3. `part-of` is the only current transitive relation. The validator checks its declared acyclicity; it does not generate transitive closure.
4. The graph is a selected conceptual map, not a complete computational DAG. In particular, it does not represent every tensor input, target label, masking/scaling operation, residual connection, or value aggregation step.
5. Several relations are intentionally high-level (`contributes-to`, `evaluated-by`). Their descriptions must not be interpreted as strict data-flow or causal-completeness claims.
6. The review does not establish that the visual layout, labels, keyboard/touch interaction, or learner comprehension are correct. Those remain separate checks under #416 and #337.

## Remaining work

- [ ] Review the rendered graph in FR and EN: legend, relation labels, arrow direction, selection details, and links to concept pages.
- [ ] Verify keyboard, touch, mobile layout, focus order, accessible names, and a non-graph alternative.
- [ ] Confirm that only `learning_dependency: true` relations are consumed by any guided-route logic; search all graph consumers before changing renderer behavior.
- [ ] Consider adding explicit `evidence` locators to relations only if a real editorial use case requires source-level provenance; do not add empty or decorative provenance fields.
- [ ] Revisit the selected graph's completeness only when a concrete pedagogical question requires missing edges; do not turn it into a full computational graph by default.

## Session handoff

The semantic inventory and initial edge review are recorded. The implementation of the generic relation contract is proposed in #518; wait for CI and Quarto checks before merging. The next useful task is rendered FR/EN graph inspection, not another schema expansion.


## Projection preservation

The generated bilingual learning-map payload now preserves the relation type contract (family, direction, transitivity, acyclicity, learning-dependency eligibility, inverse) and localized edge rationale. The current interactive renderer still uses only direction, label and description for its legend and details. The additional fields are retained in the projection rather than discarded, but no route generation consumes `learning_dependency`.


## Interoperability export boundary

The interactive learning-map JSON now preserves the relation metadata. The separate JSON-LD export in `site/tools/export_knowledge_graph.py` currently emits typed predicates for relation edges but does not export relation-type nodes with their family, direction, transitivity, acyclicity, learning-dependency and inverse metadata. This is a selective export, not a full serialization of the relation contract.

A follow-up should decide whether external consumers need a published relation vocabulary (for example, relation-type nodes with bilingual SKOS labels/definitions and project-specific semantic properties). The exporter and validator also maintain hard-coded relation-type allowlists; assess whether those should be derived from the canonical `relation_types` mapping to reduce drift. Do not expand JSON-LD or add another vocabulary unless an interoperability consumer requires it.

## Source-level interaction and accessibility review — 2026-11-05

This is a review of the current source implementation, not a claim that the rendered pages have been visually or assistively tested in a browser.

### Confirmed in source

- The concept view is grouped by canonical discovery domain and uses a responsive CSS grid with a 240px minimum card width, rather than the earlier fixed three-column ordering.
- The relation legend is shown persistently while the concept view is active. It exposes the source → target convention, localized relation labels, and localized descriptions.
- Concepts are native buttons. Selection is represented with aria-pressed; selecting a concept highlights its neighbours and updates the details panel.
- The details panel lists each relation with source, relation label, target, and a button to inspect the connected concept.
- Mode, relation filter, and search controls have associated labels. The details panel uses a polite live region; the page also exposes a status region.
- Escape clears a query, selected concept, or active relation filter in sequence; the reset control clears all map state.
- CSS includes visible focus styles for concept buttons, relation links, map controls, and reduced-motion handling in the broader site styles.

### Important semantic clarification

The current canonical-concept view is a **domain-grouped concept browser**, not a node-link diagram: it does not draw connectors between concept nodes. Relationships are communicated through the persistent legend, neighbour highlighting, and the selected concept's textual relation list. Documentation and issue descriptions should not imply that visible edge geometry or graph layout has been validated.

### Multi-domain concept presentation

A concept assigned to multiple discovery domains is rendered once in each domain group. For example, contextualized representation belongs to both architectures/mechanisms and mathematical tools/geometry. The concept count reports unique concepts, while the grid can contain more buttons than unique concepts. Selecting one canonical concept marks each rendered copy of that same concept as pressed.

This preserves all domain memberships but can create repeated cards. It is not automatically incorrect: domain membership is many-to-many. A follow-up should decide whether to retain repeated cards for cross-domain discovery or deduplicate the concept into one card with all domain labels. Do not assign a single primary domain without an explicit canonical rule. The browser test records both total buttons and unique concept IDs.

### First browser run baseline — 2026-11-05

The first browser run on the earlier review branch completed the Q/K/V and overview/generation route-context cases in FR/EN, desktop/mobile and browser prefers-color-scheme light/dark contexts. Those cases had no horizontal overflow; guided-stage anchors resolved; single and multi-membership semantics matched the contract; keyboard traversal found visible focus targets.

The eight concept-map cases stopped at an over-strict test assertion: a concept with two domain memberships rendered two buttons with the same canonical ID, while the details panel updated correctly. The test now validates the selected canonical-ID set instead of requiring exactly one DOM button.

Axe also reported two baseline issue types on the completed page cases:
- critical aria-allowed-attr: Quarto collapsible-callout header divs expose aria-expanded without a role that supports it;
- serious color-contrast: muted text #6c757d on #f8fafc measured 4.48:1; Mermaid green edge labels #16a34a on #ebecec measured 2.78:1.

These findings require review on the current main-based rerun. They are not evidence that the new concept browser itself causes the issues. Inspect Axe output and screenshots separately; do not claim WCAG conformance from source review or Quarto success.


The current-main rerun is implemented in [PR #531](https://github.com/JM-Brun/llm-lab/pull/531). It covers the concept browser plus all four guided-route context pilots (overview, generation, embeddings and Q/K/V), and explicitly verifies that the obsolete pipeline stepper is absent from the latter two lessons. The rerun also captures Axe target HTML snippets to distinguish Quarto-generated markup from project-owned components.


## Accessibility remediation follow-up — 2026-11-05

The 40-case browser audit in merged [PR #531](https://github.com/JM-Brun/llm-lab/pull/531) established the rendered baseline. It tested browser prefers-color-scheme contexts; the Quarto site currently defines a single light theme, so this is not evidence of a dedicated dark theme.

The two cross-cutting Axe findings are tracked in [#532](https://github.com/JM-Brun/llm-lab/issues/532) and are being addressed in [PR #535](https://github.com/JM-Brun/llm-lab/pull/535): semantic keyboard support for Quarto collapsible-callout headers, improved contrast for page-navigation/breadcrumb text and Mermaid edge labels, plus blocking Axe assertions in the existing browser audit. The PR is pending CI, Quarto and browser validation.


## Follow-up semantic audit — 2026-11-06

A fresh inspection of the current canonical `data/concepts.yml` found **69 relation assertions**, rather than the 26 edges covered by the original 2026-11-05 inventory above. The original 26-edge review remains valid for that historical subset, but it must not be presented as a complete review of the current registry. This count discrepancy is an audit-scope issue, not evidence that the remaining relations are wrong.

One newly added relation was unambiguously misleading and is removed in the accompanying change:

- Removed `prefill → contrasts-with → teacher-forcing`. The concepts' own definitions establish that prefill is an inference phase processing the initial prompt before incremental generation, whereas teacher forcing is a training-time conditioning strategy using observed preceding tokens. They operate in different execution contexts and are not conceptual opposites or mutually exclusive alternatives. The existing computational graph already models prefill as a phase of autoregressive generation and teacher forcing as a condition on observed-prefix scoring/training. No replacement edge is warranted: the two concepts are distinguished by their execution context in their canonical definitions and resources.

No new relation type or graph registry is introduced. A complete review of all 69 current relation assertions remains necessary before the edge audit can be marked complete; prioritize relations added after the original 26-edge inventory and record the reviewed set explicitly.


## Follow-up review of the 42 relations added after the original inventory — 2026-11-06

After PR #609, the registry contained 68 relations. PR #613 removed one overgeneralized edge from the original 26-edge inventory, leaving 67 relations at that stage: 25 retained edges from the historical inventory and 42 later additions. The 42 additions were reviewed against their endpoint definitions, relation-type descriptions, and the separate computational spine. The present follow-up removes one of those later additions as semantically ill-typed, leaving 41 retained additions and 66 relations overall. This is a semantic review of the selected concept graph, not a claim that it is a complete tensor-level execution DAG.

### Review of the 42 additional relations

| # | Relation | Assessment |
|---:|---|---|
| 1 | `post-training → contrasts-with → pretraining` | **Accept with scope note.** These are distinguishable training phases, not opposites. This matches the controlled meaning of `contrasts-with`. |
| 2 | `instruction-tuning → part-of → post-training` | **Accept.** Supervised instruction tuning is one post-training procedure. |
| 3 | `reinforcement-learning-from-human-feedback → part-of → post-training` | **Accept.** RLHF is a family of post-training procedures. |
| 4 | `direct-preference-optimization → part-of → post-training` | **Accept.** DPO is a post-training preference-optimization method. |
| 5 | `in-context-learning → contrasts-with → instruction-tuning` | **Accept with scope note.** The edge distinguishes prompt-time adaptation without parameter updates from parameter-updating fine-tuning; it does not imply mutually exclusive model capabilities. |
| 6 | `inference-time-compute → applies-to → reasoning-model` | **Accept.** Additional inference-time resources can be used by reasoning-oriented models; the edge does not claim that only reasoning models use them. |
| 7 | `tool-calling → part-of → agentic-system` | **Accept within the registry's definition.** Tool use is explicitly part of the defined agentic loop; this should not be generalized to every possible use of the term outside this project. |
| 8 | `softmax → produces → conditional-distribution` | **Accept.** Softmax maps logits to the conditional distribution over the vocabulary. |
| 9 | `next-token-prediction → part-of → training-objective` | **Removed; no replacement.** The endpoint definitions distinguish the task (estimating the next-token conditional distribution) from the function optimized during training. A task is not a structural component of that function. The computational graph already represents the operational path from token-level NLL through loss reduction to the training objective. |
| 10 | `conditional-distribution → contributes-to → sequence-likelihood` | **Accept.** Sequence likelihood is built from conditional probabilities at successive positions. |
| 11 | `observed-target → contributes-to → sequence-likelihood` | **Accept.** The likelihood is evaluated for the observed sequence, not a model-selected continuation. |
| 12 | `conditional-distribution → prerequisite → sequence-likelihood` | **Accept.** The bilingual rationale correctly describes the mathematical construction and learner dependency. |
| 13 | `observed-target → prerequisite → sequence-likelihood` | **Accept.** The target sequence must be identified before its likelihood can be defined. |
| 14 | `sequence-likelihood → mapped-by → logarithm` | **Accept.** The logarithm transforms the positive sequence likelihood into log-likelihood. |
| 15 | `logarithm → produces → log-likelihood` | **Accept.** The operation's output is correctly identified. |
| 16 | `sequence-likelihood → prerequisite → log-likelihood` | **Accept.** The log-likelihood is defined from the sequence likelihood. |
| 17 | `log-likelihood → mapped-by → negation` | **Accept.** Negation changes the sign of the log-likelihood. |
| 18 | `negation → produces → negative-log-likelihood` | **Accept.** The operation produces the minimization-oriented quantity. |
| 19 | `log-likelihood → prerequisite → negative-log-likelihood` | **Accept.** The mathematical dependency and bilingual rationale are explicit. |
| 20 | `negative-log-likelihood → contributes-to → training-objective` | **Accept with scope note.** NLL is a common token-level contribution to the autoregressive training objective; the edge should not imply that all training objectives are NLL. |
| 21 | `training-example → produces → observed-target` | **Corrected.** A training example contains aligned input and target tokens; it does not generate the target. Replaced with `observed-target → part-of → training-example`. |
| 22 | `teacher-forcing → applies-to → training-example` | **Accept.** Teacher forcing describes how observed preceding tokens condition training predictions for the example. |
| 23 | `cross-entropy → prerequisite → training-objective` | **Accept with scope note.** This is appropriate for the project's standard GPT next-token objective, not a universal prerequisite for every possible training objective. |
| 24 | `training-objective → produces → gradient` | **Accept at the conceptual level.** Differentiation is implicit between the objective and its gradient; the separate computational graph carries the operation-level detail. |
| 25 | `gradient → prerequisite → parameter-update` | **Accept.** In the represented gradient-based optimization path, the optimizer uses gradients to compute updates. |
| 26 | `optimizer → contributes-to → parameter-update` | **Accept.** The optimizer and its state determine the update from the gradients. |
| 27 | `parameter-update → contributes-to → next-token-prediction` | **Accept with scope note.** Parameter changes alter the function used for prediction; this does not guarantee improved predictive performance. |
| 28 | `observed-target → contributes-to → cross-entropy` | **Accept.** Cross-entropy requires the target as well as the predicted distribution. |
| 29 | `generated-token-feedback → contributes-to → decode-step` | **Accept.** The selected token extends the context used by the next incremental step. |
| 30 | `decoding-policy → applies-to → conditional-distribution` | **Accept.** A decoding policy selects from the predicted distribution. |
| 31 | `decoding-policy → produces → token` | **Accept.** The selection policy returns a token ID/token from the distribution. |
| 32 | `token → contributes-to → generated-token-feedback` | **Accept.** The selected token is the payload appended to the context. |
| 33 | `generated-token-feedback → part-of → autoregressive-generation` | **Accept.** Context feedback is a defining step of autoregressive generation. |
| 34 | `prefill → part-of → autoregressive-generation` | **Accept.** Prefill processes the initial context before incremental decoding. |
| 35 | `decode-step → part-of → autoregressive-generation` | **Accept.** Incremental decode steps are repeated during autoregressive generation. |
| 36 | `decoding-policy → part-of → autoregressive-generation` | **Accept.** Token selection is part of the represented generation procedure. |
| 37 | `kv-cache → contributes-to → decode-step` | **Accept with scope note.** The cache is an optional inference optimization, not a semantic or execution prerequisite for decoding. |
| 38 | `conditional-distribution → contributes-to → autoregressive-generation` | **Accept.** The distribution is the basis for token selection at each generation step. |
| 39 | `sequence-likelihood → contributes-to → held-out-evaluation` | **Accept.** Sequence likelihood can be aggregated as an evaluation score on held-out data. |
| 40 | `cross-entropy → contributes-to → held-out-evaluation` | **Accept.** Cross-entropy is a standard held-out predictive metric as well as a training loss; the data split distinguishes the uses. |
| 41 | `conditional-distribution → evaluated-by → held-out-evaluation` | **Accept.** The evaluation assesses predictions made by the conditional distribution without updating parameters. |
| 42 | `conditional-distribution → evaluated-by → cross-entropy` | **Accept with scope note.** The predicted distribution is evaluated relative to an observed target; the target contribution is represented separately by edge 28. |

### Revisions to earlier accepted edges

Two earlier edges were re-examined against the narrower definitions and the computational graph:

- Removed `contextualized-representation → mapped-by → output-projection`. The concept definition covers contextualized states generally, including intermediate block states. The vocabulary projection acts on final hidden states only. The separate computational graph already distinguishes `final-hidden-states → vocabulary-projection`; retaining the generic concept edge would overgeneralize the projection's input.
- The original edge `softmax → evaluated-by → cross-entropy` is retained for now as a high-level shorthand, but the more precise edge `conditional-distribution → evaluated-by → cross-entropy` should be the reader-facing explanation. Revisit removal only if the graph UI makes the two edges look like competing descriptions of the same direct relation.

### Resolution and remaining validation

- Edge 9 was removed without replacement: `next-token-prediction` is the task; `training-objective` is the optimized function. Their relationship is explained by the endpoint definitions and the computational graph, not by a structural `part-of` edge.
- Keep the distinction between the concept graph and the computational graph: the latter supplies the explicit differentiation and final-hidden-state operations.
- After removing row 9, the registry contains 66 relation assertions: 25 retained edges from the original inventory plus 41 retained later additions. All 66 have received a source-semantic review. Rendered graph usability, accessibility, and learner validation remain separate gates.


## Targeted follow-up — KL divergence is not a prerequisite for cross-entropy (2026-11-22)

A later registry addition introduced the pedagogical edge
`kl-divergence → prerequisite → cross-entropy`. A focused review against the canonical bilingual lesson and the day-21 calendar pilot found that this relation overstates the mathematical dependency.

Cross-entropy is defined directly for target distribution `q` and predicted distribution `p`: `H(q, p) = -Σ_i q_i log(p_i)`. For a one-hot target, it reduces to the token-level negative log-probability. Neither definition requires KL divergence. The identity `H(q, p) = H(q) + D_KL(q || p)` is a useful decomposition and supports an optional mathematical deepening, but it does not make KL a prerequisite for calculating cross-entropy.

**Decision:** remove the `kl-divergence → prerequisite → cross-entropy` edge without replacement. The current cross-entropy concept retains its bilingual resource links to `language-modeling-math`, so the decomposition remains discoverable as optional depth. No new relation type is introduced. The separate `entropy → prerequisite → cross-entropy` edge is outside this targeted decision and is left unchanged.

### Registry coverage boundary

The historical edge review above covered 66 retained relation assertions at its recorded state. The current registry had 125 assertions immediately before this targeted removal and has 124 afterward. Therefore, 66 reviewed assertions must not be presented as a complete review of the current registry; 58 current assertions remain outside that historical review. This targeted correction does not claim to audit those other assertions.

## Complete review of the 58 assertions added after the 66-edge baseline — 2026-11-23

The 2026-11-22 issue reconciliation identified 58 current assertions outside the earlier 66-edge semantic review. I compared all 58 with their bilingual endpoint definitions, the 12 relation-type definitions, the existing graph contract, and the relevant source reviews. This is a semantic fit review of the selected concept graph; it does not claim that every relation is an execution dependency or a prerequisite.

| # | Current pre-review assertion | Decision | Semantic assessment |
|---:|---|---|---|
| 1 | `free-energy-principle → contributes-to → active-inference` | Accept, scoped | The Free Energy Principle provides a theoretical framing for active inference. Active inference is a specific perception–action framework, not a synonym for the whole FEP. |
| 2 | `active-inference → contrasts-with → aixi` | Accept, scoped | Both are formal agent frameworks, but they use different foundations and objectives. “Contrasts with” marks a useful distinction, not mutual exclusivity or opposition. |
| 3 | `predictive-compression → applies-to → conditional-distribution` | Correct direction and type | The conditional distribution supplies probabilities used by predictive coding. Replace with `conditional-distribution → contributes-to → predictive-compression`; the original direction treated the distribution as a context to which the coding method applies. |
| 4 | `predictive-compression → contributes-to → entropy-coding` | Accept | Predictive probabilities determine symbol code lengths and can feed an entropy coder. |
| 5 | `arithmetic-coding → part-of → entropy-coding` | Accept | Arithmetic coding is a member of the entropy-coding family. |
| 6 | `model-compression → contrasts-with → predictive-compression` | Accept, scoped | The concepts distinguish compression of model representation/execution from compression of data sequences. They are not opposites and can be used together. |
| 7 | `pruning → part-of → model-compression` | Accept | Removing weights or structures is a recognized model-compression method. Actual storage/latency gains depend on sparsity structure and hardware. |
| 8 | `quantization → part-of → model-compression` | Accept | Reduced numerical precision is a model-compression technique; quality and speed trade-offs depend on the implementation. |
| 9 | `knowledge-distillation → part-of → model-compression` | Weaken relation | Distillation can support compression when a smaller student replaces a larger teacher, but distillation is not inherently compression. Replace `part-of` with `contributes-to` to avoid making the narrower use case universal. |
| 10 | `surprisal → contributes-to → predictive-compression` | Accept | Ideal code length is proportional to surprisal, `-log p(x)`, under the chosen logarithm base and coding assumptions. |
| 11 | `document-retrieval → contributes-to → retrieval-augmented-generation` | Accept | Retrieval supplies external documents/passages made available to the generative model. |
| 12 | `retrieval-augmented-generation → contributes-to → context-engineering` | Accept, scoped | RAG is one way to select and supply external context; it is not the whole context-engineering practice. |
| 13 | `persistent-memory → contributes-to → context-engineering` | Accept, scoped | Persistent information can be selected and incorporated into a later model context; storage alone is not context engineering. |
| 14 | `fine-tuning → part-of → post-training` | Accept | Fine-tuning a pretrained model is one family of post-training procedures. |
| 15 | `context-injection → contrasts-with → fine-tuning` | Accept, scoped | This distinguishes changing the input context from changing model parameters. The techniques can coexist in one system and are not opposites. |
| 16 | `context-injection → contributes-to → in-context-learning` | Accept | Supplying selected information in the prompt can provide the context on which in-context adaptation operates. |
| 17 | `document-retrieval → contrasts-with → in-context-learning` | Remove | Retrieval is an information-acquisition mechanism; in-context learning is a model behaviour. Retrieval can supply examples/context for in-context learning, so the two are compatible rather than a meaningful contrast. |
| 18 | `policy-gradient → part-of → post-training` | Accept, scoped | Policy-gradient methods are used in some post-training procedures, especially reinforcement-learning-based adaptation; they do not characterize all post-training. |
| 19 | `score-function → part-of → policy-gradient` | Accept | The gradient of log policy probability is a central term in policy-gradient estimators. It is distinct from an attention compatibility score. |
| 20 | `off-policy-reinforcement-learning → part-of → post-training` | Accept, scoped | Off-policy RL can be used for post-training from trajectories generated by a behaviour policy. This is one procedure, not a property of all post-training. |
| 21 | `training-inference-mismatch → constrains → policy-gradient` | Accept, scoped | A mismatch between rollout and trainer distributions can affect the validity/stability of policy-gradient updates. It is a regime-dependent constraint, not a definition of policy gradient. |
| 22 | `score-centering → applies-to → off-policy-reinforcement-learning` | Accept | The reviewed method is an additive score correction for specified off-policy mismatch settings. Its assumptions and compatible correction families remain explicit in the source review. |
| 23 | `attention-score → contrasts-with → score-centering` | Accept | The relation prevents a naming collision: an attention compatibility score is not the gradient of a policy log-probability. |
| 24 | `importance-sampling → contrasts-with → score-centering` | Accept, scoped | Importance sampling uses multiplicative probability-ratio weights; score centering subtracts an additive sampler-expected score. They are distinct but can be composed in compatible configurations, so this is not an exclusivity claim. |
| 25 | `importance-sampling → applies-to → off-policy-reinforcement-learning` | Accept | Importance sampling corrects expectations when samples come from a behaviour distribution different from the target distribution, subject to support and variance conditions. |
| 26 | `chat-template → contributes-to → instruction-tuning` | Accept, scoped | A chat template serializes roles, boundaries and control markers for instruction examples. It supports the data/model interface but is not required by every instruction-tuning setup. |
| 27 | `dataset-curation → contributes-to → pretraining` | Accept | Selection, filtering, structuring and documentation of a corpus contribute to pretraining data quality and composition. |
| 28 | `dataset-curation → contributes-to → post-training` | Accept | Post-training datasets also require task- and objective-specific curation. |
| 29 | `group-relative-policy-optimization → part-of → post-training` | Accept, scoped | GRPO is one policy-optimization method used in some post-training pipelines; the edge does not imply that all post-training uses GRPO. |
| 30 | `policy-gradient → part-of → group-relative-policy-optimization` | Accept | GRPO is a policy-optimization method whose update uses policy log-probability gradients weighted by group-relative advantages. |
| 31 | `context-engineering → contributes-to → in-context-learning` | Accept, scoped | Selecting and structuring relevant context can support in-context learning; it does not guarantee that the model will use that context effectively. |
| 32 | `attention-mask → constrains → self-attention` | Accept | An attention mask controls which key positions may contribute to each query position. |
| 33 | `padding-mask → constrains → self-attention` | Accept | A padding mask prevents inadmissible padding positions from contributing as context. |
| 34 | `document-boundary-mask → constrains → self-attention` | Accept, scoped | This applies to packed sequences where tokens from different documents must not attend across document boundaries. |
| 35 | `loss-mask → constrains → training-objective` | Accept | A loss mask selects target positions contributing to the objective; it does not determine attention visibility. |
| 36 | `attention-mask → contrasts-with → loss-mask` | Accept | This is an important distinction between context admissibility and target-loss inclusion. The masks are not mutually exclusive and may both be used in one batch. |
| 37 | `autoregressive-generation → contrasts-with → next-concept-modeling` | Accept, scoped | The concepts distinguish incremental next-token generation from hierarchical coarse-to-fine non-autoregressive generation. This does not imply that all systems must choose one family exclusively. |
| 38 | `hierarchical-discrete-codes → part-of → next-concept-modeling` | Accept | Hierarchical discrete codes are the representation predicted level by level in the NCM definition. |
| 39 | `coarse-to-fine-generation → part-of → next-concept-modeling` | Accept | NCM predicts successive levels from coarse to fine, with parallelism within a level. |
| 40 | `multiscale-residual-vector-quantization → part-of → next-concept-modeling` | Accept, scoped | This is the tokenization/representation construction used by the described NCM formulation; do not generalize it to every possible hierarchical-code generator. |
| 41 | `positive-pair-distribution → part-of → joint-embedding-predictive-architecture` | Weaken relation | The pair distribution shapes the JEPA learning signal; it is not a structural component of the architecture. Replace `part-of` with `contributes-to`. The separate constraint on the training objective remains. |
| 42 | `positive-pair-distribution → constrains → training-objective` | Accept | The declared positive-pair relation determines which observations the objective treats as related and therefore constrains the learned geometry. |
| 43 | `joint-embedding-predictive-architecture → contrasts-with → next-token-prediction` | Accept, scoped | JEPA predicts related-observation embeddings; next-token prediction predicts a token distribution. This distinguishes objectives, not mutually exclusive model families. |
| 44 | `platonic-representation-hypothesis → evaluated-by → held-out-evaluation` | Accept, scoped | The hypothesis requires held-out cross-modal representation/alignment tests. Ordinary next-token loss alone would not test the stated hypothesis. |
| 45 | `laplacian-eigenmaps → applies-to → positive-pair-distribution` | Accept, scoped | The method applies to the weighted graph induced by the pair distribution, not to an abstract probability table without that graph construction. |
| 46 | `laplacian-eigenmaps → contributes-to → platonic-representation-hypothesis` | Remove | Laplacian eigenmaps can be an analysis tool for graph geometry, but it does not contribute to the hypothesis itself. The pair-distribution/graph relation already captures the useful mathematical bridge. |
| 47 | `joint-embedding-predictive-architecture → represented-by → laplacian-eigenmaps` | Remove | A manifold-learning method does not represent the JEPA architecture. The paper's spectral result is conditional on a specific second-order anti-collapse setup; it is not a general identity between JEPA and Laplacian eigenmaps. |
| 48 | `attention-weight → contrasts-with → mutual-information` | Accept | Attention weights are normalized compatibility coefficients; mutual information is defined from a joint probability distribution. They are not interchangeable quantities. |
| 49 | `mutual-information → contrasts-with → v-information` | Accept, scoped | V-information is a predictor-family-relative, potentially directional usable-information measure; unrestricted families recover Shannon mutual information. The relation marks a distinction, not a contradiction. |
| 50 | `kolmogorov-complexity → contributes-to → algorithmic-probability` | Accept, scoped | The coding theorem relates algorithmic probability to shortest-description complexity; neither quantity is generally computable exactly. |
| 51 | `algorithmic-probability → contributes-to → solomonoff-induction` | Accept | Solomonoff induction uses a universal algorithmic mixture for sequential prediction under formal computability assumptions. |
| 52 | `solomonoff-induction → contributes-to → aixi` | Accept, scoped | AIXI uses a universal mixture over chronological environments together with sequential decision theory. It is related to, but not simply identical with, Solomonoff prediction. |
| 53 | `sequential-decision-theory → contributes-to → aixi` | Accept | AIXI combines prediction over environments with reward-maximizing sequential action selection. |
| 54 | `aixi-tl → approximates → aixi` | Accept, scoped | AIXI(t,l) is a computable resource-bounded construction over candidate policies; the exact bounds and optimality qualifications in the source review must accompany this shorthand. |
| 55 | `resource-bounded-computation → constrains → aixi-tl` | Accept | Explicit time/program-length bounds are central to the computable construction. |
| 56 | `score-function → prerequisite → score-centering` | Accept | The learner must understand the policy score being centered. The existing bilingual rationale states this dependency and the relation is pedagogical, not an execution edge. |
| 57 | `entropy → prerequisite → cross-entropy` | Remove | Cross-entropy is defined directly from target and predicted distributions. Entropy appears in the decomposition `H(q,p)=H(q)+D_KL(q||p)`, but is not required to define or calculate cross-entropy. Preserve the decomposition as optional mathematical depth. |
| 58 | `cross-entropy → prerequisite → knowledge-distillation` | Weaken relation | Cross-entropy is one possible soft-target distillation objective, but the rationale also allows KL and other formulations. Retype to `cross-entropy → contributes-to → knowledge-distillation`: preserve the useful connection without imposing a false universal learning prerequisite. |

### Corrections applied to the canonical registry

- Reversed and retyped predictive-compression input: `conditional-distribution → contributes-to → predictive-compression`.
- Weakened knowledge distillation → model compression from `part-of` to `contributes-to`; this captures its conditional use with a smaller student.
- Weakened positive-pair distribution → JEPA from `part-of` to `contributes-to`; the distribution shapes the learning signal rather than being an architectural component.
- Removed the document-retrieval / in-context-learning contrast, two overextended Laplacian-eigenmaps / PRH assertions, and the unsupported entropy → prerequisite → cross-entropy assertion; cross-entropy's optional role in distillation is retained as a non-pedagogical contribution.

The four removals reduce the current registry from 124 to **120 typed edges**. Four retyped/reversed relations preserve their edge count. Together with the 66 previously reviewed current assertions, this completes the semantic review of all **120 retained edges**. No new relation type, graph, registry, route, or renderer is introduced.

### Evidence and remaining gates

The review uses the existing bilingual endpoint definitions and relation semantics, with focused technical support from:
- [JEPA / Platonic Representation source review](../source-reviews/platonic-representation-jepa-2026-11.md)
- [AIXI and algorithmic-computability source review](../source-reviews/aixi-kolmogorov-computability-2026-11.md)
- [Predictive V-information source review](../source-reviews/predictive-v-information-xu-2020.md)
- [Score-centering source review](../source-reviews/score-centering-2026-11.md)
- [Information-theory source review](../source-reviews/information-theory-wayland-zhang-2026-11.md)

This closes the **source-semantic edge audit**. It does not close rendered FR/EN graph inspection, touch/keyboard/screen-reader evidence, or an independent learner task. Those remain human validation gates coordinated with #584 and #337. The registry remains a selected conceptual map, not a complete execution DAG.


## 2026-11-25 delta review — lexical frequency concepts

The current canonical registry contains **122 relation assertions**. The preceding review closed the 120 retained assertions then present; two later assertions are reviewed here against their bilingual endpoint definitions, the relation contract, and the FR/EN Zipf lesson.

| Relation | Decision | Scope and rationale |
|---|---|---|
| `zipf-law → approximates → word-frequency-distribution` | **Accept, scoped** | The bilingual lesson defines Zipf's law as an approximate empirical rank–frequency regularity over lexical forms. The target is a corpus-dependent empirical distribution, not a universal or generative law. This edge asserts only an approximation of its rank–frequency structure; it does not assert an exact power law, a fixed exponent, or a causal explanation. |
| `conditional-distribution → contrasts-with → word-frequency-distribution` | **Accept, scoped** | The first is a model-produced distribution over the next token conditioned on a preceding context; the second is an empirical marginal frequency distribution over lexical forms in a specified corpus and under specified counting conventions. They are distinct statistical objects, not mutually exclusive alternatives. |

### Relation-contract clarification

The previous bilingual description of `approximates` referred only to a computable or bounded construction. That wording did not cover an empirical law such as Zipf's law. The canonical description now explicitly includes models, empirical laws and bounded constructions, while requiring the scope and assumptions of the approximation to be stated. This preserves the existing AIXI(t,l) use and does not turn approximation into identity, causal explanation or a learning dependency.

The two edges are not `prerequisite` relations and must not influence the guided route. The FR/EN lesson pair and the two exercise pages remain the explanatory resources; no duplicate concept or page relation is introduced.

**Updated inventory:** 122 current edges, all source-semantically reviewed. The remaining gates are rendered graph inspection, touch/keyboard/screen-reader validation, and an independent learner task; this source audit does not close them.


## 2026-11-27 tokenizer / text-encoding delta review

The exact-ID reconciliation in [#416](https://github.com/JM-Brun/llm-lab/issues/416) identified 25 current assertions not covered by the earlier semantic audit. I reviewed this bounded set against the current bilingual endpoint definitions and the canonical relation-type contract in `data/concepts.yml`. The 122 previously covered assertions were not re-reviewed.

| Current assertion | Decision | Scope and rationale |
|---|---|---|
| `tokenizer → applies-to → tokenization` | Accept | The tokenizer is the mechanism applied to text-tokenization. This does not imply that every tokenizer uses the same pipeline or segmentation algorithm. |
| `tokenizer-pipeline → part-of → tokenizer` | Accept | The configurable pipeline is a component of the tokenizer system. |
| `text-normalization → part-of → tokenizer-pipeline` | Accept | Normalization is an optional/configuration-dependent pipeline stage, not a universal operation. |
| `pre-tokenization → part-of → tokenizer-pipeline` | Accept | Pre-tokenization is a pipeline stage whose presence and behavior depend on the tokenizer configuration. |
| `subword-tokenization → part-of → tokenization` | Accept, scoped | This expresses family membership: subword tokenization is one family of tokenization methods, not a mandatory sequential stage after tokenization. |
| `byte-pair-encoding → part-of → subword-tokenization` | Accept, scoped | BPE is one method in the subword-tokenization family; this is a family-membership relation, not a claim that all subword tokenizers use BPE. |
| `wordpiece → part-of → subword-tokenization` | Accept, scoped | WordPiece is a distinct method in the subword-tokenization family, not a component used by BPE. |
| `unigram-tokenization → part-of → subword-tokenization` | Accept, scoped | Unigram is a distinct probabilistic method in the family, not a stage that follows BPE or WordPiece. |
| `token-vocabulary → part-of → tokenizer` | Accept | The vocabulary is a structural component of a tokenizer and associates recognized units with IDs. |
| `token-vocabulary → produces → token-id` | Accept, scoped | The vocabulary provides the token-to-ID association used by lookup. This is not a claim that the vocabulary alone tokenizes text or emits a complete ID sequence; that sequence is produced by token encoding. |
| `token → represented-by → token-id` | Accept | A token occurrence/unit is represented in the model input by the ID assigned under the associated vocabulary. The ID is vocabulary-relative, not a universal token identity. |
| `special-token → part-of → token-vocabulary` | Accept | Special tokens are reserved entries in the vocabulary, with structural/control roles distinct from ordinary text. |
| `tokenizer-training → contributes-to → token-vocabulary` | Accept | Training/fitting can construct or adjust a vocabulary; the edge does not imply that every tokenizer is trained in the same way or at runtime. |
| `token-decoding → applies-to → token-id` | Accept | Decoding operates on token IDs (or their corresponding token sequence) under the tokenizer's vocabulary and conventions. |
| `tokenizer-evaluation → applies-to → tokenizer` | Accept | The evaluation procedure is applied to a tokenizer; it can include intrinsic measures and downstream evaluation, which must remain distinct. |
| `token-fertility → part-of → tokenizer-evaluation` | Accept, scoped | Fertility is one possible intrinsic measure used within tokenizer evaluation, not a complete definition of tokenizer quality. |
| `tokenizer-evaluation → applies-to → multilingual-tokenization` | Accept, scoped | Evaluation can be conducted in multilingual-tokenization settings. This is an evaluation context, not a prerequisite or a claim that multilingual tokenization is itself an evaluation method. |
| `byte-level-encoding → part-of → tokenization` | Accept, scoped | Byte-level encoding is one possible representation path within tokenization. It is not universal to all tokenizers and must not be conflated with byte-pair merge training. |
| `tokenization → produces → token` | Accept | Tokenization yields a sequence of discrete token units. It does not by itself specify the integer IDs assigned to those units. |
| `token-encoding → produces → token-id` | Accept | Applying a configured tokenizer/vocabulary to input produces the model-facing ID sequence. This is the runtime encoding output. |
| `token-post-processing → part-of → tokenizer-pipeline` | Accept | Post-processing is a pipeline component, for example to add sequence markers or apply configured structural conventions. |
| `token-post-processing → contributes-to → special-token` | Accept, scoped | Post-processing can insert configured special tokens into an encoded sequence. It does not create the special-token definitions or vocabulary entries. |
| `subword-tokenization → part-of → tokenizer-pipeline` | Accept, scoped | The segmentation method is one possible pipeline component. It is not mandatory for byte-level or other tokenizer designs. |
| `token-id → prerequisite → token-embedding` | Accept | The ID is required to index/select the corresponding row of the model's token-embedding matrix. This is a legitimate local pedagogical dependency, not a global route order. |
| `tokenizer-compatibility → prerequisite → token-embedding` | Accept, scoped | Correct lookup requires IDs to use the vocabulary and conventions associated with the model's embedding table. This is a compatibility condition for using the lookup correctly, not an additional computation stage. |

### Delta-review result

- **25/25 previously unaudited current assertions reviewed.**
- Combined with the exact-ID reconciliation (122 covered assertions), the current registry has **147/147 assertions covered** by the semantic audit.
- No relation was changed in this pass: the reviewed assertions are consistent with the existing endpoint and relation definitions when read with the scopes above.
- The scoped interpretations are important for downstream consumers: family membership, optional pipeline stages, intrinsic metrics and tokenizer/model compatibility must not be converted into a global pedagogical sequence or computation DAG.
- This closes the **source-semantic relation review** for the current 147 assertions. It does not close consumer-consistency checks, real touch-device testing, manual screen-reader review or independent learner validation. Those remain with their existing owners (#416, #584, #988 and #447 respectively).

The source and implementation limitations recorded in the tokenization source reviews remain in force; this relation review does not upgrade partial source scans or claim independent reproduction of experiments.


## 2026-11-27 relation-consumer consistency audit

The current consumers were inspected against the canonical `relation_types` metadata and the separation between the concept graph, the guided route, and the page map.

| Consumer | Observed contract | Assessment |
|---|---|---|
| `site/tools/check_concept_registry.py` | Validates every relation type against the supported set; validates bilingual labels/descriptions and direction/family/transitivity/acyclicity metadata. Any type marked `learning_dependency: true` must be directed, acyclic and pedagogical, and each edge of that type must have a bilingual rationale. | Consistent with the canonical relation contract. The only current type marked as a learning dependency is `prerequisite`. |
| `site/tools/build_learning_map.py` | Projects all concept edges and their canonical type metadata (direction, family, transitivity, acyclicity, learning-dependency flag, localized label/description) into the bilingual map payload. | Preserves relation semantics rather than treating every edge as a prerequisite. |
| `site/tools/learning_map_renderers.py` | Uses the projected family, direction, label and description for relation filters, legend and concept details. It traverses relations only to display neighbours and does not build a learning sequence from them. | Consistent. The graph remains an exploratory semantic map. |
| `assign_route_rank` in `site/tools/build_learning_map.py` | Orders page-map presentation from authored `suggested_route.next` and page `hierarchy.children` metadata. It does not read concept relations. | Consistent. This rank is a display heuristic, not a prerequisite order. |
| Guided route and lesson contracts in `data/guided-route.yml` / `build_learning_map.py` | Resolve explicit stages, page memberships and `lesson_contracts.requires` against the authored route sequence. They do not derive route stages or lesson requirements from the concept graph. | Consistent. The pedagogical route remains an independently authored projection. |
| `site/tools/export_knowledge_graph.py` | Exports every relation as a typed predicate. `generalizes` maps to `skos:narrower`; other relation types retain their project-specific `llmlab:* ` predicate. | Semantics are not collapsed into a hierarchy or prerequisite graph. The export currently exposes predicate identity, not the full bilingual relation-type metadata. |
| Tests | `tests/knowledge/test_concept_registry.py` covers the learning-dependency invariants and bilingual rationales; `test_learning_map.py` covers relation metadata projection and page-route ranking; `test_knowledge_graph_export.py` covers non-taxonomic predicate mapping and representative typed edges. | Existing coverage supports the separation. There is no single end-to-end assertion enumerating all 147 predicates across every projection. |

### Interoperability boundary

The JSON-LD export's lack of a published, resolvable vocabulary definition for each `llmlab:*` predicate is a known interoperability limitation, not evidence that the internal graph is using the wrong relation semantics. The prior decision in #416 to defer a public relation-type vocabulary remains appropriate until a concrete external consumer requires it. Do not introduce a second vocabulary registry for the current internal map.

The supported relation-type allowlists in the validator and JSON-LD exporter are explicit code-level guards. They must be updated alongside any future canonical relation-type addition; they are not alternative sources for edge meanings.

### Consumer-audit result

- The current consumers preserve the distinction between semantic relations, pedagogical prerequisites, page-map hierarchy and the authored guided route.
- Only the canonical `prerequisite` type is currently eligible to declare a learning dependency; the validator enforces the required metadata invariants.
- No consumer was found deriving the guided route from all concept edges.
- No production code change is justified by this audit. In particular, do not convert `part-of`, `contributes-to`, `applies-to`, or computation edges into learning prerequisites.
- Remaining #416 work is limited to real touch-device validation of graph selection/navigation. Manual screen-reader and cross-page navigation checks remain with #584/#988; independent learner comprehension remains with #447.

The tests cited above were inspected as source. This documentation pass did not execute them and does not claim a new CI run.
