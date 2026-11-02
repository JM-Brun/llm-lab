# Formative sequence: text to representations

> **Status: design draft — not learner-release ready.** This document operationalizes issue [#220](https://github.com/JM-Brun/llm-lab/issues/220). It reuses canonical lesson content; it is not a new concept chapter. Release remains gated by the desktop/mobile browser review in [#82](https://github.com/JM-Brun/llm-lab/issues/82).

## Design contract

- Stable activity IDs are shared by French and English.
- Every prompt targets an observable operation: reconstruct, calculate, trace, predict, or diagnose.
- Solutions distinguish what follows mathematically from what depends on an architecture or tokenizer.
- The numerical embedding values are synthetic and reused from the canonical [embedding-space lesson](../site/en/embedding-space.qmd); they are not model parameters.
- No score is interpreted as evidence of retention or mastery. Transfer is deliberately omitted until the first sequence is complete.

## Sequence map

| ID | Activity | Observable outcome | Prerequisite | Canonical pages | G milestone |
|---|---|---|---|---|---|
| TR-01 | Reconstruct the pipeline | Put transformations in order and distinguish their outputs | First-pass text/token lesson | text-data; embedding-space | G1–G3 |
| TR-02 | Perform an embedding lookup | Select matrix rows and state the output shape | Matrix and index notation | embedding-space; tensors (optional) | G3 |
| TR-03 | Trace batch and axes | Infer shapes and explain what lookup does not do | TR-02 | embedding-space; tensors | G3 |
| TR-04 | Diagnose identity vs context | Reject invalid claims about IDs, initial vectors, position and hidden states | Pipeline and contextualization overview | contextualized-representations; positional-encoding | G3 |

---

## TR-01 — Reconstruct the pipeline

**Outcome:** reconstruct the path from a text string to context-dependent hidden states and identify the object produced at each stage.

### English prompt

Place these items in causal order, then write one sentence describing what each arrow does:

- token IDs
- contextualized hidden states
- source text
- token strings/fragments
- initial token embeddings

Do not insert a universal “position vector added at lookup” step. State where position handling belongs at this level of abstraction.

**Progressive hints**

1. Ask which component defines the token vocabulary.
2. An ID is used to retrieve a row; it is not itself a vector.
3. Contextualization happens after the initial lookup.

**Worked solution**

Source text → tokenizer output (tokens/fragments) → integer token IDs → embedding-table lookup → initial token embeddings → architecture-dependent position handling and network processing → contextualized hidden states.

The tokenizer maps text to discrete vocabulary entries. The IDs index the embedding table. The lookup selects vectors but does not mix information across sequence positions. Subsequent model computation produces context-dependent states. Position handling is architecture-dependent: learned absolute position embeddings may be added to token embeddings, while RoPE acts on query/key vectors inside attention.

**Misconception feedback**

- “The tokenizer produces embeddings”: it produces token units and IDs; the model's embedding table supplies vectors.
- “The ID is a coordinate”: it is a discrete vocabulary index. Arithmetic distance between IDs has no general semantic interpretation.
- “Every model adds a position vector immediately after lookup”: false; positional mechanisms differ.

**Assessment criterion:** all stages are ordered correctly; the learner distinguishes token, ID, initial vector and contextualized state; positional handling is not presented as universal.

### Consigne française

Remettez les éléments dans l'ordre causal, puis décrivez en une phrase ce que réalise chaque flèche :

- IDs des tokens
- états cachés contextualisés
- texte source
- fragments ou chaînes de tokens
- embeddings initiaux des tokens

N'insérez pas une étape universelle « vecteur de position ajouté au lookup ». Indiquez où se situe le traitement positionnel à ce niveau d'abstraction.

**Indices progressifs**

1. Quel composant définit le vocabulaire des tokens ?
2. Un ID sert à sélectionner une ligne ; ce n'est pas un vecteur.
3. La contextualisation intervient après le lookup initial.

**Solution détaillée**

Texte source → sortie du tokenizer (tokens/fragments) → IDs entiers → lookup dans la table d'embeddings → embeddings initiaux → traitement positionnel et calcul du réseau, dépendants de l'architecture → états cachés contextualisés.

Le tokenizer transforme le texte en unités discrètes du vocabulaire. Les IDs indexent la table d'embeddings. Le lookup sélectionne des vecteurs, sans mélanger les informations entre positions de la séquence. Les calculs ultérieurs du modèle produisent des états dépendant du contexte. Le traitement positionnel dépend de l'architecture : des embeddings positionnels absolus appris peuvent être ajoutés aux embeddings des tokens, tandis que RoPE agit sur les vecteurs requête/clé dans l'attention.

**Retour sur les erreurs fréquentes**

- « Le tokenizer produit les embeddings » : il produit des unités de tokens et des IDs ; la table du modèle fournit les vecteurs.
- « L'ID est une coordonnée » : c'est un indice discret dans le vocabulaire. La distance arithmétique entre IDs n'a pas d'interprétation sémantique générale.
- « Tous les modèles ajoutent un vecteur de position juste après le lookup » : non, les mécanismes positionnels diffèrent.

**Critère d'évaluation :** ordre correct ; distinction entre token, ID, vecteur initial et état contextualisé ; absence de généralisation abusive sur le traitement positionnel.

---

## TR-02 — Perform an embedding lookup

**Outcome:** calculate a lookup result from a matrix and explain its dimensions.

Use the synthetic matrix already introduced in the [canonical lesson](../site/en/embedding-space.qmd):

\[
E = \begin{bmatrix}
0.1 & 0.0 \\
0.0 & 0.2 \\
0.8 & -0.1 \\
-0.2 & 0.5 \\
0.3 & 0.7
\end{bmatrix}
\in \mathbb{R}^{5\times 2}.
\]

### English prompt

For token IDs \([2,0,3]\):

1. Which rows are selected, in order?
2. Write the resulting matrix \(X\).
3. Give its shape.
4. Would changing ID 3 to ID 4 mean “moving one unit” in embedding space? Explain.

**Progressive hints**

1. IDs are zero-based row indices in this example.
2. Copy the selected rows without adding or averaging them.
3. The sequence length is the number of selected IDs; the embedding dimension is the number of columns.

**Worked solution**

The selected rows are \(E_2\), \(E_0\), and \(E_3\), so

\[
X = \begin{bmatrix}
0.8 & -0.1 \\
0.1 & 0.0 \\
-0.2 & 0.5
\end{bmatrix}
\in \mathbb{R}^{3\times 2}.
\]

The shape is \((L,d)=(3,2)\): three token positions and two features per token. Replacing ID 3 by ID 4 selects a different row; the integer difference is not a distance or displacement in the learned vector space.

**Misconception feedback**

- Selecting columns instead of rows confuses embedding dimension with vocabulary index.
- Averaging selected rows changes the operation: lookup returns one row per ID.
- “ID 4 is one unit from ID 3” confuses discrete labels with geometric coordinates.

**Assessment criterion:** exact matrix, shape and explanation of why ID arithmetic is not embedding geometry.

### Consigne française

Pour les IDs \([2,0,3]\) :

1. Quelles lignes sont sélectionnées, dans quel ordre ?
2. Écrivez la matrice résultante \(X\).
3. Donnez sa forme.
4. Remplacer l'ID 3 par l'ID 4 revient-il à « avancer d'une unité » dans l'espace des embeddings ? Expliquez.

**Indices progressifs**

1. Dans cet exemple, les IDs sont des indices de lignes commençant à zéro.
2. Recopiez les lignes sélectionnées, sans les additionner ni en faire la moyenne.
3. La longueur de séquence est le nombre d'IDs ; la dimension d'embedding est le nombre de colonnes.

**Solution détaillée**

Les lignes sélectionnées sont \(E_2\), \(E_0\) et \(E_3\), donc

\[
X = \begin{bmatrix}
0.8 & -0.1 \\
0.1 & 0.0 \\
-0.2 & 0.5
\end{bmatrix}
\in \mathbb{R}^{3\times 2}.
\]

La forme est \((L,d)=(3,2)\) : trois positions de tokens et deux caractéristiques par token. Remplacer l'ID 3 par l'ID 4 sélectionne une autre ligne ; la différence entre les entiers n'est ni une distance ni un déplacement dans l'espace vectoriel appris.

**Retour sur les erreurs fréquentes**

- Sélectionner des colonnes au lieu des lignes confond dimension d'embedding et indice de vocabulaire.
- Faire la moyenne des lignes change l'opération : un lookup renvoie une ligne par ID.
- « L'ID 4 est à une unité de l'ID 3 » confond étiquettes discrètes et coordonnées géométriques.

**Critère d'évaluation :** matrice, forme et explication exactes sur l'absence de sens géométrique de l'arithmétique des IDs.

---

## TR-03 — Trace batch shapes and axes

**Outcome:** infer common tensor shapes and identify which axes lookup preserves.

### English prompt

A batch contains \(B=2\) sequences, each with \(L=3\) token IDs. The embedding dimension is \(d=2\).

1. Give the shape of the ID tensor.
2. Give the shape after embedding lookup.
3. Does lookup combine information between the three positions?
4. If a later width-preserving Transformer block returns hidden states, what is their common shape?

**Progressive hints**

1. Count examples, then positions.
2. Each ID is replaced by a vector of length \(d\).
3. Lookup is an indexed selection, not a contextual mixing operation.

**Worked solution**

\[
\text{IDs}: (B,L)=(2,3), \qquad
\text{embeddings}: (B,L,d)=(2,3,2).
\]

Lookup preserves batch and sequence-position axes and adds the feature axis. It does not mix information across positions. A width-preserving block commonly returns hidden states of shape \((2,3,2)\), although exact conventions depend on the architecture and implementation.

**Misconception feedback**

- \((2,2,3)\) swaps the position and feature axes.
- \((2,3)\) omits the vector dimension after lookup.
- Claiming that lookup contextualizes tokens assigns the Transformer's later computation to the embedding table.

**Assessment criterion:** correct shapes, axes named by meaning, and explicit separation of lookup from contextualization.

### Consigne française

Un batch contient \(B=2\) séquences, chacune composée de \(L=3\) IDs. La dimension d'embedding vaut \(d=2\).

1. Quelle est la forme du tenseur d'IDs ?
2. Quelle est sa forme après le lookup ?
3. Le lookup combine-t-il les informations entre les trois positions ?
4. Si un bloc Transformer ultérieur conserve la largeur, quelle est la forme usuelle de ses états cachés ?

**Indices progressifs**

1. Comptez d'abord les exemples, puis les positions.
2. Chaque ID est remplacé par un vecteur de longueur \(d\).
3. Le lookup est une sélection indexée, pas une opération de mélange contextuel.

**Solution détaillée**

\[
\text{IDs}: (B,L)=(2,3), \qquad
\text{embeddings}: (B,L,d)=(2,3,2).
\]

Le lookup conserve les axes batch et position, et ajoute l'axe des caractéristiques. Il ne mélange pas les informations entre positions. Un bloc Transformer qui conserve la largeur renvoie couramment des états cachés de forme \((2,3,2)\), mais les conventions exactes dépendent de l'architecture et de l'implémentation.

**Retour sur les erreurs fréquentes**

- \((2,2,3)\) échange les axes position et caractéristiques.
- \((2,3)\) omet la dimension vectorielle après le lookup.
- Dire que le lookup contextualise les tokens attribue à la table d'embeddings un calcul réalisé plus tard par le Transformer.

**Critère d'évaluation :** formes correctes, axes nommés selon leur rôle et distinction explicite entre lookup et contextualisation.

---

## TR-04 — Diagnose identity, position and context

**Outcome:** evaluate claims against the pipeline and architectural qualifications.

### English prompt

For a fixed tokenizer and fixed embedding matrix, classify each statement as **valid**, **invalid**, or **architecture-dependent**, and justify your choice.

A. The same token ID selects the same initial embedding row on every occurrence.

B. Two token IDs with consecutive integer values must have similar embeddings.

C. The same token ID must have the same contextualized hidden state in every sentence.

D. Every Transformer adds a learned position vector directly to the token embedding.

E. RoPE is applied to query/key representations inside attention, rather than being a vector universally added by the embedding lookup.

**Progressive hints**

1. Hold the tokenizer and matrix fixed.
2. Separate the lookup result from later network states.
3. Distinguish a common architecture family from a universal rule.

**Worked solution**

- **A — Valid**, under the stated fixed-matrix condition: lookup selects the same row.
- **B — Invalid:** row indices are labels, not coordinates.
- **C — Invalid:** context and position can change later hidden states even when the initial lookup is identical.
- **D — Invalid:** learned absolute position embeddings are one approach, not a universal Transformer rule.
- **E — Valid as a description of RoPE:** it acts on query/key vectors within attention; other positional mechanisms exist.

**Misconception feedback**

The decisive distinction is between a property of the tokenizer, a property of a fixed lookup table, and a property of the complete network computation. Do not infer the last from the first two.

**Assessment criterion:** classifications and justifications distinguish fixed lookup invariants from context-dependent outputs and architecture-specific mechanisms.

### Consigne française

Pour un tokenizer et une matrice d'embeddings fixés, classez chaque affirmation comme **valide**, **invalide** ou **dépendante de l'architecture**, puis justifiez votre choix.

A. Le même ID sélectionne la même ligne d'embedding initial à chaque occurrence.

B. Deux IDs consécutifs doivent avoir des embeddings similaires.

C. Un même ID doit produire le même état caché contextualisé dans toutes les phrases.

D. Chaque Transformer ajoute directement un vecteur positionnel appris à l'embedding du token.

E. RoPE s'applique aux représentations requête/clé dans l'attention ; ce n'est pas un vecteur ajouté universellement par le lookup.

**Indices progressifs**

1. Considérez le tokenizer et la matrice comme fixes.
2. Séparez le résultat du lookup des états produits ensuite par le réseau.
3. Distinguez une famille d'architectures courante d'une règle universelle.

**Solution détaillée**

- **A — Valide**, sous l'hypothèse d'une matrice fixe : le lookup sélectionne la même ligne.
- **B — Invalide :** les indices de lignes sont des étiquettes, pas des coordonnées.
- **C — Invalide :** le contexte et la position peuvent modifier les états cachés ultérieurs même si le lookup initial est identique.
- **D — Invalide :** les embeddings positionnels absolus appris constituent une approche, pas une règle universelle des Transformers.
- **E — Valide pour décrire RoPE :** le mécanisme agit sur les vecteurs requête/clé dans l'attention ; d'autres mécanismes positionnels existent.

**Retour sur les erreurs fréquentes**

La distinction décisive sépare une propriété du tokenizer, une propriété d'une table de lookup fixée et une propriété du calcul complet du réseau. Il ne faut pas déduire la troisième des deux premières.

**Critère d'évaluation :** les classements et justifications distinguent les invariants du lookup fixe, les sorties dépendantes du contexte et les mécanismes propres à certaines architectures.

---

## Review and release checklist

- [ ] Verify every statement against the current canonical FR/EN pages.
- [ ] Independently recompute the TR-02 matrix selection and TR-03 shapes.
- [ ] Check mathematical notation and Quarto rendering in both languages.
- [ ] Review whether the activity sequence is cognitively progressive without making the first pass too long.
- [ ] Check that feedback diagnoses the reasoning error, not merely the wrong answer.
- [ ] Review desktop and mobile rendering after the #82 browser gate is completed.
- [ ] Only then decide whether to embed these activities in existing pages or publish a separate practice destination.
- [ ] Do not add transfer assessment until the first learning sequence is complete.

## Ownership and evidence

- Exercise design and answer keys: [#220](https://github.com/JM-Brun/llm-lab/issues/220).
- Foundational source/content and browser gate: [#82](https://github.com/JM-Brun/llm-lab/issues/82).
- Milestone mapping: [#87](https://github.com/JM-Brun/llm-lab/issues/87).
- Reader-facing architecture: [#130](https://github.com/JM-Brun/llm-lab/issues/130).

Authored content is not yet independently reviewed, rendered, browser-reviewed, or learner-evaluated. Those are separate evidence states.
