# LLM Advent Calendar — three-day content pilot

**Status:** editorial pilot draft; not yet learner-tested  
**Purpose:** test the daily learning contract before writing the remaining 21 entries  
**Languages:** French and English  
**Canonical days:** 03 (tokenization), 09 (Q/K/V), 21 (cross-entropy)

This document contains short calendar-sized explanations, not replacement lessons. The linked LLM Lab pages remain authoritative for full explanations, figures, mathematical details, and extended exercises. The examples below are deliberately bounded to what those pages and their exercise hubs support.

## Pilot design principles

- Each entry answers one question and has one principal learning outcome.
- The short explanation should be understandable without first reading the linked lesson.
- One worked example makes the idea concrete; one active check tests a different but nearby case.
- The answer is available after the learner commits to a response; the calendar must not require an account or a custom interactive widget.
- The primary link goes to Understand. Practice is a separate link to the dedicated exercise hub.
- A calendar entry should take about 5–8 minutes including the active check. This is a hypothesis to test, not a measured result.

---

## Day 03 — How does text become tokens?

**Act:** Context and representations  
**Activity:** visual + conceptual check  
**Target duration:** 5–7 minutes  
**Canonical references:** `token`; computational nodes `tokenization`, `tokens`

### Français

**Question**

Comment un texte devient-il une séquence que le modèle peut traiter ?

**Réponse courte**

Un tokenizer découpe le texte en unités appelées *tokens*. Son vocabulaire associe chaque token à un identifiant entier (*token ID*). Le modèle reçoit la séquence ordonnée de ces identifiants.

Il faut distinguer trois objets :

1. le **token**, fragment de texte produit par le découpage ;
2. son **ID**, indice dans le vocabulaire de ce tokenizer ;
3. son **embedding**, vecteur lu dans la ligne correspondante de la table d'embeddings.

Un ID n'est pas une quantité de sens. L'ID 17 n'est ni « plus grand », ni plus fréquent, ni plus proche sémantiquement de l'ID 18. C'est un identifiant local à un vocabulaire. Deux tokenizers peuvent découper le même texte différemment et attribuer des IDs différents.

**Exemple guidé**

Avec un tokenizer jouet, « chat suit le chat » peut être découpé en quatre tokens :

`chat | suit | le | chat`

Le vocabulaire associe ici les IDs `[17, 42, 8, 17]`. La table d'embeddings lit donc les lignes 17, 42, 8 et 17, dans cet ordre. Les deux occurrences de `chat` sélectionnent le même vecteur initial si les paramètres de la table sont identiques. Le Transformer pourra ensuite produire des états contextualisés différents pour ces deux positions.

**À vous de vérifier**

Deux tokenizers donnent l'ID `17` à des tokens différents. Peut-on comparer directement leurs IDs ou conclure que les deux tokens ont le même embedding ?

<details>
<summary>Afficher la réponse</summary>

Non. Un ID n'a de sens que dans le vocabulaire qui le définit. Il faut connaître le tokenizer et sa version. Les embeddings appartiennent également aux poids du modèle associé ; l'ID 17 d'un autre vocabulaire ne sélectionne pas nécessairement la même ligne ni le même vecteur.

</details>

**À retenir**

Le tokenizer transforme le texte en tokens, puis en IDs. L'ID sert d'indice pour lire un embedding ; il n'encode pas directement le sens du token.

**Pour aller plus loin :** [Du texte aux tokens](../site/fr/text-data.qmd)  
**S'exercer :** [Exercices — Texte et données](../site/fr/exercises/text-data.qmd)

### English

**Question**

How does text become a sequence the model can process?

**Short answer**

A tokenizer splits text into units called *tokens*. Its vocabulary maps each token to an integer identifier (*token ID*). The model receives the ordered sequence of those IDs.

Keep three objects distinct:

1. the **token**, the text fragment produced by tokenization;
2. its **ID**, an index in that tokenizer's vocabulary;
3. its **embedding**, the vector read from the corresponding row of the embedding table.

