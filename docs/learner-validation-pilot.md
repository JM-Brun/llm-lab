# Learner-validation pilot: text to Q/K/V attention

**Status:** protocol only; no independent participant has been observed and no learning outcome is claimed. This is a small qualitative way to discover usability or conceptual problems, not a controlled study of learning effectiveness.

## Setup (about 15–20 minutes)

Invite a volunteer who knows basic Python but has not studied these lessons. Let them choose French or English. Ask them to think aloud, use the published site without coaching, and avoid exposing personal or proprietary text. Record language, browser, viewport, page, question, navigation obstacles, answer and elapsed time only with their consent. Notes should not include identifying details by default.

## Tasks

1. Ask them to start at the home page and find the path from text to attention. Note where they go and whether they can recover from a wrong turn.
2. Before they read the relevant explanation, ask: “If the same token ID occurs twice, must its initial embedding lookup be identical? Must its final contextual representation also be identical?” (FR: « Si un même ID de token apparaît deux fois, la recherche initiale dans la table d'embeddings doit-elle renvoyer le même vecteur ? La représentation contextualisée finale doit-elle aussi être identique ? ») Record the answer and confidence without correcting it.
3. Ask them to use the text-data, embedding-space, Q/K/V and scaled-attention pages, including any code example they choose. Observe whether “run locally” and the prerequisites are clear.
4. **Q/K/V role and counterfactual probe:** ask, “If V changes while Q, K and the mask stay fixed, which quantities must remain unchanged? What may happen to the output?” (FR: « Si V change alors que Q, K et le masque restent fixes, quelles quantités doivent rester inchangées ? Que peut-il arriver à la sortie ? ») Ask for an explanation, not only a label. Do not show the answer before the participant has committed to a response.
5. **Transfer probe:** ask, “Two sequences share the same first three token IDs but differ at position four. In a causal decoder with identical parameters, can the logits at position two change because of position four? What assumption matters?” (FR: « Deux séquences ont les trois premiers ID de tokens identiques, mais diffèrent à la quatrième position. Dans un décodeur causal aux paramètres identiques, le token futur à la position quatre peut-il modifier les logits à la position deux ? Quelle hypothèse est déterminante ? ») Ask for reasoning, not only yes/no.
6. Ask what they would change on the route, and whether any diagram, mathematical notation, disclosure or navigation control was unclear.

If time permits, use the optional geometry probe: “Let q=(1,0), k₁=(0.1,0), and k₂=(10,10). Which key has the larger dot product with q? Which has the larger cosine similarity?” (FR: « Soient q=(1,0), k₁=(0,1) et k₂=(10,10). Quelle clé donne le plus grand produit scalaire avec q ? Laquelle donne la plus grande similarité cosinus ? ») This is a diagnostic for the distinction between dot product and cosine, not a required introductory learning objective.

## Facilitator key

- **Token/embedding:** the same ID selects the same row of the *same* token-embedding table. Position embeddings and later contextual computations can differ; identical initial lookup does not imply identical final contextual states.
- **Q/K/V:** with Q, K and the mask fixed, the scores and attention weights remain unchanged if only V changes. The output is a weighted sum of V and may change; it need not change if the weighted changes cancel.
- **Causal transfer:** with a correctly implemented causal decoder and otherwise identical settings, a future token cannot change earlier-position logits. This is a causal-mask property; it does not hold for arbitrary bidirectional attention or changed parameters.
- **Geometry (optional):** dot products are q·k₁=0.1 and q·k₂=10, so the dot product ranks k₂ higher. Cosine similarities are 1 and 1/√2, so cosine ranks k₁ higher. The example demonstrates norm dependence; it does not imply that attention uses cosine similarity.

## Lightweight scoring rubric

Score each required conceptual probe independently; do not combine scores into a claim of learning effectiveness.

| Dimension | 0 — Incorrect / absent | 1 — Partial | 2 — Correct with reasoning |
|---|---|---|---|
| Token ID vs representation | Treats ID as vector/semantic coordinate or says identical ID guarantees identical contextual state | Identifies lookup row but misses positional/contextual effects | Distinguishes discrete ID, initial lookup and contextualized state |
| Q/K/V roles | Confuses roles or says V determines attention weights | Identifies some roles but confuses scores, weights or output | States Q/K determine scores/weights and V supplies aggregated vectors |
| V-only counterfactual | Says Q/K scores or weights must change | Says weights stay fixed but output must always change | Says weights stay fixed; output may change but can remain equal through cancellation |
| Causal transfer | Allows future token to affect earlier logits without qualification | Gives correct answer but no assumptions | Explains causal mask and identical-parameter/settings assumption |

For the optional geometry probe, record the two rankings separately. Do not count it as a prerequisite for understanding the core Q/K/V lesson.

## Record and follow-up

For each observation, separate what was seen from interpretation. Capture page/viewport and a reproducible description, then link confirmed site defects to existing issues before creating new ones. Record the participant's language, browser, viewport, task answers and confidence only with consent; omit identifying details by default.

A single participant can reveal confusing wording, navigation friction or a plausible misconception. It cannot establish general learning, causal learning gains or population-level effectiveness. Do not treat one volunteer's success as evidence of general learning, or a failed answer as proof that a particular page caused it.

The related exercise and browser-review work is tracked in [#220](https://github.com/JM-Brun/llm-lab/issues/220), [#310](https://github.com/JM-Brun/llm-lab/issues/310), [#320](https://github.com/JM-Brun/llm-lab/issues/320), and the pilot execution in [#447](https://github.com/JM-Brun/llm-lab/issues/447).
