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
| Guided-stage membership | `data/guided-route.yml` | Training examples are an optional companion in the training stage, not a mandatory prerequisite for inference. |

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
| `decode-step` | `inference-efficiency` | `essential` | FR/EN generation and walkthrough |

### New typed relations

- `teacher-forcing --applies-to--> training-objective`
- `prefill --part-of--> autoregressive-generation`
- `decode-step --part-of--> autoregressive-generation`
- `prefill --produces--> logits`
- `decode-step --produces--> logits`

No new relation type was needed. The new `part-of` edges are structural, not prerequisite edges; they do not drive the learning route.

### Importance metadata

All existing and new concept records now carry a controlled `importance` value:

- `essential`: central to the core conceptual model or a major mechanism;
- `important`: central to a substantial subtopic or recurring technical distinction;
- `specialized`: useful for narrower research or advanced qualification.

This field is deliberately independent of page `level`, page `destination`, route membership and prerequisite edges. The concept registry validator enforces the enum. The interactive map renders localized notion, importance and domain labels on concept cards. JSON-LD emits `llmlab:importance`; the rendered graph validator checks it.

The word “notion” is derived from membership in the canonical concept registry and displayed as a card label. It is not duplicated as a redundant field on every concept. Domain labels are derived from each concept's `domains` membership and the controlled domain registry.

## Pedagogical route changes

The final reader-facing route has eight stages: `orientation`, `text-input`, `representations`, `computation`, `prediction`, `inference`, `scoring` and `training`.

- The `prediction` stage ends at logits, the conditional distribution and predictive entropy. It does not include token selection or observed-target likelihood.
- The `inference` stage revisits the canonical generation page for prefill, iterative decode, token selection, feedback and stopping. The same page remains an early black-box preview in `orientation`.
- The `scoring` stage covers likelihood and cross-entropy for observed targets; it does not select a token or update parameters.
- The `training` stage covers aggregated loss and gradients. Cross-entropy is also an optional bridge here, and the Build `training-examples` page remains optional; it explains teacher forcing and shifted targets without becoming an inference prerequisite.
- Evaluation remains cross-cutting. The current scientific-passage ranking exercise stays in Practice and is not misrepresented as a canonical LLM-evaluation lesson in the guided route.
- The narrative learning path distinguishes these branches from the separate G1b → G2 training-data implementation branch.
- Page `suggested_route`, hierarchy and prerequisite edges are reviewed independently; route membership does not create page containment or computational edges.

## Page metadata boundary

No new page tags such as `notion:` or `domain:` are added to Quarto `keywords`. The existing six page-tag dimensions remain unchanged. Page-level `domain` is still a single primary discovery classification for Deepen pages; concept-level `domains` remains a many-to-many knowledge membership. Concept `importance` is not copied to page `level`.

## Source-to-claim audit

The source catalogue now records the following evidence and limitations. These sources serve different purposes; none should be treated as interchangeable proof for every statement.

| Claim used in the lessons | Source and locator | What it supports | Boundary / qualification |
|---|---|---|---|
| GPT training uses shifted targets and obtains a next-token distribution at each input position | Raschka, *Build a Large Language Model (From Scratch)*, Chapter 5, especially §5.1.2 and the companion code | GPT-specific input/target alignment, per-position logits, loss and pretraining workflow | The chapter demonstrates the mechanism; it does not establish that the author names it *teacher forcing*. |
| Training uses true previous tokens while inference uses model-generated previous tokens | Bengio et al. (2015), *Scheduled Sampling*, §1, §2.3–2.4 | The general sequence-prediction distinction and the rationale for scheduled sampling | The paper studies recurrent networks and 2015 sequence tasks. It supports the general conditioning distinction, not Transformer-specific implementation or a universal mitigation recommendation. |
| The consequences of exposure bias should be stated cautiously | Schmidt (2019), *Generalization in Generation*, abstract and bibliographic record | Frames exposure bias as a train–test discrepancy and discusses the debate over its consequences and countermeasures | Only the abstract and metadata were inspected in this pass; the lesson therefore avoids claims about the paper's detailed experiments or a settled consensus. |
| LLM inference has a prompt-prefill phase and an iterative decode phase | Agrawal et al. (2023), *SARATHI*, §2.2, pp. 2–3 | Prefill processes prompt positions in parallel; decode processes the newly generated token; cached K/V avoids recomputing previous projections | The paper is a serving-systems study. Its throughput, utilization and latency measurements are hardware/workload-specific and are not repeated as universal properties in the lesson. |
| KV caching is an optional inference optimization with implementation and memory trade-offs | Hugging Face Transformers, *Cache strategies*, “Default cache” and cache-strategy overview | Cache reuse, DynamicCache, disabling cache, and the existence of alternative cache strategies | The page is versioned on `main`; only the overview and introductory examples were inspected, not every cache class or model-specific behavior. |

### Source records added or updated

- Added `sebastian-raschka-llms-from-scratch-ch05`, `bengio-scheduled-sampling-2015`, `schmidt-exposure-bias-2019`, `agrawal-sarathi-prefill-decode-2023`, and `huggingface-transformers-kv-cache-strategies` to `data/sources.yml`.
- Updated the existing Hugging Face cache-explanation record to connect it to the generation lesson and the autoregressive-generation/decode concepts.
- The source catalogue uses controlled source types, domain themes and retrieval tags. Tags remain retrieval facets; canonical concept identity is carried through `concept_ids`, not duplicated as tags.

## Files changed in this increment

- `site/fr/training-examples.qmd`, `site/en/training-examples.qmd` (including source-to-claim references)
- `site/fr/generation.qmd`, `site/en/generation.qmd`
- `site/fr/glossary.qmd`, `site/en/glossary.qmd`
- `data/concepts.yml`, `data/guided-route.yml`, `data/sources.yml`
- `site/tools/check_concept_registry.py`, `site/tools/build_learning_map.py`, `site/tools/learning_map_renderers.py`, `site/tools/export_knowledge_graph.py`, `site/tools/check_knowledge_graph_rendered.py`
- `site/styles.scss`
- `tests/site/test_concept_registry.py`, `tests/site/test_learning_map.py`, `tests/site/test_knowledge_graph_export.py`
- `docs/learning-path.md`, `docs/page-metadata-schema.md`, `docs/knowledge-graph-standards.md`, `docs/audits/training-inference-concepts-2026-11-06.md`

## Validation required before merge

- [ ] Run concept registry validation against all published bilingual page IDs and controlled domains.
- [ ] Run page metadata and guided-route validators.
- [ ] Run concept graph, learning-map and JSON-LD tests.
- [ ] Run the complete Python test suite and CI.
- [ ] Render Quarto in FR and EN; verify the training/inference distinction, concept cards, responsive layout and language parity.
- [ ] Verify generated JSON-LD includes all 25 concepts and controlled importance values.
- [ ] Review the generated route to ensure training examples are visibly optional and no new hard prerequisite was inferred.

Source implementation checked: `src/llm_lab/foundations/generate.py` documents full-context recomputation and the absence of KV caching. External cache reference: [Hugging Face KV cache guide](https://huggingface.co/docs/transformers/main/en/kv_cache). Foundational implementation reference: [Raschka, LLMs from Scratch](https://github.com/rasbt/LLMs-from-scratch).
