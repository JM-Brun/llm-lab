# Audit de fond du parcours Comprendre

Audit des 20 leçons centrales et de leurs fiches FR/EN sur la branche de la PR [#1443](https://github.com/JM-Brun/llm-lab/pull/1443), à partir de l’état `3b780309`. Comparaison de l’ouverture, du plan des sections, de l’exemple principal, des exercices et de la suite proposée. Le [plan destiné aux lecteurs](../../site/fr/review-path.qmd) reprend les métadonnées des leçons et les dépendances de [guided-route.yml](../../data/guided-route.yml).

## Verdict

Le calcul commun reste lisible lorsque chaque leçon transmet un objet identifiable à la suivante, des IDs aux plongements et à la position, puis aux états des blocs, aux logits et à la distribution. Les ruptures viennent surtout de la confusion entre ordre de lecture et ordre du calcul, entre pénalité locale et objectif d’un lot, puis entre usages de la prédiction et étapes d’une exécution. Une réorganisation ciblée traite ces ruptures au sein des pages canoniques.

- **Orientation.** La carte et la sidebar demandaient de lire le cours complet de génération après le panorama, puis la carte le proposait à nouveau après les probabilités. Les deux premiers tours de l’exemple suffisent à l’orientation. Le panorama les contient. La leçon de génération est désormais rattachée à l’inférence.
- **Représentations.** Comparer un plongement initial à un état contextualisé avant d’étudier les blocs est un choix de lecture. Dans l’exécution, les projections Q/K/V et l’attention se calculent dans les blocs qui produisent ces états. L’ouverture de la leçon et l’objectif d’étape explicitent cette différence.
- **Sortie et usages.** La distribution sert à choisir le prochain token, à lire la probabilité d’une cible observée ou à ajuster les paramètres. Le contexte appliqué prolonge la première branche. Le plan donne un accès direct à chaque usage, tandis que les cartes successives proposent un ordre de lecture.
- **Pénalité et objectif.** Le résumé et le schéma d’entropie croisée se terminaient sur la moyenne du lot, qui est déjà la responsabilité de la page Perte. Le schéma part désormais des distributions cible et prédite et aboutit à la pénalité locale. Les masques et réductions restent traités sur Perte. Les développements de la première leçon à leur sujet, les exemples de bibliothèque et la perplexité restent accessibles dans son application repliée.
- **Profondeur.** La latence du serveur et la compression prédictive sont des applications. Elles enrichissent la génération et l’entropie, respectivement. Leur place dans la première lecture est explicite et leur contenu détaillé reste accessible sur les pages concernées.

## Contrôle des frontières par leçon

| Leçon | Ce qu’elle apporte et où s’arrête sa responsabilité | Repère vérifié |
|---|---|---|
| [Panorama](../../site/fr/llm-overview.qmd) | Situe une prédiction et donne une première expérience de la boucle à paramètres fixes. | Question du scribe, deux contextes successifs, puis trois usages de la distribution. |
| [Texte et tokens](../../site/fr/text-data.qmd) | Va jusqu’aux IDs. Le passage au vecteur annonce la leçon suivante. | Le tableau texte/tokens/IDs/plongements distingue les objets. L’encodage et la préparation de corpus sont reliés mais distincts. |
| [Plongements](../../site/fr/embedding-space.qmd) | Fait le lookup d’un ID dans une matrice. | La table sépare l’adresse entière, la ligne et les coordonnées du vecteur. |
| [Position](../../site/fr/positional-encoding.qmd) | Localise le signal d’ordre en entrée ou dans la comparaison en attention. | L’exemple de permutation donne une raison d’introduire la position. Le détail des rotations dispose de sa propre page. |
| [États contextualisés](../../site/fr/contextualized-representations.qmd) | Compare une identité de token à deux états d’occurrences. | L’exemple suppose explicitement un ID commun. La transformation qui produit les états est étudiée dans les blocs. |
| [Transformer](../../site/fr/transformer.qmd) | Situe la passe avant, les sous-couches, le bloc, la pile et la tête. | Le trajet des états d’entrée aux logits sert de carte aux leçons sur les mécanismes internes. |
| [Q/K/V](../../site/fr/queries-keys-values.qmd) | Attribue une fonction à chaque projection issue de l’état du bloc. | Les rôles Q/K se vérifient par les poids et le rôle de V par le contenu agrégé. |
| [Attention](../../site/fr/scaled-dot-product-attention.qmd) | Calcule une ligne, des produits scalaires à la moyenne pondérée des V. | Le découpage en cinq opérations expose l’emplacement de la mise à l’échelle et du masque. |
| [Masque causal](../../site/fr/causal-masking.qmd) | Identifie les clés accessibles et le prochain token prédit. | La diagonale, l’interdiction des positions futures et le masque de perte jouent des rôles séparés. |
| [Logits](../../site/fr/logits.qmd) | Projette un état en scores indexés par le vocabulaire. | L’exemple des quatre candidats sépare dimension cachée et taille du vocabulaire. |
| [Probabilités](../../site/fr/probabilites.qmd) | Produit et interprète une distribution pour un contexte. | L’exploration de la température dépend des logits. Le choix effectif du token est développé dans la génération. |
| [Entropie](../../site/fr/entropy.qmd) | Mesure l’incertitude avant observation. | La distribution du scribe sépare la moyenne de la pénalité d’une issue. Compression et V-information restent accessibles en approfondissement. |
| [Génération](../../site/fr/generation.qmd) | Déroule la sélection, la réinjection et l’arrêt à paramètres fixes. | Les trois tours complets et la distinction prefill/decode portent l’objectif. Le cache et le serving expliquent l’efficacité. |
| [Apprentissage en contexte](../../site/fr/in-context-learning.qmd) | Explique le changement de comportement à partir d’exemples dans le prompt. | Zero-, one- et few-shot distinguent la quantité d’exemples fournis. |
| [Ingénierie du contexte](../../site/fr/context-engineering.qmd) | Porte sur les choix du système qui fournit le contexte. | L’exemple de conception rend visibles la sélection, le format et le budget. Le scoring relève d’une autre branche. |
| [Vraisemblance](../../site/fr/vraisemblance.qmd) | Score une suite déjà observée, avec un produit de probabilités puis une somme de logarithmes. | Les trois probabilités du scribe donnent une NLL de séquence, qui change d’échelle quand on moyenne. |
| [Entropie croisée](../../site/fr/cross-entropy.qmd) | Calcule une pénalité à une position, puis retrouve la NLL dans le cas one-hot. | L’exemple à deux distributions montre le cas général. L’axe du vocabulaire, les API et la réduction restent dans l’application. |
| [Perte](../../site/fr/loss.qmd) | Agrège sur les positions valides avec une convention de réduction. | Les pertes locales du même exemple mènent au scalaire du lot. Le choix du masque et du dénominateur relève de cette leçon. |
| [Gradients](../../site/fr/gradients.qmd) | Propage une sensibilité vers les paramètres et l’utilise pour un pas simple. | La chaîne perte–logits–paramètres sépare dérivée et règle de mise à jour. |
| [Boucle d’entraînement](../../site/fr/training-loop.qmd) | Organise les opérations d’une itération répétée et distingue optimisation et suivi de validation. | Les courbes et la validation sur données réservées concluent le parcours. |

## Suivi du parcours au niveau d’une position

Le cas `[A, X, U]` / `[B, X, U]` / `[A, X, V]` est conservé sur la [page d’exercices sur les états contextualisés](../../site/fr/exercises/contextualized-representations.qmd#ex-contextualization-causal-boundary). Il sert désormais de liaison entre les états, le masque causal et les logits. Dans le GPT causal, changer la troisième position peut changer la cible observée à la deuxième position. Le préfixe accessible à cette position, son état caché et sa ligne de logits restent les mêmes dans ce cas. Le corrigé poursuit le calcul jusqu’à la pénalité locale en lisant deux colonnes de la même distribution.

La [leçon Q/K/V](../../site/fr/queries-keys-values.qmd#pourquoi-trois-projections-à-partir-de-la-même-entrée) distingue l’entrée du bloc, conservée sur le chemin résiduel, de l’entrée normalisée des projections dans le GPT pré-LN de référence. La [leçon Transformer](../../site/fr/transformer.qmd) présente l’ajout des plongements de position comme le choix de ce GPT et indique où RoPE intervient.

Le prochain point à observer chez un lecteur est sa capacité à identifier la ligne de logits et la cible sans reformuler la question à sa place. Ce point complète le [pilote auprès d’un apprenant](../learner-validation-pilot.md).

## Critère pour les prochaines révisions

L’objectif visible de chaque leçon et la vue du plan proviennent du même champ `purpose`. Pour modifier le fond, partir d’un écart mesurable entre cet objectif, l’exemple travaillé et le rappel dans la fiche. Pour changer l’ordre, contrôler quel acquis est effectivement utilisé, indépendamment de la page proposée ensuite. Les contrôles de génération vérifient les références et l’ordre des dépendances déclarées. La pertinence de ces dépendances et le transfert à un exemple inédit restent à observer auprès de lecteurs.

Deux décisions pourront être réexaminées à partir de ces observations. La leçon sur les états contextualisés mérite sa place si elle aide à lire le premier bloc sans confondre états initiaux et finaux. L’ingénierie du contexte mérite sa place dans le cours complet si la compréhension du système applicatif fait partie du résultat attendu. Une version courte centrée sur le calcul pourra sauter à la branche de scoring ou d’entraînement depuis le plan.
