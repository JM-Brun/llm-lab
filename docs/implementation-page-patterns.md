# Implementation-page patterns

**Purpose:** help contributors choose a useful structure for code-facing learning material. These patterns are soft targets, not mandatory sections. Select the pattern from the reader's task, combine patterns when needed, and omit anything that does not help the reader inspect, run, verify, or adapt the implementation.

This guide complements the [flexible page-template system](page-template-system.md), the [page patterns](page-patterns.md), the [contributor principles](contributor-guiding-principles.md), and the repository's [experiment protocol](experiment-protocol.md). It does not replace package architecture, API documentation, test conventions, or the experiment protocol.

## First classify the implementation's teaching job

| Pattern | Reader's main question | Typical artifact |
|---|---|---|
| Minimal implementation / code walkthrough | How does this mechanism translate into executable operations? | Small, readable reference implementation |
| Numerical verification | How do we know this implementation computes the intended quantity? | Unit tests, invariants, finite-difference checks, reference comparisons |
| Guided build | How can I construct the component incrementally? | Runnable notebook or staged tutorial linked to package code |
| Experiment / benchmark | What happens under a controlled change, and how strong is the evidence? | Script, configuration, results, plots, report |
| Systems / performance implementation | What resource or systems trade-off does this design create? | Profiling harness, optimized implementation, benchmark |
| Integration / usage guide | How do I use this component correctly in a larger workflow? | API example, configuration, end-to-end example |
| Debugging / failure analysis | Why does this implementation fail, and how can I diagnose it? | Reproducer, failing test, diagnostic trace |

A single page may combine a walkthrough and verification, or a guided build and experiment. If the reader's tasks are substantially different, split them into linked pages rather than forcing one long tutorial to serve every purpose.

## Shared expectations for code-facing pages

Include only the items relevant to the artifact, but make the following information easy to locate:

- **Purpose and boundary:** what is implemented, what is deliberately excluded, and which conceptual page explains the underlying mechanism.
- **Status:** distinguish planned, illustrative, executable, tested, benchmarked, and production-ready. These are not interchangeable claims.
- **Execution contract:** language/runtime, dependencies, installation or environment setup, command to run, expected duration or resource requirements when material.
- **Inputs and outputs:** types, shapes, axes, dtypes, units, conventions, valid ranges, mutation behavior, and error behavior where relevant.
- **Design choices:** explain the key representation and algorithmic choices; distinguish pedagogical simplification from a required property.
- **Verification:** show how correctness is checked and what the tests do not establish.
- **Reproducibility:** pin or report relevant versions, seeds, data provenance, configuration, hardware, and commands when results depend on them.
- **Limitations:** numerical stability, complexity, unsupported cases, performance caveats, and known failure modes.
- **Navigation:** link to the concept, implementation source, tests, and experiment/results page where they exist.

Do not paste large source files into a page when a maintained module is the canonical implementation. Use short excerpts to explain non-obvious decisions and link to the source at a stable path. Keep examples runnable and synchronized with the implementation.

## Pattern: minimal implementation or code walkthrough

**Question:** What are the essential operations, and how do they correspond to the concept?

A useful sequence is:

1. State the exact task and the smallest useful input/output contract.
2. Show the data representation, including shapes and conventions.
3. Implement the central operation in a small number of inspectable steps.
4. Explain non-obvious lines and connect them to the mathematics or system diagram.
5. Trace one small input through the implementation.
6. Identify edge cases and meaningful simplifications.
7. Link to tests and the maintained implementation.

Prefer code that exposes the mechanism over code that hides it behind abstractions. Avoid line-by-line narration of obvious syntax. Do not imply that a short teaching implementation is robust, efficient, or production-ready unless it has been evaluated for those properties.

## Pattern: numerical verification and testing

**Question:** Which properties should hold, and what evidence checks them?

Choose tests from the mathematical and software contract, for example:

- output shape, dtype, device, and value range;
- hand-computed examples and limiting cases;
- invariants, conservation properties, normalization, or symmetry;
- equivalence to a trusted reference implementation within a stated tolerance;
- gradient checks using finite differences where appropriate;
- behavior at boundaries, degenerate inputs, and invalid arguments;
- deterministic behavior under fixed seeds, where determinism is expected.

Explain why each test is informative. State tolerances and numerical precision assumptions. A passing test suite is bounded evidence: it does not prove correctness for all inputs, model quality, or production suitability. Keep tests in `tests/`; pages should explain selected tests rather than duplicate the test suite.

