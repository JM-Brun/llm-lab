# Group audit — Prediction stage (2026-11-06)

## 1. Scope

- **Group model:** guided-route stage `prediction` in `data/guided-route.yml`.
- **Core pages (FR):** `fr/logits`, `fr/probabilites`, `fr/vraisemblance`, `fr/generation`.
- **Core pages (EN):** `en/logits`, `en/probabilities`, `en/likelihood`, `en/generation`.
- **Optional resource:** `fr/decoding-strategies` / `en/decoding-strategies` (Deepen, advanced).
- **Context:** causal masking, Transformer overview, LLM overview, the learning path, Build milestones G6–G7, and the route-reconciliation audit dated 2026-11-05.
- **Boundary:** this is an audit of the prediction stage and its cross-stage reuse. It does not re-audit the Transformer computation stage or the learning-evaluation stage.
- **Revision/date:** `main`, 2026-11-06.
- **Evidence limits:** source-level inspection; no Quarto render or browser review in this audit.

## 2. Purpose and intended reader journey

The stage connects the final hidden representation to token-level predictions and then to the probability of an observed sequence. Its intended conceptual path is:

1. **Logits:** interpret the vocabulary-sized vector of unnormalized scores.
2. **Probabilities:** normalize scores into a conditional categorical distribution and understand temperature.
3. **Likelihood:** combine conditional probabilities for observed tokens into a sequence likelihood and log-likelihood; connect negative log-likelihood to the training objective.
4. **Generation:** understand how a fixed-parameter model repeatedly predicts and selects tokens in an autoregressive loop.

The fourth item has a special role: the same canonical generation page is already used in the `orientation` stage as a black-box preview. Its membership in `prediction` is an intentional revisit that reconnects the complete inference loop to the detailed output concepts. It is not a second generation lesson and is not the next prerequisite after likelihood.

## 3. Group map

| Page | Membership role in this stage | Destination / depth | Contribution and boundary |
|---|---|---|---|
| `logits.qmd` | Core concept | Understand / core | Output projection and vocabulary scores; explicitly excludes probability normalization. |
| `probabilites.qmd` / `probabilities.qmd` | Core concept | Understand / core | Conditional distribution, softmax, temperature, calibration boundary and token selection. |
| `vraisemblance.qmd` / `likelihood.qmd` | Core bridge | Understand / core | Probability of observed token sequences, chain-rule factorization, log-likelihood and NLL; bridges prediction to learning. |
| `generation.qmd` | Core stage resource; cross-stage revisit | Understand / core | Complete autoregressive inference loop with fixed parameters; previewed in Orientation and revisited after output concepts. |
| `decoding-strategies.qmd` | Optional | Deepen / advanced | Top-k, top-p, beam/contrastive methods and quality-diversity trade-offs; not needed for the core stage outcome. |

**Context, not core membership:** `causal-masking` and `transformer` explain how the final hidden states are computed; `llm-overview` frames the system and introduces the early generation preview; `cross-entropy` and `loss` take the likelihood bridge into learning; `build-path` describes implementation milestones rather than the conceptual sequence.

## 4. Overall assessment

**Coherent with a well-documented intentional revisit; one objective-level omission and one rendered-UX verification dependency.**

The first three pages form a strong concept chain. The likelihood page is a useful bridge, not a detour: it changes the question from “what distribution does the model assign to the next token?” to “what probability does the model assign to this observed sequence?” and then points toward NLL/cross-entropy.

Generation is correctly a distinct process from the probability and likelihood concepts. Its presence in both Orientation and Prediction is explicitly documented in the reconciliation audit as an intentional preview/revisit. The route documentation also states that pages inside a stage are complementary resources, not strict prerequisites. Therefore, a flat page list must not be interpreted as a strict four-step dependency chain.

The stage objective, however, mentions logits, probability distribution and next-token selection but does not explicitly name the probability of an observed sequence, even though likelihood is a core page. This is a small source-level mismatch between objective and coverage.

## 5. Page-level observations

### Logits

