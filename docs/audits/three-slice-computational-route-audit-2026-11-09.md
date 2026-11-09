# Three-slice audit of the core computational route — 2026-11-09

**Status:** source-level synthesis of the current bilingual route and computational graph. No lesson content, route registry, graph registry, generator, workflow, or tests are changed by this audit.

**Purpose:** continue the three bounded audits requested for the main LLM Lab learning path before any broader page reorganization.

**Canonical references:**
- `data/guided-route.yml` — eight-stage pedagogical route.
- `data/computational-graph.yml` — shared computation and its typed branches.
- `LLM-LAB-PAGE-MAP` metadata in each lesson — page scope, purpose, route and hierarchy.
- `docs/page-audit-inventory.md` — evidence ledger for page-level reviews.

This report is a synthesis, not a replacement for those sources.

## Executive result

| Slice | Source-level result | Decision |
|---|---|---|
| Stages 2–3: text → IDs → embeddings → position → contextual states | The conceptual objects and their dependencies are distinguished. The transition is understandable without requiring Q/K/V or block internals. | Preserve the four-page sequence; keep Transformer internals at a functional, introductory level in stage 3. |
| Stage 4: Transformer → Q/K/V → attention → causal mask | The four pages answer different questions and their scopes hand off coherently. | Preserve the sequence and the separation of roles, calculation, and visibility constraint. |
| Stages 5–8: prediction → generation / scoring / training | The computation registry represents the three uses as sibling branches from the shared predictive distribution. The pedagogical route is intentionally linear and must not be read as an execution graph. | Preserve both representations; use the computational spine, not page order, to explain the three uses. |

No evidence from this source pass justifies redesigning the curriculum, adding a new graph, introducing another navigation registry, or merging pages.

## 1. Stages 2–3 — From text to contextualized representations

### Pages inspected

- `site/{fr,en}/text-data.qmd`
- `site/{fr,en}/embedding-space.qmd`
- `site/{fr,en}/positional-encoding.qmd`
- `site/{fr,en}/contextualized-representations.qmd`

### Conceptual dependency

1. **Text → tokens → IDs.** The tokenizer defines discrete units and maps them to vocabulary indices. An ID is an index, not a semantic coordinate.
2. **IDs → initial embeddings.** The embedding lookup selects a learned row. For a fixed matrix and ID, repeated occurrences retrieve the same initial vector.
3. **Positional information.** Its insertion point depends on the architecture: absolute vectors may be added at input; relative mechanisms act in attention; RoPE rotates Q/K after projection. It is not universally an extra vector added during lookup.
4. **Contextualized states.** Subsequent network computation combines initial representations with position and surrounding accessible context. The same initial ID can therefore lead to different hidden states.

### Findings

- `text-data` deliberately groups positional handling with Transformer processing in its overview diagram and explicitly warns that this is a simplification. Its stepper then links separately to embeddings, position, and contextualized representations. This is a sound overview-to-detail transition.
- `embedding-space` distinguishes token embeddings, contextualized states, and sentence/document embeddings. Its worked lookup makes the index semantics concrete. The optional code trace labels its embedding and position values as synthetic and explicitly states that it does not run a Transformer block.
- `positional-encoding` separates positional mechanisms from causal visibility. The permutation-equivariance derivation is in a collapsed optional section; the core explanation remains focused on why order information is needed and where it enters.
- `contextualized-representations` uses the same-ID/different-context example and a three-object comparison table. Its generic block equation is explicitly conceptual, not an implementation contract. The causal-decoder versus bidirectional-encoder distinction is brief and architectural, rather than a premature derivation of attention.
- The FR/EN page purposes and examples inspected are semantically aligned. The external orientation figure on contextualized representations remains subject to the existing rights review in issue #156; this audit does not change that asset.

### Boundary to preserve

Stage 3 must explain **what changes and why**: identical lookup can lead to context-dependent states. It need not teach the internal Q/K/V projections, score normalization, causal-mask API conventions, residual paths, or MLP equations. Those belong to stage 4 and its optional implementation/deepening material.

The existing references from contextualized representations to Q/K/V and attention are useful forward links; they should not turn those mechanisms into prerequisites for understanding the distinction between initial and contextualized vectors.

**Disposition:** no source defect requiring a content edit was established. Preserve the sequence and its current level separation. Revisit only if the learner pilot shows that the functional explanation is insufficient or that the position page is being mistaken for a universal additive embedding.

## 2. Stage 4 — Transformer, Q/K/V, attention, and causal masking

### Pages inspected

- `site/{fr,en}/transformer.qmd`
- `site/{fr,en}/queries-keys-values.qmd`
- `site/{fr,en}/scaled-dot-product-attention.qmd`
- `site/{fr,en}/causal-masking.qmd`

