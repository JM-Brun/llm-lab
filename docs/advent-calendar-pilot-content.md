# LLM Advent Calendar — content drafts and pilot

**Status:** editorial drafts; not yet learner-tested  
**Purpose:** develop the daily learning contract and prepare a deliberately varied three-day novice pilot  
**Languages:** French and English  
**Drafted days:** 01–09 (except 10–20), 21  
**Pilot candidates:** 03 (tokenization), 09 (Q/K/V), 21 (cross-entropy)

This document contains short calendar-sized explanations, not replacement lessons. The linked LLM Lab pages remain authoritative for full explanations, figures, mathematical details, and extended exercises. The examples below are deliberately bounded to what those pages and their exercise hubs support.

## Pilot design principles

- Each entry answers one question and has one principal learning outcome.
- The short explanation should be understandable without first reading the linked lesson.
- One worked example makes the idea concrete; one active check tests a different but nearby case.
- The answer is available after the learner commits to a response; the calendar must not require an account or a custom interactive widget.
- The primary link goes to Understand. Practice is a separate link to the dedicated exercise hub.
- A calendar entry should take about 5–8 minutes including the active check. This is a hypothesis to test, not a measured result.

---

## Day 01 — What does an LLM predict?

**Act:** Context and representations  
**Activity:** conceptual check  
**Target duration:** 6 minutes  
**Canonical references:** next-token-prediction, conditional-distribution; computational nodes raw-text-context, logits, next-token-distribution

### Français

**Question**

Que prédit exactement un modèle de langage autorégressif ?

**Réponse courte**

À partir d'un préfixe déjà fourni, le modèle calcule des logits ; la fonction softmax les transforme en une distribution de probabilité sur les tokens possibles à l'étape suivante. Cette distribution dépend du préfixe : si le contexte change, la distribution peut changer.

Le modèle ne choisit pas nécessairement un token à cette étape. La sélection intervient ensuite, selon une politique de décodage (par exemple, prendre le token le plus probable ou échantillonner). Il faut donc distinguer **prédire une distribution** et **sélectionner un token**.

**Exemple guidé**

Après le préfixe « Le chat », imaginons la distribution jouet suivante :

| Token candidat | Probabilité |
|---|---:|
| « dort » | 0,55 |
| « mange » | 0,25 |
| « court » | 0,15 |
| Autres tokens (masse agrégée) | 0,05 |

Ces nombres sont illustratifs, pas une sortie mesurée d'un modèle réel. La ligne « Autres tokens » regroupe la masse de probabilité de tous les tokens non affichés. Le modèle attribue 0,55 à « dort », mais il ne s'agit pas encore d'une certitude ni d'un choix obligatoire.

**À vous de vérifier**

La distribution attribue 0,55 à « dort ». Peut-on conclure que le modèle a déjà généré ce token, ou qu'il est certain que « dort » est la bonne continuation ?

<details>
<summary>Afficher la réponse</summary>

Non. Le modèle a attribué une probabilité conditionnelle de 0,55 à « dort » pour le préfixe considéré. Aucun token n'a encore été sélectionné par le décodage, et cette probabilité ne garantit pas que la continuation soit vraie ou correcte.

</details>

**À retenir**

À chaque étape autorégressive, le modèle calcule une distribution conditionnelle sur le prochain token. La génération ajoute ensuite une règle de sélection ; elle ne doit pas être confondue avec le calcul de la distribution.

**Pour aller plus loin :** [Panorama : qu'est-ce qu'un LLM ?](../site/fr/llm-overview.qmd)  
**S'exercer :** [Exercices — Panorama des LLM](../site/fr/exercises/llm-overview.qmd)

### English

**Question**

What exactly does an autoregressive language model predict?

**Short answer**

Given a supplied prefix, the model computes logits; softmax transforms them into a probability distribution over possible next tokens. This distribution is conditional on the prefix: changing the context can change the distribution.

The model does not necessarily select a token at this stage. Selection happens afterward, according to a decoding policy (for example, choosing the most likely token or sampling). We must therefore distinguish **predicting a distribution** from **selecting a token**.

