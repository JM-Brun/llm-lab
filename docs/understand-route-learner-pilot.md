# Independent learner pilot: complete Understand route

**Status:** protocol only. No participant result or learning outcome is claimed. This is a qualitative, formative walkthrough of the published Understand route, not a controlled study or a test of learning effectiveness.

**Owner:** [#971 — full guided-route learner review](https://github.com/JM-Brun/llm-lab/issues/971). Keep the focused text-to-attention pilot in [#447](https://github.com/JM-Brun/llm-lab/issues/447) and its 15–20 minute [existing protocol](learner-validation-pilot.md) separate.

## Purpose and scope

Check whether a learner can use the nine-stage Understand route to build and connect one coherent mental model:

`text → token IDs → representations → Transformer computation → logits → distribution`

Then distinguish the three uses of that shared prediction mechanism:

- **Inference:** select a token and extend the context; parameters stay fixed.
- **Scoring:** evaluate an observed target under the distribution; no token is selected.
- **Training:** use observed targets to compute a loss, gradients and parameter updates.

The session samples every stage. It is **not** a request to read all 20+ pages in 45 minutes, and it does not assess the separate Build route or optional Deepen catalogue exhaustively.

## Participant and conditions

- Invite one volunteer who is comfortable with general mathematics and programming but has not studied LLMs or machine learning. This matches the exploratory target profile already used in #971; it does not represent every intended reader.
- Let the participant choose French or English.
- Use the published site, a desktop browser and a quiet setting. Record the viewport and browser version.
- Ask the participant to think aloud, navigate without coaching, and answer before opening solutions. Do not explain concepts or point to a page before the first attempt.
- With consent, record only language, browser/viewport, task, elapsed time, navigation choices, answers, confidence, hesitation and requests for help. Omit names and identifying details. Keep raw notes private unless there is a specific reason and consent to publish anonymized excerpts.

**Time budget:** 40–45 minutes. If a task runs over, record the overrun rather than rushing the participant or silently dropping a stage.

## Session protocol

### 0. Introduction and baseline — 2 minutes

Say: “I am testing the learning material, not you. Please say what you are looking for, what you think a page means, and when something is unclear. I will not help unless you ask.”

Before showing the route, ask:

1. “When a language model generates a token, what do you think changes?”
2. “Do you expect the model to update its learned parameters during an ordinary generation step? Why?”

Record the initial explanation and confidence. Do not correct it yet.

### 1. Orientation — 4 minutes

Start at the site entry point.

- Find the recommended starting point for understanding how an LLM produces text.
- Explain, in your own words, the relationship between an application, a language model, a Transformer and a GPT.
- State the question the first lesson is trying to answer.

Observe whether the learner finds the Understand route, distinguishes it from Build, and understands the route's purpose without facilitator guidance.

### 2. Text and token IDs — 3 minutes

Use the first-pass example on **Text → tokens**.

- Trace a short text fragment to tokens and token IDs.
- Explain what is passed to the model after tokenization.
- If two tokenizers process the same text, what may change?

Observe whether the learner distinguishes text, token boundaries, token strings and integer IDs. Do not require knowledge of BPE internals.

### 3. Representations — 4 minutes

Use **Embeddings**, **Positional information** and the introduction to **Contextualized representations**.

- If the same token ID occurs twice, must the embedding lookup return the same initial vector?
- Must the final contextualized representations also be identical?
- What additional information can make the two occurrences differ?

Expected distinction: the same ID indexes the same row of the same embedding table; position and accessible context can make later hidden states differ.

### 4. Transformer computation — 6 minutes

Use the first-pass explanations and one existing Q/K/V or scaled-attention exercise.

- Which objects determine the attention weights?
- Which object supplies the vectors that are combined?
- If V changes while Q, K and the mask stay fixed, what must remain unchanged, and what may change?
- Why can a future token not affect an earlier position in a causal decoder?

Expected distinction: Q and K determine scores and weights; V supplies content for the weighted aggregation. Changing V alone leaves the weights fixed, although the output may or may not change. The causal mask excludes future positions under the stated decoder assumptions.

Record separately whether the learner understands the role of the mask or merely remembers the phrase “no looking ahead.”

### 5. Prediction and inference — 6 minutes

Use the existing four-token running example from **Logits**, **Probabilities** and **Generation**.

Given the illustrative distribution:

| Candidate | Probability |
|---|---:|
| A | 0.6 |
| B | 0.2 |
| C | 0.1 |
| D | 0.1 |

Ask:

1. What does the distribution describe, and what does it not establish?
2. Which token does greedy decoding select?
3. What happens to the context after selection?
4. Which part of the computation is prefill, and which part is decode?
5. Are the model parameters updated during this loop?

Expected distinction: the distribution is conditional on the current prefix; greedy decoding selects A; the selected token is appended to the context; prefill processes the supplied prompt and decode processes newly generated tokens; parameters remain fixed.

Do not require implementation details of KV caching unless the participant opens that optional material.

### 6. Context use — 4 minutes

Use **In-context learning** and **Context engineering**.

- If examples are added to the prompt, can the model's response change without updating its weights?
- What is the difference between the model exploiting examples in context and the application selecting/assembling that context?
- How does this differ from fine-tuning?

Expected distinction: ICL describes behavior conditioned on information in the input at fixed parameters; context engineering is the system-side work of selecting and organizing that input; fine-tuning updates parameters.

Observe whether the learner can distinguish stored/retrieved information from information actually transmitted to the model.

### 7. Scoring an observed target — 5 minutes

Reuse the distribution from the previous task. Suppose the model's observed continuation is B, although greedy decoding would have selected A.

- Which probability is used to score the observed token?
- What is its token-level negative log-likelihood?
- Does scoring select a token or update parameters?

Expected answer: use (p(B)=0.2), so the token NLL is (-\ln(0.2)); scoring evaluates the observed target and does not select a token or update parameters.

Ask the learner to explain why scoring B is not the same operation as generating A. Record whether the distinction survives without the facilitator's vocabulary.

### 8. Training and parameter learning — 6 minutes

Use **Loss**, **Gradients** and **Training loop**, plus the shifted-target example where useful.

- Given tokens `[a, b, c]`, what are the teacher-forced inputs and next-token targets?
- Why is the target sequence shifted by one position?
- Where do the loss and gradients enter?
- At what operation do the parameters actually change?
- Why is teacher forcing not the same as feeding the model's own generated token at every training step?

Expected distinction: inputs `[a, b]` are paired with targets `[b, c]`; the model predicts observed next tokens from preceding ground-truth tokens; loss measures prediction errors, backpropagation computes gradients, and the optimizer updates parameters. The forward pass alone does not update weights.

### 9. Reconstruction and debrief — 4 minutes

Ask the learner to reconstruct the complete story without looking at the pages:

1. From text to the next-token distribution.
2. What happens after the distribution in inference.
3. What happens when a token is observed and scored.
4. What additional operations make this a learning process.

Then ask:

- Which transition was hardest to explain?
- Which term or diagram caused the most uncertainty?
- Where did you expect to find something but could not?
- Which page or exercise would you revisit?
- What would you change about the route?

Finish by asking the learner to distinguish the main Understand route from optional Deepen material, Practice exercises and the separate Build route.

## Observation record

For each task, record the following without turning the session into a speed test:

| Field | What to record |
|---|---|
| Route stage / page | Where the learner was and what they opened |
| Task outcome | Completed, partial, not completed, or skipped |
| First response | Short, anonymized paraphrase before hints or correction |
| Reasoning | Whether the learner explained the mechanism or only named terms |
| Time | Approximate elapsed time; note interruptions |
| Friction | Hesitation, backtracking, unexpected link, unclear term or control |
| Help | Whether a hint or facilitator intervention was requested |
| Confidence | Learner's own confidence, recorded separately from correctness |

Classify each observation as one of: **conceptual confusion**, **missing prerequisite**, **unclear wording**, **poor example/diagram**, **navigation friction**, **exercise friction**, **rendering/accessibility issue**, or **environmental issue**. One observation may have more than one plausible cause; preserve that uncertainty.

## Lightweight rubric

Score each dimension independently. Do not add the scores into a pass/fail grade or a single “learning score.”

| Dimension | 0 — Incorrect / absent | 1 — Partial | 2 — Correct with reasoning |
|---|---|---|---|
| Text and representations | Confuses text, token, ID and vector | Identifies the lookup but misses position/context | Traces IDs, lookup, position and contextualized states |
| Transformer computation | Confuses Q/K/V or causal visibility | Gets some roles right but cannot explain the intervention | Explains Q/K weights, V aggregation and causal restriction |
| Prediction and inference | Treats logits, probabilities and selected token as identical | Distinguishes some stages but not the loop | Explains conditional distribution, selection, context extension and fixed parameters |
| Context use | Says prompt examples update weights | Identifies fixed weights but conflates ICL and context engineering | Distinguishes model behavior, system-side context design and fine-tuning |
| Scoring | Scores the generated choice rather than the observed target | Finds the target probability but cannot explain the operation | Scores the observed token and distinguishes scoring from generation |
| Training | Says the forward pass or loss directly updates parameters | Understands shifted targets or gradients but not the optimizer step | Explains teacher forcing, loss, gradients and parameter update |
| Route use | Cannot find the route or interpret its optional resources | Finds the route with backtracking or uncertainty | Navigates the main route and distinguishes Understand, Deepen, Practice and Build |

The rubric is diagnostic, not psychometric. A correct answer after reading a solution is not evidence of unaided understanding. A single participant cannot establish retention, generalization, causal learning gains or population-level effectiveness.

## Follow-up decision rule

Do not rewrite a page because one learner hesitates once. First identify whether the problem is in the content, prerequisite, example, navigation, interaction or environment.

- If the learner reaches the right page but cannot explain a concept, inspect the explanation and its prerequisite.
- If the learner explains a concept but cannot transfer it to the counterfactual, inspect the worked example and exercise.
- If the learner cannot find a page or practice task, inspect the route and link labels before changing lesson content.
- If the learner succeeds only after a hint, preserve the first response and the hint; do not record the result as independent success.
- Reuse existing issues and canonical pages. Do not create a new page, route stage, exercise collection or checker unless the observation demonstrates a real gap.

After the session, compare the findings with the existing third-pass notes in [#971](https://github.com/JM-Brun/llm-lab/issues/971). Report observations separately from interpretations, note the exact site revision and language tested, and state what remains untested. Repeat with additional learner profiles before making broad claims.