### Distinct reader questions

| Page | Unique question | Boundary |
|---|---|---|
| Transformer overview | How does a GPT forward pass transform input states into logits? | Summarizes self-attention and MLP inside repeated blocks; detailed attention math is delegated. |
| Q/K/V | What are the three learned projections, and what roles do they play? | Defines projections, dimensions, and routing-versus-content roles; does not derive the full attention calculation. |
| Scaled dot-product attention | How do Q/K scores become normalized weights that aggregate V? | Derives scores, scaling, optional mask insertion, softmax, and aggregation; does not define the causal visibility policy. |
| Causal masking | Which query-key interactions are allowed in an autoregressive model? | Defines the visibility constraint and distinguishes it from padding, document-boundary, and loss masks. |

### Findings

- The Transformer overview explicitly stops at logits and points to the three canonical pages for detailed Q/K/V, attention, and causal-mask treatment. Its description of attention versus MLP is appropriately functional.
- Q/K/V are located inside each attention sublayer. The page correctly states that the input (X) is the current sublayer input: it may be an initial representation in the first block and a contextualized hidden state in later blocks.
- Q/K/V's optional training-gradient explanation and architecture variants are collapsed deepening material. They do not alter the core question of what Q, K, and V do.
- The attention page owns the score → scale → optional mask → softmax → weighted aggregation calculation. It explicitly distinguishes raw scores, normalized weights, and output vectors.
- The causal-mask page owns the allowed/blocked relation and the no-future-information invariant. Its API-specific boolean polarity and fully masked-row behavior are qualified as implementation conventions, not universal definitions.
- The causal-mask → logits hand-off is already explicit in both languages. The attention-score-scaling page is exposed as an optional deep dive in the computation stage; it is not a core prerequisite.
- Repeated references to Q/K/V roles between the Q/K/V and attention pages are intentional scaffolding: the first introduces the objects, the second uses them in a derivation. They should not be removed merely to eliminate repeated terminology.

### Boundary to preserve

Do not collapse the four questions into a single Transformer lesson. Do not describe Q/K/V, attention, and causal masking as interchangeable variants of one operation. Keep implementation-specific mask conventions and code walkthroughs optional or in Build/Deepen.

**Disposition:** the page sequence and hand-offs are coherent in source. No broad rewrite or page merge is justified. Rendered checks and evidence already recorded for the relevant slices remain scoped to their exact PR heads; this report does not upgrade source inspection into a new site-wide browser or accessibility certification.

## 3. Stages 5–8 — Predictive distribution and its three uses

### Pages and registries inspected

- `site/{fr,en}/logits.qmd`
- `site/{fr,en}/probabilites.qmd` / `probabilities.qmd`
- `site/{fr,en}/entropy.qmd`
- `site/{fr,en}/generation.qmd`
- `site/{fr,en}/vraisemblance.qmd` / `likelihood.qmd`
- `site/{fr,en}/cross-entropy.qmd`
- `site/{fr,en}/loss.qmd`
- `site/{fr,en}/gradients.qmd`
- `data/guided-route.yml`
- `data/computational-graph.yml`

### Shared boundary and sibling branches

The shared computation ends at the conditional distribution over the next token. The graph then distinguishes:

1. **Generation / inference:** a decoding policy selects a token; that token is appended to the context and the next forward pass uses the extended context. Parameters remain fixed.
2. **Observed-target scoring / evaluation:** a reference target is scored under its observed prefix; sequence log-likelihood, NLL and held-out metrics are computed without selecting a generated token or updating parameters.
3. **Training:** observed targets define per-token penalties; a specified reduction and target mask form the objective; gradients are computed and an optimizer may update parameters.

The existing graph encodes these as distinct branches. In particular, it represents distribution → generated token → feedback separately from distribution + observed target → target probability → log-probability/NLL. The training branch continues through loss reduction, objective, gradients, optimizer update, and updated parameters. Evaluation aggregates scores without an optimizer update.

### Findings