**Worked example**

After the prefix “The cat”, imagine the following toy distribution:

| Candidate token | Probability |
|---|---:|
| “sleeps” | 0.55 |
| “eats” | 0.25 |
| “runs” | 0.15 |
| Other tokens (aggregated mass) | 0.05 |

These values are illustrative, not measured output from a real model. The “Other tokens” row aggregates the probability mass of all tokens not shown. The model assigns 0.55 to “sleeps”, but that is neither certainty nor a mandatory choice.

**Check yourself**

The distribution assigns 0.55 to “sleeps”. Can we conclude that the model has already generated this token, or that it is certain “sleeps” is the correct continuation?

<details>
<summary>Show the answer</summary>

No. The model assigned a conditional probability of 0.55 to “sleeps” for the given prefix. Decoding has not selected a token yet, and this probability does not guarantee that the continuation is true or correct.

</details>

**Takeaway**

At each autoregressive step, the model computes a conditional distribution over the next token. Generation then adds a selection rule; it should not be confused with computing the distribution.

**Understand more:** [Overview: what is an LLM?](../site/en/llm-overview.qmd)  
**Practice:** [Exercises — LLM overview](../site/en/exercises/llm-overview.qmd)

---

## Day 02 — Context: what information does the model have?

**Act:** Context and representations  
**Activity:** trace  
**Target duration:** 5 minutes  
**Canonical references:** computational nodes raw-text-context, token-context

### Français

**Question**

Quelles informations peuvent conditionner la prochaine prédiction ?

**Réponse courte**

À une étape donnée, le **contexte du modèle** est le préfixe de tokens effectivement disponible pour lui, dans sa fenêtre de contexte. Le prochain token à prédire se trouve après ce préfixe : il n'en fait pas encore partie.

Pendant une génération, le token sélectionné est ajouté au préfixe. Il devient alors une information disponible pour l'étape suivante. Le contexte est donc différent d'un texte futur que le modèle n'a pas encore reçu.

Ici, « contexte » désigne l'entrée immédiate du modèle à une étape donnée. Ce n'est pas encore le sujet plus large de la construction d'un contexte applicatif (instructions, documents récupérés, mémoire, etc.).

**Exemple guidé**

- Préfixe fourni : « Le chat »
- Le modèle calcule une distribution pour le token suivant.
- Si le décodage sélectionne « dort », le nouveau préfixe devient « Le chat dort ».
- Le modèle calcule alors une nouvelle distribution, conditionnée par ce préfixe plus long.

Le second calcul ne repart pas du même contexte : le token ajouté fait désormais partie de l'entrée.

**À vous de vérifier**

Le préfixe fourni est « Le chat dort ». Le token « dort » est-il encore le prochain token à prédire ?

<details>
<summary>Afficher la réponse</summary>

Non. « dort » appartient déjà au préfixe fourni. Le modèle calcule une distribution pour le token qui vient après « Le chat dort ».

</details>

**À retenir**

Le contexte est le préfixe disponible au moment du calcul. Un token futur n'en fait pas partie avant d'avoir été fourni ou réinjecté dans la séquence.

**Pour aller plus loin :** [Panorama : qu'est-ce qu'un LLM ?](../site/fr/llm-overview.qmd)  
**S'exercer :** [Exercices — Panorama des LLM](../site/fr/exercises/llm-overview.qmd)

### English

**Question**

Which information can condition the next prediction?

**Short answer**

At a given step, the model's **context** is the prefix of tokens actually available to it within its context window. The next token to predict comes after that prefix; it is not part of the context yet.

During generation, the selected token is appended to the prefix. It then becomes available information for the next step. The context is therefore different from future text that the model has not received.

Here, “context” means the model's immediate input at a particular step. It is not yet the broader topic of constructing an application context (instructions, retrieved documents, memory, and so on).

**Worked example**

