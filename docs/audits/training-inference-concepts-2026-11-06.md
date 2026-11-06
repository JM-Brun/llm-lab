# Training/inference concepts integration audit — 2026-11-06

## Audit correction

The previous version of this document overstated the state of the bilingual lessons and source catalogue.

At the `main` baseline inspected on 2026-11-06:

- The concept registry already contained `teacher-forcing`, `prefill`, `decode-step` and `autoregressive-generation`, with their domains, importance values and resource links.
- The computational graph already contained training-context and inference-execution nodes/edges for these mechanisms.
- The bilingual canonical pages did **not** actually explain teacher forcing, prefill or incremental decode.
- The glossary did **not** contain these entries.
- The previous audit claimed that several source records had been added to `data/sources.yml`; those identifiers were not present in the current file. This document no longer claims that the source-catalogue work is complete.
- The previous audit also claimed that exposure bias was explained in the training lesson and glossary. It was not present in either page at the inspected baseline; it remains deferred rather than being silently treated as integrated.

This PR repairs the reader-facing gap without adding new pages, graph schemas, route stages or metadata fields.

## Canonical ownership

| Concept | Canonical owner | Boundary |
|---|---|---|
| Shifted input/target pairs | `site/{fr,en}/training-examples.qmd` | Data construction and alignment; not the full training loop. |
| Teacher forcing | Same training-examples pages | Training-time conditioning on the observed prefix; not a loss, optimizer or separate objective. |
| Cross-entropy / NLL | Existing cross-entropy, likelihood and loss pages | Preserve one canonical mathematical explanation for each quantity. |
| Prefill and incremental decode | `site/{fr,en}/generation.qmd` | Inference execution phases; not separate model architectures. |
| Token-selection decoding | Same generation pages and decoding-strategies deep dive | Greedy/sampling/filter policy; distinct from the incremental decode phase. |
| KV-cache mechanics | Glossary entry plus the generation lesson's bounded explanation | Optional inference optimization; the local NumPy reference does not implement it. |
| Terminology lookup | Bilingual glossary | Short definitions link to the canonical lessons. |

## Scientific distinctions

### Teacher forcing

For a token stream, construct shifted examples:

`x = [t_0, …, t_{L-1}]` and `y = [t_1, …, t_L]`.

At input position `i`, the model predicts target `y[i]` from the observed prefix `x[0:i+1]`. The causal mask prevents access to future positions. A standard training forward pass can process all positions of the input sequence in parallel; autoregressive describes the conditional factorization, not a requirement to run one forward pass per token during training.

**Teacher forcing** names this conditioning choice: use the ground-truth prefix from the data rather than previously generated model tokens. It is not the prediction objective, loss function or optimizer. The usual next-token objective is evaluated on the shifted targets; parameter updates are a separate optimization operation.

At inference, the reference continuation is unavailable. A selected/generated token is appended to the context and conditions the next prediction.

The current reference `training_examples.py` constructs sliding windows and shifted targets only. It does not implement a trainable GPT forward pass, teacher-forced execution, gradient propagation or parameter updates. The lesson now states this boundary explicitly.

### Prefill and incremental decode

- **Prefill:** process the initial prompt as a sequence under the causal mask. The model produces logits at each prompt position; the distribution at the final prompt position is used for the first generated-token selection.
- **Incremental decode:** append the selected token and compute the next distribution from the extended context; repeat.
- **KV cache:** an implementation may retain attention keys and values from prefill and earlier decode steps to avoid recomputing the whole prefix. This is an efficiency optimization, not a correctness requirement.
- **Decoding:** the token-selection policy (greedy, sampling, filters) is distinct from the decode phase of inference.

The local `generate.py` reference processes the prompt first, then recomputes the current context window at each generation step. It has no KV cache and no separately optimized incremental-decode kernel. The lesson describes the logical phases without implying that this optimization exists in the code.

## Knowledge-model alignment

No graph or concept registry change is required for this content repair.

The current `data/concepts.yml` records:
- `teacher-forcing`: domain `probabilistic-foundations-training`, importance `core`, resources in both training-examples pages;
- `prefill` and `decode-step`: domain `inference-efficiency`, importance `core`, resources in both generation pages;
- `autoregressive-generation`: domain `inference-efficiency`, importance `core`.

The concept-graph relations include:
- `teacher-forcing --applies-to--> training-example`;
- `prefill --part-of--> autoregressive-generation`;
- `decode-step --part-of--> autoregressive-generation`.

The computational graph separately models execution dependencies, including teacher-forced training context and the prefill-before-decode relation. These edges are not pedagogical prerequisites and do not change the eight-stage guided route.

Importance values use the current controlled enum (`core`, `supporting`, `specialized`). They are concept-level curriculum annotations, not page `level`, route membership or prerequisite weights.

## Source-catalogue status

The earlier version of this audit listed Raschka, Bengio et al., Schmidt and Agrawal/SARATHI source identifiers as if they were present in `data/sources.yml`. A direct inspection of the current source registry did not find those records. No claim of source-catalogue ingestion or scan completion is made in this PR.

The lesson changes are deliberately limited to definitions and operational distinctions already represented in the project model. A separate source-ingestion pass should add records only after the bibliographic details, exact locators and scan status have been verified.

Exposure bias is also deferred: it is not required to explain teacher forcing itself, and a future treatment should qualify the train/inference context mismatch without claiming that errors inevitably compound or that teacher forcing is inherently defective.

## Changes in this PR

- Add a bilingual teacher-forcing explanation immediately after shifted input/target construction.
- Add bilingual prefill/incremental-decode explanations in the generation lesson.
- Clarify the distinction between decode phase and decoding policy.
- State the actual implementation boundary: no executed training, no KV cache, and no optimized incremental decode.
- Add glossary entries for teacher forcing, prefill, incremental decode and KV cache.
- Correct this audit so it reports the actual repository state and does not claim unperformed source-catalogue work.

## Validation required

- [ ] Run page metadata, concept registry and guided-route validation.
- [ ] Run the full Python test suite and CI.
- [ ] Render the bilingual pages and verify equations, diagrams, local links and language parity.
- [ ] Verify the generation lesson does not imply that the current reference uses a KV cache.
- [ ] Verify the training lesson does not imply that `training_examples.py` performs teacher-forced model training.
- [ ] Update the parent architecture issue only after the content PR is merged and validation evidence is available.