- The probability lesson distinguishes logits, a normalized conditional distribution, temperature, predictive entropy, and factual truth. It points to likelihood for observed sequences and cross-entropy for target scoring/loss.
- The generation lesson distinguishes one prediction/selection step from the autoregressive loop, keeps parameters fixed, and separates prompt prefill and incremental decode from decoding policies. Its two guided-route memberships (Orientation preview and Inference detail) are intentional.
- The likelihood lesson explicitly uses observed reference prefixes, makes clear that no generated token is fed back, and states that scoring has no gradient or parameter update. Its one-forward-pass claim is qualified by context-window length and the need for a windowing/stride protocol beyond it.
- Cross-entropy is a shared mathematical bridge: it scores an observed target and supplies the per-token penalty used in a training objective. It is core in the scoring stage and optional in the training stage by design.
- Loss owns reduction and target masking; gradients own differentiation and the parameter-update explanation. The gradient lesson now connects the single-position (p-y) derivative to the scaling for a mean over valid target positions.
- Teacher forcing is reference-prefix conditioning in training examples; it is not the inference prefill phase. Prefill/decode are inference execution phases. The source pages and graph preserve this distinction.
- The guided route stages 5–8 are a pedagogical order, not a single runtime loop. The page-level suggested-route chain is also linear and intentionally does not encode the second visit to generation. These are separate projections, not defects in the computational graph.
- The graph's shared distribution node is assigned to the shared prediction and relevant branch memberships; generation feedback and observed-target scoring are represented by different directed edges. The training-only nodes begin at the objective/gradient/update path.

### Remaining orientation question

The probability lesson's local “Further reading” links emphasize likelihood and cross-entropy, while the full sibling-branch relationship is most explicit in the persistent computational-spine view. This is not a source-level contradiction: the generation lesson and likelihood lesson each explain their own operation, and the graph records the three branches. Whether the probability lesson itself needs a compact three-branch orientation cue is a learner-comprehension question, not a reason to duplicate the full graph or add a second diagram.

Use issue #447 to test whether readers can explain, after reaching the conditional distribution:

- why generation feeds a selected token back;
- why scoring uses an observed target and fixed parameters;
- why training uses observed targets but additionally differentiates and updates parameters.

Only add a local bridge if this test reveals a reproducible navigation or comprehension gap.

**Disposition:** preserve the three sibling branches and the current canonical registries. Do not linearize them into a single execution sequence or make scoring a prerequisite for generation, or vice versa.

## Cross-slice decisions

1. The guided route answers **what to learn next**; the computational graph answers **what is computed and how branches relate**; page hierarchy and suggested-route metadata answer other navigation questions. Do not infer one from another.
2. Keep stage 3 functional and intuitive; defer Transformer-internal mechanics to stage 4.
3. Keep stage 4 decomposed by object, calculation, and visibility constraint.
4. At the conditional distribution, show the three uses as sibling operations. The learning route may order the lessons, but must not imply that one use is an execution prerequisite for another.
5. Preserve the distinctions: prefill vs teacher forcing; decode phase vs decoding policy; predictive entropy vs observed-target likelihood; per-token cross-entropy vs aggregated loss; loss gradient vs optimizer update.
6. Do not add a new registry, workflow, diagram framework, page-level JavaScript, or per-page orientation configuration for these findings.

## Evidence already recorded (do not duplicate)

- [PR #717](https://github.com/JM-Brun/llm-lab/pull/717): bilingual suggested-route card coverage and placement across the 18-page core chain.
- [PR #722](https://github.com/JM-Brun/llm-lab/pull/722): eight-stage route/page mapping, generation's two readings, Build-branch boundaries, bounded mathematical spot checks, and exercise prerequisite audit.
- [PR #724](https://github.com/JM-Brun/llm-lab/pull/724): bounded Transformer/attention → prediction/scoring/inference → Build-data scientific and test-quality audit.
- [PR #725](https://github.com/JM-Brun/llm-lab/pull/725): Q/K/V rendered-evidence hand-off.
- [PR #745](https://github.com/JM-Brun/llm-lab/pull/745): revalidation that attention-score-scaling is optional in the computation stage.
- [PR #787](https://github.com/JM-Brun/llm-lab/pull/787): concise bilingual page summaries and generation-lesson boundary clarification.
- [PR #794](https://github.com/JM-Brun/llm-lab/pull/794) and [PR #795](https://github.com/JM-Brun/llm-lab/pull/795): formative generation, prefill/decode, and KV-cache exercises.
- [PR #800](https://github.com/JM-Brun/llm-lab/pull/800): 18-page core route review, generation/gradient corrections, missing summaries, and remaining observations about route projections.

This synthesis does not claim to repeat or supersede the evidence in those PRs.

## Validation limits and next actions

This pass inspected source files and canonical registries. It does not claim:
- a fresh full-site Quarto render or browser run for this documentation-only synthesis;
- a manual screen-reader or touch-device test;
- learner comprehension or transfer evidence;
- a fresh exhaustive mathematical certification of all 18 core page pairs.

Next actions:
1. Keep this audit as the bounded decision record; do not launch a wider content rewrite.
2. Run the existing learner pilot in #447 against the three-branch explanation and the stage-2/3 conceptual distinctions.
3. Keep manual FR/EN screen-reader and breadcrumb evidence in #584; do not substitute automated Axe results.
4. Reopen a page-level change only when a concrete reader-facing defect or learner-test finding identifies its canonical owner.
