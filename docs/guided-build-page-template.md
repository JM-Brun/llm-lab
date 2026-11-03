# Reusable guided-build page template

Use this archetype when the learner must **construct, inspect, or run a working artifact**. The page should connect conceptual understanding to reproducible implementation without pretending that an incomplete milestone is already available.

## Suggested structure

1. **Goal and expected artifact** — What will be built, inspected, or verified?
2. **Prerequisites and environment** — Required concepts, dependencies, hardware, and setup.
3. **Architecture / plan** — Show the components and their data flow before code.
4. **Build steps** — Small ordered milestones, each with an observable result.
5. **Verification** — Tests, invariants, expected shapes/outputs, and failure diagnosis.
6. **Limitations and status** — What works, what is simplified, and what remains unfinished.
7. **Further study** — Link to conceptual explanations, source files, tests, and next milestones.
8. **Self-check** — Questions about design choices and failure modes, collapsed by default.

## Compact authoring skeleton

```markdown
::: {.chapter-lead}
State what the learner will build and what the finished artifact demonstrates.
:::

::: {.callout-note .learning-outcomes collapse="true" title="Learning outcomes"}
By the end, you should be able to:
- ...
:::

## Goal and prerequisites

## Architecture and data flow

## Build milestones

### 1. ...

**Expected result:** ...

**Verify:** ...

## Tests and invariants

## Limitations and project status

::: {.callout-note collapse="true" title="Implementation detail"}
Optional implementation detail or troubleshooting note.
:::

## Further study

- Concept:
- Source:
- Tests:

::: {.callout-note collapse="true" title="Check your understanding"}
...
:::
```

## Editorial rules

- Separate what the learner can run today from planned or illustrative code.
- State tensor shapes, input/output contracts, random seeds, and numerical assumptions when relevant.
- Every claimed behavior should have a verification path: test, assertion, expected output, or explicit reasoning.
- Avoid large code dumps without explaining the purpose and invariants of each milestone.
