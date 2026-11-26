# Visual audit pilot — prediction and inference (2026-11-26)

**Scope:** EN/FR Understand lessons for logits, probabilities, entropy, generation and in-context learning, plus adjacent core visuals for the LLM overview, Q/K/V, cross-entropy and the training loop.  
**Status:** source-level audit and responsive changes completed; Quarto build and browser rendering remain unverified.

## Decisions

| Lesson | Existing visual support | Decision | Rationale |
|---|---|---|---|
| Logits | Worked four-token output-projection table and a diagram showing that adding a common offset leaves softmax unchanged | **Retain; add mobile composition** | The figure teaches an important invariance that the table alone does not show. Its 1120 px layout is too wide for legible mobile scaling. A stacked mobile version keeps both logit vectors, their equal gaps and the identical softmax distribution. |
| Probabilities | Numerical table with logits, exponentials and normalized probabilities; conditional-probability equations; an ordered decoding flow from logits through optional temperature/filtering to selection | **Keep without a new figure** | A new softmax bar chart would repeat the probability column and the entropy page's distribution visual. The table shows the actual normalization calculation; the ordered flow distinguishes a distribution from a selected token. |
| Entropy | A three-distribution comparison (certain, running example, uniform) with probability bars and entropy values | **Retain; add mobile composition** | This visual directly compares distribution spread and entropy, a relationship not conveyed as clearly by the equation alone. The existing 1200 px layout needs a vertical mobile version. |
| Cross-entropy | A two-case comparison for the same target token, p(y)=0.9 vs. p(y)=0.1, with corresponding negative log losses | **Retain; add mobile composition with explicit common scales** | The figure isolates one-hot target loss and makes the nonlinear penalty visible. The mobile version uses one common scale for the two target probabilities and another common scale for the two losses, avoiding a misleading comparison of bars across different metrics. |
| Generation | A responsive prefill/decode timeline with causal mask, first next-token distribution, incremental decode, EOS/length/application stopping and optional KV cache | **Retain** | The figure already has EN/FR desktop/mobile compositions and supports the central prefill-versus-decode distinction. No extra figure is justified. |
| In-context learning | A Mermaid flowchart separating prompt/RAG context at inference with fixed parameters from fine-tuning data and optimizer-driven parameter updates | **Retain** | The diagram addresses the main misconception (contextual adaptation vs. weight update) and the surrounding prose/table supply the definitions. Another static image would be redundant. |
| LLM overview | A six-stage horizontal generation diagram plus an EN/FR responsive diagram of the three uses of the predictive distribution | **Add mobile composition to the six-stage diagram; retain the three-uses figure** | The six-stage diagram is 1600 px wide and would become unreadable when scaled to a phone. The three-uses figure already has a vertical mobile composition. The stage for positional information also needed architecture-dependent wording. |
| Q/K/V | Responsive overview of X → Q/K/V → scores/weights → V aggregation, plus responsive S/A/O matrix comparison | **Retain** | The two diagrams answer different questions: computational path and matrix shapes/roles. Both already have mobile variants and their captions distinguish scores from normalized attention weights. No third diagram is needed. |
| Training loop | Responsive training-update flow with held-out validation branch, plus a responsive optional optimizer comparison | **Retain** | The first visual distinguishes forward/loss/backprop/update from validation without gradients; the second is appropriately kept in the optimizer deepening section. Both already have mobile variants. |

## Changes made

### LLM overview

- Added EN/FR mobile variants for the six-stage autoregressive computation diagram.
- Replaced the bare Markdown image with a responsive `picture` and a page-level alt text/caption.
- Changed the third stage from a generic “embeddings + position” statement to “initial representations”; the caption/diagram now state that positional handling depends on the architecture.
- The mobile feedback loop returns to stage 3 (initial representations) after the selected token is appended, not to the Transformer block directly.
- The example distribution matches the desktop diagram in each language.

### Logits

- Added EN/FR mobile variants for the existing common-shift invariance figure.
- Replaced the bare Markdown image with a responsive `picture` and a page-level alt text/caption.
- The mobile version shows both vectors explicitly: (2, 1) and (102, 101), each with a gap of one, followed by the same softmax distribution (73.1% / 26.9% in EN; 73,1% / 26,9% in FR).

