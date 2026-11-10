---
name: build-path-audit
description: >
  Audit and improve the LLM Lab guided Build path from the perspective of a
  learner implementing a small GPT. Use when asked to review the build route,
  check implementation steps or dependencies, harmonize build pages, verify
  that code examples and milestones fit together, or assess whether the learner
  can reproduce and validate the model. Distinct from understand-path-audit:
  this skill evaluates implementation dependencies, executable artifacts,
  tests and reproducibility, not the conceptual reading sequence.
---

# Build Path Audit

## Mission

Act as a learner following LLM Lab's practical Build path to construct, inspect, test and progressively extend a small GPT. Determine whether each step is implementable from the preceding work, whether the code and explanations form a coherent system, and whether the learner can verify what they built.

This is not a source-code-only review. Audit the complete instructional contract: prerequisites, instructions, interfaces, artifacts, tests, expected outputs, failure modes and the transition to the next milestone.

The audit must answer:

1. Can the learner identify what to build and why this step comes now?
2. Are prerequisites and implementation dependencies explicit and correctly ordered?
3. Can the learner implement the step using the supplied explanations and artifacts?
4. Can they run it and determine whether it works?
5. Does each milestone integrate cleanly with the previous and next milestones?
6. Are the implementation, tests and scientific explanation consistent?
7. Is the path reproducible without hidden state or unstated tooling?

## Canonical project contracts

Read the current versions relevant to the requested scope:

- `docs/learning-path.md`: distinction between Theory / Understand and Build; module objectives and evidence gates.
- `site/fr/build-path.qmd` and `site/en/build-path.qmd`: reader-facing Build route.
- `data/resources.yml`: canonical first-class implementation resource registry and bilingual references.
- `docs/information-architecture.md`: ownership of pages, concepts, resources, curriculum and generated projections.
- `docs/content-section-mapping.md`: Build destination boundaries and content ownership.
- `docs/implementation-page-patterns.md`, `docs/page-template-system.md`: implementation documentation patterns and soft page-composition targets.
- `docs/design-system.md` and `docs/reader-experience-and-editorial-method.md`: reader experience, shared visual patterns and editorial economy.
- `docs/experiment-protocol.md`: requirements for controlled experiments and evidence.
- `docs/project-status.md`, `docs/roadmap.md`: actual implementation status and planned work.
- `src/llm_lab/`, `tests/`, `experiments/`, `reports/`: executable implementation, tests and experiment evidence.

Follow links from these documents to the specific milestone specifications and source files. If an expected path has moved, find its canonical owner rather than creating a duplicate.

## Non-negotiable architecture

- Build and Theory / Understand are separate pathways. Build follows implementation dependencies; it does not require completing the eight-stage Understand route first. Link to theory at the point where it helps explain a code decision.
- Do not turn the Build path into a copy of the Understand route. The same concept may appear at a different time and depth because implementation has different prerequisites.
- The current Build route is status-aware. A planned milestone, placeholder, prose walkthrough, code resource, passing test and reproducible end-to-end implementation are different evidence states.
- Do not claim a full trained LLM exists if the repository only demonstrates inference with a randomly initialized model. A random model demonstrates mechanics, not language quality.
- Distinguish inference from training operations. Corpus preparation and shifted training-example construction are training-data dependencies, not prerequisites for demonstrating inference.
- Respect the canonical computational model: context → forward pass → logits → probability distribution. Generation samples/selects and feeds a token back into context; scoring evaluates observed targets without updating parameters; training computes loss/gradients and updates parameters. These branches share a forward computation but are not one execution loop.
- Q/K/V projections occur inside each Transformer block from that block's input hidden states. Do not place them after final contextualized representations.
- Preserve existing code, tests, examples, figures, references and limitations. Never silently remove a capability or claim.
- Templates are soft targets. Harmonize interfaces, explanations and verification patterns without forcing identical page outlines.
- Do not add a new workflow, GitHub Action, registry, framework or dependency unless the task demonstrates a concrete need. Prefer existing Python, Pydantic, pytest, Quarto and project conventions.

## When to run

Choose the requested scope:

- **Whole Build path:** all currently published milestones and the handoffs between them.
- **Milestone:** one milestone plus its incoming and outgoing dependencies.
- **Implementation slice:** a group of pages, code modules, tests or resources that jointly deliver one capability.
- **Learner reproduction:** attempt the documented steps in a clean or clearly described environment.
- **Build-page harmonization:** compare page structure, code presentation, expected outputs and verification guidance across related milestones.

For a group audit, inspect the previous milestone's output and the next milestone's expected input. A milestone cannot be judged only by its own page.

## Procedure

### 1. Reconstruct the real Build route

1. Read the reader-facing Build route and the curriculum/evidence definitions.
2. Resolve each milestone to its page(s), resource ID(s), source code, tests, data/configuration and expected output.
3. Identify the dependency graph from actual imports, interfaces, tensor contracts and data artifacts—not merely the visual order of pages.
4. Build a milestone table with: objective, input artifacts, output artifacts, dependencies, code owner, tests, expected observation, status and next consumer.
5. Compare the reader-facing sequence with the actual dependency graph. Report discrepancies; do not edit generated projections to conceal them.

Check that the route makes explicit which branches are optional or parallel. In particular, training data preparation and shifted-target construction should not be presented as prerequisites for inference-only milestones unless a concrete implementation dependency requires them.

### 2. Simulate the build learner

For every milestone, attempt to answer from the material:

- What problem does this component solve?
- What should exist before I start?
- What files or functions do I create or modify?
- What are the inputs, outputs, shapes, dtypes, devices and conventions?
- What is the smallest working implementation?
- What command do I run?
- What output or invariant should I observe?
- What common failure should I diagnose?
- How does this artifact feed the next milestone?

If the page does not supply enough information, inspect the actual code and tests to establish whether the gap is in the documentation or implementation. Do not fill missing instructions with assumptions.

### 3. Audit implementation dependency and integration order

Check the route against the actual model lifecycle, as applicable:

- Environment, project setup and reproducibility.
- Text representation, tokenizer/vocabulary and token IDs.
- Input batches and context conventions.
- Token and positional embeddings.
- Attention projections, head reshaping, masks and attention aggregation.
- Transformer block composition: residual paths, normalization and MLP.
- Model forward pass and output logits.
- Loss and shifted targets for training.
- Optimizer, gradient flow, parameter updates and training loop.
- Checkpointing, inference, decoding and evaluation.

This list is a diagnostic map, not an instruction to impose a new milestone structure. Use the existing Build route and its actual implementation state. Identify missing or misordered dependencies only where evidence supports the claim.

For each handoff, verify that the previous output matches the next input in type, shape, naming, layout, device, semantics and lifecycle. Explicitly inspect:

- batch/time/feature/head axis conventions;
- vocabulary and special-token ID conventions;
- causal-mask polarity, shape and broadcast behavior;
- attention scaling and softmax dimension;
- padding/document-boundary handling where relevant;
- shifted input/target alignment and ignored positions;
- train/eval mode, dropout and gradient semantics;
- logits versus probabilities and the expected loss input;
- checkpoint/configuration compatibility.

Do not assume conventions from common frameworks; inspect the project's implementation.

### 4. Audit code teaching quality

For each code example or linked implementation:

- Is the purpose connected to the preceding concept and the next integration step?
- Is the code runnable in the documented environment, or clearly labelled pseudocode?
- Are names, types, tensor shapes, axes and numerical conventions explicit?
- Is the example minimal without hiding essential behavior?
- Does reusable logic live in `src/llm_lab/` rather than being duplicated across lesson snippets?
- Are abstractions proportionate to the teaching goal?
- Are error handling and unsupported cases explained?
- Are comments explanatory rather than narrating obvious syntax?
- Is the implementation consistent with its mathematical description?
- Are deviations from referenced upstream implementations explained and cited?

Do not replace readable teaching code with optimized kernels. Do not invent code to fill a page template.

### 5. Audit verification and evidence

For each milestone, distinguish:

- **Illustration:** a snippet or diagram showing an idea.
- **Runnable example:** executes under stated conditions.
- **Unit test:** checks a defined local property.
- **Integration test:** checks component interaction.
- **Numerical/reference check:** compares with known values, a reference implementation or finite differences where appropriate.
- **Experiment:** records a hypothesis, baseline, configuration, seed, data provenance, metrics and limitations.
- **Learner reproduction:** a separate person can follow the documented steps from a stated starting state.