An ID is not an amount of meaning. ID 17 is not larger in meaning, more frequent, or semantically closer to ID 18. It is an identifier local to one vocabulary. Different tokenizers can split the same text differently and assign different IDs.

**Worked example**

With a toy tokenizer, “cat follows the cat” can be split into four tokens:

`cat | follows | the | cat`

The vocabulary maps them here to IDs `[17, 42, 8, 17]`. The embedding lookup therefore reads rows 17, 42, 8, and 17, in that order. Both occurrences of `cat` select the same initial vector when the table parameters are fixed. The Transformer can later produce different contextualized states for the two positions.

**Check yourself**

Two tokenizers assign ID `17` to different tokens. Can you compare those IDs directly or conclude that the tokens have the same embedding?

<details>
<summary>Show the answer</summary>

No. An ID has meaning only within the vocabulary that defines it. You need to know the tokenizer and its version. Embeddings also belong to the associated model weights; ID 17 in another vocabulary does not necessarily select the same row or vector.

</details>

**Takeaway**

The tokenizer turns text into tokens and then IDs. An ID is used to look up an embedding; it does not directly encode the token's meaning.

**Understand more:** [From text to tokens](../site/en/text-data.qmd)  
**Practice:** [Exercises — Text and data](../site/en/exercises/text-data.qmd)

---

## Day 09 — What are the distinct roles of Q, K, and V?

**Act:** Transformer computation  
**Activity:** visual + intervention  
**Target duration:** 6–8 minutes  
**Canonical references:** `query`, `key`, `value`; computational nodes `query-projection`, `key-projection`, `value-projection`, `queries`, `keys`, `values`

### Français

**Question**

Pourquoi l'auto-attention calcule-t-elle trois projections à partir d'une même entrée ?

**Réponse courte**

Dans une tête d'auto-attention, l'état d'entrée commun est transformé en trois vecteurs :

- **Q — Query / requête :** ce que la position courante cherche à faire correspondre ;
- **K — Key / clé :** ce que chaque position présente pour être comparé à la requête ;
- **V — Value / valeur :** le contenu porté par chaque position et susceptible d'être agrégé.

Q et K déterminent les scores, puis les poids d'attention. V fournit les vecteurs combinés à l'aide de ces poids. Les trois projections sont apprises et distinctes, même si elles partent du même état d'entrée. Dans le GPT pré-LN de référence du projet, une normalisation précède ces projections ; cet ordre ne doit pas être présenté comme universel à toutes les architectures.

**Exemple guidé**

Pour la position courante, on compare sa requête Q aux clés K des positions accessibles. Les scores obtenus sont transformés en poids d'attention. Ces poids servent ensuite à calculer une somme pondérée des valeurs V.

On peut donc séparer deux chemins :

- Q et K déterminent **où et dans quelle proportion** l'attention est distribuée ;
- V détermine **quel contenu** est mélangé selon cette distribution.

Ce n'est pas une recherche consciente : Q, K et V sont des vecteurs numériques appris.

**À vous de vérifier**

On conserve Q, K et le masque, mais on modifie V. Qu'est-ce qui reste identique ? Qu'est-ce qui peut changer ?

<details>
<summary>Afficher la réponse</summary>

Les scores et les poids d'attention restent identiques, car ils dépendent de Q, K et du masque, pas de V. La sortie agrégée peut changer puisque les vecteurs combinés ont changé. Ce changement n'est toutefois pas garanti : les variations pondérées peuvent se compenser.

</details>

**À retenir**

Q et K déterminent les poids d'attention ; V fournit le contenu agrégé. Modifier V seul ne change pas les poids, mais peut changer la sortie.

**Pour aller plus loin :** [Requêtes, clés et valeurs (Q, K, V)](../site/fr/queries-keys-values.qmd)  
**S'exercer :** [Exercices — Q, K, V](../site/fr/exercises/queries-keys-values.qmd)

### English

**Question**

Why does self-attention compute three projections from one shared input?

**Short answer**