- Supplied prefix: “The cat”
- The model computes a distribution for the next token.
- If decoding selects “sleeps”, the new prefix becomes “The cat sleeps”.
- The model then computes a new distribution conditioned on this longer prefix.

The second computation does not use the same context: the appended token is now part of the input.

**Check yourself**

The supplied prefix is “The cat sleeps”. Is “sleeps” still the next token to predict?

<details>
<summary>Show the answer</summary>

No. “sleeps” is already part of the supplied prefix. The model computes a distribution for the token that follows “The cat sleeps”.

</details>

**Takeaway**

The context is the prefix available at the time of computation. A future token is not part of it until it has been supplied or fed back into the sequence.

**Understand more:** [Overview: what is an LLM?](../site/en/llm-overview.qmd)  
**Practice:** [Exercises — LLM overview](../site/en/exercises/llm-overview.qmd)

---

## Day 03 — How does text become tokens?

**Act:** Context and representations  
**Activity:** visual + conceptual check  
**Target duration:** 5–7 minutes  
**Canonical references:** `token`; computational nodes `tokenization`, `tokens`

### Français

**Question**

Comment un tokenizer transforme-t-il un texte en unités discrètes ?

**Réponse courte**

Un tokenizer applique une règle de segmentation à une chaîne de caractères et produit une séquence ordonnée de *tokens*. Un token est une unité du vocabulaire du tokenizer : selon la méthode et le vocabulaire, il peut correspondre à un mot, une partie de mot, un caractère ou une séquence d'octets.

Il ne faut donc pas supposer qu'un token correspond toujours à un mot lisible. La segmentation dépend du tokenizer utilisé ; deux tokenizers peuvent découper différemment une même chaîne.

**Exemple guidé**

Avec un tokenizer jouet, « chat suit le chat » peut être segmenté en quatre tokens :

`chat | suit | le | chat`

Un autre tokenizer pourrait découper certains mots en sous-unités. La séquence obtenue dépend de son vocabulaire et de ses règles de segmentation.

Cette journée porte sur la segmentation elle-même. L'association de chaque token à un identifiant entier sera étudiée au jour 4 ; l'utilisation de cet identifiant pour lire un vecteur dans la table d'embeddings viendra au jour 5.

**À vous de vérifier**

Deux tokenizers segmentent la même chaîne différemment : le premier produit `["chat", "suit"]`, le second `["cha", "t", "suit"]`. Ont-ils nécessairement produit la même séquence de tokens ?

<details>
<summary>Afficher la réponse</summary>

Non. Les deux segmentations sont différentes, même si elles représentent la même chaîne de départ. Le découpage dépend du tokenizer et de son vocabulaire ; il faut connaître le tokenizer utilisé pour interpréter la séquence de tokens.

</details>

**À retenir**

La tokenisation transforme une chaîne de caractères en une séquence ordonnée d'unités discrètes. Un token n'est pas nécessairement un mot, et sa segmentation dépend du tokenizer.

**Pour aller plus loin :** [Du texte aux tokens](../site/fr/text-data.qmd)  
**S'exercer :** [Exercices — Texte et données](../site/fr/exercises/text-data.qmd)

### English

**Question**

How does a tokenizer turn text into discrete units?

**Short answer**

A tokenizer applies a segmentation rule to a character string and produces an ordered sequence of *tokens*. A token is a unit in the tokenizer's vocabulary: depending on the method and vocabulary, it may correspond to a word, part of a word, a character, or a byte sequence.

A token should therefore not be assumed to be a readable word. Segmentation depends on the tokenizer; two tokenizers may split the same string differently.

**Worked example**

With a toy tokenizer, “cat follows the cat” can be split into four tokens:

`cat | follows | the | cat`

Another tokenizer might split some words into smaller units. The resulting sequence depends on its vocabulary and segmentation rules.

This day focuses on segmentation itself. Mapping each token to an integer ID is covered on day 4; using that ID to look up a vector in the embedding table follows on day 5.

**Check yourself**

Two tokenizers segment the same string differently: the first produces `["cat", "follows"]`, while the second produces `["ca", "t", "follows"]`. Have they necessarily produced the same token sequence?

