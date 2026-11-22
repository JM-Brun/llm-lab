# Learner pilot for the visual recall cards

The trial compares two ways to present the same three recall prompts. Does a schematic help learners apply a mechanism to a new example five to seven days later? The [revision-aid pilot issue](https://github.com/JM-Brun/llm-lab/issues/1109) tracks this work.

| Mechanism | French card source | English card source |
|---|---|---|
| Token identity and position | [Information positionnelle](../site/fr/revision-positional-encoding.qmd) | [Positional information](../site/en/revision-positional-encoding.qmd) |
| Q, K and V | [Requêtes, clés et valeurs](../site/fr/revision-queries-keys-values.qmd) | [Queries, keys, and values](../site/en/revision-queries-keys-values.qmd) |
| KV cache | [Inférence et génération](../site/fr/revision-inference-generation.qmd) | [Inference and generation](../site/en/revision-inference-generation.qmd) |

## Run the trial

1. Recruit learners who have completed the three relevant lessons. Record their preferred language and whether they have implemented attention or incremental decoding before. When possible, pair learners with the same language and a comparable level of prior experience. Randomly assign one learner in each pair to each format. Use a format each learner can use comfortably and report any assignment constrained by accessibility needs separately.
2. On day 0, give each learner the same three card questions in the same order. In the visual condition, show the schematic. In the text condition, replace the schematic with the equivalent text below. Set and record the common time budget for each session before starting. Ask for an answer before revealing the same correction from the corresponding card. Record any difficulty reading or navigating the prompt separately from difficulty answering it.
3. Five to seven days later, hand out only the three delayed prompts in the learner's language. Ask learners to work from memory and explain their reasoning. Use the same time limit in both conditions. After submission, ask whether they revisited the material and record the actual delay. Score without the format assignment visible where possible.
4. Use a participant code to match sessions. Record the format, language, relevant prior experience, delay in days, reported review in the interval, each item score, and any incomplete items. Start with the delayed total out of six among learners with all three answers. For randomized pairs with two complete scores, compute the visual score minus the text score. Summarize the totals, those paired differences, and the completion counts. Report missing items and losses to follow-up separately from wrong answers.

Before the first session, freeze the exact prompts, corrections, scoring rubric, and time budgets; record deviations rather than changing one condition during the trial.

A small trial can flag confusing diagrams or recurring reasoning errors, but it cannot establish a stable learning effect on its own. Treat an apparent score advantage as a hypothesis for a larger trial. An exploratory comparison can also show whether differences coincide with prior experience, unequal review, or missed follow-up.

## Day 0 text equivalents

Use each description in place of the schematic, with the question and correction from the card.

| Card | Français | English |
|---|---|---|
| Position | Pour `chat` à la position 0, additionnez le plongement (case A) et le vecteur de position (case B). Pour `chat` à la position 3, les cases correspondantes sont C et D. | For `chat` at position 0, add the embedding (slot A) and the position vector (slot B). For `chat` at position 3, the corresponding slots are C and D. |
| Q, K, V | Combinez A pour la position courante avec B pour les positions permises pour obtenir les scores, puis les poids. Combinez ces poids avec C pour les positions permises pour obtenir la somme pondérée. | Combine A for the current position with B for the allowed positions to obtain the scores and then the weights. Combine those weights with C for the allowed positions to obtain the weighted sum. |
| Cache KV | Complétez les deux listes. La première contient les vecteurs relus pour le préfixe A B C. La deuxième contient les vecteurs calculés pour la nouvelle entrée D. | Fill in both lists. The first contains the vectors read for the prefix A B C. The second contains the vectors computed for the new input D. |

## Delayed prompts

### Français

1. **Remplacer un token à position fixe.** Comparez les séquences d’IDs `11 8 23` et `11 5 23`. L’indexation commence à 0 et le modèle utilise un encodage positionnel absolu additif. À la position 1, le modèle ajoute le vecteur `(0, 3)`. Les plongements des IDs 8 et 5 valent respectivement `(1, 2)` et `(2, 1)`. Calculez les deux entrées à la position 1. Expliquez quel terme de la somme change et pourquoi.
2. **Changer la requête.** Dans une tête à une dimension, une requête peut consulter les deux clés `1` et `−1`, associées aux valeurs `2` et `7`. Les poids sont la softmax des produits requête-clé. La requête passe de `1` à `−1`. Quelle valeur reçoit le poids le plus élevé avant et après ce changement ? La somme pondérée augmente-t-elle ou diminue-t-elle ? Justifiez sans calculer la softmax.
3. **Réutiliser les anciens poids d’attention.** Dans une tête d’auto-attention causale dense, `W X Y` est déjà traité. Au pas suivant, `Z` entre dans le modèle. Une collègue propose de conserver uniquement les poids d’attention calculés à la position `Y`. Peut-elle s’en servir pour calculer exactement la sortie à `Z`, avec ce seul état et sans recalculer le préfixe ? Justifiez en précisant les clés et les valeurs utilisées à ce pas.

### English

1. **Replace a token at a fixed position.** Compare the ID sequences `11 8 23` and `11 5 23`. Indexing starts at 0 and the model uses additive absolute positional encoding. At position 1, the model adds the vector `(0, 3)`. The embeddings for IDs 8 and 5 are `(1, 2)` and `(2, 1)`, respectively. Compute both inputs at position 1. Explain which term in the sum changes and why.
2. **Change the query.** In a one-dimensional head, a query can attend to both keys `1` and `−1`, paired with values `2` and `7`. The weights are the softmax of the query–key products. The query changes from `1` to `−1`. Which value gets the larger weight before and after this change? Does the weighted sum increase or decrease? Explain without evaluating the softmax.
3. **Reuse old attention weights.** In a dense causal self-attention head, `W X Y` has already been processed. At the next step, `Z` enters the model. A colleague proposes keeping only the attention weights computed at position `Y`. Can she compute the exact output at `Z` with this state alone and without recomputing the prefix? Explain which keys and values are used at this step.

## Scoring key

Award one point per satisfied criterion. Accept an equivalent explanation in either language.

| Item | First point | Second point |
|---|---|---|
| Position | The fixed position keeps the same positional term. The changed ID selects a different row in the embedding table. | The two input vectors are `(1, 5)` and `(2, 4)`, in that order. |
| Q, K, V | The scores change from `(1, −1)` to `(−1, 1)`, so the larger weight switches from the value `2` to the value `7`. | The sum increases because the larger of the two values now receives more weight, while the weights still sum to one. |
| Cache KV | The weights from `Y` depend on the query at `Y`. Computing the new weights calls for comparing the query at `Z` to the keys at `W X Y Z`. The old weights alone are insufficient. | The new output combines the values at `W X Y Z` with the new weights. The prefix keys and values are reused, while the key and value for `Z` are computed at this step. |
