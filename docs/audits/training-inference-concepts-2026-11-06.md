# Training/inference concepts integration audit (2026-11-06)

## Decision summary

This increment closes a conceptual gap between the training-data branch and the inference path without creating new standalone pages.

- **Teacher forcing** is taught in the existing bilingual training-examples lesson, immediately after shifted input/target construction.
- **Prefill** and **autoregressive decode** are taught in the existing bilingual generation lesson, before the distinction between token-selection decoding and the full generation loop.
- **Autoregressive generation** is made explicit as the parent process containing prefill and iterative decode.
- **Exposure bias** is introduced as a qualified training/inference mismatch in the training lesson and glossary. It is not promoted to a canonical graph node in this increment because the current relation vocabulary does not express its causal/associative relation to teacher forcing without an unjustified edge.
- The existing six domains are sufficient; no new domain is introduced.
- The page metadata tag vocabulary is unchanged. Notion/domain/importance metadata belongs to the concept model, not to page keywords.

## Canonical ownership

| Item | Canonical owner | Why |
|---|---|---|
| Shifted input/target pairs | `site/{fr,en}/training-examples.qmd` | The page already owns the construction and alignment of training examples. |
| Teacher forcing | Same training-examples pages | Explains why the input is the ground-truth prefix and how this differs from inference. |
| Cross-entropy / NLL derivation | Existing cross-entropy, likelihood and loss pages | Avoids duplicating mathematical derivations. |
| Prefill and decode phases | `site/{fr,en}/generation.qmd` | They are phases of inference, not separate model architectures or tokenization stages. |
| KV-cache mechanics | Existing source extraction and external deep-dive reference | The current reference implementation does not implement a KV cache; a cache lesson/page is not created speculatively. |
| Terminology lookup | Bilingual glossary | Concise definitions link to the canonical lessons. |
| Stable notion identity, domain membership and importance | `data/concepts.yml` + `data/domains.yml` | One language-independent concept registry and one controlled domain registry remain authoritative. |
| Guided-stage membership | `data/guided-route.yml` | Training examples are an optional companion in the learning/evaluation stage, not a mandatory prerequisite for inference. |

## Scientific distinctions retained

### Teacher forcing

For shifted examples (x=[t_0,ldots,t_{L-1}]) and (y=[t_1,ldots,t_L]), the model receives the ground-truth prefix at each position and predicts the next token. A causal mask still prevents access to future positions. The model can compute predictions at all supplied positions in one forward pass; the loss is evaluated against shifted targets and a separate optimizer step updates parameters.

Teacher forcing is a conditioning strategy. It is not the next-token objective, the loss function, or the optimizer.

At inference, the reference continuation is unavailable. The selected token is appended and becomes part of the next context. The lesson introduces exposure bias only as a possible distribution mismatch; it does not claim that errors always compound or that teacher forcing is inherently defective.

### Prefill and decode

- **Prefill:** process the initial prompt as a sequence and use the final prompt position's logits for the first token selection. Causal masking remains in force.
- **Autoregressive decode:** iteratively process each newly generated token to obtain the next prediction.
- **KV cache:** when supported, retain previous attention keys and values so decode need not recompute the whole prefix. This is an efficiency optimization, not a correctness requirement.
- **Decoding:** the token-selection procedure (greedy, sampling, filters) is distinct from the *decode phase* of inference.

The implementation at `src/llm_lab/foundations/generate.py` explicitly recomputes the current context at each step and documents that it has no KV cache. The lesson describes prefill/decode as the general inference workload while being precise about the current code's limitation.

## Knowledge model changes

### New concept nodes

| ID | Domain | Importance | Canonical resources |
|---|---|---|---|
| `teacher-forcing` | `probabilistic-foundations-training` | `essential` | FR/EN training examples |
| `autoregressive-generation` | `inference-efficiency` | `essential` | FR/EN generation and walkthrough |
| `prefill` | `inference-efficiency` | `important` | FR/EN generation and walkthrough |
| `autoregressive-decode` | `inference-efficiency` | `essential` | FR/EN generation and walkthrough |

