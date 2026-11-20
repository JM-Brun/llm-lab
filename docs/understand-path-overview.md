# Parcours « Comprendre les LLM » — synthèse et audit de navigation

**Statut :** note d'audit éditorial et proposition d'évolution  
**Date :** 2026-11-13  
**Périmètre :** point d'entrée français, panorama LLM, navigation latérale, parcours guidé et carte des ressources.

Cette note est fondée sur les sources du dépôt : `site/index.qmd`, `site/fr/learning-map.qmd`, `site/fr/llm-overview.qmd`, `site/fr/generation.qmd`, `data/guided-route.yml`, `docs/learning-path.md`, `docs/content-section-mapping.md` et `docs/information-architecture.md`. Il s'agit d'un audit éditorial des sources, pas encore d'une validation visuelle desktop/mobile ou d'un test utilisateur.

## État et travail restant au 21 novembre 2026

Le [registre du parcours](../data/guided-route.yml) porte les neuf étapes, les notions mobilisées et les objectifs des leçons. La [carte](../site/fr/learning-map.qmd#conceptual-route) présente le squelette global. Le [plan de révision](../site/fr/review-path.qmd) affiche la question et le résultat de chaque étape, puis ouvre l’écriture formelle à la demande. Depuis [Choisir une approche](../site/fr/llm-overview.qmd#choosing-an-approach), la comparaison issue de [#1455](https://github.com/JM-Brun/llm-lab/pull/1455) permet de suivre ce qui arrive au contexte et aux paramètres pendant les quatre opérations.

Les exercices sur l’entrée positionnelle et les deux axes de softmax sont intégrés via [#1452](https://github.com/JM-Brun/llm-lab/pull/1452). Les PR [#1453](https://github.com/JM-Brun/llm-lab/pull/1453) et [#1454](https://github.com/JM-Brun/llm-lab/pull/1454) sont en revue. La première ajoute la projection des états finaux vers les logits et le choix de la dernière ligne. La seconde ajoute les retours du corrigé vers les étapes concernées. Elles peuvent être intégrées dans l’un ou l’autre ordre.

| Priorité | Lot | Critère de validation |
|---|---|---|
| P0 | Terminer la revue de #1453 et #1454 | Les deux exercices de la page Logits coexistent en FR et EN. Les exercices de #1452 conservent leurs ancres. Les tests de la carte, du plan et des liens passent sur les deux changements réunis. |
| P0 | Compléter l’aller-retour du nouvel exercice | Une fois #1453 et #1454 intégrées, inclure les retours générés sous les deux corrigés de `ex-final-state-to-next-token`, puis retirer son exception dans le test. Dans le HTML, les étapes Calcul et Prédiction mènent au même exercice et le corrigé renvoie vers les deux étapes. |
| P1 | Vérifier les démarches du lecteur en FR et EN | Tester les trajets Panorama → comparaison → étape, carte → leçon → fiche, et plan → exercice → retour sur écran étroit et au clavier. Vérifier la visibilité de la cible, l’ordre du focus et le repli des formules. Consigner les étapes de reproduction des problèmes observés. |
| P1 | Revoir les énoncés formels à leur périmètre exact | Réexaminer d’abord trois cas sensibles. L’addition `E + P` décrit un mécanisme de position particulier. La normalisation d’attention porte sur les clés accessibles et celle de sortie sur le vocabulaire. Le calcul du gradient précède le pas qui modifie les paramètres. Pour chaque cas, retrouver l’explication canonique et une vérification existante ou préciser ce qui manque. |
| P2 | Tester le transfert entre les quatre opérations | Essayer un cas commun issu du fil du scribe en variant une décision à la fois. Demander au lecteur de nommer le préfixe, la cible éventuelle, la valeur lue et ce qui est modifié. Réutiliser un exercice existant s’il couvre déjà ces décisions. Observer les réponses avant de décider si un nouvel exercice est utile. |

Les sections d’audit ci-dessous conservent les propositions de la revue initiale. Le tableau ci-dessus indique les travaux à reprendre en priorité.

## 1. Ce que le parcours doit faire comprendre

Le parcours doit construire une représentation mentale progressive du système, et non faire mémoriser une liste de composants. À son terme, le lecteur doit pouvoir expliquer :

1. ce qu'est un LLM et ce que signifie prédire le prochain token ;
2. comment un texte devient une entrée exploitable par le modèle ;
3. comment cette entrée devient une représentation numérique puis contextuelle ;
4. comment le Transformer transforme ces représentations ;
5. comment le calcul aboutit à une distribution de probabilité sur le prochain token ;
6. comment le modèle exploite les instructions et exemples du contexte sans mise à jour des paramètres, et comment le système prépare ce contexte ;
7. ce que l'on peut faire de la distribution : générer, scorer une cible observée ou apprendre en ajustant les paramètres.

Le fil directeur est une question : **comment un modèle transforme-t-il un contexte en prédiction, et comment cette prédiction est-elle utilisée ?**

Trois représentations doivent rester distinctes :

- **Parcours pédagogique :** dans quel ordre est-il préférable d'apprendre ?
- **Graphe de connaissances :** quels concepts sont reliés, et par quelles relations ?
- **Graphe computationnel :** quelles opérations le modèle réalise-t-il et comment s'enchaînent-elles ?

Le parcours est une projection pédagogique des connaissances, pas une transcription de l'architecture technique. La génération, le scoring et l'apprentissage partagent un calcul prédictif, mais sont trois usages distincts et non trois étapes d'une seule boucle d'exécution.

## 2. Le parcours simplifié à présenter au lecteur

Cette synthèse en six mouvements est la couche d'orientation. Elle ne remplace pas les neuf étapes canoniques de `data/guided-route.yml`.

### 1 — Situer : qu'est-ce qu'un LLM ?

Un LLM exploite un contexte pour attribuer des probabilités aux continuations possibles. Le projet prend le GPT autorégressif comme exemple concret, sans prétendre que tous les LLM ont la même architecture ou le même objectif.

**À retenir :** LLM, GPT et Transformer ne sont pas synonymes ; architecture, apprentissage des paramètres et utilisation du modèle sont trois questions différentes.

Page : [Panorama : qu'est-ce qu'un LLM ?](../site/fr/llm-overview.qmd).

### 2 — Observer : comment produit-il du texte ?

Suivre d'abord une génération complète comme une boîte noire :

`contexte → distribution du prochain token → sélection → nouveau contexte → répétition`

Le modèle calcule une distribution ; une règle de décodage sélectionne un token ; le token est réinjecté dans le contexte. Les paramètres restent fixes pendant l'inférence ordinaire.

Page : [Générer du texte](../site/fr/generation.qmd), d'abord comme aperçu du système.

### 3 — Expliquer le calcul : que reçoit et que calcule le modèle ?

Ouvrir progressivement la boîte en quatre mouvements :

- **Texte → tokens → identifiants :** le texte est segmenté et représenté par des IDs.
- **Identifiants → représentations :** les IDs donnent accès à des vecteurs ; l'information positionnelle est ajoutée ; les couches produisent des représentations contextualisées.
- **Transformer les représentations :** les blocs Transformer appliquent notamment les projections Q/K/V, l'attention, le masque causal, les connexions résiduelles, la normalisation et les MLP.
- **États → prédiction :** les états finaux sont projetés en logits puis en distribution de probabilité sur le vocabulaire.

**Point de vigilance :** Q/K/V sont calculés à l'intérieur de chaque bloc Transformer, à partir de ses états d'entrée. Ils ne viennent pas après les représentations contextualisées finales.

Pages centrales : [Texte et données](../site/fr/text-data.qmd), [Embeddings](../site/fr/embedding-space.qmd), [Représentations contextualisées](../site/fr/contextualized-representations.qmd), [Transformer](../site/fr/transformer.qmd), [Q/K/V](../site/fr/queries-keys-values.qmd), [Attention](../site/fr/scaled-dot-product-attention.qmd), [Masque causal](../site/fr/causal-masking.qmd), [Logits](../site/fr/logits.qmd), [Probabilités](../site/fr/probabilites.qmd).

### 4 — Concevoir et exploiter le contexte : que fournit-on au modèle ?

L'**apprentissage en contexte** (*in-context learning*, ICL) décrit comment le modèle adapte ses réponses aux instructions et démonstrations présentes dans son contexte, sans mettre à jour ses paramètres. L'**ingénierie du contexte** (*context engineering*) désigne le travail du système qui sélectionne, récupère, structure, actualise et sécurise les informations transmises au modèle.

Ces notions sont liées mais différentes : ICL décrit un comportement du modèle ; context engineering décrit une pratique de conception du système. Le prompt engineering en est une partie, tandis que RAG et mémoire sont des mécanismes qui peuvent alimenter le contexte sans se confondre avec lui.

Pages centrales : [Apprentissage en contexte](../site/fr/in-context-learning.qmd), [Ingénierie du contexte](../site/fr/context-engineering.qmd). Exercices : [ICL](../site/fr/exercises/in-context-learning.qmd), [context engineering](../site/fr/exercises/context-engineering.qmd).

### 5 — Comprendre les usages : que fait-on de la prédiction ?

La distribution prédictive ouvre trois branches sœurs :

- **Générer :** sélectionner un token, l'ajouter au contexte et recommencer. Le *prefill* traite le prompt initial ; le *decode* poursuit la génération token par token.
- **Scorer :** mesurer la probabilité attribuée à un token ou à une séquence observée, sans sélectionner de token et sans mettre à jour les paramètres.
- **Apprendre :** comparer les prédictions aux cibles observées, agréger une loss, calculer des gradients et mettre à jour les paramètres. Le *teacher forcing* utilise le préfixe observé ; il ne désigne pas le *prefill*.

L'évaluation est transversale : elle mesure le comportement du modèle sur des données et selon un protocole définis. Ce n'est pas une quatrième branche d'exécution.

Pages centrales : [Génération](../site/fr/generation.qmd), [Vraisemblance](../site/fr/vraisemblance.qmd), [Cross-entropie](../site/fr/cross-entropy.qmd), [Loss](../site/fr/loss.qmd), [Gradients](../site/fr/gradients.qmd), [Évaluation expérimentale](../site/fr/evaluation-experimentale.qmd).

### 6 — Explorer selon son besoin

Après cette vue d'ensemble, le lecteur choisit librement :

- **Construire :** implémenter et vérifier un petit GPT avec le parcours Build indépendant ;
- **Pratiquer :** exercices, calculs, manipulations et expériences ;
- **Approfondir :** dérivations, géométrie, variantes d'attention, architectures et limites ;
- **Consulter :** glossaire, histoire et références.

Ces destinations complètent le parcours sans devenir des étapes obligatoires supplémentaires.

### Schéma de synthèse

```text
COMPRENDRE UN LLM

Situer le système
      ↓
Observer une génération complète (boîte noire)
      ↓
Expliquer le calcul
Texte → tokens → représentations → Transformer → distribution
      ↓
Concevoir et exploiter le contexte
      ├── ICL : exploiter les exemples sans mise à jour des paramètres
      └── Context engineering : préparer et gérer les informations
      ↓
Comprendre les usages de la prédiction
      ├── Générer : sélectionner et réinjecter
      ├── Scorer : évaluer une cible observée
      └── Apprendre : loss → gradients → paramètres
      ↓
Explorer : construire · pratiquer · approfondir · consulter
```

Ce schéma est un résumé de lecture. Il ne remplace ni le registre des neuf étapes, ni le graphe computationnel, ni la carte des concepts.

## 3. Audit de l'existant

### Points solides

- Le point d'entrée distingue déjà les deux parcours principaux et indépendants : Understand et Build.
- Le panorama commence par le système global et distingue LLM, GPT et Transformer.
- La génération est volontairement présentée tôt comme aperçu « boîte noire », puis reprise plus en détail. Cette répétition a une justification pédagogique : voir le phénomène avant d'en étudier les mécanismes.
- Le parcours guidé distingue le calcul prédictif des usages génération, scoring et apprentissage.
- `guided-route.yml` centralise les neuf étapes et leurs objectifs bilingues ; les pages facultatives ne sont pas des prérequis.
- La carte distingue pages, concepts et relations, au lieu de réduire tout le contenu à une arborescence unique.
- Build, Practice et Deepen ont des destinations distinctes.

### Frictions observées dans les sources

1. **La carte cumule plusieurs fonctions.** Elle présente le parcours guidé, les territoires, rubriques, pages, notions canoniques, filtres et vues interactives. C'est utile pour explorer, mais beaucoup à traiter pour quelqu'un qui veut seulement savoir par où commencer.
2. **La vue courte n'est pas assez immédiatement distincte de la vue exhaustive.** Neuf étapes et la carte détaillée arrivent rapidement, alors que le lecteur a d'abord besoin de retenir quelques idées structurantes.
3. **La double présence de la génération peut sembler redondante.** Son rôle d'aperçu puis de reprise détaillée doit être explicitement annoncé.
4. **La navigation latérale est profonde.** Les sous-sections aident à retrouver les pages, mais peuvent faire croire que chaque page est un chapitre obligatoire ou que l'arborescence représente exactement le calcul.
5. **Les étapes détaillées mélangent plusieurs granularités.** Les neuf étapes conviennent au guidage, mais les intitulés de haut niveau doivent rester formulés en questions et résultats compréhensibles.
6. **Les branches scoring et apprentissage sont moins visibles dans la navigation que la chaîne de calcul.** Leur distinction mérite d'être présentée dans une synthèse simple, sans les transformer en étapes de génération.
7. **La carte et la sidebar peuvent être prises pour deux parcours concurrents.** Leur rôle respectif doit être rappelé au point de choix.

## 4. Améliorations proposées

### P0 — Clarifier l'orientation, sans changer le curriculum

1. Ajouter au début de la page « Parcours guidé et carte des ressources » la synthèse en cinq mouvements : Situer, Observer, Expliquer le calcul, Comprendre les usages, Explorer.
2. Présenter les trois grandes questions : qu'est-ce qu'un LLM ? comment calcule-t-il une prédiction ? que fait-on de cette prédiction ?
3. Expliciter la double fonction de la page Génération : **aperçu du système** après le panorama, puis **explication détaillée** à l'étape inférence.
4. Rappeler que la sidebar sert à retrouver les ressources, le parcours guidé à proposer un ordre de lecture, et la carte à explorer les relations.

### P1 — Réduire la charge cognitive de la carte

1. Faire apparaître la synthèse courte avant les étapes détaillées, puis les vues exploratoires.
2. Conserver les vues Territoires / Rubriques / Pages / Notions, mais les présenter comme des outils de consultation, pas comme des étapes supplémentaires.
3. Dans les libellés, privilégier les questions et résultats attendus ; garder les inventaires de notions dans les objectifs détaillés ou les pages.
4. Distinguer les ressources centrales et facultatives sans ajouter une nouvelle taxonomie ni un nouveau registre.

### P2 — Harmoniser la navigation et les retours

1. Vérifier que les intitulés de sidebar décrivent des questions ou ensembles cohérents, et non une prétendue séquence exacte des opérations.
2. Ajouter des liens de retour sobres vers la synthèse depuis les pages centrales, sans répéter un gros bloc de navigation partout.
3. Dans les pages génération, scoring et apprentissage, rappeler les trois usages frères avec des liens croisés, sans dupliquer leurs explications.
4. Réaliser une revue visuelle desktop/mobile et clavier de la carte et de la sidebar après les modifications.

## 5. Garde-fous

- Conserver `data/guided-route.yml` comme source des étapes.
- Ne pas fusionner Understand et Build.
- Ne pas transformer la carte des connaissances en séquence linéaire.
- Ne pas faire des pages Deepen des prérequis implicites.
- Ne pas déplacer les explications canoniques dans la page d'orientation : elle doit orienter, pas répéter les leçons.
- Ne pas supprimer les détails, exemples ou références lors d'une simplification de la navigation.
- Ne pas introduire une nouvelle taxonomie si les rôles actuels suffisent.

## 6. Ordre de réalisation

1. Valider la synthèse en cinq mouvements et son vocabulaire.
2. L'intégrer à la page de carte comme couche d'orientation.
3. Ajuster les libellés qui créent une ambiguïté entre aperçu et reprise détaillée de la génération.
4. Vérifier les liens et la parité FR/EN.
5. Effectuer la revue responsive, clavier et lecteur d'écran.
6. Après cette validation seulement, décider si certains intitulés de sidebar doivent être raccourcis ou regroupés.

**Critère de réussite :** un nouveau lecteur doit pouvoir, en moins d'une minute, répondre à « par où commencer ? », décrire le fil général du fonctionnement d'un LLM et comprendre qu'il peut ensuite choisir de construire, pratiquer ou approfondir sans lire toutes les pages.
