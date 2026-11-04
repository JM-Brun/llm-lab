# Editorial boundary audit — core Understand route

**Audit date:** 2026-11-04  
**Repository baseline:** `main` at `766b703bb5138dda2a9469d46773713b2561f0ca`  
**Method:** `.agents/skills/editorial-boundary-audit/SKILL.md`  
**Status:** bounded source-level audit; recommendations are not yet content migrations.

## 1. Scope and method

The audit covers 12 bilingual page pairs (24 source pages) along the core Understand route:

| Cluster | French / English pages |
|---|---|
| Orientation and inference | `llm-overview`, `generation`, `transformer` |
| Text and input representations | `text-data`, `tokenization-strategies`, `embedding-space`, `positional-encoding`, `contextualized-representations` |
| Attention and prediction | `scaled-dot-product-attention`, `causal-masking`, `logits`, `probabilites` / `probabilities` |

Inspected the page-map metadata, learning outcomes, page leads, headings, relevant body passages, cross-links, and the corresponding entries in:

- `docs/learning-path.md`
- `docs/content-section-mapping.md`, especially the cross-page content ownership contract
- `docs/page-metadata-schema.md`
- `docs/reader-experience-and-editorial-method.md`

The comparison distinguishes a repeated explanatory sequence from a short reminder needed to make a page self-contained. French and English source structures and the main claims were compared for the candidate overlaps. This is not a browser-rendered review, a scientific source re-audit, or a complete audit of all 101 published pages.

## 2. Findings

### F1 — Softmax and temperature are taught substantively in both logits and probabilities

<badge>High confidence</badge>

**Pages:** `site/fr/logits.qmd`, `site/en/logits.qmd`, `site/fr/probabilites.qmd`, `site/en/probabilities.qmd`; with a shorter contextual reminder in `generation.qmd` (FR/EN).

**Evidence in the page bodies:**

- The logits pages derive softmax, show the two-class example `(0, log 3) → (1/4, 3/4)`, discuss softmax invariance/order, explain temperature, and include a temperature explorer and numerical workbench.
- The probabilities pages independently derive the categorical softmax distribution, repeat the same two-class example, give the temperature-scaled formula, and explain its effect on decoding.
- The generation pages provide a qualitative explanation of low/high temperature in the context of selecting the next token. This is a useful local reminder and does not reproduce the derivation.
- The current ownership table already says that `logits.qmd` owns vocabulary scores and that `probabilites.qmd` owns softmax and decoding interpretation. The current logits body therefore exceeds its declared editorial role and the existing ownership contract.

**Classification:** substantive duplication between logits and probabilities; intentional, compact reuse in generation.

**Canonical boundary proposed:**

- **Logits (FR/EN):** own the meaning and shape of the raw vocabulary score vector, what score magnitude/order can and cannot establish, and why logits are not themselves probabilities. Keep at most a minimal transition stating that a normalization step can turn scores into a distribution, with a link to the probabilities page.
- **Probabilities (FR/EN):** own the softmax definition and properties, categorical conditional distribution, numerical example, temperature transformation, and its interpretation for sampling.
- **Generation (FR/EN):** keep the intuitive one-paragraph description of temperature and its effect on next-token choice. Do not add the formula or another worked softmax example here.
- **Deepen — decoding strategies:** retain advanced filters and search methods; do not make these prerequisites for the core loop.

**Proposed change:** remove the full softmax/temperature tutorial and its duplicate interactive temperature material from the logits pages; place the useful interactive temperature demonstration with the canonical probabilities explanation (or replace it there with one bilingual shared-quality interaction). Retain a concise logits-to-probabilities bridge and links. Update both languages together.

**Preservation requirements:** preserve the score-vector definition and shape, the fact that logits are not normalized, the relationship between score differences and probability ratios if judged necessary, numerical-stability caveats, the temperature formula and its interpretation, and the existing interactive learning value. Do not move temperature into Deepen wholesale: the qualitative effect is part of the core generation objective.