- The page defines a vocabulary-sized vector (z\in\mathbb{R}^{V}), separates scores from probabilities, and explains the argmax boundary.
- It explicitly links to probabilities as the next concept and to cross-entropy as the training-time consumer of logits.
- FR and EN scopes, learning outcomes, example, and route hand-off align in the inspected source.

### Probabilities

- The page owns softmax, the conditional distribution (p_\theta(x_t\mid x_{<t})), temperature, calibration, and the distinction between probability and factual truth.
- It explicitly distinguishes next-token probabilities from sequence likelihood, entropy and training loss.
- It points to likelihood for the product/logarithm over observed tokens and to decoding/generation concepts for selection.
- FR and EN cover equivalent equations, numerical example, temperature behavior, calibration caveats and core transitions.

### Likelihood

- The page uses the chain rule rather than an independence assumption between tokens.
- It distinguishes sequence likelihood, log-likelihood, NLL, per-token averaging and batch-level loss reduction.
- It points to cross-entropy and loss as the next learning connection.
- FR and EN preserve the same mathematical scope, numerical example, tokenizer comparability caveat and transition.

### Generation

- The page defines the autoregressive loop with fixed parameters and distinguishes forward pass, decoding and generation.
- It describes greedy selection, sampling, temperature and stopping criteria, while leaving advanced filters to the optional decoding deep dive.
- Its local route metadata remains `previous: llm-overview`, `next: text-data`; it does not pretend to follow likelihood as a page-level next step.
- FR and EN preserve the same system-level scope and explicit boundary between inference and parameter learning.

### Decoding strategies

- The optional page begins from the canonical generation lesson and clearly marks itself as a deeper treatment.
- It separates local distribution transformations from search over sequences and warns that likelihood maximization does not universally optimize open-ended text quality.
- Its `Deepen` / `advanced` role is consistent in both languages.

## 6. Group-level findings

### PRED-01 — The stage objective omits sequence likelihood

- **Severity:** low to medium (P2).
- **Scope:** stage definition / objective-to-coverage alignment.
- **Evidence:** `data/guided-route.yml`, stage `prediction`, objective currently names logits, probability distribution and next-token selection; the same stage's core page list includes `vraisemblance` / `likelihood`. Both likelihood pages explicitly teach sequence probability, log-likelihood and NLL.
- **Impact:** the stage objective under-describes one of its central conceptual outcomes and can make the likelihood page appear like an incidental extra rather than the bridge from token-level prediction to sequence-level scoring.
- **Recommendation:** revise the FR/EN objective to name the probability (or likelihood) of an observed sequence in addition to the conditional next-token distribution and selection. For example, the objective should communicate: logits → conditional distribution → observed-sequence likelihood → next-token selection / autoregressive generation. Keep the objective concise and equivalent across languages.
- **Acceptance criterion:** every core page contributes visibly to the stated stage objective, and likelihood is understood as a sequence-level bridge rather than a decoding strategy.
- **Preservation:** do not merge likelihood into probabilities or cross-entropy; retain its distinct scope and worked sequence example.

### PRED-02 — Generation is reused across Orientation and Prediction; the rendered route must preserve the preview/revisit meaning

- **Severity:** observation / P2 validation dependency; not a confirmed source defect.
- **Scope:** cross-stage membership and rendered navigation.
- **Evidence:** `data/guided-route.yml` lists generation in both `orientation` and `prediction`. `docs/learning-route-reconciliation-2026-11-05.md`, sections 2 and 6, explicitly defines this as an intentional preview/revisit: Orientation is a black-box preview; Prediction reconnects token selection to logits and probabilities. The same audit records rendered desktop/mobile and learner validation as outstanding. `site/fr/generation.qmd` and its EN counterpart keep local route metadata `llm-overview → text-data`, rather than placing generation after likelihood. The learning-map pages state that pages within a stage are complementary resources, not strict prerequisites.
- **Impact:** if the generated route UI looks like a strict ordered list, the repeated generation page may be read as an accidental duplicate or as a mandatory fourth step after likelihood. Source documentation already explains the intent, but the visible experience has not been confirmed.
- **Recommendation:** preserve the two stage memberships and canonical page. In the rendered route, make the stage description or card context communicate that generation is first previewed as a whole system and revisited after studying its output. Do not create a second generation page or alter its local previous/next metadata to fit the stage list.
- **Acceptance criterion:** a reader can identify one canonical generation lesson, understand why it appears in both stages, and does not infer that likelihood is a prerequisite for the initial generation preview.
- **Preservation:** retain the early system preview; it is an explicit project-level pedagogical decision.