In one self-attention head, a shared input state is transformed into three vectors:

- **Q — Query:** what the current position is trying to match;
- **K — Key:** what each position presents for comparison with the query;
- **V — Value:** the content carried by each position that may be aggregated.

Q and K determine the scores and then the attention weights. V supplies the vectors combined using those weights. The three projections are learned and distinct, even though they start from the same input state. In the project's reference Pre-LN GPT, a normalization is applied before these projections; that order must not be presented as universal across architectures.

**Worked example**

For the current position, its query Q is compared with the keys K of accessible positions. The resulting scores are turned into attention weights. Those weights are then used to compute a weighted sum of the values V.

This separates two paths:

- Q and K determine **where and how much** attention is allocated;
- V determines **what content** is mixed according to that distribution.

This is not conscious searching: Q, K, and V are learned numerical vectors.

**Check yourself**

Keep Q, K, and the mask fixed, but change V. What stays the same? What may change?

<details>
<summary>Show the answer</summary>

The scores and attention weights stay the same because they depend on Q, K, and the mask, not on V. The aggregated output may change because the combined vectors have changed. A change is not guaranteed, however: weighted changes can cancel out.

</details>

**Takeaway**

Q and K determine the attention weights; V supplies the aggregated content. Changing V alone does not change the weights, but it may change the output.

**Understand more:** [Queries, keys, and values (Q, K, V)](../site/en/queries-keys-values.qmd)  
**Practice:** [Exercises — Q, K, and V](../site/en/exercises/queries-keys-values.qmd)

---

## Day 21 — How does a prediction become a cross-entropy cost?

**Act:** Scoring and learning  
**Activity:** numerical  
**Target duration:** 6–8 minutes  
**Canonical references:** `cross-entropy`, `negative-log-likelihood`; computational nodes `negative-log-probability`, `token-nll`

### Français

**Question**

Comment mesurer, à une position, la probabilité attribuée au token effectivement observé ?

**Réponse courte**

Le modèle produit une distribution conditionnelle $p_\theta(\cdot\mid x_{<t})$. Le token cible observé est $y_t$, présent dans la continuation de référence. Pour une cible *one-hot*, l'entropie croisée à cette position se réduit à la log-vraisemblance négative :

$$
\ell_t = -\ln p_\theta(y_t\mid x_{<t}).
$$

Plus le modèle attribue une faible probabilité au token observé, plus la pénalité est grande. Cette quantité est une perte locale pour un token ; elle n'est pas encore la moyenne d'une séquence ou d'un batch.

**Exemple guidé**

Supposons que la distribution prédite soit :

| Token candidat | Probabilité |
|---|---:|
| « Vous » | 0,6 |
| « Je » | 0,2 |
| « Moi » | 0,1 |
| « Oui » | 0,1 |

Si le token observé est « Vous », alors :

$$
\ell=-\ln(0{,}6)\approx 0{,}511\;\text{nat}.
$$

Si le token observé était « Moi », la distribution serait inchangée, mais la pénalité serait :

$$
\ell=-\ln(0{,}1)\approx 2{,}303\;\text{nats}.
$$

La distribution seule ne suffit donc pas à déterminer la cross-entropie : il faut aussi connaître la cible observée.

**À vous de vérifier**

La cible est « Je », auquel le modèle attribue une probabilité de 0,2. Quelle est la perte locale, en nats, à trois décimales ?

<details>
<summary>Afficher la réponse</summary>

$$
-\ln(0{,}2)\approx 1{,}609\;\text{nats}.
$$

</details>

**À retenir**

L'entropie croisée d'une cible one-hot est $\ell_t=-\ln p_\theta(y_t\mid x_{<t})$. Elle score un token observé ; la construction d'une loss de séquence ou de batch exige ensuite un alignement correct des cibles, des masques et une règle d'agrégation.

**Pour aller plus loin :** [Entropie croisée pour une prédiction de token](../site/fr/cross-entropy.qmd)  
**S'exercer :** [Exercices — Entropie croisée](../site/fr/exercises/cross-entropy.qmd)