<details>
<summary>Show the answer</summary>

No. The two segmentations differ, even though they represent the same original string. The split depends on the tokenizer and its vocabulary; you need to know which tokenizer was used to interpret the token sequence.

</details>

**Takeaway**

Tokenization turns a character string into an ordered sequence of discrete units. A token is not necessarily a word, and segmentation depends on the tokenizer.

**Understand more:** [From text to tokens](../site/en/text-data.qmd)  
**Practice:** [Exercises — Text and data](../site/en/exercises/text-data.qmd)

---

## Day 04 — From token to token ID

**Act:** Context and representations  
**Activity:** trace  
**Target duration:** 5 minutes  
**Canonical references:** concept token; computational nodes token-id-encoding, token-ids

### Français

**Question**

Comment le modèle retrouve-t-il l'identifiant associé à chaque token ?

**Réponse courte**

Après la segmentation, le tokenizer associe chaque token à une entrée de son vocabulaire et à un **identifiant entier** (token ID). Le modèle consomme cette séquence d'identifiants, pas directement les chaînes de caractères.

Un identifiant est un index local au vocabulaire et à la version du tokenizer. Ce n'est ni une mesure de sens, ni un rang de fréquence, ni une quantité : deux identifiants proches numériquement ne désignent pas nécessairement des tokens proches.

**Exemple guidé**

Considérons un vocabulaire jouet :

| Token | Identifiant |
|---|---:|
| « le » | 17 |
| « chat » | 42 |
| « dort » | 8 |

Le texte « le chat dort » devient la séquence d'identifiants [17, 42, 8]. Les valeurs sont arbitraires et servent uniquement à illustrer l'indexation.

Un autre tokenizer pourrait attribuer d'autres identifiants aux mêmes chaînes, ou produire une segmentation différente. Pour interpréter une séquence d'IDs, il faut donc connaître le tokenizer et son vocabulaire.

**À vous de vérifier**

Deux tokenizers différents attribuent l'identifiant 42 à un élément de leur vocabulaire. Peut-on en déduire qu'ils désignent le même token ?

<details>
<summary>Afficher la réponse</summary>

Non. L'identifiant 42 n'a de sens qu'à l'intérieur du vocabulaire correspondant. Dans deux vocabulaires différents, le même entier peut désigner des tokens différents.

</details>

**À retenir**

Le token est une unité discrète ; le token ID est l'index entier qui la désigne dans un vocabulaire donné. L'identifiant sert ensuite à sélectionner une ligne de la matrice d'embeddings.

**Pour aller plus loin :** [Du texte aux tokens](../site/fr/text-data.qmd)  
**S'exercer :** [Exercices — Texte et données](../site/fr/exercises/text-data.qmd)

### English

**Question**

How does the model retrieve the ID associated with each token?

**Short answer**

After segmentation, the tokenizer maps each token to a vocabulary entry and an integer **token ID**. The model consumes this sequence of IDs, not the character strings directly.

An ID is local to a vocabulary and tokenizer version. It is not a measure of meaning, a frequency rank, or a quantity: numerically close IDs do not necessarily represent similar tokens.

**Worked example**

Consider a toy vocabulary:

| Token | ID |
|---|---:|
| “the” | 17 |
| “cat” | 42 |
| “sleeps” | 8 |

The text “the cat sleeps” becomes the ID sequence [17, 42, 8]. These values are arbitrary and only illustrate indexing.

Another tokenizer could assign different IDs to the same strings, or produce a different segmentation. To interpret a sequence of IDs, we must know which tokenizer and vocabulary were used.

**Check yourself**

Two different tokenizers assign ID 42 to one of their vocabulary entries. Can we infer that they refer to the same token?

<details>
<summary>Show the answer</summary>

No. ID 42 only has meaning within its corresponding vocabulary. In two different vocabularies, the same integer may refer to different tokens.

</details>

**Takeaway**

