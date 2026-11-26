# Audit des redistributions du calendrier vers Approfondir

**Date :** 2026-11-26  
**Périmètre :** PR [#1695](https://github.com/JM-Brun/llm-lab/pull/1695), histoires des jours 1 à 3, pages complémentaires FR/EN, pages Practice et navigation Approfondir.

## Décision

La règle « redistribuer plutôt que supprimer » est globalement respectée pour les trois premières histoires. Les contenus retirés des récits ont été déplacés vers des pages complémentaires ou des pages Practice. L'audit a toutefois révélé un défaut d'intégration : les deux nouveaux approfondissements existaient, étaient rendus par Quarto et figuraient dans la navigation latérale, mais ils n'étaient pas correctement exposés depuis la carte éditoriale Approfondir. La page Zipf était en outre rangée dans la rubrique probabiliste, alors qu'elle traite d'abord des statistiques du langage.

La nouvelle rubrique **Modélisation du langage** dans la carte Approfondir et dans la navigation regroupe les domaines qui portent sur les modèles de langage. Elle contient des sous-rubriques thématiques ; ce n'est ni un nouveau parcours obligatoire ni une nouvelle valeur de domaine dans les métadonnées. Les domaines de page existants restent distincts et continuent à classer chaque page selon son objectif principal. **Outils mathématiques et géométrie** reste une rubrique sœur, car ces outils dépassent la seule modélisation du langage.

## Matrice de traçabilité

| Histoire | Contenu retiré ou déplacé | Destination vérifiée | État |
|---|---|---|---|
| Jour 1 — Zipf | Dérivation plus détaillée de Zipf–Mandelbrot, rapport de fréquences normalisé, effet de $\alpha$ et $\beta$, figure comparative et exemples numériques | `site/fr/zipf-law-deep-dive.qmd` et version EN | Déplacé ; lien depuis l'histoire et depuis Approfondir |
| Jour 1 — Zipf | Tableau d'observations multilingues, paramètres estimés, protocole de l'étude et précautions de comparaison | `zipf-law-deep-dive.qmd`, section « Observations multilingues » | Déplacé avec limites méthodologiques |
| Jour 1 — Zipf | Repères historiques Estoup, Zipf et Mandelbrot | `zipf-law-deep-dive.qmd`, section historique | Déplacé |
| Jour 1 — Zipf | Applications à l'analyse de corpus, à la recherche d'information, aux données d'entraînement et aux distributions de textes générés | `zipf-law-deep-dive.qmd`, section « À quoi sert-elle concrètement ? » | Déplacé ; les distinctions entre usage direct et lien indirect sont conservées |
| Jour 1 — Zipf | Bibliographie étendue et références empiriques | Sources en fin de `zipf-law-deep-dive.qmd` | Déplacé |
| Jour 2 — Surprisal | Manipulations de distributions synthétiques et vérifications pratiques | `site/fr/experience-information-theory.qmd` et version EN | Déplacé vers Practice, destination appropriée |
| Jour 2 — Surprisal | Explication contextuelle, calcul explicite d'entropie, logits → softmax → probabilité cible → surprisal, somme/moyenne de séquence et précautions sur les unités de tokenisation | Conservés et développés dans `surprisal-information-content.qmd` | Pas de perte : l'histoire a été enrichie plutôt qu'amputée |
| Jour 3 — Tokenizer | Cadre d'évaluation multidimensionnel, métriques, dénominateurs, fertilité, écarts entre langues, études comparatives, figures et ressources de recherche | `site/fr/tokenizer-multilingual-evaluation.qmd` et version EN | Déplacé vers l'approfondissement empirique |
| Jour 3 — Tokenizer | Mécanismes détaillés WordPiece et Unigram | `site/fr/tokenization-strategies.qmd` et version EN, ancre FR `#mecanismes-wordpiece-unigramme`, EN `#wordpiece-unigram-mechanisms` | Conservé dans la page canonique des mécanismes |
| Jour 3 — Tokenizer | Sonde Python d'inspection d'un tokenizer Hugging Face | `site/fr/exercises-text-data.qmd` et version EN, ancre `#tokenizer-huggingface-probe` | Déplacé vers Practice |
| Jour 3 — Tokenizer | Comparaison du coût de vocabulaire, des longueurs, des paramètres et de la projection de sortie | `tokenizer-design-evaluation.qmd` | Conservé et renforcé dans l'histoire centrale |

## Vérifications de destination

### Jour 1 — Zipf

Le récit central conserve le corpus jouet, les conventions de comptage, la relation rang–fréquence, une interprétation accessible et les limites de l'exemple. L'approfondissement récupère les développements trop longs pour le récit : variante de Mandelbrot, données comparatives, histoire, applications et bibliographie.

Le contenu est bien complémentaire et non une seconde version du récit. L'approfondissement renvoie vers l'histoire centrale ; l'histoire renvoie vers les sections spécialisées lorsqu'elles sont pertinentes.

Correction de classement : les deux pages Zipf FR/EN utilisent désormais le domaine éditorial `text-tokenization`, dont la portée est explicitée comme incluant les statistiques de corpus, la représentation du texte et la conception des tokenizers. Ce choix classe le sujet dans le domaine du texte et des données linguistiques ; il ne prétend pas que Zipf est un mécanisme de tokenisation.

### Jour 2 — Surprisal

Aucun dossier théorique séparé n'a été nécessaire : les développements supplémentaires améliorent directement l'histoire et restent dans son périmètre. Les manipulations et essais interactifs relèvent de Practice. Le déplacement du texte d'expérimentation vers une page dédiée ne constitue donc pas une suppression de contenu.

### Jour 3 — Tokenizer

La séparation est cohérente avec les responsabilités éditoriales :
- mécanismes algorithmiques dans `tokenization-strategies` ;
- décision de conception et compromis système dans `tokenizer-design-evaluation` ;
- résultats empiriques, comparaisons multilingues et métriques dans `tokenizer-multilingual-evaluation` ;
- code d'inspection reproductible et manipulation dans Practice.

## Corrections d'information et de navigation

L'audit a mis en évidence trois défauts de découverte, maintenant corrigés dans la branche associée :

1. `zipf-law-deep-dive` était placé dans « Formalisation probabiliste et chaîne de l'entraînement » dans `site/_quarto.yml`. Il est déplacé sous « Texte, corpus et tokenisation » → « Statistiques du langage ».
2. Les deux approfondissements compagnons étaient absents de la carte éditoriale `deepen.qmd`, bien qu'ils soient rendus et présents dans le menu. Ils sont désormais reliés explicitement à leurs histoires et à leurs domaines.
3. Le domaine de page des deux pages Zipf était `probabilistic-foundations-training`. Il est corrigé en `text-tokenization`, en FR et EN ; la définition de ce domaine inclut maintenant les statistiques de corpus.
4. Les pages `post-training`, `transformer-architectures` et `llm-limits` sont des leçons Understand, pas des approfondissements : elles sont retirées de la navigation latérale Deepen et restent accessibles comme leçons fondamentales associées depuis la carte (post-training et architectures Transformer) ou comme point d'entrée critique pour la rubrique Échelle (`llm-limits`). `universal-artificial-intelligence`, dont le domaine est `mathematical-tools-geometry`, est replacée dans la rubrique des outils mathématiques.

La nouvelle rubrique **Modélisation du langage** regroupe les sous-domaines suivants :
- attention, position et architectures ;
- texte, corpus et tokenisation ;
- formalisation probabiliste et chaîne de l'entraînement ;
- inférence et efficacité ;
- échelle et questions de recherche.

Les outils mathématiques et la géométrie restent séparés. La rubrique est une taxonomie de découverte : elle ne définit ni ordre de lecture, ni prérequis, ni graphe computationnel.

## Contrat de navigation après redistribution

Une porte du calendrier continue de mener à **une seule histoire centrale**. Le lien vers un approfondissement compagnon est facultatif : il ne crée pas une seconde porte, ne rallonge pas la durée annoncée de l'histoire et ne devient pas un prérequis.

La rubrique **Modélisation du langage** est la collection permanente qui rend ces contenus trouvables toute l'année. Elle expose ensemble les histoires du calendrier et leurs approfondissements lorsqu'ils partagent un domaine, tout en distinguant explicitement le récit central, le dossier avancé et la pratique. Les pages hors calendrier y sont classées selon leur question durable, sans devoir être artificiellement converties en histoires de quinze minutes.

## Limites de l'audit

- L'audit couvre les changements de contenu des trois premières histoires dans la PR #1695 ; il ne certifie pas la qualité scientifique complète de toutes les pages de destination.
- Les pages Practice sont vérifiées comme destinations éditoriales, mais l'audit ne remplace pas une revue de leurs interactions et de leur rendu.
- La cohérence source FR/EN et les liens locaux doivent encore être confirmés par les contrôles automatisés et le rendu Quarto de la PR qui porte ces corrections.

## Fichiers et références

- [PR #1695 — redistribution des trois premières histoires](https://github.com/JM-Brun/llm-lab/pull/1695)
- [Manifeste canonique du calendrier](../../data/calendars/advent-2026.yml)
- [Carte Approfondir FR](../../site/fr/deepen.qmd) · [EN](../../site/en/deepen.qmd)
- [Carte éditoriale du calendrier](../advent-calendar-editorial-redesign.md)
- [Passation — travaux restants sur Modélisation du langage et Approfondir](language-modeling-deepen-follow-up-2026-11-26.md)


## Passation — prochaine session dédiée au jour 1

**État au 2026-11-26, après la redistribution et l'audit des destinations.** Cette section est le point de reprise opérationnel ; elle évite de refaire les arbitrages déjà intégrés.

### État acquis — ne pas recommencer

- [x] Le récit Zipf a été ramené à une histoire d'environ 15 minutes dans la redistribution portée par [PR #1695](https://github.com/JM-Brun/llm-lab/pull/1695) : corpus jouet, unités, rang–fréquence, intuition log-log, limites et lien prudent aux LLM.
- [x] Les développements avancés ont été conservés dans les pages bilingues `zipf-law-deep-dive.qmd` : Zipf–Mandelbrot, paramètres et comparaison des courbes, observations multilingues et précautions, histoire, applications étendues et bibliographie complémentaire.
- [x] Les exercices et expériences restent dans les pages Practice dédiées ; le récit conserve un seul lien discret vers l'auto-vérification.
- [x] [PR #1703](https://github.com/JM-Brun/llm-lab/pull/1703) aligne le sous-titre, les descriptions FR/EN, la promesse du calendrier et la formulation sur l'exposition aux données d'entraînement. Il précise qu'une fréquence plus élevée donne davantage d'occasions d'observation à corpus et tokenizer fixés, sans garantir une meilleure représentation ni de meilleures performances.
- [x] Les comptes du corpus jouet et les conventions de comptage ont été vérifiés dans le suivi #1653 ; ne pas les recalculer sans modification du texte ou de la convention.
- [x] L'audit de redistribution n'a identifié aucune perte de contenu matériel : les éléments déplacés ont des destinations identifiées dans la matrice ci-dessus.
- [x] La correction de découvrabilité et de classement est préparée dans [PR #1707](https://github.com/JM-Brun/llm-lab/pull/1707) : rubrique « Modélisation du langage », rattachement des deux approfondissements compagnons, correction du domaine Zipf en `text-tokenization` et alignement de la carte Deepen avec la navigation.

### État non acquis — ne pas présenter comme validé

- [ ] La PR #1707 est encore ouverte au moment de cette mise à jour. Les contrôles Python/domain, le secret scanning et le rendu Quarto complet avec audit navigateur ont réussi. En revanche, la suite CI échoue sur 6 tests (828 réussis, 1 ignoré) : deux assertions FR/EN attendent encore `transformer-architectures` dans Approfondir, et quatre contrôles signalent des artefacts de carte bilingues périmés. L'arbitrage éditorial/test et la régénération des artefacts sont documentés dans [la passation des travaux restants](language-modeling-deepen-follow-up-2026-11-26.md). Ne pas fusionner avant résolution et nouvelle validation complète.
- [ ] La disponibilité publique d'une page ne vaut pas acceptation éditoriale.
- [ ] Aucune lecture novice chronométrée n'est documentée comme réalisée.
- [ ] Le rendu visuel final des pages Zipf après déploiement n'est pas validé par cette matrice de destinations. L'audit source-level ne remplace pas l'inspection HTML réelle.

### Prochaine session — ordre recommandé

1. **Établir le bon état GitHub.** Vérifier si #1707 a été fusionnée, quel commit est déployé et si les pages FR/EN de l'histoire et de l'approfondissement sont celles de ce commit. Ne pas créer une PR concurrente sur les mêmes fichiers.
2. **Inspecter le rendu publié, FR puis EN.** Contrôler desktop et mobile : titre/sous-titre, temps annoncé, formules, tableaux, figures et textes alternatifs, ancres, navigation, liens vers l'approfondissement et Practice, sélecteur de langue. Vérifier en particulier que la rubrique Deepen permet de retrouver l'histoire et son compagnon sans suggérer un parcours obligatoire.
3. **Faire une lecture novice chronométrée.** Utiliser une personne qui ne connaît pas Zipf ; ne pas lui expliquer le contenu avant la lecture. Noter temps réel, retours en arrière, passages relus et questions spontanées. À la fin, demander sans aide :
   - Quelle est l'unité comptée dans le corpus jouet ? Que distinguent occurrence, type lexical et token de tokenizer ?
   - Que signifie le rang et que décrit la relation rang–fréquence ?
   - Que permet de lire la représentation log-log, et que ne prouve pas une droite apparente ?
   - Quelle différence entre fréquence marginale dans un corpus et probabilité conditionnelle du prochain token ?
   - Quelles conclusions l'exemple autorise-t-il, et lesquelles nécessitent un corpus/une analyse plus solides ?
   - Où trouver les développements mathématiques et les expériences facultatives ?
4. **Corriger à partir des difficultés observées, pas par ajout préventif.** Si le lecteur échoue sur les unités, reprendre l'exemple suivi ; sur le rang/exposant, reprendre la transition graphique ; sur le lien LLM, reprendre l'exemple contextuel. Éviter d'ajouter à nouveau Zipf–Mandelbrot, les comparaisons multilingues ou l'histoire au récit principal : ces contenus ont déjà une destination.
5. **Faire une revue scientifique ciblée.** Vérifier les formulations qui pourraient transformer une régularité descriptive en loi universelle ou mécanisme causal, les dénominateurs et unités des chiffres cités, la séparation entre résultats empiriques et courbes synthétiques, et les affirmations sur les LLM. Revenir aux sources primaires uniquement pour les points litigieux ou insuffisamment localisés.
6. **Décider explicitement l'acceptation de #1653.** Clore uniquement lorsque la cohérence FR/EN, le rendu publié, les liens, la revue scientifique ciblée et le test novice sont documentés. Si des tâches distinctes subsistent, les créer dans leurs issues propriétaires plutôt que d'élargir indéfiniment le récit.

### Hors périmètre de cette reprise

- Le laboratoire reproductible ELTeC, l'extraction TEI, l'estimation, les incertitudes et le rééchantillonnage restent suivis dans [#1605](https://github.com/JM-Brun/llm-lab/issues/1605).
- Les ramifications théoriques ne doivent être créées que si elles sont autonomes et sourcées ; la liste des candidates dans #1653 est une possibilité, pas un engagement de création.
- Ne pas ajouter de nouvelles cartes de concepts pour chaque paramètre ou mesure. Réutiliser les concepts canoniques existants et distinguer graphe de connaissances, graphe computationnel et progression pédagogique.
- Ne pas réintroduire dans l'histoire principale le contenu déplacé uniquement pour augmenter sa longueur. La cible est une lecture claire et autonome d'environ 15 minutes, pas un quota de mots.

### Point d'entrée pour la prochaine session

Commencer par [#1653 — suivi éditorial du jour 1](https://github.com/JM-Brun/llm-lab/issues/1653), vérifier [#1707 — organisation de Deepen](https://github.com/JM-Brun/llm-lab/pull/1707), puis suivre la séquence « rendu publié → lecture novice → corrections fondées sur observation → acceptation ». La présente passation décrit le travail restant ; elle ne constitue pas une validation finale.
