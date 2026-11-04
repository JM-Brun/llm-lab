# Learner-validation pilot: text to attention

**Status:** protocol only; no independent participant has been observed and no learning outcome is claimed. This is a small qualitative way to discover usability or conceptual problems, not a controlled study of learning effectiveness.

## Setup (about 15–20 minutes)

Invite a volunteer who knows basic Python but has not studied these lessons. Let them choose French or English. Ask them to think aloud, use the published site without coaching, and avoid exposing personal or proprietary text. Record language, browser, viewport, page, question, navigation obstacles, answer and elapsed time only with their consent. Notes should not include identifying details by default.

1. Ask them to start at the home page and find the path from text to attention. Note where they go and whether they can recover from a wrong turn.
2. Before they read the relevant explanation, ask: “If the same token ID occurs twice, must its initial embedding lookup be identical? Must its final contextual representation also be identical?” Record the answer and confidence without correcting it.
3. Ask them to use the text-data, embedding-space and attention pages, including any code example they choose. Observe whether “run locally” and the prerequisites are clear.
4. Ask a transfer question with new inputs: “Two sequences share the same first three token IDs but differ at position four. In a causal decoder with identical parameters, can the logits at position two change because of position four? What assumption matters?” Ask for reasoning, not only yes/no.
5. Ask what they would change on the route, and whether any diagram, mathematical notation, or navigation control was unclear.

## Facilitator key

- The same ID selects the same row of the *same* token-embedding table. Position embeddings and later contextual computations can differ; identical initial lookup does not imply identical final contextual states.
- With a correctly implemented causal decoder and otherwise identical settings, a future token cannot change earlier-position logits. This is a causal-mask property; it does not hold for arbitrary bidirectional attention or changed parameters. Tests can support the implemented cases without proving every possible implementation correct.

## Record and follow-up

For each observation, separate what was seen from interpretation. Capture page/viewport and a reproducible description, then link confirmed site defects to existing issues before creating new ones. Do not treat one volunteer's success as evidence of general learning, or a failed answer as proof that a particular page caused it. The related exercise and browser-review work is tracked in [#220](https://github.com/JM-Brun/llm-lab/issues/220), [#310](https://github.com/JM-Brun/llm-lab/issues/310), and [#320](https://github.com/JM-Brun/llm-lab/issues/320).
