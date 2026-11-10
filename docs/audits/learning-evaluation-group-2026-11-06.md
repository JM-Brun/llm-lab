# Group audit — Learning and evaluation (2026-11-06)

## 1. Scope

- **Group model:** pedagogical learning-path stage, learning-evaluation.
- **Core inventory in data/guided-route.yml:** four entries per language:
  - FR: fr/cross-entropy, fr/loss, fr/gradients, fr/evaluation-experimentale.
  - EN: en/cross-entropy, en/loss, en/gradients, en/experimental-evaluation.
- **Audit boundary:** these four pages and their stage definition. The prediction stage, training-data branch, Build path, and mathematical foundations are inspected as context, not silently added to the core.
- **Context pages:** logits, probabilities, likelihood, generation (upstream prediction); training-examples (data prerequisite); build-path (implementation/evidence boundary); mathematical-foundations (broader mathematical reference).
- **Revision:** main, 2026-11-06. Source inspection only; no rendered browser review or Quarto build performed.

## 2. Group purpose and intended reader journey

The stage aims to connect a model's probabilistic predictions to parameter learning, then to scientific evaluation. Its intended conceptual chain is:

1. define the per-target penalty (cross-entropy);
2. aggregate valid token penalties into a scalar objective (loss);
3. differentiate that objective with respect to parameters (gradients);
4. transfer the distinction between optimization objective and evidence of model quality to an applied evaluation protocol.

This is a coherent learning-and-evaluation module, but it is not a single homogeneous chain of four concept lessons. The first three pages form a conceptual sequence; the fourth is a practice exercise on a different task (scientific-passage ranking), not the next mathematical step after gradients.

## 3. Group map

| Page | Membership role | Destination / type / depth | Contribution and boundary |
|---|---|---|---|
| cross-entropy.qmd | Core | Understand / concept lesson / core | Per-target objective; one-hot target and relation to negative log-probability. Builds on likelihood and token alignment. |
| loss.qmd | Core | Understand / concept lesson / core | Batch-level scalar objective; valid-target masks, reduction and aggregation. Does not implement a complete GPT training loop. |
| gradients.qmd | Core | Understand / concept lesson / core | Local derivatives, chain rule, backpropagation and elementary SGD update. Does not define a full optimizer/training system. |
| evaluation-experimentale.qmd | Practice branch within the stage | Practice / experiment guide / applied | Transfer exercise on estimand, grouped splits, leakage, selection bias, AP, calibration, uncertainty and reproducibility. Not an LLM benchmark or implementation. |

**Context and exclusions:** vraisemblance is the immediate conceptual predecessor to cross-entropy; training-examples supplies the input/target construction needed for training; build-path exposes the implementation status; generation is inference with fixed parameters and is not part of parameter learning. The broader evaluation concept should remain cross-cutting rather than being reduced to this one ranking exercise.

## 4. Overall assessment

**Coherent with friction.**

The three concept lessons have distinct scopes, explicit previous/next metadata, and a sound progression from local objective to scalar objective to parameter sensitivity. The applied evaluation page is relevant and valuable, but its pedagogical role differs. The route registry places it in the same ordered pages list, while its page metadata points back to exercises and its hierarchy parent is the landing page. The skill must therefore distinguish stage membership from sequential adjacency and local page navigation.

## 5. Page-level observations

- **Cross-entropy:** the opening explicitly distinguishes predictive entropy from cross-entropy and points to training-examples for input/target alignment. It distinguishes token-level loss from batch reduction. The NumPy reference is carefully bounded: (B,C), integer targets, unweighted row mean; it does not claim sequence masking or full LLM training.
- **Loss:** the page correctly owns aggregation, masks, reduction and perplexity conventions. It warns that a plausible decreasing loss can still result from a token-shift error. It links to training examples and gradients.
- **Gradients:** the page separates gradient computation, optimizer dynamics and generalization. It correctly qualifies local descent and finite-difference checks.
- **Experimental evaluation:** the page explicitly labels itself a transfer exercise with no new implementation and no benchmark result. Its concrete ranker case is deliberately not a language-model pretraining benchmark. It directly teaches why AP is not calibration and why grouped splits, leakage control and selection bias matter.

## 6. Group-level findings

### LE-01 — The route list can imply a false linear transition into the evaluation exercise

