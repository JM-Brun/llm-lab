# Pré-entraînement, perplexité et progrès mesuré — Raschka et OpenAI

**Sources principales**
- Sebastian Raschka, [Pre-training is (still) not plateauing](https://sebastianraschka.com/blog/2026/pretraining-is-still-not-plateauing.html), 22 novembre 2026. [Post LinkedIn fourni](https://www.linkedin.com/posts/sebastianraschka_pre-training-is-still-not-plateauing-finally-share-7530419578179502080-e0tU/).
- Jakub Pachocki / OpenAI, [Perplexity and Intelligence](https://openai.com/index/perplexity-and-intelligence/), 22 novembre 2026.

**Inspection (24 novembre 2026).** Le texte de Raschka a été récupéré intégralement dans le résultat public indexé ; la page canonique renvoie un cache miss. L'article OpenAI a été lu directement, y compris ses cinq notes. Les deux graphiques/visuels n'ont pas été récupérés comme fichiers image ni inspectés visuellement. Aucun chiffre n'a donc été retranscrit depuis les courbes. Aucun jeu de données ni code d'évaluation n'a été fourni ou exécuté. Réutilisation : liens et reformulation uniquement ; droits des textes et figures non établis.

## 1. Ce que dit Raschka

Raschka conteste l'idée que le pré-entraînement aurait atteint un plateau. Il s'appuie sur la courbe publiée par OpenAI, qui présente l'évolution de la log-perplexité de modèles de base successifs. Son point essentiel est que le travail de pré-entraînement reste un déterminant important des progrès, même lorsque l'attention médiatique se porte davantage sur le RLVR et les systèmes agentiques.

Il propose une distinction en trois rôles :

1. **Pré-entraînement :** établir le socle de connaissances et de régularités apprises par prédiction du prochain token.
2. **Post-entraînement :** aider le modèle à accéder à ces capacités, notamment par SFT et RLVR.
3. **Harness :** fournir le contexte, les outils et l'orchestration permettant au système d'appliquer ces capacités.

Cette grille est un modèle mental utile, pas une taxonomie formelle. En particulier, « connaissances » ne signifie pas une base de faits explicitement stockée ; il s'agit de régularités et de capacités encodées dans les paramètres. Les phases peuvent se chevaucher et les méthodes réelles sont plus diverses.

Raschka souligne que la courbe mesure la prédiction du prochain token, pas la réussite directe à une tâche. Il explique la métrique par une phrase : à chaque position, le modèle reçoit le préfixe et attribue une probabilité au token suivant observé ; on calcule le logarithme négatif de cette probabilité puis on moyenne sur les positions.

Enfin, il souhaiterait voir la même courbe en fonction des FLOPs d'entraînement. Il suggère que des choix de mélange de données, comme la quantité de code, peuvent aussi contribuer aux progrès. Il ne quantifie ni l'effet des FLOPs ni celui du mélange de données : ce sont des questions de recherche, pas des résultats expérimentaux fournis dans la note.

## 2. Ce que précise la source primaire d'OpenAI

L'article de Jakub Pachocki décrit la perplexité comme une mesure de la qualité moyenne de prédiction du prochain token. OpenAI indique suivre une série sur un jeu de données interne de code, conservé sous un snapshot fixe. Le texte explique que la log-perplexité est suivie en pratique sous la forme de la cross-entropy moyenne.

Pour une séquence évaluée (x_{1:T}), avec une convention de logarithme naturel :

[
operatorname{CE}_{mathrm{eval}}
= -rac{1}{T}sum_{t=1}^{T}
log p_	heta(x_tmid x_{<t}),
qquad
operatorname{PPL} = exp(operatorname{CE}_{mathrm{eval}}).
]

Ainsi, (log(operatorname{PPL})=operatorname{CE}_{mathrm{eval}}). Avec des logarithmes en base 2, la perplexité correspondante est (2^{operatorname{CE}_{2}}). Il faut donc toujours préciser la base du logarithme et la convention utilisée.

Une valeur plus faible signifie que le modèle attribue en moyenne une probabilité plus élevée aux tokens effectivement observés dans le corpus d'évaluation. Elle ne signifie pas, à elle seule, qu'il résout mieux toutes les tâches.

OpenAI mentionne plusieurs jalons historiques associés à des niveaux de log-perplexité, mais précise que ces seuils de capacités n'étaient pas prévisibles a priori. L'article ne démontre donc pas une loi universelle transformant une valeur de loss en une capacité donnée.

## 3. Ce que la métrique mesure — et ce qu'elle ne mesure pas

| Question | Ce que la perplexité permet de dire | Limite à conserver |
|---|---|---|
| Prédiction du prochain token | Qualité moyenne des probabilités attribuées aux tokens observés | Dépend du corpus, de la tokenisation et du protocole |
| Progrès longitudinal | Comparaison de versions sur un jeu de données fixe et une procédure stable | Ne garantit pas la comparabilité entre laboratoires |
| Capacités aval | Peut être un indicateur informatif de progrès du modèle de base | N'est pas un score de réussite à une tâche |
| Raisonnement et post-entraînement | Ne mesure pas directement les améliorations qui ne réduisent pas la NLL de pré-entraînement | Le CoT peut augmenter la performance aval sans réduire cette métrique |
| Limite informationnelle | La loss ne peut pas être interprétée comme devant tendre vers zéro | L'entropie intrinsèque du corpus et le plancher atteignable sont inconnus |

OpenAI explicite quatre difficultés :

- **Comparaison entre laboratoires :** jeux de données et mélanges d'entraînement différents.
- **Distance aux tâches :** la perplexité n'est pas une mesure directe de réussite sur une tâche utile.
- **Couverture partielle :** elle ne capture pas les gains provenant d'autres phases, notamment du raisonnement en chaîne ou du post-entraînement.
- **Plancher inconnu :** l'entropie intrinsèque des données n'est pas connue ; la progression apparente peut ralentir à mesure que le modèle s'en approche.

Le jeu d'évaluation mentionné est un corpus interne de code. La note d'OpenAI rappelle que le code est un proxy imparfait des capacités générales, en particulier pour les anciens modèles. La série est donc informative sur cette tâche de prédiction, mais ne constitue pas un classement universel de l'intelligence.

## 4. Comparaison avec LLM Lab

### Connaissances déjà couvertes

- La page [Entropie croisée](../../site/fr/cross-entropy.qmd) formalise déjà la pénalité par token et la relation avec la NLL.
- La page [Boucle d'entraînement](../../site/fr/training-loop.qmd) distingue l'ajustement sur les données d'entraînement et la mesure sur validation.
- La page [Post-entraînement](../../site/fr/post-training.qmd) sépare les mises à jour de paramètres et les modifications du contexte.
- Les ressources sur les lois d'échelle couvrent déjà les tendances empiriques et les variables d'échelle.

### Apport complémentaire

La contribution n'est pas une nouvelle définition de la cross-entropy. Elle rend visible le passage entre trois niveaux souvent séparés :

1. **Position/token :** (-log p_	heta(x_tmid x_{<t})).
2. **Corpus d'évaluation :** moyenne de ces pénalités, soit la cross-entropy empirique.
3. **Indicateur agrégé :** exponentielle de la cross-entropy (perplexité), ou log-perplexité selon la convention.

Le cas OpenAI fournit un exemple contemporain de suivi longitudinal d'un modèle de base et une bonne occasion d'enseigner les limites de validité d'une métrique.

### Décisions d'intégration

| Élément | Décision | Justification |
|---|---|---|
| Définition token-level de la cross-entropy | Déjà couvert | Ne pas dupliquer la leçon |
| Perplexité comme agrégation de NLL | À relier à la page cross-entropy | Extension naturelle de la métrique existante |
| Jeu tenu à l'écart et comparaison longitudinale | À relier à training-loop / évaluation | Clarifie le rôle de l'évaluation sans mise à jour |
| Trois rôles pré-entraînement / post-entraînement / harness | Référence complémentaire | Bonne synthèse conceptuelle, déjà couverte par morceaux |
| FLOPs et mélange de données | Question ouverte | Aucune donnée ne permet une conclusion causale |
| Proposition de limites communes de développement | Approfondissement optionnel | Hors du parcours computationnel de base |

Aucune nouvelle notion canonique ni relation du graphe n'est justifiée par cette seule source. La formule de perplexité découle de la cross-entropy existante ; la transformer en concept indépendant ferait doublon. La route pédagogique n'a pas besoin d'une nouvelle étape.

## 5. Proposition d'expérience pédagogique

Une expérience locale peut reconstruire la métrique sans prétendre reproduire les résultats d'OpenAI :

1. Prendre un petit corpus de validation qui n'a pas servi à l'entraînement.
2. Calculer les log-probabilités du token suivant à chaque position valide.
3. Moyenner les NLL en indiquant explicitement la base du logarithme.
4. Calculer la perplexité par exponentiation (ou puissance de 2 en base 2).
5. Comparer deux checkpoints évalués sur le même corpus, avec la même tokenisation, les mêmes masques et le même protocole.
6. Vérifier que la loss de validation et la perplexité portent sur exactement les mêmes tokens.

Pour étudier les causes d'un progrès, il faudrait ensuite contrôler séparément le compute, le nombre de tokens, le mélange de données, l'architecture et la recette d'optimisation. Une simple comparaison de versions ne permet pas d'attribuer causalement le gain à l'une de ces variables.

## 6. Suites possibles

- Ajouter à la page cross-entropy une courte extension sur l'agrégation corpus et la perplexité, avec une mise en garde sur les conventions de logarithme.
- Relier cette extension à l'évaluation de validation dans la page training-loop.
- Construire un exercice où deux modèles sont comparés sur le même corpus et où l'apprenant distingue meilleure prédiction, meilleure performance aval et preuve causale.
- Ne pas recopier la figure OpenAI tant que l'asset original et ses droits ne sont pas vérifiés.

**Conclusion.** La publication ne démontre pas que toute capacité progresse au même rythme que la perplexité. Elle montre l'intérêt de suivre dans le temps la qualité de prédiction du prochain token, tout en rappelant qu'une métrique prédictive n'épuise ni les capacités aval ni les effets du post-entraînement et du système qui entoure le modèle.