### PRED-03 — The optional decoding deep dive is correctly separated from the core sequence

- **Severity:** verified / no defect.
- **Scope:** optional depth and destination.
- **Evidence:** `data/guided-route.yml` places `decoding-strategies` under `optional_pages`; FR/EN metadata identify it as `type:deep-dive`, `destination:deepen`, `level:advanced`. Its opening points back to the generation lesson and states that it extends the basic loop.
- **Impact:** none identified. This separation avoids burdening the core route with beam search, top-k/top-p and contrastive decoding.
- **Disposition:** preserve; no change required.

## 7. Sequence and transition analysis

Two different maps are necessary.

### A. Conceptual dependency / explanation map

`causal masking → logits → probabilities → likelihood → cross-entropy / loss`

- Causal masking and Transformer computation establish the contextualized representation and output computation.
- Logits define the output scores.
- Probabilities normalize those scores into a conditional distribution.
- Likelihood combines conditional probabilities for the observed sequence.
- Cross-entropy/NLL and loss connect sequence scoring to parameter learning.

Generation is a process map branching from logits/probabilities:

`context → forward pass → logits → distribution → decoding/selection → append token → repeat`

### B. Guided-stage membership / reader-experience map

- `orientation`: LLM overview + generation preview.
- `prediction`: logits + probabilities + likelihood + generation revisit.
- `decoding-strategies`: optional Deepen resource associated with prediction/generation.

The two maps are compatible because stage membership is not a strict prerequisite relation and because generation is intentionally reused.

| From → To | Established by previous page | Assumed by next page | Bridge quality | Action |
|---|---|---|---|---|
| Causal masking → Logits | Final contextualized state at the prediction position | Output projection to vocabulary scores | Strong in the wider Transformer/output explanation; logits page states its position | Preserve |
| Logits → Probabilities | One unnormalized score per vocabulary token | Softmax and conditional categorical distribution | Strong: explicit previous/next metadata and route cards | Preserve |
| Probabilities → Likelihood | (p_\theta(x_t\mid x_{<t})) | Chain-rule product over observed target tokens | Strong: probability page explicitly points to sequence likelihood | Preserve |
| Likelihood → Cross-entropy / Loss | Sequence log-likelihood and NLL | Target distribution and token-level objective / batch reduction | Strong: likelihood page explicitly points to both | Preserve |
| Generation preview → Detailed prediction concepts | Whole loop observed as a black box | Internal output scores and conditional distribution | Deliberate overview → detailed mechanism | Preserve; explain the revisit |
| Likelihood → Generation | Sequence scoring and observed-token probabilities | Iterative generation with fixed parameters | Not a prerequisite transition; two distinct views of autoregressive probabilities | Do not imply linear dependency |
| Generation → Decoding strategies | Basic token selection loop | Distribution filters and sequence-search methods | Strong optional deep-dive hand-off | Preserve |

## 8. Coverage, overlap, and level boundaries

- **Useful reinforcement:** generation revisits logits and probabilities to situate them in the complete loop. This is a deliberate system overview, not duplication of their mathematical treatment.
- **Useful bridge:** likelihood links next-token conditional probabilities to sequence-level scoring and then to the training objective.
- **No demonstrated contradiction:** the audited FR/EN pages preserve the distinction between inference with fixed parameters and learning with parameter updates.
- **No overreach in the optional page:** decoding strategies distinguish local distribution transforms from sequence search and state task-dependent limitations.
- **Boundary to learning:** cross-entropy/loss are not folded into likelihood; they are linked as downstream learning concepts.
- **Boundary to Build:** the conceptual stage does not claim that a complete checkpoint-based generation or training pipeline is already implemented.

## 9. Navigation and project integration