### F2 — A stated text-data learning outcome is not visibly taught on that page

<badge color="warning">Medium confidence</badge>

**Pages:** `site/fr/text-data.qmd`, `site/en/text-data.qmd`, and the canonical `tokenization-strategies.qmd` pair.

**Evidence:**

- The text-data learning-outcomes block promises that the reader can explain why whitespace splitting is insufficient.
- The actual text-data body concentrates on the text → tokens → IDs → embedding lookup pipeline, the distinction between prompt encoding and corpus preparation, and links to the tokenization-strategies page. It does not provide a concrete whitespace-splitting counterexample in the inspected explanation.
- The tokenization-strategies pages own the comparison of word, character, byte, and subword granularities, tokenizer components, and worked examples. Their stated purpose is to compare segmentation strategies and their trade-offs.

**Classification:** learning-objective/content mismatch, not evidence of duplicated pages.

**Proposed change:** remove the whitespace-splitting outcome from the text-data learning-outcomes block and ensure it is explicitly tested on the tokenization-strategies page. Alternatively, if the outcome is considered essential to the text-data page itself, add one short counterexample there and leave the full comparison to tokenization-strategies. The first option better preserves the current concise pipeline role.

**Preservation requirements:** keep the distinction between text, bytes, tokens, IDs, and embeddings; keep the short pipeline; retain the explicit link to the canonical tokenization comparison. Do not move Unicode or tokenizer implementation details into the core page.

### F3 — Embedding lookup and contextualization share vocabulary, but the overlap is mostly intentional

<badge>High confidence</badge>

**Pages:** `embedding-space.qmd` and `contextualized-representations.qmd`, FR/EN.

**Evidence:**

- The embedding-space pages teach the lookup contract: an ID selects a row in the embedding matrix; the integer is an index, not a semantic coordinate. They stop before contextualization and direct the reader to the positional and contextualized-representation pages.
- The contextualized-representation pages use the same-ID example to teach a different outcome: identical initial lookup vectors can lead to different hidden states after positional and contextual processing.
- The second page includes the worked contextual example, a three-object comparison table, and misconception checks. These are not reproduced in full by the embedding-space page.
- This matches the existing ownership contract in `content-section-mapping.md`.

**Classification:** intentional prerequisite reminder and complementary coverage, not substantive duplication.

**Decision:** no move, merge, or content deletion recommended. Preserve the concise bridge in embedding-space because the distinction prevents readers from attributing contextual understanding to the lookup operation. Keep the worked same-ID/different-context example canonical in contextualized-representations.

### F4 — Text-data and tokenization-strategies have complementary roles

<badge>High confidence</badge>

**Pages:** `text-data.qmd` and `tokenization-strategies.qmd`, FR/EN.

**Evidence:**

- Text-data owns the end-to-end input pipeline and explicitly delegates segmentation algorithms and comparative examples.
- Tokenization-strategies owns granularities, normalization/pre-tokenization, special tokens, BPE, WordPiece, unigram, and concrete comparisons.
- Text-data's short explanation of tokenizer dependence and its link to the specialized page are useful orientation, not a second tokenizer tutorial.

**Classification:** complementary coverage with an appropriate short recap.

**Decision:** keep both pages and the current route. Do not shorten the text-data pipeline further merely to remove repeated vocabulary.

## 3. Canonical ownership map