- **Severity:** medium (P1 if the route UI renders the list as numbered/previous-next steps; otherwise P2).
- **Scope:** stage representation and transition.
- **Evidence:** data/guided-route.yml, stage learning-evaluation, places evaluation-experimentale after cross-entropy, loss, and gradients in the same pages array. By contrast, site/fr/evaluation-experimentale.qmd declares destination:practice, type:experiment-guide, suggested_route.previous: fr/exercises, suggested_route.next: null, and hierarchy.parents: [fr/index]; the EN counterpart carries the corresponding metadata.
- **Impact:** readers may infer that the AP/ranker protocol is the next concept in the derivative chain, or that gradients are a prerequisite for the exercise. Neither follows from the page's own stated purpose.
- **Recommendation:** preserve the stage membership, but render/describe the evaluation page as a Practice branch / transfer activity, not as the fourth sequential concept. If the route schema cannot represent a branch within a stage, make the distinction explicit in the stage objective or stage-level presentation rather than changing page content arbitrarily.
- **Preservation:** retain the complete exercise and its position in the wider evaluation curriculum; do not move it into a separate unrelated section merely to make the route look linear.

### LE-02 — The stage boundary should expose the actual training prerequisites

- **Severity:** medium (P2).
- **Scope:** group prerequisites and cross-stage transition.
- **Evidence:** docs/learning-path.md, milestone G8: learning requires G2 and G5–G6; G7 provides the prior inference demonstration. G2 (training examples) is a parallel branch, not a prerequisite for inference. site/fr/build-path.qmd, section “Générer d'abord, entraîner ensuite”, distinguishes fixed-parameter generation from loss-and-update learning and states that the current code has loss calculations only (losses.py). The loss page itself links to training-examples.
- **Impact:** a learner may reach loss/gradients without seeing that target construction and the model forward path are separate prerequisites for a working training loop.
- **Recommendation:** retain the conceptual sequence, but make the stage's entry note explicit: this is the conceptual learning mechanism; an actual training run additionally requires aligned examples (G2), a model forward pass (G5–G6), and the optimizer/training-loop work not yet evidenced.
- **Acceptance criterion:** a reader can explain why understanding gradients is not equivalent to having a functioning training pipeline.
- **Preservation:** do not move G2 into the inference path or imply that generation updates parameters.

### LE-03 — Evaluation must remain distinct from optimization and verification

- **Severity:** observation / P2.
- **Scope:** conceptual boundary.
- **Evidence:** docs/learning-path.md identifies E1 as cross-cutting and says evaluation design should be introduced before experiments. The evaluation exercise teaches estimand, leakage, selection bias, AP, calibration, uncertainty and reproducibility. G9 is a separate reference-implementation verification milestone, not a substitute for task-level evaluation.
- **Impact:** treating evaluation as a terminal chapter after training would obscure that evaluation design is needed before experimental choices, and that implementation correctness, task performance and generalization are different claims.
- **Recommendation:** preserve explicit links from learning to evaluation, but keep E1 cross-cutting in the curriculum narrative. Distinguish (a) optimization loss, (b) implementation verification, and (c) task-level evaluation.
- **Preservation:** keep the applied exercise as a concrete protocol-design transfer task; do not rename AP as an LLM metric or imply it measures token-generation quality.

## 7. Sequence and transition analysis

| From → To | Established by previous page | Assumed by next page | Bridge quality | Action |
|---|---|---|---|---|
| Likelihood → Cross-entropy (context → core) | Sequence probability and NLL from conditional token probabilities | Target distribution and one-hot token target | Strong: cross-entropy page defines the one-hot case and references likelihood | Preserve |
| Cross-entropy → Loss | Per-target penalty and logit/target alignment | Valid target mask and batch aggregation | Strong: loss page explicitly takes ownership of reduction and masking | Preserve |
| Loss → Gradients | Scalar objective and reduction conventions | Differentiability and parameterized logits | Strong: gradient page starts from loss and traces the chain rule | Preserve |
| Gradients → Experimental evaluation | Local objective sensitivity and update rule | Estimand, data-generating/sampling structure, metrics and uncertainty | Not a prerequisite transition; this is a concept → Practice transfer, not a derivative step | Label as branch / cross-cutting practice |
| Learning stage → Build/training implementation | Conceptual objective and gradient | G2 data, G5–G6 forward computation, optimizer and loop | Explicitly qualified in Build path; implementation remains incomplete | Keep evidence boundary visible |

## 8. Coverage, overlap, and level boundaries