### Cross-entropy

- Added EN/FR mobile variants for the existing one-hot target probability comparison.
- The mobile version uses a shared 0–1 scale for the target-probability bars and a separate shared 0–2.303 nats scale for the loss bars. It preserves the same target in both cases.
- The page-level caption states that the two metrics use different scales and that the loss rises sharply as target probability falls.
- The surrounding lesson's caveat remains essential: this is a one-token one-hot illustration, not the full vocabulary distribution, valid-position average or complete training objective.

### Entropy

- Added EN/FR mobile variants for the existing three-distribution comparison.
- Replaced the bare Markdown image with a responsive `picture` and a page-level alt text/caption.
- The mobile composition stacks the concentrated, running-example and uniform distributions, with their respective entropy values 0, 1.089 and 1.386 nats (localized decimal notation in FR).

### No new visual for probabilities, generation or ICL

- The probabilities page retains the numeric table and the ordered flow. The entropy page already visualizes the resulting distribution and its spread; duplicating it on the probabilities page would not add a distinct learning step.
- The generation timeline remains unchanged because it already has mobile variants and includes the prefill/decode distinction.
- The ICL Mermaid diagram remains the primary visual for separating context supplied at inference from parameter updates during training.

## New assets

- `llm-generation-process-en-mobile.svg`
- `llm-generation-process-fr-mobile.svg`
- `cross-entropy-target-probability-mobile.svg`
- `cross-entropy-target-probability-fr-mobile.svg`
- `logits-common-shift-en-mobile.svg`
- `logits-common-shift-fr-mobile.svg`
- `entropy-distributions-en-mobile.svg`
- `entropy-distributions-fr-mobile.svg`

All four SVGs were authored for this contribution and include SVG `title` and `desc` elements. They contain no embedded raster, script, foreignObject or external href. These source checks do not establish XML conformance, rendered accessibility, owner provenance confirmation or a licence. Owner provenance and asset-level licensing remain pending under #156/#163.

## Source-level validation completed

- EN/FR logits and entropy pages use matching mobile variants through responsive `picture` elements.
- Each updated figure has one page-level alt text and a caption.
- The French mobile labels use decimal commas and localized descriptions.
- The LLM overview diagram now has EN/FR mobile variants; the feedback loop returns to initial representations and the displayed distribution matches the desktop reference.
- Cross-entropy mobile bars use consistent scales within each metric (probability vs. loss) and correct proportional widths for 0.9/0.1 and 0.105/2.303.
- Q/K/V and training-loop diagrams were inspected at source level; their EN/FR mobile variants already exist, so no duplicate assets were added.
- The probability-page no-new-figure decision is explicit and grounded in its table/flow plus the entropy comparison.
- Existing generation responsive figures and ICL Mermaid flow are retained.

## Not yet validated

1. Run the normal Quarto build and resolve any source, HTML or asset-path failures.
2. Inspect the LLM overview mobile diagram at a narrow viewport; confirm the six cards, feedback loop and illustrative distribution remain legible.
2. Inspect the logits, entropy and cross-entropy figures at desktop and narrow mobile widths; check labels, bars, wrapping, vertical length and caption placement.
3. Inspect the Mermaid ICL diagram on mobile and confirm the two subgraphs remain readable without horizontal overflow.
4. Verify the accessibility tree: page-level alt text, SVG title/description and captions should not be announced redundantly.
5. Confirm owner provenance for the four new SVGs and record the separate asset-level licence decision.
6. Revisit the probability page after rendered inspection only if learners cannot follow the table-to-distribution transition; do not add a duplicate bar chart pre-emptively.

## Remaining route-wide work

This pilot covers the prediction and inference stage, but does not close #1729. Remaining work includes the full rendered audit of all prior visual pilots, the detailed page-by-page review of ICL and the training loop, and the cross-route consistency check for axes, notation, token examples, colour semantics, captions, alt text and responsive behavior.
