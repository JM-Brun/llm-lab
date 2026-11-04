# Guided-build page quick start

Use this pattern when the reader should **construct, inspect, or run a working artifact** through a sequence of meaningful steps. It complements, rather than replaces, the code-facing guidance in [implementation-page patterns](implementation-page-patterns.md).

## Questions worth answering

- What should exist or work at the end, and what does that demonstrate?
- Which concepts, tools, dependencies, hardware, and setup are genuinely required?
- What is the architecture or data flow before implementation details?
- Which small milestones produce observable intermediate results?
- How can each important behavior be verified?
- What is executable now, illustrative, simplified, or still planned?
- Which source files, tests, conceptual explanations, and experiments are canonical?

## Possible composition

~~~markdown
## Goal and prerequisites

## Architecture and data flow

## Build milestones

### A meaningful milestone

**Expected result:** ...

**Verify:** ...
~~~

Use only the milestones and verification steps that expose meaningful progress. A short walkthrough may need no separate architecture section; a complex build may need one.

## Implementation safeguards

- State the execution contract: environment, dependencies, setup, command, inputs, outputs, shapes, dtypes, units, and conventions where relevant.
- Keep canonical implementation in the appropriate source files and tests; do not create an unmaintained competing code sample.
- Make every claimed behavior inspectable through a test, invariant, expected output, or explicit reasoning.
- Distinguish pedagogical simplification from production-ready behavior.
- Record unsupported cases, numerical assumptions, and failure modes.
- Avoid large code dumps that do not explain design choices or invariants.

For experiments, performance work, integration, or debugging, choose the more specific workflow in [implementation-page patterns](implementation-page-patterns.md).
