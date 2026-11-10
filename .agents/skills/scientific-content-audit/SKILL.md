---
name: scientific-content-audit
description: Verify the scientific, mathematical, statistical, algorithmic and implementation claims in LLM Lab pages, code, experiments and diagrams using traceable primary evidence and reproducible checks.
---

# Scientific content audit

## Mission

Determine whether the project's technical claims are correct, appropriately scoped, reproducible where applicable, and consistent across explanation, equations, diagrams, code and tests.

This skill performs claim-level verification. It is not a general pedagogical review, a source-extraction workflow, or an editorial permission to rewrite pages.

## When to use

Use when reviewing:
- mathematical definitions, derivations, equations, dimensions or complexity;
- probability, statistics, evaluation metrics, optimization or numerical claims;
- ML/LLM mechanisms, algorithms, architecture, training or inference behavior;
- code walkthroughs and claims about the project's implementation;
- experimental results, benchmarks, plots, tables or reproducibility;
- scientific contradictions between pages, sources or code.

Use `page-content-audit` for the internal teaching quality of a page, `page-group-audit` for progression and group coherence, and `editorial-boundary-audit` for content ownership. A scientific audit may be invoked by those skills when a claim needs verification.

## Evidence hierarchy

Prefer evidence appropriate to the claim:
1. primary paper or original technical specification;
2. authoritative original implementation and version-pinned source;
3. official framework/API documentation for version-specific behavior;
4. reproducible derivation, calculation or experiment;
5. high-quality secondary explanation for context, not sole proof of disputed claims.

Record exact versions, commits, equations, sections, line ranges or experimental artifacts. Search snippets and unsourced summaries are discovery aids, not verification.

Do not assume the paper, implementation, framework documentation and project code describe identical versions or variants.

## Audit procedure

### 1. Decompose pages into auditable claims

Create a claim ledger. For each claim record:
- stable finding/claim ID;
- exact page path, heading and excerpt or equation;
- claim type: definition, theorem/derivation, algorithm, dimension/shape, complexity, implementation behavior, empirical result, interpretation or recommendation;
- assumptions and scope;
- source/version and evidence locator;
- verification method;
- result and confidence.

Separate compound sentences into independently testable claims. Do not use a general page-level verdict to conceal mixed correctness.

### 2. Verify mathematical and statistical reasoning

Where relevant:
- check definitions, quantifiers, domains, units and assumptions;
- derive equations independently and check algebraic transformations;
- verify dimensions and broadcasting/indexing conventions;
- inspect limiting cases, invariances, counterexamples and degenerate inputs;
- distinguish exact identities, approximations, asymptotic statements and heuristics;
- verify probability normalization, conditioning, independence assumptions and sampling procedures;
- check metric definitions, prevalence dependence, threshold dependence, calibration and uncertainty;
- distinguish population claims from finite-sample estimates and exploratory results from confirmatory evidence.

For numerical claims, state precision, tolerances and relevant stability assumptions. A plausible numeric example is not a proof.

### 3. Verify algorithmic and implementation claims

Trace the described operation to the actual implementation:
- locate canonical source files and exact version/commit;
- map prose steps to functions, tensor operations and data flow;
- check input/output shapes, dtype, device, masks, initialization, normalization, residual paths and parameter sharing where relevant;
- compare intended behavior with unit/integration tests;
- run a minimal independent check when a claim can be tested cheaply;
- identify behavior not covered by tests.

Do not infer runtime behavior from class or variable names. Tests establish only the behavior they actually assert.

### 4. Verify empirical claims and experiments

For each reported result inspect:
- dataset provenance, sampling and exclusions;
- split strategy, leakage risks and unit of independence;
- baseline, controls, ablations and hyperparameter selection;
- metrics and uncertainty estimates;
- number of runs, seeds, compute and software versions;
- statistical assumptions and multiplicity/selection effects;
- whether the reported observation supports the stated conclusion.

Use explicit evidence states: proposed, protocol specified, implemented, run completed, independently reproduced. Never present an unrun experiment as a result or an external result as a project result.

### 5. Verify figures, diagrams and examples

Check whether:
- labels, arrows, axes, dimensions and legends match the mechanism;
- a schematic omits details that materially change interpretation;
- examples are mathematically valid and representative;
- visual simplifications are labelled;
- captions describe what the figure actually establishes.

A diagram can aid intuition but does not independently prove a scientific claim.

### 6. Check cross-page and bilingual consistency

Compare the same claim across FR/EN counterparts and relevant neighboring pages. Look for changed assumptions, missing caveats, notation drift, inconsistent dimensions, stale versions and stronger wording in one language.

Distinguish genuine contradictions from context-specific variants. Record intentional differences explicitly.

### 7. Classify findings

Use:
- **confirmed error** — contradicted by derivation, authoritative source or reproducible test;
- **materially misleading** — technically defensible only under unstated assumptions or with an omitted qualification;
- **unsupported** — evidence is insufficient for the strength of the claim;
- **version-dependent** — correct only for a stated version/configuration;
- **notation/precision issue** — meaning is recoverable but representation risks misunderstanding;
- **verified** — checked against suitable evidence;
- **open question** — evidence is conflicting or incomplete.

Severity:
- blocker: central result or implementation is wrong;
- high: likely to teach a materially false mechanism;
- medium: important qualification, derivation or edge case is missing;
- low: local precision issue with limited impact;
- observation: sound but worth documenting.

Confidence is separate from severity. Use high/medium/low and explain the evidence.

## Required report

1. Scope, revision, files and evidence limits.
2. Claim ledger with source locators and verification methods.
3. Confirmed errors and materially misleading statements.
4. Version-dependent or unsupported claims.
5. Equation/dimension/algorithm/implementation checks as applicable.
6. Cross-page and FR/EN consistency.
7. Corrections recommended, with exact affected locations and preserved assumptions.
8. Tests or calculations run and observed outcomes.
9. Residual uncertainty and confidence.

## Quality gates

- Every substantive verdict has a traceable claim and evidence locator.
- Scientific correctness is not inferred from a green CI or a citation alone.
- A source is checked for version and scope compatibility.
- Mathematical steps are independently checked where feasible.
- Code claims are traced to actual implementation and test assertions.
- Empirical claims are bounded by the experimental design.
- Evidence, confidence and severity remain distinct.
- No claim of execution, rendering, reproduction or CI success is made without an observed result.

## Change control

This skill is diagnostic by default. If the user requests corrections, make the smallest coherent changes, preserve valid caveats and examples, add regression tests where a code invariant is involved, update FR/EN counterparts, and rerun relevant checks. Separate correction of a scientific claim from broader pedagogical restructuring. Never merge without explicit authorization.
