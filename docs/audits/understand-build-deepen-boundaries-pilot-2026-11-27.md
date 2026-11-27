# Understand / Build / Deepen — boundary audit pilot

**Date:** 2026-11-27  
**Scope:** bilingual ICL, Logits and Gradients lessons. This is a pilot, not the requested audit of all 40 pages.

## 1. Decisions

The three pages remain in the **Understand** path:

| Lesson | Current classification | Main responsibility | Route |
|---|---|---|---|
| In-context learning | `type:concept-lesson`, `destination:understand`, `level:core` | Explain adaptation through prompt examples while parameters remain fixed | Generation → ICL → Context engineering |
| Logits | `type:concept-lesson`, `destination:understand`, `level:core` | Explain the output projection, vocabulary scores and their relation to probabilities | Causal masking → Logits → Probabilities |
| Gradients | `type:concept-lesson`, `destination:understand`, `level:core` | Derive the gradient from loss through logits to parameters and distinguish it from the optimizer update | Loss → Gradients → Training loop |

No change of destination or level is justified by this review.

## 2. Why the content belongs in Understand

- The Logits page uses a worked mathematical example to explain an output projection; it does not ask the reader to implement a model.
- The Gradients page derives (p-y), applies the chain rule and works through one isolated SGD update. These are conceptual and mathematical explanations, not a training-loop implementation.
- The ICL page explains zero-shot / one-shot / few-shot behavior and the information carried by demonstrations. Its research context supports understanding rather than implementation.

The worked examples are retained in Understand because they make the core mechanism inspectable. Moving them to Build would separate the mathematical explanation from the concept it explains.

## 3. Advanced material remains optional

The following topics are appropriate as collapsed or clearly optional extensions rather than prerequisites for the core lesson:

- ICL: induction-head mechanisms and the latent-concept Bayesian framework (the latter is added in PR #1756 as a separate collapsed note).
- Gradients: Newton's method and numerical gradient checking.
- Logits: the probability-ratio identity is retained in the core explanation because it directly explains why logit differences matter; it does not require an advanced optimization or implementation background.

No advanced material currently justifies changing the main destination to Deepen. If the full calibrated duration later exceeds the upper review threshold, revisit the optional notes before splitting the lesson.

## 4. Practice / Build separation

All three lessons link to dedicated exercise pages:

- `in-context-learning-exercises`
- `logits-exercises`
- `gradients-exercises`

The main lessons do not embed growing question banks. Their role is to explain; Practice owns questions and answer feedback. The Gradients lesson points to the Training loop for the actual optimizer and training-step implementation. No runnable implementation code needs to move from these three pages to Build in this pass.

## 5. Boundary rules for the 40-page audit

Apply the following tests consistently:

1. **Understand:** the page explains what a concept means, why it exists, how its mathematical or architectural mechanism works, and its limits. A worked numerical example is allowed.
2. **Build:** the reader implements or modifies a working component: tokenizer, model block, loss, optimizer, training loop, generation routine, cache, evaluation pipeline, or equivalent code.
3. **Deepen:** the page studies advanced theory, alternative architectures, research evidence, formal derivations beyond the core explanation, performance trade-offs or unresolved mechanisms.
4. **Practice:** questions, exercises, coding challenges and answer feedback live on dedicated exercise pages, linked from the lesson.
5. **Do not classify by vocabulary alone:** mentioning PyTorch, gradients, attention, or an equation does not make a page Build or Deepen. Classify by the reader's task and the page's learning objective.
6. **Preserve causal continuity:** split only at a genuine change of objective or abstraction level, not to satisfy a duration target.
7. **Use metadata consistently:** `destination` describes the learning destination; `level` describes depth; `type` describes the page artifact. Do not use one field as a substitute for another.

## 7. First structural inventory of the 40-page core route

The route definition in `data/guided-route.yml` identifies **40 core page instances: 20 French and 20 English**. A first structural pass fetched those pages and inspected their metadata tags, headings, fenced blocks, callouts and links to dedicated exercises.

The first finding is methodological: **a raw code-block count is not a reliable Understand/Build classifier**.

- The Cross-entropy lesson groups its NumPy and PyTorch code examples inside a collapsed implementation callout.
- The Training-loop lesson keeps its executable micro-code inside a collapsed optional callout.
- The Generation lesson contains a fenced HTML visualization, not a Python implementation.
- The ICL lesson uses fenced prompt examples and Mermaid content; these are not implementation code.

These examples do not currently justify moving the lessons out of Understand. Their implementation content is explicitly optional and separated from the main conceptual explanation. The inventory is structural only; it does not replace the page-by-page pedagogical review of all 40 pages.

## 6. Remaining work

- Run the same boundary audit over the complete set of 40 core pages.
- Check bilingual parity and page-to-page prerequisites, not just local tags.
- Identify pages that mix implementation with conceptual explanation and move only the implementation-specific material to Build.
- Identify Deepen material currently embedded in core pages; keep short optional callouts when they support the main explanation, and split only when the advanced content forms a coherent independent objective.
- Revisit the decisions after the reading-time estimator has been calibrated. Do not add or adjust durations in this pilot.