A token is a discrete unit; a token ID is the integer index that identifies it in a given vocabulary. The ID is then used to select a row from the embedding matrix.

**Understand more:** [From text to tokens](../site/en/text-data.qmd)  
**Practice:** [Exercises — Text and data](../site/en/exercises/text-data.qmd)

---

## Day 05 — An ID becomes a vector

**Act:** Context and representations  
**Activity:** numerical  
**Target duration:** 7 minutes  
**Canonical references:** concept token-embedding; computational nodes embedding-lookup, token-embeddings

### Français

**Question**

Comment un identifiant discret sélectionne-t-il une représentation numérique ?

**Réponse courte**

Le modèle possède une matrice d'embeddings E de forme V × d, où V est la taille du vocabulaire et d la dimension des vecteurs. Pour un token ID i, le lookup sélectionne la ligne E[i].

L'identifiant n'est pas transformé en vecteur par une opération arithmétique sur sa valeur. Il sert d'index pour retrouver un vecteur appris. La proximité numérique entre deux IDs ne dit donc rien sur la proximité de leurs embeddings.

**Exemple guidé**

Supposons une petite table jouet de dimension d = 3 :

| ID | Ligne de la matrice |
|---:|---|
| 0 | [0.1, 0.0, -0.2] |
| 1 | [0.3, 0.4, 0.1] |
| 2 | [0.4, -0.1, 0.7] |
| 3 | [-0.2, 0.5, 0.2] |

L'ID 2 sélectionne le vecteur [0.4, -0.1, 0.7]. Pour une séquence de trois IDs, le lookup produit une matrice de forme 3 × d ; pour un batch de séquences mises à la même longueur (par exemple par padding), la forme usuelle est B × T × d.

Ces valeurs sont fictives. Dans un modèle entraîné, les lignes de la matrice sont des paramètres appris.

**À vous de vérifier**

Si l'ID passe de 2 à 3, obtient-on nécessairement un vecteur légèrement différent, comme si l'on avait ajouté 1 à une coordonnée ?

<details>
<summary>Afficher la réponse</summary>

Non. L'ID est un index, pas une coordonnée. Passer de 2 à 3 sélectionne une autre ligne de la matrice ; les deux vecteurs peuvent être proches, éloignés ou quelconques selon les paramètres appris.

</details>

**À retenir**

Un token ID sélectionne une ligne de la matrice d'embeddings. Le vecteur est appris ; la valeur entière de l'ID n'est pas une mesure géométrique.

**Pour aller plus loin :** [Des identifiants aux vecteurs : les embeddings](../site/fr/embedding-space.qmd)  
**S'exercer :** [Exercices — Espace des embeddings](../site/fr/exercises/embedding-space.qmd)

### English

**Question**

How does a discrete ID select a numerical representation?

**Short answer**

The model has an embedding matrix E with shape V × d, where V is the vocabulary size and d is the vector dimension. For a token ID i, the lookup selects row E[i].

The ID is not turned into a vector by arithmetic on its numeric value. It is an index used to retrieve a learned vector. Numerical closeness between two IDs therefore says nothing about the distance between their embeddings.

**Worked example**

Suppose we have a small toy table with dimension d = 3:

| ID | Matrix row |
|---:|---|
| 0 | [0.1, 0.0, -0.2] |
| 1 | [0.3, 0.4, 0.1] |
| 2 | [0.4, -0.1, 0.7] |
| 3 | [-0.2, 0.5, 0.2] |

ID 2 selects the vector [0.4, -0.1, 0.7]. For a sequence of three IDs, lookup produces a matrix of shape 3 × d; for a batch padded to a common length, the usual shape is B × T × d.

These values are fictional. In a trained model, the matrix rows are learned parameters.

**Check yourself**

If the ID changes from 2 to 3, must the resulting vector be only slightly different, as if we had added 1 to one coordinate?

<details>
<summary>Show the answer</summary>

No. The ID is an index, not a coordinate. Changing from 2 to 3 selects a different matrix row; the two vectors may be close, far apart, or unrelated depending on the learned parameters.

