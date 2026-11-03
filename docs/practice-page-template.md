# Reusable practice and experiment page template

Use this archetype when the learner must **test understanding, investigate a claim, or reproduce an observation**. Distinguish a short self-check from a full exercise collection or an empirical protocol.

## Suggested structure

1. **Question and objective** — What is being tested or investigated?
2. **Prerequisites** — Concepts, data, tools, and expected preparation.
3. **Task or hypothesis** — State the problem, variables, and expected evidence.
4. **Procedure** — Steps that another learner can reproduce.
5. **Analysis and interpretation** — Explain what outcomes support, weaken, or fail to test the claim.
6. **Solution / expected reasoning** — Hidden by default for exercises; never reveal only a final numeric answer.
7. **Limitations and reproducibility** — Data provenance, controls, uncertainty, seeds, environment, and known confounders.
8. **Further study** — Link back to canonical concepts and onward experiments.

## Compact authoring skeleton

```markdown
::: {.chapter-lead}
State the question and what a successful investigation or solution demonstrates.
:::

## Objective and prerequisites

## Task / hypothesis

## Procedure

## Analysis and interpretation

::: {.callout-note collapse="true" title="Solution and reasoning"}
Show the complete reasoning, assumptions, and checks.
:::

## Limitations and reproducibility

## Further study

- Concepts:
- Data / code:
- Related experiment:
```

## Editorial rules

- Keep short retrieval questions in lesson pages; use this archetype for sustained practice or investigation.
- For experiments, distinguish hypothesis, operational definition, metric, baseline, controls, and conclusion.
- Do not infer causality from correlation or from an uncontrolled before/after comparison.
- Report uncertainty and failure cases, not only successful runs.
- Record data and code provenance, environment, and random seeds where relevant.