- **Necessary reinforcement:** cross-entropy, loss and gradients all mention the same one-hot derivative or NLL relationship, but each does so for a different reason: local objective, aggregation, then differentiation. This is useful scaffolding, not redundant duplication.
- **Boundary successfully maintained:** logits/probabilities/likelihood are upstream prediction concepts; cross-entropy and loss concern the training objective; gradients concern parameter sensitivity.
- **No demonstrated contradiction** between the audited pages.
- **Important external dependency:** the actual training example alignment is owned by training-examples, not re-derived in full on every page.
- **Evaluation gap:** this exercise is one concrete ranking-protocol exercise. It does not constitute a general LLM evaluation framework, a pretraining benchmark, or a complete E1 implementation.

## 9. Navigation and project integration

- The local concept sequence is well represented by suggested_route: likelihood → cross-entropy → loss → gradients.
- The guided stage includes the evaluation exercise, but its local metadata intentionally does not place it after gradients. This is a meaningful distinction, not automatically a broken link.
- The learning-path.md narrative explicitly calls evaluation cross-cutting and separates G9 verification from E1 task evaluation.
- Build path states that the current reference implementation supports generation and loss-related calculations, but not a complete GPT-weight training/optimizer/checkpoint pipeline.
- **Bilingual parity:** counterpart files exist for all four pages. The EN/FR pages have matching destination/type/level and equivalent scope, equations, key caveats and learning intent in the inspected sections. This is a source-level semantic check, not a full line-by-line translation audit or rendered comparison.

## 10. Prioritized action plan

| Priority | Action | Affected sources | Dependency | Verification |
|---|---|---|---|---|
| P1/P2 | Make the evaluation item visibly a Practice branch, not a fourth sequential concept lesson | Guided-route presentation / generated context; possibly stage description | Confirm how the route widget renders the pages array | UI clearly distinguishes concept sequence from transfer exercise; no false gradients → AP prerequisite |
| P2 | Add a concise prerequisite/evidence boundary at the learning-stage entry | Guided-route stage context and/or landing presentation | Reuse G2/G5–G8 facts; do not duplicate status inventories | Learner can state what is needed for actual parameter training and what is currently implemented |
| P2 | Preserve E1 as cross-cutting in curriculum narrative; distinguish E1 from G9 | docs/learning-path.md and links to evaluation resources | None; current narrative already contains this distinction | No claim that code verification replaces task evaluation |
| P3 | Perform rendered EN/FR route review for this stage | Published FR/EN site | Quarto build and browser access | Verify labels, ordering, branch treatment and local navigation in both languages |

No page body was changed in this diagnostic pass. The first action depends on inspecting the rendered route UI; editing the route source before that check would risk solving a presentation problem at the wrong layer.

## 11. What is already working

- The three core concept pages have explicit, non-overlapping scopes and a clean local sequence.
- The loss page gives unusually important implementation caveats: shifted targets, valid masks, reduction denominator and comparability.
- The gradients page does not overclaim that a gradient or a finite-difference check proves training quality.
- The evaluation exercise is explicit about its transfer scope and does not claim to be an LLM benchmark.
- The learning-path document already distinguishes G8 learning from G9 verification and E1 evaluation.
- EN and FR counterparts are present and closely aligned in the inspected content.

## 12. Open questions and confidence

- **Open question:** how the rendered learning-map/route UI visually presents the stage's ordered pages list (numbered sequence, cards, or grouped links). This determines whether LE-01 is a visible defect or only a source-level ambiguity.
- **Not checked:** Quarto rendering, automated link validation, accessibility, mobile/desktop behavior, and CI.
- **Confidence:** high for page roles, conceptual sequence, source-level navigation and curriculum dependencies; medium for the user-visible impact of the route-list ordering; medium for bilingual semantic parity because the check was focused on scope, metadata, equations and key transitions rather than exhaustive sentence-level review.

## 13. Skill calibration from this application

This application adds a new reusable case beyond the first four pilots: **a mixed learning stage that combines a concept sequence with a cross-cutting applied evaluation activity**. The skill must explicitly test whether membership in a guided stage is being mistaken for sequential dependency.

New method rule:
- For any stage mixing Understand and Practice destinations, create two maps: (1) conceptual dependency/sequence and (2) stage membership/experience. A Practice item can be a required stage activity without being the next conceptual prerequisite. Inspect page-level route metadata before interpreting list order. If rendered behavior is unavailable, mark the user-visible consequence as unresolved and do not edit canonical route data speculatively.

## Revalidation log

- 2026-11-06: Compared FR/EN page headers and core explanations for cross-entropy, loss, gradients and experimental evaluation; confirmed counterpart existence and equivalent instructional intent in the inspected sections. Confirmed the local concept sequence and the evaluation page's distinct Practice metadata. Rendered route presentation remains unverified.