## Pattern: guided build

**Question:** Can the reader construct the mechanism and understand each intermediate result?

Use a sequence of checkpoints, not a monolithic code dump:

- establish the minimal environment and starting point;
- add one conceptual operation at a time;
- inspect intermediate tensors, shapes, values, or outputs;
- run a small verification after each meaningful stage;
- expose at least one likely error or misconception;
- finish with a complete runnable path and a route to the maintained package implementation.

A notebook is appropriate when interaction and intermediate inspection are central. Core reusable logic should remain importable from `src/`, with notebooks acting as teaching interfaces rather than competing implementations. Ensure the French and English versions point to equivalent code and checkpoints.

## Pattern: experiment or benchmark

**Question:** What hypothesis is being tested, against which baseline, and under what conditions?

Use the repository's [experiment protocol](experiment-protocol.md) as the authoritative contract. A page or report will typically identify:

- question, hypothesis, and expected direction of change;
- baseline and comparison conditions;
- dataset/source, provenance, preprocessing, split, and deduplication;
- controlled variables and changed variables;
- configuration, seed, software versions, hardware, and compute budget;
- metrics and why they measure the target property;
- repeated runs or uncertainty estimates when variability matters;
- results, negative findings, and deviations from the plan;
- threats to validity and limits on generalisation.

Do not infer causality from an uncontrolled comparison. Do not report a single best run as representative without justification. Separate measured results from interpretation and recommendations. Store configurations, scripts, and machine-readable results with the experiment; keep the page's synthesis concise and evidence-linked.

## Pattern: systems or performance implementation

**Question:** Which bottleneck is addressed, and what trade-off does the implementation make?

Define the workload and baseline before presenting performance. Report relevant dimensions such as throughput, latency, peak memory, numerical error, energy, or cost. Include warm-up, synchronization, batch size, sequence length, device, software stack, and measurement method when they affect the result.

Compare like with like. Explain whether a result comes from an algorithmic change, lower precision, caching, kernel fusion, hardware specialization, or measurement setup. Preserve a readable reference path where possible. Never generalize a benchmark beyond its tested workload and environment.

## Pattern: integration or usage guide

**Question:** How should a reader call this component in a larger workflow?

Show the smallest complete usage example, required configuration, expected inputs/outputs, error handling, and links to the API and underlying concept. Make version assumptions explicit. Explain lifecycle, state, device or dtype expectations, and compatibility constraints when relevant.

Do not turn a usage guide into a second conceptual explanation or duplicate API documentation. Explain only the details needed to use the component correctly.

## Pattern: debugging and failure analysis

**Question:** What observation signals a failure, what causes are plausible, and how can they be discriminated?

Start with a minimal reproducer and the observed versus expected behavior. Trace the data or computation at the relevant boundary. Present diagnostic checks in an order that rules out likely causes efficiently. Distinguish root cause from symptom and provide a regression test where appropriate.

Avoid presenting one incident as a universal failure mode. Record environment details if they affect reproduction.

## Choosing what belongs in the page

Keep the page focused on the learner's task. Put canonical implementation in package modules, regression tests in `tests/`, experiment configuration and runners in `experiments/`, and concise evidence-backed interpretation in `reports/` or the relevant site page. A page may link these artifacts rather than reproduce them.

Before adding a code section, ask: **does this help the reader understand, execute, verify, compare, or diagnose the implementation?** If not, remove it or move it to the appropriate artifact.

## Implementation contribution review

This is a diagnostic aid, not a pass/fail checklist:

- [ ] The implementation has a clear purpose, scope, and honest status.
- [ ] The source of truth is unambiguous; duplicated implementations are avoided.
- [ ] Inputs, outputs, shapes, axes, dtypes, units, and conventions are documented where relevant.
- [ ] The code is runnable with stated dependencies and commands.
- [ ] Tests cover meaningful properties and edge cases, not only the happy path.
- [ ] Numerical tolerances and reference comparisons are justified.
- [ ] Performance claims have a baseline and reproducible measurement conditions.
- [ ] Data, configuration, seeds, versions, and hardware are recorded when relevant.
- [ ] Simplifications, unsupported cases, and limitations are explicit.
- [ ] The conceptual page, code, tests, and results are linked where they exist.
- [ ] Public examples do not depend on private files, credentials, or inaccessible resources.
- [ ] The French and English explanations remain substantively equivalent.

Mark irrelevant items not applicable. Do not add sections or artifacts merely to satisfy the list.