Verify that tests actually test the claimed property. Look for shape and dtype checks, deterministic fixtures, numerical edge cases, gradient checks, causal leakage checks, target alignment and failure cases as appropriate.

A passing test does not prove model quality, scientific validity or learner mastery. A successful render does not prove the code works. A generated sample from random weights does not prove training succeeded.

Where training or evaluation is in scope, check data provenance, split policy, deduplication/leakage, configuration, seed, compute budget, baseline, metrics and held-out test discipline. Do not claim reproducibility when essential environment or data details are missing.

### 6. Audit page harmonization and reader ergonomics

Compare related Build pages for consistent treatment of:

- Goal and motivation at the top.
- Prerequisites and starting state.
- Inputs/outputs and interface contracts.
- Implementation steps and code placement.
- Shapes, conventions and equations.
- Commands, dependencies and environment assumptions.
- Expected output, tests and troubleshooting.
- Completion/evidence status and limitations.
- Links to theory, source code, tests and next milestone.
- Shared Quarto components, headings, callouts, figures, captions and code blocks.
- French/English substantive parity.

Classify variations as intentional, harmless or harmful. Build pages need a stronger operational structure than conceptual lessons, but they should still share the project's visual language and avoid boilerplate.

### 7. Reproduce the path where feasible

Use the repository's documented setup and smallest relevant commands. Prefer a clean environment or state the existing environment precisely. Run only proportionate checks for the changed scope, then relevant broader checks if integration risk warrants them.

Record exact commands, versions, inputs, outputs and failures. Do not silently install a new dependency or change the user's environment without authorization. If a step cannot be run because data, credentials, hardware or external services are unavailable, identify the missing condition and mark the evidence as unverified.

For numerical code, inspect expected tolerances and deterministic behavior. For training, avoid expensive or large-scale runs unless explicitly requested; use small controlled fixtures when they test the same contract.

### 8. Prioritize and repair

For each finding, record:

- Milestone, page IDs, resource IDs, code paths and test paths.
- Evidence and the exact broken contract or learner friction.
- Consequence: blocked implementation, silent wrong result, unreproducible step, confusing instruction or cosmetic inconsistency.
- Severity: **P0** incorrect/unsafe computation or impossible core route; **P1** broken milestone or integration; **P2** material verification/usability gap; **P3** polish.
- Smallest corrective action and canonical owner.
- Existing behavior, data, references and tests that must be preserved.
- Exact validation needed.

Fix canonical sources only. Keep generated route fragments and projections derived. Avoid a new action/workflow for a single concept or milestone. Prefer one coherent patch over a new abstraction layer.

### 9. Re-run the learner handoff

After changes, start from the stated entry condition and follow the changed milestone through its next consumer. Confirm that the artifacts integrate and that a learner can verify completion. Re-run relevant tests and report any remaining manual or environment-dependent step.

## Expected output

Use this structure; omit empty sections.

1. **Scope and evidence** — milestones/pages/resources/code/tests inspected; environment and commands; what was not runnable.
2. **Build dependency map** — milestone, required inputs, produced artifacts, next consumer and status.
3. **Learner walkthrough** — what the learner does, observes and verifies at each step.
4. **Findings** — prioritized, evidence-linked implementation, integration, documentation and harmonization issues.
5. **Page consistency matrix** — shared operational pattern, intentional differences and inconsistencies with learner cost.
6. **Recommended changes** — minimal coherent patch, canonical owners and preservation notes.
7. **Validation results** — exact commands and outcomes, including failures and unverified claims.
8. **Residual risks** — concrete blockers or environment-dependent evidence only.

Use evidence states such as **documented**, **implemented**, **tested**, **integrated**, **reproduced** and **planned** precisely. Do not compress them into one ambiguous "done" label.

## Completion criteria

An audit is complete when:

- The actual route and implementation dependency graph have been reconstructed.
- Each milestone's inputs, outputs and next consumer are understood.
- The code and prose contracts agree.
- Tests verify the properties claimed by the pages.
- At least one relevant handoff has been checked for the requested scope.
- Reproduction limits and evidence levels are explicit.
- Page differences are harmonized only where they harm the learner.
- Existing useful information and artifacts are preserved.
- Changes, if requested, are validated and the next milestone remains buildable.