| Concept / learner question | Canonical owner | Permitted reuse elsewhere |
|---|---|---|
| Raw text → tokens → IDs → initial embedding lookup | `text-data.qmd` (FR/EN) | A one-line input reminder in generation/Transformer overviews |
| Segmentation units, tokenizer components, BPE/WordPiece/Unigram trade-offs | `tokenization-strategies.qmd` (FR/EN) | A short statement that tokenizer configuration affects IDs and sequence length |
| Token ID → learned vector lookup and embedding-space interpretation | `embedding-space.qmd` (FR/EN) | Contextualized-representations may recall that equal IDs share an initial lookup |
| Positional mechanism families | `positional-encoding.qmd` (FR/EN) | A compact indication of where position enters a system diagram |
| Same initial embedding → context-dependent hidden state | `contextualized-representations.qmd` (FR/EN) | Embedding-space may state that lookup itself does not contextualize |
| Raw vocabulary scores and their interpretation | `logits.qmd` (FR/EN) | Probabilities may identify logits as the input to normalization |
| Softmax, next-token categorical distribution, temperature | `probabilites.qmd` / `probabilities.qmd` | Generation may retain a qualitative temperature reminder; logits may link to this page |
| Iterative autoregressive loop with fixed parameters | `generation.qmd` (FR/EN) | Overview and Transformer pages may locate the loop without reproducing it |

## 4. Core versus optional depth

The sampled route remains coherent:

- **Core prerequisites and explanations:** text/IDs, embedding lookup, positional information at a conceptual level, contextualized states, Transformer computation, attention, causal constraint, logits, probabilities, and the basic autoregressive generation loop.
- **Optional depth:** Unicode/UTF-8 internals; tokenizer implementation and empirical design; RoPE derivation and variants; advanced attention variants such as cross-attention; detailed tensor algebra; advanced decoding filters and search strategies.
- **Build / Practice:** implementation contracts, tests, numerical invariants, and exercises remain linked as evidence or practice, not silently inserted as prerequisites for the conceptual route.

No evidence in this bounded review justifies moving a necessary core explanation into Deepen. The main correction is to make the softmax/temperature ownership consistent between the source pages and the already documented editorial map.

## 5. Recommended implementation order

1. **P1 — Resolve F1 in FR and EN together.** Make probabilities the sole full explanation of softmax and temperature; reduce logits to score interpretation and a concise link. Preserve or relocate the interactive temperature activity.
2. **P2 — Resolve F2 in FR and EN together.** Align the text-data learning-outcomes block with what the page actually teaches; ensure the whitespace-splitting outcome is owned and tested by tokenization-strategies.
3. **No change — F3 and F4.** Keep the current canonical split and short pedagogical reminders.

These are focused edits. Do not combine them with page renames, route redesign, or unrelated scientific revisions.

## 6. Preservation ledger

Before implementing F1/F2, preserve:

- logits: score-vector definition, vocabulary dimension, score-versus-probability distinction, ordering and translation-invariance claims where still relevant;
- probabilities: softmax equation, categorical normalization, conditional-prefix interpretation, numerical example, temperature equation and interpretation, calibration-versus-truth caveats;
- generation: fixed-parameter loop, sampling versus deterministic selection, qualitative temperature effect, stopping criteria;
- text-data: text/bytes/tokens/IDs/embedding distinctions, inference-versus-corpus branch, tokenizer compatibility and explicit hand-offs;
- tokenization-strategies: granularity comparison, tokenizer pipeline components, special-token caveats, algorithm-specific examples, and counterexamples;
- contextualized-representations: same-ID/different-context example, positional qualifications, causal-context caveat, three-object table, and misconceptions.

No source content has been moved or deleted in this audit.

## 7. Validation status

| Check | Status |
|---|---|
| Source metadata and editorial contracts inspected | Passed for the bounded scope |
| FR/EN source comparison | Passed for candidate overlap clusters |
| Page-body overlap classification | Completed for F1–F4 |
| Scientific reference re-audit | Not run |
| Rendered browser review / responsive layout | Not run |
| Quarto render and local-link checks | Not run for this audit report |
| Automated semantic-duplication test | Not applicable; lexical similarity is triage only |

**Conclusion:** the route does not need a structural reorganization based on this sample. The strongest actionable defect is duplicated softmax/temperature teaching across logits and probabilities, plus a smaller learning-outcome mismatch in text-data. The embedding and tokenization page pairs should remain separate.