</details>

**Takeaway**

A token ID selects a row from the embedding matrix. The vector is learned; the integer value of the ID is not a geometric measurement.

**Understand more:** [From IDs to vectors: embeddings](../site/en/embedding-space.qmd)  
**Practice:** [Exercises — Embedding space](../site/en/exercises/embedding-space.qmd)

---

## Day 06 — Why does position matter?

**Act:** Context and representations  
**Activity:** visual  
**Target duration:** 7 minutes  
**Canonical references:** concept positional-encoding; computational node positional-information

### Français

**Question**

Pourquoi les représentations doivent-elles tenir compte de l'ordre des tokens ?

**Réponse courte**

L'embedding initial représente l'identité du token. Il ne suffit pas, à lui seul, à indiquer sa position dans la séquence. Or l'ordre change le rôle des mots et donc le sens d'une phrase.

L'information positionnelle permet au Transformer de distinguer les occurrences selon leur place. Dans un schéma additif simple, on combine embedding du token et vecteur de position. D'autres méthodes, comme les positions relatives ou RoPE, injectent cette information autrement : il ne faut pas supposer qu'une seule méthode est universelle.

**Exemple guidé**

Comparez :

- « Le chien poursuit le chat. »
- « Le chat poursuit le chien. »

Les tokens sont les mêmes, mais leur ordre change qui poursuit qui. Les représentations doivent donc contenir une information sur la position, en plus de l'identité lexicale.

**À vous de vérifier**

Le même token ID apparaît à deux positions différentes. Son embedding lexical initial est-il nécessairement différent ? L'information de position utilisée par le Transformer est-elle la même ?

<details>
<summary>Afficher la réponse</summary>

L'embedding lexical sélectionné par le même ID est le même pour une matrice donnée. En revanche, l'information positionnelle dépend de la position : dans un schéma additif, un vecteur de position différent est ajouté à l'entrée ; avec RoPE, la position intervient dans la transformation des requêtes et des clés. Les calculs d'attention peuvent donc différer sans que l'embedding lexical initial change.

</details>

**À retenir**

L'identité du token et sa position sont deux informations distinctes. Le Transformer doit disposer d'un signal d'ordre, mais les méthodes qui l'encodent varient selon les architectures.

**Pour aller plus loin :** [Encodage positionnel](../site/fr/positional-encoding.qmd)  
**S'exercer :** [Exercices — Encodage positionnel](../site/fr/exercises/positional-encoding.qmd)

### English

**Question**

Why must representations account for token order?

**Short answer**

The initial embedding represents token identity. By itself, it does not indicate the token's position in the sequence. Yet word order changes grammatical roles and therefore the meaning of a sentence.

Positional information lets the Transformer distinguish occurrences by their place. In a simple additive scheme, the token embedding is combined with a position vector. Other methods, such as relative positions or RoPE, inject this information differently; no single method should be assumed universal.

**Worked example**

Compare:

- “The dog chases the cat.”
- “The cat chases the dog.”

The tokens are the same, but their order changes who chases whom. Representations therefore need information about position in addition to lexical identity.

**Check yourself**

The same token ID appears at two different positions. Must its initial lexical embedding be different? Is the positional information used by the Transformer the same?

<details>
<summary>Show the answer</summary>

The lexical embedding selected by the same ID is the same for a fixed matrix. Positional information, however, depends on position: an additive scheme adds a different position vector to the input, while RoPE applies position-dependent transformations to queries and keys. Attention computations can therefore differ even though the initial lexical embedding is unchanged.

</details>

**Takeaway**

Token identity and position are distinct kinds of information. The Transformer needs an order signal, but the methods used to encode it vary across architectures.

**Understand more:** [Positional encoding](../site/en/positional-encoding.qmd)  
**Practice:** [Exercises — Positional encoding](../site/en/exercises/positional-encoding.qmd)

---

## Day 07 — Why can the same token have different representations?

