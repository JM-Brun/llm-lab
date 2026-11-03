# Formative sequence: text to representations

> **Status: design draft — not learner-release ready.** This document operationalizes issue [#220](https://github.com/JM-Brun/llm-lab/issues/220). It reuses canonical lesson content; it is not a new concept chapter. Release remains gated by the deferred desktop/mobile browser review in [#320](https://github.com/JM-Brun/llm-lab/issues/320); source-level foundational work is tracked separately in the now-closed [#82](https://github.com/JM-Brun/llm-lab/issues/82).

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
| TR-05 | Complete a partially worked shape trace | Complete shapes while distinguishing vocabulary, sequence and feature axes | TR-02 | embedding-space; tensors | G3 |
| TR-06 | Predict what changes and what remains invariant | Separate lookup invariants from positional and contextual effects | TR-01–TR-03 and the positional/contextualization overview | contextualized-representations; positional-encoding | G3 |

**Suggested teaching order:** TR-01 → TR-02 → TR-05 → TR-03 → TR-06 → TR-04. The stable IDs identify activities across languages and references; they do not prescribe a numerical order. The sequence deliberately moves from reconstruction to a worked calculation, scaffolded completion, less-scaffolded tracing, prediction, and finally misconception diagnosis.

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

For a fixed tokenizer and fixed embedding matrix, classify each statement as **valid**, **invalid**, or **architecture-dependent**, and justify your choice. No specific model configuration is supplied: when a statement refers to “this model”, decide whether the information given is sufficient to determine its behavior.

A. The same token ID selects the same initial embedding row on every occurrence.

B. Two token IDs with consecutive integer values must have similar embeddings.

C. The same token ID must have the same contextualized hidden state in every sentence.

D. This model adds a learned absolute position vector to each token embedding before its first Transformer block.

E. RoPE is applied to query/key representations inside attention, rather than being a vector universally added by the embedding lookup.

**Progressive hints**

1. Hold the tokenizer and matrix fixed.
2. Separate the lookup result from later network states.
3. Distinguish a common architecture family from a universal rule.

**Worked solution**

- **A — Valid**, under the stated fixed-matrix condition: lookup selects the same row.
- **B — Invalid:** row indices are labels, not coordinates.
- **C — Invalid:** context and position can change later hidden states even when the initial lookup is identical.
- **D — Architecture-dependent / not decidable from the information given:** learned absolute position embeddings are one possible design, but the exercise does not specify which positional mechanism this model uses. Do not turn a possible design into a universal claim.
- **E — Valid as a description of RoPE:** it acts on query/key vectors within attention; other positional mechanisms exist.

**Misconception feedback**

The decisive distinction is between a property of the tokenizer, a property of a fixed lookup table, and a property of the complete network computation. Do not infer the last from the first two.

**Assessment criterion:** classifications and justifications distinguish fixed lookup invariants from context-dependent outputs and architecture-specific mechanisms.

### Consigne française

Pour un tokenizer et une matrice d'embeddings fixés, classez chaque affirmation comme **valide**, **invalide** ou **dépendante de l'architecture**, puis justifiez votre choix. Aucune configuration de modèle particulière n'est fournie : lorsqu'une affirmation parle de « ce modèle », déterminez si les informations données suffisent pour établir son comportement.

A. Le même ID sélectionne la même ligne d'embedding initial à chaque occurrence.

B. Deux IDs consécutifs doivent avoir des embeddings similaires.

C. Un même ID doit produire le même état caché contextualisé dans toutes les phrases.

D. Ce modèle ajoute un vecteur positionnel absolu appris à chaque embedding de token avant son premier bloc Transformer.

E. RoPE s'applique aux représentations requête/clé dans l'attention ; ce n'est pas un vecteur ajouté universellement par le lookup.

**Indices progressifs**

1. Considérez le tokenizer et la matrice comme fixes.
2. Séparez le résultat du lookup des états produits ensuite par le réseau.
3. Distinguez une famille d'architectures courante d'une règle universelle.

**Solution détaillée**

- **A — Valide**, sous l'hypothèse d'une matrice fixe : le lookup sélectionne la même ligne.
- **B — Invalide :** les indices de lignes sont des étiquettes, pas des coordonnées.
- **C — Invalide :** le contexte et la position peuvent modifier les états cachés ultérieurs même si le lookup initial est identique.
- **D — Dépendante de l'architecture / indéterminable avec les informations fournies :** les embeddings positionnels absolus appris constituent une possibilité, mais l'exercice ne précise pas le mécanisme positionnel utilisé par ce modèle. Il ne faut pas transformer une conception possible en règle universelle.
- **E — Valide pour décrire RoPE :** le mécanisme agit sur les vecteurs requête/clé dans l'attention ; d'autres mécanismes positionnels existent.

**Retour sur les erreurs fréquentes**

La distinction décisive sépare une propriété du tokenizer, une propriété d'une table de lookup fixée et une propriété du calcul complet du réseau. Il ne faut pas déduire la troisième des deux premières.

**Critère d'évaluation :** les classements et justifications distinguent les invariants du lookup fixe, les sorties dépendantes du contexte et les mécanismes propres à certaines architectures.

---

## TR-05 — Complete a partially worked shape trace

**Outcome:** complete a scaffolded representation trace without confusing the vocabulary axis, sequence axis and feature axis.

### English prompt

A batch contains two sequences, each represented by three token IDs. The embedding table has vocabulary size \(V=5\) and embedding dimension \(d=2\).

Complete the missing entries:

| Object | Shape | Meaning |
|---|---:|---|
| Embedding table \(E\) | \((5,2)\) | vocabulary entries × features |
| Token IDs | \((2,3)\) | batch × sequence |
| Lookup result | ? | batch × sequence × features |
| One sequence after lookup | ? | sequence × features |

Then explain why the vocabulary size \(V\) does not appear as an axis in the lookup result.

**Progressive hints**

1. Each of the six IDs selects one row of \(E\).
2. The selected row has length \(d=2\).
3. The lookup output contains one vector for each batch-position pair, not the entire vocabulary table.

**Worked solution**

The lookup result has shape \((2,3,2)\); one sequence has shape \((3,2)\). The vocabulary axis indexes the source table. After row selection, the output axes describe the batch, sequence positions and features. The vocabulary dimension is therefore not retained as an output axis.

**Misconception feedback**

- \((2,3,5,2)\) would incorrectly retain the whole vocabulary table as an extra output axis.
- \((2,3,5)\) confuses vocabulary size with embedding width.
- \((2,2,3)\) swaps the sequence and feature axes.

**Assessment criterion:** both shapes are correct and the learner explains why lookup removes the vocabulary axis from the selected output.

### Consigne française

Un batch contient deux séquences de trois IDs chacune. La table d'embeddings possède un vocabulaire de taille \(V=5\) et une dimension d'embedding \(d=2\).

Complétez les formes manquantes :

| Objet | Forme | Signification |
|---|---:|---|
| Table d'embeddings \(E\) | \((5,2)\) | entrées du vocabulaire × caractéristiques |
| IDs des tokens | \((2,3)\) | batch × séquence |
| Résultat du lookup | ? | batch × séquence × caractéristiques |
| Une séquence après lookup | ? | séquence × caractéristiques |

Expliquez ensuite pourquoi la taille du vocabulaire \(V\) ne figure pas parmi les axes du résultat du lookup.

**Indices progressifs**

1. Chacun des six IDs sélectionne une ligne de \(E\).
2. La ligne sélectionnée possède une longueur \(d=2\).
3. Le résultat contient un vecteur par couple batch-position, et non toute la table du vocabulaire.

**Solution détaillée**

Le résultat du lookup a pour forme \((2,3,2)\) ; une séquence a pour forme \((3,2)\). L'axe du vocabulaire indexe la table source. Après sélection des lignes, les axes du résultat décrivent le batch, les positions de séquence et les caractéristiques. La dimension du vocabulaire n'est donc pas conservée comme axe de sortie.

**Retour sur les erreurs fréquentes**

- \((2,3,5,2)\) conserverait à tort toute la table du vocabulaire comme axe supplémentaire.
- \((2,3,5)\) confond la taille du vocabulaire et la largeur des embeddings.
- \((2,2,3)\) échange les axes séquence et caractéristiques.

**Critère d'évaluation :** les deux formes sont correctes et l'explication montre pourquoi le lookup élimine l'axe du vocabulaire du résultat sélectionné.

---

## TR-06 — Predict what changes, and what stays invariant

**Outcome:** predict which representation changes when token identity, position or surrounding context changes, while holding the tokenizer and parameters fixed.

### English prompt

Assume a deterministic tokenizer and a fixed model checkpoint. Consider the same token ID \(t\) in these situations:

1. It occurs twice in the same input sequence.
2. It occurs in two different input sequences with different preceding (visible) context. For a decoder-only causal model, tokens to the right are masked and cannot affect this position.
3. It is replaced by a different ID \(u\), while all other positions remain unchanged.

For each situation, predict whether the following can change:

- the initial embedding selected by lookup;
- the effect of the positional mechanism (whether applied to the token stream before the first block or inside attention);
- the contextualized hidden state.

State any architectural qualification needed. Do not assume that a change at one position leaves all later states unchanged.

**Progressive hints**

1. A fixed embedding table maps an ID to a fixed row.
2. Some architectures add position information to the token stream before the first block; RoPE instead transforms query/key vectors inside attention. Do not assume every model has a distinct position-aware input embedding.
3. Contextualized states depend on the network computation and surrounding input.

**Worked solution**

1. The same ID selects the same initial embedding row. If the architecture adds learned absolute position embeddings before the first block, the resulting input representation can differ by position. With a mechanism such as RoPE, the token embedding itself is not changed by a position vector; positional effects enter later inside attention. Contextualized states may differ because position and surrounding context matter.
2. The initial lookup row remains the same for the same ID and fixed table. The positional mechanism may act on the token stream or inside attention, depending on the architecture. Contextualized states can differ when the preceding/visible context differs; in a causal decoder, tokens to the right cannot affect this position.
3. A different ID generally selects a different row. If its position is unchanged, the positional operation itself need not change: an absolute scheme adds the same position vector, while RoPE applies the same position-dependent rotation to the newly computed query/key vectors. The resulting position-aware representations can nevertheless change because their content inputs changed. Contextualized states may change at that position and at other positions that depend on it.

These are qualitative predictions, not guarantees about the magnitude of a numerical change. Exact effects depend on architecture, masking, position mechanism and model parameters.

**Misconception feedback**

- “Same ID means same hidden state”: only the initial lookup row is invariant under a fixed table; later computation is context-sensitive.
- “Changing one ID affects only one output position”: contextual mixing can propagate the change to other positions, subject to the architecture and attention mask.
- “Different IDs must produce very different vectors”: distinct rows need not be far apart geometrically.

**Assessment criterion:** the learner separates lookup invariance from position- and context-dependent representations, and avoids unsupported claims about the magnitude or propagation of changes.

### Consigne française

Supposez que le tokenizer soit déterministe et que le checkpoint du modèle soit fixe. Considérez le même ID \(t\) dans les situations suivantes :

1. Il apparaît deux fois dans la même séquence d'entrée.
2. Il apparaît dans deux séquences différentes, avec un contexte précédent (visible) différent. Dans un modèle décodeur causal, les tokens situés à droite sont masqués et ne peuvent pas influer sur cette position.
3. Il est remplacé par un autre ID \(u\), tous les autres emplacements restant inchangés.

Pour chaque situation, prévoyez si les éléments suivants peuvent changer :

- l'embedding initial sélectionné par lookup ;
- l'effet du mécanisme positionnel (appliqué au flux de tokens avant le premier bloc ou à l'intérieur de l'attention) ;
- l'état caché contextualisé.

Précisez les réserves liées à l'architecture. Ne supposez pas qu'un changement à une position laisse nécessairement inchangés tous les états ultérieurs.

**Indices progressifs**

1. Une table d'embeddings fixe associe un ID à une ligne fixe.
2. Certaines architectures ajoutent l'information positionnelle au flux de tokens avant le premier bloc ; RoPE transforme plutôt les vecteurs requête/clé à l'intérieur de l'attention. Ne supposez pas que chaque modèle possède un embedding d'entrée distinct tenant compte de la position.
3. Les états contextualisés dépendent du calcul du réseau et du contexte de la séquence.

**Solution détaillée**

1. Le même ID sélectionne la même ligne d'embedding initial. Si l'architecture ajoute des embeddings positionnels absolus appris avant le premier bloc, la représentation d'entrée qui en résulte peut différer selon la position. Avec un mécanisme comme RoPE, l'embedding du token n'est pas modifié par un vecteur positionnel ; les effets de position interviennent plus tard, dans l'attention. Les états contextualisés peuvent différer en raison de la position et du contexte.
2. La ligne initiale sélectionnée reste la même pour un ID donné et une table fixe. Le mécanisme positionnel peut agir sur le flux de tokens ou à l'intérieur de l'attention, selon l'architecture. Les états contextualisés peuvent différer lorsque le contexte précédent/visible change ; dans un décodeur causal, les tokens situés à droite ne peuvent pas influer sur cette position.
3. Un ID différent sélectionne généralement une autre ligne. Si sa position reste inchangée, l'opération positionnelle elle-même n'a pas besoin de changer : un mécanisme absolu ajoute le même vecteur de position, tandis que RoPE applique la même rotation dépendant de la position aux nouveaux vecteurs requête/clé calculés. Les représentations résultantes tenant compte de la position peuvent néanmoins changer puisque leur contenu d'entrée a changé. Les états contextualisés peuvent changer à cette position ainsi qu'à d'autres positions qui en dépendent.

Il s'agit de prédictions qualitatives, pas de garanties sur l'amplitude d'un changement numérique. Les effets exacts dépendent de l'architecture, du masque, du mécanisme positionnel et des paramètres du modèle.

**Retour sur les erreurs fréquentes**

- « Même ID signifie même état caché » : seule la ligne du lookup initial est invariante pour une table fixe ; les calculs ultérieurs dépendent du contexte.
- « Changer un ID ne modifie que la sortie à cette position » : le mélange contextuel peut propager le changement à d'autres positions, selon l'architecture et le masque d'attention.
- « Des IDs différents doivent produire des vecteurs très éloignés » : des lignes distinctes ne sont pas nécessairement éloignées géométriquement.

**Critère d'évaluation :** l'apprenant distingue l'invariance du lookup des représentations dépendantes de la position et du contexte, sans avancer d'affirmation non justifiée sur l'amplitude ou la propagation des changements.

---

## Review and release checklist

- [ ] Verify every statement against the current canonical FR/EN pages.
- [ ] Independently recompute the TR-02 matrix selection and TR-03 shapes.
- [ ] Check mathematical notation and Quarto rendering in both languages.
- [ ] Review whether the activity sequence is cognitively progressive without making the first pass too long.
- [ ] Check that feedback diagnoses the reasoning error, not merely the wrong answer.
- [ ] Review desktop and mobile rendering when the deferred #320 browser gate is completed.
- [ ] Only then decide whether to embed these activities in existing pages or publish a separate practice destination.
- [ ] Do not add transfer assessment until the first learning sequence is complete.

## Ownership and evidence

- Exercise design and answer keys: [#220](https://github.com/JM-Brun/llm-lab/issues/220).
- Foundational source/content: [#82](https://github.com/JM-Brun/llm-lab/issues/82) (closed); deferred browser review: [#320](https://github.com/JM-Brun/llm-lab/issues/320).
- Milestone mapping: [#87](https://github.com/JM-Brun/llm-lab/issues/87).
- Reader-facing architecture: [#130](https://github.com/JM-Brun/llm-lab/issues/130).

Authored content is not yet independently reviewed, rendered, browser-reviewed, or learner-evaluated. Those are separate evidence states.