### New typed relations

- `teacher-forcing --applies-to--> training-objective`
- `prefill --part-of--> autoregressive-generation`
- `autoregressive-decode --part-of--> autoregressive-generation`
- `prefill --produces--> logits`
- `autoregressive-decode --produces--> logits`

No new relation type was needed. The new `part-of` edges are structural, not prerequisite edges; they do not drive the learning route.

### Importance metadata

All existing and new concept records now carry a controlled `importance` value:

- `essential`: central to the core conceptual model or a major mechanism;
- `important`: central to a substantial subtopic or recurring technical distinction;
- `specialized`: useful for narrower research or advanced qualification.

This field is deliberately independent of page `level`, page `destination`, route membership and prerequisite edges. The concept registry validator enforces the enum. The interactive map renders localized notion, importance and domain labels on concept cards. JSON-LD emits `llmlab:importance`; the rendered graph validator checks it.

The word “notion” is derived from membership in the canonical concept registry and displayed as a card label. It is not duplicated as a redundant field on every concept. Domain labels are derived from each concept's `domains` membership and the controlled domain registry.

## Pedagogical route changes

- The Prediction-stage objective now includes the distinction between prompt prefill and iterative decode.
- The Learning/evaluation-stage objective now names ground-truth conditioning (teacher forcing).
- Training examples are added as an **optional** resource in that stage. The Build route remains the canonical path for the corpus-preparation and training-example implementation branch.
- The narrative learning path now explains prefill/decode before training, then introduces teacher forcing in the learning section and revisits it in the G2 training-data branch.
- No page-level `suggested_route`, hierarchy or prerequisite edge is added merely to imitate the route order.

## Page metadata boundary

No new page tags such as `notion:` or `domain:` are added to Quarto `keywords`. The existing six page-tag dimensions remain unchanged. Page-level `domain` is still a single primary discovery classification for Deepen pages; concept-level `domains` remains a many-to-many knowledge membership. Concept `importance` is not copied to page `level`.

## Files changed in this increment

- `site/fr/training-examples.qmd`, `site/en/training-examples.qmd`
- `site/fr/generation.qmd`, `site/en/generation.qmd`
- `site/fr/glossary.qmd`, `site/en/glossary.qmd`
- `data/concepts.yml`, `data/guided-route.yml`
- `site/tools/check_concept_registry.py`, `site/tools/build_learning_map.py`, `site/tools/learning_map_renderers.py`, `site/tools/export_knowledge_graph.py`, `site/tools/check_knowledge_graph_rendered.py`
- `site/styles.scss`
- `tests/site/test_concept_registry.py`, `tests/site/test_learning_map.py`, `tests/site/test_knowledge_graph_export.py`
- `docs/learning-path.md`, `docs/page-metadata-schema.md`, `docs/knowledge-graph-standards.md`

## Validation required before merge

- [ ] Run concept registry validation against all published bilingual page IDs and controlled domains.
- [ ] Run page metadata and guided-route validators.
- [ ] Run concept graph, learning-map and JSON-LD tests.
- [ ] Run the complete Python test suite and CI.
- [ ] Render Quarto in FR and EN; verify the training/inference distinction, concept cards, responsive layout and language parity.
- [ ] Verify generated JSON-LD includes all 25 concepts and controlled importance values.
- [ ] Review the generated route to ensure training examples are visibly optional and no new hard prerequisite was inferred.

Source implementation checked: `src/llm_lab/foundations/generate.py` documents full-context recomputation and the absence of KV caching. External cache reference: [Hugging Face KV cache guide](https://huggingface.co/docs/transformers/main/en/kv_cache). Foundational implementation reference: [Raschka, LLMs from Scratch](https://github.com/rasbt/LLMs-from-scratch).
