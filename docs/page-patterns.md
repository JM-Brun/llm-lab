# Page patterns: flexible starting points

These patterns operationalise the [page-template system](page-template-system.md). They are **subject-specific explanatory patterns**, not documentation genres and not metadata types. They are **prompts, not outlines to reproduce mechanically**. Start with the dominant learner question, keep what helps, combine adjacent elements, and omit everything else.

First identify the page's broad documentation job: tutorial, how-to, reference, or explanation (or a deliberate hybrid). Then choose the scientific pattern below. For example, a mathematical concept can be taught as an explanation; an algorithm can be the subject of a tutorial; an architecture can be described in a reference page. The pattern selects useful explanatory modules, not a mandatory section sequence. The repository's page metadata contract remains authoritative for stable page classification; do not add another metadata field to encode these patterns.

## Concept, quantity, or notion

**Question:** What does this mean, why does it matter, and how should I interpret it?

Consider: intuition; precise definition and notation; domain, units or dimensions; a small example; application; assumptions and common misinterpretations; links to neighbouring concepts.

A short concept may need only an opening, a definition, an example, and one meaningful limitation.

## Algorithm

**Question:** What problem does it solve, what is its central idea, and how does it produce an output?

Consider: inputs and outputs; objective; intuition; step-by-step mechanism or pseudocode; mathematical update rule; a worked iteration; relevant guarantees and their assumptions; complexity when useful; consequential hyperparameters; variants; implementation and tests when they exist.

Do not automatically include proofs, complexity analysis, a full numerical example, or history. Include them when they help the reader understand, choose, implement, or critique the method.

## Mathematical concept or object

**Question:** What is the formal object, how can it be understood, and what follows from its properties?

Consider: geometric or intuitive entry point; formal definition; domain and conventions; useful equivalent formulations; derivation or proof; worked example; counterexample; conditions of important results; links to applications.

Keep essential formalism visible. Longer proofs may be optional. Never state a theorem without its material hypotheses.

## Physical concept, quantity, or law

**Question:** What phenomenon is described, what does the quantity mean physically, and within which regime is the model valid?

Consider: observable phenomenon; physical interpretation; units and dimensional checks; governing relation; assumptions and idealisations; boundary conditions; order-of-magnitude example; limiting cases; experimental evidence where relevant.

Distinguish a physical law, a model, an approximation, and an empirical fit. A formula alone is not a physical explanation.

## Architecture or system

**Question:** What are the parts, how do they interact, and how does information or control flow?

Consider: system boundary and purpose; overview diagram; component responsibilities and interfaces; trace through a representative input or operating cycle; design alternatives; constraints and bottlenecks; links to component-level pages.

The overview owns end-to-end relationships; component pages own detailed mechanisms.

## Technology or implementation technique

**Question:** What changes in the system, how does the technique work, and what trade-off follows?

Consider: motivating constraint; mechanism; changes to representation, computation, hardware, or workflow; relevant quality, latency, memory, compute, energy, or cost trade-offs; compatibility constraints; alternatives; measured evidence where available.

Do not present a trade-off as universal when it depends on workload, hardware, model, software, or evaluation setup. Distinguish an algorithmic property from a benchmark result.

## Method, approach, or research paradigm

**Question:** What problem does this approach formulate, what assumptions does it make, and how does it differ from alternatives?

Consider: problem framing; core principle and workflow; assumptions about data, feedback, or objectives; evaluation and baselines; strengths and limitations; competing approaches; evidence and open questions.

Separate the general idea from one specific implementation or paper.

## Overview or synthesis

**Question:** How do several mechanisms fit together, and which relationships matter most?

Consider: one organising question; a small number of structuring principles; diagram or comparison; distinctions between commonly conflated ideas; contextual links to canonical pages; compact synthesis.

An overview connects and orients; it should not reproduce the full content of its component pages. Avoid generic “further reading” sections when contextual links already provide useful routes.

## Combining patterns

A training algorithm may combine algorithm and mathematical-concept patterns; a physical technology may combine physical-concept and technology patterns. Choose one primary pattern and borrow only what resolves a real explanatory need.

If two distinct learner questions each require substantial treatment, consider separate canonical pages or a focused companion. Do not split content merely because two patterns overlap.
