# Practice and experiment page quick start

Use this pattern when the reader must do more than answer a short in-page comprehension check: solve a sequence of problems, practise transfer, investigate a claim, or reproduce an observation. These are related but distinct jobs. Do not force an exercise set and an empirical protocol into the same outline.

The [flexible page-template system](page-template-system.md) defines shared composition principles. For code execution, benchmarking, and reproducibility details, also consult the [implementation-page patterns](implementation-page-patterns.md) and the repository's experiment protocol.

## For an exercise collection

Clarify only what the learner needs:

- What capability or concept is being practised?
- Which prerequisites are genuinely necessary?
- What response is expected: explanation, derivation, calculation, code, diagnosis, or critique?
- Are hints useful, and can they reveal reasoning progressively?
- What does a complete solution explain, including assumptions and common mistakes?
- Does the collection build from interpretation to calculation, diagnosis, and transfer where appropriate?

Keep solutions hidden by default. A short self-check embedded in a lesson should remain short; it is not a reason to create a separate practice page.

## For an experiment or investigation

Clarify the scientific question and the evidence needed:

- State the hypothesis or question, operational definitions, variables, metric, and baseline.
- Describe the procedure sufficiently for another person to reproduce the relevant result.
- Record data and code provenance, controls, configuration, seeds, environment, and uncertainty where they matter.
- Interpret what the result supports, weakens, or leaves untested.
- Report failed runs and limitations; do not infer causality from an uncontrolled comparison.

## Possible composition

~~~markdown
## Objective and prerequisites

## Task / hypothesis

## Procedure and evidence

## Solution / interpretation
~~~

This is only a compact example. Omit, combine, or rename sections according to whether the page is primarily practice or investigation.

## Keep evidence claims bounded

A worked solution demonstrates a line of reasoning; it does not establish that a learner has retained or transferred the concept. A reproducible experiment supports only the claims justified by its design, controls, and measurements. Keep those evidence levels separate.
