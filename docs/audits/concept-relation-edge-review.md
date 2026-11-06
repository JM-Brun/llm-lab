# Concept relation edge review

**Date:** 2026-11-05  
**Status:** semantic registry review complete; source-level interaction review recorded; browser/accessibility and learner validation remain open  
**Canonical data:** [`data/concepts.yml`](../data/concepts.yml)  
**Tracking:** [LLM Lab #416](https://github.com/JM-Brun/llm-lab/issues/416), [merged validator PR #520](https://github.com/JM-Brun/llm-lab/pull/520)

## Scope and method

This review covers the 10 declared relation types and all 26 current edges in the canonical concept registry. It checks the intended reading, direction, relation family, and whether the edge should influence learning order. It is a conceptual review, not a proof that the graph is a complete execution graph or a rendered-UX evaluation.

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

After PR #609, the registry contained 68 relations. This follow-up removes one overgeneralized edge from the original 26-edge inventory; the current branch therefore contains 67 relations: 25 retained edges from that historical inventory and 42 later additions. The 42 additions were reviewed against their endpoint definitions, relation-type descriptions, and the separate computational spine; one was subsequently removed as semantically ill-typed, leaving 41 retained additions. This is a semantic review of the selected concept graph, not a claim that it is a complete tensor-level execution DAG.

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

### Remaining semantic decisions

- Edge 9 was removed without replacement: `next-token-prediction` is the task; `training-objective` is the optimized function. Their relationship is explained by the endpoint definitions and the computational graph, not by a structural `part-of` edge.
- Keep the distinction between the concept graph and the computational graph: the latter supplies the explicit differentiation and final-hidden-state operations.
- After removing row 9, the registry contains 66 relation assertions: 25 retained edges from the original inventory plus 41 retained later additions. All 66 have received a source-semantic review. Rendered graph usability, accessibility, and learner validation remain separate gates.
