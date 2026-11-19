# Interactive explanatory lesson pattern

**Status:** adopted editorial/UX pattern; apply selectively and validate in rendered pages.  
**Reference case:** [“Multiplier deux nombres — de Karatsuba à l'IA”](https://djamchid.fr/blog/posts/2026-11-18-multiplication-karatsuba.html), inspected 2026-11-19.

## Purpose

Turn a difficult technical idea into a guided investigation: the reader meets a concrete question, builds a mental model, sees the mechanism, manipulates a meaningful representation, and leaves able to explain what the result does—and does not—show.

This is a composition pattern, not a mandatory page template, new page archetype, curriculum stage, or requirement to add an interactive widget to every lesson. It complements the canonical [page-template guide](page-template-guide.md), [visual design system](design-system.md), and existing Understand / Build / Deepen / Practice destinations.

## What the reference page does well

The Karatsuba article combines six moves:

1. **A motivating question and familiar baseline.** It starts with school multiplication, then exposes the inefficiency worth investigating.
2. **A worked transformation.** A small numerical example makes the algebra inspectable before generalization.
3. **A central interactive experiment.** Inputs, presets, a clear action, and exact integer arithmetic let readers test the claim themselves.
4. **A process visualization.** The recursion tree makes repeated decomposition visible, while explaining when the display is truncated.
5. **A theory/practice comparison.** Complexity, real implementation thresholds, overhead and non-benchmark caveats are kept distinct.
6. **A historical/research horizon.** A timeline connects the local trick to later advances, while the ending distinguishes a claimed result from independent validation.

The transferable quality is the alternation of explanation, evidence, visual representation and learner action—not the specific styling or the number of sections.

## The reusable learning rhythm

Use the following sequence when it fits the learner question. Merge or omit steps when they add no value.

### 1. Orient — why should I care?

- Open with one concrete question, tension, prediction or misconception.
- State what the learner should be able to explain, calculate, inspect or decide.
- Give the minimum context needed to enter the problem.
- Preview the answer without disclosing every intermediate step.

### 2. Establish a baseline

- Start with a small, inspectable example or the simplest correct mechanism.
- Name the baseline's assumptions and limitations.
- Make the problem observable before introducing a more complex solution.
- Use consistent values, symbols and shapes in later sections.

### 3. Reveal the mechanism step by step

- Explain one transformation at a time.
- Pair equations with symbol definitions, dimensions and a plain-language interpretation.
- Show intermediate values or tensor shapes where they carry explanatory weight.
- Keep the essential derivation in the main reading flow; optional algebra may be disclosed separately.
- Explicitly distinguish analogy, formal mechanism and implementation choice.

### 4. Let the learner manipulate the idea

Add an interactive explorer only if changing an input changes a meaningful state and helps answer the page's central question better than prose or a static figure.

A useful explorer has:
- a clear learner question and a short instruction;
- bounded, labelled inputs with units, shapes or constraints;
- meaningful presets or a reproducible default example;
- an explicit action/result relationship (or a clearly explained live update);
- visible intermediate state, not only a final answer;
- exactness/approximation and implementation status stated;
- reset/recovery, keyboard operation, visible focus and accessible names;
- a static or textual explanation that preserves the essential learning if scripting is unavailable.

Do not add interaction merely to increase engagement. Avoid controls whose effects are unclear, hidden state, unexplained random outputs, fake live model behavior, or widgets that cannot be independently tested.

### 5. Make structure visible

Choose a representation that matches the mechanism:
- sequence for ordered transformations;
- tree for recursion or branching;
- matrix/heatmap for pairwise relations such as attention scores;
- layered diagram for model components and tensor flow;
- distribution plot for logits/probabilities and sampling;
- timeline for historical development;
- comparison table when alternatives share explicit dimensions.

Label axes, units, tensor dimensions, direction and legend. Explain what the visualization omits or simplifies. Provide a textual equivalent; colour and motion must never be the only carriers of meaning. Do not use a graph where a list is clearer.

### 6. Reconcile theory with reality

Where relevant, distinguish:
- asymptotic complexity from measured latency or throughput;
- mathematical operation counts from actual implementation costs;
- toy/synthetic examples from model outputs or empirical evidence;
- reference implementations from optimized kernels;
- expected behavior from observed test results;
- published claims from independently validated findings.

State what a graph measures, what it excludes, and what conclusion it supports. Never present an illustrative curve as a benchmark. Put caveats beside the claim they qualify.

### 7. Connect outward and close the loop

- Link to the canonical concept explanation at the point of need.
- Use a short timeline or research context only when it clarifies why the mechanism matters.
- Cite primary sources and exact evidence for substantive claims.
- End with a compact synthesis: what changed in the reader's mental model, the key limitation, and a meaningful next question.
- Add a self-check that tests explanation, prediction, calculation or transfer—not recall of isolated wording.

## LLM Lab application opportunities

These are candidate interaction patterns, not commitments to build all of them. Prefer the smallest implementation that teaches the intended mechanism, and reuse shared bilingual components where appropriate.

| Learning question | Possible learner action | Useful visible state | Guardrail |
|---|---|---|---|
| How does tokenization split text? | Change text or tokenizer/example | Tokens, IDs, offsets and reconstruction | Distinguish illustrative segmentation from a specific tokenizer's actual output |
| How does attention combine information? | Select a query position or vary a small score example | Scores, mask, softmax weights and weighted value combination | Keep shapes and causal constraints explicit; avoid implying a live trained model |
| How do logits become probabilities? | Change a small logit vector or temperature | Logits, normalized distribution and selected token | State exact formula and avoid fabricated model probabilities |
| How does autoregressive generation proceed? | Select a token and continue the prefix | Current prefix and next-token distribution | Preserve the same example values and disclose illustrative branches |
| What does a Transformer block change? | Inspect one stage or tensor | Input/output shapes and residual/attention/MLP stages | Do not overload the first explanation with every implementation detail |
| What does training optimize? | Change a tiny prediction/target example | Per-token loss, aggregate loss and gradient intuition | Clearly separate toy arithmetic from actual parameter training |
| How do experiments support a claim? | Change one controlled parameter | Baseline, configuration, metric and result | Preserve seeds, provenance, units and limitations; never call a demo a benchmark |

## Visual and interaction direction

- Reuse the existing green identity, typography, spacing, callout semantics and Quarto components. Do not introduce a parallel palette or a one-off component system.
- Give the lesson a strong first-screen hierarchy: title/question, one-sentence promise, and concise orientation. Avoid a decorative hero that pushes the actual question below the fold.
- Use section numbers or compact progress cues only when they clarify the local argument; they are not curriculum stage numbers.
- Let figures and interactive blocks breathe, but keep prose at the established readable measure. Avoid a wall of cards or repeated coloured callouts.
- Make controls visually distinct from explanatory output. Keep the current value and its effect close together.
- Respect reduced motion, narrow screens, keyboard use, contrast and bilingual label wrapping.
- Keep French and English behavior, claims, assumptions, presets and caveats equivalent.

## Page-level acceptance checklist

A reviewer should be able to answer yes to the applicable questions:

- [ ] The opening gives a specific question and a reason to care.
- [ ] A concrete baseline/example appears before unnecessary abstraction.
- [ ] Each major transformation is explained, not merely shown.
- [ ] Equations define their symbols and conventions; tensor examples expose relevant shapes.
- [ ] Every interactive control changes a meaningful, visible state.
- [ ] The interactive result is reproducible and its exactness/approximation is stated.
- [ ] Visuals have labels, legends, textual explanation and honest simplification notes.
- [ ] Theory, implementation, illustrative examples and measured evidence are not conflated.
- [ ] Caveats are adjacent to the claims they qualify.
- [ ] Sources support the relevant claims; uncertainty and provenance remain visible.
- [ ] The ending synthesizes the insight and offers a meaningful next question.
- [ ] FR/EN parity, responsive layout, keyboard operation and accessibility are checked where relevant.

This checklist is a review aid, not a requirement to force every page into the same structure. Record non-applicable items rather than adding filler.

## Validation boundary

A source-level review can assess the authored explanation and interaction contract. A successful Quarto render establishes that the site builds, not that the interaction is correct or that learners understand it. For changed interactive pages, use the existing rendered-site browser harness and inspect both language versions at desktop and narrow widths; test keyboard behavior and the actual state transition. Learner comprehension requires separate learner evidence and must not be inferred from visual polish, test coverage or page completion.