**Act:** Context and representations  
**Activity:** conceptual check  
**Target duration:** 6 minutes  
**Canonical references:** `contextualized-representation`, `token-embedding`; computational nodes `initial-hidden-states`, `transformer-block-input`, `contextualized-hidden-states`

### Français

**Question**

Deux occurrences du même token doivent-elles avoir le même état caché ?

**Réponse courte**

Avec un tokenizer, un vocabulaire et une matrice d'embeddings fixes, le même token ID sélectionne la même ligne `E[i]` lors du lookup initial. Mais cette égalité ne se propage pas automatiquement dans le réseau : l'information positionnelle et les tokens accessibles contribuent aux calculs des blocs Transformer. Les états cachés contextualisés peuvent donc différer selon la position et le contexte.

**Exemple guidé**

Considérons deux emplois de « vol » :

- « Le pilote prépare le vol » — un trajet aérien.
- « Le voleur prépare le vol » — un larcin.

Le token « vol » apparaît à la même position dans les deux exemples, mais les préfixes diffèrent. Supposons que le tokenizer lui attribue le même ID dans les deux cas. Le lookup initial `E[i]` est alors le même. En revanche, les préfixes accessibles diffèrent ; les blocs Transformer peuvent donc construire des états cachés différents. L'exemple suppose explicitement un token unique : un mot visible peut en réalité être découpé en plusieurs tokens.

**À vous de vérifier**

À poids fixes, deux occurrences ont le même ID et une même position, mais des préfixes accessibles différents. Leur état caché doit-il être identique ? Dans un GPT causal, un token strictement situé après la position courante peut-il modifier l'état calculé à cette position ?

<details>
<summary>Afficher la réponse</summary>

Non : le lookup initial est identique, mais le contexte accessible peut conduire à des états contextualisés différents. Et non : le masque causal empêche une position de dépendre des tokens futurs.

</details>

**À retenir**

Même ID → même embedding initial ; le contexte accessible et la position contribuent ensuite à la représentation contextualisée. Dans un décodeur causal, cette dépendance reste limitée au préfixe autorisé.

**Pour aller plus loin :** [Représentations contextualisées](../site/fr/contextualized-representations.qmd)  
**S'exercer :** [Exercices — représentations contextualisées](../site/fr/exercises/contextualized-representations.qmd)

### English

**Question**

Must two occurrences of the same token have the same hidden state?

**Short answer**

With a fixed tokenizer, vocabulary, and embedding matrix, the same token ID selects the same row `E[i]` during the initial lookup. That equality does not automatically persist through the network: positional information and the tokens accessible to the position contribute to Transformer-block computations. Contextualized hidden states can therefore differ with position and context.

**Guided example**

Consider the two uses of “bat”:

- “The player saw a bat” — sports equipment.
- “The cave contained a bat” — an animal.

The token “bat” appears at the same position in both examples, but the prefixes differ. Assume the tokenizer assigns it the same ID in both cases. The initial lookup `E[i]` is then the same. The accessible prefixes differ, however, so Transformer blocks may construct different hidden states. This example explicitly assumes one token; a visible word may in practice be split into several tokens.

**Check yourself**

With fixed weights, two occurrences have the same ID and the same position, but different accessible prefixes. Must their hidden states be identical? In a causal GPT, can a token strictly after the current position change the state computed at that position?

<details>
<summary>Show the answer</summary>

No: the initial lookup is identical, but the accessible context can lead to different contextualized states. And no: the causal mask prevents a position from depending on future tokens.

</details>

**Takeaway**

Same ID → same initial embedding; accessible context and position then contribute to the contextualized representation. In a causal decoder, this dependency is restricted to the permitted prefix.

**Learn more:** [Contextualized representations](../site/en/contextualized-representations.qmd)  
**Practice:** [Exercises — contextualized representations](../site/en/exercises/contextualized-representations.qmd)

---

## Day 08 — What does a Transformer block do?

**Act:** Transformer computation  
**Activity:** trace  
**Target duration:** 7 minutes  
**Canonical references:** `self-attention`, `multi-head-attention`; computational nodes `transformer-block-input`, `block-update`

