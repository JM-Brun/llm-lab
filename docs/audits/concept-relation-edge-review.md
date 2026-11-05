# Concept relation edge review

**Date:** 2026-11-05  
**Status:** first semantic review; rendered graph and learner validation remain open  
**Canonical data:** [`data/concepts.yml`](../data/concepts.yml)  
**Tracking:** [LLM Lab #416](https://github.com/JM-Brun/llm-lab/issues/416), [validator PR #518](https://github.com/JM-Brun/llm-lab/pull/518)

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
