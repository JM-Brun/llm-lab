# Deux sens de la compression appliqués aux LLM — comparaison pédagogique

**Périmètre :** comparaison de deux billets introductifs, pas une revue systématique :
- Karthik Shashidhar, [LLMs and compression algorithms](https://artofdatascience.substack.com/p/llms-and-compression-algorithms), 27 août 2024.
- Sasirekha Cota, [Understanding Compression of Large Language Models (LLMs)](https://medium.com/@sasirekharameshkumar/understanding-compression-of-large-language-models-2ee3b8a350a2), 22 novembre 2023.

## 1. La confusion à éviter

Le mot *compression* désigne ici deux opérations différentes :

1. **Compression prédictive / statistique :** exploiter un modèle probabiliste pour représenter une séquence avec un code plus court en moyenne, parce que les événements prévisibles reçoivent des codes plus courts.
2. **Compression du modèle :** réduire la représentation numérique ou la structure du modèle lui-même afin de diminuer sa taille, sa mémoire, son coût ou sa latence d'exécution.

Ces opérations peuvent être liées dans un système complet, mais elles ne répondent pas à la même question et ne se mesurent pas avec les mêmes métriques.

## 2. Comparaison directe

| Dimension | Compression prédictive (Shashidhar) | Compression du modèle (Cota) |
|---|---|---|
| Question | Pourquoi les régularités apprises rendent-elles certaines continuations prévisibles ? | Comment réduire le coût de stockage et d'exécution d'un modèle ? |
| Objet compressé | Une séquence / un flux de données, encodé à l'aide d'un modèle de probabilité | Les paramètres et/ou certaines structures du modèle |
| Mécanisme central | Probabilités conditionnelles, surprisal et codage entropique | Pruning, quantification, distillation |
| Où intervient le LLM ? | Comme modèle probabiliste qui attribue des probabilités aux prochains tokens | Comme objet que l'on transforme, ou comme enseignant qui entraîne un étudiant |
| Mesure pertinente | Longueur de code, bits par token, cross-entropy / NLL | Taille du checkpoint, mémoire de travail, latence, débit, qualité |
| Perte d'information | Un codage entropique correctement conçu peut être sans perte ; l'approximation du modèle affecte l'efficacité, pas nécessairement l'exactitude du décodage | Quantification/pruning peuvent être avec perte ; distillation transfère sélectivement des comportements |
| Risque de mauvaise interprétation | Croire que les poids sont une archive compressée du corpus ou que générer équivaut à décompresser | Croire qu'un fichier plus petit est toujours plus rapide ou aussi performant |

## 3. Le lien mathématique : prédire pour coder

Pour une séquence de tokens (x_1,\ldots,x_T), un modèle autorégressif factorise :

\[
p(x_{1:T})=\prod_{t=1}^{T}p(x_t\mid x_{<t}).
\]

Le surprisal du token (x_t), en bits, est :

\[
I(x_t\mid x_{<t})=-\log_2 p(x_t\mid x_{<t}).
\]

La longueur de code idéale cumulée est donc approximativement :

\[
L(x_{1:T})\approx-\sum_{t=1}^{T}\log_2 p(x_t\mid x_{<t}).
\]

Un codeur arithmétique ou un autre codeur entropique adapté peut exploiter ces probabilités pour encoder la séquence. Un modèle qui attribue de bonnes probabilités aux tokens observés peut donc permettre une longueur de code moyenne plus courte.

**Mais il faut un véritable protocole de codage.** L'encodeur et le décodeur doivent partager le même modèle, le même tokenizer, la même précision numérique et les mêmes conventions de calcul ; le décodeur doit pouvoir reconstruire exactement les symboles. Une simple génération à partir d'un prompt n'est pas un décodage sans perte du corpus d'entraînement.

La cross-entropy moyenne (avec logarithme naturel, en nats, ou en base 2, en bits) mesure la qualité probabiliste moyenne. Elle ne prouve pas que les poids stockent littéralement les exemples d'entraînement.

## 4. Le lien — et la différence — avec la compression du modèle

La compression du modèle modifie le coût de représentation ou d'utilisation du modèle probabiliste :

- **Quantification :** réduire le nombre de bits utilisés pour représenter les poids (et parfois les activations). Le modèle résultant approxime le modèle initial ; les probabilités peuvent changer.
- **Pruning :** retirer des poids ou structures. La fonction calculée peut être modifiée ; la sparsité ne donne un gain matériel que si le format et les kernels l'exploitent.
- **Distillation :** entraîner un modèle étudiant qui reproduit certains comportements du professeur. Il s'agit d'un transfert approximatif, pas d'une copie exacte de la distribution du professeur.

Ces transformations peuvent dégrader ou modifier les probabilités du modèle. Si le modèle compressé sert ensuite de modèle de codage, son efficacité de compression doit être mesurée à nouveau, par exemple en bits par token et en taux de reconstruction exact.

Inversement, un modèle plus petit peut coûter moins cher à déployer sans être un meilleur codeur des données. Une bonne compression des poids ne garantit donc pas une bonne compression prédictive.

## 5. Troisième notion à distinguer : la mémoire d'exécution

Le cache KV, les buffers d'activations, les états de génération et les caches de préfixes concernent la mémoire temporaire et le débit du système pendant l'inférence.

Ils ne sont ni le corpus compressé, ni nécessairement le checkpoint compressé. Quantifier le cache KV peut réduire la mémoire de travail pour les longs contextes, sans réduire directement le fichier de poids.

Il faut donc suivre trois budgets distincts :

1. **Stockage persistant :** taille du checkpoint.
2. **Mémoire d'exécution :** poids chargés, KV cache, activations et buffers.
3. **Codage des données :** longueur en bits nécessaire pour représenter une séquence avec un codeur donné.

La latence et le débit sont des mesures supplémentaires : ils ne se déduisent pas directement d'un seul de ces budgets.

## 6. Comment les deux articles se complètent

### Apport de Shashidhar
Il propose une intuition sur les régularités : les continuations familières ou composées de motifs appris sont souvent mieux prédites. C'est une bonne porte d'entrée vers les probabilités conditionnelles, le surprisal, la cross-entropy et la généralisation. Son rapprochement avec LZW reste une analogie, pas une identité algorithmique.

### Apport de Cota
Elle décrit des méthodes d'ingénierie qui rendent le modèle moins coûteux : élagage, quantification et distillation. Son billet est une taxonomie introductive utile, mais plusieurs chiffres de taille et de vitesse dépendent du matériel, des kernels et du protocole. Le KV cache doit être traité comme mémoire d'exécution, et non comme poids du modèle.

### Synthèse
Shashidhar parle principalement de **ce que le modèle a appris à prédire et de la façon dont cette prédictibilité peut être exploitée pour coder des données**. Cota parle de **la façon de rendre le modèle lui-même moins cher à stocker ou exécuter**.

## 7. Expérience commune proposée

Construire une expérience contrôlée qui relie les deux niveaux sans les confondre :

1. Choisir un petit modèle causal de référence et un corpus de validation tenu à l'écart de l'entraînement.
2. Mesurer la NLL et les bits par token du modèle de référence.
3. Produire une variante quantifiée (par exemple poids-only INT8 puis INT4) et, si les outils le permettent, une variante élaguée ou distillée.
4. Pour chaque variante, mesurer la taille du checkpoint, le pic mémoire, la latence de préremplissage et de génération, le débit et la NLL sur exactement les mêmes séquences.
5. Optionnel : encoder puis décoder exactement les séquences avec un codeur entropique utilisant les probabilités du modèle ; vérifier l'égalité bit à bit des séquences décodées.

Tableau de résultats à remplir :

| Variante | Checkpoint (Mo) | Pic mémoire (Mo) | Latence (ms/token) | Débit (tokens/s) | NLL (nats/token) | Bits/token | Décodage exact |
|---|---:|---:|---:|---:|---:|---:|---|
| Référence | À mesurer | À mesurer | À mesurer | À mesurer | À mesurer | À mesurer | À vérifier |
| Quantifiée INT8 | À mesurer | À mesurer | À mesurer | À mesurer | À mesurer | À mesurer | À vérifier |
| Quantifiée INT4 | À mesurer | À mesurer | À mesurer | À mesurer | À mesurer | À mesurer | À vérifier |
| Élaguée / distillée | À mesurer | À mesurer | À mesurer | À mesurer | À mesurer | À mesurer | À vérifier |

Contrôler matériel, versions, backend, tokenizer, corpus, batch, longueur de contexte et paramètres de génération. Les cellules « à mesurer » ne sont pas des résultats et ne doivent pas être remplacées par des estimations issues d'autres matériels.

## 8. Placement dans LLM Lab

| Ressource | Rôle éditorial | Destination |
|---|---|---|
| Shashidhar | Intuition de compression prédictive et lien avec la théorie de l'information | Probabilités, entropie, vraisemblance, cross-entropy, généralisation |
| Cota | Panorama des techniques de compression du modèle | Complexité computationnelle, efficacité d'inférence, évolution des modèles |
| Cette comparaison | Distinguer les sens du mot et relier les métriques | Fiche transversale optionnelle ; pas une nouvelle étape obligatoire du parcours |

Ne pas créer une nouvelle page canonique ou un concept de registre uniquement pour accueillir ces deux billets. Réutiliser les pages et exercices existants. Coordonner la quantification avec l'issue [#266](https://github.com/JM-Brun/llm-lab/issues/266), et le volet expérimental prédictif avec [#1058](https://github.com/JM-Brun/llm-lab/issues/1058), après vérification de leurs états courants.

## 9. Conclusion à mémoriser

**Compression prédictive :** un modèle probabiliste apprend à attribuer des probabilités aux séquences ; ces probabilités peuvent permettre de coder les données plus efficacement.

**Compression du modèle :** on réduit le coût de stockage ou d'exécution du modèle par quantification, pruning ou distillation.

**Mémoire d'exécution :** on optimise les états et buffers temporaires utilisés pendant la génération.

Ces trois notions interagissent, mais ne sont pas interchangeables. Pour comparer des modèles compressés, il faut mesurer à la fois leur coût matériel et la qualité de leur distribution prédictive ; pour parler de compression de données sans perte, il faut en plus démontrer un encodage/décodage exact.

## Références

- Shashidhar (2024), [LLMs and compression algorithms](https://artofdatascience.substack.com/p/llms-and-compression-algorithms).
- Cota (2023), [Understanding Compression of Large Language Models](https://medium.com/@sasirekharameshkumar/understanding-compression-of-large-language-models-2ee3b8a350a2).
- SparseGPT, [Frantar & Alistarh (2023)](https://proceedings.mlr.press/v202/frantar23a.html).
- SmoothQuant, [Xiao et al. (2023)](https://proceedings.mlr.press/v202/xiao23c.html).
- DistilBERT, [Sanh et al. (2019)](https://arxiv.org/abs/1910.01108).


## 10. Audit de clarté et intégration pédagogique dans LLM Lab

L'audit des pages existantes confirme que les notions de probabilité conditionnelle, entropie, surprise du token observé et entropie croisée étaient déjà expliquées dans les leçons canoniques. Le manque était le passage explicite entre ces notions et un protocole de codage sans perte, ainsi que la comparaison directe avec la compression du réseau.

Intégrations réalisées sur cette branche :
- La leçon bilingue sur l'entropie contient maintenant une section **« Les LLM sont-ils des algorithmes de compression ? » / “Are LLMs compression algorithms?”** qui explique le lien prédiction → surprisal en bits → longueur de code idéale → codeur/décodeur, puis les limites de l'analogie.
- La leçon bilingue sur l'évolution des LLM distingue maintenant compression prédictive, compression du modèle (quantification, pruning, distillation) et mémoire d'exécution (KV cache/activations).
- L'expérience predictive-compression entraîne un petit modèle bigramme sur un alphabet synthétique, construit un intervalle de codage arithmétique exact, encode une séquence, puis vérifie son décodage exact. Elle ne prétend pas mesurer un LLM ni la compression du langage naturel.

Exécution vérifiée avec Python standard : coût idéal 19,642 bits, code fini 21 bits, référence uniforme 40 bits, reconstruction exacte. Cette expérience illustre le mécanisme ; elle ne démontre pas un gain net après coût de transmission du modèle, tokenizer et métadonnées.

Les résultats CI de la PR doivent encore confirmer le rendu Quarto et les liens de ces ajouts ; aucun test utilisateur ou contrôle visuel indépendant n'est revendiqué ici.