- `suggested_route` for logits → probabilities → likelihood is explicit and aligned in FR/EN.
- The likelihood page points onward to cross-entropy and loss; this is a cross-stage hand-off into learning.
- Generation's local route is intentionally independent: LLM overview → text/data. This preserves its early-preview function.
- The guided route YAML intentionally reuses generation in Orientation and Prediction. The 2026-11-05 reconciliation report records the rationale and calls for a rendered/learner check.
- The learning-map pages explicitly state that pages within a stage are complementary resources, not strict prerequisites.
- Build milestones G6–G7 describe token prediction/selection and autoregressive generation on the inference branch; G8 learning is separate and requires training examples plus the model path.
- Optional decoding strategies are clearly classified as Deepen/advanced in both languages.
- **Bilingual parity:** structural parity is confirmed for the four core pages and optional decoding page. Semantic parity is high in the inspected scope, equations, examples, caveats and navigation. This is a source-level comparison, not exhaustive line-by-line or rendered parity.

## 10. Prioritized action plan

| Priority | Action | Sources | Verification |
|---|---|---|---|
| P2 | Add sequence likelihood / observed-sequence probability to the stage objective in both languages | `data/guided-route.yml` | Objective covers the actual core-page set without suggesting likelihood is a decoding algorithm |
| P2 | Complete the already-tracked rendered desktop/mobile and learner validation for the repeated generation resource | Existing ownership in `docs/learning-route-reconciliation-2026-11-05.md`, #337/#417/#225 | Readers recognize one canonical page and understand preview → revisit; route is not mistaken for a strict prerequisite chain |
| P3 | Preserve optional decoding as a Deepen branch; no content change needed | `data/guided-route.yml`, FR/EN decoding pages | Generator confirms optional resource resolution; no duplicate core lesson |

No canonical source was changed in this audit. The stage-objective wording is a recommendation, not an implemented change. Rendered behavior remains an open validation item; do not duplicate or rewrite the existing reconciliation work.

## 11. What is already working

- The three-page logits → probabilities → likelihood chain has explicit route metadata and pedagogically distinct ownership.
- Likelihood is correctly treated as a sequence-level quantity, not as a synonym for next-token probability or batch loss.
- Generation is introduced early as a black-box preview, then revisited in context; the rationale is explicitly documented.
- The route registry and learning-map page distinguish stage membership from strict prerequisites.
- Advanced decoding is optional and correctly assigned to Deepen.
- The FR/EN pages are closely aligned in the inspected core teaching intent.

## 12. Open questions and confidence

- **Open validation:** rendered route appearance and the learner's interpretation of generation's repeated membership. Source intent is explicit, but the user-facing experience is not established by this audit.
- **Open implementation decision:** whether to revise the stage objective now or coordinate it with a broader route-copy pass. The mismatch is small and does not require a structural change.
- **Not checked:** Quarto render, generated include output, desktop/mobile layout, keyboard/touch accessibility, local link validation, and CI.
- **Confidence:** high for source-level page roles, route metadata, cross-stage reuse rationale and conceptual transitions; medium for semantic bilingual parity; low-to-medium for user-visible interpretation until browser/learner review.

## 13. Skill calibration from this application

This case tests a second pattern beyond mixed Understand/Practice stages: **one canonical page may intentionally belong to multiple guided stages**, serving as an early preview and a later conceptual revisit.

Reusable rule added:
- Audit cross-stage page reuse explicitly. For every repeated page ID, determine whether the repetition is an intentional preview/revisit, a context link, a duplicate listing, or a true conflict. Compare the narrative curriculum, all stage memberships, page-level suggested_route/hierarchy, and the existing reconciliation decision. Do not infer a duplicate page or sequential dependency from repeated membership. If the intended revisit is documented but rendered/learner behavior is unverified, close the source-level intent check as verified and retain only the rendered UX as an open validation item.

## Revalidation log

- 2026-11-06: Compared FR/EN metadata and core explanations for logits, probabilities, likelihood and generation; inspected both decoding deep dives; checked the guided-route registry, learning-map route explanation, Build G6–G8 boundary, and the 2026-11-05 route-reconciliation decision. Confirmed that generation's two-stage membership is intentional at source level. No rendered behavior was claimed as verified.
