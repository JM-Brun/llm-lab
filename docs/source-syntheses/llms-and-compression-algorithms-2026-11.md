# LLMs and compression algorithms — synthèse critique

**Source :** Karthik Shashidhar, “LLMs and compression algorithms”, 27 août 2024.  
**URL :** https://artofdatascience.substack.com/p/llms-and-compression-algorithms  
**Langue :** anglais. **Type :** billet de vulgarisation / opinion.  
**Scan :** corps de l'article récupéré ; discussion visible partiellement inspectée.  
**Réutilisation :** lien et reformulation seulement ; aucune licence de republication établie.

## 1. Question d'apprentissage

Pourquoi un modèle de langage peut-il produire une réponse ou un programme long à partir d'une instruction courte, et pourquoi cette capacité varie-t-elle selon la fréquence et la spécificité du domaine ?

**Position pédagogique :** utiliser la compression comme intuition introductive pour expliquer l'apprentissage de régularités et la prédiction du prochain token, en la reliant à la théorie de l'information, à l'entropie conditionnelle et à la généralisation. Ne pas présenter « le LLM est un algorithme de compression » comme une identité technique.

## 2. Résumé fidèle

L'auteur part de Lempel–Ziv–Welch (LZW), qui détecte des séquences répétées et leur associe des codes plus courts. Il propose ensuite une analogie : les paramètres d'un LLM condensent les régularités statistiques de grands corpus ; le modèle peut alors restituer certaines régularités à partir d'un prompt bref.

Il relie cette intuition à trois observations :
1. Les domaines abondamment représentés dans les données d'entraînement sont souvent mieux modélisés.
2. Les assistants de code réussissent davantage sur les motifs courants (par exemple les applications web usuelles) que sur des langages, bibliothèques ou tâches rares.
3. Une instruction courte peut suffire lorsque la tâche correspond à des motifs largement réutilisés ; les tâches atypiques ou fortement contraintes demandent davantage de spécification et de vérification.

L'auteur conclut que savoir programmer reste important pour détecter les erreurs et traiter les problèmes que le modèle ne sait pas reconstruire de manière fiable.

## 3. Carte des contributions

| Élément | Contribution | Nature / force |
|---|---|---|
| Analogie LZW ↔ LLM | Point d'entrée intuitif vers la compression de régularités | Analogie pédagogique, pas démonstration mécaniste |
| Densité des exemples | Relie fréquence des motifs et facilité de prédiction | Hypothèse plausible, non mesurée dans l'article |
| Code courant vs niche | Rend concrète la dépendance au domaine et à la distribution | Observation anecdotique de l'auteur |
| Prompt court → code long | Illustre la réutilisation de motifs appris | Intuition utile, simplifie contexte, outils et inférence |
| Apprendre à programmer | Insiste sur vérification et traitement du non-standard | Conclusion pédagogique pertinente |

## 4. À conserver et à nuancer

### À conserver
- Les modèles apprennent des régularités statistiques à partir de données.
- La fréquence, la qualité, la diversité et la représentativité des exemples influencent les performances, sans les déterminer seules.
- Une tâche familière peut être complétée à partir d'un contexte succinct parce que le modèle a appris des régularités transférables.
- Les tâches rares, ambiguës, nouvelles ou fortement contraintes exposent davantage les limites de généralisation.
- La compétence humaine consiste aussi à spécifier, tester, diagnostiquer et valider les sorties.

