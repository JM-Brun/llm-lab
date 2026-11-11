# Learner feedback: main Understand path (2026-11-11)

**Status:** evidence-backed learner feedback and implementation crosswalk; not a new curriculum architecture or a claim of validated learning outcomes.

**Source:** the French learner review of [Panorama : qu'est-ce qu'un LLM ?](https://jm-brun.github.io/llm-lab/fr/llm-overview.html), recorded in [issue #971](https://github.com/JM-Brun/llm-lab/issues/971). The review is from a beginner-oriented reading perspective. Its observations are not a formal bilingual, responsive, accessibility, or controlled learner study.

## Executive summary

The main Understand path already has a strong scientific foundation: it connects the LLM lifecycle to tokens, representations, Transformer computation, prediction, generation, scoring, and learning. Its strongest learner-facing assets should be preserved: the Asterix/Otis example, the small explicitly synthetic probability table, the one-minute takeaway, the LLM/Transformer/GPT distinction, the separation between architecture/training/use, and the warnings against equating plausible text with truth or prompt success with evaluation.

The main opportunity is not to simplify or shorten the science. It is to make the existing route easier to enter, follow, rehearse, and connect to observable behavior. The recommendations below are mapped to existing project ownership. **Do not create a parallel roadmap, page inventory, curriculum registry, exercise sequence, or Build path.**

## Learner observations and recommended responses

### 1. Make the intended entry route unmistakable

**Observation:** a first-time reader entering through the panorama may not immediately recognize the guided Understand route or know which links are the recommended next step versus optional detours.

**Response:**
- Make the existing Understand route discoverable from the panorama and the learning-map entry points.
- Explain the purpose of the route and the distinction between its main conceptual sequence and optional Deepen/Practice resources.
- Keep the distinction between Theory/Understand and the independent Build path explicit.
- Do not add a new route or duplicate the existing guided-route data.

**Existing owners:** [#130](https://github.com/JM-Brun/llm-lab/issues/130) (site-wide learning architecture and coordination), [#337](https://github.com/JM-Brun/llm-lab/issues/337) (rendered curriculum/navigation reconciliation), [#368](https://github.com/JM-Brun/llm-lab/issues/368) (page-level navigation and lesson anatomy), and [#584](https://github.com/JM-Brun/llm-lab/issues/584) (computational spine and overview integration).

**Acceptance evidence:** FR and EN entry points identify the same intended route; a first-time reader can distinguish the next conceptual step from optional detail and from Build; route links and breadcrumbs work in desktop and mobile rendered checks.

### 2. Explain the two roles of the generation lesson

**Observation:** generation is introduced early as an observable black-box behavior and revisited later to explain the internal autoregressive mechanism. The repetition is sound but may look accidental.

**Response:**
- Preserve the single canonical generation lesson and its existing route memberships.
- Label the early encounter as a preview/observation and the later encounter as the mechanistic explanation.
- State what new understanding the later pass adds; avoid duplicating the lesson or creating two competing canonical pages.

**Existing owners:** [#584](https://github.com/JM-Brun/llm-lab/issues/584) (one canonical page with preview and detailed inference memberships), [#368](https://github.com/JM-Brun/llm-lab/issues/368) (page purpose and contextual navigation), and [#130](https://github.com/JM-Brun/llm-lab/issues/130) (curriculum coordination).

**Acceptance evidence:** the route and page explain why generation is encountered twice; the two links resolve to the same canonical lesson; the early preview does not require knowledge introduced only later.

### 3. Strengthen the running example without turning it into decoration

**Observation:** the Asterix/Otis example and synthetic probability table help make abstract computations tangible. Learners would benefit from seeing the same example recur at carefully chosen conceptual transitions.

**Response:**
- Reuse the established prompt/continuation and probability-table conventions where they genuinely illuminate a transformation.
- Map where the example is useful, optional, or intentionally absent across the Understand stages.
- Keep tokenization-dependent IDs, vectors, shapes, probabilities, and outputs explicitly synthetic or derived from a named tokenizer/model; never invent stable values.
- Do not turn every page into a story or repeat the example where it adds no explanatory value.
- Keep Build's Otis integration separately scoped to implementation contracts and observable checkpoints.

**Existing owners:** [#971](https://github.com/JM-Brun/llm-lab/issues/971) (panorama learner observations), [#924](https://github.com/JM-Brun/llm-lab/issues/924) (Otis example in Build only; deferred and selective), [#368](https://github.com/JM-Brun/llm-lab/issues/368) (page archetypes and repetition), and [#130](https://github.com/JM-Brun/llm-lab/issues/130) (coordination).

**Acceptance evidence:** a lightweight stage-to-example map exists in the owning issue/PR; every reuse has a pedagogical reason; FR/EN examples and any computed values agree; no duplicate conceptual explanation is introduced.

### 4. Make lesson outcomes, prerequisites, and closure actionable

**Observation:** the reader does not always know what they should be able to explain after a lesson, which prerequisites are essential, or which details can safely be deferred.

**Response:**
- Apply the existing archetype-aware editorial contract, not a rigid checklist to every page.
- For substantive lessons, state observable learning outcomes and only the prerequisites that materially affect comprehension.
- Distinguish essential concepts from optional mathematical/implementation detail.
- Close with a short retrieval/self-check and a purposeful next step where these add value.
- Add a reading-time estimate only when it is credible and useful; do not make it mandatory boilerplate.
- Retain the existing one-minute takeaway where it already works; do not duplicate it with another generic recap.

**Existing owners:** [#368](https://github.com/JM-Brun/llm-lab/issues/368) (shared anatomy by archetype), [#280](https://github.com/JM-Brun/llm-lab/issues/280) (incremental page convergence and existing inventory), [#282](https://github.com/JM-Brun/llm-lab/issues/282) (bounded lesson-template pilot), and [#971](https://github.com/JM-Brun/llm-lab/issues/971) (specific panorama wording and glossary-link observations).

**Acceptance evidence:** changes are made in bounded FR/EN page pairs; outcomes are observable rather than vague; optional material is visibly optional without hiding qualifications needed for the main claim; no empty callouts or generic boilerplate are added.

### 5. Connect intuition, math, examples, code, and tests

**Observation:** definitions and equations can arrive before the learner has a stable intuition for the problem they solve. Learners need to know why a mechanism exists and what can be inspected to check their understanding.

**Response:**
- Prefer the sequence: problem/question → intuition → visual or concrete example → formalism → hand-checkable calculation → implementation/test or experiment → limitations.
- Use this sequence when it improves a page; do not force every element into every archetype.
- Explain Q/K/V and attention in terms of the information-routing problem before deriving score and softmax equations.
- Distinguish conceptual illustrations, synthetic toy calculations, actual model outputs, executable tests, and empirical evidence.
- Reuse canonical concept pages and the existing computational spine rather than creating a second explanation.

**Existing owners:** [#368](https://github.com/JM-Brun/llm-lab/issues/368) (intuition before notation), [#584](https://github.com/JM-Brun/llm-lab/issues/584) (persistent computational spine), [#80](https://github.com/JM-Brun/llm-lab/issues/80) and [#81](https://github.com/JM-Brun/llm-lab/issues/81) (attention and causal-mask contracts; check their current status before acting), and [#483](https://github.com/JM-Brun/llm-lab/issues/483) (Q/K/V rendered/media follow-up).

**Acceptance evidence:** worked examples can be checked by hand or by a clearly scoped executable check; assumptions and tensor dimensions are explicit; figures identify whether they are conceptual, synthetic, or measured; tests are not presented as proof of scientific correctness.

### 6. Integrate formative practice instead of creating a parallel exercise catalogue

**Observation:** the site has exercises and practice resources, but the learner may experience them as parallel destinations rather than a natural part of the learning sequence.

**Response:**
- Link an exercise at the point where it rehearses a concept and explain what it checks.
- Reuse the existing Practice destination and exercise IDs/anchors.
- Use retrieval, worked-example completion, prediction, misconception diagnosis, and transfer only where the prerequisite and timing gates allow.
- Feedback should explain why plausible wrong answers fail, not only reveal the correct answer.
- Do not infer durable mastery from a quiz score or an automated check.

**Existing owners:** [#220](https://github.com/JM-Brun/llm-lab/issues/220) (bilingual formative text-to-representation sequence), [#329](https://github.com/JM-Brun/llm-lab/issues/329) (rendered exercise review after integration), [#337](https://github.com/JM-Brun/llm-lab/issues/337) (Practice as a cross-cutting destination), and [#130](https://github.com/JM-Brun/llm-lab/issues/130) (overall architecture).

**Acceptance evidence:** each linked activity has a stable FR/EN identity, an explicit learning outcome and prerequisites, progressive hints, a worked solution, misconception-focused feedback, and a rendered check; the route does not create a new exercise system.

### 7. Add small, purposeful experiments where they provide observable learning

**Observation:** short manipulations could make tokenization, embeddings, attention, decoding, and training more concrete than prose alone.

**Response (candidate experiments, not authorization to build all of them):**
- Compare tokenization of French/English text, punctuation, numbers, and rare words.
- Inspect synthetic embedding vectors and distances, while explicitly warning that token IDs are not metric coordinates.
- Change an attention input or causal mask and inspect the resulting toy computation.
- Compare greedy decoding and sampling, including temperature, while keeping probabilities and selected tokens visible.
- Inspect loss/gradient changes in a tiny model only where the implementation is real, tested, and accurately described.

Prioritize reuse of existing notebooks, widgets, experiments, and Practice infrastructure. Do not add Pyodide/JupyterLite or another execution platform without a bounded benchmark, pedagogical justification, and maintenance/performance decision. Do not build a visual solely because it looks engaging.

**Existing owners:** [#756](https://github.com/JM-Brun/llm-lab/issues/756) (pedagogical value audit of comparable projects), [#220](https://github.com/JM-Brun/llm-lab/issues/220) (formative exercises), [#268](https://github.com/JM-Brun/llm-lab/issues/268) (browser execution exploration; respect its benchmark gate), [#584](https://github.com/JM-Brun/llm-lab/issues/584) (shared computational spine), and the existing Practice/experiment owners identified by #130.

**Acceptance evidence:** each experiment states its question, inputs, assumptions, expected observable result, limitations, and whether values are synthetic or measured; no unverified model behavior is implied.

### 8. Clarify the path from base model to assistant

**Observation:** a beginner may understand next-token prediction but still not understand how a pretrained base model becomes an instruction-following assistant or how the assistant application differs from the underlying model.

**Response:**
- Reuse the panorama's existing distinction between model, assistant application, and product.
- Explain the stages at a high level: pretraining → base model → supervised instruction fine-tuning → preference/post-training methods where covered → serving/orchestration (prompt format, tools, retrieval, safety/evaluation).
- Distinguish model training/adaptation from inference-time prompting, retrieval, and application/tool orchestration.
- Keep claims architecture- and method-qualified; do not imply every LLM follows one universal pipeline or that RAG changes model parameters.
- Link to canonical fine-tuning/post-training and evaluation resources rather than adding a duplicate overview.

**Existing owners:** [#130](https://github.com/JM-Brun/llm-lab/issues/130) (site-wide architecture), [#108](https://github.com/JM-Brun/llm-lab/issues/108) (bilingual LLM panorama; verify its current status before action), [#101](https://github.com/JM-Brun/llm-lab/issues/101) (instruction fine-tuning coverage audit), [#95](https://github.com/JM-Brun/llm-lab/issues/95) (what LLMs are/system context), and [#584](https://github.com/JM-Brun/llm-lab/issues/584) (computational spine and crosswalk).

**Acceptance evidence:** the panorama explains the distinction without duplicating deep-dive material; FR/EN scope and caveats match; the route points to canonical resources; assistant-level capabilities are not attributed to the base model alone.

## Prioritization

This is a sequencing recommendation, not a change to GitHub labels or project priority policy.

| Order | Outcome | Existing owner(s) | Why |
|---|---|---|---|
| 1 | Close entry-point, route-context, and generation-preview clarity gaps | #130, #337, #584, #368 | Reduce first-session disorientation without changing content architecture |
| 2 | Apply outcome/prerequisite/closure conventions to core Understand lessons | #368, #280, #282 | Make lessons easier to enter and complete; reuse current audit inventory |
| 3 | Connect existing formative exercises to the route | #220, #329, #337 | Turn reading into retrieval and feedback |
| 4 | Selectively extend the running example in Understand | #971, #368; coordinate with #924 only for Build | Improve continuity without story-driven duplication |
| 5 | Add or improve small experiments only after inventorying existing ones | #756, #220, #268, #584 | Prefer demonstrated learning value over new infrastructure |
| 6 | Improve the base-model-to-assistant bridge | #130, #108, #101, #95 | Complete the learner's system-level mental model |

## Non-goals and safeguards

- No wholesale rewrite, simplification-by-deletion, or mandatory single linear course.
- No new curriculum registry, route generator, page inventory, or parallel Build/Practice structure.
- No second canonical generation lesson.
- No requirement to repeat the running example on every page.
- No universal template or mandatory reading-time metadata.
- No new interactive runtime/platform without a bounded value and maintenance case.
- No claims of learner mastery from page presence, CI, browser checks, quiz completion, or illustrative diagrams.
- No merging of Theory/Understand and Build: they remain independent paths with different learning objectives and ordering constraints.
- Preserve bilingual parity, existing sources/assets, technical caveats, and the project's evidence boundaries.

## Validation model

Report these as separate forms of evidence:

1. **Source/content review:** scientific accuracy, assumptions, examples, page ownership, and preservation of information.
2. **Automated checks:** Python tests, route/page-map validation, local links, and Quarto render.
3. **Rendered review:** FR/EN desktop/mobile inspection, navigation, keyboard/focus, responsive layout, and relevant accessibility checks.
4. **Learner evidence:** a small, explicitly scoped pilot with representative learners and observable tasks; do not claim general effectiveness from one reader's feedback.

The current review in #971 is one learner-perspective signal, not a substitute for the above validation.

## Ownership and maintenance

- [#130](https://github.com/JM-Brun/llm-lab/issues/130) remains the single coordination point for site-wide learning architecture.
- [#971](https://github.com/JM-Brun/llm-lab/issues/971) remains the record of this specific panorama learner review and its bounded local observations.
- [#368](https://github.com/JM-Brun/llm-lab/issues/368), [#280](https://github.com/JM-Brun/llm-lab/issues/280), [#337](https://github.com/JM-Brun/llm-lab/issues/337), [#584](https://github.com/JM-Brun/llm-lab/issues/584), [#220](https://github.com/JM-Brun/llm-lab/issues/220), [#924](https://github.com/JM-Brun/llm-lab/issues/924), and [#78](https://github.com/JM-Brun/llm-lab/issues/78) retain their existing bounded deliverables.
- Before implementation, refresh the status and acceptance criteria of each linked issue. A search result or historical issue note is not proof that work remains open.
- Add follow-up issues only for a genuinely ownerless deliverable after this crosswalk and the existing issue bodies have been reconciled.
