# Understand destination evidence — batch 5: autoregressive generation

**Issue:** [#1739 — distinctive intellectual value for every Understand lesson](https://github.com/JM-Brun/llm-lab/issues/1739)  
**Review date:** 2026-11-28  
**Scope:** canonical Understand lesson `generation`, its FR/EN counterparts and dedicated Practice companions. The source-level intellectual-contribution audit for this page already exists; this batch applies the #1778 destination-evidence contract and does not repeat the scientific audit.  
**Method:** inspect current Quarto page-map metadata, the bilingual lesson body, explicit anchors, internal links and dedicated Practice companions. This is a source-level destination audit, not a rendered-browser, accessibility or learner validation.

## 1. Generation — `generation`

**Page identity:** `site/fr/generation.qmd` / `site/en/generation.qmd`  
**Declared purpose:** trace selection of the first token from prefill, then feedback of selected tokens until generation stops.

| Local contribution | Claim to preserve | Provenance | FR destination | EN destination | Presence and decision |
|---|---|---|---|---|---|
| `generation-ic-01-forward-pass-selection-and-loop-are-distinct` | The forward pass maps the current context to logits and a conditional distribution; decoding applies a selection rule; generation is the complete autoregressive loop, including feedback and stopping. The model supplies the distribution but does not itself choose a token. | Project-derived computational synthesis, consistent with the canonical computational graph and shared prediction spine. The illustrative probabilities are explicitly fictional, not measured model outputs. | [One-minute summary](../../site/fr/generation.qmd#revision-summary); [three-turn loop](../../site/fr/generation.qmd#la-boucle-sur-un-exemple); [one step in notation](../../site/fr/generation.qmd#une-étape-en-notation) | [One-minute summary](../../site/en/generation.qmd#revision-summary); [three-turn loop](../../site/en/generation.qmd#the-loop-on-an-example); [one step in notation](../../site/en/generation.qmd#one-step-in-notation) | Explicit in both languages. Keep the three levels distinct; do not describe token selection as an internal Transformer operation. |
| `generation-ic-02-selected-token-changes-future-context` | The selected token is appended to the prefix and conditions the next prediction. A different first choice can change later distributions. Greedy selection maximizes the local next-token probability, not necessarily the probability of the complete continuation. | Autoregressive factorization and project-derived worked example; the limitation of local greedy choice is explained directly in the lesson. | [Three-turn loop](../../site/fr/generation.qmd#la-boucle-sur-un-exemple); [selection strategies](../../site/fr/generation.qmd#comment-le-prochain-token-est-il-choisi) | [Three-turn loop](../../site/en/generation.qmd#the-loop-on-an-example); [selection strategies](../../site/en/generation.qmd#how-is-the-next-token-chosen) | Explicit in both languages, with a counterfactual first-token explanation and greedy/sampling distinction. Preserve the fact that later distributions depend on the chosen prefix. |
| `generation-ic-03-fixed-parameters-and-stopping` | Generation changes the context but not the model parameters. It stops according to an explicit criterion such as EOS, a maximum length or an application rule; stopping does not imply that the model has completed a reasoning process. | Project-derived operational definition of free-running inference. | [Three-turn loop](../../site/fr/generation.qmd#la-boucle-sur-un-exemple); [what generation does not do](../../site/fr/generation.qmd#ce-que-la-génération-ne-fait-pas) | [Three-turn loop](../../site/en/generation.qmd#the-loop-on-an-example); [what generation does not do](../../site/en/generation.qmd#what-generation-does-not-do) | Explicit in both languages. The one-minute summary states fixed parameters; the loop explains EOS, length and application stop conditions. Keep these separate from optimizer updates and validation. |
| `generation-ic-04-prefill-decode-kv-cache-and-teacher-forcing` | Prefill processes the known prompt; incremental decode advances generation one token at a time. KV cache optionally reuses prior keys/values for efficiency. Decode is an execution phase, while decoding is the selection policy. Prefill and teacher forcing both condition on known tokens but serve different operational roles. | Project-derived inference/training boundary, consistent with the computational graph and the canonical training/scoring audit. KV cache is an optional optimization, not a correctness prerequisite. | [Prompt, prefill and decode](../../site/fr/generation.qmd#du-prompt-aux-tokens-suivants-prefill-et-decode); [Practice comparison](../../site/fr/exercises/generation.qmd) | [Prompt, prefill and decode](../../site/en/generation.qmd#from-the-prompt-to-subsequent-tokens-prefill-and-decode); [Practice comparison](../../site/en/exercises/generation.qmd) | Explicit in both languages. The Practice companion's fourth self-check compares prefill with teacher forcing and also notes observed-prefix scoring. Preserve the distinction; do not equate prefill with teacher forcing. |

**Practice destination:** [FR](../../site/fr/exercises/generation.qmd) / [EN](../../site/en/exercises/generation.qmd). Both companions have four matching self-check questions: stochastic variation under sampling, low-temperature behavior, fixed parameters during generation, and prefill versus teacher forcing. Each links to the shared [Generation exercise collection](../../site/fr/exercises-generation.qmd) / [EN](../../site/en/exercises-generation.qmd), which contains the longer EOS-loop, distribution-selection, temperature, filtering and KV-cache tasks. This is a deliberate hub→collection relationship; do not create a duplicate second collection.

**Placement decision:** keep the basic autoregressive loop, fixed-parameter semantics, selection distinction, stopping criteria and prefill/decode explanation in Understand. Keep self-checks and learner-directed traces in Practice. Serving latency, scheduling, batching, cache-memory estimates and speculative decoding remain optional Deepen material; the reference-code walkthrough remains in Build.

## 2. Cross-page decisions and route continuity

- The lesson intentionally revisits generation at a greater depth after the early overview preview. The repetition is pedagogical: first observe a complete black-box loop, then inspect the mechanism and notation. It is not a duplicate concept or an extra mandatory route stage.
- The forward computation is shared with scoring and training. Generation differs in its context source: it feeds back the model-selected token. Scoring and teacher-forced training use observed reference prefixes; neither is a generation loop.
- The probability lesson introduces the base conditional distribution. This page explains the inference-specific selection and feedback that follow it. The route cross-reference to generation is a sibling-use explanation, not evidence that scoring or training depends on generation.
- The page distinguishes *decode* (inference phase) from *decoding* (selection policy), and prefill from teacher forcing. These terms must remain distinct in later page migrations and diagrams.
- KV cache is optional and changes computational efficiency, not the underlying conditional prediction rule or model parameters.
- The FR/EN page-map scopes, purposes, route destinations, core claims, stopping semantics and Practice questions match in substance. The examples are localized, so parity is conceptual and computational rather than literal.

## 3. Validation boundary and follow-up

**Completed in this batch:** source inspection of both generation lessons and both dedicated Practice companions; comparison of page-map metadata and local destinations; verification of the explicit anchors and shared exercise-collection links; preservation and placement decisions.

**Not completed:** deployed rendered-anchor verification, visual inspection of the generation trace and figure, responsive/mobile review, keyboard review, manual screen-reader review and learner validation. The earlier browser evidence for the Practice migration is not reused as evidence for this destination audit's current page head.

**Next batch by canonical route order:** `in-context-learning` and `context-engineering`, then `likelihood`, `loss`, `gradients` and `training-loop`. Reuse their existing source audits; do not repeat the already completed scientific analysis.

## 4. Sources and inspected artifacts

- `data/guided-route.yml` — canonical stage order and reader-facing route.
- `data/computational-graph.yml` — shared prediction and generation feedback relations.
- `docs/canonical-computational-spine.md` — generation, scoring and training boundaries.
- `docs/source-syntheses/understand-generation-scoring-training-contributions-audit-2026-11.md` — existing source-level contribution audit.
- `site/fr/generation.qmd`, `site/en/generation.qmd`.
- `site/fr/exercises/generation.qmd`, `site/en/exercises/generation.qmd`.
- `site/fr/exercises-generation.qmd`, `site/en/exercises-generation.qmd`.