### Nuances indispensables
1. **Compression n'est pas stockage réversible.** Les poids ne constituent ni une archive textuelle du corpus, ni un dictionnaire LZW consultable. L'apprentissage ajuste une fonction paramétrique qui approxime des distributions conditionnelles sur les séquences.
2. **LZW et un LLM n'ont pas le même objectif.** LZW est un algorithme de compression sans perte avec dictionnaire adaptatif explicite ; un LLM est généralement entraîné par prédiction de tokens et ne reconstruit pas le corpus d'entraînement.
3. **La taille du modèle ne se résume pas à des “bits de niche”.** La relation entre paramètres, capacité, données, calcul, architecture et performances est complexe. L'affirmation de l'article comparant Llama 3.1 70B et 405B est une intuition non étayée ici, pas une conclusion générale.
4. **Rareté n'implique pas automatiquement échec.** Compositionnalité, transfert, raisonnement, outils, récupération documentaire, post-entraînement et données synthétiques peuvent améliorer les performances sur des tâches peu fréquentes.
5. **La fréquence n'est pas une mesure directe de difficulté.** Une tâche fréquente peut rester difficile ; une tâche rare peut être résolue par transfert depuis des structures proches.
6. **“Information content” doit être défini.** Surprisal, entropie conditionnelle, longueur de description et complexité algorithmique sont des notions distinctes.

## 5. Ancrage théorique recommandé

Pour rendre l'intuition rigoureuse, relier cette source à :
- **Prédiction autorégressive :** (p(x_t \mid x_{<t})), distribution du prochain token conditionnée par le contexte.
- **Surprisal :** (-\log p(x_t \mid x_{<t})), information associée à un token dans un contexte donné.
- **Entropie conditionnelle :** incertitude moyenne restante sur le prochain token sachant le contexte.
- **Cross-entropy / negative log-likelihood :** objectif d'entraînement usuel qui pénalise les prédictions attribuant une faible probabilité aux tokens observés.
- **Compression prédictive :** un modèle probabiliste performant permet un codage plus court en moyenne si l'on code selon les probabilités qu'il attribue ; ce lien formel est différent de l'idée que les poids seraient une archive compressée.
- **Généralisation et distribution :** distinguer interpolation dans des régions bien représentées, transfert vers des combinaisons nouvelles et extrapolation hors distribution.

Formulation sûre : *un modèle de langage apprend une représentation paramétrique des régularités qui rendent les séquences prévisibles ; cette modélisation peut être interprétée comme une forme de compression statistique ou prédictive.*

## 6. Décision d'intégration dans LLM Lab

**Décision : intégrer comme intuition complémentaire et point de départ d'une expérience, pas comme source de référence scientifique.**

| Destination | Décision | Justification |
|---|---|---|
| Tokenisation et prédiction du prochain token | Lien transversal | Prépare le passage des séquences à leur modélisation probabiliste |
| Entraînement et fonction de perte | Perspective complémentaire | Introduit NLL, cross-entropy et surprisal |
| Généralisation / limites | Exemple introductif | Motive fréquence, transfert et décalage de distribution |
| Fiche de révision | Encadré « intuition et limites » | Mémorisation facile si les garde-fous restent visibles |
| LZW | Mini-comparaison optionnelle | Distingue compression sans perte et modélisation probabiliste |
| Affirmation sur 70B vs 405B | Ne pas intégrer comme fait | Non démontrée par l'article |

## 7. Activité reproductible proposée

Construire un petit corpus avec deux familles de motifs (fréquents et rares), puis comparer un modèle n-gramme ou un petit Transformer sur :
1. des exemples fréquents ;
2. des exemples rares mais interpolatifs ;
3. des exemples réellement hors distribution.

Mesurer la cross-entropy moyenne, puis tester l'effet de l'ajout de données représentatives et celui de la recombinaison de motifs connus dans une structure nouvelle. Contrôler taille du corpus, nombre de paramètres, étapes d'entraînement et difficulté. Rapporter les distributions et l'incertitude ; ne pas confondre rareté, nouveauté structurelle et difficulté intrinsèque.

**Question de réflexion :** une séquence rare mais composée de motifs connus est-elle aussi difficile à prédire qu'une séquence fréquente contenant une relation nouvelle ?

## 8. Limites de la source

- Billet court de vulgarisation, non évalué par les pairs.
- Aucun protocole expérimental, jeu de données, métrique ou référence quantitative permettant de tester les affirmations.
- L'expérience de l'auteur en programmation R et assistants de code constitue un témoignage, pas une comparaison contrôlée.
- Les commentaires visibles évoquent le rôle possible du reinforcement learning et des données spécialisées, sans apporter de preuve permettant de trancher.
- L'article ne distingue pas systématiquement fréquence des exemples, difficulté, transfert et incertitude du modèle.