### English

**Question**

How do we measure the probability assigned to the token actually observed at one position?

**Short answer**

The model produces a conditional distribution $p_\theta(\cdot\mid x_{<t})$. The observed target token is $y_t$, present in the reference continuation. For a *one-hot* target, cross-entropy at that position reduces to negative log-likelihood:

$$
\ell_t = -\ln p_\theta(y_t\mid x_{<t}).
$$

The lower the probability assigned to the observed token, the larger the penalty. This is a local loss for one token; it is not yet a sequence or batch average.

**Worked example**

Suppose the predicted distribution is:

| Candidate token | Probability |
|---|---:|
| “They” | 0.6 |
| “Aqueducts” | 0.2 |
| “Nothing” | 0.1 |
| “Well” | 0.1 |

If the observed token is “They”, then:

$$
\ell=-\ln(0.6)\approx 0.511\;\text{nats}.
$$

If the observed token were “Nothing”, the distribution would be unchanged, but the penalty would be:

$$
\ell=-\ln(0.1)\approx 2.303\;\text{nats}.
$$

The distribution alone therefore does not determine cross-entropy: we also need the observed target.

**Check yourself**

The target is “Aqueducts”, to which the model assigns probability 0.2. What is the local loss, in nats, to three decimal places?

<details>
<summary>Show the answer</summary>

$$
-\ln(0.2)\approx 1.609\;\text{nats}.
$$

</details>

**Takeaway**

Cross-entropy for a one-hot target is $\ell_t=-\ln p_\theta(y_t\mid x_{<t})$. It scores one observed token; building a sequence or batch loss additionally requires correct target alignment, masks, and an aggregation rule.

**Understand more:** [Cross-entropy for a token prediction](../site/en/cross-entropy.qmd)  
**Practice:** [Exercises — Cross-entropy](../site/en/exercises/cross-entropy.qmd)

---

## Pilot review protocol

The pilot is not considered validated merely because the examples are mathematically correct. A small formative review should check whether a novice can use the idea independently.

### Suggested protocol

Use 3–5 readers who have not recently studied these exact pages. This is a qualitative usability sample, not a statistically representative study.

For each day:

1. Ask the reader to complete the entry without opening the linked lesson.
2. Record elapsed time, including the active check.
3. Ask for a confidence rating (1–5) before revealing the answer.
4. Ask the reader to explain the key distinction in their own words.
5. Give one transfer question with a changed surface example.
6. Only then expose the Understand and Practice links; ask whether the next step is clear and appropriately scoped.

### Day-specific transfer checks

| Day | Transfer prompt | Evidence of understanding |
|---|---|---|
| 03 — Tokenization | Explain why ID 17 cannot be compared across two tokenizer vocabularies. | Distinguishes token, vocabulary-local ID, and embedding lookup. |
| 09 — Q/K/V | Predict the effect of changing K alone, then V alone, with the other inputs fixed. | Recognizes that Q/K affect scores and weights, while V affects the aggregated content. |
| 21 — Cross-entropy | Keep the target fixed and compare losses when its probability changes from 0.8 to 0.2. | Uses (-\ln p(y)), gets the direction right, and does not confuse local token loss with batch loss. |

### Record per reader and day

- completion time;
- confidence before feedback;
- correctness of the active check;
- transfer answer and misconception category;
- whether the Understand / Practice links were discoverable;
- whether the entry required clarification from a facilitator.

Do not optimize only for speed. A 7-minute entry that produces correct transfer is preferable to a 3-minute entry that produces superficial recognition.

### Decision rule

Revise an entry if readers repeatedly:
- confuse a token with its ID or embedding;
- say V determines attention weights;
- confuse predictive entropy with cross-entropy, or token loss with batch loss;
- cannot solve the transfer prompt after reading the explanation;
- cannot identify the appropriate canonical lesson or exercise page.

No learner test has been run yet. Results must be recorded before the pilot is described as validated.