### Français

**Question**

Quelles grandes opérations transforment les états d'entrée d'un bloc Transformer ?

**Réponse courte**

Dans le GPT de référence étudié ici, un bloc Transformer est une unité de calcul répétée dans une pile. Il combine deux sous-couches principales :

| Élément | Rôle |
|---|---|
| Auto-attention | Combine des informations entre les positions autorisées. |
| MLP (réseau feed-forward) | Transforme chaque position indépendamment, avec des poids partagés entre positions. |
| Connexions résiduelles | Réinjectent l'état précédent et l'actualisation produite par une sous-couche dans le flux résiduel. |
| Normalisation | Stabilise l'échelle des activations ; son placement dépend de la variante d'architecture. |

**Exemple guidé**

Suivez les états d'entrée d'un bloc : l'auto-attention permet à chaque position de combiner des informations provenant des positions autorisées ; la MLP transforme ensuite l'état de chaque position. Les connexions résiduelles et la normalisation accompagnent ces sous-couches. Les états de sortie deviennent l'entrée du bloc suivant.

Cette description est une carte fonctionnelle, pas un ordre d'exécution universel : le placement précis des normalisations et des additions résiduelles varie selon les architectures. Après la pile de blocs, la normalisation finale et la tête de sortie produisent les logits. La softmax et le décodage viennent ensuite, hors des blocs.

**À vous de vérifier**

Quelle sous-couche combine des informations entre positions, et laquelle transforme chaque position séparément ? Le bloc choisit-il lui-même le prochain token ?

<details>
<summary>Afficher la réponse</summary>

L'auto-attention combine des informations entre positions autorisées ; la MLP transforme chaque position indépendamment. Le bloc ne choisit pas de token : il produit des états cachés qui alimentent le bloc suivant ou, après la pile, la tête de sortie.

</details>

**À retenir**

Un bloc Transformer ne se réduit pas à l'attention : il associe attention, MLP, connexions résiduelles et normalisation. La pile transforme les représentations ; la prédiction du prochain token intervient à sa sortie.

**Pour aller plus loin :** [Architecture Transformer](../site/fr/transformer.qmd)  
**S'exercer :** [Exercices — Transformer](../site/fr/exercises/transformer.qmd)

### English

**Question**

Which major operations transform a Transformer's input states inside one block?

**Short answer**

In the reference GPT studied here, a Transformer block is a repeated computation unit in a stack. It combines two main sublayers:

| Component | Role |
|---|---|
| Self-attention | Combines information across permitted positions. |
| MLP (feed-forward network) | Transforms each position independently, using weights shared across positions. |
| Residual connections | Carry the previous state and the sublayer update into the residual stream. |
| Normalization | Stabilizes activation scale; its placement depends on the architecture variant. |

**Guided example**

Trace a block's input states: self-attention lets each position combine information from permitted positions; the MLP then transforms each position's state. Residual connections and normalization accompany these sublayers. The output states become the input to the next block.

This is a functional map, not a universal execution order: the exact placement of normalization and residual additions varies across architectures. After the stack of blocks, the final normalization and output head produce logits. Softmax and decoding come next, outside the blocks.

**Check your understanding**

Which sublayer combines information across positions, and which transforms each position independently? Does the block itself choose the next token?

<details>
<summary>Show the answer</summary>

Self-attention combines information across permitted positions; the MLP transforms each position independently. The block does not choose a token: it produces hidden states that feed the next block or, after the stack, the output head.

</details>

**Takeaway**

A Transformer block is not just attention: it combines attention, an MLP, residual connections, and normalization. The stack transforms representations; next-token prediction happens at its output.

**Learn more:** [Transformer architecture](../site/en/transformer.qmd)  
**Practice:** [Exercises — Transformer](../site/en/exercises/transformer.qmd)

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
| 03 — Tokenization | Explain why two tokenizers can segment the same character string into different token sequences. | Distinguishes the original string from tokenizer-dependent token segmentation. |
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