## 9. Synthèse opérationnelle

**À retenir :** les LLM sont meilleurs lorsqu'ils ont appris des régularités pertinentes et transférables ; leur modélisation peut être comprise comme une compression statistique. Les prompts courts fonctionnent souvent parce qu'ils activent des structures déjà apprises.

**À ne pas conclure :** qu'un LLM est littéralement LZW, qu'il archive le web dans ses poids, que la fréquence suffit à expliquer ses performances, ou que les tâches rares sont nécessairement impossibles.

**Valeur pour le parcours :** élevée comme accroche intuitive ; moyenne comme explication autonome ; faible comme preuve empirique. La leçon doit prolonger l'analogie par la probabilité conditionnelle, la cross-entropy, l'entropie et des expériences de généralisation.

## 10. Raccordement au parcours canonique existant

L'article doit servir de **pont interprétatif**, pas de nouvelle leçon autonome. Les pages existantes couvrent déjà les définitions mathématiques nécessaires :

| Étape du raisonnement | Ressource canonique FR | Ressource canonique EN | Rôle de l'article |
|---|---|---|---|
| Une continuation est une distribution conditionnelle | [Probabilités de sortie](../../site/fr/probabilites.qmd) | [Output probabilities](../../site/en/probabilities.qmd) | Introduire l'idée qu'un modèle apprend des régularités utiles à la prédiction du prochain token |
| L'incertitude moyenne dépend de la distribution | [Entropie](../../site/fr/entropy.qmd) | [Entropy](../../site/en/entropy.qmd) | Distinguer l'intuition de compression de la mesure formelle d'entropie |
| La surprise dépend du token observé | [Vraisemblance](../../site/fr/vraisemblance.qmd) | [Likelihood](../../site/en/likelihood.qmd) | Relier une faible probabilité attribuée à une continuation à une longueur de code prédictive plus élevée |
| L'écart entre cible et prédiction produit une pénalité | [Entropie croisée](../../site/fr/cross-entropy.qmd) | [Cross-entropy](../../site/en/cross-entropy.qmd) | Faire le lien formel le plus direct entre prédiction probabiliste, NLL et codage arithmétique idéal |
| L'objectif est optimisé sur des données et évalué sur d'autres | [Boucle d'entraînement](../../site/fr/training-loop.qmd) | [Training loop](../../site/en/training-loop.qmd) | Introduire la question de la généralisation, des données représentatives et du décalage de distribution |

**Précaution sur le codage :** pour un événement de probabilité $p$, le coût idéal associé est $-\log_2 p$ bits. En revanche, la loss usuelle exprimée avec le logarithme naturel est en nats. La cross-entropy moyenne correspond à une longueur de code idéale moyenne seulement sous les hypothèses du codage probabiliste approprié ; elle ne signifie pas que les poids du modèle sont eux-mêmes un fichier compressé du corpus.

### Décision éditoriale

- Ne pas ajouter une deuxième explication de l'entropie ou du surprisal : ces distinctions sont déjà explicites dans les leçons canoniques et leurs exercices.
- Ne pas ajouter de contenu à la page Understand sur « les LLM compressent Internet ».
- Utiliser cette source dans une fiche de synthèse transversale ou un encadré optionnel qui relie probabilités, longueur de code et généralisation.
- Pour une expérience, réutiliser l'issue [#1058](https://github.com/JM-Brun/llm-lab/issues/1058) comme point de coordination : elle conserve déjà le volet non résolu d'un calcul token-level sur un vrai modèle. Ne pas recopier les prototypes jouets rejetés ni créer un doublon de cette activité.
- La proposition d'expérience du §7 reste un protocole de recherche pédagogique à construire et à contrôler, pas un résultat déjà obtenu.

## Référence

Karthik Shashidhar (2024), [LLMs and compression algorithms](https://artofdatascience.substack.com/p/llms-and-compression-algorithms), *Art of Data Science*, 27 août 2024. Consulté le 16 novembre 2026.
